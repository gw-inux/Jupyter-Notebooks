import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import scipy.interpolate as interp
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
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("Process-based implementation of Flow to Pumping wells")
st.subheader("Theory and Concept of the Multi-Node-Well package (MNW) in MODFLOW", divider="green")

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
st.session_state.Q_show = 0.1
st.session_state.A = 5.0
st.session_state.B = 5.0
st.session_state.C = 5.0
st.session_state.P = 2.0
st.session_state.A2 = 5.0
st.session_state.B2 = 5.0
st.session_state.C2 = 5.0
st.session_state.P2 = 2.0
st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    "---"
    # Switches
    columns1 = st.columns((1,1), gap = 'large')              
    with columns1[0]:
        turn = st.toggle('Toggle to turn the plot 90 degrees')
        st.session_state.number_input = st.toggle("Toggle to use Slider or Number input.")
        second = st.toggle("Toggle to define a second parameter set for comparison")
    with columns1[1]:
        st.write('**:green[Target for evaluation/visualization]**')
        h_target = st.toggle('Toggle for Q-target/h-target')

    columns2 = st.columns((1,1), gap = 'large')              
    with columns2[1]:
        if h_target:
            if st.session_state.number_input:
                dh_show = st.number_input("**Drawdown in the pumping well**", 0.01, 10.0, 5.0, 0.1, key="dh_show_input", on_change=update_dh_show)
            else:
                dh_show = st.slider      ("**Drawdown in the pumping well**", 0.01, 10.0, 5.0, 0.1, key="dh_show_input", on_change=update_dh_show)
        else:
            if st.session_state.number_input:
                Q_show = st.number_input("**Discharge in the pumping well**", 0.001, 1.0, 0.1, 0.001, key="Q_show_input", on_change=update_Q_show)
            else:
                Q_show = st.slider      ("**Discharge in the pumping well**", 0.001, 1.0, 0.1, 0.001, key="Q_show_input", on_change=update_Q_show)                
    "---"
    columns3 = st.columns((1,1,1,1))
    
    with columns3[0]:
        if st.session_state.number_input:
            A = st.number_input("**Linear aquifer-loss coeff. A in s/m²**", 0.01, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A)
        else:
            A = st.slider      ("**Linear aquifer-loss coeff. A in s/m²**", 0.01, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A)
    with columns3[1]:
        if st.session_state.number_input:
            B = st.number_input("**Linear well-loss coeff. B in s/m²**", 0.01, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B)
        else:
            B = st.slider      ("**Linear well-loss coeff. B in s/m²**", 0.01, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B)        
    with columns3[2]:
        if st.session_state.number_input:
            C = st.number_input("**Nonlinear well-loss coeff. C in s^P/m^(3P-1)**", 0.01, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C)
        else:
            C = st.slider      ("**Nonlinear well-loss coeff. C in s^P/m^(3P-1)**", 0.01, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C)   
    with columns3[3]:
        if st.session_state.number_input:
            P = st.number_input("**Power of the nonlinear well-loss P**", 1.0, 4.0, st.session_state.P, 0.1, key="P_input", on_change=update_P)
        else:
            P = st.slider      ("**Power of the nonlinear well-loss P**", 1.0, 4.0, st.session_state.P, 0.1, key="P_input", on_change=update_P)
    
    if second:
        columns4 = st.columns((1,1,1,1))
    
        with columns4[0]:
            if st.session_state.number_input:
                A2 = st.number_input("**comparison A2**", 0.01, 10.0, st.session_state.A2, 0.1, key="A2_input", on_change=update_A2)
            else:
                A2 = st.slider      ("**comparison A2**", 0.01, 10.0, st.session_state.A2, 0.1, key="A2_input", on_change=update_A2)
        with columns4[1]:
            if st.session_state.number_input:
                B2 = st.number_input("**comparison B2**", 0.01, 10.0, st.session_state.B2, 0.1, key="B2_input", on_change=update_B2)
            else:
                B2 = st.slider      ("**comparison B2**", 0.01, 10.0, st.session_state.B2, 0.1, key="B2_input", on_change=update_B2)        
        with columns4[2]:
            if st.session_state.number_input:
                C2 = st.number_input("**comparison C2**", 0.01, 10.0, st.session_state.C2, 0.1, key="C2_input", on_change=update_C2)
            else:
                C2 = st.slider      ("**comparison C2**", 0.01, 10.0, st.session_state.C2, 0.1, key="C2_input", on_change=update_C2)   
        with columns4[3]:
            if st.session_state.number_input:
                P2 = st.number_input("**comparison P2**", 1.0, 4.0, st.session_state.P2, 0.1, key="P2_input", on_change=update_P2)
            else:
                P2 = st.slider      ("**comparison P2**", 1.0, 4.0, st.session_state.P2, 0.1, key="P2_input", on_change=update_P2)
   
    "---"
    aquifer_thickness = 10.0
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
        
    # PLOT HERE
    # Create side-by-side plots
    fig, (ax_schematic, ax_plot) = plt.subplots(1, 2, figsize=(12, 6), width_ratios=[1, 3])
    
    # --- LEFT AXIS: Schematic view (Aquifer head vs Well head) ---

    schematic_width = 1.0
    
    # Aquifer: full height blue rectangle
    ax_schematic.add_patch(plt.Rectangle((0.0, 0), schematic_width*0.5, aquifer_thickness, color='skyblue'))
    ax_schematic.add_patch(plt.Rectangle((0.6, 0), schematic_width*0.5, aquifer_thickness, color='skyblue'))
    
    # Well water level: narrower grey rectangle, Head level indicators (dashed lines) and Labels wellls
    if second and not h_target:
        ax_schematic.add_patch(plt.Rectangle((0.50, delta_head),  schematic_width * 0.05, 10-delta_head, color='darkblue'))
        ax_schematic.add_patch(plt.Rectangle((0.55, delta_head2), schematic_width * 0.05, 10-delta_head2, color='red'))
        ax_schematic.plot([0.55, 1.7], [delta_head2, delta_head2], 'k--', linewidth=1)
        ax_schematic.text(1.15, delta_head2 - 0.2, 'Well Head 2', color='red', fontsize=10)
    else:
        ax_schematic.add_patch(plt.Rectangle((0.5, delta_head), schematic_width * 0.1, 10-delta_head, color='darkblue'))

    
    # Head level indicators (dashed lines) and Labels Aquifer and Well 1
    ax_schematic.plot([0.5, 1.7], [delta_head, delta_head], 'k--', linewidth=1)
    ax_schematic.text(1.15, delta_head - 0.2, 'Well Head', color='black', fontsize=10)
    ax_schematic.plot([0.0, 1.7], [0, 0], 'b--', linewidth=1)
    ax_schematic.text(1.15, 0 - 0.2, 'Aquifer Head', color='blue', fontsize=10)
     
    # Style
    ax_schematic.set_xlim(0, 2)
    ax_schematic.set_ylim(10, 0)
    ax_schematic.axis('off')
    
    
    # --- RIGHT AXIS: Q vs Δh plot ---
    if turn:
        ax_plot.plot(Q_values, delta_h_range, label="$Q-h$ relation", color='darkblue', linewidth=3)
        if h_target:
            ax_plot.plot(Q_show, delta_head, 'ro',markersize=10, label="h_target")
            ax_plot.plot([0, Q_line], [delta_head, delta_head], linestyle='dotted', color='grey', linewidth=2)
        else:
            ax_plot.plot(Q_show, delta_head, 'bo',markersize=10, label="Q_target")
            ax_plot.plot([Q_show, Q_show], [aquifer_thickness, h_line], linestyle='dotted', color='grey', linewidth=2)
        if second:
            ax_plot.plot(Q_values2, delta_h_range2, label="$Q-h$ relation 2", linestyle='--', color='red', linewidth=3)
            if h_target:
                ax_plot.plot(Q_show2, delta_head2, 'ro',markersize=10)
            else:
                ax_plot.plot(Q_show2, delta_head2, 'bo',markersize=10)            
        ax_plot.set_ylabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=14)
        ax_plot.set_xlabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=14)
        ax_plot.set_ylim(10, 0)
        ax_plot.set_xlim(0, 1)
    else:
        ax_plot.plot(delta_h_range, Q_values, label="Discharge $Q_n$", color='darkblue', linewidth=3)
        if h_target:
            ax_plot.plot(delta_head,Q_show, 'ro',markersize=10, label="h_target")
            ax_plot.plot([delta_head, delta_head], [0, Q_line], linestyle='dotted', color='grey', linewidth=2)
        else:
            ax_plot.plot(delta_head, Q_show,'bo',markersize=10, label="Q_target")
            ax_plot.plot([aquifer_thickness, h_line], [Q_show, Q_show], linestyle='dotted', color='grey', linewidth=2)
        if second:
            ax_plot.plot(delta_h_range2, Q_values2, label="Discharge $Q2_n$", linestyle='--', color='red', linewidth=3)
            if h_target:
                ax_plot.plot(delta_head2, Q_show2, 'ro',markersize=10)
            else:
                ax_plot.plot(delta_head2, Q_show2, 'bo',markersize=10)  
        ax_plot.set_xlabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=14)
        ax_plot.set_ylabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=14)
        ax_plot.set_xlim(0, 10)
        ax_plot.set_ylim(0, 1)
    
    ax_plot.set_title("Flow Between Aquifer and Well (MNW Boundary)", fontsize=14)
    ax_plot.tick_params(axis='both', labelsize=12)
    ax_plot.legend(fontsize=12)
    
    # Show in Streamlit
    st.pyplot(fig)
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
        

Q_h_plot()

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
