# Initialize librarys
import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from streamlit_book import multiple_choice

# ---------- Authors, institutions, and year
year = 2025 
authors = {
    "Markus Giese": [1],  # Author 1 belongs to Institution 1
    "Thomas Reimann": [2],
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
module_path = '02_Basic_hydrology/'
# --- path to questions for the assessments (direct path)
path_quest_ini   = module_path + "questions/infiltration_initial.json"
path_quest_final = module_path + "questions/infiltration_final.json"

#Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)

# --- Functions

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

def get_label(val: float, labels: list[str]) -> str:
    """Given a float value and a list of scientific notation labels, return the closest label."""
    label_vals = [float(l) for l in labels]
    idx = np.abs(np.array(label_vals) - val).argmin()
    return labels[idx]

def get_step(val: float) -> float:
    """Return a step that modifies the first digit after the decimal point in scientific notation."""
    if val == 0:
        return 1e-8  # fallback
    exponent = int(np.floor(np.log10(abs(val))))
    return float(10 ** (exponent - 1))
    
def flip_assessment(section_id: str):
    """Flip the boolean flag for a given section_id."""
    key = f"exp_{section_id}"
    st.session_state[key] = not st.session_state.get(key, False)
    
def render_toggle_container(
    section_id: str,
    label: str,
    content_fn,                 # a function that renders the section contents when open
    *,
    default_open: bool = False,
    col_ratio=(25, 1),
    container_border: bool = True,
):
    """
    Renders a toggleable container with two buttons:
    - Left: text button with your label
    - Right: chevron button (▲/▼)
    Each section manages its own state via section_id.

    Parameters
    ----------
    section_id : unique id string, e.g., "general_01"
    label      : button label shown on the left
    content_fn : callable with no args that renders the open content
    default_open : initial open state (only used on first render)
    col_ratio  : column width ratio for (label_button, chevron_button)
    container_border : show a border around the section container
    """
    state_key = f"exp_{section_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_open

    with st.container(border=container_border):
        ass_c1, ass_c2 = st.columns(col_ratio)

        # Left button – same on_click toggler for consistency
        with ass_c1:
            st.button(label,key=f"btn_label_{section_id}",type="tertiary",on_click=flip_assessment,args=(section_id,))

        # Right chevron button – also toggles the same state
        with ass_c2:
            chevron = "▲" if st.session_state[state_key] else "▼"
            st.button(chevron,key=f"btn_chev_{section_id}",type="tertiary",on_click=flip_assessment,args=(section_id,))

        # Conditional content
        if st.session_state[state_key]:
            content_fn()
            

        
st.title('Infiltration capacity (according to Horton)')
st.subheader('Describing :blue[overland flow] during intense rainfall', divider="blue")


st.markdown("""
#### 💡 Motivation:

Understanding **infiltration** is essential for predicting how much rainfall becomes **runoff**, **recharge**, or **soil storage**. The Horton model offers a simple way to see how infiltration capacity changes during a storm and when **infiltration-excess overland flow** is likely to occur.

#### 🎯 Learning Objectives

By studying this section, you will be able to:

- Explain the basic idea of the **Horton infiltration model** (high initial capacity, decreasing over time).  
- Identify the roles of $f_0$, $f_c$, and $k$ in shaping the infiltration curve.  
- Relate **rainfall intensity** and **infiltration capacity** to the onset of **Hortonian overland flow**.
""")

 #--- INITIAL ASSESSMENT ---
def content_initial_HOR():
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
    section_id="HOR_01",
    label="✅ **Show the initial assessment** – to assess your **EXISTING** knowledge",
    content_fn=content_initial_HOR,
    default_open=False,
)

