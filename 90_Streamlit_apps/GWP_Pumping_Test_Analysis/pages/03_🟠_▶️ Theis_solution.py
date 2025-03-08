# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button

st.title('🟠 :red[Theis] parameter estimation')

st.header('For drawdown in :red[confined aquifers]')
st.markdown("""
            This section uses the Theis Solution for drawdown in response to pumping a :red[confined aquifer] to estimate Transmissivity and Storativity.
            """) 
st.subheader(':red-background[Introduction]', divider="red")
st.markdown(""" 
            The Theis (1935) solution was developed to calculate drawdown due to pumping a confined aquifer.
            
            This application uses the Theis Solution to estimate Transmissivity $T$ and Storativity $S$ from drawdown data collected during a pumping test. 
            
            You can estimate $T$ and $S$ by adjusting the sliders to modify $T$ and $S$ until the measured data align with the Theis curve for the input parameters.
            """)
            
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/confined_aquifer.png', caption="Cross section of a pumped confined aquifer, Kruseman et al., 1991")
            
st.markdown("""
            Before investigating the Theis Solution it is useful to think about the questions provided in this initial assessment.
"""
)

# Initial assessment
   
with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1,1))
    
    with columnsQ1[0]:
        stb.single_choice(":blue[**What conditions are appropriate for use of the Theis Solution?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, semiconfined aquifer",
                  "Transient flow, semiconfined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT! Theis is designed for transient flow in a fully confined aquifer', error='This is not correct ... You can learn more about the Theis Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 8](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
        stb.single_choice(":blue[**How does storativity $S$ influence the response of an aquifer to pumping?**]",
                  ["A higher storativity results in a slower drawdown response", "A higher storativity leads to more rapid flow to the well", "Storativity only affects steady-state conditions", "Storativity is not relevant for confined aquifers"],
                  0,success='CORRECT! A higher storativity results in a slower drawdown response, because more water must be removed for an equivalent decline in head.', error='This is not correct. Storativity does not influence the rate of groundwater flow. Storativity is not relevant to steady state flow which is defined by no change in storage. Storativity is relevant to all types of aquifers. Feel free to answer again.')
    
    with columnsQ1[1]:
        stb.single_choice(":blue[**How does the drawdown change at one specific place and time if the transmissivity is increased?**]",
                  ["The drawdown is less", "The drawdown is more", "The drawdown is not affected", "All of the above depending on the parameter values"],
                  3,success='CORRECT! When all else is equal, a higher transmissivity will produce a broader cone of depression that is not as deep. So, near the well there will be less drawdown but far from the well there will be more drawdown. You can investigate this with the interactive plot and the option to plot a second set of $T$ and $S$ for comparison', error='This is not completely correct ... You can use the application to investigate what happens when you increase transmissivity, e.g. with the option to plot a second set of $T$ and $S$ for comparison. However, you will need to experiment with different combinations of hydraulic parameters as well as distance and time, then holding all else constant, except $T$, observe the change in drawdown. When all else is equal, a higher transmissivity will produce a broader cone of depression that is not as deep. So, near the well there will be less drawdown but far from the well there will be more drawdown.')
        stb.single_choice(":blue[**Which of the following assumptions was made in the development of the Theis solution for transient flow to a well?**]",
                  ["The aquifer has variable thickness", "The aquifer is confined and infinite in lateral extent", "The well fully penetrates an unconfined aquifer", "The pumping rate varies with time"],
                  1,success='CORRECT! The aquifer is confined and infinite in lateral extent', error='This is not correct. You can learn more about the Theis Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 8](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
                  
st.subheader(':red-background[Underlying Theory] - Theis Solution for Pumping Test Evaluation', divider="red")
st.markdown(
    """
    The Theis solution is a fundamental method in hydrogeology that is used to analyze transient flow to a well pumping at a constant rate _Q_ in a confined aquifer. It describes the drawdown $s$ as a function of time $t$ since pumping began and radial distance $r$ from a pumping well under the assumption of a laterally infinite, homogeneous, and isotropic aquifer with uniform thickness.
    """
    )
    
# Optional theory here
with st.expander('**Click here for more information** about the underlying theory of the :red[**Theis solution**]'):
    st.markdown(""" 
            The Theis solution is a fundamental method in hydrogeology used to analyze transient flow to a well in a confined aquifer. It describes the drawdown $s$ as a function of time  $t$ since pumping began and radial distance $r$ from a well pumping at a constant rate from a laterally infinite, homogeneous, and isotropic aquifer with uniform thickness.
            
            The solution is derived from the radial groundwater flow equation. The drawdown at a distance $r$ from a well pumping at a constant rate _Q_ is given by:
            """
    )
    
    st.latex(r'''s(r,t) = \frac{Q}{4\pi T} W(u)''')

    st.markdown(
    """    
    where:
    - $s$ is drawdown at time $t$ and distance $r$ from the well
    - $T$ is the transmissivity of the aquifer
    - _W(u)_ is the well function defined below
    - _u_ is a dimensionless time parameter defined as:
    """
    )
    
    st.latex(r'''u = \frac{r^2 S}{4 T t}''')
    
    st.markdown(
    """
    where:
    - $S$ is the storativity (specific storage times aquifer thickness)
    - $t$ is the time since pumping began
    
    The well function _W(u)_ is given by the integral:
    """
    )

    st.latex(r'''W(u) = \int_u^{\infty} \frac{e^{-x}}{x} dx''')
    
    st.markdown(
    """
    This function is commonly evaluated using numerical techniques or tables of _W(u)_ as a function of _u_. The Theis solution is widely used in pumping test analysis to estimate aquifer properties by fitting observed drawdown data to the Theis type curve.
    """
    )

st.subheader(':red-background[Estimate $T$ and $S$ by matching a Theis Curve] to ideal (i.e., error free) drawdown data', divider="red")

st.markdown("""
            In this section, you can **adjust the values of transmissivity and storativity until the calculated curve of drawdown versus time using the input values of $T$ and $S$ matches the ideal drawdown data**. The ideal data represent drawdown at a distance of 120 m from a well pumping 0.005 m³/s.
            
            A match indicates that the selected values are a reasonable representation of the aquifer properties.
            
            For more precise matching, zoom in by using the toogle.
            
            Toggling on the scatter plot provides an visual comparison of the data and the fitted curve. A 1 to 1, 45 degree line, indicates a perfect match.
"""
)
# Computation
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
    
def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s
    
def compute_statistics(measured, computed):
    # Calculate the number of values
    n = len(measured)

    # Initialize a variable to store the sum of squared differences
    total_me = 0
    total_mae = 0
    total_rmse = 0

    # Loop through each value
    for i in range(n): # Add the squared difference to the total
        total_me   += (computed[i] - measured[i])
        total_mae  += (abs(computed[i] - measured[i]))
        total_rmse += (computed[i] - measured[i])**2

    # Calculate the me, mae, mean squared error
    me = total_me / n
    mae = total_mae / n
    meanSquaredError = total_rmse / n

    # Raise the mean squared error to the power of 0.5 
    rmse = (meanSquaredError) ** (1/2)
    return me, mae, rmse

# Initialize session state for value and toggle state
if "T_slider_value" not in st.session_state:
    st.session_state["T_slider_value"] = -3.0  # Default value
if "S_slider_value" not in st.session_state:
    st.session_state["S_slider_value"] = -4.0  # Default value
number_input = False
st.session_state.number_input = number_input  # Default to number_input

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_min = -5
u_max = 4

u = np.logspace(u_min,u_max)
u_inv = 1/u
w_u = well_function(u)



@st.fragment
def inverse(v):
    Viterbo = False
    Varnum = False
    # This is the function to plot the graph with the data     
    # Get input data
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
    log_max2 = 0.0  # S / Corresponds to 10^0 = 1
    
    # Toggle to switch between slider and number-input mode
    st.session_state.number_input = st.toggle("Use Slider/Number number for paramter input", key = 10+v)
   
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        refine_plot = st.toggle("**Zoom in** on the **data in the graph**", key = 20+v)
        scatter = st.toggle('Show scatter plot', key = 30+v)
        if v==2:
            Viterbo = True
        if v==3:
            Varnum = True
    with columns2[1]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()
        if st.session_state.number_input:
            T_slider_value_new = st.number_input("_(log of) Transmissivity in m²/s_", log_min1,log_max1, st.session_state["T_slider_value"], 0.01, format="%4.2f", key = 40+v)
        else:
            T_slider_value_new = st.slider("_(log of) Transmissivity in m²/s_", log_min1, log_max1, st.session_state["T_slider_value"], 0.01, format="%4.2f", key = 40+v)
        st.session_state["T_slider_value"] = T_slider_value_new
        T = 10 ** T_slider_value_new
        container.write("**Transmissivity in m²/s:** %5.2e" %T)
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR STORATIVITY
        container = st.container()
        if st.session_state.number_input:
            S_slider_value_new=st.number_input('_(log of) Storativity_', log_min2,log_max2,st.session_state["S_slider_value"],0.01,format="%4.2f", key = 50+v)
        else:
            S_slider_value_new=st.slider('_(log of) Storativity_', log_min2,log_max2,st.session_state["S_slider_value"],0.01,format="%4.2f", key = 50+v)
        st.session_state["S_slider_value"] = S_slider_value_new
        S = 10 ** S_slider_value_new
        container.write("**Storativity (dimensionless):** %5.2e" %S)
    
    # Drawdown data from SYMPLE exercise and parameters 
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d

    if Viterbo:
        # Drawdown data from Viterbo exercise and parameters 
        m_time = [ 1, 1.416666667, 2.166666667, 2.5, 2.916666667, 3.566666667, 3.916666667, 4.416666667, 4.833333333, 5.633333333, 6.516666667, 7.5, 8.916666667, 10.13333333, 11.16666667, 12.6, 16.5, 18.53333333, 22.83333333, 27.15, 34.71666667, 39.91666667, 48.21666667, 60.4, 72.66666667, 81.91666667, 94.66666667, 114.7166667, 123.5]
        m_ddown = [ 0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285, 0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415, 0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525, 0.53, 0.56, 0.57, 0.58]
        r = 21           # m
        b = 13          # m
        Qs = 11.16/3600   # m^3/s
        Qd = Qs*60*60*24 # m^3/d

    if Varnum:
        #R12\n",
        m_time =  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325] # time in minutes\n",
        m_ddown = [2E-05,0.02022,0.04591,0.0716,0.09342,0.11433,0.12882,0.14332,0.15139,0.16313,0.17396,0.18203,0.18827,0.1936,0.19878,0.2012,0.20729,0.21247,0.21489,0.22007,0.22249,0.22583,0.22826,0.23068,0.23358,0.23648,0.23938,0.24228,0.24243,0.24533,0.24915,0.2493,0.2522,0.25235,0.2551,0.2551,0.25785,0.25785,0.2606,0.2606,0.26335,0.26335,0.2661,0.2661,0.26597,0.26585,0.26847,0.2656,0.26822,0.27177,0.26797,0.27152,0.27139,0.27402,0.27397,0.27392,0.27387,0.27382,0.27652,0.27647,0.27642,0.27637,0.27907,0.27627,0.27614,0.27877,0.27589,0.27577,0.27839,0.27735,0.27814,0.2771,0.28064,0.2796,0.27712,0.2774,0.28042,0.27795,0.27822,0.2785,0.28152,0.27905,0.28207,0.28235,0.28307,0.28012,0.28175,0.2843,0.2841,0.28482,0.28462,0.28442,0.28422,0.28402,0.28404,0.28407,0.28684,0.28412,0.28689,0.28692,0.28694,0.28422,0.28699,0.28702,0.28717,0.28732,0.28747,0.28762,0.28777,0.28792,0.28807,0.28822,0.28837,0.28852,0.29144,0.28887,0.29179,0.28922,0.28939,0.28957,0.28974,0.28992,0.29009,0.29027,0.28994,0.29237,0.28929,0.29172,0.29139,0.29107,0.29074,0.29042,0.29009,0.28977,0.28974,0.28972,0.28969,0.29333,0.28964,0.28687,0.28959,0.29323,0.28954,0.28952,0.29336,0.29353,0.29371,0.29022,0.29406,0.29423,0.29441,0.29458,0.29109,0.29493,0.29488,0.29483,0.29478,0.29473,0.29468,0.29463,0.29458,0.29453,0.29723,0.29718,0.29443,0.29443,0.29443,0.29443,0.29443,0.29718,0.29443,0.29443,0.29443,0.29718,0.29701,0.29683,0.29666,0.29648,0.29631,0.29613,0.29596,0.29578,0.29561,0.29543,0.29561,0.29853,0.29596,0.29613,0.29631,0.29648,0.29666,0.29683,0.29701,0.29993,0.29688,0.29658,0.29628,0.29598,0.29568,0.29538,0.29508,0.29478,0.29723,0.29693,0.29418,0.29418,0.29418,0.29418,0.29693,0.29693,0.29418,0.29418,0.29693,0.29418,0.29433,0.29723,0.29738,0.29478,0.29768,0.29783,0.29798,0.29813,0.29828,0.29843,0.29838,0.29833,0.29828,0.29823,0.29818,0.29813,0.29808,0.29803,0.29798,0.29793,0.29796,0.29798,0.29801,0.29803,0.30081,0.30083,0.29811,0.29813,0.29816,0.30093,0.29853,0.29888,0.29923,0.29958,0.29993,0.30303,0.30338,0.30098,0.30133,0.30168,0.30408,0.30098,0.30063,0.30303,0.29993,0.30233,0.29923,0.29888,0.29853,0.29818,0.30113,0.30133,0.29878,0.29898,0.30193,0.30213,0.30233,0.30253,0.30273,0.30018,0.30001,0.30258,0.30241,0.29948,0.29931,0.29913,0.30171,0.29878,0.29861,0.29843,0.30133,0.29873,0.29888,0.29903,0.29918,0.29933,0.29948,0.29963,0.30253,0.29993,0.30011,0.30028,0.30046,0.30063,0.30081,0.30373,0.30391,0.30133,0.30151,0.30443,0.30151,0.30133,0.30116,0.30098,0.30081,0.30338,0.30046,0.30028,0.30286,0.29993,0.30286,0.30303,0.30321,0.30338,0.30356,0.30373,0.30391,0.30408,0.30426,0.30443,0.30408] # drawdown in meters\n",
        r = 38.9     # m
        b = 12       # m
        Qs = 0.01317   # m^3/s
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
    
    # Compute point data for scatter plot 
    m_ddown_theis = [compute_s(T, S, i, Qs, r) for i in m_time_s]
    
    # Find the max for the scatter plot
    max_s = math.ceil(max(m_ddown)*10)/10
        
    fig = plt.figure(figsize=(10,14))
    ax = fig.add_subplot(2, 1, 1)
    # Info-Box
    props   = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    out_txt = '\n'.join((       
                         r'$T$ (m²/s) = %10.2E' % (T, ),
                         r'$S$ (-) = %10.2E' % (S, )))
    ax.plot(t, s, label=r'calculated Theis drawdown for T and S')
    if Viterbo:
        ax.plot(m_time_s, m_ddown,'go', label=r'measured drawdown - Viterbo 23')
    elif Varnum:
        ax.plot(m_time_s, m_ddown,'go', label=r'measured drawdown - Varnum16/R12')
    else:
        ax.plot(m_time_s, m_ddown,'ro', label=r'measured drawdown - ideal data')
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
    plt.text(0.97, 0.15,out_txt, horizontalalignment='right', transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    
    if scatter:
        x45 = [0,200]
        y45 = [0,200]
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x45,y45, '--')
        if Viterbo:
            ax.plot(m_ddown, m_ddown_theis,  'go', label=r'measured')
        elif Varnum:
            ax.plot(m_ddown, m_ddown_theis,  'go', label=r'measured')
        else:
            ax.plot(m_ddown, m_ddown_theis,  'ro', label=r'measured')
        me, mae, rmse = compute_statistics(m_ddown, m_ddown_theis)
        plt.title('Scatter plot', fontsize=16)
        plt.xlabel(r'Measured s in m', fontsize=14)
        plt.ylabel(r'Computed s in m', fontsize=14)
        plt.ylim(0, max_s)
        plt.xlim(0, max_s)
        out_txt = '\n'.join((
                             r'$ME = %.3f$ m' % (me, ),
                             r'$MAE = %.3f$ m' % (mae, ),
                             r'$RMSE = %.3f$ m' % (rmse, ))) 
        plt.text(0.97*max_s, 0.05*max_s, out_txt, horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='wheat'), fontsize=14)
    
    
    st.pyplot(fig)
    
    columns3 = st.columns((1,10,1), gap = 'medium')
    with columns3[1]:
        if st.button(':green[**Submit**] your parameters and **show results**', key = 60+v):
            st.write("**Parameters and Results**")
            st.write("- Distance of measurement from the well **$r$ = %3i" %r," m**")
            st.write("- Pumping rate during test **$Q$ = %5.3f" %Qs," m³/s**")
            st.write("- Transmissivity **$T$ = % 10.2E"% T, " m²/s**")
            st.write("- Storativity    **$S$ = % 10.2E"% S, "[dimensionless]**")

