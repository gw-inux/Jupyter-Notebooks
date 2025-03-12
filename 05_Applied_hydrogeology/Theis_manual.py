# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import io
import streamlit as st

### 01 TITLE AND HEADER

st.title('🎯 The Theis solution for pumping test evaluation')

st.header(':blue[Manually parmater fitting with type-curve matching]')

st.subheader(':blue-background[Materials and Guidance for Theis Type-curve matching]', divider="blue")

### 02 INITIAL EXPLANATION
st.markdown('''
            Transient Flow toward a well in a confined aquifer is described here using the Theis Solution. You can use the subsequent materials and instructions to perform manual type-curve matching.
            '''
)

### 03 INITIAL ASSESSMENTS

### 04 THEORY

### 05 FUNCTIONS

#Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def theis_wu(Q, T, s):
    wu = s * 4. * np.pi * T / Q
    return wu

def deriv(t, tm, s, sm):
    #d = (s-sm)/(np.log(t)-np.log(tm))
    d=((t+tm)/2)*((s-sm)/(t-tm))
    return d
    
### 06 READ AND PREPARE DATA

# TODO ALLOW CSV / MORE DATA (RANDOM GENERATED)
# Aquifer test data
# Drawdown data from SYMPLE exercise and parameters 
m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
r = 120       # m
b = 8.5       # m
Qs = 0.3/60   # m^3/s
Qd = Qs*60*60*24 # m^3/d
    
    
# Data
u_max = 10
r_max = 1000000
t_max = len(m_time)
u  = [u_max for x in range(r_max)]
um = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
um_inv = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]
w_um = [well_function(u_max/r_max) for x in range(r_max)]
d = [0 for x in range(t_max)]

### 07 COMPUTATION
for x in range(1,r_max,1):
    if x>0:
        u[x] = x*u_max/r_max
        u_inv[x] = 1/u[x]
        w_u[x] = well_function(u[x])
        
### 08 PLOTTING
# Plotting the Theis curve

#W(u) is match_wu and 1/u is match_uinv

u_inv_values = [0.1, 1.0, 10, 100, 1000]
wu_values = [0.01, 0.1, 1.0, 10]

columns1 = st.columns((1,1), gap = 'large')
with columns1[0]:
    match_u_inv = st.select_slider('Select 1/u for the matchpoint', options= u_inv_values, value=1.0)
with columns1[1]:
    match_wu     =st.select_slider('Select w(u) for the matchpoint', options= wu_values, value=1.0)
        
matchgrid_x=[match_u_inv, match_u_inv]
matchgrid_y=[match_wu, match_wu]
matchgrid  =[0.001, 1000000]

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)  # adjust plot area

#plot the data
ax.plot(u_inv, w_u, color = 'black', linewidth = 2)
ax.plot(match_u_inv, match_wu,'ro',markersize=6)
ax.plot(matchgrid_x,matchgrid,color ='lime', linewidth = 1)
ax.plot(matchgrid,matchgrid_y,color = 'lime', linewidth = 1)

#set up the diagramm
plt.yscale("log")
plt.xscale("log")
plt.axis([0.1,1E4,1E-2,1E+1])
ax.set(xlabel='1/u', ylabel='w(u)',
       title='Theis type curve for manual evaluation')
ax.grid(which="both",color='whitesmoke', linewidth=0.5)

#box around plot
ax.spines['top'].set_color('lightgrey')
ax.spines['bottom'].set_color('lightgrey')
ax.spines['right'].set_color('lightgrey')
ax.spines['left'].set_color('lightgrey')

ax.tick_params(which='both', colors='lightgrey')

st.pyplot(fig)

# Safe the figure
# Convert figure to a BytesIO object
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format="png", dpi=300)
img_buffer.seek(0)  # Reset buffer position

columns5 = st.columns((1,1,1), gap = 'large')
with columns5[1]:
    # Add download button
    st.download_button(
        label=":green[**Download**] **Theis Type Curve**",
        data=img_buffer,
        file_name="Theis_type_curve.png",
        mime="image/png"
        )
        
# PLOTTING DATA

st.subheader(':red[Here you will find soon an option to choose from different data sets and to upload own data]')

semilog = st.toggle('Switch from log-log to semi-log plot')
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)  # adjust plot area
ax.plot(m_time, m_ddown,'bo', markersize=3)
if semilog:
    plt.xscale("log")
else:
    plt.xscale("log")
    plt.yscale("log")
plt.axis([0.1,1E4,1E-2,1E+1])
ax.set(xlabel='time t (min)', ylabel='drawdown s (m)',
       title='Measured data')
ax.grid(which="both", color='grey',linewidth=0.5)

st.pyplot(fig)

# Safe the figure
# Convert figure to a BytesIO object
img_buffer = io.BytesIO()
fig.savefig(img_buffer, transparent='true', format="png", dpi=300)
img_buffer.seek(0)  # Reset buffer position

columns6 = st.columns((1,1,1), gap = 'large')
with columns6[1]:
    # Add download button
    st.download_button(
        label=":green[**Download**] **Measured Data for Theis**",
        data=img_buffer,
        file_name="measured_data_Theis.png",
        mime="image/png"
        )
        
        
st.subheader(':red[Here you will find soon further explanation and instructions how to perform type curve matching]')        
        
# TODO - NUMBER INPUT AND EVALUATION
# fig.savefig(img_buffer,  transparent='true',format="png", dpi=300)
# TODO - INSTRUCTION HOW TO USE (MAYBE SCREENCAST)