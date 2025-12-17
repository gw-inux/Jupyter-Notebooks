import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#TO DO:
# - Description
# - Slider
# - Plot
# - Purpose (compare different soil etc.)

# Streamlit app title and description
# Developed by Markus Giese University of Gothenburg 2025

# Authors, institutions, and year
year = 2025 
authors = {
    "Markus Giese": [1],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "University of Gothenburg, Department of Earth Sciences",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# Markdown description
st.title('Mualem Equation')
st.subheader('Describing unsaturated hydraulic conductivity as a function of soil suction', divider="black")
st.markdown(r"""
### **Introduction**  
The Mualem equation describes the relationship between the unsaturated hydraulic conductivity $k(\psi)$ and the soil water retention curve. It links how easily water moves through partially saturated soil to how much water the soil holds at a given pressure (matric potential), usually using effective saturation as a bridge between the two. In practice, it is often combined with a retention model such as the van Genuchten curve, so that both 
$𝜃(𝜓)$ and $k(ψ)$ are described consistently with a shared set of parameters. The Mualem formulation includes a parameter (commonly denoted $L$) that accounts for how complex pore pathways become as the soil dries, making it a widely used foundation for modelling unsaturated flow in hydrology and soil physics.

The equation is given by:  

$$
k(\psi) = k_s S_e^{0.5} \left( 1 - \left( 1 - S_e^{1/m} \right)^m \right)^2
$$

with 
$$
m = 1 - 1/n
$$

where:
- $k(\psi)$ is the hydraulic conductivity at suction pressure \( \psi \),
- $k_s$ is the saturated hydraulic conductivity,
- $S_e$ is the effective saturation,
- $n$ is an empirical parameter.

The effective saturation $S_e$ is defined as:  

$$
S_e = \frac{1}{(1 + (\alpha |\psi|)^n)^m}
$$

where:
- $\alpha$ is another empirical parameter.
""", unsafe_allow_html=True)
st.subheader('Interactive Plot and Exercise', divider="black")
# User inputs for Mualem equation
alpha = st.slider("α (1/cm)", min_value=0.008, max_value=0.145, step=0.001, value=0.075)
n = st.slider("n (dimensionless)", min_value=1.09, max_value=2.68, step=0.01, value=1.89)
k_s = st.slider("Saturated Hydraulic Conductivity \( $k_s$ \) (cm/day)", min_value=4.5, max_value=715.0, step=5.0, value=105.0)

# Convert units
alpha = alpha * 100  # Convert cm⁻¹ to m⁻¹
k_s = k_s / (100 * 24 * 60 * 60)  # Convert cm/day to m/s

# Compute Mualem equation
psi_values = np.logspace(-2, 4, 500)
m = 1 - 1/n
S_e = 1 / (1 + (alpha * np.abs(psi_values))**n)**m
k_psi = k_s * S_e**0.5 * (1 - (1 - S_e**(1/m))**m)**2

# Plot Mualem results
fig, ax = plt.subplots(figsize=(10, 6))
ax.loglog(psi_values, k_psi, label='Hydraulic Conductivity $k(\psi)$')
ax.set_xlabel('Suction Pressure (Matric Potential) $\psi$ (m)')
ax.set_ylabel('Hydraulic Conductivity $k(\psi)$ (m/s)')
ax.set_title('Mualem Equation')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend()
st.pyplot(fig)

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')


