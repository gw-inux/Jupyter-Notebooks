import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import streamlit as st

st.title('Mass balance for a decay chain')

st.subheader('***Decay of Species A to B and species B to C***')

st.write('The app demonstrate the mass balance for a decay chain')

st.header('Example: Radioactive Decay')

st.write('This illustrative example is not completely related to basic hydrogeology (although coupled decay processes are of some importance for contaminant transport in aquifers). The facts:')

st.markdown('+ Decay chain:')
st.latex(r''' A \to B \to C''')                                                                
st.markdown('+ 30% of substance *A* and 20% of substance *B*  decay each year.')
st.markdown('+ decay rate of *A* = production rate of *B* = 0.3 a^-1 x M_A')
st.markdown('+ decay rate of *B* = production rate of *C* = 0.2 a^-1 x M_B')
st.markdown('+ mass budgets for *A*, *B*, and *C*:')                             
st.latex(r''' \Delta M_A = 0.3 a^{-1} \cdot M_A  \cdot \Delta t''')
st.latex(r''' \Delta M_B = 0.3 a^{-1} \cdot M_A  \cdot \Delta t - 0.2 a^{-1} \cdot M_B  \cdot \Delta t ''')
st.latex(r''' \Delta M_C = 0.2 a^{-1} \cdot M_B  \cdot \Delta t''')
  	
st.markdown('+ Similar equations hold for quantitative descriptions of some chemical reactions which correspond to the type A -> B -> C')
"---"
st.subheader('Interactive plot of decay species A -> B and species B -> C')
#decay code
# Input value - you can modify here

columns = st.columns((1,1), gap = 'large')

with columns[0]:
    A_0=st.slider(f'**Initial mass _A_0_ [kg]**:',0,1000,0,10)
    B_0=st.slider(f'**Initial mass _B_0_ [kg]:**',0,1000,0,10)
    C_0=st.slider(f'**Initial mass _C_0_ [kg]:**',0,1000,0,10)
    
with columns[1]:
    R_A=st.slider(f'**Decay rate of A - _R_A_ [1/a]**:',0.0,1.0,0.000,0.001)
    R_B=st.slider(f'**Decay rate of A - _R_B_ [1/a]**:',0.0,1.0,0.000,0.001)

n_simulation = 101 # this number denotes how many discrete values (times) are computed - similar to the number of cells / rows in an Excel-sheet

time  = np.arange(n_simulation) # simulation time = number of simulation values at 1 (time unit) interval, in the example, the time unit is years

#initialization (fill all cells with zero)
A = np.zeros(n_simulation)
B = np.zeros(n_simulation)
C = np.zeros(n_simulation)

#The first value in the computation is the given initial value (please note that Python start counting by 0 i.e. A[0] is the first cell, A[1] is the second cell etc.)
A[0] = A_0 
B[0] = B_0
C[0] = C_0

# computation by a counting loop
for i in range(0,n_simulation-1):
    A[i+1] = A[i]-R_A*A[i]
    B[i+1] = B[i]+R_A*A[i]-R_B*B[i] 
    C[i+1] = C[i]+R_B*B[i]
    summ = A[i]+B[i]+C[i]  

# Output of results
label = ["mass A (kg)", "mass B (kg)", "mass C (kg)"]

fig = plt.figure(figsize=(9,6))
plt.plot(time, A, time, B, time, C, linewidth=3);  # plotting the results
plt.xlabel("Time [years]"); plt.ylabel("Mass [kg]") # placing axis labels
plt.legend(label, loc=0);plt.grid(); plt.xlim([0,n_simulation-1]); plt.ylim(bottom=0) # legends, grids, x,y limits

st.pyplot(fig)