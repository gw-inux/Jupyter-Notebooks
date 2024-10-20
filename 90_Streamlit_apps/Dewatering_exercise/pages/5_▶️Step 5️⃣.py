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

r_preds = np.array([100, 2500, 7500])

t2 = np.linspace(.1, 10, 100)     # in years

fig = plt.figure(figsize=(12,7))
st.markdown(
    """
    ### Dewatering exercise 💦
    ---
    ## Step 5
    Hydrogeological information is usually uncertain.
    
    🤔 What is the impact if the T and S values that you assumed were wrong?
    
    💥 Use this tool to conduct a sensitivity analysis of the impact of _S_ and _T_ values on each stakeholder.
    * Is there one combination of _S_ and _T_ - high and low - that always produces the highest or lowest drawdown?
    * Is one parameter always more important than the other?
    * How should a stakeholder decide whether to use the inferred T or S value or a slightly higher or lower value to account for uncertainty?

    We will fix the value of _Q_ = 250 m3/d and the distances to the stakeholders as previously defined.
    
    ---
"""
)

Q = 250/24/60/60      #m3/d
st.write('Consider a **maximum and minimum _T_** value to examine.')
log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

columns1 = st.columns((1,1), gap = 'large')
    
with columns1[0]:
    T_min_slider_value=st.slider('Lower (log of) Transmissivity in m2/s', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
    T_min_value = 10 ** T_min_slider_value     # Convert the slider value to the logarithmic scale

with columns1[1]:
    T_max_slider_value=st.slider('Higher (log of) Transmissivity in m2/s', T_min_slider_value,log_max1,(T_min_slider_value+log_max1)/2,0.01,format="%4.2f" )
    T_max_value = 10 ** T_max_slider_value     # Convert the slider value to the logarithmic scale

st.write('')
st.write('Consider a **maximum and minimum _S_** value to examine.')

columns2 = st.columns((1,1), gap = 'large')
    
with columns2[0]:
    S_min_slider_value=st.slider('Lower (log of) Storativity - unitless', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
    S_min_value = 10 ** S_min_slider_value     # Convert the slider value to the logarithmic scale
with columns2[1]:
    S_max_slider_value=st.slider('Higher (log of) Storativity - unitless', S_min_slider_value,log_max1,(S_min_slider_value+log_max1)/2,0.01,format="%4.2f" )
    S_max_value = 10 ** S_max_slider_value     # Convert the slider value to the logarithmic scale

S_values =  10 ** np.linspace(S_min_slider_value, S_max_slider_value, 5)

stakeholder = st.selectbox('Choose a Stakeholder:',["Mine", "Town", "Environment"])

if (stakeholder == "Mine"):
    stakeholder_slider_value = 0
if (stakeholder == "Town"):
    stakeholder_slider_value = 1
if (stakeholder == "Environment"):
    stakeholder_slider_value = 2
    
r = r_preds[stakeholder_slider_value]

t2 = np.linspace(.1, 10, 100)     # in years

T_values = [T_min_value, T_min_value, T_max_value, T_max_value]
S_values = [S_min_value, S_max_value, S_min_value, S_max_value]
    
counter=-1
for T in T_values:
    counter += 1
    S = S_values[counter]
    s = compute_s(T, S, t2*365 *24 *60 *60, Q, r)
    if counter == 0:
        plt.plot(t2, s, linewidth=3., color='r', label=r'low T / low S')
    if counter == 1:
        plt.plot(t2, s, linewidth=3., color='g', label=r'low T / high S')
    if counter == 2:
        plt.plot(t2, s, linewidth=3., color='b', label=r'high T / low S')
    if counter == 3:
        plt.plot(t2, s, linewidth=3., color='k', label=r'high T / high S')

plt.xlabel(r'Drawdown, m', fontsize=14)
plt.ylabel(r'Utility for the mine', fontsize=14)
plt.axis([0, None, 0, None])
plt.legend()
    
st.pyplot(fig)

st.markdown(
    """

    ---
    
    #### Use the following tool to explore how stakeholders can use hydrogeology to choose an optimal dewatering Q.
    
    As a class, you should agree on the utility curves for each stakeholder.

"""
)

fig = plt.figure(figsize=(12,7))

columns = st.columns((1,1,1), gap = 'large')
   
with columns[0]:
    st.write('**Mine**')
    st.write('')
    s_min = 0.0 # T / Corresponds to 10^-7 = 0.0000001
    s_max = 10.0  # T / Corresponds to 10^0 = 1
    mine_s_U0_value=st.slider('Dradown associated with **U = 0** for the **mine**', s_min,s_max,5.,0.01,format="%4.2f" )        
    mine_s_U1_value=st.slider('Dradown associated with **U = 1** for the **mine**', s_min,s_max,8.,0.01,format="%4.2f")
    if mine_s_U0_value == mine_s_U1_value:
        mine_s_U0_value = mine_s_U1_value + 0.1
    mine_t_value=st.slider('Time at which utility is determined for the **mine** in years', 0.,9.9,1.,0.1,format="%4.1f")
with columns[1]:
    st.write('**Town**')
    st.write('')
    town_s_U0_value=st.slider('Dradown associated with **U = 0** for the **town**', s_min,s_max,4.5,0.01,format="%4.2f" )        
    town_s_U1_value=st.slider('Dradown associated with **U = 1** for the **town**', s_min,s_max,1.,0.01,format="%4.2f")    
    if town_s_U0_value == town_s_U1_value:
        town_s_U0_value = town_s_U1_value + 0.1
    town_t_value=st.slider('Time at which utility is determined for the **town** in years', 0.,9.9,5.,0.1,format="%4.1f")
with columns[2]:
    st.write('**Environment**')
    st.write('')
    env_s_U0_value=st.slider('Dradown associated with U=0 for the environment', s_min,s_max,1.0,0.01,format="%4.2f" )        
    env_s_U1_value=st.slider('Dradown associated with U=1 for the environment', s_min,s_max,0.5,0.01,format="%4.2f")
    if env_s_U0_value == env_s_U1_value:
        env_s_U0_value = env_s_U1_value + 0.1
    env_t_value=st.slider('Time at which utility is determined for the environment in years', 0.,9.9,9.9,0.1,format="%4.1f")
      
s_vals = np.linspace(s_min, s_max, 100)     # in years    
mine_uvals = compute_linU(s_vals, mine_s_U0_value, mine_s_U1_value)
town_uvals = compute_linU(s_vals, town_s_U0_value, town_s_U1_value)
env_uvals = compute_linU(s_vals, env_s_U0_value, env_s_U1_value)
    
plt.plot(s_vals, mine_uvals, linewidth=3., color='r', label=r'Mine')
plt.plot(s_vals, town_uvals, linewidth=3., color='g', label=r'Town')
plt.plot(s_vals, env_uvals, linewidth=3., color='b', label=r'Environment')
plt.xlabel(r'Drawdown, m', fontsize=14)
plt.ylabel(r'Utility for the mine', fontsize=14)
plt.axis([0, None, None, None])
plt.legend()
    
st.pyplot(fig)

st.markdown(
    """

    ---

    #### Now choose a common S and T pair.

    Work together to determine the utility for each stakeholder over at least 20 pumping rates.
    
    Create a table with Q listed against the utilities.   
    
    Plot the matched utilities for the town against those of the mine.

    Be prepared to explain how this plot can be used for Pareto optimization.

    Repeat the exercise for a different S and T pair.

    Is the optimal pumping rate the same for both S and T pairs?

"""
)

Q_temp=st.slider('Pumping rate', 10.,400.,200.,10.,format="%4.0f" )
Q = Q_temp / 24 / 60 / 60
st.write('')
st.write('')

T_min_slider_value1=st.slider('(log of) Transmissivity in m2/s', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
T = 10 ** T_min_slider_value1
st.write('')
st.write('')

S_min_slider_value1=st.slider('(log of) Storativity - unitless', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
S =  10 ** S_min_slider_value1
st.write('')
st.write('')
st.write('It is assumed that T and S are only known within +- 10%.')
st.write('The stakeholders take a conservative view: the mine uses lower T and S and the town and environement use the higher values.')
st.write('')
st.write('')


multiplier_num = ([0, 1])
multiplier1 = ([0.9, 1.1])     # only need paired lowT-LowS (max) and HighT-HighS (min)
multiplier2 = ([0.9, 1.1])
    
s_forrs = np.zeros([len(r_preds),len(t2)])
   
counter=-1
for r in r_preds:
    counter += 1 
    if r==np.min(r_preds):           # mine
        s_forrs[counter,:] = np.squeeze(compute_s(T*multiplier1[0], S*multiplier2[0], t2*365 *24 *60 *60, Q, r))   # in m
    else:
        s_forrs[counter,:] = np.squeeze(compute_s(T*multiplier1[1], S*multiplier2[1], t2*365 *24 *60 *60, Q, r))   # in 
  
s_mine = np.squeeze(s_forrs[0,np.min(np.where(t2>mine_t_value))])      # use minimum drawdown for mine      
u_mine = compute_linU(s_mine, mine_s_U0_value, mine_s_U1_value)
s_env = np.squeeze(s_forrs[2,np.min(np.where(t2>env_t_value))])      # env    
u_env = compute_linU(s_env, env_s_U0_value, env_s_U1_value)
s_town = np.squeeze(s_forrs[1,np.min(np.where(t2>town_t_value))])      # town          
u_town = compute_linU(s_town, town_s_U0_value, town_s_U1_value)
        
fig = plt.figure(figsize=(12,7))
plt.plot(t2, np.squeeze(s_forrs[0,:]), linewidth=3., color='r', label=r'Mine')
plt.plot(t2[np.min(np.where(t2>mine_t_value))],s_mine, marker='o', color='r',linestyle ='None', label='@mine')
plt.plot(t2, np.squeeze(s_forrs[1,:]), linewidth=3., color='b', label=r'Town')
plt.plot(t2[np.min(np.where(t2>town_t_value))],s_town, marker='o', color='b',linestyle ='None', label='@town')
plt.plot(t2, np.squeeze(s_forrs[2,:]), linewidth=3., color='g', label=r'Env')
plt.plot(t2[np.min(np.where(t2>env_t_value))],s_env, marker='o', color='g',linestyle ='None', label='@env')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
plt.axis([0, None, 0, None])
plt.legend(fontsize=14)
    
st.write("The utility for the **mine** at the assessment time is:  %5.2f" %u_mine)
st.write("The utility for the **town** at the assessment time is:  %5.2f" %u_town)
st.write("The utility for the **environment** at the assessment time is:  %5.2f" %u_env)
  
st.pyplot(fig)
    
st.markdown(
    """

    ---

    #### Finally, consider this tradeoff curve made for the mine and the town for multiple Q values.
    
    Change T and S to see how it impacts the Pareto optimal designs.')    

    Plot the matched utilities for the town against those of the mine.')    

    Be prepared to explain how this plot can be used for Pareto optimization.')

    Repeat the exercise for a different S and T pair.')

    Is the optimal pumping rate the same for both S and T pairs?')

    Pumping rates will be examined ranging linearly from the min and max that you choose.
"""
)

Q_min_value=st.slider('**Minimum pumping rate** to consider', 10.,400.,20.,10.,format="%4.1f" )
Q_max_value=st.slider('**Maximum pumping rate** to consider', Q_min_value+10.,500.,325.,10.,format="%4.1f" )
Q_values = np.linspace(Q_min_value, Q_max_value, 50)
Q_values = Q_values / 24. / 60. / 60.
st.write('')
st.write('')

T_min_slider_value2=st.slider('Choose (log of) **Transmissivity** in m2/s', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
T = 10 ** T_min_slider_value2
st.write('')
st.write('')

S_min_slider_value2=st.slider('Choose (log of) **Storativity** - unitless', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
S =  10 ** S_min_slider_value2
st.write('')
st.write('')
st.write('It is assumed that T and S are only known within +- 10%.')
st.write('The stakeholders take a conservative view: the mine uses lower T and S and the town and environement use the higher values.')
st.write('')
st.write('')

multiplier_num = ([0, 1])
multiplier1 = ([0.9, 1.1])     # only need paired lowT-LowS (max) and HighT-HighS (min)
multiplier2 = ([0.9, 1.1])
    
s_forrs = np.zeros([len(r_preds)*len(Q_values),len(t2)])
u_mine = np.zeros([len(Q_values)])
u_town = np.zeros([len(Q_values)])
s_town = np.zeros([len(Q_values)])
u_env = np.zeros([len(Q_values)])
Q_hold = np.zeros([len(r_preds)*len(Q_values)])
            
counter=-1
Qcounter=-1
for Q in Q_values:
    Qcounter += 1 
    for r in r_preds:
        counter += 1 
        Q_hold[counter] = Q * 24. * 60. * 60.
        if r==np.min(r_preds):           # mine
            s_forrs[counter,:] = np.squeeze(compute_s(T*multiplier1[0], S*multiplier2[0], t2*365 *24 *60 *60, Q, r))   # in m
        else:
            s_forrs[counter,:] = np.squeeze(compute_s(T*multiplier1[1], S*multiplier2[1], t2*365 *24 *60 *60, Q, r))   # in    
        
        if r == np.min(r_preds):          # mine
            s_current = np.squeeze(s_forrs[counter,np.min(np.where(t2>mine_t_value))])      # use minimum drawdown for mine                     
            u_mine[Qcounter:] = compute_linU(s_current, mine_s_U0_value, mine_s_U1_value)   # in m
        elif r == np.max(r_preds):          # env
            s_current = np.squeeze(s_forrs[counter,np.min(np.where(t2>env_t_value))])      # env    
            u_env[Qcounter:] = compute_linU(s_current, env_s_U0_value, env_s_U1_value)   # in m
           
        else:          # town
            s_current = np.squeeze(s_forrs[counter,np.min(np.where(t2>town_t_value))])      # town      
            u_town[Qcounter:] = compute_linU(s_current, town_s_U0_value, town_s_U1_value)   # in m
            s_town[Qcounter:] = s_current   # in m
            
fig = plt.figure(figsize=(12,7))
plt.plot(u_mine, u_town, marker='o', color='r',linestyle ='None', label=r'Utility')
plt.xlabel(r'Utility for the Mine', fontsize=14)
plt.ylabel(r'Utility for the Town', fontsize=14)
plt.legend()
st.pyplot(fig)

fig = plt.figure(figsize=(12,7))
plt.plot(u_env, u_town, marker='o', color='r',linestyle ='None', label=r'Utility')
plt.xlabel(r'Utility for the Environment', fontsize=14)
plt.ylabel(r'Utility for the Town', fontsize=14)
plt.legend()
st.pyplot(fig)

st.markdown(
    """

    ---

    #### How can you combine these two tradeoff plots to identify the optimal pumping rate?   



    What if we optimize based on the total utility?

"""
)

u_sum = u_mine + u_town + u_env
fig = plt.figure(figsize=(12,7))
plt.plot(Q_values* 24. * 60. * 60., u_sum, marker='o', color='r',linestyle ='None', label=r'Total')
plt.plot(Q_values* 24. * 60. * 60., u_mine, marker='o', color='b',linestyle ='None', label=r'Mine')
plt.plot(Q_values* 24. * 60. * 60., u_mine + u_town, marker='o', color='g',linestyle ='None', label=r'Mine+Town')
plt.xlabel(r'Dewatering rate', fontsize=14)
plt.ylabel(r'Sum of utilities', fontsize=14)
plt.legend()
st.pyplot(fig)
st.markdown(
    """

    ---

    #### What if we optimize based on the variance of utility?
    
"""
)

u_vector = np.zeros((3,len(u_mine)))
u_vector[0,:] = u_mine
u_vector[1,:] = u_town
u_vector[2,:] = u_env

fig = plt.figure(figsize=(12,7))
plt.plot(Q_values* 24. * 60. * 60., np.var(u_vector,0), marker='o', color='r',linestyle ='None', label=r'Utility')
plt.xlabel(r'Dewatering rate', fontsize=14)
plt.ylabel(r'Variance of utilities', fontsize=14)
plt.legend()
st.pyplot(fig)

st.markdown(
    """

    ---

    #### What if tried to find the point with the highest minimum utiility across stakeholders?
    
"""
)

u_vector = np.zeros((3,len(u_mine)))
u_vector[0,:] = u_mine
u_vector[1,:] = u_town
u_vector[2,:] = u_env

fig = plt.figure(figsize=(12,7))
plt.plot(Q_values* 24. * 60. * 60., np.min(u_vector,0), marker='o', color='r',linestyle ='None', label=r'Utility')
plt.xlabel(r'Dewatering rate', fontsize=14)
plt.ylabel(r'Highest minimum utility over stakeholders', fontsize=14)
plt.legend()
st.pyplot(fig)
