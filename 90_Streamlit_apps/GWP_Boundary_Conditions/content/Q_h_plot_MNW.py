import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
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
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_mnw.json"
path_quest_plot1 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p1.json"
path_quest_plot2 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p2.json"
path_quest_plot3 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p3.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_mnw.json"

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
st.subheader("Groundwater - :rainbow[Well] interaction", divider="rainbow")

st.markdown("""
#### 💡 Motivation: Why use Multi-Node Wells (MNW)?
""")

# Initial plot
# Slider input and plot
columns0 = st.columns((1,1), gap = 'large')
with columns0[0]:
    st.markdown("""  
    Let’s reflect on these questions:
    
    1. **How does head loss in a withdrawal well affect water level within the well and the achievable flow rate?**
    
    2. **What happens if the water level in the well drops below the pump intake? Should a model continue to simulate withdrawal of groundwater?**
    
    ▶️ The :rainbow[**Multi-Node Well (MNW)**] package in MODFLOW supports more realistic simulation of well hydraulics, even in single-layer groundwater systems. MNW allows you to:
    - account for **additional drawdown within the wellbore** ($h_{aq}-h_{well}$) **due to head losses**,
    - define **limiting water levels** below which withdrawal from the well stops, and
    - simulate wells that **automatically shut off** or restart depending on drawdown conditions.
    
    This section **explores only the $Q$-$h$ relationship for an MWN well in one model cell for a withdrawal well**. It does not explore wells connected to multiple aquifer cells. The interactive plots allow **exploration of how withdrawal rate, aquifer head, well-threshold head, and connectivity between the aquifer and well (:rainbow[_CWC_]) interact to determine drawdown within the well and well discharge into or out of the aquifer**. :rainbow[_CWC_] is an abbrevation for cell-to-well conductance, which we call aquifer-to-well conductance in this module.
    
    In contrast, the **WEL boundary in MODFLOW** is a Neumann-type boundary condition with defined flow. For this initial plot, the :blue[**WEL toggle**] allows you to view the equivalent $Q$-$h$ plot for a WEL boundary where $Q$ is defined by the modeler and is independent of head $h$ in the well and aquifer.
    """)

with columns0[1]:
    # CWC
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
    col_ini = st.columns((3,1.2))
    with col_ini[0]:      
        labels, default_label = prep_log_slider(default_val = 3e-3, log_min = -4, log_max = -1)
        selected_Ci = st.select_slider("**Conductance :grey[$CWC$]** in m²/s", labels, default_label, key = "MNW_CWCi")
        st.session_state.CWCi = float(selected_Ci)
        
    with col_ini[1]:
        WEL_equi = st.toggle(':blue[**WEL**]')
        
    # COMPUTATION
    # Define aquifer head range
    h_aqi = np.linspace(0, 20, 200)
    QPi = np.full_like(h_aqi, -0.01)
    h_ni = 10.0 # Example head for the cell
    h_WELLi = np.linspace(0, 20, 200)
    Qi = (h_WELLi - h_ni) * st.session_state.CWCi
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, QPi, color='blue', linewidth=3, label='$Q$-$h_{aq}$')
    # Draw vertical line at QPi and h = 10
    ax.plot([10, 10], [-0.01, -0.05], color='blue',linestyle=':', linewidth=3, label='$h_{aq}$ = 10 m')
    if WEL_equi:
        ax.set_xlabel("Head in the WEL-aquifer system (m)", fontsize=14, labelpad=15)
        ax.set_ylabel("Flow into the groundwater \nfrom the WEL boundary $Q_{WEL}$ (m³/s)", fontsize=14, labelpad=15)
        ax.set_title("Flow Between Groundwater and WEL", fontsize=16, pad=10)
    else:
        ax.plot(h_WELLi, Qi, color='black', linewidth=3, label='$Q$-$h_{well}$')
        # Determine the y-values for h = 10
        Qi_10 = (10.0 - h_ni) * st.session_state.CWCi
        QPi_10 = -0.01     
    
        # Draw vertical line at Qi and h_intersect
        h_is = h_ni + (-0.01 / st.session_state.CWCi)
    
        ax.set_xlabel("Head in the MNW-aquifer system (m)", fontsize=14, labelpad=15)
        ax.set_ylabel("Flow into the groundwater \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14, labelpad=15)
        ax.set_title("Flow Between Groundwater and MNW", fontsize=16, pad=10)
        ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
       
        # Red note/rectangle if well is dry       
        if h_is < 0:
            ax.plot([h_is, h_is], [QPi_10, -0.05], color='red',linestyle=':', linewidth=3, label=f'$h_{{well}}$ = dry')
            ax.text(1,-0.045, "Well is dry", fontsize=16, va='center', color='red')
            rect = Rectangle((0.0, -0.05), 20, 0.1, linewidth=5, edgecolor='red', facecolor='none')
            ax.add_patch(rect) 
        else:
            ax.plot([h_is, h_is], [QPi_10, -0.05], color='black',linestyle=':', linewidth=3, label=f'$h_{{well}}$ = {h_is:5.2f}')
    ax.axvline(10, color='grey', linestyle='--', linewidth=0.8)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc="upper left", fontsize=14)
    st.pyplot(fig)
    
    st.markdown("""
    **Initial Plot** for exploring how the value of :rainbow[**MNW aquifer-to-well conductance CWC**] controls the relationship between **head in the well $h_{well}$** and :blue[**flow rate $Q$**], for a constant :blue[**aquifer head $h_{aq}$ of $10$ m**] as shown by the **solid black line**. 
    
    When **$h_{well}$** is above **:blue[$h_{aq}$]** then **$Q$** is positive and **water flows into** the well. When **$h_{well}$** is below **:blue[$h_{aq}$]** then **$Q$ is negative** and water flows **out of** the well. The slope of the line is defined by **:rainbow[aquifer-to-well conductance _CWC_]**. Later in this section (using Plot 3), we show how **threshold values are specified to limit the active range of the $Q$-$h$ function** in a specific well.
              
    The dotted lines indicate head in the :blue[ aquifer (blue)] and the **well (black)**, respectively. For this plot, :blue[**$h_{aq}$ is constant at 10 m (blue dotted line)**] and if $h_{well}$ < 0 m, the well is :red[**dry**]. The **intersection of the solid black and blue lines** indicates the head in the well for the specified flow rate **:blue[$Q$]** given the **:rainbow[aquifer-to-well conductance _CWC_]**.
    
    This **initial plot** is designed to bridge the gap between traditional Q-h plots on paper and the :rainbow[**interactive plots**] provided further down in the app. These allow you to explore the _Q_-_h_ relationships more intuitively, supported by interactive controls and guided instructions.
    """)

