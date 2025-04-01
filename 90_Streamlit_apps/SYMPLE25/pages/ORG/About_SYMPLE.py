import streamlit as st

st.title("# About :green[SYMPLE] 🌳")
st.header('School of Hydrogeological Modeling', divider="green")

st.markdown(
    """
    ### The IDEA   
    The idea of founding SYMPLE stems from the experience of the Founders, who directly experienced, in the interaction with clients, colleagues and authorities, the width of the gap between hydrogeology, data processing and modelling knowledge.
    
    ### The MISSION
    To promote and facilitate the understanding, use and evaluation of groundwater models applied in engineering and environmental management, regulation and decision-making, through an exhaustive educational program associated with the development of project-related modelling strategies.
    
    More information about [Symple on the web under https://hydrosymple.com/en/](https://hydrosymple.com/en/).
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/Symple_logo.png')
