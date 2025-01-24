import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import streamlit as st

st.title('1D Transport with advection and dispersion')
st.subheader('Solute input as :orange[Finite Pulse] ', divider="orange")

st.markdown("""
            ### About the computed situation
            
            Transport is calculated for steady one-dimensional flow through a homogeneous porous medium in a 1 meter long laboratory column with a specific discharge _q_ of 0.0001 m/s.
            
            The average velocity _v_ depends on the porosity _n_ (_v_=_q_/_n_) which is printed above the graph.
            
            Solutes are injected on the left with a constant concentration _Co_ of 1000 g/m<sup>3</sup> (same as mg/L).
            
            The user specifies the mass _M_ that is input to the column. 
            
            The duration of the source is the mass divided by the rate of mass inflow, that is, Duration = _M_ / (_Co Q_) 
""", unsafe_allow_html=True
)           


st.markdown("""
            The graph shows the solute concentration at an observation point a user-defined distance from the source for both pure advective transport and for advective-dispersive transport.  
""", unsafe_allow_html=True
)
 
"---"

columns1 = st.columns((1,1,1), gap = 'large')
with columns1[1]:
    theory = st.button('Show Equation')
    
if theory:
	
    st.markdown("""
            For t less than or equal to the source duration:
    """, unsafe_allow_html=True
    )

    st.latex(r'''C(x,t) = \frac{Co}{ 2 }  \left( erfc \left( \frac{x - vt}{2 \sqrt{Dt}} \right) + exp \left(\frac{vx}{D} \right) erfc \left( \frac{x + vt}{2 \sqrt{Dt}} \right)\right) ''')

	
    st.markdown("""
            For t greater than the sourcce duration:
    """, unsafe_allow_html=True
    )

    st.latex(r'''C(x,t) = \frac{Co}{ 2 }  \left( erfc \left( \frac{x - vt}{2 \sqrt{Dt}} \right) + exp \left(\frac{vx}{D} \right) erfc \left( \frac{x + vt}{2 \sqrt{Dt}} \right)\right) ''')
    st.latex(r'''+ \frac{-Co}{ 2 }  \left( erfc \left( \frac{x - v(t-t_{dur})}{2 \sqrt{D (t-t_{dur})}} \right) + exp \left(\frac{vx}{D} \right) erfc \left( \frac{x + v(t-t_{dur})}{2 \sqrt{D(t-t_{dur})}} \right)\right)''')

    st.markdown(
    """
    - _C_ : concentration (grams/cubic meter)
    - _Co_ : initial concentration (grams/cubic meter)
    - _x_ : distance from the source (meters)
    - _v_ : average linear velocity = Ki/n (meters/second)
    - _t_ : time since the source was introduced (seconds)
    - _t<sub>dur</sub>_ : duration of the input pulse (seconds)
    - _D_ : dispersion coefficient - product of dispersivity and average linear velocity (square meters/second)

    """, unsafe_allow_html=True
)

columns1 = st.columns((1,1,1), gap = 'large')
columns1 = st.columns((1,1,1), gap = 'large')

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


columns = st.columns((1,1), gap = 'large')

l = 0.75
t1 = 20000
c0 = 1000
Q= 2.0268E-7

with columns[0]:
    plot_DATA = st.toggle('Show Measured data for calibration',False)
    if plot_DATA:
        l = 0.75
        st.write('**Distance of observation from source is 0.75 m for the measured data**')
        st.write('**Calibration is the process of adjusting parameter values until the model matches the data**')
        st.write('**After calibrating to the data, you can check your values using the button below the graph**')
    else:
        l  = st.slider(f'**Distance of observation from source (m)**',0.01,1.0,0.5,0.01)
    
with columns[1]:
    m = st.slider(f'**Input mass (grams)**',0.01,1.,0.1,0.01) 
    n  = st.slider(f'**Porosity (dimensionless)**',0.01,0.6,0.2,0.01)       
    a  = st.slider(f'**Longitudinal dispersivity (m)**',0.001,0.1,0.01,0.001, format="%e")
"---"
# Data for plotting
t0 = 1      # Starting time
dt = 1      # Time discretization
r  = 0.0254      # Column radius
ci = 0      # Initial concentration
    
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
t = np.arange(t0, t1+1, dt)

# Computation of concentration (terms in brackets)
# Set fraction of distance
r_time = []
time   = []
conc   = []
conca  = []
   
#compute concentration
for t in range(t0, t1+1, dt):      
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
t_obs = [1000,	1250,	1500,	1750,	2000,	2250,	2500,	2750,	3000,	3250,	3500,	3750,	4000,	4250,	4500,	4750,	5000,	5250,	5500,	5750,	6000,	6250]
c_obs = [16.08,	69.12,	168.85,	300.32,	440.37,	570.62,	681.23,	769.41,	836.55,	884.15,	901.09,	866.78,	778.96,	656.93,	525.37,	402.76,	298.71,	215.88,	152.87,	106.53,	73.29,	49.90]

#compute concentration profile
for t in range(t0, t1+1, dt):      
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

#PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
ax.set_title('1D solute transport with advection-dispersion', fontsize=16)
ax.set_xlabel ('Time (s)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)

# PLOT HERE
ax.plot(time,conca, 'fuchsia', linewidth=2, label="Computed: ONLY Advection")
ax.plot(time,conc, 'navy', linewidth=2, label="Computed: Advection-Dispersion")
if plot_DATA == 1:
    ax.plot(t_obs, c_obs, 'ro', label="Measured")
plt.ylim(0, 1.05*1000)
plt.xlim(0,t1-1)
plt.xticks(np.arange(0, 20001, 2500),fontsize=14)
plt.yticks(fontsize=14)
legend = plt.legend(loc='upper right', fontsize=14, framealpha=0.8)
legend.get_frame().set_linewidth(0.0)

st.write("Average velocity (m/s) = ","% 7.3E"% v)
st.write("Source Duration (s) = ","% 7.3E"% dur)
    
st.pyplot(fig)

if plot_DATA:
    columns1 = st.columns((1,1,1), gap = 'large')
    with columns1[1]:
        calib = st.button('Show input values that will generate observed calibration data')
    
    if calib:
	
        st.markdown("""
        - mass : 0.5 grams
        - porosity : 0.3
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
        """
)
st.markdown(
    """
        :green[Please help us by using the following link when sharing this tool with others.]
        """   
)

st.markdown(
    """
        https://interactive-education.gw-project.org/1D_conservative_transport/
        """   
)

