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

with st.expander('**Click here** if you want to read more about the :green[**general concept**] of the River boundary condition in MODFLOW'):
    st.markdown("""
    ### The General Concept of the River Boundary in MODFLOW
    """)
    left_co1, cent_co1, last_co1 = st.columns((10,80,10))
    with cent_co1:
        st.image('06_Groundwater_modeling/FIGS/RIV_CONCEPT.png', caption="Concept of the River boundary, from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")


with st.expander('**Click here** if you want to see how the :green[**conductance is calculated**]'):
    st.markdown("""
    ### The Computation of the Conductance for the River Boundary in MODFLOW
    """)
    left_co2, cent_co2, last_co2 = st.columns((10,80,10))
    with cent_co2:
        st.image('06_Groundwater_modeling/FIGS/RIV_COND.png', caption="Calculation of the Riverbed conductance, from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

with st.expander('**Click here** if you want to get more information about the situation wehen the :green[**water table falls below the river bottom**]'):
    st.markdown("""
    ### Disconnected Stream - When the water table falls below the River Bottom
    """)
    left_co3, cent_co3, last_co3 = st.columns((10,80,10))
    with cent_co3:
        st.image('06_Groundwater_modeling/FIGS/RIV_CONCEPT_UNSAT.png', caption="Concept of the River boundary when the aquifer head falls below the river bottom, modified from  (McDonald and Harbaugh, 1988; https://pubs.usgs.gov/twri/twri6a1/pdf/twri_6-A1_p.pdf)")

st.subheader("Interactive plot", divider="green")

# Functions

# Callback function to update session state
def update_C():
    st.session_state.C_slider_value = st.session_state.C_input
def update_h_RIV():
    st.session_state.h_RIV = st.session_state.h_RIV_input
def update_K():
    st.session_state.K_slider_value = st.session_state.K_input
def update_L_RIV():
    st.session_state.L_RIV = st.session_state.L_RIV_input
def update_W_RIV():
    st.session_state.W_RIV = st.session_state.W_RIV_input
def update_M_RIV():
    st.session_state.M_RIV = st.session_state.M_RIV_input
def update_stage():
    st.session_state.stage = st.session_state.stage_input
def update_h_aq_show():
    st.session_state.h_aq_show = st.session_state.h_aq_show_input  
    
# Initialize session state for value and toggle state
st.session_state.C_slider_value = -2.0
st.session_state.K_slider_value = -5.0
st.session_state.thick = 20.0
st.session_state.h_ref = 0.0
st.session_state.h_aq_show = 10.0
st.session_state.h_RIV = 9.0
st.session_state.L_RIV = 100.0
st.session_state.W_RIV = 10.0
st.session_state.M_RIV = 1.0
st.session_state.stage = 2.0


st.session_state.number_input = False  # Default to number_input


# Main area inputs
@st.fragment
def Q_h_plot():
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 1.0  # T / Corresponds to 10^1 = 10
    
    # Switches
    columns1 = st.columns((1,1,1), gap = 'medium')
    with columns1[0]:
        st.markdown("""
        <div style="margin-bottom: -30px">
            <strong>Reference elevation</strong><br><span style='font-weight: normal'>(e.g., cell bottom)</span>
        </div>
        """, unsafe_allow_html=True)
        h_ref_str = st.text_input(label="",value=str(st.session_state.h_ref),key="h_ref_input")
        
        # Try converting to float and fall back to previous value if conversion fails
        try:
            h_ref = float(h_ref_str)
        except ValueError:
            h_ref = st.session_state.get("h_ref", 0.0)
        
        # Update session state manually if needed - Calculate the change in h_ref
        delta_h_ref = h_ref - st.session_state.h_ref
        
        # Apply the delta only if there's a change
        if delta_h_ref != 0.0:
            st.session_state.h_aq_show += delta_h_ref
            st.session_state.h_RIV += delta_h_ref
        
        # Update the session state values
        st.session_state.h_ref = h_ref
        
        
        st.markdown("""
        <div style="margin-bottom: -30px">
            <strong>Cell thickness</strong><br><span style='font-weight: normal'>(in m above cell bottom)</span>
        </div>
        """, unsafe_allow_html=True)
        thick_str = st.text_input(label="",value=str(st.session_state.thick),key="thick_input")
        
        # Try converting to float and fall back to previous value if conversion fails
        try:
            thick = float(thick_str)
        except ValueError:
            thick = st.session_state.get("thick", 20.0)
        
        # Update the session state values
        st.session_state.thick = thick        
        
    with columns1[1]:
        turn = st.toggle('**Turn plot** 90 degrees')
        st.session_state.number_input = st.toggle("**Use Slider or Number** for input.")        
    with columns1[2]:
        bottom = st.toggle('Account for river bottom elevation')
        condcomp = st.toggle('Compute $C_{RIV}$ explicitely')

    
    columns2 = st.columns((1,1,1), gap = 'medium')
    with columns2[0]:
        if condcomp:
            st.write ('**Compute conductance with the following geometry**')
            if st.session_state.number_input:
                 L_RIV = st.number_input("**River length ($L_{RIV}$)**", 1.0, 1000.0, st.session_state.L_RIV, 0.1, key="L_RIV_input", on_change=update_L_RIV)
            else:
                 L_RIV = st.slider      ("**River length ($L_{RIV}$)**", 1.0, 1000.0, st.session_state.L_RIV, 0.1, key="L_RIV_input", on_change=update_L_RIV)
            if st.session_state.number_input:
                 W_RIV = st.number_input("**River width ($W_{RIV}$)**", 1.0, 200.0, st.session_state.W_RIV, 0.1, key="W_RIV_input", on_change=update_W_RIV)
            else:
                 W_RIV = st.slider      ("**River width ($W_{RIV}$)**", 1.0, 200.0, st.session_state.W_RIV, 0.1, key="W_RIV_input", on_change=update_W_RIV)
            if st.session_state.number_input:
                 M_RIV = st.number_input("**River bed thickness ($M_{RIV}$)**", 0.01, 5.0, st.session_state.M_RIV, 0.01, key="M_RIV_input", on_change=update_M_RIV)
            else:
                 M_RIV = st.slider      ("**River bed thickness ($M_{RIV}$)**", 0.01, 5.0, st.session_state.M_RIV, 0.01, key="M_RIV_input", on_change=update_M_RIV)                      
    with columns2[1]:
        if st.session_state.number_input:
            h_RIV = st.number_input("**River head ($h_{RIV}$)**", 0.2+h_ref, thick+h_ref, st.session_state.h_RIV, 0.1, key="h_RIV_input", on_change=update_h_RIV)
        else:
            h_RIV = st.slider      ("**River head ($h_{RIV}$)**", 0.2+h_ref, thick+h_ref, st.session_state.h_RIV, 0.1, key="h_RIV_input", on_change=update_h_RIV)
        if st.session_state.number_input:
            h_aq_show = st.number_input("**Aquifer head ($h_{aq}$**", 0.1+h_ref, thick+h_ref, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
        else:
            h_aq_show = st.slider      ("**Aquifer head ($h_{aq}$**", 0.1+h_ref, thick+h_ref, st.session_state.h_aq_show, 0.1, key="h_aq_show_input", on_change=update_h_aq_show)
        if bottom:
            if st.session_state.number_input:
                stage = st.number_input("**River stage ($h_{stage}$)**", 0.1, 10.0, st.session_state.stage, 0.1, key="stage_input", on_change=update_stage)
            else:
                stage = st.slider      ("**River stage ($h_{stage}$)**", 0.1, 10.0, st.session_state.stage, 0.1, key="stage_input", on_change=update_stage)
            h_bot = h_RIV-stage
            if h_bot < h_ref:
                fix_issue = True
                st.write(':red[**YOUR RIVER BOTTOM IS BELOW YOUR REFERENCE LEVEL / CELL BOTTOM! INCREASE $h_{RIV}$ OR REDUCE RIVER STAGE $h_{Stage}$]')
            else:
                fix_issue = False
 
    with columns2[2]:
        if condcomp:                   
            # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
            container = st.container()  
            if st.session_state.number_input:
                K_slider_value_new = st.number_input("_(log of) Riverbed hydr. conductivity in m/s_", log_min1,log_max1, st.session_state.K_slider_value, 0.01, format="%4.2f", key="K_input", on_change=update_K)
            else:
                K_slider_value_new = st.slider      ("_(log of) Riverbed hydr. conductivity in m/s_", log_min1,log_max1, st.session_state.K_slider_value, 0.01, format="%4.2f", key="K_input", on_change=update_K)
            K = 10 ** K_slider_value_new
            container.write("**Riverbed hydr. conductivity in m/s:** %5.2e" %K)                 
                 
            C = L_RIV * W_RIV * K / M_RIV
        else:
            # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR Conductance
            container = st.container()  
            if st.session_state.number_input:
                C_slider_value_new = st.number_input("_(log of) Conductance in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)
            else:
                C_slider_value_new = st.slider      ("_(log of) Conductance in m²/s_", log_min1,log_max1, st.session_state.C_slider_value, 0.01, format="%4.2f", key="C_input", on_change=update_C)    
            C = 10 ** C_slider_value_new
            container.write("**Conductance in m²/s:** %5.2e" %C) 
    # Define aquifer head range
    h_aq = np.linspace(0+h_ref, thick+h_ref, 200)
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
        ax.axhline(h_RIV, color='blue', linewidth=2, linestyle='--', label=f'$h_{{RIV}}$ in m = {h_RIV}')
        ax.axhline(h_aq_show, color='red', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m = {h_aq_show}')
        if bottom:
            ax.axhline(h_bot, color='grey', linewidth=2, linestyle='--', label=f'$h_{{bot}}$ in m = {h_bot:.2f}')    
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
        ax.set_ylim(0+h_ref, thick+h_ref)
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
        ax.text(-0.005,1+h_ref, "Gaining Stream", va='center',color='blue')
        ax.text(0.05, 1+h_ref,  "Losing Stream", va='center',color='green')
            
    else:
        ax.plot(h_aq, Q, label=rf"$Q = C(h_{{aq}} - h_{{RIV}})$, C = {C:.2e}",color='blue', linewidth=3)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(h_RIV, color='blue', linewidth=2, linestyle='--', label=f'$h_{{RIV}}$ in m = {h_RIV}')
        ax.axvline(h_aq_show, color='red', linewidth=2, linestyle='--', label=f'$h_{{aq}}$ in m = {h_aq_show}')
        if bottom:
            ax.axvline(h_bot, color='grey', linewidth=2, linestyle='--', label=f'$h_{{bot}}$ in m = {h_bot:.2f}')
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
        ax.set_xlim(0+h_ref, thick+h_ref)
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
        ax.text((0.75*thick)+h_ref, -0.005, "Gaining Stream", va='center',color='blue')
        ax.text((0.75*thick)+h_ref, 0.005, "Losing Stream", va='center',color='green')
        
    ax.set_title("Flow Between Groundwater and Stream", fontsize=12)
    ax.grid(True)
    ax.legend()
    
    st.pyplot(fig)

    columns3 = st.columns((1,10,1), gap = 'medium')

    with columns3[1]:
        st.write("**Parameters and Results**")
        if bottom:
            if fix_issue:
                st.write(':red[**YOUR RIVER BOTTOM IS BELOW YOUR REFERENCE LEVEL / CELL BOTTOM! INCREASE $h_{RIV}$ OR REDUCE RIVER STAGE $h_{Stage}$]')
            else:
                st.write("- Aquifer (MODFLOW) hydraulic head **$h_{aq}$ = %5.2f" %h_aq_show," m**")
                st.write("- River hydraulic head **$h_{RIV}$ = %5.2f" %h_RIV," m**")
                st.write("- River bottom elevation **$h_{bot}$ = %5.2f" %h_bot," m**")
                st.write("- Riverbed conductance **$C_{RIV}$ = % 10.2E"% C, " m²/s**")
                st.write("- Flow between river and aquifer **$Q_{RIV}$ = % 10.2E"% Q_ref," m³/s**")
        else:
            st.write("- Aquifer (MODFLOW) hydraulic head **$h_{aq}$ = %5.2f" %h_aq_show," m**")
            st.write("- River hydraulic head **$h_{RIV}$ = %5.2f" %h_RIV," m**")
            st.write("- Riverbed conductance **$C_{RIV}$ = % 10.2E"% C, " m²/s**")
            st.write("- Flow between river and aquifer **$Q_{RIV}$ = % 10.2E"% Q_ref," m³/s**")

Q_h_plot()
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
