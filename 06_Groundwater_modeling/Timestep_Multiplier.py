import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

def generate_time_steps(total_time, dt0, multiplier):
    """
    Generates time step locations based on the initial step and multiplier.
    """
    time = 0
    time_steps = [time]
    while time < total_time:
        dt = dt0 * (multiplier ** len(time_steps))
        if time + dt > total_time:
            break
        time += dt
        time_steps.append(time)
    return np.array(time_steps)

def modflow_time_steps(perlen, nstp, tsmult):
    """
    Generates time step locations based on the MODFLOW formula.
    """
    if tsmult == 1.0:
        dt0 = perlen / nstp  # Equal time steps if TSMULT = 1
    else:
        dt0 = perlen * (tsmult - 1) / (tsmult ** nstp - 1)
    
    time_steps = [0]
    dt = dt0
    for _ in range(nstp):
        time_steps.append(time_steps[-1] + dt)
        dt *= tsmult
    
    return np.array(time_steps)

# Streamlit UI
st.title("MODFLOW Time Step Multiplier Illustration")

st.subheader('Theory and Functionality of the App')

st.markdown("""
    This Streamlit app illustrates the effect of **time step multipliers** in **MODFLOW** and general **geometric progression-based time stepping**. The **time step multiplier** controls how the length of successive time steps increases within a stress period, balancing computational efficiency and numerical accuracy.
    
    The app provides **two approaches** for time step generation:
    
    1. **Geometric Progression (Variant 1)** – The user defines the **initial time step** and **multiplier**. Time steps grow geometrically until reaching the total simulation time.
    
    2. **MODFLOW Formula (Variant 2)** – The user specifies the **stress period length**, **number of time steps**, and **multiplier**. The first time step is computed using the **analytical MODFLOW equation**, and subsequent time steps follow an increasing pattern.
    
    Both variants include a **reference case** with a **multiplier of 1**, ensuring constant time steps for comparison. The results are visualized as scatter plots, and key numerical values (number of time steps, initial time step size) are displayed within each plot.
            """)

st.header("Variant 1: :blue[Set the initial time step size]")
st.write('This approach is for example in MODELMUSE available')


with st.expander('**Open the interactive calculator** for variant 2 by :green[clicking here]'):
    col1, col2, col3 = st.columns(3)
    with col1:
        perlen1 = st.number_input("Stress Period Length (PERLEN)", min_value=1, value=86400, step=60, key = 10)
    with col2:
        dt0 = st.number_input("Initial Time Step $dt_0$", min_value=1, value=1800, step=60)
    with col3:
        tsmult1 = st.slider("Time Step Multiplier (TSMULT)", min_value=1.0, max_value=2.0, value=1.0, step=0.01, key = 20)
    
    steps_v1 = generate_time_steps(perlen1, dt0, tsmult1)
    steps_v1_fixed = generate_time_steps(perlen1, dt0, 1.0)
    fig1, ax1 = plt.subplots(figsize=(8, 2))
    ax1.scatter(steps_v1_fixed, np.ones_like(steps_v1_fixed), color='gray', label='TSMULT = 1 (Constant dt)')
    ax1.scatter(steps_v1, np.ones_like(steps_v1) * 1.1, color='blue', label=f'TSMULT = {tsmult1}')
    ax1.set_xlim(0, perlen1)
    ax1.set_xlabel("Time")
    ax1.set_yticks([])
    ax1.legend()
    ax1.set_title("Time Step Distribution (Geometric Progression)")
    ax1.grid(True, linestyle='--', alpha=0.6)
    num_steps_v1 = len(steps_v1)
    num_steps_v1_fixed = len(steps_v1_fixed)
    
    st.pyplot(fig1)
    
    columns2 = st.columns((1,1), gap = 'medium')
    with columns2[0]:
        st.write('Number of time steps with multiplier', tsmult1, " = ", num_steps_v1)
    with columns2[1]:
        st.write('Number of time steps with multiplier 1.0 = ', num_steps_v1_fixed)
    
st.header("Variant 2: :green[Set the number of time steps]")
st.write('This approach is in the MODFLOW DIS input integrated')

with st.expander('**Open the interactive calculator** for variant 2 by :green[clicking here]'):
    col4, col5, col6 = st.columns(3)
    with col4:
        perlen2 = st.number_input("Stress Period Length (PERLEN)", min_value=1, value=86400, step=60, key = 11)
    with col5:
        nstp = st.number_input("Number of Time Steps (NSTP)", value=48, min_value=1, step=1)
    with col6:
        tsmult2 = st.slider("Time Step Multiplier (TSMULT)", min_value=1.0, max_value=2.0, value=1.0, step=0.01, key = 21)
    
    steps_v2 = modflow_time_steps(perlen2, nstp, tsmult2)
    steps_v2_fixed = modflow_time_steps(perlen2, nstp, 1.0)
    fig2, ax2 = plt.subplots(figsize=(8, 2))
    ax2.scatter(steps_v2_fixed, np.ones_like(steps_v2_fixed), color='gray', label='TSMULT = 1 (Constant dt)')
    ax2.scatter(steps_v2, np.ones_like(steps_v2) * 1.1, color='red', label=f'TSMULT = {tsmult2}')
    ax2.set_xlim(0, perlen2)
    ax2.set_xlabel("Time")
    ax2.set_yticks([])
    ax2.legend()
    ax2.set_title("Time Step Distribution (MODFLOW Formula)")
    ax2.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig2)
    
    if tsmult2 == 1.0:
        dt0_m = perlen2 / nstp
    else:
        dt0_m = perlen2 * (tsmult2 - 1) / (tsmult2 ** nstp - 1)
    dt0_1 = perlen2 / nstp
    
    columns2 = st.columns((1,1), gap = 'medium')
    with columns2[0]:
        st.write('Initial time step $dt_0$ with multiplier', tsmult2, " = ", dt0_m)
    with columns2[1]:
        st.write('Initial time step $dt_0$ with multiplier 1.0 = ', dt0_1)
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')