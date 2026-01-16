# Initialize librarys
from scipy.special import erfc, erf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import streamlit as st
from streamlit_extras.stateful_button import button

st.title("1D transient :red[heat transport] and :blue[groundwater flow] in an unconfined aquifer")

st.subheader("Introduction and Motivation", divider="blue")

st.markdown("""
            **The aim of this app is** to demonstrate that groundwater flow and heat conduction can be described by diffusive motion.
            
            The two fundamental laws of motion in hydrogeology are
            - advective motion (due to a moving carrier) and
            - diffusive motion (due to a gradient). 
            
            The **conduction of heat** as well as **groundwater flow** can be described with diffusion equations.
            
            Accordingly, :blue[**Groundwater flow**] can be computed with the Darcy equation:
"""
)

st.latex(r'''Q_f = -K A \frac{dh}{dl}''')

st.markdown("""
            where:
            - $Q_f$ is the volumetric flow rate (L3/T),
            - _K_ is the hydraulic conductivity (L/T),
            - _A_ is the cross-sectional area of flow (L2),
            - _dh/dl_ is the hydraulic gradient (change in hydraulic head per unit length).
            
            The :red[**Heat conduction**] can be computed with Fourier's law as
"""
)

st.latex(r'''Q_h = -\lambda A \frac{dT}{dx}''')

st.markdown("""
            where:
            - _Q_h_ is the heat flux (W),
            - $\lambda$ is the thermal conductivity (),
            - _A_ is the cross-sectional area (L2),
            - _dT/dx_ = is the temperature gradient (change in temperature per unit length).
            
            Both equations can be analytically solved to describe 1D motion processes in homogenous media (groundwater flow/heat conduction). The resulting temperature _T_ (heat conduction) and the resulting hydraulic heads _h_ (groundwater flow) are comparable if the parameters are equivalent.
            
            **This interactive document allows** to apply the 1D heat conduction equation and the 1D groundwater flow equation for a 1D setup. Heat conduction is computed in water or rock (granit) only. For comparison, groundwater flow is computed for a porous media (e.g., sand).
            
            The situation is characterized by the following parameters:
            - heat transport only due to conduction
            - (for heat transport) background temperature 10 degree celsius
            - (for groundwater flow) initial head 10 m
            
            **Heat conduction** in water only with the following parameters
            - $\lambda_w$ = 0.598 W/m/K
            - $c_w$       = 4186 J/kg/K
            - $\\rho_w$      = 1000 kg/m³
            
            **Heat conduction** in granite only
            - $\lambda_r$ = 2.5 W/m/K
            - $c_r$       = 740 J/kg/K
            - $\\rho_r$   = 2650 kg/m³
            
            **User-defined** parameters for groundwater flow
            - hydraulic conductivity _K_
            - specific yield $S_y$
"""
)

st.markdown("---")

st.subheader("Theoretical background", divider="blue")

# Optional theory here
lc1, mc1, rc1 = st.columns([1,3,1])
with mc1:
    show_theory = button('Show/Hide more about the underlying **theory**', key= 'button1')
    
if show_theory:
    st.write('Equations (groundwater flow and heat conduction in water)')
    
    st.write('Subsequently, the parameters of groundwater flow (in unconfined aquifers) and heat conduction are named.')

    st.latex(r'''S = c\rho''')
    st.write('with S = Storativity, c = heat capacity, and $\\rho$ = density')

    st.latex(r'''K = \lambda''')
    st.write('with K = hydraulic conductivity, $\lambda$ = thermal conductivity')

    st.latex(r'''D_f=\frac{Kb}{S}''')
    st.write('with $D_f$ = hydraulic diffusivity, $b$ = aquifer thickness')

    st.latex(r'''D_h=\frac{\lambda_w}{c_w \rho_w}''')
    st.write('with $D_h$ = thermal diffusivity')

    st.latex(r'''h = T''')
    st.write('with h = hydraulic head, T = temperature')
    
    st.write(':blue[1-D Groundwater movement] (simplified 1D diffusivity analogy)')
    st.latex(r'''h(x,t)=h_0 erfc (\frac{x}{\sqrt{4 D_f t}})''')

    st.write(':red[1-D Conduction without heat storage]')
    st.latex(r'''T(x,t)=T_0 erfc (\frac{x}{\sqrt{4 D_h t}})''')

st.markdown("---")

# Definition of the function

