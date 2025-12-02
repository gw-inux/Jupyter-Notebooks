import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button
from decimal import Decimal

st.title('1D Transport with advection and dispersion')
st.subheader('Solute input as :orange[Continuous Injection]', divider="orange")

# version 1.1 - last modified by Thomas Reimann on 2025 02 02 

st.markdown("""
            ### About the computed situation
            
            Transport is calculated for steady one-dimensional flow through a homogeneous porous medium in a 1 meter long laboratory column with a flow rate, _Q_, of approximately 2x10<sup>-7</sup> m<sup>3</sup>/sec and specific discharge, _q_, of 0.0001 m/s.
            
            The average velocity _v_ depends on the porosity _n_ (_v=q/n_) which is printed above the graphs.
            
            Solutes are continuously injected on the left with a user-defined concentration  _Co_ in g/m<sup>3</sup> (same as mg/L).
            
            The graph shows the solute concentration at an observation point a user-defined distance from the source. Concentration is computed for pure advective transport and for advective-dispersive transport.
""", unsafe_allow_html=True
)

columns1 = st.columns((1,1,1), gap = 'large')
with columns1[1]:
    theory = button('Show/Hide Equation', key = 'button1') # This button from Streamlit.Extras keeps the part open until the user press the button again
    
if theory:
    st.latex(r'''C(x,t) = \frac{Co}{ 2 }  \left( erfc \left( \frac{x - vt}{2 \sqrt{Dt}} \right) + exp \left(\frac{vx}{D} \right) erfc \left( \frac{x + vt}{2 \sqrt{Dt}} \right)\right)''')

    st.markdown(
    """
    - _C_ : concentration (grams/cubic meter)
    - _Co_ : initial concentration (grams/cubic meter)
    - _x_ : distance from the source (meters)
    - _v_ : average linear velocity = Ki/n (meters/second)
    - _t_ : time since the source was introduced (seconds)
    - _D_ : dispersion coefficient - product of dispersivity and average linear velocity (square meters/second)
"""
)

"---"

#FUNCTIONS FOR COMPUTATION
def concentration(x, t, a, v, c0, R):
    # Computes 1D advection-dispersion with retardation
    D = v * a
    
    coeff = c0/2
    
    erf1 = special.erfc((x-v*t/R)/(2*np.sqrt(D*t/R)))
    erf2 = special.erfc((x+v*t/R)/(2*np.sqrt(D*t/R)))
    exp  = np.exp(v*x/D)
    
    return coeff * (erf1 + exp * erf2)
    
def concentration_a(x, t, v, c0, R):
    # Computes 1D advection with retardation
    tPV =   x/v*R
    residence_time = t/tPV
    
    if residence_time <= 1:
        conc = 0
    else:
        conc = c0
    
    return conc

# Data for the scenario

Q  = 2.0268E-7 # Discharge in the column (cubic meters per second)
r  = 0.0254    # Column radius (meters)
lmax = 1.0     # Column length
ci = 0         # Initial concentration

tmax = 10000   # Maximum time
dt = 10         # Time discretization for ploting

columns3 = st.columns((1,1,1), gap = 'large')

with columns3[0]:
    with st.expander("Control for the breakthrough curves"):
        l  = st.slider(f'**Distance of observation from source (m)**',0.01,lmax,0.5,0.01)

with columns3[1]:
    with st.expander("Controls for the concentration profile"):
        time_p = st.slider(f'**Time to plot the conc. profile (s)**',0,3600,600,10)
    plot_DATA = False
    #plot_DATA = st.toggle('Show Measured data for calibration',False)
    #if plot_DATA:
    #    l = 0.75
    #    time_p = l/(Q/(np.pi*r**2)/n)
    #    st.write(f"**Calibration data measured {l} m from the source**")
    #    st.write(f"**Concentration profile is for {round(time_p)} seconds**")
    #    st.write('**To calibrate, adjust parameter values until model matches data**')
    #    st.write('**Check calibrated values using button below graphs**')
    #else:
    #    l  = st.slider(f'**Distance of observation from source (m)**',0.01,lmax,0.5,0.01)
    #    time_p = st.slider(f'**Time to plot the conc. profile (s)**',0,10000,600,60)

