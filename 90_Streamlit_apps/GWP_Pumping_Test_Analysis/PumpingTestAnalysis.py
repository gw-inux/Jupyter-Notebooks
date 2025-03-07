import streamlit as st


st.set_page_config(
    page_title="Pumping Test Analysis App",
    page_icon="🌀",
)

st.title("Pumping Test Analysis App 🌀")

st.sidebar.success("☝️ Select a page above ☝️")

st.header(':blue-background[Welcome 👋]')

st.markdown(
    """
    **Pumping tests** are one of the most **important methods** in hydrogeology for acquiring information about groundwater systems. A pumping test provides values of aquifer **transmissivity** $T$ and **storativity**  $S$ and in some settings, other hydraulic parameter values.
    
    This application is designed to introduce the evaluation of pumping tests for confined, unconfined, and leaky aquifers.
"""
)

st.subheader(':blue[Overview of the application]', divider="blue")

st.markdown(
    """       
    This application combines theoretical explanations with interactive applications and exercises. Quizzes inside the application allow you to assess your understanding. The underlying theory is provided as an concise overview at the beginning.
    
    :blue[First, the general response of aquifers to groundwater abstraction] is explained as a cone of water-level drawdown expanding outward from a well over time.
    
    :blue[Then we explore how pumping test data can be evaluated] to estimate hydraulic parameters such as  **transmissivity** $T$ and **storativity** $S$ for:
    - :orange[confined],
    - :green[leaky], and
    - :violet[unconfined] aquifers.
 """
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/Flow_well_confined_2.png',caption="Sketch of developing drawdown cone around an abstraction well")


st.markdown(
    """       
    Opportunities are offered to explore the evaluation methods with a few :blue[**different data sets**]
    - synthetic and idealized data that originate from **textbooks**, as well as
    - **measured** data from 
      - the Varnum test site in Sweden,
      - the Viterbo test site in Italy,
      - the Pirna test site in Germany, and
      - you can also use **your own** data.
 """
)

st.subheader(':blue[Overview and Navigation of the application]', divider="blue")
st.markdown(
    """     
    **To navigate the pumping test analysis tool you can use menu items on the sidebar to:**
    - 📃 Learn about the underlying **Theory**,
    - 🙋 Investigate **Transient flow to a well**,
    - 🟠 Understand the behavior and characteristics of the **Theis Solution for confined aquifers**,
    - 🟢 Understand the behavior and characteristics of the **Hantush-Jacob Solution for leaky aquifers**,
    - 🟣 Understand the behavior and characteristics of the **Neuman Solution for unconfined aquifers**,
    - 🎯 **Investigate measured data of your own** (or other field datasets you provide) with the Theis, Hantush-Jacob, or Neuman Solution.
    - 📈 **Explore the impact of uncertainty associated with parameter value estimates on predicted drawdown** by estimating parameters for a random dataset with noise and using the estimates for a drawdown prediction.

    This interactive application allows investigation of transient flow to a well and estimation of aquifer parameter values using the Theis, Hantush-Jacob, and Neuman Solutions for confined, leaky, and unconfined conditions. The calculations are based on spreadsheets developed by Professor Rudolf Liedl and Professor Charles R. Fitts.
    
    :green
    ___
"""
)

left_co2, cent_co2, last_co2 = st.columns((1,8,1))
with cent_co2:
    st.markdown(
    """
        :green[The Groundwater Project is a nonprofit organization with one full-time staff and over 1000 volunteers.]

        :green[Please help us by using the following link when sharing this application with others.]   

        https://interactive-education.gw-project.org/GWP_Pumping_Test_Analysis/
        """   
    )