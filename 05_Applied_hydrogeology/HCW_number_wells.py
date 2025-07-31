import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("Horizontal Collector Well Replacement Calculator")
st.subheader('💧 Horizontal Collector Well Replacement Calculator', divider = 'blue')

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Carsten Leibenath": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Umweltbüro Vogtland GmbH"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# Define function for nc
def calculate_nc(L, m, l, sigma, r_d):
    numerator = (math.pi * L / sigma) + math.log(sigma / (2 * math.pi * r_d))
    denominator = math.log(L) - math.log((0.25 + 0.005 * L / m) * l - 0.6 * m)
    return numerator / denominator
    
st.markdown("""
This tool computes how many vertical wells can be replaced by a horizontal collector well based on hydraulic and geometric input parameters. The formula below is used for the computation:

""")

st.latex(r"""
n_c = \frac{ \frac{\pi L}{\sigma} + \ln\left( \frac{\sigma}{2\pi r_d} \right) }
           { \ln L - \ln\left( \left(0.25 + 0.005 \frac{L}{M} \right) l_{HCW} - 0.6 M \right) }
""")
st.markdown(r"""
**Parameter definitions**  
- $L$ – Hydraulic distance to the boundary (e.g., river, MAR basin) [m]  
- $M$ – Aquifer thickness (GWL thickness) [m]  
- $l_{HCW}$ – Length of the horizontal collector well screen [m]  
- $\sigma$ – Spacing between vertical wells in the gallery [m]  
- $r_d$ – Effective radius of well influence (common for both well types) [m]  
- $n_c$ – Number of vertical wells replaced by one horizontal collector well [-]

**Reference**  
Weregin, N. N. (1962): *Luchevye vodozabory dlja vodosnabzhenija gorodov i promyshlennosti*.  
Isdatelstvo kommunalnogo khozjaistva RFSR, Moscow.
""")

st.subheader('Interactive plot with variable HCW screen length $l_{HCW}$', divider = 'blue')

# Input widgets
st.markdown("""
#### :blue[INPUT parameters]
""")

columns = st.columns((1,1))

with columns[0]:
    L = st.number_input("Hydraulic distance to boundary $L$ [m]", 10, 1000, 250, 10)
    m = st.number_input("Aquifer thickness $M$ [m]", 2.0, 100.0, 10.0, 0.1)
    sigma = st.number_input("Distance between vertical wells σ [m]", 5, 500, 80, 5)
    
with columns[1]:
    r_d = st.number_input("Well radius $r_d$ [m]", 0.1, 5.0, 1.0, 0.1)
    intended_l = st.number_input("Intended screen length $l_{HCW}$ [m]", 10, 500, 300, 5)

# Range for l (length of horizontal collector well screens)
l_min = 0
l_max = 500


# Create array of l values
l_values = np.linspace(l_min, l_max, 200)
nc_values = []

for l in l_values:
    try:
        nc = calculate_nc(L, m, l, sigma, r_d)
        nc_values.append(nc)
    except ValueError:
        # Catch log domain errors
        nc_values.append(np.nan)

# Compute nc for intended length
try:
    nc_intended = calculate_nc(L, m, intended_l, sigma, r_d)
    nc_intended_rounded = math.ceil(nc_intended)
except ValueError:
    nc_intended = np.nan
    nc_intended_rounded = None

# Plot #1
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(l_values, nc_values, label="$n_c$ vs screen length",linewidth=3)
if not np.isnan(nc_intended):
    #ax.scatter([intended_l], [nc_intended], color='red', label=f"Intended l={intended_l} m, $n_c$ = {nc_intended:.2f}")
    ax.plot(intended_l, nc_intended, marker='o', markersize=10, markeredgecolor='black', markerfacecolor='red',label=f"Intended l={intended_l} m, $n_c$ = {nc_intended:.2f}")
ax.set_xlabel("HCW screen length l [m]", fontsize=14)
ax.set_ylabel("Number of wells $n_c$ [-]", fontsize=14)
ax.set_xlim(0, 500)
ax.set_ylim(0, 50)
ax.set_title("Number of vertical wells that can be replaced by a HCW", fontsize=16, pad=10)
ax.grid(True)
ax.legend(fontsize=14)

st.pyplot(fig)

# Show result
if not np.isnan(nc_intended):
    st.markdown(f"**Computed number of wells** (rounded up): **{nc_intended_rounded}**")
else:
    st.error("Invalid input: Check that the logarithm term is positive for the intended screen length.")
    
st.markdown("---")

# --- 2nd plot with variable aquifer thickness
st.subheader('Interactive plot 2 with variable aquifer thickness $M$', divider = 'blue')

show_2nd = st.toggle(':red[Toggle here] to **SHOW the influence of the AQUIFER THICKNESS on the computation**')

if show_2nd:
    # Re-Use the parameters but make the aquifer thickness the variable parameter and fix the HCW_screen_lenght to intended_l
    # Create array of m values
    
    # Input widgets
    st.markdown("""
    #### additional :green[INPUT parameters for plot 2]
    """)

    m2_min = 3
    m2_max = 100
    
    columns2 = st.columns((1,1))

    with columns2[0]:
        intended_m2 = st.number_input("Intended aquifer thickness $M$ [m]", 3, 100, 10, 1)
    
    m2_values = np.linspace(m2_min, m2_max, 200)
    nc2_values = []
    
    for m2 in m2_values:
        try:
            nc2 = calculate_nc(L, m2, intended_l, sigma, r_d)
            nc2_values.append(nc2)
        except ValueError:
            # Catch log domain errors
            nc2_values.append(np.nan)
        
    # Recompute for nc_intended_2nd 
    # Compute nc for intended length
    try:
        nc2_intended = calculate_nc(L, intended_m2, intended_l, sigma, r_d)
        nc2_intended_rounded = math.ceil(nc2_intended)
    except ValueError:
        nc2_intended = np.nan
        nc2_intended_rounded = None
    
    # Plot #1
    fig2, ax2 = plt.subplots(figsize=(8,5))
    ax2.plot(m2_values, nc2_values, label="$n_c$ vs aquifer thickness", color = 'green', linewidth=3)
    if not np.isnan(nc2_intended):
        #ax2.scatter([intended_m2], [nc2_intended], color='red', label=f"Intended M={intended_m2} m, $n_c$ = {nc2_intended:.2f}")
        ax2.plot(intended_m2, nc2_intended, marker='o', markersize=10, markeredgecolor='black', markerfacecolor='lightblue',label=f"Intended M={intended_m2} m, $n_c$ = {nc2_intended:.2f}"                )   
    ax2.set_xlabel("Aquifer thickness $M$ [m]", fontsize=14)
    ax2.set_ylabel("Number of wells $n_c$ [-]", fontsize=14)
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 50)
    ax2.set_title("Number of vertical wells that can be replaced by a HCW", fontsize=16, pad=10)
    ax2.grid(True)
    ax2.legend(fontsize=14)
    
    st.pyplot(fig2)
    
    # Show result
    if not np.isnan(nc_intended):
        st.markdown(f"**Computed number of wells (plot 2)** (rounded up): **{nc2_intended_rounded}**")
    else:
        st.error("Invalid input: Check that the logarithm term is positive for the intended screen length.")
        
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')