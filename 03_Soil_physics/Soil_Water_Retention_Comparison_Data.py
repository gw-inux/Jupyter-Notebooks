# Initialize the needed Python packages
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title('Soil Water Retention characteristics')

st.subheader('Comparison of datasets')

columns = st.columns((1,1), gap = 'large')
with columns[0]:
    st.write('**Dataset 1 - Input**')
    user1 = st.toggle('User defined data for plot 1?')
    if user1:
        tr1    = st.slider('residual water content 1 (-)', 0.01, 0.4, 0.04, 0.01)
        ts1    = st.slider('saturated water content 1 (-)', 0.15, 0.7, 0.30, 0.01)
        alpha1 = st.slider('alpha 1 (1/cm)', 0.01, 1., 0.1, 0.01)
        n1     = st.slider('n 1 (-)', 1.01, 3., 1.2, 0.01)
    else:    
        data1 = st.selectbox("**What data should be used?**",("Synthetic DS1", "Synthetic DS2"), key = 'Data1')
        if (st.session_state.Data1 == "Synthetic DS1"):
            #TODO PUT THE DATA IN ONE LIST, CHOOSE DATA FROM LIST
            tr1 = 0.06
            ts1 = 0.45
            alpha1 = 0.32
            n1 = 1.35   
        if (st.session_state.Data1 == "Synthetic DS2"):
            tr1 = 0.07
            ts1 = 0.48
            alpha1 = 0.22
            n1 = 1.15            
      
with columns[1]:
    st.write('**Dataset 2 - Input**')
    user2 = st.toggle('User defined data for plot 2?')
    if user2:
        tr2    = st.slider('residual water content 2 (-)', 0.01, 0.4, 0.06, 0.01)
        ts2    = st.slider('saturated water content 2 (-)', 0.15, 0.7, 0.35, 0.01)
        alpha2 = st.slider('alpha 2 (1/cm)', 0.01, 1., 0.2, 0.01)
        n2     = st.slider('n 2 (-)', 1.01, 3., 1.3, 0.01)
    else:
        data2 = st.selectbox("**What data should be used?**",("Synthetic DS1", "Synthetic DS2"), key = 'Data2')
        if (st.session_state.Data2 == "Synthetic DS1"):
            tr2 = 0.06
            ts2 = 0.45
            alpha2 = 0.32
            n2 = 1.35   
        if (st.session_state.Data2 == "Synthetic DS2"):
            tr2 = 0.07
            ts2 = 0.48
            alpha2 = 0.22
            n2 = 1.15 
  
plot4 = st.toggle('Plot k_r 1') 


# given data (retention) - used in exercise

t1=[0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.3,0.33,0.36,0.39,0.42,0.45]
p1=[2230.546345,577.472177,300.4391307,199.8371285,142.8205223,109.6375793,85.19965286,67.18768129,53.82569358,41.8841783,31.92533514,21.62546735,10.23974185]
t2=[0.18,0.19,0.22,0.25,0.28,0.31,0.35,0.4,0.44,0.47,0.51,0.54,0.55]
p2=[50030.534,9000.477,2000.407,900.835,500.023,120.633,60.528,30.189,11.823,7.883,1.514,0.625,0.285]
t3=[0.35,0.37,0.4,0.42,0.44,0.47,0.49,0.5,0.52,0.54,0.55,0.57,0.57]
p3=[350030.55,7800.21,1800.47,940.88,440.03,134.63,56.12,22.11,8.68,4.17,1.94,0.35,0.15]#definition of the function (conductivity)


x_max = 300
    
# intermediate results 
m1   = 1-1/n1                                              # van Genuchten parameter
PWP1 = tr1 + (ts1 - tr1)/(1+(alpha1*10**4.2)**n1)**m1      # permanent wilting point
FC1  = tr1 + (ts1 - tr1)/(1+(alpha1*10**1.8)**n1)**m1      # field capacity
eFC1 = FC1 - PWP1                                          # effective field capacity

m2   = 1-1/n2                                         # van Genuchten parameter
PWP2 = tr2 + (ts2 - tr2)/(1+(alpha2*10**4.2)**n2)**m2      # permanent wilting point
FC2  = tr2 + (ts2 - tr2)/(1+(alpha2*10**1.8)**n2)**m2      # field capacity
eFC2 = FC2 - PWP2                                      # effective field capacity

