# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
# also Interactive Documents 03-03-003
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

st.title('Analytical solution for 1D unconfined flow with one specified head boundary and one head-dependent boundary')
st.subheader('Understanding :blue[Groundwater-Surface Water Interaction]', divider="blue")

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
            y_scale = st.slider('_Scaling the y-axis of the plot_', 0,10,7,1)
        
    with columns[1]:
        with st.expander('Modify parameters'):
            # Log slider for K with input and print
            K_slider_value=st.slider('_(log of) Hydraulic conductivity input:_', log_min,log_max,-4.0,0.01,format="%4.2f" )
            K = 10 ** K_slider_value
            st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
            R = st.slider('_Recharge input:_',-400,400,0,1)
            st.write("**Recharge in mm/a:** %3i" %R)
            R = R/1000/365.25/86400
    
    with columns[2]:
        riv = st.toggle ('Head-dependent BC?')
        if riv:
            #hRiv = st.slider('River head', hr, hr+5.0, hr, 0.01)
            cRiv_slider = st.slider('_(log of) $C_{BC}$ input_', log_min2,log_max2,-5.0,0.01,format="%4.2f")
            cRiv = 10**cRiv_slider
            st.write("**$C_{BC}$:** %5.2e" %cRiv)
            hr_riv = R * L / cRiv / zb + hRiv
     
    x = np.arange(0, L, L/1000)
    
    if riv:
        phiL = 0.5 * K * (hr_riv - zb) ** 2
    else:
        phiL = 0.5 * K * (hr - zb) ** 2
    h = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L ** 2) + phiL) / K)
    
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
    # MAKE 'WATER'-TRIANGLE
    #h_arrow = zb + np.sqrt(2 * (-R / 2 * (x ** 2 - L*0.96 ** 2) + phiL) / K)  #water level at arrow
    #ax.arrow(100,150, 0.1,0.1)
    #ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
    #ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

    plt.ylim(140,hr *(1+y_scale/100))
    plt.xlim(-50,L+50)
    x_pos1 = 400
    x_pos2 = 2500
    y_pos1 = (hr *(1+y_scale/100)-140)*0.95 + 140
    plt.text(x_pos1, y_pos1, 'No Flow bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
    if riv:
        plt.text(x_pos2, y_pos1, 'Head-dependent bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='fuchsia', alpha =0.4), fontsize=12)
    else:
        plt.text(x_pos2, y_pos1, 'Specified head bc', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='deepskyblue', alpha=0.4), fontsize=12)
    
    st.pyplot(fig)
    
computation()

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')