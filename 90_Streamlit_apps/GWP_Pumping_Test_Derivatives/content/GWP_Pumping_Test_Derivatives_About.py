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
year = 2026 
authors = {
    "Thomas Reimann": [1, 2],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [1,3],
}
institutions = {
    1: "The Groundwater Project",
    2: "TU Dresden, Institute for Groundwater Management",
    3: "Colorado School of Mines" 
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]

# ------------------------------------------------------------
# Format authors
# ------------------------------------------------------------
author_list = []

for name, indices in authors.items():
    superscript = ",".join(str(i) for i in indices)
    author_list.append(f"{name}<sup>{superscript}</sup>")

# ------------------------------------------------------------
# Format institutions
# ------------------------------------------------------------
institution_list = []

for i, inst in institutions.items():
    institution_list.append(f"<sup>{i}</sup> {inst}")
institution_text = ", ".join(institution_list)

st.title('👉 About the Derivatives Module')

st.subheader('Description', divider = 'green')

st.markdown(
    """
    The Derivative Module includes interactive tools to facilitate ....
    """
)
st.subheader('Development', divider = 'green')

st.markdown(
    """
    The Derivative Module was developed by Thomas Reimann and Eileen Poeter as a Streamlit application and adapted to the Groundwater Project interactive education format. It was released in November of 2025. All Groundwater Project books are available for free download.
    """
)

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

st.subheader('Acknowledgment', divider='green')
st.markdown("""
We sincerely thank ... for the excellent and constructive feedback, which greatly helped improve the clarity and educational value of this module.""")
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
        
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png')
with columns_lic[2]:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/CC_BY-SA_icon.png')
st.markdown(
    """
    <div style="font-size:0.85em;">
    <i>
    <a href="https://gw-project.org/" target="_blank">
    The Groundwater Project
    </a>
    is a nonprofit organization with one full-time staff and over 1000 volunteers.
    Please help us by referring to
    <a href="https://gw-project.org/interactive-education/" target="_blank">
    The Groundwater Project Educational Tools
    </a>
    when sharing this app with others.
    </i>
    </div>
    """,
    unsafe_allow_html=True
)