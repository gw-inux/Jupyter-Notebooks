import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc, erf
import math

# Authors, institutions, and year
year = 2025 
authors = {
    "Markus Giese": [1],  # Author 1 belongs to Institution 1
    "Thomas Reimann": [2],
    "Nils Wallenberg": [1]
}
institutions = {
    1: "University of Gothenburg, Department of Earth Sciences",
    2: "TU Dresden, Institute for Groundwater Management",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

module_path = ""

# Streamlit app title and description
# Markdown description

st.title("SeaLevelRise")

st.subheader('Sea Level Rise Impact on Aquifer Interface', divider= "green")


st.markdown(r"""
This interactive app demonstrate the effect of sealever rise. The notebook is based on an example from the INOWAS platform (https://www.inowas.com).

### **Introduction**  
#### **General Situation** 
According to Morgan and Werner (2016), the solution developed by Chesnaux (2015) is only valid for a fixed-location, no-flow boundary (fixed-flux) in a continental unconfined aquifer. Therefore, the geological limit of the aquifer is used as the inland boundary, and other cases such as a head-dependent boundary (e.g., through pumping, evapotranspiration, rivers, drains) are not considered. To assess the impact of sea level 

#### 1. Initial Position of the Freshwater-Saltwater Interface

The initial position of the toe of the freshwater-saltwater interface, $ x_T $, can be calculated using the following equation:

$$ x_T = \sqrt{L_0^2 - \left(\frac{z_0}{\alpha \beta}\right)^2} $$

with

$$ \alpha = \sqrt{\frac{W \Delta \rho}{K (\rho_f + \Delta \rho)}} \quad \text{and} \quad \beta = \frac{\rho_f}{\Delta \rho} $$

where:
- $ z_0 $ is the initial depth below sea level to the aquifer basement (impermeable bottom) [L],
- $ W $ is recharge of the aquifer [LT\(^{-1}\)],
- $ K $ is the hydraulic conductivity of the aquifer [LT\(^{-1}\)],
- $ L_0 $ is the initial width of the aquifer [L],
- $ \rho_f $ is freshwater density [ML\(^{-3}\)],
- $ \rho_s $ is seawater density [ML\(^{-3}\)],
- $ \Delta \rho = \rho_s - \rho_f $ is the density difference between fresh and saltwater.

##### 2. Fluctuation of Aquifer Height with Sea Level Change

The fluctuation of the height of the aquifer at any position $ x $ due to sea level changes can be calculated using the following equation:

$$ I(x) = \Delta z_0 + \sqrt{\frac{-\alpha^2 \Delta z_0}{\tan \theta} \left( 2L_0 - \frac{\Delta z_0}{\tan \theta} \right) + h_0(x)^2} - h_0(x) $$

where:
- $ x $ [L] is the inland distance from the position of the coastline,
- $ \theta $ is the slope of the coastal aquifer [°],
- $ h_0(x) $ is the initial water table at position $ x $ in the aquifer [L],
- $ \Delta z_0 $ is sea level change [L].

#### 3. Change in Position of the Sea Water Toe Due to Sea Level Changes

The change in position of the seawater toe due to sea level changes can be calculated as follows:

$$ \Delta x_T = \sqrt{\left( L_0 - \frac{\Delta z_0}{\tan \theta} \right)^2 - \left( \frac{z_0 + \Delta z_0}{\alpha \beta} \right)^2} - \sqrt{L_0^2 - \left( \frac{z_0}{\alpha \beta} \right)^2} $$

#### 4. Change of Fresh Water Resouces (Volume) Due to Sea Level Changes

The change of volume of aquifer ΔV during time t and per unit length of aquifer can be calculated as follows:

$$ \Delta V = S_t x_{Tt} - S_0 x_{T0} + \frac{\alpha \pi (1 + \beta)}{4} (L_t^2 - L_0^2) + \alpha \beta \left( x_{T0} \sqrt{L_0^2 + x_{T0}^2} - x_{Tt} \sqrt{L_t^2 + x_{Tt}^2} \right) $$

rise in fixed-head aquifers, the solution by Werner and Simmons (2009) (assuming a vertical cliff) or the more generalizable solution by Ataie-Ashtiani et al. (2013) can be used.
""", unsafe_allow_html=True)

with st.expander('**References**'):
    st.markdown(r"""
Bear, J. (Ed.), 1999. Seawater intrusion in coastal aquifers: concepts, methods and practices, Theory and applications of transport in porous media. Kluwer, Dordrecht.

""", unsafe_allow_html=True)

"---"

st.subheader('Computation')


# Initialize librarys


# Parameters
z0 = ...  # Initial depth below sea level [L]
W = ...   # Surface recharge [LT^-1]
K = ...   # Hydraulic conductivity [LT^-1]
L0 = ...  # Initial width of the aquifer [L]
rho_f = ...  # Freshwater density [ML^-3]
rho_s = ...  # Seawater density [ML^-3]
theta = ...  # Slope of coastal aquifer [degrees]
delta_z0 = ...  # Sea level change [L]
h0_x = ...  # Initial water table at position x [L]
n = ...          # Porosity

def land_surface(x, theta, xmin):
    return -np.tan(np.radians(theta)) * x + xmin

# 3.49 ersetzen mit irgendwas: xmax = z0/np.tan(np.radians(theta))

def sea_surface(x, theta):
    x = np.linspace(0, xmax, 1000)
    return np.tan(np.radians(theta)) * x

def sealevelrise(z0, W, K, L0, rho_f, rho_s, theta, delta_z0, h0_x, x):

    delta_rho = rho_s - rho_f
    alpha = ((W * delta_rho) / (K * (rho_f + delta_rho)))**0.5
    h_x = alpha*(L0**2 - x**2)**0.5
    z_x = (rho_f / delta_rho) * h_x
    beta = rho_f / delta_rho   
    x_T = (L0**2 - (z0 / (alpha * beta))**2)**0.5
    I_x = delta_z0 + ((-alpha**2 * delta_z0) / np.tan(np.radians(theta)) * (2 * L0 - delta_z0 / np.tan(np.radians(theta))) + h_x**2)**0.5 - h_x
    delta_x_T = ((L0 - (delta_z0/np.tan(np.radians(theta))))**2 -((z0 + delta_z0) / (alpha * beta))**2)**0.5 - (L0**2 - (z0/(alpha*beta))**2)**0.5
    delta_L = delta_z0/np.tan(np.radians(theta))
    inu = delta_L * np.tan(np.radians(theta))
#    h_new_x = alpha*(((L0-delta_z0/np.tan(np.radians(theta)))**0.5 - x**2)**0.5 - (L0**2-x**2)**0.5) 
#    h_new_x = delta_z0 + ((-alpha**2 * delta_z0) / np.tan(np.radians(theta)) * (2 * L0 - delta_z0 / np.tan(np.radians(theta))) + h_x**2)**0.5
    h_new_x = h_x + I_x
#    I_new_x = (rho_f / delta_rho) * (h_x - I_x)
    z_new_x = (rho_f / delta_rho) * (h_new_x- delta_z0)
    delta_V =  (z0+delta_z0) * (x_T-delta_x_T) - z0 * x_T + (alpha * np.pi * (1 + beta) / 4) * ((L0-delta_L)**2 - L0**2) + alpha * beta * (x_T * (L0**2 + x_T**2)**0.5 - (x_T-delta_x_T) * ((L0-delta_L)**2 + (x_T-delta_x_T)**2)*0.5)
    return h_x, z_x, x_T, I_x, delta_x_T, delta_L, h_new_x, z_new_x, delta_V 


# including total porosity allows converting aquifer volume to freshwater volume 

z0=50
W=0.0014
K=10
L0=1000
rho_f=1000
rho_s=1025
theta=2
delta_z0=st.slider('Sea Level rise in m', 0.01, 7.6, 0.1, 0.01)
h0_x=1
n = 0.2

x_land = np.linspace(0, L0, 10000) 
xmax = z0/np.tan(np.radians(theta))
xmin = L0*np.tan(np.radians(theta))
x_sea = np.linspace(L0, L0 +xmax , 1000)
y_land = land_surface(x_land, theta, xmin)
y_sea = sea_surface(x_sea, theta)
h_x, z_x, x_T, I_x, delta_x_T, delta_L, h_new_x, z_new_x, delta_V = sealevelrise(z0, W, K, L0, rho_f, rho_s, theta, delta_z0, h0_x, x_land)
delta_FWV = delta_V*n
inundation = np.linspace(L0-delta_L, L0, 100)
    
new_sealevel = np.piecewise(
    x_land,
    [x_land < L0 - delta_L, x_land >= L0 - delta_L],
    [-z0, lambda x: land_surface(x, theta, xmin)]
)

    # PLOT FIGURE - needs to be fixed/extended
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)

