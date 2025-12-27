
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stodo import to_do

# Define Theis functions
def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T, S, r, t):
    return r ** 2 * S / (4. * T * t)

def theis_s(Q, T, u):
    return Q / (4. * np.pi * T) * well_function(u)

def compute_s(T, S, t, Q, r):
    return theis_s(Q, T, theis_u(T, S, r, t))

# Callback functions
def update_T():
    st.session_state.T_slider = st.session_state.T_input

def update_S():
    st.session_state.S_slider = st.session_state.S_input

def update_Q():
    st.session_state.Q_slider = st.session_state.Q_input

# Initialize defaults
if "T_slider" not in st.session_state:
    st.session_state.T_slider = -3.0
if "S_slider" not in st.session_state:
    st.session_state.S_slider = -4.0
if "Q_slider" not in st.session_state:
    st.session_state.Q_slider = 100.0  # m³/d
if "number_input" not in st.session_state:
    st.session_state.number_input = False

st.title('Dewatering exercise 💦')
st.subheader("Step 02 - Exploring Drawdown from Pumping", divider="blue")

st.session_state.number_input = st.toggle("Use number input instead of sliders")

@st.fragment
def dewatering_inputs_and_plot():
    log_min, log_max = -7.0, 0.0
    columns = st.columns((1,1), gap='large')
    with columns[0]:
        if st.session_state.number_input:
            logT = st.number_input('Log10 Transmissivity (m²/s)', log_min, log_max, st.session_state.T_slider, 0.01, format="%.2f", key="T_input", on_change=update_T)
        else:
            logT = st.slider('Log10 Transmissivity (m²/s)', log_min, log_max, st.session_state.T_slider, 0.01, format="%.2f", key="T_input", on_change=update_T)
        st.session_state.T_slider = logT
        T = 10 ** logT

        if st.session_state.number_input:
            logS = st.number_input('Log10 Storativity', log_min, log_max, st.session_state.S_slider, 0.01, format="%.2f", key="S_input", on_change=update_S)
        else:
            logS = st.slider('Log10 Storativity', log_min, log_max, st.session_state.S_slider, 0.01, format="%.2f", key="S_input", on_change=update_S)
        st.session_state.S_slider = logS
        S = 10 ** logS

        if st.session_state.number_input:
            Q_d = st.number_input('Pumping rate Q (m³/d)', 10.0, 1000.0, st.session_state.Q_slider, 10.0, format="%.0f", key="Q_input", on_change=update_Q)
        else:
            Q_d = st.slider('Pumping rate Q (m³/d)', 10., 1000., st.session_state.Q_slider, 10., format="%d", key="Q_input", on_change=update_Q)
        st.session_state.Q_slider = Q_d
        Q = Q_d / 86400.0  # convert to m³/s

        st.write("_T = %.2e m²/s | S = %.2e | Q = %.2e m³/s_" % (T, S, Q))

    with columns[1]:
        r = st.slider('Distance from well (m)', 10, 10000, 1000, 10)
        t_years = st.slider('Time (years)', 0.1, 10.0, 1.0, 0.1)
        t = t_years * 365 * 24 * 3600

    # Drawdown calculations
    t_array = np.linspace(0.1, 10, 100) * 365 * 24 * 3600
    s_array = compute_s(T, S, t_array, Q, r)
    s_at_t = compute_s(T, S, t, Q, r)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t_array / (365 * 24 * 3600), s_array, label='Drawdown over time', color='red')
    ax.plot(t / (365 * 24 * 3600), s_at_t, 'bo', label='Selected time drawdown')
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Drawdown (m)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    st.write("**Drawdown at r = %d m after %.2f years = %.2f m**" % (r, t_years, s_at_t))

dewatering_inputs_and_plot()
