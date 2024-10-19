import streamlit as st

st.set_page_config(
    page_title="Well capture zone",
    page_icon="💦",
)

st.write("# WellCapture App! 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    This app is designed to introduce the computation of the well capture zone. 
    
    In a contaminated aquifer, contamination within a well cpature zone will ultimately reach the well as presented conceptually in the figure below. The Well Capture interactive tool calculates the capture area for a pumping well in a confined, homogeneous, isotropic aquifer with the following properties entered by the user.
    - hydraulic conductivity _K_ (meters per second)
    - pumping rate _Q_ (cubic meters per second)
    - regional hydraulic gradient of groundwater flow _i_ (dimensionless)
    - aquifer thickness _b_ (meters)
    
    Additional inputs allow the user to reformat the graph that displays a plan view of the capture zone. The calculated values of the culmination point and the maximum width of the capture area are printed below the graph.
"""
)
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('wellcapturediagram-sm42.png', caption="Sketch of the well capture zone; modified from Grubb(1993)")

st.markdown(
    """   
    To navigate the wellcapture tool you can use menu items at the sidebar:
    - Learn about the underlying theory
    - Run the wellcapture tool from the Green "Run WellCapture" button
    
    The online version of wellcapture is copyrighted by the author and distributed by The Groundwater Project. Please use gw-project.org links when you want to share Groundwater Project materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others
"""
)