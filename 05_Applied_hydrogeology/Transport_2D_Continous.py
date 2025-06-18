import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
from scipy import special
import numpy as np
import pandas as pd
import streamlit as st

st.title('2D Solute Transport: :green[Continuous Source] in Uniform 1D Flow')
st.subheader('Solute input through :green[continuous release]', divider="green")

st.markdown("""
### About :green[this app]
This tool simulates conservative solute transport in a **2D horizontal flow domain** with a **continuous line source**.

You can adjust parameters for:

- Source and flow (e.g., concentration, width, discharge)
- Transport (dispersivities, porosity)
- Plot settings (domain size, style)

In addition to the 2D plume visualization, the app can generate **breakthrough curves** at specified observation points downstream. Locations can be set manually or automatically.

Results can be downloaded as **CSV files** for further analysis or comparison with numerical models.
""")

st.markdown("""
### About :green[the model]
This is a simplified **2D analytical solution** for solute transport in a groundwater system with:

- Uniform flow in the x-direction
- Dispersion in both x and y (no z)
- Continuous source of solute with width `Y`

Concentrations are shown as contours in the horizontal x-y plane.
""")
with st.expander('**Show equation**'):
    st.latex(r""" C(x,y,t) = \frac{C_0}{4} \cdot \operatorname{erfc}\left( \frac{x - v_x t}{2\sqrt{D_x t}} \right) \cdot \left[ \operatorname{erf} \left( \frac{y + \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right) - \operatorname{erf} \left( \frac{y - \frac{Y}{2}}{2 \sqrt{D_y \frac{x}{v}}} \right) \right] """)

st.subheader(':green[Interactive plot]', divider="green")

# Function: 2D Concentration
def concentration_2d(Y, x, y, t, ax, ay, v, C0):
    Dx = v * ax
    Dy = v * ay
    with np.errstate(divide='ignore', invalid='ignore'):
        erfc_term = special.erfc((x - v*t) / (2 * np.sqrt(Dx * t)))
        erf1 = special.erf((y + Y/2) / (2 * np.sqrt(Dy * x / v)))
        erf2 = special.erf((y - Y/2) / (2 * np.sqrt(Dy * x / v)))
        return (C0 / 4 ) * erfc_term * (erf1 - erf2)

MOD = False # Flag to account for MODFLOW input

st.session_state.MOD = MOD

