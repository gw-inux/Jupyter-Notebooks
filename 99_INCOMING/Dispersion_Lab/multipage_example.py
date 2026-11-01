"""Parent integration example. Run: streamlit run multipage_example.py

The parent owns page configuration and st.navigation. Import these callables
alongside the parent's other pages. Copy dispersion_lab/ and assets/ together.

CODE MAP — refresh with python scripts/update_code_index.py
  L0015  Module configuration / entry point
END CODE MAP
"""
import streamlit as st
from dispersion_lab.navigation import language_selector
from dispersion_lab.pages import overview, principles, references
from dispersion_lab.ui import render_page, render_pinboard

st.set_page_config(page_title="Teaching modules",page_icon="💧",layout="centered")
language_selector()  # Omit if the host already supplies the shared language state.
st.navigation({"Dispersion":[
    st.Page(overview,title="Overview",url_path="dispersion",default=True),
    st.Page(principles,title="Principles",url_path="dispersion-principles"),
    st.Page(render_pinboard,title="Pinboard",url_path="dispersion-pinboard"),
    st.Page(render_page,title="Explore",url_path="dispersion-explore"),
    st.Page(references,title="References",url_path="dispersion-references"),
]}).run()
