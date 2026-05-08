# Necessary libraries
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.ticker import MaxNLocator
import numpy as np
from numpy import nan as NaN
from IPython.display import display
import pandas as pd
from IPython.display import clear_output
import math
import streamlit as st
from streamlit_extras.stateful_button import button


# also Interactive Documents 08-02-002
# ToDo:
#    - number input

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface
st.title('Finite-Difference Numerical scheme: *Solver options*')
st.subheader('1D groundwater flow in a confined aquifer with uniform recharge *and different solver options*', divider='green')

st.markdown("""
            ### Introduction and Motivation
            Groundwater models are useful tools to evaluate groundwater systems. This app demonstrate a simple 1D numerical scheme to simulate groundwater flow in a 1D confined aquifer that is bounded by two specified head boundaries. :green[**In addition**], the app allows to investigate three different solution schemes:
            * Jacobi,
            * Gauss-Seidel, and
            * Successive Over-Relaxation (SOR).
           """)

lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('FIGS/GWF_1D_FD.png', caption="Schematic representation of the conceptual model and the numerical representation.")
    
with st.expander(":green[**Click here**] to read more about the different solution schemes"):
    st.markdown("""
    #### Jacobi iteration
    
    All cells are updated using only values from the previous iteration (*old*). This makes the method simple and robust, but convergence is typically slow.
    
    $$
    h_i = \\frac{h_{i-1}^{old} + h_{i+1}^{old}}{2}  + \\frac{R_i}{2T}\Delta x^2
    $$

    #### Gauss-Seidel iteration
    Updated values are used immediately within the same iteration (left neighbor updated, right still *old*). This accelerates convergence compared to Jacobi.

    $$
    h_i = \\frac{h_{i-1} + h_{i+1}^{old}}{2}  + \\frac{R_i}{2T}\Delta x^2
    $$    
    
    
    #### Successive Over-Relaxation (SOR) iteration
    The Gauss–Seidel update is relaxed using a factor $\omega$, combining the previous value with the new estimate.
    
    $$
    h_i = (1-\omega)h_i^{old} + \omega (\\frac{h_{i-1} + h_{i+1}^{old}}{2}  + \\frac{R_i}{2T}\Delta x^2)
    $$
    
    """)

st.subheader('Input values', divider = 'green')

st.markdown('''
            Below you can insert and modify the input parameter for the groundwater flow scenario and the numerical solution. Thereafter, you can start the simulation with the button _Run Simulation_. The results in the plot show the computed heads for the discrete cells (blue dots).
            ''')

