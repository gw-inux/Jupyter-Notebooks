# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
from pathlib import Path
from GWP_Pumping_Test_Derivatives_utils import load_css
from GWP_Pumping_Test_Derivatives_utils import load_md

# Authors, institutions, and year
year = 2026
authors = {
    "Thomas Reimann": [1, 2],
}
institutions = {
    1: "The Groundwater Project",
    2: "TU Dresden, Institute for Groundwater Management",
}

# ------------------------------------------------------------
# Format authors / institutions
# ------------------------------------------------------------
author_list = []
for name, indices in authors.items():
    superscript = ",".join(str(i) for i in indices)
    author_list.append(f"{name}<sup>{superscript}</sup>")

institution_list = []
for i, inst in institutions.items():
    institution_list.append(f"<sup>{i}</sup> {inst}")
institution_text = ", ".join(institution_list)

# --------------------------------------------------
# Analytical functions
# --------------------------------------------------
def theis_u(T, S, r, t):
    """Theis dimensionless parameter u = r²S/(4Tt)."""
    t = np.asarray(t, dtype=float)
    return r**2 * S / (4.0 * T * t)


def theis_drawdown(T, S, t, Q, r):
    """Theis drawdown at radial distance r."""
    u = theis_u(T, S, r, t)
    return Q / (4.0 * np.pi * T) * scipy.special.exp1(u)


def theis_derivative_ln_time(T, S, t, Q, r):
    """Analytical Theis derivative ds/dln(t)."""
    u = theis_u(T, S, r, t)
    return Q / (4.0 * np.pi * T) * np.exp(-u)


def image_well_distance(boundary_distance, observation_distance, observation_position):
    """Return distance from the observation point to the image well.

    The pumping well is at x = +a, its image is at x = -a, and the straight
    boundary is at x = 0.  The observation well is assumed to lie on the same
    line perpendicular to the boundary.

    Parameters
    ----------
    boundary_distance : float
        Pumping-well-to-boundary distance a [m].
    observation_distance : float
        Pumping-well-to-observation distance r [m].
    observation_position : str
        Either ``"Between pumping well and boundary"`` or
        ``"Away from boundary"``.
    """
    a = float(boundary_distance)
    r = float(observation_distance)

    if observation_position == "Between pumping well and boundary":
        if r >= a:
            raise ValueError(
                "For an observation well between the pumping well and boundary, "
                "the observation distance r must be smaller than the boundary distance a."
            )
        return 2.0 * a - r

    if observation_position == "Away from boundary":
        return 2.0 * a + r

    raise ValueError(f"Unknown observation position: {observation_position}")

def boundary_sign(boundary_type):
    """Return +1 for a no-flow image pumping well and -1 for specified head."""
    if boundary_type == "No-flow boundary":
        return 1.0
    if boundary_type == "Specified-head boundary":
        return -1.0
    raise ValueError(f"Unknown boundary type: {boundary_type}")


def compute_boundary_response(
    T,
    S,
    t,
    Q,
    observation_distance,
    boundary_distance,
    boundary_type,
    observation_position="Between pumping well and boundary",
):
    """
    Theis solution adapted to one straight boundary by the method of images.

    Pumping Q is treated as a positive pumping-rate magnitude.

    No-flow boundary:
        same-sign image well (+Q)
        s = s_real + s_image

    Specified-head boundary:
        opposite-sign image well (-Q)
        s = s_real - s_image

    The derivative is superposed analytically in exactly the same way.
    """
    r_real = float(observation_distance)
    r_image = image_well_distance(
        boundary_distance, observation_distance, observation_position
    )
    sign = boundary_sign(boundary_type)

    s_real = theis_drawdown(T, S, t, Q, r_real)
    s_image = theis_drawdown(T, S, t, Q, r_image)

    d_real = theis_derivative_ln_time(T, S, t, Q, r_real)
    d_image = theis_derivative_ln_time(T, S, t, Q, r_image)

    return {
        "drawdown": s_real + sign * s_image,
        "derivative": d_real + sign * d_image,
        "theis_drawdown": s_real,
        "theis_derivative": d_real,
        "r_real": r_real,
        "r_image": r_image,
        "plateau": Q / (4.0 * np.pi * T),
    }


