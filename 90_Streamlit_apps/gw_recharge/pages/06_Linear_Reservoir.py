import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Page intro
st.subheader(':blue-background[Model for a Linear Reservoir]', divider="blue")

st.latex('\Large V_i = V_{i-1} - Q_{i-1} \Delta t + R_i \Delta t ')
st.text('')
col0, col00 = st.columns(2)
with col0:
    st.image('90_Streamlit_apps\gw_recharge\images\Linear_reservoir.png', caption= 'Figure 1: Model for a linear reservoir.')
with col00:
    st.write('$V$...Volume of stored water [$L³$]')
    st.write('$Q$...Discharge, runoff [$L³T^{-1}$]')
    st.write('$R$...Groundwater recharge [$L³T^{-1}$]')
    st.write('$i$...Timestep [$T$]')
    st.write('$\Delta t $...Difference between two timesteps [$T$]')

st.write('')
st.write('A way to quantify, how much water is stored and released from an aquifer is the **recession coefficient S**.')
st.write('By changing the values of the slider below the effect of different values for S can be observed.')
st.write('The groundwater recharge and initial stored water volume can as well be controlled by changing the slider values.')
st.write('')

st.subheader(':blue-background[Model for a Linear Reservoir]', divider="blue")
# Interactive user input for the Parameters

## Storage coefficient
col1, col2= st.columns(2)
with col1:
    k = st.slider('Recession coefficient S', 0.0,1.0,0.1,0.01)
with col2:
    initial_vol = st.slider('Initially stored water',0,100,10,1)


# Irrigaion Exercice
#
# st.pills to select the ETP
ETA_options=['Oudin', 'Haude', 'Penman-Monteith']
ETA_selection=st.radio('Select with which ETP data you want to continue:', ETA_options, horizontal=True, )
# load data from ETP_data.csv
if ETA_selection=='Oudin':
    ETA=st.session_state.ETA.Oudin
    gw_recharge=st.session_state.gw_recharge.Oudin
elif ETA_selection=='Haude':
    ETA=st.session_state.ETA.Haude
    gw_recharge=st.session_state.gw_recharge.Haude
else:
    ETA=st.session_state.ETA.PM
    gw_recharge=st.session_state.gw_recharge.PM

data = st.session_state.data
precip = data['precip']

# Non irrigated Budget
In=gw_recharge
Out=np.zeros_like(In, dtype=float)
V=np.zeros_like(In, dtype=float)
V[0]=initial_vol
for i in range(1, len(In)):
        Out[i-1] = V[i-1] * k
        V[i] = V[i-1] - Out[i-1] + In[i]

# ploting the data
fig, ax1 = plt.subplots(figsize=(12,5)) 
ax1.plot(st.session_state.data.index, V, color = 'steelblue', label = 'V [L³]')
ax1.set_xlabel('Date')
ax1.set_ylabel('Storage volume [L]')
ax1.set_ylim(0,max(V)+10)
ax1.grid('True')
ax1.margins(x=0, y=0) 
ax1.spines['top'].set_visible(False) 

ax2 = ax1.twinx()
ax2.bar(st.session_state.data.index, In, color='skyblue', label = 'R [$L³T^{-1}$]')
ax2.plot(st.session_state.data.index, Out, color = 'navy', label = 'Q [$L³T^{-1}$]')
ax2.set_ylabel('Flow [$L³T^{-1}$]')
ax2.set_ylim(0,max(In)+10)
ax2.spines['top'].set_visible(False)

fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
st.pyplot(fig)

columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\05_Groundwater_Recharge.py")
with columnsN1[1]:
    st.subheader(':blue[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\07_About.py")
