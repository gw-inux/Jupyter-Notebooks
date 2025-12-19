# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# also Interactive Documents 08-07-003
# ToDo:
#    - K log slider

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

st.title('Analytical solution for 1D unconfined flow with one no-flow boundary and one specified head/head-dependent boundary')
st.header('Understanding :rainbow[Model Calibration]', divider="blue")

with st.expander('Show the theory (conceptual and mathematical model)'):
    st.markdown("""
            #### Conceptual model
            
            The conceptual model for both scenarios is shown in the images above. It assumes the aquifer is a **homogeneous** and **isotropic** structure with a **horizontal impermeable base at an elevation of zero** such that the heads determine the aquifer thickness. The aquifer receives uniform recharge from the surface across its entire length.
            
            The aquifer is bounded by
            - one specified-head **or** a head-dependent flow boundary on the right side, while
            - the left side is a no-flow boundary.
            
            From the top, the aquifer receives uniform groundwater recharge.
            """, unsafe_allow_html=True)
            
    lc2, cc2, rc2 = st.columns((20,60,20))
    with cc2:
        st.image('FIGS/08_07_1D_unconfined_noflow.jpg', caption="Conceptual model for a groundwater system with one no-flow boundary.")

    st.markdown("""
            #### Mathematical model
            
            The governing equation for steady-state 1D groundwater flow in an unconfined, homogeneous aquifer with recharge is
            """, unsafe_allow_html=True)
            
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')

    st.markdown("""
            with
            - _x_ is spatial coordinate along flow,
            - _h_ is hydraulic head,
            - _K_ is hydraulic conductivity,
            - _R_ is recharge.
            
            The equation can be solved by using suitable boundary conditions:
            - at $x=0$ the flow is defined as $dh/dx=0$ and
            - at $x=L$ the head is defined as $h=h_L$
            
            With some mathematical operations, see for example [Bakker and Post, 2022](https://doi.org/10.1201/9781315206134), the following analytical solutions can be derived:
            """, unsafe_allow_html=True)
            
    st.latex(r'''h(x) = \sqrt{h_L^2 + \frac{R}{K}  (L+x)  (2L - (L+x))}''')
    st.markdown("""
            where:
            - _h(x)_: hydraulic head at location _x_ (meters (m),
            - _L_: domain length (m),
            - _h<sub>L</sub>_: head at the specified-head boundary at _x_ = _L_ (m),
            - _R_: recharge (m/s),
            - _K_: hydraulic conductivity (m/s).
            
            This solution is subsequently used in the interactive plots to dynamically compute and visualize how different boundary conditions, hydraulic conductivities, and recharge rates affect the hydraulic head distribution.
            """, unsafe_allow_html=True)  

st.subheader('Computation and visualization', divider = 'violet')
st.markdown("""Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge _R_ (in mm/a) and the hydraulic conductivity _K_ (in m/s).""")
 
# Fixed data
noise = 0.2
L = 2500
hr = 150.0
zb = (hr-50)
hRiv = 150

# Data for random 'measurements'
K_random = 2.34E-4*(np.random.randint(5, 500)/100)
R_random = 150/1000/365.25/86400*(np.random.randint(50, 150)/100)
cRiv_random = 1.34E-7*(np.random.randint(5, 500)/100)
hr_riv_random = R_random * L / cRiv_random / zb + hRiv

st.session_state.K_random = K_random
st.session_state.R_random = R_random

# Equation from Bakker et al. (chapter 3); assuming the aquifer bottom is 10 m below the left boundary head
phiL_random = 0.5 * K_random * (hr - zb) ** 2
phiL_riv_random = 0.5 * K_random * (hr_riv_random - zb) ** 2

# TODO - Implement the following function
def add_noise(j,noise):
    upper_value = round((i + noise/2)/ i * 100000)
    lower_value = round((i - noise/2)/ i * 100000)
    return upper_value, lower_value
    
def compute_statistics(measured, computed):
    # Calculate the number of values
    n = len(measured)

    # Initialize a variable to store the sum of squared differences
    total_me = 0
    total_mae = 0
    total_rmse = 0

    # Loop through each value
    for i in range(n): # Add the squared difference to the total
        total_me   += (computed[i] - measured[i])
        total_mae  += (abs(computed[i] - measured[i]))
        total_rmse += (computed[i] - measured[i])**2

    # Calculate the me, mae, mean squared error
    me = total_me / n
    mae = total_mae / n
    meanSquaredError = total_rmse / n

    # Raise the mean squared error to the power of 0.5 
    rmse = (meanSquaredError) ** (1/2)
    return me, mae, rmse

