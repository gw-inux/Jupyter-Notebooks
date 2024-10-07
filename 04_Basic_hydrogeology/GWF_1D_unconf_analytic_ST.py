# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


st.title('Analytical solution for 1D unconfined flow with two defined head boundaries')

# Input data

columns = st.columns((1,1), gap = 'large')

with columns[0]:
    y_scale = st.slider('Scaling y-axis', 0,20,3,1)
    hl=st.slider('LEFT defined head', 0,300,150,1)
    hr=st.slider('RIGHT defined head', 0,300,152,1)
    L= st.slider('Length', 0,7000,2500,10)


with columns[1]:
    R=st.slider('Recharge in mm/a', -500,500,0,10)
    K=st.slider('Hydraulic conductivity in m/s', min_value=0.000001, step=0.000001, max_value=0.05, value=0.0000045, format="%e", )
    
x = np.arange(0, L,L/1000)
R=R/1000/365.25/86400
h=(hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5
    
# PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x,h)
ax.set(xlabel='x', ylabel='head',title='Hydraulic head for 1D unconfined flow')
ax.fill_between(x,0,h, facecolor='lightblue')
    
# BOUNDARY CONDITIONS hl, hr
ax.vlines(0, 0, hl, linewidth = 10, color='b')
ax.vlines(L, 0, hr, linewidth = 10, color='b')
    
# MAKE 'WATER'-TRIANGLE
h_arrow = (hl**2-(hl**2-hr**2)/L*(L*0.96)+(R/K*(L*0.96)*(L-(L*0.96))))**0.5  #water level at arrow
ax.arrow(L*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L*0.015), head_length=(h_arrow*0.0015))
ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

#ARROWS FOR RECHARGE 
if R != 0:
    head_length=(R*86400*365.25*1000*0.002)*y_scale/2
    h_rch1 = (hl**2-(hl**2-hr**2)/L*(L*0.25)+(R/K*(L*0.25)*(L-(L*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
    ax.arrow(L*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch2 = (hl**2-(hl**2-hr**2)/L*(L*0.50)+(R/K*(L*0.50)*(L-(L*0.50))))**0.5  #water level at arrow for Recharge Postition 2
    ax.arrow(L*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch3 = (hl**2-(hl**2-hr**2)/L*(L*0.75)+(R/K*(L*0.75)*(L-(L*0.75))))**0.5  #water level at arrow for Recharge Position 3
    ax.arrow(L*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)

#Groundwater divide
max_y = max(h)
max_x = x[h.argmax()]
R_min_ms=K*abs(hl**2-hr**2)/L**2
if R>R_min_ms:
    plt.vlines(max_x,0,max_y, color="r")

plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
plt.xlim(-50,L+50)
plt.text(L, (hr*1.016), 'R: {:.2e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='grey'))
ax.grid()
st.pyplot(fig)