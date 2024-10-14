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

st.title('1D FLOW - Finite-Difference Numerical scheme')

# Data input

cells   = 11
dx      = 500                  
K       = 0.001
m       = 20
RCH_IN  = 100
BC_L    = 18
BC_R    = 16
analytisch = st.toggle('Analytical solution') 
epsilon = 50
i_max   = 30   
run = st.toggle('Run computation') 

start = True       # Marks the first run
konvergenz = False
    
# Länge der x-Achse (Achtung, das numerische Verfahren ist Knotenzentriert, d. h. x = 0 in der Mitte der ersten Zelle)
L = (cells-1) * dx
    
# Transmissivität = Konstant in der Variante homogen / gespannt
T = K * m
    
# Recharge (GWN) and initial head (h)
R =   [RCH_IN for x in range(cells)]        # Initialisieren von h und RCH (Anfangswasserstand und Grundwasserneubilung)
h =   [(BC_R+BC_L)/2 for x in range(cells)] # Anfangswasserstand = Mittel beider Randbedingungen
R_out = [0 for x in range(cells)]           # Ausgabeformat
h_out = [0 for x in range(cells)]           # Ausgabeformat
        
# Recharge in m/s 
for x in range(0, cells):
    R[x] = R[x]/1000/24/3600/365.25
    R_out[x] = "%7.1e"% (R[x])
    
# Boundary conditions (defined head)
h[0]  = BC_L
h[-1] = BC_R
h_old = h.copy()
        
# Maximaler / Minimaler Anfangswasserstand für Skalierung der Abbildung
h_max = max(h)
h_min = min(h)
h_range = (h_max-h_min)
    
# Analytical solution
xa = np.arange(0, L,L/((cells-1)*dx))
N  = RCH_IN/1000/365.25/86400
ha = N/(2*T)*(L*xa-xa**2)+((BC_R-BC_L)/L)*xa+BC_L
ymax = math.ceil(max(ha)*1.1)
        
# Print starting values
#with startwerte():
#    if start:
#        clear_output(wait=True)
#        print('\n')
#        print('Recharge [m/s]')
#        print('RCH  :', R_out)
#        print('\n')
#        print('Initial head')
#        for x in range(0, cells):
#            h_out[x] = "%6.2f"% (h[x])
#        print('h_ini: ', h_out)
#        start = False

# Run iterations
i = 0
     
while i < i_max:

    if run:
        # Increase iteration count
        i = i + 1
            
        # Compute the FD equation
        for x in range(1, (cells-1)):
            h[x] = 0.5*(h_old[x-1]+h_old[x+1]+R[x]/T*dx**2)               
           
    # Potentialänderung der Iteration ermitteln
    head_change = [(abs(h[x] - h_old[x])) for x in range(1, cells-1)]
    max_head_change = max(head_change)

    # Save the current results
    h_old = h.copy()
        
    # Check closure criterion
    if(max_head_change <= epsilon):       # stop iteration
         konvergenz = True
        
    # Generate figure
    #with out_plot:
    #    # Info-Box
    #    props   = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    #    out_txt = '\n'.join((
    #                            r'$i = %i$' % (i, ),
    #                            r'$i_{max} = %i$' % (i_max, ),
    #                            r'$dh_{max} = %.4f$' % (max_head_change, )))
    #    clear_output(wait=True)
            
    fig = plt.figure(figsize=(10,7))
            
    if analytisch:
        # Plot initieren
        #fig = plt.figure(figsize=(10,7))
        ax1 = fig.add_subplot(1, 1, 1)
        ax2 = ax1.twiny() 
            
        # Daten zum Plot
        ax1.set(xlabel='Index cells (starting with 0)', ylabel='Hydraulic head (m)',title='1D GW flow, confined / homogeneous')
        ax2.set(xlabel='Distance (x-axis) in m')
        ax1.plot(h, '--o')
        ax2.plot(xa,ha,'g')
            
        #Achsen / Datenbereich definieren
        plt.ylim(h_min-h_range,ymax)
        ax1.set_xlim(0,cells-1)      # Primäre X-Achse
        ax2.set_xlim(0,L)            # Sekundäre X-Achse
            
        #Info-Box einfügen
        #plt.text(0.75, 0.95,out_txt,transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    else:
        # Plot initieren
        #fig = plt.figure(figsize=(10,7))
        ax1 = fig.add_subplot(1, 1, 1)
        ax2 = ax1.twiny() 
            
        # Daten zum Plot
        ax1.set(xlabel='Index cells (starting with 0)', ylabel='Hydraulic head (m)',title='1D GW flow, confined / homogeneous')
        ax2.set(xlabel='Distance (x-axis) in m')
        ax1.plot(h, '--o')
        
        #Achsen / Datenbereich definieren
        plt.ylim(h_min-h_range,ymax)
        ax1.set_xlim(0,cells-1)      # Primäre X-Achse
        ax2.set_xlim(0,L)            # Sekundäre X-Achse
               
        #Info-Box einfügen
        #plt.text(0.75, 0.95,out_txt,transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            
        st.pyplot(fig)
            
    # Textausgabe zum Stand der Berechnung
    #with endwerte:
    #    clear_output(wait=True)
    #    for x in range(0, cells):
    #        h_out[x] = "%6.2f"% (h[x])
    #    print('Computed head')
    #    print('h:     ', h_out)
    #    print('\n')
    if konvergenz:
        print('Convergence achieved')   
    else:
         print('! NO CONVERGENCE !')
                    
# Abbruchkriterium der Iterationsschleife
    if konvergenz:       # Abbruch der Iteration
        break
