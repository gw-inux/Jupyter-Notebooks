import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app title and description
# Developed by Markus Giese University of Gothenburg 2025

# Markdown description

st.title("Upconing")

st.subheader('Upconing of the Saltwater Interface', divider= "blue")


st.markdown(r"""
This interactive app demonstrate the principle of upconing (rise of saltwater) due to pumping. The notebook is based on an example from the INOWAS platform (https://www.inowas.com).

### **Introduction**  
#### **General Situation** 

Upconing of the saltwater interface can occur when the aquifer (freshwater) head is lowered by pumping from wells. Schmork and Mercado (1969) and Dagan and Bear (1968) developed equations to calculate upconing and determine the maximum well pumping rate at a new equilibrium caused by pumping. In these calculations, the pumping well is considered as a point.

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
""", unsafe_allow_html=True)

with st.expander('**References**'):
    st.markdown(r"""
Bear, J. (Ed.), 1999. Seawater intrusion in coastal aquifers: concepts, methods and practices, Theory and applications of transport in porous media. Kluwer, Dordrecht.

Callander, P., Lough, H., Steffens, C., 2011. New Zealand Guidelines for the Monitoring and Management of Sea Water Intrusion Risks on Groundwater. Pattle Delamore Partners LTD, New Zealand.

Schmork, S., Mercado, A., 1969. Upconing of Fresh Water-Sea Water Interface Below Pumping Wells, Field Study. Water Resources Research 5, 1290–1311. doi: 10.1029/WR005i006p01290

Dagan, G., Bear, J., 1968. Solving The Problem Of Local Interface Upconing In A Coastal Aquifer By The Method Of Small Perturbations. Journal of Hydraulic Research 6, 15–44. doi: 10.1080/00221686809500218
""", unsafe_allow_html=True)

"---"

st.subheader('Computation')

# User inputs
def upconing(x, Q, K, d_pre, rho_f, rho_s, n):

    # Compute values
    t = np.inf
    z = (1/(x**2/d_pre**2+1)**0.5-1/(x**2/d_pre**2+(1+((rho_s - rho_f)/rho_f)*K*t/(n*d_pre*(2+(rho_s - rho_f)/rho_f)))**2)**0.5)* Q/(2*np.pi*d_pre*K*((rho_s - rho_f)/rho_f))
    z_0 = Q*(rho_f/(rho_s - rho_f))/(2*np.pi*d_pre*K)
    Q_max = (0.6*np.pi*d_pre**2*K)/(rho_f/(rho_s - rho_f))
    z_max = Q_max*(rho_f/(rho_s - rho_f))/(2*np.pi*d_pre*K)
    
    return z, z_0, Q_max, z_max
   
# Parameter / Input

x = np.arange(-1000, 1000, 0.25)

lc1, rc1 = st.columns((1,1), gap = 'large')
with lc1:
    with st.expander('System parameters'):
        rho_f = st.slider("Freshwater Density ($\rho_f$) in kg/m³", min_value=950, max_value=1050, step=1, value=1000)
        rho_s = st.slider("Saltwater Density ($\rho_s$) in kg/m³", min_value=950, max_value=1050, step=1, value=1025)
with rc1:
    with st.expander('Hydrogeologic parameters'):
        K = st.slider("Hydraulic Conductivity (K) in m/d", min_value=1, max_value=100, step=1, value=50)
        n = st.slider("Porosity (n)", min_value=0.05, max_value=0.4, step=0.01, value=0.15)
    d_pre = st.slider("Pre-pumping distance ($d_{pre}$) in m", min_value=0.5, max_value=100.0, step=0.1, value=10.0)
    Q = st.slider("Freshwater Discharge (pumping rate) ($Q$) in m³/d", min_value=0, max_value=5000, step=10, value=100)
   
z, z_0, Q_max, z_max = upconing(x, Q, K, d_pre, rho_f, rho_s, n)

# Plot Glover equation results
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(x,z, color='darkblue', linewidth=2.5, label='Saltwater Interface')
plt.ylim(-5, d_pre+3)
plt.xlim(-1000, 1000)
ax.fill_between(x,z,-5, facecolor='cornflowerblue', hatch = '//')
ax.fill_between(x,z,max(z_0, d_pre +3), facecolor='lightskyblue', alpha=0.5)
ax.hlines(z_max, -1000, 1000, color = 'red', linestyle = "dashed", label='Critical upconing elevation')
ax.vlines(0, d_pre, max(z_0, d_pre +3), linewidth=10, color = 'darkgrey')
ax.vlines(2, d_pre+0.1, max(z_0, d_pre +3), linewidth=2, color = 'silver')
ax.hlines(d_pre+2,-15, 15, color = 'grey')
ax.hlines(d_pre+1.5,-15, 15, color = 'grey')
ax.hlines(d_pre+1,-15, 15, color = 'grey')
ax.hlines(d_pre+0.5,-15, 15, color = 'grey')
ax.set_xlabel('Distance from Well (m)')
ax.set_ylabel('Height above initial water table (m)')
ax.set_title("Upconing")
ax.legend(loc="upper right")
#ax.grid()
plt.text(-100, d_pre+1, 'Pumping well', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(0, -3, 'Saltwater', horizontalalignment='center', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(-950, 2.5, 'Freshwater', horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
    
st.pyplot(fig)
    
st.write(f"**Maximum upconing:** {z_0:.2f} m")
st.write(f"**Critical pumping rate:** {Q_max:.3f} m³/d")
st.write(f"**Critical upconing elevation:** {z_max:.2f} m")



# Copyright
col1, col2 = st.columns([1, 5], gap = 'large')  # Adjust column width ratio
with col1:
    st.image('04_Basic_hydrogeology/FIGS/logo_iNUX.jpg', width=125)
with col2:
    st.markdown("© 2025 iNUX Project - Interactive understanding of groundwater hydrology and hydrogeology - An ERASMUS+ cooperation project.<br>App developer: Markus Giese (University of Gothenburg)", unsafe_allow_html=True)
