import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_SFI_utils import read_md

# TO DO: 
# - Json-files (existing!) instead of questions
# - Import of questions


# ---------- Track the current page
PAGE_ID = "GLO"

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
# --- path to questions for the assessments (direct path)
path_quest_ini   = st.session_state.module_path + "questions/glover_initial.json"
path_quest_exer =  st.session_state.module_path + "docs/glover_exer.json"
path_quest_final = st.session_state.module_path + "questions/glover_final.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)

#---------- FUNCTIONS
def glover(i, b, rho_f, rho_s):
    h = (2 * i * b * (1000 - x_land) * rho_f / (rho_s - rho_f))**0.5
    z = (2 * i * b * (1000 - x_land) / (rho_s - rho_f) + (i * b * rho_f / (rho_s - rho_f))**2)**0.5
    z_0 = (rho_f / (rho_s - rho_f)) * i * b
    L = (i * b * rho_f) / (2 * (rho_s - rho_f))
    x_f = (b * (rho_s - rho_f)) / (2 * i * rho_f)
    return h, z, z_0, L, x_f
    
def sea_surface(x, p):
    """Erzeugt eine gekrümmte ansteigende Funktion von (1000,0) bis (1200,30) mit starkem Anfangsgradient."""
    return 50 * (1 - ((1200 - x) / 200) ** p)*-1

# Callback function to update session state
def update_b():
    st.session_state.b = st.session_state.b_input
def update_i():
    st.session_state.i = st.session_state.i_input
def update_rho_s():
    st.session_state.rho_s = st.session_state.rho_s_input
def update_rho_f():
    st.session_state.rho_f = st.session_state.rho_f_input

#---------- UI Starting here
st.title('Glover Equation')
st.subheader('Describing the :violet[freshwater-saltwater interface] under steady groundwater flow', divider="violet")

st.markdown("""
#### 💡 Motivation: Why investigate the Glover Relation?

- Links **regional groundwater flow** toward the coast with the **geometry of the freshwater–saltwater interface**.

- Extends beyond a **local head-depth relation** by including freshwater discharge, gradient, and aquifer thickness.

- Helps build intuition for how gradient, aquifer thickness and density contrast control interface depth at the coast and inland extent of saltwater.

- Serves as a **screening tool** before using full variable-density numerical models, making it valuable for both teaching and practice.
""")


st.markdown(r"""
#### 🎯 Learning Objectives

This section is designed with the intent that, by studying it, you will be able to do the following:

- Explain the conceptual function and mathematical formulation of the **Glover equation**, and how it differs from the **Ghyben–Herzberg relation**.

- Apply the Glover solution to determine the **shape and inland extent** of the freshwater–saltwater interface and the associated freshwater discharge toward the sea under steady, horizontal flow.

- Evaluate how hydraulic gradient, aquifer thickness and density contrast jointly affect the **position of the interface** and the **vulnerability of coastal aquifers** to saltwater intrusion.
""")


