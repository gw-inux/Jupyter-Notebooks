"""Connect underground materials to pore space and a volume experiment."""

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
from core.figures import pores, sample_cup, cup_step
from core.models import sample_volumes


def volume_input(label, storage_key, use_slider, maximum=1000):
    """Keep solids inside the sample; sliders round to the nearest 10 mL.

    Numbers retain whole-mL precision. Switching to sliders rounds both
    values and reports that change. All corrections precede widget creation.
    """
    widget_key = storage_key + "_slider" if use_slider else storage_key
    values = st.session_state.setdefault("activity_values", {})
    old = int(round(values.get(storage_key, 0)))
    value = min(maximum, max(0, old))
    if use_slider:
        value = min(maximum, 10 * ((value + 5) // 10))
    values[storage_key] = value
    st.session_state[widget_key] = value
    widget = st.slider if use_slider else st.number_input
    result = widget(
        label,
        min_value=0,
        max_value=max(10, maximum) if use_slider else maximum,
        step=10,
        format="%d",
        key=widget_key,
        disabled=maximum == 0,
        on_change=remember_activity,
        args=(widget_key, storage_key),
    )
    if use_slider and old != value and 0 <= old <= maximum:
        st.caption(tr("slider_rounding"))
    return result


heading("pores")
st.subheader(tr("underground_heading"), divider="orange")
md("pores")
with expander(tr("controls"), "controls", expanded=True):
    saturated = st.toggle(
        tr("saturated"),
        value=activity_value("pore_saturated", False),
        key="pore_saturated",
        on_change=remember_activity,
        args=("pore_saturated",),
    )
show(pores(saturated, tr))
st.caption(tr("pore_caption"))
st.subheader(tr("experiment"), divider="orange")
md("cup_intro")
with expander(tr("controls"), "controls", expanded=True):
    use_slider = st.toggle(
        tr("cup_slider_input"),
        value=activity_value("cup_slider_input", False),
        key="cup_slider_input",
        on_change=remember_activity,
        args=("cup_slider_input",),
    )
    left, right = st.columns(2)
    with left:
        bulk = volume_input(tr("bulk"), "bulk_ml", use_slider)
    with right:
        solid = volume_input(tr("solid_volume"), "solid_ml", use_slider, bulk)
n = None
try:
    pore, n = sample_volumes(bulk, solid)
except ValueError:
    st.warning(tr("invalid_solids"))
else:
    if n is None:
        st.info(tr("empty_sample"))
    else:
        show(sample_cup(bulk, solid, tr))
        st.caption(tr("cup_caption"))
        if n in [0.0, 1.0]:
            st.info(tr("end_volume"))
# The explanation remains available even before any measurements are entered.
with expander(tr("more")):
    if n is not None:
        # Keep native text results accessible alongside the values in the figure.
        col1, col2 = st.columns(2)
        col1.metric(tr("pore_volume"), f"{pore:g} mL")
        col2.metric(tr("porosity_value"), f"{n*100:.1f}%")
    md("porosity_detail")
    st.latex(r"n=\frac{V_p}{V_t}=\frac{V_t-V_s}{V_t}")
    if n is not None:
        st.latex(f"n=\\frac{{{bulk:g}-{solid:g}}}{{{bulk:g}}}={n:.3f}")
with expander(tr("hands_on"), "controls"):
    for step, column in enumerate(st.columns(3), start=1):
        with column:
            st.markdown(f"**{step} · {tr('cup_step_' + str(step))}**")
            show(cup_step(step))
            st.caption(tr("cup_step_note_" + str(step)))
    md("cup")
quiz_group("grains", "porosity", "connectivity")
source_links("S5", "S6", "S7", "S8")
next_page("beach")
