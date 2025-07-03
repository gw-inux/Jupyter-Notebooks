#-- Check and install required packages if not already installed --#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb
import json
from streamlit_book import multiple_choice

st.title('🧪 SWC Exercise 1')
st.header('Soil Water Retention Curves')
st.subheader(':violet-background[Fitting Model Parameters to measured data]', divider="violet")

# Authors, institutions, and year
year = 2025 
authors = {
    "Oriol Bertran": [1],  # Author 1 belongs to Institution 1
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "UPC Universitat Politècnica de Catalunya",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

# FUNCTIONS
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

st.markdown(""" 
            #### 💡 Motivation
            - How can we describe real soil water retention behavior using a mathematical model?
            - Which van Genuchten parameters best fit the observed retention characteristics of a given soil?
            
            In this exercise, you are given measured retention data for a soil sample. Your task is to adjust the van Genuchten parameters (θr, θs, α, and n) to visually fit the model curve to the data points. This hands-on exploration helps you understand the role of each parameter and develop practical skills in interpreting and calibrating soil water retention models.
            
            #### 🎯 Learning Objectives
            After completing this exercise, learners will be able to:
            - Interpret observed soil water retention data and understand its structure (water content θ vs. pressure head).
            - Apply the van Genuchten model to simulate soil water retention behavior.
            - Calibrate van Genuchten parameters (θr, θs, α, n) visually based on measurement data.
            - Analyze how different parameters influence the shape and fit of the retention curve.
"""
)
with st.expander('🧠 **Click here for some initial questions** - to assess wether you are ready for the exercise'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex01_ass_01.json", title="Exercise 1 – Initial assessment")
    

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
st.subheader('Exercise - Fitting the model to measured data', divider = 'violet')
st.markdown(
            """
            **Your task**: Given the suction pressure and water content data for two soil types—sand and silt—determine the best-fitting parameters.
            """
)

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
    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

st.markdown(
            """
            #### Parameters
            - *θr* : Residual soil-water content of the soil
            - *θs* : Satured soil-water content of the soil
            - *α* : alpha parameter, related to the inverse of the air entry suction
            - *n* : n parameter, is a mesure of the pore-size distribution
            """
)

columns_i1 = st.columns((1,1), gap = 'large')

with columns_i1[0]:
    tr_soil1 = st.slider(f':green-background[θr soil1]',0.0,0.5,0.2,0.001)
    ts_soil1 = st.slider(f':green-background[θs soil1]',0.0,0.5,0.2,0.001)
    alpha_soil1 = st.slider(f':green-background[α soil1]',0.0,0.1,0.05,0.0001)
    n_soil1 = st.slider(f':green-background[n soil1]',0.0,5.0,2.5,0.05)

with columns_i1[1]:
    tr_soil2 = st.slider(f':blue-background[θr soil2]',0.0,0.5,0.3,0.001)
    ts_soil2 = st.slider(f':blue-background[θs soil2]',0.0,0.5,0.3,0.001)
    alpha_soil2 = st.slider(f':blue-background[α soil2]',0.0,0.1,0.05,0.0001)
    n_soil2 = st.slider(f':blue-background[n soil2]',0.0,5.0,2.5,0.05)   

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

st.subheader('🧾 Conclusion and Final Assessment', divider='violet')
st.markdown("""  
In this exercise, you explored how to fit van Genuchten model parameters to measured soil retention data for two contrasting soils. By adjusting the parameters θ<sub>r</sub>, θ<sub>s</sub>, α, and n, you gained insight into how each one affects the shape and steepness of the soil water retention curve.

You also developed hands-on calibration skills and visually assessed the model fit—a fundamental task in soil physics and unsaturated zone hydrology.

Keep in mind that real-world fitting often involves optimization techniques, but this exercise builds the essential intuition needed to understand how retention behavior varies across soil types.
""", unsafe_allow_html=True)

with st.expander('🧠 **Click here for some final questions** - to assess your learning success'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex01_ass_03.json", title="Exercise 1 – Final assessment")

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/03_📈_▶️ The SWC in comparison.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/05_📈_▶️ SWC_Exercise_2.py")
   
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
