import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc, erf
import math
from streamlit_book import multiple_choice
import json
from streamlit_scroll_to_top import scroll_to_here
from GWP_SFI_utils import read_md

# ---------- Track the current page
PAGE_ID = "SEARISE"

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
path_quest_ini   = st.session_state.module_path + "questions/sealevelrise_initial.json"
path_quest_exer =  st.session_state.module_path + "docs/sealevelrise_exer.json"
path_quest_final = st.session_state.module_path + "questions/sealevelrise_final.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)

#---------- FUNCTIONS
def sea_surface(x, theta):
    x = np.linspace(0, xmax, 1000)
    return np.tan(np.radians(theta)) * x

def sealevelrise(z0, W, K, L0, rho_f, rho_s, theta, delta_z0, x):

    delta_rho = rho_s - rho_f
    alpha = ((W * delta_rho) / (K * (rho_f + delta_rho)))**0.5
    h_x = alpha*(L0**2 - x**2)**0.5
    z_x = (rho_f / delta_rho) * h_x
    beta = rho_f / delta_rho   
    x_T = (L0**2 - (z0 / (alpha * beta))**2)**0.5
    I_x = delta_z0 + ((-alpha**2 * delta_z0) / np.tan(np.radians(theta)) * (2 * L0 - delta_z0 / np.tan(np.radians(theta))) + h_x**2)**0.5 - h_x
    delta_x_T = ((L0 - (delta_z0/np.tan(np.radians(theta))))**2 -((z0 + delta_z0) / (alpha * beta))**2)**0.5 - (L0**2 - (z0/(alpha*beta))**2)**0.5
    delta_L = delta_z0/np.tan(np.radians(theta))
    inu = delta_L * np.tan(np.radians(theta))
#    h_new_x = alpha*(((L0-delta_z0/np.tan(np.radians(theta)))**0.5 - x**2)**0.5 - (L0**2-x**2)**0.5) 
#    h_new_x = delta_z0 + ((-alpha**2 * delta_z0) / np.tan(np.radians(theta)) * (2 * L0 - delta_z0 / np.tan(np.radians(theta))) + h_x**2)**0.5
    h_new_x = h_x + I_x
    I_new_x = (rho_f / delta_rho) * (h_x - I_x)
    z_new_x = (rho_f / delta_rho) * (h_new_x- delta_z0)
    delta_V =  (z0+delta_z0) * (x_T-delta_x_T) - z0 * x_T + (alpha * np.pi * (1 + beta) / 4) * ((L0-delta_L)**2 - L0**2) + alpha * beta * (x_T * (L0**2 + x_T**2)**0.5 - (x_T-delta_x_T) * ((L0-delta_L)**2 + (x_T-delta_x_T)**2)*0.5)
    return h_x, z_x, x_T, I_x, delta_x_T, delta_L, h_new_x, z_new_x, delta_V

def update_K():
    st.session_state.K = st.session_state.K_input
def update_n():
    st.session_state.n = st.session_state.n_input
def update_W():
    st.session_state.W = st.session_state.W_input
def update_z0():
    st.session_state.z0 = st.session_state.z0_input
def update_rho_s():
    st.session_state.rho_s = st.session_state.rho_s_input
def update_rho_f():
    st.session_state.rho_f = st.session_state.rho_f_input
def update_L0():
    st.session_state.L0 = st.session_state.L0_input
def update_theta():
    st.session_state.theta = st.session_state.theta_input
def update_delta_z0():
    st.session_state.delta_z0 = st.session_state.delta_z0_input
def update_h0_x():
    st.session_state.h0_x = st.session_state.h0_x_input
def land_surface(x, theta, xmin):
    return -np.tan(np.radians(theta)) * x + xmin
    
#---------- UI Starting here

st.title("Sea Level Rise")
st.subheader('Describing the impact of :red[sea level rise] on the freshwater-saltwater interface location', divider= "red")

st.markdown("""
#### 💡 Motivation: Why investigate Sea-Level Rise in Coastal Aquifers?

- Shows how **sea-level rise** can cause **landward migration of the saltwater wedge**, change water-table elevations, and alter freshwater storage, even without pumping.

- Provides a transparent way to explore interactions between sea-level change, recharge, aquifer slope, and hydraulic properties in a **sloping coastal aquifer**.

- Helps identify which coastal settings are **most vulnerable** to sea-level rise.
""")

