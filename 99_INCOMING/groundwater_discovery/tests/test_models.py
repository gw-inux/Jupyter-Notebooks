import numpy as np
import pytest
from core.models import (
    porosity,
    beach_hole,
    grain_centres,
    density_ratio,
    lens_profile,
    island_surface,
    POSITIONS,
    DEPTHS,
    BEACH_GROUND_SLOPE,
    BEACH_WATER_SLOPE,
    sample_volumes,
    cup_dimensions,
    cycle_head,
    LENS_LEVELS,
)


def test_porosity_and_invalid_measurements():
    assert porosity(400, 160) == 0.4
    for values in [(0, 0), (400, 401), (400, -1), (400, np.nan)]:
        with pytest.raises(ValueError):
            porosity(*values)


def test_ellipses_touch_without_overlap_and_are_horizontally_elongated():
    a, b = 0.5, 0.28
    xy = grain_centres(a=a, b=b)
    d = np.sqrt(np.sum(((xy[:, None] - xy[None, :]) / [a, b]) ** 2, axis=-1))
    np.fill_diagonal(d, np.inf)
    assert a > b
    assert np.min(d) >= 2 - 1e-12
    np.testing.assert_allclose(np.min(d, axis=1), 2, atol=1e-12)
    # Every grain belongs to one mechanically connected packing.
    seen = {0}
    while True:
        new = {j for i in seen for j in np.flatnonzero(np.isclose(d[i], 2))} | seen
        if new == seen:
            break
        seen = new
    assert len(seen) == len(xy)


@pytest.mark.parametrize("position", list(POSITIONS))
@pytest.mark.parametrize("depth", list(DEPTHS))
def test_beach_schematic_slope_and_hole_water(position, depth):
    x, d = POSITIONS[position], DEPTHS[depth]
    g, h, b, w = beach_hole(x, d)
    assert 0 < h < g
    assert h / x == pytest.approx(
        0.002
    )  # 0.2% prescribed, NOT calculated from recharge
    assert BEACH_WATER_SLOPE < BEACH_GROUND_SLOPE
    assert b == pytest.approx(g - d)
    assert w == pytest.approx(max(0, h - b))
    if w > 0:
        assert b + w == pytest.approx(h)


def test_beach_observation_outcomes():
    assert beach_hole(POSITIONS["near"], DEPTHS["shallow"])[3] > 0
    assert beach_hole(POSITIONS["middle"], DEPTHS["shallow"])[3] == 0
    assert beach_hole(POSITIONS["middle"], DEPTHS["deeper"])[3] > 0
    assert beach_hole(POSITIONS["inland"], DEPTHS["deeper"])[3] == 0
    for x, d in [(np.nan, 0.1), (0, 0.1), (21, 0.1), (3, -0.1)]:
        with pytest.raises(ValueError):
            beach_hole(x, d)


def test_lens_pressure_balance_land_and_fixed_comparison():
    x = np.linspace(-100, 100, 1001)
    for head in LENS_LEVELS.values():
        h, z = lens_profile(x, head)
        np.testing.assert_allclose(1000 * (h + z), 1025 * z, rtol=1e-14)
        np.testing.assert_allclose(h, h[::-1], atol=1e-14)
        assert np.all(h <= island_surface(x))
        assert h[0] == h[-1] == z[0] == z[-1] == 0
        assert np.all(z < 36)  # both profiles fit inside the SAME plot bounds
    assert lens_profile([0], 0.3)[1][0] < lens_profile([0], 0.7)[1][0]
    assert density_ratio() == 40
    with pytest.raises(ValueError):
        density_ratio(1000, 1000)
    with pytest.raises(ValueError):
        lens_profile([101])


def test_empty_and_invalid_sample_volumes_and_exact_cup_proportions():
    from core.figures import sample_cup

    assert sample_volumes(0, 0) == (0, None)
    assert sample_volumes(400, 240) == (160, 0.4)
    for invalid in [
        (0, 1),
        (-1, 0),
        (100, 101),
        (100, -1),
        (100, np.nan),
        (np.inf, 10),
    ]:
        with pytest.raises(ValueError):
            sample_volumes(*invalid)
    for bulk, solid in [
        (0, 0),
        (10, 6),
        (250, 150),
        (400, 240),
        (1000, 650),
        (900, 800),
        (500, 0),
        (500, 500),
    ]:
        fig = sample_cup(bulk, solid, lambda key: key)
        patches = {p.get_gid(): p for p in fig.axes[0].patches if p.get_gid()}
        if bulk == 0:
            assert not patches and not fig.axes[0].lines
            assert cup_dimensions(bulk) == (0, 0)
            continue
        s, p = patches["solid_volume"], patches["pore_volume"]
        assert s.get_width() == p.get_width()
        width, height = cup_dimensions(bulk)
        assert s.get_width() == width
        assert s.get_height() + p.get_height() == pytest.approx(height)
        assert p.get_y() == s.get_height()
        # A fixed area/volume scale; both dimensions grow, not just fill height.
        area_per_ml = 1.15 * 1.25 / 250
        assert s.get_width() * s.get_height() == pytest.approx(solid * area_per_ml)
        assert p.get_width() * p.get_height() == pytest.approx(
            (bulk - solid) * area_per_ml
        )
        assert p.get_height() / height == pytest.approx(sample_volumes(bulk, solid)[1])
    assert np.all(
        np.diff([cup_dimensions(v) for v in [10, 250, 500, 1000]], axis=0) > 0
    )
    for invalid in [-1, 1001, np.nan, np.inf]:
        with pytest.raises(ValueError):
            cup_dimensions(invalid)


def test_cycle_divide_has_zero_gradient_and_descends_to_surface_water():
    x = np.linspace(0, 7, 701)
    head = cycle_head(x)
    assert head[0] == pytest.approx(1.8)
    assert head[-1] == pytest.approx(1.4)
    assert np.all(np.diff(head) < 0)
    # Independent second-order one-sided derivative at the no-flow divide.
    dx = x[1] - x[0]
    assert (-3 * head[0] + 4 * head[1] - head[2]) / (2 * dx) == pytest.approx(
        0, abs=1e-12
    )
    ground = np.interp(x, [0, 2, 4, 6, 7], [2.2, 2.3, 2.0, 1.65, 1.4])
    assert np.all(head <= ground)
    for invalid in [[-1], [8], [np.nan]]:
        with pytest.raises(ValueError):
            cycle_head(invalid)
