"""Groundwater balance and iteration engine (no Streamlit dependencies).

TABLE OF CONTENTS — search for the numbered section comments below.
  1. Model definition, units and parameter validation
  2. ET branches, saturated thickness and interface fluxes
  3. Picard assembly, residual, Jacobian and scalar functions
  4. Iteration state, closure, accepted steps and failure diagnosis
  5. Independently verified reference and analytical 1D solution
  6. Mehl and grid benchmark factories
  7. Editable teaching presets

Units throughout: m, s, m³/s. Boundary heads are prescribed at cell centres.
Standalone solver defaults are below; app.py passes its UI closure explicitly.
"""

from dataclasses import dataclass, replace
import hashlib
import json
import numpy as np
from scipy.optimize import brentq, least_squares

YEAR = 365.25 * 86400.0
HEAD_TOL = 1e-6
FLOW_TOL = 1e-6
REFERENCE_FLOW_TOL = 1e-12  # Independent true-head verification stays strict.
MAX_STEPS = 120


# 1. Model definition
@dataclass(frozen=True)
class Model:
    conductivity: tuple
    left: float
    right: float
    dx: float = 100.0
    width: float = 1.0
    unconfined: bool = True
    thickness: float = 20.0
    recharge: float = 0.0  # m/s
    et_max: float = 0.0  # m/s over the central cell only
    et_surface: float = 0.5
    et_depth: float = 0.25
    bottom: float = 0.0
    top: float | None = None  # None retains the uncapped Mehl benchmark.
    conductance: str = "harmonic_transmissivity"  # Preserve the Mehl examples.

    @property
    def n(self):
        return len(self.conductivity)

    @property
    def area(self):
        return self.dx * self.width

    def signature(self):
        return hashlib.sha256(
            json.dumps(self.__dict__, sort_keys=True).encode()
        ).hexdigest()[:16]

    def validate(self):
        numbers = list(self.conductivity) + [
            self.left,
            self.right,
            self.dx,
            self.width,
            self.thickness,
            self.recharge,
            self.et_max,
            self.et_surface,
            self.et_depth,
            self.bottom,
        ]
        if self.top is not None:
            numbers.append(self.top)
        if not np.all(np.isfinite(numbers)):
            raise ValueError("nonfinite")
        if (
            self.n < 3
            or min(self.conductivity) <= 0
            or min(self.dx, self.width, self.thickness, self.et_depth) <= 0
        ):
            raise ValueError("parameters")
        if self.recharge < 0 or self.et_max < 0:
            raise ValueError("parameters")
        if self.top is not None and self.top <= self.bottom:
            raise ValueError("parameters")
        if self.unconfined and min(self.left, self.right) <= self.bottom:
            raise ValueError("dry")
        if self.conductance not in ("harmonic_transmissivity", "integrated_thickness"):
            raise ValueError("conductance")


# 2. ET: continuous flux; exact branch slope, including its matrix contribution
def et_terms(model, heads):
    """Return extraction E, dE/dh, intercept b in E = a*h+b, and branch code.
    At a breakpoint select the constant adjacent branch (one-sided derivative).
    ET acts only on the central cell. It is never silently extrapolated.
    """
    h = np.asarray(heads, dtype=float)
    e = np.zeros(model.n)
    a = e.copy()
    b = e.copy()
    i = model.n // 2
    he = model.et_surface - model.et_depth
    emax = model.et_max * model.area
    if emax == 0 or h[i] <= he:
        branch = "off"
    elif h[i] >= model.et_surface:
        e[i] = emax
        b[i] = emax
        branch = "maximum"
    else:
        a[i] = emax / model.et_depth
        b[i] = -a[i] * he
        e[i] = a[i] * h[i] + b[i]
        branch = "linear"
    return e, a, b, branch


