# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import math
import streamlit as st
import streamlit_book as stb

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
# Streamlit page
# --------------------------------------------------
st.title("The :red[Theis] base model and drawdown derivatives")

st.header("Basic introduction", divider="red")

st.markdown(
    """
This section uses the Theis solution for drawdown in response to pumping a
:red[confined aquifer] to estimate transmissivity and storativity.

In addition to the drawdown curve, the app also shows the **drawdown derivative**
with respect to the natural logarithm of time.
"""
)

st.subheader(":red-background[Introduction]", divider="red")

st.markdown(
    """
...
"""
)

left_co, cent_co, last_co = st.columns((20, 60, 20))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png",
        caption=(
            "Caption"
        ),
    )


# --------------------------------------------------
# Initial assessment
# --------------------------------------------------
st.markdown(
    """
Before investigating the Theis solution and its derivative, it is useful to think
about the questions provided in this initial assessment.
"""
)

with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1, 1))

    with columnsQ1[0]:
        stb.single_choice(
            ":orange[**What conditions are appropriate for use of the Theis Solution?**]",
            [
                "Steady state flow, confined aquifer.",
                "Transient flow, confined aquifer",
                "Steady state flow, semiconfined aquifer",
                "Transient flow, semiconfined aquifer",
                "Steady state flow, unconfined aquifer",
                "Transient flow, unconfined aquifer",
            ],
            1,
            success="CORRECT! Theis is designed for transient flow in a fully confined aquifer.",
            error="This is not correct. Feel free to answer again.",
        )

        stb.single_choice(
            ":orange[**How does storativity $S$ influence the response of an aquifer to pumping?**]",
            [
                "A higher storativity results in a slower drawdown response",
                "A higher storativity leads to more rapid flow to the well",
                "Storativity only affects steady-state conditions",
                "Storativity is not relevant for confined aquifers",
            ],
            0,
            success=(
                "CORRECT! A higher storativity results in a slower drawdown response, "
                "because more water must be removed for an equivalent decline in head."
            ),
            error="This is not correct. Feel free to answer again.",
        )

    with columnsQ1[1]:
        stb.single_choice(
            ":orange[**How does the drawdown change at one specific place and time if the transmissivity is increased?**]",
            [
                "The drawdown is less",
                "The drawdown is more",
                "The drawdown is not affected",
                "All of the above depending on the parameter values",
            ],
            3,
            success=(
                "CORRECT! When all else is equal, a higher transmissivity produces "
                "a broader cone of depression that is not as deep near the well."
            ),
            error="This is not completely correct. Try exploring this with the interactive plot.",
        )

        stb.single_choice(
            ":orange[**Which assumption was made in the development of the Theis solution?**]",
            [
                "The aquifer has variable thickness",
                "The aquifer is confined and infinite in lateral extent",
                "The well fully penetrates an unconfined aquifer",
                "The pumping rate varies with time",
            ],
            1,
            success="CORRECT! The aquifer is confined and infinite in lateral extent.",
            error="This is not correct. Feel free to answer again.",
        )


# --------------------------------------------------
# Theory
# --------------------------------------------------
st.subheader(
    ":red-background[Underlying Theory] - Theis Solution and Drawdown Derivatives",
    divider="red",
)

st.markdown(
    """
The Theis solution describes transient radial flow to a well pumping at a
constant rate $Q$ in a confined aquifer.

The drawdown is:

$$
s(r,t) = \\frac{Q}{4\\pi T} W(u)
$$

with

$$
u = \\frac{r^2 S}{4 T t}
$$

The derivative of drawdown with respect to the natural logarithm of time is:

$$
\\frac{\\partial s}{\\partial \\ln(t)}
=
t \\frac{\\partial s}{\\partial t}
=
\\frac{Q}{4\\pi T} e^{-u}
$$

For late time, $u$ becomes small and $e^{-u}$ approaches 1. Therefore, the
derivative approaches the plateau:

$$
d = \\frac{Q}{4\\pi T}
$$

This relationship is useful because the plateau value directly depends on
transmissivity.
"""
)


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


