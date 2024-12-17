import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import streamlit as st

#FUNCTIONS FOR COMPUTATION; ADS = ADVECTION, DISPERSION AND SORPTION - EVENTUALLY SET RETARDATION TO 1 FOR NO SORPTION

def IC(PE,r_time):
    
    IC1 = np.sqrt(0.25*PE/r_time)*(1-r_time)
    
    if (IC1>0):
        IC2 = 1-(1-special.erfc(abs(IC1)))
    else:
        IC2 = 1+(1-special.erfc(abs(IC1)))
    
    IC3 = np.sqrt(0.25*PE/r_time)*(1+r_time)
    
    if (IC3>0):
        IC4 = 1-(1-special.erfc(abs(IC3)))
    else:
        IC4 = 1+(1-special.erfc(abs(IC3)))
    
    if IC4 == 0:
        IC5 = IC2
    else:
        IC5 = IC2+np.exp(PE)*IC4
    
    IC  = 1-0.5*IC5
    
    return IC

def BC(PE,r_time, r_dur):
    # BCx positive pulse
    
    BC1 = np.sqrt(0.25*PE/r_time)*(1-r_time)
    
    if (BC1>0):
        BC2 = 1-(1-special.erfc(abs(BC1)))
    else:
        BC2 = 1+(1-special.erfc(abs(BC1)))
        
    BC3 = np.sqrt(0.25*PE/r_time)*(1+r_time)
    
    BC4 = special.erfc(BC3)
    
    if BC4 == 0:
        BC5 = BC2
    else:
        BC5 = BC2 + np.exp(PE) * BC4
    
    # BCCx negative pulse
    if r_time > r_dur:
        BCC1 = np.sqrt(0.25 * PE / (r_time - r_dur)) * (1 - (r_time - r_dur))
        if BCC1 > 0:
            BCC2 = 1 - (1 - special.erfc(abs(BCC1)))
        else:
            BCC2 = 1 + (1 - special.erfc(abs(BCC1)))  
        BCC3 = np.sqrt(0.25 * PE / (r_time - r_dur)) * (1 + (r_time - r_dur))
        BCC4 = special.erfc(BCC3)
        if BCC4 == 0:
            BCC5 = BCC2
        else:
            BCC5 = BCC2 + np.exp(PE) * BCC4      
    if r_time <= r_dur:
        BC = 0.5 * BC5
    else:
        BC = 0.5 * (BC5 - BCC5)
    return BC

st.title('1D Transport with advection and dispersion')

st.write('The plot shows the solute concentration at an observation point in a user-defined distance from the source. Transport is considered for a 1D system with steady groundwater flow. Solutes are added by an finite pulse with a concentration of 0.1 g per cubicmeter.')
"---"
columns = st.columns((1,1), gap = 'large')

#t1 = st.slider('Time max',60,86400,1800,60)
#c0 = st.slider('Mass input conc.',0.01,5.0,0.1,0.01)
#m  = st.slider('Mass input',0.0,1000.0,10.0,1.0)
#Q  = 0.2
l = 15
t1 = 1800
c0 = 0.1
m = 1000.0
Q= 0.2

with columns[0]:
    plot_A    = st.toggle('Plot Advection', True)
    plot_AD   = st.toggle('Plot Dispersion', False)
    plot_DATA = st.toggle('Show Measured data for calibration',False)
    if plot_DATA:
        l = 15
        st.write('D**Distance of observation from source** for the measured data is fixed to 15 m.')
    else:
        l  = st.slider(f'**Distance of observation from source (m)**',1,100,15,1)
    
with columns[1]:
    n  = st.slider(f'**Porosity (dimensionless)**',0.02,0.6,0.2,0.001)       
    a  = st.slider(f'**Longitudinal dispersivity (m)**',0.001,10.0,0.01,0.002)
"---"
# Data for plotting
t0 = 1      # Starting time
dt = 2      # Time discretization
r  = 2      # Column radius
ci = 0      # Initial concentration
cp = 2 * c0 # Pulse concentration
    
# Computation of intermediate results
A =     np.pi*r**2
q =     Q/A
v =     q/n
D =     a*v
PE =    l/a
dur =   m/(Q*(c0-ci))
tPV =   l/v
r_dur = dur/tPV
r_dt =  dt/tPV

# Defining time range
t = np.arange(t0, t1, dt)

# Computation of concentration (terms in brackets)
# Set fraction of distance
r_time = []
time   = []
conc   = []
conca  = []
   
#compute concentration  
for t in range(t0, t1, dt):      
    r_time = t/tPV
    
    # ADVECTION-DISPERSION
    c = ci*IC(PE,r_time)+c0*BC(PE,r_time, r_dur)
    conc.append(c)
    
    # Input pulse
    if r_time < 1:
        ca = 0
    elif r_time > 1+r_dur:
        ca = 0
    else:
        ca = c0
    
    conca.append(ca)
    
    time.append(t)
        
# measurements
t_obs = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
c_obs = [1e-3, 5e-2, 8.5e-2, 9.7e-2, 9.9e-2, 10e-2, 10e-2, 10e-2, 10e-2, 10e-2]
   
#PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
ax.set_title('1D solute transport with advection-dispersion', fontsize=16)
ax.set_xlabel ('Time (s)', fontsize=14)
ax.set_ylabel ('Concentration (g)', fontsize=14)
      
# PLOT HERE
if plot_A:
    ax.plot(time,conca, 'fuchsia', linewidth=2, label="Computed: (only) Advection")
if plot_AD:
    ax.plot(time,conc, 'navy', linewidth=2, label="Computed: Adcektion-Dispersion")
if plot_DATA == 1:
    ax.plot(t_obs, c_obs, 'ro', label="Measured")
#ax.scatter(t_obs, c_obs, marker="x", c="red", zorder=10)
plt.ylim(0, cp)
plt.xlim(0,t1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
#if not plot_A !=1 and plot_AD != 1 and plot_DATA != 1:
plt.legend(frameon=False, loc='upper right', fontsize=14)
    
st.pyplot(fig)