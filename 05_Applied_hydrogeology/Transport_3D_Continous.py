import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
from scipy import special
import numpy as np
import streamlit as st

st.title('3D Transport with advection and dispersion')
st.subheader('Tracer input as :orange[Continous injection]', divider="orange")

columns1 = st.columns((1,1,1), gap = 'large')
with columns1[1]:
    theory = st.button('Show theory')
    
if theory:
#    st.latex(r'''C(x = vt + X, y = Y, z = Z) = \frac{M}{8 (\pi t)^{\frac{3}{2}} \sqrt{D_x D_y D_z}} \exp ( - ( \frac{X^2}{4 D_x t} + \frac{Y^2}{4 D_y t} + \frac{Z^2}{4 D_z t})''')
     st.latex(r""" C(x,y,z,t) = \frac{C_0}{8}\left(\operatorname{erfc}\left( \frac{x - v_x t}{2\sqrt{D_x t}} \right) \left( \operatorname{erf} \left( \frac{y + \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right)  - \operatorname{erf} \left(\frac{y - \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right)\right)\left(\operatorname{erf} \left( \frac{z + \frac{Z}{2}}{2 \sqrt{D_z \frac{x}{v}}} \right)-\operatorname{erf} \left( \frac{z - \frac{Z}{2}}{2 \sqrt{D_z \frac{x}{v}}}\right)\right)\right)""")


st.markdown("""
            ### About the computed situation
            
            Transport is considered for a 3D system with steady groundwater flow with a specific discharge _q_ of 0.016 m/s. The average velocity is depending on the porosity and printed below the interactive plot.
            
            The solutes are constantly added at the source with C0.
            
            The plot shows the solute concentration for advective-dispersive transport. The isolines of equal concentration are computed for a horizontal-plane view (x-y plot). The z-value of the y-y slice can be modified with the sliders above the plot.
""", unsafe_allow_html=True
)
"---"

#FUNCTIONS FOR COMPUTATION; ADS = ADVECTION, DISPERSION AND SORPTION - EVENTUALLY SET RETARDATION TO 1 FOR NO SORPTION

# Define the function
def concentration(Y, Z, x, y, z, t, ax, ay, az, v, C0, down_only):
    Dx = v * ax
    Dy = v * ay
    Dz = v * az
    
    if t == 0:
        return np.zeros_like(X)  # Avoid division by zero
    
    coeff = C0/8
    
    erf1 = special.erfc((x-v*t)/(2*np.sqrt(Dx*t)))
    erf2 = special.erf((y+Y/2)/(2*np.sqrt(Dy*x/v)))
    erf3 = special.erf((y-Y/2)/(2*np.sqrt(Dy*x/v)))
    if down_only:
        erf4 = special.erf((z+Z)/(2*np.sqrt(Dz*x/v)))
        erf5 = special.erf((z-Z)/(2*np.sqrt(Dz*x/v)))
    else:
        erf4 = special.erf((z+Z/2)/(2*np.sqrt(Dz*x/v)))
        erf5 = special.erf((z-Z/2)/(2*np.sqrt(Dz*x/v)))
    
    return coeff * (erf1*(erf2-erf3)*(erf4-erf5))
    
columns1 = st.columns((1,1,1), gap = 'large')

with columns1[0]:
    with st.expander("Here you find widgets to :red[**adjust the inlet boundary**]"): 
        C0 = st.slider(f'**Source concentration (g/m3)**',1,100,10,1) 
        Y  = st.slider(f'**Source width (m)**',1,100,10,1)   
        Z  = st.slider(f'**Source thickness (m)**',1,20,2,1)
    qd = st.slider(f'**specific discharge (m/d)**',0.001,1.0,0.25,0.001,format='%5.3f') 
    q = qd/86400    
    
with columns1[1]:
    with st.expander("Here you find widgets to :orange[**adjust dispersion**]"):  
        ax = st.slider(f'**Longitudinal (x) dispersivity (m)**',0.001,10.0,1.00,0.001)
        rat_x_y = st.slider(f'**Dispersivity ratio 1/n for x/y**',1,100,10,1)
        rat_x_z = st.slider(f'**Dispersivity ratio 1/n for x/z**',1,500,100,1)
    n = st.slider(f'**Porosity (-)**',0.01,0.6,0.25,0.01)  
with columns1[2]:
    with st.expander("Here you find widgets to :green[**adjust the plot**]"):
        isolines = st.toggle("Show isolines instead of isosurfaces")
        down_only = st.toggle("Spreading is only downward")
        Zp = st.slider(f'**Slice at z (top view plot)**',-25,25,0,1)
        Yp = st.slider(f'**Slice at y (side view plot)**',-100,100,0,1)
    td  = st.slider(f'**Time for the concentration profile (d)**',1.,1800.,1.,1.)
    t = td * 86400
    
v = q/n
ay = ax/rat_x_y
az = ax/rat_x_z

# Grid for X and Y
xmax = 1000
ymax = 100
zmax = 40
x_vals = np.linspace(-0.1*xmax, xmax, 300)
y_vals = np.linspace(-ymax, ymax, 300)
z_vals = np.linspace(-zmax, zmax, 300)
xxy, yxy = np.meshgrid(x_vals, y_vals)
xxz, zxz = np.meshgrid(x_vals, z_vals)

# Compute concentration values
Cxy =    concentration(Y, Z, xxy, yxy, Zp, t, ax, ay, az, v, C0, down_only)
Cxz =    concentration(Y, Z, xxz, Yp, zxz, t, ax, ay, az, v, C0, down_only)

# Plot the concentration field
lev_exp = 10.**np.arange(-8, 3)

fig = plt.figure(figsize=(16,8))
gs = matplotlib.gridspec.GridSpec(3,2, width_ratios=[8,1.1], height_ratios=[5,0.2,2])

ax = fig.add_subplot(gs[0,:])
if isolines:
    contour = plt.contour(xxy, yxy, Cxy, lev_exp, locator=ticker.LogLocator())
else:
    contour = plt.contourf(xxy, yxy, Cxy, lev_exp, locator=ticker.LogLocator())
ax.vlines(0, -Y/2, Y/2, linewidth = 10, color='fuchsia', label='Source of contamination')
plt.colorbar(contour, label="Concentration (g/m3)", format='%.0e')
plt.xlabel("x in m",fontsize=14)
plt.ylabel("y in m",fontsize=14)
plt.xlim(-0.1*xmax,xmax)
plt.legend(fontsize=14)
plt.title(f"Contaminant Concentration (top view) at t = {t}, z = {Zp}", fontsize=16)

ax = fig.add_subplot(gs[2,0])
if isolines:
    contour2 = plt.contour(xxz, zxz, Cxz, lev_exp, locator=ticker.LogLocator())
else:
    contour2 = plt.contourf(xxz, zxz, Cxz, lev_exp, locator=ticker.LogLocator())
ax.vlines(0, -Z/2, Z/2, linewidth = 10, color='fuchsia', label='Source of contamination')
plt.xlabel("x in m",fontsize=14)
plt.ylabel("z in m",fontsize=14)
plt.xlim(-0.1*xmax,xmax)
plt.title(f"Contaminant Concentration (side view) at t = {t}, y = {Yp}", fontsize=16)

st.pyplot(fig)