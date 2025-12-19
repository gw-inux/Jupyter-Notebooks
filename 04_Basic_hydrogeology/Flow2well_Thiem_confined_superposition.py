# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# also 03-05-002
# Todo
# log slider
# number input

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

st.title('Steady-State Flow to Multiple Wells in a Confined Aquifer - Thiem Equation & Superposition')

# Import parameter
log_min = -7.0  # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0   # K / Corresponds to 10^0 = 1

columns = st.columns((1, 1, 1))

with columns[0]:
    with st.expander('Adjust the plot'):
        x_max = st.slider('x_max of the plot (m)', 10, 10000, 3000, 50, format="%5i")
    
    

with columns[1]:
    with st.expander('Adjust the aquifer parameters'):
        H = st.slider('Unaffected hydraulic head (m)', 1.0, 100.0, 50.0, 0.01, format="%5.2f")
        m = st.slider('Thickness of the aquifer (m)', 1.0, 100.0, 20.0, 0.01, format="%4.2f")
        K_slider_value = st.slider('(log of) **Hydr. conductivity (m/s)**',
                                   log_min, log_max, -3.0, 0.01, format="%4.2f")
        # Convert the slider value to the logarithmic scale
        K = 10 ** K_slider_value
        # Display the logarithmic value
        st.write("_Hydraulic conductivity (m/s):_ %5.2e" % K)

with columns[2]:
    with st.expander('Adjust the well characteristics'):
        r_w = st.slider('Well radius (m)', 0.01, 1.0, 0.3, 0.01, format="%4.2f")
        ddwn = st.toggle('Abstraction _Q_ or Drawdown _s_?')
        if ddwn:
            s = st.slider('Drawdown at the well (m)', 0.01, 10.0, 0.2, 0.01, format="%5.2f")
        else:
            Q = st.slider('Abstraction rate per well (m³/s)', 0.001, 1.0, 0.05, 0.001, format="%5.3f")

# --- Number of wells: 3, 5, or 7 (always symmetric around x = 0) ---
n_wells = st.radio("Number of wells (symmetric around the central well):", options=[1, 3, 5, 7, 9, 11, 13], index=0, horizontal=True)

# Maximum index factor: for 3 wells → 1 (positions -d, 0, d)
#                       for 5 wells → 2 (positions -2d, -d, 0, d, 2d)
#                       for 7 wells → 3 (positions -3d, -2d, -d, 0, d, 2d, 3d)
k_max = (n_wells - 1) // 2

# Distance of neighboring wells from the central well
# Ensure outermost well lies within the plotting range: k_max * d <= x_max
d = st.slider(
    'Distance of neighboring wells from the central well (m)',
    float(max(2 * r_w, 1.0)),
    float(x_max / max(k_max, 1)),  # avoid division by zero (k_max>=1 here)
    float(min(200.0, x_max / max(k_max, 1))),
    step=1.0,
    format="%5.1f"
)

# --- Initialize R and Q (single-well basis, same for all wells) ---
if ddwn:
    # Sichardt estimate for radius of influence based on drawdown s
    R = 3000 * s * K**0.5
    # Thiem: compute Q from s at well
    Q = 2 * np.pi * K * m * s / np.log(R / r_w)
else:
    # Start with an initial guess for R and iterate using your original scheme
    R_max = 3000 * (H - m) * 0.01**0.5
    R_old = R_max / 2

    # FIND R iteratively (Thiem + Sichardt)
    while True:
        h_w = H - (Q * np.log(R_old / r_w)) / (2 * np.pi * K * m)
        R = 3000 * (H - h_w) * K**0.5
        if abs(R - R_old) < 0.00001:
            break
        R_old = R

# --- COMPUTE h(x) with superposition of multiple wells ---

n_points = 5000  # reasonable resolution for plotting
x = np.linspace(-x_max, x_max, n_points)

# Well positions: symmetric multiples of d around 0
# Example: n_wells=5 → multipliers = [-2, -1, 0, 1, 2] * d
multipliers = np.arange(-k_max, k_max + 1)
well_positions = multipliers * d

# Start from undisturbed head everywhere
h = np.full_like(x, H, dtype=float)

# Precompute factor in Thiem equation
C = Q / (2 * np.pi * K * m)

# Superposition: subtract drawdown from each well
for x_w in well_positions:
    r = np.abs(x - x_w)
    # Avoid r < r_w to prevent log(0) and keep well radius
    r[r < r_w] = r_w
    # Apply drawdown only within radius of influence R
    mask = r < R
    h[mask] -= C * np.log(R / r[mask])

# Head at the central well (x = 0) including superposition from all wells
x_center = 0.0
h_center = H
for x_w in well_positions:
    r_c = abs(x_center - x_w)
    if r_c < r_w:
        r_c = r_w
    if r_c < R:
        h_center -= C * np.log(R / r_c)

# --- PLOT ---
fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(1, 1, 1)

# Check confined vs "unconfined" conditions at central well
if h_center > m:
    color = 'b'
    linestyle = '-'
else:
    color = 'r'
    linestyle = '-'
    ax.text((R / 2), (H * 1.05), 'UNCONFINED CONDITIONS - ADJUST PARAMETER')

ax.plot(x, h, linestyle + color, label='Head distribution')

# Mark well positions
for x_w in well_positions:
    ax.axvline(x=x_w, ymin=0, ymax=1, linestyle=':', color='k', linewidth=1)
    ax.text(x_w, H + 0.3, 'W', ha='center', va='bottom')

ax.set(
    xlabel='x [m]',
    ylabel='head [m]',
    xlim=[-x_max, x_max],
    ylim=[0, H + 5]
)

# MAKE 'WATER'-TRIANGLE
ax.arrow(x_max * 0.95, (H + (H * 0.04)), 0, -0.01,
         fc="k", ec="k", head_width=(x_max * 0.04), head_length=(H * 0.04))
ax.hlines(y=H - (H * 0.02), xmin=x_max * 0.93, xmax=x_max * 0.97, colors='blue')
ax.hlines(y=H - (H * 0.04), xmin=x_max * 0.94, xmax=x_max * 0.96, colors='blue')

# Aquifer top line
ax.hlines(y=m, xmin=-x_max, xmax=x_max, colors='saddlebrown')

# COLORED AREA (ATTN: Y-VALUES = RELATIVE VALUE)
ax.axvspan(-x_max, x_max, ymin=0, ymax=(m / (H + 5)), alpha=0.9, color='lightblue')
ax.axvspan(-x_max, x_max, ymin=0, ymax=1.0, alpha=0.5, color='linen')

ax.text((x_max / 2), (m / 2), 'confined aquifer')

st.pyplot(fig)

# --- OUTPUTS ---

# ---------- OUTPUTS ----------
s_center = H - h_center

st.markdown(f"""
### Model Output
**Number of wells:** {n_wells}  
**Drawdown at central well:** {s_center:.3f} m  
**Abstraction rate per well (Q):** {Q:.3f} m³/s  
**Total abstraction rate:** {(n_wells * Q):.3f} m³/s  
**Radius of influence (Sichardt):** {R:.1f} m  
"""
)

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
