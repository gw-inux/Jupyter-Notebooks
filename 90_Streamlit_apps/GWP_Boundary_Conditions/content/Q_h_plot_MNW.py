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
import json
from streamlit_book import multiple_choice

# path to questions for the assessments (direct path)
path_quest_ini   = "C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_mnw.json"
path_quest_plot1 = "C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p1.json"
path_quest_plot2 = "C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p2.json"
path_quest_plot3 = "C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p3.json"
path_quest_final = "C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_mnw.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_plot1, "r", encoding="utf-8") as f:
    quest_plot1 = json.load(f)
    
with open(path_quest_plot2, "r", encoding="utf-8") as f:
    quest_plot2 = json.load(f)

with open(path_quest_plot3, "r", encoding="utf-8") as f:
    quest_plot3 = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
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

# --- functions

def prep_log_slider(default_val: float, log_min: float, log_max: float, step: float = 0.01, digits: int = 2):
    """
    Prepares labels and default for a log-scale select_slider.

    Returns:
    --------
    labels : list of str
        Formatted string labels in scientific notation.
    default_label : str
        Closest label to the given default_val.
    """
    # --- Generate value list and labels
    log_values = np.arange(log_min, log_max + step, step)
    values = 10 ** log_values
    fmt = f"{{0:.{digits}e}}"
    labels = [fmt.format(v) for v in values]

    # --- Find closest label for default
    idx_closest = np.abs(values - default_val).argmin()
    default_label = labels[idx_closest]

    return labels, default_label
    
def get_label(val: float, labels: list[str]) -> str:
    """Given a float value and a list of scientific notation labels, return the closest label."""
    label_vals = [float(l) for l in labels]
    idx = np.abs(np.array(label_vals) - val).argmin()
    return labels[idx]

def get_step(val: float) -> float:
    """Return a step that modifies the first digit after the decimal point in scientific notation."""
    if val == 0:
        return 1e-8  # fallback
    exponent = int(np.floor(np.log10(abs(val))))
    return 10 ** (exponent - 1)

st.title("Theory and Concept of the :rainbow[Multi-Node-Well Boundary (MNW)]")
st.subheader("Process-based implementation of Flow to Pumping wells", divider="rainbow")

st.markdown("""
#### 💡 Motivation: Why Multi-Node Wells (MNW)?
""")

# Initial plot
# Slider input and plot
columns0 = st.columns((1,1), gap = 'large')
with columns0[0]:
    st.markdown("""  
    Let’s reflect on these questions:
    
    1. **How do well losses affect the actual water level inside a pumping well?**
    
    2. **What happens if the water level in the well drops below a critical threshold? Should pumping continue?**
    
    ▶️ The **Multi-Node Well (MNW)** package in MODFLOW supports more realistic simulation of well hydraulics. Even in single-layer systems, it allows you to:
    - Account for **drawdown within the wellbore** ($h_{aq}-h_{well}$) due to head losses,
    - Define **limiting water levels** below which pumping stops,
    - Simulate wells that **automatically shut off** or restart depending on drawdown conditions.
    
    The following interactive plots let you explore how discharge, cell head, and cell-to-well conductance _CWC_ interact and result in a specific drawdown in the well.
    
    In contrast, the **WEL boundary in MODFLOW** is a regular Neumann-type boundary condition (2nd type boundary with defined flow). The **WEL**-toggle allows you to see the equivalent _Q-h_-plot for a WEL boundary in MODFLOW where the defined flow _Q_ is independet from the hydraulic head _h_.
    """)

