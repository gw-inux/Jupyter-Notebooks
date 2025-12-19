# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# also 03-05-003
# Todo
# log slider
# number input

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


#--- Functions
def compute_R(Q, K, H, r_w):
    dry = False
    h = max(0.0, 0.5 * H)   # initial guess
    max_it = 200
    tol = 1e-6

    for _ in range(max_it):
        s = H - h
        R = 3000.0 * s * np.sqrt(K)

        # guard: Sichardt must give R > r_w
        if R <= r_w:
            dry = True
            return R, 0.0, dry

        discr = H**2 - (Q / (np.pi * K)) * np.log(R / r_w)

        if discr <= 0.0:
            dry = True
            return R, 0.0, dry

        h_new = np.sqrt(discr)

        if abs(h_new - h) < tol:
            h = h_new
            break

        h = h_new

    # final recompute with converged h
    s = H - h
    R = 3000.0 * s * np.sqrt(K)
    return R, h, dry


def compute_h(Q,K,H,R,r):
    h = np.sqrt (H**2 - (Q  / (np.pi * K) * np.log(R / r)))
    return h
    
#--- User Interface

st.title('Steady-State Flow to a Well in an Unconfined Aquifer - Drawdown with the Thiem equation')

# Input
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
            Q = st.slider('Abstraction rate (m3/s)', 0.001,0.2,0.05,0.001, format="%5.3f")

# Initialize
if ddwn:
    R = 3000 * s * K**0.5
    h_w = H - s
    numerator = H**2 - h_w**2  # = 2 H s - s^2
    Q = np.pi * K * numerator / np.log(R / r_w)
    dry = False
else:
    # User specifies Q per well: determine R, h_w, and potential dry condition
    R, h_w, dry = compute_R(Q, K, H, r_w)

#COMPUTE h(r)
#dry
r = np.arange(r_w, R, 0.01) 
rm = r*-1
h = compute_h(Q, K, H, R, r)

#PLOT    
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1, 1, 1)
    
if dry:
    ax.plot(r,h, '--' 'r')
    ax.plot(rm,h, '--' 'r')
    ax.hlines(y= H, xmin=R,  xmax= x_max, linestyle='--', colors='r')
    ax.hlines(y= H, xmin=-R, xmax=-x_max, linestyle='--', colors='r') 
else:
    ax.plot(r,h, '--' 'b')
    ax.plot(rm,h, '--' 'b')
    ax.hlines(y= H, xmin=R,  xmax= x_max, linestyle='--', colors='b')
    ax.hlines(y= H, xmin=-R, xmax=-x_max, linestyle='--', colors='b')

    
ax.fill_between(r, h, 0, facecolor= 'lightblue')
ax.fill_between(-r, h, 0, facecolor = 'lightblue')
ax.axvspan(xmin= R, xmax= x_max, ymin=0, ymax=H/(H+5), color='lightblue')        
ax.axvspan(xmin= -x_max, xmax= -R, ymin=0, ymax=H/(H+5),  color='lightblue')
ax.axvspan(xmin= -r_w, xmax= r_w, ymin=0, ymax=h_w/(H+5),  color='lightblue')

ax.set(xlabel='x [m]',ylabel='head [m]', xlim=[(-x_max*1.),(x_max*1.)], ylim=[0,(H+5)])
    
# MAKE 'WATER'-TRIANGLE
ax.arrow(x_max*0.95,(H+(H*0.04)), 0, -0.01, fc="k", ec="k",head_width=(x_max*0.04), head_length=(H*0.04))
ax.hlines(y= H-(H*0.02), xmin=x_max*0.92, xmax=x_max*0.98, colors='blue')   
ax.hlines(y= H-(H*0.04), xmin=x_max*0.94, xmax=x_max*0.96, colors='blue')  
if dry:
    ax.text((x_max/2),1,'unconfined aquifer')
    ax.text((x_max/2),2.5,'well running dry',color='red')
else:
    ax.text((x_max/2),1,'unconfined aquifer')
    
st.pyplot(fig)

st.markdown(f"""
### Model Output
**Drawdown at the well:** {H-h[0]:.3f} m  
**Abstraction rate (Q):** {Q:.3f} m³/s  
"""
)

"---"

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')