import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_Boundary_Conditions_utils import read_md

# ---------- Track the current page
PAGE_ID = "DRN"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
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

st.title("Theory and Concept of :blue[Evapotranspiration in MODFLOW]")
st.subheader("Groundwater - :blue[Evapotranspiration] interaction", divider="blue")

st.markdown("""
#### 💡 Motivation: Why use Evapotranspiration (EVT) Boundaries?
""")

# Initial plot
# Slider input and plot
columns0 = st.columns((1,1), gap = 'large')

with columns0[0]:
    st.markdown("""   
    Consider these questions:
    
    1. **How does groundwater contribute to plant-water demand or surface evaporation from a shallow water table?**
    
    2. **Should evapotranspiration (ET) continue if the water table drops well below the land surface and root zone?**
    
    ▶️ The **EVT Boundary** in MODFLOW captures these dynamics. It simulates water loss from the saturated zone due to evapotranspiration **when the water table is near the surface or the root zone**.
    
    Evapotranspiration occurs at a **maximum defined rate when the groundwater head is at, or above, a specified ET surface elevation**. As the groundwater head drops below that surface, the **ET rate declines in a linear manner to zero when the head reaches a defined Extinction Depth ***EXDP*** below the ET surface**. More elaborate ET packages are available that allow functions other than direct linear decline of the rate with depth (e.g., ETS, RIP). The  following introductory interactive plot is based on the MODFLOW documentation (Harbaugh, 2005). Try adjusting the extinction depth to explore how ET demand varies with depth.
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
    h_gwi = np.linspace(0, 10, 100)
    
    #ET Surface elevation at 9 m
    SURFi = 9.0
    
    #convert rate in mm/yr per m^2 to  m^3/s/km^2
    EVTRi = QET_MAXi/31557.6

    RETi = np.where(h_gwi > SURFi, EVTRi, np.where(h_gwi >= (SURFi - EXDPi), EVTRi * (h_gwi - (SURFi - EXDPi)) / EXDPi, 0))

    QETi = RETi

    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 5    ))      
    ax.plot(h_gwi, QETi, label="$Q_{ET}$",color='black', linewidth=4)
    ax.set_xlabel("Head in the groundwater system (m)", fontsize=14, labelpad=15)
    ax.set_ylabel("ET loss from groundwater over a square kilometer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.02, 0.1)
    ax.set_title("Evapotranspiration loss", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    
    # Add vertical dashed line for drain elevation and annotation
    ax.axvline(x=SURFi, color='blue', linestyle=(0, (6, 4)), linewidth=2)
    ax.text(SURFi + 0.2, 0.045, r"ET Surface", color='blue', fontsize=14, verticalalignment='center',rotation=270)
    
    ax.axvline(x=(SURFi - EXDPi), color='blue', linestyle=(0, (4, 3)), linewidth=2)
    ax.text((SURFi - EXDPi) - 0.7, 0.03, r"Extinction Depth", color='blue', fontsize=14, verticalalignment='center',rotation=270)
    
    st.pyplot(fig)    
    
    st.markdown("""   
    **Initial Plot** for exploring how changes in :blue[EVT extinction depth] changes evapotranspiration. _The maximum ET rate for this example is 2,000 mm per year (i.e., 0.063 m³/km²/s), ET surface elevation is 9 m, and extinction depth is 4 m below the ET surface (i.e, an elevation of 5 m)_.
    
    This **initial plot** is designed to bridge the gap between traditional $Q$-$h$ plots on paper and the :rainbow[**interactive plots**] provided further down in this app, that allow you to explore the $Q$-$h$ relationships more intuitively, supported by interactive controls and guided instructions.
    """)
    
st.markdown("""
####  💻 How EVT may be Applied in Field-Scale Groundwater Modeling

The EVT package is particularly relevant in applied groundwater modeling at the field scale in settings with shallow groundwater where evapotranspiration can represent a significant component of groundwater discharge.
""")
left_co, cent_co, last_co = st.columns((10,40,10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/EVT_cartoon2.png', caption="Illustration of the concept for evapotranspiration from groundwater in MODFLOW.")
with st.expander("Tell me more about **the :blue[application of EVT in Field-Scale Groundwater Modeling]**"):
    st.markdown("""
    In field-scale groundwater models the EVT boundary may be used to define an elevation for the ET surface at every node of the model. Each ET surface elevation is accompanied by a value for extinction depth and a maximum ET rate that typically vary from cell to cell depending on the local conditions (e.g., type of soil, vegetation root depth). Often the ET surface elevation is the ground surface elevation, or an elevation slightly below the ground surface, such that the maximum evapotranspiration occurs when the water table is at or just below the surface. The water loss may reflect uptake by vegetation or direct evaporation from the water table. The complete hydrologic budget will include evapotranspiration of soil moisture, whereas the EVT boundary considers only the evapotranspiration from the saturated portion of the subsurface.
    
    As the groundwater model simulation proceeds through time, water levels in each cell rise and/or fall in response to stresses in the system. Water is discharged as evapotranspiration from each model node based on the groundwater head at the node, so the rate of evapotranspiration depends on other stresses in the model. As water levels decline, the rate of evapotranspiration decreases. When a drought occurs, there is less recharge from precipitation and surface water seepage, so water levels decline and the volume previously lost to evapotranspiration is reduced. Similarly, if irrigation pumping lowers groundwater heads, then there may be less evapotranspiration from the crop being irrigated. Thus, there can be some counterbalance when other mechanisms withdraw more water from the system causing water levels to decline, in that evapotranspiration may decrease offsetting the other losses.
    """)

st.markdown("""
####  🎯 Learning Objectives
This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual function of the EVT (Evapotranspiration) boundary condition in groundwater models.
- Apply the ET equation to describe how evapotranspiration varies with water table depth.
- Analyze the influence of the ET surface, the extinction depth, and the groundwater head on the actual evapotranspiration rates calculated by the ET equation.
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
    This section of the module shows the method for calculating the flow between the water surface in a hydrostratigraphic unit and the atmosphere as implemented by the EVT package in MODFLOW (Harbaugh, 2005). The rate of evapotranspiration depends on the elevation of groundwater head $h_{gw}$ relative to a modeler-specified maximum ET surface elevation ***SURF***. When the groundwater head $h_{gw}$ ≥ ***SURF***, evapotranspiration occurs at the maximum specified rate ***EVTR***. As the groundwater head declines, the evapotranspiration rate declines linearly to zero at a modeler specified extinction depth below the ***SURF*** elevation.""")

with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    The EVT package considers evapotranspiration from the saturated zone. The following figure illustrates the concept.
    """)
        
    left_co2, cent_co2, last_co2 = st.columns((10,40,10))
    with cent_co2:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_EVT.png', caption="Schematic of the EVT boundary (modified from MODFLOW6 documentation by Langevin et al., 2017)")
    
    st.markdown("""
    The approach accounts for the following parameters/measures:
    
    - ***EVTR*** = a user defined maximum evapotranspiration rate [L/T]
    - :green[***SURF*** = an elevation called _ET surface_ [L]: when groundwater head $h_{gw}$ ≥ ***SURF***, then the maximum evapotranspiration rate occurs]
    - :orange[***EXDP*** = _extinction depth_ [L]:  when groundwater head $h_{gw}$ < **SURF**-**EXDP**, then the evapotranspiration rate is zero. (_***EXDP*** is a distance below ***SURF*** and not an elevation._)]
    - ***RET*** = model-calculated, depth-specific evapotranspiration rate [L/T]which varies from ***EVTR*** to zero, declining linearly as groundwater head declines from **SURF** to a distance **EXDP** below **SURF**
    
    The evapotranspiration rate is as follows:
    
    - if heads is at, or above, the _ET surface_ (_**SURF**_), the evapotranspiration rate _**RET**_ is the user-defined maximum rate _**EVTR**_.
    """)
    st.latex(r'''\text{RET} = \text{EVTR}, \quad for \quad h_{gw} > \text{SURF}''')
    
    st.markdown("""
    - if head is lower than the distance _**EXDP**_ below the _ET surface_ (_**SURF**_), the evapotranspiration rate _**RET**_ from the groundwater is zero.
    """)
    st.latex(r'''\text{RET} = 0, \quad for  \quad h_{gw} < (\text{SURF} - \text{EXDP})''')
    
    st.markdown("""
    - between these two thresholds, evapotranspiration increases linearly from zero at the elevation equal to **SURF**-**EXDP** to **EVTR** at the _ET surface_ **SURF**.
    """)
    st.latex(r'''\text{RET} = \text{EVTR} \frac{h_{gw} - (\text{SURF} - \text{EXDP})}{\text{EXDP}}, \quad for  \quad (\text{SURF} - \text{EXDP}) \leq h_{gw} \leq \text{SURF}
    ''')
    
    st.markdown("""
    The volumetric discharge $Q_{ET}$ is computed by multiplying the evapotranspiration rate ***RET*** by the (cell) area $A$  ($\Delta x \Delta y$):
    """)
    st.latex(r'''Q_{ET} = RET A''')
    
