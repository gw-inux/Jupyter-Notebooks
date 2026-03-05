import streamlit as st

# Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Grießer": [1],
}
institutions = {
    1: "Department of Earth Sciences, University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.markdown('''
        This application is built using the following resources:

        - Allen, R. G., Pereira, L. S., Raes, D., Smith, M., and others: Crop evapotranspiration-Guidelines for computing crop water requirements-FAO350 Irrigation and drainage paper 56, Fao, Rome, 300, D05 109, 1998.
        - Haude, W.: Determination of evapotranspiration by an approach as simple as possible, Mitt Dt Wetterdienst, 2, 1955.
        - Monteith, J. L.: Evaporation and environment, in: Symposia of the society for experimental biology, vol. 19, pp. 205–234, Cambridge University Press (CUP) Cambridge, 1965.
        - Oudin, L., Michel, C., and Anctil, F.: Which potential evapotranspiration input for a lumped rainfall-runoff model?, Journal of Hydrology, 303, 275–289, https://doi.org/10.1016/j.jhydrol.2004.08.025, 2005.
        - Penman, H. L.: Natural evaporation from open water, bare soil and grass, Proceedings of the Royal Society of London. Series A. Mathematicaland Physical Sciences, 193, 120–145, publisher: The Royal Society London, 1948.
         ''')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps\gw_recharge\images\CC_BY-SA_icon.png')


# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\07_About.py")
with columnsN1[1]:
    st.subheader(':blue[**Navigation**]')
