"""Integration checks for the three teaching stages and unchanged state model.

CODE MAP — refresh with python scripts/update_code_index.py
  L0025  check
  L0030  host
  L0043  test_start_autoplays_complete_preserves_both_plots_and_reset
  L0073  test_guided_fixed_and_no_display_options
  L0087  test_new_sample_explicit_seed_language_pending_geometry_and_export
  L0120  test_natural_completion_keeps_final_plots_and_source_state
  L0137  test_selected_particle_clamps_when_cohort_shrinks
  L0150  test_launchers_and_sidebar_destination_smoke
  L0158  test_pause_seek_and_resume_keep_the_same_calculated_run
  L0172  test_rows_background_step_and_merged_repeat_controls
  L0198  test_main_rerun_creates_new_sample_but_play_replays
END CODE MAP
"""
from pathlib import Path
import time
import numpy as np
import pytest
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]


def check(at):
    assert not at.exception,[e.message for e in at.exception]
    return at


def host(page='pinboard'):
    entry={'guided':'principles','pinboard':'render_pinboard','explore':'render_page'}[page]
    text='''import streamlit as st
from dispersion_lab.navigation import language_selector
from dispersion_lab.ui import render_page,render_pinboard
from dispersion_lab.pages import principles
st.set_page_config(layout="centered")
language_selector()
'''+entry+'()'
    return check(AppTest.from_string(text,default_timeout=40).run())


@pytest.mark.parametrize('page',['guided','pinboard','explore'])
def test_start_autoplays_complete_preserves_both_plots_and_reset(page):
    at=host(page);key='disp_'+page
    assert 'run' not in at.session_state[key]
    assert at.number_input(key=key+'_highlighted').value==1
    images=[m.value for m in at.markdown if 'class="dispersion-plot"' in m.value]
    assert len(images)==2 and 'Transport board ready' in images[1]
    assert not any(b.key==key+'_play' for b in at.button)
    check(at.button(key=key+'_run').click().run())
    state=at.session_state[key]
    assert state['playing']
    assert at.button(key=key+'_run').label=='Rerun highlighted particles'
    assert state['play_seconds']==(60 if page=='explore' else 8)
    assert at.button(key=key+'_play').disabled
    assert not at.button(key=key+'_pause').disabled
    assert at.button(key=key+'_step').disabled and at.button(key=key+'_previous').disabled
    check(at.button(key=key+'_complete').click().run())
    assert state['fraction']==1 and not state['playing']
    images=[m.value for m in at.markdown if 'class="dispersion-plot"' in m.value]
    assert len(images)==3
    assert 'Transport board' in images[1] and 'Outlet distributions' in images[2]
    check(at.button(key=key+'_reset').click().run())
    assert state['fraction']==0
    check(at.button(key=key+'_step').click().run())
    assert state['fraction']*state['run'].end_time==pytest.approx(state['run'].times[0,1])
    check(at.button(key=key+'_previous').click().run())
    assert state['fraction']==0
    assert at.button(key=key+'_previous').disabled
    assert at.button(key=key+'_reset').label=='Start'


def test_guided_fixed_and_no_display_options():
    at=host('guided')
    check(at.button(key='disp_guided_run').click().run())
    run=at.session_state['disp_guided']['run']
    assert run.config.rows==20 and run.config.mode=='regular'
    np.testing.assert_array_equal(run.arrival,[20.])
    assert len(at.number_input)==1
    assert not at.slider  # Live progress is read-only; seeking is available when paused.
    assert not at.checkbox
    assert len(at.latex)==5
    assert not any(b.key in {'disp_guided_'+x for x in ('save','clear','new','csv','json')} for b in at.button)
    assert not at.get('download_button')


def test_new_sample_explicit_seed_language_pending_geometry_and_export():
    at=host();key='disp_pinboard'
    check(at.selectbox(key=key+'_mode').select('variable').run())
    check(at.number_input(key=key+'_highlighted').set_value(10).run())
    check(at.button(key=key+'_run').click().run())
    original=at.session_state[key]['run']
    check(at.number_input(key=key+'_background_each').set_value(1000).run())
    assert not any(b.key==key+'_play' for b in at.button)
    check(at.button(key=key+'_run').click().run())
    state=at.session_state[key];run=state['run']
    assert run.config.particles==10010
    assert run.config.seed==original.config.seed+1
    assert not np.array_equal(original.paths,run.paths[:10])
    # An explicitly selected earlier seed reproduces its highlighted paths.
    check(at.number_input(key=key+'_seed').set_value(original.config.seed).run())
    check(at.button(key=key+'_run').click().run())
    run=state['run']
    np.testing.assert_array_equal(original.times,run.times[:10])
    np.testing.assert_array_equal(original.paths,run.paths[:10])
    check(at.button(key=key+'_complete').click().run())
    check(at.button(key='lang_de').click().run())
    assert state['fraction']==1 and not state['playing']
    check(at.button(key=key+'_save').click().run())
    assert state['baseline'] is run
    check(at.slider(key=key+'_rows').set_value(40).run())
    assert state['run'] is run and not state['playing']
    assert len([m for m in at.markdown if 'class="dispersion-plot"' in m.value])==2
    check(at.button(key=key+'_run').click().run())
    assert state['run'].config.rows==40
    check(at.button(key='lang_fr').click().run())
    assert state['settings']['rows']==40


