import streamlit as st
from streamlit_scroll_to_top import scroll_to_here

# ---------- Track the current page
PAGE_ID = "ABOUT"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID
    
# ---------- Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title('👉 About the Boundary Condition Module')

st.subheader('Description', divider = 'green')

st.markdown(
    """
    The Boundary Condition Module includes interactive tools to facilitate conceptual understanding of how different boundary types influence groundwater flow. The application uses **Q–h plots**, graphical representations of the relationship between discharge (_Q_) and hydraulic head (_h_), to illustrate the behavior of defined head, no-flow, and head-dependent flux boundaries such as surface water bodies and drains. A one-dimensional unconfined aquifer serves as an example to demonstrate how the boundary conditions control flow directions and magnitudes.
    """
)
st.subheader('Development', divider = 'green')

st.markdown(
    """
    Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). The iNUX project is funded by the ERASMUS+ program of the European Union.
    
    The Boundary Condition Module was developed by Thomas Reimann, Eileen Poeter, Eve L. Kuniansky, and the iNUX Team as a Streamlit application and adapted to the Groundwater Project interactive education format. It was released in August of 2025. All Groundwater Project books are available for free download.
    """
)
left_co1, cent_co1 = st.columns((20,60))
with left_co1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/iNUX_wLogo.png')
with cent_co1:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/1200px-Erasmus+_Logo.svg.png')

st.subheader('About the Developers', divider = 'green')
    
left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/thomasreimann.png')
with cent_co2:
    st.markdown(
        """
        :blue[**Thomas Reimann**] is a researcher and lecturer at the Institute for Groundwater Management at TU Dresden, Germany. With nearly 20 years of experience, Thomas’ work focuses on groundwater engineering, often in combination with distributed numerical models in different environments, e.g., karst systems or open-pit mining for soft coal. He received a diploma in water management with a focus on groundwater engineering from TU Dresden in 2003. In 2012 he was promoted to Dr.-Ing. (Ph.D.) in groundwater management for research in karst systems by TU Dresden.
        
        Thomas is a specialist in applying and adapting distributed numerical models for use in research and industry. He enhanced the distributed numerical discrete-continuum model MODFLOW Conduit Flow Process (CFP) with various boundary conditions, as well as flow and transport processes in CFPv2. Current research projects comprise Karst system characterization with inverse groundwater modeling, groundwater management in open-pit mining environments, and Managed Aquifer Recharge.
        
        Besides research, he has been actively teaching groundwater management and groundwater modeling since 2003 at TU Dresden and as a guest lecturer for Hydrogeology since 2017 at the University of Gothenburg (Sweden). His ongoing teaching activities use various innovative digital methods to improve the learning process, which was honored by the TU Dresden teaching award in 2017.
        """
    )
left_co3, cent_co3 = st.columns((20,60))
with left_co3:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/eileen.poeter.jpg')
with cent_co3:
    st.markdown(
        """
        :blue[**Eileen Poeter**] is a Professor Emeritus at Colorado School of Mines and a member of the Board of Directors for the Groundwater Project. She is also past director of the Integrated Groundwater Modeling Center and retired president of Poeter Engineering. 
        
        With 40 years of experience modeling groundwater systems, she has consulted to attorneys, industries, engineering companies, government agencies, research labs, and citizen groups on groundwater modeling projects for aquifer storage and recovery; slurry wall performance; drainage at proposed nuclear power plant facilities; regional groundwater management; large scale regional pumping; dam seepage;  migration; impacts of dewatering; and stream aquifer interaction.
        """
    )
left_co4, cent_co4 = st.columns((20,60))
with left_co4:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/evekuniansky.png')
with cent_co4:
    st.markdown(
        """
        :blue[**Eve Louise Kuniansky**] pursued a dual degree program graduating with a degree in Physics from Franklin and Marshall College in 1978; a Bachelor in Civil Engineering with highest honors from Georgia Institute of Technology, 1981; and a Master of Science in Civil Engineering from Georgia Institute of Technology, specializing in Hydrology/Hydraulics, 1982.
        
        In January 1983, she began a career with the United States Geological Survey (USGS) and gained experience in surface-water modeling, project management, borehole geophysics, geologic mapping, field data collection, groundwater flow and transport simulation, Geographic Information Systems, karst hydrology, and aquifer hydraulics. In 1998, she was promoted to Southeastern Region Groundwater Specialist providing technical assistance to groundwater projects throughout the southeastern USA, Puerto Rico, and the Virgin Islands. As the regional groundwater specialist, she was required to review and approve all aquifer pumping tests and groundwater flow modeling reports and archives prior to publication. Because of her expertise she was frequently selected for short term international assignments by the USGS International Water Resources Branch, serving in China, Israel, Cyprus, Ethiopia, Kenya, and South Africa.
        
        After 35 years with the USGS, she retired in December 2017 and has been volunteering for The Groundwater Project assisting with educational material about karst aquifers and groundwater modeling.
        """
    )
st.subheader('Acknowledgment', divider='green')
st.markdown("""
We sincerely thank Eve L. Kuniansky, Claire Tiedeman, Richard Winston, Rudolf Liedl, and William W. Woessner for the excellent and constructive feedback, which greatly helped improve the clarity and educational value of this module.""")
st.markdown("---")
left_co5, cent_co5, last_co5 = st.columns((1,8,1))
with cent_co5:
    st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over 1000 volunteers.]

        :green[Please help us by using the following link when sharing this tool with others.]   

        https://interactive-education.gw-project.org/

        :orange[If you find our materials useful, please donate.]   

        https://gw-project.org/donate/
        
        :blue[If you find our materials useful, please let us know by emailing webmaster@gw-project.org.]  
                 
        """   
    )
    
st.markdown("---")
# Navigation at the bottom of the side - useful for mobile phone users     
        
#columnsN1 = st.columns((1,1,1), gap = 'large')
#with columnsN1[0]:
#    if st.button("Previous page"):
#        st.switch_page("pages/07_📈_▶️ Parameter_Uncertainty.py")
#with columnsN1[1]:
#    st.subheader(':orange[**Navigation**]')
#with columnsN1[2]:
#    st.write()
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')