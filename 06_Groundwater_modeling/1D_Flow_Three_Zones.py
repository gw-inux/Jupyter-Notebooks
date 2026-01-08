import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------------------------------------------------------
# 1D steady groundwater flow through THREE zones in series (no recharge)
# Zones: T1 | T2 | T1  (each 333 m long), width W = 450 m
# Fixed heads: h(0)=10 m, h(L)=1 m
# Observations at x = 111, 222, 444, 555, 777, 888 m with given h-values
# UI: no sidebar, widgets above plot, log10 sliders for transmissivity
# -----------------------------------------------------------------------------

st.set_page_config(page_title="1D Calibration: Three-Zone T")

st.title("Groundwater Model Calibration (1D, three-zone aquifer)")
st.write(
    "Adjust **T1** and **T2** (log-scale sliders) and inspect the resulting **hydraulic head profile** "
    "between two fixed-head boundaries (no recharge)."
)

# --- Geometry
L1 = 333.0  # m (Zone 1: T1)
L2 = 333.0  # m (Zone 2: T2)
L3 = 333.0  # m (Zone 3: T1)
L = L1 + L2 + L3
W = 450.0   # m (model width; Q = q' * W)

# --- Fixed head boundaries (hard-coded)
h_left = 10.0  # m
h_right = 1.0  # m

# --- Observation locations (hard-coded)
x_obs1 = np.array([111.0, 555.0, 777.0])
x_obs2 = np.array([111.0, 222.0, 444.0, 555.0, 777.0, 888.0])

# --- Observation values (from your table image)
# If any value differs, just update this list.
h_obs1 = np.array([9.75, 4.25, 1.50])
h_obs2 = np.array([9.75, 9.50, 6.75, 4.25, 1.50, 1.25])

# --- Log slider ranges for T (m²/s) – similar to your snippet
log_minT = -7.0
log_maxT = 0.0

# --- Controls ABOVE the plot
cols = st.columns((1, 1, 1), gap="large")

with cols[0]:
    with st.expander("Modify the plot", expanded=False):
        n_points = st.slider("Resolution (number of x points)", 50, 2000, 601, step=25)
        ypad = st.slider("Extra y-range padding (m)", 0.0, 2.0, 0.20, 0.01)
        more_obs = st.toggle('Show more observations')

with cols[1]:
    with st.expander("Hydraulic parameters", expanded=True):
        container = st.container()
        T1s = st.slider(
            "_(log of) Transmissivity T1 [m²/s]_",
            log_minT, log_maxT, -4.0, 0.01,
            format="%4.2f",
            key="T1s",
        )
        T1 = 10 ** T1s
        container.write("**T1 [m²/s]:** %5.2e" % T1)

        container = st.container()
        T2s = st.slider(
            "_(log of) Transmissivity T2 [m²/s]_",
            log_minT, log_maxT, -4.0, 0.01,
            format="%4.2f",
            key="T2s",
        )
        T2 = 10 ** T2s
        container.write("**T2 [m²/s]:** %5.2e" % T2)

with cols[2]:
    if more_obs:
        with st.expander("Observations", expanded=True):
            st.markdown(
                f"""
    - Fixed heads: **h(0) = {h_left:.2f} m**, **h({L:.0f} m) = {h_right:.2f} m**
    - Zone lengths: **{L1:.0f} m | {L2:.0f} m | {L3:.0f} m**  (T1 | T2 | T1)
    - Width: **W = {W:.0f} m**
    - Observation x-locations: {", ".join([str(int(v)) for v in x_obs2])} m
                """
            )
    else:
        with st.expander("Observations", expanded=True):
            st.markdown(
                f"""
    - Fixed heads: **h(0) = {h_left:.2f} m**, **h({L:.0f} m) = {h_right:.2f} m**
    - Zone lengths: **{L1:.0f} m | {L2:.0f} m | {L3:.0f} m**  (T1 | T2 | T1)
    - Width: **W = {W:.0f} m**
    - Observation x-locations: {", ".join([str(int(v)) for v in x_obs1])} m
                """
            )

