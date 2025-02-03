# import librarys
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('Model for a Linear Reservoir')

st.latex('\Large V_i = V_{i-1} - Q_{i-1} \Delta t + R_i \Delta t ')
st.text('')
col0, col00 = st.columns(2)
with col0:
    st.image('FIGS/Linear_reservoir.png', caption= 'Figure 1: Model for a linear reservoir.')
with col00:
    st.write('$V$...Volume of stored water [$L³$]')
    st.write('$Q$...Discharge, runoff [$L³T^{-1}$]')
    st.write('$R$...Groundwater recharge [$L³T^{-1}$]')
    st.write('$i$...Timestep [$T$]')
    st.write('$\Delta t $...Difference between two timesteps [$T$]')

st.write('')
st.write('A way to quantify, how much water is stored and released from an aquifer is the **storage coefficient S**.')
st.write('By changing the values of the slider below the effect of different values for S can be observed.')
st.write('The groundwater recharge and initial stored water volume can as well be contolled by changing the slider values.')
st.write('')

# Interactive user input for the Parameters

## Storage coefficient
k = st.slider('Storage coefficient S', 0.0,1.0,0.1,0.1)
## Start and end of the inflow
col1, col2 = st.columns(2)
with col1:
    influx_start = st.slider('Start of recharge',0,50,10,1)
with col2:
    influx_end = st.slider('End of regarge',50,10,50,1)
## Inflow volume
col3, col4 = st.columns(2)
with col3:
    influx_v = st.slider('Recharge volume', 0,100,10,1)
## Initial stored Volume 
with col4:
    initial_v = st.slider('Water volume at the begin', 0,100,10,1)


def generate_data(k, influx_start, influx_end, influx_v, initial_v):
    '''
    input:
        k...Storage coefficient [1/t], type = int
        influx_vol...Inflow volume [L^3], type = int 
    --------------------------------------------------
    output:
        i...Timesteps, type = array
        O...Outflow [L/t], type = array
        V...Currently stored volume [L], type = array
        I...Inflow [L/t], type = array
    '''

    datalenght=100
    influx_time=[influx_start, influx_end]

    i = np.arange(datalenght)
    In = np.zeros_like(i, dtype=float)
    influx_start=influx_time[0]
    influx_end=influx_time[1]
    In[influx_start:influx_end] = influx_v
    V = np.zeros_like(i, dtype=float)
    V[0] = initial_v
    Out = np.zeros_like(i, dtype=float)
    
    for n in range(1, len(i)):
        Out[n-1] = V[n-1] * k
        V[n] = V[n-1] - Out[n-1] + In[n]
    
    return i, Out, V, In 


# creating a plot
    
i, Out, V, In = generate_data(k, influx_start, influx_end, influx_v, initial_v)

fig, ax1 = plt.subplots(figsize=(12,5)) 
ax1.plot(i, V, color = 'steelblue', label = 'V [L³]')
ax1.set_xlabel('Timesteps [T]')
ax1.set_ylabel('Storage volume [L]')
ax1.set_ylim(0,max(V)+10)
ax1.grid('True')
ax1.margins(x=0, y=0) 
ax1.spines['top'].set_visible(False) 

ax2 = ax1.twinx()
ax2.plot(i, In, color='skyblue', label = 'R [$L³T^{-1}$]')
ax2.plot(i, Out, color = 'navy', label = 'Q [$L³T^{-1}$]')
ax2.set_ylabel('Flow [$L³T^{-1}$]')
ax2.set_ylim(0,max(In)+10)
ax2.spines['top'].set_visible(False)

fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

st.pyplot(fig)