# Initialize the needed Python packages
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb

st.title('📈 The SWC interactive')
st.header('Soil Water Retention characteristics')
st.subheader(':red-background[Understanding the soil water retention curve]', divider="red")

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Rudolf Liedl": [1],
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
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
            #### Motivation
            """     
)
st.subheader('Interactive plot of the Soil Water Retention Curve', divider = 'red')

st.markdown("""
            ### Computation of the soil water retention
            Subsequently, the Soil Water Retention is computed with Python routines. The interactive plot demonstrate the response of the soil water retention behavior on parameter changes.            
            
            """     
)

# Input data
columns = st.columns((1,3))
with columns[0]:
    with st.expander('**SWRC parameter**'):
        tr    = st.slider('residual water content (-)', 0.01, 0.4, 0.05, 0.01)
        ts    = st.slider('saturated water content (-)', 0.15, 0.7, 0.30, 0.01)   
        alpha = st.slider('alpha (1/cm)', 0.01, 1., 0.1, 0.01)
        n     = st.slider('n (-)', 1.01, 3., 1.2, 0.01)
    with st.expander('**Plot controls**'):
        FKplot  = st.toggle('Show Field Capacity FC')
        PWPplot = st.toggle('Show Permanent Wilting Point PWP')
        plot4   = st.toggle('Plot the relative permeability $k_r$')
  
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
        
fig = plt.figure(figsize=(6,5))
ax  = fig.add_subplot()
ax.plot(t_plot, p_plot, 'b', markersize=3, linewidth=3)
ax.vlines(x= tr, ymin=1e-1, ymax=1e+5, colors='b', linewidth=1, linestyle='-.', label = 'residual water content')      
if PWPplot:
    ax.hlines(y= 10**4.2, xmin=0, xmax=PWP, colors='r', linewidth=1)    #upper green line
    ax.vlines(x= PWP, ymin=1e-1, ymax=10**4.2, colors='r',linestyle=':', linewidth=2.0, label = 'Permanent wilting point PWP')
if FKplot:
    ax.hlines(y= 10**1.8, xmin=0, xmax=FC, colors='g', linewidth=1)     #bottom green line
    ax.vlines(x= FC, ymin=1e-1, ymax=10**1.8, colors='g',linestyle='--', linewidth=2.0, label = 'Field capacity FK')
ax.set(xlabel='water content [-]', ylabel ='suction head [cm]', xlim = [0, 0.7], ylim = [1e-1,1e+5], yscale = 'log' )
ax.grid(which="both", color='grey',linewidth=0.5)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.1), borderaxespad=0, ncol=1, frameon=False, fontsize = 12)   

    
with columns[1]:
    st.pyplot(fig)

with st.expander('**Click here to see the computed data**'):
    st.write('Van Genuchten             m:', '{:.5f}'.format(m) )
    st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP) )
    st.write('Field Capacity           FC:', '{:.2f}'.format(FC) )
    st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC) ) 

if plot4:
    fig = plt.figure(figsize=(6,5))
    ax  = fig.add_subplot()
    ax.plot(t_plot, kr_plot, 'b', markersize = 3)
    ax.set(xlabel='water content [-]', ylabel='rel hydraulic conductivity [-]', xlim = [0, 0.7], ylim = [0,1] )
    ax.grid(which="major", color='grey',linewidth=0.5)
    with columns[1]:
        st.pyplot(fig)

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/02_📈_▶️ Transient_Flow to a Well.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/03_📈_▶️ The SWC in comparison.py")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')