# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title('Steady-State Flow to a Well in an Unconfined Aquifer - Drawdown with the Thiem equation')

# Input
# Import parameter
log_min = -7.0 # K / Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # K / Corresponds to 10^0 = 1
columns = st.columns((1,1), gap = 'large')

with columns[0]:
    x_max = st.slider('xmax',50,10000,2000,50)
    H = st.slider('H',1.,100.,15.,0.01)
    r_w   = st.slider('r_w',0.01,1.,0.3,0.01)
with columns[1]:
    K_slider_value=st.slider('(log of) **Hydr. conductivity (m/s)**', log_min,log_max,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_Hydraulic conductivity (m/s):_ %5.2e" %K)
    Q     = st.slider('Q',0.001,0.5,0.01,0.001,format="%5.3f")
    
# Function to calculate the hydraulic head h in an unsaturated aquifer as a function of distance r
def compute_R(Q,K,H,r_w):
    # Initial guess for h (starting at H) and R
    dry = False
    h = H/2       
    max_it = 1000  # Limit on iterations to prevent infinite loops
    tol = 1e-6     # Convergence tolerance
    for iteration in range(max_it):
        R = 3000 * (H-h) * np.sqrt(K)
        h_new = np.sqrt(H**2-(Q/(np.pi*K) * np.log(R/r_w)))       
        # Check for convergence
        if np.abs(h_new - h) < tol:
            break     
        # Check for dry condition
        if (H**2-(Q/(np.pi*K) * np.log(R/r_w))) < 0.0:
            dry = True
            break  
    R = 3000 * (H-h) * np.sqrt(K)
    return R, h, dry

def compute_h(Q,K,H,R,r):
    h = np.sqrt (H**2 - (Q  / (np.pi * K) * np.log(R / r)))
    return h
    
#run the initial iteration to get R
R, h_w, dry = compute_R(Q,K,H,r_w)

#COMPUTE h(r)
dry
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