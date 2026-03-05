import streamlit as st

st.markdown(
    """
    This app is part of the :blue-background[iNUX] project. 
        Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). 
        The project is funded by the ERASMUS+ program of the European Union.
"""
)

left_co, cent_co = st.columns((20,60))
with left_co:
    st.image('90_Streamlit_apps\\gw_recharge\\images\\iNUX_wLogo.png')
with cent_co:
    st.image('90_Streamlit_apps\\gw_recharge\\images\\1200px-Erasmus+_Logo.svg.png')

# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page('90_Streamlit_apps\\gw_recharge\\pages\\06_Linear_Reservoir.py')
with columnsN1[1]:
    st.subheader(':blue[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("90_Streamlit_apps\\gw_recharge\\pages\\08_References.py")
