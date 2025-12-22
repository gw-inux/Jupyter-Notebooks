# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st

# also Interactive Documents 03-05-006
# ToDo:
#    - K log slider
#    - number input

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface
st.title('Transient Flow towards wells and superposition')
st.subheader('Consideration of two wells under the principle of :orange[superposition]', divider="orange")

st.markdown(r"""
### **Introduction and Motivation**  
We consider a confined, homogeneous, isotropic aquifer with constant transmissivity. Water abstraction will induce radial flow towards the well. The hydraulic situation can be calculated with the Theis solution.

Accoding to the principle of superposition, the drawdown of different wells in one space is added, see the following figure.  
""", unsafe_allow_html=True)

lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('04_Basic_hydrogeology/FIGS/ferris_no_flow_small.png', caption="Conceptual sketch through an aquifer with one pumping well and an imaginary well to represent a no-flow boundary [Ferris et al. 1962]( https://pubs.usgs.gov/wsp/wsp1536-E/).")

st.markdown(r"""
### This app allows to investigate the principle of superposition for two abstraction wells. The pumping rate can be uniform or different.

Further, the principle of superposition can also be used to account for the effect of no-flow and infiltration boundaries.  
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
st.subheader('Computation of well drawdown with the principle of superposition', divider = 'orange')

st.markdown(r"""
The menu point '**Use cases**' allows you to choose different scenarios and to modify the pumping rate and the position of the wells.  
""", unsafe_allow_html=True)
# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

# (Here, the method computes the data for the well function. Those data can be used to generate a type curve.)
u_max = 1
r_max = 10000
u  = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s


# This is the function to plot the graph with the data     

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1

   
columns = st.columns((1,1,1))

with columns[0]:
    with st.expander('Modify the plot'):
        max_s = st.slider(f'Drawdown range in the plot (m)',1,50,20,1)
        max_r = st.slider(f'Distance range in the plot (m)',10,10000,1000,1)
        #x_search = st.slider(f'Distance for result printoutrange in the plot (m)',0,10000,0,1)
    t = st.slider(f'**Time (s)**',0,86400*7,86400,600)
    
with columns[1]:
    with st.expander('Hydraulic parameters'):
        # Transmissivity
        container = st.container()
        Ts =st.slider('_(log of) Transmissivity in m2/s_', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        T  = 10 ** Ts
        container.write("**Transmissivity in m2/s:** %5.2e" %T)
        # Storativity
        container = st.container()
        Ss=st.slider('_(log of) Storativity_', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        S = 10 ** Ss
        container.write("**Storativity (dimensionless):** %5.2e" %S)
with columns[2]:
    with st.expander('Use cases'):
        case = st.selectbox("**What situation should be considered?**",
              ("Two wells same pumping", "Two wells different pumping", "Well with noflow bc", "Well with infiltration bc"), key = 'case')
        if st.session_state.case == 'Two wells same pumping':
            distanz = st.slider(f'**Distance between wells** (m)',10,1500,500,10, key = 'Distanz')
            Q1 = st.slider(f'**Pumping rate (m^3/s)**', 0.000,0.100,0.005,0.001,format="%5.3f")
            Q2 = Q1
        elif st.session_state.case == 'Two wells different pumping':
            distanz = st.slider(f'**Distance between wells** (m)',10,1500,500,10, key = 'Distanz')
            Q1 = st.slider(f'**Pumping rate well 1 (m³/s)**', 0.000,0.100,0.005,0.001,format="%5.3f")
            Q2 = st.slider(f'**Pumping rate well 2 (m³/s)**', 0.000,0.100,0.002,0.001,format="%5.3f")
        elif st.session_state.case == 'Well with noflow bc':
            distanzbc = st.slider(f'**Distance from the well to the boundary** (m)',5,750,250,5, key = 'Distanz2')
            distanz = 2*distanzbc
            Q1 = st.slider(f'**Pumping rate (m³/s)**', 0.000,0.100,0.005,0.001,format="%5.3f")
            Q2 = Q1
        elif st.session_state.case == 'Well with infiltration bc':
            distanzbc = st.slider(f'**Distance from the well to the boundary** (m)',5,750,250,5, key = 'Distanz2')
            distanz = 2*distanzbc
            Q1 = st.slider(f'**Pumping rate (m³/s)**', 0.000,0.100,0.005,0.001,format="%5.3f")
            Q2 = Q1*-1

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
    
plt.plot(r1, s1,     linewidth=1., color='b', label=r'drawdown well 1')
plt.plot(r1_neg, s1, linewidth=1., color='b')
plt.plot(r2, s2,     linewidth=1., color='g', label=r'drawdown well 2')
plt.plot(r2_neg, s2, linewidth=1., color='g')
plt.plot(r_super, s_super, linewidth=2, color='black',label=r'resulting drawdown')

plt.fill_between(r_super,s_super,max_s, facecolor='lightblue')

plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.xlabel(r'spatial coordinate in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.title('Drawdown prediction with Theis - principle of superposition', fontsize=16)

if st.session_state.case == 'Two wells same pumping':
    ax.vlines(0.5*distanz, max_s, -0.5, linewidth = 3, color='darkblue')
    ax.vlines(-0.5*distanz, max_s, -0.5, linewidth = 3, color='darkgreen')
    plt.text (  0.5*distanz, -1, 'pumping \n well', horizontalalignment='center', fontsize=12)
    plt.text (- 0.5*distanz, -1, 'pumping \n well', horizontalalignment='center', fontsize=12)
if st.session_state.case == 'Two wells different pumping':
    ax.vlines(0.5*distanz, max_s, -0.5, linewidth = 3, color='darkblue')
    ax.vlines(-0.5*distanz, max_s, -0.5, linewidth = 3, color='darkgreen')
    plt.text (  0.5*distanz, -1, 'pumping \n well 1', horizontalalignment='center', fontsize=12)
    plt.text (- 0.5*distanz, -1, 'pumping \n well 2', horizontalalignment='center', fontsize=12)
if st.session_state.case == 'Well with noflow bc':
    ax.vlines(0, max_s, -5, linestyle="--", linewidth = 2, color='black')
    ax.vlines(0.5*distanz, max_s, -0.5, linewidth = 3, color='darkblue')
    ax.vlines(-0.5*distanz, max_s, -0.5, linestyle=":", linewidth = 3, color='darkgreen')
    plt.text (120, max_s-1, 'real \n system', horizontalalignment='center', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
    plt.text (-150, max_s-1, 'imaginary \n system', horizontalalignment='center', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
    plt.text (  0.55*distanz, 1, 'real \n pumping well', horizontalalignment='left', fontsize=12)
    plt.text (- 0.55*distanz, 1, 'imaginary \n pumping well', horizontalalignment='right', fontsize=12)
    plt.text (-20, max_s-5, 'no flow boundary', rotation=90, horizontalalignment='right', fontsize=12)
if st.session_state.case == 'Well with infiltration bc':
    ax.vlines(0, max_s, -5, linestyle="--", linewidth = 2, color='black')
    ax.vlines(0.5*distanz, max_s, -0.5, linewidth = 3, color='darkblue')
    ax.vlines(-0.5*distanz, max_s, -0.5, linestyle=":", linewidth = 3, color='darkgreen')
    plt.text (120, max_s-1, 'real \n system', horizontalalignment='center', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
    plt.text (-150, max_s-1, 'imaginary \n system', horizontalalignment='center', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
    plt.text (  0.55*distanz, 5, 'real \n pumping well', horizontalalignment='left', fontsize=12)
    plt.text (- 0.55*distanz, 1, 'imaginary \n infiltration well', horizontalalignment='right',  fontsize=12)
    plt.text (-20, max_s-5, 'discharge boundary', rotation=90, horizontalalignment='right', fontsize=12)
    
plt.legend(loc='lower right', fontsize=12)

st.pyplot(fig)
if st.session_state.case == 'Well with noflow bc':
    with st.expander('Here you can find additional explanation'):
        st.image('04_Basic_hydrogeology/FIGS/ferris_no_flow.png', caption="Conceptual sketch through an aquifer with one pumping well and an imaginary well to represent a no-flow boundary [Ferris et al. 1962]( https://pubs.usgs.gov/wsp/wsp1536-E/).")

if st.session_state.case == 'Well with infiltration bc':
    with st.expander('Here you can find additional explanation'):
        st.image('04_Basic_hydrogeology/FIGS/ferris_infiltration.png', caption="Conceptual sketch through an aquifer with one pumping well and an imaginary well to represent an infiltration boundary [Ferris et al. 1962]( https://pubs.usgs.gov/wsp/wsp1536-E/).")

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')