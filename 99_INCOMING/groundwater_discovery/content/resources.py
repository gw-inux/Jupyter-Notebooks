"""Explain the core ideas, then choose a Groundwater Project reading."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import heading, expander
from core.sources import (
    SOURCES,
    FLOW_MODULE_URL,
    CHERRY_VIDEO_URL,
    CHERRY_START_SECONDS,
)

heading("resources")
st.subheader("👉 " + tr("reflection"), divider="violet")
md("reflection")
with expander(tr("reflection_guidance"), "reflection"):
    md("reflection_answers")
results = st.session_state.get("results", {})
core_ids = [
    "stores",
    "role",
    "limits",
    "grains",
    "porosity",
    "connectivity",
    "recharge",
    "beach",
    "exchange",
]
correct = sum(bool(results.get(q, {}).get("correct")) for q in core_ids)
st.caption(tr("progress") + f": {correct} / {len(core_ids)}")
st.subheader(tr("learn_more"), divider="violet")
md("resources_intro")
st.link_button("The Groundwater Project", "https://gw-project.org/", type="primary")
books = [
    (
        "cover_water_cycle.png",
        "Groundwater in Our Water Cycle",
        "Poeter, Fan, Cherry, Wood & Mackay (2020)",
        "groundwater-in-our-water-cycle",
    ),
    (
        "cover_hydrogeologic.png",
        "Hydrogeologic Properties of Earth Materials and Principles of Groundwater Flow",
        "Woessner & Poeter (2020)",
        "hydrogeologic-properties-of-earth-materials-and-principles-of-groundwater-flow",
    ),
    (
        "cover_exchange.png",
        "Groundwater–Surface Water Exchange: Rivers, Lakes, and Wetlands",
        "Woessner (2020)",
        "groundwater-surface-water-exchange",
    ),
]
for col, (cover, title, authors, slug) in zip(st.columns(3), books):
    with col:
        with st.container(border=True):
            path = ROOT / "assets/images" / cover
            if path.is_file():
                st.image(str(path), width="stretch")
            st.markdown("**" + title + "**")
            st.caption(authors)
            st.link_button(tr("book"), "https://gw-project.org/books/" + slug + "/")
st.caption(tr("cover_credit"))
with expander(tr("cherry_talk")):
    md("cherry_talk")
    st.video(CHERRY_VIDEO_URL, start_time=CHERRY_START_SECONDS)
    st.link_button(tr("watch_youtube"), f"{CHERRY_VIDEO_URL}&t={CHERRY_START_SECONDS}s")
st.link_button(tr("advanced_link"), FLOW_MODULE_URL)
with expander(tr("all_sources"), "sources"):
    for id, (title, url) in SOURCES.items():
        st.markdown(f"**[{id}]** [{title}]({url})")
with expander(tr("facilitator")):
    md("facilitator")
if st.button(tr("reset"), key="reset_session"):
    lang = st.session_state.language
    layout = st.session_state.layout_choice
    for key in list(st.session_state):
        del st.session_state[key]
    st.session_state.language = lang
    st.session_state.layout_choice = layout
    st.switch_page("content/home.py")