# Data for Calibration exercises
# 1 Regular
xp1 = [250, 500, 750, 1000, 1250, 1500, 1750,2000, 2250]
hp1 = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_random) / K_random) for x in xp1]
hp1_riv = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_riv_random) / K_random) for x in xp1]

# 2 Random calib points
n_random2 = np.random.randint(3,8)
xp2 = []
for i in range(n_random2):
    xp2.append(np.random.randint(100, 2500))
hp2 = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_random) / K_random) for x in xp2]
hp2_riv = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_riv_random) / K_random) for x in xp2]

# 3 Random calib points with uncertainty
n_random3 = np.random.randint(5,8)
xp3 = []
for i in range(n_random3):
    xp3.append(np.random.randint(100, 2500))
# Provide heads and add noise
hp3 = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_random) / K_random) for x in xp3]
hp3_riv = [zb + np.sqrt(2 * (-R_random / 2 * (x ** 2 - L ** 2) + phiL_riv_random) / K_random) for x in xp3]
hp3 = [i*np.random.randint(round((i - noise/2)/ i * 100000),round((i + noise/2)/ i * 100000))/100000 for i in hp3]
hp3_riv = [i*np.random.randint(round((i - noise/2)/ i * 100000),round((i + noise/2)/ i * 100000))/100000 for i in hp3_riv]


