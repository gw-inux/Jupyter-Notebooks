import streamlit as st

st.set_page_config(
    page_title="Soil Water Retention",
    page_icon="💦",
)

st.write("# SoilWaterRetention App! :droplet:")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Oriol Bertran": [2],
    "Daniel Fernàndez-Garcia": [2]
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
    2: "UPC Universitat Politècnica de Catalunya",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

st.markdown(
    """
    This app is designed to introduce the soil water retention behavior and to describe the water distribution in the unsaturated zone. 
    """
    )

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/freeze_cherry.png', caption="Characteristic curve relating moisture content to pressure head for a naturally ocurring sand soil. Adapted from Freeze and Cherry (1979)")

st.markdown(
    """
    `Skills`

    Upon completing this app, you will be able to understand:

    - The meaning of unsaturated zone.
    - Key concepts related to transport in unsaturated soil, including surface tension, wettability, capillary pressure, and retention curves.
    - The constitutive equations that define soil-water retention curve models.
    - How the parameters defining the retention curve influence its shape and depend on soil characteristics.

    `Suggested Readings`

    **Books**:

    - [Cherry, J. A., & Freeze, R. A. (1979). Groundwater (p. 370). Englewood Cliffs, NJ: Prentice-Hall.](https://gw-project.org/books/groundwater/) (**Chapter 2.6:** *Unsaturated Flow and the Water Table*, p. 38)
    - Custodio, E., & Llamas, M. R. (1983). Hidrología subterránea. (**Chapter 8.8:** *Capilaridad y flujo multifase*, p. 553 & **Chapter 8.9:** *Movimiento del agua en los medios porosos no saturados y teoría de la infiltración*, p. 564)    - Bear, J., & Cheng, A. H. D. (2010). Modeling groundwater flow and contaminant transport (Vol. 23, p. 834). Dordrecht: Springer. (**Chapter 9.4:** *Unsaturated Flow*, p. 474)
    - Bear, J., & Cheng, A. H. D. (2010). Modeling groundwater flow and contaminant transport (Vol. 23, p. 834). Dordrecht: Springer. (**Chapter 6:** *Unsaturated Flow Models*, p. 251)
    - Bear, J. (2013). Dynamics of fluids in porous media. Courier Corporation. (**Chapter 9.4:** *Unsaturated Flow*, p. 474)
    - Stephens, D. B. (2018). Vadose zone hydrology. CRC press.
    

    **Papers**:

    - [Mualem, Y. (1976). A new model for predicting the hydraulic conductivity of unsaturated porous media. Water resources research, 12(3), 513-522.](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/WR012i003p00513)
    - [Van Genuchten, M. T. (1980). A closed‐form equation for predicting the hydraulic conductivity of unsaturated soils. Soil science society of America journal, 44(5), 892-898.)](https://www.researchgate.net/publication/250125437_A_Closed-form_Equation_for_Predicting_the_Hydraulic_Conductivity_of_Unsaturated_Soils1)
    """
)


st.markdown(
    """    
    :information_source: To navigate the soilwaterretention tool you can use menu items at the sidebar:
    - Learn about the underlying theory
    - Run the soilwaterretention tool from the different pages in the sidebar menu
"""
)

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('figs/CC_BY-SA_icon.png')
    
st.markdown('<span style="font-size: 15px;">*The online version of soilwaterretention is copyrighted by the author and distributed by* The Groundwater Project. *Please use* gw-project.org *links when you want to share* Groundwater Project *materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others.*</span>', 
            unsafe_allow_html=True)

