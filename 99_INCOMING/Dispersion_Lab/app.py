"""Standalone multipage launcher. Run: streamlit run app.py

CODE MAP — refresh with python scripts/update_code_index.py
  L0010  Module configuration / entry point
END CODE MAP
"""
import streamlit as st
from dispersion_lab.navigation import run_module

st.set_page_config(page_title="Dispersion laboratory",page_icon="💧",
                   layout=st.session_state.get("layout_choice","centered"))
run_module()
