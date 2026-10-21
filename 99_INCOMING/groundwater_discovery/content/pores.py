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
from core.figures import pores, sample_cup
from core.models import sample_volumes


def volume_input(label, storage_key, use_slider):
    """Share whole-mL values between number and slider widgets.

    Separate widget keys avoid type/identity conflicts when switching modes.
    A one-mL slider step preserves integers typed into the number input.
    """
    widget_key = storage_key + "_slider" if use_slider else storage_key
    value = int(round(activity_value(storage_key, 0)))
    widget = st.slider if use_slider else st.number_input
    return widget(
        label,
        min_value=0,
        max_value=2000,
        value=value,
        step=1 if use_slider else 10,
        format="%d",
        key=widget_key,
        on_change=remember_activity,
        args=(widget_key, storage_key),
    )


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
    bulk = volume_input(tr("bulk"), "bulk_ml", use_slider)
    solid = volume_input(tr("solid_volume"), "solid_ml", use_slider)
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
        col1, col2 = st.columns(2)
        col1.metric(tr("pore_volume"), f"{pore:g} mL")
        col2.metric(tr("porosity_value"), f"{n*100:.1f}%")
        if n in [0.0, 1.0]:
            st.info(tr("end_volume"))
# The explanation remains available even before any measurements are entered.
with expander(tr("more")):
    md("porosity_detail")
    st.latex(r"n=\frac{V_p}{V_t}=\frac{V_t-V_s}{V_t}")
    if n is not None:
        st.latex(f"n=\\frac{{{bulk:g}-{solid:g}}}{{{bulk:g}}}={n:.3f}")
with expander(tr("hands_on"), "controls"):
    md("cup")
quiz_group("grains", "porosity", "connectivity")
source_links("S3", "S4", "S10", "S11")
next_page("beach")
