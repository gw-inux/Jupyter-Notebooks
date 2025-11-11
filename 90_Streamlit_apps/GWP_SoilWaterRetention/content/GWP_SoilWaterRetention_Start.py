import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from GWP_SoilWaterRetention_utils import read_md

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
    "Oriol Bertran": [2],
    "Daniel Fernàndez-Garcia": [2],
    "Eileen Poeter": [3]
}
institutions = {
    1: "TU Dresden",
    2: "UPC Universitat Politècnica de Catalunya",
    3: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

st.title('Welcome to the Soil Water Retention Module 💦')
st.subheader('An Application Elucidating Soil Water Retention and Unsaturated Zone Hydraulics 👋', divider='blue')

st.markdown("""#### 💡 Why is water held within soils?
When rain falls on dry ground, where does the water go? How tightly is it held by the soil? Can plants still access it — or is it lost to evaporation or drainage?

These questions are central to understanding how water behaves in the **unsaturated zone** — the part of the subsurface between the ground surface and the water table. The answers have profound implications for **agriculture**, **ecosystem resilience**, **groundwater recharge**, and our ability to **adapt to drought and climate change**.

This interactive module introduces the science behind soil water retention and helps you explore the underlying processes using the **van Genuchten–Mualem model**, one of the most widely used formulations in vadose zone hydrology.
    """
    )

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/SW_intro.png', caption="Sketch through the underground with the unsaturated and the saturated zone.")

st.markdown("""
    #### 📘 What this module covers
    
    This module explains how water is held in unsaturated soils, focusing on the **van Genuchten–Mualem model**. You’ll explore the physics of retention, interact with parameter controls, and practice interpreting and calibrating real soil data with advanced modeling concepts.
    
    The module is designed as an step by step guide for those who are new to the topic but also for those who want to refresh their knowledge.

    #### 🎯 Learning Objectives
    
    By the end of this module, you will be able to:
    
    - Understand and explain key processes governing water retention in the unsaturated zone.
    - Reflect on key concepts related to transport in unsaturated soil, including surface tension, wettability, capillary pressure, and retention curves.
    - Understand how the parameters defining the retention curve influence its shape and depend on soil characteristics.
    - Interpret and apply the van Genuchten–Mualem model.
    - Analyze how soil properties influence water content and flow.
    - Fit retention curves to observed or synthetic datasets using interactive tools.

    #### 🗂️ Module Structure
    
    - **📚 Theory**  
      Learn the fundamentals of unsaturated flow: capillary pressure, surface tension, soil water retention, and the van Genuchten–Mualem model.
    
    - **📈 The SWRC Interactive**  
      Explore how model parameters (θᵣ, θₛ, α, n) shape soil water retention curves in real time.
    
    - **📊 The SWRC in Comparison**  
      Compare water retention behavior across different soil textures (e.g., sand, loam, silt).
    
    - **🧪 SWRC Exercise 1**  
      Fit the van Genuchten model to measured retention data and interpret parameter influences on curve shape.
    
    - **🧪 SWRC Exercise 2**  
      Interpret synthetic datasets to identify soil types and evaluate agricultural suitability and flow implications.
    
    :information_source: To navigate the soilwaterretention tool you can use menu items at the sidebar"""
)


#st.subheader('Getting started')
st.markdown("""
#### Getting started
Groundwater models are only as good as the accuracy of both the system representation (including boundary conditions) and the values of observations used to calibrate the model.
""")
    
st.markdown("""
💡 This interactive module is designed **to deepen your understanding** of 

💡 This module offers intuitive visualizations, conceptual explanations, and interactive tools to help bridge theory and application for ...
""")

columns = st.columns((1,6,1))

with columns[1]:
    st.markdown("""
    👉 :green[**Use the sidebar to navigate through examples and boundary types.**] 👈
    """
    )

st.subheader('How to Use this Module', divider= 'green')

st.markdown("""
A flexible resource for both beginners and experienced ...

- ***Who is this module for?*** This module is intended for ...

- ***Structure of the module***: The ... ***Note: rectangles with a downward caret "v" expand to provide more detailed information or a self-assessment:***
""")

# Expander with "open in new tab"
DOC_FILE = "GWP_SoilWaterRetention_Start_example.md"
with st.expander(':rainbow[**Expand this example**]'):
    st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE}")
    st.markdown(read_md(DOC_FILE))

st.markdown("""
...
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
