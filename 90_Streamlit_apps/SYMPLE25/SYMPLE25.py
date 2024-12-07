import streamlit as st


st.set_page_config(
    page_title="SYMPLE25 App",
    page_icon="💦",
)

st.sidebar.success("☝️ Select a page above. ☝️")

# OVERVIEW SECTION
symple25app = st.Page("pages/SYMPLE25APP.py", title="🌳 SYMPLE25 App")

# Orientation meeting SECTION
motivation = st.Page("pages/00_OM/Motivation_Hydrogeology.py", title="🙌 Motivation 4 Hydrogeology")
gfw_1D_unconf_rech_OM = st.Page("pages/00_OM/1D_GWF_Unconfined Recharge.py", title="📈 ▶️ Initial Model: 1D GWF")
well_capture_OM = st.Page("pages/00_OM/WellCapture.py", title="📈 ▶️ Initial Model: Well Capture")

# About Section
about = st.Page("pages/About.py", title="👉 About")

pg = st.navigation(
    {
        "💦 Overview": [symple25app],
        "🔶 Orientation meeting": [motivation, gfw_1D_unconf_rech_OM, well_capture_OM],
        "💨 General info": [about],
    }
)

pg.run()
