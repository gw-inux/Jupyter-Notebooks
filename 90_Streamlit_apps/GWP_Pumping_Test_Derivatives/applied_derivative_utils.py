"""Utilities for the measured/own-data derivative section.

The functions in this module are deliberately independent from Streamlit so that
all numerical operations can be unit tested.  Derivatives are returned as
``ds/dln(t)`` and therefore have the same length unit as drawdown.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
from typing import Dict, Iterable, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import special
from scipy.optimize import least_squares
from scipy.signal import savgol_filter

from inner_boundary_utils import pumping_well_response

try:
    from neuman_derivative import neuman_response
except Exception:  # pragma: no cover - keeps non-Neuman utilities importable
    neuman_response = None


# -----------------------------------------------------------------------------
# Data cleaning / filtering
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class CleaningReport:
    rows_input: int
    rows_output: int
    removed_non_numeric_or_missing: int
    removed_nonpositive_time: int
    duplicate_times_aggregated: int


def clean_time_drawdown(
    time: Iterable[float],
    drawdown: Iterable[float],
) -> Tuple[np.ndarray, np.ndarray, CleaningReport]:
    """Return sorted, finite, positive-time data with duplicate times aggregated.

    Duplicate times are represented by the median drawdown.  The function does
    not automatically remove statistical outliers; potentially real hydraulic
    features should not be deleted without user review.
    """
    frame = pd.DataFrame({"time": time, "drawdown": drawdown})
    n_input = len(frame)
    frame["time"] = pd.to_numeric(frame["time"], errors="coerce")
    frame["drawdown"] = pd.to_numeric(frame["drawdown"], errors="coerce")

    finite_mask = np.isfinite(frame["time"].to_numpy(dtype=float)) & np.isfinite(
        frame["drawdown"].to_numpy(dtype=float)
    )
    removed_missing = int((~finite_mask).sum())
    frame = frame.loc[finite_mask].copy()

    positive_mask = frame["time"] > 0.0
    removed_nonpositive = int((~positive_mask).sum())
    frame = frame.loc[positive_mask]

    n_before_duplicates = len(frame)
    frame = (
        frame.groupby("time", as_index=False, sort=True)["drawdown"]
        .median()
        .sort_values("time")
    )
    duplicate_count = int(n_before_duplicates - len(frame))

    t = frame["time"].to_numpy(dtype=float)
    s = frame["drawdown"].to_numpy(dtype=float)
    report = CleaningReport(
        rows_input=n_input,
        rows_output=len(frame),
        removed_non_numeric_or_missing=removed_missing,
        removed_nonpositive_time=removed_nonpositive,
        duplicate_times_aggregated=duplicate_count,
    )
    return t, s, report


def log_reduce(
    time: Iterable[float],
    drawdown: Iterable[float],
    points_per_decade: int = 18,
) -> Tuple[np.ndarray, np.ndarray]:
    """Reduce data to at most approximately ``points_per_decade`` log-time bins.

    For every occupied logarithmic bin the *original* observation closest to the
    median log-time is retained.  This avoids creating artificial drawdown values
    while preventing late-time, high-frequency measurements from dominating.
    """
    t, s, _ = clean_time_drawdown(time, drawdown)
    if len(t) <= 2:
        return t, s

    ppd = max(2, int(points_per_decade))
    x = np.log10(t)
    width = 1.0 / ppd
    origin = math.floor(float(x.min()) * ppd) / ppd
    bins = np.floor((x - origin) / width + 1e-12).astype(int)

    keep = []
    for b in np.unique(bins):
        idx = np.where(bins == b)[0]
        if len(idx) == 1:
            keep.append(int(idx[0]))
            continue
        target = float(np.median(x[idx]))
        keep.append(int(idx[np.argmin(np.abs(x[idx] - target))]))

    # Always preserve first and last observations.
    keep.extend([0, len(t) - 1])
    keep = np.array(sorted(set(keep)), dtype=int)
    return t[keep], s[keep]


def moving_average(drawdown: Iterable[float], window: int = 7) -> np.ndarray:
    """Centered rolling mean with edge windows automatically shortened."""
    y = pd.Series(np.asarray(drawdown, dtype=float))
    w = max(1, int(window))
    if w % 2 == 0:
        w += 1
    return y.rolling(window=w, center=True, min_periods=1).mean().to_numpy()


def savgol_smooth(drawdown: Iterable[float], window: int = 9, polyorder: int = 2) -> np.ndarray:
    """Savitzky-Golay smoothing for already log-reduced data.

    This is offered as an advanced alternative; it is not required by the report
    workflow.  The window is forced to an odd, valid size.
    """
    y = np.asarray(drawdown, dtype=float)
    if len(y) < 5:
        return y.copy()
    w = max(5, int(window))
    if w % 2 == 0:
        w += 1
    if w > len(y):
        w = len(y) if len(y) % 2 == 1 else len(y) - 1
    p = min(max(1, int(polyorder)), w - 2)
    if w < p + 2:
        return y.copy()
    return savgol_filter(y, window_length=w, polyorder=p, mode="interp")


def hampel_flags(drawdown: Iterable[float], window: int = 7, n_sigma: float = 4.0) -> np.ndarray:
    """Flag local outlier candidates using a Hampel (median/MAD) criterion.

    Flags are diagnostics only; callers decide whether flagged values are removed.
    """
    y = np.asarray(drawdown, dtype=float)
    n = len(y)
    flags = np.zeros(n, dtype=bool)
    radius = max(1, int(window) // 2)
    for i in range(n):
        lo = max(0, i - radius)
        hi = min(n, i + radius + 1)
        local = y[lo:hi]
        med = np.median(local)
        mad = np.median(np.abs(local - med))
        scale = 1.4826 * mad
        if scale > 0 and abs(y[i] - med) > float(n_sigma) * scale:
            flags[i] = True
    return flags


# -----------------------------------------------------------------------------
# Derivative calculations
# -----------------------------------------------------------------------------

def compute_log_derivative(
    time: Iterable[float],
    drawdown: Iterable[float],
    method: str = "bourdet1989",
    L: float = 0.2,
    n_neighbors: int = 1,
    positive_only: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute ``ds/dln(t)`` using methods introduced in the module/report.

    Supported methods: ``renard2009``, ``log_difference``,
    ``neighboring_points``, ``bourdet1989``, ``spane_wurstner1993``.
    ``L`` is a spacing/window measured in log10 cycles for the last two methods.
    """
    t, s, _ = clean_time_drawdown(time, drawdown)
    if len(t) < 2:
        return np.array([], dtype=float), np.array([], dtype=float)

    ln_t = np.log(t)
    log_t = np.log10(t)
    method = str(method).lower()

    if method == "renard2009":
        ds = np.diff(s)
        dt = np.diff(t)
        td = 0.5 * (t[1:] + t[:-1])
        d = (ds / dt) * td

    elif method == "log_difference":
        ds = np.diff(s)
        dln = np.diff(ln_t)
        td = np.sqrt(t[:-1] * t[1:])
        d = ds / dln

    elif method == "neighboring_points":
        nn = max(1, int(n_neighbors))
        td, d = [], []
        for i in range(nn, len(t) - nn):
            il, ir = i - nn, i + nn
            dx1 = ln_t[i] - ln_t[il]
            dx2 = ln_t[ir] - ln_t[i]
            if dx1 <= 0 or dx2 <= 0:
                continue
            m1 = (s[i] - s[il]) / dx1
            m2 = (s[ir] - s[i]) / dx2
            td.append(t[i])
            d.append((m1 * dx2 + m2 * dx1) / (dx1 + dx2))
        td = np.asarray(td, dtype=float)
        d = np.asarray(d, dtype=float)

    elif method == "bourdet1989":
        L = max(1e-3, float(L))
        td, d = [], []
        for i in range(1, len(t) - 1):
            left_candidates = np.where(log_t[:i] <= log_t[i] - L)[0]
            il = int(left_candidates[-1]) if len(left_candidates) else 0
            right_rel = np.where(log_t[i + 1 :] >= log_t[i] + L)[0]
            ir = int(i + 1 + right_rel[0]) if len(right_rel) else len(t) - 1
            if il >= i or ir <= i:
                continue
            dx1 = ln_t[i] - ln_t[il]
            dx2 = ln_t[ir] - ln_t[i]
            if dx1 <= 0 or dx2 <= 0:
                continue
            m1 = (s[i] - s[il]) / dx1
            m2 = (s[ir] - s[i]) / dx2
            td.append(t[i])
            d.append((m1 * dx2 + m2 * dx1) / (dx1 + dx2))
        td = np.asarray(td, dtype=float)
        d = np.asarray(d, dtype=float)

    elif method == "spane_wurstner1993":
        L = max(1e-3, float(L))
        td, d = [], []
        idx_all = np.arange(len(t))
        for i in range(1, len(t) - 1):
            left_idx = idx_all[(log_t >= log_t[i] - L) & (idx_all <= i)]
            right_idx = idx_all[(log_t <= log_t[i] + L) & (idx_all >= i)]
            if len(left_idx) < 2:
                left_idx = np.arange(0, i + 1)
            if len(right_idx) < 2:
                right_idx = np.arange(i, len(t))
            if len(left_idx) < 2 or len(right_idx) < 2:
                continue
            m1 = np.polyfit(ln_t[left_idx], s[left_idx], 1)[0]
            m2 = np.polyfit(ln_t[right_idx], s[right_idx], 1)[0]
            dx1 = ln_t[i] - ln_t[left_idx[0]]
            dx2 = ln_t[right_idx[-1]] - ln_t[i]
            if dx1 <= 0 or dx2 <= 0:
                continue
            td.append(t[i])
            d.append((m1 * dx2 + m2 * dx1) / (dx1 + dx2))
        td = np.asarray(td, dtype=float)
        d = np.asarray(d, dtype=float)

    else:
        raise ValueError(f"Unknown derivative method: {method}")

    valid = np.isfinite(td) & np.isfinite(d)
    if positive_only:
        valid &= d > 0
    return td[valid], d[valid]


