# Loading the required Python libraries
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

from GWP_Pumping_Test_Derivatives_utils import load_css
from applied_derivative_utils import theis_response
from inner_boundary_utils import pumping_well_response, theis_skin_response

# Authors, institutions, and year
year = 2026
authors = {"Thomas Reimann": [1, 2]}
institutions = {
    1: "The Groundwater Project",
    2: "TU Dresden, Institute for Groundwater Management",
}

author_list = []
for name, indices in authors.items():
    superscript = ",".join(str(i) for i in indices)
    author_list.append(f"{name}<sup>{superscript}</sup>")
institution_list = [f"<sup>{i}</sup> {inst}" for i, inst in institutions.items()]
institution_text = ", ".join(institution_list)

# Project paths / styling
APP_ROOT = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives")
if not APP_ROOT.exists():
    APP_ROOT = Path.cwd()
CSS_DIR = APP_ROOT / "assets" / "css"
load_css(CSS_DIR, "segment_control_Theis_Deriv_Ini.css")


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _positive(values):
    values = np.asarray(values, dtype=float)
    return np.isfinite(values) & (values > 0)


def _on_off_radio(label, key, default=False):
    return st.radio(
        label,
        options=["Off", "On"],
        index=1 if default else 0,
        horizontal=True,
        key=key,
    ) == "On"


def _plot_diagnostic(
    curves,
    *,
    show_drawdown=True,
    show_derivative=True,
    semilog=False,
    show_ground_model=True,
    ground=None,
    show_gwm=False,
    gwm=None,
    title="Inner-boundary effects",
):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    positive_values = []

    for i, curve in enumerate(curves):
        t = np.asarray(curve["time"], dtype=float)
        s = np.asarray(curve["drawdown"], dtype=float)
        d = np.asarray(curve["derivative"], dtype=float)
        label = curve["label"]
        color = colors[i % len(colors)]
        if show_drawdown:
            m = _positive(s)
            ax.plot(t[m], s[m], linewidth=2.1, color=color, label=f"Drawdown: {label}")
            positive_values.extend(s[m].tolist())
        if show_derivative:
            m = _positive(d)
            ax.plot(t[m], d[m], "--", linewidth=2.0, color=color, label=f"Derivative: {label}")
            positive_values.extend(d[m].tolist())

    if show_ground_model and ground is not None:
        t, s, d = ground
        if show_drawdown:
            m = _positive(s)
            ax.plot(t[m], s[m], ":", color="0.35", linewidth=1.7, label="Ground model (no inner boundary)")
            positive_values.extend(np.asarray(s)[m].tolist())
        if show_derivative:
            m = _positive(d)
            ax.plot(t[m], d[m], "-.", color="0.35", linewidth=1.5, label="Ground-model derivative")
            positive_values.extend(np.asarray(d)[m].tolist())

    if show_gwm and gwm is not None:
        t, s, d = gwm
        if show_drawdown:
            m = _positive(s)
            ax.plot(t[m], s[m], linewidth=1.6, alpha=0.65, label="Observation well at 30 m")
            positive_values.extend(np.asarray(s)[m].tolist())
        if show_derivative:
            m = _positive(d)
            ax.plot(t[m], d[m], "--", linewidth=1.4, alpha=0.65, label="Observation-well derivative")
            positive_values.extend(np.asarray(d)[m].tolist())

    ax.set_xscale("log")
    if not semilog:
        ax.set_yscale("log")
    ax.set_xlim(1e-2, 1e5)
    if semilog:
        ymax = max(positive_values) if positive_values else 1.0
        ax.set_ylim(0.0, max(1.05 * ymax, 0.1))
    else:
        ax.set_ylim(1e-5, 1e2)
    ax.grid(which="both", alpha=0.3)
    ax.set_xlabel("time $t$ in s", fontsize=14)
    if show_drawdown and show_derivative:
        ax.set_ylabel(r"drawdown $s$ and derivative $ds/d\ln(t)$ in m", fontsize=14)
    elif show_derivative:
        ax.set_ylabel(r"drawdown derivative $ds/d\ln(t)$ in m", fontsize=14)
    else:
        ax.set_ylabel("drawdown $s$ in m", fontsize=14)
    ax.set_title(title, fontsize=16)
    ax.legend(fontsize=8.5, loc="best")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Page header / theory
