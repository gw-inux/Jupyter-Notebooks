# Initialize librarys
from scipy.special import erfc, erf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
import math
import streamlit as st

st.title("1D transient heat transport by conduction and convection")

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

def temp(T0, x, v, t, alpha, D_H, R):
    time = t * 86400
    D = v * alpha + D_H
    
    coeff = T0/2
    
    erf1 = special.erfc((x-v*time/R)/(2*np.sqrt(D*time/R)))
    erf2 = special.erfc((x+v*time/R)/(2*np.sqrt(D*time/R)))
    exp  = np.exp(v*x/D)
    
    return coeff * (erf1 + exp * erf2)




columns = st.columns((1,1,1))
with columns[0]:
    tmax = st.slider('Time for printout in days', 1., 730., 10., 1.)
    x = st.slider('Distance from the input', 0.1, 10., 1., 0.1)
    T_BC = st.slider('Temp. BC', 0.1, 50., 13., 0.1)
    
with columns[1]:
    # Define the minimum and maximum for the logarithmic scale
    log_min = -7.0 # Corresponds to 10^-7 = 0.0000001
    log_max =  -3.0  # Corresponds to 10^0 = 1
    # Log slider with input and print
    K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
    K = 10 ** K_slider_value
    st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
    n_e = st.slider('Effective porosity', 0.01, 0.50, 0.25, 0.01)

with columns[2]:
    heatstor = st.toggle('Account for heat storage')

#Convection
#K = 1e-4
i = 0.001
#n_e = 0.25
q = K * i
v = q/n_e

#Transport general
alpha = 0.01

# Heat transport
T_ini = 8.
#T_BC = 13.

lambda_w = 0.598
lambda_s = 0.35
c_s      = 840
c_w      = 4186.
rho_w    = 1000.
rho_s    = 2650


T0 = T_BC - T_ini


t = np.arange(0., tmax,tmax/80)
    
D_H = (n_e*lambda_w + (1-n_e)*lambda_s) /(n_e * c_w * rho_w)
Kd = c_s/(c_w * rho_w)
R = 1 + (1-n_e)/n_e * rho_s * Kd

T1 = temp(T0, x, v, t, alpha, D_H, 1) + T_ini
T  = temp(T0, x, v, t, alpha, D_H, R) + T_ini

fig, ax = plt.subplots()
ax.plot(t,T1, 'r', label= 'without heat storage')
if heatstor:
    ax.plot(t,T, 'g', label= 'with heat storage')
ax.set(xlabel='time in days', ylabel='temperature (in Celsius)',title='1D Conductive heat transfer')
plt.axis([0,tmax,T_ini-1,T_BC+1])
plt.legend(loc='lower right')
st.pyplot(fig=fig)

st.write("D_H: ",D_H)
st.write("K_H: ",Kd)
st.write("R: ",R)