# -----------------------------------------------------------------------------
# Analytical model responses
# -----------------------------------------------------------------------------

def theis_response(time, Q: float, T: float, S: float, r: float):
    t = np.asarray(time, dtype=float)
    u = r * r * S / (4.0 * T * t)
    scale = Q / (4.0 * np.pi * T)
    return scale * special.exp1(u), scale * np.exp(-u)


def image_well_distance(
    boundary_distance: float,
    observation_distance: float,
    observation_position: str = "Between pumping well and boundary",
) -> float:
    a = float(boundary_distance)
    r = float(observation_distance)
    if observation_position == "Between pumping well and boundary":
        if a <= r:
            raise ValueError("Boundary distance must exceed observation distance for this geometry.")
        return 2.0 * a - r
    if observation_position == "Away from boundary":
        return 2.0 * a + r
    if observation_position == "Parallel to boundary":
        return math.sqrt(r * r + (2.0 * a) ** 2)
    if observation_position == "At pumping well":
        # The observation point coincides with the pumping well. The image well
        # is mirrored across the straight boundary and therefore lies 2a away.
        return 2.0 * a
    raise ValueError(f"Unknown observation geometry: {observation_position}")


def boundary_response(
    time,
    Q: float,
    T: float,
    S: float,
    r: float,
    boundary_distance: float,
    boundary_type: str,
    observation_position: str = "Between pumping well and boundary",
):
    s0, d0 = theis_response(time, Q, T, S, r)
    ri = image_well_distance(boundary_distance, r, observation_position)
    si, di = theis_response(time, Q, T, S, ri)
    btype = boundary_type.lower()
    if btype in {"specified-head", "specified head", "recharge", "constant-head"}:
        sign = -1.0
    elif btype in {"no-flow", "no flow", "barrier"}:
        sign = 1.0
    else:
        raise ValueError(f"Unknown boundary type: {boundary_type}")
    return s0 + sign * si, d0 + sign * di


