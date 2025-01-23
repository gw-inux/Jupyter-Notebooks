import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
from scipy import special
import numpy as np
import streamlit as st

st.title('3D Transport with advection and dispersion')
st.subheader('Tracer input as :green[Dirac Pulse] data', divider="green")

columns1 = st.columns((1,1,1), gap = 'large')
with columns1[1]:
    theory = st.button('Show theory')
    
if theory:
    st.latex(r'''C(x = vt + X, y = Y, z = Z) = \frac{M}{8 (\pi t)^{\frac{3}{2}} \sqrt{D_x D_y D_z}} \exp ( - ( \frac{X^2}{4 D_x t} + \frac{Y^2}{4 D_y t} + \frac{Z^2}{4 D_z t})''')


st.markdown("""
            ### About the computed situation
            
            Transport is considered for a 3D system with steady groundwater flow with a specific discharge _q_ of 0.016 m/s. The average velocity is depending on the porosity and printed below the interactive plot.
            
            The solutes are added by an Dirac pulse with a mass of 10 gramms.
            
            The plot shows the solute concentration for advective-dispersive transport. The isolines of equal concentration are computed for a horizontal-plane view (x-y plot). The z-value of the y-y slice can be modified with the sliders above the plot.
""", unsafe_allow_html=True
)
"---"

#FUNCTIONS FOR COMPUTATION; ADS = ADVECTION, DISPERSION AND SORPTION - EVENTUALLY SET RETARDATION TO 1 FOR NO SORPTION

# Define the function
def concentration(X, Y, Z, t, M, ax, ay, az, v):
    Dx = v * ax
    Dy = v * ay
    Dz = v * az
    
    if t == 0:
        return np.zeros_like(X)  # Avoid division by zero
    
    coeff = M / (8 * (np.pi * t) ** (3/2) * np.sqrt(Dx * Dy * Dz))
    
    exponent = -(((X- v * t)**2) / (4 * Dx * t) + (Y**2) / (4 * Dy * t) + (Z**2) / (4 * Dz * t))
    
    return coeff * np.exp(exponent)
    
columns1 = st.columns((1,1,1), gap = 'large')

with columns1[0]:
    t = st.slider(f'**Time for the concentration profile (s)**',1.,1800.,1.,1.)
    Zp = st.slider(f'**Slice at z (top view plot)**',-25,25,1,1)
    Yp = st.slider(f'**Slice at y (side view plot)**',-100,100,0,1)
    
with columns1[1]:
    #M = st.slider(f'**Input mass (g)**',0.01,5.0,1.0,0.01)  
    n = st.slider(f'**Porosity (-)**',0.01,0.6,0.25,0.01)    
    ax = st.slider(f'**Longitudinal (x) dispersivity (m)**',0.001,1.0,0.01,0.001)
    rat_x_y = st.slider(f'**Dispersivity ratio 1/n for x/y**',1,100,10,1)
    rat_x_z = st.slider(f'**Dispersivity ratio 1/n for x/z**',1,500,100,1)
with columns1[2]:
    isolines = st.toggle("Show isosurfaces instead of isolines")
    
M = 10
v = 0.016/n
ay = ax/rat_x_y
az = ax/rat_x_z

# Grid for X and Y
xmax = 1000
ymax = 100
zmax = 25
X_vals = np.linspace(-0.05*xmax, xmax, 300)
Y_vals = np.linspace(-ymax, ymax, 300)
Z_vals = np.linspace(-zmax, zmax, 300)
Xxy, Yxy = np.meshgrid(X_vals, Y_vals)
Xxz, Zxz = np.meshgrid(X_vals, Z_vals)

# Compute concentration values
Cxy =    concentration(Xxy, Yxy, Zp, t, M, ax, ay, az, v)
Cxz =    concentration(Xxz, Yp, Zxz, t, M, ax, ay, az, v)

# Plot the concentration field
lev_exp = 10.**np.arange(-12, 1)

fig = plt.figure(figsize=(16,8))
gs = matplotlib.gridspec.GridSpec(3,2, width_ratios=[8,1.1], height_ratios=[4,0.2,1])

ax = fig.add_subplot(gs[0,:])
ax.plot(0,0, marker='o', color='r',linestyle ='None', label='Source of contamination')
if isolines:
    contour = plt.contourf(Xxy, Yxy, Cxy, lev_exp, locator=ticker.LogLocator())
else:
    contour = plt.contour(Xxy, Yxy, Cxy, lev_exp, locator=ticker.LogLocator())
plt.colorbar(contour, label="Concentration (g/m3)", format='%.0e')
plt.xlabel("x in m",fontsize=14)
plt.ylabel("y in m",fontsize=14)
plt.xlim(-0.05*xmax,xmax)
plt.legend(fontsize=14)
plt.title(f"Contaminant Concentration (top view) at t = {t}, z = {Zp}", fontsize=16)

ax = fig.add_subplot(gs[2,0])
ax.plot(0,0, marker='o', color='r',linestyle ='None', label='Source of contamination')
if isolines:
    contour2 = plt.contourf(Xxz, Zxz, Cxz, lev_exp, locator=ticker.LogLocator())
else:
    contour2 = plt.contour(Xxz, Zxz, Cxz, lev_exp, locator=ticker.LogLocator())
plt.xlabel("x in m",fontsize=14)
plt.ylabel("z in m",fontsize=14)
plt.xlim(-0.05*xmax,xmax)
plt.title(f"Contaminant Concentration (side view) at t = {t}, y = {Yp}", fontsize=16)

st.pyplot(fig)