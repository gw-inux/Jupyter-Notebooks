import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.title('Slugtest evaluation')

t = np.arange(0, 60, 0.1)

L = 2.1

R = 0.085

F = 2 * np.pi * L/np.log(L/R)

r = 0.025

prq = np.pi * r**2

# Define the minimum and maximum for the logarithmic scale
log_min = -5.0 # Corresponds to 10^-7 = 0.0000001
log_max =  -2.0  # Corresponds to 10^0 = 1

# Log slider with input and print
K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-3.0,0.01,format="%4.2f" )
K = 10 ** K_slider_value
st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)

exp_decay = np.exp(-F/prq*K*t)


# Plot figure
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot()
ax.plot(t,exp_decay, color='magenta', label='exp_decay')
plt.axis([0,60,0,1])
ax.set(xlabel='t', ylabel='H/Ho', title='Slugtest positive')
ax.grid()
plt.legend()
    
#plt.show()

st.pyplot(fig=fig)