import numpy as np
import matplotlib.pyplot as plt
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

# Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# path to questions for the assessments (direct path)
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_drn.json"
path_quest_exer =  "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_drn.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_drn.json"

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
    
st.title("Theory and Concept of the :green[Drain Boundary (DRN) in MODFLOW]")
st.subheader("Groundwater - :green[Drain] interaction", divider="green")

st.markdown("""
    #### 💡 Motivation: Why use Drain Boundaries?
    """)

columns0 = st.columns((1,1), gap='large')
with columns0[0]:
    st.markdown("""      
    Consider these questions:
    
    1. **How would you simulate a ditch, tile drain, or trench that only removes water from the groundwater when the water table is high enough to flow into the feature?**
    
    2. **What if you want to stop outflow when the groundwater falls below a certain elevation?** 
    
    3. **How can you allow a spring to develop when head in an unconfined aquifer rises to the ground surface?** 
    
    ▶️ The :green[**Drain (DRN) Boundary**] in MODFLOW is designed for such situations. It allows water to leave the groundwater compartment only if the head in the groundwater $h_{gw}$ exceeds the drain elevation $H_D$. In the drain package, **a drain can never provide inflow to a model**. _The Drain Return Package, DRT, can be used to return flow from a drain to another location in the groundwater system._ The outflow $Q_{D}$ is computed using the drain conductance $C_D$ as: """)
   
    st.latex(r'''Q_{D} = C_{D} (H_{D}-h_{gw})''')
    st.markdown("""The following introductory interactive plot is based on the MODFLOW documentation (Harbaugh, 2005) and assumes **$H_{D}$ is 8 m**. Try adjusting the drain conductance in the initial plot to explore how flow varies as a function of head in the groundwater system.
    """)
with columns0[1]:    
    # Slider input and plot
    # C_DRN
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
    labels, default_label = prep_log_slider(default_val = 3e-3, log_min = -4, log_max = -1)
    selected_Ci = st.select_slider("**Conductance :green[$C_{D}$]** in m²/s", labels, default_label, key = "DRN_Ci")
    st.session_state.Ci_DRN = float(selected_Ci)
# Computation 
HDi = 8 
h_gwi = np.linspace(0, 20, 200)
Qi = np.where(h_gwi >= HDi, st.session_state.Ci_DRN * (h_gwi - HDi)*-1, 0)

# Create the plot
with columns0[1]:
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_gwi, Qi, color='black', linewidth=4)
    ax.set_xlabel("Head in the groundwater system (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow into the groundwater \nfrom the DRN boundary $Q_{D}$ (m³/s) \nwith DRN elevation $H_{D}$ = 8 m", fontsize=14, labelpad=15)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    ax.set_title("Flow Between Groundwater and DRN", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)    
    
    st.markdown("""
        **Initial plot** for exploring how outflow varies with a change of the :green[drain conductance].
        
        _**"Flow into"** is from the perspective of the groundwater system. **Drain flow is always negative or zero** because it is flow leaving the system._

         This **initial plot** is designed to bridge the gap between traditional $Q$-$h$ plots on paper and the :rainbow[**interactive plots**] provided further down in this app, that allow you to explore the $Q$-$h$ relationships more intuitively, supported by interactive controls and guided instructions.
    """)
    