st.markdown(r"""
#### 🎯 Learning Objectives

This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual model and analytical formulation used to describe how sea-level rise affects water-table elevation, the position of the saltwater toe, and freshwater volume in a sloping unconfined coastal aquifer.

- Quantify **changes in interface position and freshwater storage** for specified sea-level rise scenarios and aquifer parameters (recharge, K, slope, density contrast).

- Evaluate the sensitivity of different coastal aquifer types to sea-level rise.
""")


st.markdown(r"""
### **Introduction**  

Sea-level rise is expected to alter not only coastlines at the surface, but also the **position and thickness of coastal freshwater bodies** that many communities rely on. In unconfined coastal aquifers, freshwater recharged inland flows toward the sea and overlies denser seawater, forming a wedge-shaped saltwater body. When mean sea level rises, the shoreline can migrate inland, the hydraulic gradient from land to sea can change, and the freshwater–saltwater interface may move landward and upward, with consequences for groundwater levels and freshwater storage.
In this formulation, the initial position of the **saltwater toe** $x_T$ is obtained from a closed-form expression that links the interface depth at the coast, the aquifer geometry and the density contrast: 

$$
x_T = \sqrt{L_0^2 - \left(\frac{z_0}{\alpha \beta}\right)^2}
$$

where $L_0$ is the initial aquifer width, $z_0$ is the initial depth from sea level down to the aquifer base, and the composite parameters

$$
\alpha = \sqrt{\frac{W \,\Delta \rho}{K \,(\rho_f + \Delta \rho)}}\quad\text{and}\quad\beta = \frac{\rho_f}{\Delta \rho}
$$
combine the effects of **recharge** $W$, **hydraulic conductivity** $K$, and the **density difference** $\Delta$ $\rho$ = $\rho_s$ - $\rho_f$ between seawater $\rho_s$ and freshwater $\rho_f$. These expressions define how far inland the saltwater toe extends under initial (pre–sea-level-rise) conditions for a given set of aquifer and fluid properties.
When **sea level changes** by $\Delta z_0$, the **water-table elevation** adjusts along the sloping aquifer. The vertical change in water-table height at any inland position $x$, denoted $I(x)$, can be written as

$$
I(x) = \Delta z_0 + \sqrt{\frac{-\alpha^2 \Delta z_0}{\tan\theta}\left(2L_0 - \frac{\Delta z_0}{\tan\theta}\right)+ h_0(x)^2}- h_0(x),
$$

where $\theta$ is the **slope of the coastal aquifer**, and $h_0(x)$ is the **initial water-table elevation** at position $x$. This relation shows how a rise in sea level can lead to water-table rise inland, with the response controlled by aquifer slope, recharge and the initial head distribution.

The **landward migration of the saltwater toe** due to sea-level rise is quantified through the change $\Delta x_T$:

$$
\Delta x_T =\sqrt{\left(L_0 - \frac{\Delta z_0}{\tan\theta}\right)^2 - \left(\frac{z_0 + \Delta z_0}{\alpha\beta}\right)^2}-\sqrt{L_0^2 - \left(\frac{z_0}{\alpha\beta}\right)^2}.
$$

A positive $\Delta x_T$ indicates that the toe has moved further inland, reducing the width of the freshwater zone.

Finally, the model allows the **change in freshwater volume** $\Delta V$ (per unit width of aquifer) to be estimated from the change in toe position and aquifer geometry:

$$
\Delta V = S_t x_{Tt} - S_0 x_{T0}+ \frac{\alpha \pi (1 + \beta)}{4} \left(L_t^2 - L_0^2\right)+ \alpha \beta \left(x_{T0} \sqrt{L_0^2 + x_{T0}^2}- x_{Tt} \sqrt{L_t^2 + x_{Tt}^2}\right),
$$

where $S_0$ and $S_t$ are the cross-sectional freshwater areas at the initial and final states, $x_{T0}$ and $x_{Tt}$ are the initial and final toe positions, and $L_0$ and $L_t$ are the initial and final aquifer widths.
These equations provide a compact way to explore sensitivity to sea-level rise without running a full variable-density numerical model.

The conceptual model rests on a number of simplifying assumptions. Flow is treated as **one-dimensional Dupuit flow** in a **homogeneous, isotropic, unconfined aquifer**, with **constant recharge** and a **sharp freshwater–saltwater interface** (no explicit mixing zone, dispersion or diffusion). The inland boundary is a **fixed-location no-flow boundary**, so the system represents a **flux-controlled aquifer** where the total freshwater throughflow is prescribed, rather than a head-controlled system where inland heads are fixed by rivers, lakes, pumping or drainage. As pointed out by Morgan and Werner (2016), this means the Chesnaux solution is appropriate for continental or island aquifers bounded inland by a groundwater divide, but not for cases where inland heads are tightly constrained by surface water bodies or strong pumping; in those situations, other analytical or numerical models are more suitable.
""", unsafe_allow_html=True)
st.subheader('Interactive Plot and Exercise', divider="orange")
st.markdown(""" #### :orange[INPUT CONTROLS]""")

