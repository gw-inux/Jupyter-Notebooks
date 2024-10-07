import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import streamlit as st

#decay code
# Input value - you can modify here
    
A_0=st.slider('A_0:',0,1000,0,10)
B_0=st.slider('B_0:',0,1000,0,10)
C_0=st.slider('C_0:',0,1000,0,10)
R_A=st.slider('R_A:',0.0,1.0,0.000,0.001)
R_B=st.slider('R_B:',0.0,1.0,0.000,0.001)

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
d = {"Mass_A": A, "Mass_B": B, "Mass_C": C, "Total Mass": summ}
df = pd.DataFrame(d) # Generating result table
label = ["Mass A (g)", "Mass B (g)", "Mass C (g)"]
fig = plt.figure(figsize=(9,6))
plt.plot(time, A, time, B, time, C, linewidth=3);  # plotting the results
plt.xlabel("Time [Time Unit]"); plt.ylabel("Mass [g]") # placing axis labels
plt.legend(label, loc=0);plt.grid(); plt.xlim([0,n_simulation-1]); plt.ylim(bottom=0) # legends, grids, x,y limits

st.pyplot(fig)

df.round(2) #display result table with 2 decimal places 