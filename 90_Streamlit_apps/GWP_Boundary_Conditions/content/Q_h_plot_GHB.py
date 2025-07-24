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

st.title("Theory and Concept of the :orange[General Head Boundary (GHB) in MODFLOW]")
#st.subheader("Interaction Between Groundwater and Head-Dependent Boundaries", divider="orange")
st.subheader("Groundwater - :orange[Head-Dependent Boundary] interaction", divider="orange")

st.markdown("""
#### 💡 Motivation: Why General Head Boundaries?
""")

columns0 = st.columns((1,1), gap = 'large')

with columns0[0]:
    st.markdown(""" 
    Before jumping into equations and applications, consider:
    
    1. **How would you represent a distant river or lake that interacts with groundwater but lies outside your model domain?**
    2. **Can a boundary both add to and remove water from the aquifer — depending on heads?**
    
    ▶️ The :orange[**General Head Boundary (GHB)**] addresses these situations. It allows for dynamic, head-dependent exchange with an external water body. The following interactive plot illustrates how the flow $Q_B$ depends on the aquifer head $h_{aq}$ for a fixed boundary head $H_B$ and conductance $C_B$. The interactive plot is based on the MODFLOW documentation (Harbaugh, 2005) and consider **$H_B$ as 8 m**. Modify the conductance $C_B$ to see its effect.
    """)
    
    st.latex(r'''Q_B = C_B(H_B - h_{aq})''')

# Initial plot
# fixed values
HBi = 8.0

# Initialize session state for value and toggle state
st.session_state.Ci_slider_value = -2.5
if "Ci" not in st.session_state:
    st.session_state.Ci = 10 ** st.session_state.Ci_slider_value

with columns0[1]:
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
    container = st.container()  
    Ci_slider_value_new = st.slider("_(log of) Conductance $C_B$ in m²/s_", -5.,-0., -2.5, 0.01, format="%4.2f")    
    st.session_state.Ci = 10 ** Ci_slider_value_new
    container.write("**:orange[$C_B$]** in m²/s: %5.2e" %st.session_state.Ci)

    # Define aquifer head range
    h_aqi = np.linspace(0, 20, 200)
    Qi = st.session_state.Ci * (HBi - h_aqi)

    fig, ax = plt.subplots(figsize=(5, 5))      
    ax.plot(h_aqi, Qi, color='black', linewidth=4)
    ax.set_xlabel("Heads in the GHB-Aquifer System (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("Flow Into the Groundwater \nfrom the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.05, 0.05)
    ax.set_title("Flow Between Groundwater and GHB", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)