st.subheader('🧪 Introduction', divider="blue")
st.markdown(r"""
### 🌧 Horton Infiltration

When rain falls on the ground, part of the water **infiltrates into the soil**, while the rest may **pond on the surface** and eventually run off. The **infiltration capacity** of a soil is the maximum rate at which water can enter the ground at a given moment. In reality, this capacity is usually **high at the beginning of a storm** (dry soil, lots of storage space) and then **decreases over time** as the soil becomes wetter.

The **Horton infiltration model** is a simple, empirical way to describe this behaviour. It assumes that the infiltration capacity starts at an initial value \( f_0 \) and then **decays exponentially** toward a lower, constant value \( f_c \) as time passes during a storm. A single decay parameter \( k \) controls how quickly this change happens.

$$
f_p = f_c + (f_o - f_c) e^{-kt}
$$

with

$f_p$ = infiltration capacity (cm/hr)

$f_c$ = equilibrium infiltration capacity (cm/hr)

$f_0$ = initial infiltration capacity (cm/hr)

$k$ = rate of infiltration capacity decrease (1/hr)

In very simple terms:

- At the start of rainfall: infiltration is **fast** (dry soil, high capacity).  
- As the storm continues: infiltration capacity **drops** and approaches a **final constant value**.  
- If rainfall intensity becomes **greater than the infiltration capacity**, the **excess water** can form **Hortonian overland flow** (infiltration-excess runoff).

The Horton model is intentionally simple. It does **not** describe the detailed movement of water in the soil profile or changes between storms, but it is an excellent **first step** for building intuition about how soils respond to rainfall and when surface runoff is likely to begin.
""")

#-------INTERACTIVE PLOT
st.subheader('Interactive Plot and Exercise', divider="blue")

# Input data

def update_f0():
    st.session_state.f0 = st.session_state.f0_input
    
def update_fc():
    st.session_state.fc = st.session_state.fc_input
    
#def update_k():
#    st.session_state.k = st.session_state.k_input 
    
def update_prec():
    st.session_state.prec = st.session_state.prec_input 

# Callback function to update session state
def update_k():
    """Handles both number input (float) and select_slider (str)"""
    raw_val = st.session_state.k_input
    if isinstance(raw_val, str):
        st.session_state.k = float(raw_val)  # from select_slider
    elif isinstance(raw_val, float):
        st.session_state.k = raw_val         # from number_input
    
# Define the minimum and maximum for the logarithmic scale
log_min = -2.0 # Corresponds to 10^-7 = 0.0000001
log_max = 1.0  # Corresponds to 10^0 = 1
    
# User defined input
st.session_state.f0 = 7.0
st.session_state.fc = 4.0
st.session_state.prec = 3.0

# Initialize session state for value and toggle state
if "k" not in st.session_state:
    st.session_state.k = 1e+1
st.session_state.k_label = "1e-2"

# ---- Initialize k and k_input ----
labels, default_label = prep_log_slider(default_val=1e+1,
                                        log_min=log_min,
                                        log_max=log_max)

if "k" not in st.session_state:
    st.session_state.k = float(default_label)



columns1 = st.columns((1,1,1), gap = 'small')
with columns1[0]:
        with st.expander("Modify the **Plot Controls**"):
            x_point = st.slider(f'**Point (x-axis) for result output**:',0,86400,0,10)
            st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $h$, $rho_f$ and $rho_s$.")
#            reset = st.button(':red[Reset the plot to the initial values]')
#            if reset:
#                st.session_state.f0 = 7.0
#                st.session_state.fc = 4.0
#                st.session_state.prec = 3.0
#                st.session_state.k = 1e+1

