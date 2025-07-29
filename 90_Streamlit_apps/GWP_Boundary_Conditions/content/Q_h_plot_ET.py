import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from streamlit_book import multiple_choice

# path to questions for the assessments (direct path)
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_et.json"
path_quest_exer   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_et.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_et.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
# TODO:
# - allow user to plot rate / discharge 
# - adjust plot for discharge according to the max (rate x area)

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

st.title("Theory and Concept of :blue[Evapotranspiration in MODFLOW]")
st.subheader("Consideration of :blue[Evapotranspiration] on Groundwater", divider="blue")

st.markdown("""
#### 💡 Motivation: Why Evapotranspiration (ET) Boundaries?
""")

# Initial plot
# Slider input and plot
columns0 = st.columns((1,1), gap = 'large')

with columns0[0]:
    st.markdown("""   
    Think about these questions:
    
    1. **How does groundwater contribute to plant water demand or surface evaporation in shallow water table environments? Is there evapotranspiration from groundwater?**
    
    2. **Should evapotranspiration continue if the water table drops well below the root zone or land surface?**
    
    ▶️ The **ET Boundary** in MODFLOW captures these dynamics. It simulates water loss from the saturated zone due to evapotranspiration, **but only when the water table is near enough to the surface**. As the groundwater head drops below a defined extinction depth, the ET rate gradually reduces to zero. The following interactive plot helps to visualize this relationship. Adjust parameters like ET rate and extinction depth to explore how ET demand interacts with groundwater levels.
    """)

