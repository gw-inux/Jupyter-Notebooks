import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import scipy.special
import scipy.interpolate as interp
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("Theory and Concept of the :blue[Multi-Node-Well package (MNW) in MODFLOW]")
st.subheader("Process-based implementation of Flow to Pumping wells", divider="blue")

st.markdown("""
This app calculates the flow between a Multi-Node-Well (MNW) and a model cell depending on the system parameters describing the flow in the vicinity of the well and into the well.
 
In general, the flow into the well is described with a Cell to Well Conductance:
""")

st.latex(r'''Q_W = C_{CWC} (H_{well} - h_{{aq}})''')

st.markdown("""
where:
- $Q_W$ is the flow between the well and the aquifer, taken as positive if it is directed into the aquifer [L3/T]
- $H_{well}$ is the water level in the well (L),
- $C_{CWC}$ is the Cell to Well conductance of the MNW-aquifer interconnection [L2/T], and
- $h_{aq}$ is the head in the aquifer that interacts with the well (L).

Further, the CWC is composed by three terms, describing (1) flow to the well, (2) the skin effect for flow into the well, and (3) the effect of turbulence in the vicinity of the well. Accordingly, the Cell to Well conductance can be defined as:
""")

st.latex(r'''CWC_n = [ A + B + C Q_n^{(p-1)}]^{-1}''')

st.markdown("""
where:
- $A$ = Linear aquifer-loss coefficient; Represents head loss due to flow through the aquifer to the well [T/L²].
- $B$ = Linear well-loss coefficient. Accounts for head loss associated with linear flow components in the well [T/L²].
- $C$ = Nonlinear well-loss coefficient, Governs the nonlinear (e.g., turbulent) head loss in the well. [T^P/L^(3P-1)], and
- $P$ = is the power (exponent) of the nonlinear discharge component of well loss.
""")

st.subheader('Interactive plot of the $Q-h$ relationship of the MNW package', divider='green')

st.markdown("""
The subsequent interactive plot allows you to investigate the behavior of the Multi-Node-Well (MNW) boundary in MODFLOW. The plot shows the relationship between the cell water level (aquifer head) and the head in the pumping well. The application allows you to evaluate and visualize for a
- defined discharge (i.e, $Q$ is defined and the head in the well $h_w$ is calculated)
- defined head (i.e., $h_w$ is defined and the discharge $Q$ in the well is calculated.
You can use the toggle to switch between both target parameters.

Further, the application allows by toggles:
- to turn the plot by 90 degrees,
- to switch between number input or sliders,
- to plot a second set of parameters for comparison.

The values of the $Q-h$ relationship are shown below the interactive plot.
""")
# Functions

# Define the nonlinear equation to solve: Q = Δh / (A + B + C * Q**(p-1))
def discharge_equation(Q, delta_h, A, B, C, p):
    return Q - delta_h / (A + B + C * Q**(p - 1))
    
# Callback function to update session state
def update_dh_show():
    st.session_state.dh_show = st.session_state.dh_show_input
def update_Q_show():
    st.session_state.Q_show = st.session_state.Q_show_input
def update_A():
    st.session_state.A = st.session_state.A_input
def update_B():
    st.session_state.B = st.session_state.B_input
def update_C():
    st.session_state.C = st.session_state.C_input
def update_P():
    st.session_state.P = st.session_state.P_input 

def update_A2():
    st.session_state.A2 = st.session_state.A2_input
def update_B2():
    st.session_state.B2 = st.session_state.B2_input
def update_C2():
    st.session_state.C2 = st.session_state.C2_input
def update_P2():
    st.session_state.P2 = st.session_state.P2_input 
    
    
    
# Initialize session state for value and toggle state
st.session_state.dh_show = 5.0
st.session_state.Q_show = 0.2
st.session_state.A = 5.0
st.session_state.B = 5.0
st.session_state.C = 0.0
st.session_state.P = 2.0
st.session_state.A2 = 5.0
st.session_state.B2 = 5.0
st.session_state.C2 = 5.0
st.session_state.P2 = 2.0
st.session_state.number_input = False  # Default to number_input