# Initial parameters
# Heat transport
T_ini = 10.
h_ini = T_ini

# Water
lambda_w = 0.598
c_w      = 4186.
rho_w    = 1000.

# Granite
lambda_r = 2.5
c_r      = 750
rho_r    = 2650.

# Porous sand
ne = 0.25
lambda_s = 0.35
c_s = 840
rho_s = 2650

# For this app we dont show heat conduction in porous media
show_porous = False

# Variable parameters
columns = st.columns((1,1))
with columns[0]:
    TB = st.slider('Temperature/Head at inlet boundary', T_ini, 100., 15., 0.1)
    show_rock = st.toggle('Click here if you want to compute heat conduction for Granite')
    #show_porous = st.toggle('Click here if you want to compute heat conduction for water saturated sand')
    tmax = st.slider('Time to plot in days', 1., 730., 60., 1.)
    x = st.slider('Distance from the source', 0.1, 10., 1., 0.1)
    
with columns[1]:
    show_flow = st.toggle('Click here if you want to compute groundwater flow')
    # Define the minimum and maximum for the logarithmic scale
    log_min = -13.0 # Corresponds to 10^-7 = 0.0000001
    log_max =  -3.0  # Corresponds to 10^0 = 1
    # Log slider with input and print
    if show_flow:
        container = st.container()
        K_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min,log_max,-5.0,0.01,format="%4.2f" )
        K = 10 ** K_slider_value
        container.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
        SY = st.slider('**Specific Yield**', 0.01, 0.50, 0.25, 0.01)
        S = SY
        b = st.slider('**Aquifer thickness**', 1, 50, 10, 1)

#Computation
T0 = TB - T_ini
h0 = T0

#t = np.arange(0., tmax,tmax/80)
#t_r = np.arange(0., tmax,tmax/200)
 
t = np.linspace(1e-6, tmax, 81)       # days
t_r = np.linspace(1e-6, tmax, 201)    # days
 
D_H_w = lambda_w /(c_w * rho_w)
D_H_r = lambda_r /(c_r * rho_r)
D_H_s = (ne * lambda_w + (1-ne) * lambda_s) /(ne * c_w * rho_w)
K_H_s = c_s / (c_w * rho_w)
R_s = 1 + (1-ne)/ne * rho_s * K_H_s

T_w = T_ini + T0 * erfc(x/np.sqrt(4.*D_H_w*(t*86400.)))

if show_rock:
    T_r = T_ini+T0 * erfc(x/np.sqrt(4.*D_H_r*(t_r*86400.)))
    
if show_porous:
    T_s = T_ini+T0 * erfc(x/np.sqrt(4.*D_H_s*(t_r*86400.)))
    T_s2 = T_ini+T0 * erfc(x/np.sqrt(4.*D_H_s*(t_r*86400.)/R_s))

if show_flow:
    D_F = K*b/S
    h = h_ini + h0 * erfc(x/np.sqrt(4.*D_F*(t*86400.)))
 
# Plotting
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(t, T_w, 'c', label = 'Heat cond. in water only')

if show_rock:
    ax.plot(t_r,T_r, 'r', label = 'Heat cond. in granite only')
    
if show_porous:
    ax.plot(t_r,T_s, 'c--', label = 'Heat cond. in water-saturated sand - without heat storage')
    ax.plot(t_r,T_s2, 'c', label = 'Heat cond. in water-saturated sand - with heat storage')
    
if show_flow:
    ax.plot(t,h, 'bo', mfc='none', label = 'Groundwater flow')
    plt.ylabel("temp. (in Celsius) / head (in m)",fontsize=14)
else:
    plt.ylabel("temperature (in Celsius)",fontsize=14)
    
plt.axis([0,tmax,T_ini-1,TB+1])
plt.title(f"1D heat conduction & groundwater flow at x = {x} m", fontsize=16)
plt.xlabel("time in days",fontsize=14)
plt.legend(frameon=False, fontsize=12)

st.pyplot(fig=fig)

st.write(':red[Thermal] diffusivity pure water:  %5.2e' %D_H_w)
if show_rock:
    st.write(':red[Thermal] diffusivity granite:  %5.2e' %D_H_r)
if show_porous:
    st.write(':orange[Thermal] diffusivity water saturated sand:  %5.2e' %D_H_s)
if show_flow:
    st.write(':blue[Hydraulic] diffusivity:  %5.2e' %D_F)