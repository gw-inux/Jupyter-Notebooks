# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import streamlit as st
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_SFI_utils import read_md

# ---------- Track the current page
PAGE_ID = "INTRO"

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

def prep_log_slider(default_val: float, log_min: float, log_max: float, step: float = 0.01, digits: int = 2):
    """
    Prepares labels and default for a log-scale select_slider.

    Returns:
    --------
    labels : list of str
        Formatted string labels in scientific notation.
    default_label : str
        Closest label to the given default_val.
    """
    # --- Generate value list and labels
    log_values = np.arange(log_min, log_max + step, step)
    values = 10 ** log_values
    fmt = f"{{0:.{digits}e}}"
    labels = [fmt.format(v) for v in values]

    # --- Find closest label for default
    idx_closest = np.abs(values - default_val).argmin()
    default_label = labels[idx_closest]

    return labels, default_label
 
def update_index():
    selected_label = st.session_state.bc_index_input
    if   selected_label == "**None**":
        index = 0
    elif selected_label == ":orange[**No-flow**]":
        index = 1
    elif selected_label == ":green[**Recharge**]":
        index = 2
    elif selected_label == ":violet[**River**]":
        index = 3
    elif selected_label == ":blue[**Specified head**]":
        index = 3
    else:
        index = 0
    
    st.session_state.bc_index = index

#---------- UI Starting here
st.title(':blue[Analytical Solutions] of Freshwater-Saltwater Interface')
st.subheader('Theory, dynamics and management', divider="blue")


# --- MOTIVATION ---
st.markdown("""
#### 💡 Motivation - Saltwater Intrusion in Coastal Aquifers

Saltwater intrusion is the movement of saline water into freshwater aquifers, typically occurring in coastal areas due to the natural hydraulic connection between groundwater and seawater. Under normal conditions, freshwater flows toward the sea, creating a pressure barrier. Freshwater from the land naturally “floats” above denser saltwater from the sea, creating an interface zone. But when this balance is disrupted, saltwater can encroach into the aquifer. The direction of the saltwater encroachment is highly correlated to the dominating processes caused by both natural and anthropogenic factors. Changes of boundary conditions (link to BC app?) mainly trigger lateral and upward saltwater intrusion. Downward saltwater intrusion, as a consequence of saltwater inflow from the surface due to temporary (e.g. storm floods) or permanent (e.g. estuaries, marsh flats) saltwater flooding, is not covered by this module. Independent of the causes of saltwater intrusion the consequence is a degraded groundwater quality making it unsuitable for drinking, irrigation, and industrial use.

Coastal aquifers are vital freshwater sources for millions of people worldwide (50% of the world population lives within 60 km of the shoreline). These underground reservoirs supply drinking water, support agriculture, and sustain ecosystems. However, their delicate balance is increasingly under threat from a range of environmental and human-induced pressures which have deteriorated the groundwater situation in coastal areas around the globe:

🧂 Overpumping – Excessive groundwater extraction lowers freshwater pressure, allowing denser seawater to migrate inland.

🧂 Sea-level rise – Higher ocean levels push the freshwater–saltwater interface further into the aquifer.

🧂 Climate change – Altered rainfall patterns and prolonged droughts reduce aquifer recharge, intensifying the risk of intrusion.

🧂 Storm surges and extreme weather – Coastal flooding events can rapidly accelerate saltwater migration.

🧂 Man-made infrastructure – Canals and drainage systems may inadvertently act as conduits for saltwater movement.

""")

#left_co, cent_co, last_co = st.columns((20,80,20))
#with cent_co:
#    st.image(st.session_state.module_path + 'images/GenericSaltwaterIntrusion.jpg')
#    st.markdown("""Generic illustration of before and after saltwater intrusion""")

st.markdown("""#### 🚨 Why Study It?

Understanding and predicting saltwater intrusion is critical for sustainable water management in coastal regions. Without proactive monitoring and modeling, communities risk:

🚱 Water supply contamination, requiring costly treatment or alternative sources.

🌾 Agricultural damage, as saline water harms crops and soil health.

🏙️ Infrastructure challenges, including well abandonment and land-use restrictions.

💰 Economic strain, from mitigation efforts and loss of water-dependent industries.
                        
""")

st.markdown(""" 
In coastal aquifers, freshwater from the land naturally “floats” above denser saltwater from the sea, creating an 
interface zone. Under undisturbed conditions, the two systems remain in balance. When that balance is disturbed—by 
pumping, recharge changes, or sea-level rise—the saltwater front can move inland, threatening freshwater supplies.

#### 🎯 Learning Objectives
By the end of this module, you should be able to:

1. **Explain the physical principles governing freshwater–saltwater distribution.**

2. **Apply key analytical models (e.g., Ghyben–Herzberg, Glover–Morgan) to estimate interface depth and movement.**

3. **Evaluate how pumping, recharge changes, and sea-level rise affect the position of the freshwater–saltwater interface.**

4. **Interpret and use model results for informed groundwater management decisions.**
""")

# with st.expander('**Show the initial assessment** - to assess your EXISTING knowledge'):
#     st.markdown("""
#     #### 📋 Initial assessment
#     You can use the initial questions to assess your existing knowledge.
#     """)

#     # Render questions in a 2x2 grid (row-wise, aligned)
#     for row in [(0, 1), (2, 3)]:
#         col1, col2 = st.columns(2)
    
#         with col1:
#             i = row[0]
#             st.markdown(f"**Q{i+1}. {quest_ini[i]['question']}**")
#             multiple_choice(
#                 question=" ",  # suppress repeated question display
#                 options_dict=quest_ini[i]["options"],
#                 success=quest_ini[i].get("success", "✅ Correct."),
#                 error=quest_ini[i].get("error", "❌ Not quite.")
#             )
    
