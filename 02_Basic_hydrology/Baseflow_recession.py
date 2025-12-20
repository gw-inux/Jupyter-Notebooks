import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import streamlit as st

# also 02-02-001
# Todo
# log slider
# number input

# --- Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann":[1]
}
institutions = {
    1: "Institute for Groundwater Management, TU Dresden"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)


st.title('Baseflow recession')


st.write('This application compute the baseflow recession and plots discharge as function of time. The function we are looking is') 
st.latex("Q = Q_0 e^{-at}")
st.write('with')
st.markdown("* Q = flow at ome time t after recession started (m3/s)")
st.markdown("* Q_0 = flow at the start of the recession (m3/s)")
st.markdown("* a = is the recession constant for the basin (1/d)")
st.markdown("* t = is the time since the start of the recession (d)")

"---"

columns = st.columns((1,1), gap = 'large')

# This is a simple computation with a fixed temperature of 10 degrees celsius.

# Initialize librarys - This eventually needs adapted
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from ipywidgets import *

tmax = 91
t = np.arange(0, tmax, tmax/200)

# Define the minimum and maximum for the logarithmic scale
log_min = -3.0 # Corresponds to 10^-6 = 0.000001
log_max = 0.0  # Corresponds to 10^0 = 1

with columns[0]:
    Q0 = st.slider(f'**Flow at the start of recession (m3/s)**:',0.0,5000.0,1000.0,0.01)
    x_point = st.slider(f'**Point (x-axis) for result output**:',0,tmax,0,1)
with columns[1]:
    a_slider_value = st.slider(f'(log of) **Recession constant for the basin (1/d)**',log_min,log_max,log_max,0.01)
    # Convert the slider value to the logarithmic scale
    a = 10 ** a_slider_value
    # Display the logarithmic value
    st.write("**Recession constant:** %5.2e" %a)
    


Q = Q0*(math.e**(a*t*-1))
    
#Compute K_eq for the example point
Q_point = Q0*(math.e**(a*x_point*-1))
    
# Plot
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(t,Q, linewidth =3, label='Baseflow recession')
ax.set(xlabel='time in d', ylabel='Flow in m3/s',title='Baseflow recession')
ax.set(xlim=(0, tmax), ylim=(0, 5000))
ax.fill_between(t, Q, 0, facecolor= 'lightblue')
plt.plot(x_point,Q_point, marker='o', color='r',linestyle ='None', label='your input')
xticks = np.arange(0, tmax, 7)
ax.set_xticks(xticks)
ax.grid()
plt.legend()

st.pyplot(fig)
 
st.write("Time after beginning of recession: %3i" %x_point)
st.write('Flow rate in m3/s:  %5.2f' %Q_point)

st.markdown('---')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')