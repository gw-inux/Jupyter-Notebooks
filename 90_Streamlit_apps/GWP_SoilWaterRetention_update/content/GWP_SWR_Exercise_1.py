#-- Check and install required packages if not already installed --#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb
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
PAGE_ID = "EX1"

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

# --- LOAD QUESTIONS
path_quest_ex1_01   = "90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex01_ass_01.json"
path_quest_ex1_02   = "90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex01_ass_02.json"
path_quest_ex1_03   = "90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex01_ass_03.json"
# Load questions
with open(path_quest_ex1_01, "r", encoding="utf-8") as f:
    quest_ex1_01 = json.load(f)
with open(path_quest_ex1_02, "r", encoding="utf-8") as f:
    quest_ex1_02 = json.load(f)
with open(path_quest_ex1_03, "r", encoding="utf-8") as f:
    quest_ex1_03 = json.load(f)

# Authors, institutions, and year
year = 2026
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

# --- FUNCTIONS
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

def dimensionless_water_content(t, tr, ts):
    """Function that calculates the dimensionless water content. 
    Based on van Genuchten, 1980 (Eq. 2) 
    Parameters
    ----------
    t : float
        soil-water content
    tr : float
        residual values of soil-water content
    ts : float
        saturated values of soil-water content
    Returns
    -------
    float
        dimensionless water content
    """ 
    T_dim = (t - tr)/(ts - tr)      
    return T_dim

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

st.title(
    ui_text(
        "🧪 SWRC Exercise 1",
        de="🧪 SWRC-Übung 1",
        it="🧪 Esercizio SWRC 1",
        es="🧪 Ejercicio SWRC 1",
        pt="🧪 Exercício SWRC 1",
        fr="🧪 Exercice SWRC 1",
        zh="🧪 SWRC 练习 1",
    )
)

st.header(
    ui_text(
        "Soil Water Retention Curves",
        de="Bodenwasserretentionskurven (SWRC)",
        it="Curve di ritenzione idrica del suolo (SWRC)",
        es="Curvas de retención de agua en el suelo (SWRC)",
        pt="Curvas de retenção de água no solo (SWRC)",
        fr="Courbes de rétention d'eau dans le sol (SWRC)",
        zh="土壤水分保持曲线 (SWRC)",
    )
)

st.subheader(
    ":violet-background[" +
    ui_text(
        "Fitting Model Parameters to Measured Data",
        de="Anpassung der Modellparameter an Messdaten",
        it="Adattamento dei parametri del modello ai dati misurati",
        es="Ajuste de los parámetros del modelo a los datos medidos",
        pt="Ajuste dos parâmetros do modelo aos dados medidos",
        fr="Ajustement des paramètres du modèle aux données mesurées",
        zh="将模型参数拟合到实测数据",
    ) +
    "]",
    divider="violet",
)

st.markdown(load_md(MD_DIR, "swr_ex1_01.md", st.session_state.language))
    
