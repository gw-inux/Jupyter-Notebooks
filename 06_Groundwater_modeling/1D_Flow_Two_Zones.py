import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------------------------------------------------------
# 1D steady groundwater flow through TWO zones in series (no recharge)
# -----------------------------------------------------------------------------

#st.set_page_config(page_title="1D Calibration: Two-Zone K")  # no wide layout

st.title("Groundwater Model Calibration (1D, two-zone aquifer)")
st.write(
    "Adjust **K1** and **K2** (log-scale sliders) and inspect the resulting **hydraulic head profile** "
    "between two fixed-head boundaries (no recharge)."
)

# --- Geometry (from sketch: 500 m + 500 m)
L1 = 500.0  # m
L2 = 500.0  # m
L = L1 + L2

# --- Fixed head boundaries (hard-coded)
h_left = 50.0   # m
h_right = 49.0  # m

# --- Measurement locations (hard-coded, along x)
x_mst1 = 250.0  # m (zone 1)
x_mst2 = 750.0  # m (zone 2)

# --- Observed heads (as provided)
h_obs_mst1 = 49.95  # m
h_obs_mst2 = 49.45  # m

# --- Log slider ranges for K (m/s)
log_minK = -8.0  # 1e-8
log_maxK = -2.0  # 1e-2

# --- Controls ABOVE the plot (3 columns, like your style)
cols = st.columns((1, 1, 1), gap="large")

with cols[0]:
    with st.expander("Modify the plot", expanded=False):
        n_points = st.slider("Resolution (number of x points)", 50, 1200, 401, step=25)
        ypad = st.slider("Extra y-range padding (m)", 0.0, 1.0, 0.10, 0.01)

with cols[1]:
    with st.expander("Hydraulic parameters", expanded=True):
        container = st.container()
        K1s = st.slider(
            "_(log of) Hydraulic conductivity K1 [m/s]_",
            log_minK, log_maxK, -5.0, 0.01,
            format="%4.2f",
            key="K1s",
        )
        K1 = 10 ** K1s
        container.write("**K1 [m/s]:** %5.2e" % K1)

        container = st.container()
        K2s = st.slider(
            "_(log of) Hydraulic conductivity K2 [m/s]_",
            log_minK, log_maxK, -5.3, 0.01,
            format="%4.2f",
            key="K2s",
        )
        K2 = 10 ** K2s
        container.write("**K2 [m/s]:** %5.2e" % K2)

with cols[2]:
    with st.expander("Observation points", expanded=True):
        st.markdown(
            f"""
- **Mst1** at *x* = {x_mst1:.0f} m (Zone 1), observed **h = {h_obs_mst1:.2f} m**
- **Mst2** at *x* = {x_mst2:.0f} m (Zone 2), observed **h = {h_obs_mst2:.2f} m**
            """
        )

# --- Model
def head_profile_two_zone(
    x: np.ndarray, hL: float, hR: float, L1: float, L2: float, K1: float, K2: float
):
    # Series resistances (unit area): R = L/K
    #R_total = (L1 / K1) + (L2 / K2)
    R_total = (L1+L2)/((L1 / K1) + (L2 / K2))
    q = (hL - hR) / (L1+L2) * R_total

    # head drop over zone 1
    dh1 = q * (L1 / K1)

    h = np.empty_like(x, dtype=float)

    mask1 = x <= L1
    h[mask1] = hL - q * (x[mask1] / K1)

    mask2 = ~mask1
    h[mask2] = (hL - dh1) - q * ((x[mask2] - L1) / K2)

    return h, q

def h_at(x_query: float, x: np.ndarray, h: np.ndarray) -> float:
    return float(np.interp(x_query, x, h))

# --- Compute
x = np.linspace(0.0, L, int(n_points))
h, q = head_profile_two_zone(x, h_left, h_right, L1, L2, K1, K2)

h_mod_mst1 = h_at(x_mst1, x, h)
h_mod_mst2 = h_at(x_mst2, x, h)

res1 = h_mod_mst1 - h_obs_mst1
res2 = h_mod_mst2 - h_obs_mst2
rmse = float(np.sqrt((res1**2 + res2**2) / 2.0))

# --- Plot (below widgets)
fig, ax = plt.subplots(figsize=(9, 4.8))

# zone shading + interface
ax.axvspan(0, L1, alpha=0.12)
ax.axvspan(L1, L, alpha=0.12)
ax.axvline(L1, linewidth=1)

ax.plot(x, h, linewidth=2, label="Model head h(x)")
ax.scatter([0, L], [h_left, h_right], zorder=5, label="Fixed-head boundaries")

# observations and modeled values at those x
ax.scatter([x_mst1, x_mst2], [h_obs_mst1, h_obs_mst2], marker="x", s=90, zorder=6, label="Observed heads")
ax.scatter([x_mst1, x_mst2], [h_mod_mst1, h_mod_mst2], s=60, zorder=6, label="Model @ obs points")

ax.set_xlabel("Distance x [m]")
ax.set_ylabel("Hydraulic head h [m]")
ax.set_title("1D steady head profile (two-zone aquifer)")
ax.grid(True, alpha=0.3)
ax.set_xlim(0, L)

# y-limits: keep robust + allow a small padding
hmin = min(h_left, h_right, h_obs_mst1, h_obs_mst2, h.min())
hmax = max(h_left, h_right, h_obs_mst1, h_obs_mst2, h.max())
ax.set_ylim(hmin - ypad, hmax + ypad)

ax.legend(loc="best")
st.pyplot(fig, clear_figure=True)

# --- Compact diagnostics
st.markdown(
    f"""
**Diagnostics**  
- Flux (unit area): **q = {q:.3e} m²/s**  
- Residuals (model−obs): **Mst1 {res1:+.3f} m**, **Mst2 {res2:+.3f} m**  
- **RMSE (2 points): {rmse:.3f} m**
"""
)

st.caption(
    "Assumptions: 1D steady flow, constant cross-sectional area, no recharge/sinks, "
    "piecewise-constant K in two zones (series resistances)."
)
