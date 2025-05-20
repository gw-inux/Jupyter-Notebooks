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
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("Theory and Concept of the :orange[General Head Boundary (GHB) in MODFLOW]")
st.subheader("Interaction Between Groundwater and head-dependent boundaries", divider="orange")

st.markdown("""
This app calculates the flow between a General Head Boundary (GHB) and a model cell depending on the boundary head $HB$ and the conductance $C_B$ between the boundary and the aquifer cell.
 
The relationship follows:
""")

st.latex(r'''Q_B = C_B (H_B - h_{{aq}})''')

st.markdown("""
where:
- $Q_B$ is the flow between the GHB and the aquifer, taken as positive if it is directed into the aquifer [L3/T]
- $H_B$ is the water level (stage) in the general head boundary (L),
- $C_B$ is the hydraulic conductance of the GHB-aquifer interconnection [L2/T], and
- $h_{aq}$ is the head in the aquifer that interacts with the river (L).

The following figure illustrates the setup.
""")

left_co, cent_co, last_co = st.columns((10,80,10))
with cent_co:
    st.image('06_Groundwater_modeling/FIGS/GHB.png', caption="Schematic illustration of the GHB boundary, modified from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

st.subheader("Interactive plot", divider="orange")

# Functions

# Callback function to update session state
def update_C():
    st.session_state.C_slider_value = st.session_state.C_input
def update_K():
    st.session_state.K_slider_value = st.session_state.K_input
def update_LB():
    st.session_state.LB = st.session_state.LB_input
def update_AB():
    st.session_state.AB = st.session_state.AB_input
def update_HB():
    st.session_state.HB = st.session_state.HB_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.C_slider_value = -2.5
st.session_state.K_slider_value = -3.5
st.session_state.LB = 100.
st.session_state.AB = 1000.0
st.session_state.HB = 8.0
st.session_state.stage = 2.0
st.session_state.h_aq_show = 10.0

st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    # Switches
    turn = st.toggle('Toggle to turn the plot 90 degrees', key="GHB_turn")
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C_B$, $H_B$, $A_B$, $L_B$, and $h_{aq}$.")
    c_computed = st.toggle('Toggle to compute conductance')
    visualize = st.toggle(':rainbow[**Make the plot alive** and visualize the input values]', key="GHB_vis")
    
    columns1 = st.columns((1,1), gap = 'large')
    
    # Initialize st.session_state.C
    if "C" not in st.session_state:
        st.session_state.C = 10 ** st.session_state.C_slider_value
    
    with columns1[0]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        if c_computed:
            container = st.container()  
            if st.session_state.number_input:
                K_slider_value_new = st.number_input("_(log of) Hydraulic conductivity $K_B$ in m/s_", log_min1,log_max1, st.session_state.K_slider_value, 0.01, format="%4.2f", key="K_input", on_change=update_K)
            else:
                K_slider_value_new = st.slider      ("_(log of) Hydraulic conductivity $K_B$ in m/s_", log_min1,log_max1, st.session_state.K_slider_value, 0.01, format="%4.2f", key="K_input", on_change=update_K)   
            K = 10 ** K_slider_value_new
            container.write("**Hydraulic conductivity $K_B$ in m/s:** %5.2e" %K)
            if st.session_state.number_input:
                LB = st.number_input("**GHB lenght ($L_B$)**", 1.0, 10000.0, st.session_state.LB, 1., key="LB_input", on_change=update_LB)
            else:
                LB = st.slider      ("**GHB lenght ($L_B$)**", 1.0, 10000.0, st.session_state.LB, 1., key="LB_input", on_change=update_LB)
            if st.session_state.number_input:
                AB = st.number_input("**GHB area ($A_B$)**", 1.0, 100000.0, st.session_state.AB, 1., key="AB_input", on_change=update_AB)
            else:
                AB = st.slider      ("**GHB area ($A_B$)**", 1.0, 100000.0, st.session_state.AB, 1., key="AB_input", on_change=update_AB)
            st.session_state.C = K * AB / LB
            
            # Update C_slider_value based on computed values
            st.session_state.C_slider_value = np.log10(st.session_state.C)
        else:
            container = st.container()  
            if st.session_state.number_input:
                C_slider_value_new = st.number_input("_(log of) Conductance $C_B$ in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)
            else:
                C_slider_value_new = st.slider      ("_(log of) Conductance $C_B$ in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)    
            st.session_state.C = 10 ** C_slider_value_new
            container.write("**Conductance $C_B$ in m²/s:** %5.2e" %st.session_state.C)
            
            # Update K_slider_value based on computed values
            st.session_state.K_slider_value = np.log10(st.session_state.C * st.session_state.LB / st.session_state.AB)
    with columns1[1]:
        if st.session_state.number_input:
            HB = st.number_input("**GHB head ($HB$)**", 5.0, 20.0, st.session_state.HB, 0.1, key="HB_input", on_change=update_HB)
        else:
            HB = st.slider      ("**GHB head ($HB$)**", 5.0, 20.0, st.session_state.HB, 0.1, key="HB_input", on_change=update_HB)
        if st.session_state.number_input:
            h_aq_show = st.number_input("**Aquifer head ($h_{aq}$)**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
        else:
            h_aq_show = st.slider      ("**Aquifer head ($h_{aq})$**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
    
    # Define aquifer head range
    h_aq = np.linspace(0, 20, 200)
    Q = st.session_state.C * (HB - h_aq)
    Q_ref = st.session_state.C * (HB - h_aq_show)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    if visualize:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='orange', linewidth=3)
            ax.axvline(0, color='black', linewidth=1)
            ax.axhline(HB, color='green', linewidth=2, linestyle='--', label=f'$H_B$ in m= {HB}')
            ax.axhline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05, -0.05)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HB),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
                )
            else:
                ax.annotate(
                    '',  # no text
                    xy=(Q_ref,HB),  # arrowhead
                    xytext=(Q_ref, h_aq_show),  # arrow start
                    arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
                )
            # Add gaining/losing stream annotations
            ax.text(-0.003,1, "Gaining GHB boundary", va='center',color='blue',  fontsize=16)
            ax.text(0.002, 1,  "Losing GHB boundary", va='center', ha='right',color='green',  fontsize=16)
                
        else:
            ax.plot(h_aq, Q, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='orange', linewidth=3)
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(HB, color='green', linewidth=2, linestyle='--', label=f'$H_B$ in m= {HB}')
            ax.axvline(h_aq_show, color='blue', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
            if Q_ref < 0:
                ax.annotate(
                    '',  # no text
                    xy=(HB, Q_ref),  # arrowhead
                    xytext=(h_aq_show, Q_ref),  # arrow start
                    arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
                )
            else:
                ax.annotate(
                '',  # no text
                xy=(HB, Q_ref),  # arrowhead
                xytext=(h_aq_show, Q_ref),  # arrow start
                arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
                )
            # Add gaining/losing stream annotations
            ax.text(19.8, -0.003, "Gaining GHB boundary", va='center', ha='right',color='blue',  fontsize=16)
            ax.text(19.8, 0.003, "Losing GHB boundary", va='center', ha='right',color='green',  fontsize=16)
    else:
        if turn:
            ax.plot(Q, h_aq, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_ylabel("Heads and elevations in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_xlabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_ylim(0, 20)
            ax.set_xlim(0.05,-0.05)
        else:        
            ax.plot(h_aq, Q, label=rf"$Q_B = C_B(H_B - h_{{aq}})$, $C_B$ = {st.session_state.C:.2e}",color='black', linewidth=3)
            # Labels and formatting
            ax.set_xlabel("Heads and elevations in the GHB Boundary-Aquifer System (m)", fontsize=14, labelpad=15)
            ax.set_ylabel("Flow Into the Ground-Water System From the GHB $Q_B$ (m³/s)", fontsize=14, labelpad=15)
            ax.set_xlim(0, 20)
            ax.set_ylim(-0.05, 0.05)
   
   # === SHARED FORMATTING === #        
    ax.set_title("Flow Between Groundwater and GHB boundary", fontsize=16, pad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14) 
    ax.legend(fontsize=14)
    
    st.pyplot(fig)

Q_h_plot()
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
