"""Regression checks for newly constrained inputs and linked coastal controls."""

from pathlib import Path
import warnings
import xml.etree.ElementTree as ET
import pytest
from streamlit.testing.v1 import AppTest
from core.coastal import pumping_limit
from core.i18n import TEXT, LANGUAGES
from core.figures import density_principle, browser_svg, prepare_fonts

ROOT = Path(__file__).resolve().parents[1]


def test_pumping_controls_clamp_and_survive_language_navigation():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=40).run()
    at.switch_page("content/lab.py").run()
    at.button(key="scenario_pumping").click().run()
    at.slider(key="lens_head").set_value(1.0).run()
    at.slider(key="pumping_rate").set_value(50.0).run()
    assert not at.exception
    assert len(at.metric) == 6
    assert float(at.metric[3].value.split()[0]) < 1.0
    assert at.metric[4].proto.delta.startswith("-")
    at.slider(key="lens_head").set_value(0.1).run()
    assert not at.exception
    q = at.slider(key="pumping_rate").value
    assert 0 < q <= pumping_limit(0.1)
    for lang in ["fa", "hi", "zh", "pt", "pl"]:
        at.button(key="lang_" + lang).click().run()
        assert not at.exception
        assert at.slider(key="lens_head").value == 0.1
        assert at.slider(key="pumping_rate").value == q
    at.switch_page("content/home.py").run()
    at.switch_page("content/lab.py").run()
    assert at.slider(key="pumping_rate").value == q
    at.button(key="scenario_natural").click().run()
    assert len(at.metric) == 3
    assert not any(s.key == "pumping_rate" for s in at.slider)
    at.button(key="scenario_pumping").click().run()
    assert at.slider(key="pumping_rate").value == q
    at.button(key="next_resources").click().run()
    assert TEXT["resources"]["pl"] in at.header[0].value
    assert not at.exception


def test_retained_legacy_volumes_are_clamped_before_widget_creation():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.session_state["activity_values"] = {"bulk_ml": 2000, "solid_ml": 1800}
    at.run()
    at.switch_page("content/pores.py").run()
    assert not at.exception
    assert [v.value for v in at.number_input] == [1000, 1000]
    at.number_input(key="bulk_ml").set_value(0).run()
    assert at.number_input(key="solid_ml").value == 0
    assert at.number_input(key="solid_ml").disabled
    assert not at.metric and not at.exception


@pytest.mark.parametrize("lang", ["hi", "zh", "fa", "ar"])
def test_new_script_figures_have_no_missing_glyph_warnings(lang):
    fig = density_principle(lambda key: TEXT[key][lang])
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        svg = browser_svg(fig)
    assert not [w for w in seen if "missing from font" in str(w.message)]
    root = ET.fromstring(svg)
    assert not root.findall(".//{http://www.w3.org/2000/svg}script")
    if lang == "hi":
        assert "data:font/ttf;base64," in svg
        assert 'lang="hi"' in svg
    if lang == "fa":
        assert "direction: rtl" in svg
    fig.clear()


def test_all_expanders_have_localised_open_close_cue():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    for lang in LANGUAGES:
        at.button(key="lang_" + lang).click().run()
        assert not at.exception
        assert all(TEXT["open_close"][lang] in e.label for e in at.expander)
