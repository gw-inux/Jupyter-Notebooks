import streamlit as st
import numpy as np

st.set_page_config(page_title="Logarithmic Slider Test", layout="centered")
st.title("Logarithmic Parameter Input Test")

# --- Hide floating label above thumb AND tick labels below slider
hide_elements = """
    <style>
        /* Hide value above thumb */
        div[data-baseweb="slider"] > div > div > div[role="slider"] > div {
            display: none;
        }

        /* Hide tick bar min and max labels below slider */
        div[data-testid="stSliderTickBarMin"],
        div[data-testid="stSliderTickBarMax"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)

# --- Log-scale settings
log_min = -8.0
log_max = -1.0
log_default = -4.0

# --- Slider input
log_C = st.slider("(log of) Conductance", log_min, log_max, log_default, 0.01, format="%.2f")

# --- Custom labels for physical interpretation
st.markdown("""
<div style='display: flex; justify-content: space-between; font-size: 0.85rem; padding: 0 6px 6px 6px;'>
    <span>1e-08</span>
    <span>1e-01</span>
</div>
""", unsafe_allow_html=True)

# --- Compute and display result
C = 10 ** log_C
st.markdown(f"**Conductance $C$ in m/s:** {C:.2e}")