st.markdown("""
####  💻 How the head-dependent flow feature of MNW may be Applied in Field-Scale Groundwater Modeling

The MNW boundary represents a withdrawal well with a specified desired discharge rate, accounts for well losses based on connectivity of the well and aquifer to calculate head within the well, and, if needed, reduces the well discharge. In contrast, the WEL boundary applies the specified desired discharge without adjustment if the well is stressed to the point that it cannot supply the desired discharge. MNW also accomodates modeling of wells that extend through multiple model cells and calculates flow to/from each layer, however this module only addresses the head-dependent flow feature of MNW.""")
left_co, cent_co, last_co = st.columns((10,40,10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/MNWsketch2.png', caption="Illustration of the head losses that can lead to discharge reduction using MNW in MODFLOW. (modified from Shapiro, A.. D. Oki, and E. Greene (1998). Estimating Formation Properties from Early-Time Recovery in Wells Subject to Turbulent Head Losses. Journal of Hydrology. 208. p. 223-236. https://doi.org/10.1016/S0022-1694(98)00170-X.)")

with st.expander("Show me more about **the :rainbow[application of MNW in Field-Scale Groundwater Modeling]**"):
    st.markdown("""
    For MNW wells, parameter values can be specified that limit injection or discharge depending on the head in the well. MNW can account for head losses within the well, both linear (due to flow through the aquifer and the well skin) and nonlinear (due to turbulence of flow converging on the well, moving through the well wall, and flowing through the tangle of pipes and wires within the wellbore). If connectivity between the well and aquifer is high, drawdown in the well is what would be expected in order to drive flow through the aquifer to the well. 
    
    As the connectivity decreases in an aging well (i.e., lower conductance due to wellbore wall damage and aging components within the well) the head in the well will reflect additional drawdown as required to drive the water through the well skin and along the wellbore.
    
    As the water level in the well declines, the pump's ability to discharge water may be affected because the lower head above the pump in the well decreases the pump efficiency, or the water level drops to the level of the pump intake. Accordingly, the flow rate is reduced below the specified flow rate and ultimately may become zero because the water level is below the pump intake or  minimum allowed elevation. The MNW package makes the appropriate adjustments to the flow rate and keeps track of the flow rate reductions through out the model for all the MNW wells.
    
    As aquifer heads decline in response to other stresses with in the model, the MNW thresholds are met at lower flow rates, resulting in more reduction of flow to wells than in healthier aquifers.
    """)

#TODO
st.markdown("""
####  🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following:
- Understand the conceptual and practical differences between Multi-Node Wells (MNW) and traditional Well (WEL) boundaries in MODFLOW.
- Evaluate the influence of well efficiency, skin effects, and conductance on MNW flow behavior.
- Interpret Q–h relationships for MNWs and how they reflect physical and operational limits of well systems.
- Describe how head-dependent flow and constraints such as pump limitations and cell drawdowns are represented in the MNW package.
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
This app calculates the flow between a Multi-Node-Well (MNW) and the aquifer depending on the system parameters describing the flow near, into, and within the well.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    In general, from the groundwater system into a well is described with a aquifer-to-well conductance:
    """)
    st.latex(r'''Q = CWC (h_{well} - h_{aq})''')
    
    st.markdown("""
    where:
    - $Q$ is the flow between the aquifer and well, taken as negative if it is directed out of the aquifer [L³/T]
    - $h_{well}$ is the head in the well (L),
    - $CWC$ is the aquifer-to-well conductance [L²/T], and
    - $h_{aq}$ is the aquifer head [L]. _This head depends on the values of parameters and stresses (e.g., pumping, recharge) throughout the model. It can vary with time and reach a different steady state depending on all the model inputs._
    
    The CWC is composed of three terms, describing (1) flow to the well, (2) the skin effect that influences ease of flow through the well wall, and (3) the effect of turbulence within and in the vicinity of the well. Accordingly, the aquifer-to-well conductance $CWC$ is defined as:
    """)
    
    st.latex(r'''CWC = [ A + B + C Q^{(P-1)}]^{-1}''')
    
    st.markdown("""
    where:
    - $A$ = Linear aquifer-loss coefficient that represents head loss due to flow through the aquifer to the well. In a numerical model the head in the aquifer is the average head in the model cell that contains the well so the well head is lower than the aquifer cell head even when there is no additional resistance at the well wall or in the well. Loss due to A is calculated using the Thiem equation with T as the inverse of A and the radius of influence being the an effective radius based on the size of the model cell. [T/L²].
    - $B$ = Linear well-loss coefficient that accounts for head loss from _skin effects_ associated with resistance due to **laminar** components of flow adjacent to the well, through the screen, and within the wellbore [T/L²].
    - $C$ = Nonlinear well-loss coefficient that accounts for head loss from _skin effects_ associated with resistance due to **turbulent** components of flow adjacent to the well, through the screen, and within the wellbore, with units of:
    """)
    st.latex(r'''T^{P}/L^{3P-1}''')
    st.markdown("""
    - $P$ = is the power (exponent) of the nonlinear discharge component of well loss.
    """)

st.subheader('Interactive plots to understand the general characteristics of the discharge-head relationships in MNW package', divider='rainbow')

st.markdown("""
Three interactive plots are provided to allow you to investigate different aspects of the Multi-Node-Well (MNW) boundary in MODFLOW.

:blue[**PLOT 1 - Hydraulic heads in the MNW boundary**]:
Illustrates the additional drawdown in the well due to the lower aquifer-to-well conductance CWC. Two parameter sets for the CWC can be used.

:green[**PLOT 2 - Q-h behavior of the MNW boundary**]: An interactive plot of the Q-h relationship for the specified aquifer discharge ($Q$-$h_{aq}$) and the well discharge ($Q$-$h_{well}$) which may be reduced depending on physical conditions.

:red[**PLOT 3 - Q-h behavior for the aquifer head with thresholds**]: Illustrates the effect of thresholds on the simulated withdrawal rate.

_For all plots, the application includes toggles to:_
- turn the plots by 90 degrees,
- switch between number input or sliders.
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
def update_h_cell_slider():
    st.session_state.h_cell_slider = st.session_state.h_cell_slider_input
def update_h_thr():
    st.session_state.h_thr = st.session_state.h_thr_input
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
st.session_state.Q_show = 0.5
st.session_state.h_cell_slider = 12.0
st.session_state.h_thr = 5.0
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
        plot_choice = st.selectbox( "**SELECT a plot to display:**", ["🔵 Plot 1", "🟢 Plot 2", "🔴 Plot 3"], index=0)
        
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
    
    # INPUT SECTION
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    st.markdown("""
       #### :rainbow[INPUT CONTROLS]
        """)
    # Switches
    columns1 = st.columns((1,1,1), gap = 'small')              
    
    with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="MNW_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number input.")
            visualize = st.toggle(':rainbow[**Make the plot live**] and visualize the input values', key="MNW_vis", value=True)
    
    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Discharge**]'):
        # The additional controls only for visualization
            if visualize:
                st.write('**:green[Target for evaluation/visualization]**')
                h_target = st.toggle('Toggle for :blue[**Q-**] or :red[**H-**]target')
    
                if h_target:
                    st.markdown(":red[**H-target**]")
                    if st.session_state.number_input:
                        dh_show = st.number_input("**Drawdown $$\Delta h$$** in withdrawal well", 0.01, 10.0, st.session_state.dh_show, 0.1, key="dh_show_input", on_change=update_dh_show)
                    else:
                        dh_show = st.slider      ("**Drawdown $$\Delta h$$** in withdrawal well", 0.01, 10.0, st.session_state.dh_show, 0.1, key="dh_show_input", on_change=update_dh_show)
                else:
                    st.markdown(":blue[**Q-target**]")
                    if st.session_state.number_input:
                        Q_show = st.number_input("**Withdrawal rate $Q$** in the well", 0.001, 1.0, st.session_state.Q_show, 0.001, key="Q_show_input", on_change=update_Q_show)
                    else:
                        Q_show = st.slider      ("**Withdrawal rate $Q$** in the well", 0.001, 1.0, st.session_state.Q_show, 0.001, key="Q_show_input", on_change=update_Q_show)   
            if show_plot3:
                if st.session_state.number_input:
                    h_cell_slider = st.number_input("**Aquifer head** $h_{aq}$ [m]", 0.0, 20.0, st.session_state.h_cell_slider, 0.1, key="h_cell_slider_input", on_change=update_h_cell_slider)
                else:
                    h_cell_slider = st.slider      ("**Aquifer head** $h_{aq}$ [m]", 0.0, 20.0, st.session_state.h_cell_slider, 0.1, key="h_cell_slider_input", on_change=update_h_cell_slider)
                if st.session_state.number_input:
                    h_thr = st.number_input("**Threshold head** $h_{thr}$ [m]", 0.0, 10.0, st.session_state.h_thr, 0.1, key="h_thr_input", on_change=update_h_thr)
                else:
                    h_thr = st.slider      ("**Threshold head** $h_{thr}$ [m]", 0.0, 10.0, st.session_state.h_thr, 0.1, key="h_thr_input", on_change=update_h_thr)                 
                th = st.toggle("Apply withdrawal thresholds")
                if th:
                    Q_range = st.slider("Discharge cutoff range $[Q_{mn}, Q_{mx}]$ [m³/s]", 0.0, st.session_state.Q_show, (0.1*st.session_state.Q_show, 0.3*st.session_state.Q_show), 0.01)
                    Q_mn, Q_mx = Q_range                
    
    with columns1[2]:
        modify_CWC = st.toggle('Toggle to **modify CWC parameters**')
    
    # Parameter control below the general pattern
    if modify_CWC:
        # Activate second dataset
        if show_plot1 or show_plot3:
            st.session_state.second = st.toggle("Toggle to define a second parameter set for comparison")
        st.latex(r'''CWC = [ A + B + C Q^{(P-1)}]^{-1}''')
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
                A = st.number_input("", 0.001, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A, label_visibility="collapsed")
            with columns4[1]:
                B = st.number_input("", 0.001, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B, label_visibility="collapsed")
            with columns4[2]:
                C = st.number_input("", 0.00, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C, label_visibility="collapsed")
            with columns4[3]:
                P = st.number_input("", 1.0, 4.0,   st.session_state.P, 0.1, key="P_input", on_change=update_P, label_visibility="collapsed")
        else:
            with columns4[0]:
                A = st.slider      ("", 0.001, 10.0, st.session_state.A, 0.1, key="A_input", on_change=update_A, label_visibility="collapsed")
            with columns4[1]:
                B = st.slider      ("", 0.001, 10.0, st.session_state.B, 0.1, key="B_input", on_change=update_B, label_visibility="collapsed")        
            with columns4[2]:
                C = st.slider      ("", 0.00, 10.0, st.session_state.C, 0.1, key="C_input", on_change=update_C, label_visibility="collapsed")   
            with columns4[3]:
                P = st.slider      ("", 1.0, 4.0,   st.session_state.P, 0.1, key="P_input", on_change=update_P, label_visibility="collapsed")
        
        if st.session_state.second:
            st.write('**:red[Dataset 2]** (A, B, C, P)')
            columns5 = st.columns((1,1,1,1))
            if st.session_state.number_input:
                with columns5[0]:
                    A2 = st.number_input("", 0.001, 10.0, st.session_state.A2, 0.1, key="A2_input", on_change=update_A2, label_visibility="collapsed")
                with columns5[1]:
                    B2 = st.number_input("", 0.001, 10.0, st.session_state.B2, 0.1, key="B2_input", on_change=update_B2, label_visibility="collapsed")
                with columns5[2]:
                    C2 = st.number_input("", 0.00, 10.0, st.session_state.C2, 0.1, key="C2_input", on_change=update_C2, label_visibility="collapsed")
                with columns5[3]:
                    P2 = st.number_input("", 1.0, 4.0,   st.session_state.P2, 0.1, key="P2_input", on_change=update_P2, label_visibility="collapsed")
            else:
                with columns5[0]:
                    A2 = st.slider      ("", 0.001, 10.0, st.session_state.A2, 0.1, key="A2_input", on_change=update_A2, label_visibility="collapsed")
                with columns5[1]:
                    B2 = st.slider      ("", 0.001, 10.0, st.session_state.B2, 0.1, key="B2_input", on_change=update_B2, label_visibility="collapsed")        
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
       
    # ------------------   
    # FIRST PLOT
    
    #with st.expander("Show / Hide the Discharge-Drawdown relationship for the MNW boundary", expanded = True):
    if show_plot1:
        st.subheader('🔵 Plot 1', divider = 'blue')
        st.markdown("""
        :blue[**Plot 1**: Withdrawal and drawdown in a well.] This figure shows the relationship between **withdrawal rate _Q_**, and the resulting **drawdown**. Here, drawdown is the difference between the aquifer head and head in the well. Up to **two parameter sets of the CWC** can be considered. _For a model representing a field setting, the aquifer head varies with time depending on model parameters and boundary stresses such as other wells pumping, variable recharge, and stream seepage. Here, one value of head is assigned to the aquifer cell and calculations are made for parameter variations assuming that aquifer head is constant._
        """)
            
        label_head_axis = "Head difference $\Delta h = h_{aq} - h_{Well}$ (m) "
        label_flow_axis = "Withdrawal rate $Q$ (m³/s)"
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
            ax_schematic.text(0.5, 0 - 0.2, 'Aquifer (cell) \nhead', color='blue', fontsize=12)
            # Style
            ax_schematic.set_xlim(0, 2)
            ax_schematic.set_ylim(10, 0)
            ax_schematic.axis('off')
            
            # --- RIGHT AXIS: Q vs Δh plot ---
            # Values related to Q are negative to indicate pumping from the aquifer
            if turn:
                #ax_plot.plot(Q_values, delta_h_range, label="$Q$-$\Delta h$ relation 1", color='darkblue', linewidth=4)
                ax_plot.plot([-q for q in Q_values], delta_h_range, label="$Q$-$\Delta h$ relation 1", color='darkblue', linewidth=4)
                if st.session_state.second:
                    ax_plot.plot([-q for q in Q_values2], delta_h_range2, label="$Q$-$\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
                if h_target:
                    ax_plot.plot(-Q_show, delta_head, 'ro',markersize=10, label="h_target")
                    ax_plot.plot([0, -Q_line], [delta_head, delta_head], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(-Q_show2, delta_head2, 'ro',markersize=10)
                else:
                    ax_plot.plot(-Q_show, delta_head, 'o',markersize=10, markerfacecolor='lightblue', markeredgecolor='blue', label="Q_target")
                    ax_plot.plot([-Q_show, -Q_show], [aquifer_thickness, h_line], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(-Q_show2, delta_head2, 'o', markersize=10, markerfacecolor='lightblue', markeredgecolor='blue')            
                ax_plot.set_ylabel(label_head_axis, fontsize=12, labelpad=15)
                ax_plot.set_xlabel(label_flow_axis, fontsize=12, labelpad=15)
                ax_plot.set_ylim(10.1, 0)
                ax_plot.set_xlim(0, -1.01)
            else:
                ax_plot.plot(delta_h_range, [-q for q in Q_values], label="$Q$-$\Delta h$ relation 1", color='darkblue', linewidth=4)
                if st.session_state.second:
                    ax_plot.plot(delta_h_range2, [-q for q in Q_values2], label="$Q$-$\Delta h$ relation 2", linestyle='--', color='red', linewidth=3)
                if h_target:
                    ax_plot.plot(delta_head,-Q_show, 'ro',markersize=10, label="h_target")
                    ax_plot.plot([delta_head, delta_head], [0, -Q_line], linestyle='dotted', color='grey', linewidth=2)
                    if st.session_state.second:
                        ax_plot.plot(delta_head2, -Q_show2, 'ro',markersize=10)
                else:
                    ax_plot.plot(delta_head, -Q_show,'bo',markersize=10, markerfacecolor='lightblue', markeredgecolor='blue', label="Q_target")
                    if st.session_state.second:
                        ax_plot.plot(delta_head2, -Q_show2, 'bo',markersize=10, markerfacecolor='lightblue', markeredgecolor='blue')
                        ax_plot.plot([0, h_line], [-Q_show2, -Q_show2], linestyle='dotted', color='grey', linewidth=2)
                    else:
                        ax_plot.plot([0, h_line], [-Q_show, -Q_show], linestyle='dotted', color='grey', linewidth=2)
                ax_plot.set_xlabel(label_head_axis, fontsize=12, labelpad=15)
                ax_plot.set_ylabel(label_flow_axis, fontsize=12, labelpad=5)
                ax_plot.set_xlim(0, 10.1)
                ax_plot.set_ylim(0, -1.01)
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
                st.write(':blue[***CWC1***] (in m²/s) = %5.2f' %(st.session_state.A + st.session_state.B + st.session_state.C * Q_show**(st.session_state.P - 1)))
                if st.session_state.second:
                    st.write(':red[**Discharge $Q2$ to the well**] (in m³/s) = %5.3f' %Q_show2)
                    st.write(':red[***CWC2***] (in m²/s) = %5.2f' %(st.session_state.A2 + st.session_state.B2 + st.session_state.C2 * Q_show2**(st.session_state.P2 - 1)))
            else:
                st.write(':grey[**Discharge to the well**] (in m³/s) = %5.3f' %Q_show)
                st.write(':blue[**Drawdown $$\Delta h$$ in the well**] (in m) = %5.2f' %delta_head)
                st.write(':blue[***CWC1***] (in m²/s) = %5.2f' %(st.session_state.A + st.session_state.B + st.session_state.C * Q_show**(st.session_state.P - 1)))
                if st.session_state.second:
                    st.write(':red[**Drawdown $$\Delta h2$$ in the well**] (in m) = %5.2f' %delta_head2)
                    st.write(':red[***CWC2***] (in m²/s) = %5.2f' %(st.session_state.A2 + st.session_state.B2 + st.session_state.C2 * Q_show2**(st.session_state.P2 - 1)))                    
    
        # --- PLOT 1 EXPLANATION ---  
        with st.expander('Click here to read more :blue[**About this Plot**]'):
            st.markdown("""
            #### :blue[🔎 About this Plot]
            
            This plot illustrates the relationship between discharge and drawdown (the difference between the aquifer head ($h_{aq}$) and the well head ($h_{well}$)), using the Multi-Node Well (MNW)  package to represent a withdrawal well.
            
            It allows for exploration of two operating modes:
            1. :blue[**Q-target**] (defined discharge): Calculates the resulting drawdown for a given withdrawal rate.
            2. :red[**H-target**] (defined drawdown): Calculates the discharge required to maintain a specified drawdown (e.g., to avoid reaching a threshold head in the well that would reduce, or stop, withdrawal).
            
            The interactive plot is shown in two side-by-side images:
            - On the **right**, the Q–Δh curve shows how head loss varieswith withdrawal rate.
            - On the **left**, a schematic illustrates the difference between $h_{aq}$ and $h_{well}$ (drawdown) in relationship to the withdrawal rate $Q$.
            
            Users can modify the **aquifer-to-well conductance (CWC)**, defined via the parameters $A$, $B$, $C$, and the exponent $P$, and compare two configurations to better understand how well losses (linear and nonlinear) influence the character of the relationship.
            
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
               * Modify the withdrawal rate and the parameters to investigate the response in the interactive plot. A higher withdrawal rate causes more head decline in the well, but the modest settings of CWC parameter values result in minimal additional head loss in the well for extremely high flow rates.
            
            2. **Switch to H-target**
               * Set the CWC parameters to:
                 * $A = 5.0$, $B = 5.0$, $C = 0.0$, $P = 2.0$
               * Toggle to :red[**H-target**] mode
               * Vary drawdown Δh from $0.5$ to $5.0$ m
               * Observe how $Q$ responds to increasing drawdown. The relationship is the same, but now setting $h_{well}$ produces the related value of $Q$, instead of setting $Q$ to obtain the value of $h_{well}$.
            
            3. **Compare Parameter Sets**
               * Toggle for a **Second parameter set** in the CWC menu and try a restrictive case:
                 * e.g., $A = 1.0$, $B = 0.2$, $C = 2.0$, $P = 2.5$
               * Compare the resulting Q–Δh relationships.
            
            _Use the plot orientation toggle for alternate layouts and enable/disable the schematic as needed._
            """)
        with st.expander('Click here for an :blue[**Exercise Related to this Plot**]'):
            st.markdown("""
            🎯 **Learning Objectives**
            
            This exercise is designed with the intent that, by completing it, you will be able to:
            
            - Understand how the withdrawal–drawdown relationship is defined for MNW boundaries
            - Explain the influence of CWC parameters ($A$, $B$, $C$, $P$)
            - Differentiate between Q-target and H-target modes
            - Compare well behavior for different parameter values
            
            🛠️ **Tasks**
            
            1. **Explore Q–Δh Relationship**
               * Set: $A = 4.0$, $B = 5.0$, $C = 1.0$, $P = 2.0$
               * Use :blue[**Q-target**] mode
               * Vary $Q$ from $0.01$ to $0.5$ m³/s
               * 📝 Record where the curve steepens and explain the influence of the different parameters in CWC ($A$, $B$, $C$, and $P$)
            
            2. **Test Parameter Sensitivity**
               * Keep: $A = 4.0$, $B = 5.0$, $C = 1.0$, $P = 2.0$
               * Set $Q = 0.3$ m³/s in :blue[**Q-target**] mode
               * Enable the **second parameter set** 
               * Vary $A$, then systematically change $B$, $C$, and $P$ (ultimately setting all values to 4) and compare responses
               * 💭 Reflect on the role of linear versus nonlinear resistance.
                   * Switch on/off the linear resistance by setting $A$ and $B$ to $0$.
                   * Switch on/off the nonlinear resistance by setting $C$ to $0$.
               * 💭 Reflect on what parameter values would represent well-aging?
            
            3. **Reverse Analysis with H-target**
               * Switch to :red[**H-target**] and make sure to use the initial parameter set: $A$ = $4.0$, $B$ = $5.0$, $C$ = $1.0$, $P$ = $2.0$
               * Set $Δh$ = $2.0$, $4.0$, $6.0$ m
               * Compare resulting $Q$ values across different parameter sets (e.g., to reflect an aged well).
               * At what Δh value does $Q$ exceed $0.2$ m³/s? How much does well-aging affect the efficiency?
            
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
    
    # ------------------   
    # SECOND PLOT
    
    #with st.expander("Show / Hide the **Q-h plot** for the MNW boundary"):
    if show_plot2:
        st.subheader('🟢 Plot 2', divider = 'green')
        st.markdown("""
        :green[**Plot 2**: Relationship between discharge (_Q_), heads (_h_), and drawdown as function of CWC]. The plot shows the **_Q-h_-relationship** for an MNW withdrawal well. Additionally, the relationship between discharge and hydraulic head in a well relative to the head in the aquifer (drawdown) is presented as function of the CWC.
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
                ax2.plot(Q_2nd, h_2nd, color='black', label=fr"$Q$-$h_{{aq}}$ plot with $Q = {Q_show:.2f}$ m³/s", linewidth=4)
                ax2.plot(Q_values_2nd, h_well_range, linestyle='--', color='lightgrey', linewidth=3, label=r"$Q$-$h_{Well}$")
                ax2.axhline(y=h_cell, linestyle='dotted', color='black', linewidth=2)
                ax2.set_ylabel("Hydraulic head $h$ [L]", fontsize=14)
                ax2.set_xlabel("Flow Into the Ground-Water System \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14)
                ax2.set_xlim(-1, 1)
                ax2.set_ylim(0, 20)
                if visualize:
                    ax2.plot(Q_show*-1, h_cell,'o', color='skyblue', markersize=12, label=f'head in cell = {h_cell:.2f} m')
                    ax2.plot(Q_show*-1, h_well,'o', color='blue',markersize=10, label=f'head in well = {h_well:.2f} m')    
            else:
                ax2.plot(h_2nd, Q_2nd, color='black', label=fr"$Q$-$h_{{aq}}$ plot with $Q = {Q_show:.2f}$", linewidth=4)
                ax2.plot(h_well_range, Q_values_2nd, linestyle='--', color='lightgrey', linewidth=3, label=r"$Q$-$h_{Well}$")
                ax2.axvline(x=h_cell, linestyle='dotted', color='black', linewidth=2)
                ax2.set_xlabel("Hydraulic head $h$ [L]", fontsize=14)
                ax2.set_ylabel("Flow Into the Ground-Water System \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14)
                ax2.set_ylim(-1, 1)
                ax2.set_xlim(0, 20)
                if visualize:
                    ax2.plot(h_cell, Q_show*-1, 'o',color='skyblue', markersize=12, label=f'head in cell = {h_cell:.2f} m')
                    ax2.plot(h_well, Q_show*-1, 'o',color='blue', markersize=10, label=f'head in well = {h_well:.2f} m')
            
            ax2.set_title("Q-h Behavior for the MNW Boundary", fontsize=16, pad=20)
            ax2.tick_params(axis='both', labelsize=12)        
            ax2.legend(fontsize=14, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
            
            columns_fig2=st.columns((1,8,1))
            with columns_fig2[1]:
                st.pyplot(fig2, bbox_inches='tight')    
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Make the plot live and visualize the results]** to see this plot')
            
            
        # --- PLOT 2 EXPLANATION ---  
        with st.expander('Click here to read more :green[**About this Plot**]'):
            st.markdown("""
            #### :green[🔎 About this Plot]
            
            This plot illustrates the relationship between **well head ($h_{well}$)** and **discharge (Q)** for a **fixed aquifer head ($h_{aq}$)** in a Multi-Node Well (MNW). 
            
            Two modes are available:
            1. :blue[**Q-target**]: Specify the discharge and calculate the resulting $h_{well}$ (drawdown) for a given conductance (initially set to $1.0$).
            2. :red[**H-target**]: Specify $h_{well}$ and compute the discharge resulting from head difference and conductance.
            
            Unlike the MODFLOW well (WEL) or recharge (RCH) boundaries that impose a fixed flux, and unlike RIV or DRN boundaries that assume **linear head-dependent flow**, MNW simulates **nonlinear resistance** due to turbulence that result from high flow velocity or well construction effects. This is controlled by the **aquifer-to-well conductance (CWC)**, defined by parameters $A$, $B$, $C$, and $P$.
            
            The aquifer head ($h_{aq}$) is always $10$ m for this plot, so that the interaction between discharge and well head is isolated for analysis.
            """)
        with st.expander('Click here for :green[**Instructions To Get Started with this Plot**]'):
            st.markdown("""
            #### :green[🧭 Getting Started]

            Begin with the following steps to explore the MNW discharge–head relationship:
            
            1. **Reference Parameters**
               * The aquifer head is fixed at $h_{aq}$ = $10$ m in this plot
            
            2. **Explore Q-target Mode**
               * Set the CWC parameter values to: $A$ = $5.0$, $B$ = $5.0$, $C$ = $1.0$, $P$ = $2.0$
               * Set discharge $Q$ between $0.05$ and $0.7$ m³/s
               * Observe the resulting well head $h_{well}$ and the increasing drawdown
            
            3. **Switch to H-target Mode**
               * Set the CWC parameter values to: $A$ = $5.0$, $B$ = $5.0$, $C$ = $1.0$, $P$ = $2.0$
               * Set drawdown $Δh$ between $1.0$ and $6.5$ m
               * Observe how discharge changes with increasing drawdown
            
            4. **Modify CWC Parameter Values**
               * For both Q-target Mode and H-target Mode:
                 * Try different values for $A$, $B$, and $P$
                 * Compare how the drawdown or flow response changes
            
            💡 Consider how your observations differ from the behavior of **DRN** and **RIV** boundaries (linear, head-dependent flow) and from **WEL** and **RCH** boundaries (fixed Q).

            """)
        with st.expander('Click here for an :green[**Exercise About this Plot**]'):
            st.markdown("""
            🎯 **Learning Objectives**
            
            This exercise is designed with the intent that, by completing it, you will be able to:
            
            - Understand how MNW models nonlinear resistance between aquifer and well
            - Interpret how discharge and drawdown change under different parameterizations
            - Explain how MNW behavior differs from other boundary conditions (WEL, RCH, DRN, RIV)
            - Identify cases where turbulence becomes dominant
            
            🛠️ **Tasks**
            
            1. **Well Head Response to Discharge**
               * Use :blue[**Q-target**] mode
               * Set: $A = 0.5$, $B = 0.05$, $C = 1.0$, $P = 2.0$
               * Vary $Q$ from $0.05$ to $0.8$ m³/s
               * 📝 Record $h_{well}$ and compute the drawdown: $\Delta h = h_{aq} - h_{well}$
            
            2. **Effect of Parameter Variation**
               * Starting with the CWC settings from step 1, for a few values of Q, make the following changes and note the drawdown
                 * Double $A$
                 * Double $B$
                 * Double $C$
                 * Increase $P$ to $2.5$ or $3.0$
               * 📝 Record how each change affects drawdown for a given $Q$
               * Which parameters cause nonlinear increases in $Q$?
            
            3. **Explore H-target Mode**
               * Retaining the final settings for CWC from step 2, set drawdown to $Δh$ = $2.0$ m, then in a few steps, lower it to $0.5$ m
                 * 📝 Record how discharge changes (when the value is out of the axis range as is the case for $Δh$ = $2.0$ m, the value of $Q$ can be found in the legend)
            
            4. **Conceptual Comparison**
               * When is the MNW behavior close to:
                 - A constant $Q$ source (WEL)?
                 - A linear head-dependent boundary (RIV)?
               * What role does the parameter $P$ play in making this boundary behave differently?
            
            🧠 Reflect: What happens if you set $A$ = $0$? When is turbulence (nonlinear loss) dominant?

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

      
    # ------------------   
    # THIRD PLOT HERE - Q vs h_cell (with head and discharge thresholds)
    
    #with st.expander('Show the MNW boundary with varying aquifer heads'):  
    if show_plot3:
        st.subheader('🔴 Plot 3', divider = 'red')
        st.markdown("""
        :red[**Plot 3**: _Q-h_-Relationship for a withdrawal well with thresholds.] This plot demonstrates the effect of a threshold head that limits the withdrawal rate _Q_.
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
            fig3, ax3 = plt.subplots(figsize=(10, 8))
            fig3.subplots_adjust(right=0.6)  # reserve 25% of figure width for legend
            if turn:
                # if threshold is considered
                if th:
                    ax3.axvline(x=-Q_show, linestyle='--', color='lightgrey', linewidth=1)  
                    ax3.plot([-q for q in Q_plot], h_3rd, color='black', linewidth=1, linestyle=':')
                    ax3.plot([-q for q in Q_plot_mn], h_3rd, color='black', linewidth=3, label=r"$Q$-$h_{aq}$ with threshold")
                    ax3.plot([-q for q in Q_plot_mx], h_3rd, color='black', linewidth=3, linestyle='--')       
                    if st.session_state.second:
                        ax3.plot([-q for q in Q_plot2], h_3rd, color='red', linewidth=1, linestyle=':', label=r"$Q$-$h_{aq}$ with threshold CWC2")                    
                    # Empty line for legend entry
                    ax3.plot([], [], linewidth=0, label=r'$\mathit{Active\ Q\ for\ selected\ heads:}$')                    
                    ax3.plot(-Q_dot_th, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'Q for $h_{{aq}}$ = {h_cell_slider:.2f} m')
                    if st.session_state.second:
                        ax3.plot(-Q_dot_th2, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'Q for $h_{{aq}}$ = {h_cell_slider:.2f} m')
                else:                
                    ax3.axvline(x=-Q_show, linestyle='--', color='lightgrey', linewidth=1)
                    ax3.plot([-q for q in Q_plot], h_3rd, color='black', linewidth=4, label=r"$Q$-$h_{aq}$ with threshold")       
                    if st.session_state.second:
                        ax3.plot([-q for q in Q_plot2], h_3rd, color='red', linewidth=2, linestyle=':', label=r"$Q(h_{aq})$ with threshold CWC2")
                    # Empty line for legend entry
                    ax3.plot([], [], linewidth=0, label=r'$\mathit{Active\ Q\ for\ selected\ heads:}$')                        
                    ax3.plot(-Q_dot, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Q for $h_{{aq}}$ = {h_cell_slider:.2f} m')
                    if st.session_state.second:
                        ax3.plot(-Q_dot2, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'Q for $h_{{aq}}$ = {h_cell_slider:.2f} m')
                ax3.axhline(y=h_cell_slider, linestyle='--', color='dodgerblue', linewidth=2)
                ax3.axhline(y=h_thr, linestyle='--', color='orange', linewidth=2)
                if h_well >= h_thr:
                    ax3.plot(-Q_dot, h_well, 'o', markersize=10, markeredgecolor='darkblue', markerfacecolor='none', label=f'Q projected on $h_{{Well}}$ = {h_well:.2f} m')
                else:
                    ax3.plot(-Q_dot, h_thr, 'ro',markersize=10, label=f'Q for $h_{{Well}}$  = {h_thr:.2f} m  = $h_{{thr}}$')  
                if st.session_state.second:
                    if h_well2 >= h_thr:
                        ax3.plot(-Q_dot2, h_well2, 'o', markersize=10, markeredgecolor='darkblue', markerfacecolor='none', label='Q projected on $h_{Well} CWC2$')
                    else:
                        ax3.plot(-Q_dot2, h_thr, 'ro',markersize=10, label=f'Q projected on $h_{{Well}}$ CWC2  = {h_thr:.2f} m  = $h_{{thr}}$')       
            
                # Add head annotations
                ax3.text(-0.65, h_cell_slider+1.3, "hydraulic head \nin the cell $h_{aq}$", va='center',color='dodgerblue',  fontsize=14)
                ax3.text(-0.57, h_thr-0.9, "threshold head $h_{thr}$",  va='center',color='red', fontsize=14)                        
                
                ax3.set_xlabel("Withdrawal rate $Q$ (m³/s)", fontsize=14)
                ax3.set_ylabel("Hydraulic heads $h$ (m)", fontsize=14)
                ax3.set_xlim(0.01, -1)
                ax3.set_ylim(0, 20)
            else:
                # if threshold is considered
                if th:
                    ax3.plot(h_3rd, [-q for q in Q_plot], color='black', linewidth=1, linestyle=':')
                    ax3.plot(h_3rd, [-q for q in Q_plot_mn],  color='black', linewidth=3, label=r"$Q$-$h_{aq}$ with threshold")
                    ax3.plot(h_3rd, [-q for q in Q_plot_mx],  color='black', linewidth=3, linestyle='--')
                    if st.session_state.second:
                        ax3.plot(h_3rd, [-q for q in Q_plot_th], color='red', linewidth=1, linestyle=':', label=r"$Q$-$h_{aq}$ with threshold CWC2")
                    # Empty line for legend entry
                    ax3.plot([], [], linewidth=0, label=r'$\mathit{Active\ Q\ for\ selected\ heads:}$')   
                    ax3.plot(h_cell_slider, -Q_dot_th, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'Q for $h_{{aq}}$ = {h_cell_slider:.2f} m')
                    if st.session_state.second:
                        ax3.plot(h_cell_slider, -Q_dot_th2, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label='Q for $h_{aq}$ CWC2')        
                else:
                    ax3.plot(h_3rd, [-q for q in Q_plot], color='black', linewidth=4, label=r"$Q$-$h_{aq}$ with threshold")
                    if st.session_state.second:
                        ax3.plot(h_3rd, [-q for q in Q_plot2], color='red', linewidth=2, linestyle=':', label=r"$Q(h_{aq})$ with threshold")
                    # Empty line for legend entry
                    ax3.plot([], [], linewidth=0, label=r'$\mathit{Active\ Q\ for\ selected\ heads:}$')   
                    ax3.plot(h_cell_slider, -Q_dot, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'Q for $h_{{aq}}$ = {h_cell_slider:.2f} m')
                    if st.session_state.second:
                        ax3.plot(h_cell_slider, -Q_dot2, 'ro', markersize=10, label='Q for $h_{aq}$ CWC2')
                ax3.axvline(x=h_cell_slider, linestyle='--', color='dodgerblue', linewidth=2)
                ax3.axvline(x=h_thr, linestyle='--', color='orange', linewidth=2)
                if h_well >= h_thr:
                    ax3.plot(h_well, -Q_dot, 'o', markersize=10, markeredgecolor='darkblue', markerfacecolor='none', label=f'Q projected on $h_{{Well}}$ = {h_well:.2f} m')
                else:
                    ax3.plot(h_thr, -Q_dot, 'ro',markersize=10, label=f'Q for $h_{{Well}}$  = {h_thr:.2f} m  = $h_{{thr}}$')
                if st.session_state.second:
                    if h_well2 >= h_thr:
                        ax3.plot(h_well2, -Q_dot2, 'o', markersize=10, markeredgecolor='darkblue', markerfacecolor='none', label='Q projected on $h_{Well} CWC2$')
                    else:
                        ax3.plot(h_thr, -Q_dot2, 'ro',markersize=10, label=f'Q for $h_{{Well}}$ CWC2 = {h_thr:.2f} m  = $h_{{thr}}$')           
                        
                # Add head annotations
                ax3.text(h_cell_slider+0.5, -0.93, "hydraulic head \nin the cell $h_{aq}$", va='center',color='dodgerblue',  fontsize=14)
                ax3.text(h_thr-4.5, -0.93, "threshold \nhead $h_{thr}$",  va='center',color='red', fontsize=14)     
                
                ax3.set_xlabel("Hydraulic heads $h$ [m]", fontsize=14)
                ax3.set_ylabel("Discharge $Q$ [m³/s]", fontsize=14)
                ax3.set_xlim(0, 20)
                ax3.set_ylim(0.01, -1)
            
            ax3.set_title("Q-h Behavior for the MNW Boundary with Threshold", fontsize=16, pad=20)
            ax3.tick_params(axis='both', labelsize=12)
            ax3.legend(fontsize=14, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
            
            columns_fig3=st.columns((1,10,1))
            with columns_fig3[1]:
                st.pyplot(fig3, bbox_inches='tight') 
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Make the plot live and visualize the results]** to see this plot')

        # --- PLOT 3 EXPLANATION ---  
        with st.expander('Click here to read more :red[**About this Plot**]'):
            st.markdown("""
            #### :red[🔎 About this Plot]
            
            This plot illustrates the **_Q–h_-relationship of a Multi-Node Well (MNW)** under conditions where a **threshold head** is imposed so that the model does not allow withdrawal to continue at a rate greater than can be produced in the field. 
            
            The aquifer head ($h_{aq}$) and the discharge ($Q$) define the well head ($h_{well}$) through the nonlinear **aquifer-to-well conductance (CWC)** equation (as discussed in the Theory section above).
                      
            If the computed well head falls **below the defined threshold head**, the withdrawal rate is automatically **reduced** such that the well head is held at the threshold. This mechanism mimics a pump protection strategy to avoid dry wells or pump damage due to excessive drawdown.
            
            The MNW behavior is also constrained by rate thresholds that reflect practical limitations of typical pumps:
            - **Qmn** – the lower limit of the pump capacity, which, when reached, the well will be shut off in the model simulation
            - **Qmx** – the calculated discharge rate that triggers a switched-off pump to switch back on
            
            This plot helps visualize:
            - When the **threshold becomes active**
            - How **withdrawal is limited** to protect the well
            - The nonlinear relationship between Q and $h_{well}$ under withdrawal-limited conditions for various CWC parameters

            """)
        with st.expander('Click here for :red[**Instructions To Get Started with this Plot**]'):
            st.markdown("""
            #### :red[🧭 Getting Started]
            
            Follow these steps to explore threshold-controlled withdrawal behavior in MNW:
            
            1. **Set Initial Conditions**
               * $h_{aq} = 10$ m
               * Threshold head $h_{thr} = 6.0$ m
               * CWC parameters: $A = 0.5$, $B = 0.05$, $C = 0$, $P = 2.0$
            
            2. **Sweep through values of Q**
               * Vary withdrawal rate $Q$ from 0.05 to 0.7 m³/s
               * Observe how $h_{well}$ responds to withdrawal
               * Identify where the well head $h_{well}$ reaches the threshold head $h_{thr}$
            
            3. **Explore Threshold Activation**
               * Increase the withdrawal rate _Q_ beyond the point where $h_{well} = h_{thr}$
               * Note that the active _Q_ (represented by the dot in the plot) is automatically reduced to keep $h_{well} = h_{min}$
            
            4. **Explore Withdrawal Thresholds**
               * Set the threshold head $h_{thr}$ to 5.0 m and the aquifer head $h_{aq}$ to 15.0 m. Set the withdrawal rate to 0.5 m³/s. With these settings, the system is in proper operation.
               * Toggle **Apply withdrawal thresholds** to automatically switch off/on the pump then the Qmn and Qmx will appear on the plot as solid and dashed black lines
               * Set Qmn and Qmx to 0.05 and 0.2 m³/s
               * Now, lower the aquifer head $h_{aq}$ smoothly down to 5.1 m. Lowering the aquifer head can be caused by various reasons, e.g., neighboring withdrawal wells. (_hint: if you access this app through a computer, you can gradually reduce Q with the arrow-keys of your keyboard_)
               * While lowering the aquifer head, observe how the adjusted withdrawal rate - represented by the dot in the plot - is affected.
               * Once the aquifer head reaches 5.1 m, graduallly raise the head back to 15.0 m and observe the adjusted withdrawal rate (dot in the plot).
            
            5. **Modify Parameters**
               * Try different values for $A$, $B$, $C$, and $P$
               * Vary Q (Q-target), Δh (H-target), aquifer head $h_{aq}$ and threshold head $h_{thr}$, and investigate the MNW behavior with the interactive plot.
            
            💡 This exercise facilitates understanding of how operational constraints (like prevention of water level dropping below a pump) interact with well head-loss to adjust the simulated flow rate so a model cannot represent more withdrawal of water than the well design will allow.
            """)
        with st.expander('Click here for an :red[**Exercise About this Plot**]'):
            st.markdown("""
            🎯 **Learning Objectives**
            
            This exercise is designed with the intent that, by completing it, you will be able to:
            
            - Explain how threshold head limits influence MNW discharge behavior
            - Identify the conditions for shich withdrawal is reduced to protect a wells
            - Analyze how nonlinear head losses and operational limits combine to define feasible withdrawal rates
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
               * Set Qmn = 0.05 m³/s and Qmx = 0.2 m³/s
               * Try to exceed this value by lowering the aquifer head to the threshold head $h_{thr}$ adn take notice of the aquifer head when withdrawal stops. (_hint: if you access this app through a computer, you can gradually reduce Q with the arrow-keys of your keyboard_)
               * Now, increase the aquifer head to 15.0 m and notice the value of aquifer head when withdrawal starts again.
               * Double the parameter for linear well loss $B$ and repeat the procedure. Quantify the changes in terms of aquifer heads for switching off/on the withdrawal.
            
            💭 Reflect:
            - When is the threshold head the limiting factor?
            - How do Qmn/Qmx affect the value of practical withdrawal?
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
The Multi-Node Well (MNW) boundary in MODFLOW adds realism to well simulations by distributing flow across multiple model cells and introducing operational and physical constraints. This boundary goes beyond fixed withdrawal rates by simulating **head-dependent flow**, **skin effects**, and **withdrawal limits** — key factors in models properly representing wells in physical settings.

Q–h plots, allowed exploration of how MNW behavior with transitions between active withdrawal, flow cutoffs, and constraint-induced reduction of flow. Understanding these condtions supports better interpretation, calibration, and reliability in groundwater modeling projects.

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
