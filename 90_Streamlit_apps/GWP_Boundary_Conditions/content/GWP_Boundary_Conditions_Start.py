import streamlit as st

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

st.title("Welcome to the Boundary Condition Module 💦")
st.subheader('A Multipage Application Elucidating Boundary Conditions in Groundwater Flow Models 👋', divider= 'green')

#st.subheader('Getting started')
st.markdown("""
#### Getting started
Groundwater models are only as good as the accuracy of both the system representation (including boundary conditions) and the values of observations used to calibrate the model.
""")

left_co, cent_co, last_co = st.columns((5,80,5))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_title.png',caption="Schematic representation of groundwater flow. Physical features of the area like the lake, stream, and pumping well are represented by boundary conditions. Figure modified from [Grannemann et al. 2000](https://mi.water.usgs.gov/pubs/WRIR/WRIR00-4008/).")
    
st.markdown("""
💡 This interactive module is designed to deepen your understanding of the basic ways in which different types of boundary conditions - specified head, specified flow, and head-dependent flow - influence the magnitude and direction of groundwater flow when used in solving the partial differential equation for groundwater flow.

💡 This module offers intuitive visualizations, conceptual explanations, and interactive tools to help bridge theory and application for both advanced students and practicing hydrogeologists. To get the most out of this resource, see the **How to Use this Module** section below.
""")

columns = st.columns((1,6,1))

with columns[1]:
    st.markdown("""
    👉 :green[**Use the sidebar to navigate through examples and boundary types.**] 👈
    """
    )

st.subheader('How to Use this Module', divider= 'green')

st.markdown("""
A flexible resource for both beginners and experienced users of groundwater modeling.

- ***Who is it for?***: The module is intended for beginners as well as advanced and experienced users who wish to refresh their understanding of specific boundary types. A basic familiarity with hydrogeology and groundwater flow is recommended, but no prior experience with MODFLOW is required.

- ***Structure of the module***: The opening :red[📕 Introduction] Section provides an overview of groundwater models and introduces the role of boundary conditions in MODFLOW. Following this, each boundary condition is presented in its own dedicated section, where the concepts, applications, and implications are explained in detail.

- ***Flexibility for experienced users***: Experienced users can use the module selectively, for example, by going directly to a single section of interest to refresh their knowledge of a specific boundary condition.

- ***Time needed***: Completing the full module typically requires 4-8 hours, while individual sections can be completed in 15–30 minutes depending on prior knowledge and level of detail explored.

- ***Practical focus***: Exercises and examples are embedded throughout, ensuring that users not only understand the concepts but also see their application in practice.

- ***Learning through assessments***: Each section integrates assessments to provide immediate feedback. These include short questions at the beginning to activate prior knowledge, as well as exercises and final self-checks to consolidate understanding.

- ***Instructions and exercises***: Beginners are guided step by step through initial instructions and hands-on exercises that help build familiarity with each boundary condition.
""")

st.markdown('---')
left_co4, cent_co4, last_co4 = st.columns((1,8,1))
with cent_co4:
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
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')
