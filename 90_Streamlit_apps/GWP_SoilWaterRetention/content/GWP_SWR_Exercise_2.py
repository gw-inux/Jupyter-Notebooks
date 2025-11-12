# Initialize the needed Python packages
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb
import json
from streamlit_book import multiple_choice
from streamlit_scroll_to_top import scroll_to_here
from GWP_SoilWaterRetention_utils import read_md
from GWP_SoilWaterRetention_utils import flip_assessment
from GWP_SoilWaterRetention_utils import render_toggle_container

# --- Track the current page / Scroll to top
PAGE_ID = "EX2"

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
path_quest_ex2_01   = "90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex02_ass_01.json"
path_quest_ex2_02   = "90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex02_ass_02.json"
path_quest_ex2_03   = "90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex02_ass_03.json"
# Load questions
with open(path_quest_ex2_01, "r", encoding="utf-8") as f:
    quest_ex2_01 = json.load(f)
with open(path_quest_ex2_02, "r", encoding="utf-8") as f:
    quest_ex2_02 = json.load(f)
with open(path_quest_ex2_03, "r", encoding="utf-8") as f:
    quest_ex2_03 = json.load(f)
    
# --- Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Rudolf Liedl": [1],
    "Oriol Bertran": [2],
    "Daniel Fernàndez-Garcia": [2],
    "Eileen Poeter": [3]
}
institutions = {
    1: "TU Dresden",
    2: "UPC Universitat Politècnica de Catalunya",
    3: "Colorado School of Mines"
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

st.title('🧪 SWRC Exercise 2')
st.header('Soil Water Retention Curves')
st.subheader(':rainbow-background[SWRC Analysis for Agriculture and Flow]', divider="rainbow")

st.markdown(""" 
            #### 💡 Motivation
            In agricultural and environmental applications, understanding soil hydraulic behavior is essential for effective water management. 
            
            This exercise challenges you to fit the van Genuchten model to real soil retention data and interpret key hydraulic properties.
            
            You will evaluate how field capacity (FC), permanent wilting point (PWP), and relative permeability influence plant water availability and infiltration.
            
            #### 🎯 Learning Objectives  
            After completing this exercise, you will be able to:  
            - Fit van Genuchten parameters $\\theta_r$, $\\theta_s$, $\\alpha$, $m$, and $n$ to observed soil retention data.  
            - Calculate and interpret **PWP**, **FC**, and **effective field capacity (eFC)** for different soils.  
            - Compute and evaluate **relative hydraulic conductivity $k_r$ curves.  
            - Differentiate between soil types based on retention and conductivity characteristics.  
            - Assess implications of SWRC behavior for **agriculture** and **unsaturated flow modeling**.  
""")

# --- INITIAL ASSESSMENT ---
def content_ex2_01():
    st.markdown("""#### Initial assessment""")
    st.info("You can use the initial questions to assess your existing knowledge.")
    
    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_ex2_01[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_ex2_01[i]["options"],
                success=quest_ex2_01[i].get("success", "✅ Correct."),
                error=quest_ex2_01[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_ex2_01[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_ex2_01[i]["options"],
                success=quest_ex2_01[i].get("success", "✅ Correct."),
                error=quest_ex2_01[i].get("error", "❌ Not quite.")
            )

# Render initial assessment
render_toggle_container(
    section_id="ex2_01",
    label="✅ **Show the initial assessment** - to assess wether you are ready for the exercise",
    content_fn=content_ex2_01,
    default_open=False,
)
st.subheader('Exercise - Fitting the model to measured data', divider = 'rainbow')
st.markdown("""  
#### 📌 Tasks  
- Fit the curve to each dataset (Dataset 1–3) and describe the best-fitting soil type (e.g., sand, silt, clay).  
- Estimate and compare the **effective field capacity (eFC)** of the soils.  
- Interpret how **k<sub>r</sub>** changes across the datasets.  
- Which soil is best suited for crop water availability? Which drains the fastest?  

#### 📝 Instructions  
- Use the toggles to select different soil datasets.  
- Adjust the van Genuchten parameters until your model fits the observed data visually.  
- Explore the effect of parameters on PWP, FC, and effective FC.  
- Optionally visualize the relative permeability curve.  
- Use the plots and indicators to answer the questions in the final assessment.
""")


columns = st.columns((1,1,1), gap = 'large')
with columns[0]:
    with st.expander('**Exercise data**'):
        plot1 = st.toggle('Plot Dataset 1')   
        plot2 = st.toggle('Plot Dataset 2')      
        plot3 = st.toggle('Plot Dataset 3')      
with columns[1]:
    with st.expander('**Plot controls**'):
        FKplot  = st.toggle('Show Field Capacity FC')
        PWPplot = st.toggle('Show Permanent Wilting Point PWP')
        plot4   = st.toggle('Plot the relative permeability $k_r$')
with columns[2]:
    with st.expander('**SWRC parameter**'):
        tr    = st.slider('residual water content (-)', 0.01, 0.4, 0.05, 0.01)
        ts    = st.slider('saturated water content (-)', 0.15, 0.7, 0.30, 0.01)   
        alpha = st.slider('alpha (1/cm)', 0.01, 1., 0.1, 0.01)
        n     = st.slider('n (-)', 1.01, 3., 1.2, 0.01)

# given data (retention) - used in exercise

t1=[0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.3,0.33,0.36,0.39,0.42,0.45]
p1=[2230.546345,577.472177,300.4391307,199.8371285,142.8205223,109.6375793,85.19965286,67.18768129,53.82569358,41.8841783,31.92533514,21.62546735,10.23974185]
t2=[0.18,0.19,0.22,0.25,0.28,0.31,0.35,0.4,0.44,0.47,0.51,0.54,0.55]
p2=[50030.534,9000.477,2000.407,900.835,500.023,120.633,60.528,30.189,11.823,7.883,1.514,0.625,0.285]
t3=[0.35,0.37,0.4,0.42,0.44,0.47,0.49,0.5,0.52,0.54,0.55,0.57,0.57]
p3=[350030.55,7800.21,1800.47,940.88,440.03,134.63,56.12,22.11,8.68,4.17,1.94,0.35,0.15]#definition of the function (conductivity)

x_max = 300
    
# intermediate results 
m   = 1-1/n                                         # van Genuchten parameter
PWP = tr + (ts - tr)/(1+(alpha*10**4.2)**n)**m      # permanent wilting point
FC  = tr + (ts - tr)/(1+(alpha*10**1.8)**n)**m      # field capacity
eFC = FC - PWP                                      # effective field capacity

# model output
t_plot  = []                                        # t  = theta = moisture content
p_plot  = []                                        # p  = phi   = suction head
kr_plot = []                                        # kr = rel. permeability
    
for x in range (0, x_max):
    t = tr + (ts-tr)*x/(x_max-1)                    # [-] moisture content; please note that range counts up to x_max-1
    te = (t-tr)/(ts-tr)                             # [-] effective saturation      
    if x == 0:
        p     = 1E18                                # [cm] suction head
        kr    = 0                                   # [-] relative hydraulic conductivity
    else: 
        p     = ((te**(-1/m)-1)**(1/n))/alpha                      
        kr    = np.sqrt(te)*(1-(1-te**(1/m))**m)**2
    t_plot.append(t)
    p_plot.append(p)
    kr_plot.append(kr)
        
    
fig = plt.figure(figsize=(6,4))
ax  = fig.add_subplot()
ax.plot(t_plot, p_plot, 'b', markersize=3, linewidth=3)
ax.vlines(x= tr, ymin=1e-1, ymax=1e+5, colors='b', linewidth=1, linestyle='-.', label = 'residual water content')  
if PWPplot:
    ax.hlines(y= 10**4.2, xmin=0, xmax=PWP, colors='r', linewidth=1)    #upper green line
    ax.vlines(x= PWP, ymin=1e-1, ymax=10**4.2, colors='r',linestyle=':', linewidth=2.0, label = 'Permanent wilting point PWP')
if FKplot:
    ax.hlines(y= 10**1.8, xmin=0, xmax=FC, colors='g', linewidth=1)     #bottom green line
    ax.vlines(x= FC, ymin=1e-1, ymax=10**1.8, colors='g',linestyle='--', linewidth=2.0, label = 'Field capacity FK')
if plot1 == 1:
    ax.plot(t1, p1,'ro', markersize=3)
if plot2 == 1:
    ax.plot(t2, p2,'bo', markersize=3)
if plot3 == 1:
    ax.plot(t3, p3,'go', markersize=3)
ax.set(xlabel='water content [-]', ylabel ='suction head [cm]', xlim = [0, 0.7], ylim = [1e-1,1e+5], yscale = 'log' )
ax.grid(which="both", color='grey',linewidth=0.5)
st.pyplot(fig)

if plot4 == 1:
    fig = plt.figure(figsize=(6,4))
    ax  = fig.add_subplot()
    ax.plot(t_plot, kr_plot, 'b', markersize = 3)
    ax.set(xlabel='water content [-]', ylabel='rel hydraulic conductivity [cm/d]', xlim = [0, 0.7], ylim = [0,1] )
    ax.grid(which="major", color='grey',linewidth=0.5)
    st.pyplot(fig)
    
st.write('Van Genuchten             m:', '{:.5f}'.format(m) )
st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP) )
st.write('Field Capacity           FC:', '{:.2f}'.format(FC) )
st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC) )

