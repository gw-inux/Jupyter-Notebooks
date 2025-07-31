import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("Horizontal Collector Well Replacement Calculator")
st.subheader('Online calculator', divider = 'blue')

st.markdown("""
### 💧 Horizontal Collector Well Replacement Calculator

This tool computes how many vertical wells can be replaced by a horizontal collector well based on hydraulic and geometric input parameters. The formula below is used for the computation:

""")

st.latex(r"""
n_c = \frac{ \frac{\pi L}{\sigma} + \ln\left( \frac{\sigma}{2\pi r_d} \right) }
           { \ln L - \ln\left( \left(0.25 + 0.005 \frac{L}{m} \right) l - 0.6 m \right) }
""")
st.markdown(r"""
**Parameter definitions**  
- $L$ – Hydraulic distance to the boundary (e.g., river, MAR basin) [m]  
- $m$ – Aquifer thickness (GWL thickness) [m]  
- $l$ – Length of the horizontal collector well screen [m]  
- $\sigma$ – Spacing between vertical wells in the gallery [m]  
- $r_d$ – Effective radius of well influence (common for both well types) [m]  
- $n_c$ – Number of vertical wells replaced by one horizontal collector well [-]

**Reference**  
Weregin, N. N. (1962): *Luchevye vodozabory dlja vodosnabzhenija gorodov i promyshlennosti*.  
Isdatelstvo kommunalnogo khozjaistva RFSR, Moscow.
""")


# Input widgets
st.subheader('Parameter input', divider = 'blue')
L = st.number_input("Hydraulic distance to boundary (L) [m]", 10, 1000, 250, 10)
m = st.number_input("Aquifer thickness (m) [m]", 2.0, 100.0, 10.0, 0.1)
sigma = st.number_input("Distance between vertical wells (σ) [m]", 5, 500, 80, 5)
r_d = st.number_input("Well radius $r_d$ [m]", 0.1, 5.0, 1.0, 0.1)

# Range for l (length of horizontal collector well screens)
l_min = 0
l_max = 500
intended_l = st.number_input("Intended screen length (l) [m]", 10, 500, 300, 5)

# Define function for nc
def calculate_nc(L, m, l, sigma, r_d):
    numerator = (math.pi * L / sigma) + math.log(sigma / (2 * math.pi * r_d))
    denominator = math.log(L) - math.log((0.25 + 0.005 * L / m) * l - 0.6 * m)
    return numerator / denominator

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

# Plot
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(l_values, nc_values, label="$n_c$ vs screen length")
if not np.isnan(nc_intended):
    ax.scatter([intended_l], [nc_intended], color='red', label=f"Intended l={intended_l} m, $n_c$ = {nc_intended:.2f}")
ax.set_xlabel("HCW screen length l [m]", fontsize=14)
ax.set_ylabel("Number of wells $n_c$ [-]", fontsize=14)
ax.set_xlim(0, 500)
ax.set_ylim(0, 50)
ax.set_title("Number of vertical wells that can be replaced by a HCW", fontsize=16, pad=10)
ax.grid(True)
ax.legend(fontsize=14)

st.markdown('---')
st.pyplot(fig)

# Show result
if not np.isnan(nc_intended):
    st.markdown(f"### Computed number of wells (rounded up): **{nc_intended_rounded}**")
else:
    st.error("Invalid input: Check that the logarithm term is positive for the intended screen length.")