# --------------------------------------------------
# Streamlit widget helpers
# --------------------------------------------------
def update_log_parameter(prefix, suffix):
    """Synchronize number input with the persistent slider value."""
    st.session_state[f"{prefix}_slider_value_{suffix}"] = st.session_state[
        f"{prefix}_input_{suffix}"
    ]


def prepare_synced_widget_keys(prefix, suffix, default, use_number_input):
    """Prepare paired number-input/slider keys while retaining the current value."""
    slider_key = f"{prefix}_slider_value_{suffix}"
    input_key = f"{prefix}_input_{suffix}"
    mode_key = f"{prefix}_widget_mode_{suffix}"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = default

    new_mode = "number" if use_number_input else "slider"
    old_mode = st.session_state.get(mode_key)

    if new_mode == "number":
        if old_mode != "number" or input_key not in st.session_state:
            st.session_state[input_key] = st.session_state[slider_key]
    else:
        if old_mode == "number" and input_key in st.session_state:
            st.session_state[slider_key] = st.session_state[input_key]

    st.session_state[mode_key] = new_mode
    return slider_key, input_key


def log_widget(label, minimum, maximum, default, suffix, prefix, use_number_input):
    """Render a synchronized logarithmic parameter input and return log10(value)."""
    slider_key, input_key = prepare_synced_widget_keys(
        prefix, suffix, default, use_number_input
    )

    if use_number_input:
        return st.number_input(
            label,
            min_value=minimum,
            max_value=maximum,
            step=0.01,
            format="%4.2f",
            key=input_key,
            on_change=update_log_parameter,
            args=(prefix, suffix),
        )

    return st.slider(
        label,
        min_value=minimum,
        max_value=maximum,
        step=0.01,
        format="%4.2f",
        key=slider_key,
    )


def update_linear_parameter(prefix, suffix):
    """Synchronize a linear number input with its persistent slider value."""
    st.session_state[f"{prefix}_slider_value_{suffix}"] = st.session_state[
        f"{prefix}_input_{suffix}"
    ]


def boundary_distance_widget(
    label, default, suffix, use_number_input
):
    """Synchronized direct input for pumping-well-to-boundary distance a [m].

    The widget range is intentionally independent of the observation distance r.
    This keeps the physical pumping-well-to-boundary distance unchanged when the
    user modifies the observation location. Geometric compatibility (a > r when
    the observation point lies between pumping well and boundary) is checked
    separately after all inputs have been read.
    """
    prefix = "bc_D"
    min_distance = 10.0
    default = float(max(default, min_distance))

    slider_key, input_key = prepare_synced_widget_keys(
        prefix, suffix, default, use_number_input
    )

    if use_number_input:
        return st.number_input(
            label,
            min_value=min_distance,
            max_value=5000.0,
            step=10.0,
            format="%.0f",
            key=input_key,
            on_change=update_linear_parameter,
            args=(prefix, suffix),
        )

    return st.slider(
        label,
        min_value=min_distance,
        max_value=5000.0,
        step=10.0,
        format="%.0f m",
        key=slider_key,
    )