# model output
t_plot1  = []                                        # t  = theta = moisture content
p_plot1  = []                                        # p  = phi   = suction head
kr_plot1 = []                                        # kr = rel. permeability

# model output
t_plot2  = []                                        # t  = theta = moisture content
p_plot2  = []                                        # p  = phi   = suction head
kr_plot2 = []                                        # kr = rel. permeability
    
for x in range (0, x_max):
    t1 = tr1 + (ts1-tr1)*x/(x_max-1)                 # [-] moisture content; please note that range counts up to x_max-1
    t2 = tr2 + (ts2-tr2)*x/(x_max-1)                 # [-] moisture content; please note that range counts up to x_max-1
    te1 = (t1-tr1)/(ts1-tr1)                         # [-] effective saturation      
    te2 = (t2-tr2)/(ts2-tr2)                         # [-] effective saturation
    if x == 0:
        p1     = 1E18                                # [cm] suction head
        p2     = 1E18
        kr1    = 0                                   # [-] relative hydraulic conductivity
        kr2    = 0
    else: 
        p1     = ((te1**(-1/m1)-1)**(1/n1))/alpha1                      
        p2     = ((te2**(-1/m2)-1)**(1/n2))/alpha2
        kr1    = np.sqrt(te1)*(1-(1-te1**(1/m1))**m1)**2
        kr2    = np.sqrt(te2)*(1-(1-te2**(1/m2))**m2)**2
    t_plot1.append(t1)
    p_plot1.append(p1)
    kr_plot1.append(kr1)
    t_plot2.append(t2)
    p_plot2.append(p2)
    kr_plot2.append(kr2)
        
    
fig = plt.figure(figsize=(9,6))
ax  = fig.add_subplot()
ax.plot(t_plot1, p_plot1, 'r', markersize=3, label=r'Dataset 1')
ax.plot(t_plot2, p_plot2, 'g', markersize=3, label=r'Dataset 2')
ax.vlines(x= tr1, ymin=1e-1, ymax=1e+5, linestyle='--', colors='r')  
ax.vlines(x= tr2, ymin=1e-1, ymax=1e+5, linestyle='--', colors='g')    
ax.hlines(y= 10**4.2, xmin=0, xmax=PWP1, colors='r')    #upper green line
ax.vlines(x= PWP1, ymin=1e-1, ymax=10**4.2, colors='r')
ax.hlines(y= 10**4.2, xmin=0, xmax=PWP2, colors='g')    #upper green line
ax.vlines(x= PWP2, ymin=1e-1, ymax=10**4.2, colors='g')
ax.hlines(y= 10**1.8, xmin=0, xmax=FC1, colors='r')     #bottom green line
ax.vlines(x= FC1, ymin=1e-1, ymax=10**1.8, colors='r')
ax.hlines(y= 10**1.8, xmin=0, xmax=FC2, colors='g')     #bottom green line
ax.vlines(x= FC2, ymin=1e-1, ymax=10**1.8, colors='g')

ax.set(xlabel='water content [-]', ylabel ='suction head [cm]', xlim = [0, 0.7], ylim = [1e-1,1e+5], yscale = 'log' )
ax.grid(which="both", color='grey',linewidth=0.5)
plt.legend()
st.pyplot(fig)

columns2 = st.columns((1,1), gap = 'large')
with columns2[0]:
    st.write('**Dataset 1**')
    st.write('Van Genuchten             m:', '{:.5f}'.format(m1) )
    st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP1) )
    st.write('Field Capacity           FC:', '{:.2f}'.format(FC1) )
    st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC1) )
  
      
with columns2[1]:
    st.write('**Dataset 2**')
    st.write('Van Genuchten             m:', '{:.5f}'.format(m2) )
    st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP2) )
    st.write('Field Capacity           FC:', '{:.2f}'.format(FC2) )
    st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC2) )

if plot4 == 1:
    fig = plt.figure(figsize=(6,4))
    ax  = fig.add_subplot()
    ax.plot(t_plot1, kr_plot1, 'r', markersize = 3, label=r'Dataset 1')
    ax.plot(t_plot2, kr_plot2, 'g', markersize = 3, label=r'Dataset 1')
    ax.set(xlabel='water content [-]', ylabel='rel hydraulic conductivity [cm/d]', xlim = [0, 0.7], ylim = [0,1] )
    ax.grid(which="major", color='grey',linewidth=0.5)
    plt.legend()
    st.pyplot(fig)