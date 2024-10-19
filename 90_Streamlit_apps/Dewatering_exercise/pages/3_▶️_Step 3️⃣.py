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

st.markdown(
    """
    ### Dewatering exercise 💦
    ---
    ## Step 3
    Each stakeholder will place a different value on a given drawdown.
    Utility is a way to normalize these values.
    
    Consider a stakeholder for whom more drawdown is a worse outcome.    
    They would assign U=0 to a drawdown associated with the worst outcome ... further drawdown cannot make things any worse.
    They would assign U=1 to a drawdown associated with the best outcome ... less drawdown would not make things any better.
    
    This could be a very complicated function and, in reality, it is very difficult to define.
    To get a feel for it, we will use a simple linear function.
    
    To define the function, you identify the drawdown values that you want to associate with U=0 and U=1.
    The utility then varies linearly between these points.
    
    Note that if the drawdown for U=1 is lower than the drawdown for U=0, then the stakeholder prefers less drawdown.
    Conversely if the drawdown for U=1 is higher than the drawdown for U=0, then the stakeholder prefers more drawdown.
    
    Give it a try for the following conditions.
    
    A stakeholder decides that U=0 is associated with a drawdown of 0.5 m and U=1 corresponds to a drawdown of 0.05.
    
    Repeat if a stakeholder decides that U=1 is associated with a drawdown of 0.5 m and U=0 corresponds to a drawdown of 0.05.
    

    **Develop a utility curve for the town and be prepared to explain your choices.**
    
    **Develop a utility curve for the environment and be prepared to explain your choices.**
    
    #### In the previous exercise, you were told that:
    
    - The mine requires a minimum drawdown of 5 m and a maximum drawdown of 8 m.
    - Develop a utility curve for the mine.
    
    **Discuss why different stakeholders may have a different time at which they would assess utility.**
    
    ---
"""
)

columns = st.columns((1,1), gap = 'large')
    
with columns[0]:
    s_min = 0.0 # T / Corresponds to 10^-7 = 0.0000001
    s_max = 5.0  # T / Corresponds to 10^0 = 1
    s_U0_value=st.slider('Dradown associated with U=0', s_min,s_max,0.0,0.01,format="%4.2f" ) 
    s_U1_value=st.slider('Dradown associated with U=1', s_min,s_max,s_max/2,0.01,format="%4.2f" )
        
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