@lru_cache(maxsize=8)
def _gauss_nodes(order: int):
    return np.polynomial.legendre.leggauss(int(order))


def hantush_well_function(u, rho: float, order: int = 64) -> np.ndarray:
    """Fast Gauss-Legendre evaluation of Hantush-Jacob W(u, r/B).

    The transformed integral is
        W = integral[ln(u), inf] exp(-exp(x) - rho^2/(4 exp(x))) dx.
    A finite upper bound is safe because the integrand decays super-exponentially
    for large x.  The implementation is vectorized over u.
    """
    u = np.asarray(u, dtype=float)
    rho = max(0.0, float(rho))
    out = np.zeros_like(u)
    good = np.isfinite(u) & (u > 0)
    if not np.any(good):
        return out

    a = np.log(u[good])
    b = np.full_like(a, np.log(max(60.0, 20.0 + 10.0 * rho)))
    integrate = a < b
    if np.any(integrate):
        nodes, weights = _gauss_nodes(order)
        aa = a[integrate][:, None]
        bb = b[integrate][:, None]
        x = 0.5 * (bb - aa) * nodes[None, :] + 0.5 * (aa + bb)
        z = np.exp(x)
        integrand = np.exp(-z - (rho * rho) / (4.0 * z))
        values = 0.5 * (bb[:, 0] - aa[:, 0]) * (integrand @ weights)
        indices = np.where(good)[0][integrate]
        out[indices] = values
    return out


def hantush_response(time, Q: float, T: float, S: float, r: float, B: float):
    t = np.asarray(time, dtype=float)
    u = r * r * S / (4.0 * T * t)
    rho = r / B
    scale = Q / (4.0 * np.pi * T)
    W = hantush_well_function(u, rho)
    # Exact derivative of the lower-bound integral with respect to ln(t).
    dD = np.exp(-u - (rho * rho) / (4.0 * u))
    return scale * W, scale * dD


def neuman_response_fast(time, Q, T, S_a, S_y, r, beta):
    if neuman_response is None:
        raise RuntimeError("neuman_derivative.py could not be imported.")
    result = neuman_response(
        np.asarray(time, dtype=float),
        Q=float(Q),
        T=float(T),
        S_a=float(S_a),
        S_y=float(S_y),
        r=float(r),
        beta=float(beta),
        # A fixed scaled-Hankel extent is sufficient for the educational
        # parameter range and avoids a very large quadrature domain when an
        # image well makes beta large. Validation tests compare this fast
        # setting against the full Neuman solver over the plotted range.
        x_max=150.0,
        x_step=1.5,
        quad_order=4,
        points_per_decade=18,
        check_applicability=False,
    )
    return result.drawdown, result.derivative_ln_time


