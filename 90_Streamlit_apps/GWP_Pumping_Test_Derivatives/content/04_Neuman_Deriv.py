# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import scipy.interpolate
from pathlib import Path
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

def neuman_branch_curve(T, Ss, Sy, beta_index, r, b, Qs, u_inv_a, u_inv_b, w_u_a, w_u_b):
    """
    Compute early- and late-time Neuman drawdown branches.

    The early branch is controlled by elastic aquifer storage:
        Sa = Ss * b

    The late branch is controlled by specific yield:
        Sy

    Parameters
    ----------
    T : float Transmissivity [m²/s]
    Ss : float Specific storage [1/m
    Sy : float Specific yield [-]
    beta_index : int Column index of the selected Neuman beta curve.
    r : float Radial distance from pumping well [m]
    b : float Aquifer thickness [m]
    Qs : float Pumping rate [m³/s]
    u_inv_a, u_inv_b : ndarray Inverse dimensionless time arrays for Neuman early and late curves.
    w_u_a, w_u_b : ndarray Neuman well-function table values for early and late curves.

    Returns
    -------
    t_a, s_a, t_b, s_b : ndarray Early and late Neuman branch times and drawdowns.
    """

    Sa = Ss * b
    s_term = Qs / (4.0 * np.pi * T)

    # Early branch: elastic storage
    t_a_term = r**2 * Sa / (4.0 * T)
    t_a = u_inv_a * t_a_term
    s_a = w_u_a[:, beta_index] * s_term

    # Late branch: water-table drainage / specific yield
    t_b_term = r**2 * Sy / (4.0 * T)
    t_b = u_inv_b * t_b_term

    s_b = []

    for i, u_inv_value in enumerate(u_inv_b):

        w_value = w_u_b[i, beta_index]

        # In the table, 999 marks values where the Theis well function is used
        if w_value == 999:
            w_value = scipy.special.exp1(1.0 / u_inv_value)

        s_b.append(w_value * s_term)

    s_b = np.asarray(s_b)

    return t_a, s_a, t_b, s_b
    

def smooth_loglog_curve(time, drawdown, n_dense=500, smoothing_factor=1e-3):
    """
    Smooth a drawdown curve in log(time)-log(drawdown) space.

    This function returns only the smoothed drawdown curve.
    The derivative is computed separately with the Bourdet method.
    """

    time = np.asarray(time, dtype=float)
    drawdown = np.asarray(drawdown, dtype=float)

    valid = (
        np.isfinite(time)
        & np.isfinite(drawdown)
        & (time > 0)
        & (drawdown > 0)
    )

    time = time[valid]
    drawdown = drawdown[valid]

    if len(time) < 4:
        return time, drawdown

    # --------------------------------------------------
    # Sort by time
    # --------------------------------------------------
    sort_idx = np.argsort(time)
    time = time[sort_idx]
    drawdown = drawdown[sort_idx]

    log_t = np.log(time)
    log_s = np.log(drawdown)

    # --------------------------------------------------
    # Remove duplicate or near-duplicate log-time values
    # --------------------------------------------------
    grouped = {}

    for x, y in zip(log_t, log_s):
        key = round(float(x), 10)

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(float(y))

    log_t_unique = np.array(sorted(grouped.keys()))
    log_s_unique = np.array(
        [np.mean(grouped[key]) for key in log_t_unique]
    )

    if len(log_t_unique) < 4:
        return time, drawdown

    # --------------------------------------------------
    # Normalize x-values for stable spline fitting
    # --------------------------------------------------
    x_min = log_t_unique.min()
    x_max = log_t_unique.max()

    x_unique = (log_t_unique - x_min) / (x_max - x_min)

    log_t_dense = np.linspace(
        log_t_unique.min(),
        log_t_unique.max(),
        n_dense,
    )

    x_dense = (log_t_dense - x_min) / (x_max - x_min)

    # --------------------------------------------------
    # Smooth spline in log-log space
    # --------------------------------------------------
    k = min(3, len(x_unique) - 1)

    spline = scipy.interpolate.UnivariateSpline(
        x_unique,
        log_s_unique,
        k=k,
        s=smoothing_factor * len(x_unique),
    )

    log_s_dense = spline(x_dense)

    t_dense = np.exp(log_t_dense)
    s_dense = np.exp(log_s_dense)

    return t_dense, s_dense


def bourdet_derivative_logcycle(time, drawdown, L=1.0):
    """
    Compute the Bourdet derivative ds/dln(t).

    L is the total derivative window in log10 time cycles.

    Example:
        L = 1.0 means one full log cycle:
            left support point  = log10(t_i) - 0.5
            right support point = log10(t_i) + 0.5

    The derivative is computed from interpolated support points on the
    smoothed drawdown curve.
    """

    time = np.asarray(time, dtype=float)
    drawdown = np.asarray(drawdown, dtype=float)

    # --------------------------------------------------
    # Keep only valid positive values
    # --------------------------------------------------
    valid = (
        np.isfinite(time)
        & np.isfinite(drawdown)
        & (time > 0)
        & (drawdown > 0)
    )

    time = time[valid]
    drawdown = drawdown[valid]

    if len(time) < 5:
        return np.array([]), np.array([])

    # --------------------------------------------------
    # Sort by time
    # --------------------------------------------------
    sort_idx = np.argsort(time)
    time = time[sort_idx]
    drawdown = drawdown[sort_idx]

    # --------------------------------------------------
    # Work in natural-log time because the derivative is ds/dln(t)
    # --------------------------------------------------
    ln_t = np.log(time)

    # L is given in log10 cycles.
    # Convert half the L-window to natural-log units.
    half_window_ln = 0.5 * L * np.log(10.0)

    derivative_time = []
    derivative = []

    # --------------------------------------------------
    # Compute Bourdet derivative
    # --------------------------------------------------
    for i in range(len(time)):

        ln_t_i = ln_t[i]
        ln_left = ln_t_i - half_window_ln
        ln_right = ln_t_i + half_window_ln

        # Skip points where the full L-window is outside the data range
        if ln_left < ln_t[0] or ln_right > ln_t[-1]:
            continue

        # Interpolate drawdown at the left and right support points
        s_left = np.interp(ln_left, ln_t, drawdown)
        s_mid = drawdown[i]
        s_right = np.interp(ln_right, ln_t, drawdown)

        # Local slopes
        left_slope = (s_mid - s_left) / (ln_t_i - ln_left)
        right_slope = (s_right - s_mid) / (ln_right - ln_t_i)

        # Bourdet weighted derivative
        d_left = ln_t_i - ln_left
        d_right = ln_right - ln_t_i

        d_bourdet = (
            d_right * left_slope + d_left * right_slope
        ) / (d_left + d_right)

        if np.isfinite(d_bourdet) and d_bourdet > 0:
            derivative_time.append(time[i])
            derivative.append(d_bourdet)

    return np.asarray(derivative_time), np.asarray(derivative)


