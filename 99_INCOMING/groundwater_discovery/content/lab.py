"""Optional density comparison: read the section before changing its level."""

import streamlit as st
from core.i18n import tr, md
from core.ui import heading, show, source_links, quiz_group, expander
from core.figures import lens
from core.models import LENS_LEVELS, density_ratio
from core.sources import FLOW_MODULE_URL, SOURCES

heading("lab")
st.subheader(tr("lens_heading"), divider="violet")
md("lens")
labels = {key: tr(key) for key in LENS_LEVELS}
# Keep the physical selection independent of translated slider labels and
# multipage widget cleanup, just as the layout setting is kept in app.py.
if st.session_state.get("lens_choice") not in LENS_LEVELS:
    st.session_state["lens_choice"] = "higher"


def save_level():
    st.session_state["lens_choice"] = st.session_state["lens_level"]


with expander(tr("controls"), "controls", expanded=True):
    level = st.select_slider(
        tr("lens_level"),
        list(LENS_LEVELS),
        value=st.session_state["lens_choice"],
        format_func=lambda key: labels[key],
        key="lens_level",
        on_change=save_level,
    )
head = LENS_LEVELS[level]
show(lens(head, tr))
st.caption(tr("lens_caption"))
col1, col2 = st.columns(2)
col1.metric(tr("peak_head"), f"{head:.1f} m")
col2.metric(tr("interface_depth"), f"{head*density_ratio():.1f} m")
st.caption(tr("lens_values_note"))
with expander(tr("equations")):
    md("lens_model")
quiz_group("lens", "density", "lens_scope")
source_links("S6", "S8", "S9", "S12")
st.subheader(tr("learn_more"), divider="violet")
st.link_button(tr("advanced_link"), FLOW_MODULE_URL)
st.link_button(tr("book") + " · Analytical Groundwater Modeling", SOURCES["S7"][1])
