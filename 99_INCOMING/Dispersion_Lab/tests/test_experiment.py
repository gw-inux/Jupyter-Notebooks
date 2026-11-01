"""Cohort invariants, preview isolation, original-kernel regression, translations.

CODE MAP — refresh with python scripts/update_code_index.py
  L0027  test_background_retains_entire_highlighted_paths
  L0044  test_preview_contains_no_transport_and_matches_actual_geometry
  L0062  test_fully_collected_highlighted_markers_still_visible
  L0072  test_cohort_limits
  L0076  test_soilwater_markdown_convention
  L0087  test_extended_pinboard_capacity_conserves_mass_and_prefix
  L0102  test_paused_steps_hit_adjacent_events_and_guard_endpoints
  L0120  test_grain_upward_and_slow_segments_follow_flow_without_stalling
  L0159  test_new_realization_seed_policy_and_explicit_reproduction
  L0175  test_grain_display_has_equal_physical_scales
END CODE MAP
"""
from dataclasses import replace
import numpy as np
import pytest
from dispersion_lab.model import Config,simulate,mass_counts
from dispersion_lab.experiment import prepare_board,particle_count,with_background,step_fraction,realization_config
from dispersion_lab.i18n import MD_ROOT,LANGUAGES,content,load_md
from dispersion_lab.plots import board_figure,preview_figure,empty_figure


@pytest.mark.parametrize('mode',['regular','variable','grains'])
@pytest.mark.parametrize('highlighted',[1,3,10])
def test_background_retains_entire_highlighted_paths(mode,highlighted):
    base=simulate(Config(mode=mode,particles=highlighted,injection_s=6.))
    expanded=with_background(base,highlighted,1000)
    for i in range(highlighted):
        a=np.isfinite(base.times[i]);b=np.isfinite(expanded.times[i])
        np.testing.assert_array_equal(base.times[i,a],expanded.times[i,b])
        np.testing.assert_array_equal(base.paths[i,a],expanded.paths[i,b])
    np.testing.assert_array_equal(base.release,expanded.release[:highlighted])
    np.testing.assert_array_equal(base.arrival,expanded.arrival[:highlighted])
    assert expanded.config.particles==highlighted*1001
    assert mass_counts(expanded,expanded.end_time)==(0,0,highlighted*1001)
    removed=with_background(expanded,highlighted,0)
    np.testing.assert_array_equal(removed.paths,base.paths)
    np.testing.assert_array_equal(removed.times,base.times)


@pytest.mark.parametrize('mode',['regular','variable','grains'])
def test_preview_contains_no_transport_and_matches_actual_geometry(mode):
    c=Config(mode=mode,particles=10,rows=5)
    preview=prepare_board(c);run=simulate(c)
    assert not hasattr(preview,'paths') and not hasattr(preview,'times')
    np.testing.assert_array_equal(preview.xy,run.xy)
    np.testing.assert_array_equal(preview.edges,run.edges)
    if mode=='grains':
        np.testing.assert_array_equal(preview.network.grains,run.network.grains)
        np.testing.assert_array_equal(preview.network.flow,run.network.flow)
    fig=preview_figure(preview,10)
    assert len([t for t in fig.axes[0].texts if t.get_text().isdigit()])==10
    fig.clear()
    empty=empty_figure(preview)
    assert not any(t.get_text().isdigit() for t in empty.axes[0].texts)
    assert empty.axes[0].get_aspect()==(1 if mode=='grains' else 2)
    empty.clear()


def test_fully_collected_highlighted_markers_still_visible():
    run=simulate(Config(particles=10))
    fig=board_figure(run,run.end_time,highlighted=10)
    labels=[a.get_text() for a in fig.axes[0].texts]
    ids={int(x) for label in labels if all(c.isdigit() or c==',' for c in label) for x in label.split(',')}
    assert ids==set(range(1,11))
    fig.clear()


@pytest.mark.parametrize('h,b',[(0,0),(11,0),(1,-1),(1,1001),(1.5,0)])
def test_cohort_limits(h,b):
    with pytest.raises(ValueError):particle_count(h,b)


def test_soilwater_markdown_convention(tmp_path):
    (tmp_path/'demo.md').write_text('English')
    (tmp_path/'demo_de.md').write_text('Deutsch')
    assert load_md(tmp_path,'demo.md','de')=='Deutsch'
    assert load_md(tmp_path,'demo.md','fr')=='English'
    assert list(LANGUAGES)==['en','de','it','es','pt','fr','zh','ar','hi']
    for name in ['start_01','start_02','guided_01','explore_01','activities','settings_map']+[f'theory_{i:02}' for i in range(1,7)]:
        assert len(content(name,'en'))>100 and len(content(name,'de'))>100
        assert content(name,'fr')==content(name,'en')

