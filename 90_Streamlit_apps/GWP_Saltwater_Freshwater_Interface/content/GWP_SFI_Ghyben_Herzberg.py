import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_SFI_utils import read_md
from GWP_SFI_utils import flip_assessment
from GWP_SFI_utils import render_toggle_container
from GWP_SFI_utils import prep_log_slider
from GWP_SFI_utils import get_label
from GWP_SFI_utils import get_step

# ---------- Track the current page
PAGE_ID = "GHY"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID

# ---------- Doc-only view for expanders (must run first)
params = st.query_params
DOC_VIEW = params.get("view") == "md" and params.get("doc")

if DOC_VIEW:
    md_file = params.get("doc")

    st.markdown("""
    <style>
      /* Hide sidebar & its nav */
      [data-testid="stSidebar"],
      [data-testid="stSidebarNav"] { display: none !important; }

      /* Hide the small chevron / collapse control */
      [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(read_md(md_file))
    st.stop()
    
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
path_quest_ini   = st.session_state.module_path + "questions/ghyben_initial.json"
path_quest_exer =  st.session_state.module_path + "docs/ghyben_exer.json"
path_quest_final = st.session_state.module_path + "questions/ghyben_final.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
#---------- FUNCTIONS
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

def update_h():
    st.session_state.h = st.session_state.h_input
    
def update_rho_s():
    st.session_state.rho_s = st.session_state.rho_s_input
    
def update_rho_f():
    st.session_state.rho_f = st.session_state.rho_f_input  
    
#---------- UI Starting here
st.title('The Ghyben-Herzberg Relation')
st.subheader('Describing the :orange[freshwater-saltwater interface] under static hydraulic conditions', divider="orange")

st.markdown("""
    #### 💡 Motivation: Why investigate the Ghyben-Herzberg Relation?
    
    - It provides a **simple link** between freshwater head and the depth of the freshwater–saltwater interface, allowing quick, first-order estimates of **freshwater lens thickness** without running a full numerical model.
    
    - It helps building **physical intuition**: See how a small change in groundwater level (e.g. due to pumping, reduced recharge, or sea-level rise) can translate into a large shift of the interface at depth.
    
    - It is still widely used as a **screening and communication tool** in coastal groundwater studies, making it a natural starting point before introducing more complex density-dependent models.
    
    - Understanding its **assumptions and limitations** (hydrostatic equilibrium, homogeneity, sharp interface) trains the user to critically judge when a “classic” textbook relation is useful—and when it can be misleading in real-world applications.
    
    """)

st.markdown(r"""
    ####  🎯 Learning Objectives
    This section is designed with the intent that, by studying it, you will be able to do the following:
    
    - Explain the conceptual function of the **Ghyben–Herzberg relation** and its mathematical formulation including the origin and meaning of the “40:1” rule of thumb.
    - Apply the Ghyben–Herzberg relation to calculate **interface depth and freshwater lens thickness** for simple coastal and island aquifer settings, and 
    - Evaluate how changes in density contrast $\rho_s$ - $\rho_f$) and freshwater head $\h$) affect the interface position.

    
    """)    
    
# --- INITIAL ASSESSMENT ---
def content_initial_GHY():
    st.markdown("""#### Initial assessment""")
    st.info("You can use the initial questions to assess your existing knowledge.")
    
    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_ini[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_ini[i]["options"],
                success=quest_ini[i].get("success", "✅ Correct."),
                error=quest_ini[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_ini[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_ini[i]["options"],
                success=quest_ini[i].get("success", "✅ Correct."),
                error=quest_ini[i].get("error", "❌ Not quite.")
            )

# Render initial assessment
render_toggle_container(
    section_id="GHY_01",
    label="✅ **Show the initial assessment** – to assess your **EXISTING** knowledge",
    content_fn=content_initial_GHY,
    default_open=False,
)

st.subheader('🧪 Theory and Background', divider="orange")
st.markdown("""
#### Introduction
The first general scientific descriptions of saltwater intrusion were published at the end of the nineteenth century. Based on field observations, Drabbe and Badon-Ghyben (1888) and Herzberg (1901) derived the first quantitative relationship of the saltwater–freshwater interface location as a linear function of the water-table elevation in steady-state conditions. The resulting conceptual theorem, the Ghyben-Herzberg theorem, is named after two of the leading authors. The conceptual model of a sharp interface is still frequently applied, although it does not account for mixing along the interface and therefore the validity of a sharp interface applied on real case scenarios is limited.
The Ghyben-Herzberg relation describes the equilibrium relationship between fresh groundwater and underlying seawater in coastal aquifers. Due to the density difference between freshwater and seawater, a lens of fresh groundwater floats above the denser saltwater, see the following figure.
""", unsafe_allow_html=True)

lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image(st.session_state.module_path + 'images/Saltwater_intrusion_en.png', caption="Conceptual sketch of the fresh-water saltwater interface under hydrostatic conditions (Barlow 2003)[https://pubs.usgs.gov/circ/2003/circ1262/].")

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

#-------INTERACTIVE PLOT

st.subheader('Interactive Plot and Exercise', divider="orange")

ymin = -200 # lower value for plotting

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

# Expander with "open in new tab"
DOC_FILE1 = "GHY_instructions.md"
with st.expander('Show the :blue[**INSTRUCTIONS**]', icon ="🧪"):
    st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE1}")
    st.markdown(read_md(DOC_FILE1))
    
# Expander with "open in new tab"
DOC_FILE2 = "GHY_exercise.md"
with st.expander('Show the :rainbow[**EXERCISE**]', icon ="🧩"):
    st.link_button("*Open in new tab* ↗️ ", url=f"?view=md&doc={DOC_FILE2}")
    st.markdown(read_md(DOC_FILE2))
        
with st.expander('Show the :rainbow[**EXERCISE**]', icon ="🧩"):
    st.markdown(r"""
    ### 📘 Exercise – Comparing well designs and pumping strategies

🎯 Expected Learning Outcomes:

""")

# --- EXERCISE ASSESSMENT ---

def content_exer_GHY():
    st.markdown("""#### 🧠 Exercise assessment""")
    st.info("These questions test your understanding after doing the DRN exercise.")
    
    # Render questions in a 2x3 grid (row-wise)
    for row in [(0, 1), (2, 3), (4, 5)]:
        col1, col2 = st.columns(2)

        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_exer[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_exer[i]["options"],
                success=quest_exer[i].get("success", "✅ Correct."),
                error=quest_exer[i].get("error", "❌ Not quite.")
            )

        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_exer[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_exer[i]["options"],
                success=quest_exer[i].get("success", "✅ Correct."),
                error=quest_exer[i].get("error", "❌ Not quite.")
            )
            
# Render exercise assessment
render_toggle_container(
    section_id="GHY_02",
    label="✅ **Show the :rainbow[**EXERCISE**] assessment** - to self-check your understanding",
    content_fn=content_exer_GHY,
    default_open=False,
)

st.subheader('✔️ Conclusion', divider = 'orange')
st.markdown("""
The **Ghyben–Herzberg relation** is a simple but powerful tool for estimating the position of the freshwater–saltwater interface from the freshwater head above sea level. By linking head and interface depth through the density contrast between fresh and saline water, it provides a fast, first-order way to estimate **freshwater lens thickness** in coastal and island aquifers without running a full variable-density model.

Unlike more complex approaches, the Ghyben–Herzberg concept assumes **hydrostatic equilibrium**, a **homogeneous aquifer**, and a **sharp interface**. Within these limits, adjusting parameters such as **freshwater head** and **density contrast** helps you see how small changes in water level can translate into large shifts in interface depth (for example, the familiar “40:1” rule of thumb). This builds strong physical intuition for why even modest drawdown, reduced recharge, or sea-level change can have large implications for freshwater availability.

The insights from this app form the conceptual foundation for the more advanced tools in this module. **Glover** extends the idea to a *regional wedge*, **upconing** illustrates *local vertical disturbances by pumping*, and the **sea-level rise** app explores *time-dependent boundary changes*. After working through the Ghyben–Herzberg app, you may wish to test your understanding using the corresponding initial and final assessments.
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

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image(st.session_state.module_path + 'images/CC_BY-SA_icon.png')
