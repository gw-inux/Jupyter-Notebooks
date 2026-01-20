import numpy as np
import matplotlib.pyplot as plt
import math
import streamlit as st

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface
#st.set_page_config(page_title="1D Recharge + No-Flow/Head BC (2-zone K)")

st.title("1D Flow with Recharge: No-Flow (left) + Fixed Head (right)")

# --- Geometry
L1 = 10.0
L2 = 10.0
L = L1 + L2
h_right = 1.0

# -----------------------------------------------------------------------------
# Exercise: parameter ranges for random scenarios
# -----------------------------------------------------------------------------

EX_RANGE = {
    "K1_log10": (-7.0, -5.0),     # log10(K1 [m/s])
    "K2_log10": (-7.0, -5.0),     # log10(K2 [m/s])
    "R_mm_a":   (120.0, 400.0),    # recharge [mm/a]
}

# --- Slider ranges
log_minK, log_maxK = -8.0, -2.0
R_min_mm_a, R_max_mm_a = 0.0, 500.0

# --- Observation points for exercise
x_obs = np.arange(0.0, 20.0 + 1e-9, 2.0)

def mm_a_to_m_s(mm_a: float) -> float:
    return mm_a / 1000.0 / (365.0 * 24.0 * 3600.0)

def head_profile_two_zone_recharge_noflow_head(x, L1, L, K1, K2, R, hR):
    D2 = hR + (R / (2.0 * K2)) * (L ** 2)
    C2 = D2 + (R / 2.0) * (L1 ** 2) * (1.0 / K1 - 1.0 / K2)

    h = np.empty_like(x, dtype=float)
    m1 = x <= L1
    h[m1] = - (R / (2.0 * K1)) * (x[m1] ** 2) + C2
    h[~m1] = - (R / (2.0 * K2)) * (x[~m1] ** 2) + D2
    return h

def _log_uniform(rng, lo_log10, hi_log10):
    return 10 ** rng.uniform(lo_log10, hi_log10)
    
def clear_pick():
    # Clear the radio widget's stored value
    st.session_state.pop("pick_widget", None)
    # Also clear the mirrored variable (optional)
    st.session_state.user_pick = None

def generate_exercise_scenario(seed=None):
    rng = np.random.default_rng(seed)

    # --- Draw TRUE parameters from defined ranges
    K1_true = 10 ** rng.uniform(*EX_RANGE["K1_log10"])
    K2_true = 10 ** rng.uniform(*EX_RANGE["K2_log10"])
    R_true_mm_a = float(rng.uniform(*EX_RANGE["R_mm_a"]))
    R_true = mm_a_to_m_s(R_true_mm_a)

    # Synthetic observations
    x_dense = np.linspace(0.0, L, 801)
    h_dense = head_profile_two_zone_recharge_noflow_head(x_dense, L1, L, K1_true, K2_true, R_true, h_right)
    h_obs = np.interp(x_obs, x_dense, h_dense)

    wrong_param = rng.choice(["K1", "K2", "RCH"])

    # Initial = true except one wrong
    K1_init, K2_init, R_init_mm_a = K1_true, K2_true, R_true_mm_a

    def perturb_log(val):
        v = np.log10(val)
        for _ in range(20):
            v_new = np.clip(v + rng.uniform(-0.8, 0.8), log_minK, log_maxK)
            if abs(v_new - v) > 0.15:
                return 10 ** v_new
        return 10 ** np.clip(v + 0.3, log_minK, log_maxK)

    def perturb_mm_a(val):
        for _ in range(20):
            v_new = float(np.clip(val * (10 ** rng.uniform(-0.5, 0.5)), R_min_mm_a, R_max_mm_a))
            if abs(v_new - val) > 10.0:
                return v_new
        return float(np.clip(val + 50.0, R_min_mm_a, R_max_mm_a))

    if wrong_param == "K1":
        K1_init = perturb_log(K1_true)
    elif wrong_param == "K2":
        K2_init = perturb_log(K2_true)
    else:
        R_init_mm_a = perturb_mm_a(R_true_mm_a)

    return dict(
        K1_true=K1_true, K2_true=K2_true, R_true_mm_a=R_true_mm_a,
        h_obs=h_obs, wrong_param=wrong_param,
        K1_init=K1_init, K2_init=K2_init, R_init_mm_a=R_init_mm_a,
    )

# -------------------------
# Exercise toggle + scenario storage
# -------------------------




# -------------------------
# Controls above plot
# -------------------------
cols = st.columns((1, 1), gap="large")

with cols[0]:
    with st.expander("Modify the plot", expanded=False):
        n_points = 100
        show_flux = st.checkbox("Show flux plot (q = R·x)", value=False)