with columns3[2]:
    with st.expander("Controls for the solute transport"):
        c0 = st.slider(f'**Input concentration (g/m³) (same as mg/L)**',100,10000,1000,100) 
        n  = st.slider(f'**Porosity (dimensionless)**',0.01,0.6,0.2,0.01)       
        disp = st.toggle('Toggle here to account for dispersion')
        a  = st.slider(f'**Longitudinal dispersivity (m)**',0.002,0.100,0.010,0.001, format="%5.3f")
    
"---"

# Computation of intermediate results
A =     np.pi*r**2
q =     Q/A
v =     q/n

# Compute concentration for profile
loc = np.arange(0., lmax, lmax/150)
conc_p = concentration(loc, time_p, a, v, c0, 1)
    
# Advection only
loca =    []
conca_p = []

for x in np.linspace(0, lmax, num=150):
    ca_p = concentration_a(x, time_p, v, c0, 1)
    conca_p.append(ca_p)
    loca.append(x)


# Computation of breakthrough
time = np.arange(0., tmax, tmax/150)
conc = concentration(l, time, a, v, c0, 1)

# Computation of breakthrough for advection only
timea  = []
conca  = []

for t in range(0, tmax, dt):
    ca = concentration_a(l, t, v, c0, 1)
    
    conca.append(ca)
    timea.append(t)
    
         
# measurements
t_obs = [1000,	1250,	1500,	1750,	2000,	2250,	2500,	2750,	3000,	3250,	3500,	3750,	4000,	4250]
c_obs = [5.79,	32.19,	93.93,	190.40,	308.54,	432.26,	548.89,	651.01,	735.79,	803.45,	855.85,	895.50,	924.97,	946.55]

st.write("Concentration for an average velocity _v_ = ","% 7.3E"% v, " (m/s)")

# PLOT FIGURE

# General figure settings
fig = plt.figure(figsize=(9,8))
ax = fig.add_subplot(2, 1, 1)
# Upper figure 
ax.set_title  (f"Concentration breakthrough curve at x = {l} meters", fontsize=14)
ax.set_xlabel ('Time (s)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
ax.plot(timea, conca, 'fuchsia', linewidth=2, label="Computed: ONLY Advection")
if disp:
    ax.plot(time,  conc,  'navy',    linewidth=2, label="Computed: Advection-Dispersion")

if plot_DATA == 1:
    ax.plot(t_obs, c_obs, 'ro', label="Measured")

plt.ylim(0, 1.12*c0)
plt.xlim(0, tmax)
plt.xticks(np.arange(0, 11000, 1000),fontsize=14)
plt.yticks(fontsize=14)
legend = plt.legend(loc='upper right', fontsize=14, framealpha=0.8)
legend.get_frame().set_linewidth(0.0)

ax = fig.add_subplot(2, 1, 2)
# Lower figure
ax.set_title  (f"Concentration profile along the column at t = {round(time_p)} seconds", fontsize=14)
ax.set_xlabel ('Column length (m)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
  
ax.plot(loca, conca_p, 'orange', linewidth=2, label="Computed: ONLY Advection")  
if disp:
    ax.plot(loc,  conc_p,  'green',    linewidth=2, label="Computed: Advection-Dispersion")

plt.ylim(0, 1.19*c0)
plt.xlim(0, lmax)
plt.xticks(np.arange(0, 1.01*lmax, 0.1),fontsize=14)
plt.yticks(fontsize=14)
legend = plt.legend(loc='upper right', fontsize=14, framealpha=0.8)
legend.get_frame().set_linewidth(0.0)

plt.subplots_adjust(hspace=0.40)
st.pyplot(fig)

if plot_DATA:
    columns4 = st.columns((1,1,1), gap = 'large')
    with columns4[1]:
        calib = st.button('Show input values that will generate observed calibration data')
    
    if calib:
        st.markdown("""
        - concentration : 1000 grams per cubic meter
        - porosity : 0.34
        - longitudinal dispersivity : 0.05 meters
        """, unsafe_allow_html=True
        )
        
st.markdown (
    """   
    :green
    ___
  
"""
)

st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over a 1000 volunteers.]

        :green[Please help us by using the following link when sharing this tool with others.]

        https://interactive-education.gw-project.org/1D_conservative_transport/
        """   
)

