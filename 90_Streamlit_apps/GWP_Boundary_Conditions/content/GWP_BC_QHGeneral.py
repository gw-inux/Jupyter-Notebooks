# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import streamlit as st
import json
from streamlit_book import multiple_choice

# path to questions for the assessments (direct path)
path_quest_ini   = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/initial_general_behavior.json"
path_quest_final = "90_Streamlit_apps/GWP_Boundary_Conditions/questions/final_general_behavior.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
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

st.title('General behavior of boundary conditions in groundwater models')
st.subheader('Understanding :blue[the relationship between flow _Q_ and hydraulic head _h_ using Q–h plots for different boundary conditions]', divider="blue")


# --- MOTIVATION ---
st.markdown("""
#### 💡 Motivation - Boundary conditions and Q-h plots in groundwater modeling
Understanding how different boundary conditions influence groundwater flow is fundamental to building reliable groundwater models. Boundary conditions control how water enters, leaves, or interacts with the groundwater system, whether through defined heads, specified flows, or head-dependent exchanges such as rivers or drains. However, the behavior of these boundaries can be misinterpreted or misunderstood, especially in the early stages of model development.

This app provides an intuitive visual and interactive exploration of :orange[**Q–h plots**], graphical representations of the :orange[**relationship between discharge (_Q_) and hydraulic head (_h_) at boundary conditions**], also see the following figure. These Q-h plots are powerful conceptual tools to classify and compare the response of boundary conditions in groundwater models.
""")

