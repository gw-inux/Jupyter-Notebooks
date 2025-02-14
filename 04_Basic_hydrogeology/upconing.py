import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app title and description
# Developed by Markus Giese University of Gothenburg 2025

# Markdown description
st.markdown(r"""
### **Upconing of the Saltwater Interface**
This notebook demonstrate the principle of upconing (rise of saltwater) due to pumping. The notebook is based on an example from the INOWAS platform (https://www.inowas.com).

### **Introduction**  
#### **General Situation** 

Upconing of the saltwater interface can occur when the aquifer head is lowered by pumping from wells. Schmork and Mercado (1969) and Dagan and Bear (1968) developed equations to calculate upconing and determine the maximum well pumping rate at a new equilibrium caused by pumping. In these calculations, the pumping well is considered as a point.

The maximum upconing, which occurs directly underneath the pumping well, can be calculated as:

$$ 
z(0) = \frac{Q}{2 \pi d K \Delta \rho} 
$$

As a guideline, Dagan and Bear (1969) propose that the interface will remain stable if the upconed height ($z$) does not exceed the critical elevation, which is defined as one-third of $d$ (Callander et al., 2011). Based on this, the permitted pumping rate should not exceed:

$$ 
Q_{\text{max}} \leq \frac{0.6 \pi d^2 K}{\Delta \rho} 
$$

where
$$ 
\Delta \rho = \frac{\rho_s - \rho_f}{\rho_f} 
$$
and

- $z$ = new equilibrium elevation (distance between the upconed and original interface) [L],
- $Q$ = pumping rate [L³/T],
- $d$ = pre-pumping distance from base of well to interface [L],
- $K$ = hydraulic conductivity [L/T].

To calculate the upconing at any distance ($x$) from the well, the following equation can be used under steady-state conditions $( t \to \infty ) $ (Bear, 1999):

$$ 
z(x) = \left( \frac{1}{\sqrt{\frac{x^2}{d^2} + 1}} - \frac{1}{\sqrt{\frac{x^2}{d^2} + \left(1 + \frac{\Delta \rho K t}{n d (2 + \Delta \rho)}\right)^2}} \right) \frac{Q}{2 K \pi d \Delta \rho} 
$$

where

- $n$ = porosity [-],
- $t$ = time [T],
- $x$ = distance from the well [L].

#### **References**
Bear, J. (Ed.), 1999. Seawater intrusion in coastal aquifers: concepts, methods and practices, Theory and applications of transport in porous media. Kluwer, Dordrecht.

Callander, P., Lough, H., Steffens, C., 2011. New Zealand Guidelines for the Monitoring and Management of Sea Water Intrusion Risks on Groundwater. Pattle Delamore Partners LTD, New Zealand.

Schmork, S., Mercado, A., 1969. Upconing of Fresh Water-Sea Water Interface Below Pumping Wells, Field Study. Water Resources Research 5, 1290–1311. doi: 10.1029/WR005i006p01290

Dagan, G., Bear, J., 1968. Solving The Problem Of Local Interface Upconing In A Coastal Aquifer By The Method Of Small Perturbations. Journal of Hydraulic Research 6, 15–44. doi: 10.1080/00221686809500218

""", unsafe_allow_html=True)

# User inputs
def upconing(Q, K, d_pre, rho_f, rho_s, n):

    # Compute values
    t = np.inf
    x = np.arange(-1000, 1000, 0.25)
    z = (1/(x**2/d_pre**2+1)**0.5-1/(x**2/d_pre**2+(1+((rho_s - rho_f)/rho_f)*K*t/(n*d_pre*(2+(rho_s - rho_f)/rho_f)))**2)**0.5)* Q/(2*np.pi*d_pre*K*((rho_s - rho_f)/rho_f))
    z_0 = Q*(rho_f/(rho_s - rho_f))/(2*np.pi*d_pre*K)
    Q_max = (0.6*np.pi*d_pre**2*K)/(rho_f/(rho_s - rho_f))
    z_max = Q_max*(rho_f/(rho_s - rho_f))/(2*np.pi*d_pre*K)
    

    # Plot Glover equation results
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(x,z, color='darkblue', linewidth=2.5, label='Saltwater Interface')
    ax.fill_between(x,z,-2.5, facecolor='cornflowerblue', hatch = '//')
    ax.fill_between(x,z,max(z_0, d_pre +3), facecolor='lightskyblue', alpha=0.5)
    ax.hlines(z_max, -1000, 1000, color = 'red', linestyle = "dashed", label='Critical upconing elevation')
    ax.vlines(2.5, d_pre, max(z_0, d_pre +3), color = 'black', linestyle = "dashed", label = 'Pumping well')
    ax.vlines(-2.5, d_pre, max(z_0, d_pre +3), color = 'black', linestyle = "dashed")
    ax.set_xlabel('Distance from Well (m)')
    ax.set_ylabel('Height above initial water table (m)')
    ax.set_title("Upconing")
    ax.legend(loc="upper right")
    ax.grid()
    plt.text(100, -2, 'Saltwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
    plt.text(-750, 2.5, 'Freshwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
    
    st.write(f"**Maximum upconing:** {z_0:.2f} m")
    st.write(f"**Critical pumping rate:** {Q_max:.3f} m^3/d")
    st.write(f"**Critical upconing elevation:** {z_max:.2f} m")
    return fig 
    
# Streamlit UI
st.title("Upconing")

Q = st.slider("Freshwater Discharge (Q)", min_value=100, max_value=5000, step=10, value=1000)
K = st.slider("Hydraulic Conductivity (K)", min_value=1, max_value=100, step=1, value=50)
d_pre = st.slider("Pre-pumping distance (d_pre)", min_value=0.5, max_value=100.0, step=0.1, value=10.0)
rho_f = st.slider("Freshwater Density (ρ_f)", min_value=950, max_value=1050, step=1, value=1000)
rho_s = st.slider("Saltwater Density (ρ_s)", min_value=950, max_value=1050, step=1, value=1025)
n = st.slider("Porosity (n)", min_value=0.05, max_value=0.4, step=0.01, value=0.15)

fig = upconing(Q, K, d_pre, rho_f, rho_s, n)
st.pyplot(fig)

# Copyright
col1, col2 = st.columns([1, 5], gap = 'large')  # Adjust column width ratio
with col1:
    st.image('Jupyter-Notebooks/04_Basic_hydrology/FIGS/logo_iNUX.jpg', width=125)
with col2:
    st.markdown("© 2025 iNUX Project - Interactive understanding of groundwater hydrology and hydrogeology - An ERASMUS+ cooperation project.<br>App developer: Markus Giese (University of Gothenburg)", unsafe_allow_html=True)
