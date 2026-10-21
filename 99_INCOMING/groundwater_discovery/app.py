from pathlib import Path
import sys

APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))
import streamlit as st
from core.i18n import tr, LANGUAGES
from core.ui import ICONS

st.session_state.setdefault("language", "en")
if st.session_state.language not in LANGUAGES:
    st.session_state.language = "en"
# This key is NEVER owned by a widget. Translated widget identities may change
# or be cleaned up during navigation; page configuration must remain canonical.
layout = st.session_state.get("layout_choice", "centered")
st.session_state.layout_choice = (
    layout if layout in ("centered", "wide") else "centered"
)
st.set_page_config(
    page_title="Groundwater discovery | The Groundwater Project",
    page_icon="💧",
    layout=st.session_state.layout_choice,
)

# Reference-module pattern: title first, left-aligned bold navigation,
# compact flag buttons, native body typography, optional wide layout.
st.sidebar.markdown("## 💧 :blue[" + tr("title") + "]")
st.markdown(
    """<style>
section[data-testid="stSidebar"] .stButton button {
 background:none; border:none; text-align:left; padding:.3rem .6rem;
 font-size:1.2rem; font-weight:700; line-height:1.1;
}
section[data-testid="stSidebar"] .stButton button:hover {
 background-color:rgba(44,123,229,.1); border-radius:5px;
}
section[data-testid="stSidebar"] .stButton button p {text-align:left;}
</style>""",
    unsafe_allow_html=True,
)
if st.session_state.language == "ar":
    st.markdown(
        """<style>
    [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
    [data-testid="stRadio"] label, [data-testid="stButton"] button p {
        direction:rtl; text-align:right;
    }
    [data-testid="stNumberInput"] input {direction:ltr; text-align:left;}
    </style>""",
        unsafe_allow_html=True,
    )
ids = ["home", "importance", "pores", "beach", "resources", "lab"]
pages = {
    id: st.Page(
        "content/" + id + ".py", title=tr(id), url_path=id, default=id == "home"
    )
    for id in ids
}
st.session_state["_pages"] = pages
active = st.navigation(list(pages.values()), position="hidden")
destination = None
for id in ids:
    if id == "importance":
        st.sidebar.markdown("**" + tr("core") + "**")
    if id == "lab":
        st.sidebar.markdown("**" + tr("extra") + "**")
    marker = " 👈" if active.url_path == pages[id].url_path else ""
    if st.sidebar.button(ICONS[id] + " " + tr(id) + marker, key="nav_" + id):
        destination = pages[id]


# Callback runs before rendering on rerun: no one-rerun delay or rerun loop.
def set_language(lang):
    st.session_state.language = lang


st.sidebar.markdown("---")
st.sidebar.markdown("#### 🌍 " + tr("language"))
items = list(LANGUAGES.items())
for start in range(0, len(items), 4):
    for col, (lang, (flag, name)) in zip(
        st.sidebar.columns(4), items[start : start + 4]
    ):
        col.button(
            flag, key="lang_" + lang, help=name, on_click=set_language, args=(lang,)
        )
st.sidebar.caption(
    tr("module_language") + ": " + LANGUAGES[st.session_state.language][1]
)
st.sidebar.markdown("---")
layout_labels = {value: tr(value) for value in ["centered", "wide"]}
layout_key = "_layout_ui_" + st.session_state.language
st.session_state[layout_key] = st.session_state.layout_choice


def save_layout():
    value = st.session_state.get(layout_key)
    st.session_state.layout_choice = (
        value if value in ("centered", "wide") else "centered"
    )


st.sidebar.radio(
    tr("layout"),
    ["centered", "wide"],
    format_func=lambda value, labels=layout_labels: labels[value],
    key=layout_key,
    on_change=save_layout,
)
st.sidebar.link_button("The Groundwater Project", "https://gw-project.org/")
# Render every common widget before switching, including on navigation runs.
if destination is not None:
    st.switch_page(destination)
active.run()