#         with col2:
#             i = row[1]
#             st.markdown(f"**Q{i+1}. {quest_ini[i]['question']}**")
#             multiple_choice(
#                 question=" ",
#                 options_dict=quest_ini[i]["options"],
#                 success=quest_ini[i].get("success", "✅ Correct."),
#                 error=quest_ini[i].get("error", "❌ Not quite.")
#       )

# --- TYPES OF BOUNDARY CONDITIONS ---
st.subheader('🧪 Theory: ', divider='blue')
st.markdown("""

"""
)
with st.expander("Show more :blue[**explanation about saltwater intrusion**]"):
    st.markdown(r"""### Transport processes:

The main transport mechanism for dissolved substances in groundwater is **advection** – movement with the bulk flow of water driven by hydraulic gradients (gravity and pressure differences). If the water is at static but density differences exist (for example between fresh and saline water), the lighter water will tend to overlie the denser water and a **stable horizontal stratification** forms. When groundwater flows, these density differences can produce **sloping density interfaces** between fresh and saline water, as in coastal aquifers.

In addition to advection, **molecular diffusion** contributes to solute transport. Diffusion is the microscopic movement of ions and molecules driven purely by **concentration gradients**, independent of bulk flow. Its effect grows roughly with the square root of time, which means that in many groundwater systems diffusion is relatively slow. At a sharp initial boundary between fresh and saline water, diffusion will gradually smear out the concentration contrast and create a **transition zone of brackish water**.

Groundwater flow also produces **mechanical dispersion**, a mixing process that arises because groundwater velocities vary in magnitude and direction within the pore space. Some flow paths are faster, some slower, so a plume of solute spreads out even if molecular diffusion were negligible. On larger scales, **heterogeneities in aquifer properties** (layering, lenses, fractures) cause additional spreading, often called **macrodispersion**. The amount of spreading due to dispersion is roughly proportional to the **groundwater velocity**, so faster flow leads to stronger mechanical mixing.

Both **diffusion and dispersion** act to **smooth concentration gradients** and broaden originally sharp interfaces between fluids of different salinity. In practice they are difficult to separate, so their combined effect is represented with a **hydrodynamic dispersion coefficient**, which includes both molecular diffusion and mechanical dispersion. In many coastal aquifers, advection and dispersion dominate at the field scale, while diffusion controls mixing at very small scales or over long time periods in low-permeability zones.

### Density:

In groundwater systems, the **density** of water is not a fixed value. In general it depends on **pressure**, **temperature** and the **concentration of dissolved substances**:

$$
\rho = f(p, T, S)
$$

where  

- $\rho$ is water density [M/L3]  
- $p$ is pressure [M/L/T2]  
- $T$ is water temperature [K]  
- $S$ is salinity or total dissolved solids (TDS) (M/L3)

For most hydrogeologic settings, the effect of **pressure** on density is very small and can usually be neglected. The influence of **temperature** is often modest compared to the influence of **dissolved solids**, especially in shallow aquifers where temperature variations are relatively limited. As a result, in many groundwater applications density is treated primarily as a function of **dissolved solids concentration**, while temperature is assumed constant.

left_co, cent_co, last_co = st.columns((20,80,20))
with cent_co:
    st.image(st.session_state.module_path + 'images/Density.png')
    st.markdown("""""")

When groundwater “quality” is of interest, we often describe the water in terms of **salinity** or **total dissolved solids (TDS)**. TDS is particularly useful in practice because it can be estimated quickly from measurements of **electrical conductivity** of a water sample.

Dissolved solids consist of a mixture of **cations** (positively charged ions) and **anions** (negatively charged ions). Typical major ions include, for example, Na⁺, K⁺, Ca²⁺, Mg²⁺, Cl⁻, SO₄²⁻ and HCO₃⁻. Ocean water contains a characteristic mixture of these ions, with **chloride (Cl⁻)** being the dominant anion.

In coastal hydrogeology, chloride is often used as a **tracer for salinity**. Because chloride is abundant, conservative (it reacts little with the aquifer matrix) and relatively easy to measure, changes in **chloride concentration** are commonly taken to represent changes in the **overall dissolved solids**. In other words, when models or measurements focus on chloride distribution, it is usually assumed that the **proportional composition of the other ions** remains similar to that of seawater, and that chloride can be used as a proxy for the total salinity distribution in the groundwater system.    """)
    
# --- EXPLANATORY EXAMPLES ---
st.subheader('💫 Examples ...', divider='blue')
st.markdown("""
  
"""
)

            

st.subheader('📈 Computation and Visualization', divider='blue')
st.markdown("""

""")

st.subheader('✔️ Conclusion', divider = 'blue')
st.markdown("""

""")


# with st.expander('**Show the final assessment** - to self-check your understanding'):
#     st.markdown("""
#     #### 🧠 Final assessment
#     These questions test your conceptual understanding after working with the application.
#     """)

#     # Render questions in a 2x3 grid (row-wise)
#     for row in [(0, 1), (2, 3), (4, 5)]:
#         col1, col2 = st.columns(2)

#         with col1:
#             i = row[0]
#             st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
#             multiple_choice(
#                 question=" ",
#                 options_dict=quest_final[i]["options"],
#                 success=quest_final[i].get("success", "✅ Correct."),
#                 error=quest_final[i].get("error", "❌ Not quite.")
#             )

#         with col2:
#             i = row[1]
#             st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
#             multiple_choice(
#                 question=" ",
#                 options_dict=quest_final[i]["options"],
#                 success=quest_final[i].get("success", "✅ Correct."),
#                 error=quest_final[i].get("error", "❌ Not quite.")
#             )

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image(st.session_state.module_path + 'images/CC_BY-SA_icon.png')
