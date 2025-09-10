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
    **Anderson, M.P., Woessner, W.W. and Hunt, R.J. (2015).** Applied Groundwater Modeling: Simulation of Flow and Advective Transport. 2nd Edition, Academic Press, Cambridge.
    
    **Grannemann, N.G., Hunt, R.J., Nicholas, J.R., Reilly, T.E. and Winter, T.C. (2000).** The Importance of Ground Water in the Great Lakes Region: Water Resources Investigations Report 00-4008, https://mi.water.usgs.gov/pubs/WRIR/WRIR00-4008/.

    **Reilly, T.E. (2001).** System and boundary conceptualization in ground-water flow simulation. US Geological Survey Techniques of Water-Resources Investigations TWRI, book 3, chap. B8, 25p., https://pubs.usgs.gov/twri/twri-3_B8/.
    
    **Morway, E.D., Niswonger, R.G., & Triana, E. (2016).** Toward improved simulation of river operations through integration with a hydrologic model. Environmental Modelling & Software, 82, pp. 255-274. https://doi.org/10.1016/j.envsoft.2016.04.018.
    
    **Shapiro, A.D. Oki, and E. Greene (1998).** Estimating Formation Properties from Early-Time Recovery in Wells Subject to Turbulent Head Losses. Journal of Hydrology. 208. pp. 223-236. https://doi.org/10.1016/S0022-1694(98)00170-X.
"""
)

st.subheader("MODFLOW-Specific documents", divider='blue')

st.markdown("""
    
    ***MODFLOW family of codes:***
    
    **Boyce, S.E., Hanson, R.T., Ferguson, I., Schmid, W., Henson, W., Reimann, T., Mehl, S.M., and Earll, M.M. (2020).** One-Water Hydrologic Flow Model: A MODFLOW based conjunctive-use simulation software: U.S. Geological Survey Techniques and Methods 6–A60, 435 p., https://doi.org/10.3133/tm6A60.
    
    **Harbaugh, A.W. (2005).** MODFLOW-2005, The U.S. Geological Survey modular ground-water model—the Ground-Water Flow Process: U.S. Geological Survey Techniques and Methods 6-A16, https://pubs.usgs.gov/tm/2005/tm6A16/. 

    **Langevin, C.D., Hughes, J.D., Banta, E.R., Niswonger, R.G., Panday, Sorab, and Provost, A.M. (2017).** Documentation for the MODFLOW 6 Groundwater Flow Model: U.S. Geological Survey Techniques and Methods, book 6, chap. A55, 197 p., https://doi.org/10.3133/tm6A55.

    **Niswonger, R.G., Panday, S., and Ibaraki, M. (2011).** MODFLOW-NWT, A Newton formulation for MODFLOW-2005: U.S. Geological Survey Techniques and Methods 6–A37, 44 p, https://pubs.usgs.gov/tm/tm6a37/.

    **McDonald, M.G. and Harbaugh, A.W. (1988).** A modular three-dimensional finite-difference ground-water flow model. U.S. Geological Survey Techniques of Water-Resources Investigations 06-A1. https://doi.org/10.3133/twri06A1.

    
    _Dedicated documentation of advanced boundary conditions_
    
    **Banta, E.R. (2000).** MODFLOW-2000, the U.S. Geological Survey Modular Ground-Water Model - Documentation of Packages for Simulating Evapotranspiration with a Segmented Function (ETS1) and Drains with Return Flow (DRT1): U.S. Geological Survey Open-File Report 00-466, 127 p.
    
    **Fenske, J.P., Leake, S.A., and Prudic, D.E. (1996).** Documentation of a computer program (RES1) to simulate leakage from reservoirs using the modular finite-difference ground-water flow model (MODFLOW): U.S. Geological Survey Open-File Report 96-364, 51 p.
    
    **Konikow, L.F., Hornberger, G.Z., Halford, K.J., and Hanson, R.T. (2009).** Revised multi-node well (MNW2) package for MODFLOW ground-water flow model: U.S. Geological Survey Techniques and Methods 6–A30, 67 p.
    
    
    ***Other numerical model codes:***
    
    **Voss, C.I., Provost, A.M., McKenzie, J.M., & Kurylyk, B.L. (2024).** SUTRA—A code for simulation of saturated-unsaturated, variable-density groundwater flow with solute or energy transport—Documentation of the version 4.0 enhancements—Freeze-thaw capability, saturation and relative-permeability relations, spatially varying properties, and enhanced budget and velocity outputs: U.S. Geological Survey Techniques and Methods, book 6, chap. A63, 91 p., https://doi.org/10.3133/tm6A63.
    
    ***User-Interfaces and other tools for using MODFLOW:***
    
    **Winston, R.B. (2024).** Revision of ModelMuse to support the use of PEST software with MODFLOW and SUTRA models: U.S. Geological Survey Techniques and Methods book 6, chap. A64, 56 p., https://doi.org/10.3133/tm6A64.
    
    https://water.usgs.gov/nrp/gwsoftware/ModelMuse/Help/beginners_guide_to_modflow.html
    https://water.usgs.gov/nrp/gwsoftware/ModelMuse/Help/beginners_guide_to_modflow.html
"""
)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
