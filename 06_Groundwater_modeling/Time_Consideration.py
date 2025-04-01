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
            This application investigate for an underground structure and provided boundary characteristics (distance and period of forcing function) wether steady-state or transient conditions are required. The theory can be found in Anderson et al. 2015 (Applied Groundwater Modeling' on page 307ff (chapter 7.2 - Steady state or Transient?). 
            """) 
st.subheader(':green-background[Overview]', divider="green")

st.subheader('Interactive Plot of $L$ and $T^*$ (distance between system boundaries $L$ and groundwater system time constant $T^*$', divider="green")
st.markdown("""
            The groundwater system time constant is described by the following equations
            """) 
st.latex(r'''T^* = \frac{S L^2}{K b}''')
            
st.markdown('''            
            where:
            - $T^*$ is the groundwater system time constant [T],
            - $S$ is Storativity [-],
            - $L$ is the distance between system boundaries [L],
            - $K$ is the hydraulic conductivity [L/T],
            - $b$ is the aquifer thickness [L].
            
            If the time for what the model observation is significantly larger than $T^*$, the system can be represented by a steady-state equation.
            ''') 
            
# Get input data
# Define the minimum and maximum for the logarithmic scale
log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1
log_min2 = -6.0 # S / Corresponds to 10^-7 = 0.0000001
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
        L_point = st.slider("Lenght of interest [m]", min_value=1.0, max_value=10000.0, value=100.0, step=0.1, key = 35)
        
    L_min, L_max = 1.0,10000.0  # Define range for L
    L = np.linspace(L_min, L_max, 500)  # L values
    
    # Calculate Transmissivity
    T = K * b
    
    # Compute System Time Constant T*
    T_star = (S * L**2) / T
    T_star_point = (S * L_point**2) / T
    
    T_star_day = T_star/86400
    T_star_point_day = T_star_point/86400
    
    # Plot the function L vs. T*
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(L, T_star_day, label=r"$T^* = \frac{S L^2}{Kb}$", color="b")
    ax.plot(L_point, T_star_point_day, 'ro', label=r"$L$ of interest")
    ax.fill_between(L, T_star_day, max(T_star_day) * 1000, color="blue", alpha=0.1)
    ax.fill_between(L, 0, T_star_day, color="green", alpha=0.1)
    ax.set_xlabel("distance between system boundaries $L$ (m)")
    ax.set_ylabel(r"$T^*$ (in days)")
    if log:
        ax.set_xscale("log")  # Log scale for better visualization
        ax.set_yscale("log")
        ax.set_xlim(1E0, 1e4)
        ax.set_ylim(1E-2, 1e4)
        
        # Add a textbox in the lower right corner (max X, min Y)
        ax.text(
            8000, 0.02, "represented \nby a transient \nsolution", 
            ha="right", va="bottom", fontsize=8, bbox=dict(facecolor="white", alpha=0.8, edgecolor="black")
        )
        
        # Add a textbox in the upper left corner (min X, max Y)
        ax.text(
            1.3, 7000, "can be represented \nby a steady state \nsolution", 
            ha="left", va="top", fontsize=8, bbox=dict(facecolor="white", alpha=0.8, edgecolor="black")
        )
    else:
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 365)
        # Add a textbox in the lower right corner (max X, min Y)
        ax.text(
            990, 10, "represented \nby a transient \nsolution", 
            ha="right", va="bottom", fontsize=8, bbox=dict(facecolor="white", alpha=0.8, edgecolor="black")
        )
        
        # Add a textbox in the upper left corner (min X, max Y)
        ax.text(
            20, 360, "can be represented \nby a steady state \nsolution", 
            ha="left", va="top", fontsize=8, bbox=dict(facecolor="white", alpha=0.8, edgecolor="black")
        )
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)


    ax.legend(loc="upper right")
    
    # Display plot in Streamlit
    st.pyplot(fig)

    st.write("- Length of interest **$L$ = % 8.2f"% L_point, " m**")
    st.write("- Groundwater system time constant    **$T^*$ = % 6.2f"% T_star_point_day, " days**")


st.subheader('Interactive Plot of Period of the forcing function and Aquifer Response Time', divider="green")

st.markdown("""
            The aquifer response time $\\tau$ is computed as
            """) 
st.latex(r'''\tau = \frac{1}{4P} \frac{S L^2}{K b} = \frac{T^*}{4P}''')
            
st.markdown('''            
            where:
            - $P$ is the period of the forcing function [T].
            
            The dimensionless aquifer response time $\\tau$ indicate the necessity of time consideration as:
            - with $\\tau$ > 1.0, a steady-state model is appropriate.
            - with 0.1 < $\\tau$ < 1.0, a transient model is required.  
            - with $\\tau$ < 0.1, bounding or successive steady-state solutions may be used.  
            ''') 


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
        S2_slider_value=st.slider('_(log of) Storativity', log_min2,log_max2,-3.0,0.01,format="%4.2f", key = 60)
        S2 = 10 ** S2_slider_value
        container.write("**Storativity (dimensionless):** %5.2e" %S2) 
    with columns2[1]:
        b2 = st.slider("Aquifer Thickness (b) [m]", min_value=1.0, max_value=100.0, value=10.0, step=0.1, key = 70)
        L2 = st.slider("Characteristic Length (L) [m]", min_value=1.0, max_value=1000.0, value=400.0, step=1.0, key = 80)
        P_point = st.slider("period of the forcing function of interest [d]", min_value=0.01, max_value=1000.0, value=7.0, step=0.1, key = 90)
        
    P_min, P_max = 0, 1000  # Range for P in days
    if log:
        P_min, P_max = 0.001, 1000  # Range for P in days
        P_values = np.logspace(np.log10(P_min), np.log10(P_max), 1000)
    else:
        P_min, P_max = 0, 1000  # Range for P in days
        P_values = np.linspace(P_min, P_max, 1000)  # P values
    
    # Compute T*
    T2 = K2 * b2
    T2_star = (S2 * L2**2) / T2  # System Time Constant
    
    T2_star_day = T2_star/86400
    
    # Compute τ
    tau_values = T2_star_day / (4 * P_values)
    tau_point = T2_star_day / (4 * P_point)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Fill background colors for different τ ranges
    ax.fill_between(P_values, 1, 10, color="blue", alpha=0.1, label=r"$\tau > 1$")
    ax.fill_between(P_values, 0.1, 1, color="green", alpha=0.1, label=r"$0.1 \leq \tau \leq 1$")
    ax.fill_between(P_values, 1e-2, 0.1, color="yellow", alpha=0.1, label=r"$\tau < 0.1$")
    
    # Plot P vs. τ
    ax.plot(P_values, tau_values, color="blue", linewidth=2, label=r"$\tau = \frac{T^*}{4P}$")
    ax.plot(P_point, tau_point, 'ro', label=r"$P$ of interest")
    # Labels and Scale
    ax.set_xlabel("P")
    ax.set_ylabel(r"$\tau$")
    if log:
        ax.set_xscale("log")  # Log scale for better visualization
        ax.set_yscale("log")
        ax.set_ylim(1E-2, 10)
        ax.set_xlim(1E-1, 1000)
    #else:
        #ax.set_ylim(0, 5)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend()
    
    # Display plot in Streamlit
    st.pyplot(fig)

    st.write("- Forcing period length of interest **$P$ = % 8.2f"% P_point, " m**")
    st.write("- Aquifer response time    **$\\tau$ = % 6.2f"% tau_point, " (dimensionless)**")





'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')