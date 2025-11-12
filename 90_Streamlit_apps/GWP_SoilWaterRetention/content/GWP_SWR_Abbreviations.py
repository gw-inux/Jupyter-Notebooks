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
    "Oriol Bertran": [2],
    "Daniel Fernàndez-Garcia": [2],
    "Eileen Poeter": [3]
}
institutions = {
    1: "TU Dresden",
    2: "UPC Universitat Politècnica de Catalunya",
    3: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

st.title("📌 Abbreviations and Parameters")
st.subheader(":blue[used in the Boundary Conditions Module]")

# Define your table rows
# Abbreviations
entries_abbrev = [
    (r"$ET$", "evapotranspiration"),
]

# Parameters
entries_para = [
    (r"$K$", "hydraulic conductivity"),
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
