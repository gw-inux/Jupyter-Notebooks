import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app title and description
st.markdown(r"""
### **Ghyben-Herzberg Relation**  
The Ghyben-Herzberg relation approximates the location of the interface between fresh and saltwater under static hydraulic conditions.

### **Introduction**  
#### **General Situation**  
The Ghyben-Herzberg relation describes the equilibrium relationship between fresh groundwater and underlying seawater in coastal aquifers. Due to the density difference between freshwater and seawater, a lens of fresh groundwater floats above the denser saltwater.

This relation can be expressed as:  

$$
z = \frac{\rho_f}{\rho_s - \rho_f} h
$$

where:  
- \( z \) is the depth of the freshwater-saltwater interface below sea level,  
- \( h \) is the height of the freshwater table above sea level,  
- \( $\rho_f$ \) is the density of freshwater (approximately \( 1000 \, kg/m^3 \)),  
- \( $\rho_s$ \) is the density of seawater (approximately \( 1025 \, kg/m^3 \)).  

For typical values, this relation simplifies to:  

$$
z \approx 40h
$$

This means that for every meter of freshwater head above sea level, the freshwater-saltwater interface extends approximately **40 meters** below sea level.
""", unsafe_allow_html=True)

def ghyben_herzberg(hl, rho_f, rho_s):
    x = np.arange(0, 1000, 0.1)
    h = (hl**2 - (hl**2 - 0**2) / 1000 * x) ** 0.5
    z = (rho_f / (rho_s - rho_f)) * h

    # Calculate landscape geometry
    plot_x = np.append(np.arange(0, 2000, 10), 2000)
    norm_x = np.linspace(-5, 5, len(plot_x))
    plot_x = plot_x[:121]
    plot_y = np.arctan(1 / norm_x)
    plot_y[norm_x < 0] = plot_y[norm_x < 0] + np.pi
    scale = (10 - -10) / (np.max(plot_y) - np.min(plot_y))
    offset = -10 - plot_y[-1] * scale
    plot_y = plot_y * scale + offset
    plot_y = plot_y[:121]

    # Plot figure
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(x, h, color='skyblue', label="Freshwater Head")
    ax.plot(x, -z, color='red', linewidth=2.5, label="Saltwater Interface")
    ax.hlines(0, 1000, 1200, color='blue')
    ax.fill_between(x, 0, h, facecolor='lightblue', alpha=0.6)
    ax.fill_between(x, 0, -z, facecolor='lightblue', alpha=0.4)
    ax.plot(plot_x, plot_y, c="black")
    ax.fill_between(x, -z, np.min(-z), facecolor='blue')
    ax.fill_between(np.append(999, 1200), 0, np.min(-z), facecolor='blue')
    ax.set_xlabel("x [m]")
    ax.set_ylabel("Head [m]")
    ax.set_title("Ghyben-Herzberg Theorem")
    ax.legend()
    
    return fig

# Streamlit UI
st.title("Ghyben-Herzberg Theorem")

hl = st.slider("Freshwater head (h)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
rho_f = st.number_input("Freshwater Density ($ρ_f$)", min_value=950, max_value=1050, value=1000, step=1)
rho_s = st.number_input("Saltwater Density ($ρ_s$)", min_value=950, max_value=1050, value=1025, step=1)

fig = ghyben_herzberg(hl, rho_f, rho_s)
st.pyplot(fig)
