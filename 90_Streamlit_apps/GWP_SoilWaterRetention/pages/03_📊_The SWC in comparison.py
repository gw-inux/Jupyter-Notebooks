# Initialize the needed Python packages
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb
import json
from streamlit_book import multiple_choice

st.title('📊 The SWC in comparison')
st.header('Soil Water Retention characteristics')
st.subheader(':green-background[Comparison of datasets]', divider="green")

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Oriol Bertran": [2],
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
    2: "UPC Universitat Politècnica de Catalunya",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

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
            #### 💡 Motivation for comparing Soil Water Retention Curves
            
            Different soil textures exhibit distinct water retention behaviors, which influence agricultural productivity, drainage, and plant-available water. In this section, you will compare soil water retention characteristics (SWRCs) for two soil types side-by-side using real or synthetic data. Understanding these differences helps you make informed decisions in land management, irrigation design, and soil classification.
            
            Key questions to consider:
            - How do field capacity and wilting point differ across soils?
            - Which soils retain more water in the plant-available range?
            - How do changes in van Genuchten parameters shape the retention curve?.
            
            #### 🎯 Learning Objectives
            After completing this interactive section of the module, you will be able to:
            - Interpret differences in SWRCs between soil textures based on van Genuchten parameters.
            - Compare field capacity (FC), permanent wilting point (PWP), and effective field capacity (eFC) between two datasets.
            - Assess how changes in α and n influence the shape and steepness of retention curves.
            - Analyze and compare relative hydraulic conductivity curves derived from SWRCs.
            """     
)
with st.expander('🧠 **Show some questions for self-assessment** - to assess your initial understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/comparison_ass_01.json", title="Initial assessment")

st.subheader('Available data sets', divider = 'green')
st.markdown("""
            The interactive plot allows to compare different data sets. Various data sets are available.
            """
)

with st.expander('**Click here if you want to see the available data sets**'):
    st.markdown('''
                The interactive plot allows to compare different data sets. Various data sets are available.
                
                This table shows the available data sets. You can choose the data sets with the dropdown menu in the following interactive plot.
                
                The data for the various soil types originate from Carsel and Parrish (1988):
                    
                | Soil texture       | θ_r   | θ_s   | α (cm⁻¹) | n    | K_s (cm per day) |
                |--------------------|-------|-------|----------|------|-------------------|
                | sand               | 0.045 | 0.43  | 0.145    | 2.68 | 712.8            |
                | loamy sand         | 0.057 | 0.41  | 0.124    | 2.28 | 350.2            |
                | sandy loam         | 0.065 | 0.41  | 0.075    | 1.89 | 106.1            |
                | loam               | 0.078 | 0.43  | 0.036    | 1.56 | 24.96            |
                | silt               | 0.034 | 0.46  | 0.016    | 1.37 | 6.00             |
                | silt loam          | 0.067 | 0.45  | 0.020    | 1.41 | 10.80            |
                | sandy clay loam    | 0.100 | 0.39  | 0.059    | 1.48 | 31.44            |
                | clay loam          | 0.095 | 0.41  | 0.019    | 1.31 | 6.24             |
                | silty clay loam    | 0.089 | 0.43  | 0.010    | 1.23 | 1.68             |
                | sandy clay         | 0.100 | 0.38  | 0.027    | 1.23 | 2.88             |
                | silty clay         | 0.070 | 0.36  | 0.005    | 1.09 | 0.48             |
                | clay               | 0.068 | 0.38  | 0.008    | 1.09 | 4.80             |
                '''
    )

# Dictionary with soil data
soil_profiles = {
"1) Sand": {"θr": 0.045, "θs": 0.43, "α": 0.145, "n": 2.68, "Ks": 712.8, "color": "gold"},
"2) Loamy Sand": {"θr": 0.057, "θs": 0.41, "α": 0.124, "n": 2.28, "Ks": 350.2, "color": "orange"},
"3) Sandy Loam": {"θr": 0.065, "θs": 0.41, "α": 0.075, "n": 1.89, "Ks": 106.1, "color": "sandybrown"},
"4) Loam": {"θr": 0.078, "θs": 0.43, "α": 0.036, "n": 1.56, "Ks": 24.96, "color": "black"},
"5) Silt": {"θr": 0.034, "θs": 0.46, "α": 0.016, "n": 1.37, "Ks": 6.00, "color": "darkgray"},
"6) Silt Loam": {"θr": 0.067, "θs": 0.45, "α": 0.020, "n": 1.41, "Ks": 10.80, "color": "dimgray"},
"7) Sandy Clay Loam": {"θr": 0.100, "θs": 0.39, "α": 0.059, "n": 1.48, "Ks": 31.44, "color": "chocolate"},
"8) Clay Loam": {"θr": 0.095, "θs": 0.41, "α": 0.019, "n": 1.31, "Ks": 6.24, "color": "brown"},
"9) Silty Clay Loam": {"θr": 0.089, "θs": 0.43, "α": 0.010, "n": 1.23, "Ks": 1.68, "color": "slategray"},
"10) Sandy Clay": {"θr": 0.100, "θs": 0.38, "α": 0.027, "n": 1.23, "Ks": 2.88, "color": "peru"},
"11) Silty Clay": {"θr": 0.070, "θs": 0.36, "α": 0.005, "n": 1.09, "Ks": 0.48, "color": "cadetblue"},
"12) Clay": {"θr": 0.068, "θs": 0.38, "α": 0.008, "n": 1.09, "Ks": 4.80, "color": "darkred"},
"13) Synthetic DS1": {"θr": 0.060, "θs": 0.45, "α": 0.320, "n": 1.35, "Ks": 100.0, "color": "darkblue"},
"14) Synthetic DS2": {"θr": 0.070, "θs": 0.48, "α": 0.220, "n": 1.15, "Ks": 100.0, "color": "crimson"}
}

st.subheader('📊 Interactive plot to compare Soil Water Retention Curves for different media', divider = 'green')
st.markdown("""
            The interactive plot allows to compare different data sets. Various data sets are available.
            """
)
with st.expander("**Click here for instructions about how to work with this interactive tool**"):
    st.markdown("""
        #### 🛠️ Instructions How to Use the Interactive Plot 
        - Select two different datasets for comparison using the dropdowns. You can also define your own parameter values.
        - Toggle the plot options to show Field Capacity (FC), Permanent Wilting Point (PWP), and Relative Permeability.
        - Observe how the two soil types behave differently in terms of water retention and desaturation patterns.
        - Compare the computed FC, PWP, and effective field capacity (eFC) values shown below the plot.
        - Reflect on how parameter differences relate to real-world soil texture and functionality.
    """
)

columns = st.columns((1,1,1), gap = 'large')
with columns[0]:
    st.write('**Dataset 1 - Input**')
    user1 = st.toggle('User defined data for plot 1?')
    if user1:
        tr1    = st.slider('residual water content 1 (-)', 0.01, 0.4, 0.04, 0.01)
        ts1    = st.slider('saturated water content 1 (-)', 0.15, 0.7, 0.30, 0.01)
        alpha1 = st.slider('alpha 1 (1/cm)', 0.01, 1., 0.1, 0.01)
        n1     = st.slider('n 1 (-)', 1.01, 3., 1.2, 0.01)
        color1 = 'green'
        label1 = f"Dataset 1: User defined"  
    else:    
        soil_options = list(soil_profiles.keys())
        data1 = st.selectbox("Select Dataset 1", soil_options, key='Data1')    
        params1 = soil_profiles[data1]
        tr1 = params1["θr"]
        ts1 = params1["θs"]
        alpha1 = params1["α"]
        n1 = params1["n"]
        color1 = params1["color"]
        label1 = f"Dataset 1: {data1}"        
      
with columns[1]:
    st.write('**Dataset 2 - Input**')
    user2 = st.toggle('User defined data for plot 2?')
    if user2:
        tr2    = st.slider('residual water content 2 (-)', 0.01, 0.4, 0.06, 0.01)
        ts2    = st.slider('saturated water content 2 (-)', 0.15, 0.7, 0.35, 0.01)
        alpha2 = st.slider('alpha 2 (1/cm)', 0.01, 1., 0.2, 0.01)
        n2     = st.slider('n 2 (-)', 1.01, 3., 1.3, 0.01)
        color2 = 'red'
        label2 = f"Dataset 2: User defined"  
    else:
        soil_options = list(soil_profiles.keys())
        data2 = st.selectbox("Select Dataset 2", soil_options, key='Data2')     
        params2 = soil_profiles[data2]
        tr2 = params2["θr"]
        ts2 = params2["θs"]
        alpha2 = params2["α"]
        n2 = params2["n"]
        color2 = params2["color"]
        label2 = f"Dataset 2: {data2}"

with columns[2]:
    with st.expander('**Plot controls**'):
        FKplot  = st.toggle('Show Field Capacity FC')
        PWPplot = st.toggle('Show Permanent Wilting Point PWP')
        plot4   = st.toggle('Plot the relative permeability $k_r$')
# given data (retention) - used in exercise

x_max = 300
    
# intermediate results 
m1   = 1-1/n1                                              # van Genuchten parameter
PWP1 = tr1 + (ts1 - tr1)/(1+(alpha1*10**4.2)**n1)**m1      # permanent wilting point
FC1  = tr1 + (ts1 - tr1)/(1+(alpha1*10**1.8)**n1)**m1      # field capacity
eFC1 = FC1 - PWP1                                          # effective field capacity

m2   = 1-1/n2                                         # van Genuchten parameter
PWP2 = tr2 + (ts2 - tr2)/(1+(alpha2*10**4.2)**n2)**m2      # permanent wilting point
FC2  = tr2 + (ts2 - tr2)/(1+(alpha2*10**1.8)**n2)**m2      # field capacity
eFC2 = FC2 - PWP2                                      # effective field capacity

# model output
t_plot1  = []                                        # t  = theta = moisture content
p_plot1  = []                                        # p  = phi   = suction head
kr_plot1 = []                                        # kr = rel. permeability

# model output
t_plot2  = []                                        # t  = theta = moisture content
p_plot2  = []                                        # p  = phi   = suction head
kr_plot2 = []                                        # kr = rel. permeability
    
for x in range (0, x_max):
    t1 = tr1 + (ts1-tr1)*x/(x_max-1)                 # [-] moisture content; please note that range counts up to x_max-1
    t2 = tr2 + (ts2-tr2)*x/(x_max-1)                 # [-] moisture content; please note that range counts up to x_max-1
    te1 = (t1-tr1)/(ts1-tr1)                         # [-] effective saturation      
    te2 = (t2-tr2)/(ts2-tr2)                         # [-] effective saturation
    if x == 0:
        p1     = 1E18                                # [cm] suction head
        p2     = 1E18
        kr1    = 0                                   # [-] relative hydraulic conductivity
        kr2    = 0
    else: 
        p1     = ((te1**(-1/m1)-1)**(1/n1))/alpha1                      
        p2     = ((te2**(-1/m2)-1)**(1/n2))/alpha2
        kr1    = np.sqrt(te1)*(1-(1-te1**(1/m1))**m1)**2
        kr2    = np.sqrt(te2)*(1-(1-te2**(1/m2))**m2)**2
    t_plot1.append(t1)
    p_plot1.append(p1)
    kr_plot1.append(kr1)
    t_plot2.append(t2)
    p_plot2.append(p2)
    kr_plot2.append(kr2)
    
fig = plt.figure(figsize=(9,6))
ax  = fig.add_subplot()
ax.plot(t_plot1, p_plot1, color=color1, markersize=3, label=label1, linewidth=3)
ax.plot(t_plot2, p_plot2, color=color2, markersize=3, label=label2, linewidth=3)
ax.vlines(x= tr1, ymin=1e-1, ymax=1e+5, color=color1, linewidth=1, label = 'residual water content DS1')   
ax.vlines(x= tr2, ymin=1e-1, ymax=1e+5, color=color2, linewidth=1, label = 'residual water content DS2')     
if PWPplot:
    ax.hlines(y= 10**4.2, xmin=0, xmax=PWP1, colors='r')    #upper green line
    ax.vlines(x= PWP1, ymin=1e-1, ymax=10**4.2, color=color1,linestyle=':', linewidth=2.0, label = 'Permanent wilting point PWP DS1')
    ax.hlines(y= 10**4.2, xmin=0, xmax=PWP2, colors='r')    #upper green line
    ax.vlines(x= PWP2, ymin=1e-1, ymax=10**4.2, color=color2,linestyle=':', linewidth=2.0, label = 'Permanent wilting point PWP DS2')
if FKplot:
    ax.hlines(y= 10**1.8, xmin=0, xmax=FC1, colors='g')     #bottom green line
    ax.vlines(x= FC1, ymin=1e-1, ymax=10**1.8, color=color1,linestyle='--', linewidth=2.0, label = 'Field capacity FK DS1')
    ax.hlines(y= 10**1.8, xmin=0, xmax=FC2, colors='g')     #bottom green line
    ax.vlines(x= FC2, ymin=1e-1, ymax=10**1.8, color=color2,linestyle='--', linewidth=2.0, label = 'Field capacity FK DS2')

ax.set(xlabel='water content [-]', ylabel ='suction head [cm]', xlim = [0, 0.7], ylim = [1e-1,1e+5], yscale = 'log' )
ax.grid(which="both", color='grey',linewidth=0.5)
plt.legend()
st.pyplot(fig)

with st.expander('**Click here to see the used data sets**'):
    
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        st.write('**Dataset 1**')
        st.write('Van Genuchten             m:', '{:.5f}'.format(m1) )
        st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP1) )
        st.write('Field Capacity           FC:', '{:.2f}'.format(FC1) )
        st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC1) )
 
    with columns2[1]:
        st.write('**Dataset 2**')
        st.write('Van Genuchten             m:', '{:.5f}'.format(m2) )
        st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP2) )
        st.write('Field Capacity           FC:', '{:.2f}'.format(FC2) )
        st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC2) )

if plot4:
    fig = plt.figure(figsize=(9,6))
    ax  = fig.add_subplot()
    ax.plot(t_plot1, kr_plot1, color=color1, markersize=3, label=label1)
    ax.plot(t_plot2, kr_plot2, color=color2, markersize=3, label=label2)
    ax.set(xlabel='water content [-]', ylabel='rel hydraulic conductivity [cm/d]', xlim = [0, 0.7], ylim = [0,1] )
    ax.grid(which="major", color='grey',linewidth=0.5)
    plt.legend()
    st.pyplot(fig)
    
st.subheader('🧾 Conclusion and Final Assessment', divider='green')
st.markdown("""
    This section allowed you to visually explore how soil texture and van Genuchten parameters influence soil water retention. By comparing two datasets side-by-side, you gained deeper insight into differences in water availability, retention dynamics, and hydraulic behavior across soils. Such comparisons are essential when selecting appropriate soil models for hydrologic, agricultural, or ecological applications.
    """
)
with st.expander('🧠 **Show questions for the final assessment** - to assess your learning success'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/comparison_ass_02.json", title="Final assessment", max_questions=6)
"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/02_📈_▶️ The SWC interactive.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/04_📈_▶️ SWC_Exercise_1.py")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
