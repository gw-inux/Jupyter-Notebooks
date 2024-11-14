# Initialize the needed Python packages
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title('Soil Water Retention characteristics')

columns = st.columns((1,1), gap = 'large')
with columns[0]:
    plot1 = st.toggle('Plot Dataset 1')   
    plot2 = st.toggle('Plot Dataset 2')      
    plot3 = st.toggle('Plot Dataset 3')      
    plot4 = st.toggle('Plot k_r 1')   
with columns[1]:
    tr    = st.slider('residual water content (-)', 0.01, 0.4, 0.05, 0.01)
    ts    = st.slider('saturated water content (-)', 0.15, 0.7, 0.30, 0.01)
    alpha = st.slider('alpha (1/cm)', 0.01, 1., 0.1, 0.01)
    n     = st.slider('n (-)', 1.01, 3., 1.2, 0.01)
  



# given data (retention) - used in exercise

t1=[0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.3,0.33,0.36,0.39,0.42,0.45]
p1=[2230.546345,577.472177,300.4391307,199.8371285,142.8205223,109.6375793,85.19965286,67.18768129,53.82569358,41.8841783,31.92533514,21.62546735,10.23974185]
t2=[0.18,0.19,0.22,0.25,0.28,0.31,0.35,0.4,0.44,0.47,0.51,0.54,0.55]
p2=[50030.534,9000.477,2000.407,900.835,500.023,120.633,60.528,30.189,11.823,7.883,1.514,0.625,0.285]
t3=[0.35,0.37,0.4,0.42,0.44,0.47,0.49,0.5,0.52,0.54,0.55,0.57,0.57]
p3=[350030.55,7800.21,1800.47,940.88,440.03,134.63,56.12,22.11,8.68,4.17,1.94,0.35,0.15]#definition of the function (conductivity)


x_max = 300
    
# intermediate results 
m   = 1-1/n                                         # van Genuchten parameter
PWP = tr + (ts - tr)/(1+(alpha*10**4.2)**n)**m      # permanent wilting point
FC  = tr + (ts - tr)/(1+(alpha*10**1.8)**n)**m      # field capacity
eFC = FC - PWP                                      # effective field capacity

# model output
t_plot  = []                                        # t  = theta = moisture content
p_plot  = []                                        # p  = phi   = suction head
kr_plot = []                                        # kr = rel. permeability
    
for x in range (0, x_max):
    t = tr + (ts-tr)*x/(x_max-1)                    # [-] moisture content; please note that range counts up to x_max-1
    te = (t-tr)/(ts-tr)                             # [-] effective saturation      
    if x == 0:
        p     = 1E18                                # [cm] suction head
        kr    = 0                                   # [-] relative hydraulic conductivity
    else: 
        p     = ((te**(-1/m)-1)**(1/n))/alpha                      
        kr    = np.sqrt(te)*(1-(1-te**(1/m))**m)**2
    t_plot.append(t)
    p_plot.append(p)
    kr_plot.append(kr)
        
    
fig = plt.figure(figsize=(9,6))
ax  = fig.add_subplot()
ax.plot(t_plot, p_plot, 'r', markersize=3)
ax.vlines(x= tr, ymin=1e-1, ymax=1e+5, linestyle='--')      
ax.hlines(y= 10**4.2, xmin=0, xmax=PWP, colors='g')    #upper green line
ax.vlines(x= PWP, ymin=1e-1, ymax=10**4.2, colors='g')
ax.hlines(y= 10**1.8, xmin=0, xmax=FC, colors='b')     #bottom green line
ax.vlines(x= FC, ymin=1e-1, ymax=10**1.8, colors='b')
if plot1 == 1:
    ax.plot(t1, p1,'ro', markersize=3)
if plot2 == 1:
    ax.plot(t2, p2,'bo', markersize=3)
if plot3 == 1:
    ax.plot(t3, p3,'go', markersize=3)
ax.set(xlabel='water content [-]', ylabel ='suction head [cm]', xlim = [0, 0.7], ylim = [1e-1,1e+5], yscale = 'log' )
ax.grid(which="both", color='grey',linewidth=0.5)
st.pyplot(fig)

if plot4 == 1:
    fig = plt.figure(figsize=(6,4))
    ax  = fig.add_subplot()
    ax.plot(t_plot, kr_plot, 'b', markersize = 3)
    ax.set(xlabel='water content [-]', ylabel='rel hydraulic conductivity [cm/d]', xlim = [0, 0.7], ylim = [0,1] )
    ax.grid(which="major", color='grey',linewidth=0.5)
    st.pyplot(fig)
    
st.write('Van Genuchten             m:', '{:.5f}'.format(m) )
st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP) )
st.write('Field Capacity           FC:', '{:.2f}'.format(FC) )
st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC) )