import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
from scipy import special
import numpy as np
import streamlit as st
from streamlit_extras.stateful_button import button

st.title('3D :red-background[Heat transport] with convection, conduction, and dispersion')
st.subheader('Heat input as :orange[Continous injection]', divider="orange")

columns1 = st.columns((1,1,1), gap = 'large')
with columns1[1]:
    theory = button('Show/Hide theory', key = 'button1')
    
if theory:
#    st.latex(r'''C(x = vt + X, y = Y, z = Z) = \frac{M}{8 (\pi t)^{\frac{3}{2}} \sqrt{D_x D_y D_z}} \exp ( - ( \frac{X^2}{4 D_x t} + \frac{Y^2}{4 D_y t} + \frac{Z^2}{4 D_z t})''')
     st.latex(r""" H(x,y,z,t) = \frac{C_0}{8}\left(\operatorname{erfc}\left( \frac{x - v_x t}{2\sqrt{D_x t}} \right) \left( \operatorname{erf} \left( \frac{y + \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right)  - \operatorname{erf} \left(\frac{y - \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right)\right)\left(\operatorname{erf} \left( \frac{z + \frac{Z}{2}}{2 \sqrt{D_z \frac{x}{v}}} \right)-\operatorname{erf} \left( \frac{z - \frac{Z}{2}}{2 \sqrt{D_z \frac{x}{v}}}\right)\right)\right)""")

'---'

st.markdown("""
            ### About the computed situation
            
            Heat transport is considered for a 3D system with steady groundwater flow with a user-defined specific discharge. The average velocity is depending on the effective porosity and printed below the interactive plot.
            
            The heat is constantly added at the source with T0.
            
            The plot shows the heat for convective-dispersive transport. The isolines of equal temperatures are computed for a horizontal-plane view (x-y plot). The z-value of the y-y slice can be modified with the sliders above the plot.
""", unsafe_allow_html=True
)
"---"

#FUNCTIONS FOR COMPUTATION; ADS = CONVECTION, DISPERSION AND SORPTION - EVENTUALLY SET RETARDATION TO 1 FOR NO SORPTION

# Define the function
def heat(Y, Z, x, y, z, t, ax, ay, az, q, n_e, T0, lambda_s, c_s, rho_s, T_ini, down_only):
    lambda_w = 0.598
    c_w = 4186.
    rho_w = 1000.
    
    v = q/n_e
    
    D_H = (n_e * lambda_w + (1-n_e)*lambda_s) /(n_e * c_w * rho_w)
    Kd = c_s/(c_w * rho_w)
    R = 1 + (1-n_e)/n_e * rho_s * Kd

    Dx = v * ax + D_H
    Dy = v * ay + D_H
    Dz = v * az + D_H
    
    if t == 0:
        return np.zeros_like(X)  # Avoid division by zero
    
    coeff = T0/8
    
    erf1 = special.erfc((x-v*t)/(2*np.sqrt(Dx*t)))
    erf2 = special.erf((y+Y/2)/(2*np.sqrt(Dy*x/v)))
    erf3 = special.erf((y-Y/2)/(2*np.sqrt(Dy*x/v)))
    if down_only:
        erf4 = special.erf((z+Z)/(2*np.sqrt(Dz*x/v)))
        erf5 = special.erf((z-Z)/(2*np.sqrt(Dz*x/v)))
    else:
        erf4 = special.erf((z+Z/2)/(2*np.sqrt(Dz*x/v)))
        erf5 = special.erf((z-Z/2)/(2*np.sqrt(Dz*x/v)))
    
    return  T_ini + coeff * (erf1*(erf2-erf3)*(erf4-erf5))
    
# Computation

# Defined/fixed parameters (sand)
lambda_s = 0.35
c_s      = 840
rho_s    = 2650
T_ini    = 10

columns1 = st.columns((1,1,1), gap = 'large')

with columns1[0]:
    TB = st.slider(f'**Source temperature (g/m3)**',1,100,T_ini+10,1) 
    Y  = st.slider(f'**Source width (m)**',1,100,10,1)   
    Z  = st.slider(f'**Source thickness (m)**',1,20,2,1) 
    q  = st.slider(f'**specific discharge (m/s)**',0.001,0.1,0.016,0.001,format='%5.3f') 
    
