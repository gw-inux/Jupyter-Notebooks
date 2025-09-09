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

st.title("📖 References")
st.subheader(":blue[used in the Boundary Conditions Module]")

st.subheader("General Information and Conceptual Model", divider='blue')

st.markdown("""
    **Reilly, T. E. (2001).** System and boundary conceptualization in ground-water flow simulation. US Geological Survey Techniques of Water-Resources Investigations TWRI, book 3, chap. B8, 25p., https://pubs.usgs.gov/twri/twri-3_B8/.
"""
)

st.subheader("MODFLOW-Specific documents", divider='blue')

st.markdown("""
    
    **Anderson, M.P., Woessner, W.W. and Hunt, R.J. (2015).** Applied Groundwater Modeling: Simulation of Flow and Advective Transport. 2nd Edition, Academic Press, Cambridge.
    
    **Langevin, C.D., Hughes, J.D., Banta, E.R., Niswonger, R.G., Panday, Sorab, and Provost, A.M. (2017).** Documentation for the MODFLOW 6 Groundwater Flow Model: U.S. Geological Survey Techniques and Methods, book 6, chap. A55, 197 p., https://doi.org/10.3133/tm6A55.

    **McDonald, M.G. and Harbaugh, A.W. (1984).** A modular three-dimensional finite-difference ground-water flow model: U.S. Geological Survey Techniques Open-File Report 83-875, 528p. https://doi.org/10.3133/ofr83875.
    
    **Morway, E. D., Niswonger, R. G., & Triana, E. (2016).** Toward improved simulation of river operations through integration with a hydrologic model. Environmental Modelling & Software, 82, pp. 255-274. https://doi.org/10.1016/j.envsoft.2016.04.018.
    
    **Shapiro, A. D. Oki, and E. Greene (1998).** Estimating Formation Properties from Early-Time Recovery in Wells Subject to Turbulent Head Losses. Journal of Hydrology. 208. pp. 223-236. https://doi.org/10.1016/S0022-1694(98)00170-X.
    
    **Voss, C.I., Provost, A.M., McKenzie, J.M., & Kurylyk, B.L. (2024).** SUTRA—A code for simulation of saturated-unsaturated, variable-density groundwater flow with solute or energy transport—Documentation of the version 4.0 enhancements—Freeze-thaw capability, saturation and relative-permeability relations, spatially varying properties, and enhanced budget and velocity outputs: U.S. Geological Survey Techniques and Methods, book 6, chap. A63, 91 p., https://doi.org/10.3133/tm6A63.
"""
)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