# --------------------------------------------------
# Small conceptual image-well sketch
# --------------------------------------------------
def plot_image_well_geometry(
    boundary_distance,
    observation_distance,
    boundary_type,
    observation_position,
):
    """Create a compact conceptual image-well sketch for the current geometry."""
    a = float(boundary_distance)
    r_obs = float(observation_distance)

    x_image = -a
    x_boundary = 0.0
    x_pump = a

    if observation_position == "Between pumping well and boundary":
        x_obs = a - r_obs
    else:
        x_obs = a + r_obs

    fig, ax = plt.subplots(figsize=(8, 2.2))

    ax.axvline(x_boundary, linestyle="--", linewidth=1.8, color="0.25")
    ax.axhline(0.0, linewidth=1.0, color="0.5")

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    real_color = colors[0]
    obs_color = colors[1]
    image_color = colors[2]

    ax.scatter([x_pump], [0], s=90, color=real_color, zorder=3)
    ax.scatter([x_obs], [0], s=80, color=obs_color, zorder=3)
    ax.scatter(
        [x_image], [0], s=90, facecolors="none", edgecolors=image_color,
        linewidth=2, zorder=3
    )

    ax.text(x_boundary, 0.12, "boundary", ha="center", va="bottom")
    ax.text(x_pump, -0.12, "pumping well\n+Q", ha="center", va="top")
    ax.text(x_obs, 0.12, "observation", ha="center", va="bottom")

    image_label = (
        "image pumping well\n+Q"
        if boundary_type == "No-flow boundary"
        else "image injection well\n−Q"
    )
    ax.text(x_image, -0.12, image_label, ha="center", va="top")

    ax.annotate(
        "",
        xy=(x_boundary, -0.33),
        xytext=(x_pump, -0.33),
        arrowprops=dict(arrowstyle="<->", linewidth=1.0),
    )
    ax.text(0.5 * (x_boundary + x_pump), -0.37, f"a = {a:.0f} m", ha="center", va="top")

    ax.annotate(
        "",
        xy=(x_pump, 0.33),
        xytext=(x_obs, 0.33),
        arrowprops=dict(arrowstyle="<->", linewidth=1.0),
    )
    ax.text(0.5 * (x_pump + x_obs), 0.37, f"r = {r_obs:.0f} m", ha="center", va="bottom")

    span = max(a, r_obs, 1.0)
    x_min = min(x_image, x_boundary, x_obs) - 0.15 * span
    x_max = max(x_pump, x_obs) + 0.15 * span
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.65, 0.65)
    ax.set_yticks([])
    ax.set_xlabel("conceptual coordinate perpendicular to the boundary")
    ax.spines[["left", "right", "top"]].set_visible(False)
    fig.tight_layout()
    return fig


# --------------------------------------------------
# Streamlit page
# --------------------------------------------------
MD_DIR = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/md")
CSS_DIR = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/css")

load_css(CSS_DIR, "segment_control_Theis_Deriv_Ini.css")


def render_boundary_markdown(filename, fallback):
    """Use the project's multilingual markdown file when present; otherwise show English fallback text."""
    path = MD_DIR / filename
    if path.exists():
        st.markdown(load_md(MD_DIR, filename, st.session_state.language))
    else:
        st.markdown(fallback)



st.header(
    "Understanding :orange[**Drawdown Derivatives**] with :orange[**hydraulic boundaries**]",
    divider="orange",
)

render_boundary_markdown(
    "boundary_deriv_01.md",
    """External hydraulic boundaries can change pumping-test drawdown once the cone of depression reaches the boundary. This section uses the Theis solution, the principle of superposition, and image wells to explore how those effects appear in drawdown and drawdown-derivative plots.""",
)

st.subheader("Introduction", divider="orange")
render_boundary_markdown(
    "boundary_deriv_02.md",
    """A no-flow boundary is represented by an image **pumping** well with the same pumping rate. A specified-head boundary is represented by an image **injection** well with the opposite rate. The real and image-well responses are superposed at the observation point.""",
)

# --------------------------------------------------
# Initial assessment
# --------------------------------------------------
render_boundary_markdown(
    "boundary_deriv_03.md",
    """Use the initial questions to check whether you can distinguish the expected late-time signatures of no-flow and specified-head boundaries.""",
)

with st.expander(":orange[**Show/Hide the initial assessment**]"):
    st.write("Show the initial assessment")

# --------------------------------------------------
# Theory
# --------------------------------------------------
st.subheader(
    "Underlying Theory - :orange[Theis superposition and image wells]",
    divider="orange",
)
render_boundary_markdown(
    "boundary_deriv_04.md",
    r"""For an infinite confined aquifer, $s=QW(u)/(4\pi T)$ with $u=r^2S/(4Tt)$. For one straight boundary, an image well is placed symmetrically across the boundary. The image has $+Q$ for a no-flow boundary and $-Q$ for a specified-head boundary. Because the Theis equation is linear, both drawdown and the analytical derivative $ds/d\ln(t)$ can be superposed directly. For one no-flow boundary the late derivative approaches $2d$; for one specified-head boundary it approaches zero, where $d=Q/(4\pi T)$.""",
)

# --------------------------------------------------
# Interactive section
# --------------------------------------------------
st.subheader(
    "Explore :orange[boundary effects] in diagnostic plots",
    divider="orange",
)
render_boundary_markdown(
    "boundary_deriv_05.md",
    """Start with one boundary and then compare several pumping-well-to-boundary distances. Moving the boundary changes mainly **when** the derivative departs from the infinite-aquifer Theis response.""",
)

