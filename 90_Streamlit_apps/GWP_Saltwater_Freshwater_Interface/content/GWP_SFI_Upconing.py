import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt
from streamlit_book import multiple_choice
import json
from streamlit_scroll_to_top import scroll_to_here
from GWP_SFI_utils import read_md

# ---------- Track the current page
PAGE_ID = "UPCONE"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID

# ---------- Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# ---------- Authors, institutions, and year
year = 2025 
authors = {
    "Markus Giese": [1],  # Author 1 belongs to Institution 1
    "Thomas Reimann": [2],
    "Nils Wallenberg": [1]
}
institutions = {
    1: "University of Gothenburg, Department of Earth Sciences",
    2: "TU Dresden, Institute for Groundwater Management",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# ---------- Define paths, loading files
path_quest_ghp = st.session_state.module_path + "questions/exer_ghp.json"

#---------- UI Starting here
st.title("Upconing")
st.subheader('Describing the :orange[upconing] of the freshwater-saltwater interface due to pumping', divider= "orange")


st.markdown(r"""
### **Introduction**  

In aquifers where saline groundwater lies beneath freshwater, pumping can disturb the balance between the two. When pumping lowers the piezometric head in the freshwater zone, the underlying saltwater responds by moving upward toward the well. This process is known as interface upconing.
Upconing is a particular concern in heavily exploited coastal aquifers, where groundwater is the main source of drinking water. In such areas, over-pumping and illegal abstractions can significantly lower groundwater heads, allowing the saline–freshwater interface to rise. If pumping continues, the interface may eventually reach the well screen. Once this happens, the pumped water becomes increasingly saline and unsuitable for domestic use, forcing a reduction or complete stop of pumping.
To avoid or limit these negative effects, the pumping rate must be kept below a critical value, so that the drawdown of the piezometric head stays within acceptable limits. If pumping is reduced sufficiently, the interface can gradually move back downward toward its original position, although this recovery is usually slow because of the long response times of aquifer systems. Another management option is to relocate wells or to distribute pumping over several wells instead of a single high-capacity well.
Based on a sharp-interface concept and a number of simplifying assumptions (homogeneous aquifer, steady pumping, axisymmetric flow, and clear density contrast between fresh and saline water), analytical solutions have been developed to estimate the amount of upconing beneath a pumping well (Bear & Dagan, 1964; Dagan & Bear, 1968; Schmorak & Mercado, 1969). These solutions are widely used for screening-level assessments and teaching, helping to identify safe pumping rates and understand the key controls on upconing, before more detailed numerical modelling is applied.
coning of the saltwater interface can occur when the aquifer (freshwater) head is lowered by pumping from wells. Schmork and Mercado (1969) and Dagan and Bear (1968) developed equations to calculate upconing and determine the maximum well pumping rate at a new equilibrium caused by pumping. In these calculations, the pumping well is considered as a point.

The maximum upconing, which occurs directly underneath the pumping well, can be calculated as:

$$ 
z(0) = \frac{Q}{2 \pi d K \Delta \rho} 
$$

As a guideline, Dagan and Bear (1969) propose that the interface will remain stable if the upconed height ($z$) does not exceed the critical elevation, which is defined as one-third of $d$ (Callander et al., 2011). Based on this, the permitted pumping rate should not exceed:

$$ 
Q_{\text{max}} \leq \frac{0.6 \pi d^2 K}{\Delta \rho} 
$$

where
$$ 
\Delta \rho = \frac{\rho_s - \rho_f}{\rho_f} 
$$
and

- $z$ = new equilibrium elevation (distance between the upconed and original interface) [L],
- $Q$ = pumping rate [L³/T],
- $d$ = pre-pumping distance from base of well to interface [L],
- $K$ = hydraulic conductivity [L/T].

In literature, the safety factor varies from 0.25 to 0.6 considering how strict the water-quality target is, how thick the mixing zone is assumed to be, and how conservative the design is.

To calculate the upconing at any distance ($x$) from the well, the following equation can be used under steady-state conditions $( t \to \infty ) $ (Bear, 1999):

$$ 
z(x) = \left( \frac{1}{\sqrt{\frac{x^2}{d^2} + 1}} - \frac{1}{\sqrt{\frac{x^2}{d^2} + \left(1 + \frac{\Delta \rho K t}{n d (2 + \Delta \rho)}\right)^2}} \right) \frac{Q}{2 K \pi d \Delta \rho} 
$$

where

- $n$ = porosity [-],
- $t$ = time [T],
- $x$ = distance from the well [L].
""", unsafe_allow_html=True)

#with st.expander('**References**'):
#    st.markdown(r"""
#Bear, J. (Ed.), 1999. Seawater intrusion in coastal aquifers: concepts, methods and practices, Theory and applications of transport in porous media. Kluwer, Dordrecht.

#Callander, P., Lough, H., Steffens, C., 2011. New Zealand Guidelines for the Monitoring and Management of Sea Water Intrusion Risks on Groundwater. Pattle Delamore Partners LTD, New Zealand.

#Schmork, S., Mercado, A., 1969. Upconing of Fresh Water-Sea Water Interface Below Pumping Wells, Field Study. Water Resources Research 5, 1290–1311. doi: 10.1029/WR005i006p01290

#Dagan, G., Bear, J., 1968. Solving The Problem Of Local Interface Upconing In A Coastal Aquifer By The Method Of Small Perturbations. Journal of Hydraulic Research 6, 15–44. doi: 10.1080/00221686809500218
#""", unsafe_allow_html=True)

st.subheader('Interactive Plot and Exercise', divider="orange")
st.markdown(""" #### :orange[INPUT CONTROLS]""")
# Callback function to update session state
def update_K():
    st.session_state.K = st.session_state.K_input
def update_n():
    st.session_state.n = st.session_state.n_input
def update_Q():
    st.session_state.K = st.session_state.K_input
def update_d_pre():
    st.session_state.n = st.session_state.n_input
def update_rho_s():
    st.session_state.rho_s = st.session_state.rho_s_input
def update_rho_f():
    st.session_state.rho_f = st.session_state.rho_f_input
# User inputs
def upconing(x, Q, K, d_pre, rho_f, rho_s, n):
    # Compute values
    t = np.inf
    z = (1/(x**2/d_pre**2+1)**0.5-1/(x**2/d_pre**2+(1+((rho_s - rho_f)/rho_f)*K*t/(n*d_pre*(2+(rho_s - rho_f)/rho_f)))**2)**0.5)* Q/(2*np.pi*d_pre*K*((rho_s - rho_f)/rho_f))
    z_0 = Q*(rho_f/(rho_s - rho_f))/(2*np.pi*d_pre*K)
    Q_max = (0.6*np.pi*d_pre**2*K)/(rho_f/(rho_s - rho_f))
    z_max = Q_max*(rho_f/(rho_s - rho_f))/(2*np.pi*d_pre*K)
    
    return z, z_0, Q_max, z_max
   
# Parameter / Input

st.session_state.K = 50
st.session_state.Q = 100
st.session_state.n = 0.15
st.session_state.d_pre = 25
st.session_state.rho_f = 1000
st.session_state.rho_s = 1025


columns1 = st.columns((1,1,1), gap = 'small')
with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            st.session_state.number_input = st.toggle(r"Toggle to use Slider or Number for input of $K$, $n$, $Q$, $d_{pre}$, $\rho_f$ and $\rho_s$.")
            reset = st.button(':red[Reset the plot to the initial values]')
            if reset:
                st.session_state.K = 50
                st.session_state.Q = 100
                st.session_state.n = 0.15
                st.session_state.d_pre = 25
                st.session_state.rho_f = 1000
                st.session_state.rho_s = 1025

with columns1[1]:
        with st.expander('Modify :orange[**Aquifer properties and well design**]'):
            if st.session_state.number_input:
                K = st.number_input(":green[**Hydraulic conductivity** $K$ (m/d)]", 1, 100, st.session_state.K, 1, key="K_input", on_change=update_K)
            else:
                K = st.slider      (":green[**Hydraulic conductivity** $K$ (m/d)]", 1, 100, st.session_state.K, 1, key="K_input", on_change=update_K)
            if st.session_state.number_input:
                n = st.number_input(":blue[**Porosity** $n$ ]", 0.05, 0.4, st.session_state.n, 0.01, key="n_input", on_change=update_n)
            else:
                n = st.slider      (":blue[**Porosity** $n$ ]", 0.05, 0.4, st.session_state.n, 0.01, key="n_input", on_change=update_n)
            if st.session_state.number_input:
                Q = st.number_input(":red[**Pumping rate** $Q$ (m3/d)]", 50, 2500, st.session_state.Q, 1, key="Q_input", on_change=update_Q)
            else:
                Q = st.slider      (":red[**Pumping rate** $Q$ (m3/d)]", 50, 2500, st.session_state.Q, 1, key="Q_input", on_change=update_Q)
            if st.session_state.number_input:
                d_pre = st.number_input(":orange[**Pre-pumping distance** $d_{pre}$ (m)]", 1, 200, st.session_state.d_pre, 1, key="d_pre_input", on_change=update_d_pre)
            else:
                d_pre = st.slider      (":orange[**Pre-pumping distance** $d_{pre}$ (m)]", 1, 200, st.session_state.d_pre, 1, key="d_pre_input", on_change=update_d_pre)

with columns1[2]:
        with st.expander('Modify :blue[**Density**]'):
            if st.session_state.number_input:
                rho_f = st.number_input(r":green[**Freshwater Density** $\rho_f$ (kg/m³)]", 950, 1050, st.session_state.rho_f, 1, key="rho_f_input", on_change=update_rho_f)
            else:
                rho_f = st.slider      (r":green[**Freshwater Density** $\rho_f$ (kg/m³)]", 950, 1050, st.session_state.rho_f, 1, key="rho_f_input", on_change=update_rho_f)
            if st.session_state.number_input:
                rho_s = st.number_input(r":blue[**Saltwater Density** $\rho_s$ (kg/m³)]", 950, 1050, st.session_state.rho_s, 1, key="rho_s_input", on_change=update_rho_s)
            else:
                rho_s = st.slider      (r":blue[**Saltwater Density** $\rho_s$ (kg/m³)]", 950, 1050, st.session_state.rho_s, 1, key="rho_s_input", on_change=update_rho_s)
# Ensure physical consistency: rho_s > rho_f
if rho_s <= rho_f:
    st.warning(
        "Saltwater density must be greater than freshwater density. "
        "Adjusting ρ_s to ρ_f + 1 kg/m³."
    )
    rho_s = rho_f + 1
    st.session_state.rho_s = rho_s

#Calculation
x = np.arange(-1000, 1000, 0.25)
z, z_0, Q_max, z_max = upconing(x, Q, K, d_pre, rho_f, rho_s, n)

# Plot Glover equation results
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(x,z, color='darkblue', linewidth=2.5, label='Saltwater Interface')
plt.ylim(-5, d_pre+3)
plt.xlim(-1000, 1000)
ax.fill_between(x,z,-5, facecolor='cornflowerblue', hatch = '//')
ax.fill_between(x,z,max(z_0, d_pre +3), facecolor='lightskyblue', alpha=0.5)
ax.hlines(z_max, -1000, 1000, color = 'red', linestyle = "dashed", label='Critical upconing elevation')
ax.vlines(0, d_pre, max(z_0, d_pre +3), linewidth=10, color = 'darkgrey')
ax.vlines(2, d_pre+0.1, max(z_0, d_pre +3), linewidth=2, color = 'silver')
ax.hlines(d_pre+2,-15, 15, color = 'grey')
ax.hlines(d_pre+1.5,-15, 15, color = 'grey')
ax.hlines(d_pre+1,-15, 15, color = 'grey')
ax.hlines(d_pre+0.5,-15, 15, color = 'grey')
ax.set_xlabel('Distance from Well (m)')
ax.set_ylabel('Height above initial water table (m)')
ax.set_title("Upconing")
ax.legend(loc="upper right")
#ax.grid()
plt.text(-100, d_pre+1, 'Pumping well', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(0, -3, 'Saltwater', horizontalalignment='center', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(-950, 2.5, 'Freshwater', horizontalalignment='left', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
    
st.pyplot(fig)
    
st.write(f"**Maximum upconing:** {z_0:.2f} m")
st.write(f"**Critical pumping rate:** {Q_max:.3f} m³/d")
st.write(f"**Critical upconing elevation:** {z_max:.2f} m")

with st.expander('Show the :rainbow[**EXERCISE**]', icon ="🧩"):
    st.markdown(r"""
    ### 📘 Exercise – Comparing well designs and pumping strategies

🎯 Expected Learning Outcomes:

Completion of this exercise helps you to accomplish the following.

- Understand how the hydrological conditions and pump design influence the risk of upconing
- Develop the knowledge to guide sustainable well-field design in coastal areas. 

A coastal water utility is planning to supply a small town using groundwater from an aquifer where saline water underlies freshwater. They are considering two alternative designs:

1. **Design A – One deep, high-capacity well**  
   - One fully penetrating well located close to the coast  
   - Screened close to the initial interface  
   - High pumping rate to meet the entire demand with a single well  

2. **Design B – Several shallower, lower-capacity wells**  
   - A cluster of wells further inland  
   - Each well has a shallower screen, farther above the interface  
   - Lower pumping rate per well, with the total demand shared between them  

Use the **upconing app** and explore how upconing under a single **deep, strongly pumped well** compares to that under **multiple shallow wells with lower pumping rates**.
Therefore systematically vary
  - pumping rate $Q$,
  - pre-pumping distance $d_{pre}$,
  - hydraulic conductivity $K$,
  - porosity $n$,
  - and density contrast $\Delta \rho$

and analyse how each affects the **maximum upconing at the well** and the **critical pumping rate**.
Discuss which design (A or B) is more robust against salinisation and under what conditions the difference between the designs becomes most pronounced.
""")

with st.expander('**Show self-test** - to assess your EXISTING knowledge'):
    st.markdown("""
    #### 📋 Self-test
    You can use the initial questions to assess your existing knowledge.
    Questions need to be transfered to a json-file. The import routine can be find in line 27-29

**Which of the following statements about upconing are correct?**

A. Upconing is the upward movement of the saltwater–freshwater interface below a pumping well caused by lowering of freshwater heads. ✅

B. Upconing occurs only when the pumping rate exceeds the critical rate Q_{max}

C. Upconing can occur even at relatively low pumping rates if the initial distance d between the well and the interface is small. ✅

D. Upconing is driven solely by molecular diffusion and does not depend on pumping.

**Which of the following parameter changes would tend to increase the amount of upconing z(0), assuming all other parameters remain constant?**

A. Increasing the pumping rate Q. ✅

B. Increasing hydraulic conductivity K.

C. Decreasing the pre-pumping distance d between the well screen and the interface. ✅

D. Increasing the density difference

**The analytical upconing solution used in your app is based on several simplifying assumptions. Which of the following are standard assumptions in these models?**

A. The interface between fresh and saline groundwater is sharp, with no transition zone. ✅

B. The aquifer is homogeneous, isotropic and of uniform thickness. ✅

C. Flow to the well is axisymmetric, and the well is treated as a point sink. ✅

D. The model fully accounts for complex density-dependent flow and dispersion in a thick mixing zone.

**Which design choices typically reduce the risk of salinisation due to upconing?**

A. Using several shallow wells with lower pumping rates instead of one deep, heavily pumped well. ✅

B. Placing well screens as close as possible to the initial interface to maximise yield.

C. Increasing the distance between the well and the coastline, where feasible. ✅

D. Concentrating all abstraction in a single well field close to the coast.

**In the classical sharp-interface upconing solution, which parameter primarily affects the time scale over which the interface approaches its maximum rise beneath the well, but does not change the steady-state maximum upconing height at the well?**

A. Hydraulic conductivity 

B. Pumping rate 

C. Pre-pumping distance between well screen and interface

D. Effective porosity ✅""")


    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_sfi[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_sfi[i]["options"],
                success=quest_sfi[i].get("success", "✅ Correct."),
                error=quest_sfi[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_sfi[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_sfi[i]["options"],
                success=quest_sfi[i].get("success", "✅ Correct."),
                error=quest_sfi[i].get("error", "❌ Not quite.")
            )

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image(st.session_state.module_path + 'images/CC_BY-SA_icon.png')