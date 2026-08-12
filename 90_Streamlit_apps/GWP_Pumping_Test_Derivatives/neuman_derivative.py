"""Exact Neuman (1972/1975) delayed-water-table response and log-time derivative.

This module implements the complete-penetration Neuman solution in the form
published by Neuman (1975), eqs. (1)-(5).  The derivative ds/dln(t) is evaluated
analytically under the integral, avoiding a numerical finite-difference derivative.
Drawdown is then obtained by integrating that derivative backward in ln(time)
from the exact late-time Theis limit.  The Hankel integral is evaluated after the
change of variable x=y*sqrt(beta), which keeps the oscillatory Bessel factor on a
well-conditioned scale even for very small beta.

Notation
--------
S_a  : elastic storativity [-]
S_y  : specific yield [-]
sigma = S_a / S_y
beta  = r**2 * K_v / (b**2 * K_h)
t_s   = T*t / (S_a*r**2)
t_y   = T*t / (S_y*r**2) = sigma*t_s

The returned derivative is with respect to natural log time:
    ds/dln(t) = t * ds/dt
and therefore has units of length.  Its late-time plateau is Q/(4*pi*T).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
import warnings
from typing import Optional

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
from scipy.special import exp1, j0


@dataclass(frozen=True)
class NeumanResponse:
    time: np.ndarray
    drawdown: np.ndarray
    derivative_ln_time: np.ndarray
    u_a: np.ndarray
    u_y: np.ndarray
    beta: float
    storage_ratio: float
    derivative_plateau: float

    @property
    def derivative_log10_time(self) -> np.ndarray:
        """Return ds/dlog10(t)."""
        return np.log(10.0) * self.derivative_ln_time


@dataclass(frozen=True)
class _Spectrum:
    # Preweighted Hankel factor after the change of variable
    # x = y*sqrt(beta): 4*x/beta * J0(x) dx.
    hankel_weight: np.ndarray
    c0: np.ndarray
    a0: np.ndarray
    cn: np.ndarray
    an: np.ndarray


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0.")
    return value


def _validated_time(t) -> np.ndarray:
    arr = np.asarray(t, dtype=float)
    if arr.ndim == 0:
        arr = arr.reshape(1)
    if np.any(~np.isfinite(arr)) or np.any(arr <= 0.0):
        raise ValueError("All time values must be finite and > 0.")
    return arr


def neuman_beta(r: float, b: float, k_h: float, k_v: float) -> float:
    """Return Neuman beta = r^2 K_v / (b^2 K_h)."""
    r = _positive("r", r)
    b = _positive("b", b)
    k_h = _positive("k_h", k_h)
    k_v = _positive("k_v", k_v)
    return (r * r * k_v) / (b * b * k_h)


def neuman_u_a(t, T: float, S_a: float, r: float) -> np.ndarray:
    t = _validated_time(t)
    return r * r * S_a / (4.0 * T * t)


def neuman_u_y(t, T: float, S_y: float, r: float) -> np.ndarray:
    t = _validated_time(t)
    return r * r * S_y / (4.0 * T * t)


def _gamma_roots_for_nodes(
    y_nodes: np.ndarray,
    sigma: float,
    n_modes: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Roots gamma_0 and gamma_n of Neuman (1975), eqs. (4)-(5)."""
    gamma0 = np.empty(y_nodes.size, dtype=float)
    gamman = np.empty((n_modes, y_nodes.size), dtype=float)

    eps = 2.0e-11
    for i, y in enumerate(y_nodes):
        # Eq. (4), divided by cosh(gamma0):
        # gamma0^2 + sigma*gamma0*tanh(gamma0) = y^2.
        def f0(g):
            return g * g + sigma * g * math.tanh(g) - y * y

        gamma0[i] = brentq(
            f0,
            0.0,
            float(y),
            xtol=2.0e-12,
            rtol=2.0e-12,
            maxiter=80,
        )

        y2 = float(y * y)
        for n in range(1, n_modes + 1):
            # Neuman (1975), eq. (5):
            #   sigma*g*sin(g) + (y^2+g^2)*cos(g) = 0,
            #   (n-1/2)pi < g < n*pi.
            #
            # For small sigma the root lies extremely close to the left
            # asymptote.  Solving directly in g can then lose the sign
            # change through roundoff.  Write g=a+delta with
            # a=(n-1/2)pi.  Since tan(a+delta)=-cot(delta), the root
            # equation becomes the numerically well-conditioned
            #
            #   sigma*g*cos(delta) - (y^2+g^2)*sin(delta) = 0,
            #
            # on 0 < delta < pi/2.
            a = (n - 0.5) * math.pi

            def fdelta(delta):
                g = a + delta
                return (
                    sigma * g * math.cos(delta)
                    - (y2 + g * g) * math.sin(delta)
                )

            delta = brentq(
                fdelta,
                0.0,
                0.5 * math.pi,
                xtol=5.0e-15,
                rtol=5.0e-15,
                maxiter=100,
            )
            gamman[n - 1, i] = a + delta

    return gamma0, gamman