def solution_response(
    solution: str,
    time,
    Q: float,
    r: float,
    params: Dict[str, float],
):
    """Return drawdown and ``ds/dln(t)`` for one infinite-aquifer solution.

    ``beta`` for the Neuman solution is defined at the supplied radial distance
    ``r``.  This matters when the function is used with an image well because
    Neuman's beta contains ``r²``.
    """
    name = str(solution).strip().lower()
    if name == "theis":
        return theis_response(time, Q, params["T"], params["S"], r)
    if name in {"hantush-jacob", "hantush", "hantush jacob"}:
        return hantush_response(time, Q, params["T"], params["S"], r, params["B"])
    if name in {"neuman delayed yield", "neuman", "neumann"}:
        return neuman_response_fast(
            time,
            Q,
            params["T"],
            params["S_a"],
            params["S_y"],
            r,
            params["beta"],
        )
    raise ValueError(f"Unknown underlying solution: {solution}")


def combined_model_response(
    solution: str,
    boundary: str,
    time,
    Q: float,
    r: float,
    params: Dict[str, float],
    *,
    observation_position: str = "Between pumping well and boundary",
):
    """Combine Theis, Hantush-Jacob, or Neuman with one straight boundary.

    The lateral boundary is represented by an image well.  This superposition
    is exact for the linear Theis and Hantush-Jacob formulations.  For Neuman,
    it is applied to the linearized delayed-yield solution used throughout this
    educational module.  ``beta`` is supplied for the real observation distance
    and is scaled by ``(r_image/r_real)^2`` for the image-well response so the
    same physical vertical anisotropy is retained.
    """
    boundary_name = str(boundary).strip().lower()
    base_s, base_d = solution_response(solution, time, Q, r, params)

    if boundary_name in {"none", "no boundary", "infinite", "infinite aquifer"}:
        return base_s, base_d

    if "D" not in params:
        raise ValueError("Boundary distance D is required when a boundary is selected.")

    ri = image_well_distance(params["D"], r, observation_position)
    image_params = dict(params)
    solution_name = str(solution).strip().lower()
    if solution_name in {"neuman delayed yield", "neuman", "neumann"}:
        image_params["beta"] = float(params["beta"]) * (float(ri) / float(r)) ** 2

    image_s, image_d = solution_response(solution, time, Q, ri, image_params)

    if boundary_name in {"specified-head boundary", "specified-head", "specified head", "recharge", "constant-head"}:
        sign = -1.0
    elif boundary_name in {"no-flow boundary", "no-flow", "no flow", "barrier"}:
        sign = 1.0
    else:
        raise ValueError(f"Unknown boundary type: {boundary}")

    return base_s + sign * image_s, base_d + sign * image_d


def _normalize_inner_effects(inner_effects: str) -> str:
    name = str(inner_effects or "None").strip().lower()
    aliases = {
        "none": "none",
        "no inner boundary": "none",
        "no inner boundaries": "none",
        "skin": "skin",
        "wellbore storage": "storage",
        "storage": "storage",
        "well storage": "storage",
        "wellbore storage + skin": "storage+skin",
        "storage + skin": "storage+skin",
        "storage and skin": "storage+skin",
        "wellbore storage and skin": "storage+skin",
    }
    if name not in aliases:
        raise ValueError(f"Unknown inner-boundary selection: {inner_effects}")
    return aliases[name]


