import streamlit as st

st.title('📃 Theory underlying SoilWaterRetention')

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Oriol Bertran": [2],
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
    2: "UPC Barcelona",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

st.markdown(
    """
    ## THEORY HERE
    Text / figures / formulas.
"""
)
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Well_capture/assets/images/wellcapturediagram-sm42.png', caption="Conceptual Diagram of a well capture zone; modified from Grubb(1993)")

st.markdown(
    """
    ## The Mathematical Model for WellCapture
    The full theoretical foundation for the computation can be found in a publication from Grubb (1993).
    
    The capture area of an ideal pumping well, situated at the coordinates (0,0) can be characterized by:
    - the culmination point _x0_, and
    - the maximum width of the zone within the flow divide, _B_
"""
)
st.latex(r'''x_0=\frac{Q}{2\pi Kib}''')
st.latex(r'''B=2y_{max}=\frac{Q}{Kib}''')
st.markdown(
    """
    The symbols are: _Q_ = pumping rate, _K_ = hydraulic conductivity, _i_ = hydrauic gradient, and _b_ = aquifer thickness.
    
    - each point of the flow divide can be calculated as:
"""
)
st.latex(r'''x=\frac{-y}{\tan (\frac{2 \pi Kiby}{Q})}''')

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_📈_▶️ The SWC interactive.py")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
