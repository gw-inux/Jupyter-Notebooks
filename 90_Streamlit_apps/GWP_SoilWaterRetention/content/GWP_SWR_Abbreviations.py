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

# Track the current page
PAGE_ID = "ABBREV"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID
    
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
    "Eve L. Kuniansky": [3],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines",
    3: "Retired from the US Geological Survey"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("📌 Abbreviations and Parameters")
st.subheader(":blue[used in the Boundary Conditions Module]")

# Define your table rows
entries_abbrev = [
    (r"$DRN$", "MODFLOW drain boundary package"),
    (r"$ET$", "evapotranspiration"),
    (r"$EVT$", "MODFLOW evapotranspiration boundary package"),
    (r"$GHB$", "MODFLOW general head boundary package"),
    (r"$MNW$", "MODFLOW multi-node well boundary package"),
    (r"$MODFLOW$", "USGS groundwater modeling software"),
    (r"$RIV$", "MODFLOW river boundary package"),
    (r"$WEL$", "MODFLOW well boundarypackage"),
]

entries_para = [
    (r"$A$", "linear aquifer-loss coefficient"),
    (r"$A_{B}$", "area perpendicular to flow to/from the boundary"),
    (r"$B$", "linear well-loss coefficient"),
    (r"$C$", "conductance"),
    (r"$C$", "nonlinear well-loss coefficient"),
    (r"$C_{B}$", "conductance of the general-head boundary condition"),
    (r"$C_{D}$", "conductance of the drain boundary condition"),
    (r"$C_{RIV}$", "conductance of the river boundary condition"),
    (r"$CWC$", "cell to well conductance"),
    (r"$EVTR$", "maximum evapotranspiration rate"),
    (r"$EXDP$", "evapotranspiration extinction depth"),
    (r"$h$", "hydraulic head"),
    (r"$h_{bc}$", "head in the boundary condition"),
    (r"$h_{gw}$", "head in groundwater system"),
    (r"$h_{lim}$", "head in well at which $Q$ is reduced from desired $Q$"),
    (r"$h_{well}$", "head in well bore"),
    (r"$H_{B}$", "head in the general head boundary condition"),
    (r"$H_{D}$", "elevation of the drain boundary condition"),
    (r"$h_{RIV}$", "head in the river boundary condition"),
    (r"$K$", "hydraulic conductivity"),
    (r"$K_h$", "horizontal hydraulic conductivity"),
    (r"$K_v$", "vertical hydraulic conductivity"),
    (r"$L$", "length of river segment"),
    (r"$L_{B}$", "length of flow path between the boundary feature and the model"),
    (r"$M$", "thickness of riverbed sediments"),
    (r"$P$", "power (exponent) of the nonlinear discharge component of well loss"),
    (r"$Q$", "volumetric flow rate"),
    (r"$Q_{B}$", "volumetric flow rate to/from the general head boundary condition"),
    (r"$Q_{D}$", "volumetric flow rate to the drain boundary condition"),
    (r"$Q_{mn}$", "volumetric flow rate threshold at which pump is turned off"),
    (r"$Q_{mx}$", "volumetric flow rate threshold at which pump is restarted "),
    (r"$Q_{RIV}$", "volumetric flow rate to/from a river boundary condition"),
    (r"$Q-h$", "relationship between flow and head"),
    (r"$R$", "recharge rate"),
    (r"$R_{BOT}$", "elevation of the bottom of the river bed"),
    (r"$RET$", "depth-specific evapotranspiration rate"),
    (r"$SURF$", "evapotranspiration surface elevation"),
    (r"$W$", "width of river segment"),
]

# --- Table 1: Abbreviations ---
st.subheader("Abbreviations", divider='blue')
c1, c2 = st.columns([1, 3])
c1.markdown("**Abbreviation**")
c2.markdown("**Meaning**")
for abbr, meaning in entries_abbrev:
    c1, c2 = st.columns([1, 3])
    c1.markdown(abbr)
    c2.markdown(meaning)

# --- Table 2: Parameters ---
st.subheader("Parameters", divider='blue')
c1, c2 = st.columns([1, 3])
c1.markdown("**Parameter**")
c2.markdown("**Meaning**")
for abbr, meaning in entries_para:
    c1, c2 = st.columns([1, 3])
    c1.markdown(abbr)
    c2.markdown(meaning)

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
