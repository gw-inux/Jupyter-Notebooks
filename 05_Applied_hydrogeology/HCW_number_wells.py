import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("Horizontal Collector Well Replacement Calculator")

# Input widgets
L = st.number_input("Hydraulic distance to boundary (L) [m]", 10, 1000, 200, 10)
m = st.number_input("Aquifer thickness (m) [m]", 2.0, 100.0, 10.0, 0.1)
sigma = st.number_input("Distance between vertical wells (σ) [m]", 5, 500, 50, 5)
r_d = st.number_input("Well radius $r_d$ [m]", 0.1, 5.0, 1.0, 0.1)

# Range for l (length of horizontal collector well screens)
l_min = 0
l_max = 500
intended_l = st.number_input("Intended screen length (l) [m]", 10, 500, 50, 5)

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
ax.set_xlabel("Screen length l [m]")
ax.set_ylabel("Number of wells n_c [-]")
ax.set_xlim(0, 500)
ax.set_ylim(0, 30)
ax.grid(True)
ax.legend()

st.pyplot(fig)

# Show result
if not np.isnan(nc_intended):
    st.markdown(f"### Computed number of wells (rounded up): **{nc_intended_rounded}**")
else:
    st.error("Invalid input: Check that the logarithm term is positive for the intended screen length.")
