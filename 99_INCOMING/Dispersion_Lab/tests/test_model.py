"""Independent scientific invariants and limiting-case checks.

Run from the package root: python -m pytest -q

CODE MAP — refresh with python scripts/update_code_index.py
  L0038  test_binomial_against_exhaustive_coin_paths
  L0051  test_mass_and_snapshot_partition
  L0066  test_zero_variability_is_regular_board
  L0074  test_source_duration_does_not_create_transit_variability
  L0080  test_random_walk_sample_matches_reference
  L0090  test_repeatability_and_export
  L0103  test_network_conservation_and_independent_volume_identity
  L0127  test_grain_clearance_for_every_plotted_route
  L0137  test_pressure_scaling_and_fixed_medium
  L0149  test_uniform_packing_scaling
  L0160  test_network_particle_sample_against_exact_moments
  L0169  test_plotted_complete_histogram_has_unit_area
  L0178  test_language_fallback_and_packaged_markdown
  L0192  test_invalid_input_rejected
  L0198  test_two_row_network_matches_closed_form_hydraulics_and_times
END CODE MAP
"""
from dataclasses import replace
from itertools import product
import csv
import io

import numpy as np
import pytest

from dispersion_lab.model import (Config, board_geometry, build_network, mass_counts,
                                  network_reference, particle_csv, pin_reference,
                                  positions, simulate)
from dispersion_lab.plots import distribution_figure
from dispersion_lab.i18n import content, load_md, ui_text


def test_binomial_against_exhaustive_coin_paths():
    n = 8
    paths = np.array(list(product([-1, 1], repeat=n)))
    x = paths.sum(axis=1)*.001
    counts = np.unique(x, return_counts=True)[1]/len(x)
    ref = pin_reference(Config(rows=n))
    np.testing.assert_allclose(ref["outlet_probability"], counts)
    assert ref["mean_x"] == pytest.approx(x.mean(), abs=1e-15)
    assert ref["variance_x"] == pytest.approx(x.var())


@pytest.mark.parametrize("mode", ["regular", "variable", "grains"])
@pytest.mark.parametrize("duration", [0., 50.])
def test_mass_and_snapshot_partition(mode, duration):
    run = simulate(Config(mode=mode, particles=100, injection_s=duration))
    for time in np.linspace(-1, run.end_time+1, 17):
        counts = mass_counts(run, time)
        assert sum(counts) == run.config.particles
        assert all(v >= 0 for v in counts)
        ids, xy = positions(run, time)
        assert len(ids) == counts[1]
        assert np.isfinite(xy).all()
        if len(xy):
            assert xy[:, 1].min() >= 0
            assert xy[:, 1].max() <= run.config.rows*run.config.spacing_mm*1e-3+1e-12
    assert mass_counts(run, run.end_time) == (0, 0, run.config.particles)


def test_zero_variability_is_regular_board():
    regular = simulate(Config())
    variable = simulate(Config(mode="variable", time_cv=0.))
    np.testing.assert_array_equal(regular.paths, variable.paths)
    np.testing.assert_array_equal(regular.times, variable.times)
    assert np.unique(regular.arrival).tolist() == [12.]


def test_source_duration_does_not_create_transit_variability():
    run = simulate(Config(injection_s=20., particles=10000))
    np.testing.assert_allclose(run.arrival-run.release, 12.)
    assert run.arrival.std() == pytest.approx(20/np.sqrt(12), rel=.02)


def test_random_walk_sample_matches_reference():
    run = simulate(Config(mode="variable", particles=10000))
    ref = run.reference
    assert abs(run.exit_x.mean()) < 5*np.sqrt(ref["variance_x"]/10000)
    assert run.exit_x.var() == pytest.approx(ref["variance_x"], rel=.05)
    assert run.arrival.mean() == pytest.approx(ref["mean_arrival"], rel=.015)
    assert run.arrival.var() == pytest.approx(ref["variance_arrival"], rel=.08)


@pytest.mark.parametrize("mode", ["regular", "variable", "grains"])
def test_repeatability_and_export(mode):
    c = Config(mode=mode, particles=10)
    one, two = simulate(c), simulate(c)
    np.testing.assert_array_equal(one.paths, two.paths)
    np.testing.assert_array_equal(one.times, two.times)
    rows = list(csv.DictReader(io.StringIO(particle_csv(one))))
    assert len(rows) == 10
    assert sum(float(r["mass_fraction"]) for r in rows) == pytest.approx(1.)
    for r, end in zip(rows, one.arrival):
        assert float(r["arrival_s"]) == end


@pytest.mark.parametrize("rows,packing,variation", [(2,.5,0.), (12,.75,.25), (20,.9,.4)])
def test_network_conservation_and_independent_volume_identity(rows, packing, variation):
    net = build_network(Config(mode="grains", rows=rows, packing=packing,
                               grain_variation=variation))
    assert net.imbalance < 1e-10
    assert net.residual < 1e-10
    assert np.all(net.radii > 0)
    ref = network_reference(net)
    assert ref["outlet_probability"].sum() == pytest.approx(1., abs=1e-12)
    assert ref["mean_transit"] == pytest.approx(net.volume/net.inlet_flow, rel=1e-10)
    # Independent outlet flux calculation, not recursion through probabilities.
    outlet_q = np.zeros(len(net.xy))
    for (i,j), q in zip(net.edges, net.flow):
        outlet_q[i] -= q
        outlet_q[j] += q
    np.testing.assert_allclose(ref["outlet_probability"],
                               outlet_q[net.outlets]/net.inlet_flow, rtol=1e-9, atol=1e-12)
    for u, branches in enumerate(net.outgoing):
        if branches:
            assert sum(p for _,p,_ in branches) == pytest.approx(1.)
        for v, p, dt in branches:
            assert net.pressure[u] > net.pressure[v]
            assert p > 0 and dt > 0