def update_T(v):
    st.session_state[f"T_slider_value_{v}"] = st.session_state[f"T_input_{v}"]


def update_S(v):
    st.session_state[f"S_slider_value_{v}"] = st.session_state[f"S_input_{v}"]


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
    Viterbo = False
    Varnum = False
    
    if v == 2:
        Viterbo = True
    if v == 3:
        Varnum = True

    # --------------------------------------------------
    # Data sets
    # --------------------------------------------------
    m_time = [
        1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10,
        12, 14, 18, 24, 30, 40, 50, 60, 100, 120,
    ]

    m_ddown = [
        0.66, 0.87, 0.99, 1.11, 1.21, 1.36, 1.49, 1.59, 1.75, 1.86,
        1.97, 2.08, 2.20, 2.36, 2.49, 2.65, 2.78, 2.88, 3.16, 3.28,
    ]

    r = 120
    b = 8.5
    Qs = 0.3 / 60
    Qd = Qs * 60 * 60 * 24

    if Viterbo:
        m_time = [
            1, 1.416666667, 2.166666667, 2.5, 2.916666667,
            3.566666667, 3.916666667, 4.416666667, 4.833333333,
            5.633333333, 6.516666667, 7.5, 8.916666667,
            10.13333333, 11.16666667, 12.6, 16.5, 18.53333333,
            22.83333333, 27.15, 34.71666667, 39.91666667,
            48.21666667, 60.4, 72.66666667, 81.91666667,
            94.66666667, 114.7166667, 123.5,
        ]

        m_ddown = [
            0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285,
            0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415,
            0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525,
            0.53, 0.56, 0.57, 0.58,
        ]

        r = 21
        b = 13
        Qs = 11.16 / 3600
        Qd = Qs * 60 * 60 * 24

    if Varnum:
        m_time = list(range(1, 326))

        m_ddown = [
            2E-05, 0.02022, 0.04591, 0.0716, 0.09342, 0.11433,
            0.12882, 0.14332, 0.15139, 0.16313, 0.17396, 0.18203,
            0.18827, 0.1936, 0.19878, 0.2012, 0.20729, 0.21247,
            0.21489, 0.22007, 0.22249, 0.22583, 0.22826, 0.23068,
            0.23358, 0.23648, 0.23938, 0.24228, 0.24243, 0.24533,
            0.24915, 0.2493, 0.2522, 0.25235, 0.2551, 0.2551,
            0.25785, 0.25785, 0.2606, 0.2606, 0.26335, 0.26335,
            0.2661, 0.2661, 0.26597, 0.26585, 0.26847, 0.2656,
            0.26822, 0.27177, 0.26797, 0.27152, 0.27139, 0.27402,
            0.27397, 0.27392, 0.27387, 0.27382, 0.27652, 0.27647,
            0.27642, 0.27637, 0.27907, 0.27627, 0.27614, 0.27877,
            0.27589, 0.27577, 0.27839, 0.27735, 0.27814, 0.2771,
            0.28064, 0.2796, 0.27712, 0.2774, 0.28042, 0.27795,
            0.27822, 0.2785, 0.28152, 0.27905, 0.28207, 0.28235,
            0.28307, 0.28012, 0.28175, 0.2843, 0.2841, 0.28482,
            0.28462, 0.28442, 0.28422, 0.28402, 0.28404, 0.28407,
            0.28684, 0.28412, 0.28689, 0.28692, 0.28694, 0.28422,
            0.28699, 0.28702, 0.28717, 0.28732, 0.28747, 0.28762,
            0.28777, 0.28792, 0.28807, 0.28822, 0.28837, 0.28852,
            0.29144, 0.28887, 0.29179, 0.28922, 0.28939, 0.28957,
            0.28974, 0.28992, 0.29009, 0.29027, 0.28994, 0.29237,
            0.28929, 0.29172, 0.29139, 0.29107, 0.29074, 0.29042,
            0.29009, 0.28977, 0.28974, 0.28972, 0.28969, 0.29333,
            0.28964, 0.28687, 0.28959, 0.29323, 0.28954, 0.28952,
            0.29336, 0.29353, 0.29371, 0.29022, 0.29406, 0.29423,
            0.29441, 0.29458, 0.29109, 0.29493, 0.29488, 0.29483,
            0.29478, 0.29473, 0.29468, 0.29463, 0.29458, 0.29453,
            0.29723, 0.29718, 0.29443, 0.29443, 0.29443, 0.29443,
            0.29443, 0.29718, 0.29443, 0.29443, 0.29443, 0.29718,
            0.29701, 0.29683, 0.29666, 0.29648, 0.29631, 0.29613,
            0.29596, 0.29578, 0.29561, 0.29543, 0.29561, 0.29853,
            0.29596, 0.29613, 0.29631, 0.29648, 0.29666, 0.29683,
            0.29701, 0.29993, 0.29688, 0.29658, 0.29628, 0.29598,
            0.29568, 0.29538, 0.29508, 0.29478, 0.29723, 0.29693,
            0.29418, 0.29418, 0.29418, 0.29418, 0.29693, 0.29693,
            0.29418, 0.29418, 0.29693, 0.29418, 0.29433, 0.29723,
            0.29738, 0.29478, 0.29768, 0.29783, 0.29798, 0.29813,
            0.29828, 0.29843, 0.29838, 0.29833, 0.29828, 0.29823,
            0.29818, 0.29813, 0.29808, 0.29803, 0.29798, 0.29793,
            0.29796, 0.29798, 0.29801, 0.29803, 0.30081, 0.30083,
            0.29811, 0.29813, 0.29816, 0.30093, 0.29853, 0.29888,
            0.29923, 0.29958, 0.29993, 0.30303, 0.30338, 0.30098,
            0.30133, 0.30168, 0.30408, 0.30098, 0.30063, 0.30303,
            0.29993, 0.30233, 0.29923, 0.29888, 0.29853, 0.29818,
            0.30113, 0.30133, 0.29878, 0.29898, 0.30193, 0.30213,
            0.30233, 0.30253, 0.30273, 0.30018, 0.30001, 0.30258,
            0.30241, 0.29948, 0.29931, 0.29913, 0.30171, 0.29878,
            0.29861, 0.29843, 0.30133, 0.29873, 0.29888, 0.29903,
            0.29918, 0.29933, 0.29948, 0.29963, 0.30253, 0.29993,
            0.30011, 0.30028, 0.30046, 0.30063, 0.30081, 0.30373,
            0.30391, 0.30133, 0.30151, 0.30443, 0.30151, 0.30133,
            0.30116, 0.30098, 0.30081, 0.30338, 0.30046, 0.30028,
            0.30286, 0.29993, 0.30286, 0.30303, 0.30321, 0.30338,
            0.30356, 0.30373, 0.30391, 0.30408, 0.30426, 0.30443,
            0.30408,
        ]

        r = 38.9
        b = 12
        Qs = 0.01317
        Qd = Qs * 60 * 60 * 24


    if f"T_slider_value_{v}" not in st.session_state:
        st.session_state[f"T_slider_value_{v}"] = -3.0

    if f"S_slider_value_{v}" not in st.session_state:
        st.session_state[f"S_slider_value_{v}"] = -4.0

    log_min1 = -7.0
    log_max1 = 0.0
    log_min2 = -7.0
    log_max2 = 0.0

    number_input = st.toggle(
        "Toggle to use Slider or Number for input of $T$ and $S$",
        key=f"number_input_{v}",
    )

    columns2 = st.columns((1, 1), gap="large")

    with columns2[0]:
        semilog = st.toggle("Toggle for **semi-log drawdown graph**", key=f"semilog_{v}")
        refine_plot = st.toggle("**Zoom in** on the **data in the graph**", key=f"refine_{v}")
        scatter = st.toggle("Show scatter plot", key=f"scatter_{v}")

        show_derivative = st.toggle(
            "Show drawdown derivative plot",
            value=True,
            key=f"show_derivative_{v}",
        )
        
        if show_derivative:
            derivative_method_label = st.selectbox(
                "Derivative method",
                [
                    "Renard et al. (2009)",
                    "Logarithmic difference",
                    "Neighboring points",
                    "Bourdet et al. (1989)",
                    "Spane and Wurstner (1993)",
                ],
                key=f"derivative_method_{v}",
            )
        
            derivative_method_map = {
                "Renard et al. (2009)": "renard2009",
                "Logarithmic difference": "log_difference",
                "Neighboring points": "neighboring_points",
                "Bourdet et al. (1989)": "bourdet1989",
                "Spane and Wurstner (1993)": "spane_wurstner1993",
            }
        
            derivative_method = derivative_method_map[derivative_method_label]
        
            if derivative_method in ["bourdet1989", "spane_wurstner1993"]:
                derivative_L = st.slider(
                    "Differentiation interval L [log cycles]",
                    min_value=0.05,
                    max_value=1.0,
                    value=0.2,
                    step=0.05,
                    key=f"derivative_L_{v}",
                )
                derivative_n_neighbors = 1
        
            elif derivative_method == "neighboring_points":
                derivative_n_neighbors = st.slider(
                    "Number of neighboring points",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key=f"derivative_n_neighbors_{v}",
                )
                derivative_L = 0.2
        
            else:
                derivative_L = 0.2
                derivative_n_neighbors = 1
        
        else:
            derivative_method_label = "Renard et al. (2009)"
            derivative_method = "renard2009"
            derivative_L = 0.2
            derivative_n_neighbors = 1



    with columns2[1]:
        container = st.container()

        if number_input:
            T_slider_value_new = st.number_input(
                "_(log of) Transmissivity in m²/s_",
                log_min1,
                log_max1,
                st.session_state[f"T_slider_value_{v}"],
                0.01,
                format="%4.2f",
                key=f"T_input_{v}",
                on_change=update_T,
                args=(v,),
            )
        else:
            T_slider_value_new = st.slider(
                "_(log of) Transmissivity in m²/s_",
                log_min1,
                log_max1,
                st.session_state[f"T_slider_value_{v}"],
                0.01,
                format="%4.2f",
                key=f"T_input_{v}",
                on_change=update_T,
                args=(v,),
            )

        T = 10**T_slider_value_new
        container.write("**Transmissivity in m²/s:** %5.2e" % T)

        container = st.container()

        if number_input:
            S_slider_value_new = st.number_input(
                "_(log of) Storativity_",
                log_min2,
                log_max2,
                st.session_state[f"S_slider_value_{v}"],
                0.01,
                format="%4.2f",
                key=f"S_input_{v}",
                on_change=update_S,
                args=(v,),
            )
        else:
            S_slider_value_new = st.slider(
                "_(log of) Storativity_",
                log_min2,
                log_max2,
                st.session_state[f"S_slider_value_{v}"],
                0.01,
                format="%4.2f",
                key=f"S_input_{v}",
                on_change=update_S,
                args=(v,),
            )

        S = 10**S_slider_value_new
        container.write("**Storativity dimensionless:** %5.2e" % S)



    # --------------------------------------------------
    # Calculations
    # --------------------------------------------------
    m_time_s = np.asarray(m_time, dtype=float) * 60.0
    m_ddown = np.asarray(m_ddown, dtype=float)

    K = T / b
    SS = S / b

    t_term = r**2 * S / (4.0 * T)
    s_term = Qs / (4.0 * np.pi * T)

    t = u_inv * t_term
    s = w_u * s_term
    
    sort_idx = np.argsort(t)
    t = t[sort_idx]
    s = s[sort_idx]