def conceptual_model_response(
    solution: str,
    boundary: str,
    time,
    Q: float,
    r: float,
    params: Dict[str, float],
    *,
    observation_position: str = "Between pumping well and boundary",
    inner_effects: str = "None",
):
    """Return the selected aquifer/outer-boundary model with optional well effects.

    ``inner_effects='None'`` delegates directly to the established response, so
    all previous behavior is retained. Inner boundaries are only meaningful for
    pumping-well data. In that case ``r`` is the effective screen radius and
    ``observation_position`` must be ``'At pumping well'``.

    Theis and Hantush-Jacob wellbore storage are solved with the finite-radius
    Laplace-space well solution. Skin is the conventional steady-state head loss.
    For Neuman delayed yield, a bounded confined-elastic finite-well composite
    based on S_a bridges the storage-dominated early phase to the established
    delayed-yield response. The UI marks this combination as an approximation
    rather than an exact finite-diameter Neuman solution.
    """
    inner = _normalize_inner_effects(inner_effects)
    if inner == "none":
        return combined_model_response(
            solution, boundary, time, Q, r, params,
            observation_position=observation_position,
        )

    if observation_position != "At pumping well":
        raise ValueError(
            "Wellbore storage and skin are pumping-well inner boundaries. "
            "Select pumping-well data before activating them."
        )

    T = float(params["T"])
    skin = float(params.get("skin", 0.0)) if inner in {"skin", "storage+skin"} else 0.0
    use_storage = inner in {"storage", "storage+skin"}

    if not use_storage:
        base_s, base_d = combined_model_response(
            solution, boundary, time, Q, r, params,
            observation_position=observation_position,
        )
        return base_s + float(Q) * skin / (2.0 * math.pi * T), base_d

    if "rc" not in params:
        raise ValueError("Effective casing/storage radius rc is required for wellbore storage.")
    rc = float(params["rc"])
    rw = float(r)
    if rc <= 0 or rw <= 0:
        raise ValueError("rw and rc must be positive.")

    solution_name = str(solution).strip().lower()
    boundary_name = str(boundary).strip().lower()
    boundary_distance = None if boundary_name in {
        "none", "no boundary", "infinite", "infinite aquifer"
    } else float(params["D"])

    if solution_name == "theis":
        return pumping_well_response(
            time, Q, T, float(params["S"]), rw, rc=rc, skin=skin,
            boundary=boundary, boundary_distance=boundary_distance,
        )

    if solution_name in {"hantush-jacob", "hantush", "hantush jacob"}:
        return pumping_well_response(
            time, Q, T, float(params["S"]), rw, rc=rc, skin=skin,
            B=float(params["B"]), boundary=boundary, boundary_distance=boundary_distance,
        )

    if solution_name in {"neuman delayed yield", "neuman", "neumann"}:
        # No closed finite-radius wellbore-storage form is implemented for the
        # Neuman delayed-yield solution.  Use a deliberately bounded composite
        # instead of adding a confined storage correction directly: the exact
        # confined finite-well response controls the storage-dominated early
        # phase, while the established Neuman response (plus the steady skin
        # offset) controls late time.  The transition weight is derived from
        # the corresponding confined finite-well attenuation, so the result
        # approaches pure wellbore storage at early time and the unchanged
        # Neuman solution at late time without producing negative drawdown.
        base_neuman_s, _ = combined_model_response(
            solution, boundary, time, Q, rw, params,
            observation_position="At pumping well",
        )
        elastic_params = {"T": T, "S": float(params["S_a"])}
        if boundary_distance is not None:
            elastic_params["D"] = boundary_distance
        base_elastic_s, _ = combined_model_response(
            "Theis", boundary, time, Q, rw, elastic_params,
            observation_position="At pumping well",
        )
        inner_elastic_s, _ = pumping_well_response(
            time, Q, T, float(params["S_a"]), rw, rc=rc, skin=skin,
            boundary=boundary, boundary_distance=boundary_distance,
        )
        skin_offset = float(Q) * skin / (2.0 * math.pi * T)
        reference_no_storage = base_elastic_s + skin_offset
        ratio = np.divide(
            inner_elastic_s,
            reference_no_storage,
            out=np.ones_like(inner_elastic_s),
            where=np.abs(reference_no_storage) > 1.0e-14,
        )
        ratio = np.clip(ratio, 0.0, 1.0)
        target_late = base_neuman_s + skin_offset
        scaled_neuman = target_late * ratio
        storage_weight = np.clip(1.0 - ratio * ratio, 0.0, 1.0)
        drawdown = (
            storage_weight * inner_elastic_s
            + (1.0 - storage_weight) * scaled_neuman
        )
        time_arr = np.asarray(time, dtype=float)
        if len(time_arr) >= 3:
            derivative = np.gradient(drawdown, np.log(time_arr), edge_order=2)
        elif len(time_arr) == 2:
            derivative = np.gradient(drawdown, np.log(time_arr), edge_order=1)
        else:
            derivative = np.full_like(drawdown, np.nan)
        return drawdown, derivative

    raise ValueError(f"Unknown underlying solution: {solution}")


def model_response(
    model: str,
    time,
    Q: float,
    r: float,
    params: Dict[str, float],
    *,
    observation_position: str = "Between pumping well and boundary",
):
    """Backward-compatible model dispatcher used by the first app version."""
    model_lower = str(model).lower()
    if model_lower == "theis":
        return combined_model_response("Theis", "No boundary", time, Q, r, params, observation_position=observation_position)
    if model_lower == "hantush-jacob":
        return combined_model_response("Hantush-Jacob", "No boundary", time, Q, r, params, observation_position=observation_position)
    if model_lower == "specified-head boundary":
        return combined_model_response("Theis", "Specified-head boundary", time, Q, r, params, observation_position=observation_position)
    if model_lower == "no-flow boundary":
        return combined_model_response("Theis", "No-flow boundary", time, Q, r, params, observation_position=observation_position)
    if model_lower == "neuman delayed yield":
        return combined_model_response("Neuman delayed yield", "No boundary", time, Q, r, params, observation_position=observation_position)
    raise ValueError(f"Unknown model: {model}")


