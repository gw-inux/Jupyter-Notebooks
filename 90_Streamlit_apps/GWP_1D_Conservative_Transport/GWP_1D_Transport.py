import streamlit as st


st.set_page_config(
    page_title="'1D Transport'",
    page_icon="💦",
)

st.write("# 1D Conservative Transport App! 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    This app is designed to introduce the computation of solute transport in a steady 1D flow domain. 
     
    In an aquifer, a possible contamination will be transported along the regional groundwatre flow direction by processes like advection and hydrodynamic dispersion. The 1D Conservative Transport interactive tool calculates the break through curve for different input signals in a 1D steady flow field (i.e., representing flow in a homogeneous, isotropic aquifer).
"""
)
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/tracer_input_signals.jpg', caption="Overview about the tracer input signals that are available in the 1D Conservative Transport App.")

st.markdown (
    """
    
    The following transport related properties can be entered by the user:
    - effective porosity _n_ (dimensionless)
    - dispersivity _alpha_ (meters)
    
    Additional inputs allow the user to modify the shown plot of the break through curve and to add measured data for a calibration exercise.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/break_through_curve.jpg', caption="A breakt through curve (concentration over time) for an observation well.")

st.markdown(
    """   
    To navigate the '1D ConservativeTransport' tool you can use menu items on the sidebar:
    - Learn about the underlying theory
    - Run the 1D Conservative Transport tool from the "Run 1D Transport" button
    
    The online version of '1D ConservativeTransport' is copyrighted by the author and distributed by The Groundwater Project. Please use gw-project.org links when you want to share Groundwater Project materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others.
    
"""
)
