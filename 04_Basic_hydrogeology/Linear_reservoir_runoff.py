# import librarys
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('Runoff for a linear Reservoir')
st.write('description')

# Interactive user input for the Parameters

## Storage coefficient
col1, col2 = st.columns(2)
with col1:
    k = st.slider('storage coefficient', 0.0,1.0,0.1,0.01)
## Initial stored Volume 
with col2:
    initial_v = st.slider('stored volume', 0,100,10,1)
## Scaling for the y-axis
ax_scale = st.radio('Scaling of the y-axis',['linear', 'log'])

# calculate the Outflow for a linear reservoir without inflow
t = np.arange(100-1)
V = np.zeros_like(t, dtype=float)
V[0] = initial_v
Out = np.zeros_like(t, dtype=float)
for n in range (1, len(t)):
    Out[n-1]=V[n-1]*k
    V[n] = V[n-1] - Out[n-1] 

Out0 = float(Out[0])
t_a = (np.linspace(0, 100, 10000))
Out_a = Out0 * np.exp(-k*t_a)
   
# plot the data
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(t, Out, 'r+', label='iterativ solution')
ax.plot(t_a, Out_a, label='analytic solution')
ax.set_ylabel('Outflow [L^3/t]')
ax.set_xlabel('time [t]')
ax.legend()
ax.grid(which='major')
ax.grid(which='minor')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.yscale(ax_scale)
st.pyplot(fig)