with cols[1]:
    exercise_mode = st.toggle("Exercise mode (generate synthetic observations)", value=False)
    if exercise_mode:
        if "exercise_scenario" not in st.session_state:
            st.session_state.exercise_scenario = generate_exercise_scenario()
    
        sc = st.session_state.exercise_scenario
    
        # IMPORTANT: use separate, non-widget state variables for slider values
        if "K1s_model" not in st.session_state:
            st.session_state.K1s_model = float(np.log10(sc["K1_init"]))
        if "K2s_model" not in st.session_state:
            st.session_state.K2s_model = float(np.log10(sc["K2_init"]))
        if "R_mm_a_model" not in st.session_state:
            st.session_state.R_mm_a_model = float(sc["R_init_mm_a"])
        if "user_pick" not in st.session_state:
            st.session_state.user_pick = None
    
    else:
        # optional cleanup when leaving exercise mode
        for k in ["exercise_scenario", "K1s_model", "K2s_model", "R_mm_a_model", "user_pick"]:
            st.session_state.pop(k, None)
    
    if exercise_mode:
        st.write("Which parameter should be modified?")
        st.session_state.user_pick = st.radio(
            "Select one:",
            ["K1", "K2", "RCH"],
            index=None,
            key="pick_widget",
        )

cols2 = st.columns((1,1,1))
with cols2[1]:
    if exercise_mode:
        R_mm_a = st.slider("Recharge R [mm/a]", R_min_mm_a, R_max_mm_a, st.session_state.R_mm_a_model, 5.0,
                            key="R_widget")
        st.session_state.R_mm_a_model = R_mm_a
    else:
         R_mm_a = st.slider("Recharge R [mm/a]", R_min_mm_a, R_max_mm_a, 100.0, 5.0, key="R_widget")
    R = mm_a_to_m_s(R_mm_a)
    st.write("**Recharge R [m/s]:** %5.2e" % R)
    
with cols2[0]:
    if exercise_mode:
        K1s = st.slider("_(log of) K1 [m/s]_", log_minK, log_maxK, st.session_state.K1s_model, 0.01,
                        format="%4.2f", key="K1s_widget")
        st.session_state.K1s_model = K1s
    else:
        K1s = st.slider("_(log of) K1 [m/s]_", log_minK, log_maxK, -5.0, 0.01, format="%4.2f", key="K1s_widget")
    K1 = 10 ** K1s
    st.write("**K1 [m/s]:** %5.2e" % K1)
    
with cols2[2]:
    if exercise_mode:
        K2s = st.slider("_(log of) K2 [m/s]_", log_minK, log_maxK, st.session_state.K2s_model, 0.01,
                        format="%4.2f", key="K2s_widget")
        st.session_state.K2s_model = K2s
    else:
        K2s = st.slider("_(log of) K2 [m/s]_", log_minK, log_maxK, -5.3, 0.01, format="%4.2f", key="K2s_widget") 
    K2 = 10 ** K2s
    st.write("**K2 [m/s]:** %5.2e" % K2)
    
# -------------------------
# Compute + plot
# -------------------------
x = np.linspace(0.0, L, int(n_points))
h_model = head_profile_two_zone_recharge_noflow_head(x, L1, L, K1, K2, R, h_right)

# --- Flux profile (unit thickness)
# With no-flow at x=0 and uniform recharge:
# q(x) = R · x
q = R * x

fig, ax = plt.subplots(figsize=(9, 4.8))
ax.axvspan(0, L1,color="aquamarine", alpha=0.12)
ax.axvspan(L1, L,color="blue", alpha=0.08)
ax.axvline(L1, color="teal", linewidth=0.5)

ax.plot(x, h_model, color="royalblue", linewidth=3, label="Model head h(x)")
#ax.scatter([L], [h_right], s=100, color = "darkorange", zorder=5, label="Defined head")

# --- y-axis: max of plotted data, rounded up to next multiple of 2
y_max = max(
    float(np.max(h_model)),
    float(h_right),
    float(np.max(sc["h_obs"])) if exercise_mode else -np.inf
)

# Round up to the next integer that is a multiple of 2
# Example: 9.0 -> 10, 9.01 -> 10, 10.0 -> 10, 10.01 -> 12
y_top = int(math.ceil(y_max))           # next integer (or same if already integer)
y_top = int(2 * math.ceil(y_top / 2))   # next multiple of 2 (or same)

if exercise_mode:
    sc = st.session_state.exercise_scenario
    ax.scatter(x_obs, sc["h_obs"], marker="x", color = "firebrick", s=100, zorder=6, label="Synthetic observations")

