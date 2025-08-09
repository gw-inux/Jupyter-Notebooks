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
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_riv.json"
path_quest_exer =  "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_riv.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_riv.json"

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
    
st.title("Theory and Concept of the :violet[River Boundary (RIV) in MODFLOW]")
st.subheader("Groundwater - :violet[River Boundary] interaction", divider="violet")

st.markdown("""
#### 💡 Motivation: Why River Boundaries?
""")

# Initial plot
x_multi = 1
h_RIVi = 8
h_boti = 6

# Slider input and plot
columns0 = st.columns((1,1), gap = 'large')
with columns0[0]:
    st.markdown("""
    Let’s begin with some simple questions:
    - Can groundwater both **discharge** into a river and **receive recharge** from a river?
    - How does **stream stage** influence exchange flow?
    - What happens if the **aquifer drops below the riverbed**?
    
    
    groundwater would be discharging into a river (gaining stream) and when river water would be recharging the groundwater system (losing stream)
    
    ▶️ The :violet[**River (RIV) Boundary**] in MODFLOW handles these dynamics by simulating a **head-dependent flow** that includes a check for streambed drying. The relationship between aquifer head $h_{aq}$ and river head $h_{RIV}$ is defined via a **conductance term** $C_{RIV}$. The following interactive plot shows how the flow between river and groundwater $Q_{RIV}$ responds to these changing conditions. The interactive plot is based on the MODFLOW documentation (Harbaugh, 2005) and consider **$h_{RIV}$ as 8 m** with a **river bottom elevation of 6 m**.Try adjusting the river conductance to explore the general behavior.
    """)
    st.latex(r'''Q_{RIV} = C_{RIV} (h_{RIV} - h_{{aq}})''')

    
    
with columns0[1]:
    #C_RIV
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
    labels, default_label = prep_log_slider(default_val = 3e-3, log_min = -5, log_max = 0)
    selected_Ci = st.select_slider("**Conductance :violet[$C_{Riv}$]** in m²/s", labels, default_label, key = "RIV_Ci")
    st.session_state.Ci_RIV = float(selected_Ci)
            
    # COMPUTATION
    # Define aquifer head range
    h_aqi = np.linspace(0, 20, 200)
    Qi = np.where(h_aqi >= h_boti, st.session_state.Ci_RIV * (h_RIVi - h_aqi), st.session_state.Ci_RIV * (h_RIVi - h_boti))

    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, Qi, color='black', linewidth=4)
    ax.set_xlabel("Heads and elevations in the RIV-Aquifer System (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow into the Groundwater \nfrom the RIV boundary $Q_{RIV}$ (m³/s)", fontsize=14, labelpad=15)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    ax.set_title("Flow Between Groundwater and RIV", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)
    
    st.markdown("""
    **FIG:** Explore with the initial plot how outflow varies for changes of the :violet[river conductance].
    
    This **initial plot** is designed to bridge the gap between traditional Q-h plots on paper and the :rainbow[**interactive plots**] provided further down in the app. These allow you to explore the _Q_-_h_ relationships more intuitively, supported by interactive controls and guided instructions.
    """)

st.markdown("""
#### 🎯 Learning Objectives

By the end of this section, you will be able to:

- Explain the conceptual and mathematical formulation of the RIV boundary condition in MODFLOW.
- Apply the RIV flow equation to simulate groundwater–river exchange and identify when groundwater would be discharging into a river (gaining stream) and when river water would be recharging the groundwater system (losing stream).
- Evaluate how river stage, aquifer head, riverbed elevation, and conductance control the direction and magnitude of exchange.
- Interpret _Q_–_h_ plots that illustrate the flow regime, including unsaturated conditions when aquifer heads drop below the riverbed.
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
            
st.subheader('🧪 Theory and Background', divider="violet")
st.markdown("""
In groundwater modeling, simulating the interaction between an aquifer and a river is essential for understanding stream depletion, baseflow contribution, and groundwater–surface water exchange. But how do we realistically represent a river in a groundwater model?
""")

with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    The flow between a stream and an aquifer, $Q_{RIV}$, depends on the groundwater head in the river $h_{aq}$. 
    The relationship is as follows:
    """)
    st.latex(r'''Q_{RIV} = C_{RIV} (h_{RIV} - h_{{aq}})''')
    
    st.markdown("""
    where:
    - $Q_{RIV}$ is the flow between the river and the aquifer (positive if it is directed into the aquifer) [L3/T]
    - $h_{RIV}$ is the water level (head) of the river (L),
    - $C_{RIV}$ is the hydraulic conductance of the river bed [L²/T], and
    - $h_{aq}$ is the head in the aquifer beneath the river bed (L).
    
    If the aquifer head $h_{aq}$ is below the elevation of the bottom of the river bed, $R_{BOT}$, the relationship is as follows:
    """)
    
    st.latex(r'''Q_{RIV} = C_{RIV} (h_{RIV} - R_{{BOT}})''')
   
    st.markdown("""
    where:
    - $R_{BOT}$ is the elevation of the river bed bottom [L].
    """)
    st.write(':blue[**It is important to compare the calculated flow between the river and aquifer to the flow in the segment of river being modeled.**] :green[The amount of water lost or gained needs to be concistent with observed river flow over the length of the segment such that it is reasonable to assume a constant river head.]')
    
    
    st.write(':blue[**If there is a significant gain or loss of flow, the river head may rise or fall, but the MODFLOW RIV package will continue to use the same river head.**] :green[If the modeler wants to represent feedback between the amount of water lost or gained and the elevation of the river head, the STR  (stream package) can be used. The concepts for flow between the river and the aquifer do not change from what is presented here.]')


