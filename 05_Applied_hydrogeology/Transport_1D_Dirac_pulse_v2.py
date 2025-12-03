import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import streamlit as st
import json
from streamlit_book import multiple_choice

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

def read_md(doc_name: str) -> str:
    if not doc_name or not ALLOWED.match(doc_name):
        return f"**Invalid document name:** `{doc_name}`"
    p = (DOCS_DIR / doc_name).resolve()
    try:
        if DOCS_DIR not in p.parents:
            return f"**Access denied:** `{doc_name}`"
        if not p.exists() or not p.is_file():
            return f"**Document not found:** `{doc_name}`"
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"**Error reading `{doc_name}`:** {e}"

# RENDER ASSESSMENTS

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
            
def read_numerical_breakthrough(uploaded_file):
    """
    Reads a text file with lines like:
    STEP   TIME   CONC
    1    1.0000   0.0000
    1    2.0000   0.0000
    ...
    Returns: time_array, concentration_array
    """
    import io

    # UploadedFile -> bytes -> text
    content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    data = []
    for line in lines:
        parts = line.split()
        # Expect at least: STEP, TIME, CONC
        if len(parts) < 3:
            continue
        try:
            step = int(parts[0])
            t = float(parts[1])
            c = float(parts[2])
            data.append((step, t, c))
        except ValueError:
            # Skip header or non-numeric lines
            continue

    if not data:
        return None, None

    arr = np.array(data)
    time_num = arr[:, 1]
    conc_num = arr[:, 2]
    return time_num, conc_num

#FUNCTIONS FOR COMPUTATION; ADS = ADVECTION, DISPERSION AND SORPTION - EVENTUALLY SET RETARDATION TO 1 FOR NO SORPTION
def c_ADE(x, t, dM, Area, n, a, v):
    
    D = v * a
    
    # Pre-factor term
    prefactor = dM / (2 * Area * n * np.sqrt(np.pi * D * t))
    
    # Exponential term
    exponential = np.exp(-((x - v * t) ** 2) / (4 * D * t))
    
    # Concentration
    c = prefactor * exponential
    return c

# --- INITIALIZE AND LOADING
# --- LOAD ASSESSMENTS
# ---------- path to questions for the assessments (direct path)
path_quest_ini   = "05_Applied_hydrogeology/questions/1D_AD_Dirac_initial.json"
path_quest_final = "05_Applied_hydrogeology/questions/1D_AD_Dirac_final.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)


# --- Starting the App here

st.title('1D Transport with advection and dispersion')
st.subheader('Tracer input as :green[Dirac Pulse] data', divider="green")
    
st.markdown("""
    #### Motivation
    Analytical solutions of conservative solute transport are useful for process understanding. They allow to investigate the effects of advection and dispersion on concentration profiles (concentration along the flow path) and breakthrough curves (concentration over time). Besides, analytical solutions are very useful for comparison with numerical solutions to understand the requirements of these methods, for example regarding discretization, and to understand also the limitations of these methods. With this knowledge, numerical models can be designed in an efficient way.
    
    The control panel allows to adjust the breakthrough curve and the concentration profile. In addition, it's possible to upload results from MT3D, e.g., a mass-transport-observation file with computed concentrations.
    Use the control panel on the right side to adjust the parameter of the advection-dispersion equation.
    
    #### Learning objectives
    The learning objectives of this interactive app are
    - Understand and explain the effects of advective and dispersive transport on solute concentration in a 1D column.
    - Analyse the effects of porosity and dispersivity on the transport behavior.
    - Analyse the results of a numerical model and optimize the numerical model accordingly.
""")    
    
# --- INITIAL ASSESSMENT ---
def content_initial():
    st.markdown("""#### Initial assessment""")
    st.info("You can use the initial questions to assess your existing knowledge.")
    
    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3), (4,5)]:
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
    section_id="green_ampt_ini",
    label="✅ **Show the initial assessment** – to assess your **EXISTING** knowledge",
    content_fn=content_initial,
    default_open=False,
)
    
st.subheader("Introduction and Overview", divider = 'blue')
st.markdown("""
The 1D advection-dispersion equation computes conservative transport. A solution if provided by Ogata and Banks (1961).
""")
with st.expander("Show more theory"):
    st.latex(r'''c(x,t) = \frac{\Delta M}{2 \cdot A \cdot n_e \sqrt{\pi \cdot D \cdot t}} e^{-\frac{(x - v \cdot t)^2}{4 D \cdot t}}''')

