import streamlit as st


st.set_page_config(
    page_title="SYMPLE25 App",
    page_icon="💦",
)

st.sidebar.success("☝️ Select a page above. ☝️")

# OVERVIEW SECTION
symple25app = st.Page("pages/SYMPLE25APP.py", title="SYMPLE25 🌳 App")

# Orientation meeting SECTION
motivation = st.Page("pages/00_OM/Motivation_Hydrogeology.py", title="Motivation 4 Hydrogeology 🌐")
gwf_1D_unconf_rech_OM = st.Page("pages/00_OM/1D_GWF_Unconfined Recharge.py", title="Initial Model: 💧 1D GWF")
well_capture_OM = st.Page("pages/00_OM/WellCapture.py", title="Initial Model: 📈 Well Capture")

#M1A - Basics
f2w_conf_unconf             = st.Page("pages/M1A/Flow2Well_transient_unconfined_confined_basics.py", title="Flow2Well: 📈 1D radial flow to wells")
heat_transport_basics         = st.Page("pages/M1A/Heat_transport_flow_1D_basics.py", title="Types of movement: 📈 Comparison heat transport and groundwater flow")
transport_1D_basics         = st.Page("pages/M1A/Transport_1D_AD_basics.py", title="Types of movement: 📈 Example of 1D transport")
gwf_1D_unconf_basics        = st.Page("pages/M1A/GWF_1D_unconf_analytic_noflow_calib_basics.py", title="Regional Hydrology: 📈 Example of 1D flow")
radio_decay                 = st.Page("pages/M1A/Radioactive_Decay_basics.py", title="Radioactive Decay: 📈 Example of a mass balance")

# M1C - Flow modeling
gwf_1D_FD                   = st.Page("pages/M1C/GWF_1D_conf_FD.py",        title="Finite Difference scheme: 📈 1D flow with 2 defined heads")
gwf_1D_unconf_calib         = st.Page("pages/Calibration/GWF_1D_unconf_analytic_calib.py",        title="Model calibration I: 📈 1D flow with 2 defined heads")
gwf_1D_unconf_no_flow_calib = st.Page("pages/Calibration/GWF_1D_unconf_analytic_noflow_calib.py", title="Model calibration II: 📈 1D flow with defined head / river")

# About Section
about = st.Page("pages/About.py", title="About 👈")
about_symple = st.Page("pages/About_SYMPLE.py", title="About SYMPLE 🌳")

pg = st.navigation(
    {
        "💦 Overview": [symple25app],
        #"🔶 Orientation meeting": [motivation, gfw_1D_unconf_rech_OM, well_capture_OM],
        "🔶 Orientation meeting": [gwf_1D_unconf_rech_OM, well_capture_OM],
        "🔶 M1A - Basics": [f2w_conf_unconf,heat_transport_basics,transport_1D_basics,gwf_1D_unconf_basics,radio_decay],
        "🔶 M1B - Data processing": [],
        "🔶 M1C - Flow modeling": [gwf_1D_FD, gwf_1D_unconf_calib, gwf_1D_unconf_no_flow_calib],
        "🔶 M1D - Transport modeling": [],
        "🔶 M1E - Model design": [],
        "🔶 M1F - Conduit Flow Process": [],
        "🔷 General info": [about, about_symple],
    }
)

pg.run()
