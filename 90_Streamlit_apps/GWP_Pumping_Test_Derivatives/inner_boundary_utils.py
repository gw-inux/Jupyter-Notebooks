from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
from scipy.special import kve


def _stehfest_coefficients(n: int = 12) -> np.ndarray:
    if n % 2 or n < 4:
        raise ValueError('Stehfest order n must be even and >= 4.')
    m = n // 2
    coeff = np.zeros(n, dtype=float)
    for k in range(1, n + 1):
        total = 0.0
        j0 = (k + 1) // 2
        j1 = min(k, m)
        for j in range(j0, j1 + 1):
            num = (j ** m) * math.factorial(2 * j)
            den = (
                math.factorial(m - j)
                * math.factorial(j)
                * math.factorial(j - 1)
                * math.factorial(k - j)
                * math.factorial(2 * j - k)
            )
            total += num / den
        coeff[k - 1] = ((-1) ** (k + m)) * total
    return coeff

_STEHFEST_12 = _stehfest_coefficients(12)


def invert_laplace_stehfest(F, time, order: int = 12):
    t = np.asarray(time, dtype=float)
    if np.any(~np.isfinite(t)) or np.any(t <= 0):
        raise ValueError('All inversion times must be finite and > 0.')
    V = _STEHFEST_12 if order == 12 else _stehfest_coefficients(order)
    ln2 = math.log(2.0)
    out = np.empty_like(t)
    for idx, ti in np.ndenumerate(t):
        k = np.arange(1, order + 1, dtype=float)
        p = k * ln2 / float(ti)
        vals = np.asarray(F(p), dtype=float)
        out[idx] = ln2 / float(ti) * float(np.dot(V, vals))
    return out


def _lambda_p(p, T: float, S: float, B: float | None = None):
    p = np.asarray(p, dtype=float)
    val = p * float(S) / float(T)
    if B is not None:
        val = val + 1.0 / float(B) ** 2
    return np.sqrt(val)


def _finite_well_self_impedance(p, T: float, S: float, rw: float, B: float | None = None):
    lam = _lambda_p(p, T, S, B)
    x = np.maximum(float(rw) * lam, 1e-300)
    # kve(v,x)=exp(x) K_v(x), so the exponential scaling cancels in K0/K1.
    ratio = kve(0, x) / kve(1, x)
    return ratio / (2.0 * np.pi * float(T) * x)


def _finite_well_field_impedance(p, T: float, S: float, rw: float, radius: float, B: float | None = None):
    lam = _lambda_p(p, T, S, B)
    xw = np.maximum(float(rw) * lam, 1e-300)
    xr = np.maximum(float(radius) * lam, xw)
    # K0(xr)/(xw K1(xw)); use scaled Bessels and explicit exponential difference.
    exponent = np.clip(-(xr - xw), -745.0, 0.0)
    ratio = np.exp(exponent) * kve(0, xr) / kve(1, xw)
    return ratio / (2.0 * np.pi * float(T) * xw)


def pumping_well_response(
    time,
    Q: float,
    T: float,
    S: float,
    rw: float,
    *,
    rc: float | None = None,
    skin: float = 0.0,
    B: float | None = None,
    boundary: str = 'No boundary',
    boundary_distance: float | None = None,
    stehfest_order: int = 12,
):
    """Finite-radius pumping-well drawdown with optional storage, skin and one outer boundary.

    Parameters use groundwater units (s, m, m3/s). ``rw`` is the effective
    screen radius. If ``rc`` is None or <=0, wellbore storage is disabled;
    otherwise the water-column storage coefficient is Cw=pi*rc**2 [m2].
    ``skin`` is the conventional dimensionless steady-state skin factor.

    The confined aquifer transfer impedance is the finite-radius radial-flow
    solution. Supplying ``B`` adds Hantush-Jacob leakage via
    lambda² = S p/T + 1/B². A straight outer boundary is added by an image
    well at 2D from the pumping well. The storage/skin boundary condition is
    then applied in Laplace space and inverted with Stehfest's algorithm.
    """
    t = np.asarray(time, dtype=float)
    if float(T) <= 0 or float(S) <= 0 or float(rw) <= 0:
        raise ValueError('T, S and rw must be > 0.')
    if B is not None and float(B) <= 0:
        raise ValueError('B must be > 0 when supplied.')
    bname = str(boundary).strip().lower()
    no_boundary = bname in {'none','no boundary','infinite','infinite aquifer'}
    if not no_boundary:
        if boundary_distance is None or float(boundary_distance) <= 0:
            raise ValueError('A positive boundary_distance is required.')
        if bname in {'no-flow boundary','no-flow','no flow','barrier'}:
            sign = 1.0
        elif bname in {'specified-head boundary','specified-head','specified head','recharge','constant-head'}:
            sign = -1.0
        else:
            raise ValueError(f'Unknown boundary type: {boundary}')
    else:
        sign = 0.0

    Cw = 0.0 if rc is None or float(rc) <= 0 else np.pi * float(rc) ** 2
    Rskin = float(skin) / (2.0 * np.pi * float(T))

    def F(p):
        p = np.asarray(p, dtype=float)
        Za = _finite_well_self_impedance(p, T, S, rw, B)
        if sign:
            Zi = _finite_well_field_impedance(
                p, T, S, rw, 2.0 * float(boundary_distance), B
            )
            Za = Za + sign * Zi
        Z = Za + Rskin
        return (float(Q) / p) * Z / (1.0 + Cw * p * Z)

    s = invert_laplace_stehfest(F, t, order=stehfest_order)
    # Numerical inversion can generate tiny negative roundoff at extremely early time.
    scale = max(float(np.nanmax(np.abs(s))) if s.size else 0.0, 1.0)
    s = np.where((s < 0) & (np.abs(s) < 1e-10 * scale), 0.0, s)
    if len(t) >= 3:
        d = np.gradient(s, np.log(t), edge_order=2)
    elif len(t) == 2:
        d = np.gradient(s, np.log(t), edge_order=1)
    else:
        d = np.full_like(s, np.nan)
    return s, d


def theis_skin_response(time, Q: float, T: float, S: float, rw: float, skin: float):
    """Report Eq. (67)/(68): line-source Theis at r=rw plus steady-state skin."""
    from scipy.special import exp1
    t = np.asarray(time, dtype=float)
    u = float(rw) ** 2 * float(S) / (4.0 * float(T) * t)
    base = float(Q) / (4.0 * np.pi * float(T)) * exp1(u)
    offset = float(Q) / (2.0 * np.pi * float(T)) * float(skin)
    deriv = float(Q) / (4.0 * np.pi * float(T)) * np.exp(-u)
    return base + offset, deriv


def storage_only_response(time, Q: float, T: float, S: float, rw: float, rc: float):
    return pumping_well_response(time, Q, T, S, rw, rc=rc, skin=0.0)