def mean_wet_thickness(model, heads):
    """Integral of wet thickness between two heads, divided by their difference.

    Below the roof this is the arithmetic mean thickness. Above it, thickness
    is constant. The mixed branch integrates across the roof exactly, without
    dividing by nearly equal heads or extrapolating thickness above the roof.
    Return the mean and its derivatives with respect to the left/right heads.
    """
    b = np.asarray(heads, dtype=float) - model.bottom
    left, right = b[:-1], b[1:]
    mean = (left + right) / 2
    dl = np.full_like(mean, 0.5)
    dr = np.full_like(mean, 0.5)
    if model.top is None:
        return mean, dl, dr
    roof = model.top - model.bottom
    full = np.minimum(left, right) >= roof
    mean[full], dl[full], dr[full] = roof, 0.0, 0.0
    mixed = (np.minimum(left, right) < roof) & (np.maximum(left, right) > roof)
    if np.any(mixed):
        lower = np.minimum(left[mixed], right[mixed])
        span = np.abs(left[mixed] - right[mixed])
        ratio = (roof - lower) / span
        mean[mixed] = roof - 0.5 * (roof - lower) * ratio
        dlow, dhigh = ratio - 0.5 * ratio**2, 0.5 * ratio**2
        left_is_low = left[mixed] < right[mixed]
        dl[mixed] = np.where(left_is_low, dlow, dhigh)
        dr[mixed] = np.where(left_is_low, dhigh, dlow)
    return mean, dl, dr


def interfaces(model, heads):
    h = np.asarray(heads, dtype=float)
    k = np.asarray(model.conductivity)
    if model.unconfined and np.any(h <= model.bottom):
        raise ValueError("dry")
    factor = model.width / model.dx
    if model.unconfined and model.conductance == "integrated_thickness":
        # Q = K_face*w/dx * [Phi(h_left)-Phi(h_right)], Phi'=wet thickness.
        # Harmonic K retains the resistance of both half-cells. For homogeneous
        # unconfined flow this gives the analytical quadratic h² at grid nodes.
        kface = 2 * k[:-1] * k[1:] / (k[:-1] + k[1:])
        mean, dl, dr = mean_wet_thickness(model, h)
        return kface * factor * mean, kface * factor * dl, kface * factor * dr
    if model.unconfined:
        # At the aquifer roof, choose the saturated (constant-T) derivative.
        wet = h if model.top is None else np.minimum(h, model.top)
        t = k * (wet - model.bottom)
        dt = k if model.top is None else k * (h < model.top)
    else:
        t = k * model.thickness
        dt = np.zeros(model.n)
    a, b = t[:-1], t[1:]
    c = 2 * a * b / (a + b) * factor
    dl = (
        2 * b * b / (a + b) ** 2 * dt[:-1] * factor
        if model.unconfined
        else np.zeros(model.n - 1)
    )
    dr = (
        2 * a * a / (a + b) ** 2 * dt[1:] * factor
        if model.unconfined
        else np.zeros(model.n - 1)
    )
    return c, dl, dr


def fluxes(model, heads):
    """Face flux positive to the right. Interior F = left inflow-right outflow+R-E."""
    h = np.asarray(heads)
    c, _, _ = interfaces(model, h)
    et, _, _, branch = et_terms(model, h)
    faces = c * (h[:-1] - h[1:])
    residual = faces[:-1] - faces[1:] + model.recharge * model.area - et[1:-1]
    return faces, et, residual, branch


