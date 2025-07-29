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

st.title("Theory and Concept of the :green[Drain Boundary (DRN) in MODFLOW]")
st.subheader("Groundwater - :green[Drain] interaction", divider="green")

st.markdown("""
    #### 💡 Motivation: Why Drain Boundaries?
    """)

columns0 = st.columns((1,1), gap='large')
with columns0[0]:
    st.markdown("""      
    Consider these two questions:
    
    1. **How would you simulate a ditch, tile drain, or trench that only removes water from the aquifer when the water table is high enough?**
    
    2. **What if you want to stop flow when the groundwater falls below a certain level—like the bottom of the drain?** 
    
    ▶️ The :green[**Drain (DRN) Boundary**] in MODFLOW is designed for such features. It allows water to leave the aquifer only if the head in the cell $h_n$ exceeds the drain elevation $H_D$ —**no inflow is ever allowed**. The outflow $Q_{out}$ is computed with the drain conductance $C_D$ as: """)
    
    st.latex(r'''Q_{out} = C_{D} (H_{D} - h_{{aq}})''')
with columns0[1]:    
    # Slider input and plot
    # C_DRN
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
    container = st.container()  
    CDi_slider_value_new = st.slider      ("_(log of) Conductance_", -5.,-0., -2.5, 0.01, format="%4.2f")    
    CDi = 10 ** CDi_slider_value_new
    container.write("**:green[$C_D$]** in m²/s: %5.2e" %CDi) 
# Computation 
HDi = 8 
h_aqi = np.linspace(0, 20, 200)
Qi = np.where(h_aqi >= HDi, CDi * (HDi - h_aqi)*-1, 0)

# Create the plot
with columns0[1]:
    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, Qi, color='black', linewidth=4)
    ax.set_xlabel("Heads and elevations in the DRN-Aquifer System (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow out of the Groundwater \ninto the DRN boundary $Q_{DRN}$ (m³/s)", fontsize=14, labelpad=15)
    ax.set_xlim(0, 20)
    ax.set_ylim(0.05, -0.05)
    ax.set_title("Flow Between Groundwater and DRN", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)    
    
    st.markdown("""**FIG:** Explore with the initial plot how outflow varies for changes of the drain conductance.
    """)
#TODO
st.markdown("""
####  🎯 Learning Objectives
By the end of this tool, you will be able to:
- Explain the conceptual role of the Drain (DRN) boundary in simulating groundwater discharge to drainage features such as tile drains, trenches, or natural depressions.
- Apply the analytical relationship $Q_D = C_D(h_{aq}-H_D)$ to calculate boundary flows.
- Identify conditions under which the DRN boundary is active or inactive, and understand the role of the drain elevation in limiting flow.
- Evaluate the influence of aquifer head, drain elevation, and conductance on the magnitude and direction of drainage.
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
This app calculates the flow between  a model cell and a drain (DRN) depending on the drain elevation $H_D$ and the conductance $C_D$ between the boundary and the aquifer cell. The following figure illustrates the setup.""")
  
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    This app calculates the flow between  a model cell and a drain (DRN) depending on the drain elevation $H_D$ and the conductance $C_D$ between the boundary and the aquifer cell. The following figure illustrates the setup.""")
    
    left_co, cent_co, last_co = st.columns((10,80,10))
    with cent_co:
        st.image('06_Groundwater_modeling/FIGS/DRN.png', caption="Schematic illustration of the DRN boundary with a) drain pipe burried in backfill ditch, and b) open drain; modified from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")
    st.markdown("""
    The relationship between the amount of water that flows into the drain and the head in the aquifer is:
    """)
    
    st.latex(r'''Q_{out} = C_D (h_n-H_D)''')
    
    st.markdown("""
    where:
    - $Q_{out}$ is the flow from the aquifer into the drain [L3/T]
    - $H_D$ is the drain elevation (L),
    - $C_D$ is the drain conductance [L2/T], and
    - $h_n$ is the head in the cell that interacts with the drain (L).
    
    
    """)

st.subheader("Interactive Plot and Exercise", divider="green")
st.markdown("""
The interactive plot illustrates how the flow $Q_{DRN}$ across a Drain Boundary is driven by the **difference between aquifer head** ($h_{aq}$) and **drain elevation** ($H_D$), while being scaled by the **drain conductance** ($C_D$). Flow only occurs when the aquifer head exceeds the drain elevation, meaning the boundary acts as a one-way outlet.

