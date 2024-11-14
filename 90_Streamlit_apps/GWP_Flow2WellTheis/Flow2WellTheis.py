import streamlit as st


st.set_page_config(
    page_title="Flow2Well Theis",
    page_icon="💦",
)

st.write("# Flow2Well - Transient Theis App 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    This app is designed to introduce the computation of transient flow to a well in a confined aquifer. 
     
    [Motivation / reason] with the following properties entered by the user.
    - Transmissivity _T_ (square meters per second)
    - Storativity _S_
    - pumping rate _Q_ (cubic meters per second)
    
    Additional inputs allow the user to reformat the graph ...
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Flow2WellTheis/assets/images/Flow_well_confined.png', caption="Sketch of the developing cone of drawdown for abstraction wells; modified from YX(XZY)")

st.markdown(
    """   
    To navigate the Flow2Well tool you can use menu items at the sidebar:
    - Learn about the underlying theory
    - Investigate how a confined aquifer reacts on pumping
    - Estimate the parameters of an aquifer by parameter fitting
    - Estimate the parameters of real aquifers by example data sets
    - Finally, compare the reaction of confined and unconfined aquifers on pumping.
    
    The online version of Flow2Well is copyrighted by the author and distributed by The Groundwater Project. Please use gw-project.org links when you want to share Groundwater Project materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others
"""
)
