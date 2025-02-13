import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app title and description
# Developed by Markus Giese University of Gothenburg 2025

st.title('The Ghyben-Herzberg Relation')

st.subheader('Describing the :blue[freshwater-saltwater interface] under static hydraulic conditions', divider="blue")

st.markdown(r"""
### **Introduction**  
The Ghyben-Herzberg relation describes the equilibrium relationship between fresh groundwater and underlying seawater in coastal aquifers. Due to the density difference between freshwater and seawater, a lens of fresh groundwater floats above the denser saltwater, see the following figure.
""", unsafe_allow_html=True)

lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('04_Basic_hydrogeology/FIGS/Saltwater_intrusion_en.png', caption="Conceptual sketch of the fresh-water saltwater interface under hydrostatic conditions (Barlow 2003)[https://pubs.usgs.gov/circ/2003/circ1262/].")

st.markdown(r"""
This relation can be expressed as:  

$$
z = \frac{\rho_f}{\rho_s - \rho_f} h
$$

where:  
- \( z \) is the depth of the freshwater-saltwater interface below sea level,  
- \( h \) is the height of the freshwater table above sea level,  
- \( $\rho_f$ \) is the density of freshwater (approximately \( 1000 \, kg/m³ \)),  
- \( $\rho_s$ \) is the density of seawater (approximately \( 1025 \, kg/m³ \)).  

For typical values, this relation simplifies to:  

$$
z \approx 40h
$$

This means that for every meter of freshwater head above sea level, the freshwater-saltwater interface extends approximately **40 meters** below sea level.
""", unsafe_allow_html=True)

def land_surface(x, p):
    """Quadratische Funktion, die von y=10 (bei x=0) auf y=0 (bei x=1000) fällt. The exponent defines the shape"""
    return 10 * (1 - (x / 1000)**p)

def sea_surface(x, p):
    """Erzeugt eine gekrümmte ansteigende Funktion von (1000,0) bis (1200,30) mit starkem Anfangsgradient."""
    return 50 * (1 - ((1200 - x) / 200) ** p)*-1

def ghyben_herzberg(hl, rho_f, rho_s, x):
    h = (hl**2 - (hl**2 - 0**2) / 1000 * x) ** 0.5
    z = (rho_f / (rho_s - rho_f)) * h
    return h, z
    
ymin = -200 # lower value for plotting

# User defined input

lc1, rc1 = st.columns((1,1), gap = 'large')
with lc1:
    rho_f = st.number_input("Freshwater Density ($ρ_f$ in kg/m³)", min_value=950, max_value=1050, value=1000, step=1)
    rho_s = st.number_input("Saltwater Density ($ρ_s$)in kg/m³", min_value=950, max_value=1050, value=1025, step=1)
with rc1:
    hl = st.slider("Freshwater head at x = 0 ($h$) in m a.s.l.", min_value=0.1, max_value=8.0, value=5.0, step=0.1)
    
# Calculation

x_land = np.linspace(0, 1000, 500)   
x_sea = np.linspace(1000, 1200, 200)
y_land = land_surface(x_land, 4)
y_sea = sea_surface(x_sea, 1.5)
h, z = ghyben_herzberg(hl, rho_f, rho_s, x_land)



# Plot figure
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(x_land, h, color='steelblue', lw = 1.0, label="Freshwater Head")
ax.plot(x_land, y_land, c="black")
ax.plot(x_sea, y_sea, c="black")
ax.plot(x_land, x_land*0, c="royalblue",linestyle=':')
ax.plot(x_land, -z, color='darkblue', linewidth=2.5, label="Saltwater Interface")
ax.hlines(0, 1000, 1200, color='blue')

ax.fill_between(x_land, h, y_land, facecolor='wheat', alpha=1.0)   #unsaturated zone

ax.fill_between(x_land, 0, h, facecolor='lightskyblue', alpha=0.5)  #filling fresh water below sea
ax.fill_between(x_land, 0, -z, facecolor='lightskyblue', alpha=0.5) #filling fresh water below sea

ax.fill_between(x_land, -z, ymin, facecolor='cornflowerblue', hatch = '//') # salty aquifer land
ax.fill_between(x_sea-1, y_sea, ymin, facecolor='cornflowerblue', hatch = '//')   # salty aquifer sea
ax.fill_between(x_sea-1, 0, y_sea, facecolor='royalblue')   # sea
ax.set_xlabel("x [m]",fontsize=14)
plt.ylim(ymin,20)
plt.xlim(0,1200)
ax.set_ylabel("hydraulic head [m]",fontsize=14)
ax.set_title("Freshwater-Saltwater Interface",fontsize=16)
ax.legend(loc = 'lower right', fontsize=12)
plt.text(1180, -20, 'Sea', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(1180, -80, 'Saltwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(150, -10, 'Freshwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
    
st.pyplot(fig)
