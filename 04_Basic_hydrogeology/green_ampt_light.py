import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path
import re
import json
from streamlit_book import multiple_choice

COLOR_CYCLE = [
    "tab:blue", "tab:orange", "tab:green", "tab:red",
    "tab:purple", "tab:brown", "tab:pink", "tab:gray",
    "tab:olive", "tab:cyan",
]

st.set_page_config(page_title = "iNUX - Green Ampt", page_icon="04_Basic_hydrogeology/FIGS/iNUX_wLogo.png")

# --- Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Grießer": [1],
    "Matthias Hausleber": [1]
}
institutions = {
    1: "Department of Earth Sciences, University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# --- FUNCTIONS
# Make docs/ relative to THIS file, not the working directory
DOCS_DIR = (Path(__file__).parent / "docs").resolve()
DOCS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED = re.compile(r"^[A-Za-z0-9_\-]+\.md$")

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


# --- INITIALIZATION
if "saved_params" not in st.session_state:
    st.session_state["saved_params"] = []
    
# --- LOAD ASSESSMENTS
# ---------- path to questions for the assessments (direct path)
path_quest_ini   = "03_Soil_physics/questions/green_ampt_ini.json"
path_quest_final = "03_Soil_physics/questions/green_ampt_final.json"

# Load questions
with open(path_quest_ini, "r", encoding="utf-8") as f:
    quest_ini = json.load(f)
    
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
st.title('Green-Ampt-Model for Infiltration v2')
st.subheader('Understanding infiltration into soils', divider = 'green')

st.markdown("""
#### 💡 Motivation
Understanding infiltration into soils is fundamental for many fields of groundwater and hydrological practice. The Green–Ampt model provides a simple but powerful way to describe how water moves from the surface into variably wet soils. This app enables learners to explore how soil properties and initial conditions affect infiltration behavior, helping to connect theory with visual, interactive interpretation. Accordingly, this app:
- Helps understand how soils respond to rainfall or irrigation.
- Links soil hydraulic properties (saturated hydraulic conductivity $K_s$, difference in soil water content $\Delta \\theta$, head difference $\Delta h$) to infiltration processes.
- Offers an intuitive introduction before more complex models (e.g., van Genuchten–Mualem).
- Supports applied questions in hydrology, agriculture, and groundwater recharge analysis.""")

st.markdown("""
#### 🎯 Learning Objectives
After working with this app, you will be able to:
- Understand the conceptual assumptions of the Green–Ampt infiltration approach (sharp wetting front, $\Delta \\theta$, $\Delta h$).
- Interpret how changes in soil hydraulic properties influence cumulative infiltration and infiltration rates.
- Analyze the effect of varying $K_s$, $\Delta \\theta$, and $\Delta h$ using interactive plots and identify characteristic infiltration patterns.
""")

# --- INITIAL ASSESSMENT ---
def content_initial():
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
    section_id="green_ampt_ini",
    label="✅ **Show the initial assessment** – to assess your **EXISTING** knowledge",
    content_fn=content_initial,
    default_open=False,
)
st.markdown(""" 

#### 📐 Some theory

Figure 1 shows a situation where the rainfall rate was greater than the infiltration rate such that ponding occured and water infiltrates into the soil. In consequence, infiltration occurs, which can be computed by the Green-Ampt equation.
""")

st.image("04_Basic_hydrogeology/FIGS/Green_Ampt_Model.png", caption="Figure 1: Soil water profile for the case of ponding (a). Volumetric water content as a function of soil depth for a (b) 'real situation' and (c) assumptions underlying the Green-Ampt equation.")

