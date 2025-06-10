import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy import special
import numpy as np
import streamlit as st

st.title('2D Solute Transport: Continuous Source in Uniform 1D Flow')
st.subheader('Tracer input as :orange[Continuous injection]', divider="orange")

with st.expander('Show theory'):
    st.latex(r""" C(x,y,t) = \frac{C_0}{4} \cdot \operatorname{erfc}\left( \frac{x - v_x t}{2\sqrt{D_x t}} \right) \cdot \left[ \operatorname{erf} \left( \frac{y + \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right) - \operatorname{erf} \left( \frac{y - \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right) \right] """)

st.markdown("""
### About the model
This is a simplified **2D analytical solution** for solute transport in a groundwater system with:

- Uniform flow in the x-direction
- Dispersion in both x and y (no z)
- Continuous source of solute with width `Y`

Concentrations are shown as contours in the horizontal x-y plane.
""")

"---"

# Function: 2D Concentration
def concentration_2d(Y, x, y, t, ax, ay, v, C0):
    Dx = v * ax
    Dy = v * ay
    with np.errstate(divide='ignore', invalid='ignore'):
        erfc_term = special.erfc((x - v*t) / (2 * np.sqrt(Dx * t)))
        erf1 = special.erf((y + Y/2) / (2 * np.sqrt(Dy * x / v)))
        erf2 = special.erf((y - Y/2) / (2 * np.sqrt(Dy * x / v)))
        return (C0 / 4) * erfc_term * (erf1 - erf2)

columns1 = st.columns((1,1,1), gap='large')
# Widgets
with columns1[0]:
    with st.expander("Adjust :red[**source and flow**]"): 
        C0 = st.slider(f'Source concentration (g/m³)', 1, 100, 10, 1)
        Y = st.slider(f'Source width Y (m)', 1, 100, 10, 1)
        qd = st.slider(f'Specific discharge q (m/d)', 0.001, 1.0, 0.25, 0.001, format='%5.3f')
        q = qd / 86400

with columns1[1]:
    with st.expander("Adjust :orange[**dispersion**]"):  
        ax = st.slider(f'Longitudinal dispersivity αₓ (m)', 0.001, 10.0, 1.00, 0.001)
        rat_x_y = st.slider(f'Dispersivity ratio 1/n for x/y', 1, 100, 10, 1)
    n = st.slider(f'Porosity (-)', 0.01, 0.6, 0.25, 0.01)

with columns1[2]:
    with st.expander("Adjust :green[**plot**]"):
        isolines = st.toggle("Show isolines instead of filled contours")
        xmax = st.slider(f'max extension in x-direction', 10, 10000, 1000, 10)
        ymax = st.slider(f'max extension in y-direction', 10, 1000, 100, 10)
    td = st.slider(f'Time (days)', 1., 1800., 100., 1.)
    t = td * 86400

# Velocity and dispersivities
v = q / n
ay = ax / rat_x_y

# Grid
x_vals = np.linspace(-0.1 * xmax, xmax, 300)
y_vals = np.linspace(-ymax, ymax, 300)
xxy, yxy = np.meshgrid(x_vals, y_vals)

# Concentration field
Cxy = concentration_2d(Y, xxy, yxy, t, ax, ay, v, C0)

# Compute levels based on max concentration
cmax = np.nanmax(Cxy)
if cmax == 0 or np.isnan(cmax):
    levels = [1e-6]  # fallback
else:
    levels = [cmax * i / 10 for i in range(1, 11)]  # ascending: 0.1 to 1.0 * cmax

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

if isolines:
    contour = ax.contour(xxy, yxy, Cxy, levels=levels, cmap='plasma')
else:
    contour = ax.contourf(xxy, yxy, Cxy, levels=levels, cmap='plasma')

# Colorbar with float tick labels (1 decimal)
cbar = plt.colorbar(contour, label="Concentration (g/m³)", format='%.1f')
cbar.outline.set_linewidth(0.5)

# Source marker
ax.vlines(0, -Y/2, Y/2, linewidth=10, color='fuchsia', label='Source')
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_xlim(-0.1 * xmax, xmax)
ax.legend()
ax.set_title(f"2D Concentration at t = {int(td)} days", fontsize=16)
ax.grid()

 
st.pyplot(fig)