# -----------------------------------------------------------------------------
st.header(
    "Understanding :orange[**Drawdown Derivatives**] with :orange[**inner boundaries**]",
    divider="orange",
)

st.markdown(
    """
**Inner boundaries** are effects created by the pumping well itself. This section focuses on the two effects emphasized in the diagnostic-plot report: **wellbore storage** and **well skin**. Both primarily affect the early-time response measured in the pumping well, whereas the infinite-acting radial-flow plateau remains the key phase for estimating transmissivity.
"""
)

st.subheader("Introduction", divider="orange")
st.markdown(
    r"""
At the start of pumping, part or all of the pumped water can come from the water stored inside the well. For a freely falling water column, the pure-storage limit is

$$s=\frac{Q}{\pi r_c^2}t,$$

so drawdown and its logarithmic-time derivative coincide and form a unit-slope line in a log-log diagnostic plot. As aquifer inflow takes over, the derivative develops the characteristic **wellbore-storage hump** before approaching the radial-flow plateau.

A steady skin represents an additional hydraulic resistance at the well-aquifer interface. Its drawdown contribution is

$$s_{skin}=\frac{Q}{2\pi T}S_F.$$

Without wellbore storage, this is a constant drawdown offset: the skin changes drawdown but **not** the derivative. When storage and skin occur together, the skin delays the transition from storage-dominated flow and increases/broadens the characteristic derivative hump.
"""
)

with st.expander(":orange[**Show/Hide the initial assessment**]"):
    st.write("1. What slope do drawdown and derivative have during pure wellbore storage?")
    st.write("2. Does a steady skin change the late radial-flow derivative plateau?")
    st.write("3. What happens to the storage hump when both well radius and positive skin increase?")

st.subheader("Explore :orange[inner-boundary effects] in diagnostic plots", divider="orange")

