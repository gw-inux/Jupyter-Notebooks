from pathlib import Path
import ast, json
import pytest
from PIL import Image
from streamlit.testing.v1 import AppTest
from core.i18n import LANGUAGES, TEXT, load_md
from core.sources import SOURCES

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["home", "importance", "pores", "beach", "resources", "lab"]
BLOCKS = [
    "home",
    "importance",
    "importance_reveal",
    "pores",
    "cup",
    "cycle",
    "cycle_detail",
    "beach",
    "beach_limits",
    "field",
    "lens",
    "lens_model",
    "reflection",
    "facilitator",
    "home_cycle",
    "cup_intro",
    "porosity_detail",
    "river_intro",
    "river_detail",
    "reflection_answers",
    "resources_intro",
    "draft_notice",
    "water_distribution",
    "cherry_talk",
    "about_description",
    "about_development",
    "about_author",
    "about_contact",
    "go_deeper_intro",
    "density_parameters",
    "island_photo",
    "island_model",
]


def run_app():
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()


def no_error(at):
    assert not at.exception, [(e.message, e.stack_trace) for e in at.exception]


def test_translation_assets_questions_and_fallback(tmp_path):
    for key, row in TEXT.items():
        assert set(row) == set(LANGUAGES), key
        assert all(row.values()), key
    lessons = json.loads((ROOT / "assets/lessons.json").read_text())
    assert set(lessons) == set(PAGES)
    for page, row in lessons.items():
        assert set(row) == set(LANGUAGES), page
        for lesson in row.values():
            assert lesson["motivation"] and len(lesson["objectives"]) == 2
            assert all(lesson["objectives"])
    assert "pilot" not in TEXT
    for page in ["importance", "pores", "beach", "resources"]:
        assert all(not value[0].isdigit() for value in TEXT[page].values())
    for path in (ROOT / "assets/images").glob("cover_*.png"):
        with Image.open(path) as image:
            image.verify()
    assert len(list((ROOT / "assets/images").glob("cover_*.png"))) == 3
    eng = json.loads((ROOT / "assets/questions/checks.json").read_text())
    assert len(eng) == 12
    for lang in LANGUAGES:
        suffix = "" if lang == "en" else "_" + lang
        for name in BLOCKS:
            assert (ROOT / f"assets/markdown/{name}{suffix}.md").read_text().strip()
        with Image.open(ROOT / f"assets/images/water_cycle_{lang}.jpg") as image:
            image.verify()
        qs = json.loads((ROOT / f"assets/questions/checks{suffix}.json").read_text())
        assert [q["id"] for q in qs] == [q["id"] for q in eng]
        for en, q in zip(eng, qs):
            assert list(q["options"].values()) == list(en["options"].values())
            assert len(q["options"]) == 3 and sum(q["options"].values()) == 1
            assert q["source"] in SOURCES
    (tmp_path / "sample.md").write_text("English fallback")
    assert load_md(tmp_path, "sample.md", "xx") == "English fallback"
    with pytest.raises(ValueError):
        load_md(tmp_path, "../sample.md")
    # Catch references to deleted/replaced translation keys before navigation.
    for path in list((ROOT / "content").glob("*.py")) + [
        ROOT / "app.py",
        ROOT / "core/ui.py",
    ]:
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "tr"
                and node.args
            ):
                if isinstance(node.args[0], ast.Constant):
                    assert node.args[0].value in TEXT


@pytest.mark.parametrize("lang", list(LANGUAGES))
@pytest.mark.parametrize("layout", ["centered", "wide"])
def test_navigation_language_and_both_layouts(lang, layout):
    at = run_app()
    at.radio(key="_layout_ui_en").set_value(layout).run()
    no_error(at)
    at.button(key="lang_" + lang).click().run()
    no_error(at)
    for page in PAGES + ["about"]:
        at.button(key="nav_" + page).click().run()
        no_error(at)
        assert TEXT["title" if page == "home" else page][lang] in at.header[0].value
        if page != "about":
            assert any(
                TEXT["learning_objectives"][lang] in m.value for m in at.markdown
            )
        else:
            assert any("mailto:mail@reimann-thomas.de" in m.value for m in at.markdown)
            assert not any("ERASMUS" in m.value.upper() for m in at.markdown)
        assert not any(c.value == "The Groundwater Project" for c in at.caption)
        assert all("**" in e.label for e in at.expander)
        assert at.session_state["layout_choice"] == layout
        # AppTest doesn't retain the browser page hash after st.switch_page.
        at.switch_page("content/" + page + ".py").run()
        no_error(at)
        assert at.radio(key="_layout_ui_" + lang).value == layout
    at.button(key="lang_en").click().run()
    no_error(at)
    assert at.session_state["layout_choice"] == layout


