# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# also Interactive Documents 08-07-002
# ToDo:
#    - K log slider
#    - account/warn for negative heads
#    - option for specified head

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

st.title('Analytical solution for 1D unconfined flow with two specified head boundaries')
st.header('Understanding :rainbow[Model Calibration]', divider="blue")


with st.expander('Show the theory (conceptual and mathematical model)'):
    st.markdown("""
    #### Conceptual model
    
    The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by two specified-head boundary conditions on the in- and outflow part. From the top, the aquifer receives uniform groundwater recharge.
    """)
    st.image('FIGS/03_03_concept_1D_flow_unconfined.png', caption="Sketch of the conceptual model for the UNCONFINED aquifer.")
    
    st.markdown("""
    #### Mathematical model
    
    The equation for 1D groundwater flow in a homogeneous aquifer is
    """)
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')
    
    st.markdown("""
    with
    * _x_ is spatial coordinate along flow,
    * _h_ is hydraulic head,')
    * _K_ is hydraulic conductivity,')
    * _R_ is recharge.')
    
    A solution for the equation can be obtained with two boundary conditions at _x_ = 0 and _x_ = _L_:
    """)
    st.latex(r'''h(0) = h_0''')
    st.latex(r'''h(L) = h_L''')
    st.markdown("""The solution for hydraulic head _h_ along _x_ is""")
    
    st.latex(r'''h(x)=\sqrt{h_0^2-\frac{h_0^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}''')

st.subheader('Computation and visualization', divider='violet')
st.markdown("""Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge _R_ (in mm/a) and the hydraulic conductivity _K_ (in m/s).""")

# Random data for 'measurements'
K_random = 2.34E-5*(np.random.randint(5, 500)/100)
R_random = 250/1000/365.25/86400*(np.random.randint(50, 150)/100)
st.session_state.K_random = K_random
st.session_state.R_random = R_random

# Pre setting data
hl = 152
hr = 150
L = 2500
noise = 0.2
calib = 'No calibration'

# TODO - Implement the following function to add noise
def add_noise(j,noise):
    upper_value = round((i + noise/2)/ i * 100000)
    lower_value = round((i - noise/2)/ i * 100000)
    return upper_value, lower_value

# Postprocessing statistics
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
    
# Compute the measurements for calibration

#1 Regular
xp1 = [250, 500, 750, 1000, 1250, 1500, 1750,2000, 2250]
hp1 = [(hl**2-(hl**2-hr**2)/L*x+(R_random/K_random*x*(L-x)))**0.5 for x in xp1]

#2 Random x positions calib points
n_random2 = np.random.randint(3,8)
xp2 = []
for i in range(n_random2):
    xp2.append(np.random.randint(100, 2500))
hp2 = [(hl**2-(hl**2-hr**2)/L*x+(R_random/K_random*x*(L-x)))**0.5 for x in xp2]

#3 Random calib points with noise
n_random3 = np.random.randint(5,8)
xp3 = []
for i in range(n_random3):
    xp3.append(np.random.randint(100, 2500))
# Provide heads and add noise
hp3 = [((hl**2-(hl**2-hr**2)/L*x+(R_random/K_random*x*(L-x)))**0.5) for x in xp3]
hp3 = [i*np.random.randint(round((i - noise/2)/ i * 100000),round((i + noise/2)/ i * 100000))/100000 for i in hp3]

# Subsequently the computation
@st.fragment
def computation():
    # Input data
    # Define the minimum and maximum for the logarithmic scale
    log_min = -6.0 # Corresponds to 10^-7 = 0.0000001
    log_max = -2.0  # Corresponds to 10^0 = 1

    columns = st.columns((1,1,1))
    with columns[0]:
        with st.expander('Adjust the plot'):
            y_scale = st.slider('_Scaling the y-axis of the plot_', 0,20,3,1)
    
    with columns[1]:
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
            # Log slider with input and print
            # K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
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
      
    # Computation of head
    x = np.arange(0, L,L/1000)
    h=(hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5
    
    # PLOT FIGURE
    fig = plt.figure(figsize=(9,12))
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(x,h)
    if calib == 'Regular data':
        ax.plot(xp1,hp1, 'ro', label=r'measured')
        # compute heads for measurments
        hm = [((hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5) for x in xp1]
    if calib == 'Irregular data':
        ax.plot(xp2,hp2, 'go', label=r'measured')
        # compute heads for measurments
        hm = [((hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5) for x in xp2]
    if calib == 'Irregular data with noise':
        ax.plot(xp3,hp3, 'bo', label=r'measured')
        # compute heads for measurments
        hm = [((hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5) for x in xp3]
    ax.fill_between(x,0,h, facecolor='lightblue')
    plt.title('Hydraulic head for 1D unconfined flow', fontsize=16)
    plt.xlabel(r'x in m', fontsize=14)
    plt.ylabel(r'hydraulic head in m', fontsize=14)
    
    # BOUNDARY CONDITIONS hl, hr
    ax.vlines(0, 0, hl, linewidth = 10, color='b')
    ax.vlines(L, 0, hr, linewidth = 10, color='b')
    
    # MAKE 'WATER'-TRIANGLE
    h_arrow = (hl**2-(hl**2-hr**2)/L*(L*0.96)+(R/K*(L*0.96)*(L-(L*0.96))))**0.5  #water level at arrow
    ax.arrow(L*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L*0.015), head_length=(h_arrow*0.0015))
    ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
    ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

    # Groundwater divide
    max_y = max(h)
    max_x = x[h.argmax()]
    R_min_ms=K*abs(hl**2-hr**2)/L**2
    if R>R_min_ms:
        plt.vlines(max_x,0,max_y, color="r")

    plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
    plt.xlim(-50,L+50)
    x_pos1 = 550
    x_pos2 = 2500
    y_pos1 = ((hr *(1+y_scale/100))-150)*0.9+150
    plt.text(x_pos1, y_pos1, 'Specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
    plt.text(x_pos2, y_pos1, 'Specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
    
    if scatter:
        x45 = [0,200]
        y45 = [0,200]
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x45,y45, '--')
        if calib == 'Regular data':
            ax.plot(hm,hp1, 'ro', label=r'measured')
            me, mae, rmse = compute_statistics(hm, hp1)
        if calib == 'Irregular data':
            ax.plot(hm,hp2, 'go', label=r'measured')
            me, mae, rmse = compute_statistics(hm, hp2)
        if calib == 'Irregular data with noise':
            ax.plot(hm,hp3, 'bo', label=r'measured')
            me, mae, rmse = compute_statistics(hm, hp3)
        plt.title('Scatter plot', fontsize=16)
        plt.xlabel(r'Computed head in m', fontsize=14)
        plt.ylabel(r'Measured head in m', fontsize=14)
        plt.ylim(150, hr *(1+y_scale/100))
        plt.xlim(150, hr *(1+y_scale/100))
        # Generate the data for printing in the plot
        out_txt = '\n'.join((
                             r'$ME = %.3f$ m' % (me, ),
                             r'$MAE = %.3f$ m' % (mae, ),
                             r'$RMSE = %.3f$ m' % (rmse, ))) 
        x_pos3 = ((hr *(1+y_scale/100))-150)*0.25+150
        y_pos3 = ((hr *(1+y_scale/100))-150)*0.82+150
        plt.text(x_pos3, y_pos3, out_txt, horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=14)
        
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
    
computation()

lc2, cc2, rc2 = st.columns((1,1,1), gap = 'large')
with cc2:
    st.button('Restart with new data? Press here!')
    
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')