# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import streamlit as st

# also 03-05-004
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

st.title('Steady-State Flow to Multiple Wells in an Unconfined Aquifer - Thiem Equation & Superposition')

# Input
log_min = -7.0  # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0   # K / Corresponds to 10^0 = 1

columns = st.columns((1,1,1), gap='medium')

with columns[0]:
    with st.expander('Show plot and system parameter'):
        x_max = st.slider('x_max (m)', 50, 3000, 500, 10)
        H = st.slider('Initial water table elevation H (m)', 1.0, 100.0, 25.0, 0.01)
    
with columns[1]:
    show_pit = st.toggle('Show the construction pit')
    # Construction pit parameters
    if show_pit:
        pit_depth = st.slider("Pit penetration into groundwater (m)", 0.0, 20.0, 5.0, 0.1)
        pit_length = st.slider("Pit length (m)", 1.0, float(2 * x_max), 80.0, 1.0)

with columns[2]:
    with st.expander('Show K and Q'):
        K_slider_value = st.slider('(log of) Hydraulic conductivity K (m/s)',
                                   log_min, log_max, -3.0, 0.01, format="%4.2f")
        K = 10 ** K_slider_value
        st.write("_Hydraulic conductivity (m/s):_ %5.2e" % K)
    
        ddwn = st.toggle('Specify abstraction _Q_ or drawdown _s_ at central well?')
        if ddwn:
            s_user = st.slider('(local) Drawdown at central well (m)', 0.01, max(H - 0.1, 0.5), 0.5, 0.01)
            Q = None  # will be computed below
        else:
            Q = st.slider('Abstraction rate per well Q (m³/s)', 0.001, 0.5, 0.01, 0.001, format="%5.3f")
            s_user = None

# -------- Number of wells: 3, 5, 7 (symmetric around x = 0) --------
columns2 = st.columns((1,3,1), gap='medium')
with columns2[1]:
    n_wells = st.radio("Number of wells (symmetric around the central well):", options=[1, 3, 5, 7, 9, 11, 13], index=0, horizontal=True)
k_max = (n_wells - 1) // 2  # e.g. 3→1, 5→2, 7→3
with columns2[2]:
    capa = st.toggle('Show wells and their capacity')


columns3 = st.columns((1,1), gap='medium')
# Distance of neighboring wells from the central well
with columns3[0]:
    r_w = st.slider('Well radius r_w (m)', 0.01, 1.0, 0.3, 0.01)
with columns3[1]:
    d = st.slider(
        'Distance between wells (m)',
        5.0,
        float(x_max / max(k_max, 1)),
        float(min(50.0, x_max / max(k_max, 1))),
        step=1.0,
        format="%5.1f"
    )


# ---------- Functions for unconfined Thiem ----------

def compute_R(Q, K, H, r_w):
    """
    Iteratively compute R and h_w for a single unconfined well
    using the Dupuit-Thiem equation and Sichardt's empirical formula.
    """
    dry = False
    h = H / 2.0
    max_it = 1000
    tol = 1e-6

    for _ in range(max_it):
        R = 3000 * (H - h) * np.sqrt(K)
        term = H**2 - (Q / (np.pi * K) * np.log(R / r_w))
        if term < 0.0:
            dry = True
            break
        h_new = np.sqrt(term)

        if np.abs(h_new - h) < tol:
            h = h_new
            break

        h = h_new

    # Final R with last h
    R = 3000 * (H - h) * np.sqrt(K)
    return R, h, dry


# ---------- Initialize R and Q (single-well basis) ----------

if ddwn:
    # User specifies drawdown at central well: s_user
    # Sichardt estimate for radius of influence:
    R = 3000 * s_user * np.sqrt(K)
    # Unconfined Thiem at the well:
    # (H - s)^2 = H^2 - (Q / (pi K)) ln(R / r_w)
    # => Q = pi K (H^2 - (H - s)^2) / ln(R / r_w)
    h_w = H - s_user
    numerator = H**2 - h_w**2  # = 2 H s - s^2
    Q = np.pi * K * numerator / np.log(R / r_w)
    dry_single = False  # by construction this is consistent
else:
    # User specifies Q per well: determine R, h_w, and potential dry condition
    R, h_w, dry_single = compute_R(Q, K, H, r_w)

# ---------- Superposition for multiple wells (along x) ----------

n_points = 5000
x = np.linspace(-x_max, x_max, n_points)

# Well positions: symmetric around 0 with spacing d
multipliers = np.arange(-k_max, k_max + 1)
well_positions = multipliers * d

# Start from H^2 everywhere (unconfined Thiem is linear in h^2)
h2 = np.full_like(x, H**2, dtype=float)

# Apply superposition: for each well, subtract its contribution in H^2 - h^2
# h^2 = H^2 - (Q / (pi K)) * sum_i ln(R / r_i)
for x_w in well_positions:
    r = np.abs(x - x_w)
    r[r < r_w] = r_w
    mask = r < R
    h2[mask] -= (Q / (np.pi * K)) * np.log(R / r[mask])

# Identify dry zones (where h^2 <= 0)
dry = np.any(h2 <= 0.0)
h2_clipped = np.maximum(h2, 0.0)
h = np.sqrt(h2_clipped)

# Head at central well (x=0) including superposition
x_center = 0.0
h2_center = H**2
for x_w in well_positions:
    r_c = abs(x_center - x_w)
    if r_c < r_w:
        r_c = r_w
    if r_c < R:
        h2_center -= (Q / (np.pi * K)) * np.log(R / r_c)