st.markdown(r"""
### **Introduction**  

Glover’s equation takes into account the freshwater gradient to approximate the position and shape of the interface between a body of freshwater and underlying seawater in a coastal aquifer. Instead of treating the contact as a simple vertical line beneath the coastline, it shows how freshwater discharges into the sea across a finite zone.
In Glover’s formulation, the coastal aquifer is assumed to be homogeneous and of uniform thickness, with flow that is essentially horizontal (Dupuit approximation) and a sharp interface separating freshwater and saltwater. The solution includes the density difference between freshwater and seawater and uses the regional freshwater gradient to determine both the depth of the interface beneath the shoreline and its curvature inland. This makes Glover’s approach more physically realistic than Ghyben–Herzberg for flowing systems, while still being simple enough for analytical treatment and classroom use.

The shape of the freshwater-saltwater interface can be described by:

$$ 
z^2 = \frac{2 q x \rho_f}{K (\rho_s - \rho_f)} + \left( \frac{q \rho_f}{K (\rho_s - \rho_f)} \right)^2 
$$

where:
- $q$ is the freshwater outflow rate per unit length of coastline [L²/T],
- $K$ is the hydraulic conductivity [L/T],
- $x, z$ are coordinate distances from the shoreline [L],
- $\rho_f$ is the density of freshwater [M/L³],
- $\rho_s$ is the density of saltwater [M/L³].

Using Darcy’s law, this equation can be rewritten as:

The depth of the interface beneath the shoreline is:

$$
z(x) = \sqrt{\frac{2 i b x}{(\rho_s - \rho_f)} + \left( \frac{i b \rho_f}{(\rho_s - \rho_f)} \right)^2} 
$$

where:
- $i$ is the hydraulic gradient [L/L],
- $b$ is the aquifer thickness [L].

The shape of the freshwater table, $h_f(x)$, is defined as:

$$ 
h_f(x) = \sqrt{\frac{2 i b x \rho_f}{(\rho_s - \rho_f)}} 
$$

The width of the zone $L$, where freshwater flows into the sea (when $z = 0$), can be calculated as:

$$ 
L = \frac{i b x \rho_f}{2 (\rho_s - \rho_f)} 
$$

The depth of the freshwater-saltwater interface beneath the shoreline (when $x = 0$) can be determined using the equation:

$$ 
z_0 = \frac{i b \rho_f}{(\rho_s - \rho_f)} 
$$

**Assumptions:**

- Aquifer is homogeneous, isotropic, and of uniform thickness.
- Flow is steady and primarily horizontal (Dupuit–Forchheimer approximation)
- Sharp interface between fresh and salt water (no mixing zone).
- Hydrostatic equilibrium (no flow effects on interface position).

**Limitations:**

- Real aquifers have a transition zone due to dispersion and diffusion.
- Heterogeneity is not captured (e.g. layered systems, lenses)
- Does not account for pumping, tidal effects or strong vertical flows.
""", unsafe_allow_html=True)

st.subheader('Interactive Plot and Exercise', divider="violet")

# User input
# Initialize session state for value and toggle state
st.session_state.i = 0.0001
st.session_state.b = 50
st.session_state.rho_f = 1000
st.session_state.rho_s = 1025

columns1 = st.columns((1,1,1), gap = 'small')
with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $b$, $i$, $rho_f$ and $rho_s$.")
            reset = st.button(':red[Reset the plot to the initial values]')
            if reset:
                st.session_state.i = 0.0001
                st.session_state.b = 50
                st.session_state.rho_f = 1000
                st.session_state.rho_s = 1025

with columns1[1]:
        with st.expander('Modify :orange[**Aquifer properties**]'):
            if st.session_state.number_input:
                b = st.number_input(":green[**Aquifer thickness** $b$ (m)]", 1, 100, st.session_state.b, 1, key="b_input", on_change=update_b)
            else:
                b = st.slider      (":green[**Aquifer thickness** $b$ (m)]", 1, 100, st.session_state.b, 1, key="b_input", on_change=update_b)
            if st.session_state.number_input:
                i = st.number_input(":blue[**Hydraulic gradient** $i$ ]", 0.00001, 0.01, st.session_state.i, 0.0001, key="i_input", on_change=update_i)
            else:
                i = st.slider      (":blue[**Hydraulic gradient** $i$ ]", 0.00001, 0.01, st.session_state.i, 0.0001, key="i_input", on_change=update_i)

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

# Calculation

x_land = np.linspace(0, 1000, 500)
h, z, z_0, L, x_f = glover(i, b, rho_f, rho_s)
x_sea = np.linspace(1000, 1200, 200)
x_max = 1000.0
offset_land = 2.5 * (1 - x_land / x_max)   # 5 m at x=0, 0 m at x = x_max
y_land = h + offset_land
y_sea = sea_surface(x_sea, 1.5)
mask = (x_sea >= x_max) & (x_sea <= x_max + L)

# Plot figure
fig, ax = plt.subplots(figsize=(9, 6))
plt.vlines(1000+L, -b, 0, color = 'yellow', linestyle = "dashed")
plt.hlines(-z_0, 1000+L, 0, color = 'yellow', linestyle = "dashed")
ax.plot(x_land, h, color='steelblue', lw = 1.0, label="Freshwater Head")
ax.plot(x_land,-z, color='darkblue', linewidth=2.5, label="Saltwater Interface")
ax.plot(x_land, y_land, c="black")
ax.plot(x_sea, y_sea, c="black")
ax.plot(x_land, x_land*0, c="royalblue",linestyle=':')
plt.hlines(0, 1000, 1200, color = 'blue')
plt.hlines(-b, 0, 1200, color = 'black', linewidth = 5)

