import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import scipy.interpolate as interp
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button

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

st.title("Interaction Between Groundwater and Drains")
st.subheader("Theory and Concept of the Drain Boundary (DRN) in MODFLOW", divider="green")

st.markdown("""
This app calculates the flow between  a model cell and a Drain (DRN) depending on the drain elevation $H_{drain}$ and the conductance $C_{drain}$ between the boundary and the aquifer cell.
 
The relationship follows:
""")

st.latex(r'''Q_{out} = C_{D} (H_{D} - h_{{aq}})''')

st.markdown("""
where:
- $Q_{out}$ is the flow from the aquifer into the drain [L3/T]
- $H_{drain}$ is the drain elevation (L),
- $C_{drain}$ is the drain conductance [L2/T], and
- $h_{aq}$ is the head in the aquifer that interacts with the drain (L).

The following figure illustrates the setup.
""")

left_co, cent_co, last_co = st.columns((10,80,10))
with cent_co:
    st.image('06_Groundwater_modeling/FIGS/DRN.png', caption="Schematic illustration of the DRN boundary with a) drain pipe burried in backfill ditch, and b) open drain; modified from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

st.subheader("Interactive plot", divider="green")

# Functions

# Callback function to update session state
def update_CD():
    st.session_state.CD_slider_value = st.session_state.CD_input
def update_HD():
    st.session_state.HD = st.session_state.HD_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.CD_slider_value = -3.0
st.session_state.HD = 9.0
st.session_state.h_aq_show = 10.0

st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    # Switches
    turn = st.toggle('Toggle to turn the plot 90 degrees')
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_D$, $H_D$, and $h_{aq}$.")
    
    columns1 = st.columns((1,1), gap = 'large')
    
    # Initialize st.session_state.C
    if "CD" not in st.session_state:
        st.session_state.CD = 10 ** st.session_state.CD_slider_value
    
    with columns1[0]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()  
        if st.session_state.number_input:
            CD_slider_value_new = st.number_input("_(log of) Conductance $C_D$ in m²/s_", log_min1,log_max1, st.session_state.CD_slider_value, 0.01, format="%4.2f", key="CD_input", on_change=update_CD)
        else:
            CD_slider_value_new = st.slider      ("_(log of) Conductance $C_D$ in m²/s_", log_min1,log_max1, st.session_state.CD_slider_value, 0.01, format="%4.2f", key="CD_input", on_change=update_CD)    
        st.session_state.CD = 10 ** CD_slider_value_new
        container.write("**Conductance $C_D$ in m²/s:** %5.2e" %st.session_state.CD)
    with columns1[1]:
        if st.session_state.number_input:
            HD = st.number_input("**drain elevation ($H_D$)**", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
        else:
            HD = st.slider      ("**drain elevation ($H_D$)**", 5.0, 20.0, st.session_state.HD, 0.1, key="HD_input", on_change=update_HD)
        if st.session_state.number_input:
            h_aq_show = st.number_input("**Aquifer head ($h_{aq}$)**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
        else:
            h_aq_show = st.slider      ("**Aquifer head ($h_{aq})$**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
    
    # Define aquifer head range
    h_aq = np.linspace(0, 20, 200)
    
    Q = np.where(h_aq >= HD, st.session_state.CD * (HD - h_aq)*-1, 0)
    Q_ref = st.session_state.CD * (HD - h_aq_show)*-1 if h_aq_show >= HD else 0   
        
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    if turn:
        ax.plot(Q, h_aq, label=rf"$Q_o = C_D(H_D - h_{{aq}})$, $C_D$ = {st.session_state.CD:.2e}",color='orange', linewidth=3)
        ax.axvline(0, color='black', linewidth=1)
        ax.axhline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m= {HD}')
        ax.axhline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
        # Labels and formatting
        ax.set_ylabel("Heads and elevations in the DRN Boundary-Aquifer System (m)", fontsize=10)
        ax.set_xlabel("Flow from the Ground-Water System into the DRN  $Q_{out}$ (m³/s)", fontsize=10)
        ax.set_ylim(0, 20)
        ax.set_xlim(0.05, -0.05)
        if Q_ref > 0:
            ax.annotate(
                '',  # no text
                xy=(Q_ref,HD),  # arrowhead
                xytext=(Q_ref, h_aq_show),  # arrow start
                arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
            )
        else:
            ax.annotate(
                '',  # no text
                xy=(Q_ref,HD),  # arrowhead
                xytext=(Q_ref, h_aq_show),  # arrow start
                arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
            )
        # Add gaining/losing stream annotations
        ax.text(0.037,1, "Gaining DRN boundary", va='center',color='blue')
        #ax.text(0.035, 1,  "Losing DRN boundary", va='center',color='green')
            
    else:
        ax.plot(h_aq, Q, label=rf"$Q_o = C_D(H_D - h_{{aq}})$, $C_D$ = {st.session_state.CD:.2e}",color='orange', linewidth=3)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(HD, color='green', linewidth=2, linestyle='--', label=f'$H_D$ in m= {HD}')
        ax.axvline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
        # Labels and formatting
        ax.set_xlabel("Heads and elevations in the DRN Boundary-Aquifer System (m))", fontsize=10)
        ax.set_ylabel("Flow from the Ground-Water System into the DRN $Q_{out}$ (m³/s)", fontsize=10)
        ax.set_xlim(0, 20)
        ax.set_ylim(-0.05, 0.05)
        if Q_ref < 0:
            ax.annotate(
                '',  # no text
                xy=(HD, Q_ref),  # arrowhead
                xytext=(h_aq_show, Q_ref),  # arrow start
                arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
            )
        else:
            ax.annotate(
            '',  # no text
            xy=(HD, Q_ref),  # arrowhead
            xytext=(h_aq_show, Q_ref),  # arrow start
            arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
            )
        # Add gaining/losing stream annotations
        ax.text(13, -0.003, "Gaining DRN boundary", va='center',color='blue')
        #ax.text(13, 0.003, "Losing DRN boundary", va='center',color='green')
        
    ax.set_title("Flow Between Groundwater and DRN boundary", fontsize=12)
    ax.grid(True)
    ax.legend()
    
    st.pyplot(fig)

Q_h_plot()
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
