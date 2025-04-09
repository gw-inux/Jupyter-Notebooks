import streamlit as st

st.title("Groundwater Flow and Solute Transport in Groundwater and the Vadose Zone APP! 💦")
st.header('Welcome to the FLOWTRANS_GWVZ App! 👋')

st.markdown(
    """
    Introduction and landing page text
    
    This app is designed to accompany the book Groundwater Flow and Solute Transport in Groundwater and the Vadose Zone by Ty Ferre.  
     
    The app is composed of various applications that contain demonstrations, applications, and exercises to the different book chapters. 
    
    You can access the individual topics through the sidebar menu.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/Water_Flow_Solute_Transport_GW_Vadose/assets/images/iNUX_wLogo.png')
