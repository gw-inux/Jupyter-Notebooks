# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import streamlit as st
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_Boundary_Conditions_utils import read_md

# ---------- Track the current page
PAGE_ID = "GENERAL"

# Prevent collapsing st.expander with toggle inside
if "qh_expander_open" not in st.session_state:
    st.session_state.qh_expander_open = False

st.session_state.setdefault('exp_general_01', False)
st.session_state.setdefault('exp_general_02', False)
    
# if we just navigated back to this page, reset the expander to closed
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
    
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID
    st.session_state.qh_expander_open = False 
    st.session_state['exp_general_01'] = False
    st.session_state['exp_general_02'] = False
    
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

# ---------- path to questions for the assessments (direct path)
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_general_behavior.json"
path_quest_exer_sc1   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_general_sc1.json"
path_quest_exer_sc2   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/exer_general_sc2.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_general_behavior.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)

with open(path_quest_exer_sc1, "r", encoding="utf-8") as f:
    quest_exer_sc1 = json.load(f)
    
with open(path_quest_exer_sc2, "r", encoding="utf-8") as f:
    quest_exer_sc2 = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)

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
 
def update_index():
    selected_label = st.session_state.bc_index_input
    if   selected_label == "**None**":
        index = 0
    elif selected_label == ":orange[**No-flow**]":
        index = 1
    elif selected_label == ":green[**Recharge**]":
        index = 2
    elif selected_label == ":violet[**River**]":
        index = 3
    elif selected_label == ":blue[**Specified head**]":
        index = 3
    else:
        index = 0
    
    st.session_state.bc_index = index
   
def mark_qh_expander_open():
    # Call this from inside the expander on first render (and from the toggle's on_change)
    st.session_state.qh_expander_open = True
     
    
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

# Starting the text for the page

st.title('General Behavior of Boundary Conditions in :blue[Groundwater Models]')
st.subheader('Understanding the :blue[relationship between flow _Q_ and hydraulic head _h_ using _Q_-_h_ plots] for different boundary conditions', divider="blue")

# --- MOTIVATION ---
st.markdown("""
#### 💡 Motivation - Boundary conditions and _Q_-_h_ plots in groundwater modeling
Understanding how different boundary conditions influence groundwater flow is fundamental to building reliable groundwater models. Boundary conditions control how water enters, leaves, or interacts with the groundwater system, whether through specified heads, specified flows, or head-dependent exchanges such as rivers or drains. However, the behavior of these boundaries can be misinterpreted or misunderstood.

This app provides an intuitive visual and interactive exploration of :blue[**_Q_-_h_ plots**], which are graphical representations of the :blue[**relationship between groundwater outflow or inflow (_Q_) and hydraulic head (_h_) at a boundary**], as shown in the following figure. :blue[**_Q_-_h_ plots**] are powerful conceptual tools to classify and compare the general response of boundary conditions in groundwater models.
""")