# 3.49 ersetzen mit irgendwas: xmax = z0/np.tan(np.radians(theta))

st.session_state.z0=50
st.session_state.W=0.0014
st.session_state.K=50
st.session_state.L0=1000
st.session_state.rho_f=1000
st.session_state.rho_s=1025
st.session_state.theta=2
st.session_state.delta_z0=0.0
st.session_state.n = 0.15

columns1 = st.columns((1,1,1), gap = 'small')
with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            st.session_state.number_input = st.toggle(r"Toggle to use Slider or Number for input of $K$, $n$, $z0$, $\theta$, $L0$, $\rho_f$, $\rho_s$, $W$, $h0_{x}$, and $\Delta_z0$.")
            reset = st.button(':red[Reset the plot to the initial values]')
            if reset:
                st.session_state.z0=50
                st.session_state.W=0.0014
                st.session_state.K=50
                st.session_state.L0=1000
                st.session_state.rho_f=1000
                st.session_state.rho_s=1025
                st.session_state.theta=2
                st.session_state.delta_z0=0.5
                st.session_state.n = 0.15

with columns1[1]:
        with st.expander('Modify :orange[**Aquifer properties**]'):
            if st.session_state.number_input:
                K = st.number_input(":green[**Hydraulic conductivity** $K$ (m/d)]", 1, 100, st.session_state.K, 1, key="K_input", on_change=update_K)
            else:
                K = st.slider      (":green[**Hydraulic conductivity** $K$ (m/d)]", 1, 100, st.session_state.K, 1, key="K_input", on_change=update_K)
            if st.session_state.number_input:
                n = st.number_input(":blue[**Porosity** $n$ ]", 0.05, 0.4, st.session_state.n, 0.01, key="n_input", on_change=update_n)
            else:
                n = st.slider      (":blue[**Porosity** $n$ ]", 0.05, 0.4, st.session_state.n, 0.01, key="n_input", on_change=update_n)
            if st.session_state.number_input:
                z0 = st.number_input(":red[**Aquifer basement depth** $z0$ (L)]", 1, 200, st.session_state.z0, 1, key="z0_input", on_change=update_z0)
            else:
                z0 = st.slider      (":red[**Aquifer basement depth** $z0$ (L)]", 1, 200, st.session_state.z0, 1, key="z0_input", on_change=update_z0)
            if st.session_state.number_input:
                theta = st.number_input(r":orange[**Slope of coastal aquifer** $\theta$]", 1, 25, st.session_state.theta, 1, key="theta_input", on_change=update_theta)
            else:
                theta = st.slider      (r":orange[**Slope of coastal aquifer** $\theta$]", 1, 25, st.session_state.theta, 1, key="theta_input", on_change=update_theta)
            if st.session_state.number_input:
                L0 = st.number_input(":orange[**Initial width of the aquifer** $L0$]", 1, 2000, st.session_state.L0, 1, key="L0_input", on_change=update_L0)
            else:
                L0 = st.slider      (":orange[**Initial width of the aquifer** $L0$]", 1, 2000, st.session_state.L0, 1, key="L0_input", on_change=update_L0)

with columns1[2]:
        with st.expander('Modify :blue[**Density and freshwater head/sea level rise**]'):
            if st.session_state.number_input:
                rho_f = st.number_input(r":green[**Freshwater Density** $\rho_f$ (kg/m³)]", 950, 1050, st.session_state.rho_f, 1, key="rho_f_input", on_change=update_rho_f)
            else:
                rho_f = st.slider      (r":green[**Freshwater Density** $\rho_f$ (kg/m³)]", 950, 1050, st.session_state.rho_f, 1, key="rho_f_input", on_change=update_rho_f)
            if st.session_state.number_input:
                rho_s = st.number_input(r":blue[**Saltwater Density** $\rho_s$ (kg/m³)]", 950, 1050, st.session_state.rho_s, 1, key="rho_s_input", on_change=update_rho_s)
            else:
                rho_s = st.slider      (r":blue[**Saltwater Density** $\rho_s$ (kg/m³)]", 950, 1050, st.session_state.rho_s, 1, key="rho_s_input", on_change=update_rho_s)
            if st.session_state.number_input:
                W = st.number_input(":green[**Recharge** $W$ (m³/)]", 0.0, 0.002, st.session_state.W, 0.0001, key="W_input", on_change=update_W)
            else:
                W = st.slider      (":green[**Recharge** $W$ (m³/)]", 0.0, 0.002, st.session_state.W, 0.0001, key="W_input", on_change=update_W)
            if st.session_state.number_input:
                delta_z0 = st.number_input(r":blue[**Sea level rise** $\Delta_z0$ (m)]", 0.0, 3.5, st.session_state.delta_z0, 0.1, key="delta_z0_input", on_change=update_delta_z0)
            else:
                delta_z0 = st.slider      (r":blue[**Sea level rise** $\Delta_z0$ (m)]", 0.0, 3.5, st.session_state.delta_z0, 0.1, key="delta_z0_input", on_change=update_delta_z0)
