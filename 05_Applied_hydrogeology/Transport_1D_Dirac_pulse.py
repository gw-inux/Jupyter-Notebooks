import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import streamlit as st

st.title('1D Transport with advection and dispersion')
st.subheader('Tracer input as :green[Dirac Pulse] data', divider="green")
    
with st.expander("Show the equation"):
    st.latex(r'''c(x,t) = \frac{\Delta M}{2 \cdot A \cdot n_e \sqrt{\pi \cdot D \cdot t}} e^{-\frac{(x - v \cdot t)^2}{4 D \cdot t}}''')

st.markdown("""
            ### About the computed situation
            
            Transport is considered for a 1D system with the following characteristics
            * steady groundwater flow,
            * specific discharge $q$ of 0.016 m/s.
            * The solutes are added by an Dirac pulse with a user defined mass.
            
            The average velocity is depending on the porosity and printed below the interactive plot.        
            
            The plots show the solute concentration for advective-dispersive transport.
            
            (1) The **break through** curve is computed for an observation point in a user-defined distance from the source. It is possible to plot a second breakthrough curve in an user-defined distance relative to the first observation.
            
            (2) The **concentration profile** shows the situation for a specific time.
""", unsafe_allow_html=True
)

st.subheader("Interactive plot", divider = 'green')
#FUNCTIONS FOR COMPUTATION; ADS = ADVECTION, DISPERSION AND SORPTION - EVENTUALLY SET RETARDATION TO 1 FOR NO SORPTION

def c_ADE(x, t, dM, Area, n, a, v):
    
    D = v * a
    
    # Pre-factor term
    prefactor = dM / (2 * Area * n * np.sqrt(np.pi * D * t))
    
    # Exponential term
    exponential = np.exp(-((x - v * t) ** 2) / (4 * D * t))
    
    # Concentration
    c = prefactor * exponential
    return c

st.write('')
"---"
columns2 = st.columns((1,1,1))

with columns2[0]:
    with st.expander("Control for the breakthrough curves"):
        multi = st.toggle("Plot two curves")
        x  = st.slider(f'**Distance of the primary observation from source (m)**',1.,100.,1.,1.)
        if multi:
            dx = st.slider(f'**Distance between the primary and secondary observation (m)**',0.,50.,1.,0.1) 

with columns2[1]:
    with st.expander("Controls for the concentration profile"):
        tp = st.slider(f'**Time for the concentration profile (s)**',1.,1800.,120.,1.)      
 
with columns2[2]:
    with st.expander("Controls for the solute transport"):
        dM = st.slider(f'**Input mass (g)**',0.01,5.0,1.0,0.01)
        n = st.slider(f'**Porosity (dimensionless)**',0.02,0.6,0.2,0.001)       
        a = st.slider(f'**Longitudinal dispersivity (m)**',0.001,1.0,0.01,0.001)
    
"---"
r  = 2      # Column radius
Q = 0.2
Area = np.pi*r**2
q = Q/Area
v = q/n

# Data for plotting
t0 = 1      # Starting time
t1 = 1800   # Ending time
dt = 2      # Time discretization
ci = 0      # Initial concentration

# Defining time range
t = np.arange(t0, t1, dt)

# Computation of concentration (terms in brackets)
# Set fraction of distance
cmax   = 0
time   = []
space  = []
conc   = []
conc2  = []
concp  = []
   

#compute break through
for t in range(t0, t1, dt):      
    # ADVECTION-DISPERSION
    cmax1 = ci+c_ADE(1, t, 1, Area, n, 0.01, v)
    if cmax1 > cmax:
        cmax = cmax1
    c = ci+c_ADE(x, t, dM, Area, n, a, v)
    conc.append(c)
    if multi:
        c2 = ci+c_ADE(x+dx, t, dM, Area, n, a, v)
        conc2.append(c2) 
    time.append(t)
    
#compute concentration profile
for xp in np.linspace(0, 100, num=1000):      
    # ADVECTION-DISPERSION
    cp = ci+c_ADE(xp, tp, dM, Area, n, a, v)
    concp.append(cp)
    space.append(xp)     
        
# measurements
t_obs = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
c_obs = [1e-3, 5e-2, 8.5e-2, 9.7e-2, 9.9e-2, 10e-2, 10e-2, 10e-2, 10e-2, 10e-2]
   
#PLOT FIGURE
fig = plt.figure(figsize=(9,8))
ax = fig.add_subplot(2, 1, 1)
ax.set_title('1D solute transport with advection-dispersion', fontsize=16)
ax.set_xlabel ('Time (s)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
# PLOT HERE
ax.plot(time,conc, 'navy', linewidth=2, label="Breakthrough observation 1")
if multi:
    ax.plot(time,conc2, 'lightblue', linewidth=2, label="Breakthrough observation 2")
plt.ylim(0,cmax*0.5)
plt.xlim(0,t1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(frameon=False, loc='upper right', fontsize=14)

ax = fig.add_subplot(2, 1, 2)
ax.set_xlabel ('Distance from source along flow directions (m)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
# PLOT HERE
ax.plot(space,concp, 'orange', linewidth=2, label="Concentration profile")
plt.ylim(0,cmax*0.5)
plt.xlim(0,100)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(frameon=False, loc='upper right', fontsize=14)
    
st.pyplot(fig)

st.write("Average velocity _v_ (m/s) = ","% 7.3E"% v)