"""Shared presentation helpers; keep page scripts focused on learning steps."""

import json
from contextlib import contextmanager
import streamlit as st
from core.i18n import ROOT, tr
from core.sources import SOURCES
from core.figures import needs_browser_text, browser_svg

COLORS = {
    "home": "blue",
    "importance": "blue",
    "pores": "orange",
    "beach": "green",
    "resources": "violet",
    "lab": "violet",
}
ICONS = {
    "home": "💧",
    "importance": "🌍",
    "pores": "🧪",
    "beach": "🌊",
    "resources": "📚",
    "lab": "🔎",
}


def heading(page, introduction=None):
    """Page title and learning frame, with an optional opening panel."""
    st.session_state["_section"] = page
    st.session_state["_panel_count"] = 0
    title = tr("title") if page == "home" else tr(page)
    st.header(f":{COLORS[page]}[{title}]", divider=COLORS[page])
    # Scope the tint to our keyed containers. Native details/summary keeps
    # keyboard operation and focus styles; all body text inherits the theme.
    palettes = {
        "controls": (206, 120, 49),
        "reflection": (123, 83, 165),
        "details": (25, 127, 158),
        "sources": (55, 139, 104),
    }
    rules = []
    for kind, rgb in palettes.items():
        selector = (
            f'div[class*="st-key-panel_"][class*="_{kind}_"] [data-testid="stExpander"]'
        )
        color = ",".join(map(str, rgb))
        rules.append(
            f"{selector} {{background:rgba({color},.07); border-radius:.6rem;}}"
        )
        rules.append(f"{selector} details {{border-color:rgba({color},.35);}}")
        rules.append(f"{selector} summary p {{font-weight:650;}}")
    st.markdown("<style>" + "".join(rules) + "</style>", unsafe_allow_html=True)
    if introduction is not None:
        introduction()
    lessons = json.loads((ROOT / "assets/lessons.json").read_text(encoding="utf-8"))
    lesson = lessons[page].get(
        st.session_state.get("language", "en"), lessons[page]["en"]
    )
    st.info(lesson["motivation"], icon="💡")
    st.markdown("**🎯 " + tr("learning_objectives") + "**")
    st.markdown("\n".join("- " + objective for objective in lesson["objectives"]))
    st.caption(tr("expander_hint"))


@contextmanager
def expander(label, kind="details", expanded=False):
    colors = {
        "controls": "orange",
        "reflection": "violet",
        "details": "blue",
        "sources": "green",
    }
    count = st.session_state.get("_panel_count", 0)
    st.session_state["_panel_count"] = count + 1
    key = f'panel_{st.session_state.get("_section","home")}_{kind}_{count}'
    with st.container(key=key):
        with st.expander(f":{colors[kind]}[**{label}**]", expanded=expanded):
            yield


def source_links(*ids):
    with expander(tr("source"), "sources"):
        for id in ids:
            title, url = SOURCES[id]
            st.markdown(f"**[{id}]** [{title}]({url})")


def show(fig):
    if needs_browser_text(fig):
        # Streamlit serves SVG as an image data URI. Browser text rendering
        # handles Arabic without any extra Python shaping/bidi packages.
        st.image(browser_svg(fig), width="stretch")
        fig.clear()
    else:
        st.pyplot(fig, clear_figure=True, width="stretch")


def quiz(qid):
    lang = st.session_state.get("language", "en")
    directory = ROOT / "assets/questions"
    path = directory / ("checks" + ("" if lang == "en" else "_" + lang) + ".json")
    if not path.is_file():
        path = directory / "checks.json"
    q = next(q for q in json.loads(path.read_text(encoding="utf-8")) if q["id"] == qid)
    labels = list(q["options"])
    with st.container(border=True):
        # Language-specific widgets prevent stale labels; semantic results persist.
        key = f"answer_{qid}_{lang}"
        answers = st.session_state.setdefault("answers", {})
        st.session_state[key] = answers.get(qid)

        def save_answer():
            st.session_state["answers"][qid] = st.session_state[key]

        answer = st.radio(
            q["question"],
            list(range(len(labels))),
            index=None,
            format_func=lambda i: labels[i],
            key=key,
            on_change=save_answer,
        )
        results = st.session_state.setdefault("results", {})
        submitted = results.get(qid)
        if st.button(tr("check"), key=f"check_{qid}"):
            if answer is None:
                st.info(tr("choose"))
            else:
                correct = q["options"][labels[answer]]
                results[qid] = {"answer": answer, "correct": correct}
                submitted = results[qid]
        # If selection changes, don't show obsolete feedback as if it applied.
        if submitted and (answer is None or submitted["answer"] == answer):
            if submitted["correct"]:
                st.success(tr("correct") + " " + q["success"])
            else:
                st.info(tr("retry") + " " + q["error"])


def quiz_group(*ids):
    with expander("👉 " + tr("quiz") + f" · {len(ids)}", "reflection"):
        for qid in ids:
            quiz(qid)


def next_page(page):
    if st.button(tr("next") + " → " + tr(page), key="next_" + page, type="primary"):
        st.switch_page(st.session_state["_pages"][page])


def activity_value(key, default):
    """Retrieve an activity choice independently of widget cleanup/language."""
    return st.session_state.setdefault("activity_values", {}).get(key, default)


def remember_activity(key, storage_key=None):
    """Retain a semantic value; two input modes may share one storage key."""
    st.session_state.setdefault("activity_values", {})[storage_key or key] = (
        st.session_state[key]
    )
