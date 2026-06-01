import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import math
import streamlit as st
import streamlit_book as stb
from pathlib import Path
import pandas as pd
from GWP_Pumping_Test_Derivatives_utils import load_css
from GWP_Pumping_Test_Derivatives_utils import load_md

# Authors, institutions, and year
year = 2026 
authors = {"Thomas Reimann": [1, 2]}  # Author 1 belongs to Institution 1
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
    return scipy.special.exp1(u)

def theis_u(T, S, r, t):
    return r**2 * S / (4.0 * T * t)

def theis_s(Q, T, u):
    return Q / (4.0 * np.pi * T) * well_function(u)

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    return theis_s(Q, T, u)

def compute_theis_derivative_analytical(T, S, t, Q, r):
    """
    Analytical Theis derivative with respect to ln(t):

        ds/dln(t) = t * ds/dt = Q / (4*pi*T) * exp(-u)
    """
    u = theis_u(T, S, r, t)
    return Q / (4.0 * np.pi * T) * np.exp(-u)

def compute_drawdown_derivative(time, drawdown, positive_only=True, method="renard", L=1.0):
    """
    Compute drawdown derivative with respect to log time.

    Parameters
    ----------
    time : array-like Time values. Must be positive.
    drawdown : array-like Drawdown values.
    positive_only : bool; If True, only positive derivative values are returned.
    method : str
        "renard" keeps the existing finite-difference approximation.
        "bourdet" applies the Bourdet derivative.
    L : float
        Bourdet smoothing distance in log10 cycles.
        L = 1 means one full log10 cycle.
    """

    time = np.asarray(time, dtype=float)
    drawdown = np.asarray(drawdown, dtype=float)

    if len(time) != len(drawdown):
        raise ValueError("time and drawdown must have the same length.")

    # Sort defensively
    sort_idx = np.argsort(time)
    time = time[sort_idx]
    drawdown = drawdown[sort_idx]

    valid = (
        (time > 0)
        & np.isfinite(time)
        & np.isfinite(drawdown)
    )

    time = time[valid]
    drawdown = drawdown[valid]

    if len(time) < 2:
        raise ValueError("At least two valid time points are required.")

    if np.any(np.diff(time) <= 0):
        raise ValueError("Time values must be strictly increasing.")

    # --------------------------------------------------
    # Existing Renard-style finite difference
    # --------------------------------------------------
    if method == "renard":

        ds = np.diff(drawdown)
        dt = np.diff(time)

        derivative_time = 0.5 * (time[1:] + time[:-1])
        derivative = (ds / dt) * derivative_time

    # --------------------------------------------------
    # Bourdet derivative
    # L is interpreted in log10 cycles
    # L = 1 means one decade
    # --------------------------------------------------
    elif method == "bourdet":

        if len(time) < 3:
            raise ValueError("At least three valid points are required for Bourdet derivative.")

        log_t = np.log10(time)

        derivative_time = []
        derivative = []

        for i in range(1, len(time) - 1):

            # left point at least L/2 log cycles away, if possible
            j_left = i - 1
            while j_left > 0 and (log_t[i] - log_t[j_left]) < L / 2:
                j_left -= 1

            # right point at least L/2 log cycles away, if possible
            j_right = i + 1
            while j_right < len(time) - 1 and (log_t[j_right] - log_t[i]) < L / 2:
                j_right += 1

            if log_t[i] == log_t[j_left] or log_t[j_right] == log_t[i]:
                continue

            d_left = (
                (drawdown[i] - drawdown[j_left])
                / (log_t[i] - log_t[j_left])
            )

            d_right = (
                (drawdown[j_right] - drawdown[i])
                / (log_t[j_right] - log_t[i])
            )

            w_left = log_t[j_right] - log_t[i]
            w_right = log_t[i] - log_t[j_left]

            d_i = (
                w_left * d_left
                + w_right * d_right
            ) / (w_left + w_right)

            derivative_time.append(time[i])
            derivative.append(d_i)

        derivative_time = np.asarray(derivative_time)
        derivative = np.asarray(derivative)

    else:
        raise ValueError("method must be either 'renard' or 'bourdet'.")

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

def update_T(v):
    st.session_state[f"T_slider_value_{v}"] = st.session_state[f"T_input_{v}"]

def update_S(v):
    st.session_state[f"S_slider_value_{v}"] = st.session_state[f"S_input_{v}"]

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

    # Remove widget-specific T/S input states
    widget_keys_to_delete = [
        f"T_input_slider_{v}",
        f"T_input_number_{v}",
        f"S_input_slider_{v}",
        f"S_input_number_{v}",
    ]

    for key in widget_keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

