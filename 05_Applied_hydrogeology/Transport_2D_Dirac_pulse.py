import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
import math
import pandas as pd
import streamlit as st


# ToDo
# Make fragment with initial values and put computation in loop
# MODFLOW comparison
# Number input
# Multiple observations

st.title('2D Solute Transport: :orange[Slug Injection (Dirac Input)] in Uniform 1D Flow')
st.subheader(':orange[Instantaneous solute input through a point source]', divider="orange")

with st.expander('**Show theory**'):
    st.markdown("""
    #### 2D transport in a uniform flow field with a pulse source
    """)
    
    st.latex(r"""
    C(x, y, t) = \frac{M}{4 \pi t \sqrt{D_x D_y}} \cdot \exp\left( -\frac{(x - v t)^2}{4 D_x t} - \frac{y^2}{4 D_y t} \right)
    """)
    
    st.markdown(r"""
    #### Modification to make the solution comparable with numerical models
    
    It is required to account for the source geometry if the analytical solution is intended to serve as comparison with the results from numerical models. The Dirac pulse release all the mass in a single point. However, if the solute is placed in a discrete cell of a numerical model the solute concentration is affected by dillution. Accordingly, the mass for a 2D model cell is divided by the aquifer thickness _m_ and the porosity _n_, resulting in
    """)
    
    st.latex(r"""
    C(x, y, t) = \frac{M}{4 \pi m n t \sqrt{D_x D_y}} \cdot \exp\left( -\frac{(x - v t)^2}{4 D_x t} - \frac{y^2}{4 D_y t} \right)
    """)
    
    
st.markdown("""
This app shows the evolution of a solute plume after an **instantaneous (slug) injection** at a point.

- The source releases a given **mass** at time zero.
- Transport occurs via **advection** and **dispersion** in the x–y plane.
- The plume shape depends on **velocity** and **dispersivities**.
""")

# Function: 2D Dirac/Slug Concentration
def concentration_slug(x, y, t, ax, ay, v, M, nf, thick):
    Dx = v * ax
    Dy = v * ay
    with np.errstate(divide='ignore', invalid='ignore'):
        coeff = M / (4 * np.pi * t * thick * nf * np.sqrt(Dx * Dy))
        exponent = -((x - v * t)**2 / (4 * Dx * t) + y**2 / (4 * Dy * t))
        return coeff * np.exp(exponent)

#Initialize
nf = 1      # Presetting - needs to be porosity if results should be compared to MODFLOW/MT3D
thick = 1   # Presetting - needs to be aquifer thickness if results should be compared to MODFLOW/MT3D
MOD = False # Flag to account for MODFLOW input

st.session_state.nf = nf
st.session_state.thick = thick
st.session_state.MOD = MOD

