# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:28:58 2024

@author: tyfer
"""

# This is a copy of Thomas Reimann's code to guide students through a mine dewatering, multiple stakeholder negotiation


# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stodo import to_do

# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis

def compute_linU(s, s_U0, s_U1):
    u = (s-s_U0)/(s_U1-s_U0)
    u = u.clip(0,1)
    return u


fig = plt.figure(figsize=(12,7))

st.title('Dewatering exercise 💦')
st.subheader("Step 03 - Exploring Stakeholder Utility", divider="blue")

# I found U slightly confusing because it is also used in the Theis context

if st.toggle('Show additional **Notes for instructors**'):
    to_do(
    [(st.write, "Lead a discussion to examine how we 'value' things.")],
    "td01",)
    to_do(
    [(st.write, "Start with everyday things ... how do we determine if something is 'worth the price'?")],
    "td02",)
    to_do(
    [(st.write, "Then move on to town stakeholder - how do they value water?  Repeat for mine, then for environment.")],
    "td03",)
    to_do(
    [(st.write, "Discuss pros and cons of translating everything to monetary value for valuation.")],
    "td04",)
    to_do(
    [(st.write, "Introduce the idea of 'utility', varying from worthless U=0 to couldn't be better U=1.")],
    "td05",)
    to_do(
    [(st.write, "What is the shape of U versus water level in a well?  How could you actually decide?")],
    "td06",)
    

st.markdown(
    """

    Each stakeholder will place a different value on a given drawdown. Utility _U_ is a way to normalize these values.
    
    Consider a stakeholder for whom more drawdown is a worse outcome.    
    * They would assign U = 0 to a drawdown associated with the worst outcome ... further drawdown cannot make things any worse.
    * They would assign U = 1 to a drawdown associated with the best outcome ... less drawdown would not make things any better.
    
    This could be a very complicated function and, in reality, it is very difficult to define.
    
    To get a feel for it, we will use a simple linear function between two threshhold drawdown values.
    
    To define the function, you identify the drawdown _s_ values that you want to associate with U = 0 and U = 1. The utility then varies linearly between these points.
    
    Note that if the drawdown for U = 1 is lower than the drawdown for U = 0, then the stakeholder prefers less drawdown. Conversely if the drawdown for U = 1 is higher than the drawdown for U = 0, then the stakeholder prefers more drawdown.
    
    Give it a try for the following conditions.
    * A stakeholder decides that U = 0 is associated with a drawdown of 0.5 m and U = 1 corresponds to a drawdown of 0.05.
    * Repeat if a stakeholder decides that U = 1 is associated with a drawdown of 0.5 m and U = 0 corresponds to a drawdown of 0.05.
    

    👉 Develop a utility curve for the town and be prepared to explain your choices.
    
    👉 Develop a utility curve for the environment and be prepared to explain your choices.
    
    In the previous exercise, you were told that:
    
    - The mine requires a minimum drawdown of 5 m and a maximum drawdown of 7 m.
    - Develop a utility curve for the mine.
    
    👉 Discuss why different stakeholders may have a different time at which they would assess utility.
    
    Come up with a decision that you have to make in your life:
    
    - What is the STATE upon which you make the decision.
    - What is the OUTCOME upon which you make the decision.
    - Define the outcomes that define utilities of 0 and 1
    - Create a utility curve to relate the state to the utility
    
    👉 Discuss how utility framing may help you to make a more efficient and effective decision.
    
    ---
"""
)

# Input parameter
s_min = 0.0
s_max = 5.0

columns = st.columns((1,1), gap = 'large')
    
with columns[0]:
    s_U0_value=st.slider('Drawdown s (in m) associated with U = 0', s_min,s_max,0.0,0.01,format="%4.2f" ) 
    s_U1_value=st.slider('Drawdown s (in m) associated with U = 1', s_min,s_max,s_max/2,0.01,format="%4.2f" )
        
xvals = [s_min, s_U0_value, s_U1_value, 2*s_max]

if s_U0_value == s_U1_value:
    s_U0_value = s_U1_value + 0.1
    
if s_U0_value < s_U1_value:
    yvals = [0, 0, 1, 1]
    xvals = [s_min, s_U0_value, s_U1_value, 2*s_max]
else:
    yvals = [1, 1, 0, 0]
    xvals = [s_min, s_U1_value, s_U0_value, 2*s_max]

plt.plot(xvals, yvals, linewidth=3., color='r', label=r'Drawdown prediction')
plt.xlabel(r'Drawdown, m', fontsize=14)
plt.ylabel(r'Utility', fontsize=14)
st.pyplot(fig)

st.markdown(
    """
    ---
    ### Self-check questions 💦
 
"""
)
st.write('')
st.write('')
question1 = "What is the meaning of a threshold drawdown below which the utilty is zero?"
options1 = "It is the minimum expected drawdown.", "Any drawdown below this value is equally bad, having zero utility for the stakeholder.", "The stakeholders haven't considered these drawdown levels."
answer_index1 = 1
stb.single_choice(question1, options1, answer_index1, success='Correct!  This would indicate a stakeholder who values more drawdown more highly, like the mine, and who finds drawdown below a given level to have no utility.', error='Incorrect - in most cases very low or zero drawdown will be considered - it corresponds to the no-pumping case.', button='Check answer')

st.write('')
st.write('')
question1 = "Why is it useful to consider a simple, linear-step utility function?"
options2 = "It is the best representation of reality for most stakeholders.", "It allows for the development of simple analytical solutions.", "It is probably not correct, but it is easy to understand and probably not too far from true."
answer_index2 = 2
stb.single_choice(question1, options2, answer_index2, success='Correct!  It is extremely difficult - if not impossible - to define a true cost function for a stakeholder group, but this simple model provides much of the insight about them', error='Incorrect - this simple model is almost certainly not correct and these problems are generally too messy to lead to clean analytical solutions!', button='Check answer')

st.write('')
st.write('')
question3 = "What are the units of utility?"
options3 = "Utility is unitless.", "Whatever the local currency is.", "Each stakeholder has different units."
answer_index3 = 0
stb.single_choice(question3, options3, answer_index3, success='Correct!  It is useful to think of utilty as representing a level of satisfaction.  They are intentionally unitless to allow for comparison among stakeholders..', error='Incorrect - while it is true that some stakeholders use currency for value and each may have their own basis for value, it is important to think of utility as unitless.', button='Check answer')