def update_T(v):
    """Synchronize number input values to the associated T slider state."""
    st.session_state[f"T_slider_value_{v}"] = st.session_state[f"T_input_{v}"]


def update_S(v):
    """Synchronize number input values to the associated storage slider state."""
    st.session_state[f"S_slider_value_{v}"] = st.session_state[f"S_input_{v}"]


def prepare_synced_widget_keys(prefix, suffix, default, use_number_input):
    """
    Prepare paired number-input/slider keys.

    This keeps the established update_T/update_S structure while allowing
    several T, Ss, and Sy widgets in one app. The value stored in the slider
    key is treated as the persistent value. When switching widget modes, the
    currently active value is copied to the newly visible widget.
    """

    slider_key = f"{prefix}_slider_value_{suffix}"
    input_key = f"{prefix}_input_{suffix}"
    mode_key = f"{prefix}_widget_mode_{suffix}"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = default

    new_mode = "number" if use_number_input else "slider"
    old_mode = st.session_state.get(mode_key, None)

    if new_mode == "number":
        if old_mode != "number" or input_key not in st.session_state:
            st.session_state[input_key] = st.session_state[slider_key]
    else:
        if old_mode == "number" and input_key in st.session_state:
            st.session_state[slider_key] = st.session_state[input_key]

    st.session_state[mode_key] = new_mode

    return slider_key, input_key

