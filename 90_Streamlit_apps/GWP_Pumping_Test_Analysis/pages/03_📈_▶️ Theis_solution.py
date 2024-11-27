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
        refine_plot = st.toggle("**Refine** the range of the **Data matching plot**")
        Viterbo = st.toggle("**Use real data from Viterbo 2023**")
    with columns2[1]:
        T_slider_value=st.slider('(log of) **Transmissivity** in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        T = 10 ** T_slider_value
        # Display the logarithmic value
        st.write("_Transmissivity_ in m2/s: %5.2e" %T)
        S_slider_value=st.slider('(log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        S = 10 ** S_slider_value
        # Display the logarithmic value
        st.write("_Specific storage_ (dimensionless):** %5.2e" %S)
    
    # Data from SYMPLE exercise
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    # Parameters needed to solve Theis (From the SYMPLE example/excercise)
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d

    if Viterbo:
        # Data from Viterbo 2023
        m_time = [0.083333333, 1, 1.416666667, 2.166666667, 2.5, 2.916666667, 3.566666667, 3.916666667, 4.416666667, 4.833333333, 5.633333333, 6.516666667, 7.5, 8.916666667, 10.13333333, 11.16666667, 12.6, 16.5, 18.53333333, 22.83333333, 27.15, 34.71666667, 39.91666667, 48.21666667, 60.4, 72.66666667, 81.91666667, 94.66666667, 114.7166667, 123.5]
        m_ddown = [0.04, 0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285, 0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415, 0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525, 0.53, 0.56, 0.57, 0.58]
        # Parameters needed to solve Theis (From the SYMPLE example/excercise) !!! UPDATE !!!
        r = 130       # m
        b = 8.5       # m
        Qs = 0.3/60   # m^3/s
        Qd = Qs*60*60*24 # m^3/d

    m_time_s = [i*60 for i in m_time] # time in seconds
    num_times = len(m_time)
    # Compute K and SS to provide parameters for plausability check
    # (i.e. are the parameter in a reasonable range)
    K = T/b     # m/s
    
   
    # Early (a) and late (b) Theis curve
    t_term = r**2 * S / 4 / T
    s_term = Qs/(4 * np.pi * T)

    t = u_inv * t_term
    s = w_u * s_term
        
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(t, s, label=r'Computed drawdown - Theis')
    if Viterbo:
        ax.plot(m_time_s, m_ddown,'go', label=r'measured drawdown - Viterbo 23')
    else:
        ax.plot(m_time_s, m_ddown,'ro', label=r'measured drawdown - synthetic textbook')
    plt.yscale("log")
    plt.xscale("log")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if refine_plot:
        plt.axis([1E0,1E4,1E-1,1E+1])
    else:
        plt.axis([1E-1,1E5,1E-4,1E+1])
    ax.grid(which="both")
    plt.xlabel(r'time t in (s)', fontsize=14)
    plt.ylabel(r'drawdown s in (m)', fontsize=14)
    plt.title('Theis drawdown', fontsize=16)
    plt.legend(fontsize=14)
    st.pyplot(fig)

    columns3 = st.columns((1,1), gap = 'medium')
    with columns3[0]:
        st.write("**Parameter estimation**")
        st.write("Distance of measurement from the well (in m): %3i" %r)
        st.write("Pumping rate of measurement (in m^3/s): %5.3f" %Qs)
        st.write("Transmissivity T = ","% 10.2E"% T, " m^2/s")
        st.write("Storativity    S = ","% 10.2E"% S, "[-]")

inverse()
