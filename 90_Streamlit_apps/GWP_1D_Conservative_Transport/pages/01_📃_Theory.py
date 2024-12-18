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
    ...
"""
)
st.latex(r'''x_0=\frac{Q}{2\pi Kib}''')
st.latex(r'''B=2y_{max}=\frac{Q}{Kib}''')
st.markdown(
    """
    The symbols are: _Q_ = pumping rate, _K_ = hydraulic conductivity, _i_ = hydrauic gradient, and _b_ = aquifer thickness.
    
    - each point on the flow divide can be calculated as:
"""
)

st.latex(r'''x=\frac{-y}{\tan (\frac{2 \pi Kiby}{Q})}''')

st.markdown(
    """
UPDATE  References

"""
)