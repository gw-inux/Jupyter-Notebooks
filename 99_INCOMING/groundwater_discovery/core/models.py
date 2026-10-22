"""Pure teaching geometry. Beach coordinates are illustrative, not observations.

The separate optional coastal model is in core.coastal.
"""

import numpy as np

BEACH_GROUND_SLOPE = 0.020
BEACH_WATER_SLOPE = 0.002
# Seven stops, retaining the three original positions and their saved keys.
POSITIONS = {
    "near": 3.0,
    "position_2": 16 / 3,
    "position_3": 23 / 3,
    "middle": 10.0,
    "position_5": 38 / 3,
    "position_6": 46 / 3,
    "inland": 18.0,
}
DEPTHS = {"shallow": 0.08, "deeper": 0.26}
LENS_LEVELS = {"lower": 0.2, "medium_low": 0.4, "medium_high": 0.6, "higher": 0.8}


def cup_dimensions(bulk_ml):
    """Drawing dimensions whose product is proportional to total volume.

    Both dimensions scale with sqrt(V / 250 mL), so colored AREA represents
    volume. These are graphical dimensions, not physical cup measurements.
    At zero volume both dimensions are zero; no empty capacity outline exists.
    """
    if not np.isfinite(bulk_ml) or not 0 <= bulk_ml <= 1000:
        raise ValueError("Require a sample between 0 and 1000 mL.")
    scale = np.sqrt(bulk_ml / 250.0)
    return 1.15 * scale, 1.25 * scale


def sample_volumes(bulk_ml, solid_ml):
    """Volume accounting; an empty sample has no defined porosity.

    Solids exclude all pores. Water displacement approximates this for clean,
    non-absorbent grains with no internal porosity and no trapped air.
    """
    if not np.isfinite([bulk_ml, solid_ml]).all() or not 0 <= solid_ml <= bulk_ml:
        raise ValueError("Require 0 <= solid volume <= bulk volume.")
    pore_ml = bulk_ml - solid_ml
    return pore_ml, None if bulk_ml == 0 else pore_ml / bulk_ml


def cycle_head(x):
    """Prescribed conceptual head, flat at the divide (x=0), sink at x=7.

    This is drawing geometry, not a calibrated recharge/flow computation.
    Its derivative is -0.8*x/49: zero at the divide, negative toward the sea.
    """
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all() or np.any((x < 0) | (x > 7)):
        raise ValueError("x outside conceptual catchment.")
    return 1.4 + 0.4 * (1 - (x / 7) ** 2)


def porosity(bulk_ml, water_ml):
    if (
        not np.isfinite([bulk_ml, water_ml]).all()
        or bulk_ml <= 0
        or not 0 <= water_ml <= bulk_ml
    ):
        raise ValueError(
            "Require positive bulk volume and 0 <= pore water <= bulk volume."
        )
    return water_ml / bulk_ml


def beach_hole(x, depth):
    """Prescribed modest slopes; NOT a hydraulic solution or Sopot calibration.

    Horizontal and vertical coordinates use a consistent internal length unit.
    Display deliberately omits numbers and exaggerates the vertical direction.
    """
    if not np.isfinite([x, depth]).all() or not 1 <= x <= 20 or depth < 0:
        raise ValueError("Invalid hole position/depth.")
    ground = BEACH_GROUND_SLOPE * x
    water = BEACH_WATER_SLOPE * x
    bottom = ground - depth
    return ground, water, bottom, max(0.0, water - bottom)


def grain_centres(rows=5, columns=9, a=0.5, b=0.28):
    """Affine image of touching equal-circle hexagonal packing.

    Tangency: ((dx/a)**2+(dy/b)**2)**.5 == 2 for nearest neighbours.
    Ellipses share orientation; this is a conceptual section, not a porosity model.
    """
    return np.array(
        [
            (a + 2 * a * c + (a if r % 2 else 0), b + np.sqrt(3) * b * r)
            for r in range(rows)
            for c in range(columns)
        ]
    )


def density_ratio(rho_f=1000.0, rho_s=1025.0):
    if not np.isfinite([rho_f, rho_s]).all() or not 0 < rho_f < rho_s:
        raise ValueError("Require 0 < freshwater density < saltwater density.")
    return rho_f / (rho_s - rho_f)


def lens_profile(x, peak_head=0.5, half_width=100.0, rho_s=1025.0):
    """Ideal symmetric strip-island equilibrium profile; depth positive down.

    h=h_max sqrt(1-(x/L)^2); z=alpha*h. Uniform recharge, Dupuit/sharp-interface
    approximation, no limiting shallow base. Changing h_max is NOT a pumping
    calculation. The land surface is a separate geometric illustration.
    """
    x = np.asarray(x, dtype=float)
    alpha = density_ratio(rho_s=rho_s)
    if (
        not np.isfinite([peak_head, half_width]).all()
        or peak_head < 0
        or half_width <= 0
    ):
        raise ValueError("Invalid lens parameters.")
    if not np.isfinite(x).all() or np.any(np.abs(x) > half_width):
        raise ValueError("x outside island.")
    h = peak_head * np.sqrt(np.maximum(0, 1 - (x / half_width) ** 2))
    return h, alpha * h


def island_surface(x, half_width=100.0):
    x = np.asarray(x, dtype=float)
    return 3 * np.sqrt(np.maximum(0, 1 - (x / half_width) ** 2))