st.markdown("""
#### 🎯 Learning Objectives
By the end of this section of the module, you will be able to:

- Explain the conceptual function and mathematical formulation of a General Head Boundary (GHB).
- Apply the GHB equation $Q_B = C_B(H_B - h_{aq})$ to calculate boundary flows and analyze flow directions.
- Evaluate how conductance, aquifer head, and boundary head jointly affect the groundwater–boundary exchange.
- Visualize flow directions and boundary behavior (gaining vs. losing) under different conditions.
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
The General Head Boundary (GHB), also referred to as the Head-Dependent Flux Boundary in MODFLOW, allows for a more realistic simulation of boundary conditions by enabling **exchange with an external reservoir**. In groundwater models, General Head Boundaries are used to simulate hydraulic interaction with an external water body or zones with a defined (fixed) head. The conductance term determines how easily water can flow across the boundary.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
        Unlike defined head boundaries, the GHB responds to changes in aquifer head. It is governed by a linear relationship:
        
        $$
        Q_B = C_B(H_B - h_{aq})
        $$
        
        where:
        - $Q_B$ is the flow between the GHB and the aquifer, taken as positive if it is directed into the aquifer [L3/T]
        - $H_B$ is the boundary head [L], representing e.g., an external water level like a distant lake,
        - $C_B$ is the hydraulic conductance of the GHB-aquifer interconnection [L2/T], which encapsulates **geometry and material properties**, and
        - $h_{aq}$ is the head [L] in the model cell where the GHB boundary is active.
        
        The conductance is
        
        $$
        C_B = \\frac{K A_B}{L_B}
        $$
        
        where:
        - $K$: Hydraulic conductivity [m/s],
        - $A_B$: Cross-sectional area of the interconnection [m²],
        - $L_B$: Length of flow path between aquifer and boundary [m].
        
        The following figure illustrates the setup.
        """)
        
    left_co, cent_co, last_co = st.columns((10,80,10))
    with cent_co:
        st.image('06_Groundwater_modeling/FIGS/GHB.png', caption="Schematic illustration of the GHB boundary, modified from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

st.subheader("📈 Interactive Plot and Exercise", divider="orange")
st.markdown("""
    The interactive plot shows how the flow $Q_B$ across a General Head Boundary depends on the difference between aquifer head ($h_{aq}$) and boundary head ($H_B$), and on the conductance ($C_B$). 
    
    Use the sliders or number inputs to adjust these parameters. You can also toggle between direct conductance input or compute it from hydraulic properties. The plot updates dynamically and supports different viewing orientations.
    
    - You can investigate the plot on your own. Some :blue[**INITIAL INSTRUCTIONS**] may guide you.
    - An :rainbow[**EXERCISE**] allows you to apply the plot and to deepen your understanding. This exercise invites you to investigate how the conductance parameter and the difference in head affect the boundary flux. Use the interactive GHB plot to explore how variations in conductance influence the exchange flux between an aquifer and a connected boundary condition, and to interpret physical meaning based on Q–h plots.
""")

with st.expander('Show the :blue[**INITIAL INSTRUCTIONS**]'):
    st.markdown("""
    **Getting Started with the Interactive Plot**
    
    Before starting the exercise, follow these quick steps to explore GHB behavior:

    **1. Set a Reference Case**

    * Set **boundary head $H_B$ = 10.0 m**.
    * Vary **aquifer head $h_{aq}$** between 5 and 15 m.
    * Observe how **flow $Q_B$** changes.
    * Investigate that 
        * A gaining GHB removes water from the aquifer (Q < 0) and
        * A losing GHB adds water to the aquifer (Q > 0).  

    **2. Test Different Conductance Values**

    * Use the slider to vary $C_B$.
    * Note how the **slope of the $Q$–$h$ curve** changes.

    **3. Optional: Compute Conductance**

    * Toggle “Compute conductance”.
    * Enter $K$, $A_B$, and $L_B$ to calculate $C_B = \\frac{K A_B}{L_B}$.
    * Note how the **slope of the $Q$–$h$ curve** changes.

    These steps help you build intuition for how GHB parameters control flow, a key foundation for the exercise. Feel free to further investigate the interactive plot on your own.
    """)

with st.expander('Show the :rainbow[**EXERCISE**]'):
    
    st.markdown("""
    
    🎯 **Expected Learning Outcomes**
    
    By completing this exercise, you will:
    
    * Understand how GHB flux is driven by head difference and conductance.
    * Interpret Q–h plots in relation to the hydrogeologic behavior.
    * Develop the ability to use the app for conceptual testing and scenario analysis.
   
    🛠️ **Instructions**
    
    Use the interactive GHB plot and complete the following:
    
    1. **Initial Exploration**
    
    * Set the boundary head (`H_B`) to **10 m**.
    * Vary the aquifer head (`h_aq`) from **5 m to 15 m**.
    * Observe and describe how the flux (`Q`) changes.
    * Record:
    
      * The sign of the flux for different `h_aq` values.
      * The value of `Q` when `h_aq = h_GHB`.
    
    2. **Conductance Effect**
    
    * (Keep `H_B` at 10 m)
    * Choose three different conductance values (e.g., **3E-2, 3E-3, and 3E-4 m²/s**).
    * For each conductance value:
    
      * Plot (e.g., on a separate paper) `Q_B` vs `h_aq` for `h_aq` in the range from 5 to 15 m.
      * Compare the slope and shape of the resulting lines.
      * Eventually repeat with an increased/decreased `H_B`
    
    3. **Realistic Scenarios**
    
    * Imagine a GHB represents a canal system connected to the aquifer. The canal water level is 10 m.
    * Assume the aquifer head starts at 8 m.
    * Evaluate how much water would enter the aquifer for:
    
      * A poorly connected canal (low conductance).
      * A well-connected canal (high conductance).
    * Discuss the implications for water management.    
    """)

st.markdown('---')
# Functions

# Callback function to update session state
def update_C():
    st.session_state.C_slider_value = st.session_state.C_input
def update_K():
    st.session_state.K_slider_value = st.session_state.K_input
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
st.session_state.C_slider_value = -2.5
st.session_state.K_slider_value = -3.5
st.session_state.LB = 100.
st.session_state.AB = 1000.0
st.session_state.HB = 8.0
st.session_state.stage = 2.0
st.session_state.h_aq_show = 10.0

st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    # Input widgets

    st.markdown("#### :orange[Model parameters]")
    
    columns1 = st.columns((1,1,1), gap = 'small')
    
    
    # Initialize st.session_state.C
    if "C" not in st.session_state:
        st.session_state.C = 10 ** st.session_state.C_slider_value
    
    with columns1[0]:
        with st.expander('Modify the plot control'):
            visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="GHB_vis")
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="GHB_turn")
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_B$, $H_B$, $A_B$, $L_B$, and $h_{aq}$.")
            
            
    with columns1[1]:
        with st.expander('Modify heads and elevations'):
            if st.session_state.number_input:
                HB = st.number_input("**GHB head ($H_B$)**", 5.0, 20.0, st.session_state.HB, 0.1, key="HB_input", on_change=update_HB)
            else:
                HB = st.slider      ("**GHB head ($H_B$)**", 5.0, 20.0, st.session_state.HB, 0.1, key="HB_input", on_change=update_HB)
            if st.session_state.number_input:
                h_aq_show = st.number_input("**Aquifer head ($h_{aq}$)**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
            else:
                h_aq_show = st.slider      ("**Aquifer head ($h_{aq})$**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)            
            
    with columns1[2]:
        with st.expander('Modify the conductance'):
            # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
            c_computed = st.toggle('Toggle to compute conductance')
            if c_computed:
                container = st.container()  
                if st.session_state.number_input:
                    K_slider_value_new = st.number_input("_(log of) Hydraulic conductivity $K_B$ in m/s_", log_min1,log_max1, st.session_state.K_slider_value, 0.01, format="%4.2f", key="K_input", on_change=update_K)
                else:
                    K_slider_value_new = st.slider      ("_(log of) Hydraulic conductivity $K_B$ in m/s_", log_min1,log_max1, st.session_state.K_slider_value, 0.01, format="%4.2f", key="K_input", on_change=update_K)   
                K = 10 ** K_slider_value_new
                container.write("**Hydraulic conductivity $K_B$ in m/s:** %5.2e" %K)
                if st.session_state.number_input:
                    LB = st.number_input("**GHB lenght ($L_B$)**", 1.0, 10000.0, st.session_state.LB, 1., key="LB_input", on_change=update_LB)
                else:
                    LB = st.slider      ("**GHB lenght ($L_B$)**", 1.0, 10000.0, st.session_state.LB, 1., key="LB_input", on_change=update_LB)
                if st.session_state.number_input:
                    AB = st.number_input("**GHB area ($A_B$)**", 1.0, 100000.0, st.session_state.AB, 1., key="AB_input", on_change=update_AB)
                else:
                    AB = st.slider      ("**GHB area ($A_B$)**", 1.0, 100000.0, st.session_state.AB, 1., key="AB_input", on_change=update_AB)
                st.session_state.C = K * AB / LB
                
                # Update C_slider_value based on computed values
                st.session_state.C_slider_value = np.log10(st.session_state.C)
            else:
                container = st.container()  
                if st.session_state.number_input:
                    C_slider_value_new = st.number_input("_(log of) Conductance $C_B$ in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)
                else:
                    C_slider_value_new = st.slider      ("_(log of) Conductance $C_B$ in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)    
                st.session_state.C = 10 ** C_slider_value_new
                container.write("**Conductance $C_B$ in m²/s:** %5.2e" %st.session_state.C)
                
                # Update K_slider_value based on computed values
                st.session_state.K_slider_value = np.log10(st.session_state.C * st.session_state.LB / st.session_state.AB)

    
    # Define aquifer head range
    h_aq = np.linspace(0, 20, 200)
    Q = st.session_state.C * (HB - h_aq)
    Q_ref = st.session_state.C * (HB - h_aq_show)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='orange', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_B$ = {Q_ref:.2e} m³/s")
            ax.axvline(0, color='black', linewidth=1)
            ax.axhline(HB, color='green', linewidth=2, linestyle='--', label=f'$H_B$ in m= {HB}')
            ax.axhline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
            
            # Labels and formatting
            ax.set_ylabel("Heads in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05, -0.05)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HB),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
                )
            else:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HB),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
                )
            # Add gaining/losing stream annotations
            ax.text(-0.003,1, "Gaining GHB", va='center',color='blue',  fontsize=16)
            ax.text(0.002, 1,  "Losing GHB", va='center', ha='right',color='green',  fontsize=16)
                
        else:
            ax.plot(h_aq, Q, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='orange', linewidth=3)
            ax.plot([], [], ' ', label=fr"$Q_B$ = {Q_ref:.2e} m³/s")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(HB, color='green', linewidth=2, linestyle='--', label=f'$H_B$ in m= {HB}')
            ax.axvline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')

            # Labels and formatting
            ax.set_xlabel("Heads in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(HB, Q_ref),  # arrowhead
                    xytext=(h_aq_show, Q_ref),  # arrow start
                    arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
                )
            else:
                ax.annotate(
                '',  # no text
                xy=(HB, Q_ref),  # arrowhead
                xytext=(h_aq_show, Q_ref),  # arrow start
                arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
                )
            # Add gaining/losing stream annotations
            ax.text(19.8, -0.003, "Gaining GHB", va='center', ha='right',color='blue',  fontsize=16)
            ax.text(19.8, 0.003, "Losing GHB", va='center', ha='right',color='green',  fontsize=16)
    else:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_ylabel("Heads in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05,-0.05)
        else:        
            ax.plot(h_aq, Q, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_xlabel("Heads in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
   
   # === SHARED FORMATTING === #        
    ax.set_title("Flow Between Groundwater and GHB", fontsize=16, pad=10)
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



st.subheader('✅ Conclusion', divider = 'orange')
st.markdown("""
The General Head Boundary (GHB) offers a flexible way to simulate interactions with external water bodies or regions not explicitly modeled — such as distant lakes, rivers, or adjacent aquifer systems. Its formulation as a **head-dependent boundary** enables both **inflow and outflow**, depending on the head difference between the model cell and the boundary.

The GHB condition captures the essential physics of cross-boundary exchange using only a few parameters: the **boundary head**, **aquifer head**, and **conductance**, which reflects the geometry and hydraulic properties of the connection.

By analyzing **Q–h plots**, you've gained a clearer understanding of how conductance controls the slope of the exchange curve and how head differences dictate the flow direction. This conceptual insight is essential for setting realistic boundary conditions in MODFLOW models.

You're now ready to assess your understanding of GHB behavior in the final quiz.
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
