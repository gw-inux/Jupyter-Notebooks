"""Text lookup and assessment UI.

TABLE OF CONTENTS — search for the numbered section comments below.
  1. Markdown loading, English fallback, labels and equation rendering
  2. Number/slider input with a shared value
  3. Scoped toolbar/settings styling and durable layout toggles
  4. Persistent iNUX assessment state, answer controls and feedback

Maintenance: edit assets/md/*.md and questions/<language>/*.json for learner text.
Eight complete languages are bundled. Missing translations use English.
"""

from pathlib import Path
import json
import re
import streamlit as st

ROOT = Path(__file__).resolve().parent
LANGUAGES = {
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "it": "🇮🇹 Italiano",
    "hi": "🇮🇳 हिन्दी",
    "ar": "🌐 العربية",
    "zh": "🇨🇳 简体中文",
    "pt": "🇵🇹 Português",
    "bn": "🇧🇩 বাংলা (Bengali)",
}


# 1. Soil Water Retention filename convention and English fallback
def _markdown_path(md_dir, filename, language="en"):
    """Select filename_<language>.md, otherwise the English filename.md.

    This is the Soil Water Retention load_md lookup algorithm, shared by the
    text reader and image renderer so both resolve the same source document.
    """
    md_dir = Path(md_dir)
    base = Path(filename)
    if language.lower() != "en":
        translated = md_dir / f"{base.stem}_{language}{base.suffix}"
        if translated.exists():
            return translated
    return md_dir / filename


def load_md(md_dir, filename, language="en"):
    """Read UTF-8 Markdown with the Soil Water Retention English fallback."""
    return _markdown_path(md_dir, filename, language).read_text(encoding="utf-8")


def read_md(name, lang):
    return load_md(ROOT / "assets" / "md", name + ".md", lang)


def load_ui(lang):
    def parse(text):
        chunks = re.split(r"^## (\w+)\s*$", text, flags=re.M)
        return {chunks[i]: chunks[i + 1].strip() for i in range(1, len(chunks), 2)}

    base = parse(read_md("ui", "en"))
    if lang != "en":
        base.update(parse(read_md("ui", lang)))
    return base


def translator(lang):
    labels = load_ui(lang)

    def t(key, **kwargs):
        return labels[key].format(**kwargs) if kwargs else labels[key]

    return t


def render_md(name, lang):
    """Render equations and standalone local images from editable Markdown.

    Image paths are relative to the Markdown file, as in a Markdown editor.
    Text, image placement and captions can therefore be edited or translated
    without changing Python. Existing text/equation rendering is retained.
    """
    source = _markdown_path(ROOT / "assets" / "md", name + ".md", lang)
    image_pattern = r"^!\[[^\]\n]*\]\(([^)\n]+)\)[ \t]*$"
    chunks = re.split(
        r"(\$\$[\s\S]*?\$\$|^!\[[^\]\n]*\]\([^)\n]+\)[ \t]*$)",
        read_md(name, lang),
        flags=re.M,
    )
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("$$"):
            st.latex(chunk[2:-2].strip())
        elif match := re.fullmatch(image_pattern, chunk):
            st.image(str((source.parent / match[1]).resolve()), width="stretch")
        else:
            st.markdown(chunk)


# 2. Keep the numerical value separate from either widget's disposable state.
def head_input(label, key, *, minimum, maximum, default, step=0.1, disabled=False, t):
    """Changing input mode must neither change the head nor reset a solver run."""
    st.session_state.setdefault(key, float(default))
    slider = st.toggle(t("slider_input"), key=key + "_use_slider")
    widget_key = key + ("_slider" if slider else "_number")
    st.session_state[widget_key] = float(st.session_state[key])

    def remember_value():
        st.session_state[key] = float(st.session_state[widget_key])

    widget = st.slider if slider else st.number_input
    widget(
        label,
        min_value=float(minimum),
        max_value=float(maximum),
        step=float(step),
        format="%.2f",
        disabled=disabled,
        key=widget_key,
        on_change=remember_value,
    )
    return st.session_state[key]


# 3. Only explicit public widget/container keys are styled; no global overrides.
def toolbar_style(key, synchronized):
    background = "#fae9eb" if synchronized else "transparent"
    border = "#d47b85" if synchronized else "transparent"
    st.html(f"""<style>
    .st-key-{key}_play_group {{
        background-color: {background}; border: 1px solid {border};
        border-radius: 0.75rem; padding: 0.35rem;
    }}
    .st-key-{key}_reset button {{
        background-color: #e5eff9; border-color: #9bb9d7; color: #174875;
    }}
    .st-key-{key}_reset button:hover {{
        background-color: #d2e4f5; border-color: #527fa9; color: #10395f;
    }}
    </style>""")


