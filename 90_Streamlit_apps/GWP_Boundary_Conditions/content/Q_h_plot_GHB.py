import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy.special
import scipy.interpolate as interp
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_Boundary_Conditions_utils import read_md

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

# Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# path to questions for the assessments (direct path)
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_ghb.json"
path_quest_exer = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_ghb.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_ghb.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)
    
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

st.title("Theory and Concept of the :orange[General Head Boundary (GHB) in MODFLOW]")
#st.subheader("Interaction Between Groundwater and Head-Dependent Boundaries", divider="orange")
st.subheader("Groundwater - :orange[Head-Dependent Boundary] interaction", divider="orange")

st.markdown("""
#### 💡 Motivation: Why use General Head Boundaries?
""")

columns0 = st.columns((1,1), gap = 'large')

with columns0[0]:
    st.markdown(""" 
    Before jumping into equations and applications, consider:
    
    1. **How would you represent a distant river or lake that interacts with groundwater but lies outside your model domain?**
    2. **Can a boundary sometimes add and other times remove water from the groundwater system — depending on heads?**
    
    ▶️ The :orange[**General Head Boundary (GHB)**] addresses these situations. It allows for dynamic, head-dependent exchange with an external water body. The following introductory interactive plot illustrates how the flow $Q_B$ depends on the groundwater head $h_{gw}$ for a fixed boundary head $H_B$ and conductance $C_B$. The interactive plot is based on the MODFLOW documentation (Harbaugh, 2005) and assumes that the boundary head **$H_B$ is 8 m**. Try modifying the conductance $C_B$ to explore its effect.
    """)
    
    st.latex(r'''Q_B = C_B(H_B - h_{gw})''')

# Initial plot
# fixed values
HBi = 8.0

# Initialize session state for value and toggle state
st.session_state.Ci_slider_value = -2.5
if "Ci_GHB" not in st.session_state:
    st.session_state.Ci_GHB = 3e-3

with columns0[1]:
    # Conductance
    labels, default_label = prep_log_slider(default_val = 3e-3, log_min = -4, log_max = -1)
    selected_Ci = st.select_slider("**Conductance :orange[$C_B$]** in m²/s", labels, default_label, key = "GHB_Ci")
    st.session_state.Ci_GHB = float(selected_Ci)
    
    # Define groundwater head range
    h_aqi = np.linspace(0, 20, 200)
    Qi = st.session_state.Ci_GHB * (HBi - h_aqi)

    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, Qi, color='black', linewidth=4)
    ax.set_xlabel("Head in the groundwater system (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow into the groundwater \nfrom the GHB $Q_{B}$ (m³/s) \nwith boundary head $H_{B}$ = 8 m", fontsize=14, labelpad=15)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    ax.set_title("Flow Between Groundwater and GHB", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)
    
    st.markdown("""
    **Initial Plot** for exploring how changes in :orange[GHB conductance] changes flow at the boundary.
    
    This **initial plot** is designed to bridge the gap between traditional $Q$-$h$ plots on paper and the :rainbow[**interactive plots**] provided further down in this app, that allow you to explore the $Q$-$h$ relationships more intuitively, supported by interactive controls and guided instructions.
    """)

st.markdown("""
####  💻 How GHB may be Applied in Field-Scale Groundwater Modeling

The GHB package is particularly relevant in applied groundwater modeling at the field scale, especially in settings with large water bodies that can provide water to, or receive water from, the groundwater system without significant change in the surface elevation of the water body. Regardless of the physical feature that a GHB represents, mathematically it will supply, or receive, any amount of water that is calculated during the simulation, but the head in the water body will not change. Therefore, it is important to ensure that the simulated volumetric flow rate is reasonable given the nature of the boundary in the field.
""")

