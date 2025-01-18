import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import streamlit as st

st.title('1D transport with advection and dispersion')
st.subheader('Tracer input as :green[Mass Pulse] data', divider="green")

columns1 = st.columns((1,1,1), gap = 'large')
with columns1[1]:
    theory = st.button('Show Equation')
    
if theory:
    st.latex(r'''C(x,t) = \frac{M}{2  A  n \sqrt{\pi  D  t}} e^{-\frac{(x - v t)^2}{4 D t}}''')
    st.markdown(
    """    
    - M : mass (grams)
    - C : concentration (grams/cubic meter)
    - A : area of flow column (square meters)
    - v : average linear velocity = product of hydraulic conductivity and gradient divided by effective porosity (meters/second)
    - D : dispersion coefficient - product of dispersivity and average linear velocity (square meters/second)
    - x : distance from the source (meters)
    - t : time since the source was introduced (seconds)

"""
)

st.markdown("""
            ### About the computed situation
            
            Solute transport with one-dimensional spreading (longitudinal in the direction of flow) in steady flow through ahomogeneous porous medium.
            
            The specific discharge _q_ is fixed at 0.01 m/s. However, the average linear velocity depends on the effective porosity (v = q/n). The velocity is printed below the interactive plot.
            
            The solute is added as a user defined mass on the plane of the inlet end of the flow column at time = 0. The plane is infinitesimally thin, which although impossible in physical space, can be mathematically useful in representing a spill of finite mass in a small area.

            Concentration is calculated at a user-defined distance from the source.
            
            The result is shown as a graph of concentration versus time (a break through curve). A second breakthrough curve can be calculated and displayed for another location at a user-defined distance downgradient of the first observation.
""", unsafe_allow_html=True
)
"---"

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

columns2 = st.columns((1,1), gap = 'large')

with columns2[0]:
    tp = st.slider(f'**Time for the concentration profile (s)**',60.,6000.,60.,1.)
    multi = st.toggle("Plot two curves")
    x  = st.slider(f'**Distance of the primary observation from source (m)**',0.1,1.0,0.1,0.01)
    if multi:
        dx = st.slider(f'**Distance between the primary and secondary observation (m)**',0.1,1.0,0.1,0.01) 
    
with columns2[1]:
    dM = st.slider(f'**Input mass (mg)**',0.001,0.1,0.001,0.0001,("%.3e"))
    n = st.slider(f'**Porosity (dimensionless)**',0.02,0.6,0.2,0.001)       
    a = st.slider(f'**Longitudinal dispersivity (m)**',0.001,1.0,0.01,0.001)
    
"---"
r  = 0.0254      # Column radius in meters 
Q = 4.05365983277998E-07 # 24.322 ml/minute which is a reasonable flow for laboratory column and produces a q of 0.0002,
Area = np.pi*r**2
q = Q/Area
v = q/n

# Data for plotting
t0 = 1      # Starting time
t1 = 6000   # Ending time
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
    cmax1 = ci+c_ADE(0.1, t, dM, Area, n, 0.01, v)
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
   
st.write("**Average velocity _v_ (m/s)** = ","% 7.3E"% v)

#PLOT FIGURE
fig = plt.figure(figsize=(9,12))
ax = fig.add_subplot(2, 1, 1)
ax.set_title('1D solute transport with advection-dispersion', fontsize=16)
ax.set_xlabel ('Time (s)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
# PLOT HERE
ax.plot(time,conc, 'navy', linewidth=2, label="Breakthrough observation 1")
if multi:
    ax.plot(time,conc2, 'lightblue', linewidth=2, label="Breakthrough observation 2")
plt.ylim(0,cmax)
plt.xlim(0,t1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(frameon=False, loc='upper right', fontsize=14)

ax = fig.add_subplot(2, 1, 2)
ax.set_xlabel ('Distance from source along flow directions (m)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
# PLOT HERE
ax.plot(space,concp, 'orange', linewidth=2, label="Concentration profile")
plt.ylim(0,cmax)
plt.xlim(0,100)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(frameon=False, loc='upper right', fontsize=14)
    
st.pyplot(fig)