#    m_ddown_theis = np.asarray(
#        [compute_s(T, S, i, Qs, r) for i in m_time_s]
#    )
    m_ddown_theis = compute_s(T, S, m_time_s, Qs, r)

    # --------------------------------------------------
    # Theis derivative: analytical solution, no smoothing
    # --------------------------------------------------
    derivative_time_theis = t
    derivative_theis = compute_theis_derivative_analytical(
        T,
        S,
        derivative_time_theis,
        Qs,
        r,
    )
    
    # --------------------------------------------------
    # Measured derivative: selected numerical/smoothing method
    # --------------------------------------------------
    derivative_time_meas, derivative_meas = compute_drawdown_derivative(
        m_time_s,
        m_ddown,
        method=derivative_method,
        L=derivative_L,
        n_neighbors=derivative_n_neighbors,
        positive_only=False,
    )
    
    
    plateau_d = Qs / (4.0 * np.pi * T)

    max_s = math.ceil(max(m_ddown) * 10) / 10

    theis_derivative_label = "Theis derivative, analytical"
    if derivative_method in ["bourdet1989", "spane_wurstner1993"]:
        measured_derivative_label = f"measured derivative ({derivative_method_label}, L = {derivative_L:.2f})"
    elif derivative_method == "neighboring_points":
        measured_derivative_label = f"measured derivative ({derivative_method_label}, n = {derivative_n_neighbors})"
    else:
        measured_derivative_label = f"measured derivative ({derivative_method_label})"
    
    # --------------------------------------------------
    # Plot layout
    # --------------------------------------------------
    if scatter:
        fig = plt.figure(figsize=(10, 14))
        ax = fig.add_subplot(2, 1, 1)
    else:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(1, 1, 1)

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

    out_txt = "\n".join(
        (
            r"$T$ (m²/s) = %10.2E" % (T,),
            r"$S$ (-) = %10.2E" % (S,),
            r"$d = Q/(4\pi T)$ = %10.2E m" % (plateau_d,),
        )
    )

    ax.plot(t, s, color = 'black', label="calculated Theis drawdown")

    if Viterbo:
        ax.plot(m_time_s, m_ddown, "go", label="measured drawdown - Viterbo 23")
    elif Varnum:
        ax.plot(m_time_s, m_ddown, "go", label="measured drawdown - Varnum16/R12")
    else:
        ax.plot(m_time_s, m_ddown, "ro", label="measured drawdown - ideal data")

    if show_derivative:
        valid_theis = derivative_theis > 0
        valid_meas = derivative_meas > 0
    
        ax.plot(
            derivative_time_theis[valid_theis],
            derivative_theis[valid_theis],
            "--",
            linewidth=2,
            label=theis_derivative_label,
        )
    
        ax.plot(
            derivative_time_meas[valid_meas],
            derivative_meas[valid_meas],
            "o",
            markersize=4,
            markerfacecolor="none",
            markeredgecolor="blue",
            linestyle="none",
            label=measured_derivative_label,
        )
    
        ax.axhline(
            plateau_d,
            linestyle=":",
            linewidth=2,
            label=r"plateau $d = Q/(4\pi T)$",
        )

    ax.set_xscale("log")

    if not semilog:
        ax.set_yscale("log")

    if refine_plot:
        if semilog:
            ax.axis([1E0, 1E4, 0, 4])
        else:
            ax.axis([1E0, 1E4, 1E-2, 1E1])
    else:
        if semilog:
            ax.axis([1E-1, 1E5, 0, 10])
            ax.text(0.2, 0.8, "Coarse plot - Refine for final fitting")
        else:
            ax.axis([1E-1, 1E5, 1E-4, 1E1])
            ax.text(0.2, 1.8E-4, "Coarse plot - Refine for final fitting")

    ax.grid(which="both", alpha = 0.5)
    ax.set_xlabel("time t in s", fontsize=14)
    ax.set_ylabel("drawdown s in m", fontsize=14)
    ax.set_title("Theis drawdown", fontsize=16)
    ax.legend(fontsize=12)

    if semilog:
        ax.text(
            0.3,
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
            0.15,
            out_txt,
            horizontalalignment="right",
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=props,
        )

    # --------------------------------------------------
    # Scatter plot
    # --------------------------------------------------
    if scatter:
        ax3 = fig.add_subplot(2, 1, 2)

        x45 = [0, 200]
        y45 = [0, 200]

        ax3.plot(x45, y45, "--")

        if Viterbo or Varnum:
            ax3.plot(m_ddown, m_ddown_theis, "go", label="measured")
        else:
            ax3.plot(m_ddown, m_ddown_theis, "ro", label="measured")

        me, mae, rmse = compute_statistics(m_ddown, m_ddown_theis)

        ax3.set_title("Scatter plot", fontsize=16)
        ax3.set_xlabel("Measured s in m", fontsize=14)
        ax3.set_ylabel("Computed s in m", fontsize=14)
        ax3.set_ylim(0, max_s)
        ax3.set_xlim(0, max_s)

        out_txt_scatter = "\n".join(
            (
                r"$ME = %.3f$ m" % (me,),
                r"$MAE = %.3f$ m" % (mae,),
                r"$RMSE = %.3f$ m" % (rmse,),
            )
        )

        ax3.text(
            0.97 * max_s,
            0.05 * max_s,
            out_txt_scatter,
            horizontalalignment="right",
            bbox=dict(boxstyle="square", facecolor="wheat"),
            fontsize=14,
        )

    fig.tight_layout()
    st.pyplot(fig)

    # --------------------------------------------------
    # Submit results
    # --------------------------------------------------
    columns3 = st.columns((1, 10, 1), gap="medium")

    with columns3[1]:
        if st.button(
            ":green[**Submit**] your parameters and **show results**",
            key=f"submit_{v}",
        ):
            st.write("**Parameters and Results**")
            st.write("- Distance of measurement from the well **$r$ = %3i m**" % r)
            st.write("- Pumping rate during test **$Q$ = %5.3f m³/s**" % Qs)
            st.write("- Transmissivity **$T$ = %10.2E m²/s**" % T)
            st.write("- Storativity **$S$ = %10.2E [-]**" % S)
            st.write("- Hydraulic conductivity **$K$ = %10.2E m/s**" % K)
            st.write("- Specific storage **$S_s$ = %10.2E 1/m**" % SS)
            st.write("- Derivative plateau **$d = Q/(4\\pi T)$ = %10.2E m**" % plateau_d)