with columns0[1]:
    # CWC
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
    col_ini = st.columns((3,1.2))
    with col_ini[0]:      
        labels, default_label = prep_log_slider(default_val = 3e-3, log_min = -5, log_max = 0)
        selected_Ci = st.select_slider("**Conductance :grey[$CWC$]** in m²/s", labels, default_label, key = "MNW_CWCi")
        st.session_state.CWCi = float(selected_Ci)
        
    with col_ini[1]:
        WEL_equi = st.toggle('**WEL**')
        
    # COMPUTATION
    # Define aquifer head range
    h_aqi = np.linspace(0, 20, 200)
    QPi = np.full_like(h_aqi, -0.02)
    h_ni = 10.0 # Example head for the cell
    h_WELLi = np.linspace(0, 20, 200)
    Qi = (h_WELLi - h_ni) * st.session_state.CWCi
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, QPi, color='black', linewidth=4, label='$Q$-$h_{aq}$')
    if WEL_equi:
        ax.set_xlabel("Heads in the WEL-Aquifer System (m)", fontsize=14, labelpad=15)
        ax.set_ylabel("Flow into the Groundwater \nfrom the WEL boundary $Q_{WEL}$ (m³/s)", fontsize=14, labelpad=15)
        ax.set_title("Flow Between Groundwater and WEL", fontsize=16, pad=10)
    else:
        ax.plot(h_WELLi, Qi, color='lightgrey', linestyle='--', linewidth=3, label='$Q$-$h_{well}$')
        # Determine the y-values for h = 10
        Qi_10 = (10.0 - h_ni) * st.session_state.CWCi
        QPi_10 = -0.02     
    
        # Draw vertical line at Qi and h_intersect
        h_is = h_ni + (-0.02 / st.session_state.CWCi)
        ax.plot([h_is, h_is], [QPi_10, -0.05], color='lightgrey',linestyle=':', linewidth=3)
    
        ax.set_xlabel("Heads in the MNW-Aquifer System (m)", fontsize=14, labelpad=15)
        ax.set_ylabel("Flow into the Groundwater \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14, labelpad=15)
        ax.set_title("Flow Between Groundwater and MNW", fontsize=16, pad=10)
        ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    
    # Draw vertical line at QPi and h = 10
    ax.plot([10, 10], [-0.02, -0.05], color='black',linestyle=':', linewidth=3)
    ax.axvline(10, color='grey', linestyle='--', linewidth=0.8)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 

    ax.legend(loc="upper left", fontsize=14)
    st.pyplot(fig)
    
    st.markdown("""
    Please note that for this plot the head in the cell around the pumping well is **defined as $h_{aq}$ = 10 m** _(black dotted line)_.
    
    The :grey[dashed line $Q$-$h_{aq}$] illustrate the relationship between discharge and hydraulic head in well relative to the head in the cell (drawdown) whereas the black and grey dotted lines indicate the hydraulic heads in the cell and the well respectively.
    
    This **initial plot** is designed to bridge the gap between traditional Q-h plots on paper and the :rainbow[**interactive plots**] provided further down in the app. These allow you to explore the _Q_-_h_ relationships more intuitively, supported by interactive controls and guided instructions.
    """)

#TODO
st.markdown("""
####  🎯 Learning Objectives
By the end of this section, learners will be able to:
- Understand the conceptual and practical differences between Multi-Node Wells (MNW) and traditional Well (WEL) boundaries in MODFLOW.
- Evaluate the influence of well efficiency, skin effects, and conductance on MNW flow behavior.
- Interpret Q–h relationships for MNWs and how they reflect physical and operational limits of well systems.
- Describe how head-dependent flow and constraints such as pump limits and cell drawdowns are represented in the MNW package.
""")

with st.expander('**Show the initial assessment** - to assess your existing knowledge'):
    st.markdown("""
    #### 📋 Initial assessment
    You can use the initial questions to assess your existing knowledge.
    """)

    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_ini[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_ini[i]["options"],
                success=quest_ini[i].get("success", "✅ Correct."),
                error=quest_ini[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_ini[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_ini[i]["options"],
                success=quest_ini[i].get("success", "✅ Correct."),
                error=quest_ini[i].get("error", "❌ Not quite.")
            )
            
st.subheader('🧪 Theory and Background', divider="rainbow")
st.markdown("""
This app calculates the flow between a Multi-Node-Well (MNW) and a model cell depending on the system parameters describing the flow in the vicinity of the well and into the well.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    This app calculates the flow between a Multi-Node-Well (MNW) and a model cell depending on the system parameters describing the flow in the vicinity of the well and into the well.
     
    In general, the flow into the well that is placed in the n-th cell is described with a cell-to-well conductance:
    """)
    st.latex(r'''Q_n = CWC_n (h_{well} - h_{aq,n})''')
    
    st.markdown("""
    where:
    - $Q_n$ is the flow between the n-th cell and the well, taken as positive if it is directed into the cell [L3/T]
    - $h_{well}$ is the head in the well (L),
    - $CWC_n$ is the n-th cell-to-well conductance [L2/T], and
    - $h_{aq,n}$ is the (aquifer) head in the n-th cell of the model [L]. (_Note: This head depends on model parameters and boundary stresses (such as pumping), and it may vary across different states or time steps._)
    
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

st.subheader('Interactive plots to understand the general characteristics of the discharge-head relationships in MNW package', divider='rainbow')

st.markdown("""
The subsequent interactive plots allows you to investigate different aspects of the Multi-Node-Well (MNW) boundary in MODFLOW.

:blue[**PLOT 1 - Hydraulic heads in the MNW boundary**]:
Illustrates the additional drawdown in the well due to the Cell-to-Well conductance CWC. Two parameter sets for the CWC can be used.

:green[**PLOT 2 - Q-h behavior MNW boundary**]: An interactive plot of the Q-h relationship for the cell ($Q-h_{aq}$)and the well ($Q-h_{well}$).

:red[**PLOT 3 - Q-h bevaior for the cell head with thresholds**]: Illustrates the effect of threshold on the abstraction rate.

_For all plots, the application allows by toggles:_
- to turn the plots by 90 degrees,
- to switch between number input or sliders.
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
if 'second' not in st.session_state:
    st.session_state.second = False

# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Choose the plot

    col_plot = st.columns((1,1,1), gap = 'small')              
    with col_plot[1]:
        plot_choice = st.selectbox( "**SELECT a plot to display:**", ["🔵 Plot 1", "🟢 Plot 2", "🔴 Plot 3"])
        
    if plot_choice == '🔵 Plot 1':
        show_plot1 = True
        show_plot2 = False
        show_plot3 = False
        explanation = False
        instruction = False
    if plot_choice == '🟢 Plot 2':
        show_plot2 = True
        show_plot1 = False
        show_plot3 = False
        explanation = False
        instruction = False
        st.session_state.second = False
    if plot_choice == '🔴 Plot 3':
        show_plot3 = True
        show_plot1 = False
        show_plot2 = False
        explanation = False
        instruction = False
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    st.markdown("""
       #### :rainbow[INPUT CONTROLS]
        """)
    # Switches
    columns1 = st.columns((1,1,1), gap = 'small')              
    
    with columns1[0]:
        with st.expander("Modify the **Plot Control**"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="MNW_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number input.")
            visualize = st.toggle(':rainbow[**Make the plot alive**] and visualize the input values', key="MNW_vis", value=True)
    
    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Discharge**]'):
        # The additional controls only for visualization
            if visualize:
                st.write('**:green[Target for evaluation/visualization]**')
                h_target = st.toggle('Toggle for :blue[**Q-**] or :red[**H-**]target')
    
                if h_target:
                    st.markdown(":red[**H-target**]")
                    if st.session_state.number_input:
                        dh_show = st.number_input("**Drawdown $$\Delta h$$** in the pumping well", 0.01, 10.0, 5.0, 0.1, key="dh_show_input", on_change=update_dh_show)
                    else:
                        dh_show = st.slider      ("**Drawdown $$\Delta h$$** in the pumping well", 0.01, 10.0, 5.0, 0.1, key="dh_show_input", on_change=update_dh_show)
                else:
                    st.markdown(":blue[**Q-target**]")
                    if st.session_state.number_input:
                        Q_show = st.number_input("**Pumping rate $Q$** in the well", 0.001, 1.0, 0.5, 0.001, key="Q_show_input", on_change=update_Q_show)
                    else:
                        Q_show = st.slider      ("**Pumping rate $Q$** in the well", 0.001, 1.0, 0.5, 0.001, key="Q_show_input", on_change=update_Q_show)   
            if show_plot3:
                h_cell_slider = st.slider("**Cell head** $h_{aq}$ [m]", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
                h_thr = st.slider("**Threshold head** $h_{thr}$ [m]", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
                th = st.toggle("Apply pumping thresholds")
                if th:
                    Q_range = st.slider("Discharge cutoff range $[Q_{mn}, Q_{mx}]$ [m³/s]", 0.0, 1.0, (0.1, 0.15), 0.01)
                    Q_mn, Q_mx = Q_range                
    
    with columns1[2]:
        modify_CWC = st.toggle('Toggle to **modify CWC parameters**')
    
    # Parameter control below the general pattern
    if modify_CWC:
        # Activate second dataset
        if show_plot1 or show_plot3:
            st.session_state.second = st.toggle("Toggle to define a second parameter set for comparison")
        
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
        
        if st.session_state.second:
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
    
    # Input for visualization
    if visualize:
        if h_target:
            delta_head = dh_show
            Q_guess = delta_head / (st.session_state.A + st.session_state.B)  # initial guess
            Q_show, = fsolve(discharge_equation, Q_guess, args=(delta_head, st.session_state.A, st.session_state.B, st.session_state.C, st.session_state.P))
            if st.session_state.second:
                delta_head2 = delta_head
                Q_guess2 = delta_head2 / (st.session_state.A2 + st.session_state.B2)  # initial guess
                Q_show2, = fsolve(discharge_equation, Q_guess2, args=(delta_head2, st.session_state.A2, st.session_state.B2, st.session_state.C2, st.session_state.P2))
        else:
            delta_head = Q_show * (st.session_state.A + st.session_state.B + st.session_state.C * Q_show**(st.session_state.P - 1))
            if st.session_state.second:
                Q_show2 = Q_show
                delta_head2 = Q_show2 * (st.session_state.A2 + st.session_state.B2 + st.session_state.C2 * Q_show2**(st.session_state.P2 - 1))
        
        # Define the values for the visual help lines
        if st.session_state.second:
            Q_line = max(Q_show, Q_show2)
            h_line = min(delta_head, delta_head2)
        else:
            Q_line = Q_show
            h_line = delta_head
                
    #Define aquifer head range / Range of head differences Δh
    delta_h_range = np.linspace(0.01, 10, 200)
    Q_values = []
    if st.session_state.second:
        delta_h_range2 = np.linspace(0.01, 10, 200)
        Q_values2 = []
    
    # Solve for Q_n for each Δh
    for delta_h in delta_h_range:
        Q_initial_guess = delta_h / (st.session_state.A + st.session_state.B)  # reasonable initial guess
        Q_solution, = fsolve(discharge_equation, Q_initial_guess, args=(delta_h, st.session_state.A, st.session_state.B, st.session_state.C, st.session_state.P))
        Q_values.append(Q_solution)
    
    if st.session_state.second:
        for delta_h2 in delta_h_range2:
            Q_initial_guess2 = delta_h2 / (st.session_state.A2 + st.session_state.B2)  # reasonable initial guess
            Q_solution2, = fsolve(discharge_equation, Q_initial_guess2, args=(delta_h2, st.session_state.A2, st.session_state.B2, st.session_state.C2, st.session_state.P2))
            Q_values2.append(Q_solution2)   
       
       
       
    # FIRST PLOT HERE
    #with st.expander("Show / Hide the Discharge-Drawdown relationship for the MNW boundary", expanded = True):
    if show_plot1:
        st.subheader('🔵 Plot 1', divider = 'blue')
        st.markdown("""
        :blue[**Plot 1**: Pumping and drawdown in the well.] The figure shows the relationship between **pumping rate _Q_**, and the resulting **drawdown** between the (aquifer) head in the cell and the head in the well. Up to **two parameter sets of the CWC** can be considered. (_Note: For a real model, the aquifer head in the cell depends on model parameters and boundary stresses (such as pumping), and it may vary across different states or time steps. Here, it is assumed to be given._)
        """)
            
        label_head_axis = "Head difference $\Delta h = h_{Well} - h_{aq}$ (m)"
        label_flow_axis = "Pumping rate $Q$ (m³/s)"
        if visualize:
            # PLOT HERE - Create side-by-side plots
            fig, (ax_schematic, ax_plot) = plt.subplots(1, 2, figsize=(8, 5), width_ratios=[1, 3])
            fig.subplots_adjust(wspace=0.5)  # Increase horizontal space between ax_schematic and ax_plot
            
            # --- LEFT AXIS: Schematic view (Aquifer head vs Well head) ---
            schematic_width = 1.0
            # Aquifer: full height blue rectangle
            ax_schematic.add_patch(plt.Rectangle((0.0, 0), schematic_width*0.5, aquifer_thickness, color='skyblue'))
            ax_schematic.add_patch(plt.Rectangle((0.6, 0), schematic_width*0.5, aquifer_thickness, color='skyblue'))
            # Well water level: narrower grey rectangle, Head level indicators (dashed lines) and Labels wellls
            if st.session_state.second and not h_target:
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
                ax_plot.plot(Q_values, delta_h_range, label="$Q$-$\Delta h$ relation 1", color='darkblue', linewidth=4)
                if st.session_state.second:
                    ax_plot.plot(Q_values2, delta_h_range2, label="$Q$-$\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
                if h_target:
                    ax_plot.plot(Q_show, delta_head, 'ro',markersize=10, label="h_target")
                    ax_plot.plot([0, Q_line], [delta_head, delta_head], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(Q_show2, delta_head2, 'ro',markersize=10)
                else:
                    ax_plot.plot(Q_show, delta_head, 'bo',markersize=10, label="Q_target")
                    ax_plot.plot([Q_show, Q_show], [aquifer_thickness, h_line], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(Q_show2, delta_head2, 'bo',markersize=10)            
                ax_plot.set_ylabel(label_head_axis, fontsize=12, labelpad=15)
                ax_plot.set_xlabel(label_flow_axis, fontsize=12, labelpad=15)
                ax_plot.set_ylim(10, 0)
                ax_plot.set_xlim(0, 1)
            else:
                ax_plot.plot(delta_h_range, Q_values, label="$Q$-$\Delta h$ relation 1", color='darkblue', linewidth=4)
                if st.session_state.second:
                    ax_plot.plot(delta_h_range2, Q_values2, label="$Q$-$\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
                if h_target:
                    ax_plot.plot(delta_head,Q_show, 'ro',markersize=10, label="h_target")
                    ax_plot.plot([delta_head, delta_head], [0, Q_line], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(delta_head2, Q_show2, 'ro',markersize=10)
                else:
                    ax_plot.plot(delta_head, Q_show,'bo',markersize=10, label="Q_target")
                    ax_plot.plot([aquifer_thickness, h_line], [Q_show, Q_show], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(delta_head2, Q_show2, 'bo',markersize=10)  
                ax_plot.set_xlabel(label_head_axis, fontsize=12, labelpad=15)
                ax_plot.set_ylabel(label_flow_axis, fontsize=12, labelpad=15)
                ax_plot.set_xlim(0, 10)
                ax_plot.set_ylim(0, 1)
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
                if st.session_state.second:
                    ax_plot.plot(Q_values2, delta_h_range2, label="$Q-\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)           
                ax_plot.set_ylabel(label_head_axis, fontsize=12, labelpad=15)
                ax_plot.set_xlabel(label_flow_axis, fontsize=12, labelpad=15)
                ax_plot.set_ylim(10, 0)
                ax_plot.set_xlim(0, 1)
            else:
                ax_plot.plot(delta_h_range, Q_values, label="$Q-\Delta h$ relation 1", color='black', linewidth=4)
                if st.session_state.second:
                    ax_plot.plot(delta_h_range2, Q_values2, label="$Q-\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
                ax_plot.set_xlabel(label_head_axis, fontsize=12, labelpad=15)
                ax_plot.set_ylabel(label_flow_axis, fontsize=12, labelpad=15)
                ax_plot.set_xlim(0, 10)
                ax_plot.set_ylim(0, 1)
            
        ax_plot.set_title("Hydraulic Heads in the MNW Boundary", fontsize=14, pad=20)
        ax_plot.tick_params(axis='both', labelsize=12)
        ax_plot.legend(fontsize=12)    
        
        # Show in Streamlit
        columns_fig1=st.columns((1,8,1))
        with columns_fig1[1]:
                st.pyplot(fig, bbox_inches='tight') 
        
        if visualize:
            st.write('**Drawdown and flow in the well:**')
            if h_target:
                st.write(':grey[**Drawdown in the well**] (in m) = %5.2f' %delta_head)
                st.write(':blue[**Discharge $Q$ to the well**] (in m³/s) = %5.3f' %Q_show)
                if st.session_state.second:
                    st.write(':red[**Discharge $Q2$ to the well**] (in m³/s) = %5.3f' %Q_show2)
            else:
                st.write(':grey[**Discharge to the well**] (in m³/s) = %5.3f' %Q_show)
                st.write(':blue[**Drawdown $$\Delta h$$ in the well**] (in m) = %5.2f' %delta_head)
                if st.session_state.second:
                    st.write(':red[**Drawdown $$\Delta h2$$ in the well**] (in m) = %5.2f' %delta_head2)    
    
        # --- PLOT 1 EXPLANATION ---  
        with st.expander('Click here to read more :blue[**About this Plot**]'):
            st.markdown("""
            #### :blue[🔎 About this Plot]
            
            This plot illustrates the relationship between discharge and drawdown between the aquifer cell head ($h_{aq}$) and the well head ($h_{well}$), using the Multi-Node Well (MNW) abstraction package.
            
            It allows users to explore two operating modes:
            1. :blue[**Q-target**] (defined discharge): Calculates the resulting drawdown for a given pumping rate.
            2. :red[**H-target**] (defined drawdown): Calculates the discharge required to maintain a specified drawdown (e.g., to avoid reaching a critical well head).
            
            The interactive plot is split in two:
            - On the **right**, the Q–Δh curve shows how head losses evolve with pumping.
            - On the **left**, a schematic illustrates the difference between $h_{aq}$ and $h_{well}$ (drawdown) in relationship to the pumping rate $Q$.
            
            Users can modify the **cell-to-well conductance (CWC)**, defined via the parameters $A$, $B$, $C$, and the exponent $P$, and compare two configurations to better understand how well losses (linear and nonlinear) influence the characteristics.
            
            """)
        with st.expander('Click here for :blue[**Instructions To Get Started with this Plot**]'):
            st.markdown("""
            #### :blue[🧭 Getting Started]
            
            Use these initial steps to familiarize yourself with the model:
            
            1. **Define a Reference Case**
               * Set the CWC parameters to:
                 * $A = 0.5$, $B = 0.05$, $C = 1.0$, $P = 2.0$
               * Select :blue[**Q-target] mode** and set $Q = 0.02$ m³/s
               * Observe the drawdown between $h_{aq}$ and $h_{well}$
               * Modify the pumping rate and the parameters to investigate the response in the interactive plot.
            
            2. **Switch to H-target**
               * Toggle to :red[**H-target**] mode
               * Vary drawdown Δh from **0.5 to 5.0 m**
               * Observe how $Q$ responds to increasing drawdown
            
            3. **Compare Parameter Sets**
               * Toggle for a **Second parameter set** in the CWC menu and try a restrictive case:
                 * e.g., $A = 1.0$, $B = 0.2$, $C = 2.0$, $P = 2.5$
               * Compare the resulting Q–Δh responses
            
            _Use the plot orientation toggle for alternate layouts and enable/disable the schematic as needed._
            """)
        with st.expander('Click here for an :blue[**Exercise About this Plot**]'):
            st.markdown("""
            🎯 **Learning Objectives**
            
            By completing this exercise, you will:
            
            - Understand how the discharge–drawdown relationship is defined for MNW boundaries
            - Explain the influence of CWC parameters ($A$, $B$, $C$, $P$)
            - Differentiate between Q-target and H-target abstraction modes
            - Compare well behavior under different parameter configurations
            
            🛠️ **Your Tasks**
            
            1. **Explore Q–Δh Relationship**
               * Set: $A = 0.5$, $B = 0.05$, $C = 1.0$, $P = 2.0$
               * Use :blue[**Q-target**] mode
               * Vary $Q$ from 0.01 to 0.5 m³/s
               * 📝 Record where the curve steepens and explain the influence of the different parameters in CWC ($A$, $B$, $C$, and $P$)
            
            2. **Test Parameter Sensitivity**
               * Keep $Q = 0.3$ m³/s in :blue[**Q-target**] mode
               * Enable the **second parameter set** 
               * Vary $A$, then systematically change $B$, $C$, and $P$ and compare responses
               * **Deal with the following tasks**
                   * 💭 Reflect on the role of linear vs. nonlinear resistance.
                   * 💭 Switch on/off the nonlinear resistance with suitable parameter settings.
                   * What parameter set represents well-aging?
            
            3. **Reverse Analysis with H-target**
               * Switch to :red[**H-target**]
               * Set Δh = 2.0, 4.0, 6.0 m
               * Compare resulting $Q$ values across different parameter sets (e.g., to reflect an aged well).
               * 📝 Answer: When does $Q > 0.4$ m³/s? How much does well-aging affect the efficiency?
            
            _Use this exploration to build deeper insight into how MNW wells behave under variable design conditions._
            """)
        
        with st.expander('Click here for an :rainbow[**Assessment About this Plot**]- to self-check your understanding'):
            st.markdown("""
            #### 🧠 Final assessment for Plot 1
            These questions test your conceptual understanding after working with the app.
            """)
        
            # Render questions in a 2x3 grid (row-wise)
            for row in [(0, 1), (2, 3), (4, 5)]:
                col1, col2 = st.columns(2)
        
                with col1:
                    i = row[0]
                    st.markdown(f"**Q{i+1}. {quest_plot1[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot1[i]["options"],
                        success=quest_plot1[i].get("success", "✅ Correct."),
                        error=quest_plot1[i].get("error", "❌ Not quite.")
                    )
        
                with col2:
                    i = row[1]
                    st.markdown(f"**Q{i+1}. {quest_plot1[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot1[i]["options"],
                        success=quest_plot1[i].get("success", "✅ Correct."),
                        error=quest_plot1[i].get("error", "❌ Not quite.")
                    )
    
    
    # SECOND PLOT HERE
    #with st.expander("Show / Hide the **Q-h plot** for the MNW boundary"):
    if show_plot2:
        st.subheader('🟢 Plot 2', divider = 'green')
        st.markdown("""
        :green[**Plot 2**: Relationship between discharge in the boundary (_Q_), heads (_h_), and drawdown as function of CWC]. The plot shows the **_Q-h_-relationship** for the cell with an abstraction well. Additionally, the relationship between discharge and hydraulic head in a well relative to the head in the cell (drawdown) is presented as function of the CWC.
        """)
 
        if visualize:   
            # --- CONSTANT DISCHARGE PLOT ---
            h_2nd = np.linspace(0, 20, 20)
            Q_2nd = np.ones_like(h_2nd) * Q_show * -1
            h_cell = 10
            h_well = h_cell - delta_head
            # Change sign to account for the MODFLOW convention of negative sign for discharge
            Q_values_2nd = [-1 * q for q in Q_values]
            
            # Interpolate Q at h_thr using the Q(h_well) relation
            Q_interp = interp1d(h_cell - delta_h_range, Q_values, kind='linear', fill_value="extrapolate")
            h_well_range = h_cell - delta_h_range  # h_cell is fixed (currently set to 10)
            
            # --- Plot Q vs. h_well ---
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            if turn:
                ax2.plot(Q_2nd, h_2nd, color='black', label=fr"$Q$-$h_{{aq}}$ plot with $Q = {Q_show:.2f}$", linewidth=4)
                ax2.plot(Q_values_2nd, h_well_range, linestyle='--', color='lightgrey', linewidth=3, label=r"$Q$-$h_{Well}$")
                ax2.axhline(y=h_cell, linestyle='dotted', color='black', linewidth=2)
                ax2.set_ylabel("Hydraulic head $h_n$ [L]", fontsize=14)
                ax2.set_xlabel("Flow Into the Ground-Water System \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14)
                ax2.set_xlim(-1, 1)
                ax2.set_ylim(0, 20)
                if visualize:
                    ax2.plot(Q_show*-1, h_cell,'o', color='skyblue', markersize=10, label='head in cell')
                    ax2.plot(Q_show*-1, h_well,'o', color='blue',markersize=10, label='head in well')    
            else:
                ax2.plot(h_2nd, Q_2nd, color='black', label=fr"$Q$-$h_{{aq}}$ plot with $Q = {Q_show:.2f}$", linewidth=4)
                ax2.plot(h_well_range, Q_values_2nd, linestyle='--', color='lightgrey', linewidth=3, label=r"$Q$-$h_{Well}$")
                ax2.axvline(x=h_cell, linestyle='dotted', color='black', linewidth=2)
                ax2.set_xlabel("Hydraulic head $h_n$ [L]", fontsize=14)
                ax2.set_ylabel("Flow Into the Ground-Water System \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14)
                ax2.set_ylim(-1, 1)
                ax2.set_xlim(0, 20)
                if visualize:
                    ax2.plot(h_cell, Q_show*-1, 'o',color='skyblue', markersize=10, label='head in cell')
                    ax2.plot(h_well, Q_show*-1, 'o',color='blue', markersize=10, label='head in well')
            
            ax2.set_title("Q-h Behavior for the MNW Boundary", fontsize=16, pad=20)
            ax2.tick_params(axis='both', labelsize=12)        
            ax2.legend(fontsize=14, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
            
            columns_fig2=st.columns((1,8,1))
            with columns_fig2[1]:
                st.pyplot(fig2, bbox_inches='tight')    
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Make the plot alive and visualize the results]** to see this plot')
            
            
        # --- PLOT 2 EXPLANATION ---  
        with st.expander('Click here to read more :green[**About this Plot**]'):
            st.markdown("""
            #### :green[🔎 About this Plot]
            
            This plot illustrates the relationship between **well head ($h_{well}$)** and **discharge (Q)** for a **fixed aquifer cell head ($h_{aq}$)** in a Multi-Node Well (MNW) configuration. 
            
            Two modes are available:
            1. :blue[**Q-target**]: Specify the discharge and calculate the resulting $h_{well}$ (drawdown).
            2. :red[**H-target**]: Specify $h_{well}$ and compute the discharge resulting from head difference and conductance.
            
            Unlike simple well (WEL) or recharge (RCH) boundaries that impose fixed flux, and unlike RIV or DRN boundaries that assume **linear head-dependent flow**, MNW simulates **nonlinear resistance** due to turbulence or well construction effects. This is controlled by the **cell-to-well conductance (CWC)**, defined by parameters $A$, $B$, $C$, and $P$.
            
            The aquifer head ($h_{aq}$) remains constant (10 m) throughout the plot, allowing you to isolate and analyze how discharge and well head interact.
            """)
        with st.expander('Click here for :green[**Instructions To Get Started with this Plot**]'):
            st.markdown("""
            #### :green[🧭 Getting Started]

            Begin with the following steps to explore the MNW discharge–head relationship:
            
            1. **Set Reference Parameters**
               * Aquifer cell head: $h_{aq} = 10$ m (fixed)
               * CWC: $A = 0.5$, $B = 0.05$, $C = 1.0$, $P = 2.0$
            
            2. **Try Q-target Mode**
               * Set discharge $Q$ between 0.05 and 0.7 m³/s
               * Observe the resulting well head $h_{well}$ and the increasing drawdown
            
            3. **Switch to H-target Mode**
               * Set drawdown Δh between 1.0 and 6.5 m
               * See how discharge changes with increasing drawdown
            
            4. **Modify CWC Parameters**
               * Try different values for $A$, $B$, and $P$
               * Compare how the drawdown or flow response changes
               * Test an extreme case: set $A = 0$ & $B = 0$ and explore the purely nonlinear behavior
            
            💡 Try to relate your observations to how **DRN** and **RIV** boundaries behave (linear, head-dependent flow) or how **WEL** and **RCH** impose fixed Q.

            """)
        with st.expander('Click here for an :green[**Exercise About this Plot**]'):
            st.markdown("""
            🎯 **Learning Objectives**
            
            By completing this exercise, you will:
            
            - Understand how MNW models nonlinear resistance between cell and well
            - Interpret how discharge and drawdown interact under different parameterizations
            - Compare MNW behavior to other boundary conditions (WEL, RCH, DRN, RIV)
            - Identify cases where turbulence becomes dominant
            
            🛠️ **Your Tasks**
            
            1. **Well Head Response to Discharge**
               * Use :blue[**Q-target**] mode
               * Set: $A = 0.5$, $B = 0.05$, $C = 1.0$, $P = 2.0$
               * Vary $Q$ from 0.05 to 0.8 m³/s
               * 📝 Record $h_{well}$ and compute drawdown: $\Delta h = h_{aq} - h_{well}$
            
            2. **Effect of Parameter Variation**
               * Try:
                 * Doubling $A$
                 * Doubling $B$
                 * Doubling $C$
                 * Increasing $P$ to 2.5 or 3.0
               * Observe how each change affects drawdown for a given Q
            
            3. **Explore H-target Mode**
               * Fix drawdown Δh = 6.0 m, then lower it to 1.5 m
               * See how discharge changes
               * 📝 Which parameters cause nonlinear increases in Q?
            
            4. **Conceptual Comparison**
               * When is the MNW behavior close to:
                 - A constant Q source (WEL)?
                 - A linear head-dependent boundary (RIV)?
               * What role does the parameter $P$ play in making this boundary behave differently?
            
            🧠 Reflect: What happens if you set $A = 0$? When is turbulence (nonlinear loss) dominant?

            """)
        
        with st.expander('Click here for an :rainbow[**Assessment About this Plot**]- to self-check your understanding'):
            st.markdown("""
            #### 🧠 Final assessment for Plot 2
            These questions test your conceptual understanding after working with the app.
            """)
        
            # Render questions in a 2x3 grid (row-wise)
            for row in [(0, 1), (2, 3), (4, 5)]:
                col1, col2 = st.columns(2)
        
                with col1:
                    i = row[0]
                    st.markdown(f"**Q{i+1}. {quest_plot2[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot2[i]["options"],
                        success=quest_plot2[i].get("success", "✅ Correct."),
                        error=quest_plot2[i].get("error", "❌ Not quite.")
                    )
        
                with col2:
                    i = row[1]
                    st.markdown(f"**Q{i+1}. {quest_plot2[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot2[i]["options"],
                        success=quest_plot2[i].get("success", "✅ Correct."),
                        error=quest_plot2[i].get("error", "❌ Not quite.")
                    )

      

    # THIRD PLOT HERE - Q vs h_cell (with head and discharge thresholds)
    #with st.expander('Show the MNW boundary with varying cell heads'):  
    if show_plot3:
        st.subheader('🔴 Plot 3', divider = 'red')
        st.markdown("""
        :red[**Plot 3**: _Q-h_-Relationship for an abstraction well with thresholds.] The plot demonstrate the effect of a threshold head that limits the pumping rate _Q_.
        """)
        
        if visualize:
            # Plotting range
            h_3rd = np.linspace(0, 20, 300)

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
            if st.session_state.second:
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
           
            # --- CREATE THE 3RD PLOT ---
            fig3, ax3 = plt.subplots(figsize=(6, 5))
            if turn:
                # if threshold is considered
                if th:
                    ax3.axvline(x=Q_show, linestyle='--', color='lightgrey', linewidth=1)  
                    ax3.plot(Q_plot, h_3rd, color='black', linewidth=1, linestyle=':')
                    ax3.plot(Q_plot_mn, h_3rd, color='black', linewidth=3, label=r"$Q$-$h_{aq}$ with threshold")
                    ax3.plot(Q_plot_mx, h_3rd, color='black', linewidth=3, linestyle='--')                                      
                    ax3.plot(Q_dot_th, h_cell_slider, 'o', color = 'lightblue', markersize=10, label='$h_{aq}$')
                    if st.session_state.second:
                        ax3.plot(Q_plot2, h_3rd, color='red', linewidth=1, linestyle=':', label=r"$Q$-$h_{aq}$ with threshold CWC2")
                        ax3.plot(Q_dot_th2, h_cell_slider, 'o', color = 'lightblue',  markersize=10, label='$h_{aq}$')
                else:                
                    ax3.axvline(x=Q_show, linestyle='--', color='lightgrey', linewidth=1)
                    ax3.plot(Q_plot, h_3rd, color='black', linewidth=4, label=r"$Q$-$h_{aq}$ with threshold")               
                    ax3.plot(Q_dot, h_cell_slider, 'o', color = 'lightblue', markersize=10, label='$h_{aq}$')
                    if st.session_state.second:
                        ax3.plot(Q_plot2, h_3rd, color='red', linewidth=2, linestyle=':', label=r"$Q(h_{aq})$ with threshold")
                        ax3.plot(Q_dot2, h_cell_slider, 'o', color = 'lightblue', markersize=10, label='$h_{aq}$')
                ax3.axhline(y=h_cell_slider, linestyle='--', color='lightblue', linewidth=2)
                ax3.axhline(y=h_thr, linestyle='--', color='orange', linewidth=2)
                if h_well >= h_thr:
                    ax3.plot(Q_dot, h_well, 'o', color = 'blue', markersize=10, label='$h_{Well}$')
                else:
                    ax3.plot(Q_dot, h_thr, 'ro',markersize=10, label='$h_{Well}$ (threshold)')  
                if st.session_state.second:
                    if h_well2 >= h_thr:
                        ax3.plot(Q_dot2, h_well2, 'o', color = 'blue', markersize=10, label='$h_{Well} CWC2$')
                    else:
                        ax3.plot(Q_dot2, h_thr, 'ro',markersize=10, label='$h_{Well}$ CWC2 (threshold)')       
            
                # Add head annotations
                ax3.text(0.65, h_cell_slider+1.1, "hydraulic head \nin the cell $h_{aq}$", va='center',color='lightblue',  fontsize=14)
                ax3.text(0.65, h_thr-0.9, "threshold head $h_{thr}$",  va='center',color='red', fontsize=14)                        
                
                ax3.set_xlabel("Pumping rate $Q$ (m³/s)", fontsize=14)
                ax3.set_ylabel("Hydraulic heads $h$ (m)", fontsize=14)
                ax3.set_xlim(-0.01, 1)
                ax3.set_ylim(0, 20)
            else:
                # if threshold is considered
                if th:
                    ax3.plot(h_3rd, Q_plot, color='black', linewidth=1, linestyle=':')
                    ax3.plot(h_3rd, Q_plot_mn,  color='black', linewidth=3, label=r"$Q$-$h_{aq}$ with threshold")
                    ax3.plot(h_3rd, Q_plot_mx,  color='black', linewidth=3, linestyle='--')
                    ax3.plot(h_cell_slider, Q_dot_th, 'o', color='lightblue', markersize=10, label='$h_{aq}$')
                    if st.session_state.second:
                        ax3.plot(h_3rd, Q_plot_th, color='red', linewidth=1, linestyle=':', label=r"$Q$-$h_{aq}$ with threshold CWC2")
                        ax3.plot(h_cell_slider, Q_dot_th2, 'o', color='lightblue', markersize=10, label='$h_{aq}$ CWC2')
  
                                        
                else:
                    ax3.plot(h_3rd, Q_plot, color='black', linewidth=4, label=r"$Q$-$h_{aq}$ with threshold")
                    ax3.plot(h_cell_slider, Q_dot, 'o', color='lightblue', markersize=10, label='$h_{aq}$')
                    if st.session_state.second:
                        ax3.plot(h_3rd, Q_plot2, color='red', linewidth=2, linestyle=':', label=r"$Q(h_{aq})$ with threshold")
                        ax3.plot(h_cell_slider, Q_dot2, 'ro', markersize=10, label='$h_{aq}$ CWC2')
                ax3.axvline(x=h_cell_slider, linestyle='--', color='lightblue', linewidth=2)
                ax3.axvline(x=h_thr, linestyle='--', color='orange', linewidth=2)
                if h_well >= h_thr:
                    ax3.plot(h_well, Q_dot, 'o', color = 'blue', markersize=10, label='$h_{Well}$')
                else:
                    ax3.plot(h_thr, Q_dot, 'ro',markersize=10, label='$h_{Well}$ (threshold)')
                if st.session_state.second:
                    if h_well2 >= h_thr:
                        ax3.plot(h_well2, Q_dot2, 'o', color = 'blue', markersize=10, label='$h_{Well} CWC2$')
                    else:
                        ax3.plot(h_thr, Q_dot2, 'ro',markersize=10, label='$h_{Well}$ CWC2 (threshold)')           
                        
                # Add head annotations
                ax3.text(h_cell_slider+0.5, 0.93, "hydraulic head \nin the cell $h_{aq}$", va='center',color='lightblue',  fontsize=14)
                ax3.text(h_thr-4.5, 0.93, "threshold \nhead $h_{thr}$",  va='center',color='red', fontsize=14)     
                
                ax3.set_xlabel("Hydraulic heads $h$ [m]", fontsize=14)
                ax3.set_ylabel("Discharge $Q$ [m³/s]", fontsize=14)
                ax3.set_xlim(0, 20)
                ax3.set_ylim(-0.01, 1)
            
            ax3.set_title("Q-h Behavior for the MNW Boundary with Threshold", fontsize=16, pad=20)
            ax3.tick_params(axis='both', labelsize=12)
            ax3.legend(fontsize=14, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
            
            columns_fig3=st.columns((1,8,1))
            with columns_fig3[1]:
                st.pyplot(fig3, bbox_inches='tight') 
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Make the plot alive and visualize the results]** to see this plot')

        # --- PLOT 3 EXPLANATION ---  
        with st.expander('Click here to read more :red[**About this Plot**]'):
            st.markdown("""
            #### :red[🔎 About this Plot]
            
            This plot illustrates the **_Q–h_-relationship of a Multi-Node Well (MNW)** under conditions where a **threshold head** is imposed to protect the well from excessive drawdown. 
            
            The cell head ($h_{aq}$) and the discharge ($Q$) define the well head ($h_{well}$) through the nonlinear **cell-to-well conductance (CWC)** equation (see Theory section above).
                      
            If the computed well head falls **below the defined threshold head**, the pumping rate is automatically **reduced** such that the well head is held at the threshold. This mechanism mimics a pump protection strategy to avoid dry wells or damage due to excessive drawdown.
            
            The MNW behavior is also constrained by pumping thresholds that reflect practical limitations of typical pumps:
            - **Qmn** – the lower limit of the pump capacity
            - **Qmx** – the rate that a switched-off pump is restored to.
            
            This plot helps visualize:
            - When the **threshold becomes active**
            - How **pumping is limited** to protect the well
            - The nonlinear relationship between Q and $h_{well}$ under pumping-limited conditions for various CWC parameters

            """)
        with st.expander('Click here for :red[**Instructions To Get Started with this Plot**]'):
            st.markdown("""
            #### :red[🧭 Getting Started]
            
            Follow these steps to explore threshold-controlled pumping behavior in MNW:
            
            1. **Set Initial Conditions**
               * $h_{aq} = 10$ m
               * Threshold head $h_{thr} = 6.0$ m
               * CWC parameters: $A = 0.5$, $B = 0.05$, $C = 0$, $P = 2.0$
            
            2. **Run Q Sweep**
               * Vary pumping rate $Q$ from 0.05 to 0.7 m³/s
               * Observe how $h_{well}$ responds to pumping
               * Identify where the head in the cell $h_{aq}$ reaches the threshold $h_{thr}$
            
            3. **Explore Threshold Activation**
               * Increase the pumping rate _Q_ beyond the point where $h_{well} = h_{thr}$
               * Note that the active _Q_ (represented by the dot in the plot) is automatically reduced to keep $h_{well} = h_{min}$
            
            4. **Explore Pumping Thresholds**
               * Make sure the threshold head $h_{thr}$ is set to 5.0 m and the cell head $h_{aq}$ is set to 15.0 m. Set the pumping rate to 0.5 m³/s. With this settings, the system is in proper operation.
               * Toggle **Apply pumping thresholds** to automatically switch off/on the pump
               * set Qmn and Qmx to 0.05 and 0.2 m³/s
               * Now, lower the cell head $h_{aq}$ smoothly down to 5.1 m. Lowering the cell head can be caused by various reasons, e.g., neighboring abstraction wells. (_hint: if you access this app through a computer, you can gradually reduce Q with the arrow-keys of your keyboard_)
               * While lowering the cell head, observe how the 'real' pumping rate - represented by the dot in the plot - is affected.
               * Once the cell head reached 5.1 m, rise the head again back to 15.0 m and observe the real pumping rate (dot in the plot).
            
            5. **Modify Parameters**
               * Try different values for $A$, $B$, $C$, and $P$
               * Vary Q (Q-target), Δh (H-target), cell head $h_{aq}$ and threshold head $h_{thr}$, and investigate the MNW behavior with the interactive plot.
            
            💡 This setup helps understand how operational constraints (like dry well prevention) interact with physical head-loss mechanisms in a realistic MNW implementation.
            """)
        with st.expander('Click here for an :red[**Exercise About this Plot**]'):
            st.markdown("""
            🎯 **Learning Objectives**
            
            After completing this exercise, you will be able to:
            
            - Explain how threshold head limits influence MNW discharge behavior
            - Identify at what conditions pumping is reduced due to well protection
            - Analyze how nonlinear head losses and operational limits combine to define feasible abstraction rates
            - Understand the role of Qmn and Qmx in the MNW implementation
            
            🛠️ **Exercise Instructions**
            
            1. **Locate Threshold Activation Point**
               * Set: $A = 0.5$, $B = 0.05$, $C = 1.0$ $P = 3.0$, $h_{aq} = 15$ m, $h_{thr} = 5$ m
               * Increase Q from 0.01 to 0.8 m³/s
               * 📝 Identify the Q at which $h_{well} = h_{thr}$ — call this $Q_{lim}$
            
            2. **Test Effect of Exponent P**
               * Increase $P$ to 4.0 and repeat the test
               * Decrease $P$ to 1.0 and repeat the test
               * How does $Q_{lim}$ change?
               * Is the threshold reached earlier or later?
            
            3. **Apply Qmn and Qmx Limits**
               * Set Qmn = 0.05 m³/s and Qmx = = 0.2 m³/s
               * Try to exceed this value by lowering the cell head to the threshold head h_{thr}$. Note the cell head when pumping stopped. (_hint: if you access this app through a computer, you can gradually reduce Q with the arrow-keys of your keyboard_)
               * Now, increase the cell head again to 15.0 m.  Note the cell head when pumping started again.
               * Double the parameter for linear well loss $B$ and repeat the procedure. Quantify the changes in terms of cell heads for switching off/on the pumping.
            
            💭 Reflect:
            - When is the threshold head the limiting factor?
            - How to Qmn/Qmx affect practical pumping?
            - How is this behavior affected by the CWC respectively the individual processes that result in CWC (aquifer loss, linear and nonlinear well loss).
            
            This exploration prepares you to interpret MNW behavior in model calibration and design tasks.
            """)
        
        with st.expander('Click here for an :rainbow[**Assessment About this Plot**]- to self-check your understanding'):
            st.markdown("""
            #### 🧠 Final assessment for Plot 3
            These questions test your conceptual understanding after working with the app.
            """)
        
            # Render questions in a 2x3 grid (row-wise)
            for row in [(0, 1), (2, 3), (4, 5)]:
                col1, col2 = st.columns(2)
        
                with col1:
                    i = row[0]
                    st.markdown(f"**Q{i+1}. {quest_plot3[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot3[i]["options"],
                        success=quest_plot3[i].get("success", "✅ Correct."),
                        error=quest_plot3[i].get("error", "❌ Not quite.")
                    )
        
                with col2:
                    i = row[1]
                    st.markdown(f"**Q{i+1}. {quest_plot3[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot3[i]["options"],
                        success=quest_plot3[i].get("success", "✅ Correct."),
                        error=quest_plot3[i].get("error", "❌ Not quite.")
                    )

Q_h_plot()

st.subheader('✅ Conclusion', divider = 'rainbow')
st.markdown("""
The Multi-Node Well (MNW) boundary in MODFLOW adds realism to well simulations by distributing flow across multiple model cells and introducing operational and physical constraints. This boundary goes beyond fixed pumping rates by simulating **head-dependent flow**, **skin effects**, and **pumping limits** — key factors in representing real-world wells.

Through Q–h plots, you explored how MNW behavior transitions between active pumping, flow cutoffs, and constraint-induced flattening. Understanding these flow regimes supports better interpretation, calibration, and reliability in groundwater modeling projects.

You're now ready to assess your understanding in the final quiz.
""")


with st.expander('**Show the final assessment** - to self-check your understanding'):
    st.markdown("""
    #### 🧠 Final assessment
    These questions test your conceptual understanding after working with the app.
    """)

    # Render questions in a 2x3 grid (row-wise)
    for row in [(0, 1), (2, 3), (4, 5)]:
        col1, col2 = st.columns(2)

        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )

        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )
            
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
