import streamlit as st

st.header('👉 About The Soil Water Retention Module')
st.markdown(
    """
    ### Description
    The SoilWaterRetention interactive tool calculates the water distribution in the soil and unsaturated zone.
    
    ### Development
    Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). The iNUX project is funded by the ERASMUS+ program of the European Union.
    
    SoilWaterRetention was developed by Thomas Reimann, Oriol Bertran and Daniel Fernàndez-Garcia as Jupyter notebooks and adapted to the Groundwater Project interactive education format. The computations are partially based on earlier spreadsheet tools that were developed by Prof. Rudolf Liedl. The SoilWaterRetention tool was released in November of 2024. All Groundwater Project books are available for free download.
    """
)

left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/iNUX_wLogo.png')
with cent_co2:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/1200px-Erasmus+_Logo.svg.png')

st.markdown(
    """
    ### About the Developers
"""
)

left_co1, cent_co1 = st.columns((20,60))
with left_co1:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/thomasreimann.png')
with cent_co1:
    st.markdown(
        """
        Thomas Reimann is a researcher and lecturer at the Institute for Groundwater Management at TU Dresden, Germany. With nearly 20 years of experience, Thomas’ work focus on groundwater engineering, often in combination with distributed numerical models in different environments, e.g., karst systems or open-pit mining for soft coal. He received a diploma in water management with a focus on groundwater engineering from TU Dresden in 2003. In 2012 he was promoted to Dr.-Ing. (Ph.D.) in groundwater management for research in karst systems by TU Dresden.
        
        Thomas is a specialist in applying and adapting distributed numerical models for use in research and industry. He enhanced the distributed numerical discrete-continuum model MODFLOW Conduit Flow Process (CFP) by various boundary conditions, flow- and transport processes as CFPv2. Current research projects comprise Karst system characterization with inverse groundwater modeling, groundwater management in open-pit mining environments, and Managed Aquifer Recharge.
        
        Besides research, he has been actively teaching groundwater management and groundwater modeling since 2003 at TU Dresden and as a guest lecturer for Hydrogeology since 2017 at the University of Gothenburg (Sweden). The ongoing teaching activities use various innovative digital methods to improve the learning process, which was honored by the TU Dresden teaching award in 2017.
        """
    )
    
left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/oriolbertran.jpg')
with cent_co2:
    st.markdown(
        """
        Oriol Bertran graduated as a Geologist from the Universitat de Barcelona (UB) and further specialized through the Master's in Hydrogeology at the Polytechnic University of Catalonia (UPC). Holding a PhD in the Geotechnical Engineering program at UPC's Hydrogeology Group, his research focused on studying mixing processes in heterogeneous porous media—from laboratory characterization to the design of engineered chaotic flows for practical applications in groundwater remediation. His main tasks included: (i) designing and conducting laboratory experiments followed by data processing through image analysis, and (ii) running stochastic models of groundwater flow and transport using Monte Carlo simulations.

        He is currently a researcher at UPC, where he develops tools to streamline hydrogeological data collection and analysis. His work leverages programming languages such as Python, R, SQL, and Java, along with techniques like API requests, web scraping, and machine learning. In addition to his research, Oriol actively contributes to several industry projects focused on the interaction between civil works and hydrogeology.
        """
    )

left_co3, cent_co3 = st.columns((20,60))
with left_co3:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/danielfernandez.png')
with cent_co3:
    st.markdown(
        """
        Daniel Fernàndez-Garcia is a Full Professor at the Department of Civil and Environmental Engineering at the Universitat Politècnica de Catalunya (UPC), where he plays a leading role within the Barcelona Groundwater Hydrogeology Group. With over 20 years of experience in hydrogeology, his research focuses on modeling flow and solute transport in porous media, risk analysis, and groundwater management.
        
        Daniel holds a Ph.D. degree in Environmental Science and Engineering from the Colorado School of Mines. Since he joined UPC in 2006, he has led and collaborated on numerous national and international projects related to aquifer contamination, reactive transport, artificial recharge, and climate-driven groundwater challenges. His work includes a variety of topics, such as groundwater–civil engineering interactions, multiphase and geothermal flow modelling, remediation engineering and stochastic methods and numerical modeling applied to hydrogeology. Scientific methods in his research combine mathematical and theoretical developments, numerical simulation, laboratory experiments in intermediate-scale sand boxes and field applications. Daniel’s work improve the understanding of processes such as reactive transport in porous media, seawater intrusion, and managed aquifer recharge.
        
        In addition to his research activities, Daniel has been teaching both undergraduate and graduate courses at UPC since 2006. His teaching covers a wide range of topics, from introductory hydrogeology to advanced subjects such as flow and transport modeling in porous media, soil and groundwater contamination, and the interaction between civil works and hydrogeology. Since 2020, he is also the Vice-Dean of the Civil Engineering School at UPC and, since 2011, he has been an active associate editor for Water Resources Research of the American Geophysical Union.
        """
    )

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/05_🧪_SWRC_Exercise_2.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