def test_grain_clearance_for_every_plotted_route():
    net = build_network(Config(mode="grains", packing=.9, grain_variation=.4))
    centres, radii = net.grains[:,:2], net.grains[:,2]
    for i,j in net.edges:
        start, delta = net.xy[i], net.xy[j]-net.xy[i]
        fraction = np.clip((centres-start)@delta/(delta@delta), 0, 1)
        distances = np.linalg.norm(centres-(start+fraction[:,None]*delta), axis=1)
        assert np.all(distances > radii)


def test_pressure_scaling_and_fixed_medium():
    c = Config(mode="grains", particles=250, injection_s=10.)
    a, b = simulate(c), simulate(replace(c, pressure_pa=2*c.pressure_pa))
    np.testing.assert_array_equal(a.paths, b.paths)
    np.testing.assert_array_equal(a.release, b.release)
    np.testing.assert_allclose(a.arrival-a.release, 2*(b.arrival-b.release))
    np.testing.assert_allclose(b.network.flow, 2*a.network.flow)
    other = simulate(replace(c, seed=43))
    np.testing.assert_array_equal(a.network.grains, other.network.grains)
    assert not np.array_equal(a.paths, other.paths)


def test_uniform_packing_scaling():
    c = Config(mode="grains", grain_variation=0., packing=.6)
    a, b = build_network(c), build_network(replace(c, packing=.8))
    # The pore radii halve; flow decreases by 16; transit time increases by 4.
    np.testing.assert_allclose(b.radii, a.radii/2)
    np.testing.assert_allclose(b.flow, a.flow/16, rtol=1e-10)
    ra, rb = network_reference(a), network_reference(b)
    assert rb["mean_transit"] == pytest.approx(4*ra["mean_transit"])
    np.testing.assert_allclose(ra["outlet_probability"], rb["outlet_probability"])


def test_network_particle_sample_against_exact_moments():
    run = simulate(Config(mode="grains", particles=10000))
    ref = run.reference
    assert abs(run.arrival.mean()-ref["mean_arrival"]) < 5*np.sqrt(ref["variance_arrival"]/10000)
    assert run.arrival.var() == pytest.approx(ref["variance_arrival"], rel=.1)
    assert abs(run.exit_x.mean()-ref["mean_x"]) < 5*np.sqrt(ref["variance_x"]/10000)


@pytest.mark.parametrize("mode", ["regular", "variable", "grains"])
def test_plotted_complete_histogram_has_unit_area(mode):
    run = simulate(Config(mode=mode, particles=100))
    fig = distribution_figure(run, run.end_time, bins=33)
    area = sum(p.get_width()*p.get_height() for p in fig.axes[1].patches)
    assert area == pytest.approx(1.)
    assert sum(p.get_height() for p in fig.axes[0].patches) == pytest.approx(1.)
    fig.clear()


def test_language_fallback_and_packaged_markdown(tmp_path):
    for name in ("introduction", "activities", "theory", "scope"):
        assert len(content(name,"en")) > 100
        assert len(content(name,"de")) > 100
        assert content(name,"unknown") == content(name,"en")
    assert ui_text("Original", language="de") == "Original"
    (tmp_path/"demo.md").write_text("fallback", encoding="utf8")
    assert load_md(tmp_path, "demo.md", "de") == "fallback"
    with pytest.raises(ValueError):
        load_md(tmp_path, "../secret.md", "en")


@pytest.mark.parametrize("change", [{"rows":0},{"particles":0},{"time_cv":-1.},
                                   {"packing":1.},{"pressure_pa":float("nan")}])
def test_invalid_input_rejected(change):
    with pytest.raises(ValueError):
        simulate(replace(Config(), **change))


@pytest.mark.parametrize('packing,pressure',[(.5,.05),(.75,.5),(.9,2.)])
def test_two_row_network_matches_closed_form_hydraulics_and_times(packing,pressure):
    """Two identical inlet branches, each followed by two parallel outlet tubes.

    Kirchhoff gives P_middle=P_in/3, Q_in=4*g*P_in/3 and total transit
    4.5*V/(g*P_in). This checks throat radius/diameter, viscosity, length and
    branching factors independently of the general network solver/recursion.
    """
    c=Config(mode='grains',rows=2,particles=100,grain_variation=0.,packing=packing,pressure_pa=pressure)
    a=c.spacing_mm*1e-3
    radius=np.sqrt(2)*a*(1-packing)/2
    length=np.sqrt(2)*a
    conductance=np.pi*radius**4/(8*.001*length)
    volume=np.pi*radius**2*length
    expected=4.5*volume/(conductance*pressure)
    run=simulate(c);net=run.network
    np.testing.assert_allclose(net.radii,radius,rtol=1e-12)
    np.testing.assert_allclose(net.pressure[1:3],pressure/3,rtol=1e-12)
    assert net.inlet_flow==pytest.approx(4*conductance*pressure/3,rel=1e-12)
    assert run.reference['mean_transit']==pytest.approx(expected,rel=1e-12)
    np.testing.assert_allclose(run.arrival,expected,rtol=1e-12)
    np.testing.assert_allclose(np.diff(run.times,axis=1),np.tile([expected/3,2*expected/3],(100,1)),rtol=1e-12)
