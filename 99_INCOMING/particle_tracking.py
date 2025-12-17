import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Polygon

st.set_page_config(page_title = "iNUX - Particle Tracking", page_icon=".\FIGS\iNUX_wLogo.png")

st.title('Groundwater Particle Tracking')
st.markdown('''This app demonstrates how a conceptual particle is advected through a groundwater system by the subsurface flow field. 
            Groundwater flow at the aquifer scale is governed by Darcy’s law, 
            which relates fluid flux in porous media to hydraulic gradients and aquifer properties and forms the theoretical foundation of groundwater flow modeling (Darcy, 1856). 
            By following the trajectory of a single particle over time, the app adopts a Lagrangian particle-tracking perspective, 
            emphasizing advective transport along flow paths rather than concentration changes at fixed locations. 
            This approach is widely used to analyze groundwater travel times and flow paths under steady-state conditions, 
            for example in particle-tracking methods coupled to groundwater flow models (Pollock, 1988; Zheng & Bennett, 2002).''')

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        "x<sub>0</sub> [m]  \n"
        "<small>Location of first groundwater contact</small>",
        unsafe_allow_html=True
    )
    x0 = st.slider('',1,400,20,1)
with col2:
    st.markdown(
        "q [m/a]  \n"
        "<small>Infiltration rate</small>",
        unsafe_allow_html=True
    )
    q = st.slider('',0.1,1.0,0.3,0.01)

col3, col4 = st.columns(2)
with col3:
    st.markdown(
        "D [m]  \n"
        "<small>Average aquifer thickness</small>",
        unsafe_allow_html=True
    )
    D = st.slider('',1,80,30,1)
with col4:
    st.markdown(
        "n<sub>0</sub> [%]  \n"
        "<small>Effective porosity</small>",
        unsafe_allow_html=True
    )
    n0 = st.slider('',1,100,20,1)

col5, col6 = st. columns(2)
with col5:
    st.markdown(
    "t [a]  \n"
    "<small>Time since particle reached the groundwater table</small>",
    unsafe_allow_html=True
)
    t_set = st.slider('',0,500,20,1)


def calc_x(x0,q,t,D,n0):
    x=x0*np.exp((q*t)/(D*(n0*0.01)))
    return x

def calc_d(x0,q,t,D,n0):
    d=D*(1-np.exp(-((q*t)/(D*(n0*0.01)))))
    return d

# define values
t= np.arange(1001)

x= calc_x(x0,q,t,D,n0)
d= calc_d(x0,q,t,D,n0)


# create a plot
fig,ax=plt.subplots(figsize=(12,((D+10)/10)))

ax.spines[['bottom','right']].set_visible(False)
ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_ylim(-10,D+5)
ax.set_xlim(0,1000)
ax.invert_yaxis()


# Plot the values

ax.plot(x,d)    # graph

plt.axhspan(0,D,facecolor='b', alpha=0.3)   # groundwater body
tgl = [[900,0],[890, -2.5],[910, -2.5]] # water triangle
ax.add_patch(Polygon(tgl))
ax.hlines(0, 890, 910) #(y,x1,x2)
ax.hlines(1, 895, 905)
ax.hlines(2, 899, 901)

ax.plot(x[t_set], d[t_set], 'ro')   # marker for specific t
ax.axhline(d[t_set], linestyle=':', c='grey')
ax.axvline(x[t_set], linestyle=':', c='grey')

red_dot = mlines.Line2D([],[],color='r',marker='o',linestyle='', markersize=10,     # legent for the marker
                            label=f't={t_set} [a], d={d[t_set]:.2f} [m], x={x[t_set]:.2f} [m]')
ax.legend(handles=[red_dot], loc='upper right')
st.pyplot(fig)

st.markdown('''This work &copy; 2024 by Edith Grießer, Steffen Birk (University of Graz) is licensed under  
            <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY 4.0
            </a></p> ''', unsafe_allow_html=True)
