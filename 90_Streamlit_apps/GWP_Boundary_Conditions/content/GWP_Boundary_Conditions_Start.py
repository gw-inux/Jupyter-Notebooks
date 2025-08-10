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
st.header('A Multipage Application Elucidating Boundary Conditions in Groundwater Flow Models 👋', divider= 'green')

st.subheader('Overview')
st.markdown(
    """
Groundwater models are only as accurate as their boundary conditions. This interactive module is designed to deepen your understanding of how different types of boundary conditions — defined head, defined flow, and head-dependent flow — influence groundwater flow systems.
""")

left_co, cent_co, last_co = st.columns((5,80,5))
with cent_co:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_title.png',caption="Schematic representation of groundwater flow. Physical features of the area like the lake, stream, and pumping well are represented by boundary conditions. Figure modified from [Grannemann et al. 2000](https://mi.water.usgs.gov/pubs/WRIR/WRIR00-4008/).")

st.markdown(
    """
Whether you're an advanced student or a practicing hydrogeologist, this module offers intuitive visualizations, conceptual explanations, and interactive tools to help bridge theory and application.
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
The sidebar links to sections that cover the specific boundary conditions that are available in MODFLOW, the USGS groundwater flow model:
- :orange[**GHB:**] The **General Head** Boundary package to simulate head dependent flux in or out of the model.
- :violet[**RIV:**] The **River** Boundary package to simulate head dependent flux in or out of the model.
- :green[**DRN:**] The **Drain** package to simulate head dependent flux out of the model.
- :rainbow[**MNW:**] The **Multi-Node-Well** package to simulate head dependent flux in or out of wells.
- :blue[**EVT:**] The **Evapotranspiration** package to simulate flux out of the model.
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
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')
