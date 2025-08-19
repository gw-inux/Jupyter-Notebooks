# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import streamlit as st
import json
from streamlit_book import multiple_choice

# Authors, institutions, and year
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

# path to questions for the assessments (direct path)
module_path = ""
# path_quest_ini = module_path + "questions/initial_general_behavior.json"
# path_quest_exer_sc1 = module_path + "questions/exer_general_sc1.json"
# path_quest_exer_sc2 = module_path + "questions/exer_general_sc2.json"
# path_quest_final = module_path + "questions/final_general_behavior.json"

# # Load questions
# with open(path_quest_ini, "r", encoding="utf-8") as f:
#     quest_ini = json.load(f)

# with open(path_quest_exer_sc1, "r", encoding="utf-8") as f:
#     quest_exer_sc1 = json.load(f)
    
# with open(path_quest_exer_sc2, "r", encoding="utf-8") as f:
#     quest_exer_sc2 = json.load(f)
    
# with open(path_quest_final, "r", encoding="utf-8") as f:
#     quest_final = json.load(f)

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

st.title('Freshwater-Saltwater Interface :blue[Groundwater Models]')
st.subheader('Theory, dynamics and management', divider="blue")


# --- MOTIVATION ---
st.markdown("""
#### 💡 Motivation - Why it matters
Saltwater Intrusion in Coastal Aquifers
Coastal aquifers are vital freshwater sources for millions of people worldwide. These underground reservoirs supply drinking water, support agriculture, and sustain ecosystems. However, their delicate balance is increasingly under threat from a range of environmental and human-induced pressures:

* Overpumping – Excessive groundwater extraction lowers freshwater pressure, allowing denser seawater to migrate inland.

* Sea-level rise – Higher ocean levels push the freshwater–saltwater interface further into the aquifer.

* Climate change – Altered rainfall patterns and prolonged droughts reduce aquifer recharge, intensifying the risk of intrusion.

* Storm surges and extreme weather – Coastal flooding events can rapidly accelerate saltwater migration.

* Man-made infrastructure – Canals and drainage systems may inadvertently act as conduits for saltwater movement.

These factors can cause the saltwater–freshwater interface to migrate landward, contaminating wells and reducing water supply reliability—a process known as saltwater intrusion.

Saltwater intrusion is the movement of saline water into freshwater aquifers, typically occurring in coastal areas due to the natural hydraulic connection between groundwater and seawater. Under normal conditions, freshwater flows toward the sea, creating a pressure barrier that keeps saltwater at bay. But when this balance is disrupted, saltwater can encroach laterally or vertically into the aquifer, degrading groundwater quality and making it unsuitable for drinking, irrigation, and industrial use.

#### 🚨 Why Study It?

Understanding and predicting saltwater intrusion is critical for sustainable water management in coastal regions. Without proactive monitoring and modeling, communities risk:

🚱 Water supply contamination, requiring costly treatment or alternative sources.

🌾 Agricultural damage, as saline water harms crops and soil health.

🏙️ Infrastructure challenges, including well abandonment and land-use restrictions.

💰 Economic strain, from mitigation efforts and loss of water-dependent industries.
                        
Therefore, understanding and predicting saltwater intrusion is critical for sustainable water management in coastal regions.
""")

left_co, cent_co, last_co = st.columns((20,80,20))
with cent_co:
    st.image(module_path + 'images/GenericSaltwaterIntrusion.jpg')
    st.markdown("""Generic illustration of before and after saltwater intrusion""")

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
    st.markdown("""
    
    """)
    
# --- EXPLANATORY EXAMPLES ---
st.subheader('💫 Examples ...', divider='blue')
st.markdown("""
  
"""
)

            

st.subheader('📈 Computation and Visualization', divider='blue')
st.markdown("""

""")

st.subheader('✅ Conclusion', divider = 'blue')
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

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image(module_path + 'images/CC_BY-SA_icon.png')