# 3. Picard matrix A*h=b; residual F=b-A*h; full Newton Jacobian dF/dh
def assemble(model, heads):
    h = np.asarray(heads, dtype=float)
    c, dl, dr = interfaces(model, h)
    et, ea, eb, _ = et_terms(model, h)
    a = np.diag(c[:-1] + c[1:] + ea[1:-1])
    a += np.diag(-c[1:-1], 1) + np.diag(-c[1:-1], -1)
    b = np.full(model.n - 2, model.recharge * model.area) - eb[1:-1]
    b[0] += c[0] * model.left
    b[-1] += c[-1] * model.right
    f = (
        c[:-1] * (h[:-2] - h[1:-1])
        + c[1:] * (h[2:] - h[1:-1])
        + model.recharge * model.area
        - et[1:-1]
    )
    j = np.diag(
        dr[:-1] * (h[:-2] - h[1:-1])
        - c[:-1]
        + dl[1:] * (h[2:] - h[1:-1])
        - c[1:]
        - ea[1:-1]
    )
    j += np.diag(dl[1:-1] * (h[1:-2] - h[2:-1]) + c[1:-1], -1)
    j += np.diag(dr[1:-1] * (h[2:-1] - h[1:-2]) + c[1:-1], 1)
    return a, b, f, j


def scalar_values(model, h):
    """A genuinely scalar 3-cell problem (also used for selected-cell slices)."""
    heads = np.array([model.left, float(h), model.right])
    a, b, f, j = assemble(model, heads)
    return float(b[0] / a[0, 0]), float(f[0]), float(j[0, 0])


def cell_slice(model, neighbors, cell):
    """Conditional single-cell equation. Cell is zero-based interior index."""
    if not 1 <= cell < model.n - 1:
        raise ValueError("cell")
    return replace(
        model,
        conductivity=tuple(model.conductivity[cell - 1 : cell + 2]),
        left=float(neighbors[cell - 1]),
        right=float(neighbors[cell + 1]),
        et_max=model.et_max if cell == model.n // 2 else 0.0,
    )


# 4. Histories: rejected proposals are recorded, never clipped into the solution
def initial_state(model, initial):
    h = np.asarray(initial, dtype=float).copy()
    h[0] = model.left
    h[-1] = model.right
    return {
        "heads": [h.tolist()],
        "residual": [float(max(abs(assemble(model, h)[2])))],
        "status": "ready",
        "rejected": None,
        "change": None,
        "omega": [],
    }


def refresh_closure(state, head_tol=HEAD_TOL, flow_tol=FLOW_TOL):
    """Reassess a saved iterate without deleting it when closure criteria change."""
    if (
        not np.isfinite(head_tol)
        or not np.isfinite(flow_tol)
        or min(head_tol, flow_tol) <= 0
    ):
        raise ValueError("closure")
    if state["status"] in ("running", "converged"):
        state["status"] = (
            "converged"
            if state["change"] < head_tol and state["residual"][-1] < flow_tol
            else "running"
        )


def iteration_proposal(model, heads, method):
    """One undamped full-system proposal; also used by the coupled-map plots."""
    old = np.asarray(heads, dtype=float)
    a, b, f, j = assemble(model, old)
    proposal = old.copy()
    proposal[1:-1] = (
        np.linalg.solve(a, b)
        if method == "Picard"
        else old[1:-1] + np.linalg.solve(j, -f)
    )
    proposal[0], proposal[-1] = model.left, model.right
    return proposal


def advance(model, state, method, omega=1.0, *, head_tol=HEAD_TOL, flow_tol=FLOW_TOL):
    refresh_closure(state, head_tol, flow_tol)
    if state["status"] not in ("ready", "running"):
        return
    old = np.asarray(state["heads"][-1])
    try:
        proposal = iteration_proposal(model, old, method)
    except np.linalg.LinAlgError:
        state["status"] = "singular"
        return
    new = old + omega * (proposal - old)
    new[0], new[-1] = model.left, model.right
    if not np.all(np.isfinite(new)) or max(abs(new)) > 1e8:
        state["status"] = "diverged"
        state["rejected"] = new.tolist()
        return
    if model.unconfined and min(new) <= model.bottom:
        state["status"] = "dry"
        state["rejected"] = new.tolist()
        return
    residual = float(max(abs(assemble(model, new)[2])))
    change = float(max(abs(new - old)))
    state["heads"].append(new.tolist())
    state["residual"].append(residual)
    state["omega"].append(omega)
    state["change"] = change
    state["status"] = "running"
    if change < head_tol and residual < flow_tol:
        state["status"] = "converged"
    elif len(state["heads"]) >= 4 and max(
        abs(new - np.asarray(state["heads"][-3]))
    ) < min(head_tol, 64 * np.finfo(float).eps * max(1.0, max(abs(new)))):
        # Detect an actual repeated cycle, even if a loose flow test passes.
        # A shrinking cobweb within head_tol is not yet a repeated cycle.
        state["status"] = "cycle"
    elif len(state["heads"]) - 1 >= MAX_STEPS:
        state["status"] = "limit"


