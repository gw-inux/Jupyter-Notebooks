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
#### 💡 Motivation: Why use Evapotranspiration (EVT) Boundaries?
""")

# Initial plot
# Slider input and plot
columns0 = st.columns((1,1), gap = 'large')

with columns0[0]:
    st.markdown("""   
    Think about these questions:
    
    1. **How does groundwater contribute to plant-water demand or surface evaporation from an aquifer with a shallow water table? Is there evapotranspiration from groundwater?**
    
    2. **Should evapotranspiration (ET) continue if the water table drops well below the land surface and root zone?**
    
    ▶️ The **EVT Boundary** in MODFLOW captures these dynamics. It simulates water loss from the saturated zone due to evapotranspiration, **when the water table is near the surface or root zone**.
    
    Evapotranspiration occurs at a **maximum defined rate when the groundwater head is at, or above, a modeler-defined ET surface elevation**. As the aquifer head drops below that surface, the **ET rate declines in a linear manner to zero when the head reaches a defined Extinction Depth ***EXDP*** below the ET surface**. More elaborate ET packages are available that allow functions other than direct linear decline of the rate with depth. The following interactive plot helps to (initially) visualize this relationship. Adjust the extinction depth to explore how ET demand varies with depth.
    """)

with columns0[1]:
#    # EXPDi / EVTRi input
#    col_ini = st.columns((1,1))
#    with col_ini[0]:
#        EXDPi = st.slider("**Extinction depth (EXDP)**", 0.1, 5.0, 4.0, 0.1)  
#    with col_ini[1]:
#        EVTRi = st.slider("**Max. ET rate**", 0.0, 4.0/86400000, 2.0/86400000, .1/86400000) 
    # EXPDi / EVTRi input
    EXDPi = st.slider("**Extinction depth (_EXDP_)**", 0.1, 5.0, 4.0, 0.1)
    
    # Computation 
    # max ET in mm/yr    
    QET_MAXi = 2000
    
    # Assuming head range from 0 to 10
    h_aqi = np.linspace(0, 10, 100)
    
    #ET Surface elevation at 9 m
    SURFi = 9.0
    
    #convert rate in mm/yr per m^2 to  m^3/s/km^2
    EVTRi = QET_MAXi/31557.6

    RETi = np.where(h_aqi > SURFi, EVTRi, np.where(h_aqi >= (SURFi - EXDPi), EVTRi * (h_aqi - (SURFi - EXDPi)) / EXDPi, 0))

    QETi = RETi

    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5    ))      
    ax.plot(h_aqi, QETi, label="$Q_{ET}$",color='black', linewidth=4)
    ax.set_xlabel("Head/Elevation in the EVT-aquifer system (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("ET loss from the aquifer ($Q_{ET}$) in m³/km²/s", fontsize=14, labelpad=15)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.02, 0.1)
    ax.set_title("Evapotranspiration losses", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)    
    
    st.markdown("""   
    **Initial Plot** for exploring how changes in :blue[EVT extinction depth] changes evapotranspiration. _The maximum ET rate for this example is defined as 2,000 mm per year and the maximum ET surface elevation is defined as 9 m_.
    
    This **initial plot** is designed to bridge the gap between traditional $Q$-$h$ plots on paper and the :rainbow[**interactive plots**] provided further down in this app, that allow you to explore the $Q$-$h$ relationships more intuitively, supported by interactive controls and guided instructions.
    """)
    
st.markdown("""
####  💻 How EVT may be Applied in Field-Scale Groundwater Modeling

The EVT package is particularly relevant in applied groundwater modeling at the field scale, especially in settings with shallow groundwater close to the surface, where evapotranspiration can represent a significant component of groundwater discharge.
""")
with st.expander("Show me more about **the :blue[application of EVT in Field-Scale Groundwater Modeling]**"):
    st.markdown("""
    In field-scale groundwater models the EVT boundary may be used to define an elevation for the ET surface at every node of the model. Each is accompanied by a value for extinction depth and a maximum ET rate that typically vary from cell to cell depending on the local conditions (e.g., type of soil, vegetation root depth). Often the ET surface elevation is the ground surface elevation or slightly below it such that the maximum evapotranspiration occurs when the water table is at or just below the surface. The water loss may reflect uptake by vegetation or direct evaporation from the water table. 
    
    As the groundwater model simulation proceeds through time, water levels in each cell rise and/or fall in response to stresses in the system and water is discharged as evapotranspiration from each model node based on the groundwater head at the node. There are connections between the rate of evapotranspiration at each node and other stresses in the model. As evapotranspiration occurs, water levels decline and the rate of evapotranspiration decreases. When a drought occurs, there is less recharge from precipitation and surface water seepage, so water levels decline and the volume previously lost to evapotranspiration is reduced. If irrigation pumping lowers groundwater heads, then there is less evapotranspiration.
    """)

#TODO
st.markdown("""
####  🎯 Learning Objectives
By the end of this section, learners will be able to:

