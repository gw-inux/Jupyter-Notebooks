# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# also Interactive Documents 03-03-002
# ToDo:
#    - K log slider
#    - account/warn for negative heads

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

st.title('Analytical solutions for 1D flow')
st.header(':blue[Unconfined] and :red[Confined] aquifer bounded by two specified head boundaries')


st.subheader('Conceptual model', divider='green')
st.write("The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by two specified-head boundary conditions on the in- and outflow part. The aquifer don't receive any groundwater recharge. The app account for an unconfined and a confined aquifer setup, as illustrated with the following figures.")

columnsfig = st.columns((1,1))

with columnsfig[0]:
    st.image('FIGS/03_03_concept_1D_flow_unconfined.png', caption="Sketch of the conceptual model for the UNCONFINED aquifer.")
with columnsfig[1]:
    st.image('FIGS/03_03_1D_confined.png', caption="Sketch of the conceptual model for the CONFINED aquifer.")

st.subheader('Mathematical model', divider = 'orange')
st.markdown("""
#### :red[Confined] Aquifer
The equation for 1D groundwater flow in a confined homogeneous aquifer is
""")
with st.expander("Click here to see the equation and solution for the confined aquifer"):
    st.latex(r'''\frac{d}{dx}(-BmK\frac{dh}{dx})=0''')
    st.markdown("""
    with
    * _x_ is spatial coordinate along flow,
    * _h_ is hydraulic head,
    * _K_ is hydraulic conductivity,
    * _m_ is the aquifer thickness,
    * _B_ is the (unit) width.
    
    A solution for the equation can be obtained with two boundary conditions at _x_ = 0 and _x_ = _L_:
    """)
    
    st.latex(r'''h(0) = h_0''')
    st.latex(r'''h(L) = h_L''')
    st.write('The solution for hydraulic head _h_ along _x_ is')
    st.latex(r'''h(x)=h_0-(h_0-h_L)\frac{x}{L}''')

st.markdown("""
#### :blue[Unconfined] Aquifer
The equation for 1D groundwater flow in an unconfined homogeneous aquifer is
""")
with st.expander("Click here to see the equation and solution for the confined aquifer"):
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')
    
    st.markdown("""
    with
    * _R_ is recharge.
    
    In the subsequent computation, the recharge is considered as _R_ = 0.
    
    A solution for the equation can be obtained with two boundary conditions at _x_ = 0 and _x_ = _L_:
    """)
    st.latex(r'''h(0) = h_0''')
    st.latex(r'''h(L) = h_L''')
    st.write('The solution for hydraulic head _h_ along _x_ is')
    st.latex(r'''h(x)=\sqrt{h_0^2-\frac{h_0^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}''')

st.subheader('Computation and visualization', divider = 'violet')
st.markdown("""Subsequently, the solution is computed and results are visualized. You can modify the hydraulic conductivity _K_ (in m/s) to investigate the functional behavior. You can further modify the hydraulic head of the left boundary and the head difference between the left and right boundary.""")

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
        K_slider_value=st.slider('(log of) hydraulic conductivity in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        K = 10 ** K_slider_value
        # Display the logarithmic value
        st.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
 
with columns[2]:
    with st.expander('Adjust the specified heads'):
            st.write('The aquifer bottom is horizontal and at 0 m.')
            hl=st.slider('LEFT specified head', 5,160,30,1)
            dh=st.slider('Head difference', 0,50,2,1)
            hr = hl-dh
    
conf = st.toggle('Show confined solution?')
        
R = 0
x = np.arange(0, L,L/1000)
h=(hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5

hconf = (hr-hl)/L * x + hl
    
# PLOT FIGURE
fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x,h,label = 'Unconfined aquifer')
if conf:
    ax.plot(x,hconf, label = 'Confined aquifer', color = 'red')
ax.set(xlabel='x', ylabel='head',title='Hydraulic head for 1D confined/unconfined flow')
ax.fill_between(x,0,h, facecolor='lightblue')
    
# BOUNDARY CONDITIONS hl, hr
ax.vlines(0, 0, hl, linewidth = 5, color='b')
ax.vlines(L, 0, hr, linewidth = 5, color='b')

#Groundwater divide
max_y = max(h)
max_x = x[h.argmax()]
R_min_ms=K*abs(hl**2-hr**2)/L**2
if R>R_min_ms:
    plt.vlines(max_x,0,max_y, color="r")

#plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
plt.ylim(0,hl*(1+y_scale/100))
plt.xlim(-20,L+20)
plt.legend(fontsize = 10)
st.pyplot(fig)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')