def settings_style():
    """Match the three outer expander headers to their section heading highlights."""
    rules = ["""
        .st-key-three_preset [role="group"] {
            background-color: #EDF5FF;
            background-color: light-dark(#EDF5FF, #1E2A3D);
        }
    """]
    for section, light, dark in (
        ("theory", "#EDF5FF", "#1E2A3D"),
        ("three", "#F1FBF6", "#0E2F24"),
        ("grid", "#FFF6ED", "#342414"),
    ):
        # Style only the outer summary. Nested expanders have their own colors.
        scope = f".st-key-{section}_section"
        rules.append(f"""
            {scope} details:not({scope} details details) > summary {{
                background-color: {light};
                background-color: light-dark({light}, {dark});
            }}
        """)
    for section in ("three", "grid"):
        for group, background, border in (
            ("boundary", "#EEF7F0", "#9CC9AB"),
            ("aquifer", "#FFF4E8", "#E8BD86"),
        ):
            selector = f".st-key-{section}_{group}"
            rules.append(f"""
            {selector} details {{border-color: {border};}}
            {selector} summary {{background-color: {background}; border-radius: 7px;}}
            {selector} details[open] > summary {{border-radius: 7px 7px 0 0;}}
            """)
    if st.session_state.get("picard_newton_language") == "ar":
        # The course sidebar and all numerical/math displays keep their direction.
        rules.append("""
            .stMain [data-testid="stMarkdownContainer"],
            .stMain [data-testid="stWidgetLabel"] {
                direction: rtl; text-align: right;
            }
            .stMain .katex, .stMain .katex-display,
            .stMain [data-testid="stDataFrame"] {
                direction: ltr; text-align: initial;
            }
        """)
    st.html("<style>" + "".join(rules) + "</style>")


def durable_toggle(label, *, key, value=False, **kwargs):
    """Remember optional controls when switching between the two plot layouts."""
    stored = key + "_saved_value"
    st.session_state.setdefault(stored, st.session_state.get(key, value))
    st.session_state[key] = st.session_state[stored]

    def remember():
        st.session_state[stored] = st.session_state[key]

    return st.toggle(label, key=key, on_change=remember, **kwargs)


# 4. Boundary-condition module's two-button pattern, with durable answer state
# Checkbox widget state may be removed by Streamlit when hidden. The separate
# answers dictionary survives collapsing, language changes and model reruns.
def flip_assessment(bank):
    key = "exp_" + bank
    st.session_state[key] = not st.session_state.get(key, False)


def remember_answer(qid, index, key):
    records = st.session_state.setdefault("picard_newton_answers", {})
    record = records.setdefault(qid, {"choices": {}, "submitted": None})
    record["choices"][index] = bool(st.session_state[key])


def grade_choices(choices, truth):
    """Award points only for selected correct options; judge the entire answer.

    Unselected options and selected distractors earn no points. A full score
    does not imply a fully correct answer if a distractor was also selected.
    """
    if len(choices) != len(truth):
        raise ValueError(
            "Each assessment option needs one selection and one truth value"
        )
    score = sum(selected and correct for selected, correct in zip(choices, truth))
    incorrect = sum(
        selected and not correct for selected, correct in zip(choices, truth)
    )
    missing = sum(not selected and correct for selected, correct in zip(choices, truth))
    status = (
        "full" if not incorrect and not missing else "partial" if score else "wrong"
    )
    return dict(
        score=score,
        total=sum(truth),
        incorrect=incorrect,
        missing=missing,
        status=status,
    )


def assessment(bank, lang, t):
    state_key = "exp_" + bank
    st.session_state.setdefault(state_key, False)
    st.session_state.setdefault("picard_newton_answers", {})
    with st.container(border=True):
        left, right = st.columns([25, 1])
        left.button(
            "🧠 **" + t("assess") + " · " + t(bank + "_quiz") + "**",
            key="label_" + bank,
            type="tertiary",
            on_click=flip_assessment,
            args=(bank,),
        )
        right.button(
            "▲" if st.session_state[state_key] else "▼",
            key="chevron_" + bank,
            type="tertiary",
            on_click=flip_assessment,
            args=(bank,),
        )
        if not st.session_state[state_key]:
            return
        st.caption(t("assessment_info"))
        path = ROOT / "questions" / lang / (bank + ".json")
        if not path.exists():
            path = ROOT / "questions" / "en" / (bank + ".json")
        questions = json.loads(path.read_text(encoding="utf-8"))
        cols = st.columns(2)
        for i, q in enumerate(questions):
            with cols[i % 2]:
                st.markdown(f"**{i+1}. {q['question']}**")
                qid = f"{bank}_{i}"
                record = st.session_state["picard_newton_answers"].setdefault(
                    qid, {"choices": {}, "submitted": None}
                )
                choices = []
                for j, label in enumerate(q["options"]):
                    key = f"choice_{qid}_{j}"
                    if key not in st.session_state:
                        st.session_state[key] = record["choices"].get(j, False)
                    # Markdown supports LaTeX reliably; checkbox labels support
                    # only a restricted Markdown subset in current Streamlit.
                    tick, option = st.columns([1, 9], gap="small")
                    choices.append(
                        tick.checkbox(
                            re.sub(r"[$\\]", "", label),
                            label_visibility="collapsed",
                            key=key,
                            on_change=remember_answer,
                            args=(qid, j, key),
                        )
                    )
                    option.markdown(label)
                if st.button(t("check"), key="check_" + qid):
                    record["submitted"] = choices.copy()
                if record["submitted"] == choices:
                    truth = list(q["options"].values())
                    result = grade_choices(choices, truth)
                    feedback = (
                        q["success"]
                        if result["status"] == "full"
                        else q.get("failure", q.get("error", ""))
                    )
                    message = (
                        "**"
                        + t("answer_" + result["status"])
                        + "** · "
                        + t("score", score=result["score"], total=result["total"])
                    )
                    if result["status"] != "full":
                        message += "\n\n" + t(
                            "assessment_details",
                            incorrect=result["incorrect"],
                            missing=result["missing"],
                        )
                    message += "\n\n" + feedback
                    {"full": st.success, "partial": st.warning, "wrong": st.error}[
                        result["status"]
                    ](message)
