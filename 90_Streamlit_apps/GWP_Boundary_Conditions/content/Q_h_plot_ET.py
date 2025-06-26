import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
    
    1. **How does groundwater contribute to plant water demand or surface evaporation in shallow water table environments?**
    
    2. **Should evapotranspiration continue if the water table drops well below the root zone or land surface?**
    
    ▶️ The **ET Boundary** in MODFLOW captures these dynamics. It simulates water loss from the saturated zone due to evapotranspiration—**but only when the water table is near enough to the surface**. As the groundwater head drops below a defined extinction depth, the ET rate gradually reduces to zero. The interactive plot below helps visualize this relationship. Adjust parameters like ET rate and extinction depth to explore how ET demand interacts with groundwater levels.
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
    ax.set_ylabel("Evapotranspiration loss from the aquifer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
    ax.set_xlim(0, -10)
    ax.set_ylim(-0.0001, 0.0005)
    ax.set_title("Evapotranspiration losses", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
    st.pyplot(fig)    
    
#TODO
st.markdown("""
####  🎓 Learning Objectives
By the end of this tool, you will be able to:
- Explain the conceptual function of a General Head Boundary (GHB) in groundwater models.
- Apply the analytical equation $Q_B = C_B(H_B - h_{aq})$ to calculate boundary flows.
- Evaluate the influence of conductance, boundary head, and aquifer head on exchange fluxes.
- Visualize flow directions and boundary behavior (gaining vs. losing) under different conditions.
- Understand the physical interpretation of conductance and its dependence on system geometry and hydraulic conductivity.
""")

st.subheader('🧪 Theory and Background', divider="blue")
st.markdown("""
This app shows the effect of evapotranspiration in removing water from an aquifer according to Harbaugh (2005) as it is implemented by the EVT package in MODFLOW.
""")
with st.expander("Show me more about **the Theory**"):
    st.markdown("""
    The EVT package consider only evapotranspiration from the saturated zone. The approach considers the following parameters/measures:
    - $EVTR$ = a user defined maximum evapotranspiration rate,
    - :green[$SURF$ = a specific elevation named _ET surface_ up to which the full evapotranspiration rate is acting],
    - $RET$ = the depth-specific evapotranspiration rate,
    - :orange[$EXDP$ = _extinction depth_ or cutoff depth ($EXDP$), where the evapotranspiration rate $ETR$ from the groundwater becomes zero.]
    
    The approach assumes:
    - if heads are above the _ET surface_ ($SURF$), the evapotranspiration rate $RET$ is the user-defined maximum rate $EVTR$
    """)
    st.latex(r'''\text{RET} = \text{EVTR}, \quad h_{i,j,k} > \text{SURF}''')
    st.markdown("""
    - if heads are below the _ET surface_ ($SURF$) and exceeding the _extinction depth_ or cutoff depth ($EXDP$), the evapotranspiration rate $ETR$ from the groundwater becomes zero.
    """)
    st.latex(r'''\text{RET} = 0, \quad h_{i,j,k} < \text{SURF} - \text{EXDP}''')
    st.markdown("""
    - between these two thresholds, evapotranspiration increase linearly from the _extinction depth_ to the _ET surface_.
    """)
    st.latex(r'''\text{RET} = \text{EVTR} \frac{h_{i,j,k} - (\text{SURF} - \text{EXDP})}{\text{EXDP}}, \quad (\text{SURF} - \text{EXDP}) \leq h_{i,j,k} \leq \text{SURF}
    ''')
    st.markdown("""
    The volumetric discharge is computed by multiplying the evapotranspiration rate $RET$ by the cell area $\Delta x \Delta y$:
    """)
    st.latex(r'''Q_{ET} = RET \Delta x \Delta y''')

st.subheader("Interactive plot", divider="blue")
st.markdown("""
The interactive plot allows you to investigate $Q_{ET}$ in dependence from the _ET surface_ and the _extinction depth_. You can turn the plot by using the toggle above the input widgets.
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

    turn = st.toggle('Toggle to turn the plot 90 degrees', key="ET_turn")
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $SURF$, $EXDP$, and $EVTR$.")
    visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="ET_vis")
    
    columns1 = st.columns((1,1), gap = 'large')
    with columns1[0]:
        if st.session_state.number_input:
            SURF = st.number_input("**ET surface $SURF$**", -3.0, 0.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
            EXDP = st.number_input("**Extinction depth $EXDP$**", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
        else:
            SURF = st.slider("**ET surface $SURF$**", -3.0, 0.0, st.session_state.SURF, 0.1,key="SURF_input", on_change=update_SURF)
            EXDP = st.slider("**Extinction depth $EXDP$**", 0.1, 5.0, st.session_state.EXDP, 0.1,key="EXDP_input", on_change=update_EXDP)
    
    with columns1[1]:
        if st.session_state.number_input:
            EVTR_input = st.number_input("**Maximum Evapotranspiration rate ($EVTR$ in mm/d)**", 0.1, 20.0, st.session_state.EVTR_input, 0.1,key="EVTR_input_input", on_change=update_EVTR_input)
        else:
            EVTR_input = st.slider("**Maximum Evapotranspiration rate ($EVTR$ in mm/d)**", 0.1, 20.0, st.session_state.EVTR_input, 0.1,key="EVTR_input_input", on_change=update_EVTR_input)
        EVTR = EVTR_input/86400000
        AREA = st.number_input("**Cell Area ($\\Delta x \\Delta y$) in m2**", min_value=1.0, max_value=40000.0, value=10000.0, step=100.0)
    
    QET_MAX = 0.0005
    
    # Computation / Define aquifer head range
    h_aq = np.linspace(-10, 0, 100)
    RET = np.where(h_aq > SURF, EVTR, np.where(h_aq >= (SURF - EXDP), EVTR * (h_aq - (SURF - EXDP)) / EXDP, 0))
    QET = RET*AREA
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(QET, h_aq, label="$Q_{ET}$",color='gold', linewidth=4)
            ax.axhline(0, color='black', linewidth=5)
            ax.axhline(SURF, color='green', linestyle='--', label=f'$SURF$ in m a.s.l.= {SURF:5.2f}')
            ax.axhline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP):5.2f}')
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
                fontsize=10,
                ha='center'
            )
        else:
            ax.plot(h_aq, QET, label="$Q_{ET}$",color='gold', linewidth=4)
            ax.axvline(0, color='black', linewidth=5)
            ax.axvline(SURF, color='green', linestyle='--', label=f'$SURF$ in m a.s.l.= {SURF:5.2f}')
            ax.axvline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP):5.2f}')
            
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
    else:
        if turn:
            ax.plot(QET, h_aq, label="$Q_{ET}$",color='black', linewidth=4)
        else:
            ax.plot(h_aq, QET, label="$Q_{ET}$",color='black', linewidth=4)
        
    # Labels and formatting
    if turn:
        ax.set_ylabel("Heads in the aquifer system in m above sea level (a.s.l)", fontsize=14, labelpad=15)
        ax.set_xlabel("Evapotranspiration loss from the aquifer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
        ax.set_ylim(-10,0)
        ax.set_xlim(-0.1*QET_MAX, QET_MAX)
    else:
        ax.set_xlabel("Heads in the aquifer system in m above sea level (a.s.l)", fontsize=14, labelpad=15)
        ax.set_ylabel("Evapotranspiration loss from the aquifer ($Q_{ET}$) in m³/s", fontsize=14, labelpad=15)
        ax.set_xlim(0,-10)
        ax.set_ylim(-0.1*QET_MAX, QET_MAX)
    
    # === SHARED FORMATTING === #
    ax.set_title("Evapotranspiration losses", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.legend(fontsize=14)
    
    st.pyplot(fig)

Q_h_plot()
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
