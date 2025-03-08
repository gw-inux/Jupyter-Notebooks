# Initialize the needed Python packages
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb

st.title('Soil Water Retention characteristics')

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

# Initial assessment

columnsQ1 = st.columns((1,1), gap = 'large')

with columnsQ1[0]:
    stb.single_choice(":red[**How is saturation defined?**]",
                  ["Total volume divided by water volume.", "Pore volume divided by water volume.", "Volume of solids divided by water volume.",
                  "Water volume divided by Pore volume."],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about saturation _S_ in the following ressources _reference to GWP books...')
    stb.single_choice(":red[**Question2?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
                  
with columnsQ1[1]:
    stb.single_choice(":red[**Question3?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')             
    stb.single_choice(":red[**Question4?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
"---"
st.markdown("""
            ### Computation of the soil water retention
            Subsequently, the Soil Water Retention is computed with Python routines. The interactive plot demonstrate the response of the soil water retention behavior on parameter changes.            
            
            """     
)

columns = st.columns((1,1), gap = 'large')
with columns[0]:
    tr    = st.slider('residual water content (-)', 0.01, 0.4, 0.05, 0.01)
    ts    = st.slider('saturated water content (-)', 0.15, 0.7, 0.30, 0.01)   
with columns[1]:
    alpha = st.slider('alpha (1/cm)', 0.01, 1., 0.1, 0.01)
    n     = st.slider('n (-)', 1.01, 3., 1.2, 0.01)
  
plot4 = st.toggle('Plot k_r 1')


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
        
fig = plt.figure(figsize=(9,6))
ax  = fig.add_subplot()
ax.plot(t_plot, p_plot, 'r', markersize=3)
ax.vlines(x= tr, ymin=1e-1, ymax=1e+5, linestyle='--')      
ax.hlines(y= 10**4.2, xmin=0, xmax=PWP, colors='g')    #upper green line
ax.vlines(x= PWP, ymin=1e-1, ymax=10**4.2, colors='g')
ax.hlines(y= 10**1.8, xmin=0, xmax=FC, colors='b')     #bottom green line
ax.vlines(x= FC, ymin=1e-1, ymax=10**1.8, colors='b')
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