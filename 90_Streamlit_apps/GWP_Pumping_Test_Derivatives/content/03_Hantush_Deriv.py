# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
from scipy.integrate import quad
from functools import lru_cache
import math
import streamlit as st
from pathlib import Path
import pandas as pd
from GWP_Pumping_Test_Derivatives_utils import load_css
from GWP_Pumping_Test_Derivatives_utils import load_md

# Authors, institutions, and year
year = 2026
authors = {
    "Thomas Reimann": [1, 2],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "The Groundwater Project",
    2: "TU Dresden, Institute for Groundwater Management"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]

# ------------------------------------------------------------
# Format authors
# ------------------------------------------------------------
author_list = []

for name, indices in authors.items():
    superscript = ",".join(str(i) for i in indices)
    author_list.append(f"{name}<sup>{superscript}</sup>")

# ------------------------------------------------------------
# Format institutions
# ------------------------------------------------------------
institution_list = []

for i, inst in institutions.items():
    institution_list.append(f"<sup>{i}</sup> {inst}")
institution_text = ", ".join(institution_list)

# --------------------------------------------------
# Functions
# --------------------------------------------------
def well_function(u):
    """Theis well function W(u)."""
    return scipy.special.exp1(u)

def theis_u(T, S, r, t):
    """Dimensionless time parameter u."""
    return r**2 * S / (4.0 * T * t)

@lru_cache(maxsize=50000)
def hantush_well_scalar(u, r_div_B):
    """
    Hantush-Jacob well function W(u, r/B) for a scalar u.

    The integral is evaluated directly to obtain a smooth curve that is suitable
    for derivative analysis.
    """
    u = float(u)
    r_div_B = float(r_div_B)

    if u <= 0 or not np.isfinite(u):
        return np.nan

    # Theis limit
    if abs(r_div_B) < 1e-14:
        return scipy.special.exp1(u)

    def integrand(x):
        return np.exp(-x - r_div_B**2 / (4.0 * x)) / x

    value, _ = quad(
        integrand,
        u,
        np.inf,
        epsabs=1e-10,
        epsrel=1e-8,
        limit=200,
    )

    return value

def hantush_well(u, r_div_B):
    """Vectorized Hantush-Jacob well function."""
    u = np.asarray(u, dtype=float)
    return np.array([hantush_well_scalar(ui, r_div_B) for ui in u])

def hantush_s(Q, T, u, r_div_B):
    """Hantush-Jacob drawdown for known u and r/B."""
    return Q / (4.0 * np.pi * T) * hantush_well(u, r_div_B)

def compute_s(T, S, t, Q, r, r_div_B):
    """Compute Hantush-Jacob drawdown."""
    u = theis_u(T, S, r, t)
    return hantush_s(Q, T, u, r_div_B)

def compute_hantush_derivative_analytical(T, S, t, Q, r, r_div_B):
    """
    Analytical Hantush-Jacob derivative with respect to ln(t):

        ds/dln(t) = Q / (4*pi*T) * exp(-u - (r/B)^2/(4u))
    """
    u = theis_u(T, S, r, t)
    return Q / (4.0 * np.pi * T) * np.exp(-u - r_div_B**2 / (4.0 * u))

def compute_theis_s(T, S, t, Q, r):
    """Compute Theis drawdown for comparison."""
    u = theis_u(T, S, r, t)
    return Q / (4.0 * np.pi * T) * well_function(u)

def compute_theis_derivative_analytical(T, S, t, Q, r):
    """Analytical Theis derivative with respect to ln(t), for comparison."""
    u = theis_u(T, S, r, t)
    return Q / (4.0 * np.pi * T) * np.exp(-u)