# -----------------------------------------------------------------------------
# Plateau search and model fitting
# -----------------------------------------------------------------------------

def detect_plateau(time, derivative, min_decades: float = 0.65) -> Optional[Dict[str, float]]:
    """Find a conservative candidate derivative plateau.

    Candidate windows must span ``min_decades``.  The score combines absolute
    log-log slope and robust scatter; this is an aid for the user, not an
    automatic hydraulic interpretation.
    """
    t = np.asarray(time, dtype=float)
    d = np.asarray(derivative, dtype=float)
    mask = np.isfinite(t) & np.isfinite(d) & (t > 0) & (d > 0)
    t, d = t[mask], d[mask]
    if len(t) < 6:
        return None
    x, y = np.log10(t), np.log10(d)
    candidates = []
    n = len(t)
    max_d = float(np.max(d))
    full_span = max(float(x[-1] - x[0]), 1e-9)
    for i in range(n - 4):
        # Consider windows from min_decades to roughly 1.5 decades.
        for j in range(i + 4, n):
            span = x[j] - x[i]
            if span < min_decades:
                continue
            if span > 1.5:
                break
            xx, yy = x[i : j + 1], y[i : j + 1]
            slope = float(np.polyfit(xx, yy, 1)[0])
            med = float(np.median(yy))
            scatter = float(1.4826 * np.median(np.abs(yy - med)))
            d_med = float(np.median(d[i : j + 1]))
            # Reject vanishing early-time tails and deep derivative minima.
            # The 0.4 threshold intentionally retains the first d-plateau of a
            # one-sided no-flow case even when the later plateau is ~2d.
            if d_med < 0.40 * max_d:
                continue
            position = ((x[i] + x[j]) * 0.5 - x[0]) / full_span
            # Prefer a flat, low-scatter *early* admissible plateau.  This is
            # important for barrier-boundary data, where the late 2d plateau
            # must not be mistaken for the radial-flow d plateau.
            score = abs(slope) + 0.65 * scatter + 0.08 * position - 0.025 * span
            candidates.append({
                "t_start": float(t[i]),
                "t_end": float(t[j]),
                "d_median": d_med,
                "slope": slope,
                "scatter_log10": scatter,
                "decades": float(span),
                "n": int(j - i + 1),
                "score": score,
            })
    if not candidates:
        return None
    # When more than one plateau exists (most importantly d followed by ~2d
    # near a barrier boundary), the radial-flow plateau is normally the first
    # sufficiently flat, well-populated plateau.  Prefer that early admissible
    # window instead of simply selecting the mathematically flattest late one.
    strict = [
        item for item in candidates
        if abs(item["slope"]) <= 0.10 and item["scatter_log10"] <= 0.06
    ]
    if strict:
        first = min(strict, key=lambda item: (item["t_start"], item["score"]))
        later = [item for item in strict if item["t_start"] > first["t_end"]]
        if later:
            # Delayed-yield/dual-storage responses can contain an early flat
            # shoulder, a pronounced derivative minimum, and a later radial
            # plateau.  If such a real dip separates two flat intervals, prefer
            # the later plateau.  A barrier boundary, in contrast, rises from d
            # toward ~2d and therefore does not satisfy this dip criterion.
            later_best = min(later, key=lambda item: item["score"] )
            between = (t > first["t_end"]) & (t < later_best["t_start"] )
            if np.any(between) and float(np.min(d[between])) < 0.65 * first["d_median"]:
                return later_best
        return first
    return min(candidates, key=lambda item: item["score"])


def plateau_transmissivity(Q: float, plateau_derivative: float) -> float:
    d = float(plateau_derivative)
    if d <= 0:
        return float("nan")
    return float(Q) / (4.0 * math.pi * d)


def default_conceptual_initial(
    solution: str,
    boundary: str,
    r: float,
    *,
    T_hint: Optional[float] = None,
    inner_effects: str = "None",
) -> Dict[str, float]:
    """Return conservative manual/pre-fit starting parameters."""
    T0 = float(T_hint) if T_hint and np.isfinite(T_hint) and T_hint > 0 else 1e-3
    solution_name = str(solution).strip().lower()
    boundary_name = str(boundary).strip().lower()

    if solution_name == "theis":
        initial = {"T": T0, "S": 1e-3}
    elif solution_name in {"hantush-jacob", "hantush", "hantush jacob"}:
        initial = {"T": T0, "S": 1e-3, "B": max(10.0 * float(r), 100.0)}
    elif solution_name in {"neuman delayed yield", "neuman", "neumann"}:
        initial = {"T": T0, "S_a": 5e-4, "S_y": 0.1, "beta": 0.1}
    else:
        raise ValueError(f"Unknown underlying solution: {solution}")

    if boundary_name not in {"none", "no boundary", "infinite", "infinite aquifer"}:
        initial["D"] = max(5.0 * float(r), float(r) + 1.0)

    inner = _normalize_inner_effects(inner_effects)
    if inner in {"storage", "storage+skin"}:
        initial["rc"] = max(float(r), 0.05)
    if inner in {"skin", "storage+skin"}:
        initial["skin"] = 5.0
    return initial


