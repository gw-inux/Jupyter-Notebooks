import streamlit as st

st.title('📃 Theory underlying SoilWaterRetention')

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