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
from core.figures import lens, density_principle, head_detail
from core.coastal import ISLAND, island_profile, pumping_limit, freshwater_volume

heading("lab")
st.subheader(tr("lens_heading"), divider="violet")
md("lens")
responsive_image(str(ROOT / "assets/images/island_corn.jpg"))
md("island_photo")
with expander(tr("controls"), "controls", expanded=True):
    scenario_labels = {value: tr(value) for value in ("natural", "pumping")}
    scenario = st.radio(
        tr("scenario"),
        ("natural", "pumping"),
        horizontal=True,
        index=("natural", "pumping").index(activity_value("lens_scenario", "natural")),
        format_func=scenario_labels.__getitem__,
        key="lens_scenario",
        on_change=remember_activity,
        args=("lens_scenario",),
    )
    head_control, detail = st.columns([1.15, 1])
    with head_control:
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
        st.caption(tr("head_detail_caption"))
    with detail:
        show(head_detail(head, tr))
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
if scenario == "pumping":
    well_head, well_depth = map(
        float, island_profile(ISLAND.well_radius_m, head, pumping)
    )
    baseline_head, baseline_depth = map(
        float, island_profile(ISLAND.well_radius_m, head)
    )
    st.markdown("**" + tr("at_pumping_well") + "**")
    level_column, interface_column, volume_column = st.columns(3)
    with level_column:
        st.metric(
            tr("well_head"),
            f"{well_head:.2f} m",
            f"{well_head-baseline_head:+.2f} m",
            delta_color="off",
        )
    with interface_column:
        st.metric(
            tr("interface_depth"),
            f"{well_depth:.2f} m",
            f"{well_depth-baseline_depth:+.2f} m",
            delta_color="off",
        )
    with volume_column:
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
    density_control, _ = st.columns(2)
    density_head = density_control.slider(
        tr("density_head"),
        0.1,
        1.0,
        value=float(activity_value("density_head", 0.8)),
        step=0.1,
        format="%.1f m",
        key="density_head",
        on_change=remember_activity,
        args=("density_head",),
    )
    show(density_principle(tr, density_head))
    st.caption(f"h = {density_head:.1f} m · z = {ISLAND.alpha * density_head:.1f} m")
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
