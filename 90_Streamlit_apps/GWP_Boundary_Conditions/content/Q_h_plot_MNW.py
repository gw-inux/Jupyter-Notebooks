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
from streamlit_scroll_to_top import scroll_to_here
from GWP_Boundary_Conditions_utils import read_md
from GWP_Boundary_Conditions_utils import flip_assessment
from GWP_Boundary_Conditions_utils import render_toggle_container
from GWP_Boundary_Conditions_utils import prep_log_slider
from GWP_Boundary_Conditions_utils import get_label
from GWP_Boundary_Conditions_utils import get_step

# ---------- Track the current page
PAGE_ID = "MNW"

# Do (optional) things/settings if the user comes from another page
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID
    
# ---------- Doc-only view for expanders (must run first)
params = st.query_params
DOC_VIEW = params.get("view") == "md" and params.get("doc")

if DOC_VIEW:
    md_file = params.get("doc")

    st.markdown("""
    <style>
      /* Hide sidebar & its nav */
      [data-testid="stSidebar"],
      [data-testid="stSidebarNav"] { display: none !important; }

      /* Hide the small chevron / collapse control */
      [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(read_md(md_file))
    st.stop()
    
# ---------- Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# path to questions for the assessments (direct path)
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_mnw.json"
path_quest_plot1 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p1.json"
path_quest_plot2 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p2.json"
path_quest_plot3 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p3.json"
path_quest_plot4 = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_mnw_p4.json"
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

with open(path_quest_plot4, "r", encoding="utf-8") as f:
    quest_plot4 = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
    "Eve L. Kuniansky": [3],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines",
    3: "Retired from the US Geological Survey"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# --- Start here

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
    
    2. **What happens if the water level in the well (but not the water level in the model cell) drops below the pump intake? Should a model continue to simulate withdrawal of groundwater?**
    
    ▶️ The :rainbow[**Multi-Node Well (MNW)**] package in MODFLOW supports more realistic simulation of well hydraulics than the Well package, even in one-node wells. MNW allows you to:
    - account for **additional drawdown within the wellbore** ($h_{gw}-h_{well}$) **due to head losses**,
    - define **limiting water levels** below which withdrawal from the well stops, and
    - simulate wells that **automatically shut off** or restart depending on drawdown conditions.
    
    This section **explores the $Q$-$h$ relationship for a withdrawal well in one model cell**. It does not explore injection wells or wells connected to multiple model cells. The interactive plots allow **exploration of how withdrawal rate, groundwater head, well-threshold head, and connectivity between the groundwater and well (:rainbow[_CWC_]) interact to determine drawdown within the well and groundwater discharge to the well**. :rainbow[_CWC_] is an abbreviation for cell-to-well conductance. 'Cell' refers to the model element, which can represent any hydrostratigraphic unit, but is likely an aquifer because most wells are installed in aquifers.
    
    In contrast to the head-dependent MNW boundary, the **WEL boundary in MODFLOW** is a Type II (i.e., Neumann) boundary condition with specified flow. For this initial $Q$-$h$ plot for an MNW boundary, the :blue[**WEL toggle**] allows you to view the equivalent plot for a WEL boundary where $Q$ is defined by the modeler and is independent of head $h$ in the well and groundwater.
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
    # Define groundwater head range
    h_gwi = np.linspace(0, 20, 200)
    QPi = np.full_like(h_gwi, -0.01)
    h_ni = 10.0 # Example head for the cell
    h_WELLi = np.linspace(0, 20, 200)
    Qi = (h_WELLi - h_ni) * st.session_state.CWCi
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_gwi, QPi, color='blue', linewidth=3, label='$Q$-$h_{gw}$')
    # Draw vertical line at QPi and h = 10
    ax.plot([10, 10], [-0.01, -0.05], color='blue',linestyle=':', linewidth=3, label='$h_{gw}$ = 10 m')
    if WEL_equi:
        ax.set_xlabel("Head in the groundwater system (m)", fontsize=14, labelpad=15)
        ax.set_ylabel("Flow into the groundwater \nfrom the WEL boundary $Q_{WEL}$ (m³/s) \nfor $h_{gw}$ = 10 m", fontsize=14, labelpad=15)
        ax.set_title("Flow Between Groundwater and WEL", fontsize=16, pad=10)
    else:
        ax.plot(h_WELLi, Qi, color='black', linewidth=3, label='$Q$-$h_{well}$')
        # Determine the y-values for h = 10
        Qi_10 = (10.0 - h_ni) * st.session_state.CWCi
        QPi_10 = -0.01     
    
        # Draw vertical line at Qi and h_intersect
        h_is = h_ni + (-0.01 / st.session_state.CWCi)
    
        ax.set_xlabel("Head in well and groundwater system (m)", fontsize=14, labelpad=15)
        ax.set_ylabel("Flow into the groundwater \nfrom the MNW boundary $Q_{MNW}$ (m³/s) \nfor $h_{gw}$ = 10 m", fontsize=14, labelpad=15)
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
    **Initial Plot** for exploring how the value of :rainbow[**MNW cell-to-well conductance CWC**] controls the relationship between **head in the well $h_{well}$** and :blue[**flow rate $Q$**] as shown by the **solid black line**, for a constant :blue[**groundwater head $h_{gw}$ of $10$ m**]. 
    
    When **$h_{well}$** is above **:blue[$h_{gw}$]** then **$Q_{MNW}$** is positive and **water flows from the well into the hydrostratigraphic unit** (these conditions are not represented by the initial plot). When **$h_{well}$** is below **:blue[$h_{gw}$]** then **$Q_{MNW}$ is negative** and water flows **out of the hydrostratigraphic unit into the well**. The slope of the $Q$-$h{well}$ line is defined by **:rainbow[cell-to-well conductance _CWC_]**. Later in this section (using Plot 3), we show how **threshold values are specified to limit the active range of the $Q$-$h$ function** in a specific well.
              
    The dotted lines indicate head in the :blue[groundwater (blue)] and head in the **well (black)**, respectively. For this plot, :blue[**$h_{gw}$ is constant at 10 m (blue dotted line)**] and if $h_{well}$ < 0 m, the well is :red[**dry**].  The solid blue $Q$-$h_{gw}$ line is horizontal and represents the specified flow rate $Q_{MNW}$ = -0.01 m³/s. The **intersection of the solid black and blue lines** indicates the head in the well for the specified flow rate **:blue[$Q$]** given the **:rainbow[cell-to-well conductance _CWC_]**.
    
    This **initial plot** is designed to bridge the gap between traditional $Q$-$h$ plots on paper and the :rainbow[**interactive plots**] provided further down in this app, that allow you to explore the $Q$-$h$ relationships more intuitively, supported by interactive controls and guided instructions.
    """)

st.markdown("""
####  💻 How the head-dependent flow feature of MNW may be Applied in Field-Scale Groundwater Modeling

The MNW boundary represents a well with a specified desired discharge rate and accounts for well losses (i.e., lower head within the well than the surrounding hydrostratigraphic unit) that are a function of the connectivity between the well and the hydrostratigraphic unit. If needed, MNW reduces the well discharge to meet criteria specified to protect the well. In contrast, the WEL boundary applies the specified desired discharge without adjustment for the condition where the well is stressed to the point that it cannot supply the desired discharge. MNW also accommodates modeling of wells that extend through multiple model cells and calculates flow to/from each layer, however this module only addresses the head-dependent flow feature of MNW.""")
left_co, cent_co, last_co = st.columns((1,58,1))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/MNWsketch6.png', caption="Illustration of the head losses that can lead to discharge reduction using MNW in MODFLOW. In situation (1) head in the well is above the threshold so the well is pumping at the desired rate. In situation (2) head in the well reached the threshold so the pumping rate is reduced to keep the head in the well at the threshold. In situation (3) head in the aquifer reached the threshold so the pump is shut off. (modified and enhanced from Shapiro et al., 1998)")

with st.expander("Tell me more about **the :rainbow[application of MNW in Field-Scale Groundwater Modeling]**", icon ="🌍"):
    st.markdown("""
    For MNW wells, parameter values can be specified that limit injection or discharge depending on the head in the well. MNW can account for head losses within the well, both linear (due to flow through the hydrostratigraphic unit and the well skin) and nonlinear (due to turbulence of flow converging on the well, moving through the well wall, and flowing through the tangle of pipes and wires within the wellbore). All these processes are accounted for in the cell-to-well conductance term $CWC$. If connectivity between the well and the hydrostratigraphic unit is high, there is no low-hydraulic conductivity skin around the well, and flow is laminar, then drawdown in the well is what would be expected in order to drive flow through the hydrostratigraphic unit to the well. 
    
    As the connectivity decreases in an aging well (i.e., lower conductance due to wellbore wall damage and aging components within the well) the head in the well will reflect additional drawdown as required to drive the water through the well skin and along the wellbore.
    
    As the water level in the well declines, the pump's ability to discharge water may be affected because the lower head above the pump in the well decreases the pump efficiency, or the water level drops to the level of the pump intake. Accordingly, the flow rate is reduced below the specified flow rate due to reduced performance of the well at the lower water level. Ultimately the discharge may be set to zero because the water level is below either the pump intake or the minimum water-level elevation allowed by the well manager who may install switches triggered by water level to prevent damage to the pump. The MNW package makes the appropriate adjustments to the flow rate and reports flow rate reductions to the modeler.
    
    As groundwater heads decline in response to other stresses with in the model, the MNW thresholds are met at lower flow rates, resulting in more reduction of flow to wells than in healthier hydrostratigraphic units.
    """)

