# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import streamlit as st
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here

# ---------- Track the current page
PAGE_ID = "Overview"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID

# ---------- Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# ---------- Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Grießer": [1],
}
institutions = {
    1: "Department of Earth Sciences, University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)


#---------- UI Starting here
st.title(':blue[Getting started] with Groundwater Recharge')
st.subheader('Theory, processes, and applications', divider="blue")


# --- MOTIVATION ---
st.markdown("""
#### 💡 Motivation - Groundwater Recharge

Why is the topic relevant

""")

#left_co, cent_co, last_co = st.columns((20,80,20))
#with cent_co:
#    st.image(st.session_state.module_path + 'images/GenericSaltwaterIntrusion.jpg')
#    st.markdown("""Generic illustration of before and after saltwater intrusion""")

st.markdown("""#### 🚨 Why Study It?

Understanding ...
                        
""")

st.markdown(""" 
...

#### 🎯 Learning Objectives
By the end of this module, you should be able to:

1. **Explain ...**
""")

st.subheader('🧪 Theory: ', divider='blue')
st.markdown("""

"""
)
    

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps\gw_recharge\images\CC_BY-SA_icon.png')