def compute_drawdown_derivative(
    time,
    drawdown,
    method="renard2009",
    L=0.2,
    n_neighbors=1,
    positive_only=True,
):
    """
    Compute drawdown derivative with respect to ln(t).

    Methods
    -------
    renard2009:
        ds/dln(t) ≈ ((s_i - s_i-1) / (t_i - t_i-1)) * ((t_i + t_i-1) / 2)

    log_difference:
        ds/dln(t) ≈ (s_i - s_i-1) / (ln(t_i) - ln(t_i-1))

    neighboring_points:
        Weighted Bourdet-type derivative using n neighboring points
        before and after point i.

    bourdet1989:
        Fixed end-point method after Bourdet et al. (1989).
        L is interpreted as log10-cycle spacing.

    spane_wurstner1993:
        Least-squares method after Spane and Wurstner (1993).
        L is interpreted as log10-cycle spacing.
    """

    time = np.asarray(time, dtype=float)
    drawdown = np.asarray(drawdown, dtype=float)

    ln_time = np.log(time)
    log10_time = np.log10(time)

    # --------------------------------------------------
    # Renard et al. (2009)
    # --------------------------------------------------
    if method == "renard2009":

        ds = np.diff(drawdown)
        dt = np.diff(time)

        derivative_time = 0.5 * (time[1:] + time[:-1])
        derivative = (ds / dt) * derivative_time

    # --------------------------------------------------
    # Direct logarithmic difference
    # --------------------------------------------------
    elif method == "log_difference":

        ds = np.diff(drawdown)
        dln_t = np.diff(ln_time)

        derivative_time = np.sqrt(time[:-1] * time[1:])
        derivative = ds / dln_t

    # --------------------------------------------------
    # Point-based neighboring method
    # --------------------------------------------------
    elif method == "neighboring_points":

        n_neighbors = int(n_neighbors)

        derivative_time = []
        derivative = []

        for i in range(n_neighbors, len(time) - n_neighbors):

            left_idx = i - n_neighbors
            right_idx = i + n_neighbors

            dln_t1 = ln_time[i] - ln_time[left_idx]
            dln_t2 = ln_time[right_idx] - ln_time[i]

            if dln_t1 <= 0 or dln_t2 <= 0:
                continue

            ds1 = drawdown[i] - drawdown[left_idx]
            ds2 = drawdown[right_idx] - drawdown[i]

            slope1 = ds1 / dln_t1
            slope2 = ds2 / dln_t2

            deriv_i = (
                slope1 * dln_t2
                + slope2 * dln_t1
            ) / (
                dln_t1 + dln_t2
            )

            derivative_time.append(time[i])
            derivative.append(deriv_i)

        derivative_time = np.asarray(derivative_time)
        derivative = np.asarray(derivative)

    # --------------------------------------------------
    # Bourdet et al. (1989)
    # Fixed end-point method
    # L is in log10 cycles
    # --------------------------------------------------
    elif method == "bourdet1989":

        derivative_time = []
        derivative = []

        n = len(time)

        last_valid_right_slope = None

        # derivative is not calculated for the first data point
        for i in range(1, n):

            # -----------------------------
            # Left side
            # -----------------------------
            left_target = log10_time[i] - L

            left_candidates = np.where(log10_time[:i] <= left_target)[0]

            if len(left_candidates) > 0:
                left_idx = left_candidates[-1]
            else:
                # early-time end correction:
                # use the first available point, even if ΔX1 < L
                left_idx = 0

            if left_idx == i:
                continue

            dX1 = log10_time[i] - log10_time[left_idx]

            if dX1 <= 0:
                continue

            dP1 = drawdown[i] - drawdown[left_idx]
            slope1 = dP1 / dX1

            # -----------------------------
            # Right side
            # -----------------------------
            if i < n - 1:

                right_target = log10_time[i] + L

                right_candidates = np.where(log10_time[i + 1:] >= right_target)[0]

                if len(right_candidates) > 0:
                    right_idx = i + 1 + right_candidates[0]
                else:
                    # use last point if full L-spacing is not available
                    right_idx = n - 1

                dX2 = log10_time[right_idx] - log10_time[i]

                if dX2 <= 0:
                    continue

                dP2 = drawdown[right_idx] - drawdown[i]
                slope2_current = dP2 / dX2

                # save the last right-side slope that used approximately full L-spacing
                if dX2 >= L:
                    last_valid_right_slope = slope2_current
                    slope2 = slope2_current
                else:
                    # late-time end correction:
                    # use last valid right-side slope if available
                    if last_valid_right_slope is not None:
                        slope2 = last_valid_right_slope
                    else:
                        slope2 = slope2_current

            else:
                # last point: no right-side slope can be computed
                # use last valid right-side slope if available
                if last_valid_right_slope is None:
                    continue

                dX2 = dX1
                slope2 = last_valid_right_slope

            deriv_i_log10 = (
                slope1 * dX2
                + slope2 * dX1
            ) / (
                dX1 + dX2
            )

            # Convert from ds/dlog10(t) to ds/dln(t)
            deriv_i = deriv_i_log10 / np.log(10)

            derivative_time.append(time[i])
            derivative.append(deriv_i)

        derivative_time = np.asarray(derivative_time)
        derivative = np.asarray(derivative)

    # --------------------------------------------------
    # Spane and Wurstner (1993)
    # Least-squares regression method
    # L is in log10 cycles
    # --------------------------------------------------
    elif method == "spane_wurstner1993":

        derivative_time = []
        derivative = []

        n = len(time)

        last_valid_right_slope = None

        # derivative is not calculated for the first data point
        for i in range(1, n):

            # -----------------------------
            # Left regression interval
            # -----------------------------
            left_min = log10_time[i] - L

            left_mask = (
                (log10_time >= left_min)
                & (log10_time <= log10_time[i])
            )

            # early-time correction:
            # include all available points to the left if full L is not available
            left_mask[:i + 1] = left_mask[:i + 1]
            left_indices = np.where(left_mask & (np.arange(n) <= i))[0]

            if len(left_indices) < 2:
                left_indices = np.arange(0, i + 1)

            if len(left_indices) < 2:
                continue

            slope1, _ = np.polyfit(
                log10_time[left_indices],
                drawdown[left_indices],
                1,
            )

            dX1 = log10_time[i] - log10_time[left_indices[0]]

            if dX1 <= 0:
                continue

            # -----------------------------
            # Right regression interval
            # -----------------------------
            if i < n - 1:

                right_max = log10_time[i] + L

                right_mask = (
                    (log10_time >= log10_time[i])
                    & (log10_time <= right_max)
                )

                right_indices = np.where(right_mask & (np.arange(n) >= i))[0]

                if len(right_indices) < 2:
                    right_indices = np.arange(i, n)

                if len(right_indices) < 2:
                    continue

                slope2_current, _ = np.polyfit(
                    log10_time[right_indices],
                    drawdown[right_indices],
                    1,
                )

                dX2 = log10_time[right_indices[-1]] - log10_time[i]

                if dX2 <= 0:
                    continue

                # save the last right-side regression slope with approximately full L-spacing
                if dX2 >= L:
                    last_valid_right_slope = slope2_current
                    slope2 = slope2_current
                else:
                    if last_valid_right_slope is not None:
                        slope2 = last_valid_right_slope
                    else:
                        slope2 = slope2_current

            else:
                if last_valid_right_slope is None:
                    continue

                dX2 = dX1
                slope2 = last_valid_right_slope

            deriv_i_log10 = (
                slope1 * dX2
                + slope2 * dX1
            ) / (
                dX1 + dX2
            )

            # Convert from ds/dlog10(t) to ds/dln(t)
            deriv_i = deriv_i_log10 / np.log(10)

            derivative_time.append(time[i])
            derivative.append(deriv_i)

        derivative_time = np.asarray(derivative_time)
        derivative = np.asarray(derivative)

    else:
        raise ValueError(f"Unknown derivative method: {method}")

    # --------------------------------------------------
    # Optional filtering
    # --------------------------------------------------
    if positive_only:
        valid = derivative > 0
        derivative_time = derivative_time[valid]
        derivative = derivative[valid]

    return derivative_time, derivative

