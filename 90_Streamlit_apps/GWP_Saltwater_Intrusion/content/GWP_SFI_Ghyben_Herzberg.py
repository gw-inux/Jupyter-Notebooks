import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_Saltwater_Intrusion_utils import read_md
from GWP_Saltwater_Intrusion_utils import flip_assessment
from GWP_Saltwater_Intrusion_utils import render_toggle_container
from GWP_Saltwater_Intrusion_utils import prep_log_slider
from GWP_Saltwater_Intrusion_utils import get_label
from GWP_Saltwater_Intrusion_utils import get_step

# ---------- Track the current page
PAGE_ID = "GHY"
module_path = "90_Streamlit_apps/GWP_Saltwater_Intrusion/"

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


# ---------- path to questions for the assessments (direct path)
path_quest_ini   = module_path + "questions/ghyben_initial.json"
path_quest_exer =  module_path + "questions/ghyben_exer.json"
path_quest_final = module_path + "questions/ghyben_final.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)


# --- Authors, institutions, and year
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

# Streamlit app title and description

st.title('The Ghyben-Herzberg Relation')

st.subheader('Describing the :orange[freshwater-saltwater interface] under static hydraulic conditions', divider="orange")

st.markdown(r"""
### **Introduction**  
The first general scientific descriptions of saltwater intrusion were published at the end of the nineteenth century. Based on field observations, Drabbe and Badon-Ghyben (1888) and Herzberg (1901) derived the first quantitative relationship of the saltwater–freshwater interface location as a linear function of the water-table elevation in steady-state conditions. The resulting conceptual theorem, the Ghyben-Herzberg theorem, is named after two of the leading authors. The conceptual model of a sharp interface is still frequently applied, although it does not account for mixing along the interface and therefore the validity of a sharp interface applied on real case scenarios is limited.
The Ghyben-Herzberg relation describes the equilibrium relationship between fresh groundwater and underlying seawater in coastal aquifers. Due to the density difference between freshwater and seawater, a lens of fresh groundwater floats above the denser saltwater, see the following figure.
""", unsafe_allow_html=True)

#lc0, cc0, rc0 = st.columns((20,60,20))
#with cc0:
#"    st.image(module_path + 'images/Saltwater_intrusion_en.png', caption="Conceptual sketch of the fresh-water saltwater interface under hydrostatic conditions (Barlow 2003)[https://pubs.usgs.gov/circ/2003/circ1262/].")

st.markdown(r"""
This relation can be expressed as:  

$$
z = \frac{\rho_f}{\rho_s - \rho_f} h
$$

where:  
- $z$ is the depth of the freshwater-saltwater interface below sea level [L],  
- $h$ is the height of the freshwater table above sea level [L],  
- $\rho_{f}$ is the density of freshwater [M/L³] ($\approx$ 1000 kg/m³),  
- $\rho_{s}$ is the density of seawater [M/L³] ($\approx$ 1025 kg/m³).  

For typical values, this relation simplifies to:  

$$
z \approx 40h
$$

This means that for every meter of freshwater head above sea level, the freshwater-saltwater interface extends approximately **40 meters** below sea level.

**Assumptions:**

- Static (no pumping, no recharge change) conditions.
- Homogeneous, isotropic aquifer.
- Sharp interface between fresh and salt water (no mixing zone).
- Hydrostatic equilibrium (no flow effects on interface position).

**Limitations:**

- Real aquifers have a transition zone due to dispersion and diffusion.
- Does not account for pumping cones of depression or tidal effects.

""", unsafe_allow_html=True)

def land_surface(x, p):
    """Quadratische Funktion, die von y=10 (bei x=0) auf y=0 (bei x=1000) fällt. The exponent defines the shape"""
    return 10 * (1 - (x / 1000)**p)

def sea_surface(x, p):
    """Erzeugt eine gekrümmte ansteigende Funktion von (1000,0) bis (1200,30) mit starkem Anfangsgradient."""
    return 50 * (1 - ((1200 - x) / 200) ** p)*-1

def ghyben_herzberg(h, rho_f, rho_s, x):
    h = (h**2 - (h**2 - 0**2) / 1000 * x) ** 0.5
    z = (rho_f / (rho_s - rho_f)) * h
    return h, z
    