with st.expander(":orange[**General hydraulic setup**]", expanded=True):
    setup_col1, setup_col2, setup_col3 = st.columns(3)

    with setup_col1:
        Q_lps = st.number_input(
            "Pumping rate Q in L/s",
            min_value=0.01,
            max_value=100.0,
            value=2.0,
            step=0.10,
            format="%.2f",
            key="bc_Q_lps_global",
        )
        Q = Q_lps / 1000.0

    with setup_col2:
        r_obs = st.number_input(
            "Observation distance r from pumping well in m",
            min_value=0.1,
            max_value=2000.0,
            value=30.0,
            step=1.0,
            format="%.1f",
            key="bc_r_obs_global",
        )

    with setup_col3:
        observation_position = st.selectbox(
            "Observation position",
            [
                "Between pumping well and boundary",
                "Away from boundary",
            ],
            index=0,
            key="bc_observation_position_global",
        )

    st.caption(
        "The image-well distance depends on geometry. For an observation well between "
        r"the pumping well and boundary, $r_i=2a-r$ and therefore $a>r$. "
        r"For an observation well on the opposite side, $r_i=2a+r$."
    )


active_tab = st.segmented_control(
    "Select topic",
    options=[
        "01: Single boundary",
        "02: Distance to no-flow boundary",
        "03: Distance to specified-head boundary",
    ],
    default="01: Single boundary",
    label_visibility="collapsed",
)

if active_tab is None:
    st.info("Please select one topic to continue.")
    st.stop()


