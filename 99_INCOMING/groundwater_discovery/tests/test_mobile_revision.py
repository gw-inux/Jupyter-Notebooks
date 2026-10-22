"""Reveal feedback, figure results and consistent citations after the field review."""

import re
from pathlib import Path

import pytest
from matplotlib.backends.backend_agg import FigureCanvasAgg
from streamlit.testing.v1 import AppTest

from core.figures import sample_cup, water_store, cup_step
from core.i18n import LANGUAGES, TEXT, load_md
from core.sources import SOURCES

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "prediction,close", [(0, False), (65, False), (70, True), (80, True), (100, True)]
)
def test_reveal_feedback_uses_submitted_prediction(prediction, close):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    at.switch_page("content/importance.py").run()
    at.slider(key="freshwater_guess").set_value(prediction).run()
    at.button(key="reveal_store").click().run()
    key = "guess_close" if close else "guess_far"
    assert not at.exception
    assert any(TEXT[key]["en"] in message.value for message in at.info)
    # Navigation removes the slider widget but must not rewrite the submitted guess.
    at.switch_page("content/home.py").run()
    at.switch_page("content/importance.py").run()
    at.button(key="lang_pl").click().run()
    assert not at.exception
    assert at.session_state["revealed_guess"] == prediction
    assert any(TEXT[key]["pl"] in message.value for message in at.info)


@pytest.mark.parametrize(
    "bulk,solid,expected",
    [
        (250, 150, ("100 mL", "40.0%")),
        (1000, 0, ("1000 mL", "100.0%")),
        (1000, 1000, ("0 mL", "0.0%")),
    ],
)
def test_cup_results_inside_figure_match_measurements(bulk, solid, expected):
    for lang in LANGUAGES:
        fig = sample_cup(bulk, solid, lambda key: TEXT[key][lang])
        labels = {label.get_gid(): label.get_text() for label in fig.axes[0].texts}
        assert (labels["cup_pore_result"], labels["cup_porosity_result"]) == expected
        fig.clear()


def test_water_store_fact_is_below_grid():
    fig = water_store(lambda key: TEXT[key]["en"])
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    ax = fig.axes[0]
    assert ax.get_legend().get_window_extent(renderer).y1 < min(
        p.get_window_extent(renderer).y0 for p in ax.patches
    )
    fig.clear()


def test_cup_steps_preserve_grain_geometry_when_water_is_added():
    dry, wet = cup_step(1), cup_step(2)

    def grains(fig):
        return [
            (p.center, p.width, p.height)
            for p in fig.axes[0].patches
            if hasattr(p, "center")
        ]

    assert grains(dry) == grains(wet)
    assert len(grains(dry)) == 24
    dry.clear()
    wet.clear()
    with pytest.raises(ValueError):
        cup_step(4)


def test_citation_sequences_match_in_all_translations():
    assert list(SOURCES) == [f"S{i}" for i in range(1, 19)]
    for base in (ROOT / "assets/markdown").glob("*.md"):
        if any(base.stem.endswith("_" + lang) for lang in LANGUAGES if lang != "en"):
            continue
        english = re.findall(r"\bS\d+\b", base.read_text())
        assert all(source in SOURCES for source in english)
        for lang in LANGUAGES:
            translated = re.findall(r"\bS\d+\b", load_md(base.parent, base.name, lang))
            assert translated == english, (base.name, lang)
    first = (ROOT / "assets/markdown/home_cycle.md").read_text()
    assert "[S1, S2]" in first
