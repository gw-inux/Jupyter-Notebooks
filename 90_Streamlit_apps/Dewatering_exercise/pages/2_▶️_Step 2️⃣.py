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
    ## Step 2
    
    Consider a well pumping at a rate of Q = 250 m3/d
    The aquifer has the properties: T = 2.14 e-04 m2/s, S = 9.33 e-06
    The far edge of the zone to be dewatered is at a distance r = 100 from the well.
    
    #### Use the following tool to answer these questions.
    
    - The mine requires a minimum drawdown of 5 m, how long will this take to achieve❓
    - The mine requires a maximum drawdown of 8 m, when is this drawdown reached❓
    
    #### Then answer these questions.
    
    - How would dewatering impact a town well that is 2500 m from the dewatering well❓
    - Should the town object to the dewatering❓
    
    - How might dewatering impact a stream that is 7500 m from the dewatering well❓
    - Should an environmental group object to the dewatering❓
    
    #### Finally, use your results and the tool to address these questions.🚀
    
    - How are the drawdown curves at 100, 2500, and 7500 similar and how are they different?
    - Explore different dewatering pumping rates to see their impacts on the three stakeholders.
    
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

st.markdown(
    """
    ---
    
    #### Assignment after step 2.
    Produce three curves of s(t) out to two years, one at the distance relevant for each stakeholder, on the same axes.
    Explain in a clear paragraph why they all have the same general shape, but they are different in the details.
    Discuss your understanding at this time of the role of a hydrogeologist in negotiating water issues related to dewatering.
"""
)