def _quadrature_nodes(
    y_max: float,
    high_step: float,
    quad_order: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Nonuniform Gauss-Legendre grid for the Hankel integral.

    Logarithmically refined intervals near y=0 resolve the increasingly narrow
    late-time contribution.  Uniform intervals above y=1 resolve J0 oscillations.
    """
    # 64 intervals between 1e-8 and 1 plus the initial 0--1e-8 interval.
    low_edges = np.r_[0.0, np.logspace(-8.0, 0.0, 65)]
    high_edges = np.arange(1.0 + high_step, y_max + 0.5 * high_step, high_step)
    edges = np.r_[low_edges, high_edges]
    if edges[-1] < y_max:
        edges = np.r_[edges, y_max]
    elif edges[-1] > y_max:
        edges[-1] = y_max

    xg, wg = leggauss(quad_order)
    a = edges[:-1]
    b = edges[1:]
    center = 0.5 * (a + b)
    half = 0.5 * (b - a)

    y = (center[:, None] + half[:, None] * xg[None, :]).ravel()
    w = (half[:, None] * wg[None, :]).ravel()
    return y, w


@lru_cache(maxsize=96)
def _build_spectrum_cached(
    sigma_key: float,
    beta_key: float,
    n_modes: int,
    x_max: float,
    x_step: float,
    quad_order: int,
) -> _Spectrum:
    """Precompute the modal spectrum on the scaled Hankel coordinate x.

    Neuman's real-time integral contains J0(y*sqrt(beta)).  Integrating directly
    in y requires a beta-dependent upper limit that becomes enormous for small
    beta.  The substitution x=y*sqrt(beta) keeps the Bessel oscillations on a
    fixed numerical scale and is essential for robust small-beta calculations.
    """
    sigma = float(sigma_key)
    beta = float(beta_key)

    x, wx = _quadrature_nodes(x_max, x_step, quad_order)
    y = x / math.sqrt(beta)
    gamma0, gamman = _gamma_roots_for_nodes(y, sigma, n_modes)

    y2 = y * y
    g02 = gamma0 * gamma0
    gn2 = gamman * gamman

    # Neuman (1975), eq. (2), evaluated with the root relation (4) to
    # avoid cancellation when gamma0 is close to y.
    tanh0 = np.tanh(gamma0)
    a0 = sigma * gamma0 * tanh0  # y^2 - gamma0^2
    den0_inner = (
        (2.0 + sigma) * g02
        + a0
        - sigma * g02 * tanh0 * tanh0
    )
    den0 = den0_inner * gamma0
    c0 = tanh0 / den0

    # Neuman (1975), eq. (3).  y^2+gamma_n^2 is a sum (not a
    # cancellation), so form it directly.  The root equation then gives
    # tan(gamma_n)=-(y^2+gamma_n^2)/(sigma*gamma_n), which remains stable
    # even when gamma_n lies extremely close to (n-1/2)pi.
    an = y2[None, :] + gn2
    tan_n = -an / (sigma * gamman)
    den_n_inner = (
        y2[None, :]
        - (1.0 + sigma) * gn2
        - (an * an) / sigma
    )
    den_n = den_n_inner * gamman
    cn = tan_n / den_n

    # Eq. (1) after x=y*sqrt(beta):
    #   4*y*J0(y*sqrt(beta))*dy = 4*x/beta*J0(x)*dx.
    hankel_weight = (4.0 * x / beta) * j0(x) * wx

    for array in (hankel_weight, c0, a0, cn, an):
        array.setflags(write=False)

    return _Spectrum(hankel_weight, c0, a0, cn, an)

def _default_mode_count(beta: float) -> int:
    """Choose a conservative number of vertical eigenmodes for beta.

    The modal series converges more slowly for small beta.  The thresholds are
    deliberately conservative for the beta range used in Neuman type curves and
    in the educational app.  Very small beta values are uncommon in the app but
    are supported for validation and field applications.
    """
    beta = float(beta)
    if beta < 1.0e-3:
        return 120
    if beta < 3.0e-3:
        return 64
    if beta < 2.0e-2:
        return 36
    if beta < 1.0e-1:
        return 24
    return 16


def _spectrum(
    sigma: float,
    beta: float,
    *,
    n_modes: int,
    x_max: Optional[float],
    x_step: float,
    quad_order: int,
) -> _Spectrum:
    # Rounding makes cache hits robust to harmless binary floating-point noise.
    sigma_key = round(float(sigma), 14)
    beta_key = round(float(beta), 14)

    # x must cover both the Bessel oscillations and a minimum physical extent
    # in the original y coordinate.  The latter matters for larger beta.
    if x_max is None:
        x_max_value = max(150.0, 300.0 * math.sqrt(beta))
    else:
        x_max_value = float(x_max)

    return _build_spectrum_cached(
        sigma_key,
        beta_key,
        int(n_modes),
        x_max_value,
        float(x_step),
        int(quad_order),
    )

def _dimensionless_derivative(
    t_s,
    beta: float,
    spectrum: _Spectrum,
) -> np.ndarray:
    """Return d(s_D)/dln(t) from the analytically differentiated Eq. (1)."""
    t_s = np.atleast_1d(np.asarray(t_s, dtype=float))
    hankel = spectrum.hankel_weight

    out = np.empty(t_s.size, dtype=float)
    for i, ts in enumerate(t_s):
        z0 = beta * spectrum.a0 * ts
        modal = spectrum.c0 * z0 * np.exp(-z0)

        zn = beta * spectrum.an * ts
        modal = modal + np.sum(
            spectrum.cn * zn * np.exp(-zn),
            axis=0,
        )
        out[i] = np.sum(hankel * modal)

    # Tiny negative values can result from truncating an oscillatory integral at
    # extremely early times where the physical derivative is effectively zero.
    tiny = np.abs(out) < 2.0e-7
    out[tiny & (out < 0.0)] = 0.0
    return out


def _internal_ts_grid(
    ts_requested: np.ndarray,
    ts_anchor: float,
    points_per_decade: int,
) -> np.ndarray:
    """Dense logarithmic grid from the earliest request to a late anchor."""
    ts_min_req = float(np.min(ts_requested))
    ts_max = max(float(np.max(ts_requested)), float(ts_anchor))

    decades = max(0.0, math.log10(ts_max / ts_min_req))
    n = max(120, int(math.ceil(points_per_decade * decades)) + 1)
    dense = np.logspace(math.log10(ts_min_req), math.log10(ts_max), n)

    grid = np.unique(np.r_[dense, ts_requested, ts_anchor])
    grid.sort()
    return grid


def neuman_response(
    t,
    Q: float,
    T: float,
    S_a: float,
    S_y: float,
    r: float,
    beta: float,
    *,
    n_modes: Optional[int] = None,
    x_max: Optional[float] = None,
    x_step: float = 0.5,
    quad_order: int = 8,
    points_per_decade: int = 36,
    check_applicability: bool = True,
) -> NeumanResponse:
    """Compute the complete-penetration Neuman drawdown and ds/dln(t).

    Parameters use one consistent unit system.  In SI, for example, use t [s],
    Q [m3/s], T [m2/s], r [m].  S_a, S_y and beta are dimensionless.

    `beta` is the dimensionless Neuman parameter itself.  If K_h and K_v are
    available, use :func:`neuman_beta` or :func:`neuman_response_from_conductivities`.

    `n_modes=None` (default) selects a beta-dependent modal count.  Supplying an
    integer is mainly useful for convergence testing.

    The derivative is evaluated directly from the analytical time derivative of
    Neuman's integral.  Drawdown is recovered by cumulative integration in ln(t),
    which avoids numerical differentiation and the slowly convergent drawdown
    Hankel integral.
    """
    time = _validated_time(t)
    Q = _positive("Q", Q)
    T = _positive("T", T)
    S_a = _positive("S_a", S_a)
    S_y = _positive("S_y", S_y)
    r = _positive("r", r)
    beta = _positive("beta", beta)

    if S_a >= S_y:
        warnings.warn(
            "The classical Neuman delayed-yield model normally has S_a << S_y.",
            RuntimeWarning,
            stacklevel=2,
        )
    if check_applicability and S_y / S_a <= 10.0:
        warnings.warn(
            "S_y/S_a <= 10; the usual Neuman type-curve applicability condition "
            "is not well satisfied.",
            RuntimeWarning,
            stacklevel=2,
        )

    if n_modes is None:
        n_modes_value = _default_mode_count(beta)
    else:
        n_modes_value = int(n_modes)
        if n_modes_value < 4:
            raise ValueError("n_modes must be >= 4.")

    if x_max is not None and x_max <= 20.0:
        raise ValueError("x_max should be > 20 for the oscillatory Hankel integral.")
    if x_step <= 0.0 or quad_order < 4 or points_per_decade < 12:
        raise ValueError("Invalid numerical-resolution setting.")

    sigma = S_a / S_y
    t_s_req = T * time / (S_a * r * r)

    spec = _spectrum(
        sigma,
        beta,
        n_modes=n_modes_value,
        x_max=x_max,
        x_step=x_step,
        quad_order=quad_order,
    )

    # Recover drawdown by integrating the exact derivative *backward* from a
    # very-late-time Theis anchor.  This is substantially more stable than
    # integrating forward from t->0, where the truncated Hankel integral can
    # contain tiny oscillatory errors whose accumulated area becomes an
    # arbitrary drawdown offset.
    #
    # At late time the full Neuman solution tends to the Theis solution with
    # total storativity S_a + S_y.  In terms of t_y=Tt/(S_y r^2),
    # u_total=(1+sigma)/(4 t_y).
    t_y_req = sigma * t_s_req
    t_y_anchor = max(1.0e8, 10.0 * float(np.max(t_y_req)))
    t_s_anchor = t_y_anchor / sigma

    ts_grid = _internal_ts_grid(t_s_req, t_s_anchor, points_per_decade)
    dd_grid = _dimensionless_derivative(ts_grid, beta, spec)

    # The physical Neuman derivative is non-negative.  Tiny negative values can
    # occur only where the oscillatory integral is below numerical significance.
    dd_grid = np.maximum(dd_grid, 0.0)

    log_grid = np.log(ts_grid)
    dlog = np.diff(log_grid)
    segment_area = 0.5 * (dd_grid[:-1] + dd_grid[1:]) * dlog
    tail_integral = np.r_[np.cumsum(segment_area[::-1])[::-1], 0.0]

    u_total_anchor = (1.0 + sigma) / (4.0 * t_y_anchor)
    sD_anchor = float(exp1(u_total_anchor))
    sD_grid = sD_anchor - tail_integral

    # Requested t_s values were inserted into ts_grid, so interpolation merely
    # restores the original ordering.
    sD_req = np.interp(np.log(t_s_req), log_grid, sD_grid)
    dd_req = np.interp(np.log(t_s_req), log_grid, dd_grid)

    # In the vanishing early-time tail, use the confined/Theis asymptote
    # directly.  This avoids cancellation when s_D is many orders of magnitude
    # smaller than the late-time anchor.
    u_a_req = 1.0 / (4.0 * t_s_req)

    # Two safe early-time criteria are used.  The first handles the vanishing
    # Theis tail for every beta.  The second is important for very small beta:
    # in that limit many vertical modes are needed to reconstruct the confined
    # early response, even though the exact solution is already asymptotic to
    # Theis.  Using the asymptote before gravity drainage becomes significant
    # removes a slowly convergent modal tail without changing the physics.
    beta_ts_req = beta * t_s_req
    very_early = (
        (u_a_req >= 12.0)
        | ((beta_ts_req <= 1.0e-5) & (t_y_req <= 0.1))
    )
    if np.any(very_early):
        sD_req = np.asarray(sD_req)
        dd_req = np.asarray(dd_req)
        sD_req[very_early] = exp1(u_a_req[very_early])
        dd_req[very_early] = np.exp(-u_a_req[very_early])

    scale = Q / (4.0 * math.pi * T)
    drawdown = scale * sD_req
    derivative = scale * dd_req

    u_a = 1.0 / (4.0 * t_s_req)
    t_y = sigma * t_s_req
    u_y = 1.0 / (4.0 * t_y)

    return NeumanResponse(
        time=time.copy(),
        drawdown=drawdown,
        derivative_ln_time=derivative,
        u_a=u_a,
        u_y=u_y,
        beta=beta,
        storage_ratio=sigma,
        derivative_plateau=scale,
    )


def neuman_drawdown(
    t,
    Q: float,
    T: float,
    S_a: float,
    S_y: float,
    r: float,
    beta: float,
    **solver_options,
) -> np.ndarray:
    """Return Neuman drawdown."""
    return neuman_response(
        t=t, Q=Q, T=T, S_a=S_a, S_y=S_y, r=r, beta=beta,
        **solver_options,
    ).drawdown


def neuman_log_derivative(
    t,
    Q: float,
    T: float,
    S_a: float,
    S_y: float,
    r: float,
    beta: float,
    *,
    log_base: str = "e",
    **solver_options,
) -> np.ndarray:
    """Return ds/dln(t), or ds/dlog10(t) when log_base='10'."""
    d = neuman_response(
        t=t, Q=Q, T=T, S_a=S_a, S_y=S_y, r=r, beta=beta,
        **solver_options,
    ).derivative_ln_time

    if log_base in ("e", "ln", "natural"):
        return d
    if log_base in ("10", "log10"):
        return np.log(10.0) * d
    raise ValueError("log_base must be 'e'/'ln' or '10'/'log10'.")


def neuman_response_from_conductivities(
    t,
    Q: float,
    r: float,
    b: float,
    k_h: float,
    k_v: float,
    S_a: float,
    S_y: float,
    **solver_options,
) -> NeumanResponse:
    """Convenience wrapper using T=K_h*b and beta=r^2 K_v/(b^2 K_h)."""
    b = _positive("b", b)
    k_h = _positive("k_h", k_h)
    k_v = _positive("k_v", k_v)
    T = k_h * b
    beta = neuman_beta(r=r, b=b, k_h=k_h, k_v=k_v)
    return neuman_response(
        t=t,
        Q=Q,
        T=T,
        S_a=S_a,
        S_y=S_y,
        r=r,
        beta=beta,
        **solver_options,
    )


def clear_spectrum_cache() -> None:
    """Clear cached sigma-dependent spectral quadrature data."""
    _build_spectrum_cached.cache_clear()


__all__ = [
    "NeumanResponse",
    "neuman_beta",
    "neuman_u_a",
    "neuman_u_y",
    "neuman_response",
    "neuman_drawdown",
    "neuman_log_derivative",
    "neuman_response_from_conductivities",
    "clear_spectrum_cache",
]
