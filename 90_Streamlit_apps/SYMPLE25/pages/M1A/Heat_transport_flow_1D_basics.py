# Initialize librarys
from scipy.special import erfc, erf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import streamlit as st

st.title("1D transient heat transport and groundwater flow")


# Definition of the function

# Heat transport

T_ini = 8.
T_BC = 13.
tmax = st.slider('Time for printout in days', 1., 730., 10., 1.)
x = st.slider('Distance from the input', 0.1, 10., 1., 0.1)
n_e = 0.25
lambda_w = 0.598
c_w      = 4186.
rho_w    = 1000.
T0 = T_BC - T_ini

# Groundwater flow
h_ini = 8
h_BC = 13
h0 = h_BC - h_ini

# Define the minimum and maximum for the logarithmic scale
log_min = -13.0 # Corresponds to 10^-7 = 0.0000001
log_max =  -3.0  # Corresponds to 10^0 = 1

# Log slider with input and print
K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
K = 10 ** K_slider_value
st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
S_S = 1E-5
m = 20
S = S_S * m



t = np.arange(0., tmax,tmax/80)
    
D_H = lambda_w /(c_w * rho_w)
D_F = K/S
    
T = T_ini+T0 * erfc(x/np.sqrt(4.*D_H*(t*86400.)))
h = h_ini+h0 * erfc(x/np.sqrt(4.*D_F*(t*86400.)))
    
fig, ax = plt.subplots()
ax.plot(t,T)
ax.plot(t,h, 'b+')
ax.set(xlabel='time in days', ylabel='temperature / hydraulic head',title='1D Conductive Heat transfer and groundwater flow')
plt.axis([0,tmax,T_ini-1,T_BC+1])
ax.grid()

st.pyplot(fig=fig)


print("D_H: ",D_H)