if h2_center <= 0.0:
    h_center = 0.0
    dry_center = True
else:
    h_center = np.sqrt(h2_center)
    dry_center = False
    
    
    
    
    
# --- Compute head and Sichardt capacity Q_c at each well ---
well_heads = []
well_Qc = []

for x_i in well_positions:
    # h² at well x_i including superposition of all wells
    h2_i = H**2
    for x_j in well_positions:
        r_ij = abs(x_i - x_j)
        if r_ij < r_w:
            r_ij = r_w
        if r_ij < R:
            h2_i -= (Q / (np.pi * K)) * np.log(R / r_ij)

    if h2_i <= 0.0:
        h_i = 0.0
    else:
        h_i = np.sqrt(h2_i)

    # Sichardt capacity: Q_c = 2 * pi * r_well * h * sqrt(K) / 15
    Q_c_i = 2.0 * np.pi * r_w * h_i * np.sqrt(K) / 15.0

    well_heads.append(h_i)
    well_Qc.append(Q_c_i)


# ---------- PLOT ----------

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1)

if dry or dry_center:
    color = 'r'
    linestyle = '-'
else:
    color = 'b'
    linestyle = '-'

ax.plot(x, h, linestyle + color)

# Fill saturated area
ax.fill_between(x, h, 0, facecolor='lightblue')

# Undisturbed water table line
ax.hlines(y=H, xmin=-x_max, xmax=x_max, linestyle='--', colors=color)

# Mark well positions + vertical line colored by capacity Q_c vs Q
if capa:
    for x_w, h_i, Q_c_i in zip(well_positions, well_heads, well_Qc):
        color_w = 'g' if Q_c_i >= Q else 'r'
    
        # Vertical line from bottom to local head at the well
        ax.vlines(x=x_w+3, ymin=0, ymax=h_i, colors=color_w, linewidth=2)
        ax.vlines(x=x_w-3, ymin=0, ymax=h_i, colors=color_w, linewidth=2)
        
        ax.vlines(x=x_w, ymin=0, ymax=H, linestyle=':', color='k', linewidth=1)
    
        # Label the well above the initial water table
        #ax.text(x_w, H + 0.3, 'W', ha='center', va='bottom', color=color_w)
else:
    for x_w, h_i, Q_c_i in zip(well_positions, well_heads, well_Qc):
        ax.vlines(x=x_w, ymin=0, ymax=H, linestyle=':', color='k', linewidth=1)
    
        # Label the well above the initial water table
        #ax.text(x_w, H + 0.3, 'W', ha='center', va='bottom', color=color_w)

ax.set(
    xlabel='x [m]',
    ylabel='head h [m]',
    xlim=[-x_max, x_max],
    ylim=[0, H + 5]
)

# MAKE 'WATER'-TRIANGLE
ax.arrow(
    x_max * 0.95, (H + (H * 0.04)), 0, -0.01,
    fc="k", ec="k", head_width=(x_max * 0.04), head_length=(H * 0.04)
)
ax.hlines(y=H - (H * 0.02), xmin=x_max * 0.92, xmax=x_max * 0.98, colors='blue')
ax.hlines(y=H - (H * 0.04), xmin=x_max * 0.94, xmax=x_max * 0.96, colors='blue')

if dry or dry_center:
    ax.text((x_max / 2), 1.0, 'unconfined aquifer')
    ax.text((x_max / 2), 2.5, 'well(s) running dry', color='red')
else:
    ax.text((x_max / 2), 1.0, 'unconfined aquifer')

if show_pit:
    # --- Construction pit (centered at x = 0) ---
    pit_half_len = pit_length / 2.0
    
    # Bottom of pit measured from initial groundwater table H downward
    # (Clamp at y = 0 so we don't go below the bottom of the plot)
    pit_bottom = max(0.0, H - pit_depth)
    
    # Draw rectangle from pit_bottom up to the top of the plot (H + 5)
    pit_rect = Rectangle(
        (-pit_half_len, pit_bottom),      # (x_left, y_bottom)
        pit_length,                       # width
        (H + 5) - pit_bottom,            # height
        linewidth=1.5,
        edgecolor="black",
        facecolor="none"
    )
    ax.add_patch(pit_rect)
    
    ax.text(
        0.0,
        H + 0.5,
        "Construction pit",
        ha="center",
        va="bottom"
    )

st.pyplot(fig)

# ---------- OUTPUTS ----------
s_center = H - h_center

st.markdown(f"""
### Model Output
**Number of wells:** {n_wells}  
**Drawdown at central well:** {s_center:.3f} m  
**Abstraction rate per well (Q):** {Q:.3e} m³/s  
**Total abstraction rate:** {(n_wells * Q):.3e} m³/s  
**Radius of influence (Sichardt):** {R:.1f} m  
"""
)

# Well-specific Sichardt capacities
if capa:
    for i, (x_w, Q_c_i) in enumerate(zip(well_positions, well_Qc), start=1):
        status = "OK" if Q_c_i >= Q else "INSUFFICIENT"
        st.markdown(f"""
            **Well {i}** at x = {x_w:.1f} m:
            $Q_c$ = {Q_c_i:.4f} m³/s ({status})"""
        )
else:
    for i, (x_w, Q_c_i) in enumerate(zip(well_positions, well_Qc), start=1):
        st.markdown(f"""
            **Well {i}** at x = {x_w:.1f} m:
            $Q_c$ = {Q_c_i:.4f} m³/s"""
        )
"---"

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
