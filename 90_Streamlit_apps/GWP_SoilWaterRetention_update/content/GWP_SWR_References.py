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
    ),
    divider="blue",
)

st.markdown("""
    **Anderson, M.P., Woessner, W.W. and Hunt, R.J. (2015).** Applied Groundwater Modeling: Simulation of Flow and Advective Transport. 2nd Edition, Academic Press, Cambridge.
    
    **Bear, J., & Cheng, A. H. D. (2010).** Modeling groundwater flow and contaminant transport (Vol. 23, p. 834). Dordrecht: Springer. (**Chapter 6:** *Unsaturated Flow Models*, p. 251).
    
    **Bear, J. (2013).** Dynamics of fluids in porous media. Courier Corporation. (**Chapter 9.4:** *Unsaturated Flow*, p. 474)
    
    **Custodio, E., & Llamas, M. R. (1983).** Hidrología subterránea. (**Chapter 8.8:** *Capilaridad y flujo multifase*, p. 553 & **Chapter 8.9:** *Movimiento del agua en los medios porosos no saturados y teoría de la infiltración*, p. 564).    

    **Freeze, R. A. & Cherry, J. A., (1979).** Groundwater (p. 370). Englewood Cliffs, NJ: Prentice-Hall.](https://gw-project.org/books/groundwater/) (**Chapter 2.6:** *Unsaturated Flow and the Water Table*, p. 38).

    **Grannemann, N.G., Hunt, R.J., Nicholas, J.R., Reilly, T.E. and Winter, T.C. (2000).** The Importance of Ground Water in the Great Lakes Region: Water Resources Investigations Report 00-4008, https://mi.water.usgs.gov/pubs/WRIR/WRIR00-4008/.

    **Reilly, T.E. (2001).** System and boundary conceptualization in ground-water flow simulation. US Geological Survey Techniques of Water-Resources Investigations TWRI, book 3, chap. B8, 25p., https://pubs.usgs.gov/twri/twri-3_B8/.
            
    **Stephens, D. B. (2018).** Vadose zone hydrology. CRC press.
    
    **Winter, T. C., Harvey, J. W., Franke, O. L., and Alley, W. M. (1998).** Ground water and surface water: A single resource (Circular No. 1139). US Geological Survey. https://doi.org/10.3133/cir1139
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
    ),
    divider="blue",
)

st.markdown("""
    [**Mualem, Y. (1976).** A new model for predicting the hydraulic conductivity of unsaturated porous media. Water resources research, 12(3), 513-522.](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/WR012i003p00513).
    
    [**Van Genuchten, M. T. (1980).** A closed‐form equation for predicting the hydraulic conductivity of unsaturated soils. Soil science society of America journal, 44(5), 892-898.)](https://www.researchgate.net/publication/250125437_A_Closed-form_Equation_for_Predicting_the_Hydraulic_Conductivity_of_Unsaturated_Soils1)

    **Jazayeri, A. and Werner, A.D. (2019).** Boundary Condition Nomenclature Confusion in Groundwater Flow Modeling. Groundwater. 57(5). https://doi.org/10.1016/S0022-1694(98)00170-X.

    **Morway, E.D., Niswonger, R.G., and Triana, E. (2016).** Toward improved simulation of river operations through integration with a hydrologic model. Environmental Modelling and Software, 82, pp. 255-274. https://doi.org/10.1016/j.envsoft.2016.04.018.
    
    **Shapiro, A.M., Oki, D.S., and E. Greene (1998).** Estimating Formation Properties from Early-Time Recovery in Wells Subject to Turbulent Head Losses. Journal of Hydrology. 208(3-4) pp. 223-236. https://doi.org/10.1016/S0022-1694(98)00170-X.
"""
)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
