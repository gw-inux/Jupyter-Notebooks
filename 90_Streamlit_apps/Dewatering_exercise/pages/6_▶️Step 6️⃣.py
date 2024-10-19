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
    ## Step 6

    A pumping well was operated for 2 days at a rate of 25 m3/d and the drawdown was measured at a monitoring well 25 m from the pumped well.
"""
)

t2 = np.linspace(.1, 2, 12)     # in days
Q_test=25
Q_test = Q_test / 24. / 60. / 60.
st.write('')
st.write('')
T_test = 3.2 * 10**-4
S_test = 2.1 * 10**-3
r_test = 25

s_test = compute_s(T_test, S_test, t2*24 *60 *60, Q_test, r_test)   # in 

fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test, marker='o', color='r',linestyle ='None')
plt.xlabel(r'Time, days', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
st.pyplot(fig)

st.write('')
st.write('')
st.write('Imagine that you have perfect, noise-free data.  Fit T and S.')
st.write('')
st.write('')

log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
T_min_slider_value_fit=st.slider('Inferred (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
T_fit = 10 ** T_min_slider_value_fit
st.write('')
st.write('')

S_min_slider_value_fit=st.slider('Inferred (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
S_fit =  10 ** S_min_slider_value_fit

s_fit = compute_s(T_fit, S_fit, t2*24 *60 *60, Q_test, r_test)   # in 

fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test, marker='o', color='r',linestyle ='None', label=r'Data')
plt.plot(t2, s_fit, linewidth=3., color='b', linestyle ='solid', label=r'Model')
plt.xlabel(r'Time, days', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
st.pyplot(fig)


st.write('')
st.write('')
st.write('Now find three reasonable fits to noisy data.  Fit T and S.')
st.write('')
st.write('')
    
s_error = np.random.normal(loc=0.0, scale=0.02, size=len(s_test))
s_noisy = s_test + s_error

log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
T_min_slider_value_fit1=st.slider('First (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
T_fit1 = 10 ** T_min_slider_value_fit1
st.write('')
st.write('')

S_min_slider_value_fit1=st.slider('First (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
S_fit1 =  10 ** S_min_slider_value_fit1

s_fit_noisy1 = compute_s(T_fit1, S_fit1, t2*24 *60 *60, Q_test, r_test)   # in 

log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
T_min_slider_value_fit2=st.slider('Second (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
T_fit2 = 10 ** T_min_slider_value_fit2
st.write('')
st.write('')

S_min_slider_value_fit2=st.slider('Second (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
S_fit2 =  10 ** S_min_slider_value_fit2

s_fit_noisy2 = compute_s(T_fit2, S_fit2, t2*24 *60 *60, Q_test, r_test)   # in 

log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
T_min_slider_value_fit3=st.slider('Third (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
T_fit3 = 10 ** T_min_slider_value_fit3
st.write('')
st.write('')

S_min_slider_value_fit3=st.slider('Third (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
S_fit3 =  10 ** S_min_slider_value_fit3

s_fit_noisy3 = compute_s(T_fit3, S_fit3, t2*24 *60 *60, Q_test, r_test)   # in 

fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_noisy, marker='o', color='r',linestyle ='None', label=r'Data')
plt.plot(t2, s_fit_noisy1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_fit_noisy2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_fit_noisy3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.xlabel(r'Time, days', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
plt.legend()
st.pyplot(fig)

st.write('')
st.write('')
st.write('This is the impact of the parameter estimates on drawdown for a well pumped at 250 m3/d for 10 years.')
st.write('')
st.write('')

t2 = np.linspace(.1, 10, 100)     # in days    
r_preds = np.array([100, 2500, 7500])

s_test_mine1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_test_mine2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_test_mine3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test_mine1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_mine2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_mine3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown at the mine', fontsize=14)
plt.legend()
st.pyplot(fig)

st.write('')
st.write('')

s_test_town1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_test_town2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_test_town3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test_town1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_town2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_town3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown at the town', fontsize=14)
plt.legend()
st.pyplot(fig)
st.write('')
st.write('')

s_test_env1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_test_env2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_test_env3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test_env1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_env2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_env3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
plt.xlabel(r'Time, years', fontsize=14)
plt.ylabel(r'Drawdown at the env', fontsize=14)
plt.legend()
st.pyplot(fig)

st.write('')
st.write('')
st.write('Assignment after step 6.')
st.write('How should each stakeholder decide which fit to trust?')
st.write('Can you think of an objective way to find the best model?  What are the limitations to this approach?')
st.write('Can you think of an objective way to use all three models?')
st.write('Comment on the value of improving data quality for hydrogeologic analyses.')
st.write('What are the risks or potential costs of poor data quality?')
st.write('')
st.write('')