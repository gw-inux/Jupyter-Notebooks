"""Conservative transport on a pinboard or an idealized grain network.

Internal length: m; time: s; pressure potential: Pa; flow: m³/s.
Every marker carries 1/N of the prescribed total mass. No Streamlit imports.

CODE MAP — refresh with python scripts/update_code_index.py
  L0039  Config
  L0053  Config.validate
  L0071  Network
  L0088  Run
  L0101  Run.end_time
  L0105  Run.exit_x
  L0110  node_id
  L0114  board_geometry
  L0123  build_network
  L0195  pin_reference
  L0206  network_reference
  L0234  simulate
  L0290  mass_counts
  L0297  positions
  L0314  particle_csv
  L0326  summary
END CODE MAP
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import comb
import csv
import io

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


# 1. Data structures and validation --------------------------------------------
@dataclass(frozen=True)
class Config:
    mode: str = "regular"
    rows: int = 12
    particles: int = 1000
    spacing_mm: float = 1.0
    mean_step_s: float = 1.0
    time_cv: float = 0.6
    injection_s: float = 0.0
    seed: int = 42
    packing: float = 0.75
    grain_variation: float = 0.25
    pressure_pa: float = 0.5
    medium_seed: int = 7

    def validate(self):
        if self.mode not in ("regular", "variable", "grains"):
            raise ValueError("Unknown model mode.")
        for name, lo, hi in (("rows", 2, 40), ("particles", 1, 10010),
                             ("seed", 0, 2**32-1), ("medium_seed", 0, 2**32-1)):
            value = getattr(self, name)
            if not isinstance(value, (int, np.integer)) or not lo <= value <= hi:
                raise ValueError(f"{name} must be an integer in [{lo}, {hi}].")
        for name, lo, hi in (("spacing_mm", .2, 3.), ("mean_step_s", .1, 10.),
                             ("time_cv", 0., 1.5), ("injection_s", 0., 1000.),
                             ("packing", .5, .9), ("grain_variation", 0., .4),
                             ("pressure_pa", .05, 2.)):
            value = getattr(self, name)
            if not np.isfinite(value) or not lo <= value <= hi:
                raise ValueError(f"{name} must be finite and in [{lo}, {hi}].")


@dataclass
class Network:
    xy: np.ndarray
    edges: np.ndarray
    outlets: np.ndarray
    grains: np.ndarray      # x, flowwise coordinate, radius (m)
    radii: np.ndarray      # equivalent cylindrical throat radii (m)
    pressure: np.ndarray
    flow: np.ndarray       # signed, in the original edge orientation
    outgoing: list         # each entry: (destination, probability, transit time)
    inlet_flow: float
    residual: float        # maximum relative nodal residual
    imbalance: float       # relative inlet/outlet imbalance
    max_reynolds: float
    volume: float


@dataclass
class Run:
    config: Config
    xy: np.ndarray
    edges: np.ndarray
    paths: np.ndarray      # node ids; final node repeated in unused columns
    times: np.ndarray      # arrival time at node; unused columns = +inf
    release: np.ndarray
    arrival: np.ndarray
    exit_nodes: np.ndarray
    network: Network | None
    reference: dict

    @property
    def end_time(self):
        return float(self.arrival.max())

    @property
    def exit_x(self):
        return self.xy[self.exit_nodes, 0]


# 2. Geometry and hydraulic network -------------------------------------------
def node_id(row: int, column: int) -> int:
    return row * (row + 1) // 2 + column


def board_geometry(rows: int, spacing_m: float):
    xy = np.array([((2*k-r)*spacing_m, r*spacing_m)
                   for r in range(rows+1) for k in range(r+1)])
    edges = np.array([(node_id(r, k), node_id(r+1, k+d))
                      for r in range(rows) for k in range(r+1) for d in (0, 1)])
    outlets = np.arange(node_id(rows, 0), node_id(rows, rows)+1)
    return xy, edges, outlets


def build_network(c: Config) -> Network:
    """Solve steady incompressible flow with one inlet and equal-pressure outlets.

    Grain centres form the dual lattice. Adjacent grains flank every edge.
    Their surface gap defines the DIAMETER of a cylindrical throat surrogate.
    Pore-body resistance/storage and sub-throat velocity profiles are omitted.
    The plot coordinate is flowwise distance, not gravitational elevation.
    """
    c.validate()
    a = c.spacing_mm * 1e-3
    xy, edges, outlets = board_geometry(c.rows, a)
    grain_ids, grain_list = {}, []
    rng = np.random.default_rng([c.medium_seed, 0])
    for r in range(c.rows+1):
        for k in range(-1, r+1):
            grain_ids[(r, k)] = len(grain_list)
            radius = a/np.sqrt(2) * c.packing * (1-c.grain_variation*rng.random())
            grain_list.append(((2*k-r+1)*a, r*a, radius))
    grains = np.asarray(grain_list)
    radii = []
    for r in range(c.rows):
        for k in range(r+1):
            # left then right, in exactly the board_geometry edge order
            for g1, g2 in (((r, k-1), (r+1, k)), ((r, k), (r+1, k))):
                radii.append((np.sqrt(2)*a - grains[grain_ids[g1], 2]
                              - grains[grain_ids[g2], 2]) / 2)
    radii = np.asarray(radii)
    length = np.linalg.norm(xy[edges[:, 1]] - xy[edges[:, 0]], axis=1)
    viscosity = 1e-3  # Pa s; fixed illustrative water property
    conductance = np.pi*radii**4 / (8*viscosity*length)
    # Normalize only the linear system to improve numerical scaling.
    g = conductance / conductance.max()
    i, j = edges.T
    matrix = coo_matrix((np.r_[g, g, -g, -g],
                        (np.r_[i, j, i, j], np.r_[i, j, j, i])),
                       shape=(len(xy), len(xy))).tocsr()
    fixed = np.r_[0, outlets]
    free = np.setdiff1d(np.arange(len(xy)), fixed)
    pressure = np.zeros(len(xy))
    pressure[0] = c.pressure_pa
    pressure[free] = spsolve(matrix[free][:, free],
                             -matrix[free][:, fixed] @ pressure[fixed])
    flow = conductance * (pressure[i]-pressure[j])
    balance = np.bincount(i, weights=flow, minlength=len(xy))
    balance -= np.bincount(j, weights=flow, minlength=len(xy))
    qin = float(balance[0])
    if not qin > 0 or not np.all(np.isfinite(pressure)):
        raise ValueError("The hydraulic network did not produce a valid inlet flow.")
    outgoing = [[] for _ in xy]
    for e, (u, v) in enumerate(edges):
        if flow[e] == 0:
            continue
        if flow[e] < 0:
            u, v = v, u
        q = abs(flow[e])
        transit = np.pi*radii[e]**2 * length[e] / q
        outgoing[u].append((int(v), q, transit))
    for u, branches in enumerate(outgoing):
        total = sum(b[1] for b in branches)
        outgoing[u] = [(v, q/total, dt) for v, q, dt in branches]
    speed = np.abs(flow) / (np.pi*radii**2)
    residual = float(np.max(np.abs(balance[free])) / qin)
    imbalance = float(abs(qin + balance[outlets].sum()) / qin)
    if max(residual, imbalance) > 1e-8:
        raise ValueError("Hydraulic mass balance exceeds the verification tolerance.")
    return Network(xy, edges, outlets, grains, radii, pressure, flow, outgoing,
                   qin, residual, imbalance,
                   float(np.max(1000*speed*2*radii/viscosity)),
                   float(np.sum(np.pi*radii[flow != 0]**2*length[flow != 0])))


# 3. Exact reference statistics ------------------------------------------------
def pin_reference(c: Config) -> dict:
    prob = np.array([comb(c.rows, k)/2**c.rows for k in range(c.rows+1)])
    cv = c.time_cv if c.mode == "variable" else 0.
    return {"outlet_probability": prob, "mean_x": 0.,
            "variance_x": c.rows*(c.spacing_mm*1e-3)**2,
            "mean_transit": c.rows*c.mean_step_s,
            "variance_transit": c.rows*(c.mean_step_s*cv)**2,
            "mean_arrival": c.rows*c.mean_step_s+c.injection_s/2,
            "variance_arrival": c.rows*(c.mean_step_s*cv)**2+c.injection_s**2/12}


def network_reference(net: Network, injection_s: float = 0.) -> dict:
    """Exact moments of the finite flow-directed graph, independent of particles.

    Strictly falling pressure prevents cycles, including locally upward flow.
    """
    size = len(net.xy)
    mean, second, reach = np.zeros(size), np.zeros(size), np.zeros(size)
    order = np.argsort(net.pressure)
    for u in order:
        for v, p, dt in net.outgoing[u]:
            mean[u] += p*(dt+mean[v])
            second[u] += p*(dt*dt+2*dt*mean[v]+second[v])
    reach[0] = 1.
    for u in order[::-1]:
        for v, p, _ in net.outgoing[u]:
            reach[v] += reach[u]*p
    probability = reach[net.outlets]
    x = net.xy[net.outlets, 0]
    mean_x = float(probability @ x)
    variance = max(0., float(second[0]-mean[0]**2))
    return {"outlet_probability": probability, "mean_x": mean_x,
            "variance_x": float(probability @ (x-mean_x)**2),
            "mean_transit": float(mean[0]), "variance_transit": variance,
            "mean_arrival": float(mean[0]+injection_s/2),
            "variance_arrival": variance+injection_s**2/12}


# 4. Particle experiments ------------------------------------------------------
def simulate(c: Config) -> Run:
    c.validate()
    route_rng = np.random.default_rng([c.seed, 1])
    time_rng = np.random.default_rng([c.seed, 2])
    release_rng = np.random.default_rng([c.seed, 3])
    release = release_rng.uniform(0, c.injection_s, c.particles)
    if c.mode != "grains":
        xy, edges, outlets = board_geometry(c.rows, c.spacing_mm*1e-3)
        right = route_rng.integers(0, 2, size=(c.particles, c.rows))
        columns = np.column_stack((np.zeros(c.particles, dtype=int),
                                   np.cumsum(right, axis=1)))
        row = np.arange(c.rows+1)
        paths = row*(row+1)//2 + columns
        if c.mode == "variable" and c.time_cv > 0:
            sigma = np.sqrt(np.log1p(c.time_cv**2))
            dt = time_rng.lognormal(np.log(c.mean_step_s)-sigma**2/2,
                                    sigma, size=(c.particles, c.rows))
        else:
            dt = np.full((c.particles, c.rows), c.mean_step_s)
        times = release[:, None]+np.column_stack((np.zeros(c.particles),
                                                 np.cumsum(dt, axis=1)))
        return Run(c, xy, edges, paths, times, release, times[:, -1].copy(),
                   paths[:, -1].copy(), None, pin_reference(c))
    net = build_network(c)
    path_list, time_list = [], []
    for start in release:
        u, path, event_times = 0, [0], [float(start)]
        while net.outgoing[u]:
            branches = net.outgoing[u]
            cdf = np.cumsum([b[1] for b in branches])
            index = min(int(np.searchsorted(cdf, route_rng.random(), side="right")),
                        len(branches)-1)
            v, _, dt = branches[index]
            path.append(v)
            event_times.append(event_times[-1]+dt)
            if not net.pressure[v] < net.pressure[u]:
                raise RuntimeError("Particle did not follow decreasing pressure.")
            u = v
        if u not in net.outlets:
            raise RuntimeError("Particle terminated before reaching an outlet.")
        path_list.append(path)
        time_list.append(event_times)
    width = max(map(len, path_list))
    paths = np.empty((c.particles, width), dtype=int)
    times = np.full((c.particles, width), np.inf)
    for p, (path, event_times) in enumerate(zip(path_list, time_list)):
        paths[p, :] = path[-1]
        paths[p, :len(path)] = path
        times[p, :len(path)] = event_times
    return Run(c, net.xy, net.edges, paths, times, release,
               np.array([t[-1] for t in time_list]),
               np.array([p[-1] for p in path_list]), net,
               network_reference(net, c.injection_s))


# 5. Snapshots, accounting, and export -----------------------------------------
def mass_counts(run: Run, time: float) -> tuple[int, int, int]:
    """Not yet injected, within the domain, collected (exhaustive, disjoint)."""
    waiting = int(np.count_nonzero(run.release > time))
    collected = int(np.count_nonzero(run.arrival <= time))
    return waiting, run.config.particles-waiting-collected, collected


def positions(run: Run, time: float, indices=None):
    if indices is None:
        indices = np.arange(run.config.particles)
    indices = np.asarray(indices, dtype=int)
    active = (run.release[indices] <= time) & (time < run.arrival[indices])
    ids = indices[active]
    if not len(ids):
        return ids, np.empty((0, 2))
    step = np.sum(run.times[ids] <= time, axis=1)-1
    step = np.minimum(step, run.times.shape[1]-2)
    t0, t1 = run.times[ids, step], run.times[ids, step+1]
    fraction = (time-t0)/(t1-t0)
    start = run.xy[run.paths[ids, step]]
    finish = run.xy[run.paths[ids, step+1]]
    return ids, start+fraction[:, None]*(finish-start)


def particle_csv(run: Run) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["particle", "mass_fraction", "release_s", "arrival_s",
                     "transit_s", "outlet_x_mm"])
    for i in range(run.config.particles):
        writer.writerow([i+1, 1/run.config.particles, run.release[i],
                         run.arrival[i], run.arrival[i]-run.release[i],
                         run.exit_x[i]*1e3])
    return output.getvalue()


def summary(run: Run) -> dict:
    values = {"config": asdict(run.config), "version": "2.4.0",
              "mean_transit_s": float(np.mean(run.arrival-run.release)),
              "mean_arrival_s": float(np.mean(run.arrival)),
              "std_arrival_s": float(np.std(run.arrival)),
              "mean_exit_x_mm": float(np.mean(run.exit_x)*1e3),
              "std_exit_x_mm": float(np.std(run.exit_x)*1e3),
              "exact_reference": {k: v.tolist() if isinstance(v, np.ndarray) else v
                                  for k, v in run.reference.items()}}
    if run.network is not None:
        values["hydraulics"] = {"inlet_flow_m3_s": run.network.inlet_flow,
                               "relative_nodal_residual": run.network.residual,
                               "relative_flow_imbalance": run.network.imbalance,
                               "max_throat_Re": run.network.max_reynolds}
    return values