- Explain the conceptual function of the EVT (Evapotranspiration) boundary condition in groundwater models.
- Apply the ET equation to describe how evapotranspiration varies with water table depth.
- Analyze the influence of the ET surface, the extinction depth, and the aquifer head on the actual evapotranspiration rates.
- Interpret the shape of _Q–h_-plots for the EVT boundary and understand the limitations of this conceptualization.
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

st.markdown("""
    This section of the module calculates the flow between the water surface in an aquifer and the atmosphere. The rate of evapotranspiration depends on the elevation of aquifer head $h_{aq}$ relative to a modeler specified maximum ET surface elevation ***SURF***. When the aquifer head $h_{aq}$ ≥ ***SURF***, evapotranspiration occurs at the maximum specified rate ***EVTR***. As the aquifer head declines, the evapotranspiration rate declines linearly to zero at a modeler specified extinction depth below the ***SURF*** elevation.""")

with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    The EVT package considers evapotranspiration from the saturated zone. The following figure illustrates the setup.
    """)
        
    left_co, cent_co, last_co = st.columns((10,40,10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_EVT.png', caption="Schematic illustration of the EVT boundary, modified from the [MODFLOW6 documentaion (Langevin et al., 2017)](https://doi.org/10.3133/tm6A55)")
    
    st.markdown("""
    The approach accounts for the following parameters/measures:
    
    - ***EVTR*** = a user defined maximum evapotranspiration rate
    - :green[***SURF*** = an elevation called _ET surface_: when aquifer head $h_{aq}$ ≥ ***SURF***, then the maximum evapotranspiration rate occurs]
    - :orange[***EXDP*** = _extinction depth_:  when aquifer head $h_{aq}$ < **SURF**-**EXDP**, then the evapotranspiration rate is zero. (_***EXDP*** is a distance below ***SURF*** and not an elevation._)]
    - ***RET*** = depth-specific evapotranspiration rate which varies from ***EVTR*** to zero, declining linearly as aquifer head declines from **SURF** to a distance **EXDP** below **SURF**
    
    The evapotranspiration rate is as follows:
    
    - if heads is at, or above, the _ET surface_ (_**SURF**_), the evapotranspiration rate _**RET**_ is the user-defined maximum rate _**EVTR**_.
    """)
    st.latex(r'''\text{RET} = \text{EVTR}, \quad for \quad h_{aq} > \text{SURF}''')
    
    st.markdown("""
    - if head is more than a distance _**EXDP**_ below the _ET surface_ (_**SURF**_) the evapotranspiration rate _**RET**_ from the groundwater is zero.
    """)
    st.latex(r'''\text{RET} = 0, \quad for  \quad h_{aq} < \text{SURF} - \text{EXDP}''')
    
    st.markdown("""
    - between these two thresholds, evapotranspiration increases linearly from zero at the elevation equal to **SURF**-**EXDP** to **EVTR** at the _ET surface_ **SURF**.
    """)
    st.latex(r'''\text{RET} = \text{EVTR} \frac{h_{aq} - (\text{SURF} - \text{EXDP})}{\text{EXDP}}, \quad for  \quad (\text{SURF} - \text{EXDP}) \leq h_{aq} \leq \text{SURF}
    ''')
    
    st.markdown("""
    The volumetric discharge $Q_{ET}$ is computed by multiplying the evapotranspiration rate ***RET*** by the (cell) area $A$  ($\Delta x \Delta y$):
    """)
    st.latex(r'''Q_{ET} = RET A''')
    
st.subheader("Interactive Plot and Exercise", divider="blue")
st.markdown("""
    The interactive plot illustrates how the evapotranspiration loss $Q_{ET}$ varies with depth from the surface (that eventually can be related to a **groundwater head** $h_{aq}$), depending on the defined **ET surface** (_**SURF**_), **extinction depth** (_**EXDP**_), and the **maximum ET rate** (_**EVTR**_). ET occurs only when the groundwater is within range of the surface — it drops linearly to zero below the extinction depth. 
    
    Below, under INPUT CONTROLS, in the **"Modify Plot Controls"** drop-down menu, you can toggle to: 1) turn the plot 90 degrees, 2) choose between slider or typed input to adjust the parameter values, and 3) make the plot "live" to switch from the static plot to the interactive plot. Under :blue[**"Modify Head & Elevations"**], you can adjust the value of ET surface elevation, extinction depth, and aquifer head elevation RELATIVE to a reference elevation of zero. Finally, under **"Modify ET rate"**, you define the Maximum ET rate. The plot updates dynamically and supports different viewing orientations.

    The interactive plot includes a legend that provides the parameter values. It also graphically displays the $Q$-$h$ relationship, each parameter value, and a yellow arrow that indicates the head difference $H_{D}$-$h_{aq}$ and points to the value of flow $Q_{ET}$ on the axis.
    
    - You can investigate the plot on your own, perhaps using some of the :blue[**INITIAL INSTRUCTIONS**] provided below the plot to guide you.
    - A subsequent :rainbow[**EXERCISE**] invites you to use the interactive plot to investigate how _**SURF**_, _**EXDP**_, and _**EVTR**_ influence the _Q–h_ relationship and the conditions for which ET becomes fully active, partially active, or negligible.
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
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.SURF = 9.0
st.session_state.EXDP = 4.0
st.session_state.EVTR_input = 2000.
st.session_state.h_aq_show = 8.0

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
        with st.expander("Modify the **Plot Control**"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="ET_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of _SURF_, _EXDP_, and _EVTR_.")
            visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="ET_vis", value=True)
            # Time unit for rate - the user can choose between seconds, days, years through dropdown
            rate_unit = st.selectbox("Select unit for ET rate:", ["mm/yr", "mm/day", "m/s"], index=1)
            # Unit selection for area
            #area_unit = st.selectbox("Select area unit:", ["km²", "ha", "m²"], index=0)          

    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Elevations**]'):
            if st.session_state.number_input:
                SURF = st.number_input(":green[**ET surface** _SURF_ (m)]", 7.0, 10.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
                EXDP = st.number_input(":orange[**Extinction depth** _EXDP_ (m)]", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
            else:
                SURF = st.slider(":green[**ET surface** _SURF_ (m)]", 7.0, 10.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
                EXDP = st.slider(":orange[**Extinction depth** _EXDP_ (m)]", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
            if st.session_state.number_input:
                h_aq_show = st.number_input(":blue[**Aquifer head** $h_{aq}$ (m)]", 0.0, 10.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
            else:
                h_aq_show = st.slider      (":blue[**Aquifer head** $h_{aq}$ (m)]", 0.0, 10.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)      

    with columns1[2]:
#        with st.expander('Modify **ET rate & Cell Area**'):
        with st.expander('Modify **ET rate**'):
            if st.session_state.number_input:
                EVTR_input = st.number_input("**Maximum ET rate** _EVTR_ (mm/yr)", 300., 4000., st.session_state.EVTR_input, 10.,key="EVTR_input_input", on_change=update_EVTR_input)
            else:
                EVTR_input = st.slider("**Maximum ET rate** _EVTR_ (mm/yr)", 300., 4000., st.session_state.EVTR_input, 10.,key="EVTR_input_input", on_change=update_EVTR_input)
#convert rate in mm/yr per m^2 to  m^3/s/km^2
            EVTR = EVTR_input/31557.6
            AREA = 1
     
    QET_MAX = 4000./31557.6
    
    # Computation / Define aquifer head range
    h_aq = np.linspace(0, 10, 100)
    RET = np.where(h_aq > SURF, EVTR, np.where(h_aq >= (SURF - EXDP), EVTR * (h_aq - (SURF - EXDP)) / EXDP, 0))
    QET = RET*AREA
    # Compute RET and QET for specific evaluation elevation
    RET_eval = EVTR if st.session_state.h_aq_show > SURF else (EVTR * (st.session_state.h_aq_show - (SURF - EXDP)) / EXDP if st.session_state.h_aq_show >= (SURF - EXDP) else 0)
    QET_eval = RET_eval * AREA

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(QET, h_aq, label="$Q_{ET}$",color='blue', linewidth=4)
            ax.axhline(0, color='black', linewidth=5)
            ax.axhline(SURF, color='green', linestyle='--', label=f'$SURF$ in m = {SURF:5.2f} m')
            ax.axhline((SURF-EXDP), color='red', linestyle='--', label=f'Expiration elevation in m = {(SURF-EXDP):5.2f} m')
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
                color='orange',
                fontsize=14,
                ha='left'
            )
             
            # Add head annotations
            ax.text(QET_MAX*0.9, SURF+0.2, "SURF", va='center',color='green',  fontsize=14)
            
            # Add evaluation point marker and label 
            ax.axhline(st.session_state.h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ = {st.session_state.h_aq_show:.2f} m')
            ax.plot(
                QET_eval, st.session_state.h_aq_show,
                marker='o',
                markersize=12,
                markeredgecolor='black',
                markerfacecolor='lightblue',
                label=f'$Q_{{ET}}$ at $h_{{aq}}$ = {QET_eval:.2e} m³/km²/s'
            )            
        else:
            ax.plot(h_aq, QET, label="$Q_{ET}$",color='blue', linewidth=4)
            ax.axvline(0, color='black', linewidth=5)
            ax.axvline(SURF, color='green', linestyle='--', label=f'$SURF$ in m = {SURF:5.2f} m')
            ax.axvline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP):5.2f} m')
            
            arrow_y = -0.05 * QET_MAX  # horizontal position
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
                color='orange',
                fontsize=14,
                ha='center'
            )
            # Add head annotations
            ax.text(SURF+0.15, QET_MAX*-0.05, "SURF", va='center',color='green',  fontsize=14)
            
            # Add evaluation point marker and label
            ax.axvline(st.session_state.h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ = {st.session_state.h_aq_show:.2f} m')
            ax.plot(
                st.session_state.h_aq_show, QET_eval, 
                marker='o',
                markersize=12,
                markeredgecolor='black',
                markerfacecolor='lightblue',
                label=f'$Q_{{ET}}$ at $h_{{aq}}$ = {QET_eval:.2e} m³/km²/s'
            )   
    else:
        if turn:
            ax.plot(QET, h_aq, label="$Q_{ET}$",color='black', linewidth=4)
        else:
            ax.plot(h_aq, QET, label="$Q_{ET}$",color='black', linewidth=4)
        
    # Labels and formatting
    if turn:
        ax.set_ylabel("Heads and elevations in the aquifer system in m above reference level", fontsize=14, labelpad=15)
        ax.set_xlabel("ET loss from the aquifer ($Q_{ET}$) in m³/km²/s", fontsize=14, labelpad=15)
        ax.set_ylim(0,10)
        ax.set_xlim(-0.1*QET_MAX, 1.1*QET_MAX)
        # Add second x-axis for different units
        if rate_unit == "mm/yr":
            secax = ax.secondary_xaxis('top', functions=(
                lambda x: x / 1000 * 86400 * 365.25,      # m³/km²/s -> mm/yr
                lambda x: x * 1000 / 86400 / 365.25       # mm/yr -> m³/km²/s
            ))
            secax.set_xlabel("Evapotranspiration loss rate from the aquifer ($RET$) in mm/yr", color = 'grey', fontsize=14, labelpad=15)
        elif rate_unit == "mm/day":
            secax = ax.secondary_xaxis('top', functions=(
                lambda x: x / 1000 * 86400,        # m³/km²/s -> mm/d
                lambda x: x * 1000 / 86400         # mm/d -> m³/km²/s
            ))
            secax.set_xlabel("Evapotranspiration loss rate from the aquifer ($RET$) in mm/d", color = 'grey', fontsize=14, labelpad=15)
        elif rate_unit == "m/s":
            secax = ax.secondary_xaxis('top', functions=(
                lambda x: x / 1000000,        # m³/km²/s -> m/s
                lambda x: x * 1000000         # m/s -> m³/km²/s
            ))
            secax.set_xlabel("Evapotranspiration loss rate from the aquifer ($RET$) in m/s", color = 'grey', fontsize=14, labelpad=15)
        secax.tick_params(axis='x', labelsize=14)
    else:
        ax.set_xlabel("Heads and elevations in the aquifer system in m above reference level", fontsize=14, labelpad=15)
        ax.set_ylabel("ET loss from the aquifer ($Q_{ET}$) in m³/km²/s", fontsize=14, labelpad=15)
        ax.set_xlim(0,10)
        ax.set_ylim(-0.1*QET_MAX, 1.1*QET_MAX)
        # Add second y-axis
        if rate_unit == "mm/yr":
            secax = ax.secondary_yaxis('right', functions=(
                lambda y: y / 1000 * 86400 * 365.25,      # m³/km²/s -> mm/yr
                lambda y: y * 1000 / 86400 / 365.25       # mm/yr -> m³/km²/s
            ))
            secax.set_ylabel("Evapotranspiration loss rate from the aquifer ($RET$) in mm/yr", color = 'grey', fontsize=14, labelpad=15)
        if rate_unit == "mm/day":
            secax = ax.secondary_yaxis('right', functions=(
                lambda y: y / 1000 * 86400,        # m³/km²/s -> mm/d
                lambda y: y * 1000 / 86400         # mm/d -> m³/km²/s
            ))
            secax.set_ylabel("Evapotranspiration loss rate from the aquifer ($RET$) in mm/d", color = 'grey', fontsize=14, labelpad=15)
        if rate_unit == "m/s":
            secax = ax.secondary_yaxis('right', functions=(
                lambda y: y / 1000000,        # m³/km²/s -> mm/d
                lambda y: y * 1000000         # mm/d -> m³/km²/s
            ))
            secax.set_ylabel("Evapotranspiration loss rate from the aquifer ($RET$) in m/s", color = 'grey', fontsize=14, labelpad=15)
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
        
        Before starting the exercise, it is helpful to follow these steps to understand how evapotranspiration (ET) interacts with the water table:
        
        **1. Set a Reference Case** - there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider 
        
        * Set the **ET surface** (_**SURF**_) to –1.0 m below the reference elevation
        * Set **extinction depth** (_**EXDP**_) to 3.0 m
        * Use an **ET rate** (_**EVTR**_) of 2.0 mm/day
        * Envision the aquifer head  $h_{aq}$ ranging from –5.0 m to 0.0 m below surface and acknowledge how $Q_{ET}$ changes:
          - ET is zero below _**SURF**_ - _**EXDP**_
          - ET increases linearly as $h_{aq}$ rises above _**SURF**_ - _**EXDP**_
          - Full ET occurs when $h_{aq}$ => _**SURF**_
          - Return  $h_{aq}$ to -3 m
    
        **2. Analyze the Influence of _EXDP_**
        
        * Increase _**EXDP**_ gradually and observe how the slope of the _Q–h_ curve flattens
        * Notice how $Q_{ET}$ changes
    
        These steps build a foundation for the full exercise. Feel free to interactively explore additional parameter value combinations.
        """)
    
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        st.markdown("""   
        🎯 **Expected Learning Outcomes**
        
        Completing this exercise helps you:
        
        - Understand the threshold-controlled behavior of the ET boundary condition
        - Evaluate how extinction depth and surface elevation influence the rate of evapotranspiration
        - Relate evapotranspiration losses to aquifer sustainability
        
        🛠️ **Instructions**
        
        Use the interactive ET plot and complete the following steps:
        
        1. **Initial Setup**
        
            * Set _**SURF**_ = –1.0 m
            * Set _**EXDP**_ = 3.0 m
            * Use _**EVTR**_ = 2.0 mm/day
            * Envision the aquifer head range from –5.0 m to 0.0 m
        
            **Observe and record:**
        
                * The head at which ET reaches its maximum value
                * The head at which ET drops to zero
                * The shape of the Q–h curve between these thresholds
        
        2. **Test Sensitivity to Extinction Depth**
        
            * Keep _**SURF**_ fixed at -1.0 m
            * Set "Evaluate ET at this elevation" to -1.5 m
            * Envision results for _**EXDP**_ = 1.0, 3.0, and 5.0 m
            * For each value of _**EXDP**_, observe the slope of the ET curve and the value of $Q_{ET}$ at -1.5 m
        
        3. **Explore ET Surface Elevation Effects**
        
            * Set and keep _**EXDP**_ = 3.0 m
            * Set "Evaluate ET at this elevation" to -1.5 m
            * Envision results for _**SURF**_ = –0.5 m, –1.0 m, –2.0 m
            * For each value of _**SURF**_, observe the slope of the ET curve and the value of $Q_{ET}$ at -1.5 m
            * Observe how this shifts the entire ET response curve along the vertical axis
        
        💡 **Reflection:**
        - When is groundwater significantly contributing to ET?
        - What happens to ET during droughts or drawdown due to pumping?
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
The Evapotranspiration (EVT) boundary in MODFLOW simulates the loss of shallow groundwater to the atmosphere through vegetation uptake and surface evaporation. It simulates a **head-dependent** process that operates when the water table is within a defined range between the **ET surface** and **extinction depth**.

Q–h plots help us visualize how ET varies with groundwater depth — from maximum evapotranspiration to no evapotranspiration loss. This boundary type is especially relevant in arid or irrigated regions where shallow groundwater contributes to ET.

By understanding ET behavior, we can make groundwater models more representative of the field setting and better identify where water-table dynamics can critically affect water balance and sustainability.
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