st.markdown("""
####  💻 How DRN may be Applied in Field-Scale Groundwater Modeling

The DRN package is particularly relevant in applied groundwater modeling at the field scale, especially in agricultural, construction, and mine settings where drains are an important part of the system.
""")
with st.expander("Tell me more about **the :green[application of DRN in Field-Scale Groundwater Modeling]**"):
	
    st.markdown("""
    In field-scale groundwater models a DRN may be associated with one or many cells, and these cells can be anywhere within the three-dimensional model.
    """)
    
    st.markdown("""
    A DRN boundary might be used to allow springs to form at the ground surface. When the water level declines, spring flow will decrease, eventually ceasing when the water level falls below the surface.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNspring1.png', caption="Illustration of water table rising above the ground surface because there is no mechanism to allow groundwater outflow.")
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNspring2.png', caption="Illustration of springs developing at the ground surface when the water table rises.")
    
    st.markdown("""
    A DRN boundary could be used to represent a swamp that might be dewatered at some time during model simulation. For example, in a groundwater model with a swamp that is viewed as a permanent feature of the system, the swamp could be represented by a general head boundary to allow flow into and out of the system.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNapplied1.png', caption="Illustration of a GHB boundary used to represent a swamp allowing exchange of water between the swamp and groundwater system.")
    
    st.markdown("""
     However, if the model is later used to simulate inflow to a new open pit mine, then continuing to represent the swamp with a GHB is unrealistic because this boundary condition allows an unlimited amount of water to flow from the swamp into the groundwater system and discharge in the mine pit.  
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNapplied2.png', caption="Illustration of a GHB boundary resulting in overestimation of mine inflow.")

    st.markdown("""
    However, if a drain is used to simulate the swamp, then once pumping at the mine causes the groundwater level to decline below the  bottom of the swamp, the swamp will dry up and the simulated flow at the mine will be a more realistic representation of the system.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNapplied3.png', caption="Illustration of a DRN representing a swamp such that it goes dry when groundwater levels decline.")
   
st.markdown("""
####  🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual role of the Drain (DRN) boundary in simulating groundwater discharge to drainage features such as tile drains, trenches, or natural depressions.
- Apply the analytical relationship $Q_{D} = C_D(H_D-h_{gw})$ to calculate boundary flows.
- Identify conditions under which the DRN boundary is active or inactive, and understand the role of the drain elevation in preventing inflow to groundwater and limiting outflow from groundwater.
- Evaluate the influence of groundwater head, drain elevation, and conductance on the magnitude of drainage.
- Interpret Q–h plots to analyze the linear and threshold-based behavior of the DRN boundary.
- Understand how the conductance term reflects the geometry and properties of the connection between the groundwater compartment and the drain system.
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
            
st.subheader('🧪 Theory and Background', divider="green")
st.markdown("""
Some groundwater models need to allow outflow of groundwater when the groundwater head reaches a specific elevation that might be the ground surface, a tunnel, a mine drift, or a drainage tile. How do we realistically represent a such a condition in a groundwater model?
""")

  
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    This app calculates the flow between a model and a drain (DRN) depending on the drain elevation $H_D$ and the conductance $C_D$ between the boundary and the groundwater. The following figure illustrates some examples of features that require use of the DRN boundary.""")
    
    left_co, cent_co, last_co = st.columns((10,80,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRN.png', caption="Schematic of the DRN boundary with (a) drain pipe buried in a backfilled ditch, and (b) an open drain at the ground surface (modified from McDonald and Harbaugh, 1988)")
    st.markdown("""
    The relationship between the amount of water that flows out of the groundwater system into the drain and the head in the groundwater is:
    """)
    
    st.latex(r'''Q_{D} = C_D (H_D-h_{gw})''')
    
    st.markdown("""
    where:
    - $Q_{D}$ is the flow from the groundwater into the drain [L³/T]
    - $H_D$ is the drain elevation (L),
    - $C_D$ is the drain conductance [L²/T], and
    - $h_{gw}$ is the head in the cell that interacts with the drain (L).
   
    If the groundwater head $h_{gw}$ is below the elevation of the drain, $H_{D}$, then there is no flow.
    
    """)
    
with st.expander('**Click here** to read how :green[**conductance is calculated**]'):
    st.markdown("""
    ### Calculating MODFLOW Drain Boundary Conductance
    """)
    
    st.markdown("""
    MODFLOW requires input of conductance.

    Conductance includes all terms of Darcy's Law except the head difference between the drain and the groundwater. 
    """)    
    st.latex(r'''Q_{DRN} = KA \frac{\Delta h}{M}''')
    
    st.latex(r'''C_{DRN} = KA \frac{1}{M} = KLW \frac{1}{M}''')

    st.markdown("""
    where: 

    - $K$ is hydraulic conductivity of the drain lining or "skin" [L/T]
    - $A$ is flow area of the drain that may be a rectangle or a cylinder (=$LW$) [L²]
    - $M$ is thickness of the resistive material around the drain (the distance over which the gradient is calculated) [L]
    """)
    
    left_co, cent_co, last_co = st.columns((10,80,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DrainConductance.png', caption="Schematic of the DRN boundary with labels indicating parameters used to calculate conductance (modified from McDonald and Harbaugh, 1988)")
    
    st.markdown("""
    $\Delta h$ is the difference between the drain head (which is the drain elevation because pressure is assumed to be atmospheric) and groundwater head.

    In general, MODFLOW calculates flow $Q$ with a conductance $C$ as
    """)
    st.latex(r'''Q = C \Delta h''')

st.subheader("Interactive Plot and Exercise", divider="green")
st.markdown("""
    The interactive plot illustrates how the flow $Q_{D}$ across a Drain Boundary is driven by the **difference between groundwater head** ($h_{gw}$) and **drain elevation** ($H_D$), while being scaled by the **drain conductance** ($C_{D}$). Flow only occurs when the groundwater head exceeds the drain elevation, meaning the boundary acts as a one-way outlet. 
    
    Below, under INPUT CONTROLS, in the **"Modify Plot Controls"** drop-down menu, you can adjust the limits and range of the plot, and also toggle to: 1) turn the plot 90 degrees – this different viewing orientation might help you interpret the results, 2) choose between slider or typed input to adjust the parameter values, and 3) visualize the input values, which helps to interpret the plot. Under :blue[**"Modify Head & Elevations"**], you can adjust the value of drain elevation and groundwater head. Finally, under :green[**"Modify Conductance"**] you can adjust the conductance value.

    The interactive plot includes a legend that provides the parameter values. It also graphically displays the $Q$-$h$ relationship, each parameter value, and an arrow that indicates the head difference $h_{gw}$-$H_{D}$ and points to the value of flow $Q_{D}$ on the axis.
    
    - You can investigate the plot on your own, perhaps using some of the :blue[**INSTRUCTIONS**] provided below the plot to guide you.
    - A subsequent :rainbow[**EXERCISE**] invites you to use the interactive plot to investigate how the conductance value and the difference in head affect the boundary flux, as well as to interpret the physical meaning of the situation based on Q–h plots, that is, when the drain is **active** or **inactive** and how this affects groundwater discharge.
""")


# Functions

# Callback function to update session state
def update_C_DRN():
    """Handles both number input (float) and select_slider (str)"""
    raw_val = st.session_state.C_input
    if isinstance(raw_val, str):
        st.session_state.C_DRN = float(raw_val)  # from select_slider
    elif isinstance(raw_val, float):
        st.session_state.C_DRN = raw_val         # from number_input
def update_HD():
    st.session_state.HD = st.session_state.HD_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_gw_show():
    st.session_state.h_gw_show = st.session_state.h_gw_show_input  
    
# Initialize session state for value and toggle state
st.session_state.C_DRN = 1e-2
st.session_state.C_DRN_label = "1e-2"
st.session_state.HD = 8.0
st.session_state.h_gw_show = 10.0
st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    st.markdown("""
       #### :green[INPUT CONTROLS]
        """)
    columns1 = st.columns((1,1,1), gap = 'small')
    # Switches
    with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="DRN_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_D$, $H_D$, and $h_{gw}$.")
            visualize = st.toggle(':rainbow[Visualize the input values]', key="DRN_vis", value=True)

    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Elevations**]'):
            if st.session_state.number_input:
                HD = st.number_input(":green[**Drain elevation** $H_D$ (m)]", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
            else:
                HD = st.slider      (":green[**Drain elevation** $H_D$ (m)]", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
            if st.session_state.number_input:
                h_gw_show = st.number_input(":blue[**Groundwater head** $h_{gw}$ (m)]", 0.0, 20.0, st.session_state.h_gw_show, 0.1, key="h_gw_show_input", on_change=update_h_gw_show)
            else:
                h_gw_show = st.slider      (":blue[**Groundwater head** $h_{gw}$ (m)]", 0.0, 20.0, st.session_state.h_gw_show, 0.1, key="h_gw_show_input", on_change=update_h_gw_show)
    
    with columns1[2]:
        with st.expander('Modify :green[**Conductance**]'):
            # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
            #C_RIV
            if st.session_state.number_input:
                st.number_input("**Conductance** $C_D$ (m²/s)", 10**log_min1, 10**log_max1, st.session_state.C_DRN, get_step(st.session_state.C_DRN), format="%.2e", key="C_input", on_change=update_C_DRN)
            else:
                labels, _ = prep_log_slider(default_val=1e-2, log_min=log_min1, log_max=log_max1)
                # Ensure label string matches st.session_state.K_GHB
                st.session_state.C_DRN_label = get_label(st.session_state.C_DRN, labels)
                st.select_slider("**Conductance** $C_D$ (m²/s)", labels, value = st.session_state.C_DRN_label, key="C_input", on_change=update_C_DRN)
    
    # Computation - Define groundwater head range
    h_gw = np.linspace(0, 20, 200)
    
    Q = np.where(h_gw >= HD, st.session_state.C_DRN * (HD - h_gw), 0)
    Q_ref = st.session_state.C_DRN * (HD - h_gw_show) if h_gw_show >= HD else 0   
        
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(Q, h_gw, label=rf"$Q_D = C_D(H_D-h_{{gw}})$",color='green', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            ax.axvline(0, color='black', linewidth=1)
            ax.axhline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m = {HD:.2f}')
            ax.axhline(h_gw_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{gw}}$ in m = {h_gw_show:.2f}')
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the DRN Boundary-Groundwater System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05, -0.05)
            ax.legend(loc="upper left", fontsize=14)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HD),  # arrowhead
                    xytext=(Q_ref, h_gw_show),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='blue', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
#            else:
#                ax.annotate(
#                    '',  # no text
#                    xy=(Q_ref,HD),  # arrowhead
#                    xytext=(Q_ref, h_gw_show),  # arrow start
#                    arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
#                )
            # Add gaining annotations
            if h_gw_show > HD:
                ax.text(-0.04*0.05,20*0.97, "Flow INTO the Drain", fontsize=16, va='center', color='blue')
            else:
                ax.text(-0.04*0.05,20*0.97, "Drain inactive", fontsize=16, va='center', color='red')  
        else:
            ax.plot(h_gw, Q, label=rf"$Q_D = C_D(H_D - h_{{gw}})$",color='green', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m = {HD:.2f}')
            ax.axvline(h_gw_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{gw}}$ in m = {h_gw_show:.2f}')
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the DRN Boundary-Groundwater System (m))", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
            ax.legend(loc="upper right", fontsize=14)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(HD, Q_ref),  # arrowhead
                    xytext=(h_gw_show, Q_ref),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='blue', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
            # Add gaining drn annotations
            if h_gw_show > HD:
                ax.text(0.5, -0.003, "Flow INTO the Drain", fontsize=16, va='center', color='blue')
            else:
                ax.text(0.5, -0.003, "Drain inactive", fontsize=16, va='center', color='red')
    else:
        if turn:
            ax.plot(Q, h_gw, label=rf"$Q_D = C_D(H_D - h_{{gw}})$",color='black', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the DRN Boundary-Groundwater System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(-0.05, 0.05)
            ax.legend(loc="upper left", fontsize=14)
        else:
            ax.plot(h_gw, Q, label=rf"$Q_D = C_D(H_D - h_{{gw}})$",color='black', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the DRN Boundary-Groundwater System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)            
            ax.legend(loc="upper right", fontsize=14)
    # === SHARED FORMATTING === #     
    ax.set_title("Flow Between Groundwater and DRN boundary", fontsize=16, pad=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    
    
    st.pyplot(fig)
    if visualize:
        st.markdown("""
        _The arrow in the plot indicates the head difference $H_{D}-h_{gw}$ and points to the resulting flow $Q_{D}$._
        """)
    st.markdown("""
        _* from the **perspective of inflow** into the groundwater, **drain flow is always negative** or zero because it is flow leaving the groundwater._
        """)
    
    with st.expander('Show the :blue[**INSTRUCTIONS**]'):
        st.markdown("""
        **Getting Started with the Interactive Plot**
        
       Before starting the exercise, it is helpful to follow these steps to explore DRN behavior:
        
       1. **Start with $H_{D}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s** 
        
        * Vary **groundwater head** $h_{gw}$ in steps between 6 and 12 m (if you prefer there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider).
        * Observe how the flow $Q_D$ changes:
            * When $h_{gw} > H_D$, the groundwater drains, that is flow leaves the groundwater through the drain.
            * When $h_{gw} \leq H_D$, no flow occurs because the drain is inactive.
            
       2. **Experiment with Different Conductance Values**
        
        * With $h_{gw} > H_D$, use the slider to vary $C_D$ and notice how the **slope of the Q–h curve** changes — higher conductance leads to stronger response of outflow to head differences.
        
        These steps help you build intuition for how DRN parameters govern flow — especially the **threshold behavior** and **linear relationship** between head difference and outflow. Feel free to further investigate the interactive plot on your own.
        """)
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        
        st.markdown("""   
        🎯 **Expected Learning Outcomes**
        
        Completion of this exercise helps you to:
        
        - Understand how drain–groundwater interaction is controlled by groundwater head, drain elevation, and conductance.
        - Interpret the boundary characteristics with a Q–h plot.
        - Recognize the threshold behavior of the DRN package and its role as a one-way boundary.
        - Evaluate how conductance controls the rate of drainage when groundwater head is above a threshold elevation.
        - Analyze realistic scenarios (e.g., excavation of a building foundation) and the implications for boundary fluxes.
        
        🛠️ **Instructions**
        
        Use the interactive DRN plot to complete the following steps:
        
        1. **Initial Exploration (hint: there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider)**
        
        * Start with $H_{D}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s
        * Vary the groundwater head ($h_{gw}$) from 8 m to 12 m and observe how the flow ($Q_D$) responds to changes in head
        
        Make a record of:
        
            * The threshold value at which the drain becomes active
            * The linearity of the Q–h relationship once the threshold is exceeded
            * Drain flow when groundwater head is less than the drain elevation

        2. **Effect of Conductance**
        * Start with $H_{D}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s
        * Choose three different conductance values (e.g., 1x10⁻², 1x10⁻³, and 1x10⁻⁴ m²/s)
          * For each of the 3 conductance values view the plot $Q_{D}$ vs $h_{gw}$ while adjusting $h_{gw}$ from 6 m to 12 m and note the influence of conductance on the slope of the line and the magnitude of flow.

        3. **Realistic Scenario: Excavating a building foundation**
        - Fix the groundwater head at 10.3 m
        - In 1-m steps, vary drain elevation from 9.3 m to 6.3 m, and make note of the flow rate to the drain
        - Consider this as a simplified representation of increasing inflow that needs to be collected and routed away from a construction site. A similar process might be used at a larger scale for an open-pit mine.
    
        💡 **Explore:**
        - How does flow to the drain change as the excavation deepens?
        - What would the construction company have to do to address the inflow?
        - What would reduce the inflow?
        - How might conductance be decreased on excavation walls?
        - How might surrounding groundwater heads be lowered?
        """)

Q_h_plot()

with st.expander('**Show the :rainbow[**EXERCISE**] assessment** - to self-check your understanding'):
    st.markdown("""
    #### 🧠 Exercise assessment
    These questions test your understanding after doing the exercise.
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

st.subheader('✅ Conclusion', divider = 'green')
st.markdown("""
The Drain (DRN) boundary condition simulates discharge to external drains, ditches, trenches, topographic depressions, mines, and other features where a hydrostratigraphic unit encounters an opening to atmospheric pressure conditions. Flow _only_ occurs when groundwater levels are at or above the opening elevation. This boundary introduces a **physical cutoff based on the drain elevation** that prevents outflow, making it conceptually different from other head-dependent boundaries. A DRN boundary can be defined in any groundwater-flow-model cell. It need not be defined in the surface layer, for example it might be defined deep inside a model to represent a tunnel or an underground mine. 

Analyzing **Q–h plots** allows exploration of how the discharge remains zero until the groundwater head exceeds the drain elevation, after which it increases linearly based on the conductance. This behavior supports the simulation of seepage faces and artificial drainage systems without over-extracting water from the model.

By adjusting parameters like drain **elevation** and **conductance**, modelers can explore how the discharge remains zero until the groundwater head exceeds the drain elevation, after which it increases linearly based on the conductance. This behavior supports the simulation of seepage faces, artificial drainage systems, and excavations without over-extracting water from the model. Understanding these behaviors through Q–h plots supports stronger conceptual models and more reliable groundwater–surface water integration.

A related boundary package is the drain return package (DRT) in which water is removed from the groundwater system just as it is in the DRN package, and some, or all, of that water can be returned to the groundwater system at specified locations. It is akin to having injection wells connected to the drain. The total rate of injection is limited by the rate of outflow from the groundwater system to the drain.

After studying this section about drain boundaries, you may want to evaluate your knowledge using the final assessment.
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
