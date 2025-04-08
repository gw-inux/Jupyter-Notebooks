import streamlit as st

st.title("Multipage App Template! 💦")
st.header('Welcome to the Multipage App Template! 👋')

st.markdown(
    """
    Introduction and landing page text
    
    This app is designed to accompany ... 
     
    The app is composed of various applications that contain demonstrations, applications, and exercises to the various lectures. The content will be updated over the course. 
    
    You can access the individual topics through the sidebar menu.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/Symple_logo.png')
