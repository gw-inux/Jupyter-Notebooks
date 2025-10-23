import streamlit as st

st.header('👉 About the SYMPLE25 App')
st.markdown(
    """
    ### Description
    The MWW01 interactive app is a collection of various educational tools for hydrogeology and groundwater management.
    
    ### Development
    Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). The iNUX project is funded by the ERASMUS+ program of the European Union.
    
    The SYMPLE25 app was developed by Thomas Reimann based on several Jupyter notebooks and adapted for the Streamlit app format. It was released in December of 2024.
    """
)

left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/MWW01/assets/images/iNUX_wLogo.png')
with cent_co2:
    st.image('90_Streamlit_apps/MWW01/assets/images/1200px-Erasmus+_Logo.svg.png')

st.markdown(
    """
    ### About the Developers
"""
)

left_co1, cent_co1 = st.columns((20,60))
with left_co1:
    st.image('90_Streamlit_apps/MWW01/assets/images/blank_profile.png')
with cent_co1:
    st.markdown(
        """
        Information about contributors.
        
        
        ... add for all contributors
        """
    )
    
left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/thomasreimann.png')
with cent_co2:
    st.markdown(
        """
        Thomas Reimann is a researcher and lecturer at the Institute for Groundwater Management at TU Dresden, Germany. With nearly 20 years of experience, Thomas’ work focus on groundwater engineering, often in combination with distributed numerical models in different environments, e.g., karst systems or open-pit mining for soft coal. He received a diploma in water management with a focus on groundwater engineering from TU Dresden in 2003. In 2012 he was promoted to Dr.-Ing. (Ph.D.) in groundwater management for research in karst systems by TU Dresden.
        
        Thomas is a specialist in applying and adapting distributed numerical models for use in research and industry. He enhanced the distributed numerical discrete-continuum model MODFLOW Conduit Flow Process (CFP) by various boundary conditions, flow- and transport processes as CFPv2. Current research projects comprise Karst system characterization with inverse groundwater modeling, groundwater management in open-pit mining environments, and Managed Aquifer Recharge.
        
        Besides research, he has been actively teaching groundwater management and groundwater modeling since 2003 at TU Dresden and as a guest lecturer for Hydrogeology since 2017 at the University of Gothenburg (Sweden). The ongoing teaching activities use various innovative digital methods to improve the learning process, which was honored by the TU Dresden teaching award in 2017.
        """
    )
