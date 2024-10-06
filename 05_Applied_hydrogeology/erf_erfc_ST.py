from scipy.special import erfc, erf
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.title('Visualization of erf(x)/erfc(x)')

x = np.arange(-3, 3, 0.01)
s1 = erf(x)
s2 = erfc(x)

x_print = st.slider('Select the value for printout', -3.0,3.0,0.0,0.01)
s1_print = erf(x_print)
s2_print = erfc(x_print)

st.subheader('Plot of erf/erfc')

# Plot figure
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot()
ax.plot(x,s1, color='magenta', label='erf(x)')
ax.plot(x,s2, color='darkblue', label='erfc(x)')
ax.plot(x_print,s1_print, marker='o', color='magenta',linestyle ='None', label='erf(x_print)')
ax.plot(x_print,s2_print, marker='o', color='darkblue',linestyle ='None', label='erfc(x_print)')
plt.axis([-3,3,-1.5,2.5])
ax.set(xlabel='x', ylabel='erf(x) / erfc(x)', title='Gauss error functions erf(x) and erfc(x)')
ax.grid()
plt.legend()
    
#plt.show()

st.pyplot(fig=fig)
    
st.write('Computed values for x =:',"% 3.2F"%  x_print)
st.write('erf(x)  =',"% 5.4F"% s1_print)
st.write('erfc(x) =',"% 5.4F"% s2_print)