with st.expander('**Click here** to read about the :green[**heads used**] in the River Boundary condition of MODFLOW'):
    st.markdown("""
    ### Heads used in the River Boundary of MODFLOW
    """)
    st.markdown("""
    MODFLOW assumes that the river bed permeability is substantially lower than the aquifer permeability.

    Consequently, all the head loss between the river and the aquifer occurs between the top and bottom of the river bed.

    MODFLOW requires input values for:

    - Elevation of the River head $h_{RIV}$ (called Stage in MODFLOW, is labeled River Surface in this image). Because the river is an open body of water it is assumed the River head occurs at the top of the river bed.

    - River bottom elevation (called $R_{bot}$ in MODFLOW, is the bottom of the hatched zone in this image).  
    """)
    left_co1, cent_co1, last_co1 = st.columns((10,80,10))
    with cent_co1:
        st.image('06_Groundwater_modeling/FIGS/RIV_CONCEPT_2.png', caption="Concept of the River boundary (modified from McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")
    st.markdown("""
    Aquifer head elevation is calculated by MODFLOW in response to all the model inputs (labeled Head in Cell in this image). It is assumed the aquifer head is uniform throughout the cell and thus occurs at the elevation of the river bottom.

    When the aquifer head is above the river bottom, the head difference across the river bed is: (Stage – Head in Cell). When this value is negative, water is flowing from the aquifer to the river.

    This head difference is multiplied by Conductance to determine Flow Rate between the River and the Aquifer.
 
    """)