# Ensure physical consistency: rho_s > rho_f
if rho_s <= rho_f:
    st.warning(
        "Saltwater density must be greater than freshwater density. "
        "Adjusting ρ_s to ρ_f + 1 kg/m³."
    )
    rho_s = rho_f + 1
    st.session_state.rho_s = rho_s

#Calculation
x_land = np.linspace(0, L0, 10000) 
xmax = z0/np.tan(np.radians(theta))
xmin = L0*np.tan(np.radians(theta))
x_sea = np.linspace(L0, L0 +xmax , 1000)
y_land = land_surface(x_land, theta, xmin)
y_sea = sea_surface(x_sea, theta)
h_x, z_x, x_T, I_x, delta_x_T, delta_L, h_new_x, z_new_x, delta_V = sealevelrise(z0, W, K, L0, rho_f, rho_s, theta, delta_z0, x_land)
delta_FWV = delta_V*n
inundation = np.linspace(L0-delta_L, L0, 100)
new_sealevel = np.piecewise(
    x_land,
    [x_land < L0 - delta_L, x_land >= L0 - delta_L],
    [-z0, lambda x: land_surface(x, theta, xmin)]
)

# PLOT FIGURE 
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)

# Freshwater heads
ax.plot(x_land, h_x, color = 'skyblue', linestyle=':')
ax.plot(x_land, h_new_x, color = 'skyblue')
# Interface
ax.plot(x_land,-z_x, color = 'red', linestyle=':')
ax.plot(x_land,-z_new_x + delta_z0 , color = 'red')
# Diagonal lines (?)
ax.plot(x_sea, -y_sea, c="black")
ax.plot(x_land, y_land, c="black")

ax.fill_between(x_land,h_x,h_new_x, facecolor='lightblue', alpha= 0.5)

ax.hlines(-z0, 0, L0+xmax, color = 'black', linewidth = 5) # Bottom of the plot
ax.hlines(0, L0, L0+xmax, color='black', linestyle=':')     # Original sea level
ax.hlines(delta_z0, L0-delta_L, L0 + xmax, color='blue')   # new sea level

ax.fill_between(x_land, -z_x, -z0, facecolor='cornflowerblue', hatch = '//')
ax.fill_between(x_sea-1, -y_sea, -z0, facecolor='cornflowerblue', hatch = '//')

ax.fill_between(x_sea, 0, -y_sea, facecolor='royalblue')
ax.fill_between(x_sea, delta_z0, 0, facecolor='royalblue', alpha=0.5)

ax.fill_between(x_land, delta_z0, np.maximum(y_land,0), facecolor='royalblue', alpha=0.5, where=(x_land >= L0-delta_L))

ax.fill_between(x_land, np.maximum(-z_new_x + delta_z0, -z_x), -z_x, facecolor='red', alpha=0.5, hatch='//')
ax.fill_between(x_land, np.maximum(new_sealevel, -z_x), -z_x, facecolor='red', alpha=0.5, hatch='//')

ax.fill_between(x_land, 0, h_x, facecolor='lightskyblue', alpha=0.5)
ax.fill_between(x_land, 0, -z_x, facecolor='lightskyblue', alpha=0.5)
ax.legend(loc = 'lower left', fontsize=12)
#plt.text(-z0, L0 + xmax, 'θ', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(1180, -20, 'Sea', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(1180, -80, 'Saltwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(150, -10, 'Freshwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
ax.set(xlabel='x [m]', ylabel='head [m]',title='Sea level rise')
plt.ylim(-z0, 15)
plt.xlim(0,L0 + xmax)

st.pyplot(fig)