with st.expander("Show more explanation", icon ="📑"):
        st.markdown("""  A similar situation occurs in experiments with double ring infiltrometers (Figure 2). """)

        st.image("04_Basic_hydrogeology/FIGS/Doppelring-Infiltrometer.jpg", caption='Figure 2: Double Ring Infiltrometer', width=350)

        st.markdown("""
        In these experiments, two concentric rings, which are partially inserted into the soil, are filled with water. The water in the outer ring is intended to prevent lateral flow. Therefore, we assume vertical infiltration in the inner ring as an approximation. As a result of the ponding, a wetting front moves downward in the soil.
        
        In the wetted zone above the wetting front, the soil is saturated and has a water content $\\theta_0$ close to saturation (field saturated).
        
        Below this, the soil still has its initial water content $\\theta_i$. There is a (positive) pressure potential $h_0$ at the soil surface due to the ponding, and a (negative) matrix potential $h_f$ at the moisture front due to the unsaturated conditions. 
        
        The conceptual model described above simplifies the distribution of the water content and the matrix potential in the soil. Depending on the soil properties, the transition from field saturation to initial conditions is less abrupt. However, the simplified assumption of a sharp wetting front allows the derivation of a mathematical relationship between the cumulative infiltration $I(t)$ and the time $t$ since the infiltration began:""")
        
        st.latex(r'''I(t) - \Delta\theta \Delta h \ln \left( 1 + \frac{I(t)}{\Delta h} \right) = K_s t''')
        
        st.markdown("""
        
        with 
        - $\\theta_0$ = soil water content before infiltration starts
        - $\\theta_i$ = soil water content after infiltration
        - $\\Delta \\theta$ = $\\theta_0 - \\theta_i$
        - $h_0$ = matrix potential at the ground surface}
        - $h_f$ = matrix potential at the wetting front
        - $\\Delta h$ = $h_0 - h_f$
        - $K_s$ = hydraulic conductivity of the saturated soil in the wetted zone
        
        Although this equation cannot be solved for $I(t)$, we can solve it for $t$ and thus calculate and visualize the cumulative infiltration $I(t)$ for given values of the time $t$:""")
        
        st.latex(r'''t = \frac{I(t) - \Delta\theta \Delta h \ln \left(1 + \frac{I(t)}{\Delta\theta \Delta h} \right)}{K_s}''')
        
        st.markdown("""
        To understand which and how the model parameters control the infiltration process, it is helpful to change the individual parameter values and examine the effects on the cumulative infiltration and the infiltration rate. The latter is obtained by divding the change of the cumulative infiltration in a short time intervall through the length of this time intervall.""")

# ToDo: Implement a table to choose the suitable parameters (see GWP_SoilWaterRetention)
with st.expander("Show typical parameter values"):
        st.markdown( r""" *Table 1: Typical parameter values (after Chin, D.A.: Water-Resources Enginieering, 2013).
        Please note that for the use in this app, the values of $K_s$ need to be transformed from mm/h to mm/min.
        The (field-)saturated water content $\theta_0$ can be approximated by the porosity, 
        the initial water content $\theta_i$ is likely to range between field capacity and wilting point, 
        with the field capacitiy representing conditions a few days after a rain event and the wilting point 
        those after a long drought.* """)
        st.markdown(""" 
                | USD soil-texture class | Hydraulic conductivity [mm/h] | Suction head matrix potential [mm] | Porosity [-] | Field capacity [-] | Wilting point [-] |
                |------------|:--------------------------------------:|:-----------------:|:-------------:|:-------------:|:----------:|
                | Sand | 120 | -49 bis -150 | 0,437 | 0,062 | 0,024 |
                | Loamy sand | 30 | -61 bis -250 | 0,437 | 0,105 | 0,047 |
                | Sandy Loam | 11 | -110 bis -250 | 0,453 | 0,190 | 0,085 |
                | Loam | 3 | -89 bis -350 | 0,463 | 0,232 | 0,116 |
                | Silt Loam | 7 | -170 | 0,501 | 0,284 | 0,135 |
                | Sandy clay loam | 2 | -220 | 0,398 | 0,244 | 0,136 |
                | Clay loam | 1 | -210 | 0,464 | 0,310 | 0,187 |
                | silty clay loam | 1 | -270 | 0,471 | 0,342 | 0,210 |
                | Sandy clay | 1 | -240 | 0,430 | 0,321 | 0,221 |
                | Silty clay | 1 | -290 | 0,479 | 0,371 | 0,251 |
                | Clay | 0,3 | -320 bis -1000 | 0,475 | 0,378 | 0,265 |""",unsafe_allow_html=True,)

st.subheader("Interactive plot", divider = 'green')

st.markdown("""
The interactive plot visualizes how cumulative infiltration _I(t)_ and infiltration rate _i(t)_ evolve over time based on the selected soil parameters. By adjusting $K_s$, $\Delta \\theta$, and $\Delta h$, users can investigate how soil wetness, suction forces, and hydraulic conductivity control infiltration behavior.

How to use the plot

Modify $\Delta h$ to see how the suction head contrast influences infiltration.

Adjust $\Delta \\theta$ to explore the effect of soil wetness and available pore space.

Change $K_s$ to examine how hydraulic conductivity controls long-term infiltration.

Save multiple parameter sets to compare scenarios in a single figure.

The plot helps build intuition for how physical soil properties shape the infiltration response.
You can modify the input with the following sliders. Additionally, you can save the computed line by using the button.
""")
# Interactive Input
col3, col4, col5 = st.columns((1,1,1), gap="large")
with col3:
        hf_h0 = st.slider(r'$h_f - h_0 \, \text{[mm]}$',-1000,500,[-600,0],1,key='hf_h0')
