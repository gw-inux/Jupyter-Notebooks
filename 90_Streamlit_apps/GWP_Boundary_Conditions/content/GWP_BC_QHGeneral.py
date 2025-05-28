# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import streamlit as st

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
st.subheader('Understanding :blue[the Q-h plot for different boundary conditions]', divider="blue")

st.markdown("""This interactive app demonstrates the fundamental types of boundary conditions in groundwater modeling using a well-known 1D analytical solution for unconfined flow with recharge. It allows users to explore how different boundary types—defined head, defined flow, and head-dependent flow—influence the hydraulic head distribution. A key focus is placed on understanding the resulting Q–h relationships, which are central to the conceptualization and interpretation of boundary conditions in groundwater models like MODFLOW.
""")

with st.expander('Initial assessment'):
    st.write('Here we will add 3-4 MC questions')

st.subheader('💡 Types of Boundary Conditions in Groundwater Modeling and Q-h plots for description', divider='blue')
st.markdown("""
In groundwater flow modeling, boundary conditions define how water enters, exits, or is restricted at the limits of the modeled domain. In this app, we illustrate their effects using a 1D unconfined aquifer receiving uniform recharge, bounded by a no-flow boundary on one side and either a constant head or a head-dependent flux boundary (e.g., river) on the other.
"""
)
with st.expander("Show more :blue[**explanation about the boundary condition types**]"):
    st.markdown("""
    #### 1. Defined Head Boundary (Dirichlet condition)
    **Definition:** Hydraulic head is fixed at a specific value.
    
    **Example in the app:** The right boundary (x = L) with fixed water level (e.g., 150 m).
    
    **Effect:** Simulates a strong external control like a large river or lake. Water flows to this boundary depending on the head difference and recharge.
    
    #### 2. Defined-Flow Boundary (Neumann condition, special case is the Neumann conditions with zero flux)
    **Definition:** A defined flow of water crosses this boundary. A special case is the no-flow boundary with zero flow; the normal component of the flow is zero.
    
    **Example in the app:** The left boundary (x = 0) is a no-flow boundary, simulating a symmetry line or impermeable barrier. The recharge on the top is a defined flow bounary.
    
    **Effect** of the no-flow boundary in the example: Water cannot flow out; it forces groundwater to move in one direction—towards the right.
    **Effect** of the defined flow boundary in the example (recharge): Water enters the system with a defined flow rate. In response, water flow towards the system outlet is initiated.
    
    #### 3. Head-Dependent Flux Boundary (Robin condition)
    **Definition:** The flow across the boundary is proportional to the difference between the aquifer head and an external water level (e.g., river stage), controlled by a conductance factor.
    
    **Example in the app:** The right boundary becomes head-dependent when the River BC toggle is activated.
    
    **Effect:** Simulates partial connection to a river or drain. The boundary acts as a “leaky” outlet where both head and flow can change dynamically.
    
    _Note_: In some references this kind of boundary condition is denoted as Cauchy boundary. However, the mathematically correct terminology is Robin boundary. For more information, please refer to [Jazayeri and Werner (2019): Boundary Condition Nomenclature Confusion in Groundwater Flow Modeling](https://ngwa.onlinelibrary.wiley.com/doi/abs/10.1111/gwat.12893)
    """)
with st.expander("Show more :blue[**explanation about Q-h plots**] to describe boundary conditions"):
    st.markdown("""
    The relationship between discharge (Q) and hydraulic head (h) at model boundaries provides a powerful way to conceptualize and compare different types of boundary conditions in groundwater flow modeling. Q–h plots visually illustrate how flow into or out of a model domain responds to parameter changes, highlighting the fundamental behavior of defined-head, defined-flow, and head-dependent boundaries. These plots serve as intuitive tools to understand how boundary conditions influence system response, and how they are implemented in models like MODFLOW.
    
    The subsequent figure presents various Q-h plots to describe the boundary conditions in MODFLOW. The subsequent sections of this module allow to investigate and use the specific boundary conditions with interactive plots.
    """
    )
    lc1, cc1, rc1 = st.columns((20,60,20))
    with cc1:
        st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/Q_h_plots_MF2005.png', caption="Q-h plots to describe the behavior of boundary conditions. onceptual model for a groundwater system with one no-flow boundary, from  (Harbaugh, 2005; https://pubs.usgs.gov/tm/2005/tm6A16/).")
    

lc1, cc1, rc1 = st.columns((20,60,20))
with cc1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/GWF_008.jpg', caption="Conceptual model for a groundwater system with one no-flow boundary.")

with st.expander('Show more about the theory of the :blue[**model and the analytical solution**]'):
    st.markdown("""
            ### Conceptual model
            
            The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by one defined-head boundary on the right side (left side is no-flow). From the top, the aquifer receives uniform groundwater recharge.
            """, unsafe_allow_html=True)

    st.markdown("""
            ### Mathematical model
            
            The equation for 1D groundwater flow in a homogeneous aquifer is
            """, unsafe_allow_html=True)
            
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')

    st.markdown("""
            with
            - _x_ is spatial coordinate along flow,
            - _h_ is hydraulic head,
            - _K_ is hydraulic conductivity,
            - _R_ is recharge.
            
            A solution for the equation can be obtained with... TODO
            
            """, unsafe_allow_html=True)
            
st.markdown("---")

st.subheader('Computation and visualization', divider='blue')
st.markdown("""Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the
- groundwater **recharge _R_** (in mm/a) and
- the **hydraulic conductivity _K_** (in m/s).

You can further toggle between a defined head and a river boundary condition on the right side of the model. 

At the right side of the control panel you can plot the Q-h relationship for different boundary conditions. The position within the model plot that refers to the Q-h plot is marked by a colored circle. Additionally you con toggle to turn the Q-h plots 90 degrees clockwise (transfer to h-Q plots) for a more intuitive view.""")

st.markdown("---")

# Fixed data
L = 2500
hr = 150.0
zb = (hr-50)
hRiv = 150
y_scale = 7

@st.fragment
def computation():
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
        riv = st.toggle (':violet[**River BC?**]')
        if riv:
            #hRiv = st.slider('River head', hr, hr+5.0, hr, 0.01)
            cRiv_slider = st.slider('_(log of) $C_{RIV}$ input_', log_min2,log_max2,-5.0,0.01,format="%4.2f")
            cRiv = 10**cRiv_slider
            st.write("**$C_{RIV}$:** %5.2e" %cRiv)
 #           hr_riv = R * L / cRiv / zb + hRiv
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
    # Computation here
    
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
    Q_defh_point = R*2500
    
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
    ax.set_title('Hydraulic head for 1D unconfined flow', fontsize=16, pad=10)
    ax.set_xlabel(r'x [m]', fontsize=14)
    ax.set_ylabel(r'hydraulic head [m]', fontsize=14)
    
    # BOUNDARY CONDITIONS hl, hr
    ax.vlines(0, 0, 1000, linewidth = 10, color='darkorange', alpha = 0.7)
    if riv:
        ax.vlines(L, 0, hr, linewidth = 10, color='deepskyblue')
        ax.vlines(L-5, 0, hr_riv, linewidth = 3, color='fuchsia')
    else:
        ax.vlines(L, 0, hr, linewidth = 10, color='deepskyblue')
    # MAKE 'WATER'-TRIANGLE
    #h_arrow = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L*0.96 ** 2) + phiL) / K)  #water level at arrow
    #ax.arrow(100,150, 0.1,0.1)
    #ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
    #ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')
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
    
computation()

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')