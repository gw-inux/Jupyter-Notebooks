# import librarys
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


st.title('Runoff from a linear Reservoir')
st.write('')

c1, c2 = st.columns(2)
with c1:
    st.write(r'$Q = S V $')
    st.write(r'$ Q = - \frac{dV}{dt}$')
    st.write('')
    st.write(r'$\frac{dV}{dt} = -S V $')
    st.write(r'$\frac{dV}{d} = - S dt$')
    st.write(r'$\int \frac{dV}{V} = - \int S dt$')
    st.write('$ln V = -S t + ln V_0$')
    st.write('')
    st.write('$V = V_0 e^{-St}$, where $ V_0 = V_{t=0}$')
    st.write('$Q = Q_0 e^{-St}$, where $Q_0 = Q_{t=0}$')
with c2:
    st.image('FIGS\Linear_reservoir_runoff.png', caption= 'Figure 1: Runoff model for a linear reservoir.')
st.write('')
st.write('Where: $V$...Volume of stored water [$L³$], $Q$...Discharge, runoff [$L³T^{-1}$], $S$...Storage coefficient')
st.write('')

# Interactive user input for the Parameters

## Storage coefficient
col1, col2 = st.columns(2)
with col1:
    k = st.slider('Storage coefficient S', 0.0,.5,0.1,0.01)
## Initial stored Volume 
with col2:
    initial_v = st.slider('Stored volume V', 0,100,10,1)
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
ax.plot(t, Out, 'r+', label='iterative solution')
ax.plot(t_a, Out_a, label='analytic solution')
ax.set_ylabel(r'Runoff [$\frac{L^3}{T}$]')
ax.set_xlabel('Time [T]')
ax.legend()
ax.grid(which='major')
ax.grid(which='minor')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.yscale(ax_scale)
st.pyplot(fig)
