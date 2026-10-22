"""Check the connected-river teaching cases independently of UI labels."""

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest
from pathlib import Path

from core.river import (
    RIVER_POSITIONS,
    RIVER_DEPTHS,
    RIVER_REGIMES,
    river_ground,
    river_head,
    river_observation,
)
from core.i18n import TEXT

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("regime", RIVER_REGIMES)
@pytest.mark.parametrize("position", RIVER_POSITIONS)
@pytest.mark.parametrize("depth", RIVER_DEPTHS)
def test_river_observation_wet_dry_and_equilibrated_level(regime, position, depth):
    observation = river_observation(RIVER_POSITIONS[position], depth, regime)
    expected_wet = depth == "river_deep" or (
        depth == "river_level_depth"
        and (position == "river_near" or regime == "gaining")
    )
    assert (observation.water_depth > 0) == expected_wet
    assert observation.bottom < observation.ground
    assert observation.head < observation.ground
    if expected_wet:
        assert observation.bottom + observation.water_depth == pytest.approx(
            observation.head
        )


def test_river_gradient_and_connection_at_bank():
    x = np.linspace(0, 80, 401)
    for regime in RIVER_REGIMES:
        head = river_head(x, regime)
        assert head[-1] == 0
        assert head[0] == pytest.approx(0.6 if regime == "gaining" else -0.6)
        # The conceptual near-bank slope steepens toward the surface water.
        # Gaining bends down; losing bends up toward its higher river level.
        curvature = np.diff(head, n=2)
        assert np.all(curvature < 0) if regime == "gaining" else np.all(curvature > 0)
        assert abs(head[-1] - head[-2]) > abs(head[1] - head[0])
        assert np.all(head[:-1] < river_ground(x)[:-1])
        assert head[-1] == river_ground(x)[-1]
        assert (
            np.all(np.diff(head) < 0)
            if regime == "gaining"
            else np.all(np.diff(head) > 0)
        )
    for invalid in [-1, 81, np.nan, np.inf]:
        with pytest.raises(ValueError):
            river_head(invalid, "gaining")
    with pytest.raises(ValueError):
        river_head(24, "unknown")
    with pytest.raises(ValueError):
        river_observation(24, "unknown", "gaining")


def test_river_controls_all_outcomes_and_language_page_persistence():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    at.switch_page("content/beach.py").run()
    at.toggle(key="river_reveal").set_value(True).run()
    for regime in RIVER_REGIMES:
        at.radio(key="river_regime").set_value(regime).run()
        for position in RIVER_POSITIONS:
            at.select_slider(key="river_position").set_value(position).run()
            for depth in RIVER_DEPTHS:
                at.radio(key="river_depth").set_value(depth).run()
                assert not at.exception
                observation = river_observation(
                    RIVER_POSITIONS[position], depth, regime
                )
                key = "water_found" if observation.water_depth > 0 else "no_water"
                assert at.info[-1].value == TEXT[key]["en"]
    at.radio(key="river_depth").set_value("river_level_depth").run()
    for lang in ["ar", "pl", "en"]:
        at.button(key="lang_" + lang).click().run()
        assert not at.exception
        assert at.radio(key="river_regime").value == "losing"
        assert at.select_slider(key="river_position").value == "river_inland"
        assert at.radio(key="river_depth").value == "river_level_depth"
        assert at.toggle(key="river_reveal").value
        assert at.info[-1].value == TEXT["no_water"][lang]
    at.switch_page("content/home.py").run()
    at.switch_page("content/beach.py").run()
    assert not at.exception
    assert at.radio(key="river_regime").value == "losing"
    assert at.select_slider(key="river_position").value == "river_inland"
    assert at.radio(key="river_depth").value == "river_level_depth"
    assert at.toggle(key="river_reveal").value


def test_cup_and_beach_choices_survive_translation_and_page_cleanup():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    at.switch_page("content/pores.py").run()
    at.number_input(key="bulk_ml").set_value(250).run()
    at.number_input(key="solid_ml").set_value(150).run()
    at.toggle(key="pore_saturated").set_value(True).run()
    at.button(key="lang_ar").click().run()
    assert at.number_input(key="bulk_ml").value == 250
    assert at.number_input(key="solid_ml").value == 150
    at.switch_page("content/beach.py").run()
    at.select_slider(key="hole_position").set_value("middle").run()
    at.radio(key="hole_depth").set_value("deeper").run()
    at.toggle(key="beach_reveal").set_value(True).run()
    at.button(key="lang_pl").click().run()
    assert at.select_slider(key="hole_position").value == "middle"
    assert at.radio(key="hole_depth").value == "deeper"
    assert at.toggle(key="beach_reveal").value
    at.switch_page("content/pores.py").run()
    assert not at.exception
    assert at.number_input(key="bulk_ml").value == 250
    assert at.number_input(key="solid_ml").value == 150
    assert at.toggle(key="pore_saturated").value
    at.switch_page("content/beach.py").run()
    assert not at.exception
    assert at.select_slider(key="hole_position").value == "middle"
    assert at.radio(key="hole_depth").value == "deeper"
    assert at.toggle(key="beach_reveal").value
