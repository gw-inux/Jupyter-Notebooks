"""Shared presentation helpers; keep page scripts focused on learning steps."""

import json
from contextlib import contextmanager
from inspect import signature
from html import escape
import streamlit as st
from core.i18n import ROOT, tr
from core.sources import SOURCES
from core.figures import needs_browser_text, browser_svg, prepare_fonts

COLORS = {
    "home": "blue",
    "importance": "blue",
    "pores": "orange",
    "beach": "green",
    "resources": "violet",
    "lab": "violet",
    "about": "blue",
}
ICONS = {
    "home": "💦",
    "importance": "🌍",
    "pores": "🧪",
    "beach": "🌊",
    "resources": "📚",
    "lab": "🔎",
    "about": "ℹ️",
}


def heading(page, introduction=None, learning=True):
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
        "notice": (205, 96, 51),
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
    if not learning:
        return
    lessons = json.loads((ROOT / "assets/lessons.json").read_text(encoding="utf-8"))
    lesson = lessons[page].get(
        st.session_state.get("language", "en"), lessons[page]["en"]
    )
    st.info(lesson["motivation"], icon="💡")
    st.markdown("**🎯 " + tr("learning_objectives") + "**")
    st.markdown("\n".join("- " + objective for objective in lesson["objectives"]))


def sidebar_hint():
    """Show an opening-page cue only while Streamlit's sidebar is collapsed.

    CSS follows the native sidebar's live aria-expanded state, including
    mobile resizing and toggling; it does not add session state or JavaScript.
    """
    st.markdown(
        """<style>
.gw-sidebar-hint {display:none; padding:.65rem .8rem; margin-bottom:.5rem;
 border:1px solid #397FA5; border-radius:.5rem;
 background:#397FA5; color:#fff; font-size:1rem; font-weight:600;}
body:has([data-testid="stSidebar"][aria-expanded="false"]) .gw-sidebar-hint {
 display:block;
}
</style>"""
        + '<div class="gw-sidebar-hint"><span aria-hidden="true">↖️ </span>'
        + escape(tr("sidebar_hint"))
        + "</div>",
        unsafe_allow_html=True,
    )


@contextmanager
def expander(label, kind="details", expanded=False):
    colors = {
        "controls": "orange",
        "reflection": "violet",
        "details": "blue",
        "sources": "green",
        "notice": "orange",
    }
    count = st.session_state.get("_panel_count", 0)
    st.session_state["_panel_count"] = count + 1
    key = f'panel_{st.session_state.get("_section","home")}_{kind}_{count}'
    cue = tr("open_close")
    with st.container(key=key):
        with st.expander(f":{colors[kind]}[**{label}**] ({cue})", expanded=expanded):
            yield


def source_links(*ids):
    with expander(tr("source"), "sources"):
        for id in sorted(set(ids), key=lambda value: int(value[1:])):
            title, url = SOURCES[id]
            st.markdown(f"**[{id}]** [{title}]({url})")
            if id == "S2":  # USGS water-cycle illustration collection.
                st.caption(tr("poster_versions"))


def _stretch_options(renderer):
    """Use the container width with either the older or newer Streamlit API.

    Newer renderers declare a string default for ``width``. Older images
    require a numeric width, and older pyplot forwards unknown keywords to
    Matplotlib. Check the declared parameter before passing ``"stretch"``.
    """
    width = signature(renderer).parameters.get("width")
    if width is not None and isinstance(width.default, str):
        return {"width": "stretch"}
    return {"use_container_width": True}


def responsive_image(image, **kwargs):
    """Display an image at the available width across supported Streamlit versions."""
    st.image(image, **_stretch_options(st.image), **kwargs)


def show(fig):
    prepare_fonts(fig)
    if needs_browser_text(fig):
        # Streamlit serves SVG as an image data URI. Browser text rendering
        # handles Arabic without any extra Python shaping/bidi packages.
        responsive_image(browser_svg(fig))
        fig.clear()
    else:
        st.pyplot(fig, clear_figure=True, **_stretch_options(st.pyplot))


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


@contextmanager
def action_box(key):
    """Centered outlined actions, scoped so quiz and sidebar buttons stay intact."""
    with st.container(key="action_" + key):
        st.markdown(
            """<style>
        div[class*="st-key-action_"] [data-testid="stButton"],
        div[class*="st-key-action_"] [data-testid="stLinkButton"] {
          display:flex; justify-content:center;
        }
        div[class*="st-key-action_"] button,
        div[class*="st-key-action_"] [data-testid="stLinkButton"] a {
          margin-inline:auto; border:2px solid #397FA5; background:transparent;
          color:#397FA5; border-radius:.5rem; font-weight:650;
        }
        div[class*="st-key-action_"] button:hover,
        div[class*="st-key-action_"] [data-testid="stLinkButton"] a:hover {
          background:rgba(57,127,165,.10); border-color:#397FA5;
        }
        @media(prefers-color-scheme:dark) {
          div[class*="st-key-action_"] button,
          div[class*="st-key-action_"] [data-testid="stLinkButton"] a {color:#87C7EB;}
        }
        </style>""",
            unsafe_allow_html=True,
        )
        yield


def centered_link(label, url, key):
    with action_box(key):
        st.link_button(label, url)


def next_page(page, label=None):
    with action_box("next_" + page):
        if st.button(label or (tr("next") + " → " + tr(page)), key="next_" + page):
            st.switch_page(st.session_state["_pages"][page])


def reset_button():
    """Restart learning activities while retaining language and layout."""
    with action_box("reset_session"):
        if st.button(tr("reset"), key="reset_session"):
            lang, layout = st.session_state.language, st.session_state.layout_choice
            for key in list(st.session_state):
                del st.session_state[key]
            st.session_state.language, st.session_state.layout_choice = lang, layout
            st.switch_page("content/home.py")


def activity_value(key, default):
    """Retrieve an activity choice independently of widget cleanup/language."""
    return st.session_state.setdefault("activity_values", {}).get(key, default)


def remember_activity(key, storage_key=None):
    """Retain a semantic value; two input modes may share one storage key."""
    st.session_state.setdefault("activity_values", {})[storage_key or key] = (
        st.session_state[key]
    )
