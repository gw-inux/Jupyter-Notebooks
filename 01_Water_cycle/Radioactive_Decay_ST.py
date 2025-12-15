import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import streamlit as st

# also Interactive Documents 05-06-001

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],
    "Rudolf Liedl": [1]    # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface

st.title('Mass balance for a decay chain')
st.header('Decay of Species A to B and species B to C', divider='green')

st.markdown("""The app demonstrate the mass balance for a decay chain""")
st.subheader('Example: Radioactive Decay', divider ='violet')

st.markdown(""" This illustrative example is not completely related to basic hydrogeology (although coupled decay processes are of some importance for contaminant transport in aquifers).""")
with st.expander('Click here to see the equations and example parameters'):
    st.markdown("""
         The facts:
        * Decay chain: $A \\to B \\to C$
        * decay rate of $A$ = production rate of $B$
        * decay rate of $B$ = production rate of $C$
        * $\\Delta M_A = R_A \\cdot M_A  \\cdot \\Delta t$
        * $\\Delta M_B = R_A \\cdot M_A  \\cdot \\Delta t - R_B \\cdot M_B  \\cdot \\Delta t $
        * $\\Delta M_C = R_B \\cdot M_B  \\cdot \\Delta t$
        
        ***Example:***
        
        * 30% of substance *A* and 20% of substance $B$  decay each year.
        * decay rate of $A$ = production rate of $B$ = 0.3 $a^{-1}$ x $M_A$.
        * decay rate of $B$ = production rate of $C$ = 0.2 $a^{-1}$ x $M_B$.
        
        ***Mass budgets for $A$, $B$, and $C$:***                         
        * $\\Delta M_A = 0.3 a^{-1} \\cdot M_A  \\cdot \Delta t$
        * $\\Delta M_B = 0.3 a^{-1} \\cdot M_A  \\cdot \Delta t - 0.2 a^{-1} \\cdot M_B  \\cdot \\Delta t$
        * $\\Delta M_C = 0.2 a^{-1} \\cdot M_B  \\cdot \Delta t$
          	
        Similar equations hold for quantitative descriptions of some chemical reactions which correspond to the type $A \\to B \\to C$.""")

st.subheader('Interactive plot of decay species A -> B and species B -> C', divider='rainbow')
#decay code
# Input value - you can modify here

columns = st.columns((1,1))

with columns[0]:
    with st.expander('Modify the **Initial Masses**'):
        A_0=st.slider(f'**Initial mass $A_0$ [kg]**:',0,1000,500,10)
        B_0=st.slider(f'**Initial mass $B_0$ [kg]:**',0,1000,0,10)
        C_0=st.slider(f'**Initial mass $C_0$ [kg]:**',0,1000,0,10)
    
with columns[1]:
    with st.expander('Modify the **Decay Rates**'):
        R_A=st.slider(f'**Decay rate of $A$: $R_A$ [1/a]**:',0.0,1.0,0.000,0.001)
        R_B=st.slider(f'**Decay rate of $B$: $R_B$ [1/a]**:',0.0,1.0,0.000,0.001)

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

fig = plt.figure(figsize=(7,5))
plt.plot(time, A, time, B, time, C, linewidth=3);  # plotting the results
plt.xlabel("Time [years]"); plt.ylabel("Mass [kg]") # placing axis labels
plt.legend(label, loc=0);plt.grid(); plt.xlim([0,n_simulation-1]); plt.ylim(bottom=0) # legends, grids, x,y limits

st.pyplot(fig)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')