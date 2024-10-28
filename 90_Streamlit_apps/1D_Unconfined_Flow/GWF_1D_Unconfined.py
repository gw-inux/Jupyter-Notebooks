import streamlit as st

st.set_page_config(
    page_title="1D Groundwater flow in an unconfined aquifer with recharge",
    page_icon="💦",
)

st.write("# Welcome 👋")

st.sidebar.success("Select a step above.")

st.header('Analytical solution of the groundwater flow equation: 1D groundwater flow in an isotropic, homogenous, and unconfined aquifer 💦')

st.markdown(
    """
    This notebook is designed to demonstrate the solution of the groundwater flow equation for an idealized setup.
   

    Use the sidebar to choose the step to activate
    
    ---
"""
)


