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
from GWP_SoilWaterRetention_utils import ui_text

# Track the current page
PAGE_ID = "REF"

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
        "📖 References",
        de="📖 Literatur",
        it="📖 Riferimenti bibliografici",
        es="📖 Referencias",
        pt="📖 Referências",
        fr="📖 Références",
        zh="📖 参考文献",
        ar="📖 المراجع",
        hi="📖 संदर्भ",
    )
)

st.subheader(
    ":blue[" +
    ui_text(
        "used in the Soil Water Retention Module",
        de="verwendet im Soil Water Retention Modul",
        it="utilizzati nel modulo Soil Water Retention",
        es="utilizados en el móduloSoil Water Retention",
        pt="utilizados no móduloSoil Water Retention",
        fr="utilisés dans le moduleSoil Water Retention",
        zh="用于土壤水分保持模块 Soil Water Retention",
        ar="المستخدمة في وحدة احتفاظ التربة بالماء Soil Water Retention",
        hi="मृदा जल धारण मॉड्यूल Soil Water Retention में प्रयुक्त",
    ) +
    "]"
)

st.subheader(
    ui_text(
        "Books",
        de="Bücher",
        it="Libri",
        es="Libros",
        pt="Livros",
        fr="Livres",
        zh="书籍",
        ar="الكتب",
        hi="पुस्तकें",
    ),
    divider="blue",
)

st.markdown("""
    
    **Bear, J., & Cheng, A. H. D. (2010).** Modeling groundwater flow and contaminant transport (Vol. 23, p. 834). Dordrecht: Springer. (**Chapter 6:** *Unsaturated Flow Models*, p. 251).
    
    **Bear, J. (2013).** Dynamics of fluids in porous media. Courier Corporation. (**Chapter 9.4:** *Unsaturated Flow*, p. 474)
    
    **Custodio, E., & Llamas, M. R. (1983).** Hidrología subterránea. (**Chapter 8.8:** *Capilaridad y flujo multifase*, p. 553 & **Chapter 8.9:** *Movimiento del agua en los medios porosos no saturados y teoría de la infiltración*, p. 564).    

    **Freeze, R. A. & Cherry, J. A., (1979).** Groundwater (p. 370). Englewood Cliffs, NJ: Prentice-Hall.](https://gw-project.org/books/groundwater/) (**Chapter 2.6:** *Unsaturated Flow and the Water Table*, p. 38).
            
    **Stephens, D. B. (2018).** Vadose zone hydrology. CRC press.

    """)
    

st.subheader(
    ui_text(
        "Papers",
        de="Fachartikel",
        it="Articoli scientifici",
        es="Artículos científicos",
        pt="Artigos científicos",
        fr="Articles scientifiques",
        zh="科研论文",
        ar="الأوراق العلمية",
        hi="वैज्ञानिक शोध-पत्र",
    ),
    divider="blue",
)

st.markdown("""
    [**Mualem, Y. (1976).** A new model for predicting the hydraulic conductivity of unsaturated porous media. Water resources research, 12(3), 513-522.](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/WR012i003p00513).
    
    [**Van Genuchten, M. T. (1980).** A closed‐form equation for predicting the hydraulic conductivity of unsaturated soils. Soil science society of America journal, 44(5), 892-898.)](https://www.researchgate.net/publication/250125437_A_Closed-form_Equation_for_Predicting_the_Hydraulic_Conductivity_of_Unsaturated_Soils1)

"""
)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