st.subheader("Interactive Plot and Exercise", divider="blue")
st.markdown("""
    The interactive plot illustrates how the evapotranspiration loss $Q_{ET}$ varies with depth from the surface, depending on the defined **ET surface** (_**SURF**_), **extinction depth** (_**EXDP**_), and the **maximum ET rate** (_**EVTR**_). ET occurs only when the groundwater head $h_{gw}$ is within range of the surface — it drops linearly to zero below the extinction depth. 
    
    Below, under INPUT CONTROLS, in the **"Modify Plot Controls"** drop-down menu, you can toggle to: 1) turn the plot 90 degrees, 2) choose between slider or typed input to adjust the parameter values, and 3) make the plot "live" to switch from the static plot to the interactive plot. Under :blue[**"Modify Head & Elevations"**], you can adjust the value of ET surface elevation, extinction depth, and groundwater head elevation RELATIVE to a reference elevation of zero. Finally, under **"Modify ET rate"**, you define the Maximum ET rate. The plot updates dynamically and supports different viewing orientations.

    The interactive plot graphically displays the $Q$-$h$ relationship. When the toggle to visualize the input values is on, it includes a legend that provides the parameter values and graphically displays each parameter value, including a yellow arrow that indicates the value of (_**EXDP**_) and points to the value of flow $Q_{ET}$ on the axis.
    
    - You can investigate the plot on your own, perhaps using some of the :blue[**INSTRUCTIONS**] provided below the plot to guide you.
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
def update_h_gw_show():
    st.session_state.h_gw_show = st.session_state.h_gw_show_input  
    
# Initialize session state for value and toggle state
st.session_state.SURF = 9.0
st.session_state.EXDP = 4.0
st.session_state.EVTR_input = 2000.
st.session_state.h_gw_show = 8.0
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
        with st.expander("Modify the **Plot Controls**"):
            turn = st.toggle('Toggle to turn the plot 90 degrees', key="ET_turn", value=True)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of _SURF_, _EXDP_, and _EVTR_.")
            visualize = st.toggle(':rainbow[Visualize the input values]', key="ET_vis", value=True)
            # Time unit for rate - the user can choose between seconds, days, years through dropdown
            rate_unit = st.selectbox("Select unit for ET rate:", ["mm/yr", "mm/day", "m/s"], index=1)
            # Unit selection for area
            #area_unit = st.selectbox("Select area unit:", ["km²", "ha", "m²"], index=0)
            reset = st.button(':red[Reset the plot to the initial values]')
            if reset:
                st.session_state.SURF = 9.0
                st.session_state.EXDP = 4.0
                st.session_state.EVTR_input = 2000.
                st.session_state.h_gw_show = 8.0
                st.session_state.number_input = False

    with columns1[1]:
        with st.expander('Modify :blue[**Heads** & **Elevations**]'):
            if st.session_state.number_input:
                SURF = st.number_input(":green[**ET surface** _SURF_ (m)]", 7.0, 10.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
                EXDP = st.number_input(":orange[**Extinction depth** _EXDP_ (m)]", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
            else:
                SURF = st.slider(":green[**ET surface** _SURF_ (m)]", 7.0, 10.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
                EXDP = st.slider(":orange[**Extinction depth** _EXDP_ (m)]", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
            if st.session_state.number_input:
                h_gw_show = st.number_input(":blue[**Groundwater head** $h_{gw}$ (m)]", 0.0, 10.0, st.session_state.h_gw_show, 0.1, key="h_gw_show_input", on_change=update_h_gw_show)
            else:
                h_gw_show = st.slider      (":blue[**Groundwater head** $h_{gw}$ (m)]", 0.0, 10.0, st.session_state.h_gw_show, 0.1, key="h_gw_show_input", on_change=update_h_gw_show)      

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
    
    # Computation / Define groundwater head range
    h_gw = np.linspace(0, 10, 100)
    RET = np.where(h_gw > SURF, EVTR, np.where(h_gw >= (SURF - EXDP), EVTR * (h_gw - (SURF - EXDP)) / EXDP, 0))
    QET = RET*AREA
    # Compute RET and QET for specific evaluation elevation
    RET_eval = EVTR if st.session_state.h_gw_show > SURF else (EVTR * (st.session_state.h_gw_show - (SURF - EXDP)) / EXDP if st.session_state.h_gw_show >= (SURF - EXDP) else 0)
    QET_eval = RET_eval * AREA

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(QET, h_gw, label="$Q_{ET}$",color='blue', linewidth=4)
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
            ax.axhline(st.session_state.h_gw_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{gw}}$ = {st.session_state.h_gw_show:.2f} m')
            ax.plot(
                QET_eval, st.session_state.h_gw_show,
                marker='o',
                markersize=12,
                markeredgecolor='black',
                markerfacecolor='lightblue',
                label=f'$Q_{{ET}}$ at $h_{{gw}}$ = {QET_eval:.2e} m³/km²/s'
            )            
        else:
            ax.plot(h_gw, QET, label="$Q_{ET}$",color='blue', linewidth=4)
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
            ax.axvline(st.session_state.h_gw_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{gw}}$ = {st.session_state.h_gw_show:.2f} m')
            ax.plot(
                st.session_state.h_gw_show, QET_eval, 
                marker='o',
                markersize=12,
                markeredgecolor='black',
                markerfacecolor='lightblue',
                label=f'$Q_{{ET}}$ at $h_{{gw}}$ = {QET_eval:.2e} m³/km²/s'
            )   
    else:
        if turn:
            ax.plot(QET, h_gw, label="$Q_{ET}$",color='black', linewidth=4)
        else:
            ax.plot(h_gw, QET, label="$Q_{ET}$",color='black', linewidth=4)
        
    # Labels and formatting
    if turn:
        ax.set_ylabel("Heads and elevations in the groundwater system in m above reference level", fontsize=14, labelpad=15)
        ax.set_xlabel("ET loss from groundwater over a square kilometer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
        ax.set_ylim(0,10)
        ax.set_xlim(-0.1*QET_MAX, 1.1*QET_MAX)
        # Add second x-axis for different units
        if rate_unit == "mm/yr":
            secax = ax.secondary_xaxis('top', functions=(
                lambda x: x / 1000 * 86400 * 365.25,      # m³/km²/s -> mm/yr
                lambda x: x * 1000 / 86400 / 365.25       # mm/yr -> m³/km²/s
            ))
            secax.set_xlabel("Evapotranspiration rate from groundwater ($RET$) mm/yr", color = 'black', fontsize=14, labelpad=15)
        elif rate_unit == "mm/day":
            secax = ax.secondary_xaxis('top', functions=(
                lambda x: x / 1000 * 86400,        # m³/km²/s -> mm/d
                lambda x: x * 1000 / 86400         # mm/d -> m³/km²/s
            ))
            secax.set_xlabel("Evapotranspiration rate from groundwater ($RET$) mm/d", color = 'black', fontsize=14, labelpad=15)
        elif rate_unit == "m/s":
            secax = ax.secondary_xaxis('top', functions=(
#                lambda x: x / 1000000,        # m³/km²/s -> m/s
#                lambda x: x * 1000000         # m/s -> m³/km²/s
                lambda x: x / 0.1,        # m³/km²/s -> m/s
                lambda x: x * 0.1         # m/s -> m³/km²/s
            ))
            secax.set_xlabel("Evapotranspiration rate from groundwater ($RET$) m/s times 10⁻⁷", color = 'black', fontsize=14, labelpad=15)
        secax.tick_params(axis='x', labelsize=14)
    else:
        ax.set_xlabel("Heads and elevations in the groundwater system in m above reference level", fontsize=14, labelpad=15)
        ax.set_ylabel("ET loss from groundwater over a square kilometer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
        ax.set_xlim(0,10)
        ax.set_ylim(-0.1*QET_MAX, 1.1*QET_MAX)
        # Add second y-axis
        if rate_unit == "mm/yr":
            secax = ax.secondary_yaxis('right', functions=(
                lambda y: y / 1000 * 86400 * 365.25,      # m³/km²/s -> mm/yr
                lambda y: y * 1000 / 86400 / 365.25       # mm/yr -> m³/km²/s
            ))
            secax.set_ylabel("Evapotranspiration rate from groundwater ($RET$) mm/yr", color = 'grey', fontsize=14, labelpad=15)
        if rate_unit == "mm/day":
            secax = ax.secondary_yaxis('right', functions=(
                lambda y: y / 1000 * 86400,        # m³/km²/s -> mm/d
                lambda y: y * 1000 / 86400         # mm/d -> m³/km²/s
            ))
            secax.set_ylabel("Evapotranspiration rate from groundwater ($RET$) mm/d", color = 'grey', fontsize=14, labelpad=15)
        if rate_unit == "m/s":
            secax = ax.secondary_yaxis('right', functions=(
#                lambda y: y / 1000000,        # m³/km²/s -> mm/d
#                lambda y: y * 1000000         # mm/d -> m³/km²/s
                lambda y: y / 0.1,        # m³/km²/s -> mm/d
                lambda y: y * 0.1         # mm/d -> m³/km²/s
            ))
            secax.set_ylabel("Evapotranspiration rate from groundwater ($RET$) m/s times 10⁻⁷", color = 'grey', fontsize=14, labelpad=15)
        secax.tick_params(axis='y', labelsize=14)

    # === SHARED FORMATTING === #
    ax.set_title("Evapotranspiration loss", fontsize=16, pad=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.legend(fontsize=14)
    
    st.pyplot(fig)
    
    # Expander with "open in new tab"
    DOC_FILE1 = "Q_h_plot_EVT_instructions.md"
    with st.expander('Show the :blue[**INSTRUCTIONS**]'):
        st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE1}")
        st.markdown(read_md(DOC_FILE1))
        
    # Expander with "open in new tab"
    DOC_FILE2 = "Q_h_plot_EVT_exercise.md"
    with st.expander('Show the :rainbow[**EXERCISE**]'):
        st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE2}")
        st.markdown(read_md(DOC_FILE2))

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

st.subheader('✅ Conclusion', divider = 'blue')
st.markdown("""
The Evapotranspiration (EVT) boundary in MODFLOW simulates the loss of shallow groundwater to the atmosphere through vegetation uptake and surface evaporation. It simulates a **head-dependent** process that operates when the water table is within a defined range between the **ET surface** and **extinction depth**. The EVT boundary is defined over an area of a groundwater-flow model that may include only one or many cells. In a multilayer model, depending on the input specifications, ET may be drawn from deeper layers if the groundwater head falls below the bottom of overlying layers.

Q–h plots help us visualize how ET varies with groundwater depth — from maximum evapotranspiration to no evapotranspiration. This boundary type is especially relevant in arid or irrigated regions where shallow groundwater contributes to ET.

By understanding ET behavior, we can make groundwater models more representative of the field setting and better identify where water-table dynamics can critically affect water balance and sustainability.

MODFLOW boundary condition packages related to the EVT boundary package provide for more elaborate representation of the evapotranspiration process. These include the ETS, evapotranspiration segments package, that allows the slope of the function defining the rate of evapotranspiration with depth to vary; and the RIP, riparian evapotranspiration package, that allows definition of the spatial distribution of plant type and associated evapotranspiration behavior including the possible decrease in the evapotranspiration rate when groundwater head rises in cases where a high water table is detrimental to plants.

After studying this section about evapotranspiration boundaries, you may want to evaluate your knowledge using the final assessment.
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
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
