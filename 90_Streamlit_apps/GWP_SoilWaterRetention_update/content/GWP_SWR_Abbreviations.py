import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy.special
import scipy.interpolate as interp
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_SoilWaterRetention_utils import load_md
from GWP_SoilWaterRetention_utils import ui_text

# Track the current page
PAGE_ID = "ABBREV"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID
    
# Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# Authors, institutions, and year
year = 2026
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

st.title(
    ui_text(
        "📌 Abbreviations and Parameters",
        de="📌 Abkürzungen und Parameter",
        it="📌 Abbreviazioni e parametri",
        es="📌 Abreviaturas y parámetros",
        pt="📌 Abreviações e parâmetros",
        fr="📌 Abréviations et paramètres",
        zh="📌 缩略语与参数",
        ar="📌 الاختصارات والمعلمات",
        hi="📌 संक्षिप्ताक्षर और पैरामीटर",
    )
)

st.subheader(
    ":blue[" +
    ui_text(
        "used in the Soil Water Retention Module",
        de="verwendet im Modul Bodenwasserretention",
        it="utilizzati nel modulo sulla ritenzione idrica del suolo",
        es="utilizados en el módulo de retención de agua en el suelo",
        pt="utilizados no módulo de retenção de água no solo",
        fr="utilisés dans le module sur la rétention d'eau dans le sol",
        zh="用于土壤水分保持模块",
        ar="المستخدمة في وحدة احتفاظ التربة بالماء",
        hi="मृदा जल धारण मॉड्यूल में प्रयुक्त",
    ) +
    "]"
)

# Define your table rows
# Abbreviations
entries_abbrev = [
    (r"$AWC$", "available water capacity"),
    (r"$eFC$", "effective field capacity; here defined as the difference between field capacity and permanent wilting point"),
    (r"$FC$", "field capacity"),
    (r"$PWP$", "permanent wilting point"),
    (r"$SWRC$", "soil water retention curve"),
    (r"$VG$", "van Genuchten model"),
    (r"$VGM$", "van Genuchten–Mualem model"),
]

# Parameters
entries_para = [
    (r"$\alpha$", "van Genuchten parameter related to the inverse of the air-entry suction"),
    (r"$D(\Theta)$", "describes how quickly moisture redistributes in soil (essentially, the ratio of effective hydraulic conductivity and dimensionless water content = hydraulic diffusivity as a function of effective saturation / dimensionless water content)"),
    (r"$h$", "pressure head or suction head, depending on the sign convention used in the plot"),
    (r"$h_c$", "capillary rise or capillary pressure head"),
    (r"$i$", "index for a fluid or material phase"),
    (r"$k$", "index for a fluid or material phase"),
    (r"$K_r$", "relative hydraulic conductivity"),
    (r"$k_r$", "relative permeability; used synonymously with relative hydraulic conductivity when normalized by saturated conductivity"),
    (r"$K_s$", "saturated hydraulic conductivity"),
    (r"$m$", r"van Genuchten model exponent, commonly defined as $m = 1 - \frac{1}{n}$"),
    (r"$n$", "van Genuchten pore-size distribution parameter controlling the steepness of the retention curve"),
    (r"$P_c$", "capillary pressure or capillary suction"),
    (r"$r$", "pore or meniscus radius"),
    (r"$V_t$", "total volume of the soil sample or representative elementary volume"),
    (r"$V_w$", "volume of water"),
    (r"$W_{ik}$", "work required to separate two phases or substances and create interfacial area"),
    (r"$\sigma$", "surface tension"),
    (r"$\sigma_{GL}$", "gas–liquid surface tension"),
    (r"$\sigma_{SG}$", "solid–gas surface tension"),
    (r"$\sigma_{SL}$", "solid–liquid surface tension"),
    (r"$\sigma_{ik}$", "interfacial tension between phases or substances i and k"),
    (r"$\theta$", "volumetric water content"),
    (r"$\Theta$", "effective saturation or dimensionless water content"),
    (r"$\theta_r$", "residual volumetric water content"),
    (r"$\theta_s$", "saturated volumetric water content"),
    (r"$\theta_{fc}$", "volumetric water content at field capacity"),
    (r"$\theta_w$", "volumetric water content; water content of the wetting phase"),
    (r"$\theta_{wp}$", "volumetric water content at the permanent wilting point"),
    (r"$\psi$", "matric potential or suction head"),
]

# --- Table 1: Abbreviations ---
st.subheader(
    ui_text(
        "Abbreviations",
        de="Abkürzungen",
        it="Abbreviazioni",
        es="Abreviaturas",
        pt="Abreviações",
        fr="Abréviations",
        zh="缩略语",
        ar="الاختصارات",
        hi="संक्षिप्ताक्षर",
    ),
    divider="blue",
)
c1, c2 = st.columns([1, 3])
c1.markdown("**Abbreviation**")
c2.markdown("**Meaning**")
for abbr, meaning in entries_abbrev:
    c1, c2 = st.columns([1, 3])
    c1.markdown(abbr)
    c2.markdown(meaning)

# --- Table 2: Parameters ---
st.subheader(
    ui_text(
        "Parameters",
        de="Parameter",
        it="Parametri",
        es="Parámetros",
        pt="Parâmetros",
        fr="Paramètres",
        zh="参数",
        ar="المعلمات",
        hi="पैरामीटर",
    ),
    divider="blue",
)
c1, c2 = st.columns([1, 3])
c1.markdown("**Parameter**")
c2.markdown("**Meaning**")
for abbr, meaning in entries_para:
    c1, c2 = st.columns([1, 3])
    c1.markdown(abbr)
    c2.markdown(meaning)

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
