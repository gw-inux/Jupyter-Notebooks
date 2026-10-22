"""Independent physical checks for the optional steady island comparison."""

import numpy as np
import pytest
from core.coastal import (
    ISLAND,
    Island,
    island_profile,
    pumping_limit,
    recharge_m_day,
    freshwater_volume,
    coastal_outflow,
)


def test_natural_geometry_pressure_balance_and_volume():
    a = ISLAND.radius_m
    assert np.pi * a * a == pytest.approx(1_000_000)
    r = np.linspace(0, a, 10001)
    for peak in np.arange(0.1, 1.01, 0.1):
        h, z = island_profile(r, peak)
        assert h[0] == pytest.approx(peak)
        assert h[-1] == z[-1] == 0
        np.testing.assert_allclose(ISLAND.rho_f * (h + z), ISLAND.rho_s * z, rtol=1e-14)
        # Independent midpoint integration over equal-area annuli.
        radial_mid = a * np.sqrt((np.arange(100000) + 0.5) / 100000)
        hm, zm = island_profile(radial_mid, peak)
        volume = np.mean(hm + zm) * ISLAND.area_m2 * ISLAND.porosity
        assert freshwater_volume(peak) == pytest.approx(volume, rel=2e-8)
        assert freshwater_volume(peak) == pytest.approx(8_200_000 * peak)


def test_pumping_lowers_head_raises_interface_and_reduces_store():
    a, rw = ISLAND.radius_m, ISLAND.well_radius_m
    for peak in [0.1, 0.4, 1.0]:
        previous_volume = freshwater_volume(peak)
        previous_h = float(island_profile(rw, peak)[0])
        for fraction in [0.1, 0.5, 1.0]:
            q = fraction * pumping_limit(peak)
            h, z = island_profile(np.geomspace(rw, a, 1001), peak, q)
            assert h[0] < previous_h
            assert h[0] >= 0.5 * float(island_profile(rw, peak)[0]) - 1e-12
            assert z[0] == pytest.approx(40 * h[0])
            assert h[-1] == z[-1] == 0
            volume = freshwater_volume(peak, q)
            assert 0 < volume < previous_volume
            previous_volume, previous_h = volume, h[0]
            # Independent high-resolution radial midpoint integration.
            edges = np.linspace(rw, a, 100001)
            r = (edges[1:] + edges[:-1]) / 2
            hm, zm = island_profile(r, peak, q)
            numerical = np.sum((hm + zm) * np.diff(np.pi * edges**2)) * ISLAND.porosity
            assert volume == pytest.approx(numerical, rel=2e-6)
        with pytest.raises(ValueError):
            island_profile([rw], peak, 1.01 * pumping_limit(peak))


def test_potential_satisfies_radial_recharge_and_boundary_budget():
    # Evaluate the divergence numerically, rather than repeating the profile formula.
    a = ISLAND.radius_m
    h0 = 0.7
    q = 0.5 * pumping_limit(h0)
    r = np.linspace(10, a - 10, 40001)
    h, _ = island_profile(r, h0, q)
    potential = 0.5 * ISLAND.conductivity_m_day * (1 + ISLAND.alpha) * h * h
    flux = -np.gradient(potential, r, edge_order=2)
    divergence = np.gradient(r * flux, r, edge_order=2) / r
    np.testing.assert_allclose(divergence[20:-20], recharge_m_day(h0), rtol=2e-4)
    total = 2 * np.pi * r * flux
    # Point-sink approximation: recharge inside a radius minus pumping.
    np.testing.assert_allclose(
        total[20:-20],
        np.pi * r[20:-20] ** 2 * recharge_m_day(h0) - q,
        rtol=2e-4,
        atol=2e-4,
    )
    assert coastal_outflow(h0, q) + q == pytest.approx(
        recharge_m_day(h0) * ISLAND.area_m2
    )
    assert coastal_outflow(h0, q) > 0


def test_invalid_model_inputs_are_rejected():
    for args in [
        {"area_m2": 0},
        {"porosity": 1},
        {"well_radius_m": 1000},
        {"rho_s": 999},
        {"conductivity_m_day": np.nan},
    ]:
        with pytest.raises(ValueError):
            Island(**args)
    for head in [0, -1, np.nan, np.inf]:
        with pytest.raises(ValueError):
            freshwater_volume(head)
    for radius in [[np.nan], [ISLAND.radius_m + 1]]:
        with pytest.raises(ValueError):
            island_profile(radius, 0.5)
    with pytest.raises(ValueError):
        island_profile([0], 0.5, -1)