# --- INITIAL ASSESSMENT ---
def content_ex1_01():
    st.markdown("""#### Initial assessment""")
    st.info("You can use the initial questions to assess your existing knowledge.")
    
    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_ex1_01[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_ex1_01[i]["options"],
                success=quest_ex1_01[i].get("success", "✅ Correct."),
                error=quest_ex1_01[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_ex1_01[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_ex1_01[i]["options"],
                success=quest_ex1_01[i].get("success", "✅ Correct."),
                error=quest_ex1_01[i].get("error", "❌ Not quite.")
            )

# Render initial assessment
render_toggle_container(
    section_id="ex1_01",
    label="✅ **Show the initial assessment** - to assess wether you are ready for the exercise",
    content_fn=content_ex1_01,
    default_open=False,
)

#
# Example for retention curves - Interactive plots
#

#-----------------------------------#
# From the table to a dataframe     #
#-----------------------------------#

#-- Soil 1 --#
Soil1 = pd.DataFrame()
Soil1["Suction Pressure [hPa]"] = [1, 2, 3, 4, 8, 12, 17, 23, 32, 46, 65, 98, 148, 328, 726, 1217, 
                                      2175, 4330, 7576, 16796, 41464, 95973]
Soil1["Water Content"] = [0.368, 0.365, 0.358, 0.348, 0.321, 0.293, 0.267, 0.240, 0.213, 0.185, 0.160, 
                             0.137, 0.119, 0.090, 0.074, 0.065, 0.059, 0.054, 0.051, 0.048, 0.046, 0.045]

#-- Silt Soil --#
Soil2 = pd.DataFrame()
Soil2["Suction Pressure [hPa]"] = [1, 2, 6, 25, 49, 118, 235, 354, 488, 765, 1033, 1456, 2656, 4351, 
                                      6830, 13582, 26438, 45248, 98112, 199482, 396999, 958958]
Soil2["Water Content"] = [0.422, 0.422, 0.421, 0.417, 0.412, 0.395, 0.366, 0.342, 0.319, 0.285, 0.260, 
                             0.236, 0.195, 0.167, 0.143, 0.113, 0.089, 0.074, 0.057, 0.045, 0.035, 0.026]


#-----------------------------------#
# Resolution and plot               # 
#-----------------------------------#
st.subheader(
    ui_text(
        "Exercise – Fitting the Model to Measured Data",
        de="Übung – Anpassung des Modells an Messdaten",
        it="Esercizio – Adattamento del modello ai dati misurati",
        es="Ejercicio – Ajuste del modelo a los datos medidos",
        pt="Exercício – Ajuste do modelo aos dados medidos",
        fr="Exercice – Ajustement du modèle aux données mesurées",
        zh="练习——将模型拟合到实测数据",
    ),
    divider="violet",
)
st.markdown(load_md(MD_DIR, "swr_ex1_02.md", st.session_state.language))

data = {
        "Soil 1 |ψ| [hPa]": [1, 2, 3, 4, 8, 12, 17, 23, 32, 46, 65, 98, 148, 328, 726, 1217, 2175, 4330, 7576, 16796, 41464, 95973],
        "θ (Sand)": [0.368, 0.365, 0.358, 0.348, 0.321, 0.293, 0.267, 0.240, 0.213, 0.185, 0.160, 0.137, 0.119, 0.090, 0.074, 0.065, 0.059, 0.054, 0.051, 0.048, 0.046, 0.045],
        "Soil 2 |ψ| [hPa]": [1, 2, 6, 25, 49, 118, 235, 354, 488, 765, 1033, 1456, 2656, 4351, 6830, 13582, 26438, 45248, 98112, 199482, 396999, 958958],
        "θ (Silt)": [0.422, 0.422, 0.421, 0.417, 0.412, 0.395, 0.366, 0.342, 0.319, 0.285, 0.260, 0.236, 0.195, 0.167, 0.143, 0.113, 0.089, 0.074, 0.057, 0.045, 0.035, 0.026]
        }

# Convert to DataFrame
df = pd.DataFrame(data)

with st.expander('Click here if you want to see the table with the measurements'):
    # Display the table with markdown
    st.dataframe(df, hide_index=True, use_container_width=True)
    #st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

st.markdown(load_md(MD_DIR, "swr_ex1_03.md", st.session_state.language))

columns_i1 = st.columns((1,1), gap = 'large')

# with columns_i1[0]:
#     tr_soil1 = st.slider(f':green-background[θr soil1]',0.0,0.5,0.2,0.001)
#     ts_soil1 = st.slider(f':green-background[θs soil1]',0.0,0.5,0.2,0.001)
#     alpha_soil1 = st.slider(f':green-background[α soil1]',0.0,0.1,0.05,0.0001)
#     n_soil1 = st.slider(f':green-background[n soil1]',0.0,5.0,2.5,0.05)

# with columns_i1[1]:
#     tr_soil2 = st.slider(f':blue-background[θr soil2]',0.0,0.5,0.3,0.001)
#     ts_soil2 = st.slider(f':blue-background[θs soil2]',0.0,0.5,0.3,0.001)
#     alpha_soil2 = st.slider(f':blue-background[α soil2]',0.0,0.1,0.05,0.0001)
#     n_soil2 = st.slider(f':blue-background[n soil2]',0.0,5.0,2.5,0.05)   

with columns_i1[0]:
    tr_soil1 = st.slider(
        ':green-background[θr soil1]', min_value=0.0, max_value=0.5, value=0.2, step=0.001, format="%.3f"
    )
    ts_soil1 = st.slider(
        ':green-background[θs soil1]', min_value=0.0, max_value=0.5, value=0.2, step=0.001, format="%.3f"
    )
    alpha_soil1 = st.slider(
        ':green-background[α soil1]', min_value=0.0, max_value=0.1, value=0.05, step=0.0001, format="%.4f"
    )
    n_soil1 = st.slider(
        ':green-background[n soil1]', min_value=0.0, max_value=5.0, value=2.5, step=0.05, format="%.2f"
    )

with columns_i1[1]:
    tr_soil2 = st.slider(
        ':blue-background[θr soil2]', min_value=0.0, max_value=0.5, value=0.3, step=0.001, format="%.3f"
    )
    ts_soil2 = st.slider(
        ':blue-background[θs soil2]', min_value=0.0, max_value=0.5, value=0.3, step=0.001, format="%.3f"
    )
    alpha_soil2 = st.slider(
        ':blue-background[α soil2]', min_value=0.0, max_value=0.1, value=0.05, step=0.0001, format="%.4f"
    )
    n_soil2 = st.slider(
        ':blue-background[n soil2]', min_value=0.0, max_value=5.0, value=2.5, step=0.05, format="%.2f"
    )


#-- Generating the range of head values
h_values = np.logspace(0, 6, 100)
      
#-- Calculating the soil-water content for both soild
t_soil1 = [soil_water_content(tr_soil1, ts_soil1, alpha_soil1, h, n_soil1) for h in h_values]
t_soil2 = [soil_water_content(tr_soil2, ts_soil2, alpha_soil2, h, n_soil2) for h in h_values]
    
#-- Plotting the results
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(Soil1["Water Content"], Soil1["Suction Pressure [hPa]"], 'o', mfc='none', 
        c="green", label="Observations Soil 1")
ax.plot(Soil2["Water Content"], Soil2["Suction Pressure [hPa]"], 'o', mfc='none',
        c="blue", label="Observations Soil 2")   
ax.plot(t_soil1, h_values, 
        c="green", label="Model Soil 1")
ax.plot(t_soil2, h_values, 
        c="blue", label="Model Soil 2")
ax.set_xlim(0, 0.5)
ax.set_ylim(1, 1000000)
ax.set_yscale('log')
ax.set_xlabel(r'Water Content, $\Theta$')
ax.set_ylabel('Suction Pressure [hPa]')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig.tight_layout()
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
st.pyplot(fig)

with st.expander(':violet[**Click here to submit and assess your analysis**]'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex01_ass_02.json", title="Exercise 1 – Submit and assess your analysis")

st.subheader(
    ui_text(
        "🧾 Conclusion and Final Assessment",
        de="🧾 Zusammenfassung und Abschließende Wissensüberprüfung",
        it="🧾 Conclusioni e valutazione finale",
        es="🧾 Conclusión y evaluación final",
        pt="🧾 Conclusão e avaliação final",
        fr="🧾 Conclusion et évaluation finale",
        zh="🧾 总结与最终测评",
    ),
    divider="violet",
)

st.markdown(load_md(MD_DIR, "swr_ex1_04.md", st.session_state.language))

# --- FINAL ASSESSMENT ---
def content_ex1_03():
    st.markdown("""#### Final assessment""")
    st.info("You can use these final questions to assess your learning success.")
    
    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_ex1_03[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_ex1_03[i]["options"],
                success=quest_ex1_03[i].get("success", "✅ Correct."),
                error=quest_ex1_03[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_ex1_03[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_ex1_03[i]["options"],
                success=quest_ex1_03[i].get("success", "✅ Correct."),
                error=quest_ex1_03[i].get("error", "❌ Not quite.")
            )

# Render initial assessment
render_toggle_container(
    section_id="ex1_03",
    label="✅ **Show the final assessment** - to assess your learning success",
    content_fn=content_ex1_03,
    default_open=False,
)

"---"
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