def neuman_combined_curve(
    T,
    Ss,
    Sy,
    beta_index,
    r,
    b,
    Qs,
    u_inv_a,
    u_inv_b,
    w_u_a,
    w_u_b,
    n_dense=300,
    transition_buffer_log_cycles=0.25,
    early_theis_extension_log_cycles=2.0,
):
    """
    Compute one combined and densified Neuman drawdown curve from the early
    A-branch and the late B-branch.

    The sparse tabulated Neuman type-curve data are first combined, then
    interpolated in log(time)-log(drawdown) space. This gives a smoother
    drawdown curve and a more stable numerical derivative.

    Parameters
    ----------
    n_dense : int
        Number of points in the returned dense curve.

    transition_buffer_log_cycles : float
        Width around the detected A/B transition where both branches are
        allowed to contribute to the interpolation point cloud.
        This avoids a hard splice and reduces artificial derivative dips.
    """

    Sa = Ss * b
    s_term = Qs / (4.0 * np.pi * T)

    # --------------------------------------------------
    # Physical time axes
    # --------------------------------------------------
    t_a_term = r**2 * Sa / (4.0 * T)
    t_b_term = r**2 * Sy / (4.0 * T)

    t_a = np.asarray(u_inv_a, dtype=float) * t_a_term
    t_b = np.asarray(u_inv_b, dtype=float) * t_b_term
    
    # --------------------------------------------------
    # Optional early-time Theis extension
    # --------------------------------------------------
    if early_theis_extension_log_cycles > 0:
        t_a_min = np.min(t_a)
    
        t_theis_min = t_a_min / (10 ** early_theis_extension_log_cycles)
        t_theis_max = t_a_min
    
        t_theis_early = np.logspace(
            np.log10(t_theis_min),
            np.log10(t_theis_max),
            80,
        )
    
        u_theis_early = r**2 * Sa / (4.0 * T * t_theis_early)
        s_theis_early = scipy.special.exp1(u_theis_early) * s_term
    else:
        t_theis_early = np.array([])
        s_theis_early = np.array([])

    # --------------------------------------------------
    # Well-function values
    # --------------------------------------------------
    w_a = np.asarray(w_u_a[:, beta_index], dtype=float)
    w_b = np.asarray(w_u_b[:, beta_index], dtype=float).copy()

    # Replace 999 placeholders in B branch
    for i, u_inv_value in enumerate(u_inv_b):
        if np.isclose(w_b[i], 999.0) or np.isclose(w_b[i], 9.99e2):
            w_b[i] = scipy.special.exp1(1.0 / u_inv_value)

    s_a = w_a * s_term
    s_b = w_b * s_term
    
    # --------------------------------------------------
    # Add early-time Theis response to A branch
    # --------------------------------------------------
    t_a = np.concatenate([t_theis_early, t_a])
    s_a = np.concatenate([s_theis_early, s_a])
    w_a = np.concatenate([
        scipy.special.exp1(u_theis_early),
        w_a,
    ])

    # --------------------------------------------------
    # Clean branches
    # --------------------------------------------------
    valid_a = (
        np.isfinite(t_a)
        & np.isfinite(s_a)
        & np.isfinite(w_a)
        & (t_a > 0)
        & (s_a > 0)
        & (w_a > 0)
    )

    valid_b = (
        np.isfinite(t_b)
        & np.isfinite(s_b)
        & np.isfinite(w_b)
        & (t_b > 0)
        & (s_b > 0)
        & (w_b > 0)
    )

    t_a = t_a[valid_a]
    s_a = s_a[valid_a]
    w_a = w_a[valid_a]

    t_b = t_b[valid_b]
    s_b = s_b[valid_b]
    w_b = w_b[valid_b]

    sort_a = np.argsort(t_a)
    sort_b = np.argsort(t_b)

    t_a = t_a[sort_a]
    s_a = s_a[sort_a]
    w_a = w_a[sort_a]

    t_b = t_b[sort_b]
    s_b = s_b[sort_b]
    w_b = w_b[sort_b]

    if len(t_a) < 2 or len(t_b) < 2:
        return np.array([]), np.array([]), np.array([]), np.array([])

    # --------------------------------------------------
    # Identify overlap by closest W-value in log space
    # --------------------------------------------------
    log_w_a = np.log10(w_a)
    log_w_b = np.log10(w_b)

    diff_matrix = np.abs(log_w_a[:, None] - log_w_b[None, :])

    ia, ib = np.unravel_index(
        np.nanargmin(diff_matrix),
        diff_matrix.shape,
    )

    transition_time = max(t_a[ia], t_b[ib])
    log_transition_time = np.log10(transition_time)

    # --------------------------------------------------
    # Soft transition interval
    # --------------------------------------------------
    log_t_a = np.log10(t_a)
    log_t_b = np.log10(t_b)

    lower_transition = log_transition_time - transition_buffer_log_cycles
    upper_transition = log_transition_time + transition_buffer_log_cycles

    # Keep A before and through the transition region
    use_a = log_t_a <= upper_transition

    # Keep B from the transition region onward
    use_b = log_t_b >= lower_transition

    t_sparse = np.concatenate([t_a[use_a], t_b[use_b]])
    s_sparse = np.concatenate([s_a[use_a], s_b[use_b]])
    source_sparse = np.concatenate([
        np.full(np.sum(use_a), "A"),
        np.full(np.sum(use_b), "B"),
    ])

    # --------------------------------------------------
    # Sort sparse point cloud
    # --------------------------------------------------
    sort_sparse = np.argsort(t_sparse)

    t_sparse = t_sparse[sort_sparse]
    s_sparse = s_sparse[sort_sparse]
    source_sparse = source_sparse[sort_sparse]

    # --------------------------------------------------
    # Remove duplicated time values by averaging in log-space
    # --------------------------------------------------
    log_t_sparse = np.log10(t_sparse)
    log_s_sparse = np.log10(s_sparse)

    df_like = {}

    for lt, ls in zip(log_t_sparse, log_s_sparse):
        # round to avoid numerical duplicates at nearly identical x locations
        key = round(float(lt), 10)

        if key not in df_like:
            df_like[key] = []

        df_like[key].append(float(ls))

    log_t_unique = np.array(sorted(df_like.keys()))
    log_s_unique = np.array([
        np.mean(df_like[key])
        for key in log_t_unique
    ])

    if len(log_t_unique) < 2:
        return np.array([]), np.array([]), source_sparse, np.array([transition_time])

    # --------------------------------------------------
    # Dense log-log interpolation
    # --------------------------------------------------
    log_t_dense = np.linspace(
        log_t_unique.min(),
        log_t_unique.max(),
        n_dense,
    )

    log_s_dense = np.interp(
        log_t_dense,
        log_t_unique,
        log_s_unique,
    )

    t_dense = 10 ** log_t_dense
    s_dense = 10 ** log_s_dense

    return (
        t_dense,
        s_dense,
        source_sparse,
        np.array([transition_time]),
    )

# --------------------------------------------------
# Type curve data
# --------------------------------------------------
# Neuman type-curve data used to construct early-time and late-time drawdown branches.
u_inv_a = np.array([4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00, 4.00E+00, 8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01, 8.00E+01, 1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02, 1.40E+03, 2.40E+03, 4.00E+03, 8.00E+03])

u_inv_b = np.array([1.40E-02, 2.40E-02, 4.00E-02, 8.00E-02, 1.40E-01, 2.40E-01, 4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00, 4.00E+00, 8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01, 8.00E+01, 1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02, 1.00E+03])


# Neuman type curve data from tables
# ToDo: Save as CSV and then load the CSV from the DATA-folder

