# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:28:58 2024

@author: tyfer
"""

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

## ToDo:
#    - number input
#    - log slider
#    - revise UI
#    - generate random data in a proper way

#--- User Interface

# This is a copy of Thomas Reimann's code to guide students through a mine dewatering, multiple stakeholder negotiation


# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stodo import to_do

st.title('Dewatering exercise 💦')
st.subheader("Step 06 - Pumping Tests and the Impacts of Hydrogeologic Uncertainty", divider="blue")

# I found U slightly confusing because it is also used in the Theis context

if st.toggle('Show additional **Notes for instructors**'):
    to_do(
    [(st.write, "Remind students of what S and T are and how they affect drawdown versus distance and time.")],
    "td01",)
    to_do(
    [(st.write, "Ask them how they think that S and T could be measured.")],
    "td02",)
    to_do(
    [(st.write, "Introduce the idea of inverse modeling - parameter estimation - and a pumping test.")],
    "td03",)
    to_do(
    [(st.write, "Discuss measurement uncertainty and conceptual errors in conducting a pumping test.")],
    "td04",)
    to_do(
    [(st.write, "Circle back to the previous exercise, now extending from measurement uncertainty, to parameter uncertainty, to prediction uncertainty, to loss of utility.")],
    "td05",)
    
    
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
    A pumping well was operated for 2 days at a rate of 25 m3/d and the drawdown was measured at a monitoring well 25 m from the pumped well.
    
    
"""
)

log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max_fit = 0.0  # T / Corresponds to 10^0 = 1

t2 = np.linspace(.1, 2, 12)     # in days
Q_test=25
Q_test = Q_test / 24. / 60. / 60.
T_test = 3.2 * 10**-4
S_test = 2.1 * 10**-3
r_test = 25

s_test = compute_s(T_test, S_test, t2*24 *60 *60, Q_test, r_test)   # in 

fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test, marker='o', color='r',linestyle ='None', label='Measured drawdown')
plt.xlabel(r'Time, days', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
plt.legend(fontsize=14)
plt.axis([0, None, 0, None])
st.pyplot(fig)

st.markdown(
    """

    ---

    #### Imagine that you have perfect, noise-free data.  Fit T and S.')
    
"""
)

columns = st.columns((1,1), gap = 'large')
   
with columns[0]:
    T_min_slider_value_fit=st.slider('Inferred (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    T_fit = 10 ** T_min_slider_value_fit

with columns[1]:
    S_min_slider_value_fit=st.slider('Inferred (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    S_fit =  10 ** S_min_slider_value_fit

st.write('')
st.write('')

s_fit = compute_s(T_fit, S_fit, t2*24 *60 *60, Q_test, r_test)   # in 

fig = plt.figure(figsize=(12,7))
plt.plot(t2, s_test, marker='o', color='r',linestyle ='None', label=r'Data')
plt.plot(t2, s_fit, linewidth=3., color='b', linestyle ='solid', label=r'Model')
plt.xlabel(r'Time, days', fontsize=14)
plt.ylabel(r'Drawdown', fontsize=14)
plt.legend(fontsize=14)
plt.axis([0, None, 0, None])
st.pyplot(fig)

st.markdown(
    """

    ---

    #### Now find three reasonable fits to noisy data.  Fit T and S.')
    
"""
)
    
s_error = np.random.normal(loc=0.0, scale=0.02, size=len(s_test))
s_noisy = s_test + s_error

columns2 = st.columns((1,1,1), gap = 'medium')
   
with columns2[0]:
    st.write('**MODEL 1**')
    T_min_slider_value_fit1=st.slider('1st (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    T_fit1 = 10 ** T_min_slider_value_fit1
    st.write('')
    S_min_slider_value_fit1=st.slider('1st (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    S_fit1 =  10 ** S_min_slider_value_fit1
    s_fit_noisy1 = compute_s(T_fit1, S_fit1, t2*24 *60 *60, Q_test, r_test)   # in 
    
with columns2[1]:
    st.write('**MODEL 2**')
    T_min_slider_value_fit2=st.slider('2nd (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    T_fit2 = 10 ** T_min_slider_value_fit2
    st.write('')
    S_min_slider_value_fit2=st.slider('2nd (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    S_fit2 =  10 ** S_min_slider_value_fit2
    s_fit_noisy2 = compute_s(T_fit2, S_fit2, t2*24 *60 *60, Q_test, r_test)   # in 
    
with columns2[2]:
    st.write('**MODEL 3**')
    T_min_slider_value_fit3=st.slider('3rd (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
    T_fit3 = 10 ** T_min_slider_value_fit3
    st.write('')
    S_min_slider_value_fit3=st.slider('3rd (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,(log_min_fit+0.9*log_max_fit)/2,0.01,format="%4.2f" )
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

st.markdown(
    """

    ---

    #### This is the impact of the parameter estimates on drawdown for a well pumped at 250 m3/d for 10 years.
    
"""
)
t2 = np.linspace(.1, 10, 100)     # in days    
r_preds = np.array([100, 2500, 7500])

s_test_mine1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_test_mine2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 
s_test_mine3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[0])   # in 

s_test_town1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_test_town2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
s_test_town3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 

s_test_env1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_test_env2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
s_test_env3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 

s_max_plot = max(s_test_mine1+s_test_mine2+s_test_mine3+s_test_town1+s_test_town2+s_test_town3+s_test_env1+s_test_env2+s_test_env3)
norm_plots = st.toggle('Same range of drawdown for all plots')

fig = plt.figure(figsize=(12,7))
plt.title('Drawdown at the mine', fontsize=16)
plt.plot(t2, s_test_mine1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
plt.plot(t2, s_test_mine2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
plt.plot(t2, s_test_mine3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
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
    
    ---
    
    #### Assignment after step 6. 📑
    👉 How should each stakeholder decide which fit to trust?
    
    👉 Can you think of an objective way to find the best model?  What are the limitations to this approach?
    
    👉 Can you think of an objective way to use all three models?
    
    👉 Comment on the value of improving data quality for hydrogeologic analyses.
    
    👉 What are the risks or potential costs of poor data quality?
    
"""
)


st.markdown(
    """
    ---
    ### Self-check questions 💦
 
"""
)
st.write('')
st.write('')
question1 = "What is parameter estimation?"
options1 = "Making an educated guess about parameter values.", "Rethinking the processes that describe a system given new data.", "Finding the values of parameters that make a model fit the data as well as possible."
answer_index1 = 2
stb.single_choice(question1, options1, answer_index1, success='Correct!  In parameter estimation, we typically assume that our model is correct, but that it has to be tuned to match the data.', error='Incorrect - while we often start with an educated guess, we then alter parameter values to fit our model to data.  If we cannot get a good fit, we may have to rethink our model!', button='Check answer')

st.write('')
st.write('')
question1 = "If a model does not fit the data, then the parameters are wrong."
options2 = "True - this is the basis of parameter estimation.", "False - data typically include measurement error so we shouldn't expect the model to fit the data exactly.", "True - data cannot reveal mistakes in our understanding of the system."
answer_index2 = 1
stb.single_choice(question1, options2, answer_index2, success='Correct!  Collecting more (and better) data can reduce the impacts of measurement error, but it will always exist!', error='Incorrect - we might assume that our model is correct and that we only have to find the right parameters to fit the data, but we should always be on the lookout for structural errors built into our models.', button='Check answer')

st.write('')
st.write('')
question3 = "Uncertain data leads to uncertain parameters which lead to uncertain predictions."
options3 = "True - you should quantify prediction errors and let a stakeholder decide how to consider them.", "True - but the best fitting model is usually good enough to rely on for decision making.", "False - it is our job as a scientist to provide the best possible prediction; adding uncertainty reduces our credibility."
answer_index3 = 0
stb.single_choice(question3, options3, answer_index3, success='True - we should included errors on our predictions because they always exist.  Sophisticated decision makers will know how to account for prediction error.', error='Incorrect - in some cases there may be very little data, so a single model is adquate; but the job of a scientist is to provide the best possible answer including the level of uncertainty.', button='Check answer')

st.write('')
st.write('')
question4 = "A pumping test is designed to:"
options4 = "Choose the right pump to use in a well.", "Test how solidly a well was constructed.", "Determine the hydraulic properties of an aquifer."
answer_index4 = 2
stb.single_choice(question4, options4, answer_index4, success='Correct!  A pumping test is a classic hydrogeologic method to determine aquifer hydraulic properties, which can then be used in models to make predictions.', error='Incorrect - it is true that a pumping test may indicate that too small or large a pump was used or that the well was poorly installed, but these are not the main purposes of the test.', button='Check answer')

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')