ax.fill_between(x_land, h, y_land, facecolor='wheat', alpha=1.0)   #unsaturated zone
ax.fill_between(x_land, 0, h, facecolor='lightskyblue', alpha=0.5)  #filling fresh water above sea level
ax.fill_between(x_land, 0, -z, facecolor='lightskyblue', alpha=0.5) #filling fresh water below sea level
ax.fill_between(x_land, -z, -b, facecolor='cornflowerblue', hatch = '//') # salty aquifer land
ax.fill_between(x_sea-1, y_sea, -b, facecolor='cornflowerblue', hatch = '//')   # salty aquifer sea
ax.fill_between(x_sea-1, 0, y_sea, facecolor='royalblue')   # sea
ax.fill_between(x_sea[mask], y_sea[mask], -z_0, facecolor='white') # Freshwater flow zone
ax.fill_between(x_sea[mask], y_sea[mask], -z_0, facecolor='lightskyblue', alpha=0.5) # Freshwater flow zone
plt.ylim(-b, )
plt.xlim(0,1200)
ax.legend(loc = 'lower right', fontsize=12)
#plt.text(1180, -20, 'Sea', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(1180, -80, 'Saltwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
#plt.text(150, -10, 'Freshwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
st.pyplot(fig)
st.write(f"**Depth of Interface Below Shoreline ($z₀$):** {z_0:.2f} m")
st.write(f"**Width of Freshwater Flow Zone ($L$):** {L:.2f} m")
st.write(f"**Inland Extent of Saltwater Toe ($x_f$):** {x_f:.2f} m")

with st.expander('Show the :rainbow[**EXERCISE**]', icon ="🧩"):
    st.markdown(r"""
    ### 📘 Exercise – Comparing well designs and pumping strategies

Maybe better tp provide values for i?

🎯 Expected Learning Outcomes:

Completion of this exercise helps you to accomplish the following.

- Understand how the hydrological conditions and pump design influence the risk of upconing
- Develop the knowledge to guide sustainable well-field design in coastal areas. 

### 1. Coastal aquifer

The small coastal community relies almost entirely on a coastal aquifer for its drinking water. The town sits a few hundred metres inland from the shoreline, and the local water authority is worried that **future changes in recharge and sea level** could threaten their freshwater supply.
You have been asked to provide a **screening-level assessment** of the aquifer using the **Glover equation**. Although simplified, the **Glover equation** can give  a first idea of how robust the freshwater lens is under different conditions.

Local hydrogeologists have been estimated the following baseline values:

- Aquifer thickness: $b$ = 40 m)  
- Hydraulic gradient toward the sea: $i$ = 0.001)  
- Freshwater density: $\rho_f$ = 1000 kg/m^3)  
- Seawater density: $\rho_s$ = 1025 kg/m^3)

1. Plot the **freshwater–saltwater interface**. 
2. From the plot, estimate:
   - the **interface depth at the shoreline**,  
   - whether the interface reaches the **aquifer base** within 1000 m inland,  
   - the **overall shape** of the interface (nearly flat, gently curved, or strongly curved).  

### 2. A drier future – reduced recharge

Climate projections suggest that the region may experience **reduced recharge**, lowering the hydraulic gradient toward the sea.

1. Decrease the hydraulic gradient and re-plot the interface. 
2. Compare this “dry future” scenario to the baseline:
   - Is the interface at the shoreline **shallower or deeper**?  
   - Has the **saltwater toe** moved **further inland** or **further seaward**?  

👉 *Based on this, explain whether reduced recharge makes Strandby’s aquifer **more or less vulnerable** to saltwater intrusion.*

### 3. Managed aquifer recharge – remediation possible?

The community is considering a **managed aquifer recharge (MAR)** project: capturing excess stormwater and infiltrating it inland to increase the freshwater gradient toward the sea
1. Increase the hydraulic gradient and re-plot the interface. 
2. Compare all three scenarios:
   - In which case is the **interface deepest at the shoreline**?
   - In which case is the **saltwater toe furthest seaward**?

### 4. Uncertainty – Influence of aquifer thickness?

The local hydrogeologists are still uncertain about the true thickness of the aquifer.
1. Keep the hydraulic gradient and the densities and explore the impact of aquifer thickness
2. Compare two scenarios:
    - How does the depth at the shoreline change 
    - How does the inland extent of the saltwater toe change

👉 Finally, reflect on the **limitations** of using the Glover equation: Which important processes and complexities are **not** represented (e.g. pumping, heterogeneity, mixing zone, transients)?  
""")

