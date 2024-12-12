# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


st.title('Analytical solution for 1D unconfined flow with one defined head boundary/river boundary')
st.subheader('Understanding :rainbow[Model Calibration]', divider="blue")

lc1, cc1, rc1 = st.columns((1,1,1), gap = 'large')
with cc1:
    theory = st.button('Show theory')
if theory:
    st.subheader('Conceptual model')
    st.write('The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by one defined-head boundary on the right side (left side is no flow). From the top, the aquifer receives uniform groundwater recharge.')
    
    st.subheader('Mathematical model')
    st.write('The equation for 1D groundwater flow in a homogeneous aquifer is')
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')
    st.write('with')
    st.write('- _x_ is spatial coordinate along flow,')
    st.write('- _h_ is hydraulic head,')
    st.write('- _K_ is hydraulic conductivity,')
    st.write('- _R_ is recharge.')
    st.write('A solution for the equation can be obtained with... TODO')


st.subheader('Computation and visualization')
st.write('Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge _R_ (in mm/a) and the hydraulic conductivity _K_ (in m/s).')

"---"
# Data for 'measurements'
K_random = 2.34E-4*(np.random.randint(5, 500)/100)
R_random = 150/1000/365.25/86400*(np.random.randint(50, 150)/100)

st.session_state.K_random = K_random
st.session_state.R_random = R_random

noise = 0.2

hr = 150.0
L = 2500
zb = (hr-10)

# Equation from Bakker et al. (chapter 3); assuming the aquifer bottom is 10 m below the left boundary head
phiL_random = 0.5 * K_random * (hr - zb) ** 2

# TODO - Implement the following function
def add_noise(j,noise):
    upper_value = round((i + noise/2)/ i * 100000)
    lower_value = round((i - noise/2)/ i * 100000)
    return upper_value, lower_value

# Equation from Bakker et al. (chapter 3); assuming the aquifer bottom is 10 m below the left boundary head
# phi = (-R_random / 2 * (x ** 2 - L ** 2) + phiL)
# h = zb + np.sqrt(2 * phi / K_random)

# Data for Calibration exercises
# 1 Regular
xp1 = [250, 500, 750, 1000, 1250, 1500, 1750,2000, 2250]
hp1 = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_random) / K_random) for x in xp1]

# 2 Random calib points
n_random2 = np.random.randint(3,8)
xp2 = []
for i in range(n_random2):
    xp2.append(np.random.randint(100, 2500))
hp2 = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_random) / K_random) for x in xp2]

# 3 Random calib points with uncertainty
n_random3 = np.random.randint(5,8)
xp3 = []
for i in range(n_random3):
    xp3.append(np.random.randint(100, 2500))
# Provide heads and add noise
hp3 = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_random) / K_random) for x in xp3]
hp3 = [i*np.random.randint(round((i - noise/2)/ i * 100000),round((i + noise/2)/ i * 100000))/100000 for i in hp3]


@st.fragment
def computation():
    # Input data
    # Define the minimum and maximum for the logarithmic scale
    log_min = -7.0 # Corresponds to 10^-7 = 0.0000001
    log_max =  0.0  # Corresponds to 10^0 = 1
    log_min2 = -9.0 
    log_max2 = -3.0 

    columns = st.columns((1,1), gap = 'large')
    with columns[0]:
        y_scale = st.slider('Scaling y-axis', 0,20,3,1)
        #hl=st.slider('LEFT defined head', 120,180,150,1)
        #hr=st.slider('RIGHT defined head', 120,180,152,1)
        #L= st.slider('Length', 0,7000,2500,10)
        if st.toggle('Provide data for calibration?'):
            calib = st.selectbox("What data for calibration?", ('Regular data', 'Irregular data', 'Irregular data with noise'))
        else:
            calib = 'No calibration'
        
    with columns[1]:
        R=st.slider('Recharge in mm/a',0,500,0,5)
        R = R/1000/365.25/86400
        # Log slider with input and print
        K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
        K = 10 ** K_slider_value
        st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
        riv = st.toggle ('River BC?')
        if riv:
            #hRiv = st.slider('River head', hr, hr+5.0, hr, 0.01)
            hRiv=150
            cRiv_slider=st.slider('(log of) CRIV', log_min2,log_max2,-5.0,0.01,format="%4.2f")
            cRiv = 10**cRiv_slider
            st.write("**CRIV:** %5.2e" %cRiv)
            hr2 = R * L / cRiv / zb + hRiv
      
    x = np.arange(0, L, L/1000)
    
    
    if riv:
        phiL = 0.5 * K * (hr2 - zb) ** 2
    else:
        phiL = 0.5 * K * (hr - zb) ** 2
    h = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K)
    
    # PLOT FIGURE
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x,h)
    if calib == 'Regular data':
        ax.plot(xp1,hp1, 'ro', label=r'measured')
    if calib == 'Irregular data':
        ax.plot(xp2,hp2, 'go', label=r'measured')
    if calib == 'Irregular data with noise':
        ax.plot(xp3,hp3, 'bo', label=r'measured')
    ax.set(xlabel='x', ylabel='head',title='Hydraulic head for 1D unconfined flow')
    ax.fill_between(x,0,h, facecolor='lightblue')
    
    # BOUNDARY CONDITIONS hl, hr
    ax.vlines(0, 0, 1000, linewidth = 10, color='lightgrey')
    ax.vlines(L, 0, hr, linewidth = 10, color='blue')
    if riv:
        ax.vlines(L, 0, hr, linewidth = 3, color='blue')
        ax.vlines(L-5, 0, hr2, linewidth = 3, color='fuchsia')
    else:
        ax.vlines(L, 0, hr, linewidth = 10, color='blue')
    # MAKE 'WATER'-TRIANGLE
    #h_arrow = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L*0.96 ** 2) + phiL) / K)  #water level at arrow
    #ax.arrow(100,150, 0.1,0.1)
    #ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
    #ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

    #ARROWS FOR RECHARGE 
    #if R != 0:
    #    head_length=(R*86400*365.25*1000*0.002)*y_scale/2
    #    h_rch1 = (hl**2-(hl**2-hr**2)/L*(L*0.25)+(R/K*(L*0.25)*(L-(L*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
    #    ax.arrow(L*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    #    h_rch2 = (hl**2-(hl**2-hr**2)/L*(L*0.50)+(R/K*(L*0.50)*(L-(L*0.50))))**0.5  #water level at arrow for Recharge Postition 2
    #    ax.arrow(L*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    #    h_rch3 = (hl**2-(hl**2-hr**2)/L*(L*0.75)+(R/K*(L*0.75)*(L-(L*0.75))))**0.5  #water level at arrow for Recharge Position 3
    #    ax.arrow(L*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)

    plt.ylim((hr+2)*(1-y_scale/100),hr *(1+y_scale/100))
    plt.xlim(-50,L+50)
    plt.text(L, 0.99 * hr *(1+y_scale/100), 'R: {:.2e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=14)
    st.pyplot(fig)
    
computation()

lc2, cc2, rc2 = st.columns((1,1,1), gap = 'large')
with cc2:
    st.button('Regenerate data? Press here!')