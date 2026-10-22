"""Prescribed river/groundwater geometry for the introductory activity.

This is a connected, unconfined aquifer with negligible bed resistance and
negligible vertical head differences. It is NOT a groundwater-flow solver.
Coordinates use consistent internal length units; learners see no numeric axes.
The open inland boundary supplies water in the gaining case and receives it in
the losing case. There is no no-flow divide in this separate river example.
"""

from dataclasses import dataclass

import numpy as np

RIVER_BANK = 80.0
RIVER_LEVEL = 0.0
RIVER_BEND = 0.06  # Small prescribed curvature; not a recharge parameter.
# Seven equally spaced stops; existing semantic keys keep saved choices valid.
RIVER_POSITIONS = {
    "river_near": 74.0,
    "position_2": 197 / 3,
    "position_3": 172 / 3,
    "river_middle": 49.0,
    "position_5": 122 / 3,
    "position_6": 97 / 3,
    "river_inland": 24.0,
}
RIVER_DEPTHS = ("river_shallow", "river_level_depth", "river_deep")
RIVER_REGIMES = ("gaining", "losing")


def _land_coordinates(x):
    values = np.asarray(x, dtype=float)
    if not np.isfinite(values).all() or np.any((values < 0) | (values > RIVER_BANK)):
        raise ValueError("Position must be on the illustrated riverbank.")
    return values


def river_ground(x):
    """Gently rising terrain inland, with a short cut bank beside the river."""
    x = _land_coordinates(x)
    return (0.45 + 1.05 * (1 - x / RIVER_BANK) ** 0.7) * np.minimum(
        1, (RIVER_BANK - x) / 4
    )


def river_head(x, regime):
    """Gently curved head with unchanged end levels and exchange directions.

    The two profiles have opposite bends, steepening toward the water body.
    This near-bank shape is illustrative, not a calibrated flow solution or a
    universal curvature rule. Both profiles remain monotonic; the original
    observation choices retain their wet/dry outcomes.
    """
    x = _land_coordinates(x)
    if regime not in RIVER_REGIMES:
        raise ValueError("Unknown river exchange regime.")
    sign = 1.0 if regime == "gaining" else -1.0
    fraction = x / RIVER_BANK
    bend = 4 * RIVER_BEND * fraction * (1 - fraction)
    return RIVER_LEVEL + sign * (0.6 * (1 - fraction) + bend)


@dataclass(frozen=True)
class RiverObservation:
    ground: float
    head: float
    bottom: float
    water_depth: float


def river_observation(x, depth, regime):
    """Equilibrated water in a hypothetical hole; excavation effects omitted.

    A deeper hole reveals the SAME local water-table elevation. It does not
    pull the equilibrium level down to the bottom of the hole.
    """
    ground = float(river_ground(x))
    head = float(river_head(x, regime))
    if depth == "river_shallow":
        bottom = ground - 0.2
    elif depth == "river_level_depth":
        bottom = RIVER_LEVEL - 0.08
    elif depth == "river_deep":
        bottom = RIVER_LEVEL - 0.9
    else:
        raise ValueError("Unknown observation depth.")
    return RiverObservation(ground, head, bottom, max(0.0, head - bottom))
