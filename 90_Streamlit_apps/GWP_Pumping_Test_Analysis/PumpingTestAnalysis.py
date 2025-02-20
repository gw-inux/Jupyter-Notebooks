import streamlit as st


st.set_page_config(
    page_title="Pumping Test Analysis",
    page_icon="💦",
)

st.write("# Pumping Test Analysis Application 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    Pumping tests are one of the most important methods in hydrogeology for acquiring information about groundwater systems. A pumping test provides values of aquifer transmissivity _T_ and storativity _S_. This application is designed to introduce the evaluation of pumping tests for confined, unconfined, and leaky aquifers.
"""
)



st.markdown(
    """       
    First, the general response of aquifers to groundwater abstraction is explained as a cone of water-level drawdown expanding outward from a well over time. 
 """
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/Flow_well_confined_2.png', caption="Sketch of developing drawdown cone around an abstraction well")


st.markdown(
    """    
    Then we explore how pumping test data can be evaluated to estimate hydraulic parameters such as  transmissivity _T_ and storativity _S_ for:
    - confined,
    - leaky, and
    - unconfined aquifers.
    
    We will use a few different data sets
    - synthetic and idealized data that originate from textbooks,
    - measured data from the Varnum test site in Sweden,
    - measured data from the Viterbo test site in Italy,
    - measured data from the Pirna test site in Germany,
    - and you can also use your own data.


    **To navigate the pumping test analysis tool you can use menu items on the sidebar:**
    - Learn about the underlying **Theory**,
    - Investigate **Transient flow to a well**,
    - Understand the behavior and characteristics of the **Theis solution for confined aquifers**,
    - Understand the behavior and characteristics of the **Hantush/Jacob solution for leaky aquifers**,
    - Understand the behavior and characteristics of the **Neuman solution for unconfined aquifers**,
    - **Investigate measured data of your own** with the Theis, Hantush/Jacob, or Neuman solution.
    - **Explore the impact of uncertainty associated with parameter values estimates on predicted drawdown**, by estimating parameters for a random dataset with noise and using the estimates for a drawdown prediction.
"""
)


st.markdown(
    """
    This interactive application allows investigation of transient flow to a well and estimation of aquifer parameter values using the Theis and Neuman solutions for confined and unconfined conditions, respectively. The calculations are based on spreadsheets developed by Professor Rudolf Liedl and Professor Charles R. Fitts, respectively.
    """
)

st.markdown (
    """   
    :green
    ___
"""
)


st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over a 1000 volunteers.]
        """
)
st.markdown(
    """
        :green[Please help us by using the following link when sharing this tool with others.]
        """   
)

st.markdown(
    """
        https://interactive-education.gw-project.org/GWP_Pumping_Test_Analysis/
        """   
)
