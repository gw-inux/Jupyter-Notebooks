import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from pathlib import Path
from GWP_SoilWaterRetention_utils import read_md
from GWP_SoilWaterRetention_utils import flip_assessment
from GWP_SoilWaterRetention_utils import render_toggle_container
from GWP_SoilWaterRetention_utils import load_md
from GWP_SoilWaterRetention_utils import ui_text


# --- Track the current page / Scroll to top
PAGE_ID = "THE"

# Do (optional) things/settings if the user comes from another page
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_ID
if st.session_state.current_page != PAGE_ID:
    st.session_state.current_page = PAGE_ID
    
# Start the page with scrolling here
if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
#Empty space at the top
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# Authors, institutions, and year
year = 2025 
authors = {
    "Oriol Bertran": [1],
    "Daniel Fernàndez-Garcia": [1],
    "Thomas Reimann": [2],    
    "Eileen Poeter": [3]
}
institutions = {
    1: "UPC Universitat Politècnica de Catalunya",
    2: "TU Dresden",
    3: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

# --- FUNCTIONS ---
def m_val(n):
    """Function that returns the value of "m"
    Parameters
    ----------
    n : float
        value of "n"
    Returns
    -------
    float
        value of "m"
    """
    m = 1 - (1/n)
    return m

def water_content(alpha, h, n):  
    """Function that calculates the water content.  
    Based on van Genuchten, 1980 (Eq. 3)
    Parameters
    ----------
    alpha : float
        alpha parameter
    h : float
        head pressure (positive)
    n : float
        n parameter
    Returns
    -------
    float
        water content
    """  
    T = ((1 + (alpha*h)**(n)))**(-(m_val(n)))  
    return T

def soil_water_content(tr, ts, alpha, h, n):
    """Function that calculates the soil-water content. 
    Based on van Genuchten, 1980 (Eq. 21)
    Parameters
    ----------
    tr : float
        residual values of soil-water content
    ts : float
        saturated values of soil-water content
    alpha : float
        alpha parameter
    n : float
        n parameter  
    Returns
    -------
    float
        soil-water content
    """
    t = tr + ((ts - tr) / ((1 + (alpha*h)**(n))**m_val(n)))   

    return t  

def relative_hydraulic_conductivity(alpha, n, h, T):
    """Function that calculates the relative hydraulic conductivity. 
    Based on van Genuchten, 1980 (Eq. 8 and 9).
    Parameters
    ----------
    alpha : float
        alpha parameter
    n : float
        n parameter
    h : float 
        head pressure (positive)
    T : float
        water content
    Returns
    -------
    T: float
        _description_
    Kr_T: float
        relative hydraulic conductivity expressed in terms of the dimensionless water content
    Kr_h: float
        relative hydraulic conductivity expressed in terms of the head pressure   
    Raises
    ------
    ValueError
        If m value is not between 0 and 1
    """
    
    # Check that m_val(n) is within the expected range
    if not (0 < m_val(n) < 1):
        raise ValueError("Parameter 'm' out of range: must be between 0 and 1")

    #-- Relative hydraulic conductivity expressed in terms of the water content
    Y = (1 - T**(1 / m_val(n)))**m_val(n)
    Kr_T = T**0.5 * (1 - Y)**2                     
    
    #-- Relative hydraulic conductivity expressed in terms of the pressure head
    I = (1 - alpha * h)
    U = I**(n - 1)
    P = (1 + (alpha * h)**n)**(m_val(n) / 2)
    
    if I > 0:
        Kr_h = ((U * T)**2) / P 
    else:
        Kr_h = np.nan                        
    
    return Kr_T, Kr_h

def soil_water_diffusivity(Ks, n, ts, tr, T):
    """Function that calculates the soil water diffusivity.
    Based on van Genuchten, 1980 (Eq. 11).
    Parameters
    ----------
    Ks : float
        hydraulic conductivity at saturation
    n  : float
        n parameter
    ts : float
        satured soil-water content
    tr : float
        residual soil-water content
    T : float
        dimensionless water content
    Returns
    -------
    D_T : float
        soil water diffusivity
    """  
    I = ((1 - m_val(n))*Ks) / (alpha*m_val(n)*(ts - tr))
    L = T**(0.5 - (1/m_val(n)))
    Y = (1 - T**(1 / m_val(n)))**m_val(n)
    P = ((1/Y) + (Y) - 2)
    
    D_T = I * L * P                                        

    return D_T
    
def render_assessment(filename, title="📋 Assessment", max_questions=4):

    with open(filename, "r", encoding="utf-8") as f:
        questions = json.load(f)

    st.markdown(f"#### {title}")
    for idx in range(0, min(len(questions), max_questions), 2):
        col1, col2 = st.columns(2)
        for col, i in zip((col1, col2), (idx, idx+1)):
            if i < len(questions):
                with col:
                    q = questions[i]
                    st.markdown(f"**Q{i+1}. {q['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=q["options"],
                        success=q.get("success", "✅ Correct."),
                        error=q.get("error", "❌ Not quite.")
                    )
                    
# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

MD_DIR  = Path("90_Streamlit_apps/GWP_SoilWaterRetention_update/assets/md")

videourl1 = 'https://youtu.be/zMzqiAuOSz0'
videourl2 = 'https://youtu.be/9gm81GghMrk'
videourl3 = 'https://youtu.be/aaGJS5pAmp4'

#st.title('📚 Theory underlying SoilWaterRetention')

st.title(
    ui_text(
        "📚 Theory underlying Soil Water Retention",
        de="📚 Theorie der Bodenwasserretention",
        it="📚 Teoria della ritenzione idrica del suolo",
        fr="📚 Théorie de la rétention d'eau dans le sol",
        es="📚 Teoría de la retención de agua en el suelo",
        pt="📚 Teoria da retenção de água no solo",
        zh="📚 土壤水分保持理论",
    )
)

st.header(
    ui_text(
        "The concepts 📖",
        de="Die Konzepte 📖",
        it="I concetti 📖",
        fr="Les concepts 📖",
        es="Los conceptos 📖",
        pt="Os conceitos 📖",
        zh="基本概念 📖",
    )
)
#-----------------------------------------------#
# UNSATURATED ZONE                              #
#-----------------------------------------------#
st.subheader(
    ":blue-background[" +
    ui_text(
        "An initial overview about the unsaturated zone",
        de="Ein erster Überblick über die ungesättigte Zone",
        it="Una prima panoramica della zona insatura",
        fr="Un premier aperçu de la zone non saturée",
        es="Una primera visión general de la zona no saturada",
        pt="Uma visão geral inicial da zona não saturada",
        zh="非饱和带概述",
    ) +
    "]",
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_01.md", st.session_state.language))

left_co, cent_co, last_co = st.columns((10, 80, 10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/freeze_cherry_2.png')
    st.markdown(
        r"Fig. 1- Groundwater conditions near the ground surface. (a) Saturated and unsaturated zone; (b) profile of moisture content versus depth; (c) pressure-head and. Adapted from Freeze and Cherry (1979)"
    )
    
st.markdown(load_md(MD_DIR, "theory_02.md", st.session_state.language))

#-----------------------------------------------#
# SURFACE TENSION AND WETTABILITY               #
#-----------------------------------------------#
st.subheader(
    ui_text(
        "Surface tension and wettability",
        de="Oberflächenspannung und Benetzungsverhalten",
        it="Tensione superficiale e bagnabilità",
        fr="Tension superficielle et mouillabilité",
        es="Tensión superficial y humectabilidad",
        pt="Tensão superficial e molhabilidade",
        zh="表面张力与润湿性",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_03.md", st.session_state.language))

with st.expander(':rainbow[**Click here to read more about the theoretical aspects of surface tension and wettability**]'):
    st.markdown(load_md(MD_DIR, "theory_04.md", st.session_state.language))

    left_co, cent_co, last_co = st.columns((10, 100, 10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/surface_tension_schema.png')
        st.markdown(
            r"**Fig. 2-** Surface tension schema."
        )
    st.markdown(load_md(MD_DIR, "theory_05.md", st.session_state.language))
        
    left_co, cent_co, last_co = st.columns((1, 2, 1))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/surface_tension_bear.png')   
        st.markdown(
            r"**Fig. 3-** Interfacial tension. From Bear, J. (2013)."
        )
        
    st.markdown(load_md(MD_DIR, "theory_06.md", st.session_state.language))
    
    st.latex(r"W_{ik} = \sigma_{i} + \sigma_{k} - \sigma_{ik}")
    
    left_co, cent_co, last_co = st.columns((10, 30, 10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/water_strider.jpg')
        st.markdown(
            r"**Fig. 4-** Water strider and the surface tension."
            )
    st.markdown(load_md(MD_DIR, "theory_07.md", st.session_state.language))
    
    st.latex(r"cos \theta = \frac{\sigma_{SG} - \sigma_{SL}}{\sigma_{GL}}")
    
    st.markdown(load_md(MD_DIR, "theory_08.md", st.session_state.language))
    
    st.video(videourl1) 

with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/questions/theory_ass_01.json", title="Surface tension and wettability – self assessment")
    
#-----------------------------------------------#
# CAPILLARY PRESSURE                            #
#-----------------------------------------------#
st.subheader(
    ui_text(
        "Capillary pressure",
        de="Kapillardruck",
        it="Pressione capillare",
        fr="Pression capillaire",
        es="Presión capilar",
        pt="Pressão capilar",
        zh="毛细压力",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_09.md", st.session_state.language))

# PLOT CAPILlARY RISE
lc0, rc0 = st.columns((2,1), gap="large")

# Constants
sigma = 0.072  # Surface tension of water [N/m]
theta = 0      # Contact angle [radians] for complete wetting
cos_theta = np.cos(theta)
rho = 1000     # Density of water [kg/m^3]
g = 9.81       # Gravitational acceleration [m/s^2]
    
# Slider to choose radius in micrometers
with lc0:
    st.markdown(load_md(MD_DIR, "theory_10.md", st.session_state.language))
    
    r_mm = st.slider("Pore radius (mm)", min_value=0.005, max_value=1.5, value=0.2, step=0.005, format="%.3f")
    
# Calculate capillary rise height in meters
h_m = (2 * sigma * cos_theta) / (r_mm * 1e-3 * rho * g)

# Plot setup
fig, ax = plt.subplots(figsize=(4, 5))
x = [-r_mm, r_mm]
y = [0, h_m]

# Fill capillary rise area
ax.fill_betweenx([0, h_m], -r_mm, r_mm, color='blue', alpha=0.6, label=f'Capillary rise = {h_m*100:.1f} cm')

# Tube walls
ax.axvline(x=-r_mm, color='grey')
ax.axvline(x= r_mm, color='grey')
    
# Axes and labels
ax.set_xlim(-2, 2)
ax.set_ylim(0, max(1, h_m*1.2))
ax.tick_params(axis='both', labelsize=14)
ax.set_xlabel("Tube cross-section (mm)", fontsize = 14)
ax.set_ylabel("Capillary rise height (m)", fontsize = 14)
ax.set_title("Capillary Rise vs. Tube Radius", fontsize = 16)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.1), borderaxespad=0, ncol=1, frameon=False, fontsize = 14)   

with rc0:
    st.pyplot(fig)

with st.expander(':rainbow[**Click here to read more about the theoretical aspects of capillary pressure**]'):
    
    st.markdown(load_md(MD_DIR, "theory_11.md", st.session_state.language))
    
    st.latex(r"P_{c} = \frac{2\sigma cos\theta}{r}")
    
    st.markdown(load_md(MD_DIR, "theory_12.md", st.session_state.language))
       
    st.video(videourl2)
    
with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/questions/theory_ass_02.json", title="Capillary pressure – self assessment")
    
#-----------------------------------------------#
# Retention curve                               #
#-----------------------------------------------#
st.subheader(
    ui_text(
        "Retention curve",
        de="Retentionskurve",
        it="Curva di ritenzione idrica",
        fr="Courbe de rétention d'eau",
        es="Curva de retención de agua",
        pt="Curva de retenção de água",
        zh="持水曲线",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_13.md", st.session_state.language))

with st.expander(':rainbow[**Click here to read more about the theoretical aspects of the retention curve**]'):
    st.markdown(load_md(MD_DIR, "theory_14.md", st.session_state.language))
    
    left_co, cent_co, last_co = st.columns((10, 50, 10))
    with cent_co:
        st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/retention_curve_mod.png')
        st.markdown(
        r"**Fig. 5-** Example of a retention curve for two types of soil, modified from Bear and Cheng (2010)."
        )
    st.markdown(load_md(MD_DIR, "theory_15.md", st.session_state.language))
    
    left_co, cent_co, last_co = st.columns((10, 50, 10))  
    with cent_co:
        st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/field_capacity.png')
        st.markdown(
            r"**Fig. 6** – Indices describing the retention curves, where (i) $\theta_{fc}$ is the field capacity; "
            r"(ii) $\theta_{wp}$ represents the wilting point; (iii) $\theta_{r}$ is the residual water content; "
            r"and (iv) $\psi_{a}$ is the entry pressure head. Adapted from Stephens, D. B. (2018)."
        )
    st.markdown(load_md(MD_DIR, "theory_16.md", st.session_state.language))

    st.video(videourl3)
    
with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/questions/theory_ass_03.json", title="Capillary pressure – self assessment")
    
st.subheader(
    ui_text(
        "Applications in Agriculture 🌱",
        de="Anwendungen in der Landwirtschaft 🌱",
        it="Applicazioni in agricoltura 🌱",
        fr="Applications en agriculture 🌱",
        es="Aplicaciones en la agricultura 🌱",
        pt="Aplicações na agricultura 🌱",
        zh="农业中的应用 🌱",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_17.md", st.session_state.language))

with st.expander(':rainbow[**Click here to read more about the applications in agriculture**]'):
    st.markdown(load_md(MD_DIR, "theory_18.md", st.session_state.language))

with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/questions/theory_ass_04.json", title="Capillary pressure – self assessment")
    
#-----------------------------------------------#
# The formulation                               #
#-----------------------------------------------#

st.header(
    ui_text(
        "The Formulation :abacus:",
        de="Die Formulierung :abacus:",
        it="La formulazione :abacus:",
        fr="La formulation :abacus:",
        es="La formulación :abacus:",
        pt="A formulação :abacus:",
        zh="数学表达 :abacus:",
    )
)

st.markdown(load_md(MD_DIR, "theory_19.md", st.session_state.language))

st.subheader(
    ui_text(
        "Parameters and Equations",
        de="Parameter und Gleichungen",
        it="Parametri ed equazioni",
        fr="Paramètres et équations",
        es="Parámetros y ecuaciones",
        pt="Parâmetros e equações",
        zh="参数与方程",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_20.md", st.session_state.language))

with st.expander("**Click here to see further details**"):
    st.markdown(load_md(MD_DIR, "theory_21.md", st.session_state.language))

    st.latex(r"\theta = \frac{V_w}{V_t}")
    
    st.markdown(load_md(MD_DIR, "theory_22.md", st.session_state.language))

    st.latex(r"\Theta = \frac{\theta - \theta_{r}}{\theta_{s} - \theta_{r}}")
    
    st.markdown(load_md(MD_DIR, "theory_23.md", st.session_state.language))

    st.latex(r"\Theta = \left[\frac{1}{1 + (\alpha h)^{n}}\right]")
    
    st.markdown(load_md(MD_DIR, "theory_24.md", st.session_state.language))
    
    st.latex(r"\theta = \theta_{r} + \frac{(\theta_{s} - \theta_{r})}{\left[1 + (\alpha h)^{n}\right]^{m}}")
    
    st.markdown(load_md(MD_DIR, "theory_25.md", st.session_state.language))

st.markdown(load_md(MD_DIR, "theory_26.md", st.session_state.language))

with st.expander("**Click here to see further details**"):
    st.markdown(load_md(MD_DIR, "theory_27.md", st.session_state.language))

    st.latex(r"K_{r}(h) = \frac{\{ 1 - (\alpha h)^{n-1} \left[ 1 + (\alpha h)^{n} \right]^{-m} \}^{2}}{\left[1 + (\alpha h)^{n}\right]^{m/2}}")
    
    st.markdown(load_md(MD_DIR, "theory_28.md", st.session_state.language))
    
    st.latex(r"K_{r}(\Theta) = \Theta^{1/2} \left[1 - \left(1 - \Theta^{1/m}\right)^{m} \right]^{2}, \quad m = 1 - \frac{1}{n}, \quad 0 > m > 1")

st.markdown(load_md(MD_DIR, "theory_29.md", st.session_state.language))

with st.expander("**Click here to see further details**"):
    st.latex(r"D(\Theta) = \frac{(1 - m)K_s}{\alpha m (\theta_{s} - \theta_{r})} \Theta^{1/2 - 1/m} \left[\left( 1 - \Theta^{1/m} \right)^{-m} + \left( 1 - \Theta^{1/m} \right)^{m} - 2 \right]")
    
    st.markdown(load_md(MD_DIR, "theory_30.md", st.session_state.language))
    
st.subheader(
    ui_text(
        "Vizualization of the relationships for different soil materials",
        de="Visualisierung der Zusammenhänge für verschiedene Bodenarten",
        it="Visualizzazione delle relazioni per diversi tipi di suolo",
        fr="Visualisation des relations pour différents types de sols",
        es="Visualización de las relaciones para diferentes tipos de suelo",
        pt="Visualização das relações para diferentes tipos de solo",
        zh="不同土壤类型关系的可视化",
    ),
    divider="blue",
)

st.markdown(load_md(MD_DIR, "theory_31.md", st.session_state.language))

columns = st.columns((2,1), gap = 'large')
with columns[0]:
    st.markdown(load_md(MD_DIR, "theory_32.md", st.session_state.language))

#-----------------------------------------------#
# Plot: Three different soils, incl. th example from Van Genuchten 1980
#-----------------------------------------------#

soil_profiles = {
"Loam (default, from Van Genuchten (1980))": {
"θr": 0.10,
"θs": 0.50,
"α": 0.005,
"n": 2.0,
"Ks": 100,
"color": "orange"
},
"Sand": {
"θr": 0.05,
"θs": 0.40,
"α": 0.035,
"n": 2.7,
"Ks": 500,
"color": "green"
},
"Clay": {
"θr": 0.12,
"θs": 0.56,
"α": 0.001,
"n": 1.3,
"Ks": 10,
"color": "red"
}
}

with columns[1]:
    # Selection of dataset
    selected_profile = st.selectbox("Select soil type", list(soil_profiles.keys()))
    params = soil_profiles[selected_profile]
    color = params["color"]

tr = params["θr"]
ts = params["θs"]
alpha = params["α"]
n = params["n"]
Ks = params["Ks"]

#-- Generate pressure head values:
h_values = np.logspace(0, 6, 100)  

#-- Calculate water content values
t_values = [soil_water_content(tr, ts, alpha, h, n) for h in h_values]
T_values = [water_content(alpha, h, n) for h in h_values]

#-- Calculate dimensionless water content and relative hydraulic conductivity
Kr_T, Kr_h = zip(*[relative_hydraulic_conductivity(alpha, n, h, T) for h, T in zip(h_values, T_values)])
Kr_T = list(Kr_T)  
Kr_h = list(Kr_h) 

#-- Calculate the soil-water diffusivity
D_T = [soil_water_diffusivity(Ks, n, ts, tr, T) for T in T_values]

#-- Plot the 3 figures
#fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 5))
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(9, 3), constrained_layout=True)

# ax1: Water content vs. Pressure head
ax1.plot(t_values, np.abs(h_values),color=color, label=selected_profile)
ax1.set_xlim(0, 0.6)
ax1.set_ylim(np.abs(h_values[0]), np.abs(h_values[-1]))
ax1.set_yscale('log')
ax1.set_xlabel(r'Water Content, $\Theta$')
ax1.set_ylabel(r'Pressure Head, $h$ [cm]')

# ax2: Water content vs. Relative Hydraulic Conductivity expressed in terms of water content
ax2.plot(t_values, Kr_T,color=color, label=selected_profile) 
ax2.set_yscale('log')
ax2.set_ylim(0.000001, 1)
ax2.set_xlim(0, 0.6)
ax2.set_xlabel(r'Water Content, $\Theta$')
ax2.set_ylabel(r'Relative Hydraulic Conductivity, $K_{r}$($\Theta$)')

# ax2: Water content vs. Relative Hydraulic Conductivity expressed in terms of pressure head
ax3.plot(np.abs(h_values), Kr_T,color=color, label=selected_profile) 
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlim(1, 10000)
ax3.set_ylim(0.000001, 1)
ax3.set_xlabel('Pressure Head, $h$ [cm] ')
ax3.set_ylabel(r'Relative Hydraulic Conductivity, $K_{r}($h$)$')

# ax4: Water content vs. Diffusivity
ax4.plot(t_values, D_T,color=color, label=selected_profile)
ax4.set_xlim(0, 0.6)
ax4.set_yscale('log')
ax4.set_ylim(1, 1000000)
ax4.set_xlabel(r'Water Content, $\Theta$')
ax4.set_ylabel(r'Diffusivity, $D$')

#plt.tight_layout()
st.pyplot(fig)

st.subheader(
    ui_text(
        "🧾 Conclusion and Final Assessment",
        de="🧾 Zusammenfassung und Abschließende Wissensüberprüfung",
        it="🧾 Conclusioni e valutazione finale",
        fr="🧾 Conclusion et évaluation finale",
        es="🧾 Conclusión y evaluación final",
        pt="🧾 Conclusão e avaliação final",
        zh="🧾 总结与最终测评",
    ),
    divider="blue",
)
st.markdown(load_md(MD_DIR, "theory_33.md", st.session_state.language))

with st.expander('🧠 **Show the final assessment** - to evaluate your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/questions/theory_ass_05.json", title="Theory section - final assessment", max_questions=6)
        
# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