@st.fragment
def boundary_interactive(v, Q_lps, Q, r_obs, observation_position):
    """Interactive boundary-condition diagnostic plots."""

    # --------------------------------------------------
    # Plot / parameter defaults
    # --------------------------------------------------
    t_plot = np.logspace(0, 8, 360)
    number_input = st.toggle(
        "Use number input instead of sliders",
        key=f"bc_number_input_{v}",
    )

    col_1, col_2, col_3 = st.columns((1, 1, 1), gap="medium")

    # --------------------------------------------------
    # Plot settings
    # --------------------------------------------------
    with col_1:
        with st.expander(":red[**Plot settings**]"):
            show_drawdown = st.toggle(
                "Show boundary drawdown",
                value=True,
                key=f"bc_show_drawdown_{v}",
            )
            show_derivative = st.toggle(
                "Show drawdown derivative",
                value=True,
                key=f"bc_show_derivative_{v}",
            )
            show_theis = st.toggle(
                "Show infinite-aquifer Theis reference",
                value=True,
                key=f"bc_show_theis_{v}",
            )
            semilog = st.toggle(
                "Toggle for **semi-log graph**",
                key=f"bc_semilog_{v}",
            )
            show_geometry = st.toggle(
                "Show image-well geometry",
                value=False,
                key=f"bc_show_geometry_{v}",
            )

    # --------------------------------------------------
    # Aquifer parameters
    # --------------------------------------------------
    with col_2:
        with st.expander(":blue[**Transmissivity**]"):
            log_T = log_widget(
                "_(log of) Transmissivity in m²/s_",
                -6.0,
                -1.0,
                -2.0,
                f"bc_T_{v}",
                "bc_T",
                number_input,
            )
            T = 10**log_T
            st.write("**T:** %5.2e m²/s" % T)


    with col_3:
        with st.expander(":green[**Storativity**]"):
            log_S = log_widget(
                "_(log of) Storativity S_",
                -7.0,
                -1.0,
                -3.0,
                f"bc_S_{v}",
                "bc_S",
                number_input,
            )
            S = 10**log_S
            st.write("**S:** %5.2e" % S)

    # --------------------------------------------------
    # Version-specific boundary controls
    # --------------------------------------------------
    parameter_sets = []

    if v == 1:
        with col_3:
            with st.expander(":orange[**Boundary condition**]"):
                boundary_type = st.selectbox(
                    "Boundary type",
                    ["No-flow boundary", "Specified-head boundary"],
                    index=0,
                    key=f"bc_type_{v}",
                )

                boundary_distance = boundary_distance_widget(
                    "Distance a from pumping well to boundary [m]",
                    530.0,
                    f"bc_distance_{v}",
                    number_input,
                )

                parameter_sets.append(
                    {
                        "label": boundary_type,
                        "boundary_type": boundary_type,
                        "boundary_distance": boundary_distance,
                    }
                )

    elif v == 2:
        boundary_type = "No-flow boundary"
        with col_3:
            with st.expander(":orange[**Boundary distances**]"):
                defaults = [100.0, 500.0, 1000.0]
                for i, default in enumerate(defaults, start=1):
                    distance = boundary_distance_widget(
                        f"Distance a{i} [m]",
                        default,
                        f"bc_noflow_distance_{v}_{i}",
                        number_input,
                    )
                    parameter_sets.append(
                        {
                            "label": f"a = {distance:.0f} m",
                            "boundary_type": boundary_type,
                            "boundary_distance": distance,
                        }
                    )

    elif v == 3:
        boundary_type = "Specified-head boundary"
        with col_3:
            with st.expander(":orange[**Boundary distances**]"):
                defaults = [100.0, 500.0, 1000.0]
                for i, default in enumerate(defaults, start=1):
                    distance = boundary_distance_widget(
                        f"Distance a{i} [m]",
                        default,
                        f"bc_head_distance_{v}_{i}",
                        number_input,
                    )
                    parameter_sets.append(
                        {
                            "label": f"a = {distance:.0f} m",
                            "boundary_type": boundary_type,
                            "boundary_distance": distance,
                        }
                    )
    else:
        st.error("Unknown boundary-condition version.")
        return

    # --------------------------------------------------
    # Geometry validation
    # --------------------------------------------------
    # Keep a (pumping-well-to-boundary distance) and r (pumping-well-to-
    # observation distance) as independent user inputs. Changing r must never
    # silently modify a. If the chosen geometry is impossible, retain all input
    # values and ask the user to correct either r, a, or the observation side.
    if observation_position == "Between pumping well and boundary":
        invalid_distances = [
            par["boundary_distance"]
            for par in parameter_sets
            if r_obs >= par["boundary_distance"]
        ]

        if invalid_distances:
            invalid_text = ", ".join(f"{value:.0f} m" for value in invalid_distances)
            st.error(
                "For an observation point between the pumping well and the boundary, "
                "the observation distance r must be smaller than every selected "
                "pumping-well-to-boundary distance a. The boundary distance values "
                "have been kept unchanged. Increase a, reduce r, or select "
                "'Away from boundary'. Invalid a value(s): " + invalid_text
            )
            return

    if not show_drawdown and not show_derivative:
        st.info("Select drawdown and/or the drawdown derivative.")
        return

    # --------------------------------------------------
    # Optional conceptual geometry
    # --------------------------------------------------
    if show_geometry:
        geometry_boundary_type = parameter_sets[0]["boundary_type"]
        geometry_distance = parameter_sets[0]["boundary_distance"]
        st.pyplot(
            plot_image_well_geometry(
                geometry_distance,
                r_obs,
                geometry_boundary_type,
                observation_position,
            )
        )
        if v in (2, 3):
            st.caption(
                "The sketch uses the first distance variant. The diagnostic plot below "
                "contains all three selected boundary distances."
            )

    # --------------------------------------------------
    # Plot
    # --------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    boundary_handles = []
    boundary_labels = []
    derivative_handles = []
    derivative_labels = []
    theis_handles = []
    theis_labels = []

    plotted_positive_values = []

    for i, par in enumerate(parameter_sets):
        color = colors[i % len(colors)]
        response = compute_boundary_response(
            T=T,
            S=S,
            t=t_plot,
            Q=Q,
            observation_distance=r_obs,
            boundary_distance=par["boundary_distance"],
            boundary_type=par["boundary_type"],
            observation_position=observation_position,
        )

        label = par["label"]

        if show_drawdown:
            y = response["drawdown"]
            valid = np.isfinite(y) & (y > 0)
            line, = ax.plot(
                t_plot[valid],
                y[valid],
                linewidth=2,
                color=color,
                label="_nolegend_",
            )
            boundary_handles.append(line)
            boundary_labels.append(f"Drawdown: {label}")
            plotted_positive_values.extend(y[valid].tolist())

        if show_derivative:
            y = response["derivative"]
            valid = np.isfinite(y) & (y > 0)
            derivative_line, = ax.plot(
                t_plot[valid],
                y[valid],
                "--",
                linewidth=2,
                color=color,
                label="_nolegend_",
            )
            derivative_handles.append(derivative_line)
            derivative_labels.append(rf"Derivative $ds/d\ln(t)$: {label}")
            plotted_positive_values.extend(y[valid].tolist())

    # One infinite-aquifer Theis reference is sufficient because T, S, Q and r are fixed within a tab.
    ref = compute_boundary_response(
        T=T,
        S=S,
        t=t_plot,
        Q=Q,
        observation_distance=r_obs,
        boundary_distance=parameter_sets[0]["boundary_distance"],
        boundary_type=parameter_sets[0]["boundary_type"],
        observation_position=observation_position,
    )

    if show_theis:
        if show_drawdown:
            valid = np.isfinite(ref["theis_drawdown"]) & (ref["theis_drawdown"] > 0)
            theis_line, = ax.plot(
                t_plot[valid],
                ref["theis_drawdown"][valid],
                linestyle=":",
                linewidth=1.8,
                color="0.35",
                label="_nolegend_",
            )
            theis_handles.append(theis_line)
            theis_labels.append("Infinite-aquifer Theis drawdown")
            plotted_positive_values.extend(ref["theis_drawdown"][valid].tolist())

        if show_derivative:
            valid_d = np.isfinite(ref["theis_derivative"]) & (ref["theis_derivative"] > 0)
            theis_d_line, = ax.plot(
                t_plot[valid_d],
                ref["theis_derivative"][valid_d],
                linestyle="-.",
                linewidth=1.5,
                color="0.35",
                label="_nolegend_",
            )
            theis_handles.append(theis_d_line)
            theis_labels.append(r"Infinite-aquifer Theis derivative")
            plotted_positive_values.extend(ref["theis_derivative"][valid_d].tolist())

    # Reference plateaus
    if show_derivative:
        d_plateau = Q / (4.0 * np.pi * T)
        ax.axhline(
            d_plateau,
            linestyle=":",
            linewidth=1.2,
            color="0.55",
            alpha=0.9,
        )

        if all(par["boundary_type"] == "No-flow boundary" for par in parameter_sets):
            ax.axhline(
                2.0 * d_plateau,
                linestyle=":",
                linewidth=1.2,
                color="0.25",
                alpha=0.9,
            )

    # --------------------------------------------------
    # Axes
    # --------------------------------------------------
    ax.set_xscale("log")
    if not semilog:
        ax.set_yscale("log")

    ax.set_xlim(1e0, 1e8)

    if semilog:
        y_max = max(plotted_positive_values) if plotted_positive_values else 1.0
        ax.set_ylim(0.0, max(1.05 * y_max, 0.1))
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

    if v == 1:
        ax.set_title("Effect of one hydraulic boundary", fontsize=16)
    elif v == 2:
        ax.set_title("Effect of distance to a no-flow boundary", fontsize=16)
    else:
        ax.set_title("Effect of distance to a specified-head boundary", fontsize=16)

    # --------------------------------------------------
    # Legend
    # --------------------------------------------------
    legend_handles = []
    legend_labels = []

    if show_drawdown:
        legend_handles.extend(boundary_handles)
        legend_labels.extend(boundary_labels)

    if show_derivative:
        legend_handles.extend(derivative_handles)
        legend_labels.extend(derivative_labels)

    if show_theis:
        legend_handles.extend(theis_handles)
        legend_labels.extend(theis_labels)

    ax.legend(legend_handles, legend_labels, fontsize=9, loc="best")

    # --------------------------------------------------
    # Parameter box
    # --------------------------------------------------
    d_plateau = Q / (4.0 * np.pi * T)

    if v == 1:
        par = parameter_sets[0]
        r_img = image_well_distance(par["boundary_distance"], r_obs, observation_position)
        boundary_short = "no-flow" if par["boundary_type"] == "No-flow boundary" else "specified head"
        out_txt = "\n".join(
            (
                r"$T$ (m²/s) = %10.2E" % T,
                r"$S$ (-) = %10.2E" % S,
                r"$Q$ (L/s) = %5.2f" % Q_lps,
                r"$r$ observation (m) = %6.1f" % r_obs,
                f"Observation: {'toward boundary' if observation_position == 'Between pumping well and boundary' else 'away from boundary'}",
                r"$a$ boundary (m) = %6.1f" % par["boundary_distance"],
                r"$r_i$ image (m) = %6.1f" % r_img,
                f"Boundary: {boundary_short}",
                r"$d=Q/(4\pi T)$ = %10.2E m" % d_plateau,
            )
        )
    else:
        boundary_short = "no-flow" if v == 2 else "specified head"
        out_txt = "\n".join(
            (
                r"$T$ (m²/s) = %10.2E" % T,
                r"$S$ (-) = %10.2E" % S,
                r"$Q$ (L/s) = %5.2f" % Q_lps,
                r"$r$ observation (m) = %6.1f" % r_obs,
                f"Observation: {'toward boundary' if observation_position == 'Between pumping well and boundary' else 'away from boundary'}",
                f"Boundary: {boundary_short}",
                r"$d=Q/(4\pi T)$ = %10.2E m" % d_plateau,
            )
        )

    ax.text(
        0.03,
        0.97,
        out_txt,
        horizontalalignment="left",
        transform=ax.transAxes,
        fontsize=10.5,
        verticalalignment="top",
        bbox=props,
    )

    fig.tight_layout()
    st.pyplot(fig)

    # --------------------------------------------------
    # Interpretation below plot
    # --------------------------------------------------
    if v == 1:
        boundary_type = parameter_sets[0]["boundary_type"]
        if boundary_type == "No-flow boundary":
            st.caption(
                r"For a single no-flow boundary, the same-sign image well causes the late-time "
                r"derivative to approach $2d$, where $d=Q/(4\pi T)$."
            )
        else:
            st.caption(
                r"For a single specified-head boundary, the opposite-sign image well limits "
                r"drawdown and the derivative approaches zero at late time."
            )


