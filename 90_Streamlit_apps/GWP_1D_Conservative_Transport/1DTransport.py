import streamlit as st


st.set_page_config(
    page_title="1D Transport",
    page_icon="💦",
)

st.write("# 1D Conservative Transport App! 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    This app is designed to introduce the computation of solute transport in a steady 1D flow domain. 
     
    In an aquifer, a possible contamination will be transported along the regional groundwatre flow direction by processes like advection and hydrodynamic dispersion. The 1D Conservative Transport interactive tool calculates the break through curve for a block input in a 1D steady flow field (i.e., representing flow in a homogeneous, isotropic aquifer). The following properties can be entered by the user.
    - effective porosity _n_ (dimensionless)
    - dispersivity _alpha_ (meters)
    
    Additional inputs allow the user to modify the shown plot and to add measured data.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/wellcapturediagram-sm42.png', caption="Sketch of the well capture zone; modified from Grubb(1993)")

st.markdown(
    """   
    To navigate the '1D ConservativeTransport' tool you can use menu items on the sidebar:
    - Learn about the underlying theory
    - Run the 1D Conservative Transport tool from the "Run 1D Transport" button
    
    The online version of '1D ConservativeTransport' is copyrighted by the author and distributed by The Groundwater Project. Please use gw-project.org links when you want to share Groundwater Project materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others.
    
"""
)
