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

st.markdown(
    """
    ### Dewatering exercise 💦
    ---
    ## Step 7

    #### Start from fitting three curves, as you did at the end of the last exercise.
    
    🚀 You have a head start this time! 
"""
)

t2 = np.linspace(.1, 2, 12)     # in days
Q_test=25
Q_test = Q_test / 24. / 60. / 60.

T_test = 3.2 * 10**-4
S_test = 2.1 * 10**-3
r_test = 25

s_test = compute_s(T_test, S_test, t2*24 *60 *60, Q_test, r_test)   # in 

st.markdown(
    """

    ---

    #### Now find three reasonable fits to noisy data.  Fit T and S.
    
"""
)

log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
    
s_error = np.random.normal(loc=0.0, scale=0.02, size=len(s_test))
s_noisy = s_test + s_error

columns = st.columns((1,1,1), gap = 'medium')
   
with columns[0]:
    st.write('**MODEL 1**')
    T_min_slider_value_fit1=st.slider('1st (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,-3.37,0.01, format="%4.2f" )
    T_fit1 = 10 ** T_min_slider_value_fit1
    st.write('')
    S_min_slider_value_fit1=st.slider('1st (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,-3.19,0.01, format="%4.2f" )
    S_fit1 =  10 ** S_min_slider_value_fit1
    s_fit_noisy1 = compute_s(T_fit1, S_fit1, t2*24 *60 *60, Q_test, r_test)   # in 
    
with columns[1]:
    st.write('**MODEL 2**')
    T_min_slider_value_fit2=st.slider('2nd (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,-3.61,0.01, format="%4.2f" )
    T_fit2 = 10 ** T_min_slider_value_fit2
    st.write('')
    S_min_slider_value_fit2=st.slider('2nd (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,-2.48,0.01, format="%4.2f" )
    S_fit2 =  10 ** S_min_slider_value_fit2
    s_fit_noisy2 = compute_s(T_fit2, S_fit2, t2*24 *60 *60, Q_test, r_test)   # in 
    
with columns[2]:
    st.write('**MODEL 3**')
    T_min_slider_value_fit3=st.slider('3rd (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,-3.5,0.01, format="%4.2f" )
    T_fit3 = 10 ** T_min_slider_value_fit3
    st.write('')
    S_min_slider_value_fit3=st.slider('3rd (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,-2.6,0.01, format="%4.2f" )
    S_fit3 =  10 ** S_min_slider_value_fit3
    s_fit_noisy3 = compute_s(T_fit3, S_fit3, t2*24 *60 *60, Q_test, r_test)   # in 

fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_noisy, marker='o', color='r',linestyle ='None', label=r'Data')
plt.plot(t2, s_fit_noisy1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_fit_noisy2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_fit_noisy3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.xlabel(r'Time, days', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
plt.legend(fontsize=14)
plt.axis([0, None, 0, None])
st.pyplot(fig)

diff_model1 = s_fit_noisy1 - s_test
se_model1 = diff_model1**2
rmse_model1 = np.sqrt(np.sum(se_model1))/len(s_test)

diff_model2 = s_fit_noisy2 - s_test
se_model2 = diff_model2**2
rmse_model2 = np.sqrt(np.sum(se_model2))/len(s_test)

diff_model3 = s_fit_noisy3 - s_test
se_model3 = diff_model3**2
rmse_model3 = np.sqrt(np.sum(se_model3))/len(s_test)

L_model1 = 1/rmse_model1
L_model2 = 1/rmse_model2
L_model3 = 1/rmse_model3
L_sum = (L_model1 + L_model2 + L_model3)
L_model1 = L_model1/L_sum
L_model2 = L_model2/L_sum
L_model3 = L_model3/L_sum
    
columns2 = st.columns((1,1,1), gap = 'medium')

st.write('')
st.write('')
with columns2[0]:
    st.write('**MODEL 1**')
    st.write("The Root Mean Square Error is:  %7.4f" %rmse_model1)
    st.write("The likelihood is:  %7.4f" %L_model1)
    
with columns2[1]:
    st.write('**MODEL 2**')
    st.write("The Root Mean Square Error is:  %7.4f" %rmse_model2)
    st.write("The likelihood is:  %7.4f" %L_model2)
    
with columns2[2]:
    st.write('**MODEL 3**')
    st.write("The Root Mean Square Error is:  %7.4f" %rmse_model3)
    st.write("The likelihood is:  %7.4f" %L_model3)

st.write('')
st.write('')
st.write('**This is the impact of the parameter estimates on drawdown for a well pumped at 250 m3/d for 10 years.**')
st.write('')
st.write('')

t2 = np.linspace(.1, 10, 100)     # in days    
r_preds = np.array([100, 2500, 7500])

s_test_mine1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_test_mine2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_test_mine3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_Lw_mine = s_test_mine1 * L_model1 + s_test_mine2 * L_model2 + s_test_mine3 * L_model3   

s_test_town1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_test_town2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_test_town3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_Lw_town = s_test_town1 * L_model1 + s_test_town2 * L_model2 + s_test_town3 * L_model3   

s_test_env1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_test_env2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_test_env3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_Lw_env = s_test_env1 * L_model1 + s_test_env2 * L_model2 + s_test_env3 * L_model3  

s_max_plot = max(s_test_mine1+s_test_mine2+s_test_mine3+s_test_town1+s_test_town2+s_test_town3+s_test_env1+s_test_env2+s_test_env3)
norm_plots = st.toggle('Same range of drawdown for all plots')

fig = plt.figure(figsize=(12,7))
plt.title('Drawdown at the mine', fontsize=16)
plt.plot(t2, s_test_mine1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_mine2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_mine3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.plot(t2, s_Lw_mine, linewidth=3., color='r', linestyle ='dashed', label=r'Lw')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown at the mine', fontsize=14)
plt.legend(fontsize=14)
if norm_plots:
    plt.axis([0, None, 0, s_max_plot])
else:
    plt.axis([0, None, 0, None])
st.pyplot(fig)

st.write('')
st.write('')

fig = plt.figure(figsize=(12,7))
plt.title('Drawdown at the town', fontsize=16)
plt.plot(t2, s_test_town1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_town2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_town3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.plot(t2, s_Lw_town, linewidth=3., color='r', linestyle ='dashed', label=r'Lw')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown at the town', fontsize=14)
plt.legend(fontsize=14)
if norm_plots:
    plt.axis([0, None, 0, s_max_plot])
else:
    plt.axis([0, None, 0, None])
st.pyplot(fig)

st.write('')
st.write('')
    
fig = plt.figure(figsize=(12,7))
plt.title('Drawdown at the environment', fontsize=16)
plt.plot(t2, s_test_env1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_env2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_env3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.plot(t2, s_Lw_env, linewidth=3., color='r', linestyle ='dashed', label=r'Lw')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown at the env', fontsize=14)
plt.legend(fontsize=14)
if norm_plots:
    plt.axis([0, None, 0, s_max_plot])
else:
    plt.axis([0, None, 0, None])
st.pyplot(fig)

st.markdown(
    """

    #### Explore the parameter estimations.
    * Does a poorly fitted model have much impact on the likelihood-weighted predictions?
    
    * Discuss why this Bayesian approach helps to guard against erroneous fitting of a model to data.
"""
)

# If there is time
    # add plots to show utilities for each stakeholder for each fit and for the likelihood weighted average
    # discuss whether stakeholders should use the Lweighted average
        # remember - what is the prior for this model!?
    # discuss why collecting additional data might be useful
    # discuss when you know that you don't need any more data