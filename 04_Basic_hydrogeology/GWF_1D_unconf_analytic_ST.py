# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# also Interactive Documents 03-03-001
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
st.title('Analytical solution for 1D unconfined flow with two specified head boundaries')

st.subheader('Conceptual model', divider='green')
st.write('The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by two defined-head boundary conditions on the in- and outflow part. From the top, the aquifer receives uniform groundwater recharge.')
st.image('FIGS/03_03_concept_1D_flow_unconfined.png', caption="Sketch of the conceptual model.")

st.subheader('Mathematical model', divider = 'orange')
st.write('The equation for 1D groundwater flow in a homogeneous aquifer is')
st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')
st.write('with')
st.write('- _x_ is spatial coordinate along flow,')
st.write('- _h_ is hydraulic head,')
st.write('- _K_ is hydraulic conductivity,')
st.write('- _R_ is recharge.')
st.write('A solution for the equation can be obtained with two boundary conditions at _x_ = 0 and _x_ = _L_:')
st.latex(r'''h(0) = h_0''')
st.latex(r'''h(L) = h_L''')
st.write('The solution for hydraulic head _h_ along _x_ is')
st.latex(r'''h(x)=\sqrt{h_0^2-\frac{h_0^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}''')

st.subheader('Computation and visualization', divider = 'violet')
st.write('Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge _R_ (in mm/a) and the hydraulic conductivity _K_ (in m/s).')

"---"

# Input data

# Define the minimum and maximum for the logarithmic scale
log_min = -7.0 # Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # Corresponds to 10^0 = 1

columns = st.columns((1,1,1))

with columns[0]:
    with st.expander('Adjust the plot'):
        y_scale = st.slider('Scaling y-axis', 0,20,3,1)
        L= st.slider('Length', 0,7000,2500,10)


with columns[1]:
    with st.expander('Modify parameters'):
        R=st.slider('Recharge in mm/a', -500,500,0,10)
        K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        K = 10 ** K_slider_value
        # Display the logarithmic value
        st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
    
with columns[2]:
    with st.expander('Adjust the specified heads'):
            hl=st.slider('LEFT specified head', 120,180,152,1)
            hr=st.slider('RIGHT specified head', 120,180,150,1)
    
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
plt.text(L, hr*(1+y_scale/100)*0.997, 'R: {:.2e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=12)
#ax.grid()
st.pyplot(fig)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')