# Freshwater heads
ax.plot(x_land, h_x, color = 'skyblue', linestyle=':')
ax.plot(x_land, h_new_x, color = 'skyblue')
# Interface
ax.plot(x_land,-z_x, color = 'red', linestyle=':')
ax.plot(x_land,-z_new_x + delta_z0 , color = 'red')
# Diagonal lines (?)
ax.plot(x_sea, -y_sea, c="black")
ax.plot(x_land, y_land, c="black")

ax.fill_between(x_land,h_x,h_new_x, facecolor='lightblue', alpha= 0.5)

ax.hlines(-z0, 0, L0+xmax, color = 'black', linewidth = 5) # Bottom of the plot
ax.hlines(0, L0, L0+xmax, color='black', linestyle=':')     # Original sea level
ax.hlines(delta_z0, L0-delta_L, L0 + xmax, color='blue')   # new sea level

ax.fill_between(x_land, -z_x, -z0, facecolor='cornflowerblue', hatch = '//')
ax.fill_between(x_sea-1, -y_sea, -z0, facecolor='cornflowerblue', hatch = '//')

ax.fill_between(x_sea, 0, -y_sea, facecolor='royalblue')
ax.fill_between(x_sea, delta_z0, 0, facecolor='royalblue', alpha=0.5)