@st.fragment
def dirac2D():
    
    # Sidebar controls
    columns1 = st.columns((1,1,1))
    
    with columns1[0]:
        with st.expander("Adjust :red[**source and flow**]"): 
            M = st.slider('Released mass M (g)', 1, 10000, 1000, 1)
            qd = st.slider('Specific discharge q (m/d)', 0.001, 1.0, 0.25, 0.001, format='%5.3f')
            q = qd / 86400
            st.session_state.MOD = st.toggle('Toggle here for source equivalent to model cell')
            if st.session_state.MOD:
                st.session_state.thick = st.slider('Layer thickness (m)', 1, 100, 10, 1)
            else:
                st.session_state.thick = 1
    
    with columns1[1]:
        with st.expander("Adjust :orange[**Transport parameter**]"):  
            ax_disp = st.slider('Longitudinal dispersivity αₓ (m)', 0.001, 100.0, 10.00, 0.1)
            rat_x_y = st.slider('Dispersivity ratio 1/n for x/y', 1, 100, 10, 1)
            n = st.slider('Porosity (-)', 0.01, 0.6, 0.25, 0.01)
            if st.session_state.MOD:
                st.session_state.nf = n
            else:
                st.session_state.nf = 1
    
    with columns1[2]:
        with st.expander("Adjust :green[**plot**]"):
            log_upper = st.toggle("Use log scale for conc.", value=False)
            dynamic = st.toggle("Use dynamic levels for concentration", value=True, disabled=log_upper, help="When enabled, contour levels are based on actual plume concentrations. Disabled when log scale is selected.")
            cmax_man = st.slider('max conc of plot (g/m3)', 0.1, 10., 5., 0.1, disabled=log_upper or dynamic, help="Used when log and dynamic scaling are disabled")
            if log_upper:
                dynamic = False
            isolines = st.toggle("Show isolines instead of filled contours")
            
            xmax = st.slider('max extension in x-direction', 10, 10000, 2000, 10)
            ymax = st.slider('max extension in y-direction', 10, 1000, 400, 10)
            
            
    td = st.slider('Time to show (days)', 1., 1800., 100., 1.)
    t = td * 86400
    
    # Breakthrough curve toggle
    show_bt = st.toggle("📈 Show breakthrough curves")
    
    # Velocity and dispersivities
    v = q / n
    ay_disp = ax_disp / rat_x_y
    
    # Compute C_ref_max1 
    ref_time = np.linspace(1, 864000, 240)
    # for upper plot at 3 m
    ref_distance1 = 5  # meters
    C_ref1 = concentration_slug(ref_distance1, 0, ref_time, ax_disp, ay_disp, v, M, st.session_state.nf, st.session_state.thick)
    C_ref_max1 = 10**math.ceil(np.log10(np.nanmax(C_ref1)))
    # for lower plot at 15 m
    ref_distance2 = 15  # meters
    C_ref2 = concentration_slug(ref_distance2, 0, ref_time, ax_disp, ay_disp, v, M, st.session_state.nf, st.session_state.thick)
    C_ref_max2 = round(np.max(C_ref2))
    
    # Grid for plume plot
    x_vals = np.linspace(-0.1 * xmax, xmax, 300)
    y_vals = np.linspace(-ymax, ymax, 300)
    xxy, yxy = np.meshgrid(x_vals, y_vals)
    
    # Concentration field
    Cxy = concentration_slug(xxy, yxy, t, ax_disp, ay_disp, v, M, st.session_state.nf, st.session_state.thick)
    
    # Dynamic levels     
    if log_upper:
        min_level = C_ref_max1 / 1e5
        levels = np.logspace(np.log10(min_level), np.log10(C_ref_max1), 10)
    else:
        if dynamic:
            cmax = np.nanmax(Cxy)
            if cmax == 0 or np.isnan(cmax):
                levels = [1e-6]
            else:
                levels = [cmax * i / 10 for i in range(1, 11)]
        else:
            levels = [1e-6] + [cmax_man * i / 10 for i in range(1, 11)]
    
    # FIGURE 1 - Plot plume
    fig, ax = plt.subplots(figsize=(12, 4))
    if isolines:
        contour = ax.contour(xxy, yxy, Cxy, levels=levels, cmap='plasma',
                             norm=LogNorm(vmin=levels[0], vmax=levels[-1]) if log_upper else None,
                             linewidths=2.0)
    else:
        contour = ax.contourf(xxy, yxy, Cxy, levels=levels, cmap='plasma',
                              norm=LogNorm(vmin=levels[0], vmax=levels[-1]) if log_upper else None)
    
    cbar = plt.colorbar(contour, ticks=LogLocator() if log_upper else levels,
                        format='%.1e' if log_upper else '%.2f')
    cbar.outline.set_linewidth(1.5)
    
    ax.plot(0, 0, 'o', color='fuchsia', label='Injection point')
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_xlim(-0.1 * xmax, xmax)
    ax.set_ylim(-ymax, ymax)
    ax.legend()
    ax.set_title(f"2D Concentration after Dirac Input at t = {int(td)} days", fontsize=16)
    st.pyplot(fig)
    
    # Compute breakthrough
    if show_bt:
        st.markdown('''
        #### Breakthrough curves''')
        columns2 = st.columns((2,1), gap='large')
        with columns2[0]:
            with st.expander("Adjust :orange[**observation(s) location(s)**]"):
                # Number of observation points
                n_obs = st.slider("Number of observation points", 1, 10, 1)
            
                if n_obs == 1:
                    distance = st.slider("Distance to observation point (m)", 1, int(xmax), 20, 1, format="%4.2f")
                    distances = [distance]
                    st.session_state.distance = distance
                else:
                    min_max = st.slider("Range of observation distances (m)", 1, int(xmax), (20, 200), step=1)
                    distances = np.linspace(min_max[0], min_max[1], n_obs)
                
                    manual_input = st.checkbox("📝 Manually specify observation distances")
                    if manual_input:
                        st.markdown("Adjust individual observation distances:")
                        distances_manual = []
                        cols = st.columns(min(n_obs, 5))
                        for i, d in enumerate(distances):
                            col = cols[i % len(cols)]
                            with col:
                                val = st.number_input(f"x_obs {i+1}", min_value=1.0, max_value=float(xmax), value=float(d), step=1.0, key=f"x_obs_{i}")
                                distances_manual.append(val)
                        distances = distances_manual   
        # Plot settings
        with columns2[1]:
            with st.expander("Adjust :green[**plot**]"):
                tmax = st.slider('max time of plot (d)', 10, 1800, 1800, 1)
                cmax = st.number_input('max conc of plot (g/m3)', 0, 100, C_ref_max2, 1)
    
        # Time vector
        times_days = np.linspace(0.1, tmax, 300)
        times_sec = times_days * 86400
    
        # Plot breakthrough curves
        fig_bt, ax_bt = plt.subplots(figsize=(10, 4))
        for d in distances:
            C_bt = concentration_slug(d, 0, times_sec, ax_disp, ay_disp, v, M, st.session_state.nf, st.session_state.thick)
            ax_bt.plot(times_days, C_bt, linewidth=2, label=f"{d:.1f} m")
    
        ax_bt.set_xlabel("Time (days)")
        ax_bt.set_ylabel("Concentration (g/m³)")
        ax_bt.set_title("Breakthrough Curves")
        ax_bt.set_xlim(0, tmax)
        ax_bt.set_ylim(0, cmax)
        ax_bt.legend(title="Distance", loc="upper right")
        st.pyplot(fig_bt)
    
        # Download CSV for all
        df_bt_all = pd.DataFrame({'Time_days': times_days})
        for d in distances:
            C_bt = concentration_slug(d, 0, times_sec, ax_disp, ay_disp, v, M, st.session_state.nf, st.session_state.thick)
            df_bt_all[f"C_{d:.1f}m"] = C_bt
    
        csv = df_bt_all.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Breakthrough Curves as CSV",
            data=csv,
            file_name='breakthrough_curves.csv',
            mime='text/csv'
        )
dirac2D()