with st.expander(":orange[**General hydraulic setup**]", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        Q_lps = st.number_input(
            "Pumping rate Q in L/s", 0.01, 100.0, 2.0, 0.1,
            format="%.2f", key="ib_Q_lps"
        )
        Q = Q_lps / 1000.0
    with c2:
        T = 10.0 ** st.slider(
            "log₁₀ T [m²/s]", -6.0, -1.0, -2.0, 0.05, key="ib_logT"
        )
        st.caption(f"T = **{T:.3g} m²/s**")
    with c3:
        S = 10.0 ** st.slider(
            "log₁₀ S [-]", -7.0, -1.0, -3.0, 0.05, key="ib_logS"
        )
        st.caption(f"S = **{S:.3g}**")
    st.caption(
        "The defaults Q = 2 L/s, T = 0.01 m²/s and S = 0.001 reproduce the hydraulic setup used for the well-storage and skin examples in the report."
    )

active_tab = st.segmented_control(
    "Select topic",
    options=[
        "01: Storage and skin",
        "02: Vary wellbore storage",
        "03: Vary skin factor",
    ],
    default="01: Storage and skin",
    label_visibility="collapsed",
    key="ib_active_topic",
)
if active_tab is None:
    st.info("Please select one topic to continue.")
    st.stop()


@st.fragment
def _single_inner_case(Q_lps, Q, T, S):
    t = np.logspace(-2, 5, 260)
    top1, top2, top3 = st.columns(3, gap="medium")
    with top1:
        with st.expander(":red[**Plot settings**]"):
            show_drawdown = st.toggle("Show drawdown", True, key="ib1_show_s")
            show_derivative = st.toggle("Show derivative", True, key="ib1_show_d")
            show_ground = st.toggle("Show no-inner-boundary reference", True, key="ib1_ground")
            semilog = st.toggle("Toggle for **semi-log graph**", False, key="ib1_semilog")
    with top2:
        with st.expander(":blue[**Activate inner boundaries**]", expanded=True):
            use_storage = _on_off_radio("Wellbore storage", "ib1_storage", True)
            use_skin = _on_off_radio("Skin", "ib1_skin", True)
    with top3:
        with st.expander(":green[**Well geometry / skin**]", expanded=True):
            rw = st.number_input(
                "Effective screen radius r_w [m]", 0.005, 2.0, 0.10, 0.01,
                format="%.3f", key="ib1_rw"
            )
            if use_storage:
                rc = st.number_input(
                    "Casing/storage radius r_c [m]", 0.005, 2.0, 0.10, 0.01,
                    format="%.3f", key="ib1_rc"
                )
            else:
                rc = None
            if use_skin:
                sf_min = 0.0 if use_storage else -10.0
                if "ib1_SF" in st.session_state:
                    st.session_state["ib1_SF"] = float(
                        np.clip(st.session_state["ib1_SF"], sf_min, 100.0)
                    )
                SF = st.slider(
                    "Skin factor S_F [-]",
                    float(sf_min),
                    100.0,
                    5.0,
                    1.0,
                    key="ib1_SF",
                )
                if use_storage:
                    st.caption("For the combined storage + skin formulation, S_F is restricted to non-negative values. Negative skin can be explored with storage switched off.")
            else:
                SF = 0.0

    if not show_drawdown and not show_derivative:
        st.info("Select drawdown and/or derivative.")
        return

    s, d = pumping_well_response(t, Q, T, S, rw, rc=rc, skin=SF)
    ref_s, ref_d = pumping_well_response(t, Q, T, S, rw, rc=None, skin=0.0)
    _plot_diagnostic(
        [{"time": t, "drawdown": s, "derivative": d, "label": "selected inner boundaries"}],
        show_drawdown=show_drawdown,
        show_derivative=show_derivative,
        semilog=semilog,
        show_ground_model=show_ground,
        ground=(t, ref_s, ref_d),
        title="Wellbore storage and skin",
    )

    d_plateau = Q / (4.0 * np.pi * T)
    st.caption(
        f"Radial-flow derivative reference d = Q/(4πT) = **{d_plateau:.3g} m**. "
        + ("During the earliest storage-controlled period, drawdown and derivative should approach the same unit-slope trend. " if use_storage else "")
        + ("A steady skin increases pumping-well drawdown; without storage it does not change the derivative." if use_skin else "")
    )
    if use_storage and use_skin:
        st.info(
            "With both effects active, the calculation uses the finite-radius well solution with wellbore storage and a steady skin boundary condition. Positive skin prolongs the storage-dominated transition and enlarges the derivative hump."
        )


@st.fragment
def _storage_variation(Q, T, S):
    t = np.logspace(-2, 5, 260)
    c1, c2 = st.columns((1, 2), gap="medium")
    with c1:
        with st.expander(":red[**Plot settings**]", expanded=False):
            show_drawdown = st.toggle("Show drawdown", True, key="ib2_show_s")
            show_derivative = st.toggle("Show derivative", True, key="ib2_show_d")
            show_ground = st.toggle("Show report ground model", True, key="ib2_ground")
            show_gwm = st.toggle("Show observation well at 30 m", True, key="ib2_gwm")
            semilog = st.toggle("Toggle for **semi-log graph**", False, key="ib2_semilog")
    with c2:
        st.markdown(
            "**Report benchmark:** vary the well radius while Q, T and S remain fixed. The report uses r_w = r_c and the radii 0.05, 0.10, 0.25 and 0.50 m."
        )
        radii = []
        cols = st.columns(4)
        defaults = [0.05, 0.10, 0.25, 0.50]
        for i, (col, default) in enumerate(zip(cols, defaults), 1):
            with col:
                radii.append(st.number_input(
                    f"r_c{i}=r_w{i} [m]", 0.005, 2.0, default, 0.01,
                    format="%.3f", key=f"ib2_rc_{i}"
                ))

    curves = []
    for rc in radii:
        s, d = pumping_well_response(t, Q, T, S, rc, rc=rc, skin=0.0)
        curves.append({"time": t, "drawdown": s, "derivative": d, "label": f"r_c = {rc:g} m"})
    # The report's ground-model curve uses the line-source limit; 1e-10 m is
    # the value explicitly shown in its conceptual sketch for the analogous skin example.
    ground = theis_response(t, Q, T, S, 1e-10)
    gwm = theis_response(t, Q, T, S, 30.0)
    _plot_diagnostic(
        curves,
        show_drawdown=show_drawdown,
        show_derivative=show_derivative,
        semilog=semilog,
        show_ground_model=show_ground,
        ground=(t, ground[0], ground[1]),
        show_gwm=show_gwm,
        gwm=(t, gwm[0], gwm[1]),
        title="Effect of wellbore-storage radius",
    )
    st.caption(
        "Expected diagnostic signature: increasing r_c delays the end of wellbore storage and moves the derivative hump to later time. The early drawdown and derivative approach the same m = 1 trend; after storage dissipates, the derivative returns to the same radial-flow plateau."
    )


@st.fragment
def _skin_variation(Q, T, S):
    t = np.logspace(-2, 5, 260)
    c1, c2 = st.columns((1, 2), gap="medium")
    with c1:
        with st.expander(":red[**Plot settings**]", expanded=False):
            show_drawdown = st.toggle("Show drawdown", True, key="ib3_show_s")
            show_derivative = st.toggle("Show derivative", True, key="ib3_show_d")
            show_ground = st.toggle("Show ground model", True, key="ib3_ground")
            show_gwm = st.toggle("Show observation well at 30 m", True, key="ib3_gwm")
            semilog = st.toggle("Toggle for **semi-log graph**", False, key="ib3_semilog")
    with c2:
        st.markdown(
            "**Report benchmark:** the skin example uses the line-source limit (r_w = r_c = 10⁻¹⁰ m) and varies S_F = −5, 5, 10 and 50."
        )
        cols = st.columns(4)
        defaults = [-5.0, 5.0, 10.0, 50.0]
        skins = []
        for i, (col, default) in enumerate(zip(cols, defaults), 1):
            with col:
                skins.append(st.number_input(
                    f"S_F{i} [-]", -20.0, 100.0, default, 1.0,
                    key=f"ib3_sf_{i}"
                ))

    rw = 1e-10
    curves = []
    for sf in skins:
        s, d = theis_skin_response(t, Q, T, S, rw, sf)
        curves.append({"time": t, "drawdown": s, "derivative": d, "label": f"S_F = {sf:g}"})
    ground = theis_skin_response(t, Q, T, S, rw, 0.0)
    gwm = theis_response(t, Q, T, S, 30.0)
    _plot_diagnostic(
        curves,
        show_drawdown=show_drawdown,
        show_derivative=show_derivative,
        semilog=semilog,
        show_ground_model=show_ground,
        ground=(t, ground[0], ground[1]),
        show_gwm=show_gwm,
        gwm=(t, gwm[0], gwm[1]),
        title="Effect of the skin factor",
    )
    st.caption(
        "Expected diagnostic signature: the steady skin shifts pumping-well drawdown by Q·S_F/(2πT), while the derivative is unchanged. Consequently, the radial-flow derivative plateau still yields T even when pumping-well drawdown is strongly affected by skin."
    )


if active_tab.startswith("01"):
    st.markdown(
        "Activate **wellbore storage**, **skin**, neither, or both. This first topic demonstrates how the two inner boundaries interact in one pumping-well diagnostic plot."
    )
    _single_inner_case(Q_lps, Q, T, S)
elif active_tab.startswith("02"):
    st.markdown(
        "Investigate the parameter controlling **wellbore storage**. Larger well volume delays aquifer inflow and shifts the characteristic derivative hump to later time."
    )
    _storage_variation(Q, T, S)
elif active_tab.startswith("03"):
    st.markdown(
        "Investigate the **skin factor** independently. This reproduces the report's key result that steady skin changes pumping-well drawdown but leaves its derivative unchanged."
    )
    _skin_variation(Q, T, S)

with st.expander("**Click here for references**"):
    st.markdown(
        """
- Hekel, U. et al. (2025): *Pumpversuchsauswertung mittels Diagnostischer Plots – Ein Leitfaden für Praxis und Lehre*, Sections 2.6.1–2.6.3.
- Papadopulos, I. S. & Cooper, H. H. (1967): Drawdown in a well of large diameter. *Water Resources Research*, 3(1), 241–244.
- Agarwal, R. G., Al-Hussainy, R. & Ramey, H. J. Jr. (1970): An investigation of wellbore storage and skin effect in unsteady liquid flow: I. Analytical treatment. *Society of Petroleum Engineers Journal*, 10(3), 279–290.
- Bourdet, D. et al. (1989): Use of pressure derivative in well-test interpretation. *SPE Formation Evaluation*, 4(2), 293–302.
"""
    )

st.markdown("---")
columns_lic = st.columns((4, 1, 1))
with columns_lic[0]:
    st.markdown(
        f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}',
        unsafe_allow_html=True,
    )
with columns_lic[1]:
    st.image(str(APP_ROOT / "assets" / "images" / "gw_logo_horiz-mini.png"))
with columns_lic[2]:
    st.image(str(APP_ROOT / "assets" / "images" / "CC_BY-SA_icon.png"))