if active_tab.startswith("01"):
    render_boundary_markdown(
        "boundary_deriv_06.md",
        "Change the boundary type and distance. Compare the result with the infinite-aquifer Theis response.",
    )
    boundary_interactive(1, Q_lps, Q, r_obs, observation_position)

elif active_tab.startswith("02"):
    render_boundary_markdown(
        "boundary_deriv_07.md",
        r"Compare three no-flow-boundary distances. The derivative approaches $2d$ at late time; a closer boundary causes the transition to occur earlier.",
    )
    boundary_interactive(2, Q_lps, Q, r_obs, observation_position)

elif active_tab.startswith("03"):
    render_boundary_markdown(
        "boundary_deriv_08.md",
        "Compare three specified-head-boundary distances. A closer boundary causes the derivative to bend downward earlier and drawdown to stabilize sooner.",
    )
    boundary_interactive(3, Q_lps, Q, r_obs, observation_position)

# --------------------------------------------------
# References
# --------------------------------------------------
with st.expander("**Click here for references**"):
    render_boundary_markdown(
        "boundary_deriv_ref.md",
        """- Theis, C. V. (1935): The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage.\n- Kruseman, G. P. & de Ridder, N. A. (2000): *Analysis and Evaluation of Pumping Test Data*.\n- Hekel et al. (2025): *Pumpversuchsauswertung mittels Diagnostischer Plots – Ein Leitfaden für Praxis und Lehre*, Section 2.7.""",
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")

columns_lic = st.columns((4, 1, 1))
with columns_lic[0]:
    st.markdown(
        f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}',
        unsafe_allow_html=True,
    )
with columns_lic[1]:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png"
    )
with columns_lic[2]:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/CC_BY-SA_icon.png"
    )

st.markdown(
    """
    <div style="font-size:0.85em;">
    <i>
    <a href="https://gw-project.org/" target="_blank">
    The Groundwater Project
    </a>
    is a nonprofit organization with one full-time staff and over 1000 volunteers.
    Please help us by referring to
    <a href="https://gw-project.org/interactive-education/" target="_blank">
    The Groundwater Project Educational Tools
    </a>
    when sharing this app with others.
    </i>
    </div>
    """,
    unsafe_allow_html=True,
)
