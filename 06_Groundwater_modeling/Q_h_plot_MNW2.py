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
- $A$ Linear aquifer-loss coefficient; Represents head loss due to flow through the aquifer to the well [T/L2].
- $B$ Linear well-loss coefficient. Accounts for head loss associated with linear flow components in the well [T/L2].
- $C$ Nonlinear well-loss coefficient, Governs the nonlinear (e.g., turbulent) head loss in the well. [T^P/L^(3P-1)], and
- $P$  is the power (exponent) of the nonlinear discharge component of well loss.
""")

# Functions

# Define the nonlinear equation to solve: Q = Δh / (A + B + C * Q**(p-1))
def discharge_equation(Q, delta_h, A, B, C, p):
    return Q - delta_h / (A + B + C * Q**(p - 1))
    
# Callback function to update session state
def update_A():
    st.session_state.A = st.session_state.A_input
def update_B():
    st.session_state.B = st.session_state.B_input
def update_C():
    st.session_state.C = st.session_state.C_input
def update_P():
    st.session_state.P = st.session_state.P_input 
    
# Initialize session state for value and toggle state
st.session_state.A = 1.0
st.session_state.B = 1.0
st.session_state.C = 1.0
st.session_state.P = 2.0

st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    # Switches
    columns1 = st.columns((1,1), gap = 'large')
    with columns1[1]:
        turn = st.toggle('Toggle to turn the plot 90 degrees')
        st.session_state.number_input = st.toggle("Toggle to use Slider or Number input.")
    
    columns2 = st.columns((1,1), gap = 'large')
    
    with columns2[0]:
        if st.session_state.number_input:
            A = st.number_input("**A**", 0.01, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A)
        else:
            A = st.slider      ("**A**", 0.01, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A)
        if st.session_state.number_input:
            B = st.number_input("**B**", 0.01, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B)
        else:
            B = st.slider      ("**B**", 0.01, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B)
        if st.session_state.number_input:
            C = st.number_input("**C**", 0.01, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C)
        else:
            C = st.slider      ("**C**", 0.01, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C)            
    with columns2[1]:
        if st.session_state.number_input:
            P = st.number_input("**P**", 1.0, 2.0, st.session_state.P, 0.1, key="P_input", on_change=update_P)
        else:
            P = st.slider      ("**P**", 1.0, 2.0, st.session_state.P, 0.1, key="P_input", on_change=update_P)
    
    # Define aquifer head range / Range of head differences Δh
    delta_h_range = np.linspace(0.01, 10, 200)
    Q_values = []
    
    # Solve for Q_n for each Δh
    for delta_h in delta_h_range:
        Q_initial_guess = delta_h / (A + B)  # reasonable initial guess
        Q_solution, = fsolve(discharge_equation, Q_initial_guess, args=(delta_h, A, B, C, P))
        Q_values.append(Q_solution)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10))
    if turn:
        ax.plot(Q_values, delta_h_range, label="Discharge $Q_n$", color='black', linewidth=3)
        # Labels and formatting
        ax.set_ylabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=14)
        ax.set_xlabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=14)
        ax.set_ylim(10, 0)
        ax.set_xlim(0, 5)   
    else:
        ax.plot(delta_h_range, Q_values, label="Discharge $Q_n$", color='black', linewidth=3)
        # Labels and formatting
        ax.set_xlabel("Head Difference Δh = $h_{WELL} - h_{aq}$ (m)", fontsize=14)
        ax.set_ylabel("Flow from the Ground-Water System to the MNW $Q_W$ (m³/s)", fontsize=14)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        
    ax.set_title("Flow Between Groundwater and MNW boundary", fontsize=16)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(True)
    ax.legend(fontsize=14)
    
    st.pyplot(fig)

Q_h_plot()

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
