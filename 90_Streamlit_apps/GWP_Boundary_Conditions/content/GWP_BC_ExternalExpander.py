import streamlit as st
from GWP_Boundary_Conditions_utils import read_md

st.set_page_config(page_title="Expander Content", layout="wide", initial_sidebar_state="collapsed")

doc_name = st.query_params.get("doc")

md = read_md(doc_name)

st.markdown(md)
