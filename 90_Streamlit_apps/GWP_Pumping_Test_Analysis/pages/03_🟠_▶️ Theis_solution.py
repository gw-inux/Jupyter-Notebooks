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
            This section uses the Theis Solution for drawdown in response to pumping :red[confined aquifers] to estimate Transmissivity and Storativity.
            """) 
st.subheader(':red-background[Introduction]', divider="red")
st.markdown(""" 
            The Theis (1935) solution was developed to calculate drawdown due to pumping a confined aquifer.
            
            This application uses the Theis Solution to estimate Transmissivity _T_ and Storativity _S_ from drawdown data collected during a pumping test. 
            
            You can estimate _T_ and _S_ by adjusting the sliders to modify the parameter values until the measured data align with the Theis curve for the input parameters.
            """)
            
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/confined_aquifer.png', caption="Cross section of a pumped confined aquifer, Kruseman et al., 1991")
            
st.markdown("""
            To start investigating the Theis Solution it is useful to think about the questions provided in this initial assessment.
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
        stb.single_choice(":blue[**How does storativity _S_ influence the response of an aquifer to pumping?**]",
                  ["A higher storativity results in a slower drawdown response", "A higher storativity leads to more rapid flow to the well", "Storativity only affects steady-state conditions", "Storativity is not relevant for confined aquifers"],
                  0,success='CORRECT! A higher storativity results in a slower drawdown response, because more water must be removed for an equivalent decline in head.', error='This is not correct. Storativity does not influence the rate of groundwater flow. Storativity is not relevant to steady state flow which is defined by no change in storage. Storativity is relevant to all types of aquifers. Feel free to answer again.')
    
    with columnsQ1[1]:
        stb.single_choice(":blue[**How does the drawdown change at one specific place and time if the transmissivity is increased?**]",
                  ["The drawdown is less", "The drawdown is more", "The drawdown is not affected", "All of the above depending on the parameter values"],
                  3,success='CORRECT! When all else is equal, a higher transmissivity will produce a broader cone of depression that is not as deep. So, near the well there will be less drawdown but far from the well there will be more drawdown. You can investigate this with the interactive plot and the option to plot a second set of _T_ and _S_ for comparison', error='This is not completely correct ... You can use the application to investigate what happens when you increase transmissivity, e.g. with the option to plot a second set of _T_ and _S_ for comparison. However, you will need to experiment with different combinations of hydraulic parameters as well as distance and time, then holding all else constant, except _T_, observe the change in drawdown. When all else is equal, a higher transmissivity will produce a broader cone of depression that is not as deep. So, near the well there will be less drawdown but far from the well there will be more drawdown.')
        stb.single_choice(":blue[**Which of the following assumptions was made in the development of the Theis solution for transient flow to a well?**]",
                  ["The aquifer has variable thickness", "The aquifer is confined and infinite in lateral extent", "The well fully penetrates an unconfined aquifer", "The pumping rate varies with time"],
                  1,success='CORRECT! The aquifer is confined and infinite in lateral extent', error='This is not correct. You can learn more about the Theis Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 8](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
                  
st.subheader(':red-background[Underlying Theory] - Theis Solution for Pumping Test Evaluation', divider="red")
st.markdown(
    """
    The Theis solution is a fundamental method in hydrogeology used to analyze transient flow to a well pumping at a constant rate _Q_ in a confined aquifer. It describes the drawdown _s_ as a function of time _t_ since pumping began and radial distance _r_ from a pumping well under the assumption of a laterally infinite, homogeneous, and isotropic aquifer with uniform thickness.
    """
    )
    
# Optional theory here
with st.expander('**Click here for more information** about the underlying theory of the :red[**Theis solution**]'):
    st.markdown(
    """
    ### 
    
    The Theis solution is a fundamental method in hydrogeology used to analyze transient flow to a well in a confined aquifer. It describes the drawdown _s_ as a function of time  _t_ since pumping began and radial distance _r_ from a well pumping at a constant rate from a laterally infinite, homogeneous, and isotropic aquifer with uniform thickness.
    
    The solution is derived from the groundwater flow equation and is based on the analogy between heat conduction and groundwater flow. The drawdown at a distance _r_ from a well pumping at a constant rate _Q_ is given by:
    """
    )
    
    st.latex(r'''s(r,t) = \frac{Q}{4\pi T} W(u)''')

    st.markdown(
    """    
    where:
    - _T_ is the transmissivity of the aquifer
    - _W(u)_ is the well function defined below
    - _u_ is a dimensionless time parameter defined as:
    """
    )
    
    st.latex(r'''u = \frac{r^2 S}{4 T t}''')
    
    st.markdown(
    """
    where:
    - _S_ is the storativity (specific storage times aquifer thickness)
    - _t_ is the time since pumping began
    
    The well function _W(u)_ is given by the integral:
    """
    )

    st.latex(r'''W(u) = \int_u^{\infty} \frac{e^{-x}}{x} dx''')
    
    st.markdown(
    """
    This function is commonly evaluated using numerical techniques or tables of _W(u)_ as a function of _u_. The Theis solution is widely used in pumping test analysis to estimate aquifer properties by fitting observed drawdown data to the Theis type curve.
    """
    )

st.subheader(':red-background[Estimate _T_ and _S_ by matching a Theis Curve] to measured data', divider="red")

st.markdown("""
            In this section, you can **adjust the values of transmissivity and storativity until the curve of drawdown versus time that is calculated and plotted on the graph matches the idealized measured data**. The match indicates that the selected values are a reasonable representation of the aquifer properties.
            
            For more precise matching, zoom in by using the toogle.
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

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_min = -5
u_max = 4

u = np.logspace(u_min,u_max)
u_inv = 1/u
w_u = well_function(u)



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
        refine_plot = st.toggle("**Zoom in** on the **data in the graph**", key = 10+v)
        scatter = st.toggle('Show scatter plot', key = 40+v)
        if v==2:
            Viterbo = True
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
        m_time = [ 1, 1.416666667, 2.166666667, 2.5, 2.916666667, 3.566666667, 3.916666667, 4.416666667, 4.833333333, 5.633333333, 6.516666667, 7.5, 8.916666667, 10.13333333, 11.16666667, 12.6, 16.5, 18.53333333, 22.83333333, 27.15, 34.71666667, 39.91666667, 48.21666667, 60.4, 72.66666667, 81.91666667, 94.66666667, 114.7166667, 123.5]
        m_ddown = [ 0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285, 0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415, 0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525, 0.53, 0.56, 0.57, 0.58]
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
    
    # Compute point data for scatter plot 
    m_ddown_theis = [compute_s(T, S, i, Qs, r) for i in m_time_s]
    
    # Find the max for the scatter plot
    max_s = math.ceil(max(m_ddown))
        
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
    else:
        ax.plot(m_time_s, m_ddown,'ro', label=r'measured drawdown - idealized data')
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
        if st.button(':green[**Submit**] your parameters and **show results**', key = 50+v):
            st.write("**Parameters and Results**")
            st.write("- Distance of measurement from the well **r = %3i" %r," m**")
            st.write("- Pumping rate during test **Q = %5.3f" %Qs," m³/s**")
            st.write("- Transmissivity **T = % 10.2E"% T, " m²/s**")
            st.write("- Storativity    **S = % 10.2E"% S, "[dimensionless]**")

# The first interactive plot 
inverse(1)

with st.expander('**:red[Click here]** to see one **example of the curve fitting to the :red[idealized] data**'):
    st.markdown(""" 
            The following example shows one curve match. If five experts made the curve match they would all have a slightly different set of parameter values, but the parameter sets would likely all be close enough to the shown example to draw comparable conclusions, and make similar predictions. While adjusting parameter values, one finds that the idealized data can be matched very well to the Theis curve. The reason for this behavior is that the idealized aquifer data conform to the conditions for applying the Theis solution. 
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/Theis_Idealized_example.png', caption="One example for a curve match of the Theis solution to idealized data") 

st.subheader(':red-background[Next step - Using Theis with field data]', divider="red")

st.markdown("""
           
            So far, we investigated the Theis solution with idealized data. However, data collected in the field are less than ideal. Drawdown measurements vary for many reasons.  
"""
)

# Irregularities of field datay here
with st.expander('**:red[Click here] for more information** about the causes of irregularities in field pumping test data'):
    st.markdown(
    """
            - it is not possible to maintain an absolutely constant pumping rate so the data will not form a smooth curve
            - water is removed from the well bore in the early period of pumping, but that phenomenon is not accounted for by the Theis solution that assumes an infinitesimal well diameter with instantaneous response in the aquifer so drawdown may be unexpectedly large at early times 
            - aquifers are not laterally infinite as assumed in the Theis solution, rather there may be bodies of water near the well that provide water to the system, slowing the rate of drawdown, or  there may be low permeability materials such as bedrock or faults that prevent water flow toward the well from some directions causing drawdown to occur more rapidly than calculated by the Theis Solution - these "boundary effects" are noticeable in data from later in the pumping test
            - other stresses on the groundwater system may influence groundwater levels such as pumps in nearby wells being turned on or turned off, causing either more rapid drawdown or slower drawdown (and sometimes even resulting in a rise of water levels)
            - a notable example of the effect of other stresses occurred during the test of a well in an alluvial aquifer near a river being conducted to provide example data for a class to work with - the drawdown was proceeding, but even though the pumping rate was constant the water levels began to rise around sunset, then it was realized that the cottonwood trees along the river had been "pumping water" by way of evapotranspiration all day and the evapotranspiration stopped as the sun went down. The evapotranspiration was such a powerful influence on the water levels that the data were not useful for a first-level class exercise.  
            
    """
    )

st.markdown("""
           
            The next step investigates matching the Theis solution to measured data.  
"""
)

with st.expander('**:red[Click here] to open the interactive plot with field measured data**'):
    # The second interactive plot
    inverse(2)
    
with st.expander('**:red[Click here]** to see one **example of the curve fitting to the :green[Viterbo] data**'):
    st.markdown(""" 
            The following example shows one curve match. If five experts made the curve match they would all have a slightly different set of parameter values, but the parameter sets would likely all be close enough to the shown example to draw comparable conclusions, and make similar predictions. While adjusting parameter values, one finds that the early data can be matched well to the Theis curve while the later data deviates from the curve. The reason for this behavior is that the investigated aquifer doesn't conform to the conditions for applying the Theis solution because it is not fully confined. 
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/Theis_Viterbo_example.png', caption="One example for a curve match of the Theis solution to the Viterbo data") 

st.subheader(':red-background[Some initial conclusions]', divider="red")
with st.expander('**Click here for some initial conclusions**'):
    st.markdown("""
    The **first interactive plot** showed how to modify the values used to generate the Theis curve to obtain a fit with measured data. The modifications were done by adjusting transmissivity $T$ and storativity $S$.
    
    With the idealized "textbook" data we could obtain perfect fit to the Theis solution.
    
    In the **second interactive plot** we aimed to fit the Theis solution to measured data from a field site.
    
    Also the use of field data revealed that the Theis solution may only partially reflect the measured data, that is, it may be possible to obtain a good fit for the early data or the late data, but not for both.
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
        st.switch_page("pages/02_🙋_▶️ Transient_Flow to a Well.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/04_🟢_▶️ Hantush_Jacob_solution.py")