@st.fragment
def computation():
    # Input data
    # Define the minimum and maximum for the logarithmic scale
    log_min = -5.0 # Corresponds to 10^-7 = 0.0000001
    log_max = -2.0  # Corresponds to 10^0 = 1
    log_min2 = -9.0 
    log_max2 = -3.0 

    columns = st.columns((1,1,1))
    with columns[0]:
        with st.expander('Adjust the plot'):
            y_scale = st.slider('_Scaling the y-axis of the plot_', 0,10,5,1)
        
    with columns[1]:
        riv = st.toggle ('Specified Head BC?')
        if st.toggle('Provide data for calibration?'):
            calib = st.selectbox("What data for calibration?", ('Irregular data with noise', 'Irregular data','Regular data' ))
            scatter = st.toggle('Show scatter plot')
            rch_fix = st.toggle('Fix recharge')
        else:
            calib = 'No calibration'
            scatter = False
            rch_fix = False

    
    with columns[2]:
        with st.expander('Modify parameters'):
            # Log slider for K with input and print
            K_slider_value=st.slider('_(log of) Hydraulic conductivity input:_', log_min,log_max,-4.0,0.01,format="%4.2f" )
            K = 10 ** K_slider_value
            st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
            if rch_fix:
                R = R_random
                R_print = R*1000*86400*365.25
                st.write("**Recharge (fixed) in mm/a:** %5.2f" %R_print)
            else:
                R = st.slider('_Recharge input:_',0,400,0,1)
                st.write("**Recharge in mm/a:** %3i" %R)
                R = R/1000/365.25/86400
            if riv:
                #hRiv = st.slider('River head', hr, hr+5.0, hr, 0.01)
                cRiv_slider = st.slider('_(log of) CRIV input_', log_min2,log_max2,-5.0,0.01,format="%4.2f")
                cRiv = 10**cRiv_slider
                st.write("**CRIV:** %5.2e" %cRiv)
                hr_riv = R * L / cRiv / zb + hRiv
     
    x = np.arange(0, L, L/100)
    
    if riv:
        phiL = 0.5 * K * (hr_riv - zb) ** 2
    else:
        phiL = 0.5 * K * (hr - zb) ** 2
    h = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K)
    
    # PLOT FIGURE
    fig = plt.figure(figsize=(9,12))
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(x,h)
    if calib == 'Regular data':
        if riv:
            ax.plot(xp1,hp1_riv, 'ro', label=r'measured')
            # compute heads for measurments
            hm = [zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K) for x in xp1]          
        else:
            ax.plot(xp1,hp1, 'ro', label=r'measured')          
            # compute heads for measurments
            hm = [zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K) for x in xp1]
    if calib == 'Irregular data':
        if riv:
            ax.plot(xp2,hp2_riv, 'go', label=r'measured')
            hm = [zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K) for x in xp2] 
        else:
            ax.plot(xp2,hp2, 'go', label=r'measured')
            hm = [zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K) for x in xp2]
    if calib == 'Irregular data with noise':
        if riv:
            ax.plot(xp3,hp3_riv, 'bo', label=r'measured')
            hm = [zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K) for x in xp3]
        else:
            ax.plot(xp3,hp3, 'bo', label=r'measured')
            hm = [zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K) for x in xp3]
    ax.fill_between(x,0,h, facecolor='lightblue')
    plt.title('Hydraulic head for 1D unconfined flow', fontsize=16)
    plt.xlabel(r'x in m', fontsize=14)
    plt.ylabel(r'hydraulic head in m', fontsize=14)
    
    # BOUNDARY CONDITIONS hl, hr
    ax.vlines(0, 0, 1000, linewidth = 10, color='lightgrey')
    ax.vlines(L, 0, hr, linewidth = 10, color='blue')
    if riv:
        ax.vlines(L, 0, hr, linewidth = 3, color='blue')
        ax.vlines(L-5, 0, hr_riv, linewidth = 3, color='fuchsia')
    else:
        ax.vlines(L, 0, hr, linewidth = 10, color='blue')
    # MAKE 'WATER'-TRIANGLE
    #h_arrow = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L*0.96 ** 2) + phiL) / K)  #water level at arrow
    #ax.arrow(100,150, 0.1,0.1)
    #ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
    #ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

    plt.ylim(148,hr *(1+y_scale/100))
    plt.xlim(-50,L+50)
    x_pos1 = 400
    x_pos2 = 2500
    y_pos1 = ((hr *(1+y_scale/100))-150)*0.9+150
    plt.text(x_pos1, y_pos1, 'No Flow bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
    if riv:
        plt.text(x_pos2, y_pos1, 'Head dependent bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='fuchsia', alpha=0.4), fontsize=12)
    else:
        plt.text(x_pos2, y_pos1, 'Specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
    
    if scatter:
        x45 = [0,200]
        y45 = [0,200]
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x45,y45, '--')
        if calib == 'Regular data':
            if riv:
                ax.plot(hp1_riv, hm,  'ro', label=r'measured')
                me, mae, rmse = compute_statistics(hm, hp1_riv)
            else:
                ax.plot(hp1, hm, 'ro', label=r'measured')
                me, mae, rmse = compute_statistics(hm, hp1)
        if calib == 'Irregular data':
            if riv:
                ax.plot(hp2_riv, hm, 'ro', label=r'measured')
                me, mae, rmse = compute_statistics(hm, hp2_riv)
            else:
                ax.plot(hp2, hm, 'ro', label=r'measured')
                me, mae, rmse = compute_statistics(hm, hp2)
        if calib == 'Irregular data with noise':
            if riv:
                ax.plot(hp3_riv, hm, 'ro', label=r'measured')
                me, mae, rmse = compute_statistics(hm, hp3_riv)
            else:
                ax.plot(hp3, hm, 'ro', label=r'measured')
                me, mae, rmse = compute_statistics(hm, hp3)
        plt.title('Scatter plot', fontsize=16)
        plt.xlabel(r'Measured head in m', fontsize=14)
        plt.ylabel(r'Computed head in m', fontsize=14)
        plt.ylim(150, hr *(1+y_scale/100))
        plt.xlim(150, hr *(1+y_scale/100))
        out_txt = '\n'.join((
                             r'$ME = %.3f$ m' % (me, ),
                             r'$MAE = %.3f$ m' % (mae, ),
                             r'$RMSE = %.3f$ m' % (rmse, ))) 
        x_pos = ((hr *(1+y_scale/100))-150)*0.25+150
        y_pos = ((hr *(1+y_scale/100))-150)*0.82+150
        plt.text(x_pos, y_pos, out_txt, horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=14)
    st.pyplot(fig)
    
    
    if calib != 'No calibration':
        lc2, cc2, rc2 = st.columns((1,1,1), gap = 'large')
        with cc2:
            show_truth = st.button(":rainbow[Tell me how I did the calibration!]")
    else:
        show_truth = False
        
    if show_truth:
        st.write("'True' Recharge R = ","% 5.2f"% (st.session_state.R_random*1000*86400*365.25), " m^2/s. Your fitting success is:  %5.2f" %(R/R_random*100), " %")
        st.write("'True' Hydr. Conductivity K = ","% 10.2E"% st.session_state.K_random, "[-].    Your fitting success is:  %5.2f" %(K/K_random*100), " %")
        if riv:
            st.write("'True' River conductance C = ","% 10.2E"% cRiv_random, "[-].    Your fitting success is:  %5.2f" %(cRiv/cRiv_random*100), " %")
    
computation()

lc3, cc3, rc3 = st.columns((1,1,1), gap = 'large')
with cc3:
    st.button('Restart with new data? Press here!')
    
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')