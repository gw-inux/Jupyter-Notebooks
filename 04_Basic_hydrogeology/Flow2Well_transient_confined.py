# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st

# also Interactive Documents 03-05-005
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

st.title('Transient Flow towards a well in a confined aquifer')
st.header('Drawdown computation with the Theis solution', divider='green')
st.markdown("""This notebook illustrate the drawdown in a confined aquifer in response to pumping.""")

st.subheader('General situation', divider = 'blue')
st.markdown("""We consider a confined aquifer with constant transmissivity. If a well is pumping water out of the aquifer, radial flow towards the well is induced.

The calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined aquifer without further sinks and sources:""")
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')

st.subheader('Mathematical model and solution', divider = 'blue')
st.markdown("""Charles V. Theis presented a solution for this by deriving""")
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.markdown("""with the well function""")
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.markdown("""and the dimensionless variable""")
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.markdown("""Subsequently, the Theis equation is solved with Python routines.""")

st.subheader('Interactive plot', divider = 'blue')
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
    with st.expander("Characterize the Plot"):
        max_s = st.slider(f'Drawdown range in the plot (m)',1,50,20,1)
        max_r = st.slider(f'Distance range in the plot (m)',10,10000,1000,1)
        x_search = st.slider(f'Distance for result printoutrange in the plot (m)',0,2000,200,1)
        t = st.slider(f'**Time (s)**',0,86400*7,86400,600)
    
with columns[1]:
    Q = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
   
with columns[2]:
    with st.expander("Characterize the Aquifer"):
        T_slider_value=st.slider('(log of) Transmissivity in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        T = 10 ** T_slider_value
        # Display the logarithmic value
        st.write("**Transmissivity in m2/s:** %5.2e" %T)
        S_slider_value=st.slider('(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        S = 10 ** S_slider_value
        # Display the logarithmic value
        st.write("**Storativity (dimensionless):** %5.2e" %S)

# Range of delta_h / delta_l values (hydraulic gradient)
r = np.linspace(1, max_r, 200)
r_neg = r * -1.0
    
# Compute Q for each hydraulic gradient
s  = compute_s(T, S, t, Q, r)

# Compute s for a specific point
x_point = x_search
y_point = compute_s(T, S, t, Q, x_search)
    
# Plotting
fig=plt.figure(figsize=(10, 6))
    
plt.plot(r, s, linewidth=1., color='b', label=r'drawdown prediction')
plt.plot(r_neg, s, linewidth=1, color='b')
plt.fill_between(r,s,max_s, facecolor='lightblue')
plt.fill_between(r_neg,s,max_s, facecolor='lightblue')
plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='drawdown output') 
plt.xlabel(r'Distance from the well in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.title('Drawdown prediction with Theis', fontsize=16)
plt.legend()
plt.grid(True)

st.pyplot(fig)

st.write("DRAWDOWN output:")
st.write("Distance from the well (in m): %8.2f" %x_point)
st.write('Drawdown at this distance (in m):  %5.2f' %y_point)
st.write('Time (in sec): ',t)

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')