ax.fill_between(x_land, delta_z0, np.maximum(y_land,0), facecolor='royalblue', alpha=0.5, where=(x_land >= L0-delta_L))

ax.fill_between(x_land, np.maximum(-z_new_x + delta_z0, -z_x), -z_x, facecolor='red', alpha=0.5, hatch='//')
ax.fill_between(x_land, np.maximum(new_sealevel, -z_x), -z_x, facecolor='red', alpha=0.5, hatch='//')

ax.fill_between(x_land, 0, h_x, facecolor='lightskyblue', alpha=0.5)
ax.fill_between(x_land, 0, -z_x, facecolor='lightskyblue', alpha=0.5)
#plt.text(-z0, L0 + xmax, 'θ', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(1180, -20, 'Sea', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(1180, -80, 'Saltwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(150, -10, 'Freshwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
ax.set(xlabel='x [m]', ylabel='head [m]',title='Sea level rise')
plt.ylim(-z0, 15)
plt.xlim(0,L0 + xmax)

st.pyplot(fig)

st.write("Initial position of interface toe:", x_T, "m")
st.write("Change of interface toe position:", delta_x_T, "m")
st.write("Loss of width of aquifer:", delta_L, "m")
st.write("Change of aquifer volume:", delta_V, "m**3")
st.write("Change of freshwater volume:", delta_FWV, "m**3")

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image(module_path + 'images/CC_BY-SA_icon.png')
