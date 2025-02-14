import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Markdown description
st.markdown(r"""
### **Mualem Equation**  
The Mualem equation describes the relationship between the unsaturated hydraulic conductivity \( $k(\psi)$ \) and the soil water retention curve.

This equation is given by:  

$$
k(\psi) = k_s S_e^{0.5} \left( 1 - \left( 1 - S_e^{1/m} \right)^m \right)^2
$$

with 
$$
m = 1 - 1/n
$$

where:
- \( $k(\psi)$ \) is the hydraulic conductivity at suction pressure \( \psi \),
- \( $k_s$ \) is the saturated hydraulic conductivity,
- \( $S_e$ \) is the effective saturation,
- \( n \) is an empirical parameter.

The effective saturation \( $S_e$ \) is defined as:  

$$
S_e = \frac{1}{(1 + (\alpha |\psi|)^n)^m}
$$

where:
- \( $\alpha$ \) is another empirical parameter.
""", unsafe_allow_html=True)

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