def _conceptual_bounds(
    solution: str,
    boundary: str,
    r: float,
    observation_position: str,
    inner_effects: str = "None",
):
    solution_name = str(solution).strip().lower()
    boundary_name = str(boundary).strip().lower()

    if solution_name == "theis":
        names = ["T", "S"]
        lo = [1e-8, 1e-8]
        hi = [1e-1, 5e-1]
    elif solution_name in {"hantush-jacob", "hantush", "hantush jacob"}:
        names = ["T", "S", "B"]
        lo = [1e-8, 1e-8, 0.5]
        hi = [1e-1, 5e-1, 1e6]
    elif solution_name in {"neuman delayed yield", "neuman", "neumann"}:
        names = ["T", "S_a", "S_y", "beta"]
        lo = [1e-8, 1e-8, 1e-3, 1e-4]
        hi = [1e-1, 2e-2, 6e-1, 10.0]
    else:
        raise ValueError(f"Unknown underlying solution: {solution}")

    if boundary_name not in {"none", "no boundary", "infinite", "infinite aquifer"}:
        if observation_position == "Between pumping well and boundary":
            dmin = max(float(r) * 1.001, 0.5)
        else:
            dmin = 0.5
        names.append("D")
        lo.append(dmin)
        hi.append(1e6)

    inner = _normalize_inner_effects(inner_effects)
    if inner in {"storage", "storage+skin"}:
        names.append("rc")
        lo.append(0.005)
        hi.append(5.0)
    if inner in {"skin", "storage+skin"}:
        names.append("skin")
        # A negative constant lumped skin together with wellbore storage can
        # make the simple storage/skin transfer impedance non-passive. The
        # report's combined examples use SF >= 0. Keep negative skin available
        # for the skin-only case, where Eq. (67)/(68) is well defined.
        lo.append(0.0 if inner == "storage+skin" else -10.0)
        hi.append(100.0)

    return names, np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)


def _encode_initial(
    solution: str,
    boundary: str,
    initial: Dict[str, float],
    r: float,
    observation_position: str,
    inner_effects: str = "None",
):
    names, lo, hi = _conceptual_bounds(
        solution, boundary, r, observation_position, inner_effects
    )
    x0, lower, upper = [], [], []
    for i, name in enumerate(names):
        value = float(np.clip(initial[name], lo[i] + 1e-12, hi[i] - 1e-12))
        if name == "skin":
            x0.append(value)
            lower.append(lo[i])
            upper.append(hi[i])
        else:
            value = float(np.clip(value, lo[i] * 1.001, hi[i] / 1.001))
            x0.append(math.log10(value))
            lower.append(math.log10(lo[i]))
            upper.append(math.log10(hi[i]))
    return names, np.asarray(x0), np.asarray(lower), np.asarray(upper)


def _decode_conceptual(names, x: np.ndarray) -> Dict[str, float]:
    x = np.asarray(x, dtype=float)
    out = {}
    for i, name in enumerate(names):
        out[name] = float(x[i]) if name == "skin" else float(10.0 ** x[i])
    return out