def test_natural_completion_keeps_final_plots_and_source_state():
    at=host('explore');key='disp_explore'
    check(at.button(key=key+'_run').click().run())
    state=at.session_state[key]
    state['wall_start']=time.monotonic()-100
    check(at.run())
    assert state['fraction']==1 and not state['playing']
    assert len([m for m in at.markdown if 'class="dispersion-plot"' in m.value])==3
    original=state['run']
    check(at.button(key=key+'_save').click().run())
    check(at.button(key=key+'_new').click().run())
    assert state['playing'] and state['run'].config.seed==original.config.seed+1
    np.testing.assert_array_equal(original.network.grains,state['run'].network.grains)
    assert state['baseline'] is original and state['fraction']<1
    assert not np.array_equal(original.paths,state['run'].paths)


def test_selected_particle_clamps_when_cohort_shrinks():
    at=host();key='disp_pinboard'
    check(at.number_input(key=key+'_highlighted').set_value(10).run())
    check(at.button(key=key+'_run').click().run())
    check(at.button(key=key+'_pause').click().run())
    check(at.selectbox(key=key+'_selected').select(10).run())
    check(at.number_input(key=key+'_highlighted').set_value(1).run())
    check(at.button(key=key+'_run').click().run())
    assert at.session_state[key]['selected']==1
    check(at.button(key=key+'_pause').click().run())
    check(at.button(key=key+'_step').click().run())


def test_launchers_and_sidebar_destination_smoke():
    at=check(AppTest.from_file(str(ROOT/'app.py'),default_timeout=40).run())
    assert at.button(key='nav_pinboard')
    check(at.button(key='nav_principles').click().run())
    assert at.title[0].value=='Principles and guided experiment'
    check(AppTest.from_file(str(ROOT/'multipage_example.py'),default_timeout=40).run())


def test_pause_seek_and_resume_keep_the_same_calculated_run():
    at=host('guided');key='disp_guided'
    check(at.button(key=key+'_run').click().run())
    state=at.session_state[key];run=state['run']
    check(at.button(key=key+'_pause').click().run())
    assert not state['playing']
    check(next(s for s in at.slider if s.key.startswith(key+'_seek_')).set_value(50.).run())
    assert state['fraction']==.5 and not state['playing']
    check(at.button(key=key+'_play').click().run())
    assert state['playing'] and state['fraction']>=.5
    assert state['run'] is run


@pytest.mark.parametrize('page',['pinboard','explore'])
def test_rows_background_step_and_merged_repeat_controls(page):
    at=host(page);key='disp_'+page
    assert [e.label for e in at.expander][:3]==['How to use this experiment','Board and transport','Particles and injection plan']
    assert at.slider(key=key+'_rows').value==20
    assert at.slider(key=key+'_rows').max==40
    assert at.number_input(key=key+'_background_each').step==50
    check(at.number_input(key=key+'_highlighted').set_value(10).run())
    check(at.button(key=key+'_run').click().run())
    check(at.button(key=key+'_complete').click().run())
    state=at.session_state[key];old=state['run']
    check(at.button(key=key+'_save').click().run())
    check(at.button(key=key+'_new').click().run())
    assert state['playing'] and state['run'].config.seed==old.config.seed+1
    assert state['baseline'] is old
    assert state['run'].config.particles==10
    assert not np.array_equal(state['run'].paths,old.paths)
    expanders=[e for e in at.expander if e.label=='Repeat, compare, and download']
    assert len(expanders)==1
    assert {b.key for b in expanders[0].button}=={key+'_save',key+'_clear',key+'_new'}
    if page=='explore':
        check(at.button(key=key+'_pause').click().run())
        assert 'Pressure potential (Pa)' in at.dataframe[-1].value.columns
        assert 'Next connection time (s)' in at.dataframe[-1].value.columns


@pytest.mark.parametrize('page',['guided','pinboard','explore'])
def test_main_rerun_creates_new_sample_but_play_replays(page):
    at=host(page);key='disp_'+page
    check(at.number_input(key=key+'_highlighted').set_value(10).run())
    assert at.button(key=key+'_run').label=='Run highlighted particles'
    check(at.button(key=key+'_run').click().run())
    state=at.session_state[key];old=state['run'];token=state['run_token']
    check(at.button(key=key+'_complete').click().run())
    check(at.button(key=key+'_play').click().run())
    assert state['run'] is old and state['run_token']==token
    check(at.button(key=key+'_run').click().run())
    new=state['run']
    assert state['playing'] and state['run_number']==2
    assert new.config.seed==old.config.seed+1 and state['run_token']!=token
    assert not np.array_equal(old.paths,new.paths)
    assert len([m for m in at.markdown if 'class="dispersion-plot"' in m.value])==3
    assert any('class="dispersion-preview"' in m.value and 'width:80%' in m.value for m in at.markdown)
    np.testing.assert_array_equal(old.xy,new.xy)
    if page!='guided':assert at.number_input(key=key+'_seed').value==new.config.seed
