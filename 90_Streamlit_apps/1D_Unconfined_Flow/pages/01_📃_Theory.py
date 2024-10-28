import streamlit as st

st.title('📃 Theory underlying 1D Groundwater Flow in unconfined aquifers with recharge')

st.markdown(
    """
    ## The Conceptual Model
"""
)
left_co, cent_co, last_co = st.columns((5,60,5))
with cent_co:
    st.image('90_Streamlit_apps/1D_Unconfined_Flow/assets/images/concept_1D_flow_unconfined.png', caption="Sketch of the situation")

st.markdown(
    """
    ## The Mathematical Model 
"""
)
st.latex(r'''h=stuff''')
st.markdown(
    """
    The symbols are: _h_ = hydraulic head 
"""
)
