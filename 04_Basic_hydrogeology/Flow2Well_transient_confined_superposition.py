# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st

st.title('Transient Flow towards a well in a confined aquifer')

st.subheader('Consideration of two wells with :orange[superposition]', divider="orange")

st.write('This notebook illustrate the drawdown in a confined aquifer in response to pumping.')

st.subheader('General situation')
st.write('We consider a confined aquifer with constant transmissivity. If a well is pumping water out of the aquifer, radial flow towards the well is induced.')
st.write('The calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined aquifer without further sinks and sources:')
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')

st.subheader('Mathematical model and solution')
st.write('Charles V. Theis presented a solution for this by deriving')
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.write('with the well function')
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.write('and the dimensionless variable')
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.write('Subsequently, the Theis equation is solved with Python routines.')
"---"

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

   
columns = st.columns((1,1), gap = 'large')

with columns[0]:
    max_s = st.slider(f'Drawdown range in the plot (m)',1,50,10,1)
    max_r = st.slider(f'Distance range in the plot (m)',10,10000,1000,1)
    x_search = st.slider(f'Distance for result printoutrange in the plot (m)',0,10000,0,1)
    t = st.slider(f'**Time (s)**',0,86400*7,86400,600)
    
with columns[1]:
    container = st.container()
    T_slider_value=st.slider('_(log of) Transmissivity in m2/s_', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    T = 10 ** T_slider_value
    # Display the logarithmic value
    container.write("**Transmissivity in m2/s:** %5.2e" %T)
    S_slider_value=st.slider('(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    S = 10 ** S_slider_value
    # Display the logarithmic value
    st.write("**Storativity (dimensionless):** %5.2e" %S)
    #
    with st.expander('Use cases'):
        case = st.selectbox("**What situation should be considered?**",
              ("Two wells same pumping", "Two wells different pumping", "Well with noflow bc", "Well with infiltration bc"), key = 'case')
        if st.session_state.case == 'Two wells same pumping':
            distanz = st.slider(f'**Distance between wells** (m)',10,1500,500,10, key = 'Distanz')
            Q1 = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
            Q2 = Q1
        elif st.session_state.case == 'Two wells different pumping':
            distanz = st.slider(f'**Distance between wells** (m)',10,1500,500,10, key = 'Distanz')
            Q1 = st.slider(f'**Pumping rate well A (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
            Q2 = st.slider(f'**Pumping rate well B (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
        elif st.session_state.case == 'Well with noflow bc':
            distanzbc = st.slider(f'**Distance from the well to the boundary** (m)',5,750,250,5, key = 'Distanz2')
            distanz = 2*distanzbc
            Q1 = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
            Q2 = Q1
        elif st.session_state.case == 'Well with infiltration bc':
            distanzbc = st.slider(f'**Distance from the well to the boundary** (m)',5,750,250,5, key = 'Distanz2')
            distanz = 2*distanzbc
            Q1 = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
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
    
plt.plot(r1, s1, linewidth=1., color='b', label=r'drawdown well A')
plt.plot(r1_neg, s1, linewidth=1, color='b')
plt.plot(r2, s2, linewidth=1., color='g', label=r'drawdown well B')
plt.plot(r2_neg, s2, linewidth=1, color='g')
plt.plot(r_super, s_super, linewidth=1, color='black',label=r'total drawdown')
plt.fill_between(r_super,s_super,max_s, facecolor='lightblue')
#plt.fill_between(r1_neg,s1,max_s, facecolor='lightblue')
plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.xlabel(r'spatial coordinate in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.title('Drawdown prediction with Theis', fontsize=16)
if st.session_state.case == 'Well with noflow bc':
    ax.vlines(0, max_s, -5, linewidth = 1, color='darkblue', label='No Flow Boundary')
if st.session_state.case == 'Well with infiltration bc':
    ax.vlines(0, max_s, -5, linewidth = 1, color='green', label='Infiltration Boundary')
plt.legend()
plt.grid(True)

st.pyplot(fig)