st.write("Initial position of interface toe:", x_T, "m")
st.write("Change of interface toe position:", delta_x_T, "m")
st.write("Loss of width of aquifer:", delta_L, "m")
st.write("Change of aquifer volume:", delta_V, "m**3")
st.write("Change of freshwater volume:", delta_FWV, "m**3")

with st.expander('Show the :rainbow[**EXERCISE**]', icon ="🧩"):
    st.markdown(r"""
    ### 📘 Exercise – Comparing well designs and pumping strategies

🎯 Expected Learning Outcomes:


""")

st.subheader('✔️ Conclusion', divider = 'violett')
st.markdown("""
The **sea-level rise app** demonstrates how **changes at the coastal boundary** affect groundwater heads, the position of the saltwater toe, and the volume of stored freshwater in unconfined coastal aquifers. Using an analytical sharp-interface solution, it links **sea-level change**, **recharge**, **aquifer slope**, **hydraulic conductivity**, and **density contrast** to the inland migration of the saltwater wedge and changes in freshwater storage.

By adjusting parameters such as **sea-level rise** $\Delta z_0$, **coastal slope**, and **$K$**, you can compare responses of different idealised coastal settings, from low-lying, gently sloping aquifers to steeper, more transmissive ones. The app highlights why gently sloping coasts can be especially vulnerable: a modest vertical rise in sea level can lead to a large horizontal shift of the shoreline and saltwater toe. At the same time, the tool reinforces that it is a **screening model**, based on homogeneity, a sharp interface, and steady recharge, and does not resolve full 3D salinity patterns or complex infrastructure.

Together with the **Ghyben–Herzberg**, **Glover**, and **upconing** apps, this tool completes the picture of coastal aquifers under combined pressures from **natural gradients**, **human pumping**, and **climate-driven sea-level change**. After studying this section on sea-level rise, you may wish to consolidate your understanding by working through the final assessment for this app.
""")

with st.expander('**Show self-test** - to assess your EXISTING knowledge'):
    st.markdown("""
    #### 📋 Self-test
    You can use the initial questions to assess your existing knowledge.
    Questions need to be transfered to a json-file. The import routine can be find in line 27-29

**Which of the following effects are expected when sea level rises but recharge remains constant?**

A. The saltwater toe tends to move landward, reducing the width of the freshwater zone. ✅

B. The water table near the coast can rise, potentially increasing groundwater levels in low-lying areas. ✅

C. The aquifer’s freshwater volume may decrease, because a larger part of the aquifer cross-section is occupied by saltwater. ✅

D. The porosity n automatically decreases as sea level rises.

**Which statement best reflects how K influences the response?**

A. Higher K (Aquifer B) allows freshwater to drain more efficiently toward the sea, so the relative inland movement of the saltwater toe for a given sea-level rise is generally smaller. ✅

B. Higher K always leads to a larger inland movement of the saltwater toe.

C. The position of the saltwater toe does not depend on K at all.

D. K only affects porosity and has no hydraulic significance in this model.

**Which of the following management conclusions are consistent with what this analytical sea-level rise model can show?**

A. The use of a sharp interface and homogeneous conditions is sufficient for detailed management decisions.

B. Even without pumping, sea-level rise alone can gradually reduce freshwater storage and move saltwater closer to existing wells. ✅

C. The analytical model should be used as a screening tool, and areas that appear highly vulnerable may warrant more detailed numerical modelling and field investigations. ✅

D. Low-lying, gently sloping coasts (small theta) are particularly vulnerable to inland movement of the saltwater wedge for a given sea-level rise. ✅

**Two coastal aquifers are identical in all respects (recharge, K, densities, z0, L0, delta_z0) except for the slope of the coastline. Which statement is most consistent with the result?**

A. Both aquifers respond the same way; slope has no effect on seawater intrusion.

B. The gently sloping Aquifer A is more vulnerable to inland migration of the saltwater wedge and loss of freshwater volume for the same sea-level rise. ✅

C. A steeper slope means greater landward intrusion because the interface is nearly vertical.

D. The travel time at steeper coastlines are always longer and therefore result in greater saltwater intrusion.

**Which consequences of sea-level rise are likely to promote a landward movement of the freshwater–saltwater interface?

A. An increase in long-term recharge, which raises inland groundwater levels more than sea level.

B. A decrease in seawater density, making seawater less dense than before.

C. A landward shift of the coastline, which reduces the horizontal distance between the sea and the freshwater body. ✅

D. A rise in mean sea level that reduces the hydraulic gradient from land to sea, so less freshwater is discharged seaward. ✅""")

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
