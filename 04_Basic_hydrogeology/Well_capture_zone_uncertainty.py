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
    x0 = Q/(2.*np.pi*K*i*b)
    return x0

# Computaton of the well catchment (Berechnung der Trennstromlinie)

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min = -7.0 # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # K / Corresponds to 10^0 = 1

log_min2 = -5.0 # K / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # K / Corresponds to 10^0 = 1

columns = st.columns((1,1,1), gap = 'medium')

with columns[0]:
    x_scale = st.slider('_Plot scaling in x direction_', 0.5, 10., 1.0, 0.5)
    y_scale = st.slider('_Plot scaling in y direction_', 0.5, 10., 1.0, 0.5)
with columns[1]:
    accident = st.toggle('Task: Accident')
    plume = st.toggle('Task: Plume')
    uncert = st.toggle('Add uncertainty for hydr. conductivity')
    if uncert:
        p_uncert = st.slider('+/- % deviation of hydraulic conductivity?', 0, 50, 10,1)
with columns[2]:
    b = st.slider('**Aquifer thickness (m)**', 1., 100.,25., 0.1, format="%5.2f")
    i_slider_value=st.slider('(log of) **Regional flow gradient (dimensionless)**', log_min2,log_max2,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    i = 10 ** i_slider_value   
    # Display the logarithmic value
    st.write("_Regional flow gradient (dimensionless):_ %5.2e" %i)    
    Q = st.slider('**Pumping rate (m3/s)**', 0., 0.1,0.03, 0.001, format="%5.3f")
    K_slider_value=st.slider('(log of) **Hydr. conductivity _K_ (m/s)**', log_min,log_max,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_K (m/s):_ %5.2e" %K)


x_well = 0
y_well = 0

x_max= 1000 #fixed(x_max)
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
if accident:
    ax.plot(-1400,400, marker='o', color='r',linestyle ='None', label='Accident')
if plume:
    ax.vlines(-9.95*x_plot, -770, 770, linewidth = 5, color='r',label='Plume width')
    
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
    