st.markdown("""
####  🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following.
- Understand the conceptual and practical differences between a Multi-Node Well (MNW) and a traditional Well (WEL) boundary in MODFLOW.
- Evaluate the influence of well efficiency, skin effects, and conductance on MNW flow behavior.
- Interpret Q–h relationships for MNWs and how they reflect physical and operational limits of well systems.
- Describe how head-dependent flow, water level in the hydrostratigraphic unit next to the well, and constraints such as pump limitations and acceptable water levels are incorporated in the MNW package.
""")

# --- INITIAL ASSESSMENT ---
def content_initial_mnw():
    st.markdown("""#### Initial assessment""")
    st.info("You can use the initial questions to assess your existing knowledge.")
    
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

# Render initial assessment
render_toggle_container(
    section_id="mnw_01",
    label="✅ **Show the initial assessment** – to assess your **EXISTING** knowledge",
    content_fn=content_initial_mnw,
    default_open=False,
)
            
st.subheader('🧪 Theory and Background', divider="rainbow")
st.markdown("""
Flow between a Multi-Node-Well (MNW) and hydrostratigraphic unit that is tapped by the well depends on system parameters describing the flow near, into, and within the well.
""")
with st.expander("Tell me more about **the Theory**", icon ="📑"):
    st.markdown("""
    Flow from the groundwater system into (or out of) a multi-node well is controlled by several factors. These include
    - a user-specified desired flow rate $Q$
    - a cell-to-well conductance factor ($CWC$)
    - optionally, a specified minimum pumping that must be exceeded to keep the well active, and
    - optionally, a specified pumping rate required to reactivate an inactivated well.
    
    The head in the well $h_{well}$ is determined by the interaction among these factors and the head in the groundwater system $h_{gw}$.
    """)
    
    st.latex(r'''h_{well} = h_{gw} + Q/(CWC)''')
    
    st.markdown("""
    $Q$ is negative in an abstraction well so the well losses cause the head in the well to be lower than the head in the hydrostratigraphic unit.
    """)
    
    st.markdown("""
    If the $h_{well}$ is below the well manager's specified lowest elevation, then the flow rate will be reduced to:
    """)
    
    st.latex(r'''Q = CWC (h_{well} - h_{gw})''')
    
    st.markdown("""
    to prevent the well/pump from being damaged. If that $Q$ is below the well manager's specified minimum flow rate then the discharge is reduced to zero.
    """)
    
    st.markdown("""
    where:
    - $Q$ is the flow between the groundwater and well, defined as negative if it is directed out of the groundwater [L³/T],
    - $h_{well}$ is the head in the well [L],
    - $CWC$ is the cell-to-well conductance [L²/T], and
    - $h_{gw}$ is the groundwater head [L] in the cell containing the well. _This head depends on the values of parameters and stresses (e.g., pumping, recharge) throughout the model. It can vary with time and have different values depending on all the model inputs._
    
    The CWC is composed of three terms, describing (1) flow to the well, (2) the skin effect that influences ease of flow through the well wall, and (3) the effect of turbulence in the vicinity of, and within, the well. Accordingly, the cell-to-well conductance $CWC$ is defined as:
    """)
    
    st.latex(r'''CWC = [ A + B + C Q^{(P-1)}]^{-1}''')
    
    st.markdown("""
    where:
    - $A$ = Linear aquifer-loss coefficient that represents head loss due to flow through the aquifer to the well [T/L²]. In a numerical model the head in the aquifer cell containing the well is the average head in the model cell and the lowest head in the cell occurs at the location of the abstraction well. Thus, the well head is lower than the groundwater cell head even when there is no additional resistance at the well wall or in the well. Well-head loss due to A is calculated using the Thiem equation with T being the inverse of A and the radius of influence being the effective radius based on the size of the model cell. [T/L²] ([Konikow et al. 2009](https://doi.org/10.3133/tm6A30)).
    - $B$ = Linear well-loss coefficient that accounts for head loss from _skin effects_ associated with resistance due to **laminar** components of flow adjacent to the well, through the screen, and within the wellbore.
    - $C$ = Nonlinear well-loss coefficient that accounts for head loss from _skin effects_ associated with resistance due to **turbulent** components of flow adjacent to the well, through the screen, and within the wellbore, with dimensions of:
    """)
    st.latex(r'''T^{P}/L^{3P-1}''')
    st.markdown("""
    where
    - $P$ = is the power (exponent) of the nonlinear discharge component of well loss
    - $T$ = represents the dimension of time
    - $L$ = represents the dimension of length
    """)

st.subheader('Interactive plots to facilitate understanding of the general characteristics of the discharge-head relationships in the MNW package', divider='rainbow')

st.markdown("""
Four interactive plots are provided to allow you to investigate different aspects of the Multi-Node-Well (MNW) boundary in MODFLOW.

:blue[**🔵 PLOT 1 - Hydraulic heads in the MNW boundary**]:
Illustrates the additional drawdown in the well due to lower cell-to-well conductance CWC. Two parameter sets for the CWC can be used.

:green[**🟢 PLOT 2 - Q-h behavior of the MNW boundary**]: An interactive plot of the Q-h relationship for the specified groundwater discharge ($Q$-$h_{gw}$) and the well discharge ($Q$-$h_{well}$) which may be reduced depending on physical conditions.

:red[**🔴 PLOT 3 - Q-h behavior for the groundwater head under consideration of a withdrawal well with thresholds**]: Illustrates the effect of thresholds on the simulated withdrawal rate.

:orange[**🟡 PLOT 4 - Q-h relationship for a well operated with a head target**]: Illustrates the situation where MNW computes the discharge based on a given head difference, e.g., to account for artesian free flowing wells.

_For all plots, the application includes toggles to:_
- turn the plots by 90 degrees,
- switch between number input or sliders.
""")

# --- One-time session init of the select box
if "session_init" not in st.session_state:
    st.session_state["session_init"] = True
    st.session_state["plot_choice"] = "🔵 Plot 1"
    
# Functions

# Define the nonlinear equation to solve: Q = Δh / (A + B + C * Q**(p-1))
def discharge_equation(Q, delta_h, A, B, C, p):
    return Q - delta_h / (A + B + C * Q**(p - 1))
    
# Callback function to update session state
def update_dh_show():
    st.session_state.dh_show = st.session_state.dh_show_input
def update_Q_show_neg():
    st.session_state.Q_show_neg = st.session_state.Q_show_input
def update_h_cell_slider():
    st.session_state.h_cell_slider = st.session_state.h_cell_slider_input
def update_h_cell_slider2():
    st.session_state.h_cell_slider2 = st.session_state.h_cell_slider2_input
def update_h_cell_slider4():
    st.session_state.h_cell_slider4 = st.session_state.h_cell_slider4_input
def update_h_lim():
    st.session_state.h_lim = st.session_state.h_lim_input
def update_h_lim4():
    st.session_state.h_lim4 = st.session_state.h_lim4_input
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
def update_Q_range():
    if "Q_range_input" in st.session_state:
        # from slider
        lo, hi = st.session_state.Q_range_input
    else:
        # from number inputs
        lo = st.session_state.Q_range_input_min
        hi = st.session_state.Q_range_input_max

    # clamp and order
    lo = max(0.0, min(lo, st.session_state.Q_show))
    hi = max(0.0, min(hi, st.session_state.Q_show))
    if lo > hi:
        lo, hi = hi, lo

    st.session_state.Q_range = (lo, hi)
    