MD_DIR  = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/md")
CSS_DIR = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/css")

load_css(CSS_DIR, "segment_control_Theis_Deriv.css")

# st.title("Pumping Test Evaluation with Drawdown Derivatives")
st.header("Understanding :blue[**Drawdown Derivatives**] with the :blue[**Theis**] base model for :blue[**confined aquifers**]", divider = 'blue')

# --------------------------------------------------
# Orientation/Explanation
# --------------------------------------------------
# st.subheader("Orientation", divider="blue")

st.markdown(load_md(MD_DIR, "theis_deriv_01.md", st.session_state.language))

st.subheader("Introduction", divider="blue")

st.markdown(load_md(MD_DIR, "theis_deriv_02.md", st.session_state.language))

left_co, cent_co, last_co = st.columns((20, 60, 20))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/Theis_Deriv_01.png",
        caption=(
            "Drawdown and derivatives for various transmissivities."
        ),
    )


# --------------------------------------------------
# Initial assessment
# --------------------------------------------------
st.markdown(load_md(MD_DIR, "theis_deriv_03.md", st.session_state.language))

with st.expander(":blue[**Show/Hide the initial assessment**]"):
    st.write('Show the initial assessment')


# --------------------------------------------------
# Theory
# --------------------------------------------------
st.subheader(
    ":blue-background[Underlying Theory] - Theis Solution and Drawdown Derivatives",
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theis_deriv_04.md", st.session_state.language))

            
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
    Plot Theis drawdown curves and, optionally, drawdown derivatives.

    Versions
    --------
    v = 1: Fixed S, three user-defined T variants.
    v = 2: Fixed T, three user-defined S variants.
    v = 3: Fitting to 'measured' data
    """

    # --------------------------------------------------
    # Basic hydraulic setup
    # --------------------------------------------------
    r = 100.0
    b = 10.0
    Qs = 0.1 / 60.0        # pumping rate in m³/s
    Qd = Qs * 60 * 60 * 24 # pumping rate in m³/d, currently only informative

    log_min_T = -7.0
    log_max_T = 0.0
    log_min_S = -7.0
    log_max_S = 0.0
    
    log_T_true_min = -4.0
    log_T_true_max = -2.0
    log_S_true_min = -5.0
    log_S_true_max = -3.0

    number_input = st.toggle("Use number input instead of sliders", key=f"number_input_{v}")

    # --------------------------------------------------
    # Generate synthetic measured data once and keep them stable
    # --------------------------------------------------
    generation_key = f"synthetic_generation_{v}"
    
    if generation_key not in st.session_state:
        st.session_state[generation_key] = 0
    
    generation = st.session_state[generation_key]
    
    data_key_Theis = f"synthetic_data_{v}_{generation}"

    if data_key_Theis not in st.session_state:
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
        )

        noise = rng.normal(
            loc=0.0,
            scale=noise_level,
            size=len(m_ddown_true),
        )

        m_ddown = m_ddown_true * (1.0 + noise)

        # avoid zero or negative values caused by noise
        m_ddown = np.maximum(m_ddown, 1e-8)

        st.session_state[data_key_Theis] = {
            "m_time_s": m_time_s,
            "m_ddown": m_ddown,
            "m_ddown_true": m_ddown_true,
            "T_true": T_true,
            "S_true": S_true,
            "noise_level": noise_level,
            "n_measured": n_measured,
            "t_meas_min": t_meas_min,
            "t_meas_max": t_meas_max,
        }

    m_time_s     = st.session_state[data_key_Theis]["m_time_s"]
    m_ddown      = st.session_state[data_key_Theis]["m_ddown"]
    m_ddown_true = st.session_state[data_key_Theis]["m_ddown_true"]
    T_true       = st.session_state[data_key_Theis]["T_true"]
    S_true       = st.session_state[data_key_Theis]["S_true"]
    noise_level  = st.session_state[data_key_Theis]["noise_level"]
    n_measured   = st.session_state[data_key_Theis]["n_measured"]
    t_meas_min   = st.session_state[data_key_Theis]["t_meas_min"]
    t_meas_max   = st.session_state[data_key_Theis]["t_meas_max"]

    # --------------------------------------------------
    # Optional regeneration of synthetic data
    # --------------------------------------------------
    if st.button("Generate new synthetic measured data", key=f"regen_data_{v}"):
        reset_inverse_state(v)
        st.rerun()
     
    # --------------------------------------------------
    # Input widgets in three columns
    # --------------------------------------------------
    col_1, col_2, col_3 = st.columns((1, 1, 1), gap="medium")

    # --------------------------------------------------
    # General plot controls
    # --------------------------------------------------
    with col_1:
        with st.expander(":red[**Plot settings**]"):
            show_theis = st.toggle(
                "Show Theis drawdown curve",
                value=True,
                key=f"show_theis_{v}",
            )
    
            show_derivative = st.toggle(
                "Show drawdown derivative",
                value=False,
                key=f"show_derivative_{v}",
            )
    
            semilog = st.toggle(
                "Toggle for **semi-log graph**",
                key=f"semilog_{v}",
            )

    # --------------------------------------------------
    # Version-specific parameter input
    # --------------------------------------------------
    parameter_sets = []

    # --------------------------------------------------
    # Version 1:
    # Fixed S, three T variants
    # --------------------------------------------------
    if v == 1:
    
        with col_2:
    
            with st.expander(":blue[**Transmissivity**]"):
    
                default_log_T_values = [-2.5, -3.0, -3.5]
        
                for i, default_log_T in enumerate(default_log_T_values, start=1):
        
                    if number_input:
                        log_T_i = st.number_input(
                            f"_(log of) T variant {i} in m²/s_",
                            min_value=log_min_T,
                            max_value=log_max_T,
                            value=default_log_T,
                            step=0.01,
                            format="%4.2f",
                            key=f"T_variant_{v}_{i}",
                        )
                    else:
                        log_T_i = st.slider(
                            f"_(log of) T variant {i} in m²/s_",
                            min_value=log_min_T,
                            max_value=log_max_T,
                            value=default_log_T,
                            step=0.01,
                            format="%4.2f",
                            key=f"T_variant_{v}_{i}",
                        )
        
                    T_i = 10 ** log_T_i
        
                    st.write(f"**T{i}:** {T_i:5.2e} m²/s")
        
                    parameter_sets.append(
                        {
                            "label": f"$T_{i}$ = {T_i:.1e} m²/s",
                            "T": T_i,
                            "S": None,
                            "r": r,
                            "b": b,
                            "Qs": Qs,
                            "Qd": Qd,
                        }
                    )
    
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
                st.write("**Fixed S:** %5.2e" % S_fixed)
    
        for par in parameter_sets:
            par["S"] = S_fixed
            #par["label"] = f"{par['label']}, fixed $S$"
            par["label"] = f"{par['label']}"

    # --------------------------------------------------
    # Version 2:
    # Fixed T, three S variants
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

            with st.expander(":green[**Storativity**]"):
    
                default_log_S_values = [-4.5, -4.0, -3.5]
        
                for i, default_log_S in enumerate(default_log_S_values, start=1):
        
                    if number_input:
                        log_S_i = st.number_input(
                            f"_(log of) S variant {i}_",
                            min_value=log_min_S,
                            max_value=log_max_S,
                            value=default_log_S,
                            step=0.01,
                            format="%4.2f",
                            key=f"S_variant_{v}_{i}",
                        )
                    else:
                        log_S_i = st.slider(
                            f"_(log of) S variant {i}_",
                            min_value=log_min_S,
                            max_value=log_max_S,
                            value=default_log_S,
                            step=0.01,
                            format="%4.2f",
                            key=f"S_variant_{v}_{i}",
                        )
        
                    S_i = 10 ** log_S_i
        
                    st.write(f"**S{i}:** {S_i:5.2e}")
        
                    parameter_sets.append(
                        {
                            "label": f", $S_{i}$ = {S_i:.1e}",
                            "T": T_fixed,
                            "S": S_i,
                            "r": r,
                            "b": b,
                            "Qs": Qs,
                            "Qd": Qd,
                        }
                    )
    # --------------------------------------------------
    # Version 3:
    # Measured pumping-test datasets
    # --------------------------------------------------
    elif v == 3:

        with col_1:
            with st.expander(":blue[**Synthetic dataset**]", expanded=False):
    
                st.write("Synthetic pumping-test data generated with the Theis solution.")
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
    
        with col_2:
            with st.expander(":blue[**Transmissivity**]"):
    
                if f"T_slider_value_{v}" not in st.session_state:
                    st.session_state[f"T_slider_value_{v}"] = -3.0
    
                if number_input:
                    log_T = st.number_input(
                        "_(log of) Transmissivity in m²/s_",
                        min_value=log_min_T,
                        max_value=log_max_T,
                        value=st.session_state[f"T_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=f"T_input_{v}",
                        on_change=update_T,
                        args=(v,),
                    )
                else:
                    log_T = st.slider(
                        "_(log of) Transmissivity in m²/s_",
                        min_value=log_min_T,
                        max_value=log_max_T,
                        value=st.session_state[f"T_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=f"T_input_{v}",
                        on_change=update_T,
                        args=(v,),
                    )
    
                T = 10 ** log_T
                st.write("**T:** %5.2e m²/s" % T)
    
        with col_3:
            with st.expander(":green[**Storativity**]"):
    
                if f"S_slider_value_{v}" not in st.session_state:
                    st.session_state[f"S_slider_value_{v}"] = -4.0
    
                if number_input:
                    log_S = st.number_input(
                        "_(log of) Storativity_",
                        min_value=log_min_S,
                        max_value=log_max_S,
                        value=st.session_state[f"S_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=f"S_input_{v}",
                        on_change=update_S,
                        args=(v,),
                    )
                else:
                    log_S = st.slider(
                        "_(log of) Storativity_",
                        min_value=log_min_S,
                        max_value=log_max_S,
                        value=st.session_state[f"S_slider_value_{v}"],
                        step=0.01,
                        format="%4.2f",
                        key=f"S_input_{v}",
                        on_change=update_S,
                        args=(v,),
                    )
    
                S = 10 ** log_S
                st.write("**S:** %5.2e" % S)
    
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
                "r": r,
                "b": b,
                "Qs": Qs,
                "Qd": Qd,
                "measured_df": measured_df,
            }
        )
    # --------------------------------------------------
    # Stop if nothing should be shown
    # --------------------------------------------------
    if not show_theis and not show_derivative:
        st.info("Select at least one plot option: Theis drawdown or drawdown derivative.")
        return

    # --------------------------------------------------
    # Plot
    # --------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

    # --------------------------------------------------
    # Calculation and plotting loop
    # --------------------------------------------------
    theis_handles = []
    theis_labels = []
    
    derivative_handles = []
    derivative_labels = []
    
    derivative_handle = None
    derivative_label = "drawdown derivative"
    
    plateau_handle = None
    plateau_label = r"late-time derivative plateau $Q/(4\pi T)$"
    
    for par in parameter_sets:
        # --------------------------------------------------
        # Measured data branch for v = 3
        # --------------------------------------------------
        if v == 3:
        
            label = par["label"]
            measured_df = par["measured_df"]
        
            t_meas = measured_df["time"].to_numpy()
            s_meas = measured_df["drawdown"].to_numpy()
        
            measured_handle = None
        
            if show_theis:
                measured_handle = ax.scatter(
                    t_meas,
                    s_meas,
                    s=35,
                    alpha=0.8,
                    label="_nolegend_",
                )

                if measured_handle is not None:
                    theis_handles.append(measured_handle)
                    theis_labels.append(f"Measured drawdown: {label}")
        
            if show_derivative:
        
                derivative_time, derivative = compute_drawdown_derivative(
                    t_meas,
                    s_meas,
                    positive_only=True,
                    method="bourdet",
                    L=1.0,
                )  
        
        
                derivative_line, = ax.plot(
                    derivative_time,
                    derivative,
                    "--",
                    linewidth=1,
                    label="_nolegend_",
                )
        
                derivative_handles.append(derivative_line)
                derivative_labels.append(f"Measured derivative: {label}")
            
        T = par["T"]
        S = par["S"]
        r = par["r"]
        b = par["b"]
        Qs = par["Qs"]
        Qd = par["Qd"]
        label = par["label"]
    
        # --------------------------------------------------
        # Theis drawdown
        # --------------------------------------------------
        t_term = r**2 * S / (4.0 * T)
        s_term = Qs / (4.0 * np.pi * T)
    
        t = u_inv * t_term
        s = w_u * s_term
    
        sort_idx = np.argsort(t)
        t = t[sort_idx]
        s = s[sort_idx]
    
        # --------------------------------------------------
        # Plot drawdown
        # --------------------------------------------------
        line = None
    
        if show_theis:
            line, = ax.plot(
                t,
                s,
                linewidth=2,
                label="_nolegend_",
            )
    
            theis_handles.append(line)
            theis_labels.append(f"Theis drawdown {label}")
    
        # --------------------------------------------------
        # Plot derivative
        # --------------------------------------------------
        if show_derivative:

            # --------------------------------------------------
            # Compute derivative
            # --------------------------------------------------            
            
            derivative = compute_theis_derivative_analytical(T, S, t, Qs, r)
            derivative_time = t
            plateau_d = Qs / (4.0 * np.pi * T)
    
            # Use the same color as the corresponding Theis curve
            if line is not None:
                derivative_color = line.get_color()
            else:
                derivative_color = None
    
            derivative_line, = ax.plot(
                derivative_time,
                derivative,
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
    
            #derivative_handles.append(derivative_line)
            #derivative_labels.append(rf"derivative")
    
            # Plot plateau line in dark gray.
            # Several plateau lines may be drawn, but only one appears in the legend.
            current_plateau_handle = ax.axhline(
                plateau_d,
                linestyle=":",
                linewidth=1.8,
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

    # Fixed axis limits
    if semilog:
        ax.axis([1e-0, 1e7, 0, 100])
    else:
        ax.axis([1e-0, 1e7, 1e-3, 1e2])

    ax.grid(which="both", alpha=0.3)

    ax.set_xlabel("time $t$ in s", fontsize=14)

    if show_theis and show_derivative:
        ax.set_ylabel(r"drawdown $s$ and derivative $ds/d\ln(t)$ in m", fontsize=14)
        ax.set_title("Theis drawdown and drawdown derivative", fontsize=16)
    elif show_derivative:
        ax.set_ylabel(r"drawdown derivative $ds/d\ln(t)$ in m", fontsize=14)
        ax.set_title("Theis drawdown derivative", fontsize=16)
    else:
        ax.set_ylabel("drawdown $s$ in m", fontsize=14)
        ax.set_title("Theis drawdown", fontsize=16)

    # --------------------------------------------------
    # Legend: first Theis curves, then derivatives, then plateau
    # --------------------------------------------------
    legend_handles = []
    legend_labels = []
    
    if show_theis:
        legend_handles.extend(theis_handles)
        legend_labels.extend(theis_labels)
    
    if show_derivative:
        if derivative_handle is not None:
            legend_handles.append(derivative_handle)
            legend_labels.append(derivative_label)
    
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

        S_fixed = parameter_sets[0]["S"]

        out_txt = "\n".join(
            (
                r"Fixed $S$ (-) = %10.2E" % (S_fixed,),
                r"$T$ controls vertical position",
                r"and derivative plateau.",
            )
        )

    elif v == 2:

        T_fixed = parameter_sets[0]["T"]
        plateau_d = Qs / (4.0 * np.pi * T_fixed)

        out_txt = "\n".join(
            (
                r"Fixed $T$ (m²/s) = %10.2E" % (T_fixed,),
                r"$S$ mainly shifts the curve in time.",
                r"$d = Q/(4\pi T)$ = %10.2E m" % (plateau_d,),
            )
        )

    elif v == 3:

        selected_label = parameter_sets[0]["label"]
        measured_df = parameter_sets[0]["measured_df"]

        out_txt = "\n".join(
            (
                rf"Dataset: {selected_label}",
                rf"Number of points = {len(measured_df)}",
                rf"$t_{{min}}$ = {measured_df['time'].min():.2e} s",
                rf"$t_{{max}}$ = {measured_df['time'].max():.2e} s",
            )
        )
        
    if semilog:
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
    else:
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
    if v == 3:
        show_true = st.toggle("Show true parameter values",value=False,key=f"show_true_{v}")
        if show_true:
            st.write(f"**True T:** {T_true:.2e} m²/s")
            st.write(f"**True S:** {S_true:.2e}")



# --------------------------------------------------
# First interactive plot
# --------------------------------------------------
st.subheader(
    "Investigate :blue[Theis drawdown] and the :blue[drawdown derivative]",
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theis_deriv_05.md", st.session_state.language))

active_tab = st.segmented_control(
    "Select topic",
    options=[
        "01: Variation of T",
        "02: Variation of S",
        "03: Data Fitting",
    ],
    default="01: Variation of T",
    label_visibility="collapsed",
)

if active_tab is None:
    st.info("Please select one topic to continue.")
    st.stop()

if active_tab.startswith("01"):
    st.markdown(load_md(MD_DIR, "theis_deriv_06.md", st.session_state.language))
    inverse(1)

elif active_tab.startswith("02"):
    st.markdown(load_md(MD_DIR, "theis_deriv_07.md", st.session_state.language))
    inverse(2)

elif active_tab.startswith("03"):
    st.markdown(load_md(MD_DIR, "theis_deriv_08.md", st.session_state.language))
    inverse(3)

# --------------------------------------------------
# References
# --------------------------------------------------
with st.expander("**Click here for references**"):
    st.markdown(load_md(MD_DIR, "theis_deriv_ref.md", st.session_state.language))

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png')
with columns_lic[2]:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/CC_BY-SA_icon.png')
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
    unsafe_allow_html=True
)