# --- Model (confined 1D, no recharge): q' = -T dh/dx ; piecewise constant T
def head_profile_three_zone_T(
    x: np.ndarray,
    hL: float,
    hR: float,
    L1: float,
    L2: float,
    L3: float,
    T1: float,
    T2: float,
):
    # Resistances in series (per unit width): R = L / T
    R_total = (L1 / T1) + (L2 / T2) + (L3 / T1)

    # Discharge per unit width (q', units m²/s): q' = (hL - hR) / R_total
    qprime = (hL - hR) / R_total

    # Precompute head drops over zones 1 and 2
    dh1 = qprime * (L1 / T1)
    dh2 = qprime * (L2 / T2)

    h = np.empty_like(x, dtype=float)

    # Zone 1
    m1 = x <= L1
    h[m1] = hL - qprime * (x[m1] / T1)

    # Zone 2
    m2 = (x > L1) & (x <= L1 + L2)
    h[m2] = (hL - dh1) - qprime * ((x[m2] - L1) / T2)

    # Zone 3
    m3 = x > (L1 + L2)
    h[m3] = (hL - dh1 - dh2) - qprime * ((x[m3] - (L1 + L2)) / T1)

    return h, qprime

def interp_h(x_query: np.ndarray, x: np.ndarray, h: np.ndarray) -> np.ndarray:
    return np.interp(x_query, x, h)

# --- Compute
x = np.linspace(0.0, L, int(n_points))
h, qprime = head_profile_three_zone_T(x, h_left, h_right, L1, L2, L3, T1, T2)

if more_obs:
    h_mod2 = interp_h(x_obs2, x, h)
    res2 = h_mod2 - h_obs2
    rmse2 = float(np.sqrt(np.mean(res2**2)))
else:
    h_mod1 = interp_h(x_obs1, x, h)
    res1 = h_mod1 - h_obs1
    rmse1 = float(np.sqrt(np.mean(res1**2)))

Q = qprime * W  # total discharge through width W (units m³/s)

# --- Plot
fig, ax = plt.subplots(figsize=(9, 4.8))

# zone shading + interfaces
ax.axvspan(0, L1, alpha=0.12)
ax.axvspan(L1, L1 + L2, alpha=0.08)
ax.axvspan(L1 + L2, L, alpha=0.12)
ax.axvline(L1, linewidth=1)
ax.axvline(L1 + L2, linewidth=1)

ax.plot(x, h, linewidth=2, label="Model head h(x)")

# boundaries
ax.scatter([0, L], [h_left, h_right], zorder=5, label="Specified-head boundaries")

# observations and modeled at obs points
if more_obs:
    ax.scatter(x_obs2, h_obs2, marker="x", s=90, zorder=6, label="Observed heads")
    ax.scatter(x_obs2, h_mod2, s=60, zorder=6, label="Model @ obs points")
else:
    ax.scatter(x_obs1, h_obs1, marker="x", s=90, zorder=6, label="Observed heads")
    ax.scatter(x_obs1, h_mod1, s=60, zorder=6, label="Model @ obs points")

ax.set_xlabel("Distance x [m]")
ax.set_ylabel("Hydraulic head h [m]")
ax.set_title("1D steady head profile (three-zone aquifer: T1 | T2 | T1)")
ax.grid(True, alpha=0.3)
ax.set_xlim(0, L)

# y-limits
hmin = min(h_left, h_right)
hmax = max(h_left, h_right)
ax.set_ylim(hmin - ypad, hmax + ypad)

ax.legend(loc="best")
st.pyplot(fig, clear_figure=True)

# --- Diagnostics
if more_obs:
    st.markdown(
        f"""
    **Diagnostics**  
    - Discharge per unit width: **q' = {qprime:.3e} m²/s**  
    - Total discharge (W = {W:.0f} m): **Q = {Q:.3e} m³/s**  
    - **RMSE (6 points): {rmse2:.3f} m**
    """
    )
else:
    st.markdown(
        f"""
    **Diagnostics**  
    - Discharge per unit width: **q' = {qprime:.3e} m²/s**  
    - Total discharge (W = {W:.0f} m): **Q = {Q:.3e} m³/s**  
    - **RMSE (6 points): {rmse1:.3f} m**
    """
    )
# Optional: show residuals table (compact)
with st.expander("Residuals table (model − observed)", expanded=False):
    if more_obs:
        for i, (xi, ho, hm, ri) in enumerate(zip(x_obs2, h_obs2, h_mod2, res2), start=1):
            st.write(f"h{i} at x={xi:.0f} m: obs={ho:.2f} m | model={hm:.2f} m | resid={ri:+.3f} m")
    else:
        for i, (xi, ho, hm, ri) in enumerate(zip(x_obs1, h_obs1, h_mod1, res1), start=1):
            st.write(f"h{i} at x={xi:.0f} m: obs={ho:.2f} m | model={hm:.2f} m | resid={ri:+.3f} m")

st.caption(
    "Assumptions: 1D steady confined flow, constant thickness, no recharge/sinks, "
    "piecewise-constant transmissivity in three zones (series resistances)."
)