# Initialize session state for value and toggle state
st.session_state.dh_show = 5.0
st.session_state.Q_show = 0.5
st.session_state.Q_show_neg = -0.5
st.session_state.h_cell_slider = 12.0
st.session_state.h_cell_slider2 = 10.0
st.session_state.h_cell_slider4 = 10.0
st.session_state.h_lim = 5.0
st.session_state.h_lim4 = 2.0
st.session_state.A = 5.0
st.session_state.B = 5.0
st.session_state.C = 0.0
st.session_state.P = 2.0
st.session_state.A2 = 5.0
st.session_state.B2 = 5.0
st.session_state.C2 = 5.0
st.session_state.P2 = 2.0
st.session_state.number_input = False  # Default to number_input
st.session_state.Q_range = (0.1 * st.session_state.Q_show, 0.3 * st.session_state.Q_show)

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
    if "plot_choice" not in st.session_state:
        st.session_state["plot_choice"] = "🔵 Plot 1"

    col_plot = st.columns((1,1,1), gap = 'small')              
    with col_plot[1]:
        plot_choice = st.selectbox( "**SELECT a plot to display:**", ["🔵 Plot 1", "🟢 Plot 2", "🔴 Plot 3", "🟡 Plot 4"], index=0, key="plot_choice")
        
    if plot_choice == '🔵 Plot 1':
        show_plot1 = True
        show_plot2 = False
        show_plot3 = False
        show_plot4 = False
        explanation = False
        instruction = False
    if plot_choice == '🟢 Plot 2':
        show_plot2 = True
        show_plot1 = False
        show_plot3 = False
        show_plot4 = False
        explanation = False
        instruction = False
        st.session_state.second = False
    if plot_choice == '🔴 Plot 3':
        show_plot3 = True
        show_plot1 = False
        show_plot2 = False
        show_plot4 = False
        explanation = False
        instruction = False
    if plot_choice == '🟡 Plot 4':
        show_plot4 = True
        show_plot1 = False
        show_plot2 = False
        show_plot3 = False
        explanation = False
        instruction = False
        st.session_state.second = False
    
    # INPUT SECTION
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    # Possible ToDo for later optimization: Remove the visualize flag - everything is visualize
    visualize = True
    
    st.markdown("""
       #### :rainbow[INPUT CONTROLS]
        """)
    # Switches
    columns1 = st.columns((1,1,1), gap = 'small')              
    
    with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="MNW_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number input.")
            #visualize = st.toggle(':rainbow[Visualize the input values', key="MNW_vis", value=True)
    
    with columns1[1]:
        with st.expander('Modify :blue[**Heads**]'):
            st.write('**:green[Target for evaluation/visualization]**')
            if show_plot3:
                h_target = False
            elif show_plot4:
                h_target = True
            else:
                h_target = st.toggle('Toggle for :blue[**Q-**] or :red[**H-**]target')

            if h_target:
                st.markdown(":red[**H-target**]")
                if show_plot4:
                    if st.session_state.number_input:
                        h_lim4 = st.number_input("**Well-/Limiting head** $h_{lim}$ [m]", 0.0, 10.0, st.session_state.h_lim4, 0.1, key="h_lim4_input", on_change=update_h_lim4)
                    else:
                        h_lim4 = st.slider      ("**Well-/Limiting head** $h_{lim}$ [m]", 0.0, 10.0, st.session_state.h_lim4, 0.1, key="h_lim4_input", on_change=update_h_lim4)  
                    if st.session_state.number_input:
                        h_cell_slider4 = st.number_input("**Groundwater head** $h_{gw}$ [m]", 10.0, 19.0, st.session_state.h_cell_slider4, 0.1, key="h_cell_slider4_input", on_change=update_h_cell_slider4)
                    else:
                        h_cell_slider4 = st.slider      ("**Groundwater head** $h_{gw}$ [m]", 10.0, 19.0, st.session_state.h_cell_slider4, 0.1, key="h_cell_slider4_input", on_change=update_h_cell_slider4)
                else:
                    if st.session_state.number_input:
                        dh_show = st.number_input("**Drawdown $$\Delta h$$** in withdrawal well", 0.01, 10.0, st.session_state.dh_show, 0.1, key="dh_show_input", on_change=update_dh_show)
                    else:
                        dh_show = st.slider      ("**Drawdown $$\Delta h$$** in withdrawal well", 0.01, 10.0, st.session_state.dh_show, 0.1, key="dh_show_input", on_change=update_dh_show)
            else:
                st.markdown(":blue[**Q-target**]")
                
                # Discrete negative options: −0.001, −0.002, …, −1.000
                Q_show_OPTIONS = [round(-i/1000, 3) for i in range(1, 1001)]
                if st.session_state.number_input:
                    Q_show_neg = st.number_input("**Withdrawal rate $Q$** in the well", -1.0, -0.001, st.session_state.Q_show_neg, 0.001, format="%.3f", key="Q_show_input", on_change=update_Q_show_neg)
                else:
                    Q_show_neg = st.select_slider("**Withdrawal rate $Q$** in the well", Q_show_OPTIONS, round(st.session_state.get("Q_show_neg", -0.100), 3), key="Q_show_input", on_change=update_Q_show_neg)
                Q_show = Q_show_neg * -1
#                if st.session_state.number_input:
#                    Q_show = st.number_input("**Withdrawal rate $Q$** in the well", 0.001, 1.0, st.session_state.Q_show, 0.001, key="Q_show_input", on_change=update_Q_show)
#                else:
#                    Q_show = st.slider      ("**Withdrawal rate $Q$** in the well", 0.001, 1.0, st.session_state.Q_show, 0.001, key="Q_show_input", on_change=update_Q_show)   
            if show_plot2:
                if st.session_state.number_input:
                    h_cell_slider2 = st.number_input("**Groundwater head** $h_{gw}$ [m]", 5.0, 15.0, st.session_state.h_cell_slider2, 0.1, key="h_cell_slider2_input", on_change=update_h_cell_slider2)
                else:
                    h_cell_slider2 = st.slider      ("**Groundwater head** $h_{gw}$ [m]", 5.0, 15.0, st.session_state.h_cell_slider2, 0.1, key="h_cell_slider2_input", on_change=update_h_cell_slider2)          
            if show_plot3:
                if st.session_state.number_input:
                    h_cell_slider = st.number_input("**Groundwater head** $h_{gw}$ [m]", 0.0, 20.0, st.session_state.h_cell_slider, 0.1, key="h_cell_slider_input", on_change=update_h_cell_slider)
                else:
                    h_cell_slider = st.slider      ("**Groundwater head** $h_{gw}$ [m]", 0.0, 20.0, st.session_state.h_cell_slider, 0.1, key="h_cell_slider_input", on_change=update_h_cell_slider)
                if st.session_state.number_input:
                    h_lim = st.number_input("**Limiting head** $h_{lim}$ [m]", 0.0, 10.0, st.session_state.h_lim, 0.1, key="h_lim_input", on_change=update_h_lim)
                else:
                    h_lim = st.slider      ("**Limiting head** $h_{lim}$ [m]", 0.0, 10.0, st.session_state.h_lim, 0.1, key="h_lim_input", on_change=update_h_lim)                 
                th = st.toggle("Apply withdrawal thresholds")
                if th:
#                    Q_range = st.slider("Discharge cutoff range $[Q_{mn}, Q_{mx}]$ [m³/s]", 0.0, st.session_state.Q_show, (0.1*st.session_state.Q_show, 0.3*st.session_state.Q_show), 0.01)
#                    Q_mn, Q_mx = Q_range       
                     if st.session_state.number_input:
                         # two number_inputs, grouped
                         col1, col2 = st.columns(2)
                         with col1:
                             st.number_input("Discharge cutoff min $Q_{mn}$ [m³/s]", 0.0, st.session_state.Q_show, st.session_state.Q_range[0], 0.01, key="Q_range_input_min",  on_change=update_Q_range)
                         with col2:
                             st.number_input("Discharge cutoff max $Q_{mx}$ [m³/s]", 0.0, st.session_state.Q_show, st.session_state.Q_range[1], 0.01, key="Q_range_input_max", on_change=update_Q_range)
                         Q_mn, Q_mx = st.session_state.Q_range
                     else:
                         Q_range = st.slider("Discharge cutoff range $[Q_{mn}, Q_{mx}]$ [m³/s]", 0.0, st.session_state.Q_show, st.session_state.Q_range, 0.01, key="Q_range_input", on_change=update_Q_range)
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
                A = st.number_input("", 0.001, 10.0, st.session_state.A, 0.05, key="A_input", on_change=update_A, label_visibility="collapsed")
            with columns4[1]:
                B = st.number_input("", 0.001, 10.0, st.session_state.B, 0.05, key="B_input", on_change=update_B, label_visibility="collapsed")
            with columns4[2]:
                C = st.number_input("", 0.00, 10.0, st.session_state.C, 0.05, key="C_input", on_change=update_C, label_visibility="collapsed")
            with columns4[3]:
                P = st.number_input("", 1.0, 4.0,   st.session_state.P, 0.05, key="P_input", on_change=update_P, label_visibility="collapsed")
        else:
            with columns4[0]:
                A = st.slider      ("", 0.001, 10.0, st.session_state.A, 0.05, key="A_input", on_change=update_A, label_visibility="collapsed")
            with columns4[1]:
                B = st.slider      ("", 0.001, 10.0, st.session_state.B, 0.05, key="B_input", on_change=update_B, label_visibility="collapsed")        
            with columns4[2]:
                C = st.slider      ("", 0.00, 10.0, st.session_state.C, 0.05, key="C_input", on_change=update_C, label_visibility="collapsed")   
            with columns4[3]:
                P = st.slider      ("", 1.0, 4.0,   st.session_state.P, 0.05, key="P_input", on_change=update_P, label_visibility="collapsed")
        
        if st.session_state.second:
            st.write('**:red[Dataset 2]** (A, B, C, P)')
            columns5 = st.columns((1,1,1,1))
            if st.session_state.number_input:
                with columns5[0]:
                    A2 = st.number_input("", 0.001, 10.0, st.session_state.A2, 0.05, key="A2_input", on_change=update_A2, label_visibility="collapsed")
                with columns5[1]:
                    B2 = st.number_input("", 0.001, 10.0, st.session_state.B2, 0.05, key="B2_input", on_change=update_B2, label_visibility="collapsed")
                with columns5[2]:
                    C2 = st.number_input("", 0.00, 10.0, st.session_state.C2, 0.05, key="C2_input", on_change=update_C2, label_visibility="collapsed")
                with columns5[3]:
                    P2 = st.number_input("", 1.0, 4.0,   st.session_state.P2, 0.05, key="P2_input", on_change=update_P2, label_visibility="collapsed")
            else:
                with columns5[0]:
                    A2 = st.slider      ("", 0.001, 10.0, st.session_state.A2, 0.05, key="A2_input", on_change=update_A2, label_visibility="collapsed")
                with columns5[1]:
                    B2 = st.slider      ("", 0.001, 10.0, st.session_state.B2, 0.05, key="B2_input", on_change=update_B2, label_visibility="collapsed")        
                with columns5[2]:
                    C2 = st.slider      ("", 0.00, 10.0, st.session_state.C2, 0.05, key="C2_input", on_change=update_C2, label_visibility="collapsed")   
                with columns5[3]:
                    P2 = st.slider      ("", 1.0, 4.0,   st.session_state.P2, 0.05, key="P2_input", on_change=update_P2, label_visibility="collapsed")        
    
    groundwater_thickness = 10.0
    
    # Input for visualization
    if visualize:
        if h_target:
            if show_plot4:
                #delta_head = dh_show4
                delta_head = 20
            else:
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
                
    #Define groundwater head range / Range of head differences Δh
    #delta_h_range = np.linspace(0.01, 10, 200)
    delta_h_range = np.linspace(-10, 20, 200)
    Q_values = []
    if st.session_state.second:
        delta_h_range2 = np.linspace(-10, 20, 200)
        Q_values2 = []
    
    # Solve for Q_n for each Δh
    for delta_h in delta_h_range:
        Q_initial_guess = abs(delta_h) / (st.session_state.A + st.session_state.B)  # reasonable initial guess
        Q_solution, = fsolve(discharge_equation, Q_initial_guess, args=(abs(delta_h), st.session_state.A, st.session_state.B, st.session_state.C, st.session_state.P))
        if delta_h>=0:
            Q_values.append(Q_solution)
        else:
            Q_values.append(-Q_solution)
    
    if st.session_state.second:
        for delta_h2 in delta_h_range2:
            Q_initial_guess2 = abs(delta_h2) / (st.session_state.A2 + st.session_state.B2)  # reasonable initial guess
            Q_solution2, = fsolve(discharge_equation, Q_initial_guess2, args=(abs(delta_h2), st.session_state.A2, st.session_state.B2, st.session_state.C2, st.session_state.P2))
            if delta_h2>=0:
                Q_values2.append(Q_solution2)
            else:
                Q_values2.append(-Q_solution2)
  
       
    # ------------------   
    # FIRST PLOT
    
    #with st.expander("Show / Hide the Discharge-Drawdown relationship for the MNW boundary", expanded = True):
    if show_plot1:
        st.subheader('🔵 Plot 1', divider = 'blue')
        st.markdown("""
        :blue[**Plot 1**: Withdrawal and drawdown in a well.] This figure shows the relationship between **withdrawal rate _Q_**, and the resulting **drawdown**. Here, drawdown is the difference between the groundwater head and head in the well. Up to **two parameter sets of the CWC** can be considered. _For a model representing a field setting, the groundwater head varies with time depending on model parameters and boundary stresses such as other wells pumping, variable recharge, and stream seepage. Here, one value of head is assigned to the model cell and calculations are made for parameter variations assuming that groundwater head is constant._
        """)
            
        label_head_axis = "Head difference $\Delta h = h_{gw} - h_{Well}$ (m) "
        label_flow_axis = "Withdrawal rate $Q$ (m³/s)"
        if visualize:
            # PLOT HERE - Create side-by-side plots
            fig, (ax_schematic, ax_plot) = plt.subplots(1, 2, figsize=(8, 5), width_ratios=[1, 3])
            fig.subplots_adjust(wspace=0.5)  # Increase horizontal space between ax_schematic and ax_plot
            
            # --- LEFT AXIS: Schematic view (Groundwater head vs Well head) ---
            schematic_width = 1.0
            # Groundwater: full height blue rectangle
            ax_schematic.add_patch(plt.Rectangle((0.0, 0), schematic_width*0.5, groundwater_thickness, color='skyblue'))
            ax_schematic.add_patch(plt.Rectangle((0.6, 0), schematic_width*0.5, groundwater_thickness, color='skyblue'))
            # Well water level: narrower grey rectangle, Head level indicators (dashed lines) and Labels wellls
            if st.session_state.second and not h_target:
                ax_schematic.add_patch(plt.Rectangle((0.50, delta_head),  schematic_width * 0.05, 10-delta_head, color='darkblue'))
                ax_schematic.add_patch(plt.Rectangle((0.55, delta_head2), schematic_width * 0.05, 10-delta_head2, color='red'))
                ax_schematic.plot([0.55, 1.7], [delta_head2, delta_head2], 'k--', linewidth=1, color='red')
                ax_schematic.text(1.85, delta_head2 - 0.1, 'Well \nhead 2', color='red', fontsize=12)
            else:
                ax_schematic.add_patch(plt.Rectangle((0.5, delta_head), schematic_width * 0.1, 10-delta_head, color='darkblue'))
        
            # Head level indicators (dashed lines) and Labels Groundwater and Well 1
            ax_schematic.plot([0.5, 1.7], [delta_head, delta_head], 'k--', linewidth=1, color='darkblue')
            ax_schematic.text(0.85, delta_head - 0.1, 'Well \nhead 1', color='darkblue', fontsize=12)
            ax_schematic.plot([0.0, 1.7], [0, 0], 'b--', linewidth=1)
            ax_schematic.text(0.5, 0 - 0.2, 'Groundwater (cell) \nhead', color='blue', fontsize=12)
            # Style
            ax_schematic.set_xlim(0, 2)
            ax_schematic.set_ylim(10, 0)
            ax_schematic.axis('off')
            
            # --- RIGHT AXIS: Q vs Δh plot ---
            # Values related to Q are negative to indicate pumping from the groundwater
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
                    ax_plot.plot([-Q_show, -Q_show], [groundwater_thickness, h_line], linestyle='dotted', color='grey', linewidth=2)
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
                st.write(':blue[***CWC1***] (in m²/s) = %5.2f' %((st.session_state.A + st.session_state.B + st.session_state.C * Q_show**(st.session_state.P - 1))**-1))
                if st.session_state.second:
                    st.write(':red[**Discharge $Q2$ to the well**] (in m³/s) = %5.3f' %Q_show2)
                    st.write(':red[***CWC2***] (in m²/s) = %5.2f' %((st.session_state.A2 + st.session_state.B2 + st.session_state.C2 * Q_show2**(st.session_state.P2 - 1))**-1))
            else:
                st.write(':grey[**Discharge to the well**] (in m³/s) = %5.3f' %Q_show)
                st.write(':blue[**Drawdown $$\Delta h$$ in the well**] (in m) = %5.2f' %delta_head)
                st.write(':blue[***CWC1***] (in m²/s) = %5.2f' %((st.session_state.A + st.session_state.B + st.session_state.C * Q_show**(st.session_state.P - 1))**-1))
                if st.session_state.second:
                    st.write(':red[**Drawdown $$\Delta h2$$ in the well**] (in m) = %5.2f' %delta_head2)
                    st.write(':red[***CWC2***] (in m²/s) = %5.2f' %((st.session_state.A2 + st.session_state.B2 + st.session_state.C2 * Q_show2**(st.session_state.P2 - 1))**-1))
    
        # --- PLOT 1 EXPLANATION ---  
        with st.expander('Click here to read more :blue[**About this Plot**]', icon ="📑"):
            st.markdown("""
            #### :blue[🔎 About this Plot]
            
            This plot illustrates the relationship between discharge and drawdown (the difference between the groundwater head ($h_{gw}$) and the well head ($h_{well}$)), using the Multi-Node Well (MNW)  package to represent a withdrawal well.
            
            It allows for exploration of two operating modes:
            1. :blue[**Q-target**] (defined discharge): Calculates the resulting drawdown for a given withdrawal rate.
            2. :red[**H-target**] (defined drawdown): Calculates the discharge required to maintain a specified drawdown (e.g., to avoid reaching a threshold head in the well that would reduce, or stop, withdrawal).
            
            The interactive plot is shown in two side-by-side images:
            - On the **right**, the Q–Δh curve shows how head loss varies with withdrawal rate.
            - On the **left**, a schematic illustrates the difference between $h_{gw}$ and $h_{well}$ (drawdown) in relationship to the withdrawal rate $Q$.
            
            Users can modify the **cell-to-well conductance (CWC)**, defined via the parameters $A$, $B$, $C$, and the exponent $P$, and compare two configurations to better understand how well losses (linear and nonlinear) influence the character of the relationship.
            
            """)
            
        # Expander with "open in new tab"
        DOC_FILE1 = "Q_h_plot_MNW_instructions1.md"
        with st.expander('Click here for :blue[**Instructions To Get Started with this Plot**]', icon ="🧪"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE1}")
            st.markdown(read_md(DOC_FILE1))
    
        # Expander with "open in new tab"
        DOC_FILE2 = "Q_h_plot_MNW_exercise1.md"    
        with st.expander('Click here for an :blue[**Exercise About this Plot**]', icon ="🧩"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE2}")
            st.markdown(read_md(DOC_FILE2))  

        # --- EXERCISE 1 ASSESSMENT ---        
        def content_exer1_mnw():
            st.markdown("""#### 🧠 Exercise assessment for plot 1""")
            st.info("These questions test your understanding after doing the MNW plot 1 exercise.")
            
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
                    
        # Render exercise assessment
        render_toggle_container(
            section_id="mnw_02",
            label="✅ **Show the :rainbow[**EXERCISE**] assessment about plot 1** - to self-check your understanding",
            content_fn=content_exer1_mnw,
            default_open=False,
        )
    
    # ------------------   
    # SECOND PLOT
    
    if show_plot2:
        st.subheader('🟢 Plot 2', divider = 'green')
        st.markdown("""
        :green[**Plot 2**: Relationship between discharge (_Q_), heads (_h_), and drawdown as function of CWC]. The plot shows the **_Q-h_-relationship** for an MNW withdrawal well. Additionally, the relationship between discharge and hydraulic head in a well relative to the head in the groundwater (drawdown) is presented as function of the CWC.
        """)
 
        if visualize:   
            # --- CONSTANT DISCHARGE PLOT ---
            h_2nd = np.linspace(0, 20, 20)
            Q_2nd = np.ones_like(h_2nd) * Q_show * -1
            h_cell = h_cell_slider2
            h_well = h_cell - delta_head
            # Change sign to account for the MODFLOW convention of negative sign for discharge
            Q_values_2nd = [-1 * q for q in Q_values]
            
            # Interpolate Q at h_lim using the Q(h_well) relation
            Q_interp = interp1d(h_cell - delta_h_range, Q_values, kind='linear', fill_value="extrapolate")
            h_well_range = h_cell - delta_h_range  # h_cell is fixed (currently set to 10)
            
            # --- Plot Q vs. h_well ---
            fig2, ax2 = plt.subplots(figsize=(6,6), dpi=150)
            if turn:
                ax2.plot(Q_2nd, h_2nd, color='blue', label=fr"$Q$-$h_{{gw}}$ plot with $Q = {Q_show * -1:.2f}$ m³/s", linewidth=2)
                ax2.plot(Q_values_2nd, h_well_range, color='black', linewidth=3, label=r"$Q$-$h_{Well}$")
                ax2.axhline(y=h_cell, linestyle='dotted', color='dodgerblue', linewidth=2)
                ax2.axhline(y=h_well, linestyle='dotted', color='grey', linewidth=2)
                ax2.set_ylabel("Hydraulic head $h$ [L]", fontsize=14)
                ax2.set_xlabel("Flow Into the Ground-Water System \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14)
                ax2.set_xlim(-1, 1)
                ax2.set_ylim(0, 20)
                if visualize:
                    ax2.text(0.85, h_cell+0.7, "$h_{gw}$", va='center',color='dodgerblue',  fontsize=14)
                    ax2.text(0.60, h_well+0.7, "$h_{well}$", va='center',color='black',  fontsize=14)
                    ax2.plot(Q_show*-1, h_cell,'o', markersize=12, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'head in cell = {h_cell:.2f} m')
                    ax2.plot(Q_show*-1, h_well,'o', markersize=10, markerfacecolor='none', markeredgecolor='darkblue', label=f'head in well = {h_well:.2f} m')    
            else:
                ax2.plot(h_2nd, Q_2nd, color='blue', label=fr"$Q$-$h_{{gw}}$ plot with $Q = {Q_show * -1:.2f}$ m³/s", linewidth=2)
                ax2.plot(h_well_range, Q_values_2nd, color='black', linewidth=3, label=r"$Q$-$h_{Well}$")
                ax2.axvline(x=h_cell, linestyle='dotted', color='dodgerblue', linewidth=2)
                ax2.set_xlabel("Hydraulic head $h$ [L]", fontsize=14)
                ax2.set_ylabel("Flow Into the Ground-Water System \nfrom the MNW boundary $Q_{MNW}$ (m³/s)", fontsize=14)
                ax2.set_ylim(-1, 1)
                ax2.set_xlim(0, 20)
                if visualize:
                    ax2.plot(h_cell, Q_show*-1, 'o', markersize=12, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'head in cell = {h_cell:.2f} m')
                    ax2.plot(h_well, Q_show*-1, 'o', markersize=10, markerfacecolor='none', markeredgecolor='darkblue', label=f'head in well = {h_well:.2f} m')
            
            ax2.set_title("Q-h Behavior for the MNW Boundary", fontsize=16, pad=20)
            ax2.tick_params(axis='both', labelsize=12)        
            ax2.legend(fontsize=14, loc='upper center', bbox_to_anchor=(0.5, -0.22), borderaxespad=0, ncol = 2)
            
            columns_fig2=st.columns((1,8,1))
            with columns_fig2[1]:
                st.pyplot(fig2, bbox_inches='tight')    
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Visualize the results]** to see this plot')
            
            
        # --- PLOT 2 EXPLANATION ---  
        with st.expander('Click here to read more :green[**About this Plot**]', icon ="📑"):
            st.markdown("""
            #### :green[🔎 About this Plot]
            
            This plot illustrates the relationship between **well head ($h_{well}$)** and **discharge (Q)** for a **specified groundwater head ($h_{gw}$)** in a Multi-Node Well (MNW). 
            
            Two modes are available:
            1. :blue[**Q-target**]: Where you can specify the discharge and calculate the resulting $h_{well}$ (drawdown) for a given conductance (initially set to $1.0$).
            2. :red[**H-target**]: Where you specify $h_{well}$ and compute the discharge resulting from head difference and conductance.
            
            Unlike the MODFLOW well (WEL) or recharge (RCH) boundaries that impose a fixed flow, and unlike RIV or DRN boundaries that assume **linear head-dependent flow**, MNW simulates **nonlinear resistance** due to turbulence that results from high flow velocity or well construction effects. This is controlled by the **cell-to-well conductance (CWC)**, defined by parameters $A$, $B$, $C$, and $P$.
            
            The groundwater head ($h_{gw}$) can be modified for this plot although its value has no effect on the relationship between discharge and well head. Rather, a change in groundwater head shifts the plot vertically on the graph.
            """)
            
        # Expander with "open in new tab"
        DOC_FILE3 = "Q_h_plot_MNW_instructions2.md"
        with st.expander('Click here for :green[**Instructions To Get Started with this Plot**]', icon ="🧪"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE3}")
            st.markdown(read_md(DOC_FILE3))
    
        # Expander with "open in new tab"
        DOC_FILE4 = "Q_h_plot_MNW_exercise2.md"    
        with st.expander('Click here for an :green[**Exercise About this Plot**]', icon ="🧩"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE4}")
            st.markdown(read_md(DOC_FILE4))  

        # --- EXERCISE 2 ASSESSMENT ---  
        def content_exer2_mnw():
            st.markdown("""#### 🧠 Exercise assessment for plot 2""")
            st.info("These questions test your understanding after doing the MNW plot 2 exercise.")
            
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
                    
        # Render exercise assessment
        render_toggle_container(
            section_id="mnw_03",
            label="✅ **Show the :rainbow[**EXERCISE**] assessment about plot 2** - to self-check your understanding",
            content_fn=content_exer2_mnw,
            default_open=False,
        )        
      
    # ------------------   
    # THIRD PLOT HERE - Q vs h_cell (with head and discharge thresholds)
    
    #with st.expander('Show the MNW boundary with varying groundwater heads'):  
    if show_plot3:
        st.subheader('🔴 Plot 3', divider = 'red')
        st.markdown("""
        :red[**Plot 3**: _Q-h_-Relationship for a withdrawal well with thresholds.] This plot demonstrates the effect of a limiting head that restricts the withdrawal rate _Q_.
        """)
        
        if visualize:
            # Plotting range
            h_3rd = np.linspace(0, 20, 300)

            # Computation of values to show in the plots - Currently only working with Q_target; head_target needs to be implemented for the second parameter set
            
            # Compute head difference assuming h_well stays at threshold if h_cell < h_lim
            delta_h_adjusted = np.clip(h_3rd - h_lim, 0, None)
            h_well = h_cell_slider - delta_head
            
            # Take the discharge that relates to the adjusted delta_h, define a function to interpolate
            Q_interp_func  = interp1d(delta_h_range, Q_values,  bounds_error=False, fill_value="extrapolate")
            
            # Use the interpolated value, but limit it to Q_show if it's larger
            Q_plot  = np.minimum(Q_interp_func(delta_h_adjusted),  Q_show)
            if th:
                Q_plot_mn = np.where(Q_plot <= Q_mn, 0, Q_plot)
                Q_plot_mx = np.where(Q_plot <= Q_mx, 0, Q_plot)
            
            # Generate the point to show
            if h_well >= h_lim:
                delta_h_current = h_cell_slider - h_well
            else:
                delta_h_current = max(h_cell_slider - h_lim, 0)
                
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
            
            # Repeat computation for second parameter set
            if st.session_state.second:
                if h_target:
                    h_well2 = h_cell_slider - delta_head
                    Q_interp_func2 = interp1d(delta_h_range, Q_values2, bounds_error=False, fill_value="extrapolate")
                    Q_plot2 = np.minimum(Q_interp_func2(delta_h_adjusted), Q_show2)
                    # Generate the point to show
                    if h_well2 >= h_lim:
                        delta_h_current2 = h_cell_slider - h_well2
                    else:
                        delta_h_current2 = max(h_cell_slider - h_lim, 0)
                        
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
                    if h_well2 >= h_lim:
                        delta_h_current2 = h_cell_slider - h_well2
                    else:
                        delta_h_current2 = max(h_cell_slider - h_lim, 0)
                        
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
            fig3, ax3 = plt.subplots(figsize=(6,6), dpi=150)
            if turn:
                # if threshold is considered
                if th:
                    ax3.plot([-q for q in Q_plot], h_3rd, color='blue', linewidth=1, linestyle=':')
                    ax3.plot([-q for q in Q_plot_mn], h_3rd, color='blue', linewidth=4, label=r"$Q$-$h_{gw}$ with threshold")
                    ax3.plot([-q for q in Q_plot_mx], h_3rd, color='blue', linewidth=2, linestyle='--')       
                    if st.session_state.second:
                        ax3.plot([-q for q in Q_plot2], h_3rd, color='red', linewidth=1, linestyle=':', label=r"$Q$-$h_{gw}$ with threshold CWC2")   
                    ax3.axvline(x=-Q_show, linestyle='--', color='blue', linewidth=1, label=f'Desired $Q$ = {-Q_show:.3f} (m³/s)')
                    # Plot Q for legend entry
                    if h_well >= h_lim:
                        ax3.plot(-Q_dot_th, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_show:.3f} (m³/s)')
                    else:
                        ax3.plot(-Q_dot_th, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_dot_th:.3f} (m³/s)')                       
                else:                
                    ax3.plot([-q for q in Q_plot], h_3rd, color='blue', linewidth=4, label=r"$Q$-$h_{gw}$ with threshold")       
                    if st.session_state.second:
                        ax3.plot([-q for q in Q_plot2], h_3rd, color='red', linewidth=2, linestyle=':', label=r"$Q(h_{gw})$ with threshold CWC2")
                    ax3.axvline(x=-Q_show, linestyle='--', color='blue', linewidth=1, label=f'Desired $Q$ = {-Q_show:.3f} (m³/s)')
                    # Plot Q for legend entry
                    if h_well >= h_lim:
                        ax3.plot(-Q_dot, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_show:.3f} (m³/s)')
                    else:
                        ax3.plot(-Q_dot, h_cell_slider, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_dot:.3f} (m³/s)')  
                ax3.axhline(y=h_cell_slider, linestyle='--', color='dodgerblue', linewidth=2, label=f'$h_{{gw}}$ = {h_cell_slider:.2f} m')  
                if h_well >= h_lim:
                    ax3.axhline(y=h_well, linestyle='--', color='grey', linewidth=2, label=f'$h_{{well}}$ = {h_well:.2f} m')
                    # Arrow for flow
                    ax3.annotate(
                    '',  # no text
                    xy=(-Q_dot,h_well),  # arrowhead
                    xytext=(-Q_dot,h_cell_slider),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='blue', lw=2,  alpha=0.8, mutation_scale=15)
                    )
                else:
                    if h_cell_slider < h_lim:
                        ax3.axhline(y=h_cell_slider, linestyle='--', color='grey', linewidth=2, label=f'$h_{{well}}$ = {h_cell_slider:.2f} m')
                    else: 
                        ax3.axhline(y=h_lim, linestyle='--', color='grey', linewidth=2, label=f'$h_{{well}}$ = {h_lim:.2f} m')
                        # Arrow for flow
                        if th:
                            ax3.annotate(
                            '',  # no text
                            xy=(-Q_dot_th,h_lim),  # arrowhead
                            xytext=(-Q_dot_th,h_cell_slider),  # arrow start
                            arrowprops=dict(arrowstyle='-|>', color='tomato', lw=2,  alpha=0.8, mutation_scale=15)
                            )
                        else:
                            ax3.annotate(
                            '',  # no text
                            xy=(-Q_dot,h_lim),  # arrowhead
                            xytext=(-Q_dot,h_cell_slider),  # arrow start
                            arrowprops=dict(arrowstyle='-|>', color='tomato', lw=2,  alpha=0.8, mutation_scale=15)
                            )
                ax3.axhline(y=h_lim, linestyle='--', color='orange', linewidth=2, label=f'$h_{{lim}}$ = {h_lim:.2f} m')      
                # Add head annotations
                if h_cell_slider < h_lim:
                    ax3.text(-0.63, h_cell_slider+0.7, "$h_{gw}$ =", va='center',color='dodgerblue',  fontsize=14)
                else:
                    ax3.text(-0.63, h_cell_slider+0.7, "$h_{gw}$", va='center',color='dodgerblue',  fontsize=14)
                
                if h_well >= h_lim:
                    ax3.text(-0.74, h_well+0.7, "$h_{well}$", va='center',color='grey',  fontsize=14)
                else:
                    if h_cell_slider < h_lim:
                        ax3.text(-0.74, h_cell_slider+0.7, " $h_{well}$", va='center',color='grey',  fontsize=14)
                    else:
                        ax3.text(-0.74, h_lim+0.7, " $h_{well}$ = ", va='center',color='grey',  fontsize=14)
                ax3.text(-0.92, h_lim+0.7, "$h_{lim}$",  va='center',color='red', fontsize=14)                        
                
                ax3.set_xlabel("Withdrawal rate $Q$ (m³/s)", fontsize=14)
                ax3.set_ylabel("Hydraulic heads $h$ (m)", fontsize=14)
                ax3.set_xlim(0.05, -1)
                ax3.set_ylim(0, 20)
            else:
                # if threshold is considered
                if th:
                    ax3.plot(h_3rd, [-q for q in Q_plot], color='blue', linewidth=1, linestyle=':')
                    ax3.plot(h_3rd, [-q for q in Q_plot_mn],  color='blue', linewidth=4, label=r"$Q$-$h_{gw}$ with threshold")
                    ax3.plot(h_3rd, [-q for q in Q_plot_mx],  color='blue', linewidth=4, linestyle='--')
                    if st.session_state.second:
                        ax3.plot(h_3rd, [-q for q in Q_plot_th], color='red', linewidth=1, linestyle=':', label=r"$Q$-$h_{gw}$ with threshold CWC2")
                    ax3.axhline(y=-Q_show, linestyle='--', color='blue', linewidth=1, label=f'Desired $Q$ = {-Q_show:.3f} (m³/s)')
                    # Plot Q for legend entry
                    if h_well >= h_lim:
                        ax3.plot(h_cell_slider,-Q_dot_th, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_show:.3f} (m³/s)')
                    else:
                        ax3.plot(h_cell_slider, -Q_dot_th, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_dot_th:.3f} (m³/s)')         
                else:
                    ax3.plot(h_3rd, [-q for q in Q_plot], color='blue', linewidth=4, label=r"$Q$-$h_{gw}$ with threshold")
                    if st.session_state.second:
                        ax3.plot(h_3rd, [-q for q in Q_plot2], color='red', linewidth=2, linestyle=':', label=r"$Q(h_{gw})$ with threshold")
                    ax3.axhline(y=-Q_show, linestyle='--', color='blue', linewidth=1, label=f'Desired $Q$ = {-Q_show:.3f} (m³/s)')
                    # Plot Q for legend entry
                    if h_well >= h_lim:
                        ax3.plot(h_cell_slider, -Q_dot, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_show:.3f} (m³/s)')
                    else:
                        ax3.plot(h_cell_slider, -Q_dot, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_dot:.3f} (m³/s)')
                ax3.axvline(x=h_cell_slider, linestyle='--', color='dodgerblue', linewidth=2, label=f'$h_{{gw}}$ = {h_cell_slider:.2f} m')
                if h_well >= h_lim:
                    ax3.axvline(x=h_well, linestyle='--', color='grey', linewidth=2, label=f'$h_{{well}}$ = {h_well:.2f} m')
                    # Arrow for flow
                    ax3.annotate(
                    '',  # no text
                    xy=(h_well,-Q_dot),  # arrowhead
                    xytext=(h_cell_slider,-Q_dot),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='blue', lw=2,  alpha=0.8, mutation_scale=15)
                    )
                else:
                    if h_cell_slider < h_lim:
                        ax3.axvline(x=h_cell_slider, linestyle='--', color='grey', linewidth=2, label=f'$h_{{well}}$ = {h_cell_slider:.2f} m')
                    else: 
                        ax3.axvline(x=h_lim, linestyle='--', color='grey', linewidth=2, label=f'$h_{{well}}$ = {h_lim:.2f} m')
                        # Arrow for flow
                        if th:
                            ax3.annotate(
                            '',  # no text
                            xy=(h_lim,-Q_dot_th),  # arrowhead
                            xytext=(h_cell_slider,-Q_dot_th),  # arrow start
                            arrowprops=dict(arrowstyle='-|>', color='tomato', lw=2,  alpha=0.8, mutation_scale=15)
                            )
                        else:
                            ax3.annotate(
                            '',  # no text
                            xy=(h_lim,-Q_dot),  # arrowhead
                            xytext=(h_cell_slider,-Q_dot,),  # arrow start
                            arrowprops=dict(arrowstyle='-|>', color='tomato', lw=2,  alpha=0.8, mutation_scale=15)
                            )
                ax3.axvline(x=h_lim, linestyle='--', color='orange', linewidth=2, label=f'$h_{{lim}}$ = {h_lim:.2f} m')
                # Add head annotations
                ax3.text(h_cell_slider+0.5, -0.75, "$h_{gw}$", va='center',color='dodgerblue',  fontsize=14)
                ax3.text(h_well+0.5, -0.85, "$h_{well}$", va='center',color='grey',  fontsize=14)
                ax3.text(h_lim+0.5, -0.95, "$h_{lim}$",  va='center',color='red', fontsize=14)     
                
                ax3.set_xlabel("Hydraulic heads $h$ [m]", fontsize=14)
                ax3.set_ylabel("Discharge $Q$ [m³/s]", fontsize=14)
                ax3.set_xlim(0, 20)
                ax3.set_ylim(0.05, -1)
            
            ax3.set_title("Q-h Behavior for the MNW Boundary with Threshold", fontsize=16, pad=20)
            ax3.tick_params(axis='both', labelsize=12)
            #ax3.legend(fontsize=14, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
            ax3.legend(fontsize=14, loc='upper center', bbox_to_anchor=(0.5, -0.22), borderaxespad=0, ncol = 2)
            
            columns_fig3=st.columns((1,10,1))
            with columns_fig3[1]:
                st.pyplot(fig3, bbox_inches='tight') 
            
            st.markdown("""
                _The arrow in the plot indicates the head difference :blue[$h_{well}-h_{gw}$] or :orange[$h_{lim}-h_{gw}$] and points to the resulting flow $Q$._
            """)
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Visualize the results]** to see this plot')

        # --- PLOT 3 EXPLANATION ---  
        with st.expander('Click here to read more :red[**About this Plot**]', icon ="📑"):
            st.markdown("""
            #### :red[🔎 About this Plot]
            
            This plot illustrates the **_Q–h_-relationship of a Multi-Node Well (MNW)** under conditions where a **threshold head** is imposed so that the model does not allow withdrawal to continue at a rate greater than can be produced in the field. 
            
            The groundwater head ($h_{gw}$) and the discharge ($Q$) define the well head ($h_{well}$) through the nonlinear **cell-to-well conductance (CWC)** equation (as discussed in the Theory section above).
                      
            If the computed well head falls **below the defined threshold head**, the withdrawal rate is automatically **reduced** such that the well head is held at the threshold. This mechanism mimics a pump protection strategy to avoid dry wells or pump damage due to excessive drawdown.
            
            The MNW behavior is also constrained by rate thresholds that reflect practical limitations of typical pumps:
            - **Qmn** – the lower limit of the pump capacity, when reached, the well will be shut off in the model simulation
            - **Qmx** – the calculated discharge rate that triggers a switched-off pump to switch back on
            
            This plot helps visualize:
            - When the **threshold becomes active**
            - How **withdrawal is limited** to protect the well
            - The nonlinear relationship between Q and $h_{well}$ under withdrawal-limited conditions for various CWC parameters

            """)
            
        # Expander with "open in new tab"
        DOC_FILE5 = "Q_h_plot_MNW_instructions3.md"
        with st.expander('Click here for :red[**Instructions To Get Started with this Plot**]', icon ="🧪"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE5}")
            st.markdown(read_md(DOC_FILE5))
    
        # Expander with "open in new tab"
        DOC_FILE6 = "Q_h_plot_MNW_exercise3.md"    
        with st.expander('Click here for an :red[**Exercise About this Plot**]', icon ="🧩"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE6}")
            st.markdown(read_md(DOC_FILE6))  

        # --- EXERCISE 3 ASSESSMENT ---      
        def content_exer3_mnw():
            st.markdown("""#### 🧠 Exercise assessment for plot 3""")
            st.info("These questions test your understanding after doing the MNW plot 3 exercise.")
            
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
                    
        # Render exercise assessment
        render_toggle_container(
            section_id="mnw_04",
            label="✅ **Show the :rainbow[**EXERCISE**] assessment about plot 3** - to self-check your understanding",
            content_fn=content_exer3_mnw,
            default_open=False,
        )
        