ax.set_xlabel("Distance x [m]")
ax.set_ylabel("Hydraulic head h [m]")
ax.set_title("Head profile (uniform recharge, no-flow + fixed head)")
ax.grid(True, alpha=0.3)
ax.set_xlim(0, L)
ax.set_ylim(0.0, y_top)

# --- Defined head (water level) as a horizontal line extending beyond the axis + water triangle
x_ext = 1.0  # extension length beyond x=L (in meters)

# horizontal extension line (drawn outside axes)
ax.hlines(
    y=h_right,
    xmin=L,
    xmax=L + x_ext,
    colors="royalblue",
    linewidth=3,
    zorder=6,
    clip_on=False
)

# water triangle at the end of the extension (outside axes) and horizontal lines
ax.plot(
    [L + x_ext/2],
    [h_right+0.1],
    marker="v",          # downward triangle (water level symbol)
    markersize=10,
    color="royalblue",
    zorder=7,
    clip_on=False
)

ax.hlines(
    y=h_right-0.08,
    xmin=L+0.3,
    xmax=L + x_ext-0.3,
    colors="royalblue",
    linewidth=1,
    zorder=6,
    clip_on=False
)

ax.hlines(
    y=h_right-0.15,
    xmin=L+0.4,
    xmax=L + x_ext-0.4,
    colors="royalblue",
    linewidth=1,
    zorder=6,
    clip_on=False
)

# --- Label zones directly in the plot
ymin, ymax = ax.get_ylim()
y_text = ymin + 0.08 * (ymax - ymin)   # place text near the top of the plot

box_style = dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.7)

ax.text(
    L1 / 2, y_text, "Zone 1 (K1)",
    ha="center", va="top", fontsize=12,
    bbox=box_style
)

ax.text(
    L1 + (L - L1) / 2, y_text, "Zone 2 (K2)",
    ha="center", va="top", fontsize=12,
    bbox=box_style
)
ax.legend(loc="best", fontsize=12, frameon=True)

st.pyplot(fig, clear_figure=True)

if show_flux:
    fig_q, ax_q = plt.subplots(figsize=(9, 3.5))

    ax_q.plot(x, q, linewidth=2)
    ax_q.set_xlabel("Distance x [m]")
    ax_q.set_ylabel("Specific discharge q(x) [m/s]")
    ax_q.set_title("Recharge-induced flux profile: q(x) = R · x")

    ax_q.set_xlim(0, L)
    ax_q.grid(True, alpha=0.1)

    st.pyplot(fig_q, clear_figure=True)


# RMSE + feedback in exercise mode
if exercise_mode:
    sc = st.session_state.exercise_scenario
    h_mod_at_obs = np.interp(x_obs, x, h_model)
    rmse = float(np.sqrt(np.mean((h_mod_at_obs - sc["h_obs"]) ** 2)))
    st.markdown(f"**RMSE (synthetic obs): {rmse:.3f} m**")

    if st.session_state.user_pick is not None:
        if st.session_state.user_pick == sc["wrong_param"]:
            st.success(f"Correct: the parameter that was initially wrong is **{sc['wrong_param']}**.")
        else:
            st.warning("Not quite. Try again (or adjust parameters and see what improves the fit).")

# -------------------------
# Exercise buttons (below plot) — now safe
# -------------------------
if exercise_mode:
    bcol = st.columns((1, 1, 2))
    with bcol[0]:
        if st.button("Reset to beginning", use_container_width=True):
            sc = st.session_state.exercise_scenario
            st.session_state.K1s_model = float(np.log10(sc["K1_init"]))
            st.session_state.K2s_model = float(np.log10(sc["K2_init"]))
            st.session_state.R_mm_a_model = float(sc["R_init_mm_a"])
            st.session_state.user_pick = None
            
            clear_pick()
            st.rerun()

    with bcol[1]:
        if st.button("New variant", use_container_width=True):
            st.session_state.exercise_scenario = generate_exercise_scenario()
            sc = st.session_state.exercise_scenario
            st.session_state.K1s_model = float(np.log10(sc["K1_init"]))
            st.session_state.K2s_model = float(np.log10(sc["K2_init"]))
            st.session_state.R_mm_a_model = float(sc["R_init_mm_a"])
            st.session_state.user_pick = None
            
            clear_pick()
            st.rerun()

    with st.expander("Solution (true parameters)", expanded=False):
        st.write("**True K1 [m/s]:** %5.2e" % sc["K1_true"])
        st.write("**True K2 [m/s]:** %5.2e" % sc["K2_true"])
        st.write("**True R [mm/a]:** %.1f" % sc["R_true_mm_a"])
        st.write("**Wrong parameter in initial model:** %s" % sc["wrong_param"])

st.markdown('---')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')