ymin = -200 # lower value for plotting
st.subheader('Interactive Plot and Exercise', divider="orange")

def update_h():
    st.session_state.h = st.session_state.h_input
def update_rho_s():
    st.session_state.rho_s = st.session_state.rho_s_input
def update_rho_f():
    st.session_state.rho_f = st.session_state.rho_f_input

# User defined input
st.session_state.h = 1.0
st.session_state.rho_f = 1000
st.session_state.rho_s = 1025

columns1 = st.columns((1,1,1), gap = 'small')
with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $h$, $rho_f$ and $rho_s$.")
            reset = st.button(':red[Reset the plot to the initial values]')
            if reset:
                st.session_state.h = 1.0
                st.session_state.rho_f = 1000
                st.session_state.rho_s = 1025

with columns1[1]:
        with st.expander('Modify :orange[**Freshwater head**]'):
            if st.session_state.number_input:
                h = st.number_input(":green[**Freshwater head** $h$ (m)]", 1.0, 10.0, st.session_state.h, 0.1, key="h_input", on_change=update_h)
            else:
                h = st.slider      (":green[**Freshwater head** $h$ (m)]", 1.0, 10.0, st.session_state.h, 0.1, key="h_input", on_change=update_h)
                
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

# Calculation

x_land = np.linspace(0, 1000, 500)   
x_sea = np.linspace(1000, 1200, 200)
y_land = land_surface(x_land, 4)
y_sea = sea_surface(x_sea, 1.5)
h_x, z = ghyben_herzberg(h, rho_f, rho_s, x_land)

# Plot figure
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(x_land, h_x, color='steelblue', lw = 1.0, label="Freshwater Head")
ax.plot(x_land, y_land, c="black")
ax.plot(x_sea, y_sea, c="black")
ax.plot(x_land, x_land*0, c="royalblue",linestyle=':')
ax.plot(x_land, -z, color='darkblue', linewidth=2.5, label="Saltwater Interface")
ax.hlines(0, 1000, 1200, color='blue')

ax.fill_between(x_land, h_x, y_land, facecolor='wheat', alpha=1.0)   #unsaturated zone

ax.fill_between(x_land, 0, h_x, facecolor='lightskyblue', alpha=0.5)  #filling fresh water below sea
ax.fill_between(x_land, 0, -z, facecolor='lightskyblue', alpha=0.5) #filling fresh water below sea

ax.fill_between(x_land, -z, ymin, facecolor='cornflowerblue', hatch = '//') # salty aquifer land
ax.fill_between(x_sea-1, y_sea, ymin, facecolor='cornflowerblue', hatch = '//')   # salty aquifer sea
ax.fill_between(x_sea-1, 0, y_sea, facecolor='royalblue')   # sea
ax.set_xlabel("x [m]",fontsize=14)
plt.ylim(ymin,20)
plt.xlim(0,1200)
ax.set_ylabel("hydraulic head [m]",fontsize=14)
ax.set_title("Freshwater-Saltwater Interface",fontsize=16)
ax.legend(loc = 'lower right', fontsize=12)
plt.text(1180, -20, 'Sea', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(1180, -80, 'Saltwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
plt.text(150, -10, 'Freshwater', horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'), fontsize=10)
    
st.pyplot(fig)

with st.expander('Show the :rainbow[**EXERCISE**]', icon ="🧩"):
    st.markdown(r"""
    ### 📘 Exercise – Comparing well designs and pumping strategies

🎯 Expected Learning Outcomes:


""")

st.subheader('✔️ Conclusion', divider = 'green')
st.markdown("""
...
After studying this section about the Ghyben-Herzberg principle, you may want to evaluate your knowledge using the final assessment.
""")

# --- FINAL ASSESSMENT ---
def content_final_ghy():
    st.markdown("""#### 🧠 Final assessment""")
    st.info("These questions test your conceptual understanding after working with the application.")
    
    # Render questions in a 2x3 grid (row-wise)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)

        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )

        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )
            
# Render final assessment
render_toggle_container(
    section_id="ghy_03",
    label="✅ **Show the final assessment** - to self-check your **understanding**",
    content_fn=content_final_ghy,
    default_open=False,
)
            
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')