# Copyright template

import streamlit as st
from PIL import Image

# --- Header content ---
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
   #"Colleague Name": [2],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
   #2: "Second Institution / Organization"
}
author_list = [f"{name}{''.join(f'<sup>{i}</sup>' for i in idxs)}" for name, idxs in authors.items()]
institution_text = " | ".join([f"<sup>{i}</sup> {inst}" for i, inst in institutions.items()])

# --- Footer content ---
'---'
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(
        f'Developed by {", ".join(author_list)} ({year}).<br>{institution_text}',
        unsafe_allow_html=True
    )
with columns_lic[1]:
    try:
        st.image(Image.open("FIGS/CC_BY-SA_icon.png"))
    except FileNotFoundError:
        st.image("https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/FIGS/CC_BY-SA_icon.png")