with st.expander('**Click here** to read how :green[**conductance is calculated**]'):
    st.markdown("""
    ### Calculating MODFLOW River Boundary Conductance
    """)
    
    st.markdown("""
    MODFLOW requires input of Conductance.

    Conductance includes all of Darcy's Law except the head difference between the river and the aquifer. 
    """)    
    st.latex(r'''Q_{RIV} = K_vA \frac{\Delta h}{M}''')
    
    st.latex(r'''C_{RIV} = K_vA \frac{1}{M} = K_vLW \frac{1}{M}''')

    st.markdown("""
    where: 

    - $K_v$ is vertical hydraulic conductivity of the river bed [L/T]
    - $A$ is plan view area of the river bed (=$LW$) [L²]
    - $M$ is thickness of the river bed (the distance over which the gradient is calculated) [L]
    """)
    
    
    
    left_co2, cent_co2, last_co2 = st.columns((10,80,10))
    with cent_co2:
        st.image('06_Groundwater_modeling/FIGS/RIV_COND_2.png', caption="Calculation of the Riverbed conductance (from McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

    
    st.markdown("""
    $\Delta h$ is the difference between the Head in the Stream and Head in the Aquifer (discussed above in the section about the heads used in the River Boundary condition of MODFLOW)

    In general, MODFLOW calculates flow $Q$ with a conductance $C$ as
    """)
    st.latex(r'''Q = C \Delta h''')

with st.expander('**Click here** to read how flow is calculated when the :green[**aquifer head is lower then the river bottom**]'):
    st.markdown("""
    ### A "Disconnected" River occurs when the Aquifer Head is Lower than the River Bottom""")
    
    st.markdown("""
    MODFLOW assumes the river bed permeability is substantially lower than the aquifer permeability, so the river bed remains saturated when the aquifer head is below the river bottom.

    Thus, when the aqufier head is lower than the river bottom, the pressure head at the bottom of the lower permeability material is defined as zero (ignoring matric tension) so, the hydraulic head is equal to the elevation of the river bottom. 

    """)
    left_co3, cent_co3, last_co3 = st.columns((10,80,10))
    with cent_co3:
        st.image('06_Groundwater_modeling/FIGS/RIV_CONCEPT_UNSAT_2.png', caption="Concept of the River boundary when the aquifer head falls below the river bottom (modified from McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

    st.markdown("""
    When the aquifer head $h_{aq}$ is lower than the river bottom $R_{bot}$, the head difference across the river bed is: 

    - Elevation of the River Surface $h_{Riv}$ – Elevation of the River Bottom $R_{bot}$

    - :red[This difference remains a constant.]

    This head difference is multiplied by conductance to determine the flow rate from the river to the aquifer
    """)

st.subheader("Interactive Plot and Exercise", divider="violet")
st.markdown("""
The interactive plot shows how the flow $Q_{RIV}$ across a River Boundary depends on the **difference between aquifer head** ($h_{aq}$) and **river head** ($h_{riv}$), while being constrained by the **river bottom elevation** ($R_{bot}$) and scaled by the **riverbed conductance** ($C_{RIV}$).

Use the sliders or number inputs to adjust these parameters. You can also toggle between direct conductance input or compute it from hydraulic and geometrical properties. The plot updates dynamically and supports different viewing orientations.

- You can investigate the plot on your own. Some :blue[INITIAL INSTRUCTIONS] may guide you.
- An :rainbow[EXERCISE] allows you to apply the plot and deepen your understanding. This exercise invites you to explore how river–aquifer exchange is controlled by **river stage, aquifer hydraulic head, conductance, and bottom elevation**. Use the interactive RIV plot to examine how these factors influence the exchange flow, and interpret the **physical meaning based on _Q_–_h_ plots**, especially the transitions between **gaining**, **losing**, and **decoupled** river conditions.
""")

# Functions

# Callback function to update session state
def update_C():
    st.session_state.C_slider_value = st.session_state.C_input
def update_C_RIV():
    """Handles both number input (float) and select_slider (str)"""
    raw_val = st.session_state.C_input
    if isinstance(raw_val, str):
        st.session_state.C_RIV = float(raw_val)  # from select_slider
    elif isinstance(raw_val, float):
        st.session_state.C_RIV = raw_val         # from number_input
def update_K():
    st.session_state.K_slider_value = st.session_state.K_input
def update_K_RIV():
    """Handles both number input (float) and select_slider (str)"""
    raw_val = st.session_state.K_input
    if isinstance(raw_val, str):
        st.session_state.K_RIV = float(raw_val)  # from select_slider
    elif isinstance(raw_val, float):
        st.session_state.K_RIV = raw_val         # from number_input
def update_h_RIV():
    st.session_state.h_RIV = st.session_state.h_RIV_input
def update_L_RIV():
    st.session_state.L_RIV = st.session_state.L_RIV_input
def update_W_RIV():
    st.session_state.W_RIV = st.session_state.W_RIV_input
def update_M_RIV():
    st.session_state.M_RIV = st.session_state.M_RIV_input
def update_h_bot():
   st.session_state.h_bot = st.session_state.h_bot_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
def update_elevation_input(fieldname: str):
    """
    Update h_ref or thick from text input when changed.
    """
    try:
        value = float(st.session_state[fieldname])
    except ValueError:
        return  # Ignore invalid typing for now

    if fieldname == "h_ref_input":
        st.session_state.h_ref = value
    elif fieldname == "thick_input":
        st.session_state.thick = value
    
def draw_sharp_arrow(ax, start, end, orientation='vertical', 
                     axis_range_x=None, axis_range_y=None,
                     color='blue', al=0.8, lw=2.5, hs=20):
    """
    Draws a sharp arrow between two points on a matplotlib axis.

    Parameters:
        ax: matplotlib axis object
        start: (x, y) tuple - start of arrow
        end: (x, y) tuple - end of arrow
        orientation: 'vertical' or 'horizontal'
        axis_range_x: tuple (x_min, x_max) - for head width scaling
        axis_range_y: tuple (y_min, y_max) - for head length scaling
        color: arrow color
        alpha: transparency
        linewidth: arrow line width
        head_scale: mutation scale for arrow head size
    """
    if orientation == 'vertical':
        xytext = start
        xy = end
    elif orientation == 'horizontal':
        xytext = start
        xy = end
    else:
        raise ValueError("Orientation must be 'vertical' or 'horizontal'")

    ax.annotate(
        '',
        xy=xy,
        xytext=xytext,
        arrowprops=dict(
            arrowstyle='-|>',
            color=color,
            lw=lw,
            alpha=al,
            shrinkA=0,
            shrinkB=0,
            mutation_scale=hs
        )
    )
    

# Initialize session state for value and toggle state
st.session_state.C_RIV = 1e-2
st.session_state.C_RIV_label = "1e-2"
st.session_state.K_RIV = 1e-5
st.session_state.K_RIV_label = "1e-5"
st.session_state.thick = 20.0
st.session_state.h_ref = 0.0
st.session_state.h_aq_show = 10.0
st.session_state.h_RIV = 9.0
st.session_state.L_RIV = 100.0
st.session_state.W_RIV = 10.0
st.session_state.M_RIV = 1.0
st.session_state.h_bot = 7.0
st.session_state.number_input = False  # Default to number_input
st.session_state.condcomp = False

# Main area inputs
@st.fragment
def Q_h_plot():
    
    st.markdown("""
       #### :violet[INPUT CONTROLS]
        """)
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    log_min2 = -10.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max2 = -2.0  # T / Corresponds to 10^1 = 10
    x_multi = 1
    
    # INPUT for the computation
    columns1 = st.columns((1,1,1), gap = 'small')
    
    with columns1[0]:
        with st.expander('Modify the **Plot Control**'):
            st.text_input(
                "**Lowest elevation to show on graph in m**",
                value=str(st.session_state.h_ref),
                key="h_ref_input",
                on_change=update_elevation_input,
                args=("h_ref_input",)
            )
            
            st.text_input(
                "**Highest elevation to show on graph in m**",
                value=str(st.session_state.thick),
                key="thick_input",
                on_change=update_elevation_input,
                args=("thick_input",)
            )
            
            # --- VALIDATION ---
            h_ref = st.session_state.h_ref
            thick = st.session_state.thick
            
            if thick <= h_ref+0.1:
                st.error(
                    f"🚫 Highest elevation must be greater than lowest elevation.\n\n"
                    f"Lowest entered: **{h_ref:.2f} m**\n"
                    f"Suggested highest: **{h_ref + 20.0:.2f} m**"
                )
                st.stop()    
            x_range = st.number_input("**Range of Q (m³/s) in the plot**", 0.02, 1.00, 0.05, 0.01)
            turn = st.toggle('**Turn Graph** 90 degrees', key="RIV_turn", value=True)
            st.session_state.number_input = st.toggle("**Use Slider or Number** for input")      
            visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="RIV_vis", value=True)
    
    # Make sure that heads and elevations are inside the plot
    if st.session_state.h_aq_show < 0.1+h_ref:
        st.session_state.h_aq_show = 0.1+h_ref
    if st.session_state.h_RIV < 0.1+h_ref:
        st.session_state.h_RIV = 0.1+h_ref
    if st.session_state.h_bot < 0.1+h_ref:
        st.session_state.h_bot = 0.1+h_ref        
    
    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Elevations**]'):
            #h_RIV
            if st.session_state.number_input:
                h_RIV = st.number_input(":violet[**River head** $h_{RIV}$ (m)]", 0.1+h_ref, thick, st.session_state.h_RIV, 0.1, key="h_RIV_input", on_change=update_h_RIV)
            else:
                h_RIV = st.slider      (":violet[**River head** $h_{RIV}$ (m)]", 0.1+h_ref, thick, st.session_state.h_RIV, 0.1, key="h_RIV_input", on_change=update_h_RIV)
            #h_bot
            if st.session_state.number_input:
                h_bot = st.number_input(":orange[**River bed bottom** $R_{bot}$ (m)]", 0.1+h_ref, thick, st.session_state.h_bot, 0.1, key="h_bot_input", on_change=update_h_bot)
            else:
                h_bot = st.slider      (":orange[**River bed bottom** $R_{bot}$ (m)]", 0.1+h_ref, thick, st.session_state.h_bot, 0.1, key="h_bot_input", on_change=update_h_bot)
            #h_aq
            if st.session_state.number_input:
                h_aq_show = st.number_input(":blue[**Aquifer head** $h_{aq}$ (m)]", 0.1+h_ref, thick, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
            else:
                h_aq_show = st.slider      (":blue[**Aquifer head** $h_{aq}$ (m)]", 0.1+h_ref, thick, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)            
    with columns1[2]:
        with st.expander('Modify the :violet[**Conductance**]'):
            condcomp = st.toggle('Compute $C_{RIV}$ explicitly', key='condcomp')
            if st.session_state.condcomp:
                #L_RIV
                if st.session_state.number_input:
                     L_RIV = st.number_input("**River length** $L_{RIV}$(m)", 1.0, 1000.0, st.session_state.L_RIV, 0.1, key="L_RIV_input", on_change=update_L_RIV)
                else:
                     L_RIV = st.slider      ("**River length** $L_{RIV}$(m)", 1.0, 1000.0, st.session_state.L_RIV, 0.1, key="L_RIV_input", on_change=update_L_RIV)
                #W_RIV
                if st.session_state.number_input:
                     W_RIV = st.number_input("**River width** $W_{RIV}$ (m)", 1.0, 200.0, st.session_state.W_RIV, 0.1, key="W_RIV_input", on_change=update_W_RIV)
                else:
                     W_RIV = st.slider      ("**River width** $W_{RIV}$ (m)", 1.0, 200.0, st.session_state.W_RIV, 0.1, key="W_RIV_input", on_change=update_W_RIV)
                #M_RIV
                if st.session_state.number_input:
                     M_RIV = st.number_input("**River bed thickness** $M_{RIV}$ (m)", 0.01, 5.0, st.session_state.M_RIV, 0.1, key="M_RIV_input", on_change=update_M_RIV)
                     h_bed = h_bot + M_RIV
                else:
                     M_RIV = st.slider      ("**River bed thickness** $M_{RIV}$ (m)", 0.01, 5.0, st.session_state.M_RIV, 0.1, key="M_RIV_input", on_change=update_M_RIV)
                     h_bed = h_bot + M_RIV
                # LOG Slider/number input for K_RIV
                if st.session_state.number_input:
                    st.number_input("**Riverbed hydraulic conductivity** $K_v$ (m/s)", 10**log_min2, 10**log_max2, st.session_state.K_RIV, get_step(st.session_state.K_RIV), format="%.2e", key="K_input", on_change=update_K_RIV)
                else:
                    labels, _ = prep_log_slider(default_val=1e-4, log_min=log_min2, log_max=log_max2)
                    # Ensure label string matches st.session_state.K_GHB
                    st.session_state.K_RIV_label = get_label(st.session_state.K_RIV, labels)
                    st.select_slider("**Riverbed hydraulic conductivity** $K_v$ (m/s)", labels, value = st.session_state.K_RIV_label, key="K_input", on_change=update_K_RIV)              
                st.session_state.C_RIV = st.session_state.L_RIV * st.session_state.W_RIV * st.session_state.K_RIV / st.session_state.M_RIV
            else:
                #C_RIV
                if st.session_state.number_input:
                    st.number_input("**Conductance** $C_{Riv}$ (m²/s)", 10**log_min1, 10**log_max1, st.session_state.C_RIV, get_step(st.session_state.C_RIV), format="%.2e", key="C_input", on_change=update_C_RIV)
                else:
                    labels, _ = prep_log_slider(default_val=1e-2, log_min=log_min1, log_max=log_max1)
                    # Ensure label string matches st.session_state.K_GHB
                    st.session_state.C_RIV_label = get_label(st.session_state.C_RIV, labels)
                    st.select_slider("**Conductance** $C_{Riv}$ (m²/s)", labels, value = st.session_state.C_RIV_label, key="C_input", on_change=update_C_RIV)
                # Update K_GHB_value based on computed values
                st.session_state.K_RIV = st.session_state.C_RIV * st.session_state.M_RIV / st.session_state.L_RIV / st.session_state.W_RIV        
            
    # INPUT PROCESSING
    # calculate top of river bed
    if condcomp:
        h_bed = h_bot + M_RIV
    else:
        h_bed = h_bot
    
    if h_RIV < h_ref:
        st.write(':red[**Visualization issue: River head is below lowest elevation shown on the graph.**] :green[Adjust in Graph Controls.]')
        
    if h_aq_show < h_ref:
        st.write(':red[**Visualization issue: Aquifer head is below lowest elevation shown on the graph.**] :green[Adjust in Graph Controls.]')
        
    if h_bot < h_ref:
        st.write(':red[**Visualization issue: River bottom is below lowest elevation shown on the graph.**] :green[Adjust in Graph Controls.]')
        
    if h_RIV > thick:
        st.write(':red[**Visualization issue: River head is above highest elevation shown on the graph.**] :green[Adjust in Graph Controls.]')
        
    if h_aq_show > thick:
        st.write(':red[**Visualization issue: Aquifer head is above highest elevation shown on the graph.**] :green[Adjust in Graph Controls.]')
        
    if h_bot > thick:
        st.write(':red[**Visualization issue: River bottom is above highest elevation shown on the graph.**] :green[Adjust in Graph Controls.]')
        
    if h_RIV < h_bed:
        st.write(':red[**Illogical physical representation. River head is below the top of the river bed. The value of flow will be in error because the gradient will be calculated as if dh occurs across the entire thickness of the river bed, but it does not. Also there is no open water to provide the leakage through the river bed.**] :green[Adjust River Head, River Bottom, and/or River Bed Thickness.]')
        
    if h_RIV < h_bot:
        st.write(':red[**Illogical physical representation. River head is below the bottom of the river.**] :green[Adjust River Head, River Bottom, and/or River Bed Thickness.]')
        
    # COMPUTATION
    # Define aquifer head range
    h_aq = np.linspace(0+h_ref, thick+h_ref, 200)
    Q = np.where(h_aq >= h_bot, st.session_state.C_RIV * (h_RIV - h_aq), st.session_state.C_RIV * (h_RIV - h_bot))
    Q_ref = st.session_state.C_RIV * (h_RIV - h_aq_show) if h_aq_show >= h_bot else st.session_state.C_RIV * (h_RIV - h_bot)
    
    lim1 = x_range
    lim2 = -x_range
        
    # Create the graph
    fig, ax = plt.subplots(figsize=(8,10))
    if turn:
        
        # Shown always
        xlabel = "Flow into the Ground-Water System From the River $Q_{RIV}$ (m³/s)"
        ylabel = "Heads and Elevations in the River-Aquifer System (m)"
        
        # Range of plot
        ax.set_ylim(h_ref, thick)
        ax.set_xlim(lim1,lim2)
        
        # Visualize is the plot with all the explanations
        if visualize:
            ax.plot(Q, h_aq, label=rf"$Q$ in m³/s = {Q_ref:.2e}", color='fuchsia', linewidth=3)
            # Plot visuals
            ax.axvline(0, color='black', linewidth=1)
            # Plot visualization
            ax.axhline(h_RIV,     color='navy',      linewidth=2,   linestyle='-', label=f'$h_{{RIV}}$ in m = {h_RIV:.2f}')
            ax.axhline(h_aq_show, color='lightblue', linewidth=2.5, linestyle='--', label=f'$h_{{aq}}$ in m = {h_aq_show:.2f}')
            ax.axhline(h_bed,     color='wheat',      linewidth=2,   linestyle='-', label=f'$h_{{bed}}$ in m = {h_bed:.2f}')
            ax.axhline(h_bot,     color='dimgrey',      linewidth=2,   linestyle='dotted', label=f'$R_{{bot}}$ in m = {h_bot:.2f}')    
    
            # fill ground water
            ax.fill_betweenx(y=[h_ref, h_aq_show], x1=lim2, x2=lim1, color='lightblue', alpha=0.3, label="zone of ground water")  
            # fill river water
            ax.fill_betweenx(y=[h_bed, h_RIV], x1=lim2, x2=lim1, color='navy', alpha=0.3, label="zone of river water")
            # fill river bed
            ax.fill_betweenx(y=[h_bot, h_bed],x1=lim2, x2=lim1, color='tan', edgecolor='navy', hatch='Oooo..', linewidth=2, alpha=0.3, label="zone of river bed")
            
            # Length of lines
            line_length = 0.04 * abs(lim1 - lim2)  # 5% of x-axis width
            
            # --- Triangle marker at h_RIV with two short horizontal lines below triangle --- #
            ax.plot([0.9*lim1],[h_RIV+(thick-h_ref)/70], marker='v', color='navy', markersize=12)
            line_y1 = h_RIV - (thick-h_ref)/100
            line_y2 = h_RIV - (thick-h_ref)/50            
            # Draw the lines
            ax.hlines(y=line_y1, xmin=0.9*lim1 - line_length/2, xmax=0.9*lim1 + line_length/2, color='navy', linewidth=2)
            ax.hlines(y=line_y2, xmin=0.9*lim1 - line_length/3, xmax=0.9*lim1 + line_length/3, color='navy', linewidth=2)
         
            # --- Triangle marker at h_aq with two short horizontal lines below triangle --- #
            ax.plot([0.9*lim2],[h_aq_show+(thick-h_ref)/70], marker='v', color='lightblue', markersize=12)
            line_y1 = h_aq_show - (thick-h_ref)/100
            line_y2 = h_aq_show - (thick-h_ref)/50              
            # Draw the lines
            ax.hlines(y=line_y1, xmin=0.9*lim2 - line_length/2, xmax=0.9*lim2 + line_length/2, color='lightblue', linewidth=2)
            ax.hlines(y=line_y2, xmin=0.9*lim2 - line_length/3, xmax=0.9*lim2 + line_length/3, color='lightblue', linewidth=2)
    
            # Arrows
            if Q_ref < 0:
                draw_sharp_arrow(ax, start=(Q_ref, h_aq_show), end=(Q_ref, h_RIV), orientation='vertical', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='blue', al=0.4, lw=3, hs=25)
            else:
                # Unsaturated zone flow arrows
                if h_aq_show < h_bot:
                    # Arrow indicating Q
                    draw_sharp_arrow(ax, start=(Q_ref,h_RIV ), end=(Q_ref, h_bot), orientation='vertical', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='green', al=0.4, lw=3, hs=25)
                    
                    # Unsat flow arrows
                    x_min = lim2
                    x_max = lim1
                
                    for x in np.linspace(x_min, x_max, 10):  # 10 arrows, evenly spaced
                        draw_sharp_arrow(ax, start=(x,h_bot ), end=(x, h_aq_show), orientation='vertical', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='brown', al=0.1, lw=3, hs=25)
                        
                    # Add label at far left
                    ax.text(
                        0.3*lim1,  # slightly inside the graph
                        (h_bot + h_aq_show) / 2,
                        "Unsaturated zone flow",
                        color='brown',
                        fontsize=12,
                        rotation=0,
                        va='center'
                    )
                else:
                    draw_sharp_arrow(ax, start=(Q_ref,h_RIV ), end=(Q_ref, h_aq_show), orientation='vertical', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='green', al=0.4, lw=3, hs=25)                    
            # Add gaining/losing river annotations
            ax.text(-0.04*lim1, h_ref+(thick-h_ref)*0.97, "Flow INTO the River", va='center',color='blue',  fontsize=16)
            ax.text(0.82   *lim1, h_ref+(thick-h_ref)*0.97, "Flow OUT of the River",  va='center',color='green', fontsize=16)
        else:
            ax.plot(Q, h_aq, label=rf"$Q$", color='black', linewidth=3)            
    else:
        xlabel = "Heads and elevations in the River-Aquifer System (m)"
        ylabel = "Flow into the Ground-Water System From the River $Q$ (m³/s)"
        
        # Range of plot
        ax.set_xlim(h_ref, thick)
        ax.set_ylim(lim2,lim1) 
       
        if visualize:
            ax.plot(h_aq, Q, label=rf"$Q$", color='fuchsia', linewidth=3)
            # Plot visuals
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(h_RIV,     color='navy',      linewidth=2,   linestyle='-', label=f'$h_{{RIV}}$ in m = {h_RIV:.2f}')
            ax.axvline(h_aq_show, color='lightblue', linewidth=2.5, linestyle='--', label=f'$h_{{aq}}$ in m = {h_aq_show:.2f}')
            ax.axvline(h_bed,     color='wheat',     linewidth=2,   linestyle='-', label=f'$h_{{bed}}$ in m = {h_bed:.2f}')
            ax.axvline(h_bot,     color='dimgrey',   linewidth=2,   linestyle='dotted', label=f'$R_{{bot}}$ in m = {h_bot:.2f}')
            
            # fill ground water
            ax.fill_betweenx(y=[lim2,lim1],x1=h_ref, x2=h_aq_show, color='lightblue', alpha=0.3, label="zone of ground water")  
            # fill river water
            ax.fill_betweenx(y=[lim2,lim1],x1=h_bed, x2=h_RIV, color='navy', alpha=0.3, label="zone of river water")
            # fill river bed
            ax.fill_betweenx(y=[lim2,lim1],x1=h_bot, x2=h_bed, color='tan', edgecolor='navy', hatch='Oooo..', linewidth=2, alpha=0.3, label="zone of river bed")
    
            # Length of lines
            line_length = 0.04 * abs(lim1 - lim2)  # 5% of y-axis width (now vertical!)
        
            # --- Triangle marker at h_RIV with two short vertical lines below triangle --- #
            ax.plot([h_RIV+(thick-h_ref)/70], [0.9*lim1], marker='<', color='navy', markersize=12)
            line_x1 = h_RIV - (thick-h_ref)/100
            line_x2 = h_RIV - (thick-h_ref)/50
            # Draw the lines (VERTICAL)
            ax.vlines(x=line_x1, ymin=0.9*lim1 - line_length/2, ymax=0.9*lim1 + line_length/2, color='navy', linewidth=2)
            ax.vlines(x=line_x2, ymin=0.9*lim1 - line_length/3, ymax=0.9*lim1 + line_length/3, color='navy', linewidth=2)
        
            # --- Triangle marker at h_aq with two short vertical lines below triangle --- #
            ax.plot([h_aq_show+(thick-h_ref)/70], [0.9*lim2], marker='<', color='lightblue', markersize=12)
            line_x1 = h_aq_show - (thick-h_ref)/100
            line_x2 = h_aq_show - (thick-h_ref)/50
            ax.vlines(x=line_x1, ymin=0.9*lim2 - line_length/2, ymax=0.9*lim2 + line_length/2, color='lightblue', linewidth=2)
            ax.vlines(x=line_x2, ymin=0.9*lim2 - line_length/3, ymax=0.9*lim2 + line_length/3, color='lightblue', linewidth=2)
    
            # Arrows
            if Q_ref < 0:
                draw_sharp_arrow(ax, start=(h_aq_show, Q_ref), end=(h_RIV,Q_ref), orientation='horizontal', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='blue', al=0.4, lw=3, hs=25)
            else:
                if h_aq_show < h_bot:
                    # Q arrow
                    draw_sharp_arrow(ax, start=(h_RIV, Q_ref), end=(h_bot,Q_ref), orientation='horizontal', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='green', al=0.4, lw=3, hs=25)
                    # unsat arrow
                    
                    y_min = lim2
                    y_max = lim1
                
                    for x in np.linspace(y_min, y_max, 10):  # 10 arrows, evenly spaced
                        draw_sharp_arrow(ax, start=(h_bot, x), end=(h_aq_show,x), orientation='horizontal', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='brown', al=0.1, lw=3, hs=25)
                    # Add label at far left
                    ax.text(
                        (h_bot + h_aq_show) / 2,  # slightly inside the graph
                        0.01*lim1,
                        "Unsaturated zone flow",
                        color='brown',
                        fontsize=12,
                        rotation=270,
                        va='center'
                    )
                else:
                    draw_sharp_arrow(ax, start=(h_RIV, Q_ref), end=(h_aq_show,Q_ref), orientation='horizontal', axis_range_x=(lim1, lim2), axis_range_y=(h_ref, thick), color='green', al=0.4, lw=3, hs=25)
            # Add gaining/losing river annotations
            ax.text(thick-(0.4*(thick-h_ref)), -0.05*lim1, "Flow INTO the River", va='center',color='blue',  fontsize=16)
            ax.text(thick-(0.4*(thick-h_ref)),  0.05*lim1, "Flow OUT of the River",  va='center',color='green', fontsize=16)
        else:
            ax.plot(h_aq, Q, label=rf"$Q$", color='black', linewidth=3)
   
   # === SHARED FORMATTING === #
    ax.set_xlabel(xlabel, fontsize=14, labelpad=15)
    ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)  
    ax.set_title("Flow Between Groundwater and River", fontsize=16, pad=10)
    
    #ax.grid(True)
    
    if visualize:
        # Adjust the bottom margin to make room for the legend
        fig.subplots_adjust(bottom=0.25)  # Increase if legend is large
        
        # This sorts the legend entries - Get current legend entries
        handles, labels = ax.get_legend_handles_labels()
        
        # Main handles and labels
        main_handles = [handles[i] for i in [0, 1, 2, 3, 4]]
        main_labels  = [labels[i] for i in [0, 1, 2, 3, 4]]
        
        # Last special handles and labels
        last_handles = [handles[i] for i in [5, 6, 7]]
        last_labels  = [labels[i] for i in [5, 6, 7]]
        
        # Plot first legend (normal)
        first_legend = ax.legend(
            main_handles,
            main_labels,
            loc='lower center',
            bbox_to_anchor=(0.25, -0.28), # slightly to the left
            ncol=2,
            fontsize=12,
            frameon=False
        )
        
        # Plot second legend (special column)
        second_legend = ax.legend(
            last_handles,
            last_labels,
            loc='lower center',
            bbox_to_anchor=(0.80, -0.27), # to the right
            ncol=1,
            fontsize=12,
            frameon=False
        )
        
        # Add first legend back manually
        ax.add_artist(first_legend)
    else:
        fig.subplots_adjust(bottom=0.25)  # Increase if legend is large
    "---"
    st.pyplot(fig)
    if visualize:
        st.markdown("""
        _The arrow in the plot indicates the head difference $h_{Riv}$-$h_{aq}$ respectively $h_{Riv}$-$h_{bot}$ and points to the resulting flow $Q_{Riv}$._
        """)

    "---"
    columns3 = st.columns((1,10,1), gap = 'medium')

    with columns3[1]:
        with st.expander('Click here to show **Parameters and Results**'):
            st.write("**Parameters and Results**")
            st.write("- Aquifer (MODFLOW) hydraulic head **$h_{aq}$ = %5.2f" %h_aq_show," m**")
            st.write("- River hydraulic head **$h_{RIV}$ = %5.2f" %h_RIV," m**")
            st.write("- River bottom elevation **$R_{bot}$ = %5.2f" %h_bot," m**")
            st.write("- Riverbed conductance **$C_{RIV}$ = % 10.2E"% st.session_state.C_RIV, " m²/s**")
            st.write("- Flow between river and aquifer **$Q_{RIV}$ = % 10.2E"% Q_ref," m³/s**")
    
    with st.expander('Show the :blue[**INITIAL INSTRUCTIONS**]'):
        st.markdown("""
        **Getting Started with the Interactive Plot**
        
        Before starting the exercise, follow these quick steps to explore RIV behavior:
        
        **1. Set a Reference Case**
        * Set river head $h_{riv} = 10.0$ m
        * Set river bottom elevation $R_{bot} = 9.0$ m
        * Vary aquifer head $h_{aq}$ between 8 and 12 m
        * Observe how the flow $Q_{RIV}$ changes:
            * When $h_{aq} > h_{riv}$, the aquifer discharges to the river (losing river).
            * When $h_{aq} < h_{riv}$ but $h_{aq} > R_{bot}$, the river recharges the aquifer (gaining river).
            * When $h_{aq} < R_{bot}$, the river is not longer in direct contact with the aquifer. Flow through an unsaturated zone occurs, which is driven between the head gradient between river stage and river bottom. In this case, outflow from the river is kept constant.
        
        **2. Test Different Conductance Values**
        * Use the slider to vary $C_{RIV}$
        * Note how the slope of the $Q$–$h$ curve changes — higher conductance allows more exchange.
        
        **3. Compute Conductance**
        * Toggle “Compute conductance”
        * Enter $K$, $A_{riv}$, and $L_{RIV}$ to calculate $C_{RIV} = \\frac{KA_{RIV}}{L_{RIV}}$
        * Observe how the conductance value influences the _Q_–_h_ relationship.
        * Set $h_{aq}$ < $R_{bot}$ and compute $C_{RIV}$ directly. Investigate the effect of the river bottom elevation $R_{bot}$ and river bed thickness $M_{RIV}$
        
        These steps help you build intuition for how RIV parameters control flow, a key foundation for the exercise. Feel free to further investigate the interactive plot on your own.
        """)
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        
        st.markdown("""
        
        🎯 **Expected Learning Outcomes**
        
        By completing this exercise, you will:
        
        * Understand how river–aquifer exchange is controlled by stage, aquifer head, bottom elevation, and conductance.
        * Interpret _Q_–_h_ plots in relation to gaining, losing, or inactive river segments.
        * Identify conditions that limit or enable flow across the riverbed.
        * Develop the ability to test and visualize river boundary behavior through scenario analysis.
    
        🛠️ **Instructions**
    
        Use the interactive RIV plot and complete the following steps:
        1. **Initial Exploration**
        
        * Set the **river head** ($h_{riv}$) to **10 m**
        * Set the **river bottom elevation** ($R_{bot}$) to **9 m**
        * Vary the **aquifer head** ($h_{aq}$) from **8 m to 12 m**
        * Observe and describe how the flow ($Q_{riv}$) changes.
        
        📝 Record:
        
            * Whether the river is gaining or losing in each case.
            * The conditions where no flow occurs.
            * The transition points between gaining/losing/inactive behavior.
    
        2. **Effect of Conductance**
    
        * Keep $h_{riv}$ = 10 m and $R_{bot}$ = 9 m
        * Choose three different conductance values (e.g., **1E-2, 1E-3, and 1E-4 m²/s**)
        * For each case:
            * Plot $Q_{RIV}$ vs $h_{aq}$ from 8 m to 12 m (on paper or spreadsheet)
            * Compare the slope of the curves and the magnitude of flow
            * Observe how low/high conductance limits flow exchange
        
        3. **Realistic Scenarios: Recession Flow**
        
        * Imagine a river with stage $h_{riv}$ **decreasing** from **11 m** to **9 m** (e.g., during a dry spell)
        * Set river bottom to **8.5 m**
        * Aquifer head is fixed at **9.2 m**
        
        💭 Explore:
        
            * How does the direction and magnitude of flow change as the river stage drops?
            * How does the bottom elevation restrict or allow recharge?
            * Discuss which condition (stage or bottom) dominates the system behavior    
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

st.subheader('✅ Conclusion', divider = 'violet')
st.markdown("""
The River (RIV) boundary condition is a powerful tool in MODFLOW for simulating dynamic interactions between surface water and groundwater. Unlike simpler boundary types, the RIV condition allows for **bidirectional flow** and introduces a **cutoff mechanism** when the aquifer head drops below the riverbed. In this case, RIV can capture the realistic behavior that occurs when a partially saturated zone separates the water table from the river bottom.

By adjusting parameters like **river stage**, **bed elevation**, and **conductance**, modelers can explore a wide range of hydrologic conditions, from **gaining** to **losing streams**, or even **no-flow scenarios**. Understanding these behaviors through Q–h plots supports stronger conceptual models and more reliable groundwater–surface water integration.

You're now ready to test your understanding in the final assessment.
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