def compute_statistics(measured, computed):
    measured = np.asarray(measured)
    computed = np.asarray(computed)

    error = computed - measured

    me = np.mean(error)
    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error**2))

    return me, mae, rmse

def update_T(v, source_key):
    st.session_state[f"T_slider_value_{v}"] = st.session_state[source_key]

def update_S(v, source_key):
    st.session_state[f"S_slider_value_{v}"] = st.session_state[source_key]

def update_RB(v, source_key):
    st.session_state[f"RB_slider_value_{v}"] = st.session_state[source_key]

def reset_inverse_state(v):
    """
    Start a new synthetic dataset generation and reset selected app states.
    """

    generation_key = f"synthetic_generation_{v}"

    if generation_key not in st.session_state:
        st.session_state[generation_key] = 0

    # Increase generation number.
    # This creates new widget keys and forces Streamlit to apply defaults.
    st.session_state[generation_key] += 1

    # Reset fitting values
    st.session_state[f"T_slider_value_{v}"] = -3.0
    st.session_state[f"S_slider_value_{v}"] = -4.0
    st.session_state[f"RB_slider_value_{v}"] = 0.40  # log10(r/B), equivalent to r/B ≈ 0.40

    # Remove widget-specific T/S/rB input states
    widget_keys_to_delete = [
        f"T_input_slider_{v}",
        f"T_input_number_{v}",
        f"S_input_slider_{v}",
        f"S_input_number_{v}",
        f"RB_input_slider_{v}",
        f"RB_input_number_{v}",
    ]

    for key in widget_keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

MD_DIR  = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/md")
CSS_DIR = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/css")

load_css(CSS_DIR, "segment_control_Theis_Deriv_Ini.css")

# st.title("Pumping test evaluation with :green[Drawdown Derivatives]")
st.header("Understanding :green[**Drawdown Derivatives**] with the :green[**Hantush-Jacob**] model for :green[**semi-confined aquifers**]", divider = 'green')

# --------------------------------------------------
# Orientation/Explanation
# --------------------------------------------------
st.markdown(load_md(MD_DIR, "hantush_deriv_01.md", st.session_state.language))


st.subheader("Introduction", divider="green")
st.markdown(load_md(MD_DIR, "hantush_deriv_02.md", st.session_state.language))

left_co, cent_co, last_co = st.columns((20, 60, 20))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png",
        caption="The Groundwater Project educational tools",
    )

# --------------------------------------------------
# Initial assessment
# --------------------------------------------------
st.markdown(load_md(MD_DIR, "hantush_deriv_03.md", st.session_state.language))

with st.expander(":green[**Show/Hide the initial assessment**]"):
    st.write('Show the initial assessment')
#    columnsQ = st.columns((1, 1))
#
#    with columnsQ[0]:
#        stb.single_choice(
#            ":green[**What aquifer condition is represented by the Hantush-Jacob solution used here?**]",
#            [
#                "Confined aquifer without leakage",
#                "Leaky aquifer with negligible aquitard storage",
#                "Unconfined aquifer with delayed yield",
#                "Steady-state flow to a well",
#            ],
#            1,
#            success="Correct. This version of the Hantush-Jacob solution represents a leaky aquifer with negligible aquitard storage.",
#            error="Not quite. The key addition compared with Theis is leakage through an aquitard.",
#        )
#
#        stb.single_choice(
#            ":green[**What does a larger value of r/B indicate?**]",
#            [
#                "A stronger leakage influence at the observation point",
#                "A lower pumping rate",
#                "A larger aquifer storage capacity only",
#                "No leakage",
#            ],
#            0,
#            success="Correct. Larger r/B indicates stronger leakage influence at the observation point.",
#            error="Not quite. The parameter r/B controls the leakage influence in the Hantush-Jacob well function.",
#        )
#
#    with columnsQ[1]:
#        stb.single_choice(
#            ":green[**How does the late-time Hantush-Jacob derivative differ from the Theis derivative?**]",
#            [
#                "It approaches the same constant plateau for all r/B values",
#                "It decreases when leakage becomes important",
#                "It is always zero",
#                "It increases without limit",
#            ],
#            1,
#            success="Correct. Leakage causes the derivative to decline at late time.",
#            error="Not quite. The derivative is useful because it reveals leakage-controlled late-time behavior.",
#        )
#
#        stb.single_choice(
#            ":green[**What happens when r/B approaches zero?**]",
#            [
#                "The solution approaches the Theis confined-aquifer solution",
#                "Drawdown becomes zero at all times",
#                "Leakage becomes infinite",
#                "The aquifer becomes unconfined",
#            ],
#            0,
#            success="Correct. For r/B near zero, the Hantush-Jacob response approaches the Theis response.",
#            error="Not quite. Small r/B means weak leakage influence.",
#        )

# --------------------------------------------------
# Theory
# --------------------------------------------------
st.subheader("Underlying Theory - :green[Hantush-Jacob] Solution and :green[Drawdown Derivatives]", divider="green")

st.markdown(load_md(MD_DIR, "hantush_deriv_04.md", st.session_state.language))

# --------------------------------------------------
# Type curve data
# --------------------------------------------------
u_min = -5
u_max = 4