# --------------------------------------------------
# First interactive plot
# --------------------------------------------------
st.subheader(
    ":red-background[Estimate $T$ and $S$ by matching drawdown and derivative data]",
    divider="red",
)

st.markdown(
    """
Adjust transmissivity and storativity until the calculated Theis drawdown curve
matches the measured data.

The derivative plot provides an additional diagnostic view. For ideal Theis
conditions, the derivative approaches a constant plateau. This plateau indicates
the period of infinite radial flow.
"""
)

inverse(1)

with st.expander("Do with the Viterbo data"):
    st.subheader('Viterbo data')
    inverse(2)

with st.expander("Do with the Varnum data"):
    st.subheader('Varnum data')
    inverse(3)


# --------------------------------------------------
# References
# --------------------------------------------------
with st.expander("**Click here for references**"):
    st.markdown(
        """
[Kruseman, G.P., de Ridder, N.A., & Verweij, J.M., 1991.](https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/)
Analysis and Evaluation of Pumping Test Data, International Institute for Land
Reclamation and Improvement, Wageningen, The Netherlands, 377 pages.

Theis, C.V., 1935. The relation between the lowering of the piezometric surface
and the rate and duration of discharge of a well using groundwater storage,
Transactions of the American Geophysical Union, 16, 519–524.
"""
    )

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