# ------------------   
    # Fourth PLOT HERE - Q vs h_cell (head-target)
    
    #with st.expander('Show the MNW boundary with varying groundwater heads'):  
    if show_plot4:
        st.subheader('🟡 Plot 4', divider = 'orange')
        st.markdown("""
        :orange[**Plot 4**: _Q-h_-Relationship for a well operated by a head target.] This plot demonstrates computation of the discharge _Q_ for a head target.
        """)
        
        if visualize:
            # Plotting range
            h_4th = np.linspace(0, 20, 300)
            
            # Compute head difference assuming h_well stays at threshold if h_cell < h_lim
            delta_h_adjusted = np.clip(h_4th - h_lim4, 0, None)
            h_well = h_cell_slider4 - delta_head
            
            # Take the discharge that relates to the adjusted delta_h, define a function to interpolate
            Q_interp_func  = interp1d(delta_h_range, Q_values,  bounds_error=False, fill_value="extrapolate")
            
            # Use the interpolated value, but limit it to Q_show if it's larger
            Q_plot  = np.minimum(Q_interp_func(delta_h_adjusted),  Q_show)
            
            # Generate the point to show
            if h_well >= h_lim4:
                delta_h_current = h_cell_slider4 - h_well
            else:
                delta_h_current = max(h_cell_slider4 - h_lim4, 0)
                
            Q_dot = min(Q_interp_func(delta_h_current), Q_show)                          
            
           
            # --- CREATE THE 4RD PLOT ---
            fig4, ax4 = plt.subplots(figsize=(6,6), dpi=150)
            if turn:               
                ax4.plot([-q for q in Q_plot], h_4th, color='black', linewidth=4, label=r"$Q$-$h_{gw}$ for a well with drawdown $h_{well}-h_{gw}$")       
                # Plot Q and Empty line for legend entry                       
                ax4.plot(-Q_dot, h_cell_slider4, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue',  label=f'Current $Q$ = {-Q_dot:.3f} (m³/s)')
                ax4.axhline(y=h_cell_slider4, linestyle='--', color='dodgerblue', linewidth=2, label=f'$h_{{gw}}$ = {h_cell_slider4:.2f} m')
                ax4.axhline(y=h_lim4, linestyle='--', color='orange', linewidth=2, label=f'$h_{{well}}$ = $h_{{lim}}$ = {h_lim4:.2f} m')   
                
                #Arrow indicating head difference and Q
                ax4.annotate(
                '',  # no text
                xy=(-Q_dot,h_lim4),  # arrowhead
                xytext=(-Q_dot,h_cell_slider4),  # arrow start
                arrowprops=dict(arrowstyle='-|>', color='dodgerblue', lw=2,  alpha=0.8, mutation_scale=15)
                )
                # Add head annotations
                ax4.text(-1.80, h_cell_slider4+0.7, "$h_{gw}$", va='center',color='dodgerblue',  fontsize=14)
                ax4.text(-2.20, h_lim4+0.7, " $h_{well}$ = ", va='center',color='grey',  fontsize=14)
                ax4.text(-2.70, h_lim4+0.7, "$h_{lim}$",  va='center',color='red', fontsize=14)                        
                
                ax4.set_xlabel("Withdrawal rate $Q$ (m³/s)", fontsize=14)
                ax4.set_ylabel("Hydraulic heads $h$ (m)", fontsize=14)
                ax4.set_xlim(0.05, -3)
                ax4.set_ylim(0, 20)
            else:     
                ax4.plot(h_4th, [-q for q in Q_plot], color='black', linewidth=4, label=r"$Q$-$h_{gw}$ for a well with drawdown $h_{well}-h_{gw}$")
                # Plot Q and Empty line for legend entry
                ax4.plot(h_cell_slider4, -Q_dot, 'o', markersize=10, markerfacecolor='dodgerblue', markeredgecolor='darkblue', label=f'Current $Q$ = {-Q_dot:.3f} (m³/s)')
                ax4.axvline(x=h_cell_slider4, linestyle='--', color='dodgerblue', linewidth=2, label=f'$h_{{gw}}$ = {h_cell_slider4:.2f} m')
                ax4.axvline(x=h_lim4, linestyle='--', color='orange', linewidth=2, label=f'$h_{{well}}$ = $h_{{lim}}$ = {h_lim4:.2f} m')
                ax4.annotate(
                '',  # no text
                xy=(h_lim4,-Q_dot),  # arrowhead
                xytext=(h_cell_slider4,-Q_dot),  # arrow start
                arrowprops=dict(arrowstyle='-|>', color='dodgerblue', lw=2,  alpha=0.8, mutation_scale=15)
                )
                # Add head annotations
                ax4.text(h_cell_slider4+0.5, -2.20, "$h_{gw}$", va='center',color='dodgerblue',  fontsize=14)
                ax4.text(h_lim4+0.5, -2.50, "$h_{well}$", va='center',color='grey',  fontsize=14)
                ax4.text(h_lim4+0.5, -2.70, "$h_{lim}$\n =",  va='center',color='red', fontsize=14)     
                
                ax4.set_xlabel("Hydraulic heads $h$ [m]", fontsize=14)
                ax4.set_ylabel("Discharge $Q$ [m³/s]", fontsize=14)
                ax4.set_xlim(0, 20)
                ax4.set_ylim(0.05, -3)
            
            ax4.set_title("Q-h Behavior for the MNW Boundary with head target", fontsize=16, pad=20)
            ax4.tick_params(axis='both', labelsize=12)
            #ax4.legend(fontsize=14, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
            ax4.legend(fontsize=14, loc='upper center', bbox_to_anchor=(0.5, -0.22), borderaxespad=0)
            
            columns_fig4=st.columns((1,10,1))
            with columns_fig4[1]:
                st.pyplot(fig4, bbox_inches='tight') 
        else:
            st.write('Activate the visualization with the toggle **:rainbow[Visualize the results]** to see this plot')

        # --- PLOT 4 EXPLANATION ---  
        with st.expander('Click here to read more :orange[**About this Plot**]', icon ="📑"):
            st.markdown("""
            #### :orange[🔎 About this Plot]
            
            This plot illustrates the **_Q–h_-relationship of a Multi-Node Well (MNW)** operated with a head-target. Example applications include planning of pumping capacity to lower the groundwater head to a specific target level in order to dewater for construction of a foundation, tunnel, or mine. A further example could be the representation of an artesian flowing well. The limiting head $h_{lim}$ acts as the controlling (boundary) head for the well, instead of as a limit imposed to protect the well pump which was demonstrated in Plot 3. Groundwater flows to the well when the groundwater head $h_{gw}$ exceeds $h_{lim}$ and the resulting discharge $Q$ is computed by MNW under consideration of the specified _Cell-to-well_ conductance _CWC_.
            
            In this plot the desired discharge $Q_{des}$ is set artificially high such that MNW computes the resulting discharge under the constraint of the limiting head (i.e., as _constrained_ discharge; you may find it useful to work with plot 3 of this section if you have not done so yet).
            
            Accordingly, the groundwater head ($h_{gw}$), well head ($h_{well}$), and limiting head ($h_{lim}$) define the discharge ($Q$) through the **cell-to-well conductance (CWC)** equation (as discussed in the Theory section above) by using parameters (A,B,C,P) that represent head loss for flow through the aquifer as well as linear and nonlinear loss of head between the hydrostratigraphic unit and the well.
            
            This plot helps visualize:
            - How **discharge can be computed** under consideration of a **defined head target**;
            - How **free-flow discharge** is computed for an artesian flowing aquifer;
            - The nonlinear relationship between Q and $h_{well}$ under withdrawal-limited conditions for various CWC parameters
            - How $h_{lim}$ limits the head difference and thus limits $Q$
            """)
            
        # Expander with "open in new tab"
        DOC_FILE7 = "Q_h_plot_MNW_instructions4.md"
        with st.expander('Click here for :orange[**Instructions To Get Started with this Plot**]', icon ="🧪"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE7}")
            st.markdown(read_md(DOC_FILE7))
    
        # Expander with "open in new tab"
        DOC_FILE8 = "Q_h_plot_MNW_exercise4.md"    
        with st.expander('Click here for an :orange[**Exercise About this Plot**]', icon ="🧩"):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE8}")
            st.markdown(read_md(DOC_FILE8))  
            
        # --- EXERCISE 4 ASSESSMENT --- 
        def content_exer4_mnw():
            st.markdown("""#### 🧠 Exercise assessment for plot 4""")
            st.info("These questions test your understanding after doing the MNW plot 4 exercise.")
            
            # Render questions in a 2x3 grid (row-wise)
            for row in [(0, 1), (2, 3), (4, 5)]:
                col1, col2 = st.columns(2)
        
                with col1:
                    i = row[0]
                    st.markdown(f"**Q{i+1}. {quest_plot4[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot4[i]["options"],
                        success=quest_plot4[i].get("success", "✅ Correct."),
                        error=quest_plot4[i].get("error", "❌ Not quite.")
                    )
        
                with col2:
                    i = row[1]
                    st.markdown(f"**Q{i+1}. {quest_plot4[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_plot4[i]["options"],
                        success=quest_plot4[i].get("success", "✅ Correct."),
                        error=quest_plot4[i].get("error", "❌ Not quite.")
                    )
                    
        # Render exercise assessment
        render_toggle_container(
            section_id="mnw_05",
            label="✅ **Show the :rainbow[**EXERCISE**] assessment about plot 4** - to self-check your understanding",
            content_fn=content_exer4_mnw,
            default_open=False,
        )

