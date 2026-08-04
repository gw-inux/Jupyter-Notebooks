import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from pathlib import Path
from GWP_SoilWaterRetention_utils import read_md
from GWP_SoilWaterRetention_utils import load_md
from GWP_SoilWaterRetention_utils import ui_text

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

# ------------------------------------------------------------
# Authors, institutions, and year
# ------------------------------------------------------------

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

# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

MD_DIR  = Path("90_Streamlit_apps/GWP_SoilWaterRetention_update/assets/md")

st.title(
    ui_text(
        "Welcome to the Soil Water Retention Module 💦",
        de="Willkommen zum Soil Water Retention Modul 💦",
        it="Benvenuti al modulo Soil Water Retention 💦",
        fr="Bienvenue dans le module Soil Water Retention 💦",
        es="Bienvenido al módulo Soil Water Retention 💦",
        pt="Bem-vindo ao módulo Soil Water Retention 💦",
        zh="欢迎学习土壤水分保持模块 - Soil Water Retention 💦",
    )
)

st.subheader(
    ui_text(
        "An Application Elucidating Soil Water Retention and Unsaturated Zone Hydraulics 👋",
        de="Eine Anwendung zur Veranschaulichung der Bodenwasserretention und der Hydraulik der ungesättigten Zone 👋",
        it="Un'applicazione per comprendere la ritenzione idrica del suolo e l'idraulica della zona insatura 👋",
        fr="Une application pour comprendre la rétention d'eau dans le sol et l'hydraulique de la zone non saturée 👋",
        es="Una aplicación para comprender la retención de agua en el suelo y la hidráulica de la zona no saturada 👋",
        pt="Uma aplicação para compreender a retenção de água no solo e a hidráulica da zona não saturada 👋",
        zh="一个帮助理解土壤水分保持与非饱和带水力学的应用程序 👋",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "start_01.md", st.session_state.language))

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention_update/assets/images/SW_intro.png', caption="Sketch of the underground within the unsaturated and the saturated zone.")

columns = st.columns((1,8,1))

with columns[1]:
    st.markdown(load_md(MD_DIR, "start_02.md", st.session_state.language))

st.markdown(load_md(MD_DIR, "start_03.md", st.session_state.language))


# Expander with "open in new tab"
DOC_FILE = "GWP_SoilWaterRetention_Start_example.md"
with st.expander(':rainbow[**Expand this example**]'):
    st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE}")
    st.markdown(read_md(DOC_FILE))

st.markdown('---')
left_co4, cent_co4, last_co4 = st.columns((1,8,1))
with cent_co4:
    st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time employee and over 1000 volunteers.]

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
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')
