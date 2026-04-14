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
st.subheader("Step 07 - Addressing Prediction Uncertainty", divider="blue")

# I found U slightly confusing because it is also used in the Theis context

if st.toggle('Show additional **Notes for instructors**'):
    to_do(
    [(st.write, "Remind students of how fitting a model to noisy data can give rise to different parameter values, all of which fit the data.")],
    "td01",)
    to_do(
    [(st.write, "Have them find multiple fits to the same data and ask them to discuss how to use the set of predictions.")],
    "td02",)
    to_do(
    [(st.write, "Does the perspective of which model realization to use depend on the stakeholder being asked?")],
    "td03",)
    to_do(
    [(st.write, "Ask them which model is the 'best'.  Use this to lead to the idea of goodness of fit.  Calculate the RMSE for several parameter sets.")],
    "td04",)
    to_do(
    [(st.write, "Introduce model likelihood based on inverse of RMSE.  Then explain the likelihood weighted average model result.")],
    "td05",)
    to_do(
    [(st.write, "Discuss why the L-weighted result may be better than any single model (wisdom of the crowd).")],
    "td06",)
    to_do(
     [(st.write, "Introduce Bayes' Law with the level of presentation matched to the students' level and interest.")],
    "td07",)
    to_do(
     [(st.write, "Perhaps introduce the idea that different stakeholders will have a different prior within Bayes' Law depending upon what defines risk and utility for them.")],
    "td08",)
    

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
    
    * Discuss why this Bayesian approach allows for stakeholders to propose many different models for consideration.
"""
)

# If there is time
    # add plots to show utilities for each stakeholder for each fit and for the likelihood weighted average
    # discuss whether stakeholders should use the Lweighted average
        # remember - what is the prior for this model!?
    # discuss why collecting additional data might be useful
    # discuss when you know that you don't need any more data


st.markdown(
    """
    ---
    ### Self-check questions 💦
 
"""
)
st.write('')
st.write('')
question1 = "Thomas Bayes was a professor of hydrogeology at Harvard."
options1 = "False - Bayes was alive before Harvard was founded.", "False - Bayes was alive before hydrogeology became a science.", "False - Bayes was a Presbyterian minister in England."
answer_index1 = 2
stb.single_choice(question1, options1, answer_index1, success='Correct!  Bayes had nothing to do with either Harvard (which existed when he was alive) or hydrogeology (which did not).', error='Incorrect - Bayes did predate modern hydrogeology, but not Harvard.  But we have no record of him being associated with either.', button='Check answer')

st.write('')
st.write('')
question1 = "Bayes' Law is a method to find the best fitting model parameters given data."
options2 = "False - Bayes Law is a way to balance your current belief or understanding with information contained in new data.", "False - Bayes Law has nothing to do with model likelihood weighting, which uses model fit to find the best model parameters.", "False - Bayes' Law has nothing to do with data or models."
answer_index2 = 0
stb.single_choice(question1, options2, answer_index2, success='Correct!  Bayes Law allows you to learn from new data in a rational way.', error='Incorrect - Bayes Law underlies the concept of likelihood weighting, even though it may not be clear to you how from this brief introduction!', button='Check answer')

st.write('')
st.write('')
question3 = "Using likelihood weighting is the same as using the best fit model."
options3 = "True - it is just a better way to figure out which model is best.", "False - likelihood weighting allows you to consider input from many models to form a single prediction.", "False - you don't need to use likelihood weighting if you have a best fit model."
answer_index3 = 1
stb.single_choice(question3, options3, answer_index3, success='Correct! - likelihood weighting produces a single prediction, but it is informed by many models and the available data.', error='Incorrect - likelihood weighting produces a single prediction, but it that prediction is not necessarily associated with any single model.', button='Check answer')

st.write('')
st.write('')
question4 = "Using likelihood weighting is the same as quantifying prediction uncertainty."
options4 = "False - likelihood weighting eliminates prediction uncertainty.", "True - likelihood weighting quantifies and reports prediction uncertainty as its first step.", "False - likelihood weighting produces a compromise prediction, but it does not quantify the uncertainty of that prediction."
answer_index4 = 2
stb.single_choice(question4, options4, answer_index4, success='Correct!  Likelihood weighting can be combined with uncertainty quantification, but they are separate analyses.', error='Incorrect - some of the steps used to develop the likelihood weighted prediction are also used for uncertainty quantification, but no form of averaging can remove that uncertainty.', button='Check answer')

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')