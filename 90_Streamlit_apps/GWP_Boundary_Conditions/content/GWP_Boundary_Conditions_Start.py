import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from GWP_Boundary_Conditions_utils import read_md

# ---------- Track the current page
PAGE_ID = "START"

if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID

# Do (optional) things/settings if the user comes from another page
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID

# ---------- Doc-only view for expanders (must run first)
params = st.query_params
DOC_VIEW = params.get("view") == "md" and params.get("doc")

if DOC_VIEW:
    md_file = params.get("doc")

    st.markdown("""
    <style>
      /* Hide sidebar & its nav */
      [data-testid="stSidebar"],
      [data-testid="stSidebarNav"] { display: none !important; }

      /* Hide the small chevron / collapse control */
      [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(read_md(md_file))
    st.stop()

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
    "Eve L. Kuniansky": [3],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines",
    3: "Retired from the US Geological Survey"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("Welcome to the Boundary Condition Module 💦")
st.subheader('An Application Elucidating Boundary Conditions in Groundwater Flow Models 👋', divider= 'green')

#st.subheader('Getting started')
st.markdown("""
#### Getting started
Groundwater models are only as good as the accuracy of both the system representation (including boundary conditions) and the values of observations used to calibrate the model.
""")

left_co, cent_co, last_co = st.columns((5,80,5))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/gwp_boundary_title.png',caption="Schematic representation of groundwater flow. Physical features of the area like the lake, stream, and pumping well are represented by boundary conditions. Figure modified from [Grannemann et al. 2000](https://mi.water.usgs.gov/pubs/WRIR/WRIR00-4008/).")
    
st.markdown("""
💡 This interactive module is designed **to deepen your understanding** of the basic ways in which different types of boundary conditions - specified head, specified flow, and head-dependent flow - influence the magnitude and direction of groundwater flow when used in solving the partial differential equation for groundwater flow. (_There is an additional [basic introduction app](https://boundary-conditions-intro.streamlit.app/) for those who are completely new to the topic._)

💡 This module offers intuitive visualizations, conceptual explanations, and interactive tools to help bridge theory and application for beginning modelers, advanced students, and practicing hydrogeologists. To get the most out of this resource, see the **How to Use this Module** section below.
""")

columns = st.columns((1,6,1))

with columns[1]:
    st.markdown("""
    👉 :green[**Use the sidebar to navigate through examples and boundary types.**] 👈
    """
    )

st.subheader('How to Use this Module', divider= 'green')

st.markdown("""
A flexible resource for both beginners and experienced groundwater modelers.

- ***Who is this module for?*** This module is intended for beginners who know a little about groundwater models and are ready to learn about boundary conditions, as well as advanced and experienced users who wish to refresh their understanding of specific boundary types. A basic familiarity with hydrogeology and groundwater flow is recommended, but no prior experience with MODFLOW is required.

👉 For users who are completely new to the topic, a separate [introductory application](https://boundary-conditions-intro.streamlit.app/) is available that provides a visual explanation of the fundamental concepts of boundary conditions before exploring their implementation in groundwater models.

- ***Structure of the module***: The :red[📕 Introduction] Section provides an overview of groundwater models and introduces the role of boundary conditions in MODFLOW. Following this, each boundary condition is presented in its own dedicated section, where the concepts, applications, and implications are explained in detail. ***Note: rectangles with a downward caret "v" expand to provide more detailed information or a self-assessment:***
""")

# Expander with "open in new tab"
DOC_FILE = "GWP_Boundary_Conditions_Start_example.md"
with st.expander(':rainbow[**Expand this example**]'):
    st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE}")
    st.markdown(read_md(DOC_FILE))

st.markdown("""
- ***Flexibility for experienced users***: Experienced users can use the module selectively, for example, by going directly to a single section of interest to refresh their knowledge of a specific boundary condition.

- ***Time needed***: Completing the full module typically requires 4-8 hours, while individual sections can be completed in 30–90 minutes depending on prior knowledge and level of detail explored.

- ***Practical focus***: Exercises and examples are embedded throughout, not only to help users understand the concepts, but also to show practical applications of the boundary conditions.

- ***Learning through assessments***: Each section integrates assessments to provide immediate feedback. These include short questions at the beginning to activate prior knowledge, as well as exercises and final self-checks to consolidate understanding.

- ***Instructions and exercises***: Beginners are guided step-by-step with _Initial Instructions_ that are followed by hands-on _Exercises_ to help build familiarity with each boundary condition. An **optional printable booklet** compiling all instructions and exercises from the module sections is also available for users who prefer a physical companion document alongside the app. [Click here to download the booklet](https://raw.githubusercontent.com/gw-inux/gw-project/main/GW_MODELING/GWP_Boundary_Conditions/docs/GWP_Boundary_Conditions_Module_Instructions_Exercises.pdf).
""")

st.subheader('How to Cite this Module', divider= 'green')

st.markdown("""
If you want to refer to this module, please cite as:

_Reimann, T., Poeter, E., & Kuniansky, E.L. (2025). Boundary Condition Module. An interactive educational resource for The Groundwater Project. Available at https://gw-project.org/interactive-education/module-boundary-conditions-for-groundwater-modeling, https://doi.org/10.5281/zenodo.17624994_.
""")
st.markdown('---')
left_co4, cent_co4, last_co4 = st.columns((1,8,1))
with cent_co4:
    st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over 1000 volunteers.]

        :green[Please help us by using the following link when sharing this tool with others.]   

        https://gw-project.org/interactive-education/

        :orange[If you find our materials useful, please donate.]   

        https://gw-project.org/donate/
        
        :blue[If you find our materials useful, please let us know by emailing webmaster@gw-project.org.]  
                 
        """   
    )

st.markdown("---")
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')
