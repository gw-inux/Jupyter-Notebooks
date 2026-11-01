"""Experiment staging without modifying the transport engine.

CODE MAP — refresh with python scripts/update_code_index.py
  L0017  realization_config
  L0029  particle_count
  L0037  Preview
  L0044  prepare_board
  L0054  with_background
  L0065  step_fraction
END CODE MAP
"""
from dataclasses import dataclass, replace
import numpy as np
from .model import Config, Network, Run, board_geometry, build_network, simulate


def realization_config(config: Config, previous: Config | None) -> Config:
    """Use the chosen seed initially, and a fresh seed when repeating it.

    An explicitly changed seed is respected. Otherwise advance deterministically,
    making a new sample reproducible without changing the numerical RNG streams.
    Different samples can still share an outlet or even a complete trajectory.
    """
    if previous is not None and config.seed==previous.seed:
        return replace(config,seed=(config.seed+1)%1_000_001)
    return config


def particle_count(highlighted: int, background_each: int) -> int:
    for value, lo, hi in ((highlighted, 1, 10), (background_each, 0, 1000)):
        if not isinstance(value, (int, np.integer)) or not lo <= value <= hi:
            raise ValueError("Use 1–10 highlighted and 0–1000 background particles each.")
    return int(highlighted * (1 + background_each))


@dataclass
class Preview:
    config: Config
    xy: np.ndarray
    edges: np.ndarray
    network: Network | None


def prepare_board(config: Config) -> Preview:
    """Geometry and steady water flow only; no solute trajectories are generated."""
    config.validate()
    if config.mode == "grains":
        net = build_network(config)
        return Preview(config, net.xy, net.edges, net)
    xy, edges, _ = board_geometry(config.rows, config.spacing_mm * 1e-3)
    return Preview(config, xy, edges, None)


def with_background(run: Run, highlighted: int, background_each: int) -> Run:
    """Prefix-stable random streams retain the first highlighted trajectories.

    All particles are independent equal-mass samples, not copies of a highlighted
    route. Recomputing with the same seed makes addition/removal reproducible.
    """
    if highlighted > run.config.particles:
        raise ValueError("Highlighted particles must already exist in the run.")
    return simulate(replace(run.config, particles=particle_count(highlighted, background_each)))


def step_fraction(run: Run, fraction: float, selected: int, direction: int) -> float:
    """Previous/next event of one selected marker, including injection and outlet.

    At a node, step strictly to an earlier/later event. Between nodes, step to
    the preceding/following node. Keep the complete-run clock and guard endpoints.
    """
    if direction not in (-1,1):
        raise ValueError("Step direction must be -1 or +1.")
    events=run.times[selected]
    events=events[np.isfinite(events)]
    current=fraction*run.end_time
    tolerance=1e-10*max(1.,run.end_time)
    if direction>0:
        future=events[events>current+tolerance]
        return min(1.,float(future[0])/run.end_time) if len(future) else 1.
    past=events[events<current-tolerance]
    return max(0.,float(past[-1])/run.end_time) if len(past) else 0.
