import streamlit as st


st.set_page_config(
    page_title="SYMPLE25 App",
    page_icon="💦",
)

st.sidebar.success("☝️ Select a page above. ☝️")

# 01 Overview and INTRO
mww01app    = st.Page("pages/MWW01APP.py", title="MWW01 🌳 App")
gwf1D_intro = st.Page("pages/01_Intro/1D_GWF_Unconfined Recharge_MWW01.py", title="Einführendes Modell: 1D GWF")

# 02 Conceptual model

# 03 Flow model
gwf1D_FD = st.Page("pages/03_Stroemungsmodellierung/GWF_1D_conf_FD_MWW01.py", title="1D Finite Differenzen Schema")


# 04 Transport model

trans1D_AD  = st.Page("pages/04_Transportmodellierung/Transport_1D_AD_MWW01.py", title="1D Transport mit Advektion und Dispersion")
wellcapture = st.Page("pages/04_Transportmodellierung/WellCapture_MWW01.py",     title="Brunnen EZG")

# 05 Calibration
gwf1D_calib = st.Page("pages/05_Kalibrierung/GWF_1D_unconf_analytic_calib.py", title="1D GWF Kalibrierung")
gwf1D_noflow_calib = st.Page("pages/05_Kalibrierung/GWF_1D_unconf_analytic_noflow_calib.py", title="1D GWF Kalibrierung (no flow)")

# About Section
about = st.Page("pages/About.py", title="About 👈")
about_MWW01 = st.Page("pages/About_MWW01.py", title="About MWW01 🌳")

pg = st.navigation(
    {
        "💦 Einführung und Übersicht": [mww01app, gwf1D_intro],
        "🔶 Konzeptionelles Modell": [],
        "🔶 Grundwasserströmung": [gwf1D_FD],
        "🔶 Stofftransport": [trans1D_AD,wellcapture],
        "🔶 Kalibrierung": [gwf1D_calib, gwf1D_noflow_calib],
        "🔷 General info": [about, about_MWW01],
    }
)

pg.run()
