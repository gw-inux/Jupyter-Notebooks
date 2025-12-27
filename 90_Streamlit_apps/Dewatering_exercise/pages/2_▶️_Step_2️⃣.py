# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stodo import to_do

# ToDo:
#    - number input
#    - log slider
#    - revise UI

# Authors, institutions, and year
year = 2025 
authors = {
    "Ty Ferré": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "University of Arizona, Hydrology and Atmospheric Sciences"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface

# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def theis_wu(Q, T, s):
    wu = s * 4. * np.pi * T / Q
    return wu

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s

def compute_linU(s, s_U0, s_U1):
    u = (s-s_U0)/(s_U1-s_U0)
    u = u.clip(0,1)
    return u

fig = plt.figure(figsize=(12,7))

st.title('Dewatering exercise 💦')
st.subheader("Step 02 - Exploring Drawdown from Pumping", divider="blue")

if st.toggle('Show additional **Notes for instructors**'):
    to_do(
    [(st.write, "Lead a discussion to remind students of radial flow to a well due to pumping.  Show half of a drawdown cone at two times and explain how it progresses.")],
    "td01",)
    to_do(
    [(st.write, "Lead them through a discussion of the impact of ease of flow and ease of change in storage on transient response.")],
    "td02",)
    to_do(
    [(st.write, "Define Transmissivity [L3/T] and Storativity [L].")],
    "td03",)
    to_do(
    [(st.write, "If they know these properties, a hydrogeologist can provide quantitative predictions of the impact of pumping through time.")],
    "td04",)
    to_do(
    [(st.write, "We will use an interactive model to explore the sensitivity of drawdown through time on S and T.")],
    "td05",)
    
    
st.markdown(
    """
                    
    Consider a well pumping at a rate of Q = 300 m3/d
    The aquifer has the properties: T = 3.02 e-04 m2/s, S = 3.02 e-03
    The far edge of the zone to be dewatered is at a distance r = 100 from the well.
    
    #### Use the following tool to answer these questions.
    
    - The mine requires a minimum drawdown of 5 m, how long will this take to achieve❓
    - The mine requires a maximum drawdown of 7 m, when is this drawdown reached❓
    
    #### Then answer these questions.
    
    - How would dewatering impact a town well that is 2500 m from the dewatering well❓
    - Should the town object to the dewatering❓
    
    - How might dewatering impact a stream that is 7500 m from the dewatering well❓
    - Should an environmental group object to the dewatering❓
    
    #### Finally, use your results and the tool to address these questions.🚀
    
    - How are the drawdown curves at 100, 2500, and 7500 similar and how are they different?
    - Explore different dewatering pumping rates to see their impacts on the three stakeholders.
    - Use the drawdown comparison chart that shows two curves to explore how different S and T values affect the drawdown.
    
    ---    
    ### Computational tool 💥
    
"""
)

# Code here
# Input parameter

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # T / Corresponds to 10^0 = 1

columns = st.columns((1,1), gap = 'large')
    
with columns[0]:
    T_slider_value=st.slider('(log of) **Transmissivity in m2/s**', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    T = 10 ** T_slider_value     # Convert the slider value to the logarithmic scale
    st.write("_Transmissivity in m2/s:_ %5.2e" %T)
    S_slider_value=st.slider('(log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )        
    S = 10 ** S_slider_value       # Convert the slider value to the logarithmic scale
    st.write("_Storativity (dimensionless):_ %5.2e" %S)
    Q_pred = st.slider(f'**Select the pumping rate (m^3/d) for the prediction**', 10,1000,100,10,format="%5.0f")
    Q = Q_pred /24 /60 /60    # convert to m3/s

with columns[1]:
    r_pred = st.slider(f'**Distance from the well (m) to report**', 10,10000,1000,10)
    per_pred_min = 0.1
    per_pred = 10.0 
    t_search = st.slider(f'**Time (years) to report**', per_pred_min,per_pred,0.1,0.1)
    t_pred = t_search *365 *24 *60 *60    # convert s

# Compute s through time
t2 = np.linspace(per_pred_min, per_pred, 100)     # in years
s  = compute_s(T, S, t2*365 *24 *60 *60, Q, r_pred)   # in m

# Compute s for a specific point
y_point = compute_s(T, S, t_pred, Q, r_pred)

plt.plot(t2, s, linewidth=3., color='r', label=r'Drawdown prediction')
plt.plot(t_search,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
plt.xlabel(r'Time in years', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)

st.pyplot(fig)

st.write('')   
st.write("The predicted drawdown at the reporting time and distance (in m) is:  %5.2f" %y_point)



fig = plt.figure(figsize=(12,7))

log_minT1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_maxT1 = 0.0  # T / Corresponds to 10^0 = 1

log_minS1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_maxS1 = 0.0  # T / Corresponds to 10^0 = 1

columns = st.columns((2,1), gap = 'large')
    
with columns[0]:
    T_slider_value1=st.slider('Choose first (log of) **Transmissivity in m2/s**', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    T1 = 10 ** T_slider_value1     # Convert the slider value to the logarithmic scale
    st.write("First_Transmissivity in m2/s:_ %5.2e" %T1)
    S_slider_value1=st.slider('Choose first (log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )        
    S1 = 10 ** S_slider_value1       # Convert the slider value to the logarithmic scale
    st.write("First_Storativity (dimensionless):_ %5.2e" %S1)
    T_slider_value2=st.slider('Choose second (log of) **Transmissivity in m2/s**', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    T2 = 10 ** T_slider_value2     # Convert the slider value to the logarithmic scale
    st.write("Second_Transmissivity in m2/s:_ %5.2e" %T2)
    S_slider_value2=st.slider('Choose second (log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )        
    S2 = 10 ** S_slider_value2       # Convert the slider value to the logarithmic scale
    st.write("Second_Storativity (dimensionless):_ %5.2e" %S2)

with columns[1]:
    Q_predboth = st.slider(f'**Select a common pumping rate (m^3/d) for both cases**', 10,1000,100,10,format="%5.0f")
    Qboth = Q_predboth /24 /60 /60    # convert to m3/s
    t_predboth = st.slider(f'**Select a common time of pumping in days for both cases**', 10,3650,1000,10)

# Compute s through time
t2 = np.linspace(per_pred_min, per_pred, 100)     # in years
rmin = 10
rmax = 5000
r2 = np.linspace(rmin, rmax, 100)     # in years

s1  = compute_s(T1, S1, t_predboth*365 *24 *60 *60, Qboth, r2)   # in m
s2  = compute_s(T2, S2, t_predboth*365 *24 *60 *60, Qboth, r2)   # in m

# Compute s for a specific point
plt.plot(r2, -s1, linewidth=3., color='r', label=r'Case 1 drawdown')
plt.plot(r2, -s2, linewidth=3., color='b', label=r'Case 2 drawdown')
plt.xlabel(r'Distance from the pumped well in meters', fontsize=14)
plt.ylabel(r'Negative value of drawdown in m', fontsize=14)
plt.legend()

st.pyplot(fig)

st.write('')   


st.markdown(
    """
    ---
    ### Self-check questions 💦
 
"""
)
st.write('')
st.write('')
question1 = "If everything else is kept constant, what is the effect of increasing S on the drawdown at a given distance and time?"
options1 = "Drawdown increases.", "Drawdown decreases.", "It depends."
answer_index1 = 1
stb.single_choice(question1, options1, answer_index1, success='Correct!  If S is higher, then less drawdown is needed everywhere to release the volume of water pumped by time t.', error='Incorrect - if S is higher, then less drawdown is needed everywhere to release the volume of water pumped by time t.', button='Check answer')

st.write('')
st.write('')
question2 = "If everything else is kept constant, what is the effect of increasing T on the drawdown at a given distance and time?"
options2 = "Drawdown increases.", "Drawdown decreases.", "It depends."
answer_index2 = 2
stb.single_choice(question2, options2, answer_index2, success='Correct!  Simulate the following: logS = -4, Q = 100, t = 1 yr, r = 10 and releat it for r - 10000.  No simple answer here!', error='Incorrect - explore a bit with the simulator and remember to change both T and r!', button='Check answer')

st.write('')
st.write('')
question3 = "Why does the drawdown get less steep with radial distance from the well?"
options3 = "Because flow is radially convergent, the cross section perpendicular to flow increases with distance, requiring a lower gradient.", "Because the pumping decreases K near the well.", "Because flow to a well is transient."
answer_index3 = 0
stb.single_choice(question3, options3, answer_index3, success='Correct!  If you look down at a well in map view, you will see that the same flow has to pass through smaller area as you approach the well.', error='Incorrect - transient flow has some effect and it is possible that pumping may decrease K, but these are not the major reason.', button='Check answer')

st.write('')
st.write('')
question4 = "What is the impact of the drawdown versus time curve if you increase the pumping rate?"
options4 = "It has no effect.", "The curve becomes shallower near the well.", "The shape stays the same, but the scale of the y-axis changes."
answer_index4 = 2
stb.single_choice(question4, options4, answer_index4, success='Correct!  Another way to say this is that the drawdown can be scaled by the pumping rate - this is often used to make Type Curves to interpret pumping tests.', error='Incorrect - if anything, the curve would have to get steeper near the well to drive more flow - but have a closer look at the results when you change Q!', button='Check answer')

st.write('')
st.write('')
question5 = "Why might a nearby environmental group be concerned about dewatering operations at a mine?"
options5 = "The noise of the pumps could affect wildlife.", "The pumping might cause water to flow towards the mine.", "Pumping might lower the water table, which could make it more difficult for plants to get water while also decreasing flow in streams."
answer_index5 = 2
stb.single_choice(question5, options5, answer_index5, success='Correct!  This lowering the water table decreases plant-available water and can cause streams to lose water to the subsurface.', error='Incorrect - pumps might be noisy, but this is not their main impact and water flowing toward the well is not a direct problem in most cases.', button='Check answer')

      


st.markdown(
    """
    ---
    
    #### Assignment after step 2. 📃
    * Produce three curves of }_s(t)_ out to two years, one at the distance relevant for each stakeholder, on the same axes.
    * Explain in a clear paragraph why they all have the same general shape, but they are different in the details.
    * Discuss your understanding at this time of the role of a hydrogeologist in negotiating water issues related to dewatering.
"""
)

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')