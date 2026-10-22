"""Optional coastal exploration: natural and pumped equilibrium scenarios."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import (
    heading,
    show,
    source_links,
    quiz_group,
    expander,
    responsive_image,
    next_page,
    reset_button,
    activity_value,
    remember_activity,
)
from core.figures import lens, density_principle
from core.coastal import ISLAND, island_profile, pumping_limit, freshwater_volume

heading("lab")
st.subheader(tr("lens_heading"), divider="violet")
md("lens")
responsive_image(str(ROOT / "assets/images/island_palmyra.jpg"))
md("island_photo")
with expander(tr("controls"), "controls", expanded=True):
    scenario = activity_value("lens_scenario", "natural")
    st.markdown("**" + tr("scenario") + "**")

    def choose_scenario(value):
        st.session_state.setdefault("activity_values", {})["lens_scenario"] = value

    for column, value in zip(st.columns(2), ["natural", "pumping"]):
        column.button(
            tr(value),
            key="scenario_" + value,
            type="primary" if scenario == value else "secondary",
            on_click=choose_scenario,
            args=(value,),
        )
    head = st.slider(
        tr("lens_level"),
        0.1,
        1.0,
        value=float(activity_value("lens_head", 0.8)),
        step=0.1,
        format="%.1f m",
        key="lens_head",
        on_change=remember_activity,
        args=("lens_head",),
    )
    pumping = 0.0
    if scenario == "pumping":
        # Round DOWN to cents: the slider can never exceed the model bound.
        maximum = int(pumping_limit(head) * 100) / 100
        stored = min(maximum, max(0.0, float(activity_value("pumping_rate", 0.0))))
        st.session_state["pumping_rate"] = stored
        pumping = st.slider(
            tr("pumping_rate"),
            0.0,
            maximum,
            step=0.01,
            format="%.2f m³/d",
            key="pumping_rate",
            on_change=remember_activity,
            args=("pumping_rate",),
        )
        # Persist the clamp when recharge/head changes or on a language switch.
        st.session_state["activity_values"]["pumping_rate"] = pumping
        st.caption(tr("pumping_range"))
show(lens(head, tr, pumping, scenario == "pumping"))
st.caption(tr("lens_caption"))
natural, pumped = st.columns(2)
with natural:
    st.markdown("**" + tr("without_pumping") + "**")
    st.metric(tr("peak_head"), f"{head:.1f} m")
    st.metric(tr("interface_depth"), f"{head*ISLAND.alpha:.1f} m")
    st.metric(tr("freshwater_volume"), f"{freshwater_volume(head):,.0f} m³")
if scenario == "pumping":
    well_head, well_depth = map(
        float, island_profile(ISLAND.well_radius_m, head, pumping)
    )
    baseline_head, baseline_depth = map(
        float, island_profile(ISLAND.well_radius_m, head)
    )
    with pumped:
        st.markdown("**" + tr("at_pumping_well") + "**")
        st.metric(
            tr("well_head"),
            f"{well_head:.2f} m",
            f"{well_head-baseline_head:+.2f} m",
            delta_color="off",
        )
        st.metric(
            tr("interface_depth"),
            f"{well_depth:.2f} m",
            f"{well_depth-baseline_depth:+.2f} m",
            delta_color="off",
        )
        st.metric(
            tr("freshwater_volume"),
            f"{freshwater_volume(head,pumping):,.0f} m³",
            f"{freshwater_volume(head,pumping)-freshwater_volume(head):+,.0f} m³",
            delta_color="off",
        )
    st.caption(tr("pumping_change_note"))
st.caption(tr("lens_values_note"))
with expander(tr("equations")):
    md("lens_model")
    show(density_principle(tr))
    st.caption(tr("density_caption"))
    st.latex(
        r"z=\frac{\rho_f}{\rho_s-\rho_f}\,h=\alpha h\quad\Rightarrow\quad z\approx40h"
    )
    md("density_parameters")
with expander(tr("model_assumptions")):
    md("island_model")
quiz_group("lens", "density", "lens_scope")
source_links("S12", "S15", "S16", "S17", "S18")
next_page("resources", "← " + tr("back_reflect"))
reset_button()
