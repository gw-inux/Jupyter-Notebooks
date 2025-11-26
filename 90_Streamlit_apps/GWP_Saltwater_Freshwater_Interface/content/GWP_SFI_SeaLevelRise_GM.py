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
PAGE_ID = "GM"

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
path_quest_exer  = st.session_state.module_path + "questions/exer_sfi_gm.json"

# Load questions
    
with open(path_quest_exer, "r", encoding="utf-8") as f:
    quest_exer = json.load(f)

#---------- UI Starting here
st.title("Glover–Morgan Equation – Modeling Saltwater Intrusion Dynamics")

#st.subheader('Sea Level Rise Impact on Aquifer Interface', divider= "green")


# ---------- THEORY ----------
#with st.expander("📘 Theory (click to expand)", expanded=True):
st.markdown(r"""

### **Theory**
The Glover–Morgan equation is a mathematical model used to describe the transient movement of the 
saltwater–freshwater interface in coastal aquifers following a sudden change in boundary conditions, 
such as a rise in sea level or a change in hydraulic head due to pumping.

📘 Background

Unlike the Ghyben-Herzberg Principle, which assumes a static equilibrium, the Glover–Morgan model 
accounts for time-dependent changes in the position of the saltwater interface. It is based on the 
Dupuit–Ghyben–Herzberg assumptions and treats the interface as a sharp boundary between freshwater 
and saltwater, which is a simplification but useful for analytical modeling.
            
🧮 The Equation

The Glover–Morgan equation estimates the landward movement of the saltwater interface over time:

$$
x(t) = x_0 + \sqrt{\frac{2K h}{n} t}
$$

Where:
- \( x(t) \): Position of the saltwater interface at time \( t \)
- \( x_0 \): Initial position of the interface
- \( K \): Hydraulic conductivity of the aquifer
- \( h \): Change in hydraulic head at the boundary
- \( n \): Effective porosity of the aquifer
- \( t \): Time since the change occurred

**Assumptions:**
- Sharp interface (no transition zone)
- Homogeneous, isotropic aquifer
- One-dimensional flow toward the sea
- Change in boundary head is the primary driver (e.g., sea-level rise)
                        

""")

st.divider()

# ---------- INTERACTIVE PLOT ----------
st.subheader("Interactive Plot – Sea-Level Rise Simulation")

colA, colB = st.columns(2)
with colA:
    slr_rate = st.slider("Sea-Level Rise Rate (m/year)", min_value=0.0, max_value=0.05, value=0.01, step=0.001)
    years = st.slider("Simulation Period (years)", min_value=0, max_value=100, value=50, step=1)
    L = st.number_input("Aquifer Length Scale L (m)", min_value=100, max_value=5000, value=1000, step=10)
with colB:
    T = st.number_input("Transmissivity T (m²/day)", min_value=100, max_value=10000, value=2000, step=100)
    S = st.number_input("Storage Coefficient S (-)", min_value=0.0001, max_value=0.1, value=0.01, step=0.0001, format="%.4f")
    rho_f = st.number_input("Freshwater density ρ_f (kg/m³)", min_value=990.0, max_value=1010.0, value=1000.0, step=0.1)
    rho_s = st.number_input("Seawater density ρ_s (kg/m³)", min_value=1010.0, max_value=1035.0, value=1025.0, step=0.1)

# Time axis (years)
t_years = np.linspace(0, max(years, 1), 200)

# Simple link from SLR to boundary head change (total rise over the full horizon):
delta_h_total = slr_rate * years  # meters

# You may choose a different mapping from head change to final displacement X_f.
# Here we use a didactic scaling: X_f ∝ (T/S) * (Δh / L).
X_f = (T / S) * (delta_h_total / max(L, 1))  # meters (pedagogical placeholder)

# Convert years to days for the exponential (T is per day).
tau_inv = (T / (S * (L**2))) * 365.0  # 1/year
X_t = X_f * (1.0 - np.exp(-tau_inv * t_years))

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(t_years, X_t, linewidth=2, label="Interface movement (inland)")
ax.set_xlabel("Time (years)")
ax.set_ylabel("Interface displacement inland (m)")
ax.set_title("Glover–Morgan Interface Response to Sea-Level Rise")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.markdown(f"**Final displacement after {years} years:** `{X_t[-1]:.2f} m`")
st.caption("Note: The mapping from sea-level rise to X_f is simplified for teaching. "
           "For research/operational use, calibrate against a physically based model and site data.")

st.divider()

# ---------- EXERCISE ----------
st.subheader("Exercise")
st.markdown(r"""
**Task:**  
If sea level rises by **0.3 m** over 30 years, with \(T = 3000\ \text{m}^2/\text{day}\), \(S = 0.02\), \(L = 1500\ \text{m}\), estimate the inland interface movement after **15 years** using the Glover–Morgan form.
Assume a sharp interface and no pumping.
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    ex_slr = st.number_input("SLR total (m)", min_value=0.0, value=0.3, step=0.01)
with col2:
    ex_years_total = st.number_input("Horizon (years)", min_value=1, value=30, step=1)
with col3:
    ex_years_eval = st.number_input("Evaluate at t (years)", min_value=0, value=15, step=1)
with col4:
    ex_T = st.number_input("T_ex (m²/day)", min_value=100, max_value=10000, value=3000, step=100)

ex_S = st.number_input("S_ex (-)", min_value=0.0001, max_value=0.1, value=0.02, step=0.0001, format="%.4f")
ex_L = st.number_input("L_ex (m)", min_value=100, max_value=10000, value=1500, step=10)

# Pedagogical mapping for the exercise
ex_delta_h = ex_slr  # total head change over the horizon
ex_Xf = (ex_T / ex_S) * (ex_delta_h / max(ex_L, 1))
ex_tau_inv = (ex_T / (ex_S * (ex_L**2))) * 365.0
ex_X = ex_Xf * (1.0 - np.exp(-ex_tau_inv * ex_years_eval))

st.markdown(f"**Estimated inland movement at t = {ex_years_eval} years:** `{ex_X:.2f} m`")

st.divider()

'---'

with st.expander('**Show self-test** - to assess your EXISTING knowledge'):
    st.markdown("""
    #### 📋 Self-test
    You can use the initial questions to assess your existing knowledge.
    """)

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
