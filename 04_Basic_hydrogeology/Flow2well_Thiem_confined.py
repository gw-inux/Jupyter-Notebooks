# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface

st.title('Steady-State Flow to a Well in a Confined Aquifer - Drawdown with the Thiem equation')

# Import parameter
log_min = -7.0 # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # K / Corresponds to 10^0 = 1

columns = st.columns((1,1,1))

with columns[0]:
    with st.expander('Adjust the plot'):
        x_max = st.slider('x_max of the plot (m)', 10,10000,5000,50, format="%5i")
    
with columns[1]:
    with st.expander('Adjust the aquifer parameters'):
        H =  st.slider('Unaffected hydraulic head (m)', 1.,100.,50.,0.01, format="%5.2f")
        m =  st.slider('Thickness of the aquifer (m)', 1.,100.,20.,0.01, format="%4.2f")
        K_slider_value=st.slider('(log of) **Hydr. conductivity (m/s)**', log_min,log_max,-3.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        K = 10 ** K_slider_value
        # Display the logarithmic value
        st.write("_Hydraulic conductivity (m/s):_ %5.2e" %K)
with columns[2]:
    with st.expander('Adjust the well characteristics'):
        r_w = st.slider('Well radius (m)', 0.01,1.,0.3,0.01, format="%4.2f")
        ddwn = st.toggle('Abstraction _Q_ or Drawdown _s_?')
        if ddwn:
            s = st.slider('Drawdown (m)', 0.01, 10.0, 0.2, 0.01, format="%5.2f")
        else:
            Q =  st.slider('Abstraction rate (m3/s)', 0.001,0.2,0.05,0.001, format="%5.3f")

# Initialize
if ddwn:
    R = 3000 * s * K**0.5
    Q = 2 * np.pi * K * m * s / np.log(R / r_w)
else:
    R_max = 3000*(H-m)*0.01**0.5
    R_old = R_max/2

    #FIND R
    while True: 
        h_w = H - (Q * np.log(R_old/r_w))/(2 * np.pi * K * m)
        R = 3000 * (H-h_w) * K**0.5
        if abs(R - R_old)<0.00001:
            break
        R_old = R
    
#COMPUTE h(r)
n_points = 500  # reasonable resolution for plotting
r = np.linspace(r_w, R, n_points)
rm = -r  # mirrored for left side
h = H - (Q * np.log((R)/(r)))/(2 * np.pi * K * m)
    
#PLOT    
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
if((h[0])>m):
    ax.plot(r,h, '--' 'b')
    ax.plot(rm,h, '--' 'b')
    ax.hlines(y= H, xmin=R,  xmax= x_max, linestyle='--', colors='b')
    ax.hlines(y= H, xmin=-R, xmax=-x_max, linestyle='--', colors='b')
else:
    ax.plot(r,h, 'r')
    ax.plot(rm,h, 'r')
    ax.hlines(y= H, xmin= R, xmax= x_max, colors='r')    
    ax.hlines(y= H, xmin=-R, xmax=-x_max, colors='r')
    ax.text((R/2),(H*1.05),'UNCONFINED CONDITIONS - ADJUST PARAMETER')
    
ax.set(xlabel='x [m]',ylabel='head [m]', xlim=[(-x_max*1.),(x_max*1.)], ylim=[0,(H+5)])
    
# MAKE 'WATER'-TRIANGLE
ax.arrow(x_max*0.95,(H+(H*0.04)), 0, -0.01, fc="k", ec="k",head_width=(x_max*0.04), head_length=(H*0.04))
ax.hlines(y= H-(H*0.02), xmin=x_max*0.93, xmax=x_max*0.97, colors='blue')   
ax.hlines(y= H-(H*0.04), xmin=x_max*0.94, xmax=x_max*0.96, colors='blue')   
    
ax.hlines(y= m, xmin=-x_max, xmax=x_max, colors='saddlebrown')    #AQUIFER TOP LINE
    
# COLORED AREA (ATTN: Y-VALUES = RELATIVE VALUE)
ax.axvspan(-x_max, x_max, ymin=0, ymax=(m/(H+5)), alpha=0.9, color='lightblue')
ax.axvspan(-x_max, x_max, ymin=0, ymax=((H+5)/1), alpha=0.5, color='linen')
    
ax.text((x_max/2),(m/2),'confined aquifer')
    
st.pyplot(fig)

st.markdown(f"""
### Model Output
**Drawdown at the well:** {H-h[0]:.3f} m  
**Abstraction rate (Q):** {Q:.3f} m³/s  
"""
)


# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')