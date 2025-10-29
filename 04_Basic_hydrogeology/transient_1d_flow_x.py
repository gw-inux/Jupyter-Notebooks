import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc
from matplotlib.patches import Circle, Polygon, Wedge
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

st.set_page_config(page_title = "iNUX - Transient 1D Flow")
# Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Grießer": [1],
}
institutions = {
    1: "Institute of Earth Sciences, University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title('Transient one-dimensional flow')

# Parameters
col1, col2 = st.columns(2)
with col1:
    T = st.slider('T',0.1,100.,10.,0.1)
with col2:
    S = st.slider('S', 0.,0.4,0.2,0.01)

col3, col4 = st.columns(2)
with col3:
    h0 = st.slider('h0', 0.,2.5,0.5,0.01)
with col4:
    time = st.slider('t', 0,100,1,1)
h_t0=0 
t0=0

with st.expander('See parameter description'):
    st.write('''
             *T*...Transmissivity of the aquifer\n
             *S*...Storage coefficient (storativity).\n
             *h0*...The hydraulic head after the water level has risen.\n
             *t*...Time since the water level has risen
             ''')

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Define spacing
hor0 = 0 # lower boundary of the lower confining unit
hor1 = 0.8 # upper boundery of the lower confining unit = lower baoundary of the aquifer
hor2 = 3 # upper boundary of the aquifer = lower boundary of the upper confining unit
hor3 = 4 # upper boundary of the upper confining unit = lower boundary of the unconfined unit
hor4 = 8 # terraine surface
river_basin = 1
left_river_boundary = 1
right_river_boundary = 3

# Draw the aquifer layer
aquifer_x = [0, 12, 12, 0]
aquifer_y = [hor1, hor1, hor2, hor2]
ax.fill(aquifer_x, aquifer_y, color='lightsteelblue', label='Aquifer')
ax.text(10, hor1+0.2, 'aquifer', fontsize=12, color='black')

# Draw the confining layers
# Top confining layer
confining_layer_x = [0, 12, 12, 0]
confining_layer_y_top = [hor2,hor2,hor3,hor3]
ax.fill(confining_layer_x, confining_layer_y_top, color='grey', label='Confining layer (top)')
ax.text(10, hor0+0.2, 'confining layer', fontsize=12, color='black')
# Bottom confining layer
confining_layer_y_bottom = [hor0,hor0,hor1,hor1]
ax.fill(confining_layer_x, confining_layer_y_bottom, color='grey', label='Confining layer (bottom)')
ax.text(10, hor2+0.2, 'confining layer', fontsize=12, color='black')

# unconfined layer
left_wedge= Wedge((left_river_boundary-1,hor4-1),1,0,90, color='lightgrey')
ax.add_patch(left_wedge)
right_wedge= Wedge((right_river_boundary+1,hor4-1),1,90,180,color='lightgrey')
ax.add_patch(right_wedge)
left_unconf_x =(0,left_river_boundary,left_river_boundary,left_river_boundary-1,0)
left_unconf_y =(hor3,hor3,hor4-1,hor4,hor4)
ax.fill(left_unconf_x,left_unconf_y,color='lightgrey')
right_unconf_x=(right_river_boundary,12,12,right_river_boundary+1,right_river_boundary)
right_unconf_y=(hor3,hor3,hor4,hor4,hor4-1)
ax.fill_between(right_unconf_x,right_unconf_y,color='lightgrey')

# Draw the river
river_upperpart_x=[left_river_boundary,right_river_boundary,right_river_boundary,left_river_boundary]
river_upperpart_y=[hor2-1,hor2-1,h0+4.5,h0+4.5]
ax.fill(river_upperpart_x,river_upperpart_y, color='cornflowerblue', zorder=10, label='river')
r = (right_river_boundary-left_river_boundary)/2
circle = plt.Circle((left_river_boundary+r,hor2-1),r,color='cornflowerblue')
ax.add_patch(circle)
ax.text(left_river_boundary+r-0.2, hor2-1, 'river', fontsize=12, color='black', zorder=11)

# Horizontal line at initial water level h0 (at the river)
ax.hlines(h_t0+4.5, left_river_boundary, right_river_boundary, colors='blue', linestyles=':', linewidth=1.5, zorder=10)
ax.text(left_river_boundary-0.35, h0+4.5, '$h_0$', fontsize=12, zorder=10)

# Annotations for h(x, t=0)
ax.hlines(h0+4.5, left_river_boundary, right_river_boundary, colors='blue', linewidth=1.5, zorder=10)
ax.text(left_river_boundary-1, h_t0+4.5, '$h_{(x,t=0)}$', fontsize=12, zorder=10)

# Axes
ax.set_xlim(0, 12)
ax.set_ylim(0, 9.95)
ax.axis('off')


# Data
def h_edelman(x, t, T, S, h0, t0=0): 
    # Funktion to evaluate the head change after Edelman (1947)
    u = np.sqrt(S * x ** 2 / (4 * T * (t - t0)))
    return h0 * erfc(u)

def Qx_edelman(x, t, T, S, h0, t0=0):  
    # Funktion to evaluate the 1d flux after Darcy(1856) and Edelman (1947)
    u = np.sqrt(S * x ** 2 / (4 * T * (t - t0)))
    return T * h0 * 2 * u / (x * np.sqrt(np.pi)) * np.exp(-u ** 2)

x=np.linspace(1e-12, 100, 100)
h= h_edelman(x, time, T, S, h0, t0)
Qx= Qx_edelman(x, time, T, S, h0, t0)

# Create a second Coordinate System for plotting the actual data
sec_ax = inset_axes(ax,width='100%',height='100%', bbox_to_anchor=(.24,.44,.75,.25), bbox_transform=ax.transAxes, loc=3)
sec_ax.patch.set_alpha(0)
sec_ax.set_xticks([])
sec_ax.set_yticks([])
sec_ax.spines[['top','right','bottom','left']].set_visible(False)
sec_ax.set_ylim(0,2.5)
sec_ax.set_xlim(0,50)

sec_ax.plot(x, h, color='blue')
st.pyplot(fig)

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('04_Basic_hydrogeology/FIGS/CC_BY-SA_icon.png')