# The first interactive plot 
inverse(1)

with st.expander('**:red[Click here]** to see one **example of the curve fitting to the :red[ideal] drawdown data**'):
    st.markdown(""" 
            The following example shows one curve match to the ideal drawdown data 120 m from a well pumping 0.005 m³/s. If many expert hydrogeologists matched a Theis curve to the data, they would all have a slightly different values of $T$ and $S$, but the parameter sets would likely all be close enough to the values of the aquifer $T$ and $S$ to draw comparable conclusions, and make similar predictions of drawdown for other distances from the well and for longer time than the duration of the test. While adjusting parameter values, one finds that the ideal data can be matched very well to the Theis curve. The reason for this behavior is that the ideal aquifer data conform to the conditions for applying the Theis solution. 
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/Theis_Ideal_example.png', caption="One acceptable match of the Theis curve to the drawdown data") 

st.subheader(':red-background[Next step - Matching the Theis Solution to data collected at a field site]', divider="red")

st.markdown("""
           
            Thus far, we investigated the Theis solution with ideal data. However, data collected in the field are less than ideal. Drawdown measurements vary for many reasons.  
"""
)

# Irregularities of field datay here
with st.expander('**:red[Click here] for more information** about some of the causes of irregularities in field pumping test data'):
    st.markdown(
    """
            - It is generally **not possible to maintain an absolutely constant pumping rate** so the data do not form a completely smooth curve.
            - **Water is removed from the well bore in the early period of pumping**, but that phenomenon is not accounted for by the Theis solution which assumes an infinitesimal well diameter and thus instantaneous response of head in the aquifer to pumping of the well so drawdown may be unexpectedly large and rapid at early times while water is removed from the bore.
            - **Aquifers are not laterally infinite** as assumed in the Theis solution, rather there may be bodies of water near the well that provide water to the system, slowing the rate of drawdown, or  there may be low permeability materials such as bedrock or faults that prevent water flow toward the well from some directions causing drawdown to occur more rapidly than calculated by the Theis Solution - these "boundary effects" are noticeable in data from later in the pumping test.
            - **Other stresses on the groundwater system may influence groundwater levels** such as pumps in nearby wells being turned on or turned off, causing either more rapid drawdown or slower drawdown (and sometimes even resulting in a rise of water levels). An interesting example of the effect of other stresses occurred during the test of a well in an alluvial aquifer near a river being conducted to provide example data for a class to work with - the drawdown was proceeding, but even though the pumping rate was constant the water levels began to rise as the sun began to set. It was realized that the cottonwood trees along the river had been "pumping water" by way of evapotranspiration all day while the well was pumping. The evapotranspiration stopped as the sun went down decreasing the withdrawal of water form the aquifer, thus water levels rose. The evapotranspiration was such a powerful influence on the water levels that the data were not useful for a first-level class exercise.  
            
    """
    )

st.markdown("""
           
            The next step investigates matching the Theis solution to measured data from the Varnum field site in Sweden. 
"""
)

with st.expander('**:red[Click here] to open the interactive plot with field measured data**'):
    # The second interactive plot
    inverse(3)
    
with st.expander('**:red[Click here]** to see one **example of the curve fitting to the :green[Varnum field site (Sweden)] data**'):
    st.markdown(""" 
            The following image shows one match of the Theis curve to the drawdown data. If many expert hydrogeologists matched a Theis curve to the data, they would all have a slightly different values of $T$ and $S$, but the parameter sets would likely all be close enough to the values of the aquifer $T$ and $S$ to draw comparable conclusions, and make similar predictions of drawdown for other distances from the well and for longer time than the duration of the test. 
            
            While adjusting parameter values, **one finds that the early-time drawdown data can be matched very well to the Theis curve, but the data do not fit well at later times**. The reason for this behavior is that as the drawdown cone grows in depth and extent, leakage through an aquitard enters the aquifer which slows the rate of drawdown. At that time the underlying assumptions of the Theis solution are no longer met, but the curve match to the early time data provides representative values of $T$ and $S$.
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/Theis_Varnum_example.png', caption="One example for a curve match of the Theis solution to the Varnum data") 

st.subheader(':red-background[Some initial conclusions]', divider="red")
with st.expander('**Click here for some initial conclusions**'):
    st.markdown("""
    The **first interactive plot** allowed adjustment of $T$ and $S$ values used to generate the Theis curve to obtain a fit with ideal drawdown data. **With the ideal data we could obtain perfect fit to the Theis solution**.
    
    In the **second interactive plot** we aimed to adjust $T$ and $S$ values to generate a Theis curve that matched drawdown data measured during a pumping test at a field site. **This revealed that the Theis solution may only partially match the measured drawdown data because conditions may deviate from the assumptions made when deriving the Theis solution**.
    """
)  

with st.expander('**Click here for references**'):
    st.markdown("""
    [Kruseman, G.P., de Ridder, N.A., & Verweij, J.M.,  1991.](https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/) Analysis and Evaluation of Pumping Test Data, International Institute for Land Reclamation and Improvement, Wageningen, The Netherlands, 377 pages.
    
    Theis, C.V., 1935. The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage, Transactions of the American Geophysical Union, volume 16, pages 519-524.
"""
)     
            
"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/02_🙋_▶️ Transient_Flow_to_a_Well.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/04_🟢_▶️ Hantush_Jacob_solution.py")