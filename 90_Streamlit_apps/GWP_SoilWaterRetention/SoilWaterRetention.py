import streamlit as st


st.set_page_config(
    page_title="Soil Water Retention",
    page_icon="💦",
)

st.write("# SoilWaterRetention App! 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    This app is designed to introduce the soil water retention behavior to describe the water distribution in soils and the unsaturated zone.computation of the well capture zone. 
     
    [Some motivation for users... The app allows to investigate the effect of parameter changes on the soil water retention:].
    - residual water content _Theta r_ (dimensionless)
    - saturated water content _Theta r_ (dimensionless)
    - alpha
    - n.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/wellcapturediagram-sm42.png', caption="Sketch of the well capture zone; modified from Grubb(1993)")

st.markdown(
    """   
    To navigate the soilwaterretention tool you can use menu items at the sidebar:
    - Learn about the underlying theory
    - Run the soilwaterretention tool from the different pages in the sidebar menu
    
    The online version of soilwaterretention is copyrighted by the author and distributed by The Groundwater Project. Please use gw-project.org links when you want to share Groundwater Project materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others
"""
)
