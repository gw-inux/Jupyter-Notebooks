# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi, tan
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container

st.title('Well capture zone for a confined aquifer')

st.subheader('Application/Exercise: :red[Initial Management of an accident]', divider="red")
st.markdown("""
            ### Initial situation and challenge
            
            An water abstraction well is operated to provide drinking water. Due to an accident within the well capture zone, the water production is in danger. An immidate action is requested as an initial measure.
            
            For this application, the following parameters are provided (i.e., it is not intended that you modify them):
            - Gradient of regional flow _i_ = 0.001
            - Aquifer thickness _b_ = 25 m
            
            In the following you find some initial questions to start with the challenge.
"""
)

# Initial assessment

show_initial_assessment = st.toggle("**Show the initial assessment**")
if show_initial_assessment:
    columnsQ1 = st.columns((1,1), gap = 'large')
    
    with columnsQ1[0]:
        stb.single_choice(":red[**What initial measure would you suggest?**]",
                  ["Immitiatly place a well close to the accidient to capture contaminated water.", "Immitialy stop the production well", "Reduce the pumping rate of the production well", "Increase the hydraulic conductivity of the aquifer"],
                  1,success='CORRECT! We will do this in the next steps.', error='This option is not suitable. Re-Think the situation.')
        stb.single_choice(":red[**What parameter can be adjusted to manage the capture zone of the abstraction well?**]",
                  ["Pumping rate.", "Hydraulic conductivity", "Effective porosity", "Regional flow gradient"],
                  1,success='CORRECT! We will adapt this parameter in the next step.', error='Not quite. Please rethink.')
    
    with columnsQ1[1]:
        stb.single_choice(":red[**How much is the approximate measurement uncertainty of the hydraulic conductivity?**]",
                  ["0.01%", "1%", "10%", "100%"],
                  1,success='CORRECT! Although this number is just a very rought approximate.', error='Not quite. Feel free to answer again.')             
        stb.single_choice(":red[**Question4?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
"---"

# Function for catchment width (maximale Breite des Einzugsgebietes)
def ymax_conf(Q, K, i, b):
    ymax = Q/(2.*K*i*b)
    return ymax

# Function for the culmination point (Kulminationspunkt)
def x0_conf(Q, K, i, b):
    x0 = Q/(2.*np.pi*K*i*b)
    return x0

# Computaton of the well catchment (Berechnung der Trennstromlinie)
# Get input data
# Define the minimum and maximum for the logarithmic scale

# General data here
x_well = 0
y_well = 0
b = 25
i = 0.001

x_max= 1000 #fixed(x_max)

log_min = -7.0 # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # K / Corresponds to 10^0 = 1

log_min2 = -5.0 # K / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # K / Corresponds to 10^0 = 1

@st.fragment

def wellcapture(v):
    if v==0: uncert = False
    
    columns = st.columns((1,1,1), gap = 'medium')
    
    with columns[0]:
        st.session_state.x_scale = st.slider('_Plot scaling in x direction_', 0.5, 10., 1.0, 0.5, key = 10+v)
        st.session_state.y_scale = st.slider('_Plot scaling in y direction_', 0.5, 10., 1.0, 0.5, key = 20+v)
    with columns[1]:
        accident = st.toggle('Task: Accident', value=True, key = 30+v)
        if v>0:
            uncert = st.toggle('Add uncertainty for hydr. conductivity', key = 40+v)
        if uncert:
            p_uncert = st.slider('+/- % deviation of hydraulic conductivity?', 0, 50, 10,1)
    with columns[2]:    
        Q = st.slider('**Pumping rate (m3/s)**', 0., 0.1,0.03, 0.001, format="%5.3f", key = 70+v)
        K_slider_value=st.slider('(log of) **Hydr. conductivity _K_ (m/s)**', log_min,log_max,-3.0,0.01,format="%4.2f", key = 80+v)
        # Convert the slider value to the logarithmic scale and plot value
        K = 10 ** K_slider_value
        st.write("_K (m/s):_ %5.2e" %K)
    
    if uncert:
        K1 = (1 - p_uncert/100)*K
        K2 = (1 + p_uncert/100)*K
        ymax1 = ymax_conf(Q, K1, i, b)
        ymax2 = ymax_conf(Q, K2, i, b)
        x01   = x0_conf(Q, K1, i, b)
        x02   = x0_conf(Q, K2, i, b)
        y1 = np.linspace(-ymax1*0.999, ymax1*0.999, 100)
        y2 = np.linspace(-ymax2*0.999, ymax2*0.999, 100)
        x1 = y1/(np.tan(2*np.pi*K1*i*b*y1/Q))
        x2 = y2/(np.tan(2*np.pi*K2*i*b*y2/Q))

    ymax = ymax_conf(Q, K, i, b)
    x0   = x0_conf(Q, K, i, b)
    y = np.linspace(-ymax*0.999, ymax*0.999, 100)
    # Compute catchment
    x = y/(np.tan(2*np.pi*K*i*b*y/Q))

    x_plot = 500 * st.session_state.x_scale
    y_plot = 1000 * st.session_state.y_scale
    
    # Plot
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)

    if uncert:
        ax.plot(x1,y1, label='Well capture zone lower range',color='lightblue', linestyle='dashed')
        ax.plot(x,y, label='Well capture zone')
        ax.plot(x2,y2, label='Well capture zone upper range',color='grey', linestyle='dashed')
        plt.fill_between(x1,x2,y1,y2,  color='blue', alpha=.07)
        plt.fill_between(x2,y2,    color='blue', alpha=.1)
    else:
        ax.plot(x,y, label='Well capture zone')
        plt.fill_between(x,y,color='blue', alpha=.1)
        plt.fill_between(x,-y,color='blue', alpha=.1)
    if accident:
        ax.plot(-1400,400, marker='o', color='r',linestyle ='None', label='Accident')
    ax.plot(x_well,y_well, marker='o', color='g',linestyle ='None', label='pumping well') 
    ax.set(xlabel='x (m)', ylabel='y (m)',title='Well capture zone of a pumping well')
    ax.set(xlim=(-10*x_plot,x_plot), ylim=(-y_plot, y_plot))
    ax.grid()
    plt.legend()
    st.pyplot(fig)
    
    if uncert:
        st.write("Width of capture zone (m) from: %5.2f" %(2*ymax1), " to %5.2f" %(2*ymax2))
        st.write("Culmination point x_0 (m) from:  %5.2f" %x01, " to %5.2f" %x02)
    else:
        st.write("Width of capture zone (m): %5.2f" %(2*ymax))
        st.write('Culmination point x_0 (m):  %5.2f' %x0)
    