u = np.logspace(u_min, u_max)
u_inv = 1 / u
w_u = well_function(u)

# --------------------------------------------------
# Interactive inverse function
# --------------------------------------------------
@st.fragment
def inverse(v):
    """
    Versions
    --------
    v = 1: T, S, r/B variable. Investigation of r/B
    v = 2: Fixed S, T, three user-defined r/B variants.
    v = 3: Fitting to 'measured' data
    """

    # --------------------------------------------------
    # Basic hydraulic setup
    # --------------------------------------------------
    r = 100.0              # distance from pumping well [m]
    b = 10.0               # aquifer thickness [m]
    b_aquitard = 10.0      # aquitard thickness [m]
    Qs = 0.1 / 60.0        # pumping rate [m³/s]
    Qd = Qs * 60 * 60 * 24 # pumping rate [m³/d], informative only

    # --------------------------------------------------
    # Initial values for fitting parameters
    # --------------------------------------------------
    if f"T_slider_value_{v}" not in st.session_state:
        st.session_state[f"T_slider_value_{v}"] = -3.0

    if f"S_slider_value_{v}" not in st.session_state:
        st.session_state[f"S_slider_value_{v}"] = -4.0

    if f"RB_slider_value_{v}" not in st.session_state:
        st.session_state[f"RB_slider_value_{v}"] = -0.40  # log10(r/B), equivalent to r/B ≈ 0.40

    log_min_T = -7.0
    log_max_T = 0.0
    log_min_S = -7.0
    log_max_S = 0.0
    log_min_RB = -2.0  # r/B = 0.01
    log_max_RB = 0.5   # r/B ≈ 3.16
    
    # --------------------------------------------------
    # Hidden true parameters for synthetic data generation
    # Random values are generated in log space.
    # --------------------------------------------------
    log_T_true_min = -5.0
    log_T_true_max = -3.0
    log_S_true_min = -5.0
    log_S_true_max = -3.0

    # r/B is generated in log space to avoid too many near-zero values.
    # This range corresponds approximately to r/B = 0.10 to 1.00.
    log_RB_true_min = -1.0
    log_RB_true_max = 0.0
    
    number_input = st.toggle("Use number input instead of sliders", key=f"number_input_{v}")

    # --------------------------------------------------
    # Generate synthetic measured data once and keep them stable
    # --------------------------------------------------
    generation_key = f"synthetic_generation_{v}"

    if generation_key not in st.session_state:
        st.session_state[generation_key] = 0

    generation = st.session_state[generation_key]

    data_key_Hantush = f"synthetic_data_Hantush{v}_{generation}"

    if data_key_Hantush not in st.session_state:
        rng = np.random.default_rng()
        
        # --------------------------------------------------
        # Synthetic-data settings
        # These will later become user-defined
        # --------------------------------------------------
        noise_level = rng.uniform(0.01, 0.04)     # relative noise level, e.g. 0.03 = 3 %
        n_measured = rng.integers(35, 71)        # number of synthetic measured data points
    
        t_meas_min = 1.0       # earliest measured time [s]
        t_meas_max = rng.integers(4, 10)*86400  # latest measured time [s]

        T_true = 10 ** rng.uniform(log_T_true_min, log_T_true_max)
        S_true = 10 ** rng.uniform(log_S_true_min, log_S_true_max)
        r_div_B_true = 10 ** rng.uniform(log_RB_true_min, log_RB_true_max)

        m_time_s = np.logspace(
            np.log10(t_meas_min),
            np.log10(t_meas_max),
            n_measured,
        )

        m_ddown_true = compute_s(
            T_true,
            S_true,
            m_time_s,
            Qs,
            r,
            r_div_B_true,
        )

        noise = rng.normal(
            loc=0.0,
            scale=noise_level,
            size=len(m_ddown_true),
        )

        m_ddown = m_ddown_true * (1.0 + noise)

        # avoid zero or negative values caused by noise
        m_ddown = np.maximum(m_ddown, 1e-8)

        st.session_state[data_key_Hantush] = {
            "m_time_s": m_time_s,
            "m_ddown": m_ddown,
            "m_ddown_true": m_ddown_true,
            "T_true": T_true,
            "S_true": S_true,
            "r_div_B_true": r_div_B_true,
            "noise_level": noise_level,
            "n_measured": n_measured,
            "t_meas_min": t_meas_min,
            "t_meas_max": t_meas_max,
        }

    m_time_s = st.session_state[data_key_Hantush]["m_time_s"]
    m_ddown = st.session_state[data_key_Hantush]["m_ddown"]
    m_ddown_true = st.session_state[data_key_Hantush]["m_ddown_true"]
    T_true = st.session_state[data_key_Hantush]["T_true"]
    S_true = st.session_state[data_key_Hantush]["S_true"]
    r_div_B_true = st.session_state[data_key_Hantush]["r_div_B_true"]
    noise_level  = st.session_state[data_key_Hantush]["noise_level"]
    n_measured   = st.session_state[data_key_Hantush]["n_measured"]
    t_meas_min   = st.session_state[data_key_Hantush]["t_meas_min"]
    t_meas_max   = st.session_state[data_key_Hantush]["t_meas_max"]



    # --------------------------------------------------
    # Input widgets in three columns
    # --------------------------------------------------
    col_1, col_2, col_3 = st.columns((1, 1, 1), gap="medium")

    # --------------------------------------------------
    # General plot controls
    # --------------------------------------------------
    with col_1:
        with st.expander(":red[**Plot settings**]"):
            show_hantush = st.toggle(
                "Show Hantush-Jacob drawdown curve",
                value=True,
                key=f"show_hantush_{v}_{generation}",
            )
    
            show_derivative = st.toggle(
                "Show drawdown derivative",
                value=False,
                key=f"show_derivative_{v}",
            )

            show_theis = st.toggle(
                "Show Theis drawdown curve (comparison)",
                value=True,
                key=f"show_theis_{v}",
            )
            
            semilog = st.toggle(
                "Toggle for **semi-log graph**",
                key=f"semilog_{v}",
            )
            
        if not show_hantush and not show_derivative:
            st.warning(
                "Both the Hantush-Jacob drawdown curve and the derivative plot are switched off. "
                "Only the synthetic measured drawdown data are shown."
            )