left_co, cent_co, last_co = st.columns((10,40,10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied0_2.png', caption="A GHB provides connection to a source or sink external to the model domain.")
    
left_co, cent_co, last_co = st.columns((10,40,10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBexampleAnderson-etal_modified2.png', caption="Mathematical illustration of a GHB (modified from Anderson et al., 2015).")

st.markdown("""A GHB differs from other head-dependent flow boundaries in that the relation between flow across the boundary and calculated head in the aquifer is continuously linear and there is no limit on the magnitude of flow that can occur.
""")

with st.expander("Tell me more about **the :orange[application of GHB in Field-Scale Groundwater Modeling]**"):
    st.markdown("""
    In field-scale groundwater models, a GHB may represent a variety of physical features and be associated with one or many cells. These cells can be anywhere within the three-dimensional model.
    
    A GHB might be used to represent a significant body of water external to the model domain with the bottom of its sediment layer deep enough that the groundwater level is never below its bottom. 
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied1.png', caption="GHB representation of a lake. All the cells intersecting the lake have GHBs.")
    
    st.markdown("""     
    Or, a GHB boundary might be used to represent inflow from an adjacent aquifer. The head represents head at a location far enough away that it is not expected to change in response to stress on the simulated aquifer. The head in the adjacent aquifer might be maintained by seepage from water bodies or areal recharge. The important point is not what maintains that distant head but rather that modelers use this technique to provide inflow from a region that is not simulated in the grid.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied2.png', caption="GHB representation of inflow from an area outside of the model domain.")


    st.markdown("""
     Alternatively, a GHB could be used to represent inflow, or leakage, from an underlying aquifer. Leakage varies spatially in the model depending on the head in the simulated aquifer. For example, leakage from the underlying aquifer would increase in areas of heavy pumpage in the shallow aquifer.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied3.png', caption="GHB representation of leakage from an underlying aquifer.")


st.markdown("""
#### 🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual function and mathematical formulation of a General Head Boundary (GHB).
- Apply the GHB equation $Q_B = C_B(H_B - h_{gw})$ to calculate boundary flows and determine flow direction.
- Evaluate how conductance, groundwater head, and boundary head jointly affect the groundwater–boundary exchange.
- Understand the simplicity of the GHB Q–h plot as compared with the Q–h plots of head-dependent boundaries with head constraints.
- Visualize groundwater exchange at the boundary (flow into or out of the model at the boundary).
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

st.subheader('🧪 Theory and Background', divider="orange")
st.markdown("""
The General Head Boundary (GHB), also referred to as the Head-Dependent Flux Boundary in MODFLOW, allows for a more realistic simulation of boundary conditions compared to specified head boundaries, as described below in **the Theory**, by enabling **exchange of water between the groundwater system and an external reservoir with a resistive lining**. In groundwater models, General Head Boundaries are used to simulate hydraulic interaction with external water bodies or groundwater zones adjacent to the model domain by specifying ("fixing") the head of the external feature. The conductance term determines how easily water can flow across the boundary.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
        GHB boundaries differ from specified head boundaries.  For **specified head boundaries, the groundwater head is specified at a node within the model domain** and flow in or out of the node depends on head in the surrounding nodes along with the conductance between those nodes and the specified head node. A **GHB is a connection of a model node to an external source or sink**. In the case of a GHB, the groundwater head of the model node changes during the model simulation and the value of head in the groundwater system then determines the flow rate and direction as described by the following linear relationship:
        
        $$
        Q_B = C_B(H_B - h_{gw})
        $$
        
        where:
        - $Q_B$ is the flow between the GHB and the groundwater system, defined as positive if it is directed into the groundwater system [L³/T]
        - $H_B$ is the boundary head [L], representing e.g., an external water level like a distant lake,
        - $C_B$ is the hydraulic conductance of the GHB-groundwater interconnection [L²/T], which encapsulates **geometry and material properties**, and
        - $h_{gw}$ is the head [L] in the groundwater model cell where the GHB boundary is active.
        
        The conductance is
        
        $$
        C_B = \\frac{K A_B}{L_B}
        $$
        
        where:
        - $K$: Hydraulic conductivity [L/T],
        - $A_B$: Cross-sectional area of the interconnection [L²],
        - $L_B$: Length of flow path between groundwater system and boundary [L].
        
        The following figure illustrates the setup.
        """)
        
    left_co, cent_co, last_co = st.columns((10,80,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHB.png', caption="Schematic of the GHB boundary (modified from McDonald and Harbaugh, 1988)")

st.subheader("📈 Interactive Plot and Exercise", divider="orange")
st.markdown("""
    The interactive plot shows how the flow $Q_B$ across a General Head Boundary depends on the difference between groundwater head ($h_{gw}$) and boundary head ($H_B$), and on the conductance ($C_B$). 
    
    Below, under INPUT CONTROLS, in the "Modify Plot Controls" drop-down menu, you can toggle to: 1) turn the plot 90 degrees – this different viewing orientation might help you interpret the results, 2) choose between slider or typed input to adjust the parameter values, and 3) increase the range of the $Q_B$ axis, then the plot is redrawn as soon as new values are entered. Under "Modify Head Elevations", you can adjust the value of groundwater head and GHB head. Finally, under "Modify the Conductance" you can toggle between entering direct conductance input or computing it from geometric and hydraulic properties.

    The interactive plot graphically displays the Q–h relationship. When the toggle to visualize input value is turned on, the plot includes a legend that displays all parameter values and an arrow that indicates the head difference $H_{B}$-$h_{gw}$ and points to the value of flow $Q_{GHB}$ on the axis. If the arrow is not shown, you might need to increase the Q range.
    
    - You can investigate the plot on your own, perhaps using some of the :blue[**INSTRUCTIONS**] provided below the plot to guide you.
    - A subsequent :rainbow[**EXERCISE**] invites you to use the interactive plot to investigate how the conductance value and the difference in head affect the boundary flux, as well as to interpret the physical meaning of the situation based on Q–h plots.
""")

# Functions

# Callback function to update session state
def update_C_GHB():
    """Handles both number input (float) and select_slider (str)"""
    raw_val = st.session_state.C_input
    if isinstance(raw_val, str):
        st.session_state.C_GHB = float(raw_val)  # from select_slider
    elif isinstance(raw_val, float):
        st.session_state.C_GHB = raw_val         # from number_input
def update_K_GHB():
    """Handles both number input (float) and select_slider (str)"""
    raw_val = st.session_state.K_input
    if isinstance(raw_val, str):
        st.session_state.K_GHB = float(raw_val)  # from select_slider
    elif isinstance(raw_val, float):
        st.session_state.K_GHB = raw_val         # from number_input
def update_LB():
    st.session_state.LB = st.session_state.LB_input
def update_AB():
    st.session_state.AB = st.session_state.AB_input
def update_HB():
    st.session_state.HB = st.session_state.HB_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.C_GHB = 3e-3
st.session_state.C_GHB_label = "3e-3"
st.session_state.K_GHB = 1e-4
st.session_state.K_GHB_label = "1e-4"
st.session_state.LB = 100.
st.session_state.AB = 1000.0
st.session_state.HB = 8.0
st.session_state.stage = 2.0
st.session_state.h_aq_show = 10.0
st.session_state.number_input = False  # Default to number_input
st.session_state.c_computed = False

# Main area inputs
@st.fragment
def Q_h_plot():
    
    st.markdown("""
       #### :orange[INPUT CONTROLS]
        """)
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    # Input widgets
    
    columns1 = st.columns((1,1,1), gap = 'small')
    
    with columns1[0]:
        with st.expander('Modify the **Plot Controls**'):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="GHB_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_B$, $H_B$, $A_B$, $L_B$, and $h_{gw}$.")
            relax_Q = st.toggle('Toggle to increase the Q-range shown by the plot')
            visualize = st.toggle(':rainbow[Visualize the input values]', key="GHB_vis", value=True)
            
    with columns1[1]:
        with st.expander('Modify :blue[**Head Elevations**]'):
            if st.session_state.number_input:
                HB = st.number_input(":green[**GHB head** $H_B$ (m)]", 5.0, 20.0, st.session_state.HB, 0.1, key="HB_input", on_change=update_HB)
            else:
                HB = st.slider      (":green[**GHB head** $H_B$ (m)]", 5.0, 20.0, st.session_state.HB, 0.1, key="HB_input", on_change=update_HB)
            if st.session_state.number_input:
                h_aq_show = st.number_input(":blue[**Groundwater head** $h_{gw}$ (m)]", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
            else:
                h_aq_show = st.slider      (":blue[**Groundwater head** $h_{gw}$ (m)]", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)            
            
    with columns1[2]:
        with st.expander('Modify the :orange[**Conductance**]'):
            # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
            c_computed = st.toggle('Toggle to compute conductance', key='c_computed')
            if st.session_state.c_computed:
                # LOG Slider/number input for K
                if st.session_state.number_input:
                    st.number_input("**Hydr. conductivity** $K_B$ (m/s)", 10**log_min1, 10**log_max1, st.session_state.K_GHB, get_step(st.session_state.K_GHB), format="%.2e", key="K_input", on_change=update_K_GHB)
                else:
                    labels, _ = prep_log_slider(default_val=1e-4, log_min=log_min1, log_max=log_max1)
                    # Ensure label string matches st.session_state.K_GHB
                    st.session_state.K_GHB_label = get_label(st.session_state.K_GHB, labels)
                    st.select_slider("**Hydr. conductivity** $K_B$ (m/s)", labels, value = st.session_state.K_GHB_label, key="K_input", on_change=update_K_GHB)
                if st.session_state.number_input:
                    LB = st.number_input("**GHB length** $L_B$ (m)", 1.0, 10000.0, st.session_state.LB, 1., key="LB_input", on_change=update_LB)
                else:
                    LB = st.slider      ("**GHB length** $L_B$ (m)", 1.0, 10000.0, st.session_state.LB, 1., key="LB_input", on_change=update_LB)
                if st.session_state.number_input:
                    AB = st.number_input("**GHB area** $A_B$ (m²)", 1.0, 100000.0, st.session_state.AB, 1., key="AB_input", on_change=update_AB)
                else:
                    AB = st.slider      ("**GHB area** $A_B$ (m²)", 1.0, 100000.0, st.session_state.AB, 1., key="AB_input", on_change=update_AB)
                st.session_state.C_GHB = st.session_state.K_GHB * st.session_state.AB / st.session_state.LB
            else:
                if st.session_state.number_input:
                    st.number_input("**Conductance** $C_B$ (m²/s)", 10**log_min1, 10**log_max1, st.session_state.C_GHB, get_step(st.session_state.C_GHB), format="%.2e", key="C_input", on_change=update_C_GHB)
                else:
                    labels, _ = prep_log_slider(default_val=3e-3, log_min=log_min1, log_max=log_max1)
                    # Ensure label string matches st.session_state.K_GHB
                    st.session_state.C_GHB_label = get_label(st.session_state.C_GHB, labels)
                    st.select_slider("**Conductance** $C_B$ (m²/s)", labels, value = st.session_state.C_GHB_label, key="C_input", on_change=update_C_GHB)
                # Update K_GHB_value based on computed values
                st.session_state.K_GHB = st.session_state.C_GHB * st.session_state.LB / st.session_state.AB

    
    # Define groundwater system head range
    h_aq = np.linspace(0, 20, 200)
    Q = st.session_state.C_GHB * (HB - h_aq)
    Q_ref = st.session_state.C_GHB * (HB - h_aq_show)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_B = C_B(H_B - h_{{gw}})$",color='orange', linewidth=3)
            ax.plot([], [], ' ', label=fr"$C_B$ = {st.session_state.C_GHB:.2e} m²/s")
            ax.plot([], [], ' ', label=fr"$Q_B$ = {Q_ref:.2e} m³/s")
            ax.axvline(0, color='black', linewidth=1)
            ax.axhline(HB, color='green', linewidth=2, linestyle='--', label=f'$H_B$ in m= {HB:.2f}')
            ax.axhline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{gw}}$ in m= {h_aq_show:.2f}')
            
            # Labels and formatting
            ax.set_ylabel("Heads in the GHB-Model System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into the Ground-Water System from the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            if relax_Q:
                ax.set_xlim(5,-5)
            else:
                ax.set_xlim(0.05, -0.05)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HB),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='green', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
            else:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HB),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='<|-', color='blue', lw=2.5, alpha=0.8, mutation_scale=15)
                )
            # Add gaining/losing stream annotations
            if relax_Q:
                ax.text(-0.3,1, "Flow OUT of the model", va='center',color='green',  fontsize=16)
                ax.text(0.2, 1,  "Flow INTO the model", va='center', ha='right',color='blue',  fontsize=16)
            else:
                ax.text(-0.003,1, "Flow OUT of the model", va='center',color='green',  fontsize=16)
                ax.text(0.002, 1,  "Flow INTO the model", va='center', ha='right',color='blue',  fontsize=16)
            # Add red rectangle if Q out of the plot
            if (Q_ref < -0.05 or Q_ref > 0.05) and not relax_Q:
                rect = Rectangle((min(0.05, -0.05), 0.0), abs(-0.05 - 0.05), 20.0, linewidth=5, edgecolor='red', facecolor='none')
                ax.add_patch(rect)
            elif (Q_ref < -5 or Q_ref > 5):
                rect = Rectangle((min(5, -5), 0.0), abs(-5 - 5), 20.0, linewidth=5, edgecolor='red', facecolor='none')
                ax.add_patch(rect)      
        else:
            ax.plot(h_aq, Q, label=rf"$Q_B = C_B(H_B - h_{{gw}})$",color='orange', linewidth=3)
            ax.plot([], [], ' ', label=fr"$C_B$ = {st.session_state.C_GHB:.2e} m²/s")
            ax.plot([], [], ' ', label=fr"$Q_B$ = {Q_ref:.2e} m³/s")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(HB, color='green', linewidth=2, linestyle='--', label=f'$H_B$ in m= {HB}')
            ax.axvline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{gw}}$ in m= {h_aq_show}')

            # Labels and formatting
            ax.set_xlabel("Heads in the GHB-Model System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into the Ground-Water System from the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            if relax_Q:
                ax.set_ylim(-5, 5)
            else:
                ax.set_ylim(-0.05, 0.05)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(HB, Q_ref),  # arrowhead
                    xytext=(h_aq_show, Q_ref),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='green', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
            else:
                ax.annotate(
                '',  # no text
                xy=(HB, Q_ref),  # arrowhead
                xytext=(h_aq_show, Q_ref),  # arrow start
                arrowprops=dict(arrowstyle='<|-', color='blue', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
            # Add gaining/losing stream annotations
            if relax_Q:
                ax.text(19.8, -0.3, "Flow OUT of the model", va='center', ha='right',color='green',  fontsize=16)
                ax.text(19.8, 0.3, "Flow INTO the model", va='center', ha='right',color='blue',  fontsize=16)
            else:
                ax.text(19.8, -0.003, "Flow OUT of the model", va='center', ha='right',color='green',  fontsize=16)
                ax.text(19.8, 0.003, "Flow INTO the model", va='center', ha='right',color='blue',  fontsize=16)
            # Add red rectangle if Q out of the plot
            if (Q_ref < -0.05 or Q_ref > 0.05) and not relax_Q:
                rect = Rectangle((0.0, min(0.05, -0.05)), 20.0, abs(-0.05 - 0.05), linewidth=5, edgecolor='red', facecolor='none')
                ax.add_patch(rect)  
            elif (Q_ref < -5 or Q_ref > 5):     
                rect = Rectangle((0.0, min(5, -5)), 20.0, abs(-5 - 5), linewidth=5, edgecolor='red', facecolor='none')
                ax.add_patch(rect)                 
    else:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_B = C_B(H_B - h_{{gw}})$, $C_B$ = {st.session_state.C_GHB:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_ylabel("Heads in the GHB Boundary-Groundwater System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05,-0.05)
        else:        
            ax.plot(h_aq, Q, label=rf"$Q_B = C_B(H_B - h_{{gw}})$, $C_B$ = {st.session_state.C_GHB:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_xlabel("Heads in the GHB Boundary-Groundwater System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
   
   # === SHARED FORMATTING === #        
    ax.set_title("Flow Between Groundwater and GHB", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    legend = ax.legend(loc="upper left", fontsize=14)
    # Mark Q_B in red if out of visible range
    if (Q_ref < -0.05 or Q_ref > 0.05):
        for text in legend.get_texts():
            if "$Q_B$" in text.get_text():
                text.set_color('red')
    
    st.pyplot(fig)
    
    if visualize:
        if ((Q_ref < -0.05 or Q_ref > 0.05) and not relax_Q) or (Q_ref < -5 or Q_ref > 5):
            st.markdown("""
            :red[_The green arrow, indicating the head difference $H_{B}$-$h_{gw}$ and pointing to the value of flow $Q_B$ on the axis, is out of the visible range for the plot. The value for $Q_B$ is still shown in the legend. A toggle in “Modify the Plot Controls” can be used to increase the range._]
            """)
        else:
            st.markdown("""
            _The :green[green arrow] indicates the head difference $H_{B}$-$h_{gw}$ and points to the value of flow $Q_B$ on the axis._
            """)
    
#    with st.expander('Show the :blue[**INSTRUCTIONS**]'):
#        st.markdown("""
#        **Getting Started with the Interactive Plot**
#        
#        Before starting the exercise, it is helpful to follow these steps to explore GHB behavior:
#    
#        **1) Start with $H_{B}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s**
#    
#        * Vary **groundwater head $h_{gw}$** and observe how **flow $Q_B$** changes in magnitude and direction.  
#        * Use the slider to vary $C_B$ and notice how the **slope of the $Q$–$h$ curve** changes.
#        * Toggle “Compute conductance” then enter values for $K$, $A_B$, and $L_B$ to calculate $C_B = \\frac{K A_B}{L_B}$ and notice how the **slope of the $Q$–$h$ curve** changes.
#        
#        **2) Consider the Role of Head-Dependent Boundaries in Applied Groundwater Modeling**
#        
#        Depending on the modeling objective, head-dependent boundaries like GHB can be considered in two different ways:
#        
#        **a) During Model Calibration or Setup:** Assume that the discharge is known from field data (so the recharge is determined by dividing the discharge by the surface area of the model) and the general head boundary is the only outlet of the model. Then, given head values in the groundwater system, the values of hydraulic conductivity and GHB conductance can be calibrated. **This situation is discussed in the introduction** and can be accessed by clicking on the **:red[📕 Introduction] button** on the left menu, then scrolling down and choosing **Show the :rainbow[interactive] plot for Scenario 1**, then scrolling down below the plot to open the :green[**Instructions**] and finally **scrolling down to Step 5a**.
#        
#        Another way to use a GHB head dependent boundary condition:
#        
#       **b) After the model is calibrated such that the hydraulic conductivity, recharge, and river bed conductance are specified:** If other outlets are added to the system (e.g., abstraction wells, drains) the heads in the model will be a result of all the model boundary conditions and parameter values. In consequence, the previously calibrated, and then specified, conductance will control how much of the recharge flows to the :orange[**GHB**] boundary. The discharge will also depend on the location and properties of the other outlets. Here we investigate this behavior for the :orange[**General Head Boundary GHB**]. Other head dependent boundaries like :violet[**RIV**] and :green[**DRN**] follow similar principles.
#           
#       The subsequent exercise is designed to help you build intuition for how GHB parameters control flow.  Feel free to further investigate the interactive plot on your own.
#       """)
    
    # Expander with "open in new tab"
    DOC_FILE = "Q_h_plot_GHB_instructions.md"
    with st.expander('Show the :blue[**INSTRUCTIONS**]'):
        st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE}")
        st.markdown(read_md(DOC_FILE))
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        
        st.markdown("""
        
        🎯 **Expected Learning Outcomes**
        
        Completion of this exercise helps you to:
        
        * Understand how GHB flux is driven by head difference and conductance.
        * Interpret Q–h plots in relation to hydrogeologic behavior.
        * Develop the ability to use this application for conceptual testing and scenario analysis.
       
        🛠️ **Instructions**
        
        Use the interactive GHB plot as follows:
        
        **1. Start with $H_{B}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s**
        * Vary the groundwater head ($h_{gw}$) from **5 m to 15 m**
        * Observe and describe how the flux ($Q$) changes
        * Record:
          * The sign of the flux for different $h_{gw}$ values
          * The value of $Q$ when $h_{gw}$ = $H_B$
        
        **2. Conductance Effect**
                
        * Start with $H_{B}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s
        * Choose three different conductance values (e.g., **3x10⁻², 3x10⁻³, and 3x10⁻⁴ m²/s**)
          * Cycle through the 3 conductance values a couple of times, noting the influence of conductance on the slope of the line and flow conditions
        * Choose one conductance value (e.g., **3x10⁻³ m²/s**) and three values of $H_B$ with increased and decreased values (e.g., **5, 9, and 20 m**)
          * Cycle through the 3 $H_B$ values a couple of times, noting the influence of conductance on the slope of the line and flow conditions
        
        **3. Realistic Scenarios**
        
        * Imagine a GHB represents a canal system connected to the groundwater system. The canal water level is 10 m.
        * Assume the groundwater head starts at 8 m.
        * Evaluate how much water would enter the groundwater system for:
          * A poorly connected canal (low conductance)
          * A well-connected canal (high conductance)
        * Consider the implications of your findings for water management 
        """)


Q_h_plot()

with st.expander('**Show the :rainbow[**EXERCISE**] assessment** - to self-check your understanding'):
    st.markdown("""
    #### 🧠 Exercise assessment
    These questions test your understanding after doing the GHB exercise.
    """)

    # Render questions in a 2x3 grid (row-wise)
    for row in [(0, 1), (2, 3), (4, 5)]:
        col1, col2 = st.columns(2)

        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_exer[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_exer[i]["options"],
                success=quest_exer[i].get("success", "✅ Correct."),
                error=quest_exer[i].get("error", "❌ Not quite.")
            )

        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_exer[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_exer[i]["options"],
                success=quest_exer[i].get("success", "✅ Correct."),
                error=quest_exer[i].get("error", "❌ Not quite.")
            )



st.subheader('✅ Conclusion', divider = 'orange')
st.markdown("""
The General Head Boundary (GHB) offers a flexible way to simulate interactions with external water bodies or regions not explicitly modeled — such as distant lakes, rivers, or adjacent groundwater systems. Its formulation as a **head-dependent boundary** enables both **inflow and outflow**, depending on the head difference between a groundwater-flow-model cell and its boundary. A GHB boundary can be defined in any groundwater-flow-model cell.

The GHB condition captures the essential physics of cross-boundary exchange using only a few parameters: the **boundary head**, **groundwater head**, and **conductance**, which reflects the geometry and hydraulic properties of the connection.

Analyzing **Q–h plots** facilitates understanding of how conductance controls the slope of the exchange curve and how head differences dictate the flow direction. This conceptual insight is essential for setting realistic boundary conditions in MODFLOW models.

Other boundary packages discussed in this module incorporate the concepts of head difference between the boundary and the groundwater system driving the direction of flow into or out of the system, with the magnitude of head difference and conductance controlling the flow rate. The GHB package is unique in that there are no constraints on the flow so the $Q$-$h$ plot is continuously linear.  All the other head-dependent-flow packages have head constraints causing discontinuous $Q$-$h$ plots. 

After studying this section about general head boundaries, you may want to evaluate your knowledge using the final assessment.
""")

with st.expander('**Show the :red[final assessment]** - to self-check your understanding'):
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
