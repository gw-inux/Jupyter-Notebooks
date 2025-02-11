# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi, tan
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button

st.title('Initial example for :orange[System Understanding through Model Analysis]')

st.markdown(
    """
    The aim of this tools is demonstrate a further example of a model application for an idealized situation. The aim is to compute the well capture zone for a production well in a confined, homogeneous, and isotropic aquifer. The investigation is based on an analytical solution of a groundwater flow model. Using such models is very beneficial for the necessary basic system understanding, which is an prerequisite for complex model applications, see als [Haitjema 2006: The Role of Hand Calculations in Ground Water Flow Modeling](http://dx.doi.org/10.1111/j.1745-6584.2006.00189.x). 
    """
)
st.header('Well capture zone for a confined aquifer', divider="orange")
st.markdown(
    """
    The app computes **1D groundwater flow** in an unconfined, homogeneous, and isotropic aquifer that is bounded by two defned head boundaries. The aquifer receives groundwater recharge from the top.
    
    Subsequently, you will find 
    - A short description of the initial situation that serve for an exercise,
    - Some explanation of the underlying theory of the 1D analytical groundwater flow model,
    - The exercise with questions, directions for the analysis including an interactive plot.
    """
)
"---"

# Optional theory here
lc1, mc1, rc1 = st.columns([1,2,1])
with mc1:
    show_theory = button('Show/Hide the underlying theory', key = 'button1')
    
if show_theory:
    st.markdown(
    """
    ## The Conceptual Model for WellCapture
    A well capture zone (or capture zone) is an area within an aquifer that delineates groundwater that will ultimately reach the well. It is also referred to as the zone of contribution. In a contaminated aquifer, contamination within a well capture zone will eventually reach the well as presented conceptually in the figure below.
    
    The WellCapture interactive tool calculates the capture area for a pumping well in a confined, homogeneous, isotropic aquifer. The regional groundwater flow is directed along the x-axis with a hydraulic gradient i. Accordingly, the capture area of an ideal pumping well, situated at the coordinates (0,0) can be characterized by the culmination point and the maximum width of the zone within the flow divide.
    """
    )
    left_co, cent_co, last_co = st.columns((20,60,20))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_Well_capture/assets/images/wellcapturediagram-sm42.png', caption="Conceptual Diagram of a well capture zone; modified from Grubb(1993)")

    st.markdown(
        """
        ## The Mathematical Model for WellCapture
        The full theoretical foundation for the computation can be found in a publication from Grubb (1993).
    
        The capture area of an ideal pumping well, situated at the coordinates (0,0) can be characterized by:
        - the culmination point _x0_, and
        - the maximum width of the zone within the flow divide, _B_
    """
    )
    st.latex(r'''x_0=\frac{Q}{2\pi Kib}''')
    st.latex(r'''B=2y_{max}=\frac{Q}{Kib}''')
    st.markdown(
        """
        The symbols are: _Q_ = pumping rate, _K_ = hydraulic conductivity, _i_ = hydrauic gradient, and _b_ = aquifer thickness.
    
        - each point on the flow divide can be calculated as:
    """
    )

    st.latex(r'''x=\frac{-y}{\tan (\frac{2 \pi Kiby}{Q})}''')

    st.markdown(
        """
        Grubb, S. (1993). Analytical Model for Estimation of Steady-State Capture Zones of Pumping Wells in Confined and Unconfined Aquifers. Groundwater, 31(1), 27-32. https://doi.org/10.1111/j.1745-6584.1993.tb00824.x

    """
    )
"---"

st.subheader('Own investigation (exercise)')
st.markdown(
    """
    You are asked to evaluate how parameter changes affect the capture zone for a production well.

    The following parameter are given:
    distance between the two lakes is fixed to _L_ = 2500 m.
    
    """
)

# Initial assessment

lc2, mc2, rc2 = st.columns([1,2,1])
with mc2:
    show_initial_assessment = button("**Show/Hide the initial questions**", key = 'button2')
    
if show_initial_assessment:
    stb.single_choice(":orange[The catchment area of the production well is computed and used for decision making. Afterwards it appears that the hydraulic conductivity was assumed to be too large. How much will this effect the shape of the catchment area?]",
                  ["The capture zone will be larger", "The capture zone will be smaller", "The capture zone is not affected"],
                  0,success='CORRECT! You will see this in the next steps.', error='This is not correct. In the next steps we will further investiage this behaviour.')
    stb.single_choice(":orange[The catchment area of the production well is computed and used for decision making. Afterwards it appears that the **effective porosity was assumed to be too small**. How much will this **effect the shape of the catchment area**?]",
                  ["Very high influence", "High influence", "Intermediate influence", "Minor influence", "No influence"],
                  4,success='CORRECT! You will see this in the next steps.', error='This is not correct. In the next steps we will further investiage this behaviour.')
    stb.single_choice(":red[**What parameter can be adjusted to manage the capture zone of the abstraction well?**]",
                  ["Pumping rate.", "Hydraulic conductivity", "Effective porosity", "Regional flow gradient"],
                  0,success='CORRECT! We will adapt this parameter in the next step.', error='Not quite. Please rethink.')

