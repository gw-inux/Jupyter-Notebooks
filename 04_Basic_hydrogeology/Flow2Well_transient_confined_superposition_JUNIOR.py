# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy.special
import streamlit as st
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

tree_img = mpimg.imread("04_Basic_hydrogeology/FIGS/grass.png")  # your file

def add_tree_icon(ax, x, y, zoom=0.08):
    """Place a tree icon at coordinate (x, y)."""
    # Create a NEW OffsetImage for each tree so we don't reuse the same instance
    image_obj = OffsetImage(tree_img, zoom=zoom)
    ab = AnnotationBbox(image_obj, (x, y), frameon=False, zorder=6)
    ax.add_artist(ab)
    
def add_trees_on_structure_icons(ax, x_left, structure_width, ground_y=0.0, zoom=0.08):
    # Calculate number of trees based on equation
    n_trees = max(1, int(structure_width / 30))  # ensure at least 1 tree
    
    # One tree should be centered / multiple trees should be distributed
    if n_trees == 1:
        x = x_left + structure_width*0.5
        add_tree_icon(ax, x, ground_y - 0.2, zoom=zoom)  # adjust y offset as needed
    else:
        margin = 0.08 * structure_width
        xs = np.linspace(x_left + margin,
                         x_left + structure_width - margin,
                         n_trees)      
        for x in xs:
            add_tree_icon(ax, x, ground_y - 0.2, zoom=zoom)  # adjust y offset as needed

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s
    
def update_Q2():
    st.session_state.Q2 = st.session_state.Q2_input
    
st.title('Pumping with two well :rainbow[**JUNIOR Edititon**]')

st.subheader('Prevent the nature conservation area from :orange[running dry]', divider="blue")

st.markdown(r"""
### **Introduction and Motivation**  
We are looking in a cut-off from the underground. The blue structure is the water-filled aquifer. There are two wells that are pumping water - the :blue[**Blue**] well from your neighbor and :red[**your**] :green[**Green**] well.  
""", unsafe_allow_html=True)


with st.expander('Show more theory'):
    st.markdown(r"""
    To calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined aquifer without further sinks and sources:

    $\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}$  
    
    #### Mathematical model and solution
    
    Charles V. Theis presented a solution for this by deriving
    
    $s(r,t)=\frac{Q}{4\pi T}W(u)$
    
    with the well function
    
    $W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u$
    
    and the dimensionless variable
    
    $u = \frac{Sr^2}{4Tt}$
    
    Subsequently, the Theis equation is solved with Python routines and the individual results are combined to represent the overall system response according to the principle of superposition.
        
    """, unsafe_allow_html=True)

'---'
st.subheader('Become :green[**ACTIVE**] with the interactive plot', divider = 'blue')

st.markdown(r"""
You can modify the pumping rate of your well. In addition you can also modify the time to see how the cone of drawdown developed in the past.  
""", unsafe_allow_html=True)

# (Here, the method computes the data for the well function. Those data can be used to generate a type curve.)
u_max = 1
r_max = 10000
u  = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]


# Get input data
# Define the minimum and maximum for the logarithmic scale

#defined values

T = 5e-3
S = 1e-5
max_s = 20
max_r = 1000

distanz = 750
# --- Vertical structure between the wells ---
# Random width/depth
structure_width = np.random.uniform(30.0, 250.0)
structure_depth = np.random.uniform(2.0, 8.0)
structure_center_x = np.random.uniform(-50., 50.)  # midpoint between wells

#Random pumping
Q1 = np.random.uniform(0.002,0.020)

# Reset on first run
Q2_ini = 0.0
    
@st.fragment
def plot():
    
    columns = st.columns((1,1,1))
    
    with columns[2]:
        t = st.slider(f'**Time (s)**',0,86400*21,21*86400,86400)
        
    with columns[0]:
        Q2 = st.slider(f'**Pumping rate of your well (m³/s)**', 0.000,0.100, Q2_ini, 0.001,format="%5.3f")
    
    # Range of delta_h / delta_l values (hydraulic gradient)
    r = np.linspace(1, max_r+distanz, 200)
    
    r1 = r + 0.5*distanz
    r2 = r - 0.5*distanz
    r1_neg = r1 * -1.0 + distanz
    r2_neg = r2 * -1.0 - distanz
        
    # Compute Q for each hydraulic gradient
    s1  = compute_s(T, S, t, Q1, r)
    s2  = compute_s(T, S, t, Q2, r)
    
    # Superposition
    num_steps = 500
    r_super = np.linspace(-1000, 1000, num_steps)
    s_super = []
    
    for x in r_super:
        y1 = compute_s(T, S, t, Q1, x-0.5*distanz)
        y2 = compute_s(T, S, t, Q2, x+0.5*distanz)
        y3 = y1 + y2
        s_super.append(y3)
        
    # Plotting
    fig=plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)

    plt.plot(r_super, s_super, linewidth=2, color='dodgerblue')
    plt.fill_between(r_super,s_super,max_s, facecolor='aqua')
    
    plt.xlim(-max_r, max_r)
    plt.ylim(max_s,-5)
    plt.xlabel(r'spatial coordinate in m', fontsize=14)
    plt.ylabel(r'Drawdown in m', fontsize=14)
    plt.title('Drawdown prediction with Theis - principle of superposition', fontsize=16)
    
    # --- Vertical structure between the wells ---
    x_left = structure_center_x - structure_width / 2.0
    y_top  = 0.0  # start at the surface line (drawdown = 0)
    
    rect = Rectangle(
        (x_left, y_top),
        structure_width,
        structure_depth,
        facecolor='chartreuse',
        alpha=0.6,
        edgecolor='magenta',  
        linewidth=2,             
        zorder=3  # make sure it’s visible above the blue fill
    )
    ax.add_patch(rect)
    add_trees_on_structure_icons(ax, x_left, structure_width, ground_y=-1.0, zoom=0.08)

    # Optional: legend handle for the structure
    structure_handle = Rectangle((0, 0), 1, 1, facecolor='tan', alpha=0.7, edgecolor='none')
    ax.hlines(0, -max_r, max_r, linewidth = 3, color='seagreen')
    
    ax.vlines(0.5*distanz, max_s, -0.5, linewidth = 5, color='blue')
    ax.vlines(-0.5*distanz, max_s, -0.5, linewidth = 5, color='green')
    plt.text (  0.5*distanz, -1, 'pumping \n well 1', horizontalalignment='center', fontsize=12)
    plt.text (- 0.5*distanz, -1, 'pumping \n well 2', horizontalalignment='center', fontsize=12)
    
    handles, labels = ax.get_legend_handles_labels()
    handles.append(structure_handle)
    labels.append('The root zone of the nature protection area')
    plt.legend(handles, labels, loc='lower right', fontsize=12)
    
    st.pyplot(fig)

plot()

# Move the button to appear below the plot
columns5 = st.columns((1.5,1,1), gap='large')
with columns5[1]:
    st.button(":rainbow[**RUN AGAIN**]")

'---'

# Copyright
col1, col2 = st.columns([1, 5], gap = 'large')  # Adjust column width ratio
with col1:
    st.image('04_Basic_hydrogeology/FIGS/logo_iNUX.jpg', width=125)
with col2:
    st.markdown("© 2025 iNUX Project - Interactive understanding of groundwater hydrology and hydrogeology - An ERASMUS+ cooperation project.<br>App developer: Thomas Reimann (TU Dresden)", unsafe_allow_html=True)