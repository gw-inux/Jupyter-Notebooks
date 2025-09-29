import streamlit as st

# Authors, institutions, and year
year = 2025 
authors = {
    "Markus Giese": [1],  # Author 1 belongs to Institution 1
    "Thomas Reimann": [2],
    "Nils Wallenberg": [1]
}
institutions = {
    1: "University of Gothenburg, Department of Earth Sciences",
    2: "TU Dresden, Institute for Groundwater Management",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("Welcome to the Saltwater Intrusion Module 🌊➡️💧")
st.header('A Multipage Application on Saltwater Intrusion 👋', divider= 'green')

# Module path
module_path = "90_Streamlit_apps/GWP_Saltwater_Intrusion/"
#module_path = ""

st.subheader('Overview')
st.markdown(
    """
Freshwater–Saltwater Interface: Theory, Dynamics, and Management
""")

left_co, cent_co, last_co = st.columns((5,80,5))
with cent_co:
    #st.image(module_path + 'images/gwp_boundary_title.png',caption="Schematic representation of groundwater flow. Physical features of the area like the lake, stream, and pumping well are represented by boundary conditions. Figure modified from [Grannemann et al. 2000](https://mi.water.usgs.gov/pubs/WRIR/WRIR00-4008/).")
    st.markdown('Insert image')
st.markdown(
    """
Whether you're an advanced student or a practicing hydrogeologist, this module offers intuitive visualizations, conceptual explanations, and interactive tools to 
help bridge theory and application.
"""
)   

columns = st.columns((1,6,1))

with columns[1]:
    st.markdown(
    """
👉 :green[**Use the sidebar to navigate through examples and boundary types.**] 👈
"""
)
st.markdown(
    """
The sidebar links to sections that cover the specific salt water intrusion conditions that are available in...:
- :orange[**GHP:**] The **Ghyber-Herzberg Principle**.
- :violet[**SLR:**] The **Sea Level Rise** package to simulate saltwater intrusion from sea level rise.
- :green[**SWI:**] The **Upconing** package to simulate upconing from pumping.
"""
) 
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
    st.image(module_path + 'images/CC_BY-SA_icon.png')
