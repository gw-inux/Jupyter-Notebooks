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
    Consider these two questions:
    
    1. **How would you simulate a ditch, tile drain, or trench that only removes water from the aquifer when the water table is high enough to flow into the feature?**
    
    2. **What if you want to stop outflow when the groundwater falls below a certain elevation?** 
    
    3. **How can you allow a spring to develop when head in an unconfined aquifer rises to the ground surface?** 
    
    ▶️ The :green[**Drain (DRN) Boundary**] in MODFLOW is designed for such situations. It allows water to leave the aquifer only if the head in the aquifer $h_{aq}$ exceeds the drain elevation $H_D$. **A drain can never provide inflow to a model**. (_The Drain Return Package (DRT) can be used when flow may occur from a drain into a model._) The outflow $Q_{D}$ is computed with the drain conductance $C_D$ as: """)
    
    st.latex(r'''Q_{D} = C_{D} (H_{D}-h_{aq})''')
with columns0[1]:    
    # Slider input and plot
    # C_DRN
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
    labels, default_label = prep_log_slider(default_val = 3e-3, log_min = -4, log_max = -1)
    selected_Ci = st.select_slider("**Conductance :green[$C_{D}$]** in m²/s", labels, default_label, key = "DRN_Ci")
    st.session_state.Ci_DRN = float(selected_Ci)
# Computation 
HDi = 8 
h_aqi = np.linspace(0, 20, 200)
Qi = np.where(h_aqi >= HDi, st.session_state.Ci_DRN * (h_aqi - HDi)*-1, 0)

# Create the plot
with columns0[1]:
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, Qi, color='black', linewidth=4)
    ax.set_xlabel("Head/Elevation in the DRN-aquifer system (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow into the groundwater \nfrom the DRN boundary $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    ax.set_title("Flow Between Groundwater and DRN", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)    
    
    st.markdown("""
        **Initial plot** for exploring how outflow varies with change of the :green[drain conductance].
        
        _* **"Flow into"** from the **perspective of inflow** into the groundwater, **drain flow is negative** or zero because it is flow leaving the groundwater._

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
    A DRN boundary might be used to represent a swamp that might be dewatered. For example, a groundwater model might have a swamp that is viewed as a permanent feature of the system and represented by a general head boundary to allow flow into and out of the system.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNapplied1.png', caption="Illustration of a GHB boundary used to represent a swamp allowing exchange of water between the swamp and groundwater system.")
    
    st.markdown("""
     At a later time, the model is used to simulate inflow to a new open pit mine. If the swamp continues to be represented by a GHB, it will not limit inflow and the model will predict large out flow to the mine pit that will need to be disposed of at the mine.  
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNapplied2.png', caption="Illustration of a GHB boundary resulting in overestimation of mine inflow.")

    st.markdown("""
    However, if a drain is used to simulate the swamp, then once pumping at the mine causes the groundwater level to decline below the  bottom of the swamp, the swamp will dry up and the simulated flow at the mine will be less as approrpiate for the system.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRNapplied3.png', caption="Illustration of a DRN representing a swamp such that it goes dry when groundwater levels decline.")
   
    
#TODO
st.markdown("""
####  🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual role of the Drain (DRN) boundary in simulating groundwater discharge to drainage features such as tile drains, trenches, or natural depressions.
- Apply the analytical relationship $Q_{D} = C_D(H_D-h_{aq})$ to calculate boundary flows.
- Identify conditions under which the DRN boundary is active or inactive, and understand the role of the drain elevation in preventing inflow and limiting outflow.
- Evaluate the influence of aquifer head, drain elevation, and conductance on the magnitude of drainage.
- Interpret Q–h plots to analyze the linear and threshold-based behavior of the DRN boundary.
- Understand how the conductance term reflects the geometry and properties of the connection between the aquifer and the drain system.
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
Some groundwater models need to allow outflow of groundwater when the aquifer head reaches a specific elevation that might be the ground surface, a tunnel, a mine drift, or a drainage tile. How do we realistically represent a such a condition in a groundwater model?
""")

  
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    This app calculates the flow between a model and a drain (DRN) depending on the drain elevation $H_D$ and the conductance $C_D$ between the boundary and the aquifer. The following figure illustrates some examples of features that require use of the DRN boundary.""")
    
    left_co, cent_co, last_co = st.columns((10,80,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/DRN.png', caption="Schematic illustration of the DRN boundary with a) drain pipe buried in a backfilled ditch, and b) an open drain at the ground surface; modified from (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")
    st.markdown("""
    The relationship between the amount of water that flows out of the groundwater system into the drain and the head in the aquifer is:
    """)
    
    st.latex(r'''Q_{D} = C_D (H_D-h_{aq})''')
    
    st.markdown("""
    where:
    - $Q_{D}$ is the flow from the aquifer into the drain [L³/T]
    - $H_D$ is the drain elevation (L),
    - $C_D$ is the drain conductance [L²/T], and
    - $h_{aq}$ is the head in the cell that interacts with the drain (L).
   
    If the aquifer head $h_{aq}$ is below the elevation of the drain, $H_{D}$, then there is no flow.
    
    """)

st.subheader("Interactive Plot and Exercise", divider="green")
st.markdown("""
    The interactive plot illustrates how the flow $Q_{D}$ across a Drain Boundary is driven by the **difference between aquifer head** ($h_{aq}$) and **drain elevation** ($H_D$), while being scaled by the **drain conductance** ($C_{D}$). Flow only occurs when the aquifer head exceeds the drain elevation, meaning the boundary acts as a one-way outlet. 
    
    Below, under INPUT CONTROLS, in the **"Modify Plot Controls"** drop-down menu, you can adjust the limits and range of the plot, and also toggle to: 1) turn the plot 90 degrees, 2) choose between slider or typed input to adjust the parameter values, and 3) make the plot "live" to switch from the static plot to the interactive plot. Under :blue[**"Modify Head & Elevations"**], you can adjust the value of river head, riverbed bottom elevation, and aquifer head. Finally, under :green[**"Modify Conductance"**] you can toggle between direct conductance input or computing it from geometric and hydraulic properties. The plot updates dynamically and supports different viewing orientations.

    The interactive plot includes a legend that provides the parameter values. It also graphically displays the $Q$-$h$ relationship, each parameter value, and an arrow that indicates the head difference $h_{aq}$-$H_{D}$ and points to the value of flow $Q_{D}$ on the axis.
    
    - You can investigate the plot on your own, perhaps using some of the :blue[**INITIAL INSTRUCTIONS**] provided below the plot to guide you.
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
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.C_DRN = 1e-2
st.session_state.C_DRN_label = "1e-2"
st.session_state.HD = 8.0
st.session_state.h_aq_show = 10.0
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
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_D$, $H_D$, and $h_{aq}$.")
            visualize = st.toggle(':rainbow[**Make the plot live** and visualize the input values]', key="DRN_vis", value=True)

    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Elevations**]'):
            if st.session_state.number_input:
                HD = st.number_input(":green[**Drain elevation** $H_D$ (m)]", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
            else:
                HD = st.slider      (":green[**Drain elevation** $H_D$ (m)]", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
            if st.session_state.number_input:
                h_aq_show = st.number_input(":blue[**Aquifer head** $h_{aq}$ (m)]", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
            else:
                h_aq_show = st.slider      (":blue[**Aquifer head** $h_{aq}$ (m)]", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
    
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
    
    # Computation - Define aquifer head range
    h_aq = np.linspace(0, 20, 200)
    
    Q = np.where(h_aq >= HD, st.session_state.C_DRN * (HD - h_aq), 0)
    Q_ref = st.session_state.C_DRN * (HD - h_aq_show) if h_aq_show >= HD else 0   
        
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_D = C_D(H_D-h_{{aq}})$",color='green', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            ax.axvline(0, color='black', linewidth=1)
            ax.axhline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m = {HD:.2f}')
            ax.axhline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m = {h_aq_show:.2f}')
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05, -0.05)
            ax.legend(loc="upper left", fontsize=14)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HD),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='blue', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
#            else:
#                ax.annotate(
#                    '',  # no text
#                    xy=(Q_ref,HD),  # arrowhead
#                    xytext=(Q_ref, h_aq_show),  # arrow start
#                    arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
#                )
            # Add gaining annotations
            if h_aq_show > HD:
                ax.text(-0.04*0.05,20*0.97, "Flow INTO the Drain", fontsize=16, va='center', color='blue')
            else:
                ax.text(-0.04*0.05,20*0.97, "Drain inactive", fontsize=16, va='center', color='red')  
        else:
            ax.plot(h_aq, Q, label=rf"$Q_D = C_D(H_D - h_{{aq}})$",color='green', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m = {HD:.2f}')
            ax.axvline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m = {h_aq_show:.2f}')
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the DRN Boundary-Aquifer System (m))", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
            ax.legend(loc="upper right", fontsize=14)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(HD, Q_ref),  # arrowhead
                    xytext=(h_aq_show, Q_ref),  # arrow start
                    arrowprops=dict(arrowstyle='-|>', color='blue', lw=2.5,  alpha=0.8, mutation_scale=15)
                )
            # Add gaining drn annotations
            if h_aq_show > HD:
                ax.text(0.5, -0.003, "Flow INTO the Drain", fontsize=16, va='center', color='blue')
            else:
                ax.text(0.5, -0.003, "Drain inactive", fontsize=16, va='center', color='red')
    else:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_D = C_D(H_D - h_{{aq}})$",color='black', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into* the Ground-Water System from the DRN  $Q_{D}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(-0.05, 0.05)
            ax.legend(loc="upper left", fontsize=14)
        else:
            ax.plot(h_aq, Q, label=rf"$Q_D = C_D(H_D - h_{{aq}})$",color='black', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.plot([], [], ' ', label=fr"$C_D$ = {st.session_state.C_DRN:.2e}")
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
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
        _The arrow in the plot indicates the head difference $H_{D}-h_{aq}$ and points to the resulting flow $Q_{D}$._
        """)
    st.markdown("""
        _* from the **perspective of inflow** into the groundwater, **drain flow is negative** or zero because it is flow leaving the groundwater._
        """)
    
    with st.expander('Show the :blue[**INITIAL INSTRUCTIONS**]'):
        st.markdown("""
        **Getting Started with the Interactive Plot**
        
        Before starting the exercise, it is helpful to follow these quick steps to explore **DRN** behavior:
        
        **1. Set a Reference Case** - there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider 
        
        * Set **drain elevation** $H_D$ to 10.0 m.
        * Vary **aquifer head** $h_{aq}$ between 8 and 12 m.
        * Observe how the flow $Q_D$ changes:
            * When $h_{aq} > H_D$, the aquifer drains — flow leaves the aquifer through the drain.
            * When $h_{aq} \leq H_D$, no flow occurs — the drain is inactive.
            
        **2. Test Different Conductance Values**
        
        * With $h_{aq} > H_D$, use the slider to vary $C_D$
        * Note how the **slope of the Q–h curve** changes — higher conductance leads to stronger response of outflow to head differences.
        
        These steps help you build intuition for how DRN parameters govern flow — especially the **threshold behavior** and **linear relationship** between head difference and outflow. Feel free to further investigate the interactive plot on your own.
        """)
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        
        st.markdown("""   
        🎯 **Expected Learning Outcomes**
        
        Completing this exercise helps you:
        
        - Understand how drain–aquifer interaction is controlled by aquifer head, drain elevation, and conductance.
        - Interpret the boundary characteristics with a Q–h plot.
        - Recognize the threshold behavior of the DRN package and its role as a one-way boundary.
        - Evaluate how conductance controls the rate of drainage above threshold.
        - Analyze realistic scenarios (e.g., excavation of a building foundation) and the implications for boundary fluxes.
        
        🛠️ **Instructions**
        
        Use the interactive DRN plot and complete the following steps:
        
        1. Initial Exploration - there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider
        
        * As done in the initial instructions, set the drain elevation ($H_D$) to 10 m
        * Vary the aquifer head ($h_{aq}$) from 8 m to 12 m
        * Observe how the flow ($Q_D$) responds to changes in head
        
        Make a record of:
        
            * The threshold value at which the drain becomes active
            * The linearity of the Q–h relationship once the threshold is exceeded
            * The behavior of the drain when $h_{aq} <= H_D$

        2. **Effect of Conductance**
        - Keep $H_D$ = 10 m
        - Set the aquifer head ($h_{aq}$) to 12 m
        - Choose three different conductance values (e.g., 1x10⁻², 1x10⁻³, and 1x10⁻⁴ m²/s)
        
        * For each case:
            * Plot $Q_{D}$ vs $h_{aq}$ from 8 m to 12 m (on paper or spreadsheet)
            * Compare the slope of the Q–h curves 
            * Consider the sensitivity of flow to conductance changes
              
        3. **Realistic Scenario: Excavating a building foundation**
        - Fix the aquifer head at 10.3 m
        - In 1-m steps, vary drain elevation from 9.3 m to 6.3 m, and make note of the inflow rate
        - Consider this as a stylized representation of increasing inflow that needs to be collected and routed away from a construction site. A similar process might be used at a larger scale for an open-pit mine.
    
        💡 **Explore:**
        - How does inflow change as the excavation deepens?
        - What would the construction company have to do to address the inflow?
        - What would reduce the inflow?
        - How might conductance be decreased on excavation walls?
        - How might surrounding aquifer heads be lowered?
        """)

Q_h_plot()

with st.expander('**Show the :rainbow[**EXERCISE**] assessment** - to self-check your understanding'):
    st.markdown("""
    #### 🧠 Excercise assessment
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
The Drain (DRN) boundary condition simulates discharge to external drains, ditches, trenches, topographic depressions, mines, and other features where an aquifer encounters an opening to atmospheric pressure conditions. Flow _only_ occurs when groundwater levels are at or above the opening elevation such that flow is activated. This boundary introduces a **physical cutoff** that prevents outflow based on the **drain elevation**, making it conceptually different from other head-dependent boundaries. A DRN boundary can be defined in any groundwater-flow-model cell, it need not be defined in the surface layer, for example it might be defined deep inside a model to represent a tunnel or and underground mine. 

By exploring Q–h plots, you’ve seen how the discharge remains zero until the aquifer head exceeds the drain elevation, after which it increases linearly based on the conductance. This behavior supports the simulation of seepage faces and artificial drainage systems without over-extracting water from the model.

By adjusting parameters like drain **elevation** and **conductance**, modelers can explore how the discharge remains zero until the aquifer head exceeds the drain elevation, after which it increases linearly based on the conductance. This behavior supports the simulation of seepage faces, artificial drainage systems, and excavations without over-extracting water from the model. Understanding these behaviors through Q–h plots supports stronger conceptual models and more reliable groundwater–surface water integration.

A related boundary package is the DRT boundary package in which water is removed from the groundwater system just as it is in the DRN package, and some of that water can  be returned to the groundwater system at specified locations. It is akin to having injection wells connected to the drain. The total rate of injection is limited by the rate of outflow from the groundwater system to the drain.

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