with columns1[1]:
    with st.expander('Modify :orange[**Infiltration capacity**]'):

        # --- f0
        if st.session_state.number_input:
            f0 = st.number_input(":green[**Initial infiltration capacity** $f0$ (cm/hr)]",
                                 0.0, 50.0, st.session_state.f0, 0.1,
                                 key="f0_input", on_change=update_f0)
        else:
            f0 = st.slider(":green[**Initial infiltration capacity** $f0$ (cm/hr)]",
                           0.0, 50.0, st.session_state.f0, 0.1,
                           key="f0_input", on_change=update_f0)

        # --- fc
        if st.session_state.number_input:
            fc = st.number_input(":orange[**Equilibrium infiltration capacity** $fc$ (cm/hr)]",
                                 0.0, 50.0, st.session_state.fc, 0.1,
                                 key="fc_input", on_change=update_fc)
        else:
            fc = st.slider(":orange[**Equilibrium infiltration capacity** $fc$ (cm/hr)]",
                           0.0, 50.0, st.session_state.fc, 0.1,
                           key="fc_input", on_change=update_fc)
        
        # --- Generate slider labels ---
        labels, _ = prep_log_slider(default_val=st.session_state.k,
                                    log_min=log_min,
                                    log_max=log_max)
        
        # --- Ensure k_input exists for the active mode ---
        if st.session_state.number_input:
            # numeric mode → k_input must be float
            if "k_input" not in st.session_state or isinstance(st.session_state.k_input, str):
                st.session_state.k_input = st.session_state.k
        else:
            # slider mode → k_input must be a string label
            if "k_input" not in st.session_state or isinstance(st.session_state.k_input, float):
                st.session_state.k_input = get_label(st.session_state.k, labels)
        
        
        # --- Render widget ---
        if st.session_state.number_input:
            # numeric mode
            st.number_input(
                ":red[**Rate of infiltration capacity decrease** $k$ (1/hr)]",
                10**log_min, 10**log_max,
                st.session_state.k_input,
                get_step(st.session_state.k_input),
                format="%.2e",
                key="k_input"
            )
            # update internal numeric value
            st.session_state.k = float(st.session_state.k_input)
        
        else:
            # slider mode
            st.select_slider(
                ":red[**Rate of infiltration capacity decrease** $k$ (1/hr)]",
                options=labels,
                value=get_label(st.session_state.k, labels),
                key="k_input"
            )
            # update internal numeric value
            st.session_state.k = float(st.session_state.k_input)

with columns1[2]:
        with st.expander('Modify :blue[**Precipitation**]'):
            if st.session_state.number_input:
                prec = st.number_input(r":blue[**Precipitation** $P$ (cm/hr)]", 0., 15.0, st.session_state.prec, 0.1, key="prec_input", on_change=update_prec)
            else:
                prec = st.slider      (r":blue[**Precipitation** $P$ (cm/hr)]", 0., 15.0, st.session_state.prec, 0.1, key="prec_input", on_change=update_prec)

# Convert the slider value to the logarithmic scale
k = st.session_state.k/3600 #time in seconds

tmax = 86400
t = np.arange(0, tmax, tmax/200)

if f0<fc:
    f0 = fc

y = fc+(f0-fc)*(math.e**(k*t*-1))
    
#Compute K_eq for the example point
y_point = fc+(f0-fc)*math.e**(k*-1*x_point)
    
# Plot
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(t,y, linewidth =3, label='Infiltration rate')
ax.set(xlabel='time in s', ylabel='infiltration capacity / precipitation rate in cm/hr',title='Infiltration capacity')
ax.set(xlim=(0, tmax), ylim=(0, max(f0,prec)*1.1))
if prec <= fc:
    plt.hlines(prec, 0, tmax, colors='aqua', linestyles='solid', label='precipitation rate')
ax.fill_between(t, prec, 0, facecolor= 'lightblue')
if prec > fc:
    plt.hlines(prec, 0, tmax, colors='red', linestyles='solid', label='precipitation rate')
    ax.fill_between(t, prec, y, where=prec > y, facecolor= 'red', alpha=0.5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='your input')
xticks = np.arange(0, tmax, 7200)
ax.set_xticks(xticks)
ax.grid()
plt.legend()

st.pyplot(fig)
 
st.write("Time after beginning of precipitation: %3i" %x_point)
st.write('Infiltration rate in cm/hr:  %5.2f' %y_point)

st.subheader('✔️ Conclusion', divider='blue')
st.markdown("""
The Horton model provides a simple way to describe how a soil’s **infiltration capacity** decreases during a storm and when **infiltration-excess overland flow** is likely to begin. Even though it is empirical and simplified, it is a useful first step for understanding how rainfall is partitioned between **infiltration** and **runoff**.
""")

# --- FINAL ASSESSMENT ---
def content_final_HOR():
    st.markdown("""#### Final assessment""")
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
    section_id="HOR_03",
    label="✅ **Show the final assessment** - to self-check your **understanding**",
    content_fn=content_final_HOR,
    default_open=False,
)

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
