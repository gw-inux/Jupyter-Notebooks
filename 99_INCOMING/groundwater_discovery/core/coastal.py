"""Steady circular-island teaching model, with explicit units and assumptions.

Combines Bakker & Post §6.1 (radial discharge potential) with §4.2
(unconfined sharp-interface potential). This is a Dupuit equilibrium model,
NOT the local, vertical-flow upconing solution in the supplied SFI module.
See SCIENTIFIC_NOTES.md for derivation, volume integration and limitations.
"""

from dataclasses import dataclass
import numpy as np
from core.models import density_ratio


@dataclass(frozen=True)
class Island:
    area_m2: float = 1_000_000.0
    porosity: float = 0.30
    conductivity_m_day: float = 5.0
    well_radius_m: float = 0.30
    rho_f: float = 1000.0
    rho_s: float = 1025.0

    def __post_init__(self):
        values = list(self.__dict__.values())
        if not np.isfinite(values).all() or not (
            self.area_m2 > 0
            and 0 < self.porosity < 1
            and self.conductivity_m_day > 0
            and 0 < self.well_radius_m < self.radius_m
        ):
            raise ValueError("Invalid island parameters.")
        density_ratio(self.rho_f, self.rho_s)

    @property
    def radius_m(self):
        return np.sqrt(self.area_m2 / np.pi)

    @property
    def alpha(self):
        return density_ratio(self.rho_f, self.rho_s)


ISLAND = Island()


def _head(head):
    if not np.isfinite(head) or head <= 0:
        raise ValueError("Natural maximum head must be positive.")


def recharge_m_day(peak_head, island=ISLAND):
    """Uniform recharge implied by natural maximum head, for fixed K and area."""
    _head(peak_head)
    return (
        2
        * island.conductivity_m_day
        * (1 + island.alpha)
        * peak_head**2
        / island.radius_m**2
    )


def pumping_limit(peak_head, island=ISLAND):
    """Teaching range: at most 75% of the mathematical zero-head discharge.

    This keeps well head at least half its unpumped value. It is a display
    constraint, never a safe yield, salinity threshold or regulatory limit.
    """
    _head(peak_head)
    radius, rw = island.radius_m, island.well_radius_m
    return (
        0.75
        * np.pi
        * island.conductivity_m_day
        * (1 + island.alpha)
        * peak_head**2
        * (1 - (rw / radius) ** 2)
        / np.log(radius / rw)
    )


def island_profile(radius, peak_head, pumping=0.0, island=ISLAND):
    """Head above sea and interface depth below sea [m], at radius |r|.

    Point-sink solution evaluated no closer than the finite well radius.
    The tiny well footprint is excluded from the pumped storage integral.
    No negative potentials are silently converted into a dry aquifer.
    """
    _head(peak_head)
    r = np.abs(np.asarray(radius, dtype=float))
    if not np.isfinite(r).all() or np.any(r > island.radius_m * (1 + 1e-12)):
        raise ValueError("Position outside island.")
    if not np.isfinite(pumping) or not 0 <= pumping <= pumping_limit(
        peak_head, island
    ) * (1 + 1e-12):
        raise ValueError("Pumping outside this teaching model's range.")
    if pumping:
        r = np.maximum(r, island.well_radius_m)
    scaled = np.minimum(r / island.radius_m, 1.0)
    h2 = peak_head**2 * (1 - scaled**2)
    if pumping:
        h2 += (
            pumping
            / (np.pi * island.conductivity_m_day * (1 + island.alpha))
            * np.log(scaled)
        )
    if np.any(h2 < -1e-12):
        raise ValueError("No freshwater equilibrium for these parameters.")
    h = np.sqrt(np.maximum(h2, 0))  # only round-off at the coastline
    return h, island.alpha * h


def freshwater_volume(peak_head, pumping=0.0, island=ISLAND):
    """Saturated freshwater PORE volume [m³], not extractable water/yield.

    Natural circular lens has mean thickness 2/3 of its central thickness.
    Pumped volume uses 128-point Gaussian quadrature over annular area;
    substitution r=R*sin(theta) resolves the square-root shoreline endpoint.
    """
    _head(peak_head)
    if pumping == 0:
        return 2 / 3 * island.porosity * island.area_m2 * (1 + island.alpha) * peak_head
    nodes, weights = np.polynomial.legendre.leggauss(128)
    lower, upper = np.arcsin(island.well_radius_m / island.radius_m), np.pi / 2
    theta = lower + (nodes + 1) * (upper - lower) / 2
    r = island.radius_m * np.sin(theta)
    h, z = island_profile(r, peak_head, pumping, island)
    integral = (
        np.sum(weights * (h + z) * r * island.radius_m * np.cos(theta))
        * (upper - lower)
        / 2
    )
    return 2 * np.pi * island.porosity * integral


def coastal_outflow(peak_head, pumping=0.0, island=ISLAND):
    """Recharge minus point-well discharge [m³/day]; steady mass balance."""
    island_profile([island.radius_m], peak_head, pumping, island)
    return recharge_m_day(peak_head, island) * island.area_m2 - pumping
