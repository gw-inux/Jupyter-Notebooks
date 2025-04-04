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

st.title("Interaction Between Groundwater and Surface Water")
st.subheader("Theory and Concept of River Aquifer Interaction", divider="green")

st.markdown("""
This app shows how the flow between a stream and an aquifer $Q$ depends on the groundwater head at the stream $h_{aq}$. 
The relationship follows:
""")

st.latex(r'''Q_{RIV} = C (h_{RIV} - h_{{aq}})''')

st.markdown("""
where:
- $Q_{RIV}$ is the flow between the river and the aquifer, taken as positive if it is directed into the aquifer [L3/T]
- $h_{RIV}$ is the water level (stage) in the river (L),
- $C_{RIV}$ is the hydraulic conductance of the river-aquifer interconnection [L2/T], and
- $h_{aq}$ is the head in the aquifer that interacts with the river (L).

In case the aquifer head $h_{aq}$ falls below the river bottom elevation $R_{BOT}$, the relationship is:
""")

st.latex(r'''Q_{RIV} = C (h_{RIV} - R_{{BOT}})''')

st.subheader("Interactive plot", divider="green")

# Functions

# Callback function to update session state
def update_C():
    st.session_state.C_slider_value = st.session_state.C_input
def update_h_RIV():
    st.session_state.h_RIV = st.session_state.h_RIV_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.C_slider_value = -2.0
