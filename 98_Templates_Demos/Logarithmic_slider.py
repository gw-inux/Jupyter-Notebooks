import streamlit as st
import numpy as np

st.set_page_config(page_title="Conductance Input", layout="centered")
st.title("Slider for log values")

# --- Generate log-spaced values for C
log_min = -8
log_max = -1
default_C = 1e-4
step = 0.001
log_values = np.arange(log_min, log_max + step, step)

# Input
C_values = np.power(10.0, log_values)
C_labels = [f"{c:.3e}" for c in C_values]
default_label = f"{default_C:.3e}"

# --- Slider for C (shown as labels)
container = st.container()
C_slider_label = st.select_slider("Conductance $C$ (m²/s)", C_labels, default_label)

# --- Convert back to float
C_slider_select = float(C_slider_label)

# --- Display results
container.write(f"**Conductance $C$**: {C_slider_select:.2e} m²/s")
