# Necessary libraries
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
from numpy import nan as NaN
from IPython.display import display
import pandas as pd
from IPython.display import clear_output
import math
import streamlit as st

st.title('Finite-Difference Numerical scheme')
st.subheader('1D groundwater flow in a confined aquifer with uniform recharge', divider='blue')

st.subheader('Input values')

st.markdown('''
            Below you can insert and modify the input parameter for the groundwater flow scenario and the numerical solution. Thereafter, you can start the simulation with the button _Run Simulation_
            ''')

# Data input
log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1
column = st.columns((1,1), gap = 'large')
with column[0]:
    st.write('**Parameter for the scenario**')
    m       = st.slider('Aquifer thickness (in m)', 1, 200, 20, 1)
    BC_L    = st.number_input('Left boundary head (in m)', 0.1, 500., 18., 0.1)
    BC_R    = st.number_input('Right boundary head (in m)', 0.1, 500., 16., 0.1)
    RCH_IN  = st.slider('Recharge (in mm/a)', 0, 500, 200, 1)
    K_slider_value=st.slider('(log of) **hydraulic conductivity** in m/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_hydraulic conductivity_ in m/s: %5.2e" %K)
with column[1]:
    st.write('**Parameter for the numerical solution**')
    cells   = st.number_input('Number of cells', 3, 100, 11, 1)
    dx      = st.number_input('Spatial increment dx (in m)',1,1000,500,1)   
    st.session_state.i_max   = st.number_input('Max number of iterations', 5, 500, 50, 1)    
    st.session_state.epsilon = st.number_input('Closure criteria (in m)', 0.00001, 10., 0.001, 0.00001, format="%0.4f")
    st.session_state.analytic = st.toggle("Show analytic solution", help="Press here to start the iteration with the analytic solution")    

i = 0
run = False

    
# Länge der x-Achse (Achtung, das numerische Verfahren ist Knotenzentriert, d. h. x = 0 in der Mitte der ersten Zelle)
L = (cells-1) * dx
    
# Transmissivität = Konstant in der Variante homogen / gespannt
T = K * m
    
# Recharge (GWN) and initial head (h)
st.session_state.R =   [RCH_IN for x in range(cells)]        # Initialisieren von h und RCH (Anfangswasserstand und Grundwasserneubilung)
h =   [(BC_R+BC_L)/2 for x in range(cells)] # Anfangswasserstand = Mittel beider Randbedingungen
R_out = [0 for x in range(cells)]           # Ausgabeformat
h_out = [0 for x in range(cells)]           # Ausgabeformat
        
# Recharge in m/s 
for x in range(0, cells):
    st.session_state.R[x] = st.session_state.R[x]/1000/24/3600/365.25
    R_out[x] = "%7.1e"% (st.session_state.R[x])
RA = RCH_IN/1000/24/3600/365.25
    
# Boundary conditions (defined head)
h[0]  = BC_L
h[-1] = BC_R
st.session_state.h_old = h.copy()
        
# Maximaler / Minimaler Anfangswasserstand für Skalierung der Abbildung
h_max = max(h)
h_min = min(h)
h_range = (h_max-h_min)
    
# Analytical solution
xa = np.arange(0, L,L/((cells-1)*dx))
st.session_state.ha = RA/(2*T)*(L*xa-xa**2)+((BC_R-BC_L)/L)*xa+BC_L
ymax = math.ceil(max(st.session_state.ha)*1.1)

# Generate empty container for plot
empty = st.empty()

# Generate the initial figure
# Info-Box
props   = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
out_txt = '\n'.join((
                         r'$i = %i$' % (i, ),
                         r'$i_{max} = %i$' % (st.session_state.i_max, ),
                         r'$eps = %.4f$' % (st.session_state.epsilon, )))   
fig = plt.figure(figsize=(10,7))
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twiny() 
ax1.set(xlabel='Index cells (starting with 0)', ylabel='Hydraulic head (m)',title='1D GW flow, confined / homogeneous')
ax2.set(xlabel='Distance (x-axis) in m')
ax1.plot(h, '--o')
plt.ylim(h_min-h_range,ymax)
ax1.set_xlim(0,cells-1)      # Primäre X-Achse
ax2.set_xlim(0,L)            # Sekundäre X-Achse
plt.text(0.75, 0.95,out_txt,transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)
if st.session_state.analytic:
    ax2.plot(xa,st.session_state.ha,'g')
        
with empty.container():
   st.pyplot(fig)

# Run iterations

@st.fragment
def computation():
    run = st.button("Run the computation", help="Press here to start the iteration")
    i = 0
    convergence = False
    if run:
        while i < st.session_state.i_max:
            # Increase iteration count
            i = i + 1       
            
            # Compute heads and head change
            for x in range(1, (cells-1)):
                h[x] = 0.5*(st.session_state.h_old[x-1]+st.session_state.h_old[x+1]+st.session_state.R[x]/T*dx**2)               
            head_change = [(abs(h[x] - st.session_state.h_old[x])) for x in range(1, cells-1)]
            max_head_change = max(head_change)

            # Save the current results
            st.session_state.h_old = h.copy()
        
            # Check closure criterion
            if(max_head_change <= st.session_state.epsilon):       # stop iteration
                convergence = True
        
            # Generate figure
            # Info-Box
            props   = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            out_txt = '\n'.join((
                                     r'$i = %i$' % (i, ),
                                     r'$i_{max} = %i$' % (st.session_state.i_max, ),
                                     r'$dh_{max} = %.4f$' % (max_head_change, )))   
            fig = plt.figure(figsize=(10,7))
            ax1 = fig.add_subplot(1, 1, 1)
            ax2 = ax1.twiny() 
            ax1.set(xlabel='Index cells (starting with 0)', ylabel='Hydraulic head (m)',title='1D GW flow, confined / homogeneous')
            ax2.set(xlabel='Distance (x-axis) in m')
            ax1.plot(h, '--o')
            plt.ylim(h_min-h_range,ymax)
            ax1.set_xlim(0,cells-1)      # Primäre X-Achse
            ax2.set_xlim(0,L)            # Sekundäre X-Achse
            plt.text(0.75, 0.95,out_txt,transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            if st.session_state.analytic:
                ax2.plot(xa,st.session_state.ha,'g')
        
            with empty.container():
               st.pyplot(fig)
                               
# Abbruchkriterium der Iterationsschleife
            if convergence:       # Abbruch der Iteration
                st.write('Convergence achieved')
                break
        
    # If no convergence
    if convergence == False:        
        st.write('NO CONVERGENCE YET')

computation()