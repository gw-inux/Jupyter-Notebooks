# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container

st.title('Motivation to :blue[Study Hydrogeology and Groundwater Management]')

st.markdown(
    """
    This part of the app collects different media to underline the relevance of Hydrogeology and Groundwater Management. 
    """
)
st.header('Well capture zone for a confined aquifer', divider="orange")

if st.toggle('show video'):
    st.video('https://www.youtube.com/watch?v=I3zqpXxtsHY')