"---"

# Create buttons with st.button and proceed with the steps of the exercise
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #00FF00;
        color: black;
    }""",
):
    if st.button('Proceed with Exercise Step 1'):
        st.markdown("""
            **STEP 1:**
            First we aim to investigate the sensitivity of the hydraulic conductivity _K_ on the well capture zone. To understand what happens if the hydraulic conductivity was assumed too large, we can vary this parameter.
            
           _To proceed_ (with the interactive plot):
            - Modify the hydraulic conductivity. What happens?
"""
)
    if st.button('Proceed with Exercise Step 2'):
        st.markdown("""
            **STEP 2:**
            Now we want to use the model to manage a possible contamination accident.
            
           _To proceed_ (with the interactive plot):
            - Set the hydraulic conductivity to an value of 1E-4 m/s,
            - Set the regional hydraulic gradient to 0.001,
            - Set the aquifer thickness to 20 m,
            - Set the pumping rate to 0.030 m3/s
            - Turn on the 'Manage Accident' slider,
            - Manage the contamination by adjusting the (maximum allowed) pumping rate. How much can you extract if the accident should be outside the capture zone?
            - Now modify the hydraulic gradient of the regional flow. What happens?
"""
)
st.subheader('Computation and visualization')
st.markdown(
    """
    Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the hydraulic conductivity _K_ (in m/s), the pumping rate _Q_ (in m3/s).
    """
)
# Function for catchment width (maximale Breite des Einzugsgebietes)
def ymax_conf(Q, K, i, b):
    ymax = Q/(2.*K*i*b)
    return ymax

# Function for the culmination point (Kulminationspunkt)
def x0_conf(Q, K, i, b):
    x0 = -Q/(2.*np.pi*K*i*b)
    return x0

# Computaton of the well catchment (Berechnung der Trennstromlinie)

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min = -7.0 # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # K / Corresponds to 10^0 = 1

log_min2 = -5.0 # K / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # K / Corresponds to 10^0 = 1

columns = st.columns((1,1,1), gap = 'large')

with columns[0]:
    x_scale = st.slider('_Plot scaling in x direction_', 0.5, 10., 1., 0.5)
    y_scale = st.slider('_Plot scaling in y direction_', 0.5, 10., 1., 0.5)
    accident = st.toggle('Task: Accident')
    #revers = st.toggle('Reverse x-axis')
with columns[1]:
    b = st.slider('**Aquifer thickness (m)**', 1., 100.,20., 0.1, format="%5.2f")
    container = st.container()
    i_slider_value=st.slider('_(log of) Gradient of regional flow (-)', log_min2,log_max2,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale and display the value
    i = 10 ** i_slider_value   
    container.write("**Gradient of regional flow (-):** %5.2e" %i)    
with columns[2]:  
    Q = st.slider('**Pumping rate** (m3/s)', 0., 0.1,0.03, 0.001, format="%5.3f")
    container = st.container()
    K_slider_value=st.slider('_(log of) hydr. cond. K (m/s)_', log_min,log_max,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale and display the value
    K = 10 ** K_slider_value
    container.write("**Hydraulic conductivity K (m/s):** %5.2e" %K)


x_max= 1000 #fixed(x_max),
ymax = ymax_conf(Q, K, i, b)
x0   = x0_conf(Q, K, i, b)

y = np.linspace(-ymax*0.999, ymax*0.999, 100)

x_well = 0
y_well = 0

# Compute catchment
#x = -1*y/(np.tan(2*np.pi*K*i*b*y/Q))
x = y/(np.tan(2*np.pi*K*i*b*y/Q))

x_plot = 500 * x_scale
y_plot = 1000 * y_scale
    
# Plot
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(x,y, label='Well capture zone')
ax.plot(x_well,y_well, marker='o', color='r',linestyle ='None', label='pumping well') 
ax.set(xlabel='x (m)', ylabel='y (m)',title='Well capture zone of a pumping well')
ax.set(xlim=(-10*x_plot,x_plot), ylim=(-y_plot, y_plot))
if accident:
    ax.plot(-1400,400, marker='o', color='r',linestyle ='None', label='Accident')
plt.fill_between(x,y,color='blue', alpha=.1)
plt.fill_between(x,-y,color='blue', alpha=.1)
ax.grid()
plt.legend()

st.pyplot(fig)
    
st.write("Width of capture zone (m): %5.2f" %(2*ymax))
st.write('Culmination point x_0 (m):  %5.2f' %x0)

"---"

st.subheader('Concluding remarks')
st.markdown(
    """
    The app showed the use of a simple groundwater model to investigate the well capture zone. Based on a idealized conceptual model, a groundwater model with an analytical solution is derived. 
    
    This models can be used for e.g., 
    - gaining system understanding,
    - performing (initial) assessments for different scenarios,
    - evaluating numerical models, and more.
     
    The analytical solution allows to quickly change the model parameters, for example to analyze the sensitivity of the model on input paraemters.
    """
)
    
