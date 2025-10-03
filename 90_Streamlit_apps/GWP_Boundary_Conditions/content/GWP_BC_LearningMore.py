import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy.special
import scipy.interpolate as interp
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here

# Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)


st.title("Learning More 💦")

st.markdown(
    """
This module described how boundary conditions available in MODFLOW (in particular, head-dependent boundary conditions): :orange[**GHB:**] general head; :violet[**RIV:**] river; :green[**DRN:**] drain; :rainbow[**MNW:**] multi-node-well; and :blue[**EVT:**] evapotranspiration. Boundary conditions control the rate of flow into and out of a simulated groundwater system.
"""
) 

left_co2, cent_co2, last_co2 = st.columns((5,80,5))
with cent_co2:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/final_2.jpg',caption="View of a  catchment with spatially distributed precipitation 🌦️☀️🌈")

st.markdown(
    """
Many variations of these boundary conditions are available in groundwater flow codes. When encountering a new type of boundary condition, it is useful to think of how it performs in terms of a $Q$-$h$ plot. Variations of the boundary conditions discussed in this module are mentioned in this section to provide ideas for further study. 

For example, MODFLOW includes boundary options that are similar to the RIV boundary but allow the exchange of water to change both the boundary head and the volume of water stored in the boundary feature; and some allow for outflow from the boundary to be returned to the groundwater system in other locations within the model. These river-related conditions include the following packages and processes:
- STR, stream;
- SFR, stream-flow routing;
- DAFLOW, delayed flow; 
- LAK, lake; and
- RES, reservoir.

Also, there is an enhanced version of the DRN drain boundary conditions is the DRT - drain return flow package that allows water discharged to drains to be reintroduced to the model in other locations. 

More elaborate representation of evapotranspiration is possible by using the ETS, evapotranspiration segments package that allows the ET slope to vary with depth of the groundwater head; or the RIP riparian evapotranspiration package that allows definition of the spatial distribution of plant type and associated evapotranspiration behavior including a decrease in the rate when heads rise in cases where a high water table is detrimental to plants.

More information about MODFLOW boundary conditions can be accessed via https://ca.water.usgs.gov/modeling-software/one-water-hydrologic-model/users-manual/index.html?head_dependent_flux_boundary_p.htm.

Additional, excellent discussion of boundary conditions is provided by T.E. Reilly (2001) "System and Boundary Conceptualization in Ground-Water Flow Simulation", Techniques of Water-Resources Investigations of the U.S. Geological Survey Book 3, Applications of Hydraulics, Chapter B8. https://pubs.usgs.gov/twri/twri-3_B8/pdf/twri_3b8.pdf.
"""
) 

st.markdown('---')

left_co4, cent_co4, last_co4 = st.columns((1,8,1))
with cent_co4:
    st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over 1000 volunteers.]

        :green[Please help us by using the following link when sharing this tool with others.]   

        https://interactive-education.gw-project.org/

        :orange[If you find our materials useful, please donate.]   

        https://gw-project.org/donate/
        
        :blue[If you find our materials useful, please let us know by emailing webmaster@gw-project.org.]  
                 
        """   
    )

st.markdown("---")
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')
