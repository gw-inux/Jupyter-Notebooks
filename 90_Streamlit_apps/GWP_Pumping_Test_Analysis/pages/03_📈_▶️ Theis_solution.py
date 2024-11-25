# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import pandas as pd
import streamlit as st
import streamlit_book as stb

st.title('Theis parameter estimation')

st.subheader('Understanding the :red [characteristics and behavior of the Theis solution]', divider="red")
st.markdown("""
            ### Introductionary remarks
"""
)
# Initial assessment

columnsQ1 = st.columns((1,1), gap = 'large')

with columnsQ1[0]:
    stb.single_choice(":red[**For which conditions is the Theis solution intended?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
    stb.single_choice(":red[**Question2?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
                  
with columnsQ1[1]:
    stb.single_choice(":red[**Question3?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')             
    stb.single_choice(":red[**Question4?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
"---"
# Computation
# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_min = -5
u_max = 4

u = np.logspace(u_min,u_max)
u_inv = 1/u
w_u = well_function(u)


# Data from SYMPLE exercise
m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
# Parameters needed to solve Theis (From the SYMPLE example/excercise)
r = 120       # m
b = 8.5       # m
Qs = 0.3/60   # m^3/s
Qd = Qs*60*60*24 # m^3/d

m_time_s = [i*60 for i in m_time] # time in seconds
num_times = len(m_time)

st.subheader(':green[Inverse parameter fitting]', divider="rainbow")

st.markdown("""
            Subsequently, you can modify the transmissivity and the storativity to fit your measured data to the Theis type curve. For precise fitting, you can change the plot resolution with the toogle. Additionally, you can perform a prediction of drawdown for specific times/spaces.
"""
)

@st.fragment
def inverse():
    # This is the function to plot the graph with the data     
    # Get input data
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
    log_max2 = 0.0  # S / Corresponds to 10^0 = 1
   
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        T_slider_value=st.slider('(log of) **Transmissivity** in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        T = 10 ** T_slider_value
        # Display the logarithmic value
        st.write("_Transmissivity_ in m2/s: %5.2e" %T)
        S_slider_value=st.slider('(log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        Ss = 10 ** S_slider_value
        # Display the logarithmic value
        st.write("_Specific storage_ (dimensionless):** %5.2e" %Ss)
        refine_plot = st.toggle("**Refine** the range of the **Data matching plot**")
    
    # Compute K and SS to provide parameters for plausability check
    # (i.e. are the parameter in a reasonable range)
    K = T/b     # m/s
    S = Ss * b
    
   
    # Early (a) and late (b) Theis curve
    t_term = r**2 * S / 4 / T
    s_term = Qs/(4 * np.pi * T)

    t = u_inv * t_term
    s = w_u * s_term
        
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(t, s, label=r'Computed drawdown - Theis')
    ax.plot(m_time_s, m_ddown,'ro', label=r'measured drawdown')
    plt.yscale("log")
    plt.xscale("log")
    if refine_plot:
        plt.axis([1E-0,1E4,1E-1,1E+1])
    else:
        plt.axis([1E-1,1E5,1E-4,1E+1])
    ax.set(xlabel='t', ylabel='s',title='Neuman drawdown')
    ax.grid(which="both")
    plt.legend()
    st.pyplot(fig)

    columns3 = st.columns((1,1), gap = 'medium')
    with columns3[0]:
        st.write("**Parameter estimation**")
        st.write("Distance of measurement from the well (in m): %3i" %r)
        st.write("Pumping rate of measurement (in m^3/s): %5.3f" %Qs)
        st.write("Thickness of formation b = ","% 5.2f"% b, " m")
        st.write("Transmissivity T = ","% 10.2E"% T, " m^2/s")
        st.write("(Hydr. cond. K) = ","% 10.2E"% (T/b), " m^2/s")
        st.write("Storativity    S = ","% 10.2E"% S, "[-]")

inverse()