with st.expander(':rainbow[**Click here to submit and assess your analysis**]'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/ex02_ass_02.json", title="Exercise 2 – Submit and assess your analysis", max_questions=5)
    
st.subheader('🧾 Conclusion and Final Assessment', divider='rainbow')
st.markdown("""  
This exercise guided you through fitting the van Genuchten retention model to real data from different soils.  
By analyzing the resulting curves and indicators (PWP, FC, eFC, k<sub>r</sub>), you explored how hydraulic properties affect plant-available water and soil behavior.  

Such analyses are fundamental for irrigation planning, land evaluation, and understanding unsaturated flow in the vadose zone.  
""", unsafe_allow_html=True)

# --- FINAL ASSESSMENT ---
def content_ex2_03():
    st.markdown("""#### Final assessment""")
    st.info("You can use the final questions to assess your learning success.")
    
    # Render questions in a 2x2 grid (row-wise, aligned)
    for row in [(0, 1), (2, 3)]:
        col1, col2 = st.columns(2)
    
        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_ex2_03[i]['question']}**")
            multiple_choice(
                question=" ",  # suppress repeated question display
                options_dict=quest_ex2_03[i]["options"],
                success=quest_ex2_03[i].get("success", "✅ Correct."),
                error=quest_ex2_03[i].get("error", "❌ Not quite.")
            )
    
        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_ex2_03[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_ex2_03[i]["options"],
                success=quest_ex2_03[i].get("success", "✅ Correct."),
                error=quest_ex2_03[i].get("error", "❌ Not quite.")
            )

# Render initial assessment
render_toggle_container(
    section_id="ex2_03",
    label="✅ **Show the final assessment** - to assess your learning success",
    content_fn=content_ex2_03,
    default_open=False,
)
          
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')