import streamlit as st

st.header('👉 About')
st.header('The 1D Conservative Transport Application')
st.markdown(
    """
    ### Description
    The 1D Conservative Transport interactive tool calculates the break through curve for different input sources in one-dimensional, steady, uniform, groundwater flow in a homogeneous, isotropic aquifer.
    
    ### Development
    Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). The iNUX project is funded by the ERASMUS+ program of the European Union.
    
    The 1D Conservative Transport tool was developed by Thomas Reimann and Oriol Bertran as a Jupyter notebook and converted to Streamlit. Eileen Poeter enhanced and adapted it to the Groundwater Project interactive education format. It was released in Januray of 2025.
    """
)

left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/iNUX_wLogo.png')
with cent_co2:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/1200px-Erasmus+_Logo.svg.png')

st.markdown(
    """
    ### About the Developers
"""
)
left_co, cent_co = st.columns((20,60))
with left_co:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/thomasreimann.png')
with cent_co:
    st.markdown(
        """
        Thomas Reimann is a researcher and lecturer at the Institute for Groundwater Management at TU Dresden, Germany. With nearly 20 years of experience, Thomas’ work focus on groundwater engineering, often in combination with distributed numerical models in different environments, e.g., karst systems or open-pit mining for soft coal. He received a diploma in water management with a focus on groundwater engineering from TU Dresden in 2003. In 2012 he was promoted to Dr.-Ing. (Ph.D.) in groundwater management for research in karst systems by TU Dresden.
        
        Thomas is a specialist in applying and adapting distributed numerical models for use in research and industry. He enhanced the distributed numerical discrete-continuum model MODFLOW Conduit Flow Process (CFP) with various boundary conditions, as well as flow and transport processes. It is called CFPv2. Current research projects comprise Karst system characterization with inverse groundwater modeling, groundwater management in open-pit mining environments, and Managed Aquifer Recharge.
        
        Besides research, he has been actively teaching groundwater management and groundwater modeling since 2003 at Dresden University of Technology and as a guest lecturer for Hydrogeology since 2017 at the University of Gothenburg (Sweden). His ongoing teaching activities use various innovative digital methods to improve the learning process, which was honored by the Dresden University of Technology teaching award in 2017.
        
        """
    )

left_co3, cent_co3 = st.columns((20,60))
with left_co3:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/oriolbertran.jpg')
with cent_co3:
    st.markdown(
        """
        Oriol Bertran graduated as a Geologist from the Universitat de Barcelona (UB) and further specialized through the Master's in Hydrogeology at the Polytechnic University of Catalonia (UPC). Holding a PhD in the Geotechnical Engineering program at UPC's Hydrogeology Group, his research focused on studying mixing processes in heterogeneous porous media—from laboratory characterization to the design of engineered chaotic flows for practical applications in groundwater remediation. His main tasks included: (i) designing and conducting laboratory experiments followed by data processing through image analysis, and (ii) running stochastic models of groundwater flow and transport using Monte Carlo simulations.

        He is currently a researcher at UPC, where he develops tools to streamline hydrogeological data collection and analysis. His work leverages programming languages such as Python, R, SQL, and Java, along with techniques like API requests, web scraping, and machine learning. In addition to his research, Oriol is actively contributing to several industry projects involving groundwater model development.
        """
    )

left_co3, cent_co3 = st.columns((20,60))
with left_co3:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/eileen.poeter.jpg')
with cent_co3:
    st.markdown(
        """
        Eileen Poeter is a Professor Emeritus at Colorado School of Mines and a member of the Board of Directors for the Groundwater Project. She is also past director of the Integrated Groundwater Modeling Center and retired president of Poeter Engineering. With 40 years of experience modeling groundwater systems, she has consulted to attorneys, industries, engineering companies, government agencies, research labs, and citizen groups on groundwater modeling projects for aquifer storage and recovery; slurry wall performance; drainage at proposed nuclear power plant facilities; regional groundwater management; large scale regional pumping; dam seepage;  migration; impacts of dewatering; and stream aquifer interaction.
        """
    )
