import streamlit as st


st.set_page_config(
    page_title="Soil Water Retention",
    page_icon="💦",
)

st.write("# SoilWaterRetention App! 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Oriol Bertran": [2],
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
    2: "Universitat Politècnica de Catalunya (UPC)",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

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

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
