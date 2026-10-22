"""Follow recharge, observe a beach, then transfer the idea to a river."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import (
    heading,
    show,
    source_links,
    quiz_group,
    next_page,
    expander,
    activity_value,
    remember_activity,
    responsive_image,
    centered_link,
)
from core.figures import beach, cycle, river
from core.sources import SOURCES
from core.models import beach_hole, POSITIONS, DEPTHS
from core.river import RIVER_REGIMES, RIVER_POSITIONS, RIVER_DEPTHS, river_observation


def position_labels(options):
    """Name original landmarks; intermediate stops use their position out of 7."""
    return {
        key: f"{number}/{len(options)}" if key.startswith("position_") else tr(key)
        for number, key in enumerate(options, start=1)
    }


heading("beach")
st.subheader(tr("cycle_path_heading"), divider="green")
md("cycle")
show(cycle(tr))
st.caption(tr("cycle_caption"))
st.markdown(tr("cycle_boundary") + " [S11]")
with expander(tr("more")):
    md("cycle_detail")
    poster = ROOT / "assets/images" / f"water_cycle_{st.session_state.language}.jpg"
    if not poster.is_file():
        poster = ROOT / "assets/images/water_cycle_en.jpg"
    _, preview, _ = st.columns([1, 2, 1])
    with preview:
        responsive_image(str(poster))
        st.caption(tr("cycle_preview_caption").format(url=SOURCES["S2"][1]))
    next_page("home", tr("cycle_full_link"))
st.subheader(tr("dig"), divider="green")
md("beach")
# Values stay language-independent; only their presentation is translated.
labels = {**position_labels(POSITIONS), **{key: tr(key) for key in DEPTHS}}
with expander(tr("controls"), "controls", expanded=True):
    position_col, depth_col, reveal_col = st.columns([1.1, 1.2, 1])
    location = position_col.select_slider(
        tr("position"),
        list(POSITIONS),
        value=activity_value("hole_position", "near"),
        format_func=lambda key: labels[key],
        key="hole_position",
        on_change=remember_activity,
        args=("hole_position",),
    )
    depth_label = depth_col.radio(
        tr("depth"),
        list(DEPTHS),
        horizontal=False,
        index=list(DEPTHS).index(activity_value("hole_depth", "shallow")),
        format_func=lambda key: labels[key],
        key="hole_depth",
        on_change=remember_activity,
        args=("hole_depth",),
    )
    reveal = reveal_col.toggle(
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
    st.markdown(
        f"[{tr('soilwater_link')}](https://gwp-soilwaterretention-update.streamlit.app/)"
    )
with expander(tr("field"), "controls"):
    md("field")
    photo = ROOT / "assets/images/beach_observation.png"
    if not photo.is_file():
        photo = ROOT / "assets/images/beach_observation.jpg"
    if photo.is_file():
        responsive_image(str(photo), caption=tr("beach_photo"))
    else:
        with st.container(border=True):
            st.markdown("📷 **" + tr("beach_photo") + "**")
            st.caption(tr("beach_photo_placeholder"))

# Transfer: both directions of exchange, with one hypothetical observation hole.
st.subheader(tr("river_heading"), divider="green")
md("river_intro")
# Capture labels during this run; callbacks must not read a later language state.
regime_labels = {value: tr("river_" + value) for value in RIVER_REGIMES}
river_labels = {
    **position_labels(RIVER_POSITIONS),
    **{key: tr(key) for key in RIVER_DEPTHS},
}
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
    position_col, depth_col, reveal_col = st.columns([1.1, 1.2, 1])
    location = position_col.select_slider(
        tr("river_position"),
        list(RIVER_POSITIONS),
        value=activity_value("river_position", "river_near"),
        format_func=river_labels.__getitem__,
        key="river_position",
        on_change=remember_activity,
        args=("river_position",),
    )
    depth = depth_col.radio(
        tr("river_depth"),
        RIVER_DEPTHS,
        index=RIVER_DEPTHS.index(activity_value("river_depth", "river_shallow")),
        format_func=river_labels.__getitem__,
        key="river_depth",
        on_change=remember_activity,
        args=("river_depth",),
    )
    reveal = reveal_col.toggle(
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
    centered_link(
        tr("boundary_link"),
        "https://gwp-boundary-conditions-intro.streamlit.app/",
        "boundary",
    )
quiz_group("recharge", "beach", "exchange")
source_links("S5", "S10", "S9", "S11", "S13", "S14")
next_page("resources")
