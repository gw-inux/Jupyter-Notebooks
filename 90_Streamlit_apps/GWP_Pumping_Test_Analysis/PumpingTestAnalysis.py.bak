import streamlit as st


st.set_page_config(
    page_title="Pumping Test Analysis",
    page_icon="💦",
)

st.write("# Pumping Test Analysis App 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    Pumping tests are one of the most important methods in Hydrogeology to achieve information and parameters of hydrogeological structures like aquifers. Accordingly, a pumping test provides the aquifers transmissivity _T_ and storativity _S_. This app is designed to introduce the evaluation of pumping tests for confined, unconfined, and leaky aquifers.
    
    First, you will understand the general reaction of aquifers on water abstraction. You will understand how the cone of drawdown develops over space and time. Then we will see how pumping test data can be evaluated. We will do this for
    - confined,
    - leaky, and
    - unconfined aquifers.
    
    And we will use different data sets
    - synthetic and idealized data that originate from textbooks,
    - measured data from the Varnum test site in Sweden,
    - measured data from the Viterbo test site in Italy,
    - measured data from the Pirna test site in Germany,
    - plus you can also use your own data.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Flow2WellTheis/assets/images/Flow_well_confined.png', caption="Sketch of the developing cone of drawdown for abstraction wells; modified from YX(XZY)")

st.markdown(
    """   
    To navigate the Pumping test analysis tool you can use menu items at the sidebar:
    - Learn about the underlying **theory**,
    - Investigate how a **confined aquifer reacts on pumping**,
    - Understand the behavior and characteristics of the **Theis solution for confined aquifers**,
    - Understand the behavior and characteristics of the **Hantush/Jacob solution for leaky aquifers**,
    - Understand the behavior and characteristics of the **Neuman solution for unconfined aquifers**,
    - Finally, **investigate real measured data (or your own dataset)** with the Theis, Hantush/Jacob, or Neuman solution.
    - At the end, an exercise allows you to understand you the effect of parameter uncertainty on predictions. For that reason, you can estimate parameters for a random dataset with noise, and use your estimate for drawdown prediction.
    
    This interactive app allows to investigate transient flow to a well with the Theis and Neuman solution. Applications involve the pumping test evaluation in confined and unconfined, transient setups. The computation is based on Spreadsheets from Prof. Rudolf Liedl and Prof. Charles R. Fitts.
    
    The online version of PumpingTestAnalysis is copyrighted by the author and distributed by The Groundwater Project. Please use gw-project.org links when you want to share Groundwater Project materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others
"""
)