w_u_a = [[2.48E-02, 2.41E-02, 2.30E-02, 2.14E-02, 1.88E-02, 1.70E-02, 1.38E-02, 1.00E-02, 1.00E-02],
         [1.45E-01, 1.40E-01, 1.31E-01, 1.19E-01, 9.88E-02, 8.49E-02, 6.03E-02, 3.17E-02, 1.74E-02],
         [3.58E-01, 3.45E-01, 3.18E-01, 2.79E-01, 2.17E-01, 1.75E-01, 1.07E-01, 4.45E-02, 2.10E-02],
         [6.62E-01, 6.33E-01, 5.70E-01, 4.83E-01, 3.43E-01, 2.56E-01, 1.33E-01, 4.76E-02, 2.14E-02],
         [1.02E+00, 9.63E-01, 8.49E-01, 6.88E-01, 4.38E-01, 3.00E-01, 1.40E-01, 4.78E-02, 2.15E-02],
         [1.57E+00, 1.46E+00, 1.23E+00, 9.18E-01, 4.97E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [2.05E+00, 1.88E+00, 1.51E+00, 1.03E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [2.52E+00, 2.27E+00, 1.73E+00, 1.07E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [2.97E+00, 2.61E+00, 1.85E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [3.56E+00, 3.00E+00, 1.92E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [4.01E+00, 3.23E+00, 1.93E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [4.42E+00, 3.37E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [4.77E+00, 3.43E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.16E+00, 3.45E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.40E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.54E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.59E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02]]

w_u_a = np.array(w_u_a)

w_u_b = [[5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.12E-01, 3.23E-01, 1.45E-01, 5.09E-02, 2.39E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.12E-01, 3.23E-01, 1.47E-01, 5.32E-02, 2.57E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.16E-01, 3.27E-01, 1.52E-01, 5.68E-02, 2.86E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.24E-01, 3.37E-01, 1.62E-01, 6.61E-02, 3.62E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.10E+00, 5.37E-01, 3.50E-01, 1.78E-01, 8.06E-02, 4.86E-02],
         [5.62E+00, 3.46E+00, 1.95E+00, 1.11E+00, 5.57E-01, 3.74E-01, 2.05E-01, 1.06E-01, 7.14E-02],
         [5.62E+00, 3.46E+00, 1.96E+00, 1.13E+00, 5.89E-01, 4.12E-01, 2.48E-01, 1.49E-01, 1.13E-01],
         [5.62E+00, 3.46E+00, 1.98E+00, 1.18E+00, 6.67E-01, 5.06E-01, 3.57E-01, 2.66E-01, 2.31E-01],
         [5.63E+00, 3.47E+00, 2.01E+00, 1.24E+00, 7.80E-01, 6.42E-01, 5.17E-01, 4.45E-01, 4.19E-01],
         [5.63E+00, 3.49E+00, 2.06E+00, 1.35E+00, 9.54E-01, 8.50E-01, 7.63E-01, 7.18E-01, 7.03E-01],
         [5.63E+00, 3.51E+00, 2.13E+00, 1.50E+00, 1.20E+00, 1.13E+00, 1.08E+00, 1.06E+00, 1.05E+00],
         [5.64E+00, 3.56E+00, 2.31E+00, 1.85E+00, 1.68E+00, 1.65E+00, 1.63E+00, 9.99E+02, 9.99E+02],
         [5.65E+00, 3.63E+00, 2.55E+00, 2.23E+00, 2.15E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.67E+00, 3.74E+00, 2.86E+00, 2.68E+00, 2.65E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.70E+00, 3.90E+00, 3.24E+00, 3.15E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.76E+00, 4.22E+00, 3.85E+00, 3.82E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.85E+00, 4.58E+00, 4.38E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.99E+00, 5.00E+00, 4.91E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [6.16E+00, 5.46E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [6.47E+00, 6.11E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [6.60E+00, 6.50E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02]]

w_u_b = np.array(w_u_b)

# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

MD_DIR  = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/md")
CSS_DIR = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/css")

load_css(CSS_DIR, "segment_control_Theis_Deriv_Ini.css")

#st.title("Pumping test evaluation with :blue[Drawdown Derivatives]")
st.header("Understanding :violet[**Drawdown Derivatives**] with the :violet[**Neuman**] model for :violet[**unconfined aquifers**]", divider = 'violet')

# --------------------------------------------------
# Orientation/Explanation
# --------------------------------------------------
st.markdown(load_md(MD_DIR, "neuman_deriv_01.md", st.session_state.language))
# --------------------------------------------------
# Orientation/Explanation
# --------------------------------------------------
st.subheader("Introduction", divider="violet")

st.markdown(load_md(MD_DIR, "neuman_deriv_02.md", st.session_state.language))

#st.markdown(
#    """
#    This section introduces drawdown derivatives as a diagnostic tool for pumping test evaluation. The starting point is the Neuman solution for transient radial flow to a pumping well in an unconfined aquifer. The solution accounts for delayed drainage from the water table and therefore produces diagnostic curve shapes that differ from the classical Theis response.
#    
#    In addition to the drawdown curve, the app shows the drawdown derivative with respect to the natural logarithm of time. The derivative highlights changes in curve slope and helps identify characteristic flow regimes more clearly than the drawdown curve alone.
#"""
#)

left_co, cent_co, last_co = st.columns((20, 60, 20))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/Neuman_Deriv_01.png",
        caption=(
            "Drawdown and derivatives for the Neuman function."
        ),
    )


# --------------------------------------------------
# Initial assessment
# --------------------------------------------------

st.markdown(load_md(MD_DIR, "neuman_deriv_03.md", st.session_state.language))

with st.expander(":green[**Show/Hide the initial assessment**]"):
    st.write('Show the initial assessment')


# --------------------------------------------------
# Theory
# --------------------------------------------------
st.subheader(
    "Underlying Theory - :violet[Neuman] Solution and :violet[Drawdown Derivatives]", divider="violet")

st.markdown(load_md(MD_DIR, "neuman_deriv_04.md", st.session_state.language))

# st.markdown(
#     """
# The Neuman solution describes transient flow to a pumping well in an unconfined
# aquifer. In contrast to the Theis solution for confined aquifers, the Neuman
# solution accounts for delayed drainage from the water table.
# 
# At early time, drawdown is mainly controlled by elastic storage, similar to the
# response of a confined aquifer. At later time, drainage from the water table
# becomes important and the response is increasingly controlled by specific yield.
# 
# In this app, the Neuman drawdown curve is represented by an early-time and a
# late-time branch. The drawdown derivative is computed numerically with respect
# to the natural logarithm of time:
# 
# $$
# \\frac{\\partial s}{\\partial \\ln(t)}
# $$
# 
# The derivative emphasizes changes in the slope of the drawdown curve and helps
# identify the transition from elastic storage response to delayed water-table
# drainage.
# """
# )




# --------------------------------------------------
# Interactive inverse function
# --------------------------------------------------
@st.fragment
def inverse_neuman(v):
    """
    Plot Neuman drawdown curves and, optionally, drawdown derivatives.

    Versions
    --------
    v = 1:
        One Neuman curve with user-defined T, Ss, Sy, and beta.

    v = 2:
        Fixed Ss, Sy, and beta; three user-defined T variants.

    v = 3:
        Fixed T, Ss, and beta; three user-defined Sy variants.

    v = 4:
        Fixed T, Ss, and Sy; three user-defined beta variants.

    This function is intended for diagnostic plots for unconfined aquifers
    with delayed water-table response.
    """

    # --------------------------------------------------
    # Basic hydraulic setup
    # --------------------------------------------------
    r = 100.0
    b = 10.0
    Qs = 0.1 / 60.0

    log_min_T = -7.0
    log_max_T = 0.0

    log_min_Ss = -8.0
    log_max_Ss = -1.0

    Sy_min = 0.01
    Sy_max = 0.50

    beta_labels = ["0.001", "0.01", "0.06", "0.2", "0.6", "1", "2", "4", "6"]
    
    number_input = st.toggle("Use number input instead of sliders", key=f"neu_number_input_{v}")

    # --------------------------------------------------
    # Input widgets in three columns
    # --------------------------------------------------
    col_1, col_2, col_3 = st.columns((1, 1, 1), gap="medium")

    # --------------------------------------------------
    # General plot controls
    # --------------------------------------------------
    with col_1:
        with st.expander(":red[**Plot settings**]"):

            show_drawdown = st.toggle(
                "Show Neuman drawdown",
                value=True,
                key=f"neu_show_drawdown_{v}",
            )
    
            show_derivative = st.toggle(
                "Show drawdown derivative",
                value=False,
                key=f"neu_show_derivative_{v}",
            )
    
            semilog = st.toggle(
                "Toggle for **semi-log graph**",
                key=f"neu_semilog_{v}",
            )

        if show_derivative:
            log_smoothing_factor = st.slider(
                "Drawdown-curve smoothing strength",
                min_value=-5.0,
                max_value=-1.0,
                value=-4.5,
                step=0.25,
                key=f"neu_derivative_smoothing_{v}",
                help="Use smaller values for closer fit to the table, larger values for a smoother drawdown curve before Bourdet differentiation.",
            )

            smoothing_factor = 10 ** log_smoothing_factor

            bourdet_L = st.slider(
                "Bourdet derivative window L [log cycles]",
                min_value=0.10,
                max_value=2.00,
                value=1.00,
                step=0.05,
                key=f"neu_bourdet_L_{v}",
                help="L is the total derivative window in log10 time. L = 1 means one full log cycle, with support points at ±0.5 log cycles around each evaluated time.",
            )

            st.caption(
                f"Smoothing factor: {smoothing_factor:.1e}; "
                f"Bourdet L: {bourdet_L:.2f} log cycles"
            )
        else:
            smoothing_factor = 1e-3
            bourdet_L = 1.0

    # --------------------------------------------------
    # Small helper for repeated log input widgets
    # --------------------------------------------------
    def log_widget(label, min_value, max_value, default, suffix, parameter="T"):
        """
        Render a synchronized log-parameter widget.

        parameter="T" uses update_T(); parameter="S" uses update_S().
        The suffix keeps keys unique across tabs and parameter variants.
        """

        if parameter == "T":
            slider_key, input_key = prepare_synced_widget_keys(
                "T", suffix, default, number_input
            )
            update_function = update_T
        else:
            slider_key, input_key = prepare_synced_widget_keys(
                "S", suffix, default, number_input
            )
            update_function = update_S

        if number_input:
            value = st.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                step=0.01,
                format="%4.2f",
                key=input_key,
                on_change=update_function,
                args=(suffix,),
            )
        else:
            value = st.slider(
                label,
                min_value=min_value,
                max_value=max_value,
                step=0.01,
                format="%4.2f",
                key=slider_key,
            )

        return value

    def linear_widget(label, min_value, max_value, default, step, suffix):
        """Render a synchronized linear storage widget using update_S()."""

        slider_key, input_key = prepare_synced_widget_keys(
            "S", suffix, default, number_input
        )

        if number_input:
            value = st.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                step=step,
                format="%4.2f",
                key=input_key,
                on_change=update_S,
                args=(suffix,),
            )
        else:
            value = st.slider(
                label,
                min_value=min_value,
                max_value=max_value,
                step=step,
                format="%4.2f",
                key=slider_key,
            )

        return value

    # --------------------------------------------------
    # Version-specific parameter input
    # --------------------------------------------------
    parameter_sets = []

    # --------------------------------------------------
    # Version 1:
    # One freely adjustable Neuman parameter set
    # --------------------------------------------------
    if v == 1:
        with col_2:
            with st.expander(":blue[**Transmissivity**]"):

                log_T = log_widget(
                    "_(log of) Transmissivity in m²/s_",
                    log_min_T,
                    log_max_T,
                    -3.0,
                    f"neu_T_{v}",
                )
    
                T = 10 ** log_T
                st.write("**T:** %5.2e m²/s" % T)

        with col_3:
            with st.expander(":green[**Storativity**]"):

                log_Ss = log_widget(
                    "_(log of) Specific storage in 1/m_",
                    log_min_Ss,
                    log_max_Ss,
                    -5.0,
                    f"neu_Ss_{v}",
                    parameter="S",
                )
    
                Ss = 10 ** log_Ss
                st.write("**Ss:** %5.2e 1/m" % Ss)
    
                Sy = linear_widget(
                    "_Specific yield Sy_",
                    Sy_min,
                    Sy_max,
                    0.20,
                    0.01,
                    f"neu_Sy_{v}",
                )
    
                st.write("**Sy:** %4.2f" % Sy)

        parameter_sets.append(
            {
                "label": "Neuman",
                "T": T,
                "Ss": Ss,
                "Sy": Sy,
            }
        )

    # --------------------------------------------------
    # Version 2:
    # Fixed storage parameters, three T variants
    # --------------------------------------------------
    elif v == 2:
        with col_2:
            with st.expander(":blue[**Transmissivity**]"):

                default_log_T_values = [-2.5, -3.0, -3.5]
    
                for i, default_log_T in enumerate(default_log_T_values, start=1):
    
                    log_T_i = log_widget(
                        f"_(log of) T variant {i} in m²/s_",
                        log_min_T,
                        log_max_T,
                        default_log_T,
                        f"neu_T_variant_{v}_{i}",
                    )
    
                    T_i = 10 ** log_T_i
                    st.write(f"**T{i}:** {T_i:5.2e} m²/s")
    
                    parameter_sets.append(
                        {
                            "label": f"$T_{i}$ = {T_i:.1e} m²/s",
                            "T": T_i,
                            "Ss": None,
                            "Sy": None,
                        }
                    )

        with col_3:
            with st.expander("fixed :green[**Storativity**]"):

                log_Ss_fixed = log_widget(
                    "_Fixed (log of) Specific storage in 1/m_",
                    log_min_Ss,
                    log_max_Ss,
                    -5.0,
                    f"neu_Ss_fixed_{v}",
                    parameter="S",
                )
    
                Ss_fixed = 10 ** log_Ss_fixed
                st.write("**Fixed Ss:** %5.2e 1/m" % Ss_fixed)
    
                Sy_fixed = linear_widget(
                    "_Fixed specific yield Sy_",
                    Sy_min,
                    Sy_max,
                    0.20,
                    0.01,
                    f"neu_Sy_fixed_{v}",
                )
    
                st.write("**Fixed Sy:** %4.2f" % Sy_fixed)

        for par in parameter_sets:
            par["Ss"] = Ss_fixed
            par["Sy"] = Sy_fixed
            par["label"] = f"{par['label']}, fixed $S_s$, $S_y$"

    # --------------------------------------------------
    # Version 3:
    # Fixed T and Ss, three Sy variants
    # --------------------------------------------------
    elif v == 3:
        with col_2:
            with st.expander("fixed :blue[**Transmissivity**]"):

                log_T_fixed = log_widget(
                    "_Fixed (log of) Transmissivity in m²/s_",
                    log_min_T,
                    log_max_T,
                    -3.0,
                    f"neu_T_fixed_{v}",
                )
    
                T_fixed = 10 ** log_T_fixed
                st.write("**Fixed T:** %5.2e m²/s" % T_fixed)

        with col_3:
            with st.expander(":green[**Storativity**]"):

                log_Ss_fixed = log_widget(
                    "_Fixed (log of) Specific storage in 1/m_",
                    log_min_Ss,
                    log_max_Ss,
                    -5.0,
                    f"neu_Ss_fixed_{v}",
                    parameter="S",
                )
    
                Ss_fixed = 10 ** log_Ss_fixed
                st.write("**Fixed Ss:** %5.2e 1/m" % Ss_fixed)
    
                default_Sy_values = [0.15, 0.20, 0.25]
    
                for i, default_Sy in enumerate(default_Sy_values, start=1):
    
                    Sy_i = linear_widget(
                        f"_Specific yield variant {i}_",
                        Sy_min,
                        Sy_max,
                        default_Sy,
                        0.01,
                        f"neu_Sy_variant_{v}_{i}",
                    )
    
                    st.write(f"**Sy{i}:** {Sy_i:4.2f}")
    
                    parameter_sets.append(
                        {
                            "label": rf"fixed $T$; $S_y$ variant {i} = {Sy_i:.2f}",
                            "T": T_fixed,
                            "Ss": Ss_fixed,
                            "Sy": Sy_i,
                        }
                    )

    # --------------------------------------------------
    # Version 4:
    # Fixed T, Ss, and Sy; three beta variants
    # --------------------------------------------------
    elif v == 4:
        with col_2:
            with st.expander(":blue[**Transmissivity**]"):

                log_T_fixed = log_widget(
                    "_Fixed (log of) Transmissivity in m²/s_",
                    log_min_T,
                    log_max_T,
                    -3.0,
                    f"neu_T_fixed_{v}",
                )
    
                T_fixed = 10 ** log_T_fixed
                st.write("**Fixed T:** %5.2e m²/s" % T_fixed)
    
        with col_3:
            with st.expander(":green[**Storativity**]"):

                log_Ss_fixed = log_widget(
                    "_Fixed (log of) Specific storage in 1/m_",
                    log_min_Ss,
                    log_max_Ss,
                    -5.0,
                    f"neu_Ss_fixed_{v}",
                    parameter="S",
                )
    
                Ss_fixed = 10 ** log_Ss_fixed
                st.write("**Fixed Ss:** %5.2e 1/m" % Ss_fixed)
    
                Sy_fixed = linear_widget(
                    "_Fixed specific yield Sy_",
                    Sy_min,
                    Sy_max,
                    0.20,
                    0.01,
                    f"neu_Sy_fixed_{v}",
                )
    
                st.write("**Fixed Sy:** %4.2f" % Sy_fixed)

    else:
        st.error("Unknown version. Please use v = 1, 2, 3, or 4.")
        return

    with col_2:
        with st.expander("$\\beta$"):
            beta_variant_indices = []
    
            if v == 4:
                default_beta_indices = [1, 3, 5]
            
                for i, default_idx in enumerate(default_beta_indices, start=1):
                    beta_i = st.selectbox(
                        rf"Neuman $\beta$ variant {i}",
                        beta_labels,
                        index=default_idx,
                        key=f"neu_beta_variant_{v}_{i}",
                    )
            
                    beta_idx = beta_labels.index(beta_i)
            
                    parameter_sets.append(
                        {
                            "label": rf"fixed $T$, $S_s$, $S_y$; $\beta_{i}$ = {beta_i}",
                            "T": T_fixed,
                            "Ss": Ss_fixed,
                            "Sy": Sy_fixed,
                            "beta_index": beta_idx,
                            "beta_label": beta_i,
                        }
                    )
            
                beta_choice = "variable"
                beta_index = None
    
            else:
                beta_choice = st.selectbox(
                    r"Neuman $\beta$",
                    beta_labels,
                    index=3,
                    key=f"neu_beta_{v}",
                )
    
                beta_index = beta_labels.index(beta_choice)
    
            show_table_points = st.toggle(
                "Show original tabular Neuman data",
                value=False,
                key=f"neu_show_table_points_{v}",
            )

    # --------------------------------------------------
    # Stop if nothing should be shown
    # --------------------------------------------------
    if not show_drawdown and not show_derivative:
        st.info("Select at least one plot option: Neuman drawdown or drawdown derivative.")
        return

    # --------------------------------------------------
    # Plot
    # --------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

    drawdown_handles = []
    drawdown_labels = []

    derivative_handles = []
    derivative_labels = []

    plateau_handle = None
    plateau_label = "late-time derivative plateau reference"

    # --------------------------------------------------
    # Calculation and plotting loop
    # --------------------------------------------------
    for par in parameter_sets:

        T = par["T"]
        Ss = par["Ss"]
        Sy = par["Sy"]
        label = par["label"]
        beta_index_plot = par.get("beta_index", beta_index)
        beta_choice_plot = par.get("beta_label", beta_choice)

        # --------------------------------------------------
        # Original Neuman table branches only
        # --------------------------------------------------
        t_a, s_a, t_b, s_b = neuman_branch_curve(
            T=T,
            Ss=Ss,
            Sy=Sy,
            beta_index=beta_index_plot,
            r=r,
            b=b,
            Qs=Qs,
            u_inv_a=u_inv_a,
            u_inv_b=u_inv_b,
            w_u_a=w_u_a,
            w_u_b=w_u_b,
        )
        
        # Sort branches
        sort_a = np.argsort(t_a)
        sort_b = np.argsort(t_b)
        
        t_a = np.asarray(t_a)[sort_a]
        s_a = np.asarray(s_a)[sort_a]
        
        t_b = np.asarray(t_b)[sort_b]
        s_b = np.asarray(s_b)[sort_b]

        # --------------------------------------------------
        # Combined Neuman curve
        # --------------------------------------------------
        t_neu, s_neu, source_neu, transition_time = neuman_combined_curve(
            T=T,
            Ss=Ss,
            Sy=Sy,
            beta_index=beta_index_plot,
            r=r,
            b=b,
            Qs=Qs,
            u_inv_a=u_inv_a,
            u_inv_b=u_inv_b,
            w_u_a=w_u_a,
            w_u_b=w_u_b,
        )
        
        # --------------------------------------------------
        # Smooth combined Neuman curve and compute Bourdet derivative
        # from the smoothed curve.
        # --------------------------------------------------
        t_neu_smooth, s_neu_smooth = smooth_loglog_curve(
            t_neu,
            s_neu,
            n_dense=400,
            smoothing_factor=smoothing_factor,
        )

        derivative_time, derivative = bourdet_derivative_logcycle(
            t_neu_smooth,
            s_neu_smooth,
            L=bourdet_L,
        )

        # This is not a true Neuman plateau; it is a late-time Theis-type reference
        plateau_d = Qs / (4.0 * np.pi * T)

        # --------------------------------------------------
        # Plot drawdown
        # --------------------------------------------------
        line = None

        if show_drawdown:     
            if show_table_points:
                line, = ax.plot(
                    t_a,
                    s_a,
                    marker="o",
                    linestyle="none",
                    markersize=5,
                    markerfacecolor="none",
                    alpha=0.85,
                    label="_nolegend_",
                )
                
                color = line.get_color()
                
                ax.plot(
                    t_b,
                    s_b,
                    marker="o",
                    linestyle="none",
                    markersize=5,
                    markerfacecolor="none",
                    markeredgecolor='green',
                    color='green',
                    alpha=0.85,
                    label="_nolegend_",
                )
        
            # Smoothed Neuman curve
            line, = ax.plot(
                t_neu_smooth,
                s_neu_smooth,
                linewidth=1,
                label="_nolegend_",
            )
            
            color = line.get_color()
            
            # Original tabular / combined Neuman points
#            ax.plot(
#                t_neu,
#                s_neu,
#                "o",
#                markersize=4,
#                markerfacecolor="none",
#                markeredgecolor=color,
#                alpha=0.45,
#                linestyle="none",
#                label="_nolegend_",
#            )
        
            color = line.get_color()
        
            drawdown_handles.append(line)
            drawdown_labels.append(f"Drawdown: {label}")

        # --------------------------------------------------
        # Plot derivative
        # --------------------------------------------------
        if show_derivative:

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
            derivative_labels.append(rf"Derivative $ds/d\ln(t)$: {label}")

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
        
        if show_drawdown and len(transition_time) > 0:
            ax.axvline(
                transition_time[0],
                linestyle=":",
                linewidth=1.0,
                color=color,
                alpha=0.5,
                label="_nolegend_",
            )
    # --------------------------------------------------
    # Axes
    # --------------------------------------------------
    ax.set_xscale("log")

    if not semilog:
        ax.set_yscale("log")

    if semilog:
        ax.axis([1e0, 1e8, 0, 10])
    else:
        ax.axis([1e0, 1e8, 1e-4, 1e1])

    ax.grid(which="both", alpha=0.5)

    ax.set_xlabel("time t in s", fontsize=14)

    if show_drawdown and show_derivative:
        ax.set_ylabel(r"drawdown $s$ and derivative $ds/d\ln(t)$ in m", fontsize=14)
        title_beta = "variable beta" if v == 4 else rf"$\beta$ = {beta_choice}"
        ax.set_title(rf"Neuman drawdown and derivative, {title_beta}", fontsize=16)
    elif show_derivative:
        ax.set_ylabel(r"drawdown derivative $ds/d\ln(t)$ in m", fontsize=14)
        title_beta = "variable beta" if v == 4 else rf"$\beta$ = {beta_choice}"
        ax.set_title(rf"Neuman drawdown derivative, {title_beta}", fontsize=16)
    else:
        ax.set_ylabel("drawdown s in m", fontsize=14)
        title_beta = "variable beta" if v == 4 else rf"$\beta$ = {beta_choice}"
        ax.set_title(rf"Neuman drawdown, {title_beta}", fontsize=16)

    # --------------------------------------------------
    # Legend: first drawdown curves, then derivatives, then plateau reference
    # --------------------------------------------------
    legend_handles = []
    legend_labels = []

    if show_drawdown:
        legend_handles.extend(drawdown_handles)
        legend_labels.extend(drawdown_labels)

    if show_derivative:
        legend_handles.extend(derivative_handles)
        legend_labels.extend(derivative_labels)

        if plateau_handle is not None:
            legend_handles.append(plateau_handle)
            legend_labels.append(plateau_label)

    ax.legend(
        legend_handles,
        legend_labels,
        fontsize=10,
    )

    # --------------------------------------------------
    # Parameter box
    # --------------------------------------------------
    if v == 1:

        T = parameter_sets[0]["T"]
        Ss = parameter_sets[0]["Ss"]
        Sy = parameter_sets[0]["Sy"]
        Sa = Ss * b

        out_txt = "\n".join(
            (
                r"$T$ (m²/s) = %10.2E" % (T,),
                r"$S_s$ (1/m) = %10.2E" % (Ss,),
                r"$S_a = S_s b$ (-) = %10.2E" % (Sa,),
                r"$S_y$ (-) = %4.2f" % (Sy,),
                rf"$\beta$ = {beta_choice}",
            )
        )

    elif v == 2:

        Ss_fixed = parameter_sets[0]["Ss"]
        Sy_fixed = parameter_sets[0]["Sy"]

        out_txt = "\n".join(
            (
                r"Fixed $S_s$ (1/m) = %10.2E" % (Ss_fixed,),
                r"Fixed $S_y$ (-) = %4.2f" % (Sy_fixed,),
                rf"$\beta$ = {beta_choice}",
                r"$T$ controls vertical position",
                r"and derivative level.",
            )
        )

    elif v == 3:

        T_fixed = parameter_sets[0]["T"]
        Ss_fixed = parameter_sets[0]["Ss"]

        out_txt = "\n".join(
            (
                r"Fixed $T$ (m²/s) = %10.2E" % (T_fixed,),
                r"Fixed $S_s$ (1/m) = %10.2E" % (Ss_fixed,),
                rf"$\beta$ = {beta_choice}",
                r"$S_y$ controls late-time response",
                r"and delayed drainage.",
            )
        )

    elif v == 4:

        T_fixed = parameter_sets[0]["T"]
        Ss_fixed = parameter_sets[0]["Ss"]
        Sy_fixed = parameter_sets[0]["Sy"]

        out_txt = "\n".join(
            (
                r"Fixed $T$ (m²/s) = %10.2E" % (T_fixed,),
                r"Fixed $S_s$ (1/m) = %10.2E" % (Ss_fixed,),
                r"Fixed $S_y$ (-) = %4.2f" % (Sy_fixed,),
                r"$\beta$ controls delayed drainage shape",
                r"and transition behavior.",
            )
        )

    if semilog:
        ax.text(
            0.97,
            0.95,
            out_txt,
            horizontalalignment="right",
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=props,
        )
    else:
        ax.text(
            0.97,
            0.25,
            out_txt,
            horizontalalignment="right",
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=props,
        )

    fig.tight_layout()
    st.pyplot(fig)

# --------------------------------------------------
# First interactive plot
# --------------------------------------------------
st.subheader(
    ":violet[Explore delayed water-table response with the Neuman solution]",
    divider="violet",
)

st.markdown(load_md(MD_DIR, "neuman_deriv_05.md", st.session_state.language))

active_tab = st.segmented_control(
    "Select topic",
    options=[
        "01: Single Neuman curve",
        "02: Effect of transmissivity",
        "03: Effect of specific yield",
        "04: Effect of beta",
    ],
    default="01: Single Neuman curve",
    label_visibility="collapsed",
)

if active_tab is None:
    st.info("Please select one topic to continue.")
    st.stop()

if active_tab.startswith("01"):
    inverse_neuman(1)
    st.markdown(load_md(MD_DIR, "neuman_deriv_06.md", st.session_state.language))

elif active_tab.startswith("02"):
    inverse_neuman(2)
    st.markdown(load_md(MD_DIR, "neuman_deriv_07.md", st.session_state.language))

elif active_tab.startswith("03"):
    inverse_neuman(3)
    st.markdown(load_md(MD_DIR, "neuman_deriv_08.md", st.session_state.language))

elif active_tab.startswith("04"):
    inverse_neuman(4)
    st.markdown(load_md(MD_DIR, "neuman_deriv_09.md", st.session_state.language))

#st.markdown(
#    """
#Use the sliders to explore how transmissivity, specific storage, specific yield,
#and the Neuman beta parameter influence drawdown and drawdown derivatives in an
#unconfined aquifer.
#
#Compared with the Theis solution for confined aquifers, the Neuman solution can
#show a delayed water-table response. This delayed response is often visible as
#a flattening or transition zone in the drawdown curve and as a characteristic
#change in the derivative curve.
#
#The derivative plot is especially useful because it highlights changes in flow
#regime that may be difficult to recognize from drawdown alone. In this app,
#the derivative is computed from the smoothed combined Neuman curve using the
#Bourdet method with a user-defined log-cycle window L. In this app, L = 1 corresponds to one full logarithmic time cycle.
#"""
#)

# --------------------------------------------------
# References
# --------------------------------------------------
with st.expander("**Click here for references**"):
    st.markdown(load_md(MD_DIR, "neuman_deriv_ref.md", st.session_state.language))

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