st.subheader('✔️ Conclusion', divider = 'violett')
st.markdown("""
The **Glover equation** generalizes the Ghyben–Herzberg relation from a **local head–depth estimate** to a **regional description of the freshwater–saltwater wedge** in a coastal aquifer. It explicitly includes the freshwater gradient and discharge toward the sea, allowing you to visualise how the freshwater table and interface shape vary from inland areas to the shoreline under steady conditions.

By adjusting parameters such as **hydraulic gradient**, **aquifer thickness**, and **density contrast**, the Glover app shows how these factors jointly determine the **inland extent of the saltwater toe** and the **interface depth at the coast**. Comparing the Glover interface to the Ghyben–Herzberg estimate at the shoreline highlights both the usefulness and the limitations of purely local hydrostatic relations. The model serves as an effective **screening tool** before resorting to full variable-density numerical simulations.

This regional perspective provides the **background state** on which other processes act: **pumping** can locally distort the wedge and cause upconing beneath wells, while **sea-level rise or changes in recharge** can shift the entire wedge landward or seaward. After studying this section, you may want to evaluate your knowledge with the Glover initial and final assessment questions.
""")

with st.expander('**Show self-test** - to assess your EXISTING knowledge'):
    st.markdown("""
    #### 📋 Self-test
    You can use the initial questions to assess your existing knowledge.
    Questions need to be transfered to a json-file. The import routine can be find in line 27-29

**How does the Glover equation differ conceptually from the Ghyben–Herzberg relation?**

A. Glover describes the interface profile as a function of distance from the shoreline, whereas Ghyben–Herzberg gives only a local relation between head and interface depth at a point. ✅

B. Glover explicitly includes the freshwater discharge (or gradient) toward the sea, while Ghyben–Herzberg assumes purely hydrostatic equilibrium. ✅

C. Glover assumes a mixing zone of finite thickness, while Ghyben–Herzberg assumes a perfectly sharp interface.

D. Glover can capture pumping-induced transients, while Ghyben–Herzberg is strictly a static equilibrium concept.

**In the Glover formulation for a sharp interface in a coastal aquifer (no pumping), which of the following changes will tend to increase the inland extent or thickness of the freshwater body (all else equal)?**

A. Increasing the hydraulic gradient i (= increased freshwater flowing seaward). ✅

B. Increasing the aquifer thickness b. ✅

C. Decreasing the density difference (making seawater and freshwater more similar in density). ✅

D. Decreasing the freshwater discharge toward the sea.

**Which of the following are standard assumptions is true for the Glover (1959) solution?**

A. The interface between freshwater and saltwater is sharp and separates two regions of constant density. ✅

B. The aquifer is homogeneous, isotropic, of constant thickness, and satisfies the Dupuit (essentially horizontal flow) approximation. ✅

C. Seawater is static, and freshwater flows seaward under a constant hydraulic gradient. ✅

D. Vertical flow components and dispersion in the mixing zone are fully resolved in detail.

**In the steady-state Glover solution for a sharp freshwater–saltwater interface in a coastal aquifer (no pumping), which parameter change will increase the depth of the interface beneath the shoreline, without changing the aquifer thickness?**

A. Increasing the density difference between seawater and freshwater.

B. Decreasing the freshwater hydraulic gradient i toward the sea.

C. Increasing the freshwater hydraulic gradient i toward the sea. ✅

D. Decreasing the freshwater recharge so that the discharge to the sea becomes negligible.

**In the Glover model, what is the key simplification made about groundwater flow in the freshwater zone?

A. Flow is fully three-dimensional, with strong vertical components near the coast.

B. Flow is mainly horizontal, so vertical gradients are neglected (Dupuit approximation). ✅

C. Flow is assumed to be zero everywhere; only diffusion is considered.

D. Flow occurs only in the saltwater zone, while the freshwater is static.""")

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