st.subheader('Exercise Step 1: :red[Manage the well to account for the accident]', divider="red")
st.markdown("""
            #### Actions to manage the accident
            
            To manage the accident, we will adapt the pumping rate of the well. In consequenze, the capture zone will change in a way that the accident is not longer within the capture zone.
            
            **To proceed**:
            - Modify the pumping rate.
"""
)

wellcapture(0)

st.subheader('Exercise Step 2: :red[Manage the well under additional consideration of uncertainty]', divider="red")

st.markdown("""
            #### Actions to manage the accident under consideration of uncertainty
            
            In the next step we will additionally account for the uncertainty of the hydraulic conductivity _K_. The uncertainty can occur due to different reason, for example due to measurement uncertainty but also due to local geology, which differ from the idealized assumptions that are underlying the analytical solution.
"""
)

# Create buttons with st.button
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #00FF00;
        color: black;
    }""",
):
    if st.button('Move with Exercise Step 2 and Generate the Plot'):
        st.markdown("""
           
           _To proceed_:
            - Turn on uncertainty by using the switch (middle of the input section)
            - Re-adjust the pumping rate to manage the accident under consideration of uncertainty
            - Increase/Decrease the uncetainty with the slider and investigate the effects on the well capture zone
"""
)
        wellcapture(1)