with columns0[1]:
    # EXPDi input
    EXDPi = st.slider("**Extinction depth (EXDP)**", 0.1, 5.0, 4.0, 0.1)  

    # Computation 
    QET_MAXi = 0.0005
    h_aqi = np.linspace(-10, 0, 100)
    SURFi = -1.0
    EVTRi = 2.0/86400000
    AREAi = 10000
    RETi = np.where(h_aqi > SURFi, EVTRi, np.where(h_aqi >= (SURFi - EXDPi), EVTRi * (h_aqi - (SURFi - EXDPi)) / EXDPi, 0))
    QETi = RETi*AREAi

    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5    ))      
    ax.plot(h_aqi, QETi, label="$Q_{ET}$",color='black', linewidth=4)
    ax.set_xlabel("Elevation below surface (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("ET loss from the aquifer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
    ax.set_xlim(0, -10)
    ax.set_ylim(-0.0001, 0.0005)
    ax.set_title("Evapotranspiration losses", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)    
    
    st.markdown("""   
    _Please note that the horizontal axis in the plot refers to elevation and not head_.
    """)
    
#TODO
st.markdown("""
####  🎯 Learning Objectives
By the end of this section, learners will be able to:
- Explain the conceptual function of the ET (Evapotranspiration) boundary condition in groundwater models.
- Apply the ET equation to describe how evapotranspiration varies with water table depth.
- Analyze the influence of the ET surface, the extinction depth, and the aquifer head on the actual evapotranspiration rates.
- Interpret the shape of _Q–h_-plots for the ET boundary and understand the limitations of this conceptualization.
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
            
st.subheader('🧪 Theory and Background', divider="blue")
st.markdown("""
This app shows the effect of evapotranspiration in removing water from an aquifer according to Harbaugh (2005) as it is implemented by the EVT package in MODFLOW.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    The EVT package consider only evapotranspiration from the saturated zone. The approach accounts for the following parameters/measures:
    - _**EVTR**_ = a user defined maximum evapotranspiration rate,
    - :green[_**SURF**_ = a specific elevation named _ET surface_ up to which the full evapotranspiration rate is acting],
    - _**RET**_ = the depth-specific evapotranspiration rate,
    - :orange[_**EXDP**_ = _extinction depth_ or cutoff depth (_**EXDP**_), where the evapotranspiration rate _**ETR**_ from the groundwater becomes zero.]
    
    The approach assumes:
    - if heads are above the _ET surface_ (_**SURF**_), the evapotranspiration rate _**RET**_ is the user-defined maximum rate _**EVTR**_.
    """)
    st.latex(r'''\text{RET} = \text{EVTR}, \quad h_{i,j,k} > \text{SURF}''')
    st.markdown("""
    - if heads are below the _ET surface_ (_**SURF**_) and exceeding the _extinction depth_ or cutoff depth (_**EXDP**_), the evapotranspiration rate _**ETR**_ from the groundwater becomes zero.
    """)
    st.latex(r'''\text{RET} = 0, \quad h_{i,j,k} < \text{SURF} - \text{EXDP}''')
    st.markdown("""
    - between these two thresholds, evapotranspiration increase linearly from the _extinction depth_ to the _ET surface_.
    """)
    st.latex(r'''\text{RET} = \text{EVTR} \frac{h_{i,j,k} - (\text{SURF} - \text{EXDP})}{\text{EXDP}}, \quad (\text{SURF} - \text{EXDP}) \leq h_{i,j,k} \leq \text{SURF}
    ''')
    st.markdown("""
    The volumetric discharge $Q_{ET}$ is computed by multiplying the evapotranspiration rate _**RET**_ by the (cell) area ($\Delta x \Delta y$):
    """)
    st.latex(r'''Q_{ET} = RET \Delta x \Delta y''')
    
st.subheader("Interactive Plot and Exercise", divider="blue")
st.markdown("""
The interactive plot illustrates how the evapotranspiration loss $Q_{ET}$ varies with depth from the surface (that eventually can be related to a **groundwater head** $h_{aq}$), depending on the defined **ET surface** (_**SURF**_), **extinction depth** (_**EXDP**_), and the **maximum ET rate** (_**EVTR**_). ET occurs only when the groundwater is within range of the surface — it drops linearly to zero below the extinction depth.

Use the sliders or number inputs to adjust parameters. You can also rotate the plot for a vertical or horizontal representation.

* You can explore the plot independently. Some :blue[INITIAL INSTRUCTIONS] may assist you.
* An :rainbow[EXERCISE] invites you to explore how _**SURF**_, _**EXDP**_, and _**EVTR**_ influence the _Q–h_ relationship and under what conditions ET becomes fully active, partially active, or negligible.
""")

# Functions

# Callback function to update session state
#SURF
#EXDP
#EVTR_input
def update_SURF():
    st.session_state.SURF = st.session_state.SURF_input
def update_EXDP():
    st.session_state.EXDP = st.session_state.EXDP_input
def update_EVTR_input():
    st.session_state.EVTR_input = st.session_state.EVTR_input_input
    
# Initialize session state for value and toggle state
st.session_state.SURF = -1.0
st.session_state.EXDP = 4.0
st.session_state.EVTR_input = 2.0

st.session_state.number_input = False  # Default to number_input

# Main area inputs
@st.fragment
def Q_h_plot():

    st.markdown("""
       #### :blue[INPUT CONTROLS]
        """)
        
    columns1 = st.columns((1,1,1), gap = 'small')
    # Switches
    with columns1[0]:
        with st.expander("Modify the Plot Control"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="ET_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of _SURF_, _EXDP_, and _EVTR_.")
            visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="ET_vis", value=True)

    with columns1[1]:
        with st.expander('Modify heads and elevations'):
            if st.session_state.number_input:
                SURF = st.number_input("**ET surface _SURF_**", -3.0, 0.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
                EXDP = st.number_input("**Extinction depth _EXDP_**", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
            else:
                SURF = st.slider("**ET surface _SURF_**", -3.0, 0.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
                EXDP = st.slider("**Extinction depth _EXDP_**", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
    
    with columns1[2]:
        with st.expander('Modify ET rate and area'):
            if st.session_state.number_input:
                EVTR_input = st.number_input("**Maximum Evapotranspiration rate (_EVTR_ in mm/d)**", 0.1, 20.0, st.session_state.EVTR_input, 0.1,key="EVTR_input_input", on_change=update_EVTR_input)
            else:
                EVTR_input = st.slider("**Maximum ET rate** (_EVTR_ in mm/d)", 0.1, 20.0, st.session_state.EVTR_input, 0.1,key="EVTR_input_input", on_change=update_EVTR_input)
            EVTR = EVTR_input/86400000
            AREA = st.number_input("**Area in $m^2$** (e.g., $\\Delta x \\Delta y$)", min_value=1.0, max_value=40000.0, value=10000.0, step=100.0)
    
    QET_MAX = 0.0005
    
    # Computation / Define aquifer head range
    h_aq = np.linspace(-10, 0, 100)
    RET = np.where(h_aq > SURF, EVTR, np.where(h_aq >= (SURF - EXDP), EVTR * (h_aq - (SURF - EXDP)) / EXDP, 0))
    QET = RET*AREA
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(QET, h_aq, label="$Q_{ET}$",color='blue', linewidth=4)
            ax.axhline(0, color='black', linewidth=5)
            ax.axhline(SURF, color='green', linestyle='--', label=f'$SURF$ in m = {SURF:5.2f} m')
            ax.axhline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP):5.2f} m')
            arrow_x = 0.8 * QET_MAX  # horizontal position
            arrow_y_start = SURF
            arrow_y_end = (SURF - EXDP)
            ax.annotate(
                '', 
                xy=(arrow_x, arrow_y_end),       # arrowhead
                xytext=(arrow_x, arrow_y_start), # arrow base
                arrowprops=dict(
                    arrowstyle='<->', color='orange', lw=3, alpha=0.7
                )
            )
            ax.text(
                arrow_x + 0.05 * QET_MAX,
                (arrow_y_start + arrow_y_end) / 2,
                "EXDP",
                color='black',
                fontsize=14,
                ha='left'
            )
             
            # Add head annotations
            ax.text(QET_MAX*0.9, SURF+0.2, "SURF", va='center',color='green',  fontsize=14)
        else:
            ax.plot(h_aq, QET, label="$Q_{ET}$",color='blue', linewidth=4)
            ax.axvline(0, color='black', linewidth=5)
            ax.axvline(SURF, color='green', linestyle='--', label=f'$SURF$ in m = {SURF:5.2f} m')
            ax.axvline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP):5.2f} m')
            
            arrow_y = 0.8 * QET_MAX  # horizontal position
            arrow_x_start = SURF
            arrow_x_end = (SURF - EXDP)
            ax.annotate(
                '', 
                xy=(arrow_x_end, arrow_y),       # arrowhead
                xytext=(arrow_x_start, arrow_y), # arrow base
                arrowprops=dict(
                    arrowstyle='<->', color='orange', lw=3, alpha=0.7
                )
            )
            ax.text(
                (arrow_x_start + arrow_x_end) / 2,
                arrow_y + 0.02 * QET_MAX,  # slight vertical offset
                "EXDP",
                color='black',
                fontsize=14,
                ha='center'
            )
            # Add head annotations
            ax.text(SURF-0.15, QET_MAX*0.95, "SURF", va='center',color='green',  fontsize=14)
    else:
        if turn:
            ax.plot(QET, h_aq, label="$Q_{ET}$",color='black', linewidth=4)
        else:
            ax.plot(h_aq, QET, label="$Q_{ET}$",color='black', linewidth=4)
        
    # Labels and formatting
    if turn:
        ax.set_ylabel("Elevations in the aquifer system in m above reference level", fontsize=14, labelpad=15)
        ax.set_xlabel("Evapotranspiration loss from the aquifer area ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
        ax.set_ylim(-10,0)
        ax.set_xlim(-0.1*QET_MAX, QET_MAX)
        
        # Add second x-axis (for mm/day)
        secax = ax.secondary_xaxis('top', functions=(
            lambda x: x / AREA * 86400 * 1000,        # m³/s -> mm/d
            lambda x: x * AREA / (86400 * 1000)       # mm/d -> m³/s
        ))
        secax.set_xlabel("Evapotranspiration loss rate from the aquifer ($RET$) in mm/d", color = 'grey', fontsize=14, labelpad=15)
        secax.tick_params(axis='x', labelsize=14)
    else:
        ax.set_xlabel("Elevations in the aquifer system in m above reference level", fontsize=14, labelpad=15)
        ax.set_ylabel("Evapotranspiration loss from the aquifer area ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
        ax.set_xlim(0,-10)
        ax.set_ylim(-0.1*QET_MAX, QET_MAX)
        # Add second y-axis (for mm/day)
        secax = ax.secondary_yaxis('right', functions=(
            lambda y: y / AREA * 86400 * 1000,        # m³/s -> mm/d
            lambda y: y * AREA / (86400 * 1000)       # mm/d -> m³/s
        ))
        secax.set_ylabel("Evapotranspiration loss rate from the aquifer ($RET$) in mm/d", color = 'grey', fontsize=14, labelpad=15)
        secax.tick_params(axis='y', labelsize=14)

    
    # === SHARED FORMATTING === #
    ax.set_title("Evapotranspiration losses", fontsize=16, pad=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.legend(fontsize=14)
    
    st.pyplot(fig)
    
    with st.expander('Show the :blue[**INITIAL INSTRUCTIONS**]'):
        st.markdown("""
        **Getting Started with the Interactive Plot**
        
        Before jumping into the exercise, follow these steps to understand how evapotranspiration (ET) interacts with the water table:
        
        **1. Visualize a Reference Case**
        
        * Set the **ET surface ($SURF$)** to –1.0 m a.s.l.
        * Set **extinction depth ($EXDP$)** to 3.0 m
        * Use an **ET rate ($EVTR$)** of 2.0 mm/day
        * Adjust the head from –5.0 m to 0.0 m and observe how $Q_{ET}$ changes:
          - Full ET occurs when $h_{aq} > SURF$
          - ET decreases linearly as $h_{aq}$ falls below $SURF$
          - ET becomes zero below $SURF - EXDP$
    
        **2. Analyze the Influence of EXDP**
        
        * Increase $EXDP$ gradually and observe how the slope of the Q–h curve flattens
        * Notice how the extinction point shifts further downward
    
        These quick tests build a foundation for the full exercise — feel free to explore additional combinations interactively.
        """)
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        st.markdown("""   
        🎯 **Expected Learning Outcomes**
        
        By completing this exercise, you will:
        
        - Understand the threshold-controlled behavior of the ET boundary condition
        - Distinguish between potential and actual ET based on groundwater head
        - Evaluate how extinction depth and surface elevation influence loss patterns
        - Relate evapotranspiration losses to aquifer sustainability
        
        🛠️ **Instructions**
        
        Use the interactive ET plot and complete the following steps:
        
        1. **Initial Setup**
        
        * Set $SURF$ = –1.0 m
        * Set $EXDP$ = 3.0 m
        * Use $EVTR$ = 2.0 mm/day
        * Vary aquifer head from –5.0 m to 0.0 m
        
        **Observe and record:**
        - The head at which ET reaches its maximum value
        - The head at which ET drops to zero
        - The shape of the Q–h curve between these thresholds
        
        2. **Test Sensitivity to Extinction Depth**
        
        * Keep $SURF$ fixed
        * Test $EXDP$ = 1.0, 3.0, and 5.0 m
        * Compare how the slope of the ET curve changes
        
        3. **Explore Surface Level Effects**
        
        * Fix $EXDP$ = 3.0 m
        * Set $SURF$ = –0.5 m, –1.0 m, –2.0 m
        * Observe how this shifts the entire ET response curve along the vertical axis
        
        💡 **Reflection:**
        - When is groundwater significantly contributing to ET?
        - What happens to ET during droughts or drawdowns?
        - How can extinction depth help represent different vegetation types or soil conditions?
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

st.subheader('✅ Conclusion', divider = 'blue')
st.markdown("""
The Evapotranspiration (ET) boundary in MODFLOW captures the loss of shallow groundwater to the atmosphere through plant uptake and surface evaporation. It simulates a **head-dependent** process that operates when the water table is within a defined range between the **ET surface** and **extinction depth**.

Using Q–h plots, you’ve visualized how actual ET varies with groundwater depth — from full potential extraction to zero loss. This boundary type is especially relevant in arid or irrigated regions where shallow groundwater contributes to ET.

Understanding ET behavior improves model realism and helps identify where water table dynamics can critically affect water balance and sustainability.
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
