"""Follow recharge, observe a beach, then transfer the idea to a river."""

import streamlit as st
from core.i18n import tr, md
from core.ui import (
    heading,
    show,
    source_links,
    quiz_group,
    next_page,
    expander,
    activity_value,
    remember_activity,
)
from core.figures import beach, cycle, river
from core.models import beach_hole, POSITIONS, DEPTHS
from core.river import RIVER_REGIMES, RIVER_POSITIONS, RIVER_DEPTHS, river_observation

heading("beach")
st.subheader(tr("cycle_path_heading"), divider="green")
md("cycle")
show(cycle(tr))
st.caption(tr("cycle_caption"))
st.markdown(tr("cycle_boundary") + " [S15]")
with expander(tr("more")):
    md("cycle_detail")
st.subheader(tr("dig"), divider="green")
md("beach")
# Values stay language-independent; only their presentation is translated.
labels = {key: tr(key) for key in list(POSITIONS) + list(DEPTHS)}
with expander(tr("controls"), "controls", expanded=True):
    location = st.select_slider(
        tr("position"),
        list(POSITIONS),
        value=activity_value("hole_position", "near"),
        format_func=lambda key: labels[key],
        key="hole_position",
        on_change=remember_activity,
        args=("hole_position",),
    )
    depth_label = st.radio(
        tr("depth"),
        list(DEPTHS),
        horizontal=True,
        index=list(DEPTHS).index(activity_value("hole_depth", "shallow")),
        format_func=lambda key: labels[key],
        key="hole_depth",
        on_change=remember_activity,
        args=("hole_depth",),
    )
    reveal = st.toggle(
        tr("show_water"),
        value=activity_value("beach_reveal", False),
        key="beach_reveal",
        on_change=remember_activity,
        args=("beach_reveal",),
    )
x = POSITIONS[location]
depth = DEPTHS[depth_label]
show(beach(x, depth, reveal, tr))
st.caption(tr("schematic"))
if reveal:
    water = beach_hole(x, depth)[3]
    st.info(tr("water_found") if water > 1e-9 else tr("no_water"))
with expander(tr("more") + " · " + tr("beach")):
    md("beach_limits")
with expander(tr("field"), "controls"):
    md("field")

# Transfer: both directions of exchange, with one hypothetical observation hole.
st.subheader(tr("river_heading"), divider="green")
md("river_intro")
# Capture labels during this run; callbacks must not read a later language state.
regime_labels = {value: tr("river_" + value) for value in RIVER_REGIMES}
river_labels = {value: tr(value) for value in (*RIVER_POSITIONS, *RIVER_DEPTHS)}
with expander(tr("controls"), "controls", expanded=True):
    regime = st.radio(
        tr("river_mode"),
        RIVER_REGIMES,
        index=RIVER_REGIMES.index(activity_value("river_regime", "gaining")),
        format_func=regime_labels.__getitem__,
        key="river_regime",
        on_change=remember_activity,
        args=("river_regime",),
    )
    location = st.select_slider(
        tr("river_position"),
        list(RIVER_POSITIONS),
        value=activity_value("river_position", "river_near"),
        format_func=river_labels.__getitem__,
        key="river_position",
        on_change=remember_activity,
        args=("river_position",),
    )
    depth = st.radio(
        tr("river_depth"),
        RIVER_DEPTHS,
        index=RIVER_DEPTHS.index(activity_value("river_depth", "river_shallow")),
        format_func=river_labels.__getitem__,
        key="river_depth",
        on_change=remember_activity,
        args=("river_depth",),
    )
    reveal = st.toggle(
        tr("show_water"),
        value=activity_value("river_reveal", False),
        key="river_reveal",
        on_change=remember_activity,
        args=("river_reveal",),
    )
river_x = RIVER_POSITIONS[location]
show(river(river_x, depth, regime, reveal, tr))
st.caption(tr("river_caption"))
if reveal:
    observation = river_observation(river_x, depth, regime)
    st.info(tr("water_found") if observation.water_depth > 0 else tr("no_water"))
    st.markdown(tr("river_explain_" + regime))
with expander(tr("more")):
    md("river_detail")
quiz_group("recharge", "beach", "exchange")
source_links("S3", "S5", "S13", "S15", "S16", "S17")
next_page("resources")
