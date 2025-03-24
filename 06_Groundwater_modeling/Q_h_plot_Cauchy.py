import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Interaction Between Groundwater and Surface Water")

st.markdown("""
This app shows how the flow between a stream and an aquifer $Q$ depends on the groundwater head at the stream $h_{aq}$. 
The relationship follows:  
$
Q = C \\cdot (h_{aq} - h_s)
$
""")

# Main area inputs

# Define the minimum and maximum for the logarithmic scale
log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 1.0  # T / Corresponds to 10^1 = 10

columns1 = st.columns((1,1), gap = 'large')
with columns1[0]:
    # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
    container = st.container()
    C_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min1,log_max1,-2.0,0.01,format="%4.2f")
    C = 10 ** C_slider_value
    container.write("**Conductance in m²/s:** %5.2e" %C)
with columns1[1]:
    h_RIV = st.slider("**River head ($h_{RIV}$)**", min_value=0.0, max_value=20.0, value=9.0, step=0.1)
    h_aq_show  = st.slider("**Aquifer head ($h_{aq}**$) for visualization", min_value=0.0, max_value=20.0, value=10.0, step=0.1)

# Define aquifer head range
h_aq = np.linspace(0, 20, 200)
Q = C * (h_aq - h_RIV)

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))
#ax.plot(h_aq, Q, label=f'$Q = C(h_{{aq}} - h_{{RIV}})$, C={C}')
ax.plot(h_aq, Q, label=rf"$Q = C(h_{{aq}} - h_{{RIV}})$, C = {C:.2e}")
ax.axhline(0, color='black', linewidth=1)
ax.axvline(h_RIV, color='gray', linestyle='--', label=f'$h_{{RIV}}$ = {h_RIV}')
ax.axvline(h_aq_show, color='red', linestyle='--', label=f'$h_{{aq}}$ = {h_aq_show}')

# Labels and formatting
ax.set_xlabel("Head in the Ground-Water System at the Stream ($h_{aq}$)", fontsize=10)
ax.set_ylabel("Flow Into the Ground-Water System From the Stream ($Q$)", fontsize=10)
ax.set_title("Flow Between Groundwater and Stream", fontsize=12)
ax.set_xlim(0, 20)
ax.set_ylim(-0.1, 0.1)
ax.grid(True)
ax.legend()
#ax.set_aspect('equal', adjustable='box')

# Add gaining/losing stream annotations
ax.text(1, 0.01, "Gaining Stream", va='center')
ax.text(1, -0.01, "Losing Stream", va='center')

st.pyplot(fig)
