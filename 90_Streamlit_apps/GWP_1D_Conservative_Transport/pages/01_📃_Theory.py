import streamlit as st

st.title('📃 Theory underlying 1D Conservative Transport')

st.markdown(
    """
    ## The Conceptual Model for 1D Conservative Transport
    ...
"""
)
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/break_through_curve.jpg', caption="A breakt through curve (concentration over time) for an observation well.")
st.markdown(
    """
    ## The Mathematical Model for 1D Conservative Transport
    
    UPDATE
    ...
"""
)

st.latex(r'''x=\frac{-y}{\tan (\frac{2 \pi Kiby}{Q})}''')

st.markdown(
    """
UPDATE  References

"""
)