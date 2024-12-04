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

st.subheader('Application/Exercise: :green[Management of a plume]', divider="green")
st.markdown("""
            ### Initial situation and challenge
            
            A contamination plume should be captured by an well. Your task is to find the required pumping rate to efficiently capture the plume.
            
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
        stb.single_choice(":blue[**Initial questions 1?**]",
                  ["Answer", "Answer", "Answer", "Answer"],
                  1,success='CORRECT! We will do this in the next steps.', error='This option is not suitable. Re-Think the situation.')
    
    with columnsQ1[1]:
        stb.single_choice(":blue[**Initial questions 1?**]",
                  ["Answer", "Answer", "Answer", "Answer"],
                  1,success='CORRECT! We will do this in the next steps.', error='This option is not suitable. Re-Think the situation.')
"---"
st.subheader('Exercise: :green[Manage the well to account for the accident]', divider="green")
st.markdown("""
            #### Actions to manage the plume:
                
            Subsequently you can proceed with the exercise by activating the steps.
"""
)

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
            To manage the plume, we will adapt the pumping rate of the well. In consequenze, the capture zone will change in a way that the plume is captured.
            
           _To proceed_:
            - Modify the pumping rate.
"""
)
    if st.button('Proceed with Exercise Step 2'):
        st.markdown("""
            **STEP 2:**
            An on-site investigation provided data for the hydraulic conductivity _K_. The result of the investigation is a value of _K_ = 3 x 10^-3
            
           _To proceed_:
            - Adapt the hydraulic conductivity _K_,
            - Re-adjust the pumping rate.
"""
)
    if st.button('Proceed with Exercise Step 3'):
        st.markdown("""
            **STEP 3:**
            
            Now we will additionally account for the uncertainty of the hydraulic conductivity _K_.
            
           _To proceed_:
            - Turn on uncertainty by using the switch (middle of the input section),
            - Re-adjust the pumping rate,
            - Increase/Decrease the uncetainty with the slider and investigate the effects on the well capture zone.
"""
)
        
        
        
# Function for catchment width (maximale Breite des Einzugsgebietes)
def ymax_conf(Q, K, i, b):
    ymax = Q/(2.*K*i*b)
    return ymax

# Function for the culmination point (Kulminationspunkt)
def x0_conf(Q, K, i, b):
    x0 = Q/(2.*np.pi*K*i*b)
    return x0

# Computaton of the well catchment (Berechnung der Trennstromlinie)

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

columns = st.columns((1,1,1), gap = 'medium')

with columns[0]:
    x_scale = st.slider('_Plot scaling in x direction_', 0.5, 10., 1.0, 0.5)
    y_scale = st.slider('_Plot scaling in y direction_', 0.5, 10., 1.5, 0.5)
with columns[1]:
    plume = st.toggle('Task: Plume',value=True)
    uncert = st.toggle('Add uncertainty for hydr. conductivity')
    if uncert:
        p_uncert = st.slider('+/- % deviation of hydraulic conductivity?', 0, 50, 10,1)
with columns[2]:    
    Q = st.slider('**Pumping rate (m3/s)**', 0., 0.1,0.001, 0.001, format="%5.3f")
    K_slider_value=st.slider('(log of) **Hydr. conductivity _K_ (m/s)**', log_min,log_max,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
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
#x = -1*y/(np.tan(2*np.pi*K*i*b*y/Q))
x = y/(np.tan(2*np.pi*K*i*b*y/Q))

x_plot = 500 * x_scale
y_plot = 1000 * y_scale
    
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
if plume:
    ax.vlines(-9.95*x_plot, -770, 770, linewidth = 10, color='darkorchid',label='Plume width')
    
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
    