#        st.info(
#            "The measured data are synthetic. They were generated from hidden true aquifer "
#            "parameters and include random noise."
#        )
            
    # --------------------------------------------------
    # Version-specific parameter input
    # --------------------------------------------------
    parameter_sets = []
    
    # --------------------------------------------------
    # Helper function: T widget
    # --------------------------------------------------
    def get_T_input(v, col, label="Transmissivity", default=-3.0):
        with col:
            with st.expander(f":blue[**{label}**]"):
                if f"T_slider_value_{v}" not in st.session_state:
                    st.session_state[f"T_slider_value_{v}"] = default
    
                if number_input:
                    T_widget_key = f"T_input_number_{v}"
                    if T_widget_key not in st.session_state:
                        st.session_state[T_widget_key] = st.session_state[f"T_slider_value_{v}"]
    
                    st.number_input(
                        "_(log of) Transmissivity in m²/s_",
                        min_value=log_min_T,
                        max_value=log_max_T,
                        value=st.session_state[f"T_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=T_widget_key,
                        on_change=update_T,
                        args=(v, T_widget_key),
                    )
                else:
                    T_widget_key = f"T_input_slider_{v}"
                    if T_widget_key not in st.session_state:
                        st.session_state[T_widget_key] = st.session_state[f"T_slider_value_{v}"]
    
                    st.slider(
                        "_(log of) Transmissivity in m²/s_",
                        min_value=log_min_T,
                        max_value=log_max_T,
                        value=st.session_state[f"T_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=T_widget_key,
                        on_change=update_T,
                        args=(v, T_widget_key),
                    )
    
                T = 10 ** st.session_state[f"T_slider_value_{v}"]
                st.write("**T:** %5.2e m²/s" % T)
    
        return T
    
    
    # --------------------------------------------------
    # Helper function: S widget
    # --------------------------------------------------
    def get_S_input(v, col, label="Storativity", default=-4.0):
        with col:
            with st.expander(f":green[**{label}**]"):
                if f"S_slider_value_{v}" not in st.session_state:
                    st.session_state[f"S_slider_value_{v}"] = default
    
                if number_input:
                    S_widget_key = f"S_input_number_{v}"
                    if S_widget_key not in st.session_state:
                        st.session_state[S_widget_key] = st.session_state[f"S_slider_value_{v}"]
    
                    st.number_input(
                        "_(log of) Storativity_",
                        min_value=log_min_S,
                        max_value=log_max_S,
                        value=st.session_state[f"S_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=S_widget_key,
                        on_change=update_S,
                        args=(v, S_widget_key),
                    )
                else:
                    S_widget_key = f"S_input_slider_{v}"
                    if S_widget_key not in st.session_state:
                        st.session_state[S_widget_key] = st.session_state[f"S_slider_value_{v}"]
    
                    st.slider(
                        "_(log of) Storativity_",
                        min_value=log_min_S,
                        max_value=log_max_S,
                        value=st.session_state[f"S_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=S_widget_key,
                        on_change=update_S,
                        args=(v, S_widget_key),
                    )
    
                S = 10 ** st.session_state[f"S_slider_value_{v}"]
                st.write("**S:** %5.2e" % S)
    
        return S
    
    
    # --------------------------------------------------
    # Helper function: r/B widget
    # --------------------------------------------------
    def get_RB_input(
        v,
        col,
        label="Leakage parameter r/B",
        default=0.40,
        min_RB=0.01,
        max_RB=3.00,
    ):
        with col:
            with st.expander(f":green[**{label}**]"):
                if f"RB_slider_value_{v}" not in st.session_state:
                    st.session_state[f"RB_slider_value_{v}"] = default
    
                if number_input:
                    RB_widget_key = f"RB_input_number_{v}"
    
                    if RB_widget_key not in st.session_state:
                        st.session_state[RB_widget_key] = st.session_state[
                            f"RB_slider_value_{v}"
                        ]
    
                    st.number_input(
                        "_Leakage parameter r/B_",
                        min_value=min_RB,
                        max_value=max_RB,
                        value=st.session_state[f"RB_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=RB_widget_key,
                        on_change=update_RB,
                        args=(v, RB_widget_key),
                    )
    
                else:
                    RB_widget_key = f"RB_input_slider_{v}"
    
                    if RB_widget_key not in st.session_state:
                        st.session_state[RB_widget_key] = st.session_state[
                            f"RB_slider_value_{v}"
                        ]
    
                    st.slider(
                        "_Leakage parameter r/B_",
                        min_value=min_RB,
                        max_value=max_RB,
                        value=st.session_state[f"RB_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=RB_widget_key,
                        on_change=update_RB,
                        args=(v, RB_widget_key),
                    )
    
                r_div_B = st.session_state[f"RB_slider_value_{v}"]
                st.write("**r/B:** %5.2f" % r_div_B)
    
        return r_div_B
    
    
    # --------------------------------------------------
    # Version 1: General Hantush solution
    # T, S, and r/B are variable
    # --------------------------------------------------
    if v == 1:
    
        T = get_T_input(v, col_2, label="Transmissivity")
        S = get_S_input(v, col_3, label="Storativity")
        r_div_B = get_RB_input(v, col_2, label="Leakage parameter r/B")
    
        parameter_sets.append(
            {
                "label": rf"$T$ = {T:.1e}, $S$ = {S:.1e}, $r/B$ = {r_div_B:.2f}",
                "T": T,
                "S": S,
                "r_div_B": r_div_B,
                "r": r,
                "b": b,
                "Qs": Qs,
                "Qd": Qd,
            }
        )
    
    
    # --------------------------------------------------
    # Version 2: Variation of r/B
    # Fixed T and S, three r/B variants
    # --------------------------------------------------
    elif v == 2:
    
        with col_2:
            with st.expander("Fixed :blue[**Transmissivity**]"):
    
                if number_input:
                    log_T_fixed = st.number_input(
                        "_Fixed (log of) Transmissivity in m²/s_",
                        min_value=log_min_T,
                        max_value=log_max_T,
                        value=-3.0,
                        step=0.01,
                        format="%4.2f",
                        key=f"T_fixed_{v}",
                    )

                else:
                    log_T_fixed = st.slider(
                        "_Fixed (log of) Transmissivity in m²/s_",
                        min_value=log_min_T,
                        max_value=log_max_T,
                        value=-3.0,
                        step=0.01,
                        format="%4.2f",
                        key=f"T_fixed_{v}",
                    )
    
                T_fixed = 10 ** log_T_fixed
    
                st.write("**Fixed T:** %5.2e m²/s" % T_fixed)
    
        with col_3:
            with st.expander("Fixed :green[**Storativity**]"):
    
                if number_input:
    
                    log_S_fixed = st.number_input(
                        "_Fixed (log of) Storativity_",
                        min_value=log_min_S,
                        max_value=log_max_S,
                        value=-4.0,
                        step=0.01,
                        format="%4.2f",
                        key=f"S_fixed_{v}",
                    )
                else:
    
                    log_S_fixed = st.slider(
                        "_Fixed (log of) Storativity_",
                        min_value=log_min_S,
                        max_value=log_max_S,
                        value=-4.0,
                        step=0.01,
                        format="%4.2f",
                        key=f"S_fixed_{v}",
                    )

                S_fixed = 10 ** log_S_fixed
    
        with col_2:
            with st.expander(":green[**Leakage parameter r/B**]"):
    
                default_RB_values = [0.10, 0.40, 1.00]
    
                for i, default_log_RB in enumerate(default_RB_values, start=1):
    
                    if number_input:
                        RB_i = st.number_input(
                            f"_(log of) r/B variant {i}_",
                            min_value=log_min_RB,
                            max_value=log_max_RB,
                            value=default_log_RB,
                            step=0.01,
                            format="%4.2f",
                            key=f"RB_variant_{v}_{i}",
                        )
                    else:
                        RB_i = st.slider(
                            f"_(log of) r/B variant {i}_",
                            min_value=log_min_RB,
                            max_value=log_max_RB,
                            value=default_log_RB,
                            step=0.01,
                            format="%4.2f",
                            key=f"RB_variant_{v}_{i}",
                        )
    
                    r_div_B_i = RB_i
    
                    st.write(f"**r/B {i}:** {r_div_B_i:5.2e}")
    
                    parameter_sets.append(
                        {
                            "label": rf"$r/B_{i}$ = {r_div_B_i:.2f}",
                            "T": T_fixed,
                            "S": S_fixed,
                            "r_div_B": r_div_B_i,
                            "r": r,
                            "b": b,
                            "Qs": Qs,
                            "Qd": Qd,
                        }
                    )
    
    
    # --------------------------------------------------
    # Version 3: Data fitting
    # T, S, and r/B are fitted to synthetic data
    # --------------------------------------------------
    elif v == 3:
        min_RB = 0.01
        max_RB = 3.00
        # --------------------------------------------------
        # Optional regeneration of synthetic data
        # --------------------------------------------------
        if st.button("Generate new synthetic measured data", key=f"regen_data_{v}"):
            reset_inverse_state(v)
            st.rerun()
    
        with col_1:
            with st.expander(":red[**Synthetic dataset**]", expanded=False):
                st.write("Synthetic pumping-test data generated with the Hantush-Jacob solution.")
                st.write(f"**r:** {r:.2f} m")
                st.write(f"**b:** {b:.2f} m")
                st.write(f"**Q:** {Qs:.2e} m³/s")
                st.write(f"**Q:** {Qd:.2f} m³/d")
                st.write(f"**Number of observations:** {n_measured}")
                st.write(
                    f"**Observation period:** "
                    f"{t_meas_min:.0f} s – {t_meas_max:.0f} s"
                )
                st.write(f"**Noise level:** ±{100 * noise_level:.1f}%")
    
        T = get_T_input(v, col_2, label="Transmissivity")
        S = get_S_input(v, col_3, label="Storativity")
        r_div_B = get_RB_input(v, col_2, label="Leakage parameter r/B")
    
        measured_df = pd.DataFrame(
            {
                "time": m_time_s,
                "drawdown": m_ddown,
                "drawdown_true": m_ddown_true,
            }
        )
    
        parameter_sets.append(
            {
                "label": "Synthetic data",
                "T": T,
                "S": S,
                "r_div_B": r_div_B,
                "r": r,
                "b": b,
                "Qs": Qs,
                "Qd": Qd,
                "measured_df": measured_df,
            }
        )
    
        # --------------------------------------------------
        # Calculations for fitted Hantush-Jacob curve
        # --------------------------------------------------
        K = T / b
        SS = S / b
    
        if r_div_B > 0:
            B = r / r_div_B
            K_aquitard = T * b_aquitard / B**2
        else:
            B = np.inf
            K_aquitard = 0.0
    
        t_plot = np.logspace(-1, 7, 160)
    
        s_plot = compute_s(T, S, t_plot, Qs, r, r_div_B)
    
        s_plot_theis = compute_theis_s(T, S, t_plot, Qs, r)
    
        m_ddown_hantush = compute_s(T, S, m_time_s, Qs, r, r_div_B)
    
        # --------------------------------------------------
        # Analytical derivative of fitted Hantush-Jacob curve
        # --------------------------------------------------
        derivative_time_hantush = t_plot
    
        derivative_hantush = compute_hantush_derivative_analytical(T, S, derivative_time_hantush, Qs, r, r_div_B)
    
        derivative_theis = compute_theis_derivative_analytical(T, S, derivative_time_hantush, Qs, r)
    
        # --------------------------------------------------
        # Measured derivative using Renard method only
        # --------------------------------------------------
        derivative_time_meas, derivative_meas = compute_drawdown_derivative(
            m_time_s,
            m_ddown,
            method="renard2009",
            positive_only=False,
        )
    
        theis_plateau_d = Qs / (4.0 * np.pi * T)
    
        max_s = math.ceil(max(np.max(m_ddown), np.max(m_ddown_hantush)) * 10) / 10
    
        # --------------------------------------------------
        # Text box with fitted parameters
        # --------------------------------------------------
        props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    
        out_txt = "\n".join(
            (
                r"fitted $T$ (m²/s) = %10.2E" % (T,),
                r"fitted $S$ (-) = %10.2E" % (S,),
                r"fitted $r/B$ (-) = %10.2E" % (r_div_B,),
                r"Theis plateau $Q/(4\pi T)$ = %10.2E m" % (theis_plateau_d,),
            )
        )

    # --------------------------------------------------
    # Stop if nothing should be shown
    # --------------------------------------------------
    if not show_hantush and not show_derivative and not show_theis:
        st.info("Select at least one plot option.")
        return
    
    # --------------------------------------------------
    # Plot
    # --------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    
    t_plot = np.logspace(-1, 7, 160)
    
    hantush_handles = []
    hantush_labels = []
    theis_handles = []
    theis_labels = []
    
    derivative_handle = None
    derivative_label = "drawdown derivative"
    
    plateau_handle = None
    plateau_label = r"Theis reference plateau $Q/(4\pi T)$"
    
    measured_handle = None
    measured_derivative_handle = None
    
    max_s_values = []
    
    for par in parameter_sets:
    
        T = par["T"]
        S = par["S"]
        r_div_B = par["r_div_B"]
        r = par["r"]
        Qs = par["Qs"]
        label = par["label"]
    
        s_plot = compute_s(T, S, t_plot, Qs, r, r_div_B)
        s_plot_theis = compute_theis_s(T, S, t_plot, Qs, r)
    
        max_s_values.append(np.nanmax(s_plot))
    
        # --------------------------------------------------
        # Synthetic measured data only for v = 3
        # --------------------------------------------------
        if v == 3:
            measured_df = par["measured_df"]
            t_meas = measured_df["time"].to_numpy()
            s_meas = measured_df["drawdown"].to_numpy()
    
            max_s_values.append(np.nanmax(s_meas))
    
            if show_hantush:
                measured_handle = ax.scatter(
                    t_meas,
                    s_meas,
                    s=35,
                    alpha=0.8,
                    label="_nolegend_",
                )
    
            if show_derivative:
                derivative_time_meas, derivative_meas = compute_drawdown_derivative(
                    t_meas,
                    s_meas,
                    method="renard2009",
                    positive_only=True,
                )
    
                measured_derivative_handle = ax.plot(
                    derivative_time_meas,
                    derivative_meas,
                    "o",
                    markersize=4,
                    markerfacecolor="none",
                    markeredgecolor="0.2",
                    linestyle="none",
                    label="_nolegend_",
                )[0]
    
        # --------------------------------------------------
        # Hantush drawdown
        # --------------------------------------------------
        line = None
    
        if show_hantush:
            line, = ax.plot(
                t_plot,
                s_plot,
                linewidth=2,
                label="_nolegend_",
            )
    
            hantush_handles.append(line)
            hantush_labels.append(f"Hantush-Jacob drawdown {label}")
    
        # --------------------------------------------------
        # Theis comparison
        # --------------------------------------------------
        if show_theis:
            theis_line, = ax.plot(
                t_plot,
                s_plot_theis,
                linestyle=":",
                linewidth=1.8,
                color="0.4",
                label="_nolegend_",
            )
    
            # only one Theis comparison in legend is enough
            if len(theis_handles) == 0:
                theis_handles.append(theis_line)
                theis_labels.append("Theis comparison curve")
    
        # --------------------------------------------------
        # Hantush derivative
        # --------------------------------------------------
        if show_derivative:
    
            derivative_hantush = compute_hantush_derivative_analytical(
                T,
                S,
                t_plot,
                Qs,
                r,
                r_div_B,
            )
    
            valid_hantush = derivative_hantush > 0
    
            derivative_color = line.get_color() if line is not None else None
    
            ax.plot(
                t_plot[valid_hantush],
                derivative_hantush[valid_hantush],
                "--",
                linewidth=2,
                color=derivative_color,
                label="_nolegend_",
            )
    
            if derivative_handle is None:
                derivative_handle = plt.Line2D(
                    [],
                    [],
                    linestyle="--",
                    linewidth=2,
                    color="0.2",
                )
    
            # Theis derivative / plateau as reference
            theis_plateau_d = Qs / (4.0 * np.pi * T)
    
            current_plateau_handle = ax.axhline(
                theis_plateau_d,
                linestyle=":",
                linewidth=1.6,
                color="0.2",
                alpha=0.8,
                label="_nolegend_",
            )
    
            if plateau_handle is None:
                plateau_handle = current_plateau_handle
    
    # --------------------------------------------------
    # Axes
    # --------------------------------------------------
    ax.set_xscale("log")
    
    if not semilog:
        ax.set_yscale("log")
    
    max_s = max(max_s_values) if max_s_values else 1.0
    
    if semilog:
        ax.axis([1e0, 1e7, 0, 100])
    else:
        ax.axis([1e0, 1e7, 1e-3, 1e2])
    
    ax.grid(which="both", alpha=0.3)
    
    ax.set_xlabel("time $t$ in s", fontsize=14)
    
    if show_derivative:
        ax.set_ylabel(r"drawdown $s$ and derivative $ds/d\ln(t)$ in m", fontsize=14)
    else:
        ax.set_ylabel("drawdown $s$ in m", fontsize=14)
    
    if v == 1:
        ax.set_title("Hantush-Jacob drawdown and derivative", fontsize=16)
    elif v == 2:
        ax.set_title("Influence of leakage parameter r/B", fontsize=16)
    else:
        ax.set_title("Manual fitting of synthetic Hantush-Jacob data", fontsize=16)
    
    # --------------------------------------------------
    # Legend
    # --------------------------------------------------
    legend_handles = []
    legend_labels = []
    
    if v == 3 and measured_handle is not None:
        legend_handles.append(measured_handle)
        legend_labels.append("synthetic measured drawdown")
    
    if show_hantush:
        legend_handles.extend(hantush_handles)
        legend_labels.extend(hantush_labels)
    
    if show_theis:
        legend_handles.extend(theis_handles)
        legend_labels.extend(theis_labels)
    
    if show_derivative:
        if derivative_handle is not None:
            legend_handles.append(derivative_handle)
            legend_labels.append(derivative_label)
    
        if v == 3 and measured_derivative_handle is not None:
            legend_handles.append(measured_derivative_handle)
            legend_labels.append("synthetic measured derivative")
    
        if plateau_handle is not None:
            legend_handles.append(plateau_handle)
            legend_labels.append(plateau_label)
    
    ax.legend(
        legend_handles,
        legend_labels,
        fontsize=12,
        loc="lower right",
    )
    
    # --------------------------------------------------
    # Parameter box
    # --------------------------------------------------
    if v == 1:
        par = parameter_sets[0]
        out_txt = "\n".join(
            (
                r"$T$ (m²/s) = %10.2E" % par["T"],
                r"$S$ (-) = %10.2E" % par["S"],
                r"$r/B$ (-) = %10.2E" % par["r_div_B"],
            )
        )
    
    elif v == 2:
        out_txt = "\n".join(
            (
                r"Fixed $T$ (m²/s) = %10.2E" % parameter_sets[0]["T"],
                r"Fixed $S$ (-) = %10.2E" % parameter_sets[0]["S"],
                r"$r/B$ controls leakage influence.",
            )
        )
    
    elif v == 3:
        measured_df = parameter_sets[0]["measured_df"]
        out_txt = "\n".join(
            (
                r"Fitted $T$ (m²/s) = %10.2E" % parameter_sets[0]["T"],
                r"Fitted $S$ (-) = %10.2E" % parameter_sets[0]["S"],
                r"Fitted $r/B$ (-) = %10.2E" % parameter_sets[0]["r_div_B"],
                rf"Number of points = {len(measured_df)}",
            )
        )
    
    ax.text(
        0.03,
        0.97,
        out_txt,
        horizontalalignment="left",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=props,
    )
    
    fig.tight_layout()
    st.pyplot(fig)
    
    # --------------------------------------------------
    # Show true values for fitting exercise
    # --------------------------------------------------
    if v == 3:
        show_true = st.toggle(
            "Show true parameter values",
            value=False,
            key=f"show_true_{v}",
        )
    
        if show_true:
            st.write(f"**True T:** {T_true:.2e} m²/s")
            st.write(f"**True S:** {S_true:.2e}")
            st.write(f"**True r/B:** {r_div_B_true:.2e}")

# --------------------------------------------------
# First interactive plot
# --------------------------------------------------
st.subheader(
    "Investigate :green[Hantush-Jacob drawdown] and the :green[drawdown derivative]",
    divider="green",
)

st.markdown(load_md(MD_DIR, "hantush_deriv_05.md", st.session_state.language))

active_tab = st.segmented_control(
    "Select topic",
    options=[
        "01: Understanding Hantush derivatives",
        "02: Variation of r/B",
        "03: Data Fitting",
    ],
    default="01: Understanding Hantush derivatives",
    label_visibility="collapsed",
)

if active_tab is None:
    st.info("Please select one topic to continue.")
    st.stop()

if active_tab.startswith("01"):
    st.markdown(load_md(MD_DIR, "hantush_deriv_06.md", st.session_state.language))
    inverse(1)

elif active_tab.startswith("02"):
    st.markdown(load_md(MD_DIR, "hantush_deriv_07.md", st.session_state.language))
    inverse(2)

elif active_tab.startswith("03"):
    st.markdown(load_md(MD_DIR, "hantush_deriv_08.md", st.session_state.language))
    inverse(3)

# --------------------------------------------------
# References
# --------------------------------------------------
with st.expander("**Click here for references**"):
    st.markdown(load_md(MD_DIR, "hantush_deriv_ref.md", st.session_state.language))

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4, 1, 1))
with columns_lic[0]:
    st.markdown(
        f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}',
        unsafe_allow_html=True,
    )
with columns_lic[1]:
    st.image("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png")
with columns_lic[2]:
    st.image("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/CC_BY-SA_icon.png")
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
