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
    2. **Can a boundary both add to and remove water from the groundwater system — depending on heads?**
    
    ▶️ The :orange[**General Head Boundary (GHB)**] addresses these situations. It allows for dynamic, head-dependent exchange with an external water body. The following interactive plot below illustrates how the flow $Q_B$ depends on the groundwater head $h_{gw}$ for a fixed boundary head $H_B$ and conductance $C_B$. The interactive plot is based on the MODFLOW documentation (Harbaugh, 2005) and assumes that the boundary head **$H_B$ is 8 m**. Modify the conductance $C_B$ to see its effect.
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
    ax.set_xlabel("Head in the GHB-groundwater system (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow into the groundwater \nfrom the GHB $Q_{GHB}$ (m³/s)", fontsize=14, labelpad=15)
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

The GHB package is particularly relevant in applied groundwater modeling at the field scale, especially in settings with large water bodies that can provide water to or receive water from the groundwater system without significant change in the surface elevation of the water body. Regardless of the physical feature that a GHB represents, mathematically it will supply or receive as much water as calculated during the simulation, but the head in the water body will not change, so it is important to ensure that the simulated volumetric flow rate is reasonable given the nature of the boundary in the field. GHB differs from all the other head-dependent flow boundaries in that the others (e.g., RIV, DRN, MNW, EVT) include head constraints that cause discontinuity in the Q-h plot and limit flow. Mathematically, this requires iteratively solving for the {h} vector heads.
""")
with st.expander("Tell me more about **the :orange[application of GHB in Field-Scale Groundwater Modeling]**"):
    st.markdown("""
    In field-scale groundwater models a GHB may be associated with one or many cells, and these cells can be anywhere within the three-dimensional model.
    
    A GHB boundary might be used to represent a distant, significant body of water external to the model domain. 
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied1.png', caption="Illustration of A GHB representing a distant external water body.")
    
    st.markdown("""
     Or, a GHB boundary might be used to represent inflow from an adjacent aquifer, which is shown here with a lake that supplies water to the adjacent aquifer, but the supply might also be from reachrge over a large area of the adjacent aquifer.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied2.png', caption="Illustration of A GHB representing a surficial water body.")


    st.markdown("""
     Alternatively, a GHB boundary could be used to represent inflow from an underlying aquifer. Leakage would vary spatially in the model depending on the head in the simulated aquifer. For example, leakage from the underlying aquifer would increase in areas of heavy pumpage in the shallow aquifer.
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied3.png', caption="Illustration of A GHB representing a surficial water body.")
        
    st.markdown("""
     In yet another setting, a GHB boundary might be used to represent a large lake or reservoir with a bottom deep enough that the groundwater level is never below its bottom. 
    """)
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBapplied4.png', caption="Illustration of A GHB representing a surficial water body.")


st.markdown("""
#### 🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual function and mathematical formulation of a General Head Boundary (GHB).
- Apply the GHB equation $Q_B = C_B(H_B - h_{gw})$ to calculate boundary flows and analyze flow directions.
- Evaluate how conductance, groundwater head, and boundary head jointly affect the groundwater–boundary exchange.
- Visualize groundwater exchange at the  boundary (flow into or out of the model at the boundary).
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
The General Head Boundary (GHB), also referred to as the Head-Dependent Flux Boundary in MODFLOW, allows for a more realistic simulation of boundary conditions by enabling **exchange of water between the groundwater system and an external reservoir**. In groundwater models, General Head Boundaries are used to simulate hydraulic interaction with external water bodies or groundwater zones adjacent to the model domain by defining ("fixing") the head of the external feature. The conductance term determines how easily water can flow across the boundary.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
        GHB boundaries differ from specified head boundaries for which the head is specified within the model domain and flow in or out of the model depends on head in the surrounding nodes, and the conductance between those nodes and the specified head node. The GHB response is an extension from a model node where head changes during the model simulation. The value of head in the groundwater system then determines the flow rate and direction as described by the following linear relationship:
        
        $$
        Q_B = C_B(H_B - h_{gw})
        $$
        
        where:
        - $Q_B$ is the flow between the GHB and the groundwater system, taken as positive if it is directed into the groundwater system [L³/T]
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
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHB.png', caption="Schematic illustration of the GHB boundary, modified from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

st.subheader("📈 Interactive Plot and Exercise", divider="orange")
st.markdown("""
    The interactive plot shows how the flow $Q_B$ across a General Head Boundary depends on the difference between groundwater head ($h_{gw}$) and boundary head ($H_B$), and on the conductance ($C_B$). 
    
    Below, under INPUT CONTROLS, in the "Modify Plot Controls" drop-down menu, you can toggle to: 1) turn the plot 90 degrees, 2) choose between slider or typed input to adjust the parameter values, and 3) make the plot "live", meaning it will redraw as soon as new values are entered. Under "Modify Head Elevations", you can adjust the value of groundwater head and GHB head. Finally, under "Modify the Conductance" you can toggle between direct conductance input or computing it from geometric and hydraulic properties. The plot updates dynamically and supports different viewing orientations.

    The interactive plot includes a legend that provides the parameter values. It also graphically displays the $Q$-$h$ relationship, each parameter value, and a green arrow that indicates the head difference $H_{B}$-$h_{gw}$ and points to the value of flow $Q_{GHB}$ on the axis.
    
    - You can investigate the plot on your own, perhaps using some of the :blue[**INITIAL INSTRUCTIONS**] provided below the plot to guide you.
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
            visualize = st.toggle(':rainbow[**Make the plot live** and visualize the input values]', key="GHB_vis", value=True)
            
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
    
    with st.expander('Show the :blue[**INITIAL INSTRUCTIONS**]'):
        st.markdown("""
        **Getting Started with the Interactive Plot**
        
        Before starting the exercise, it is helpful to follow these quick steps to explore GHB behavior:
    
        **1. Using the default values**
    
        * Vary **groundwater head $h_{gw}$** between 5 and 15 m.
        * Observe how **flow $Q_B$** changes in magnitude and when groundwater flows out to the (Q < 0) and boundary water flows into the groundwater (Q > 0).  
    
        **2. Test Different Conductance Values**
    
        * Use the slider to vary $C_B$ and notice how the **slope of the $Q$–$h$ curve** changes.
    
        **3. Optional: Compute Conductance**
    
        * Toggle “Compute conductance”.
        * Enter values for $K$, $A_B$, and $L_B$ to calculate $C_B = \\frac{K A_B}{L_B}$.
        * Notice how the **slope of the $Q$–$h$ curve** changes.
        
        **4. Understand the Role of Head-Dependent Boundaries in Applied Groundwater Modelling**
        
        Depending on the modeling objective, head-dependent boundaries like GHB can be considered in two different ways:
        
        **a) During Model Calibration or Setup:** Assume that the discharge is known from field data and the specified head boundary is the only outlet of the model. Then, given head values in the groundwater system, the values of hydraulic conductivity and river conductance can be calibrated. **This situation is discussed in the introduction** and can be accessed by clicking on the **:red[📕 Introduction] button** on the left menu, then scrolling down and choosing **Show the :rainbow[interactive] plot for Scenario 1**, then scrolling down below the plot to open the :green[**Initial Instructions**] and finally **scrolling down to Step 5**.
        
        Another way to use a GHB head dependent boundary condition:
        
       **b) After the Model is Calibrated such that the Recharge and Conductance are specified:** If other outlets are added to the system (e.g., abstraction wells, drains) the heads in the model will be a result of all the model boundary conditions and parameter values. In consequence, the previously calibrated, and then specified, conductance will control how much of the recharge flows to the :orange[**GHB**] boundary. The discharge will also depend on the location and properties of the other outlets. Here we investigate this behavior for the :orange[**General Head Boundary GHB**]. Other head dependent boundaries like :violet[**RIV**] and :green[**DRN**] follow similar principles.
           
        The subsequent exercise is designed to help you build intuition for how GHB parameters control flow. 
        """)
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        
        st.markdown("""
        
        🎯 **Expected Learning Outcomes**
        
        Completion of this exercise, will help you:
        
        * Understand how GHB flux is driven by head difference and conductance.
        * Interpret Q–h plots in relation to the hydrogeologic behavior.
        * Develop the ability to use the app for conceptual testing and scenario analysis.
       
        🛠️ **Instructions**
        
        Use the interactive GHB plot as follows:
        
        1. **Initial Exploration**
        
        * Start with the conductance $C_B$ = 3x10⁻³ m²/s
        * Set the groundwater head ($h_{gw}$) to **8 m**
        * Set the boundary head ($H_B$) to **10 m**
        * Vary the groundwater head ($h_{gw}$) from **5 m to 15 m**
        * Observe and describe how the flux ($Q$) changes
        * Record:
          * The sign of the flux for different $h_{gw}$ values
          * The value of $Q$ when $h_{gw}$ = $H_B$
        * Return the groundwater head ($h_{gw}$) to **8 m**
        
        2. **Conductance Effect**
                
        * Return the groundwater head ($h_{gw}$) to **8 m**
        * Keep $H_B$ at **10 m**
        * Choose three different conductance values (e.g., **3x10⁻², 3x10⁻³, and 3x10⁻⁴ m²/s**)
        * For each conductance value:
          * Plot (e.g., on a piece of paper) $Q_B$ vs $h_{gw}$ for $h_{gw}$ in the range from **5 to 15 m**
          * Compare the slope and shape of the resulting lines
        * Repeat the above procedure for 
          * Increased and decreased $H_B$ (e.g., **5, 9, and 20 m**)
          * Plot $Q_B$ vs $h_{gw}$ for a range of $H_B$
          * Compare the slope and shape of the resulting lines
        
        3. **Realistic Scenarios**
        
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
The General Head Boundary (GHB) offers a flexible way to simulate interactions with external water bodies or regions not explicitly modeled — such as distant lakes, rivers, or adjacent groundwater system systems. Its formulation as a **head-dependent boundary** enables both **inflow and outflow**, depending on the head difference between any groundwater-flow-model cell and the boundary. A GHB boundary can be defined in any groundwater-flow-model cell.

The GHB condition captures the essential physics of cross-boundary exchange using only a few parameters: the **boundary head**, **groundwater head**, and **conductance**, which reflects the geometry and hydraulic properties of the connection.

Analyzing **Q–h plots**, provides a clearer understanding of how conductance controls the slope of the exchange curve and how head differences dictate the flow direction. This conceptual insight is essential for setting realistic boundary conditions in MODFLOW models.

Other boundary packages discussed in this module incorporate the concepts of head diffference between the boundary and the groundwater system driving the direction of flow into or out of the system, with the magnitude of head difference and conductance controlling the flow rate. The GHB package is unique in that there are no constraints on the flow so the $Q$-$h$ plot is continuously linear.  All the other head-dependent-flow packages have head constraints causing discontinuous $Q$-$h$ plots. 

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
