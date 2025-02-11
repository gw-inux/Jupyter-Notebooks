# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button

st.title(':red[Theis] parameter estimation')

st.subheader('Understanding the Theis (1935) solution for :red[confined aquifers]', divider="red")

st.markdown("""
            ### Introduction
            
            The Theis solution is intended to evaluate pumping tests in confined settings.
            
            The app allows to apply the Theis solution for pumping test data. You can use the sliders to modify the transmissivity _T_ and storativity _S_ to fit the measured data to the Theis curve.
            """)
            
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/confined_aquifer.png', caption="The figure shows a cross section through a pumped confined underground formation; from Kruseman and De Ridder (1994); available as preserved book in the Groundwater Project")
            
st.markdown("""
            In the following you find some initial questions to start with the investigation of the Theis solution.
"""
)

# Initial assessment
lc0, mc0, rc0 = st.columns([1,2,1])
with mc0:
    show_initial_assessment = button('Show/Hide the initial **assessment**', key= 'button1')
    
if show_initial_assessment:
    columnsQ1 = st.columns((1,1), gap = 'large')
    
    with columnsQ1[0]:
        stb.single_choice(":red[**For which conditions is the Theis solution intended?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, semiconfined aquifer",
                  "Transient flow, semiconfined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about the Theis solution in the following ressources _reference to GWP books...')
        stb.single_choice(":red[**How does the drawdown reaction change at one specific place if the storativity is decreased**]",
                  ["The drawdown is less.", "The drawdown is more", "The drawdown is not affected."],
                  1,success='CORRECT!   ...', error='Not quite. You can use the app to investigate what happens when you decrease storativity ... If required, you can read again about storativity _S_ in the following ressources _reference to GWP books...')
    
    with columnsQ1[1]:
        stb.single_choice(":red[**How does the drawdown reaction change at one specific place if the transmissivity is increased**]",
                  ["The drawdown is less.", "The drawdown is more", "The drawdown is not affected."],
                  0,success='CORRECT!   ...', error='Not quite. You can use the app to investigate what happens when you increase transmissivity ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
        stb.single_choice(":red[**Which of the following assumptions is made in the Theis solution for transient flow to a well?**]",
                  ["The aquifer has variable thickness", "The aquifer is confined and infinite in extent", "The well fully penetrates an unconfined aquifer", "The pumping rate varies with time"],
                  1,success='CORRECT! The aquifer is confined and infinite in extent', error='Not quite. If required, you can read again about the Theis solution in the following ressources _reference to GWP books...')                 
                  
"---"

# Optional theory here
lc1, mc1, rc1 = st.columns([1,3,1])
with mc1:
    show_theory = button('Show/Hide more about the underlying **theory**', key= 'button2')
    
if show_theory:
    st.markdown(
    """
    ### Required theory - The Theis Solution for Pumping Test Evaluation
    
    The Theis solution is a fundamental method in hydrogeology used to analyze transient flow to a well in a confined aquifer. It describes the drawdown _s_ as a function of time and radial distance from a pumping well under the assumption of an infinite, homogeneous, and isotropic aquifer with uniform thickness.
    
    The solution is derived from the groundwater flow equation and is based on the analogy between heat conduction and groundwater flow. The drawdown at a distance _r_ from a well pumping at a constant rate _Q_ is given by:
    """
    )
    
    st.latex(r'''s(r,t) = \frac{Q}{4\pi T} W(u)''')

    st.markdown(
    """    
    where:
    _T_ is the transmissivity of the aquifer
    _W(u)_ is the well function of the Theis solution,
    _u_ is a dimensionless time parameter defined as:
    """
    )
    
    st.latex(r'''u = \frac{r^2 S}{4 T t}''')
    
    st.markdown(
    """
    where:
    _S_ is the storativity (specific storage times aquifer thickness),
    _t_ is the time since pumping began.
    
    The well function _W(u)_ is given by the integral:
    """
    )

    st.latex(r'''W(u) = \int_u^{\infty} \frac{e^{-x}}{x} dx''')
    
    st.markdown(
    """
    This function is commonly evaluated using numerical techniques or lookup tables. The Theis solution is widely used in pumping test analysis to estimate aquifer properties by fitting observed drawdown data to theoretical type curves.
    """
    )

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
            Subsequently, you can modify the transmissivity and the storativity to fit your measured data to the Theis type curve. For precise fitting, you can change the plot resolution with the toogle.
"""
)

@st.fragment
def inverse(v):
    Viterbo = False
    # This is the function to plot the graph with the data     
    # Get input data
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
    log_max2 = 0.0  # S / Corresponds to 10^0 = 1
   
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        refine_plot = st.toggle("**Refine** the range of the **Data matching plot**", key = 10+v)
        if v==2:
            Viterbo = st.toggle("**Use real data from Viterbo 2023**", value = True)
    with columns2[1]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()
        T_slider_value=st.slider('_(log of) Transmissivity in m²/s_', log_min1,log_max1,-3.0,0.01,format="%4.2f", key = 20+v)
        T = 10 ** T_slider_value
        container.write("**Transmissivity in m²/s:** %5.2e" %T)
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR STORATIVITY
        container = st.container()
        S_slider_value=st.slider('_(log of) Storativity_', log_min2,log_max2,-4.0,0.01,format="%4.2f", key = 30+v)
        S = 10 ** S_slider_value
        container.write("**Specific storage (dimensionless):** %5.2e" %S)
    
    # Drawdown data from SYMPLE exercise and parameters 
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d

    if Viterbo:
        # Drawdown data from Viterbo exercise and parameters 
        m_time = [0.083333333, 1, 1.416666667, 2.166666667, 2.5, 2.916666667, 3.566666667, 3.916666667, 4.416666667, 4.833333333, 5.633333333, 6.516666667, 7.5, 8.916666667, 10.13333333, 11.16666667, 12.6, 16.5, 18.53333333, 22.83333333, 27.15, 34.71666667, 39.91666667, 48.21666667, 60.4, 72.66666667, 81.91666667, 94.66666667, 114.7166667, 123.5]
        m_ddown = [0.04, 0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285, 0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415, 0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525, 0.53, 0.56, 0.57, 0.58]
        r = 20           # m
        b = 8.5          # m
        Qs = 15.6/3600   # m^3/s
        Qd = Qs*60*60*24 # m^3/d

    m_time_s = [i*60 for i in m_time] # time in seconds
    num_times = len(m_time)
    # Compute K and SS to provide parameters for plausability check
    # (i.e. are the parameter in a reasonable range)
    K = T/b     # m/s
    SS = S/b
    
   
    # Theis curve
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
        plt.axis([1E0,1E4,1E-2,1E+1])
    else:
        plt.axis([1E-1,1E5,1E-4,1E+1])
        ax.text((0.2),1.8E-4,'Coarse plot - Refine for final fitting')
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
        st.write("Pumping rate of measurement (in m³/s): %5.3f" %Qs)
        st.write("Transmissivity T = ","% 10.2E"% T, " m²/s")
        st.write("Storativity    S = ","% 10.2E"% S, "[-]")

inverse(1)

"---"

st.markdown("""
            ### Next step - How about using Theis with real data?
            
            So far, we investigate the Theis solution with idealized data. However, the real world is not always that idealistic. In the next step we will see how the Theis solution works with measured data.  
"""
)

lc2, mc2, rc2 = st.columns([1,3,1])
with mc2:
    real_data = button("Let me see how Theis works with **real data**", key = 'button3')

if real_data:
    inverse(2)

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/02_🙋_▶️ Transient_Flow to a Well.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/04_🟢_▶️ Hantush_Jacob_solution.py")