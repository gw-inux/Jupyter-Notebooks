import streamlit as st

st.header('👉 About PumpingTestAnalysis')
st.markdown(
    """
    ### Description
    The Pumping Test Analysis interactive tool calculates the drawdown response for a pumping well in a confined, homogeneous, isotropic aquifer. Based on this, the application is designed to introduce the evaluation of pumping tests for confined, unconfined, and leaky aquifers.
    
    ### Development
    Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). The iNUX project is funded by the ERASMUS+ program of the European Union.
    
    PumpingTestAnalysis was developed by Thomas Reimann and the iNUX Team as a Streamlit app and adapted to the Groundwater Project interactive education format. It was released in February of 2025. All Groundwater Project books are available for free download.
    """
)

left_co1, cent_co1 = st.columns((20,60))
with left_co1:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/iNUX_wLogo.png')
with cent_co1:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/1200px-Erasmus+_Logo.svg.png')

st.markdown(
    """
    ### About the Developers
"""
)
    
left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/thomasreimann.png')
with cent_co2:
    st.markdown(
        """
        Thomas Reimann is a researcher and lecturer at the Institute for Groundwater Management at TU Dresden, Germany. With nearly 20 years of experience, Thomas’ work focus on groundwater engineering, often in combination with distributed numerical models in different environments, e.g., karst systems or open-pit mining for soft coal. He received a diploma in water management with a focus on groundwater engineering from TU Dresden in 2003. In 2012 he was promoted to Dr.-Ing. (Ph.D.) in groundwater management for research in karst systems by TU Dresden.
        
        Thomas is a specialist in applying and adapting distributed numerical models for use in research and industry. He enhanced the distributed numerical discrete-continuum model MODFLOW Conduit Flow Process (CFP) by various boundary conditions, flow- and transport processes as CFPv2. Current research projects comprise Karst system characterization with inverse groundwater modeling, groundwater management in open-pit mining environments, and Managed Aquifer Recharge.
        
        Besides research, he has been actively teaching groundwater management and groundwater modeling since 2003 at TU Dresden and as a guest lecturer for Hydrogeology since 2017 at the University of Gothenburg (Sweden). The ongoing teaching activities use various innovative digital methods to improve the learning process, which was honored by the TU Dresden teaching award in 2017.
        """
    )
left_co3, cent_co3 = st.columns((20,60))
with left_co3:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/eileen.poeter.jpg')
with cent_co3:
    st.markdown(
        """
        Eileen Poeter is a Professor Emeritus at Colorado School of Mines and a member of the Board of Directors for the Groundwater Project. She is also past director of the Integrated Groundwater Modeling Center and retired president of Poeter Engineering. With 40 years of experience modeling groundwater systems, she has consulted to attorneys, industries, engineering companies, government agencies, research labs, and citizen groups on groundwater modeling projects for aquifer storage and recovery; slurry wall performance; drainage at proposed nuclear power plant facilities; regional groundwater management; large scale regional pumping; dam seepage;  migration; impacts of dewatering; and stream aquifer interaction.
        """
    )
"---"
left_co4, cent_co4, last_co4 = st.columns((1,8,1))
with cent_co4:
    st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over a 1000 volunteers.]

        :green[Please help us by using the following link when sharing this tool with others.]   

        https://interactive-education.gw-project.org/GWP_Pumping_Test_Analysis/
        """   
    )
    
"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/07_📈_▶️ Parameter Uncertainty.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    st.write()
        