with col4:
        thetai_theta0 = st.slider(r'$\theta_i-\theta_0 \, \text{[-]}$' , 0.,0.5,[0.1,0.4],0.01,key='thetai_theta0')

log_options = np.round(np.concatenate([
    [v for v in np.arange(0.005, 0.01, 0.0001) if int(v * 1e4) % 10 == 0],  
    np.arange(0.01, 0.1, 0.01), 
    np.arange(0.1, 1, 0.1),    
    np.arange(1, 6, 1)         
]), decimals=4)

with col5:
        Ks = st.select_slider(r'$K_s \, \text{[mm/min]}$',log_options, value=0.5, key='Ks')

# Green Ampt Modell
def t_for_It(I_t, d_theta, d_h, Ks):                                                    
        return (I_t - d_theta * d_h * np.log(1+ (I_t/(d_theta*d_h))))/Ks                                    

def long_time_approximation(Ks, x):                                                          
        it_long = np.array([Ks]*len(x))                                                                  
        return it_long
  
def infiltration_rate(new_t, t, I_t):                                         
        y2 = np.interp(new_t, t, I_t)                                                                          
        i_t = np.diff(y2)
        return i_t

def compute_curves(Ks, delta_theta, delta_h,
                   t_plot_max=185.0,
                   I_axis_max=600.0,
                   I_axis_min=0.0,
                   dI=0.1,
                   delta_t2=0.1):
    """
    Compute I(t), t, t2, i(t), and long-time approximation
    from Ks, Δθ, Δh with the same logic as the main plot.
    """

    # Estimate cumulative infiltration at t_plot_max
    I_est = Ks * t_plot_max + delta_theta * delta_h  # [mm]

    # Choose I_max within [I_axis_min, I_axis_max]
    I_max = min(I_axis_max, max(I_axis_min, I_est))

    # Cumulative infiltration grid
    I_t = np.arange(dI, I_max + dI, dI)

    # Time corresponding to I_t
    t = t_for_It(I_t, delta_theta, delta_h, Ks)

    # Guard against invalid t
    if not np.isfinite(t).all():
        return None  # caller can skip this curve

    # Uniform time grid for rate calculation
    t2 = np.arange(round(t[0], 1), round(t[-1], 1), delta_t2)
    if len(t2) < 3:
        return None

    # Infiltration rate and long-time approximation
    i_t = infiltration_rate(t2, t, I_t)
    i_t_long = long_time_approximation(Ks, t2)

    return I_t, t, t2, i_t, i_t_long



hf, h0 = hf_h0
theta_i, theta_0 = thetai_theta0
delta_theta = round(abs(theta_0-theta_i),2)
delta_h = round(abs(hf-h0),2)

t_plot_max = 185.0
I_axis_max = 600.0
I_axis_min = 0.0

delta_t2 = 0.1

curves = compute_curves(Ks, delta_theta, delta_h, delta_t2=delta_t2)

if curves is None:
    st.warning("Parameters lead to an invalid solution. Please adjust the sliders.")
    st.stop()

I_t, t, t2, i_t, i_t_long = curves
                                          

# Plot
fig, (ax1, ax2) = plt.subplots(2, figsize=(8,8))                                  

ax1.plot(t, I_t, color='black', 
    label='$I(t)$ with $\Delta h$: {}, $\Delta \\theta$: {:.2f}, $K_s$: {}'.format(delta_h, delta_theta, Ks), linewidth=1)
        
ax1.set_title(label='Green-Ampt Infiltration Model', fontsize=20, loc= 'center')                 
ax1.set_xlim(0, t_plot_max)
ax1.set_ylim(I_axis_min, I_axis_max)
ax1.set_xlabel('time [min]', fontsize=10)                                                         
ax1.set_ylabel('cummulative infiltration [mm]', fontsize=10)
ax1.grid(which = "major", linewidth = 1, alpha=0.5)                                                         
ax1.grid(which = "minor", linewidth = 0.2, alpha=0.5)
ax1.minorticks_on()
    
ax2.plot(t2[1:-5], i_t[0:-5]/delta_t2, color='black',
        label='$i(t)$ with $\Delta h$: {}, $\Delta \\theta$: {:.2f}, $K_s$: {}'.format(delta_h, delta_theta, Ks), linewidth=1)     
ax2.plot(t2, i_t_long, 'black', linestyle='--',                                         
        label='Long time approx. ~ $K_s$')
                                                                                   