st.session_state.h_RIV = 9.0
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
    bottom = st.toggle('Do you want to consider the river bottom elevation?')
    turn = st.toggle('Toggle to turn the plot 90 degrees')
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $C$, $h_{RIV}$, $h_{aq}$, and $h_{stage}$.")
    
    columns1 = st.columns((1,1), gap = 'large')
    with columns1[0]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()  
        if st.session_state.number_input:
            C_slider_value_new = st.number_input("_(log of) Conductance in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)
        else:
            C_slider_value_new = st.slider      ("_(log of) Conductance in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)    
        C = 10 ** C_slider_value_new
        container.write("**Conductance in m²/s:** %5.2e" %C)
    with columns1[1]:
        if st.session_state.number_input:
            h_RIV = st.number_input("**River head ($h_{RIV}$)**", 5.0, 20.0, st.session_state.h_RIV, 0.1, key="h_RIV_input", on_change=update_h_RIV)
        else:
            h_RIV = st.slider      ("**River head ($h_{RIV}$)**", 5.0, 20.0, st.session_state.h_RIV, 0.1, key="h_RIV_input", on_change=update_h_RIV)
        if st.session_state.number_input:
            h_aq_show = st.number_input("**Aquifer head ($h_{aq}$**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
        else:
            h_aq_show = st.slider      ("**Aquifer head ($h_{aq}$**", 0.0, 20.0, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
        if bottom:
            if st.session_state.number_input:
                stage = st.number_input("**River stage ($h_{stage}$)**", 0.1, 5.0, st.session_state.stage, 0.1, key="stage_input", on_change=update_stage)
            else:
                stage = st.slider      ("**River stage ($h_{stage}$)**", 0.1, 5.0, st.session_state.stage, 0.1, key="stage_input", on_change=update_stage)
            h_bot = h_RIV-stage
    
    # Define aquifer head range
    h_aq = np.linspace(0, 20, 200)
    if bottom:
        Q = np.where(h_aq >= h_bot, C * (h_RIV - h_aq), C * (h_RIV - h_bot))
        Q_ref = C * (h_RIV - h_aq_show) if h_aq_show >= h_bot else C * (h_RIV - h_bot)
    else:
        Q = C * (h_RIV - h_aq)
        Q_ref = C * (h_RIV - h_aq_show)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    if turn:
        ax.plot(Q, h_aq, label=rf"$Q = C(h_{{aq}} - h_{{RIV}})$, C = {C:.2e}",color='blue', linewidth=3)
        ax.axvline(0, color='black', linewidth=1)
        ax.axhline(h_RIV, color='blue', linewidth=2, linestyle='--', label=f'$h_{{RIV}}$ in m= {h_RIV}')
        ax.axhline(h_aq_show, color='red', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
        if bottom:
            ax.axhline(h_bot, color='grey', linewidth=2, linestyle='--', label=f'$h_{{bot}}$ in m= {h_bot}')    
            ax.fill_betweenx(
                y=[h_bot, h_RIV],
                x1=-0.1,  # fill across full x-axis width
                x2= 0.1,
                color='lightblue',
                alpha=0.3,
                label="River"
            )
        
        # Labels and formatting
        ax.set_ylabel("Heads and elevations in the River-Aquifer System (m)", fontsize=10)
        ax.set_xlabel("Flow Into the Ground-Water System From the Stream $Q$ (m³/s)", fontsize=10)
        ax.set_ylim(0, 20)
        ax.set_xlim(0.1, -0.1)
        if Q_ref < 0:
            ax.annotate(
                '',  # no text
                xy=(Q_ref,h_RIV),  # arrowhead
                xytext=(Q_ref, h_aq_show),  # arrow start
                arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
            )
        else:
            ax.annotate(
                '',  # no text
                xy=(Q_ref,h_RIV),  # arrowhead
                xytext=(Q_ref, h_aq_show),  # arrow start
                arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
            )
            if bottom and h_aq_show < h_bot:
                x_min = -0.1
                x_max =  0.1
                arrow_xs = np.linspace(x_min + 0.01, x_max - 0.01, 10)  # 10 arrows, evenly spaced
            
                for x in arrow_xs:
                    ax.annotate(
                        '',  # no text
                        xy=(x, h_bot),        # arrowhead at river bottom
                        xytext=(x, h_aq_show),# arrow start at aquifer head
                        arrowprops=dict(
                            arrowstyle='<-', 
                            color='brown', 
                            lw=3, 
                            alpha=0.1
                        )
                    )
            
                # Add label at far left
                ax.text(
                    x_min + 0.01,  # slightly inside the plot
                    (h_bot + h_aq_show) / 2,
                    "Unsaturated zone flow",
                    color='brown',
                    fontsize=9,
                    rotation=0,
                    va='center'
                )
        # Add gaining/losing stream annotations
        ax.text(-0.005,1, "Gaining Stream", va='center',color='blue')
        ax.text(0.05, 1,  "Losing Stream", va='center',color='green')
            
    else:
        ax.plot(h_aq, Q, label=rf"$Q = C(h_{{aq}} - h_{{RIV}})$, C = {C:.2e}",color='blue', linewidth=3)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(h_RIV, color='blue', linewidth=2, linestyle='--', label=f'$h_{{RIV}}$ in m= {h_RIV}')
        ax.axvline(h_aq_show, color='red', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m= {h_aq_show}')
        if bottom:
            ax.axvline(h_bot, color='grey', linewidth=2, linestyle='--', label=f'$h_{{bot}}$ in m= {h_bot}')
            ax.fill_betweenx(
                y=[-0.1, 0.1],
                x1=h_bot,  # fill across full x-axis width
                x2=h_RIV,
                color='lightblue',
                alpha=0.3,
                label="River"
            )
        # Labels and formatting
        ax.set_xlabel("Heads and elevations in the River-Aquifer System (m)", fontsize=10)
        ax.set_ylabel("Flow Into the Ground-Water System From the Stream $Q$ (m³/s)", fontsize=10)
        ax.set_xlim(0, 20)
        ax.set_ylim(-0.1, 0.1)
        if Q_ref < 0:
            ax.annotate(
                '',  # no text
                xy=(h_RIV, Q_ref),  # arrowhead
                xytext=(h_aq_show, Q_ref),  # arrow start
                arrowprops=dict(arrowstyle='->', color='blue', lw=3,  alpha=0.4)
            )
        else:
            ax.annotate(
            '',  # no text
            xy=(h_RIV, Q_ref),  # arrowhead
            xytext=(h_aq_show, Q_ref),  # arrow start
            arrowprops=dict(arrowstyle='<-', color='green', lw=3, alpha=0.6)
            )
            if bottom and h_aq_show < h_bot:
                y_min = -0.1
                y_max =  0.1
                arrow_xs = np.linspace(y_min + 0.01, y_max - 0.01, 10)  # 10 arrows, evenly spaced
            
                for x in arrow_xs:
                    ax.annotate(
                        '',  # no text
                        xy=(h_bot,x),        # arrowhead at river bottom
                        xytext=(h_aq_show, x),# arrow start at aquifer head
                        arrowprops=dict(
                            arrowstyle='<-', 
                            color='brown', 
                            lw=3, 
                            alpha=0.1
                        )
                    )
            
                # Add label at far left
                ax.text(
                    (h_bot + h_aq_show) / 2,  # slightly inside the plot
                    0.065,
                    "Unsaturated zone flow",
                    color='brown',
                    fontsize=9,
                    rotation=270,
                    va='center'
                )
            
            
            
        # Add gaining/losing stream annotations
        ax.text(15, -0.005, "Gaining Stream", va='center',color='blue')
        ax.text(15, 0.005, "Losing Stream", va='center',color='green')
        
    ax.set_title("Flow Between Groundwater and Stream", fontsize=12)
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
