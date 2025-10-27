import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.special import erfc
from datetime import datetime

st.set_page_config(page_title = "iNUX - Transient 1D Flow")
# Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Grießer": [1],
}
institutions = {
    1: "Institute of Earth Sciences, University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title('Transient one-dimensional flow - hydraulic head response to stream flood')
with st.expander('See explanation'):
    st.write('''
        If an aquifer hydraulically interacts with a river or stream, surface water floods will propagate into the aquifer.
        In the following, we look at a semi-infinite confined aquifer, i.e. a confined aquifer that interacts with a fully penetrating river on one side and has no boundary on the other side (Figure 1).
        This situation can be described by the following one-dimensional groundwater flow equation (assuming a homogeneous aquifer without sinks or sources, e.g. no recharge from precipitation):\n\n''')
    st.write('$$\\frac{\\partial² h}{\\partial x²} = \\frac {S \\partial h}{T \\partial t}$$\n\n')
    st.write('''where $h$ is hydraulic head, $x$ is distance from the surface water, $S$ is storage coefficient (storativity),
              $T$ is transmissivity, and $t$ is time.\n We assume the aquifer is initially in equlibrium with the surface water at $h = 0$,
              i.e. the hydraulic heads of the aquifer are initally equal to the surface water level, which is described by the following initial condition:\n\n''')
    st.write('$$h(x,t=0)=0$$ \n\n')
    st.write('At $t = 0$ the surface water level and thus the hydraulic head at $x = 0$ is subject to a sudden rise to $h_0$, which is described by the boundary condition:\n\n')
    st.write('$$h(0,t>0) = h_0$$\n\n')
    st.write('The solution of the above flow equation for the given intial and boundary conditions is\n\n')
    st.write('$$h(x,t)=h_0 \\: \\mathrm{ erfc}\\left(\\sqrt{\\frac{S x^2}{4T (t)}}\\right)$$\n\n')
    st.write('This solution can also be applied to unconfined aquifers if the variation of the hydraulic head is small relative to the saturated thickness of the aquifer such that the transmissivity can be regarded as approximately constant. \n\n')
    st.write('Bakker & Post (2022) provide more details about the derivation of this solution and a Python code for its application. This Jupyter Notebook makes use of their Python code and adds features such as sliders and textboxes that facilitate the variation of parameter values and the visualisation of their effects on the hydraulic heads.\n\n\n')
    st.image("images/Fig1_transient_1d_flow_conf.jpg", caption="Figure 1: Aquifer headchange due to surface water level change.")
    st.write('References: Bakker, M., & Post, V. (2022). Analytical groundwater modeling: Theory and applications using Python. CRC Press.')

# Parameters
col1, col2, col3 = st.columns(3)
with col1:
    T = st.slider('T',0.1,100.,10.,0.1)
with col2:
    S = st.slider('S', 0.,0.3,0.2,0.01)
with col3:
    h0 = st.slider('h0', 0.1,10.,2.,0.1)

col4, col5, col6 = st.columns(3)
with col4:
    max_x = st.slider('max_x', 1, 1000, 200, 10)
with col5:
    max_t= st.slider('max_t', 1, 1000, 100, 10)

with st.expander('See parameter description'):
    st.write('''
             *T*...Transmissivity of the aquifer\n
             *S*...Storage coefficient (storativity).\n
             *h0*...The hydraulic head after the water level has risen.\n
             *max_x*...Furthest displayed, horizontal distance from the river.\n
             *max_t*...Latest displayed time since the sudden water level rise.
             ''')

t0=0 # time of change in the river level, d

def h_edelman(x, t, T, S, h0, t0=0): 
    # Funktion to evaluate the head change after Edelman (1947)
    u = np.sqrt(S * x ** 2 / (4 * T * (t - t0)))
    return h0 * erfc(u)

def Qx_edelman(x, t, T, S, h0, t0=0):  
    # Funktion to evaluate the 1d flux after Darcy(1856) and Edelman (1947)
    u = np.sqrt(S * x ** 2 / (4 * T * (t - t0)))
    return T * h0 * 2 * u / (x * np.sqrt(np.pi)) * np.exp(-u ** 2)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
plt.subplots_adjust(hspace=0.5,bottom=0.25)
x = np.linspace(1e-12, max_x, 100)
t = np.linspace(1e-12, max_t, 100)
    
for time, c in zip([1, 10, 100], ['limegreen', 'dodgerblue', 'mediumslateblue']):    
    h = h_edelman(x, time, T, S, h0, t0)
    ax1.plot(x, h, label=f'time={time} d', color=c) 
ax1.grid()
ax1.set_xlabel('$x$ [m]')
ax1.set_ylabel('h [m]')
ax1.set_ylim(0, h0)
ax1.set_xlim(0, max_x)

for time, c in zip([1, 10, 100],  ['limegreen', 'dodgerblue', 'blueviolet']):  
    Qx = Qx_edelman(x, time, T, S, h0, t0)
    ax2.plot(x, Qx, label=f'time={time} d', color=c)  
ax2.grid()
ax2.set_xlabel('$x$ [m]')
ax2.set_ylabel('$Q_x$ [m$^2$/d]')
ax2.set_xlim(0, max_x)

for dist, c in zip([50, 100, 200], ['firebrick', 'darkorange', 'gold']):   
    h = h_edelman(dist, t, T, S, h0, t0)
    ax3.plot(t, h, label=f'distance={dist} m', color=c) 
ax3.grid()
ax3.set_xlabel('$t$ [d]')
ax3.set_ylabel('h [m]')
ax3.set_ylim(0, h0)
ax3.set_xlim(0, max_t)

for dist, c in zip([50, 100, 200],  ['firebrick', 'darkorange', 'gold']):   
    Qx = Qx_edelman(dist, t, T, S, h0, t0)
    ax4.plot(t, Qx, label=f'distance={dist} d', color=c)
ax4.grid()
ax4.set_xlabel('$t$ [d]')
ax4.set_ylabel('$Q_x$ [m$^2$/d]')
ax4.set_xlim(0, max_t)

# Legends
global lgt1, lgt2
handles_time, labels_time = ax1.get_legend_handles_labels()  # Collect from ax1 and ax2
lgt1=fig.legend(handles_time, labels_time, loc='upper center', bbox_to_anchor=(0.5, 0.57), ncol=3)  # Custom position

handles_distance, labels_distance = ax3.get_legend_handles_labels()
lgt2=fig.legend(handles_distance, labels_distance, loc='lower center', bbox_to_anchor=(0.5, 0.15), ncol=3)
st.pyplot(fig)

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('images\CC_BY-SA_icon.png')