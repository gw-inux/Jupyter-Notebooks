import streamlit as st


st.set_page_config(
    page_title="'3D Transport'",
    page_icon="💦",
) 

st.write("# 3D Solute transport within a 1D steady state flow field 💦")

st.sidebar.success("☝️ Select a page above. ☝️")

st.header('Welcome 👋')

st.markdown(
    """
    This application is designed for educational purposes to introduce the computation of solute transport in a steady one-dimensional groundwater flow domain. 
     
    In an aquifer, a conservative solute may be transported along the regional groundwater flow direction by the processes of advection and hydrodynamic dispersion. 
    
    A conservative solute does not undergo chemical reactions nor does it attach to the medium so it moves at the same velocity as the groundwater. 
    
    :blue[The 3D Transport Application calculates the break through curve for two types of input sources with longitudinal and transversal dispersion in one-dimensional steady flow through a homogeneous porous medium.] This is representative of solute moving in an homogeneous and isotropic aquifer.
"""
)
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_3D_Transport/assets/images/tracer_input_signals.jpg', caption="Solute input options for the 3D Transport Application")

st.markdown (
    """
    
    :blue[The following transport related properties can be entered by the user:]
    - effective porosity _n_ (dimensionless)
    - longitudinal dispersivity _alpha_ (meters)
    - ratio of transversal dispersivity to longitudinal dispersivity in y- and z-direction
    
    Additional inputs allow the user to specify the source parameters and observation location.
"""
)

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('C:/_1_GitHub/Jupyter-Notebooks/90_Streamlit_apps/GWP_3D_Transport/assets/images/break_through_curve.jpg', caption="Example break through curve at a given distance from the source")

st.markdown(
    """   
     :blue[To navigate the '1D Conservative Transport' tool, you can use menu items on the sidebar:]
    - Theory for the underlying assumptions and mathematics
    - Compute Continuous Injection to calculate a 
    - Compute Finite Pulse
    - Exercise Supperposition Principle
  
"""
)

st.markdown (
    """   
    :green
    ___
  
"""
)


st.markdown(
    """
        :green[The Groundwater Project is nonprofit with one full-time staff and over a 1000 volunteers.]
        """
)
st.markdown(
    """
        :green[Please help us by using the following link when sharing this tool with others.]
        """   
)

st.markdown(
    """
        https://interactive-education.gw-project.org/1D_conservative_transport/
        """   
)

