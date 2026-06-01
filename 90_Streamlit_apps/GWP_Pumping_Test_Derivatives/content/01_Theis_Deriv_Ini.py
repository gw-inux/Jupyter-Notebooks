# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import math
import streamlit as st
from pathlib import Path
import pandas as pd
from GWP_Pumping_Test_Derivatives_utils import load_css
from GWP_Pumping_Test_Derivatives_utils import load_md

# ------------------------------------------------------------
# Authors, institutions, and year
# ------------------------------------------------------------

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

def compute_drawdown_derivative(
    time,
    drawdown,
    positive_only=True,
    method="renard",
    L=1.0):
    """
    Compute drawdown derivative with respect to log time.

    Parameters
    ----------
    time : array-like, Time values. Must be positive.
    drawdown : array-like. Drawdown values.
    positive_only : bool, If True, only positive derivative values are returned.
    method : str, "renard" finite-difference approximation. "bourdet" applies the Bourdet derivative.
    L : float, Bourdet smoothing distance in log10 cycles. L = 1 means one full log10 cycle.
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
    # Renard-style finite difference
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

            # Convert from ds/dlog10(t) to ds/dln(t)
            d_i = d_i / np.log(10)

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

# Compute the derivative for the measured data only once
@st.cache_data
def cached_drawdown_derivative(t_meas, s_meas, L=1.0):
    return compute_drawdown_derivative(
        t_meas,
        s_meas,
        positive_only=True,
        method="bourdet",
        L=L,
    )
    
def compute_statistics(measured, computed):
    measured = np.asarray(measured)
    computed = np.asarray(computed)

    error = computed - measured

    me = np.mean(error)
    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error**2))

    return me, mae, rmse

@st.cache_data
def load_measured_dataset(csv_file, t_min_threshold=2000):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()

    # Flexible column detection
    time_candidates = [
        "time", "t", "Time", "TIME",
        "time_min", "time_days",
        "time [min]", "t_min", "m_time"
    ]

    head_candidates = [
        "head_observation_m",
        "head",
        "Head",
        "HEAD"
    ]

    time_col = next((c for c in time_candidates if c in df.columns), None)
    head_col = next((c for c in head_candidates if c in df.columns), None)

    if time_col is None or head_col is None:
        raise ValueError(
            f"CSV file {csv_file.name} must contain time and head columns. "
            f"Found columns: {list(df.columns)}"
        )

    df = df[[time_col, head_col]].copy()
    df.columns = ["time", "head"]

    # Convert measured time from days to seconds
    df["time"] = (df["time"] - 1.0) * 86400

    df = df.dropna()
    df = df.sort_values("time")

    h0 = df["head"].iloc[0]                # Reference head BEFORE removing early times
    df["drawdown"] = h0 - df["head"]       # Compute drawdown relative to initial head
    df = df[df["time"] >= t_min_threshold] # Remove early-time data
    df = df[df["drawdown"] >= 0]           # Remove negative drawdowns

    return df[["time", "drawdown"]]

def update_T(v):
    st.session_state[f"T_slider_value_{v}"] = st.session_state[f"T_input_{v}"]

def update_S(v):
    st.session_state[f"S_slider_value_{v}"] = st.session_state[f"S_input_{v}"]
    
# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

MD_DIR  = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/md")
CSS_DIR = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/css")

load_css(CSS_DIR, "segment_control_Theis_Deriv_Ini.css")

#st.title("Pumping Test Evaluation with :blue[Derivatives]")

st.header("**Intro:** :blue[**Understanding**] Drawdown Derivatives :blue[**with**] the :blue[**Theis**] base model", divider = 'blue')

# --------------------------------------------------
# Orientation/Explanation
# --------------------------------------------------
# st.subheader("Orientation", divider="blue")

st.markdown(load_md(MD_DIR, "theis_deriv_ini_01.md", st.session_state.language))

st.subheader("Introduction", divider="blue")

st.markdown(load_md(MD_DIR, "theis_deriv_ini_02.md", st.session_state.language))

left_co, cent_co, last_co = st.columns((20, 60, 20))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/Theis_Deriv_Ini_01.png",
        caption=(
            "Theis drawdown and drawdown derivative."
        ),
    )

# --------------------------------------------------
# Initial assessment
# --------------------------------------------------
st.markdown(load_md(MD_DIR, "theis_deriv_ini_03.md", st.session_state.language))

with st.expander(":blue[**Show/Hide the initial assessment**]"):
    st.write('Show the initial assessment')

# --------------------------------------------------
# Theory
# --------------------------------------------------
st.subheader(
    "Underlying Theory - :blue[Drawdown derivatives]",
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theis_deriv_ini_04.md", st.session_state.language))
# --------------------------------------------------
# Type curve data
# --------------------------------------------------
u_min = -5
u_max = 4

u = np.logspace(u_min, u_max)
u_inv = 1 / u
w_u = well_function(u)

# --------------------------------------------------
# Measured data information
# --------------------------------------------------
MEASURED_DATASETS = {
    "INI_01": {
        "file": Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/data/Theis_INI_01.csv"),
        "r": 100.0,          # m
        "b": 10.0,           # m
        "Qs": 1000/86400,     # m^3/s
    },
    "INI_02": {
        "file": Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/data/Theis_INI_02.csv"),
        "r": 100.0,          # m
        "b": 10.0,           # m
        "Qs": 1000/86400,     # m^3/s
    },
    "INI_03": {
        "file": Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/data/Theis_INI_03.csv"),
        "r": 100.0,          # m
        "b": 10.0,           # m
        "Qs": 1000/86400,     # m^3/s
    },
}
    
# --------------------------------------------------
# Interactive inverse function
# --------------------------------------------------
@st.fragment
def inverse(v):
    """
    Plot Theis drawdown curves and, optionally, drawdown derivatives.

    Versions
    --------
    v = 0:
        One Theis curve with user-defined T and S.
    v = 1 / 2 / 3:
        Load dataset 1 / 2 / 3
    """

    # --------------------------------------------------
    # Initialize toggle states
    # --------------------------------------------------
    toggle_defaults = {
        f"number_input_{v}": False,
        f"show_theis_{v}": True,
        f"show_derivative_{v}": False,
        f"semilog_{v}": False,
    }
    
    for key, default in toggle_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

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

    number_input = st.toggle(
                "Use number input instead of sliders",
                key=f"number_input_{v}",
            )
     
    # --------------------------------------------------
    # Input widgets in three columns
    # --------------------------------------------------
    col_1, col_2, col_3 = st.columns((1, 1, 1), gap="medium")

    # --------------------------------------------------
    # General plot controls
    # --------------------------------------------------
    with col_1:
        with st.expander(":red[**Plot settings**]"):
            show_theis = st.toggle("Show Theis drawdown curve", value=True, key=f"show_theis_{v}")
            show_derivative = st.toggle("Show drawdown derivative", value=False, key=f"show_derivative_{v}")
            semilog = st.toggle("Toggle for **semi-log graph**", key=f"semilog_{v}")

    # --------------------------------------------------
    # Version-specific parameter input
    # --------------------------------------------------
    parameter_sets = []

    # --------------------------------------------------
    # Version 0:
    # One freely adjustable T/S combination
    # --------------------------------------------------
    if v == 0:

        if f"T_slider_value_{v}" not in st.session_state:
            st.session_state[f"T_slider_value_{v}"] = -3.0

        if f"S_slider_value_{v}" not in st.session_state:
            st.session_state[f"S_slider_value_{v}"] = -4.0

        with col_2:
            with st.expander(":blue[**Transmissivity**]"):
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

        parameter_sets.append(
            {
                "label": "",
                "T": T,
                "S": S,
                "r": r,
                "b": b,
                "Qs": Qs,
                "Qd": Qd,
            }
        )

    # --------------------------------------------------
    # Version 1:
    # One freely adjustable T/S combination
    # --------------------------------------------------
    elif v == 1:

        selected_dataset = "INI_01"

        with col_1:
            with st.expander(":blue[**Measured dataset**]"):
                dataset_info = MEASURED_DATASETS[selected_dataset]
                csv_file = dataset_info["file"]
                r = dataset_info["r"]
                b = dataset_info["b"]
                Qs = dataset_info["Qs"]
                Qd = Qs * 60 * 60 * 24
                st.write(f"**File:** `{csv_file}`")
                st.write(f"**r:** {r:.2f} m")
                st.write(f"**b:** {b:.2f} m")
                st.write(f"**Q:** {Qs:.2e} m³/s")
                st.write(f"**Q:** {Qd:.2f} m³/d")

                show_points = True
                show_lines = False

        with col_2:
            with st.expander(":blue[**Transmissivity**]"):

                if f"T_slider_value_{v}" not in st.session_state:
                    st.session_state[f"T_slider_value_{v}"] = -3.0

                if f"S_slider_value_{v}" not in st.session_state:
                    st.session_state[f"S_slider_value_{v}"] = -4.0

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
        try:
            measured_df = load_measured_dataset(csv_file)

        except Exception as e:
            st.error(f"Could not load measured dataset: {e}")
            return

        parameter_sets.append(
            {
                "label": selected_dataset,
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
    # Version 2:
    # Measured pumping-test datasets
    # --------------------------------------------------
    elif v == 2:
        selected_dataset = "INI_02"
        with col_1:
            with st.expander(":blue[**Measured dataset**]"):

                dataset_info = MEASURED_DATASETS[selected_dataset]

                csv_file = dataset_info["file"]
                r = dataset_info["r"]
                b = dataset_info["b"]
                Qs = dataset_info["Qs"]
                Qd = Qs * 60 * 60 * 24

                st.write(f"**File:** `{csv_file}`")
                st.write(f"**r:** {r:.2f} m")
                st.write(f"**b:** {b:.2f} m")
                st.write(f"**Q:** {Qs:.2e} m³/s")
                st.write(f"**Q:** {Qd:.2f} m³/d")

                show_points = True

                show_lines = False

        with col_2:
            with st.expander(":blue[**Transmissivity**]"):

                if f"T_slider_value_{v}" not in st.session_state:
                    st.session_state[f"T_slider_value_{v}"] = -3.0

                if f"S_slider_value_{v}" not in st.session_state:
                    st.session_state[f"S_slider_value_{v}"] = -4.0

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

        try:
            measured_df = load_measured_dataset(csv_file)

        except Exception as e:
            st.error(f"Could not load measured dataset: {e}")
            return

        parameter_sets.append(
            {
                "label": selected_dataset,
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
    # Version 3:
    # Measured pumping-test datasets
    # --------------------------------------------------
    elif v == 3:
        selected_dataset = "INI_03"
        with col_1:
            with st.expander(":blue[**Measured dataset**]"):

                dataset_info = MEASURED_DATASETS[selected_dataset]

                csv_file = dataset_info["file"]
                r = dataset_info["r"]
                b = dataset_info["b"]
                Qs = dataset_info["Qs"]
                Qd = Qs * 60 * 60 * 24

                st.write(f"**File:** `{csv_file}`")
                st.write(f"**r:** {r:.2f} m")
                st.write(f"**b:** {b:.2f} m")
                st.write(f"**Q:** {Qs:.2e} m³/s")
                st.write(f"**Q:** {Qd:.2f} m³/d")

                show_points = True
                show_lines = False

        with col_2:
            with st.expander(":blue[**Transmissivity**]"):

                if f"T_slider_value_{v}" not in st.session_state:
                    st.session_state[f"T_slider_value_{v}"] = -3.0

                if f"S_slider_value_{v}" not in st.session_state:
                    st.session_state[f"S_slider_value_{v}"] = -4.0

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

        try:
            measured_df = load_measured_dataset(csv_file)

        except Exception as e:
            st.error(f"Could not load measured dataset: {e}")
            return

        parameter_sets.append(
            {
                "label": selected_dataset,
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
    
    PLOT_COLORS = {
    1: {
        "drawdown": "darkorange",
        "derivative": "peachpuff",
    },
    2: {
        "drawdown": "limegreen",
        "derivative": "palegreen",
    },
    3: {
        "drawdown": "darkorchid",
        "derivative": "plum",
    },
}

    # --------------------------------------------------
    # Calculation and plotting loop
    # --------------------------------------------------
    theis_handles = []
    theis_labels = []
    
    derivative_handles = []
    derivative_labels = []
    
    plateau_handle = None
    plateau_label = r"late-time derivative plateau $Q/(4\pi T)$"
    
    for par in parameter_sets:
        # --------------------------------------------------
        # Measured data branch for v 1/2/3
        # --------------------------------------------------
        if v in [1, 2, 3]:
            label = par["label"]
            measured_df = par["measured_df"]
        
            t_meas = measured_df["time"].to_numpy()
            s_meas = measured_df["drawdown"].to_numpy()
        
            measured_handle = None
            
            colors = PLOT_COLORS[v]
            drawdown_color = colors["drawdown"]
            derivative_color = colors["derivative"]
        
            if show_theis:
                measured_handle = ax.scatter(t_meas, s_meas, s=25, alpha=0.8, color = drawdown_color, label="_nolegend_")
        
                if measured_handle is not None:
                    theis_handles.append(measured_handle)
                    #theis_labels.append(f"Measured drawdown: {label}")
                    theis_labels.append(f"Drawdown measured")
        
            if show_derivative:
                derivative_time, derivative = cached_drawdown_derivative(t_meas, s_meas, L=1.0)
        
                derivative_line, = ax.plot(
                    derivative_time,
                    derivative,
                    "--o",
                    linewidth=1,
                    color=derivative_color,
                    markersize=5,
                    markerfacecolor="none",
                    markeredgecolor=derivative_color,
                    label="_nolegend_",
                )
        
                derivative_handles.append(derivative_line)
                derivative_labels.append(f"Derivative measured")
            
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
        # Theis derivative using analytical solution
        # --------------------------------------------------
        derivative_time = t
        
        derivative = compute_theis_derivative_analytical(T=T, S=S, t=t, Q=Qs, r=r)
    
        plateau_d = Qs / (4.0 * np.pi * T)
    
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
            theis_labels.append(f"Drawdown Theis")
    
        # --------------------------------------------------
        # Plot derivative
        # --------------------------------------------------
        if show_derivative:
    
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
    
            derivative_handles.append(derivative_line)
            derivative_labels.append(rf"Derivative Theis")
    
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
        ax.axis([1e1, 1e7, 0, 10])
    else:
        ax.axis([1e1, 1e7, 1e-2, 1e1])

    ax.grid(which="both", alpha=0.5)

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
        legend_handles.extend(derivative_handles)
        legend_labels.extend(derivative_labels)
    
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
    T = parameter_sets[0]["T"]
    S = parameter_sets[0]["S"]
    plateau_d = Qs / (4.0 * np.pi * T)
    
    out_txt = "\n".join(
        (
            r"$T$ (m²/s) = %10.2E" % (T,),
            r"$S$ (-) = %10.2E" % (S,),
            r"$d = Q/(4\pi T)$ = %10.2E m" % (plateau_d,),
        )
    )
        
    ax.text(0.03, 0.97, out_txt, horizontalalignment="left", transform=ax.transAxes, fontsize=12, verticalalignment="top", bbox=props)
    fig.tight_layout()
    st.pyplot(fig)

# --------------------------------------------------
# Interactive plot
# --------------------------------------------------
st.subheader("Investigate :blue[Theis drawdown] and the :blue[drawdown derivative]", divider="blue")

st.markdown(load_md(MD_DIR, "theis_deriv_ini_05.md", st.session_state.language))

left_co, cent_co, last_co = st.columns((30, 40, 30))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/Theis_Deriv_Ini_02.png",
        caption=(
            "Idealized Catchment."
        ),
    )
    
active_tab = st.segmented_control(
    "Select topic",
    options=[
        "01: A First Look on Derivatives",
        "02: A Short Pumping Test",
        "03: Pumping Longer",
        "04: A Different Well",
    ],
    default="01: A First Look on Derivatives",
    label_visibility="collapsed",
)

if active_tab is None:
    st.info("Please select one topic to continue.")
    st.stop()

if active_tab.startswith("01"):
    st.markdown(load_md(MD_DIR, "theis_deriv_ini_06.md", st.session_state.language))
    inverse(0)

elif active_tab.startswith("02"):
    st.markdown(load_md(MD_DIR, "theis_deriv_ini_07.md", st.session_state.language))
    inverse(1)

elif active_tab.startswith("03"):
    st.markdown(load_md(MD_DIR, "theis_deriv_ini_08.md", st.session_state.language))
    inverse(2)

elif active_tab.startswith("04"):
    st.markdown(load_md(MD_DIR, "theis_deriv_ini_09.md", st.session_state.language))
    inverse(3)
    
# --------------------------------------------------
# References
# --------------------------------------------------
with st.expander("**Click here for references**"):
    st.markdown(load_md(MD_DIR, "theis_deriv_ini_ref.md", st.session_state.language))

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