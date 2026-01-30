# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


st.title('Analytical solution for 1D unconfined flow with one specified head boundary/river boundary')
st.subheader('Understanding :green[Typical in- and outflows]', divider="green")

lc1, cc1, rc1 = st.columns((1,1,1), gap = 'large')
with cc1:
    theory = st.button('Show theory')
if theory:
    st.markdown("""
            ### Conceptual model
            
            The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by one specified-head boundary on the right side (left side is no flow). From the top, the aquifer receives uniform groundwater recharge.
            """, unsafe_allow_html=True)
            
    lc2, cc2, rc2 = st.columns((20,60,20))
    with cc2:
        st.image('04_Basic_hydrogeology/FIGS/GWF_008.jpg', caption="Conceptual model for a groundwater system with one no-flow boundary.")

    st.markdown("""
            ### Mathematical model
            
            The equation for 1D groundwater flow in a homogeneous aquifer is
            """, unsafe_allow_html=True)
            
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')

    st.markdown("""
            with
            - _x_ is spatial coordinate along flow,
            - _h_ is hydraulic head,
            - _K_ is hydraulic conductivity,
            - _R_ is recharge.
            
            A solution for the equation can be obtained with... TODO
            
            """, unsafe_allow_html=True)
"---"

st.subheader('Computation and visualization')
st.write('Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge _R_ (in mm/a) and the hydraulic conductivity _K_ (in m/s).')

"---"
# Fixed data
noise = 0.2
L = 2500
hr = 150.0
zb = (hr-50)
hRiv = 150

@st.fragment
def computation():
    # Input data
    # Define the minimum and maximum for the logarithmic scale
    log_min = -5.0 # Corresponds to 10^-7 = 0.0000001
    log_max = -2.0  # Corresponds to 10^0 = 1
    log_min2 = -8.0 
    log_max2 = -3.0 

    columns = st.columns((1,1,1), gap = 'large')
    with columns[0]:
        y_scale = st.slider('_Scaling the y-axis of the plot_', 0,20,3,1)
        
    with columns[1]:
        # Log slider for K with input and print
        container = st.container()
        K_slider_value=st.slider('_(log of) hydr. cond. input:_', log_min,log_max,-4.0,0.01,format="%4.2f" )
        K = 10 ** K_slider_value
        container.write("**hydr. cond. in m/s:** %5.2e" %K)
        R = st.slider('**Recharge in mm/a:**',-400,400,0,1)
        R = R/1000/365.25/86400
    with columns[2]:
        riv = st.toggle ('River BC?')
        if riv:
            #hRiv = st.slider('River head', hr, hr+5.0, hr, 0.01)
            container = st.container()
            cRiv_slider = st.slider('_(log of) CRIV input_', log_min2,log_max2,-5.0,0.01,format="%4.2f")
            cRiv = 10**cRiv_slider
            container.write("**CRIV:** %5.2e" %cRiv)
            hr_riv = R * L / cRiv / zb + hRiv
     
    x = np.arange(0, L, L/1000)
    
    if riv:
        phiL = 0.5 * K * (hr_riv - zb) ** 2
    else:
        phiL = 0.5 * K * (hr - zb) ** 2
    h = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K)
    
    Q_out = R*L*-1
    
    # PLOT FIGURE
    fig = plt.figure(figsize=(9,12))
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(x,h)
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

    plt.ylim(hr *(1-y_scale/100),hr *(1+y_scale/100))
    plt.xlim(-50,L+50)
    x_pos1 = 400
    x_pos2 = 2500
    y_pos1 = ((hr *(1+y_scale/100))-150)*0.9+150
    y_pos2 = ((hr *(1+y_scale/100))-150)*0.75+150
    plt.text(x_pos1, y_pos1, 'No Flow bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey', alpha=0.4), fontsize=12)
    if riv:
        plt.text(x_pos2, y_pos1, 'River bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey', alpha=0.4), fontsize=12)
    else:
        plt.text(x_pos2, y_pos1, 'Specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey', alpha=0.4), fontsize=12)
        plt.text(x_pos2, y_pos2, 'Q_BC: {:.2e} m³/s '.format(Q_out), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey', alpha=0.4), fontsize=12)
   
    st.pyplot(fig)
    
computation()