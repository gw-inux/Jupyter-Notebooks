import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from GWP_Pumping_Test_Derivatives_utils import read_md

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
year = 2026 
authors = {
    "Thomas Reimann": [1, 2],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "The Groundwater Project",
    2: "TU Dresden, Institute for Groundwater Management"
    
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

# ------------------------------------------------------------
# USER INTERFACE
# ------------------------------------------------------------

st.title("Welcome to the Pumping Test Evaluation with Drawdown Derivatives 💦")
st.subheader('An Application ... 👋', divider= 'green')

#st.subheader('Getting started')
st.markdown("""
#### Getting started
Pumping tests ...
""")    
    
left_co, cent_co, last_co = st.columns((20, 60, 20))
with cent_co:
    st.image(
        "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/gw_logo_horiz-mini.png",
        caption=(
            "Caption"
        ),
    )
    
st.markdown("""
💡 This interactive module is designed **to deepen your understanding** of the 

💡 This module offers intuitive visualizations, conceptual explanations, and interactive tools to help bridge theory and application for .
""")

columns = st.columns((1,6,1))

with columns[1]:
    st.markdown("""
    👉 :green[**Use the sidebar to navigate through examples and aquifer types.**] 👈
    """
    )

st.subheader('How to Use this Module', divider= 'green')

st.markdown("""
A flexible resource for ....

- ***Who is this module for?*** This module is intended for ...

👉 For users who are completely new to the topic, ...

- ***Structure of the module***: ... ***Note: rectangles with a downward caret "v" expand to provide more detailed information or a self-assessment:***
""")

# Expander with "open in new tab"
DOC_FILE = "GWP_Boundary_Conditions_Start_example.md"
with st.expander(':rainbow[**Expand this example**]'):
    st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE}")
    st.markdown(read_md(DOC_FILE))

st.markdown("""
- ***Flexibility for experienced users***: Experienced users can use the module ...

- ***Time needed***: Completing the full module typically requires ...

- ***Practical focus***: Exercises and examples are embedded throughout, not only to help users understand the concepts, but also to show practical applications of ...

- ***Learning through assessments***: Each section integrates assessments to provide immediate feedback. These include short questions at the beginning to activate prior knowledge, as well as exercises and final self-checks to consolidate understanding.

- ***Instructions and exercises***: Beginners are guided step-by-step with _Initial Instructions_ that are followed by hands-on _Exercises_ to help build familiarity with each boundary condition. An **optional printable booklet** compiling all instructions and exercises from the module sections is also available for users who prefer a physical companion document alongside the app. ...
""")

st.subheader('How to Cite this Module', divider= 'green')

st.markdown("""
If you want to refer to this module, please cite as:

_...
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

# --------------------------------------------------
# Footer
# --------------------------------------------------
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