# 5. Independent reference, not hidden iterations of the learner's history
def analytical_heads(model, x=None):
    """Homogeneous, steady 1D CHD/recharge benchmark; None when inapplicable.

    L is the distance between prescribed-head cell centres, (n-1)*dx.
    This is the Boundary Conditions module's h² solution, extended above the
    aquifer roof using the Solver Lab's discharge-potential construction.
    It is independent of the conductance choice and is NOT used by iterations.
    """
    if model.et_max or not np.all(
        np.asarray(model.conductivity) == model.conductivity[0]
    ):
        return None
    x = np.arange(model.n) * model.dx if x is None else np.asarray(x, dtype=float)
    length = (model.n - 1) * model.dx
    k = model.conductivity[0]
    recharge_term = model.recharge * x * (length - x) / (2 * k)
    if not model.unconfined:
        return (
            model.left
            + (model.right - model.left) * x / length
            + recharge_term / model.thickness
        )
    roof = np.inf if model.top is None else model.top - model.bottom
    boundary = np.array([model.left, model.right]) - model.bottom
    wet = np.minimum(boundary, roof)
    potential = 0.5 * wet**2 + wet * (boundary - wet)
    phi = potential[0] + (potential[1] - potential[0]) * x / length + recharge_term
    heads = np.sqrt(np.maximum(2 * phi, 0))
    if np.isfinite(roof):
        heads = np.where(phi <= 0.5 * roof**2, heads, phi / roof + 0.5 * roof)
    return model.bottom + heads


def reference(model):
    """Return (heads, verified). Bracket scalar wet roots; bounded least-squares for systems.
    Never present an unconverged optimizer output as a reference solution.
    """
    model.validate()
    linear = np.linspace(model.left, model.right, model.n)
    if model.n == 3:
        lo = model.bottom + 1e-9 if model.unconfined else -1e4
        hi = max(100.0, model.left * 10, model.right * 10, model.et_surface * 10)
        grid = (
            model.bottom + np.geomspace(1e-9, hi - model.bottom, 400)
            if model.unconfined
            else np.linspace(lo, hi, 800)
        )
        grid = np.unique(
            np.r_[grid, model.et_surface, model.et_surface - model.et_depth]
        )
        if model.top is not None:
            grid = np.unique(np.r_[grid, model.top])
        if model.unconfined:
            grid = grid[grid > model.bottom]
        vals = [scalar_values(model, x)[1] for x in grid]
        roots = [float(x) for x, fx in zip(grid, vals) if fx == 0.0]
        for x, y, fx, fy in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
            if fx * fy < 0:
                roots.append(
                    brentq(lambda z: scalar_values(model, z)[1], x, y, xtol=1e-13)
                )
        if not roots:
            return linear, False
        root = min(roots, key=lambda x: abs(x - linear[1]))
        h = np.array([model.left, root, model.right])
        return h, abs(scalar_values(model, root)[1]) < REFERENCE_FLOW_TOL
    if not model.unconfined and model.et_max == 0:
        a, b, _, _ = assemble(model, linear)
        linear[1:-1] = np.linalg.solve(a, b)
        return linear, max(abs(assemble(model, linear)[2])) < REFERENCE_FLOW_TOL
    scale = max(max(abs(assemble(model, linear)[2])), 1e-8)

    def fun(x):
        return assemble(model, np.r_[model.left, x, model.right])[2] / scale

    def jac(x):
        return assemble(model, np.r_[model.left, x, model.right])[3] / scale

    lower = model.bottom + 1e-9 if model.unconfined else -np.inf
    for start in (
        linear[1:-1],
        np.full(model.n - 2, max(model.left, model.right, 1.0)),
    ):
        fit = least_squares(
            fun,
            start,
            jac=jac,
            bounds=(lower, np.inf),
            xtol=1e-13,
            gtol=1e-13,
            ftol=1e-13,
            max_nfev=1500,
        )
        h = np.r_[model.left, fit.x, model.right]
        if max(abs(assemble(model, h)[2])) < REFERENCE_FLOW_TOL:
            return h, True
    return linear, False