st.subheader("Computation ", divider = 'green')
st.markdown("""
            #### About the computed situation
            
            Transport is considered for a 1D system with the following characteristics
            * column with a diamter of 0.1 m,
            * steady groundwater flow,
            * discharge $Q$ = 2.7271E-7 m3/s,
            * The solutes are added by an Dirac pulse (instantaneous release) with a mass of $M$ = 1 g.
            
            The average velocity $v_a$ is depending on the effective porosity $n_e$ and printed below the interactive plot.        
            
            The plots show the solute concentration for advective-dispersive transport:
            
           :blue[(1) The **break through** curve is computed for an observation point in a user-defined distance from the source. It is possible to plot a second breakthrough curve in an user-defined distance relative to the first observation.]
            
            :red[(2) The **concentration profile** shows the situation for a specific time.]
            
            #### Interactive plot
            
            The control panel allows to adjust the breakthrough curve and the concentration profile. In addition, it's possible to upload results from MT3D, e.g., a mass-transport-observation file with computed concentrations.
            Use the control panel on the right side to adjust the parameter of the advection-dispersion equation.
        """, unsafe_allow_html=True)

columns2 = st.columns((1,1,1))

with columns2[0]:
    with st.expander(":blue[Control for the breakthrough curves]"):
        x  = st.slider(f'**Distance of the primary observation from source (m)**',0.01,1.0,0.5,0.01)
        multi = st.toggle("Plot two curves")
        if multi:
            dx = st.slider(f'**Distance between the primary and secondary observation (m)**',0.,0.5,0.1,0.01) 
        show_num = st.toggle("Load and show numerical model results", value=False)
        uploaded_file = None
        if show_num:
            uploaded_file = st.file_uploader(
                "Upload numerical breakthrough file",
                type=["txt", "dat", "out", "mto"], 
                key="num_file"
            )
with columns2[1]:
    with st.expander(":red[Controls for the concentration profile]"):
        tp = st.slider(f'**Time for the concentration profile (s)**',0,14400,600,300)      
 
with columns2[2]:
    with st.expander("Controls for the solute transport"):
        #dM = st.slider(f'**Input mass (g)**',0.01,5.0,1.0,0.01)
        n = st.slider(f'**Porosity (dimensionless)**',0.02,0.6,0.2,0.001)       
        a = st.slider(f'**Longitudinal dispersivity (m)**',0.001,0.15,0.01,0.001, format="%.3f")
    
"---"
dM = 1
r  = 0.05      # Column radius
Q = 2.7271E-7
Area = np.pi*r**2
q = Q/Area
v = q/n

# Data for plotting
t0 = 1      # Starting time
t1 = 14400   # Ending time
dt = 10      # Time discretization
ci = 0      # Initial concentration

# Defining time range
t = np.arange(t0, t1, dt)

# Computation of concentration (terms in brackets)
# Set fraction of distance
cmax   = 0
time   = []
space  = []
conc   = []
conc2  = []
concp  = []
   

#compute break through
for t in range(t0, t1, dt):      
    # ADVECTION-DISPERSION
    cmax1 = ci+c_ADE(1, t, 1, Area, n, 0.01, v)
    if cmax1 > cmax:
        cmax = cmax1
    c = ci+c_ADE(x, t, dM, Area, n, a, v)
    conc.append(c)
    if multi:
        c2 = ci+c_ADE(x+dx, t, dM, Area, n, a, v)
        conc2.append(c2) 
    time.append(t)
    
#compute concentration profile
for xp in np.linspace(0, 1, num=100):      
    # ADVECTION-DISPERSION
    cp = ci+c_ADE(xp, tp, dM, Area, n, a, v)
    concp.append(cp)
    space.append(xp)     
        
# measurements
t_obs = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
c_obs = [1e-3, 5e-2, 8.5e-2, 9.7e-2, 9.9e-2, 10e-2, 10e-2, 10e-2, 10e-2, 10e-2]
   
#PLOT FIGURE
fig = plt.figure(figsize=(9,8))
ax = fig.add_subplot(2, 1, 1)
ax.set_title('1D solute transport with advection-dispersion', fontsize=16)
ax.set_xlabel ('Time (s)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
# PLOT HERE
ax.plot(time,conc, 'navy', linewidth=2, label="Breakthrough observation 1")
if multi:
    ax.plot(time,conc2, 'lightblue', linewidth=2, label="Breakthrough observation 2")
    
# NEW: numerical breakthrough
if show_num and uploaded_file is not None:
    time_num, conc_num = read_numerical_breakthrough(uploaded_file)
    if time_num is not None:
        ax.plot(time_num, conc_num, marker='o', markersize=5, 
        markerfacecolor='none', markeredgecolor='deepskyblue', markeredgewidth=0.6,
        linestyle='none', label="Numerical model (uploaded)")
    else:
        st.warning("Could not read any numerical data from the uploaded file.")
        
plt.ylim(0,5000)
plt.xlim(0,t1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(frameon=False, loc='upper right', fontsize=14)

ax = fig.add_subplot(2, 1, 2)
ax.set_xlabel ('Distance from source along flow directions (m)', fontsize=14)
ax.set_ylabel ('Concentration (g/m³)', fontsize=14)
      
# PLOT HERE
ax.plot(space,concp, 'orange', linewidth=2, label="Concentration profile")
plt.ylim(0,10000)
plt.xlim(0,1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(frameon=False, loc='upper right', fontsize=14)
    
st.pyplot(fig)

st.write("Average velocity _v_ (m/s) = ","% 7.3E"% v)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')