# Data input
log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1
column = st.columns((1,1,1))
with column[0]:
    with st.expander('**Parameter for the scenario**'):
        m       = st.slider('Aquifer thickness (in m)', 1, 200, 20, 1)
        BC_L    = st.number_input('Left boundary head (in m)', 0.1, 500., 18., 0.1)
        BC_R    = st.number_input('Right boundary head (in m)', 0.1, 500., 16., 0.1)
        RCH_IN  = st.slider('Recharge (in mm/a)', 0, 500, 200, 1)
        container = st.container()
        K_slider_value=st.slider('_(log of) **hydraulic conductivity_ in m/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        K = 10 ** K_slider_value
        # Display the logarithmic value
        container.write("**Hydraulic conductivity** in m/s: %5.2e" %K)
with column[1]:
    with st.expander('**Spatial discretization**'):
        cells   = st.number_input('Number of cells', 3, 101, 11, 1)
        dx      = st.number_input('Spatial increment dx (in m)',1,1000,500,1) 
with column[2]:
    with st.expander('**Parameter for the numerical solution**'):  
        st.session_state.scheme  = st.radio("Iterative solver", ["Jacobi", "Gauss-Seidel", "SOR"], index=0)
        # SOR relaxation factor
        if st.session_state.scheme == "SOR":
            st.session_state.omega = st.slider("SOR relaxation factor $\omega$", min_value=0.1, max_value=3.00, value=1.2, step=0.05, help="$\omega$ = 1 is Gauss–Seidel. Typical useful range: 1.0–1.8.")
        else:
            st.session_state.omega = 1.0
        st.session_state.i_max   = st.number_input('Max number of iterations', 5, 500, 50, 1)    
        st.session_state.epsilon = st.number_input('Closure criteria $\epsilon$ (in m)', 0.000001, 10., 0.001, 0.001, format="%0.6f")  

st.session_state.analytic = st.toggle("Show analytic solution", help="Press here to plot the analytical solution for comparison") 
    
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
st.session_state.h_ini = h.copy()
        
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
# Solver label for info box
if st.session_state.scheme == "SOR":
    scheme_txt = rf'Scheme = SOR ($\omega$ = {st.session_state.omega:.2f})'
else:
    scheme_txt = rf'Scheme = {st.session_state.scheme}'
props   = dict(boxstyle='round', facecolor='palegreen', alpha=0.5)
out_txt = '\n'.join((
                         scheme_txt,
                         r'$i = %i$' % (i, ),
                         r'$i_{max} = %i$' % (st.session_state.i_max, ),
                         r'$eps = %.2e$' % (st.session_state.epsilon, )))   
fig = plt.figure(figsize=(10,7))
ax1 = fig.add_subplot(1, 1, 1)
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2 = ax1.twiny() 
ax1.plot(h, '--o')
plt.ylim(h_min-h_range,ymax)
ax1.set_xlabel('Index cells (starting with 0)', fontsize=14)  
ax2.set_xlabel('Distance in m', fontsize=14)    
plt.ylabel('Hydraulic head (m)',fontsize=14)
plt.title('Finite Difference computation for 1D GW flow, confined / homogeneous', fontsize=16)
ax1.set_xlim(0,cells-1)      # Primäre X-Achse
ax2.set_xlim(0,L)            # Sekundäre X-Achse
plt.text(0.97, 0.95,out_txt,transform=ax1.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=props)
if st.session_state.analytic:
    ax2.plot(xa,st.session_state.ha,'g')
        
with empty.container():
   st.pyplot(fig)

# Run iterations

@st.fragment
def computation():
    
    lc2, mc2, rc2 = st.columns([1,1,1])
    with mc2:
        run = st.button("**:blue[Run the computation]**", help="Press here to start the iteration")
    
    i = 0
    convergence = False

    if run:
        h = st.session_state.h_ini.copy()
        st.session_state.h_old = h.copy()
        
        while i < st.session_state.i_max:
            # Increase iteration count
            i = i + 1       
            
            # Compute heads and head change
            
            if st.session_state.scheme == "Jacobi":
                for x in range(1, cells-1):
                    h[x] = 0.5*(st.session_state.h_old[x-1]+st.session_state.h_old[x+1]+st.session_state.R[x]/T*dx**2)               
            
            elif st.session_state.scheme in ["Gauss-Seidel", "SOR"]:
                for x in range(1, cells-1):
                    # Gauss–Seidel candidate (uses newest left neighbor)
                    h_gs = 0.5 * (h[x-1] + st.session_state.h_old[x+1] + st.session_state.R[x]/T * dx**2)
            
                    if st.session_state.scheme == "Gauss-Seidel":
                        h[x] = h_gs
                    else:
                        # SOR blend
                        h[x] = (1.0 - st.session_state.omega) * st.session_state.h_old[x] + st.session_state.omega * h_gs
            
            head_change = [(abs(h[x] - st.session_state.h_old[x])) for x in range(1, cells-1)]
            max_head_change = max(head_change)

            # Save the current results
            st.session_state.h_old = h.copy()
        
            # Check closure criterion
            if(max_head_change <= st.session_state.epsilon):       # stop iteration
                convergence = True
        
            # Generate figure
            # Info-Box
            # Solver label for info box
            if st.session_state.scheme == "SOR":
                scheme_txt = rf'Scheme = SOR ($\omega$ = {st.session_state.omega:.2f})'
            else:
                scheme_txt = rf'Scheme = {st.session_state.scheme}'
                
            props   = dict(boxstyle='round', facecolor='palegreen', alpha=0.5)
            out_txt = '\n'.join((
                                     scheme_txt,
                                     r'$i = %i$' % (i, ),
                                     r'$i_{max} = %i$' % (st.session_state.i_max, ),
                                     r'$dh_{max} = %.6f$' % (max_head_change, )))   
            fig = plt.figure(figsize=(10,7))
            ax1 = fig.add_subplot(1, 1, 1)
            ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax2 = ax1.twiny()
            ax1.set_xlabel('Index cells (starting with 0)', fontsize=14)  
            ax2.set_xlabel('Distance in m', fontsize=14)             
            plt.ylabel('Hydraulic head (m)',fontsize=14)
            plt.title('Finite Difference computation for 1D GW flow, confined / homogeneous', fontsize=16)
            ax1.plot(h, '--o')
            plt.ylim(h_min-h_range,ymax)
            ax1.set_xlim(0,cells-1)      # Primäre X-Achse
            ax2.set_xlim(0,L)            # Sekundäre X-Achse
            plt.text(0.97, 0.95,out_txt,transform=ax1.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=props)
            if st.session_state.analytic:
                ax2.plot(xa,st.session_state.ha,'g')
        
            with empty.container():
               st.pyplot(fig)
                               
# Abbruchkriterium der Iterationsschleife
            if convergence:       # Abbruch der Iteration
                st.write(':green[Convergence achieved]')
                break
        
    # If no convergence
    if convergence == False:        
        st.write(':red[NO CONVERGENCE YET]')

computation()

st.markdown('---')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')