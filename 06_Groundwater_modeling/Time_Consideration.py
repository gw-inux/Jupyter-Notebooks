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

st.title('Time Consideration')
st.header('for :green[numerical groundwater flow models]')
st.markdown("""
            This application investigate for an underground structure and provided boundary characteristics (distance and period of forcing function) wether steady-state or transient conditions are required.
            """) 
st.subheader(':green-background[Overview]', divider="green")

st.subheader('Interactive Plot of Length and Groundwater System Time Constant $T^*$', divider="green")
# Get input data
# Define the minimum and maximum for the logarithmic scale
log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1
log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1

with st.expander('Show the interactive plot'):
        
    # Sliders for input parameters
    
    log = st.toggle("Toggle for **log-log graph**", value = "True", key = 5)
    columns1 = st.columns((1,1), gap = 'large')
    with columns1[0]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()
        K_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min1,log_max1,-4.0,0.01,format="%4.2f", key = 10)
        K = 10 ** K_slider_value
        container.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
           
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Storativity
        container = st.container()
        S_slider_value=st.slider('_(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f", key = 20)
        S = 10 ** S_slider_value
        container.write("**Storativity (dimensionless):** %5.2e" %S)   
    
    with columns1[1]:
        b = st.slider("Aquifer Thickness (b) [m]", min_value=1.0, max_value=100.0, value=10.0, step=0.1, key = 30)
        
    L_min, L_max = 1.0, 1000.0  # Define range for L
    L = np.linspace(L_min, L_max, 100)  # L values
    
    # Calculate Transmissivity
    T = K * b
    
    # Compute System Time Constant T*
    T_star = (S * L**2) / T
    
    T_star_day = T_star/86400
    
    # Plot the function L vs. T*
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(L, T_star_day, label=r"$T^* = \frac{T L^2}{S}$", color="b")
    ax.set_xlabel("L (m)")
    ax.set_ylabel(r"$T^*$ (in days)")
    if log:
        ax.set_xscale("log")  # Log scale for better visualization
        ax.set_yscale("log")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend()
    
    # Display plot in Streamlit
    st.pyplot(fig)



st.subheader('Interactive Plot of Period of the forcing function and Aquifer Response Time', divider="green")

with st.expander('Show the interactive plot'):
    # Sliders for parameters
    log = st.toggle("Toggle for **log-log graph**", value = "True", key = 45)
    
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()
        K2_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min1,log_max1,-4.0,0.01,format="%4.2f", key = 50)
        K2 = 10 ** K2_slider_value
        container.write("**Hydraulic conductivity in m/s:** %5.2e" %K2)
           
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Storativity
        container = st.container()
        S2_slider_value=st.slider('_(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f", key = 60)
        S2 = 10 ** S2_slider_value
        container.write("**Storativity (dimensionless):** %5.2e" %S2) 
    with columns2[1]:
        b2 = st.slider("Aquifer Thickness (b) [m]", min_value=1.0, max_value=100.0, value=10.0, step=0.1, key = 70)
        L2 = st.slider("Characteristic Length (L) [m]", min_value=1.0, max_value=1000.0, value=100.0, step=1.0, key = 80)
        
    P_min, P_max = 0, 364  # Range for P in days
    P_values = np.linspace(P_min, P_max, 365)  # P values
    
    # Compute T*
    T2 = K2 * b2
    T2_star = (S2 * L2**2) / T2  # System Time Constant
    
    T2_star_day = T2_star/86400
    
    # Compute τ
    tau_values = T2_star_day / (4 * P_values)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Fill background colors for different τ ranges
    ax.fill_between(P_values, 1, max(tau_values), color="red", alpha=0.3, label=r"$\tau > 1$")
    ax.fill_between(P_values, 0.1, 1, color="yellow", alpha=0.3, label=r"$0.1 \leq \tau \leq 1$")
    ax.fill_between(P_values, min(tau_values), 0.1, color="green", alpha=0.3, label=r"$\tau < 0.1$")
    
    # Plot P vs. τ
    ax.plot(P_values, tau_values, color="blue", linewidth=2, label=r"$\tau = \frac{T^*}{4P}$")
    
    # Labels and Scale
    ax.set_xlabel("P")
    ax.set_ylabel(r"$\tau$")
    if log:
        ax.set_xscale("log")  # Log scale for better visualization
        ax.set_yscale("log")
        #ax.set_ylim(1E-2, 1e0)
    #else:
        #ax.set_ylim(0, 5)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend()
    
    # Display plot in Streamlit
    st.pyplot(fig)







'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')