def fit_conceptual_model(
    solution: str,
    boundary: str,
    time,
    drawdown,
    Q: float,
    r: float,
    *,
    initial: Optional[Dict[str, float]] = None,
    T_hint: Optional[float] = None,
    observation_position: str = "Between pumping well and boundary",
    inner_effects: str = "None",
    max_nfev: Optional[int] = None,
) -> Dict[str, object]:
    """Fit one selected solution/boundary combination to drawdown.

    The manual parameter set can be passed through ``initial`` and is then used
    as the nonlinear optimizer's starting point.  This is the intended workflow
    for the applied teaching page: first pre-fit by eye, then let least-squares
    refine the same conceptual model.
    """
    t, s, _ = clean_time_drawdown(time, drawdown)
    mask = np.isfinite(s) & (s >= 0)
    t, s = t[mask], s[mask]
    if len(t) < 8:
        raise ValueError("At least 8 valid observations are required for model fitting.")

    # Limit expensive fit evaluations while retaining log-time coverage.
    if len(t) > 80:
        t, s = log_reduce(t, s, points_per_decade=14)

    defaults = default_conceptual_initial(solution, boundary, r, T_hint=T_hint, inner_effects=inner_effects)
    if initial:
        defaults.update({k: float(v) for k, v in initial.items() if k in defaults})

    names, x0, lower, upper = _encode_initial(
        solution, boundary, defaults, r, observation_position, inner_effects
    )

    scale = max(float(np.nanmax(s)), 1e-6)
    floor = 0.05 * scale
    weights = 1.0 / np.sqrt(np.maximum(s, floor))
    weights /= np.mean(weights)
    solution_lower = str(solution).strip().lower()

    def residual(x):
        params = _decode_conceptual(names, x)
        if solution_lower in {"neuman delayed yield", "neuman", "neumann"}:
            if params["S_y"] <= 5.0 * params["S_a"]:
                return np.full_like(s, 25.0)
        try:
            pred, _ = conceptual_model_response(
                solution,
                boundary,
                t,
                Q,
                r,
                params,
                observation_position=observation_position,
                inner_effects=inner_effects,
            )
            if not np.all(np.isfinite(pred)):
                return np.full_like(s, 25.0)
            return (pred - s) / scale * weights
        except Exception:
            return np.full_like(s, 25.0)

    if max_nfev is None:
        # Each Neuman residual may require a second delayed-yield evaluation
        # when a boundary is active, so keep the inverse problem deliberately
        # bounded for an interactive educational app. The manual pre-fit is
        # therefore important: it gives the optimizer a physically plausible
        # local starting point instead of attempting a global inversion.
        if solution_lower in {"neuman delayed yield", "neuman", "neumann"}:
            boundary_lower = str(boundary).strip().lower()
            max_nfev = 24 if boundary_lower not in {"none", "no boundary", "infinite", "infinite aquifer"} else 32
        else:
            max_nfev = 180

    if _normalize_inner_effects(inner_effects) in {"storage", "storage+skin"}:
        max_nfev = min(
            int(max_nfev),
            70 if solution_lower not in {"neuman delayed yield", "neuman", "neumann"} else 28,
        )

    result = least_squares(
        residual,
        x0,
        bounds=(lower, upper),
        max_nfev=int(max_nfev),
        method="trf",
        xtol=3e-6,
        ftol=3e-6,
        gtol=3e-6,
    )
    params = _decode_conceptual(names, result.x)
    pred, derivative = conceptual_model_response(
        solution,
        boundary,
        t,
        Q,
        r,
        params,
        observation_position=observation_position,
        inner_effects=inner_effects,
    )
    raw_res = pred - s
    rss = float(np.sum(raw_res**2))
    n = len(s)
    k = len(params)
    rmse = float(np.sqrt(np.mean(raw_res**2)))
    mae = float(np.mean(np.abs(raw_res)))
    if rss <= 0:
        aic = -np.inf
    else:
        aic = n * math.log(rss / n) + 2 * k
    aicc = aic + (2 * k * (k + 1) / (n - k - 1)) if n > k + 1 and np.isfinite(aic) else aic

    return {
        "model": f"{solution} + {boundary}",
        "solution": solution,
        "boundary": boundary,
        "inner_effects": inner_effects,
        "params": params,
        "initial": defaults,
        "success": bool(result.success),
        "message": str(result.message),
        "nfev": int(result.nfev),
        "rmse": rmse,
        "mae": mae,
        "aicc": float(aicc),
        "time_fit": t,
        "drawdown_fit": s,
        "prediction_fit": pred,
        "derivative_fit": derivative,
    }


def fit_model(
    model: str,
    time,
    drawdown,
    Q: float,
    r: float,
    *,
    T_hint: Optional[float] = None,
    observation_position: str = "Between pumping well and boundary",
    max_nfev: Optional[int] = None,
) -> Dict[str, object]:
    """Backward-compatible wrapper for the original five candidate labels."""
    model_lower = str(model).lower()
    mapping = {
        "theis": ("Theis", "No boundary"),
        "hantush-jacob": ("Hantush-Jacob", "No boundary"),
        "specified-head boundary": ("Theis", "Specified-head boundary"),
        "no-flow boundary": ("Theis", "No-flow boundary"),
        "neuman delayed yield": ("Neuman delayed yield", "No boundary"),
    }
    if model_lower not in mapping:
        raise ValueError(model)
    solution, boundary = mapping[model_lower]
    result = fit_conceptual_model(
        solution,
        boundary,
        time,
        drawdown,
        Q,
        r,
        T_hint=T_hint,
        observation_position=observation_position,
        max_nfev=max_nfev,
    )
    result["model"] = model
    return result


def format_parameter_summary(params: Dict[str, float]) -> str:
    pieces = []
    for key, value in params.items():
        if key in {"T"}:
            pieces.append(f"{key}={value:.3g} m²/s")
        elif key in {"B", "D", "rc"}:
            pieces.append(f"{key}={value:.3g} m")
        elif key == "skin":
            pieces.append(f"SF={value:.3g}")
        else:
            pieces.append(f"{key}={value:.3g}")
    return ", ".join(pieces)