with columns1[1]:
    n_e = st.slider(f'**effective Porosity (-)**',0.01,0.6,0.25,0.01)    
    ax = st.slider(f'**Longitudinal (x) dispersivity (m)**',0.001,10.0,1.00,0.001)
    rat_x_y = st.slider(f'**Dispersivity ratio 1/n for x/y**',1,100,10,1)
    rat_x_z = st.slider(f'**Dispersivity ratio 1/n for x/z**',1,500,100,1)
with columns1[2]:
    isolines = st.toggle("Show isolines instead of isosurfaces")
    down_only = st.toggle("Spreading is only downward")
    Zp = st.slider(f'**Slice at z (top view plot)**',-25,25,0,1)
    Yp = st.slider(f'**Slice at y (side view plot)**',-100,100,0,1)
    xmax = st.slider(f'**Extension in x-direction**',0,1000,400,50)
    t = st.slider(f'**Time for the temperature profile (s)**',1.,1800.,1.,1.)
    
T0 = TB - T_ini
ay = ax/rat_x_y
az = ax/rat_x_z

# Grid for X and Y
# xmax = 500
ymax = xmax/10
zmax = 40
x_vals = np.linspace(-0.1*xmax, xmax, 300)
y_vals = np.linspace(-ymax, ymax, 300)
z_vals = np.linspace(-zmax, zmax, 300)
xxy, yxy = np.meshgrid(x_vals, y_vals)
xxz, zxz = np.meshgrid(x_vals, z_vals)

# Compute temperature values
Txy =    heat(Y, Z, xxy, yxy, Zp, t, ax, ay, az,  q, n_e, T0, lambda_s, c_s, rho_s, T_ini, down_only)
Txz =    heat(Y, Z, xxz, Yp, zxz, t, ax, ay, az,  q, n_e, T0, lambda_s, c_s, rho_s, T_ini, down_only)

# Replace NaN numbers for negative x by T_ini
Txy[np.isnan(Txy)] = T_ini
Txz[np.isnan(Txz)] = T_ini

# Plot the temperature field
lev_exp = 10.**np.arange(-8, 3)

fig = plt.figure(figsize=(16,8))
gs = matplotlib.gridspec.GridSpec(3,2, width_ratios=[8,1.1], height_ratios=[5,0.2,2])

ax = fig.add_subplot(gs[0,:])
if isolines:
    #contour = plt.contour(xxy, yxy, Txy, lev_exp, locator=ticker.LogLocator())
    contour = plt.contour(xxy, yxy, Txy)
else:
    #contour = plt.contourf(xxy, yxy, Txy, lev_exp, locator=ticker.LogLocator())
    contour = plt.contourf(xxy, yxy, Txy)
ax.vlines(0, -Y/2, Y/2, linewidth = 10, color='fuchsia', label='Source of heat')
plt.colorbar(contour, label="Temperature (degree Celsius)", format='%5.2f')
plt.xlabel("x in m",fontsize=14)
plt.ylabel("y in m",fontsize=14)
plt.xlim(-0.1*xmax,xmax)
plt.legend(fontsize=14)
plt.title(f"Temperature (top view) at t = {t}, z = {Zp}", fontsize=16)

ax = fig.add_subplot(gs[2,0])
if isolines:
    #contour2 = plt.contour(xxz, zxz, Txz, lev_exp, locator=ticker.LogLocator())
    contour2 = plt.contour(xxz, zxz, Txz)
else:
    #contour2 = plt.contourf(xxz, zxz, Txz, lev_exp, locator=ticker.LogLocator())
    contour2 = plt.contourf(xxz, zxz, Txz)
ax.vlines(0, -Z/2, Z/2, linewidth = 10, color='fuchsia', label='Source of heat')
plt.xlabel("x in m",fontsize=14)
plt.ylabel("z in m",fontsize=14)
plt.xlim(-0.1*xmax,xmax)
plt.title(f"Temperature (side view) at t = {t}, y = {Yp}", fontsize=16)

st.pyplot(fig)