@st.fragment
def continuous2D():
    columns1 = st.columns((1,1,1))
    with columns1[0]:
        with st.expander("Adjust :red[**source and flow**]"): 
            C0 = st.slider('Source concentration (g/m³)', 1, 100, 10, 1)
            Y = st.slider('Source width Y (m)', 1, 100, 10, 1)
            qd = st.slider('Specific discharge q (m/d)', 0.001, 1.0, 0.25, 0.001, format='%5.3f')
            q = qd / 86400
            st.session_state.MOD = st.toggle('Toggle here for source equivalent to model cell')

    with columns1[1]:
        with st.expander("Adjust :orange[**Transport parameter**]"):  
            ax_disp = st.slider('Longitudinal dispersivity αₓ (m)', 0.001, 10.0, 1.00, 0.001)
            rat_x_y = st.slider('Dispersivity ratio 1/n for x/y', 1, 100, 10, 1)
            n = st.slider('Porosity (-)', 0.01, 0.6, 0.25, 0.01)

    with columns1[2]:
        with st.expander("Adjust :green[**plot**]"):
            log_upper = st.toggle("Use log scale for conc.", value=False)
            cmax_man = st.slider('max conc of plot (g/m³)', 0.1, 1000., 10., 1.0, disabled=log_upper, help="Used when log and dynamic scaling are disabled")
            if log_upper:
                dynamic = False
            isolines = st.toggle("Show isolines instead of filled contours")
            xmax = st.slider('max extension in x-direction', 10, 10000, 1000, 10)
            ymax = st.slider('max extension in y-direction', 10, 1000, 100, 10)
    
    td = st.slider('Time (days)', 1., 1800., 100., 1.)
    t = td * 86400

    # Velocity and dispersivities
    v = q / n
    ay_disp = ax_disp / rat_x_y

    # Grid
    x_vals = np.linspace(-0.1 * xmax, xmax, 300)
    y_vals = np.linspace(-ymax, ymax, 300)
    xxy, yxy = np.meshgrid(x_vals, y_vals)

    # Concentration field
    Cxy = concentration_2d(Y, xxy, yxy, t, ax_disp, ay_disp, v, C0)

    # Compute levels based on max concentration
    cmax = np.nanmax(Cxy)
    if log_upper:
        min_level = cmax / 1e5 if cmax > 0 else 1e-10
        levels = np.logspace(np.log10(min_level), np.log10(cmax), 10)
    else:
        levels = [1e-6] + [cmax_man * i / 10 for i in range(1, 11)]

    # Plotting
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
    cbar.outline.set_linewidth(0.5)
    ax.vlines(0, -Y/2, Y/2, linewidth=10, color='fuchsia', label='Source')
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_xlim(-0.1 * xmax, xmax)
    ax.legend()
    ax.set_title(f"2D Concentration at t = {int(td)} days", fontsize=16)
    ax.grid()
    st.pyplot(fig)

    # --- Breakthrough Curves ---
    show_bt = st.toggle("📈 Show breakthrough curves")

    if show_bt:
        st.markdown("### Breakthrough Curves at Observation Points")

        columns2 = st.columns((2,1), gap='large')
        with columns2[0]:
            with st.expander("Adjust :orange[**observation(s) location(s)**]"):
                n_obs = st.slider("Number of observation points", 1, 10, 1)

                if n_obs == 1:
                    distance = st.slider("Distance to observation point (m)", 1, int(xmax), 100, 1, format="%4.2f")
                    distances = [distance]
                else:
                    min_max = st.slider("Range of observation distances (m)", 1, int(xmax), (50, 500), step=1)
                    distances = np.linspace(min_max[0], min_max[1], n_obs)

                    manual_input = st.checkbox("📝 Manually specify observation distances")
                    if manual_input:
                        st.markdown("Adjust individual observation distances:")
                        distances_manual = []
                        cols = st.columns(min(n_obs, 5))
                        for i, d in enumerate(distances):
                            col = cols[i % len(cols)]
                            with col:
                                val = st.number_input(f"x_obs {i+1}", min_value=1.0, max_value=float(xmax),
                                                      value=float(d), step=1.0, key=f"x_obs_{i}")
                                distances_manual.append(val)
                        distances = distances_manual

        with columns2[1]:
            with st.expander("Adjust :green[**plot**]"):
                tmax = st.slider("Max time for breakthrough plot (days)", 10, 1800, 1000, 10)
                cmax_bt = st.number_input("Max concentration (g/m³)", 0.0, 1000.0, float(np.nanmax(Cxy)), 1.0)

        t_plot_days = np.linspace(1, tmax, 300)
        t_plot_sec = t_plot_days * 86400

        fig_bt, ax_bt = plt.subplots(figsize=(10, 4))
        for d in distances:
            C_bt = concentration_2d(Y, d, 0, t_plot_sec, ax_disp, ay_disp, v, C0)
            ax_bt.plot(t_plot_days, C_bt, linewidth=2, label=f"{d:.1f} m")

        ax_bt.set_xlabel("Time (days)")
        ax_bt.set_ylabel("Concentration (g/m³)")
        ax_bt.set_title("Breakthrough Curves")
        ax_bt.set_xlim(0, tmax)
        ax_bt.set_ylim(0, cmax_bt)
        ax_bt.legend(title="Distance", loc="upper right")
        st.pyplot(fig_bt)

        df_bt_all = pd.DataFrame({'Time_days': t_plot_days})
        for d in distances:
            C_bt = concentration_2d(Y, d, 0, t_plot_sec, ax_disp, ay_disp, v, C0)
            df_bt_all[f"C_{d:.1f}m"] = C_bt

        csv = df_bt_all.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Breakthrough Curves as CSV",
            data=csv,
            file_name='breakthrough_curves.csv',
            mime='text/csv'
        )

continuous2D()