# 6. Scenario factories; Mehl values uniformly rescaled to SI, dx = 100 m.
def mehl_model(preset="smooth"):
    if preset == "et":
        return Model(
            tuple(np.array([100.0, 1.0, 0.1]) / 86400),
            2.0,
            0.5,
            et_max=73.05 / 1000 / YEAR,
            et_surface=0.5,
            et_depth=0.25,
        )
    return Model(tuple(np.array([0.005, 0.25, 100.0]) / 86400), 4.0, 0.1)


def mehl_initial_heads(preset="smooth"):
    """Published, method-specific starts shared by the theory and experiment."""
    if preset not in ("smooth", "et"):
        raise ValueError("preset")
    model = mehl_model(preset)
    starts = (0.2, 1.03) if preset == "et" else (0.1, 1.7)
    return {
        method: [model.left, head, model.right]
        for method, head in zip(("Picard", "Newton"), starts)
    }


def grid_model(
    unconfined=False,
    gradient=False,
    heterogeneous=False,
    recharge_mm=150.0,
    zones=(1e-6, 1e-4, 1e-2),
):
    k = (
        (zones[0],) * 5 + (zones[1],) + (zones[2],) * 5
        if heterogeneous
        else (1e-4,) * 11
    )
    return Model(
        k,
        18.0,
        0.1 if gradient else 16.0,
        unconfined=unconfined,
        recharge=recharge_mm / 1000 / YEAR,
    )


# 7. Review-friendly teaching presets; historical Mehl benchmarks remain above.
K_STEPS = (1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3)


def idealized_model(preset="confined"):
    """5 m confined layer below datum, or unconfined aquifer from 0 to 8 m."""
    if preset not in ("confined", "unconfined", "et"):
        raise ValueError("preset")
    return Model(
        (1e-4,) * 3,
        7.0,
        2.0,
        unconfined=preset != "confined",
        thickness=5.0,
        recharge=0.0,
        et_max=1000.0 / 1000 / YEAR if preset == "et" else 0.0,
        et_surface=7.5,
        et_depth=4.0,
        bottom=0.0 if preset != "confined" else -5.0,
        top=8.0 if preset != "confined" else 0.0,
    )


def teaching_grid_model(
    unconfined=True,
    gradient=False,
    heterogeneous=False,
    recharge_mm=150.0,
    zones=(1e-6, 1e-4, 1e-3),
    conductivity=1e-4,
    left=18.0,
    right=8.0,
):
    """Current eleven-cell lab. Historical grid_model stays a regression benchmark."""
    k = (
        (zones[0],) * 5 + (zones[1],) + (zones[2],) * 5
        if heterogeneous
        else (conductivity,) * 11
    )
    return Model(
        k,
        left,
        0.5 if gradient else right,
        unconfined=unconfined,
        thickness=20.0,
        bottom=0.0 if unconfined else -20.0,
        top=30.0 if unconfined else 0.0,
        recharge=recharge_mm / 1000 / YEAR,
        conductance="integrated_thickness",
    )