Q_h_plot()

st.subheader('✔️ Conclusion', divider = 'rainbow')
st.markdown("""
The Multi-Node Well (MNW) boundary in MODFLOW adds realism to well simulations by distributing flow across multiple model cells and introducing operational and physical constraints. This boundary goes beyond fixed withdrawal rates by simulating **head-dependent flow**, **skin effects**, and **withdrawal limits** — key factors in models properly representing wells in physical settings. An MNW boundary can be defined in any groundwater-model cell.

Q–h plots allow exploration of how MNW behavior transitions from active withdrawal, to constraint-induced reduction of flow, to cessation of flow. Understanding these conditions supports better interpretation, calibration, and reliability in groundwater modeling projects.

There are two MNW boundary condition packages for MODFLOW, MNW1 and MNW2. The MNW2 boundary is an enhanced version of MNW1. MNW2 includes the option for well discharge to be limited based on both the lift (i.e., the elevation difference between the pump and the water level in the well) and the pump characteristics as addressed in this module. The MNW1 package allows for wells to extend through more than one groundwater-model cell but does not include flow reduction. Flow into or out of any particular cell in a multi-node well depends on the head in the well, the head in the cell, and a conductance calculated using various factors describing the well hydraulics.

After studying this section about multi-node-well boundaries, you may want to evaluate your knowledge using the final assessment.
""")

# --- FINAL ASSESSMENT ---
def content_final_mnw():
    st.markdown("""#### 🧠 Final assessment""")
    st.info("These questions test your conceptual understanding after working with the application.")
    
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
            
# Render final assessment
render_toggle_container(
    section_id="mnw_06",
    label="✅ **Show the final assessment** - to self-check your **understanding**",
    content_fn=content_final_mnw,
    default_open=False,
)
            
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