ax2.set_xlim(0, t_plot_max)
ax2.set_yscale('log')   
ax2.set_ylim(0.001, 100)                                                                                
ax2.set_xlabel('time [min]', fontsize=10)                                                               
ax2.set_ylabel('infiltration rate [mm/min]', fontsize=10)
ax2.grid(which = "major", linewidth = 1, alpha=0.5)                                                               
ax2.grid(which = "minor", linewidth = 0.2, alpha=0.5)
ax2.minorticks_on()

columns_but = st.columns((1, 1, 2))

with columns_but[0]:
    
    MAX_SAVED = 8
    
    if st.button("Save line"):
        saved = st.session_state["saved_params"]
        # pick next color from the cycle, stable over time
        color_idx = len(saved) % len(COLOR_CYCLE)
        color = COLOR_CYCLE[color_idx]

        saved.append(
            {
                "Ks": float(Ks),
                "delta_theta": float(delta_theta),
                "delta_h": float(delta_h),
                "color": color,
            }
        )

        # Keep only the last MAX_SAVED entries
        if len(saved) > MAX_SAVED:
            st.session_state["saved_params"] = saved[-MAX_SAVED:]
        
with columns_but[1]:
    if st.button("Clear saved lines"):
        st.session_state["saved_params"] = []
    

# Plot saved lines (recomputed from parameters)
if st.session_state["saved_params"]:
    for sp in st.session_state["saved_params"]:
        saved_Ks = sp["Ks"]
        saved_delta_theta = sp["delta_theta"]
        saved_delta_h = sp["delta_h"]
        color = sp.get("color", "tab:blue")  # fallback if old entries exist

        saved_curves = compute_curves(
            saved_Ks,
            saved_delta_theta,
            saved_delta_h,
            delta_t2=delta_t2
        )

        if saved_curves is None:
            continue  # skip invalid combinations

        saved_I_t, saved_t, saved_t2, saved_i_t, saved_i_t_long = saved_curves

        # Upper plot: cumulative infiltration
        ax1.plot(
            saved_t,
            saved_I_t,
            color=color,
            linestyle=":",
            linewidth=1,
            label='$I(t)$ with $\\Delta h$: {}, $\\Delta \\theta$: {:.2f}, $K_s$: {}'.format(
                saved_delta_h, saved_delta_theta, saved_Ks
            ),
        )

        # Lower plot: i(t)
        ax2.plot(
            saved_t2[1:-5],
            saved_i_t[0:-5] / delta_t2,
            color=color,
            linestyle=":",
            linewidth=1,
            label='$i(t)$ with $\\Delta h$: {}, $\\Delta \\theta$: {:.2f}, $K_s$: {}'.format(
                saved_delta_h, saved_delta_theta, saved_Ks
            ),
        )

        # Lower plot: long-time approximation, same color, dashed
        ax2.plot(
            saved_t2,
            saved_i_t_long,
            color=color,
            linestyle="--",
            alpha=0.5,
            label="Long time approx. ~ $K_s$",
        )



# Make room on the right for legends
fig.subplots_adjust(right=0.75)

# Legend for upper plot (ax1) – outside right
ax1.legend(
    loc="upper left",
    bbox_to_anchor=(1.02, 1.0),
    borderaxespad=0.0,
    fontsize=9,
)

# Legend for lower plot (ax2) – outside right
ax2.legend(
    loc="upper left",
    bbox_to_anchor=(1.02, 1.0),
    borderaxespad=0.0,
    fontsize=9,
)

st.pyplot(fig)

st.subheader('✔️ Conclusion', divider = 'green')
st.markdown("""
The Green–Ampt infiltration model provides a clear and intuitive way to explore how soils respond to rainfall, irrigation, and surface water inputs. By varying the key parameters $\Delta \\theta$, $\Delta h$, and $K_s$, this app illustrates how soil moisture conditions, suction forces, and hydraulic conductivity shape both cumulative infiltration and infiltration rates over time.

While the Green–Ampt model is based on simplifying assumptions, it remains a valuable tool for conceptual learning and for examining how soil and boundary conditions influence water movement into the unsaturated zone. As an outlook, more advanced models, such as those based on the Richards equation or the van Genuchten–Mualem formulation, allow for a more detailed representation of moisture profiles and unsaturated zone hydraulics.
""")

# --- FINAL ASSESSMENT ---
def content_final():
    st.markdown("""#### 🧠 Final assessment""")
    st.info("These questions test your understanding after working with the application.")
    
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
    section_id="green_ampt_final",
    label="✅ **Show the final assessment** - to self-check your **understanding**",
    content_fn=content_final,
    default_open=False,
)

st.markdown('---')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('04_Basic_hydrogeology/FIGS/CC_BY-SA_icon.png')



