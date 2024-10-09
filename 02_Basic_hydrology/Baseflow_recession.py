import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import streamlit as st

st.title('Baseflow recession')


st.write('This application compute the baseflow recession and plots discharge as function of time. The function we are looking is') 
st.latex("Q = Q_0 e^{-at}")
st.write('with')
st.markdown("* Q = flow at ome time t after recession started (m3/s)")
st.markdown("* Q_0 = flow at the start of the recession (m3/s)")
st.markdown("* a = is the recession constant for the basin (1/d)")
st.markdown("* t = is the time since the start of the recession (d)")

columns = st.columns((1,1), gap = 'large')

# This is a simple computation with a fixed temperature of 10 degrees celsius.

# Initialize librarys - This eventually needs adapted
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from ipywidgets import *

    
with columns[0]:
    Q0 = st.slider(f'**Flow at the start of recession (m3/s)**:',0.0,5000.0,1000.0,0.01)
with columns[1]:
    a = st.slider(f'**Recession constant for the basin (1/d)**',0.000001,0.1,0.01,0.00001,format="%e")
    x_point = st.slider(f'**Point (x-axis) for result output**:',0,61,0,1)
    
tmax = 91
t = np.arange(0, tmax, tmax/200)

Q = Q0*(math.e**(a*t*-1))
    
#Compute K_eq for the example point
Q_point = Q0*(math.e**(a*x_point*-1))
    
# Plot
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(t,Q, linewidth =3, label='Baseflow recession')
ax.set(xlabel='time in d', ylabel='Flow in m3/s',title='Baseflow recession')
ax.set(xlim=(0, tmax), ylim=(0, Q0*1.1))
ax.fill_between(t, Q, 0, facecolor= 'lightblue')
plt.plot(x_point,Q_point, marker='o', color='r',linestyle ='None', label='your input')
xticks = np.arange(0, tmax, 7)
ax.set_xticks(xticks)
ax.grid()
plt.legend()

st.pyplot(fig)
 
st.write("Time after beginning of recession: %6.3f" %x_point)
st.write('Flow rate in m3/s:  %5.2f' %Q_point)