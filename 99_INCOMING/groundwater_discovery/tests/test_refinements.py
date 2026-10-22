"""Regressions for the draft notice, media, and interchangeable cup controls."""

from pathlib import Path

import numpy as np
import pytest
from PIL import Image
from streamlit.testing.v1 import AppTest

from core.figures import river
from core.i18n import LANGUAGES, TEXT
from core.river import river_head
from core.sources import REVIEW_URL, CHERRY_VIDEO_URL, CHERRY_START_SECONDS

ROOT = Path(__file__).resolve().parents[1]


def app():
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()


@pytest.mark.parametrize("lang", list(LANGUAGES))
def test_cup_modes_preserve_whole_ml_values_and_navigation(lang):
    at = app()
    at.button(key="lang_" + lang).click().run()
    at.switch_page("content/pores.py").run()
    assert not at.exception
    assert at.number_input(key="bulk_ml").value == 0
    assert at.number_input(key="bulk_ml").proto.format == "%d"
    at.number_input(key="bulk_ml").set_value(257).run()
    at.number_input(key="solid_ml").set_value(123).run()
    before = [m.value for m in at.metric]
    at.toggle(key="cup_slider_input").set_value(True).run()
    assert not at.exception
    assert not at.number_input
    assert at.slider(key="bulk_ml_slider").value == 260
    assert at.slider(key="solid_ml_slider").value == 120
    assert [m.value for m in at.metric] == ["140 mL", "53.8%"]
    at.slider(key="bulk_ml_slider").set_value(430).run()
    at.slider(key="solid_ml_slider").set_value(320).run()
    at.switch_page("content/home.py").run()
    at.switch_page("content/pores.py").run()
    assert not at.exception
    assert at.toggle(key="cup_slider_input").value
    assert at.slider(key="bulk_ml_slider").value == 430
    assert at.slider(key="solid_ml_slider").value == 320
    at.button(key="lang_en" if lang != "en" else "lang_ar").click().run()
    assert not at.exception
    assert at.slider(key="bulk_ml_slider").value == 430
    at.toggle(key="cup_slider_input").set_value(False).run()
    assert not at.exception
    assert at.number_input(key="bulk_ml").value == 430
    assert at.number_input(key="solid_ml").value == 320
    assert at.metric[0].value == "110 mL"


def test_slider_validation_empty_and_endpoints():
    at = app()
    at.switch_page("content/pores.py").run()
    at.toggle(key="cup_slider_input").set_value(True).run()
    assert not at.exception and not at.metric
    assert at.slider(key="solid_ml_slider").disabled
    at.slider(key="bulk_ml_slider").set_value(1000).run()
    at.slider(key="solid_ml_slider").set_value(0).run()
    assert [m.value for m in at.metric] == ["1000 mL", "100.0%"]
    at.slider(key="solid_ml_slider").set_value(1000).run()
    assert [m.value for m in at.metric] == ["0 mL", "0.0%"]
    at.slider(key="bulk_ml_slider").set_value(250).run()
    assert at.slider(key="solid_ml_slider").value == 250
    assert at.slider(key="solid_ml_slider").max == 250
    assert not at.exception


def test_opening_notice_and_reveal_gated_distribution_figure():
    at = app()
    assert TEXT["draft_notice"]["en"] in at.expander[0].label
    assert not at.expander[0].proto.expanded
    assert any(e.proto.url == REVIEW_URL for e in at.get("link_button"))
    assert any("initial draft" in e.value for e in at.markdown)
    at.switch_page("content/importance.py").run()
    assert not any(TEXT["draft_notice"]["en"] in e.label for e in at.expander)
    assert not any(TEXT["distribution_heading"]["en"] in e.label for e in at.expander)
    at.button(key="reveal_store").click().run()
    assert not at.exception
    assert any(TEXT["distribution_heading"]["en"] in e.label for e in at.expander)
    assert any(
        "30.1%" in e.value and "liquid freshwater" in e.value for e in at.markdown
    )
    with Image.open(ROOT / "assets/images/water_distribution_usgs.png") as im:
        im.verify()


def test_video_is_optional_and_cued_to_fifteen_minutes():
    at = app()
    at.switch_page("content/resources.py").run()
    assert not at.exception
    panel = next(e for e in at.expander if TEXT["cherry_talk"]["en"] in e.label)
    assert not panel.proto.expanded
    video = at.get("video")[0].proto
    assert video.start_time == CHERRY_START_SECONDS == 900
    assert "I3zqpXxtsHY" in video.url
    assert any(
        e.proto.url == CHERRY_VIDEO_URL + "&t=900s" for e in at.get("link_button")
    )


def test_reference_line_and_groundwater_curve_are_distinct():
    for regime in ["gaining", "losing"]:
        fig = river(24, "river_deep", regime, True, lambda key: TEXT[key]["en"])
        lines = {line.get_gid(): line for line in fig.axes[0].lines if line.get_gid()}
        reference = lines["surface_level_reference"]
        surface = lines["surface_water_level"]
        groundwater = lines["groundwater_table"]
        np.testing.assert_allclose(reference.get_xdata(), [0, 80])
        np.testing.assert_allclose(surface.get_xdata(), [80, 100])
        np.testing.assert_allclose(reference.get_ydata(), 0)
        assert reference.get_linestyle() == ":"
        np.testing.assert_allclose(
            groundwater.get_ydata(), river_head(groundwater.get_xdata(), regime)
        )
        water = next(
            p for p in fig.axes[0].patches if p.get_gid() == "observation_water"
        )
        assert water.get_y() + water.get_height() == pytest.approx(
            river_head(24, regime)
        )
        fig.clear()
