# Initialize librarys
from scipy.special import erfc, erf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import streamlit as st

st.title("1D transient heat transport and groundwater flow")

st.subheader("Theoretical background")

if st.button ('Show theory'):
    st.write('Equations (groundwater flow and heat conduction in water)')
    
    st.write('Subsequently, the parameters of groundwater flow (left side) and heat conduction (right side) are named.')

    st.latex(r'''S = c\rho''')
    st.write('with S = Storativity, c = heat capacity, and p = density')

    st.latex(r'''K = \lambda''')
    st.write('with K = hydraulic conductivity, lambda = thermal conductivity')

    st.latex(r'''D_f=\frac{K}{S}''')
    st.write('with D_f = hydraulic Diffusivity')

    st.latex(r'''D_h=\frac{\lambda_w}{c_w \rho_w}''')
    st.write('with D_h = thermal Diffusivity')

    st.latex(r'''h = T''')
    st.write('with h = hydraulic head, T = temperature')

    st.write('1-D Conduction without heat storage')

    st.latex(r'''T(x,t)=T_0 erfc (\frac{x}{\sqrt{4 D_h t}})''')

    st.write('1-D Groundwater movement')

    st.latex(r'''h(x,t)=h_0 erfc (\frac{x}{\sqrt{4 D_f t}})''')

"---"
# Definition of the function

# Heat transport

T_ini = 8.
T_BC = 13.
n_e = 0.25
lambda_w = 0.598
c_w      = 4186.
rho_w    = 1000.
T0 = T_BC - T_ini

# Groundwater flow
h_ini = 8
h_BC = 13
h0 = h_BC - h_ini

columns = st.columns((1,1))
with columns[0]:
    tmax = st.slider('Time for printout in days', 1., 730., 10., 1.)
    x = st.slider('Distance from the input', 0.1, 10., 1., 0.1)
    
with columns[1]:
    show_flow = st.toggle('Click here if you want to compute groundwater flow')
    # Define the minimum and maximum for the logarithmic scale
    log_min = -13.0 # Corresponds to 10^-7 = 0.0000001
    log_max =  -3.0  # Corresponds to 10^0 = 1
    # Log slider with input and print
    if show_flow:
        K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
        K = 10 ** K_slider_value
        st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)

S_S = 1E-5
m = 20
S = S_S * m



t = np.arange(0., tmax,tmax/80)
    
D_H = lambda_w /(c_w * rho_w)
T = T_ini+T0 * erfc(x/np.sqrt(4.*D_H*(t*86400.)))

if show_flow:
    D_F = K/S
    h = h_ini+h0 * erfc(x/np.sqrt(4.*D_F*(t*86400.)))
 
    
fig, ax = plt.subplots()
ax.plot(t,T, 'r')
if show_flow:
    ax.plot(t,h, 'b+')
    ax.set(xlabel='time in days', ylabel='temperature (in Celsius) / hydraulic head (in m)',title='1D Conductive heat transfer and groundwater flow')
else:
    ax.set(xlabel='time in days', ylabel='temperature (in Celsius)',title='1D Conductive hbeat transfer')
plt.axis([0,tmax,T_ini-1,T_BC+1])

st.pyplot(fig=fig)


print("D_H: ",D_H)