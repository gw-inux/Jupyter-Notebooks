# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import streamlit as st

st.title('Infiltration capacity')

st.write('This application compute the infiltration capacity as function of time. The function we are looking is') 
st.latex("f_p = f_c + (f_o - f_c) e^{-kt}")
st.write('with')
st.markdown("* f_p = infiltration capacity (cm/hr)")
st.markdown("* f_c = equilibrium infiltration capacity (cm/hr)")
st.markdown("* f_0 = initial infiltration capacity (cm/hr)")
st.markdown("* k = a rate of infiltration capacity decrease (1/hr)")

# Input data

# Define the minimum and maximum for the logarithmic scale
log_min = -5.0 # Corresponds to 10^-7 = 0.0000001
log_max = -2.0  # Corresponds to 10^0 = 1

columns = st.columns((1,1), gap = 'large')
    
with columns[0]:
    f0 = st.slider(f'**Initial infiltration capacity (cm/hr)**:',0.0,50.0,7.0,0.01)
    fc = st.slider(f'**Equilibrium infiltration capacity (cm/hr)**:',0.0,50.0,5.0,0.01)
    prec = st.slider(f'**Precipitation in cm/hr**:',0.0,50.0,3.0,0.01)
    
    
    
    
with columns[1]:
    k_slider_value = st.slider(f'(log of) Rate of infiltration capacity decrease',log_min,log_max,-2.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    k = 10 ** k_slider_value
    # Display the logarithmic value
    st.write("**Rate of infiltration capacity decrease (1/hr)** %5.2e" %k)
    x_point = st.slider(f'**Point (x-axis) for result output**:',0,86400,0,10)
    
    
tmax = 86400
t = np.arange(0, tmax, tmax/200)

if f0<fc:
    f0 = fc

y = fc+(f0-fc)*(math.e**(k*t*-1))
    
#Compute K_eq for the example point
y_point = fc+(f0-fc)*math.e**(k*-1*x_point)
    
# Plot
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(t,y, linewidth =3, label='Infiltration rate')
ax.set(xlabel='time in s', ylabel='infiltration capacity / precipitation rate in cm/hr',title='Infiltration capacity')
ax.set(xlim=(0, tmax), ylim=(0, max(f0,prec)*1.1))
if prec <= fc:
    plt.hlines(prec, 0, tmax, colors='aqua', linestyles='solid', label='precipitation rate')
ax.fill_between(t, prec, 0, facecolor= 'lightblue')
if prec > fc:
    plt.hlines(prec, 0, tmax, colors='red', linestyles='solid', label='precipitation rate')
    ax.fill_between(t, prec, y, where=prec > y, facecolor= 'red', alpha=0.5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='your input')
xticks = np.arange(0, tmax, 7200)
ax.set_xticks(xticks)
ax.grid()
plt.legend()

st.pyplot(fig)
 
st.write("Time after beginning of precipitation: %3i" %x_point)
st.write('Infiltration rate in cm/hr:  %5.2f' %y_point)