@pytest.mark.parametrize("bad", [None, "white", "Szeroki", "invalid"])
def test_invalid_legacy_layout_does_not_reach_page_config(bad):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.session_state["language"] = "pl"
    at.session_state["layout_choice"] = bad
    at.run()
    no_error(at)
    assert at.session_state["layout_choice"] == "centered"
    at.button(key="nav_beach").click().run()
    no_error(at)


def test_quiz_retries_unsent_answers_language_roundtrip_and_navigation():
    at = run_app()
    at.switch_page("content/importance.py").run()
    at.button(key="reveal_store").click().run()
    assert len([r for r in at.radio if r.key.startswith("answer_")]) == 3
    at.button(key="check_stores").click().run()
    no_error(at)
    assert any("Choose an answer first." in i.value for i in at.info)
    at.radio(key="answer_stores_en").set_value(0).run()
    at.button(key="check_stores").click().run()
    assert not at.session_state["results"]["stores"]["correct"]
    at.radio(key="answer_stores_en").set_value(1).run()
    at.button(key="check_stores").click().run()
    no_error(at)
    assert at.session_state["results"]["stores"]["correct"]
    at.button(key="lang_ar").click().run()
    no_error(at)
    assert at.radio(key="answer_stores_ar").value == 1
    at.radio(key="answer_role_ar").set_value(1).run()  # unsent answer must also persist
    at.button(key="lang_pl").click().run()
    no_error(at)
    assert at.radio(key="answer_role_pl").value == 1
    at.radio(key="answer_stores_pl").set_value(2).run()
    assert not at.success  # hide feedback for a different selection
    at.button(key="lang_en").click().run()
    assert at.radio(key="answer_stores_en").value == 2
    at.switch_page("content/pores.py").run()
    at.switch_page("content/importance.py").run()
    no_error(at)
    assert at.radio(key="answer_role_en").value == 1


def test_activity_extremes_three_questions_and_reset():
    at = run_app()
    at.switch_page("content/pores.py").run()
    assert len([r for r in at.radio if r.key.startswith("answer_")]) == 3
    assert at.number_input(key="bulk_ml").value == 0
    assert at.number_input(key="solid_ml").value == 0
    assert not at.metric and not at.warning
    assert (
        len(at.get("imgs")) == 4
    )  # grains and three procedural sketches; no empty cup
    assert len(at.latex) == 1  # general porosity equation available before input
    assert any(TEXT["empty_sample"]["en"] in i.value for i in at.info)
    at.number_input(key="bulk_ml").set_value(100).run()
    at.number_input(key="solid_ml").set_value(100).run()
    at.number_input(key="bulk_ml").set_value(50).run()
    no_error(at)
    assert not at.warning
    assert at.number_input(key="solid_ml").value == 50
    at.number_input(key="bulk_ml").set_value(100).run()
    at.number_input(key="solid_ml").set_value(60).run()
    no_error(at)
    assert at.metric[0].value == "40 mL"
    assert at.metric[1].value == "40.0%"
    at.switch_page("content/beach.py").run()
    assert len([r for r in at.radio if r.key.startswith("answer_")]) == 3
    assert not at.metric and not at.number_input and not at.slider
    at.toggle(key="beach_reveal").set_value(True).run()
    assert any(TEXT["water_found"]["en"] in m.value for m in at.info)
    at.select_slider(key="hole_position").set_value("middle").run()
    assert any(TEXT["no_water"]["en"] in m.value for m in at.info)
    at.radio(key="hole_depth").set_value("deeper").run()
    no_error(at)
    assert any(TEXT["water_found"]["en"] in m.value for m in at.info)
    at.switch_page("content/lab.py").run()
    assert len([r for r in at.radio if r.key.startswith("answer_")]) == 3
    assert len(at.latex) == 1 and len(at.metric) == 3
    for level in [0.1, 0.4, 0.7, 1.0]:
        at.slider(key="lens_head").set_value(level).run()
        no_error(at)
        assert [m.value for m in at.metric][:2] == [
            f"{level:.1f} m",
            f"{40*level:.1f} m",
        ]
    at.button(key="lang_cs").click().run()
    at.radio(key="_layout_ui_cs").set_value("wide").run()
    at.switch_page("content/resources.py").run()
    at.button(key="reset_session").click().run()
    no_error(at)
    assert at.session_state["language"] == "cs"
    assert at.session_state["layout_choice"] == "wide"
    assert TEXT["title"]["cs"] in at.header[0].value


def test_lens_choice_survives_language_change_and_page_cleanup():
    at = run_app()
    at.switch_page("content/lab.py").run()
    at.slider(key="lens_head").set_value(0.4).run()
    for lang in ["ar", "pl", "en"]:
        at.button(key="lang_" + lang).click().run()
        no_error(at)
        assert at.slider(key="lens_head").value == 0.4
        assert [m.value for m in at.metric][:2] == ["0.4 m", "16.0 m"]
    at.switch_page("content/pores.py").run()
    at.switch_page("content/lab.py").run()
    no_error(at)
    assert at.slider(key="lens_head").value == 0.4