left_co, cent_co, last_co = st.columns((20,80,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_Qh_scheme.png',caption="Schematic representation of an unconfined aquifer with a river boundary on the right side together with the associated Q-h plot.")

st.markdown(""" By simulating a simple 1D unconfined aquifer with recharge and various boundary types, users gain insight into the essential principles that govern groundwater model boundaries and their practical implications in tools like MODFLOW.

To support this learning, this initial part of the module applies a well-known analytical solution for 1D unconfined groundwater flow with recharge. It illustrates how different boundary types like defined head, defined flow, and head-dependent flow influence the resulting hydraulic head distribution. A key focus is placed on understanding the resulting Q–h relationships, which are central to the conceptualization and interpretation of boundary conditions in groundwater models like MODFLOW.

#### 🎯 Learning Objectives
By engaging with this section of the interactive module, you will be able to:

1. **Differentiate between defined head, defined flow, and head-dependent flow boundary conditions** and explain their conceptual roles in groundwater models.

2. **Interpret Q–h plots** to characterize the functional behavior of various boundary conditions and understand how they respond to changes in system inputs.

3. **Assess the influence of recharge and hydraulic conductivity** on the groundwater head distribution and the resulting flow dynamics at model boundaries.
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

# --- TYPES OF BOUNDARY CONDITIONS ---
st.subheader('🧪 Theory: Types of Boundary Conditions in Groundwater Modeling and Q-h plots for description', divider='blue')
st.markdown("""
In groundwater flow modeling, boundary conditions define how water enters, exits, or is restricted at the limits of the modeled domain. Understanding the different types of boundary conditions, and how they control the relationship between flow rate (Q) and hydraulic head (h), is essential for setting up realistic models and interpreting system behavior.

A **Q–h plot** displays this relationship graphically, helping to illustrate how a boundary responds to changes in model parameters and hydraulic conditions.
"""
)
with st.expander("Show more :blue[**explanation about the boundary condition types**]"):
    st.markdown("""
    Groundwater models use different boundary condition types to represent various hydrological settings and processes. Each type defines a specific characteristic for how flow and head interact at the boundary, reflecting the physical behavior of natural or engineered systems. Following, there is some explanation. The use cases can be investigate with two example configurations of an one-dimensional unconfined aquifer (:green[**Scenario 1**] and :red[**Scenario 2**]) that were implemented in two interactive plots. The interactive plots are presented in the subsequent section of this app (continue scrolling down to the bottom).
    
    #### 1. Defined Head Boundary (Dirichlet condition)
    
    **Definition:** Hydraulic head is fixed at a specific value.
    
    **Example application in the subsequent interactive plots:**
    - :green[**Scenario 1**]: The right boundary (_x_ = _L_) with user-defined water level (e.g., 150 m).
    - :red[**Scenario 2**]: The left and right boundary (x = 0 and _x_ = _L_).
    
    **Effect:** Simulates a strong external control like a large river/lake without colmation or the sea. Water flows through this boundary is driven by the hydraulic gradient. The hydraulic head is always defined and the boundary can serve as unlimited sink/source of water (e.g., imagine placing a high-capacity pumping well next to a defined head boundary. In this case, the boundary would always provide the required amount of water).
    
    #### 2. Defined-Flow Boundary (Neumann condition, special case is the Neumann conditions with zero flux)
    **Definition:** A defined flow of water crosses this boundary. A special case is the no-flow boundary with zero flow; the normal component of the flow is zero. Typical elements that are represented by this boundary condition are abstraction and infiltration wells and groundwater recharge.
    
    **Example application in the subsequent interactive plots:**
    - :green[**Scenario 1**]: The left boundary (x = 0) is a no-flow boundary, simulating an impermeable barrier. The recharge on the top is a defined flow bounary.
    - :red[**Scenario 2**]: In this scenario, the recharge on the top is a defined flow boundary.
    
    **Effect** of the defined flow boundary in the example (recharge): Water enters/leaves the system with a defined flow rate. *Effect** of a no-flow boundary in the example: Water cannot flow out/enter the system.
    
    #### 3. Head-Dependent Flux Boundary (Robin condition)
    **Definition:** The flow across the boundary is proportional to the difference between the aquifer head and an external water level (e.g., river stage, boundary head, drain elevation), controlled by a conductance factor.
    
    **Example application in the subsequent interactive plots:**
    - :green[**Scenario 1**]: The defined head boundary on the right becomes head-dependent when the River BC toggle is activated (under the assumption that the river is in contact with the aquifer and no unsaturated zone is established between river and aquifer).
    
    **Effect:** Simulates partial connection to a river or drain. Depending on the head difference between boundary and aquifer, the boundary can act as sink or source. In other words, the boundary acts as a “leaky” in-/outlet where both head and flow can change dynamically over time.
    
    _Note_: In some references this kind of boundary condition is denoted as Cauchy boundary. However, the mathematically correct terminology is Robin boundary. For more information, please refer to [Jazayeri and Werner (2019): Boundary Condition Nomenclature Confusion in Groundwater Flow Modeling](https://ngwa.onlinelibrary.wiley.com/doi/abs/10.1111/gwat.12893)
    """)
with st.expander("Show more :blue[**explanation about Q-h plots**] to describe boundary conditions"):
    st.markdown("""
    The relationship between discharge (Q) and hydraulic head (h) at model boundaries provides a powerful way to conceptualize and compare different types of boundary conditions in groundwater flow modeling. Q–h plots visually illustrate how flow into or out of a model domain responds to parameter changes, highlighting the fundamental behavior of defined-head, defined-flow, and head-dependent boundaries. These plots serve as intuitive tools to understand how boundary conditions influence system response, and how they are implemented in models like MODFLOW.
    
    The subsequent figure presents various Q-h plots to describe the boundary conditions in MODFLOW. The subsequent sections of this module allow to investigate and use the specific boundary conditions with interactive plots.
    """
    )
    lc1, cc1, rc1 = st.columns((10,60,10))
    with cc1:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/Q_h_plots_MF6.png', caption="Q-h plots to describe the behavior of boundary conditions, from  [Langevin et al., 2017](https://doi.org/10.3133/tm6A55.)")
    

# --- EXPLANATORY EXAMPLES ---
st.subheader('💫 Examples to illustrate the idea of illustrating boundary conditions with Q-h plots', divider='blue')
st.markdown("""
 In this app, we illustrate the effects of different boundary conditions using two example scenarios of 1D unconfined groundwater flow:
 
 - :green[**Scenario 1**]: with a **no-flow** boundary on one side and a **defined head** or a **head-dependent flow** boundary (e.g., river) on the other, and 
 - :red[**Scenario 2**]: with **two defined head** boundaries.
 
 In both examples, the defined head boundaries can optionally be treated as head-dependent boundaries to simulate typical boundaries like rivers and lakes in a more realistic way.
"""
)

lc1, rc1 = st.columns((1,1.4),gap = 'large')
with lc1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GWF_EX01.jpg', caption=":green[**Scenario 1**]:Conceptual model for an one dimensional unconfined groundwater system with **one defined head boundary and one no-flow boundary**.")
with rc1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GWF_EX02.png', caption=":red[**Scenario 2**]: Conceptual model for an one dimensional unconfined groundwater system with **two defined head boundaries**.")
    
with st.expander('Show more about the theory of the :blue[**model and the analytical solution**]'):
    st.markdown("""
            #### Conceptual model
            
            The conceptual model for both scenarios, shown in the figure above, consider the aquifer as a homogeneous and isotropic structure with a horizontal bottom. From the top, the aquifer receives uniform groundwater recharge.
            """, unsafe_allow_html=True)
    st.markdown("""
            In :green[**Scenario 1**], the aquifer is bounded by
            - one defined-head **or** a head-dependent flow boundary on the right side, while
            - the left side is a no-flow boundary.
            """, unsafe_allow_html=True)
    st.markdown("""
            In :red[**Scenario 2**], the aquifer is bounded
            - on both sides by defined-head boundaries.
            """, unsafe_allow_html=True)
    st.markdown("""
            These simple settings enables a clear understanding of boundary condition behavior, allowing analysis of groundwater flow and head distribution under different external constraints.
            """, unsafe_allow_html=True)
    st.markdown("""
            #### Mathematical model
            
            The governing equation for steady-state 1D groundwater flow in an unconfined, homogeneous aquifer with recharge for :green[**Scenario 1**] and :red[**Scenario 2**] is:
            """, unsafe_allow_html=True)
  
    st.latex(r'''\frac{d}{dx}(-hK\frac{dh}{dx})=R''')

    st.markdown("""
            with
            - _x_: spatial coordinate along the horizontal flow direction,
            - _h_: hydraulic head [m],
            - _K_: hydraulic conductivity [m/s],
            - _R_: recharge [m/s].
            """)
    st.markdown("""
            The equation can be solved by using suitable boundary conditions:
            
            :green[**Scenario 1**]: $h(0) = h_0$ and $h(2L) = h_0$, because the no-flow boundary is treated as a symmetry axis. This mirrors the hydraulic head $h_0$ across the boundary, resulting in identical head values at a distance of $2L$
            
            :red[**Scenario 2**]: $h(0) = h_0$ and $h(L) = h_L$
            
            """, unsafe_allow_html=True)
      
    st.markdown("""
            With some mathematical operations, see for example [Bakker and Post, 2022](https://doi.org/10.1201/9781315206134), the following analytical solutions can be derived:
            
            :green[**Scenario 1**]:
            
            """, unsafe_allow_html=True)  
    
    st.latex(r'''h(x) = \sqrt{h_0^2 + \frac{R}{K} \cdot x \cdot (2L - x)}''')
    
    st.markdown("""
            :red[**Scenario 2**]:
            """, unsafe_allow_html=True)  
            
    st.latex(r'''h(x) = \sqrt{h_0^2 - (h_0^2 - h_L^2)\cdot \frac{x}{L} + \frac{R}{K} \cdot x \cdot (L - x)}''')
    
    st.markdown("""
            where:
            - _h(x)_: hydraulic head at location _x_,
            - _L_: domain length [m],
            - _h<sub>0</sub>_: head at the defined-head boundary at _x_ = _0_.
            - _h<sub>L</sub>_: head at the defined-head boundary at _x_ = _L_.
            
            These solutions are subsequently used in the interactive plots to dynamically compute and visualize how different boundary conditions and recharge rates affect the hydraulic head distribution and the Q–h relationship.
            """, unsafe_allow_html=True)  
            

st.subheader('📈 Computation and visualization', divider='blue')
st.markdown("""Subsequently, the solutions are computed and results are visualized. You can vary the parameters to investigate the functional behavior. In general, you can modify the
- groundwater **recharge _R_** (in mm/a) and
- the **hydraulic conductivity _K_** (in m/s).

At the right side of the control panel you can plot the **Q-h relationship** for different boundary conditions. The position within the model plot that refers to the Q-h plot is marked by a colored circle. Additionally you con toggle to turn the Q-h plots 90 degrees clockwise (transfer to h-Q plots) for a more intuitive view.

Further modifications depends on your choice of :green[**Scenario 1**] or :red[**Scenario 2**]. 
""")

st.markdown("---")

# --- INTERACTIVE PLOT EXAMPLE 1 ---
colplot1, colplot2 = st.columns((1,1))
with colplot1:
    show_plot1 = st.button("**Show the :rainbow[interactive] plot for :green[SCENARIO 1]**")
with colplot2:
    show_plot2 = st.button("**Show the :rainbow[interactive] plot for :red[SCENARIO 2]**")

if show_plot1:    
    st.markdown("""
    :green[**Additional Instructions for Example 1:**]
    You can toggle between a defined head and a river boundary condition on the right side of the model. If the river boundary is choose, you can modify the river-aquifer conductance.   
    """
    )
    st.markdown("---") 
    # Fixed data
    L = 2500
    hr = 150.0
    zb = (hr-50)
    hRiv = 150
    y_scale = 7
    
    @st.fragment
    def computation1():
        # Input data
        # Define the minimum and maximum for the logarithmic scale
        log_min = -4.0 # Corresponds to 10^-7 = 0.0000001
        log_max = -2.0  # Corresponds to 10^0 = 1
        log_min2 = -5.5 
        log_max2 = -3.0 
    
        columns = st.columns((1,1,1), gap = 'small')
    
        with columns[0]:
            with st.expander("Click to modify **model parameters**:"):
                # Log slider for K with input and print
                K_slider_value=st.slider('_(log of) hydr. conductivity input:_', log_min,log_max,-3.5,0.01,format="%4.2f" )
                K = 10 ** K_slider_value
                st.write("**$K$ in m/s:** %5.2e" %K)
                st.write("")
                R = st.slider('_Recharge input:_',-300,300,0,1)
                st.write("**$R$ in mm/a:** %3i" %R)
                R = R/1000/365.25/86400
    
        with columns[1]:
            with st.expander("Click to modify **boundary condition parameters**:"):
                riv = st.toggle (':violet[**River BC?**]')
                if riv:
                    cRiv_slider = st.slider('_(log of) $C_{RIV}$ input_', log_min2,log_max2,-5.0,0.01,format="%4.2f")
                    cRiv = 10**cRiv_slider
                    st.write("**$C_{RIV}$:** %5.2e" %cRiv)
                    hr_riv = R * L / cRiv + hRiv
                
        with columns[2]:
            with st.expander("Click for **the Q-h plot**:"):
                if riv:
                    bc_type = st.radio("for the following boundary condition:",
                                  ["**None**", ":orange[**No-flow**]", ":green[**Recharge**]", ":violet[**River**]"], index=0)
                else:
                    bc_type = st.radio("for the following boundary condition:",
                                  ["**None**", ":orange[**No-flow**]", ":green[**Recharge**]", ":blue[**Defined head**]"], index=0)
                turn = st.toggle('Toggle to turn the plot 90 degrees', key="general_turn") 
        
        # --- Computation here
        x = np.arange(0, L, L/1000)
        
        if riv:
            phiL = 0.5 * K * (hr_riv - zb) ** 2
        else:
            phiL = 0.5 * K * (hr - zb) ** 2
        h = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K)
        
        # --- Q-h relationship functions ---
        
        # 1. Defined Head Boundary
        Q_defh = np.linspace((-400/1000/365.25/86400*2500), (400/1000/365.25/86400*2500), 10)
        h_defh = np.ones_like(Q_defh)* hr
        h_defh_point = hr
        Q_defh_point = R*2500*-1
        
        # 2a. Defined Flow Boundary (Q = 0)
        h_nf = np.linspace(140, 160, 20)
        Q_nf = np.zeros_like(h_nf)
        # Find the index where x is closest to 0
        x0 = np.argmin(np.abs(x - 0))
        h_nf_point = h[x0]
        Q_nf_point = 0.0
        
        # 2b. Defined Flow Boundary (Q = <>0)
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
        ax.set_xlabel(r'x [m]', fontsize=14)
        ax.set_ylabel(r'hydraulic head [m]', fontsize=14)
        
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
        if "Defined head" in bc_type:
            ax.plot(2500, h_defh_point, 'bo', markersize=10)
            ax.text(2425, h_defh_point+1.0, 'Q-h plot for this point', horizontalalignment='right', bbox=dict(boxstyle="square",facecolor='none', edgecolor='deepskyblue'), fontsize=12)
        if "River" in bc_type:
            ax.plot(2500, h_rob_point, 'o', color='fuchsia', markersize=10)
            ax.text(2425, h_rob_point+1.0, 'Q-h plot for this point', horizontalalignment='right', bbox=dict(boxstyle="square",facecolor='none', edgecolor='fuchsia'), fontsize=12)
        
        # Format plot
        ax.set_ylim(140,160)
        ax.set_xlim(-30,L+30)
        x_pos1 = 400
        x_pos2 = 2490
        y_pos1 = 158.8
        ax.text(x_pos1, y_pos1, 'No-flow bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='darkorange', alpha=0.4), fontsize=12)
        if riv:
            ax.text(x_pos2, y_pos1, 'River bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='fuchsia', alpha=0.4), fontsize=12)
        else:
            ax.text(x_pos2, y_pos1, 'Defined head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
            
        # --- Q–h PLOT in 2nd subplot ---
        if turn:
            ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_ylim(140,160)
            ax_qh.set_ylabel("hydraulic head [m]", fontsize=14)
            ax_qh.set_xlabel("flow into the model Qin [m³/s]", fontsize=14)
        else:
            ax_qh.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_xlim(140,160)
            ax_qh.set_xlabel("hydraulic head [m]", fontsize=14)
            ax_qh.set_ylabel("flow into the model Qin [m³/s]", fontsize=14)
        if "No-flow" in bc_type:
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_nf, h_nf, color='black', linewidth=3)
                ax_qh.plot(Q_nf_point, h_nf_point, 'ro', markersize=10)
                ax_qh.set_title("h-Q plot: Defined flow boundary (No-Flow)", fontsize=16, pad=15, color='orange')
                ax_qh.set_xlim(-1,1)
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else:            
                ax_qh.plot(h_nf, Q_nf, color='black', linewidth=3)
                ax_qh.plot(h_nf_point, Q_nf_point, 'ro', markersize=10)
                ax_qh.set_title("Q–h plot: Defined flow boundary (No-Flow)", fontsize=16, pad=15, color='orange')
                ax_qh.set_ylim(-1,1)
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Recharge" in bc_type:
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_rch, h_rch, color='black', linewidth=3)
                ax_qh.plot(Q_rch_point, h_rch_point, 'go', markersize=10)
                ax_qh.set_title("h-Q plot: Defined flow boundary (Recharge) at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_xlim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else:            
                ax_qh.plot(h_rch, Q_rch, color='black', linewidth=3)
                ax_qh.plot(h_rch_point, Q_rch_point, 'go', markersize=10)
                ax_qh.set_title("Q–h plot: Defined flow boundary (Recharge) at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_ylim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Defined head" in bc_type:      
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_defh, h_defh, color='black', linewidth=3)
                ax_qh.plot(Q_defh_point, h_defh_point, 'bo', markersize=10)
                ax_qh.set_title("h-Q plot: Defined head boundary", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h_defh, Q_defh, color='black', linewidth=3)
                ax_qh.plot(h_defh_point, Q_defh_point, 'bo', markersize=10)
                ax_qh.set_title("Q–h plot: Defined head boundary", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "River" in bc_type:      
            if turn:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q_rob, h_rob, color='black', linewidth=3)
                ax_qh.plot(Q_rob_point, h_rob_point, 'o', color='fuchsia', markersize=10)
                ax_qh.set_title("h-Q plot: River boundary", fontsize=16, pad=15, color = 'violet')
                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h_rob, Q_rob, color='black', linewidth=3)
                ax_qh.plot(h_rob_point, Q_rob_point, 'o', color='fuchsia', markersize=10)
                ax_qh.set_title("Q–h plot: River boundary", fontsize=16, pad=15, color = 'violet')
                ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        else:
            # Draw a blank subplot (white background, no ticks, no frame)
            ax_qh.axis('off')
        
        st.markdown("---")    
        st.pyplot(fig)
        
    computation1()

if show_plot2:
    
    st.markdown("""
    :red[**Additional Instructions for Example 2:**]
    You can modify the defined head elevation at the left side (the right side hydraulic head is defined as 150 m). The interactive plot will indicate the boundary flow (in- and outflow) for both defined head boundaries.   
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
        
        columns = st.columns((1,1,1), gap = 'small')

        with columns[0]:
            with st.expander("Click to modify **model parameters**:"):
                # Log slider for K with input and print
                K2_slider_value=st.slider('_(log of) hydr. conductivity input:_', log_min2,log_max2,-3.5,0.01,format="%4.2f" )
                K2 = 10 ** K2_slider_value
                st.write("**$K$ in m/s:** %5.2e" %K2)
                st.write("")
                R2 = st.slider('_Recharge input:_',-300,300,0,1)
                st.write("**$R$ in mm/a:** %3i" %R2)
                R2 = R2/1000/365.25/86400
        
        with columns[1]:
            with st.expander("Click to modify **boundary condition parameters**:"):
                hl2=st.slider('LEFT defined head', 145.,155.,150.,.1)
                riv2 = False
        
        with columns[2]:
            with st.expander("Click for **the Q-h plot**:"):
                if riv2:
                    bc_type2 = st.radio("for the following boundary condition:",
                                  ["**None**", ":green[**Recharge**]", ":blue[**Defined head left**]", ":violet[**River**]"], index=0)
                else:
                    bc_type2 = st.radio("for the following boundary condition:",
                                  ["**None**", ":green[**Recharge**]", ":blue[**Defined head left**]",":blue[**Defined head right**]"], index=0)
                turn2 = st.toggle('Toggle to turn the plot 90 degrees', key="general_turn2")         
        
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
        
        # 1. Defined Head Boundary
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
        
        # 2b. Defined Flow Boundary (Q = <>0)
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
        ax.set_xlabel(r'x [m]', fontsize=14)
        ax.set_ylabel(r'hydraulic head [m]', fontsize=14)
        ax.fill_between(x2,0,h2, facecolor='lightblue')
            
        # BOUNDARY CONDITIONS hl, hr
        ax.vlines(0, 0, hl2, linewidth = 10, color='deepskyblue')
        ax.vlines(L2, 0, hr2, linewidth = 10, color='deepskyblue')

        # Show the boundary plot position in the main plot
        if "Recharge" in bc_type2:
            ax.plot(1250, h2_rch_point, 'go', markersize=10)
            ax.text(1000, h2_rch_point+1.0, 'Q-h plot for this point', bbox=dict(boxstyle="square",facecolor='none', edgecolor='green'), fontsize=12)
        if "Defined head left" in bc_type2:
            ax.plot(0, h2_defh_point_l, 'bo', markersize=10)
            ax.text(75, h2_defh_point_l+1.0, 'Q-h plot for this point', horizontalalignment='left', bbox=dict(boxstyle="square",facecolor='none', edgecolor='deepskyblue'), fontsize=12)
        if "Defined head right" in bc_type2:
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
        ax.text(x2_pos1, y2_pos1, 'LEFT Defined head bc', horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
        
        # Box for boundary flow
        if R2 <= 0.0:
            ax.text(x2_pos1, y2_pos2, 'Q_BC_LEFT: {:.2e} m/s '.format(Q2_defh_point_l), horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
            ax.text(x2_pos2, y2_pos2, 'Q_BC_RIGHT: {:.2e} m/s '.format(Q2_defh_point_r), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
        else:
            ax.text(x2_pos1, y2_pos2, 'Q_BC_LEFT: {:.2e} m/s '.format(Q2_defh_point_l), horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
            ax.text(x2_pos2, y2_pos2, 'Q_BC_RIGHT: {:.2e} m/s '.format(Q2_defh_point_r), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey', alpha=0.4), fontsize=12)
        
        if riv2:
            ax.text(x2_pos2, y2_pos1, 'River bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='fuchsia', alpha=0.4), fontsize=12)
        else:
            ax.text(x2_pos2, y2_pos1, 'RIGHT Defined head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
            
        # MAKE 'WATER'-TRIANGLE
        h_arrow = (hl2**2-(hl2**2-hr2**2)/L2*(L2*0.96)+(R2/K2*(L2*0.96)*(L2-(L2*0.96))))**0.5  #water level at arrow
        ax.arrow(L2*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L2*0.015), head_length=(h_arrow*0.0015))
        ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L2*0.95, xmax=L2*0.97, colors='blue')   
        ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L2*0.955, xmax=L2*0.965, colors='blue')
        
        #ARROWS FOR RECHARGE 
        if R2 != 0:
            head_length=(R2*86400*365.25*1000*0.002)*y2_scale/5
            h_rch1 = (hl2**2-(hl2**2-hr2**2)/L2*(L2*0.25)+(R2/K2*(L2*0.25)*(L2-(L2*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
            ax.arrow(L2*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y2_scale), head_length=head_length)
            h_rch2 = (hl2**2-(hl2**2-hr2**2)/L2*(L2*0.50)+(R2/K2*(L2*0.50)*(L2-(L2*0.50))))**0.5  #water level at arrow for Recharge Postition 2
            ax.arrow(L2*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y2_scale), head_length=head_length)
            h_rch3 = (hl2**2-(hl2**2-hr2**2)/L2*(L2*0.75)+(R2/K2*(L2*0.75)*(L2-(L2*0.75))))**0.5  #water level at arrow for Recharge Position 3
            ax.arrow(L2*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y2_scale), head_length=head_length)
        
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
            ax_qh.set_ylabel("hydraulic head [m]", fontsize=14)
            ax_qh.set_xlabel("flow into the model Qin [m³/s]", fontsize=14)
        else:
            ax_qh.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            ax_qh.set_xlim(140,160)
            ax_qh.set_xlabel("hydraulic head [m]", fontsize=14)
            ax_qh.set_ylabel("flow into the model Qin [m³/s]", fontsize=14)
        if "Recharge" in bc_type2:
            if turn2:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q2_rch, h2_rch, color='black', linewidth=3)
                ax_qh.plot(Q2_rch_point, h2_rch_point, 'go', markersize=10)
                ax_qh.set_title("h-Q plot: Defined flow boundary (Recharge) at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_xlim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else:            
                ax_qh.plot(h2_rch, Q2_rch, color='black', linewidth=3)
                ax_qh.plot(h2_rch_point, Q2_rch_point, 'go', markersize=10)
                ax_qh.set_title("Q–h plot: Defined flow boundary (Recharge) at x = 1250 m", fontsize=16, pad=15, color = 'green')
                ax_qh.set_ylim(-(400/1000/365.25/86400),(400/1000/365.25/86400))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Defined head left" in bc_type2:      
            if turn2:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q2_defh, h2_defh_l, color='black', linewidth=3)
                ax_qh.plot(Q2_defh_point_l, h2_defh_point_l, 'bo', markersize=10)
                ax_qh.set_title("h-Q plot: Defined head boundary left", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h2_defh_l, Q2_defh, color='black', linewidth=3)
                ax_qh.plot(h2_defh_point_l, Q2_defh_point_l, 'bo', markersize=10)
                ax_qh.set_title("Q–h plot: Defined head boundary left", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_ylim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axhline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axvline(150, color='grey', linestyle='--', linewidth=0.8)
        elif "Defined head right" in bc_type2:      
            if turn2:
                ax_qh.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
                ax_qh.xaxis.set_major_locator(plt.MaxNLocator(3))  # Limit to 3 ticks
                ax_qh.plot(Q2_defh, h2_defh_r, color='black', linewidth=3)
                ax_qh.plot(Q2_defh_point_r, h2_defh_point_r, 'bo', markersize=10)
                ax_qh.set_title("h-Q plot: Defined head boundary right", fontsize=16, pad=15, color = 'blue')
                ax_qh.set_xlim(-(400/1000/365.25/86400*2500),(400/1000/365.25/86400*2500))
                ax_qh.axvline(0, color='grey', linestyle='--', linewidth=0.8)
                ax_qh.axhline(150, color='grey', linestyle='--', linewidth=0.8)
            else: 
                ax_qh.plot(h2_defh_r, Q2_defh, color='black', linewidth=3)
                ax_qh.plot(h2_defh_point_r, Q2_defh_point_r, 'bo', markersize=10)
                ax_qh.set_title("Q–h plot: Defined head boundary right", fontsize=16, pad=15, color = 'blue')
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
            # Draw a blank subplot (white background, no ticks, no frame)
            ax_qh.axis('off')

        st.markdown("---") 
        st.pyplot(fig)
    
    computation2()

st.subheader('✅ Conclusion', divider = 'blue')
st.markdown("""
Boundary conditions are the foundation of any groundwater model — they define how water enters, leaves, or interacts with the simulated domain. Each boundary type, whether defined head, defined flow, or head-dependent, represents a different physical assumption and has specific implications for model behavior.

This general module introduced the concept of **Q–h plots** as a powerful visual and conceptual tool. These plots help clarify the distinct flow–head relationships of different boundary types and support better understanding of model response and boundary sensitivity.

By exploring these relationships interactively, you've developed a more intuitive grasp of how boundary conditions function, how they differ, and why appropriate conceptualization is essential in MODFLOW modeling.

In the following boundary-specific sections of the module, you will now dive deeper into each condition — with visualizations, theory, and targeted assessments. But prior moving on, take the final assessment.
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
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')