left_co, cent_co, last_co = st.columns((20,80,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_Qh_scheme_v2.png')
    st.markdown("""Schematic representation of an unconfined aquifer with a river boundary on the right side together with the associated _Q_-_h_ plot.""")

st.markdown(""" 
#### 📖 Overview of this section
By simulating a simple 1D unconfined aquifer with recharge and various boundary types, users of this module can gain insight into the essential principles that govern groundwater model boundaries and their practical implications in tools like the numerical groundwater flow model MODFLOW.

To support the understanding, this 📕 :red[**Introduction**] part of the module applies well-known analytical solutions for 1D unconfined groundwater flow with recharge. It illustrates how different boundary types like specified head, specified flow, and head-dependent flux influence the resulting hydraulic head and flow distribution. A key focus is placed on understanding the resulting ***Q-h*** relationships, which are central to the conceptualization and interpretation of boundary conditions in groundwater models like MODFLOW.

The subsequent parts of this module provide more details about specific boundary conditions with a focus on MODFLOW, namely the general head (:orange[**GHB**]), river (:violet[**RIV**]), drain (:green[**DRN**]), multi-node-well (:grey[**MNW**]), and evapotranspiration (:blue[**EVT**]) boundary conditions. The menu on the left side can be used to access these sections.
""")

st.markdown("""
#### 🎯 Learning Objectives
By engaging with this section of the interactive module, you will be able to:

1. **Differentiate between specified head, specified flow, and head-dependent flux boundary conditions** and explain their conceptual roles in groundwater models.

2. **Interpret _Q_–_h_ plots** to characterize the functional behavior of boundary conditions and understand how these plots respond to changes in system inputs.

3. **Assess the influence of recharge and hydraulic conductivity** on the groundwater head distribution and the resulting flow dynamics at model boundaries.
""")

def change_ass_state():
    st.session_state.exp_general_01 = not st.session_state.exp_general_01
    
with st.container(border=True):
    ass1_1, ass1_2 = st.columns([25, 1])
    with ass1_1:
        st.markdown("<div style='text-align:left;'>", unsafe_allow_html=True)
        open_click = st.button("✅ **Show the initial assessment** – to assess your **EXISTING** knowledge", key="ass1_btn", type="tertiary",on_click=change_ass_state)
        st.markdown("</div>", unsafe_allow_html=True)
    with ass1_2:
        chevron = "▲" if st.session_state.exp_general_01 else "▼"
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        st.button(chevron, key="ass1_btn2", type="tertiary", on_click=change_ass_state)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.exp_general_01:
        st.markdown("""
        #### Initial assessment
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

# --- TYPES OF BOUNDARY CONDITIONS ---
st.subheader('🧪 Theory: A concise overview about Groundwater Modeling and Boundary Conditions', divider='blue')

st.markdown(""" 

#### 📐 Mathematical Application of Boundary Conditions in Models
To understand boundary conditions in groundwater models, it is important to first recall how numerical models approximate the governing flow equations. The following drop-down discussion on the mathematical application of boundary conditions in models provides a concise background on discretization, system equations, and implementation of specified versus head-dependent boundary conditions.
""")

with st.expander('Show more :blue[**background about the mathematical application of boundary conditions in models**]  **including why RCH and WEL are not sections in this module**', icon ="📑"):
    st.markdown("""
    The groundwater movement through porous media is described by the following **partial differential equation** (PDE):
    """)

    st.latex(r"""
    \frac{\partial}{\partial x}\!\left( K_{xx}\,\frac{\partial h}{\partial x} \right)
    +\frac{\partial}{\partial y}\!\left( K_{yy}\,\frac{\partial h}{\partial y} \right)
    +\frac{\partial}{\partial z}\!\left( K_{zz}\,\frac{\partial h}{\partial z} \right)
    + W
    = S_s\,\frac{\partial h}{\partial t}
    """)
    
    st.markdown("""
    *where*
    - $K_{xx}, K_{yy}, K_{zz}$ is the hydraulic conductivity along x, y, z [L/T],
    - $h$ is the hydraulic head $[L]$,
    - $W$ is volumetric flux per unit volume representing sources/sinks [1/T], with $W<0$ for flow *out* of the system and $W>0$ for flow *into* the system [1/T]  
    - $S_s$ is the specific storage [1/L], and
    - $t$ is time [T].
    
    **Analytical solutions** of PDEs are limited to simple geometries, typically one-dimensional scenarios. Further down in this section of the module, you will find two scenarios of groundwater flow that are examples of analytical solutions.
    
    Codes like MODFLOW ([McDonald and Harbaugh, 1988](https://doi.org/10.3133/twri06A1)) **numerically solve** the PDE for a groundwater system by dividing it into three-dimensional volumes (cells or elements) to simulate complex aquifer systems (e.g., multiple aquifers and confining units) with complex boundary conditions. The shapes of these volumes vary by model code. For some methods the hydraulic head $h$ is computed at the centroid of each volume as in the block-centered finite difference method of the original MODFLOW88 or at the intersection of volume sides as in the finite element method of SUTRA ([Voss et al., 2024](https://doi.org/10.3133/tm6A63)). For each volume, the models require geometry, hydraulic properties (e.g., $K$ and $S_S$ in the equation above), and boundary conditions (e.g., the term $W$ in the equation above). 
    
    For a numerical model, a linear system of equations is prepared and then solved. This linear system is similar to an equation of a line in matrix form""")

    st.latex(r'''[A]\{h\}=\{Q\}''')

    st.markdown("""
    where 
    - $[A]$ is a matrix containing conductances (i.e., a combination of geometry and hydraulic properties),
    - $h$ is the unknown head at each node of a cell or element [called the solution vector in linear algebra], and
    - $Q$ is the flow or flux at each discrete volume [called the right-hand side, RHS, vector in linear algebra].
    
    Flux is the rate of fluid movement across an area and flow is the product of the area and the flux. The size of the matrix $[A]$ is based on the number of head values, which is dependent on the number of discrete volumes and the solution method. Derivation of the block-centered flow, finite-difference solution for the partial differential groundwater flow equation is described in [McDonald and Harbaugh (1988)](https://doi.org/10.3133/twri06A1). The boundary conditions are added to the system of equations differently depending on the type of boundary condition.  
    
    **MODFLOW** is the most widely used numerical groundwater modeling code and this boundary condition training module uses MODFLOW terminology. The simplest discrete volume in MODFLOW is a six-sided cube (a cell) located in three-dimensional model space by row, column, layer (indices i,j,k) with head solved at the centroid of each cell.
    """
    )
    left_co, cent_co, last_co = st.columns((20,80,20))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/MF_6_cells.png')
        st.markdown("""Schematic representation a model cell with indices i,j,k and the six neighbouring cells.""")
    
    st.markdown("""    
    
    **A specified head** means that the head $h$ at that cell **is known** and the matrix equation does not need to be solved for $h_{(i,j,k)}$. With MODFLOW and the simplest discretization (6-sided cubes) the exact location in space is not required and so the indices for the location of each head $h$ is by row, column, layer (i,j,k), although more complex discretization schemes are allowed in MODFLOW6 [Langevin et al., 2017](https://doi.org/10.3133/tm6A55). which was developed after the early releases of MODFLOW.
    
    **A specified flow** means that the flow $Q$ **is known** and therefore is added directly to the right-hand side vector $Q$ for that cell, _Q(i,j,k)_. In MODFLOW there are two packages for specified flow, the Recharge package (RCH) and the Well package (WEL). The two packages work a bit differently but essentially add a value to the right-hand side vector $Q$.  
    
    **A well** specifies a volumetric flow rate, an abstraction well removes water(-) and an injection well supplies water(+). The WEL package of MODFLOW can add any number of wells to a cell, each with a rate in length cubed per volume per time and the flow rate for all wells in the cell are summed and the sum is added to the $Q$ vector for that cell location.
    
    **Recharge** is assigned as a rate in length per time [L/T] to the top of each model cell and the rate is multipled by the area of the top of the cell to calculate the volumetric flow rate _Q_ [L³/T] which is added to the $Q$ vector for that cell location. 
    
    Thus, recharge and wells can be assigned to the same cell. Their flow rates are summed to obtain a net flow rate for input to the matrix.
    
    Both the Specified head and Specified flux boundary conditions are straightforward with respect to implementation in the matrix equations and easier to understand conceptually (one fixes the head at a location and the other fixes a flow). The head-dependent-boundary conditions are more complex, in that flow at the boundary varies in magnitude and possibly direction depending on the simulated head at the boundary, model parameters, and other factors. Consequently, **this module focuses on the more complicated head-dependent flux boundary condition** packages of MODFLOW. These head-dependent flux packages add terms to both the matrix $[A]$ and the right-hand side vector $Q$ at each cell, or element, where a boundary condition is applied. There are different packages in MODFLOW that apply to different types of head-dependent flux boundary conditions. Some supply volumetric rates by multiplying a flux [L/T] and an area [L²], and some supply volumetric rates [L³/T] directly.
    """)

st.markdown("""
#### 📊 Types of Boundary Conditions in Groundwater Modeling and Q-h plots for description
In groundwater flow modeling, boundary conditions define how water enters, exits, or is prevented from flowing across a model surface. Understanding the different types of boundary conditions, and how they control the relationship between flow rate (_Q_) and hydraulic head (_h_), is essential for setting up realistic models and interpreting system behavior.

A **_Q_–_h_ plot** represents conditions at the location of the assigned boundary. It is a graphic display of the relationship between flow _Q_ and hydraulic head _h_, illustrating how a boundary responds to changes in model parameters and hydraulic conditions. Thus, a **_Q_–_h_ plot** shows what happens at the boundary.

Additional, excellent discussion of boundary conditions is provided by [T.E. Reilly (2001)](https://pubs.usgs.gov/twri/twri-3_B8/pdf/twri_3b8.pdf).
"""
)
with st.expander("Show more :blue[**explanation about the boundary condition types**]", icon ="📑"):
    st.markdown("""
    Groundwater models use different boundary condition types to represent different hydrological conditions. Each type defines a specific way that flow and head interact at the boundary, reflecting the physical behavior of the natural or engineered system. **The different types of boundaries and associated _Q_–_h_ plots** can be investigated by scrolling down to the Computation and Visualization section of this introduction and using the analytical solutions for two example configurations of a one-dimensional (1-D) unconfined aquifer (:green[**Scenario 1**] and :red[**Scenario 2**]). First, each type of boundary is described here.
    
    #### TYPE I. Specified Head Boundary (Dirichlet condition)
    
    **Definition:** For the analytical 1-D solutions illustrated in this introductory section, hydraulic head is fixed at a specific value on one, or both, of the lateral boundaries. The flow across the boundary is proportional to the difference between the groundwater head $h_{gw}$ at the boundary and an external water level $h_{bc}$. The specified head represents the stage of an incised waterbody such as a river or lake. The model hydraulic conductivity controls the flux across the boundary in response to the head difference $h_{gw}$-$h_{bc}$. In mathematical terminology, a Dirichlet condition is a boundary condition which specifies the value of the model solution, and a groundwater model solves for head.
    
    In a numerical code, hydraulic head can be specified in any node in a cell or element. It is then input to the system of equations described in the previous drop-down section "Show more :blue[background about the mathematical application of boundary conditions in models]". The flow in or out of each side of a specified-head cell is calculated using the conductance across each side of the cell and the gradient between the specified head and the head in the adjacent cell. The conductance is based on the effective hydraulic conducitivty between the adjacent cells and the head in the adjacent cell is calculated by the model simulation. The most common package of **MODFLOW** for specifying a head is the **Time Variant Specified Head package CHD**.
    
    **Effect:** Using a specified head boundary simplifies the representation of the field system by imposing the average head of a water body at its location in the model. This can be more or less appropriate depending on the system. It is more appropriate for representing a strong external control like a large river or lake, or an ocean. It is less appropriate for representing a small water body that cannot provide/receive water to/from the groundwater system without experiencing a water level change. It is also not appropriate for representing a water body that has a low-hydraulic-conductivity bed that provides resistance to flow. 
    
    The specified head boundary serves as an unlimited sink/source of water. For example, if a high-capacity pumping well was placed in a model next to a specified head boundary, that boundary condition would provide the  inflow required to satisfy the pumping well without the head changing at the boundary regardless of the flow rate through the boundary.
    
    **Example application of a TYPE I boundary in the scenarios with interactive plots:**
    - :green[**Scenario 1**]: The right boundary (_x_ = _L_) has a specified head of 150 m.
    - :red[**Scenario 2**]: The right boundary (_x_ = _L_) has a specified head of 150 m. The left boundary (_x_ = _0_) has a user-defined specified head that can range between 145 m and 155 m.
    
    #### TYPE II. Specified-Flow Boundary (Neumann condition)
    **Definition:** For the analytical 1-D solution illustrated in this introductory section, a specified flow of water crosses the top boundary. The specified flow represents recharge, which is water that infiltrates to the water table. The recharge rate is provided and multiplied by the surface area to obtain the volumetric inflow rate. Head in the groundwater adjusts to accommodate the recharge. This adjustment also depends on the model hydraulic conductivity and conditions at the other boundaries. :green[Scenario 1] includes another specified-flow boundary that is a special case of a specified-flow boundary, a no-flow boundary, with zero flow normal to the boundary. This can represent an impermeable material or a hydraulic groundwater divide that does not shift in response to model conditions. In mathematical terminology, a Neumann condition is a boundary condition with specified values of a derivative of the model solution (flow is calculated from the gradient, or derivative, of head). 
    
    For a three-dimensional numerical model such as a MODFLOW block-centered-flow formulation, a specified flow of water [L³/T] can be assigned to any cell. It is input to the right-hand-side vector $Q$ in the system of equations described in the previous drop-down section "Show more :blue[background about the mathematical application of boundary conditions in models]". Typically, model software provides options for assigning specified fluxes to a numerical model cell. In MODFLOW, a method for representing wells allows specifying the $Q$ for each well in a cell, then summing the $Q$’s and placing the net $Q$ in the right-hand side vector for that cell. A different method for assigning flux is used to represent recharge. This allows assignment of a rate [L/T] that is multiplied by the area of the top of the cell then summing it with other fluxes applied to that cell and placing the net $Q$ in the right-hand side vector for that cell.
    
    **Effect 1:** A specified flux boundary can represent recharge where flow across the model surface enters (or exits for a negative recharge rate such as for evapotranspiration in the 1-D analytical solution shown in this section). The heads within the model rise or fall depending on the specified flow rate. For three-dimensional numerical models specified flows can be assigned to the top of a cell to represent recharge or within a cell to represent a pumping or injection well.
    
    **Effect 2:** If the rate is specified as zero, then water cannot flow into or out of the system across that boundary of the analytical model. Usually, the default is for all external boundaries to be no-flow, unless the modeler specifies differently. For a three-dimensional numerical model, no-flow is often accomplished by indicating that a cell is inactive and this can be done for any cell in the model. For example, there can be an impermeable zone in the middle of a model domain. A no-flow condition can be achieved in the flow-equation formulation by setting the hydraulic conductivity to zero.
    
    **Example application in the subsequent interactive plots:**
    - :green[**Scenario 1**]: The left boundary (_x_ = 0) is a no-flow boundary, simulating an impermeable barrier. The recharge on the top is a specified flow boundary at a rate that can be adjusted by the user.
    - :red[**Scenario 2**]: In this scenario, the only specified flow boundary is the top and the rate can be adjusted by the user.
    
    #### TYPE III. Head-Dependent Flux Boundary (Robin condition, often confused with a Cauchy condition in groundwater modeling 
    **Definition:** The flow across the boundary $Q_B$ is proportional to the difference between the groundwater head $h_{gw}$ at the boundary and the external head of the boundary feature $H_{bc}$ (e.g., river stage, adjacent groundwater head, drain elevation). A *conductance factor $Q_B$ controls the flux across the boundary in response to the head gradient* between the model and the boundary. In mathematical terminology, this is a Robin condition.
    """)
    
    st.latex(r"""
    Q_B = C_B(h_{bc}-h_{gw})
    """)
    
    lc01, cc01, rc01 = st.columns((10,60,10))
    with cc01:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GHBintro.png', caption="General concept of a head dependent flow boundary condition (from  McDonald and Harbaugh, 1988)")
        
    st.markdown("""
    For some head-dependent flux boundary conditions in MODFLOW, geometric aspects of the feature represented by the boundary are used to limit or prevent flow to, or from, the boundary depending on the value of head in the groundwater at the boundary. In the case where this limit is reached, a Neumann condition prevails. 
    
    This boundary condition type has commonly been called a Cauchy condition in the groundwater modeling community. The correct definitions of Cauchy and Robin conditions, and the confusion between them, is explained by [Jazayeri and Werner, 2019](https://doi.org/10.1111/gwat.12893). They also discuss some of the boundary packages presented in this module (GHB, RIV, DRN, and EVT) and explain when they behave as a Robin condition and when they behave as a Neumann condition.
    """)
    
    st.markdown("""
    **Effect:** A head-dependent flow boundary provides a resistive zone between the groundwater and the water body that the boundary represents. Depending on the head difference between the model calculated head in the groundwater at the boundary and the assigned head from the boundary condition (e.g., river stage or drain elevation), the boundary can act as sink or source. 
    
    In other words, the boundary behaves as a specified head boundary with a resistive connection as opposed to a direct connection to the water body being represented. Like a specified-head boundary, the head in the feature represented by the boundary condition does not change no matter how much water flows into or out of the groundwater system. The difference is the additional resistance and the limit to flow based on the geometry of the feature represented by the boundary.
    
    **Example application in the subsequent interactive plots:**
    - :green[**Scenario 1**]: The specified head boundary on the right becomes head-dependent when the River BC toggle is activated (under the assumption that the river is exchanging water with the aquifer at the boundary under fully saturated conditions, allowing water to freely discharge to, or be recharged from, the river system). 
    - :red[**Scenario 2**]: This scenario does not use a specified head boundary.
    """)
    
with st.expander("Show more :blue[**explanation about _Q_-_h_ plots**] that describe boundary condition behavior", icon ="📑", expanded=st.session_state.qh_expander_open):
    st.markdown("""
    The relationship between discharge (_Q_) and hydraulic head (_h_) at model boundaries provides a powerful way to conceptualize and compare different types of boundary conditions in groundwater flow modeling. _Q_-_h_ plots visually illustrate how flow into or out of a model domain responds to parameter changes, highlighting the fundamental behavior of specified-head, specified-flow, and head-dependent flux boundaries. These plots serve as intuitive tools to understand how boundary conditions influence system response, and how they are implemented in models like MODFLOW.
    
    The following figure from the [MODFLOW6 documentation (Langevin et al., 2017)](https://doi.org/10.3133/tm6A55) presents various _Q_-_h_ plots to describe the boundary conditions in MODFLOW. :red[These plots are very powerful but not easy to understand.] You can toggle for :green[an annotated version of the plots that provides more information and explanation.]
    """
    )
    # Toggle that ensures that the expander keeps open
    modified_plot = st.toggle('**Toggle here** to see the :green[**annotated version**].',
        key="qh_toggle",
        on_change= mark_qh_expander_open,
    )
        
    st.markdown("""
    :blue[**The subsequent parts**] of this module allow investigation of these _Q_-_h_ plots :rainbow[**with color coded sections**] for various boundary conditions (_these are accessible via links on the left menu of this module_).
    """
    )
    lc1, cc1, rc1 = st.columns((10,60,10))
    
    with cc1:
        if modified_plot:
            st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/Q_h_plots_MF2005_v3.png', caption="Q-h plots describing the behavior of boundary conditions, [adapted from Langevin et al., 2017] (https://doi.org/10.3133/tm6A55.)")
        else:
            st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/Q_h_plots_MF6_v2.png', caption="Q-h plots describing the behavior of boundary conditions, [modified from Langevin et al., 2017] (https://doi.org/10.3133/tm6A55.)")
    
# --- EXPLANATORY EXAMPLES ---
st.subheader('💫 Examples that explain the use of Q-h plots to illustrate boundary conditions', divider='blue')
st.markdown("""
 In this app, we illustrate the effects of different boundary conditions using two example scenarios of 1D unconfined groundwater flow:
 
:blue[**Both Scenarios have a Specified-Flow Boundary on the Top Surface to represent Recharge**]
 - :green[**Scenario 1**]: with a **no-flow** boundary on one side and a **specified head** or a **head-dependent flow** boundary (e.g., river) on the other, and 
 - :red[**Scenario 2**]: with **two specified head** boundaries.
 
"""
)

lc1, rc1 = st.columns((1,1.45),gap = 'medium')
with lc1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GWF_EX01.jpg')
    st.markdown("""Conceptual model of :green[**Scenario 1**]: a one-dimensional unconfined groundwater system with **one no-flow boundary and one specified head (or optionally a head-dependent flux) boundary**.""")
with rc1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GWF_EX02.jpg')
    st.markdown("""Conceptual model of :red[**Scenario 2**]: a one-dimensional unconfined groundwater system with **two specified head boundaries**.""")
    
with st.expander('Show more about the theory of the :blue[**model and the analytical solution**]', icon ="📑"):
    st.markdown("""
            #### Conceptual model
            
            The conceptual model for both scenarios is shown in the images above. It assumes the aquifer is a **homogeneous** and **isotropic** structure with a **horizontal bottom at an elevation of zero** such that the heads determine the aquifer thickness. The aquifer receives uniform recharge across the top surface.
            """, unsafe_allow_html=True)
    st.markdown("""
            In :green[**Scenario 1**], the aquifer is bounded by
            - one specified-head **or** a head-dependent flow boundary on the right side, while
            - the left side is a no-flow boundary.
            """, unsafe_allow_html=True)
    st.markdown("""
            In :red[**Scenario 2**], the aquifer is bounded
            - on both sides by specified-head boundaries.
            """, unsafe_allow_html=True)
    st.markdown("""
            These simple settings provide a basis for understanding of boundary condition behavior, allowing analysis of groundwater flow and head distribution under different external constraints.
            """, unsafe_allow_html=True)
    st.markdown("""
            #### Mathematical model
            
            The governing equation for steady-state 1D groundwater flow in an unconfined, homogeneous aquifer with recharge for both :green[**Scenario 1**] and :red[**Scenario 2**] is:
            """, unsafe_allow_html=True)
  
    st.latex(r'''\frac{d}{dx}(-hK\frac{dh}{dx})=R''')

    st.markdown("""
            with
            - _x_: spatial coordinate along the horizontal flow direction (m),
            - _h_: hydraulic head (m),
            - _K_: hydraulic conductivity (m/s),
            - _R_: recharge (m/s).
            """)
    st.markdown("""
            The equation can be solved by using suitable boundary conditions:
            
            :green[**Scenario 1**]:
            - at $x=0$ the flow is defined as $dh/dx=0$ and
            - at $x=L$ the head is defined as $h=h_L$
            
            :red[**Scenario 2**]:
            - at $x=0$ the head is defined as $h=h_0$ and
            - at $x=L$ the head is defined as $h=h_L$
            
            """, unsafe_allow_html=True)
      
    st.markdown("""
            With some mathematical operations, see for example [Bakker and Post, 2022](https://doi.org/10.1201/9781315206134), the following analytical solutions can be derived:
            
            :green[**Scenario 1**]:
            
            """, unsafe_allow_html=True)  
    
    st.latex(r'''h(x) = \sqrt{h_L^2 + \frac{R}{K}  (L+x)  (2L - (L+x))}''')
    
    st.markdown("""
            :red[**Scenario 2**]:
            """, unsafe_allow_html=True)  
            
    st.latex(r'''h(x) = \sqrt{h_0^2 - (h_0^2 - h_L^2) \frac{x}{L} + \frac{R}{K}  x  (L - x)}''')
    
    st.markdown("""
            where:
            - _h(x)_: hydraulic head at location _x_ (meters (m),
            - _L_: domain length (m),
            - _h<sub>0</sub>_: head at the specified-head boundary at _x_ = _0_ (m),
            - _h<sub>L</sub>_: head at the specified-head boundary at _x_ = _L_ (m),
            - _R_: recharge (m/s),
            - _K_: hydraulic conductivity (m/s).
            
            These solutions are subsequently used in the interactive plots to dynamically compute and visualize how different boundary conditions and recharge rates affect the hydraulic head distribution and the _Q_-_h_ relationship.
            """, unsafe_allow_html=True)  
            

st.subheader('📈 Computation and Visualization', divider='blue')
st.markdown("""Subsequently, the solutions are computed and results are visualized. You can vary the parameters to investigate the functional behavior of the system. In general, you can modify the
- **recharge _R_** in millimeters/year (mm/yr) and 
- **hydraulic conductivity _K_** in meters/second (m/s), 
- with additional modifications depending on your choice of :green[**Scenario 1**] or :red[**Scenario 2**]. 

On the right side of the control panel, you can select which **_Q_-_h_ relationship** you would like to plot for different model boundaries. The position within the model plot for the head represented in the _Q_-_h_ plot is marked by a colored circle. Additionally, you can toggle to turn the _Q_-_h_ plots 90 degrees clockwise to view _h_-_Q_ plots which are more intuitive for most of us.


""")

# --- INTERACTIVE PLOT EXAMPLE 1 ---
colplot1, colplot2 = st.columns((1,1))
with colplot1:
    show_plot1 = st.button("**Show the :rainbow[interactive] plot for :green[SCENARIO 1]**")
with colplot2:
    show_plot2 = st.button("**Show the :rainbow[interactive] plot for :red[SCENARIO 2]**")

if show_plot1:    
    st.markdown("""
    #### :green[**Scenario 1:**]
    
    You can toggle between a :blue[specified head] and a :violet[head-dependent river boundary] condition on the right side of the model. If the :violet[river] boundary is chosen, you can modify the river-aquifer conductance. 
    
    _Further **instructions** for using the interactive plot and a **short assessment for self-evaluation** are available below the figure._   
    """
    )
    st.markdown("---") 
    # Fixed data
    L = 2500
    hr = 150.0
    zb = (hr-150)
    hRiv = 150
    y_scale = 7
    
    st.session_state.bc_index = 0
    st.session_state.bc_type = "**None**"
    
    @st.fragment
    def computation1():
        # Input data
        # Define the minimum and maximum for the logarithmic scale
        log_min = -4.5229 # Corresponds to 10^-7 = 0.0000001
        log_max = -2.0  # Corresponds to 10^0 = 1
        log_min2 = -5.30103
        log_max2 = -2.30103
        
        st.markdown("""
       #### :green[INPUT CONTROLS]
        """)
    
        columns = st.columns((1,1,1), gap = 'small')
    
        with columns[0]:
            with st.expander("Click to Modify **Model Parameters**:"):
                # Log slider for K with input and print
                labels, default_label = prep_log_slider(default_val = 1e-3, log_min = log_min, log_max = log_max)
                selected_K = st.select_slider("**Hydr. conductivity** $K$ in m/s", labels, default_label, key = "K_1")
                K = float(selected_K)
                # Recharge
                st.write("")
                R = st.slider('**Recharge** $R$ in mm/yr',-300,300,0,1)
                R = R/1000/365.25/86400
    
        with columns[1]:
            with st.expander("Click to Modify **Boundary Condition Parameters**:"):
                riv = st.toggle (':violet[**Head-dependent flux BC on right side?**]', key = 'riv_toggle')
                if riv:
                    # Log slider for river conductance                    
                    labels, default_label = prep_log_slider(default_val = 1e-4, log_min = log_min2, log_max = log_max2)
                    selected_cRiv = st.select_slider("**Boundary Conductance** $C_{B}$ in m²/s", labels, default_label, key = "cRiv")
                    cRiv = float(selected_cRiv)
                    hr_riv = R * L / cRiv + hRiv
                
        with columns[2]:
            with st.expander("Click for **the _Q_-_h_ plot**:"):
                if riv:
                    options = ["**None**", ":orange[**No-flow**]", ":green[**Recharge**]", ":violet[**Head-dep. flux**]"]
                    bc_type = st.radio("for the following boundary condition:", options , index=st.session_state.bc_index, key= "bc_index_input" , on_change = update_index)
                else:
                    options = ["**None**", ":orange[**No-flow**]", ":green[**Recharge**]", ":blue[**Specified head**]"]
                    bc_type = st.radio("for the following boundary condition:", options , index=st.session_state.bc_index, key= "bc_index_input" , on_change = update_index)
                # Get the selected index
                turn = st.toggle('Toggle to turn the plot 90 degrees', key="general_turn") 
        
        # --- Computation here
        x = np.arange(0, L, L/1000)
        
        if riv:
            phiL = 0.5 * K * (hr_riv - zb) ** 2
        else:
            phiL = 0.5 * K * (hr - zb) ** 2
        h = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K)
        
        # --- Q-h relationship functions ---
        
        # 1. Specified Head Boundary
        Q_defh = np.linspace((-400/1000/365.25/86400*2500), (400/1000/365.25/86400*2500), 10)
        h_defh = np.ones_like(Q_defh)* hr
        h_defh_point = hr
        Q_defh_point = R*2500*-1
        
        # 2a. Specified Flow Boundary (Q = 0)
        h_nf = np.linspace(140, 160, 20)
        Q_nf = np.zeros_like(h_nf)
        # Find the index where x is closest to 0
        x0 = np.argmin(np.abs(x - 0))
        h_nf_point = h[x0]
        Q_nf_point = 0.0
        
        # 2b. Specified Flow Boundary (Q = <>0)
        h_rch = np.linspace(140, 160, 20)
        Q_rch = np.ones_like(h_rch)* R
        # Find the index where x is closest to 1250
        x1250 = np.argmin(np.abs(x - 1250))
        h_rch_point = h[x1250]
        Q_rch_point = R
        
        # 3 River
        if riv:
            h_rob = np.linspace(140, 160, 20)
            Q_rob = np.ones_like(h_rob) * cRiv * (hRiv-h_rob)
            h_rob_point = zb + np.sqrt(2 * (-R / 2 * (2500 ** 2 - L ** 2) + phiL) / K)
            Q_rob_point = cRiv * (hRiv - h_rob_point)
        
        
        # PLOT FIGURE
        fig = plt.figure(figsize=(9, 10))
        widths = [1, 2, 1]
        heights = [1.4, 1]
        gs = fig.add_gridspec(ncols=3, nrows=2, width_ratios=widths, height_ratios=heights)
        ax = fig.add_subplot(gs[0,0:3])
        ax_qh = fig.add_subplot(gs[1,1])
        fig.subplots_adjust(hspace=0.35)  # consistent layout
        ax.plot(x,h)
        ax.fill_between(x,0,h, facecolor='lightblue')
        ax.set_title('Hydraulic head for 1D unconfined flow (Scenario 1)', color = 'green', fontsize=16, pad=10)
        ax.set_xlabel(r'x (m)', fontsize=14)
        ax.set_ylabel(r'hydraulic head (m)', fontsize=14)
        
        # BOUNDARY CONDITIONS hl, hr
        ax.vlines(0, 0, 1000, linewidth = 10, color='darkorange', alpha = 0.7)
        if riv:
            ax.vlines(L, 0, hr, linewidth = 10, color='deepskyblue')
            ax.vlines(L-5, 0, hr_riv, linewidth = 3, color='fuchsia')
        else:
            ax.vlines(L, 0, hr, linewidth = 10, color='deepskyblue')
            
        # Show the boundary plot position in the main plot
        if "No-flow" in bc_type:
            ax.plot(0, h_nf_point, 'ro', markersize=10)
            ax.text(75, h_nf_point+1.0, 'Q-h plot for this point', horizontalalignment='left', bbox=dict(boxstyle="square",facecolor='none', edgecolor='darkorange'), fontsize=12)
        if "Recharge" in bc_type:
            ax.plot(1250, h_rch_point, 'go', markersize=10)
            ax.text(1000, h_rch_point+1.0, 'Q-h plot for this point', bbox=dict(boxstyle="square",facecolor='none', edgecolor='green'), fontsize=12)
        if "Specified head" in bc_type:
            ax.plot(2500, h_defh_point, 'bo', markersize=10)
            ax.text(2425, h_defh_point+1.0, 'Q-h plot for this point', horizontalalignment='right', bbox=dict(boxstyle="square",facecolor='none', edgecolor='deepskyblue'), fontsize=12)
        if "Head-dep. flux" in bc_type:
            ax.plot(2500, h_rob_point, 'o', color='fuchsia', markersize=10)
            ax.text(2425, h_rob_point+1.0, 'Q-h plot for this point', horizontalalignment='right', bbox=dict(boxstyle="square",facecolor='none', edgecolor='fuchsia'), fontsize=12)
        
        # MAKE 'WATER'-TRIANGLE
        x1500 = np.argmin(np.abs(x - 1500))
        h_arrow = h[x1500] #water level at arrow
        L2 = 2500
        ax.arrow(L2*0.6,(h_arrow+(h_arrow*0.0030)), 0, -0.01, fc="k", ec="k", head_width=(L2*0.015), head_length=(h_arrow*0.0025))
        ax.hlines(y= h_arrow-(h_arrow*0.0010), xmin=L2*0.59, xmax=L2*0.61, colors='blue')   
        ax.hlines(y= h_arrow-(h_arrow*0.0022), xmin=L2*0.595, xmax=L2*0.605, colors='blue')
        
        
        
        # --- ARROWS FOR RECHARGE (Scenario 1) ---
        # uses: R, K, L, x, h, y_scale, ax  (already defined in computation1)
        
        if R != 0:
            mag = abs(R)
        
            # sizing (same style as Scenario 2)
            head_len  = (mag * 86400 * 365.25 * 1000 * 0.002) * y_scale / 3
            head_len  = max(head_len, 0.03)         # ensure visible head
            shaft_len = max(0.05, head_len * 1.4)   # ensure visible shaft
        
            # shaft & head widths (data units)
            shaft_width = (head_len * 120 / y_scale)
            head_width  = (head_len * 450 / y_scale)
        
            def draw_recharge_arrow(xpos, h_at_x, sign):
                """
                sign > 0 -> recharge (down arrow), tip EXACTLY at water table
                sign < 0 -> ET (up arrow), tail EXACTLY at water table
                """
                total = shaft_len + head_len
                if sign > 0:
                    # start above water, draw down so the tip lands on h_at_x
                    y0, dy = h_at_x + total, -total
                else:
                    # start on the water table, draw up so the tail sits on h_at_x
                    y0, dy = h_at_x, total
        
                ax.arrow(
                    xpos, y0, 0.0, dy,
                    length_includes_head=True,
                    width=shaft_width, head_width=head_width, head_length=head_len,
                    fc="green", ec="green", alpha=0.95, linewidth=0.8, zorder=4
                )
        
            # pick a few positions across the domain
            xs = np.array([L*0.167, L*0.333, L*0.50, L*0.666, L*0.833])
        
            # interpolate heads at those x-positions from the computed profile
            hs = np.interp(xs, x, h)
        
            sgn = 1 if R > 0 else -1
            for xi, hi in zip(xs, hs):
                draw_recharge_arrow(xi, hi, sgn)
        
        
        
        
        
        
        # Format plot
        ax.set_ylim(140,160)
        ax.set_xlim(-30,L+30)
        x_pos1 = 400
        x_pos2 = 2490
        y_pos1 = 158.8
        y_pos2 = 157.3
        
        ax.text(x_pos1, y_pos1, 'No-flow bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='darkorange', alpha=0.4), fontsize=12)
        if riv:
            ax.text(x_pos2, y_pos1, 'Head-dependent flux bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='fuchsia', alpha=0.4), fontsize=12)
            ax.text(x_pos2, y_pos2, 'Q_BC: {:.2e} m³/s '.format(Q_rob_point), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
        else:
            ax.text(x_pos2, y_pos1, 'Specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
            ax.text(x_pos2, y_pos2, 'Q_BC: {:.2e} m³/s '.format(Q_defh_point), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
        
            
        # --- Q–h PLOT in 2nd subplot ---
        if turn:
            ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_ylim(140,160)
            ax_qh.set_ylabel("hydraulic head (m)", fontsize=14)
            ax_qh.set_xlabel("+ is flow INTO the model \n$Q_{in}$ (m³/s)", fontsize=14)
        else:
            ax_qh.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_xlim(140,160)
            ax_qh.set_xlabel("hydraulic head (m)", fontsize=14)
            ax_qh.set_ylabel("+ is flow INTO the model \n$Q_{in}$ (m³/s)", fontsize=14)
        if "No-flow" in bc_type:
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_nf, h_nf, color='black', linewidth=3)
                ax_qh.plot(Q_nf_point, h_nf_point, 'ro', markersize=10)
                ax_qh.set_title("h-Q plot: Specified flow boundary (No-Flow)", fontsize=16, pad=15, color='orange')
                ax_qh.set_xlim(-1,1)
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else:            
                ax_qh.plot(h_nf, Q_nf, color='black', linewidth=3)
                ax_qh.plot(h_nf_point, Q_nf_point, 'ro', markersize=10)
                ax_qh.set_title("Q–h plot: Specified flow boundary (No-Flow)", fontsize=16, pad=15, color='orange')
                ax_qh.set_ylim(-1,1)
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Recharge" in bc_type:
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_rch, h_rch, color='black', linewidth=3)
                ax_qh.plot(Q_rch_point, h_rch_point, 'go', markersize=10)
                ax_qh.set_title("h-Q plot: Specified flow boundary (Recharge) per m² at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_xlim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else:            
                ax_qh.plot(h_rch, Q_rch, color='black', linewidth=3)
                ax_qh.plot(h_rch_point, Q_rch_point, 'go', markersize=10)
                ax_qh.set_title("Q–h plot: Specified flow boundary (Recharge) per m² at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_ylim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Specified head" in bc_type:      
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_defh, h_defh, color='black', linewidth=3)
                ax_qh.plot(Q_defh_point, h_defh_point, 'bo', markersize=10)
                ax_qh.set_title("h-Q plot: Specified head boundary", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h_defh, Q_defh, color='black', linewidth=3)
                ax_qh.plot(h_defh_point, Q_defh_point, 'bo', markersize=10)
                ax_qh.set_title("Q–h plot: Specified head boundary", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Head-dep. flux" in bc_type:      
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_rob, h_rob, color='black', linewidth=3)
                ax_qh.plot(Q_rob_point, h_rob_point, 'o', color='fuchsia', markersize=10)
                ax_qh.set_title("h-Q plot: Head-dep. flux boundary", fontsize=16, pad=15, color = 'violet')
                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h_rob, Q_rob, color='black', linewidth=3)
                ax_qh.plot(h_rob_point, Q_rob_point, 'o', color='fuchsia', markersize=10)
                ax_qh.set_title("Q–h plot: Head-dep. flux boundary", fontsize=16, pad=15, color = 'violet')
                ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        else:
            ax_qh.set_ylim(-1,1)
            ax_qh.text(150,0.75,"No Q–h plot selected.\n\nScroll down for Instructions \n\nor select a Q–h plot type in the INPUT CONTROLS (right-hand menu).", ha='center', va='center', fontsize=13, wrap=True)
            ax_qh.axis('off')
        
        st.pyplot(fig)

        if "No-flow" in bc_type:
            st.markdown("""_The dashed line in the plot represents the specified head at the right boundary with $h_{2500}$ = 150 m._""")
        
        # Expander with "open in new tab"
        DOC_FILE1 = "GWP_Boundary_Conditions_General_Instructions1.md"
        with st.expander('Show the 🧪:green[**INSTRUCTIONS for using the interactive plot for Scenario 1**]'):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE1}")
            st.markdown(read_md(DOC_FILE1))
            
        with st.expander('Show the :green[**SCENARIO 1**] :rainbow[**assessment**] - to self-check your understanding'):
            st.markdown("""
            #### 🧠 Scenario 1 assessment
            These questions provide an opportunity for you to assess your understanding of boundary conditions discussed in scenario 1.
            """)
        
            # Render questions in a 2x2 grid (row-wise, aligned)
            for row in [(0, 1), (2, 3)]:
                col1, col2 = st.columns(2)
            
                with col1:
                    i = row[0]
                    st.markdown(f"**Q{i+1}. {quest_exer_sc1[i]['question']}**")
                    multiple_choice(
                        question=" ",  # suppress repeated question display
                        options_dict=quest_exer_sc1[i]["options"],
                        success=quest_exer_sc1[i].get("success", "✅ Correct."),
                        error=quest_exer_sc1[i].get("error", "❌ Not quite.")
                    )
            
                with col2:
                    i = row[1]
                    st.markdown(f"**Q{i+1}. {quest_exer_sc1[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_exer_sc1[i]["options"],
                        success=quest_exer_sc1[i].get("success", "✅ Correct."),
                        error=quest_exer_sc1[i].get("error", "❌ Not quite.")
                    )
        
    computation1()

if show_plot2:
    
    st.markdown("""
    #### :red[**Scenario 2:**]
    
    You can modify the :blue[specified head] elevation at the left side (the right-side hydraulic head is fixed at 150 m). The interactive plot will indicate the boundary flow (inflow or outflow) for both :blue[specified head boundaries].   
    
    _Further **instructions** for using the interactive plot and a **short assessment for self-evaluation** are available below the figure._  
    """
    )
    st.markdown("---") 
    
    # Fixed data
    L2 = 2500.
    hr2 = 150.0
    y2_scale = 7    
    
    @st.fragment
    def computation2():
        
        # Interactive widgets
        # Define the minimum and maximum for the logarithmic scale
        log_min2 = -5.0 # Corresponds to 10^-7 = 0.0000001
        log_max2 = -2.0  # Corresponds to 10^0 = 1
        
        st.markdown("""
       #### :red[INPUT CONTROLS]
        """)
        
        columns = st.columns((1,1,1), gap = 'small')

        with columns[0]:
            with st.expander("Click to Modify **Model Parameters**:"):
                # Log slider for K with input and print
                labels, default_label = prep_log_slider(default_val = 1e-3, log_min = log_min2, log_max = log_max2)
                selected_K2 = st.select_slider("**Hydr. conductivity** $K$ in m/s", labels, default_label, key = "K_2")
                K2 = float(selected_K2)
                st.write("")
                R2 = st.slider('**Recharge** $R$ in mm/yr ',-300,300,0,1)
                R2 = R2/1000/365.25/86400
        
        with columns[1]:
            with st.expander("Click to Modify **Boundary Condition Parameters**:"):
                hl2=st.slider('**LEFT specified head** $h_0$ in m ', 145.,155.,150.,.1)
                riv2 = False
        
        with columns[2]:
            with st.expander("Click for **the Q-h plot**:"):
                if riv2:
                    bc_type2 = st.radio("for the following boundary condition:",
                                  ["**None**", ":green[**Recharge**]", ":blue[**Specified head left**]", ":violet[**River**]"], index=0)
                else:
                    bc_type2 = st.radio("for the following boundary condition:",
                                  ["**None**", ":green[**Recharge**]", ":blue[**Specified head left**]",":blue[**Specified head right**]"], index=0)
                turn2 = st.toggle('Toggle to turn the plot 90 degrees', key="general_turn2")
                large_range_Q = st.toggle('Toggle to increase the range of the Q-axis', key="general_large_range_Q")             
        
        x2 = np.arange(0, L2,L2/1000)
        h2=(hl2**2-(hl2**2-hr2**2)/L2*x2+(R2/K2*x2*(L2-x2)))**0.5
        
        # Groundwater divide
        if R2 >= 0:
            max_y2 = max(h2)
            max_x2 = x2[h2.argmax()]
            R2_min_ms=K2*abs(hl2**2-hr2**2)/L2**2
        else:
            max_y2 = min(h2)
            max_x2 = x2[h2.argmin()]
            R2_min_ms=K2*abs(hl2**2-hr2**2)/L2**2*-1.0
        
        
        # --- Q-h relationship functions ---
        
        # 1. Specified Head Boundary
        if large_range_Q:
            Q2_defh = np.linspace((-400/1000/365.25/86400*250000), (400/1000/365.25/86400*250000), 10)
        else:
            Q2_defh = np.linspace((-400/1000/365.25/86400*2500), (400/1000/365.25/86400*2500), 10)
        h2_defh_l = np.ones_like(Q2_defh)* hl2
        h2_defh_r = np.ones_like(Q2_defh)* hr2
        # Point heads
        h2_defh_point_r = hr2
        h2_defh_point_l = hl2
        # Compute the area AR that contributes to the recharge
        AR_r = L2 - max_x2
        AR_l = max_x2

        # Point flows
        # Negative recharge and divide
        if R2 < 0.0:
            # Divide
            if R2<R2_min_ms:
                Q2_defh_point_r = AR_r*R2*-1
                Q2_defh_point_l = AR_l*R2*-1
            # No divide
            else:
                if hr2>hl2:
                    Q2_defh_point_r = (K2/2/L2*(hl2**2-hr2**2)-(R2*L2/2))*-1
                    Q2_defh_point_l = K2/2/L2*(hl2**2-hr2**2)+(R2*L2/2)
                else:
                    Q2_defh_point_r = (K2/2/L2*(hl2**2-hr2**2)+(R2*L2/2))*-1
                    Q2_defh_point_l = K2/2/L2*(hl2**2-hr2**2)-(R2*L2/2)
        # Positive recharge and divide            
        else:        
            if R2>R2_min_ms:
                Q2_defh_point_r = AR_r*R2*-1
                Q2_defh_point_l = AR_l*R2*-1
            # No divide
            else:
                if hr2>hl2:
                    Q2_defh_point_r = (K2/2/L2*(hl2**2-hr2**2)-(R2*L2/2))*-1
                    Q2_defh_point_l = K2/2/L2*(hl2**2-hr2**2)+(R2*L2/2)
                else:
                    Q2_defh_point_r = (K2/2/L2*(hl2**2-hr2**2)+(R2*L2/2))*-1
                    Q2_defh_point_l = K2/2/L2*(hl2**2-hr2**2)-(R2*L2/2)       
        
        # 2b. Specified Flow Boundary (Q = <>0)
        h2_rch = np.linspace(140, 160, 20)
        Q2_rch = np.ones_like(h2_rch)* R2
        # Find the index where x is closest to 1250
        x1250 = np.argmin(np.abs(x2 - 1250))
        h2_rch_point = h2[x1250]
        Q2_rch_point = R2
        
#        # 3 River
#        if riv:
#            h_rob = np.linspace(140, 160, 20)
#            Q_rob = np.ones_like(h_rob) * cRiv * (hRiv-h_rob)
#            h_rob_point = zb + np.sqrt(2 * (-R / 2 * (2500 ** 2 - L ** 2) + phiL) / K)
#            Q_rob_point = cRiv * (hRiv - h_rob_point)
        
        
        # PLOT FIGURE
        fig = plt.figure(figsize=(9, 10))
        widths = [1, 2, 1]
        heights = [1.4, 1]
        gs = fig.add_gridspec(ncols=3, nrows=2, width_ratios=widths, height_ratios=heights)
        ax = fig.add_subplot(gs[0,0:3])
        ax_qh = fig.add_subplot(gs[1,1])
        fig.subplots_adjust(hspace=0.35)  # consistent layout
        ax.plot(x2,h2)
        ax.set_title('Hydraulic head for 1D unconfined flow (Scenario 2)', color = 'red', fontsize=16, pad=10)
        ax.set_xlabel(r'x (m)', fontsize=14)
        ax.set_ylabel(r'hydraulic head (m)', fontsize=14)
        ax.fill_between(x2,0,h2, facecolor='lightblue')
            
        # BOUNDARY CONDITIONS hl, hr
        ax.vlines(0, 0, hl2, linewidth = 10, color='deepskyblue')
        ax.vlines(L2, 0, hr2, linewidth = 10, color='deepskyblue')

        # Show the boundary plot position in the main plot
        if "Recharge" in bc_type2:
            ax.plot(1250, h2_rch_point, 'go', markersize=10)
            ax.text(1000, h2_rch_point+1.0, 'Q-h plot for this point', bbox=dict(boxstyle="square",facecolor='none', edgecolor='green'), fontsize=12)
        if "Specified head left" in bc_type2:
            ax.plot(0, h2_defh_point_l, 'bo', markersize=10)
            ax.text(75, h2_defh_point_l+1.0, 'Q-h plot for this point', horizontalalignment='left', bbox=dict(boxstyle="square",facecolor='none', edgecolor='deepskyblue'), fontsize=12)
        if "Specified head right" in bc_type2:
            ax.plot(2500, h2_defh_point_r, 'bo', markersize=10)
            ax.text(2425, h2_defh_point_r+1.0, 'Q-h plot for this point', horizontalalignment='right', bbox=dict(boxstyle="square",facecolor='none', edgecolor='deepskyblue'), fontsize=12)
        if "River" in bc_type2:
            ax.plot(2500, h_rob_point, 'o', color='fuchsia', markersize=10)
            ax.text(2425, h_rob_point+1.0, 'Q-h plot for this point', horizontalalignment='right', bbox=dict(boxstyle="square",facecolor='none', edgecolor='fuchsia'), fontsize=12)


        # BC denotators
        x2_pos1 = 10
        x2_pos2 = 2490
        y2_pos1 = 158.8
        y2_pos2 = 157.3
        
        # Box for boundary denotation
        ax.text(x2_pos1, y2_pos1, 'LEFT Specified head bc', horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
        
        # Box for boundary flow
        if R2 <= 0.0:
            ax.text(x2_pos1, y2_pos2, 'Q_BC_LEFT: {:.2e} m³/s '.format(Q2_defh_point_l), horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
            ax.text(x2_pos2, y2_pos2, 'Q_BC_RIGHT: {:.2e} m³/s '.format(Q2_defh_point_r), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
        else:
            ax.text(x2_pos1, y2_pos2, 'Q_BC_LEFT: {:.2e} m³/s '.format(Q2_defh_point_l), horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
            ax.text(x2_pos2, y2_pos2, 'Q_BC_RIGHT: {:.2e} m³/s '.format(Q2_defh_point_r), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
        
        if riv2:
            ax.text(x2_pos2, y2_pos1, 'River bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='fuchsia', alpha=0.4), fontsize=12)
        else:
            ax.text(x2_pos2, y2_pos1, 'RIGHT specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
            
        # MAKE 'WATER'-TRIANGLE
        h_arrow = (hl2**2-(hl2**2-hr2**2)/L2*(L2*0.6)+(R2/K2*(L2*0.6)*(L2-(L2*0.6))))**0.5  #water level at arrow
        ax.arrow(L2*0.6,(h_arrow+(h_arrow*0.0030)), 0, -0.01, fc="k", ec="k", head_width=(L2*0.015), head_length=(h_arrow*0.0025))
        ax.hlines(y= h_arrow-(h_arrow*0.0010), xmin=L2*0.59, xmax=L2*0.61, colors='blue')   
        ax.hlines(y= h_arrow-(h_arrow*0.0022), xmin=L2*0.595, xmax=L2*0.605, colors='blue')    
        
        # ARROWS FOR RECHARGE
        if R2 != 0:
            mag = abs(R2)
        
            # size scaling (kept in your style, just used consistently)
            head_len  = (mag * 86400 * 365.25 * 1000 * 0.002) * y2_scale / 3
            head_len  = max(head_len, 0.03)                 # ensure visible head
            shaft_len = max(0.05, head_len * 1.4)           # visible shaft
        
            # shaft & head widths (data units)
            shaft_width = (head_len * 120 / y2_scale)
            head_width  = (head_len * 450 / y2_scale)
        
            def draw_recharge_arrow(xpos, h_at_x, sign):
                """
                sign > 0  -> recharge (down arrow), tip EXACTLY at water table
                sign < 0  -> ET (up arrow), tail EXACTLY at water table
                """
                total = shaft_len + head_len
        
                if sign > 0:
                    # start above water, draw down so the tip lands on h_at_x
                    y0 = h_at_x + total
                    dy = -total
                else:
                    # start on the water table, draw up so the tail sits on h_at_x
                    y0 = h_at_x
                    dy = total
        
                ax.arrow(
                    xpos, y0, 0.0, dy,
                    length_includes_head=True,
                    width=shaft_width, head_width=head_width, head_length=head_len,
                    fc="green", ec="green", alpha=0.95, linewidth=0.8, zorder=4
                )
        
            # positions and water levels
            x1, x2, x3, x4, x5 = L2*0.167, L2*0.333, L2*0.50, L2*0.666, L2*0.833,
            h_rch1 = (hl2**2 - (hl2**2-hr2**2)/L2*x1 + (R2/K2)*x1*(L2-x1))**0.5
            h_rch2 = (hl2**2 - (hl2**2-hr2**2)/L2*x2 + (R2/K2)*x2*(L2-x2))**0.5
            h_rch3 = (hl2**2 - (hl2**2-hr2**2)/L2*x3 + (R2/K2)*x3*(L2-x3))**0.5
            h_rch4 = (hl2**2 - (hl2**2-hr2**2)/L2*x4 + (R2/K2)*x4*(L2-x4))**0.5
            h_rch5 = (hl2**2 - (hl2**2-hr2**2)/L2*x5 + (R2/K2)*x5*(L2-x5))**0.5
        
            sgn = 1 if R2 > 0 else -1
            draw_recharge_arrow(x1, h_rch1, sgn)
            draw_recharge_arrow(x2, h_rch2, sgn)
            draw_recharge_arrow(x3, h_rch3, sgn)
            draw_recharge_arrow(x4, h_rch4, sgn)
            draw_recharge_arrow(x5, h_rch5, sgn)
        
        
        #Groundwater divide
        if R2 > 0.0 and R2>R2_min_ms:
            ax.vlines(max_x2,0,max_y2, color="r")
        if R2 < 0.0 and R2<R2_min_ms:
            ax.vlines(max_x2,0,max_y2, color="b")
        ax.set_ylim(140,160)
        ax.set_xlim(-30,L2+30)
        
        
## --- Q–h PLOT in 2nd subplot ---
        if turn2:
            ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_ylim(140,160)
            ax_qh.set_ylabel("hydraulic head (m)", fontsize=14)
            ax_qh.set_xlabel("+ is flow INTO the model \n$Q_{in}$ (m³/s)", fontsize=14)
        else:
            ax_qh.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_xlim(140,160)
            ax_qh.set_xlabel("hydraulic head (m)", fontsize=14)
            ax_qh.set_ylabel("+ is flow INTO the model \n$Q_{in}$ (m³/s)", fontsize=14)
        if "Recharge" in bc_type2:
            if turn2:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q2_rch, h2_rch, color='black', linewidth=3)
                ax_qh.plot(Q2_rch_point, h2_rch_point, 'go', markersize=10)
                ax_qh.set_title("h-Q plot: Specified flow boundary (Recharge) per m² at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_xlim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else:            
                ax_qh.plot(h2_rch, Q2_rch, color='black', linewidth=3)
                ax_qh.plot(h2_rch_point, Q2_rch_point, 'go', markersize=10)
                ax_qh.set_title("Q–h plot: Specified flow boundary (Recharge) per m² at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_ylim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Specified head left" in bc_type2:      
            if turn2:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q2_defh, h2_defh_l, color='black', linewidth=3)
                ax_qh.plot(Q2_defh_point_l, h2_defh_point_l, 'bo', markersize=10)
                ax_qh.set_title("h-Q plot: Specified head boundary left", fontsize=16, pad=15, color = 'blue')
                if large_range_Q:
                    ax_qh.set_xlim(-(400/1000/365.25/86400*250000),(400/1000/365.25/86400*250000))
                else:
                    ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h2_defh_l, Q2_defh, color='black', linewidth=3)
                ax_qh.plot(h2_defh_point_l, Q2_defh_point_l, 'bo', markersize=10)
                ax_qh.set_title("Q–h plot: Specified head boundary left", fontsize=16, pad=15, color = 'blue')
                if large_range_Q:
                    ax_qh.set_ylim(-(400/1000/365.25/86400*250000),(400/1000/365.25/86400*250000))
                else:
                    ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Specified head right" in bc_type2:      
            if turn2:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q2_defh, h2_defh_r, color='black', linewidth=3)
                ax_qh.plot(Q2_defh_point_r, h2_defh_point_r, 'bo', markersize=10)
                ax_qh.set_title("h-Q plot: Specified head boundary right", fontsize=16, pad=15, color = 'blue')
                if large_range_Q:
                    ax_qh.set_xlim(-(400/1000/365.25/86400*250000),(400/1000/365.25/86400*250000))
                else:
                    ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h2_defh_r, Q2_defh, color='black', linewidth=3)
                ax_qh.plot(h2_defh_point_r, Q2_defh_point_r, 'bo', markersize=10)
                ax_qh.set_title("Q–h plot: Specified head boundary right", fontsize=16, pad=15, color = 'blue')
                if large_range_Q:
                    ax_qh.set_ylim(-(400/1000/365.25/86400*250000),(400/1000/365.25/86400*250000))
                else:
                    ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)                
#        elif "River" in bc_type:      
#            if turn:
#                ax_qh.plot(Q_rob, h_rob, color='black', linewidth=3)
#                ax_qh.plot(Q_rob_point, h_rob_point, 'o', color='fuchsia', markersize=10)
#                ax_qh.set_title("h-Q plot: River boundary", fontsize=16, pad=15, color = 'violet')
#                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
#                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
#                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
#            else: 
#                ax_qh.plot(h_rob, Q_rob, color='black', linewidth=3)
#                ax_qh.plot(h_rob_point, Q_rob_point, 'o', color='fuchsia', markersize=10)
#                ax_qh.set_title("Q–h plot: River boundary", fontsize=16, pad=15, color = 'violet')
#                ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
#                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
#                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        else:
            ax_qh.set_ylim(-1,1)
            ax_qh.text(150,0.75,"No Q–h plot selected.\n\nScroll down for Instructions \n\nor select a Q–h plot type in the INPUT CONTROLS (right-hand menu).", ha='center', va='center', fontsize=13, wrap=True)
            ax_qh.axis('off')
            # Draw a blank subplot (white background, no ticks, no frame)
            #ax_qh.axis('off')
        
        st.pyplot(fig)
        
        # Expander with "open in new tab"
        DOC_FILE2 = "GWP_Boundary_Conditions_General_Instructions2.md"
        with st.expander('Show the 🧪:red[**INSTRUCTIONS for using the interactive plot for Scenario 2**]'):
            st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE2}")
            st.markdown(read_md(DOC_FILE2))
        
        with st.expander('Show the :red[**SCENARIO 2**] :rainbow[**assessment**] - to self-check your understanding'):
            st.markdown("""
            #### 🧠 Scenario 2 assessment
            These questions test your understanding after investigating Scenario 2.
            """)
        
            # Render questions in a 2x2 grid (row-wise, aligned)
            for row in [(0, 1), (2, 3)]:
                col1, col2 = st.columns(2)
            
                with col1:
                    i = row[0]
                    st.markdown(f"**Q{i+1}. {quest_exer_sc2[i]['question']}**")
                    multiple_choice(
                        question=" ",  # suppress repeated question display
                        options_dict=quest_exer_sc2[i]["options"],
                        success=quest_exer_sc2[i].get("success", "✅ Correct."),
                        error=quest_exer_sc2[i].get("error", "❌ Not quite.")
                    )
            
                with col2:
                    i = row[1]
                    st.markdown(f"**Q{i+1}. {quest_exer_sc2[i]['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=quest_exer_sc2[i]["options"],
                        success=quest_exer_sc2[i].get("success", "✅ Correct."),
                        error=quest_exer_sc2[i].get("error", "❌ Not quite.")
                    )
    
    computation2()

st.subheader('✔️ Conclusion', divider = 'blue')
st.markdown("""
Boundary conditions are the foundation of any groundwater model. They define how water enters, exits, or interacts with the simulated model domain. Each boundary type, whether specified head, specified flow, or head-dependent flow, represents a different physical assumption and has specific implications for model behavior.

This general module introduces the concept of **_Q_-_h_ plots** as a powerful visual and conceptual tool. These plots help clarify the distinct relationships of flow and head for different boundary types and support better understanding of the sensitivity of model response to changes in boundary property values.

By exploring these relationships interactively, a user can develop a more intuitive grasp of how boundary conditions function, how they differ, and why appropriate conceptualization is essential in MODFLOW modeling.

In the following boundary-specific sections of the module, we dive deeper into each condition, with visualizations, theory, and targeted assessments. But prior moving on, it may be helpful to take the final assessment to self-check your understanding.
""")
with st.container(border=True):
    ass2_1, ass2_2 = st.columns((25,1))
    with ass2_1:
        open_click = st.button("✅ **Show the final assessment** - to self-check your **understanding**", key="ass2_btn", type="tertiary")
        if open_click:
            st.session_state.exp_general_02 = not st.session_state.exp_general_02
    with ass2_2:
        chevron2 = "▲" if st.session_state.exp_general_02 else "▼"
        st.markdown(chevron2)
    
    if st.session_state.exp_general_02:
        st.markdown("""
        #### Final assessment
        These questions test your conceptual understanding after working with the application.
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
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')