if 'Q_off' not in st.session_state:
    st.session_state.Q_off = False
if 'Q_off2' not in st.session_state:
    st.session_state.Q_off2 = False

# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    st.markdown("---")
    
    # Switches
    columns1 = st.columns((1,1), gap = 'large')              
    with columns1[0]:
        turn = st.toggle('Toggle to turn the plot 90 degrees', key="MNW_turn")
        st.session_state.number_input = st.toggle("Toggle to use Slider or Number input.")
        visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="MNW_vis")
    with columns1[1]:
        # The additional controls only for visualization
        if visualize:
            st.write('**:green[Target for evaluation/visualization]**')
            h_target = st.toggle('Toggle for **$Q$** or **$h$** target')

    columns2 = st.columns((1,1), gap = 'large')              
    with columns2[1]:
        # The additional controls only for visualization
        if visualize:
            if h_target:
                if st.session_state.number_input:
                    dh_show = st.number_input("**Drawdown $$\Delta h$$** in the pumping well", 0.01, 10.0, 5.0, 0.1, key="dh_show_input", on_change=update_dh_show)
                else:
                    dh_show = st.slider      ("**Drawdown $$\Delta h$$** in the pumping well", 0.01, 10.0, 5.0, 0.1, key="dh_show_input", on_change=update_dh_show)
            else:
                if st.session_state.number_input:
                    Q_show = st.number_input("**Discharge $Q$** in the pumping well", 0.001, 1.0, 0.5, 0.001, key="Q_show_input", on_change=update_Q_show)
                else:
                    Q_show = st.slider      ("**Discharge $Q$** in the pumping well", 0.001, 1.0, 0.5, 0.001, key="Q_show_input", on_change=update_Q_show)                            
    
    st.markdown("---")
    with st.expander('Click to modify model parameters and to activate a second dataset for comparison'):
        # Activate second dataset
        second = st.toggle("Toggle to define a second parameter set for comparison")
        
        # Parameter Input
        
        columns3a = st.columns((1,1,1,1))
        with columns3a[0]:
            st.write('**$A$**')
        with columns3a[1]:
            st.write('**$B$**')        
        with columns3a[2]:
            st.write('**$C$**')        
        with columns3a[3]:
            st.write('**$P$**')

        columns3 = st.columns((1,1,1,1))
        with columns3[0]:
            st.write('**Linear aquifer-loss** coeff. in s/m²')
        with columns3[1]:
            st.write('**Linear well-loss** coeff. in s/m²')        
        with columns3[2]:
            st.write('**Nonlinear well-loss** coeff. in s^P/m^(3P-1)')        
        with columns3[3]:
            st.write('Power of the nonlinear well-loss')        
            
        st.write('**:blue[Dataset 1]** (A, B, C, P)')     
        columns4 = st.columns((1,1,1,1))
        if st.session_state.number_input:
            with columns4[0]:
                A = st.number_input("", 0.00, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A, label_visibility="collapsed")
            with columns4[1]:
                B = st.number_input("", 0.00, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B, label_visibility="collapsed")
            with columns4[2]:
                C = st.number_input("", 0.00, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C, label_visibility="collapsed")
            with columns4[3]:
                P = st.number_input("", 1.0, 4.0,   st.session_state.P, 0.1, key="P_input", on_change=update_P, label_visibility="collapsed")
        else:
            with columns4[0]:
                A = st.slider      ("", 0.00, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A, label_visibility="collapsed")
            with columns4[1]:
                B = st.slider      ("", 0.00, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B, label_visibility="collapsed")        
            with columns4[2]:
                C = st.slider      ("", 0.00, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C, label_visibility="collapsed")   
            with columns4[3]:
                P = st.slider      ("", 1.0, 4.0,   st.session_state.P, 0.1, key="P_input", on_change=update_P, label_visibility="collapsed")
        
        if second:
            st.write('**:red[Dataset 2]** (A, B, C, P)')
            columns5 = st.columns((1,1,1,1))
            if st.session_state.number_input:
                with columns5[0]:
                    A2 = st.number_input("", 0.00, 10.0, st.session_state.A2, 0.1, key="A2_input", on_change=update_A2, label_visibility="collapsed")
                with columns5[1]:
                    B2 = st.number_input("", 0.00, 10.0, st.session_state.B2, 0.1, key="B2_input", on_change=update_B2, label_visibility="collapsed")
                with columns5[2]:
                    C2 = st.number_input("", 0.00, 10.0, st.session_state.C2, 0.1, key="C2_input", on_change=update_C2, label_visibility="collapsed")
                with columns5[3]:
                    P2 = st.number_input("", 1.0, 4.0,   st.session_state.P2, 0.1, key="P2_input", on_change=update_P2, label_visibility="collapsed")
            else:
                with columns5[0]:
                    A2 = st.slider      ("", 0.00, 10.0, st.session_state.A2, 0.1, key="A2_input", on_change=update_A2, label_visibility="collapsed")
                with columns5[1]:
                    B2 = st.slider      ("", 0.00, 10.0, st.session_state.B2, 0.1, key="B2_input", on_change=update_B2, label_visibility="collapsed")        
                with columns5[2]:
                    C2 = st.slider      ("", 0.00, 10.0, st.session_state.C2, 0.1, key="C2_input", on_change=update_C2, label_visibility="collapsed")   
                with columns5[3]:
                    P2 = st.slider      ("", 1.0, 4.0,   st.session_state.P2, 0.1, key="P2_input", on_change=update_P2, label_visibility="collapsed")        
    
    aquifer_thickness = 10.0
    
    # Visualization if active
    if visualize:
        if h_target:
            delta_head = dh_show
            Q_guess = delta_head / (A + B)  # initial guess
            Q_show, = fsolve(discharge_equation, Q_guess, args=(delta_head, A, B, C, P))
            if second:
                delta_head2 = delta_head
                Q_guess2 = delta_head2 / (A2 + B2)  # initial guess
                Q_show2, = fsolve(discharge_equation, Q_guess2, args=(delta_head2, A2, B2, C2, P2))
        else:
            delta_head = Q_show * (A + B + C * Q_show**(P - 1))
            if second:
                Q_show2 = Q_show
                delta_head2 = Q_show2 * (A2 + B2 + C2 * Q_show2**(P2 - 1))
        
        # Define the values for the visual help lines
        if second:
            Q_line = max(Q_show, Q_show2)
            h_line = min(delta_head, delta_head2)
        else:
            Q_line = Q_show
            h_line = delta_head
                
            
    #Define aquifer head range / Range of head differences Δh
    delta_h_range = np.linspace(0.01, 10, 200)
    Q_values = []
    if second:
        delta_h_range2 = np.linspace(0.01, 10, 200)
        Q_values2 = []
    
    # Solve for Q_n for each Δh
    for delta_h in delta_h_range:
        Q_initial_guess = delta_h / (A + B)  # reasonable initial guess
        Q_solution, = fsolve(discharge_equation, Q_initial_guess, args=(delta_h, A, B, C, P))
        Q_values.append(Q_solution)
    
    if second:
        for delta_h2 in delta_h_range2:
            Q_initial_guess2 = delta_h2 / (A2 + B2)  # reasonable initial guess
            Q_solution2, = fsolve(discharge_equation, Q_initial_guess2, args=(delta_h2, A2, B2, C2, P2))
            Q_values2.append(Q_solution2)   
        
        
    if visualize:
        # PLOT HERE - Create side-by-side plots
        fig, (ax_schematic, ax_plot) = plt.subplots(1, 2, figsize=(8, 6), width_ratios=[1, 3])
        fig.subplots_adjust(wspace=0.5)  # Increase horizontal space between ax_schematic and ax_plot
        
        # --- LEFT AXIS: Schematic view (Aquifer head vs Well head) ---
        schematic_width = 1.0
        # Aquifer: full height blue rectangle
        ax_schematic.add_patch(plt.Rectangle((0.0, 0), schematic_width*0.5, aquifer_thickness, color='skyblue'))
        ax_schematic.add_patch(plt.Rectangle((0.6, 0), schematic_width*0.5, aquifer_thickness, color='skyblue'))
        # Well water level: narrower grey rectangle, Head level indicators (dashed lines) and Labels wellls
        if second and not h_target:
            ax_schematic.add_patch(plt.Rectangle((0.50, delta_head),  schematic_width * 0.05, 10-delta_head, color='darkblue'))
            ax_schematic.add_patch(plt.Rectangle((0.55, delta_head2), schematic_width * 0.05, 10-delta_head2, color='red'))
            ax_schematic.plot([0.55, 1.7], [delta_head2, delta_head2], 'k--', linewidth=1, color='red')
            ax_schematic.text(1.85, delta_head2 - 0.1, 'Well \nhead 2', color='red', fontsize=12)
        else:
            ax_schematic.add_patch(plt.Rectangle((0.5, delta_head), schematic_width * 0.1, 10-delta_head, color='darkblue'))
    
        # Head level indicators (dashed lines) and Labels Aquifer and Well 1
        ax_schematic.plot([0.5, 1.7], [delta_head, delta_head], 'k--', linewidth=1, color='darkblue')
        ax_schematic.text(0.85, delta_head - 0.1, 'Well \nhead 1', color='darkblue', fontsize=12)
        ax_schematic.plot([0.0, 1.7], [0, 0], 'b--', linewidth=1)
        ax_schematic.text(0.5, 0 - 0.2, 'Cell (aquifer) \nhead', color='blue', fontsize=12)
        # Style
        ax_schematic.set_xlim(0, 2)
        ax_schematic.set_ylim(10, 0)
        ax_schematic.axis('off')
        
        # --- RIGHT AXIS: Q vs Δh plot ---
        if turn:
            ax_plot.plot(Q_values, delta_h_range, label="$Q-\Delta h$ relation 1", color='darkblue', linewidth=4)
            if second:
                ax_plot.plot(Q_values2, delta_h_range2, label="$Q-\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
            if h_target:
                ax_plot.plot(Q_show, delta_head, 'ro',markersize=10, label="h_target")
                ax_plot.plot([0, Q_line], [delta_head, delta_head], linestyle='dotted', color='grey', linewidth=2)
                if second:
                    ax_plot.plot(Q_show2, delta_head2, 'ro',markersize=10)
            else:
                ax_plot.plot(Q_show, delta_head, 'bo',markersize=10, label="Q_target")
                ax_plot.plot([Q_show, Q_show], [aquifer_thickness, h_line], linestyle='dotted', color='grey', linewidth=2)
                if second:
                    ax_plot.plot(Q_show2, delta_head2, 'bo',markersize=10)            
            ax_plot.set_ylabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=12, labelpad=15)
            ax_plot.set_xlabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=12, labelpad=15)
            ax_plot.set_ylim(10, 0)
            ax_plot.set_xlim(0, 1)
        else:
            ax_plot.plot(delta_h_range, Q_values, label="$Q-\Delta h$ relation 1", color='darkblue', linewidth=4)
            if second:
                ax_plot.plot(delta_h_range2, Q_values2, label="$Q-\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
            if h_target:
                ax_plot.plot(delta_head,Q_show, 'ro',markersize=10, label="h_target")
                ax_plot.plot([delta_head, delta_head], [0, Q_line], linestyle='dotted', color='grey', linewidth=2)
                if second:
                    ax_plot.plot(delta_head2, Q_show2, 'ro',markersize=10)
            else:
                ax_plot.plot(delta_head, Q_show,'bo',markersize=10, label="Q_target")
                ax_plot.plot([aquifer_thickness, h_line], [Q_show, Q_show], linestyle='dotted', color='grey', linewidth=2)
                if second:
                    ax_plot.plot(delta_head2, Q_show2, 'bo',markersize=10)  
            ax_plot.set_xlabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=12, labelpad=15)
            ax_plot.set_ylabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=12, labelpad=15)
            ax_plot.set_xlim(0, 10)
            ax_plot.set_ylim(0, 1)
        
        ax_plot.set_title("Flow Between Aquifer and Well (MNW Boundary)", fontsize=14, pad=20)
        ax_plot.tick_params(axis='both', labelsize=12)
        ax_plot.legend(fontsize=12)
    else:
        fig, (ax_schematic, ax_plot) = plt.subplots(1, 2, figsize=(8, 6), width_ratios=[1, 3])
        fig.subplots_adjust(wspace=0.5)
        
        ax_schematic.axis('off')  # Hide all axis lines and ticks
        ax_schematic.set_frame_on(False)  # Hide the frame (border)
        ax_schematic.set_xticks([])
        ax_schematic.set_yticks([])
        
        # --- RIGHT AXIS: Q vs Δh plot ---
        if turn:
            ax_plot.plot(Q_values, delta_h_range, label="$Q-\Delta h$ relation 1", color='black', linewidth=4)
            if second:
                ax_plot.plot(Q_values2, delta_h_range2, label="$Q-\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)           
            ax_plot.set_ylabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=12, labelpad=15)
            ax_plot.set_xlabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=12, labelpad=15)
            ax_plot.set_ylim(10, 0)
            ax_plot.set_xlim(0, 1)
        else:
            ax_plot.plot(delta_h_range, Q_values, label="$Q-\Delta h$ relation 1", color='black', linewidth=4)
            if second:
                ax_plot.plot(delta_h_range2, Q_values2, label="$Q-\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
            ax_plot.set_xlabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=12, labelpad=15)
            ax_plot.set_ylabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=12, labelpad=15)
            ax_plot.set_xlim(0, 10)
            ax_plot.set_ylim(0, 1)
        
        ax_plot.set_title("Flow Between Aquifer and Well (MNW Boundary)", fontsize=14, pad=20)
        ax_plot.tick_params(axis='both', labelsize=12)
        ax_plot.legend(fontsize=12)
    
    
    # Show in Streamlit
    st.pyplot(fig)
    
    
    if visualize:   
        # --- CONSTANT DISCHARGE PLOT ---
        h_2nd = np.linspace(0, 20, 20)
        Q_2nd = np.ones_like(h_2nd) * Q_show
        h_cell = 10
        h_well = h_cell - delta_head
        
        # Interpolate Q at h_thr using the Q(h_well) relation
        Q_interp = interp1d(h_cell - delta_h_range, Q_values, kind='linear', fill_value="extrapolate")
        #Q_thr = Q_interp(h_thr)
        h_well_range = h_cell - delta_h_range  # h_cell is fixed (currently set to 10)
        
        # --- Plot Q vs. h_well ---
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        if turn:
            ax2.plot(Q_2nd, h_2nd, color='black', label=fr"Discharge $Q = {Q_show:.1f}$", linewidth=4)
            ax2.axhline(y=h_cell, linestyle='dotted', color='blue', linewidth=2, label='$h_{cell}$') # Vertical line for h_cell across the entire Q range
            #ax2.plot(Q_values, h_well_range, linestyle='dotted', color='purple', linewidth=2, label=r"$Q(h_{well})$")
            ax2.plot(Q_values, h_well_range, color='darkblue', linewidth=3, label=r"$Q_w(h_{well})$")
            ax2.plot(Q_show, h_cell, 'bo',markersize=10, label='head in cell')
            ax2.plot(Q_show, h_well, 'ro',markersize=10, label='head in well')
            #ax2.axhline(y=h_thr, linestyle='--', color='orange', linewidth=2, label=r"$h_{thr}$")
            ax2.set_ylabel("Hydraulic Head $h_n$ [L]", fontsize=14)
            ax2.set_xlabel("Discharge $Q$ [L³/T]", fontsize=14)
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 20)
        else:
            
            ax2.plot(h_2nd, Q_2nd, color='black', label=fr"Discharge $Q = {Q_show:.1f}$", linewidth=4)
            ax2.axvline(x=h_cell, linestyle='dotted', color='blue', linewidth=2, label='$h_{cell}$') # Vertical line for h_cell across the entire Q range
            ax2.plot(h_well_range, Q_values, color='darkblue', linewidth=3, label=r"$Q_w(h_{well})$")
            ax2.plot(h_cell, Q_show, 'bo',markersize=10, label='head in cell')
            ax2.plot(h_well, Q_show, 'ro',markersize=10, label='head in well')
            #ax2.axvline(x=h_thr, linestyle='--', color='orange', linewidth=2, label=r"$h_{thr}$")
            ax2.set_xlabel("Hydraulic Head $h_n$ [L]", fontsize=14)
            ax2.set_ylabel("Discharge $Q$ [L³/T]", fontsize=14)
            ax2.set_ylim(0, 1)
            ax2.set_xlim(0, 20)
        
        ax2.set_title("Q-h Behavior for MNW Boundary", fontsize=16)
        ax2.tick_params(axis='both', labelsize=12)        
        ax2.legend(fontsize=12, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
        
        columns_fig2=st.columns((2,6,1))
        with columns_fig2[1]:
            st.pyplot(fig2, bbox_inches='tight')    
        
        
        st.write('**Drawdown and flow in the well:**')
        if h_target:
            st.write(':grey[**Drawdown in the well**] (in m) = %5.2f' %delta_head)
            st.write(':blue[**Discharge $Q$ to the well**] (in m³/s) = %5.3f' %Q_show)
            if second:
                st.write(':red[**Discharge $Q2$ to the well**] (in m³/s) = %5.3f' %Q_show2)
        else:
            st.write(':grey[**Discharge to the well**] (in m³/s) = %5.3f' %Q_show)
            st.write(':blue[**Drawdown $$\Delta h$$ in the well**] (in m) = %5.2f' %delta_head)
            if second:
                st.write(':red[**Drawdown $$\Delta h2$$ in the well**] (in m) = %5.2f' %delta_head2)



        # THIRD PLOT HERE - Q vs h_cell (with head and discharge thresholds)
        with st.expander('Show the MNW boundary with varying cell heads'):  
            
            # Plotting range
            h_3rd = np.linspace(0, 20, 300)
            
            # User INPUT
            col_input_fig3 = st.columns((1,1))
            with col_input_fig3[0]:
                h_cell_slider = st.slider("Head in the Cell $h_{cell}$ [m]", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
            with col_input_fig3[1]:
                h_thr = st.slider("Define threshold head $h_{thr}$ [m]", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
                th = st.toggle("Apply pumping thresholds")
                if th:
                    Q_range = st.slider("Discharge cutoff range $[Q_{mn}, Q_{mx}]$ [m³/s]", 0.0, 1.0, (0.1, 0.15), 0.01)
                    Q_mn, Q_mx = Q_range
            
            # Computation of values to show in the plots - Currently only working with Q_target; head_target needs to be implemented for the second parameter set
            # Compute head difference assuming h_well stays at threshold if h_cell < h_thr
            delta_h_adjusted = np.clip(h_3rd - h_thr, 0, None)
            
            h_well = h_cell_slider - delta_head
            # Take the discharge that relates to the adjusted delta_h, define a function to interpolate
            Q_interp_func  = interp1d(delta_h_range, Q_values,  bounds_error=False, fill_value="extrapolate")
            # Use the interpolated value, but limit it to Q_show if it's larger
            Q_plot  = np.minimum(Q_interp_func(delta_h_adjusted),  Q_show)
            if th:
                Q_plot_mn = np.where(Q_plot <= Q_mn, 0, Q_plot)
                Q_plot_mx = np.where(Q_plot <= Q_mx, 0, Q_plot)
            
            # Generate the point to show
            if h_well >= h_thr:
                delta_h_current = h_cell_slider - h_well
            else:
                delta_h_current = max(h_cell_slider - h_thr, 0)
                
            Q_dot = min(Q_interp_func(delta_h_current), Q_show)                
            
            if th:
                # Hysteresis logic with session state
                if st.session_state.Q_off:
                    if Q_dot > Q_mx:
                        Q_dot_th = Q_dot
                        st.session_state.Q_off = False
                    else:
                        Q_dot_th = 0
                else:
                    if Q_dot < Q_mn:
                        Q_dot_th = 0
                        st.session_state.Q_off = True
                    else:
                        Q_dot_th = Q_dot                
            
            # Repeat computation for second parameter set // ToDo: the subseqent second case needs to differentiat according to head / flow target; currently only flow target
            if second:
                if h_target:
                    h_well2 = h_cell_slider - delta_head
                    Q_interp_func2 = interp1d(delta_h_range, Q_values2, bounds_error=False, fill_value="extrapolate")
                    Q_plot2 = np.minimum(Q_interp_func2(delta_h_adjusted), Q_show2)
                    # Generate the point to show
                    if h_well2 >= h_thr:
                        delta_h_current2 = h_cell_slider - h_well2
                    else:
                        delta_h_current2 = max(h_cell_slider - h_thr, 0)
                        
                    Q_dot2 = min(Q_interp_func2(delta_h_current2), Q_show2)                
                    
                    if th:
                        # Hysteresis logic with session state
                        if st.session_state.Q_off2:
                            if Q_dot2 > Q_mx:
                                Q_dot_th2 = Q_dot2
                                st.session_state.Q_off2 = False
                            else:
                                Q_dot_th2 = 0
                        else:
                            if Q_dot2 < Q_mn:
                                Q_dot_th2 = 0
                                st.session_state.Q_off2 = True
                            else:
                                Q_dot_th2 = Q_dot2
                else:
                    h_well2 = h_cell_slider - delta_head2
                    Q_interp_func2 = interp1d(delta_h_range, Q_values2, bounds_error=False, fill_value="extrapolate")
                    Q_plot2 = np.minimum(Q_interp_func2(delta_h_adjusted), Q_show)
                    # Generate the point to show
                    if h_well2 >= h_thr:
                        delta_h_current2 = h_cell_slider - h_well2
                    else:
                        delta_h_current2 = max(h_cell_slider - h_thr, 0)
                        
                    Q_dot2 = min(Q_interp_func2(delta_h_current2), Q_show)                
                    
                    if th:
                        # Hysteresis logic with session state
                        if st.session_state.Q_off2:
                            if Q_dot2 > Q_mx:
                                Q_dot_th2 = Q_dot2
                                st.session_state.Q_off2 = False
                            else:
                                Q_dot_th2 = 0
                        else:
                            if Q_dot2 < Q_mn:
                                Q_dot_th2 = 0
                                st.session_state.Q_off2 = True
                            else:
                                Q_dot_th2 = Q_dot2

            
            # Create the plot
            fig3, ax3 = plt.subplots(figsize=(10, 10))
            if turn:
                if th:
                    ax3.plot(Q_plot, h_3rd, color='darkblue', linewidth=1, linestyle=':', label=r"$Q(h_{cell})$ with threshold")
                    ax3.plot(Q_dot_th, h_cell_slider, 'bo', markersize=10, label='head in cell')
                    if second:
                        ax3.plot(Q_plot2, h_3rd, color='red', linewidth=1, linestyle=':', label=r"$Q(h_{cell})$ with threshold")
                        ax3.plot(Q_dot_th2, h_cell_slider, 'bo', markersize=10, label='head in cell')
                    ax3.plot(Q_plot_mn, h_3rd, color='darkblue', linewidth=3, label=r"$Q(h_{cell})$ with $h_{thr}$ and $Q_{mn}$")
                    ax3.plot(Q_plot_mx, h_3rd, color='darkblue', linewidth=3, linestyle='--', label=r"$Q(h_{cell})$ with $h_{thr}$ and $Q_{mn}$")
                else:                
                    ax3.plot(Q_plot, h_3rd, color='darkblue', linewidth=3, label=r"$Q(h_{cell})$ with threshold")
                    ax3.plot(Q_dot, h_cell_slider, 'bo', markersize=10, label='head in cell')
                    if second:
                        ax3.plot(Q_plot2, h_3rd, color='red', linewidth=2, linestyle=':', label=r"$Q(h_{cell})$ with threshold")
                        ax3.plot(Q_dot2, h_cell_slider, 'ro', markersize=10, label='head in cell')
                ax3.axhline(y=h_cell_slider, linestyle='--', color='blue', linewidth=2, label='$h_{cell}$ (user-defined)')
                ax3.axhline(y=h_thr, linestyle='--', color='orange', linewidth=2, label=r"$h_{thr}$")
                if h_well >= h_thr:
                    ax3.plot(Q_dot, h_well, 'ro',markersize=10, label='head in well')
                else:
                    ax3.plot(Q_dot, h_thr, 'ro',markersize=10, label='head in well')
                if second:
                    if h_well2 >= h_thr:
                        ax3.plot(Q_dot2, h_well2, 'ro',markersize=10, label='head in well')
                    else:
                        ax3.plot(Q_dot2, h_thr, 'ro',markersize=10, label='head in well')                    
                ax3.set_xlabel("Discharge $Q$ [m³/s]", fontsize=14)
                ax3.set_ylabel("Hydraulic heads $h$ [m]", fontsize=14)
                ax3.set_xlim(0, 1)
                ax3.set_ylim(0, 20)
            else:
                if th:
                    ax3.plot(h_3rd, Q_plot, color='darkblue', linewidth=1, linestyle=':', label=r"$Q(h_{cell})$ with threshold")
                    ax3.plot(h_cell_slider, Q_dot_th, 'bo', markersize=10, label='head in cell')
                    if second:
                        ax3.plot(h_3rd, Q_plot_th, color='red', linewidth=1, linestyle=':', label=r"$Q(h_{cell})$ with threshold")
                        ax3.plot(h_cell_slider, Q_dot_th2, 'bo', markersize=10, label='head in cell')
                    ax3.plot(h_3rd, Q_plot_mn,  color='darkblue', linewidth=3, label=r"$Q(h_{cell})$ with $h_{thr}$ and $Q_{mn}$")
                    ax3.plot(h_3rd, Q_plot_mx,  color='darkblue', linewidth=3, linestyle='--', label=r"$Q(h_{cell})$ with $h_{thr}$ and $Q_{mn}$")  
                                        
                else:
                    ax3.plot(h_3rd, Q_plot, color='darkblue', linewidth=3, label=r"$Q(h_{cell})$ with threshold")
                    ax3.plot(h_cell_slider, Q_dot, 'bo', markersize=10, label='head in cell')
                    if second:
                        ax3.plot(h_3rd, Q_plot2, color='red', linewidth=2, linestyle=':', label=r"$Q(h_{cell})$ with threshold")
                        ax3.plot(h_cell_slider, Q_dot2, 'ro', markersize=10, label='head in cell')
                ax3.axvline(x=h_cell_slider, linestyle='--', color='blue', linewidth=2, label='$h_{cell}$ (user-defined)')
                ax3.axvline(x=h_thr, linestyle='--', color='orange', linewidth=2, label=r"$h_{thr}$")

                if h_well >= h_thr:
                    ax3.plot(h_well, Q_dot, 'ro',markersize=10, label='head in well')
                else:
                    ax3.plot(h_thr, Q_dot, 'ro',markersize=10, label='head in well')
                if second:
                    if h_well2 >= h_thr:
                        ax3.plot(h_well2, Q_dot2, 'ro',markersize=10, label='head in well')
                    else:
                        ax3.plot(h_thr, Q_dot2, 'ro',markersize=10, label='head in well')                    
                ax3.set_xlabel("Hydraulic heads $h$ [m]", fontsize=14)
                ax3.set_ylabel("Discharge $Q$ [m³/s]", fontsize=14)
                ax3.set_xlim(0, 20)
                ax3.set_ylim(0, 1)
            
            ax3.set_title("Q-h Behavior for Cell Head (Threshold Considered)", fontsize=16)
            ax3.tick_params(axis='both', labelsize=12)
            ax3.legend(fontsize=12)
            
            st.pyplot(fig3)
    
Q_h_plot()

st.markdown("---")
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