@pytest.mark.parametrize('mode',['regular','variable'])
def test_extended_pinboard_capacity_conserves_mass_and_prefix(mode):
    from dispersion_lab.model import mass_counts
    short=simulate(Config(mode=mode,rows=40,particles=10))
    full=with_background(short,10,1000)
    assert full.config.particles==10010
    np.testing.assert_array_equal(full.paths[:10],short.paths)
    np.testing.assert_array_equal(full.times[:10],short.times)
    assert mass_counts(full,full.end_time)==(0,0,10010)
    assert full.reference['variance_x']==pytest.approx(40e-6)
    assert full.reference['mean_transit']==40.
    if mode=='regular':
        np.testing.assert_array_equal(full.arrival,np.full(10010,40.))


@pytest.mark.parametrize('mode',['regular','variable','grains'])
def test_paused_steps_hit_adjacent_events_and_guard_endpoints(mode):
    run=simulate(Config(mode=mode,rows=20,particles=10,injection_s=6.))
    before=run.times.copy()
    for i in (0,9):
        events=run.times[i,np.isfinite(run.times[i])]/run.end_time
        assert step_fraction(run,0.,i,-1)==0.
        assert step_fraction(run,1.,i,1)==1.
        for k in range(1,len(events)-1):
            assert step_fraction(run,events[k],i,-1)==pytest.approx(events[k-1])
            assert step_fraction(run,events[k],i,1)==pytest.approx(events[k+1])
            mid=(events[k]+events[k+1])/2
            assert step_fraction(run,mid,i,-1)==pytest.approx(events[k])
            assert step_fraction(run,mid,i,1)==pytest.approx(events[k+1])
    np.testing.assert_array_equal(before,run.times)
    with pytest.raises(ValueError):step_fraction(run,0.,0,0)


@pytest.mark.parametrize('rows',[20,40])
def test_grain_upward_and_slow_segments_follow_flow_without_stalling(rows):
    """Exercise the reported behavior at the largest supported cohort.

    Ascending on the drawing is allowed; increasing pressure, repeated nodes,
    negative/zero time, interpolation stalls and internal termination are not.
    """
    from dispersion_lab.model import positions
    run=simulate(Config(mode='grains',rows=rows,particles=10010))
    net=run.network
    assert net.residual<1e-10 and net.imbalance<1e-10
    assert net.volume/net.inlet_flow==pytest.approx(run.reference['mean_transit'],rel=1e-10)
    upward=None;slow=None;longest=0.
    for i in range(run.config.particles):
        mask=np.isfinite(run.times[i]);path=run.paths[i,mask];times=run.times[i,mask]
        assert len(set(path))==len(path)
        assert path[-1] in net.outlets
        assert np.all(np.diff(net.pressure[path])<0)
        dt=np.diff(times)
        assert np.all(dt>0)
        up=np.flatnonzero(np.diff(run.xy[path,1])<0)
        if len(up):upward=(i,int(up[0]))
        k=int(np.argmax(dt))
        if dt[k]>longest:longest=float(dt[k]);slow=(i,k)
    assert upward is not None and slow is not None
    for i,k in (upward,slow):
        start,finish=run.xy[run.paths[i,k:k+2]]
        t0,t1=run.times[i,k:k+2]
        points=[]
        for fraction in (.25,.75):
            ids,point=positions(run,t0+fraction*(t1-t0),[i])
            assert ids.tolist()==[i]
            np.testing.assert_allclose(point[0],start+fraction*(finish-start),atol=1e-14)
            points.append(point[0])
        assert np.linalg.norm(points[1]-points[0])>0
    for t in (0.,run.end_time/2,run.end_time):
        assert sum(mass_counts(run,t))==10010
    assert mass_counts(run,run.end_time)==(0,0,10010)


def test_new_realization_seed_policy_and_explicit_reproduction():
    config=Config(seed=42,rows=20,particles=10)
    assert realization_config(config,None)==config
    fresh=realization_config(config,config)
    assert fresh.seed==43
    assert replace(fresh,seed=42)==config
    assert realization_config(replace(config,seed=100),config).seed==100
    assert realization_config(replace(config,seed=1000000),replace(config,seed=1000000)).seed==0
    old=simulate(config);new=simulate(fresh)
    assert not np.array_equal(old.paths,new.paths)
    reproduced=simulate(realization_config(config,fresh))
    np.testing.assert_array_equal(old.paths,reproduced.paths)
    np.testing.assert_array_equal(old.times,reproduced.times)


@pytest.mark.parametrize('rows',[2,20,40])
def test_grain_display_has_equal_physical_scales(rows):
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    board=prepare_board(Config(mode='grains',rows=rows))
    for fig in (preview_figure(board,10),empty_figure(board)):
        canvas=FigureCanvasAgg(fig)
        canvas.draw()
        transform=fig.axes[0].transData
        origin,x,y=transform.transform([(0,0),(1,0),(0,1)])
        assert np.linalg.norm(x-origin)==pytest.approx(np.linalg.norm(y-origin),rel=1e-12)
        injection=next(t for t in fig.axes[0].texts if t.get_text()=='Injection')
        for label in fig.axes[0].texts:
            if label.get_text().isdigit():
                assert not label.get_bbox_patch().get_window_extent(canvas.get_renderer()).overlaps(injection.get_window_extent(canvas.get_renderer()))
        fig.clear()
