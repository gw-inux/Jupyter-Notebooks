# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi, tan
import streamlit as st

st.title('Well capture zone for a confined aquifer')

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

log_min2 = -7.0 # K / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # K / Corresponds to 10^0 = 1

columns = st.columns((1,1), gap = 'large')

with columns[0]:
    x_scale = st.slider('_Plot scaling in x direction_', 0.1, 10., 0.5, 0.01)
    y_scale = st.slider('_Plot scaling in y direction_', 0.1, 10., 0.5, 0.01)
    revers = st.toggle('Revers flow direction')
with columns[1]:
    Q = st.slider('**Pumping rate (m3/s)**', 0., 0.2,0.005, 0.001, format="%5.3f")
    K_slider_value=st.slider('(log of) **Hydr. conductivity (m/s)**', log_min,log_max,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_Hydraulic conductivity (m/s):_ %5.2e" %K)
    b = st.slider('**Aquifer thickness (m)**', 1., 100.,20., 0.1, format="%5.2f")
    i = st.slider('**Gradient of regional flow (dimensionless)**', 0.0001, 1., 0.001, 0.00001,format="%5.2e")
    i_slider_value=st.slider('(log of) **Gradient of regional flow (-)**', log_min2,log_max2,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    i = 10 ** i_slider_value   
    # Display the logarithmic value
    st.write("_Gradient of regional flow (-):_ %5.2e" %K)    


x_max= 1000 #fixed(x_max),
ymax = ymax_conf(Q, K, i, b)
x0   = x0_conf(Q, K, i, b)

x = np.arange(int(x0)-1, x_max,1)
y = np.arange(-ymax*0.999, ymax, 0.1)

x_well = 0
y_well = 0

# Compute catchment
x = -1*y/(np.tan(2*np.pi*K*i*b*y/Q))
    
x_plot = 500 * x_scale
y_plot = 1000 * y_scale
    
# Plot
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(x,y, label='Well capture zone')
ax.plot(x_well,y_well, marker='o', color='r',linestyle ='None', label='pumping well') 
ax.set(xlabel='x (m)', ylabel='y (m)',title='Well capture zone of a pumping well')

if revers:
    ax.set(xlim=(10*x_plot,-x_plot,), ylim=(-y_plot, y_plot))
else:
    ax.set(xlim=(-x_plot,10*x_plot), ylim=(-y_plot, y_plot))
    

plt.fill_between(x,y,color='blue', alpha=.1)
plt.fill_between(x,-y,color='blue', alpha=.1)
ax.grid()
plt.legend()

st.pyplot(fig)
    
st.write("Width of capture zone (m): %5.2f" %(2*ymax))
st.write('Culmination point x_0 (m):  %5.2f' %x0)
    