Use the sliders or number inputs to adjust the parameters. You can toggle between direct conductance input or compute it based on hydraulic and geometrical properties. The plot updates dynamically and supports different viewing orientations.

* You can explore the plot independently. Some :blue[INITIAL INSTRUCTIONS] may assist you.
* An :rainbow[EXERCISE] invites you to investigate how **drain elevation, aquifer head, and conductance** govern outflow. Use the DRN plot to interpret the **Q–h relationship**, and understand under which conditions the drain is **active** or **inactive**, and how this affects groundwater discharge.
""")
with st.expander('Show the :blue[**INITIAL INSTRUCTIONS**]'):
    st.markdown("""
    **Getting Started with the Interactive Plot**
    
    Before starting the exercise, follow these quick steps to explore **DRN** behavior:
    
    **1. Set a Reference Case**
    
    * Set **drain elevation** $H_D$ to 10.0 m.
    * Vary **aquifer head** $h_{aq}$ between 8 and 12 m.
    * Observe how the flow $Q_D$ changes:
        * When $h_{aq} > H_D$, the aquifer drains — flow leaves the aquifer through the drain.
        * When $h_{aq} \leq H_D$, no flow occurs — the drain is inactive.
        
    **2. Test Different Conductance Values**
    
    * Use the slider to vary $C_D$
    * Note how the **slope of the Q–h curve** changes — higher conductance leads to stronger response of outflow to head differences.
    
    These steps help you build intuition for how DRN parameters govern flow — especially the **threshold behavior** and **linear relationship** between head difference and outflow. Feel free to further investigate the interactive plot on your own.
    """)

with st.expander('Show the :rainbow[**EXERCISE**]'):
    
    st.markdown("""   
    🎯 **Expected Learning Outcomes**
    
    By completing this exercise, you will:
    
    - Understand how drain–aquifer interaction is controlled by aquifer head, drain elevation, and conductance.
    - Interpret the boundary characteristics with a Q–h plot.
    - Recognize the threshold behavior of the DRN package and its role as a one-way boundary.
    - Evaluate how conductance controls the rate of drainage above threshold.
    - Analyze realistic scenarios (e.g., recession limbs of a hydrograph) and the implications for boundary fluxes.
    
    🛠️ **Instructions**
    
    Use the interactive DRN plot and complete the following steps:
    
    1. Initial Exploration
    
    - Set the drain elevation ($H_D$) to 10 m
    - Vary the aquifer head ($h_{aq}$) from 8 m to 12 m
    - Observe how the flow ($Q_D$) responds to changes in head

    📝 **Record:**
    - The threshold value at which the drain becomes active
    - The linearity of the Q–h relationship once the threshold is exceeded
    - The behavior of the drain when $h_{aq} \leq H_D$

    2. **Effect of Conductance**
    - Keep $H_D$ = 10 m
    - Choose three different conductance values (e.g., 1E-2, 1E-3, and 1E-4 m²/s)

    For each case:
    - Plot $Q_D$ vs $h_{aq}$ from 8 m to 12 m
    - Compare the slope of the Q–h curves
    - Discuss the sensitivity of flow to conductance changes

    3. **Realistic Scenario: Recession Segment**
    - Fix the aquifer head at 10.3 m
    - Vary drain elevation from 9.5 m to 10.5 m
    - Consider this as a stylized representation of a falling stream stage in a head-controlled system

    💡 **Explore:**
    - When does the drain become inactive?
    - How quickly does the flow decrease as $H_D$ rises above $h_{aq}$?
    - What are the management implications for shallow drainage systems during dry periods?
    """)
    
st.markdown("---")

# Functions

# Callback function to update session state
def update_CD():
    st.session_state.CD_slider_value = st.session_state.CD_input
def update_HD():
    st.session_state.HD = st.session_state.HD_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.CD_slider_value = -2.5
st.session_state.HD = 8.0
st.session_state.h_aq_show = 10.0

st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    columns1 = st.columns((1,1,1), gap = 'small')
    # Switches
    with columns1[0]:
        with st.expander("Modify the plot control"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="DRN_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_D$, $H_D$, and $h_{aq}$.")
            visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="DRN_vis", value=True)

    # Initialize st.session_state.C
    if "CD" not in st.session_state:
        st.session_state.CD = 10 ** st.session_state.CD_slider_value
    with columns1[1]:
        with st.expander('Modify heads and elevations'):
            if st.session_state.number_input:
                HD = st.number_input("**drain elevation ($H_D$)**", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
            else:
                HD = st.slider      ("**drain elevation ($H_D$)**", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
            if st.session_state.number_input:
                h_aq_show = st.number_input("**Aquifer head ($h_{aq}$)**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
            else:
                h_aq_show = st.slider      ("**Aquifer head ($h_{aq})$**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
    
    with columns1[2]:
        with st.expander('Modify the conductance'):
            # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
            container = st.container()  
            if st.session_state.number_input:
                CD_slider_value_new = st.number_input("_(log of) Conductance $C_D$ in m²/s_", log_min1,log_max1, st.session_state.CD_slider_value, 0.01, format="%4.2f", key="CD_input", on_change=update_CD)
            else:
                CD_slider_value_new = st.slider      ("_(log of) Conductance $C_D$ in m²/s_", log_min1,log_max1, st.session_state.CD_slider_value, 0.01, format="%4.2f", key="CD_input", on_change=update_CD)    
            st.session_state.CD = 10 ** CD_slider_value_new
            container.write("**Conductance $C_D$ in m²/s:** %5.2e" %st.session_state.CD)

    
    # Computation - Define aquifer head range
    h_aq = np.linspace(0, 20, 200)
    
    Q = np.where(h_aq >= HD, st.session_state.CD * (HD - h_aq)*-1, 0)
    Q_ref = st.session_state.CD * (HD - h_aq_show)*-1 if h_aq_show >= HD else 0   
        
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_D = C_D(H_D - h_{{aq}})$, $C_D$ = {st.session_state.CD:.2e}",color='green', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.axvline(0, color='black', linewidth=1)
            ax.axhline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m= {HD}')
            ax.axhline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow from the Ground-Water System into the DRN  $Q_{out}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(-0.05, 0.05)
            if Q_ref > 0:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HD),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
                )
            else:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HD),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
                )
            # Add gaining/losing stream annotations
            ax.text(0.005,1, "Gaining DRN boundary", va='center',color='blue')
            #ax.text(0.035, 1,  "Losing DRN boundary", va='center',color='green')
                
        else:
            ax.plot(h_aq, Q, label=rf"$Q_D = C_D(H_D - h_{{aq}})$, $C_D$ = {st.session_state.CD:.2e}",color='green', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_D$ = {Q_ref:.2e} m³/s")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m= {HD}')
            ax.axvline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the DRN Boundary-Aquifer System (m))", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow from the Ground-Water System into the DRN $Q_{out}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(0.05, -0.05)
            if Q_ref > 0:
                ax.annotate(
                    '',  # no text
                    xy=(HD, Q_ref),  # arrowhead
                    xytext=(h_aq_show, Q_ref),  # arrow start
                    arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
                )
            else:
                ax.annotate(
                '',  # no text
                xy=(HD, Q_ref),  # arrowhead
                xytext=(h_aq_show, Q_ref),  # arrow start
                arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
                )
            # Add losing drn annotations
            ax.text(0.5, 0.003, "Gaining DRN boundary", va='center',color='blue')
    else:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_o = C_D(H_D - h_{{aq}})$, $C_D$ = {st.session_state.CD:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow from the Ground-Water System into the DRN  $Q_{out}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(-0.05, 0.05)
        else:
            ax.plot(h_aq, Q, label=rf"$Q_o = C_D(H_D - h_{{aq}})$, $C_D$ = {st.session_state.CD:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow from the Ground-Water System into the DRN  $Q_{out}$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(0.05, -0.05)            
        
    # === SHARED FORMATTING === #     
    ax.set_title("Flow Between Groundwater and DRN boundary", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.legend(fontsize=14)
    
    st.pyplot(fig)

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
The Drain (DRN) boundary condition simulates discharge to external drains, ditches, or trenches — but only when groundwater levels are high enough to activate flow. This boundary introduces a **physical cutoff** based on the **drain elevation**, making it conceptually different from other head-dependent boundaries.

By exploring Q–h plots, you’ve seen how the discharge remains zero until the aquifer head exceeds the drain elevation, after which it increases linearly based on the conductance. This behavior supports the simulation of seepage faces and artificial drainage systems without over-extracting water from the model.

With this understanding, you’re ready to evaluate your knowledge in the final assessment.
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
