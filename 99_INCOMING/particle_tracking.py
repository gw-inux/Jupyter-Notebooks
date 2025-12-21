import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Polygon

# --- Authors, institutions, and year
year = 2025 
authors = {
    "Edith Grießer":[1],
    "Steffen Birk":[1]
    
}
institutions = {
    1: "University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.set_page_config(page_title = "iNUX - Particle Tracking", page_icon=".\FIGS\iNUX_wLogo.png")

st.title('Groundwater Particle Tracking')
st.header('Visualizing Groundwater Flow Paths and Travel Times', divider = 'green')

st.markdown("""
  This app demonstrates how a conceptual particle is advected through a groundwater system by the subsurface flow field.
  
  Groundwater flow at the aquifer scale is governed by Darcy’s law, which relates fluid flux in porous media to hydraulic gradients and aquifer properties and forms the theoretical foundation of groundwater flow modeling (Darcy, 1856).
  
  By following the trajectory of a single particle over time, the app adopts a Lagrangian particle-tracking perspective, emphasizing advective transport along flow paths rather than concentration changes at fixed locations.
  
  This approach is widely used to analyze groundwater travel times and flow paths under steady-state conditions, for example in particle-tracking methods coupled to groundwater flow models (Pollock, 1988; Zheng & Bennett, 2002).""")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    with st.expander('Particle and tracking characteristics'):
        x0 = st.slider('Position where the particle enters groundwater  \n$x_0$ (m)',1,400,20,1)
        t_set = st.slider('Time since particle reached the groundwater table  \n$t$ (years)',0,100,20,1)
with col2:
    q = st.slider('Infiltration rate (recharge)  \n$q$ (m/year)',0.1,0.4,0.2,0.01)

with col3:
    with st.expander('Aquifer characteristics'):
        D = st.slider('Average aquifer thickness  \n$b$ (m)',5,80,30,1)
        n0 = st.slider('Effective porosity  \n$n_0$ (%)',1,100,20,1)

def calc_x(x0,q,t,D,n0):
    x=x0*np.exp((q*t)/(D*(n0*0.01)))
    return x

def calc_d(x0,q,t,D,n0):
    d=D*(1-np.exp(-((q*t)/(D*(n0*0.01)))))
    return d

# define values
t = np.arange(1001)

x = calc_x(x0,q,t,D,n0)
d = calc_d(x0,q,t,D,n0)


# create a plot
fig,ax=plt.subplots(figsize=(8,5))

plt.title('Particle Tracking Visualization', fontsize=16)
plt.xlabel(r'x in m', fontsize=14)
plt.ylabel(r'aquifer thickness in m', fontsize=14)
    
ax.spines[['bottom','right']].set_visible(False)
ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_ylim(-D/10,D)
ax.set_xlim(0, 1000)
ax.invert_yaxis()

# Define y-ticks starting at 0
yticks = np.arange(0, D + 1, 5)   # change step if needed
ax.set_yticks(yticks)

# Move x-axis to aquifer bottom
ax.spines['bottom'].set_position(('data', D))

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

# X-axis only at y = D
ax.tick_params(axis='x', bottom=True, labelbottom=True,
               top=False, labeltop=False)

# Aquifer base line
ax.axhline(D, color='black', linewidth=1.5)
ax.vlines(x=0, ymin=0, ymax=D, color='black', linewidth=1.5)

# Plot the values
ax.plot(x,d)    # graph

plt.axhspan(0,D,facecolor='deepskyblue', alpha=0.3)   # groundwater body
tgl = [[100,0],[90, -D/25],[110, -D/25]] # water triangle
ax.add_patch(Polygon(tgl))
ax.hlines(0, 90, 110) #(y,x1,x2)
ax.hlines(D/100, 95, 105)
ax.hlines(D/50, 98, 102)

ax.plot(x[t_set], d[t_set], color='deeppink',marker='o')   # marker for specific t
ax.axhline(d[t_set], linestyle=':', c='grey')
ax.axvline(x[t_set], linestyle=':', c='grey')

red_dot = mlines.Line2D([],[],color='deeppink',marker='o',linestyle='', markersize=7,     # legent for the marker
                            label=f't={t_set} [years], z={d[t_set]:.2f} [m], x={x[t_set]:.2f} [m]')
ax.legend(handles=[red_dot], loc='upper right')
st.pyplot(fig)

st.markdown('---')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
