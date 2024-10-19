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


st.title('Finding A Compromise Solution: Mine Dewatering')
st.write('This notebook is designed to guide non-experts through the use of groundwater models to answer a water resources question.')
st.write('')
st.write('It is presented in eight steps, with an assignment given after every second step.')
st.write('')

st.write('Use this slider to choose the step to activate')
st.write('')

a_slider_value=st.slider('Step number', 0,8,0,1,format="%1.0f" )

st.write('')
st.write('')

if a_slider_value==0:

    st.subheader('The Steps')
    st.write('1. General discussion of how surrounding stakeholders might be affected by mine dewatering - qualitative discussion of the response of an aquifer to pumping.')
    st.write('2. Quantitative predictions of drawdown versus distance and time for different Q, T, and S.')
    st.write('3. Convert drawdown to utility for three stakeholders.')
    st.write('4. Introducing Pareto optimization of pumping among stakeholders.')
    st.write('5. Putting Pareto optimization in practice.')
    st.write('6. Perform a pumping test on data with error to infer T and S with uncertainty.')
    st.write('7. Bayesian multimodel analysis.')
    st.write('8. Reality: why these methods are almost never used!')
    st.write('')
    st.write('')
    st.write('')
    
    st.write('')
    st.write('')
    
    st.subheader('The Assignments')
    st.write('Encourage students to read the assignments before they are assigned!')
    st.write('')
    st.write('')
    st.write('**Assignment after step 2.**')
    st.write('Produce three curves of s(t) out to two years, one at the distance relevant for each stakeholder, on the same axes.')
    st.write('Explain in a clear paragraph why they all have the same general shape, but they are different in the details.')
    st.write('Discuss your understanding at this time of the role of a hydrogeologist in negotiating water issues related to dewatering.')
    st.write('')
    st.write('')
    st.write('**Assignment after step 4.**')
    st.write('Plot the utility for the mine against the utility for the town using a point for each dewatering rate considered in class.')
    st.write('Explain the meaning of the Pareto Front.')
    st.write('Choose one pumping rate that is not on the front and explain in a clear paragraph why it is not among the optimal pumping rates.')
    st.write('')
    st.write('')
    st.write('**Assignment after step 6.**')
    st.write('How should each stakeholder decide which fit to trust?')
    st.write('Can you think of an objective way to find the best model?  What are the limitations to this approach?')
    st.write('Can you think of an objective way to use all three models?')
    st.write('Comment on the value of improving data quality for hydrogeologic analyses.')
    st.write('What are the risks or potential costs of poor data quality?')
    st.write('')
    st.write('')
    st.write('**Assignment after step 8.**')
    st.write('Self-reflection – what did you learn in this part of the class?')
    st.write('Do you expect that you might use what you learned in your career?  In your personal life?')
    st.write('How could this section have been improved?')
    st.write('')
    st.write('')



if a_slider_value==1:

    st.subheader('Step 1')
    st.write('Lead a discussion about how dewatering might affect nearby stakeholders.  Good examples include the water supply for a nearby town and a stream that is important to an environmental group.')
    st.write('')
    st.write('Introduce Henry Darcy and show a simplified version of his experiment.  Have students reason their way to Darcys Law.')
    st.write('')
    st.write('Turn the column on its side, explore why the gradient will be constant along the column.')
    st.write('')
    st.write('Convert the column to a constant rectangular cross section.  Then reason through why the gradient would not change along the column.')
    st.write('')
    st.write('Introduce transient flow.  First, show two constant gradient condtions, same inflow H, two different outflow H values.')
    st.write('Reason through how the gradient would change in time from higher to lower inflow H with step change at boundary.')
    st.write('')
    st.write('Convert the column to a decreasing cross sectional area towards outflow.  Then reason through why the gradient would change along the column under steady state flow .')
    st.write('')
    st.write('Show two steady state conditions for column with a decreasing cross sectional area towards outflow with same inflow H, two different outflow H values.')
    st.write('Reason through how the gradient would change in time from higher to lower inflow H with step change at boundary.')
    st.write('')
    st.write('Show a cross section of a well in an aquifer - you decide if you want to show that it is confined for the sake of accuracy versus simplicity.')
    st.write('Draw analogy of radial flow towards a well and decreasing area 1D case shown previously.')
    st.write('')
    st.write('Talk through the transient response of an aquifer to pumping.')
    st.write('')
    st.write('Relate this to distant effects of pumping through time.')
    st.write('')
    st.write('Show a supply well and discuss why a decreased water level could be detrimental.')
    st.write('')
    st.write('Show a groundwater-connected stream and discuss why a decreased water level could be detrimental.')
    st.write('')



if a_slider_value==2:

    fig = plt.figure(figsize=(12,7))

    st.subheader('Step 2')
    st.write('Consider a well pumping at a rate of Q = 250 m3/d')
    st.write('The aquifer has the properties: T = 2.14 e-04 m2/s, S = 9.33 e-06')
    st.write('The far edge of the zone to be dewatered is at a distance r = 100 from the well.')
    st.write('')
    st.write('Use the following tool to answer these questions.')
    st.write('')
    st.write('..........The mine requires a minimum drawdown of 5 m, how long will this take to achieve?')
    st.write('..........The mine requires a maximum drawdown of 8 m, when is this drawdown reached?')
    st.write('')
    st.write('')
    st.write('')
    st.write('Then answer these questions.')
    st.write('')
    st.write('..........How would dewatering impact a town well that is 2500 m from the dewatering well?')
    st.write('..........Should the town object to the dewatering?')
    st.write('')
    st.write('..........How might dewatering impact a stream that is 7500 m from the dewatering well?')
    st.write('..........Should an environmental group object to the dewatering?')
    st.write('')
    st.write('')
    st.write('')
    st.write('Finally, use your results and the tool to address these questions.')
    st.write('')
    st.write('..........How are the drawdown curves at 100, 2500, and 7500 similar and how are they different?')
    st.write('')
    st.write('..........Explore different dewatering pumping rates to see their impacts on the three stakeholders.')
    st.write('')
    st.write('')
    st.write('')

    columns = st.columns((1,1), gap = 'large')
    
    with columns[0]:
        log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
        log_max1 = 0.0  # T / Corresponds to 10^0 = 1
        T_slider_value=st.slider('(log of) Transmissivity in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        T = 10 ** T_slider_value     # Convert the slider value to the logarithmic scale
        st.write("**Transmissivity in m2/s:** %5.2e" %T)

        log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
        log_max2 = 0.0  # S / Corresponds to 10^0 = 1
        S_slider_value=st.slider('(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f" )        
        S = 10 ** S_slider_value       # Convert the slider value to the logarithmic scale
        st.write("**Storativity (dimensionless):** %5.2e" %S)

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

    st.write('')
    st.write('')
    st.write('Assignment after step 2.')
    st.write('Produce three curves of s(t) out to two years, one at the distance relevant for each stakeholder, on the same axes.')
    st.write('Explain in a clear paragraph why they all have the same general shape, but they are different in the details.')
    st.write('Discuss your understanding at this time of the role of a hydrogeologist in negotiating water issues related to dewatering.')
    st.write('')
    st.write('')



if a_slider_value==3:

    fig = plt.figure(figsize=(12,7))

    st.subheader('Step 3')
    st.write('Each stakeholder will place a different value on a given drawdown.')
    st.write('Utility is a way to normalize these values.')
    st.write('')
    st.write('Consider a stakeholder for whom more drawdown is a worse outcome.')    
    st.write('They would assign U=0 to a drawdown associated with the worst outcome ... further drawdown cannot make things any worse.')
    st.write('They would assign U=1 to a drawdown associated with the best outcome ... less drawdown would not make things any better.')
    st.write('')
    st.write('This could be a very complicated function and, in reality, it is very difficult to define.')
    st.write('To get a feel for it, we will use a simple linear function.')
    st.write('')
    st.write('To define the function, you identify the drawdown values that you want to associate with U=0 and U=1.')
    st.write('The utility then varies linearly between these points.')
    st.write('')
    st.write('Note that if the drawdown for U=1 is lower than the drawdown for U=0, then the stakeholder prefers less drawdown.')
    st.write('Conversely if the drawdown for U=1 is higher than the drawdown for U=0, then the stakeholder prefers more drawdown.')
    st.write('')
    st.write('Give it a try for the following conditions.')
    st.write('')
    st.write('A stakeholder decides that U=0 is associated with a drawdown of 0.5 m and U=1 corresponds to a drawdown of 0.05.')
    st.write('')
    st.write('Repeat if a stakeholder decides that U=1 is associated with a drawdown of 0.5 m and U=0 corresponds to a drawdown of 0.05.')
    st.write('')

    st.write('Develop a utility curve for the town and be prepared to explain your choices.')
    st.write('')
    st.write('Develop a utility curve for the environment and be prepared to explain your choices.')
    st.write('')
    st.write('In the previous exercise, you were told that:')
    st.write('')
    st.write('..........The mine requires a minimum drawdown of 5 m and a maximum drawdown of 8 m.')
    st.write('..........Develop a utility curve for the mine.')
    st.write('')
    st.write('..........Discuss why different stakeholders may have a different time at which they would assess utility.')
    st.write('')

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



if a_slider_value==4:

    st.subheader('Step 4')
    st.write('Discuss how stakeholders can use utility to find a compromise decision for the dewatering rate?')
    st.write('')
    st.write('Consider that the values of T, S, and the distances to the stakeholder interests are known and correct.')
    st.write('')
    st.write('Use any tools that have been shown to you previously to explore the utilities of different pumping rates for all stakeholders.')    
    st.write('')
    st.write('You should agree upon the utility curves for each stakeholder before you begin your analyses.')    
    st.write('')
    st.write('You should work as a class, with each person exploring two different Q values that you decide upon collectively.')
    st.write('')
    st.write('Produce a common table with Q and utility for each stakeholder.')
    st.write('')
    st.write('Once you have your table complete, discuss how you can use it to choose the best Q from those that you examined.')
    st.write('')
    st.write('Introduce Pareto optimization generally and discuss how it could be applied to this problem for the mine and the town.')

    st.write('')
    st.write('')
    st.write('Assignment after step 4.')
    st.write('Plot the utility for the mine against the utility for the town using a point for each dewatering rate considered in class.')
    st.write('Explain the meaning of the Pareto Front.')
    st.write('Choose one pumping rate that is not on the front and explain in a clear paragraph why it is not among the optimal pumping rates.')
    st.write('')
    st.write('')




if a_slider_value==5:

    r_preds = np.array([100, 2500, 7500])
    t2 = np.linspace(.1, 10, 100)     # in years


    fig = plt.figure(figsize=(12,7))

    st.subheader('Step 5')
    st.write('Hydrogeological information is usually uncertain.  What is the impact if the T and S values that you assumed were wrong?')
    st.write('')
    st.write('Use this tool to conduct a sensitivity analysis of the impact of S and T values on each stakeholder.')
    st.write('Is there one combination of S and T - high and low - that always produces the highest or lowest drawdown?')
    st.write('Is one parameter always more important than the other?')
    st.write('How should a stakeholder decide whether to use the inferred T or S value or a slightly higher or lower value to account for uncertainty?')
    st.write('')
    st.write('')
    st.write('')

    st.write('We will fix the value of Q=250 m3/d and the distances to the stakeholders as previously defined.')
    Q = 250/24/60/60      #m3/d
    st.write('Consider a maximum and minimum T values to examine.')
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    T_min_slider_value=st.slider('Lower (log of) Transmissivity in m2/s', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
    T_min_value = 10 ** T_min_slider_value     # Convert the slider value to the logarithmic scale
    T_max_slider_value=st.slider('Higher (log of) Transmissivity in m2/s', T_min_slider_value,log_max1,(T_min_slider_value+log_max1)/2,0.01,format="%4.2f" )
    T_max_value = 10 ** T_max_slider_value     # Convert the slider value to the logarithmic scale
    st.write('')
    st.write('')

    st.write('Consider a maximum and minimum S values to examine.')
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    S_min_slider_value=st.slider('Lower (log of) Storativity - unitless', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
    S_min_value = 10 ** S_min_slider_value     # Convert the slider value to the logarithmic scale
    S_max_slider_value=st.slider('Higher (log of) Storativity - unitless', S_min_slider_value,log_max1,(S_min_slider_value+log_max1)/2,0.01,format="%4.2f" )
    S_max_value = 10 ** S_max_slider_value     # Convert the slider value to the logarithmic scale
    S_values =  10 ** np.linspace(S_min_slider_value, S_max_slider_value, 5)
    st.write('')
    st.write('')

    st.write('Choose a stakeholder: 0=mine, 1=town, 2=environment.')
    stakeholder_slider_value=st.slider('Stakeholder', 0,2,1,format="%4.0f" )
    r = r_preds[stakeholder_slider_value]
    st.write('')
    st.write('')

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
    plt.legend()
    
    st.pyplot(fig)

    fig = plt.figure(figsize=(12,7))

    st.write('')

    st.write('Use the following tool to explore how stakeholders can use hydrogeology to choose an optimal dewatering Q.')
    st.write('')
    st.write('As a class, you should agree on the utility curves for each stakeholder.')
    st.write('')

    columns = st.columns((1,1), gap = 'large')
    
    with columns[0]:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        s_min = 0.0 # T / Corresponds to 10^-7 = 0.0000001
        s_max = 10.0  # T / Corresponds to 10^0 = 1
        mine_s_U0_value=st.slider('Dradown associated with U=0 for the mine', s_min,s_max,5.,0.01,format="%4.2f" )        
        mine_s_U1_value=st.slider('Dradown associated with U=1 for the mine', s_min,s_max,8.,0.01,format="%4.2f")
        if mine_s_U0_value == mine_s_U1_value:
            mine_s_U0_value = mine_s_U1_value + 0.1
        mine_t_value=st.slider('Time at which utility is determined for the mine in years', 0.,9.9,1.,0.1,format="%4.1f")
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        town_s_U0_value=st.slider('Dradown associated with U=0 for the town', s_min,s_max,4.5,0.01,format="%4.2f" )        
        town_s_U1_value=st.slider('Dradown associated with U=1 for the town', s_min,s_max,1.,0.01,format="%4.2f")    
        if town_s_U0_value == town_s_U1_value:
            town_s_U0_value = town_s_U1_value + 0.1
        town_t_value=st.slider('Time at which utility is determined for the town in years', 0.,9.9,5.,0.1,format="%4.1f")
        st.write('')
        st.write('')
        st.write('')
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
    plt.legend()
    
    st.pyplot(fig)
    
    st.write('')
    st.write('')
    st.write('Now choose a common S and T pair.')    
    st.write('')
    st.write('Work together to determine the utility for each stakeholder over at least 20 pumping rates.')    
    st.write('Create a table with Q listed against the utilities.')    
    st.write('')
    st.write('Plot the matched utilities for the town against those of the mine.')    
    st.write('')
    st.write('Be prepared to explain how this plot can be used for Pareto optimization.')
    st.write('')
    st.write('Repeat the exercise for a different S and T pair.')
    st.write('')
    st.write('Is the optimal pumping rate the same for both S and T pairs?')
    st.write('')
    st.write('')

    Q_temp=st.slider('Pumping rate', 10.,400.,200.,10.,format="%4.0f" )
    Q = Q_temp / 24 / 60 / 60
    st.write('')
    st.write('')
    
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    T_min_slider_value1=st.slider('(log of) Transmissivity in m2/s', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
    T = 10 ** T_min_slider_value1
    st.write('')
    st.write('')

    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
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
    plt.legend()
    
    st.write("The utility for the mine at the assessment time is:  %5.2f" %u_mine)
    st.write("The utility for the town at the assessment time is:  %5.2f" %u_town)
    st.write("The utility for the environment at the assessment time is:  %5.2f" %u_env)
    
    st.pyplot(fig)
    

    st.write('')
    st.write('')
    st.write('Finally, consider this tradeoff curve made for the mine and the town for multiple Q values.')    
    st.write('')
    st.write('Change T and S to see how it impacts the Pareto optimal designs.')    
    st.write('')
    st.write('Plot the matched utilities for the town against those of the mine.')    
    st.write('')
    st.write('Be prepared to explain how this plot can be used for Pareto optimization.')
    st.write('')
    st.write('Repeat the exercise for a different S and T pair.')
    st.write('')
    st.write('Is the optimal pumping rate the same for both S and T pairs?')
    st.write('')
    st.write('')

    st.write('Pumping rates will be examined ranging linearly from the min and max that you choose.')
    Q_min_value=st.slider('Minimum pumping rate to consider', 10.,400.,20.,10.,format="%4.1f" )
    Q_max_value=st.slider('Maximum pumping rate to consider', Q_min_value+10.,500.,325.,10.,format="%4.1f" )
    Q_values = np.linspace(Q_min_value, Q_max_value, 50)
    Q_values = Q_values / 24. / 60. / 60.
    st.write('')
    st.write('')
    
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    T_min_slider_value2=st.slider('Choose (log of) Transmissivity in m2/s', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
    T = 10 ** T_min_slider_value2
    st.write('')
    st.write('')

    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    S_min_slider_value2=st.slider('Choose (log of) Storativity - unitless', log_min1,0.9*log_max1,(log_min1+0.9*log_max1)/2,0.01,format="%4.2f" )
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

    st.write('')
    st.write('')
    st.write('How can you combine these two tradeoff plots to identify the optimal pumping rate?')    
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    st.write('')
    st.write('')
    st.write('What if we optimize based on the total utility?')    
    st.write('')
    st.write('')
    u_sum = u_mine + u_town + u_env
    fig = plt.figure(figsize=(12,7))
    plt.plot(Q_values* 24. * 60. * 60., u_sum, marker='o', color='r',linestyle ='None', label=r'Total')
    plt.plot(Q_values* 24. * 60. * 60., u_mine, marker='o', color='b',linestyle ='None', label=r'Mine')
    plt.plot(Q_values* 24. * 60. * 60., u_mine + u_town, marker='o', color='g',linestyle ='None', label=r'Mine+Town')
    plt.xlabel(r'Dewatering rate', fontsize=14)
    plt.ylabel(r'Sum of utilities', fontsize=14)
    plt.legend()
    st.pyplot(fig)
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    st.write('')
    st.write('')
    st.write('What if we optimize based on the variance of utility?')    
    st.write('')
    st.write('')
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

    st.write('')
    st.write('')
    st.write('What if tried to find the point with the highest minimum utiility across stakeholders?')    
    st.write('')
    st.write('')
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


  
if a_slider_value==6:

    st.write('A pumping well was operated for 2 days at a rate of 25 m3/d and the drawdown was measured at a monitoring well 25 m from the pumped well.')

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


if a_slider_value==7:

    st.write('Start from fitting three curves, as you did at the end of the last exercise.')
    st.write('- you have a head start this time!')

    t2 = np.linspace(.1, 2, 12)     # in days
    Q_test=25
    Q_test = Q_test / 24. / 60. / 60.
    st.write('')
    st.write('')
    T_test = 3.2 * 10**-4
    S_test = 2.1 * 10**-3
    r_test = 25

    s_test = compute_s(T_test, S_test, t2*24 *60 *60, Q_test, r_test)   # in 

    st.write('')
    st.write('')
    st.write('Now find three reasonable fits to noisy data.  Fit T and S.')
    st.write('')
    st.write('')
    
    s_error = np.random.normal(loc=0.0, scale=0.02, size=len(s_test))
    s_noisy = s_test + s_error

    log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
    T_min_slider_value_fit1=st.slider('First (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,-3.37,0.01,format="%4.2f" )
    T_fit1 = 10 ** T_min_slider_value_fit1
    st.write('')
    st.write('')

    S_min_slider_value_fit1=st.slider('First (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,-3.19,0.01,format="%4.2f" )
    S_fit1 =  10 ** S_min_slider_value_fit1

    s_fit_noisy1 = compute_s(T_fit1, S_fit1, t2*24 *60 *60, Q_test, r_test)   # in 

    log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
    T_min_slider_value_fit2=st.slider('Second (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,-3.61,0.01,format="%4.2f" )
    T_fit2 = 10 ** T_min_slider_value_fit2
    st.write('')
    st.write('')

    S_min_slider_value_fit2=st.slider('Second (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,-2.48,0.01,format="%4.2f" )
    S_fit2 =  10 ** S_min_slider_value_fit2

    s_fit_noisy2 = compute_s(T_fit2, S_fit2, t2*24 *60 *60, Q_test, r_test)   # in 

    log_min_fit = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max_fit = 0.0  # T / Corresponds to 10^0 = 1
    T_min_slider_value_fit3=st.slider('Third (log of) Transmissivity in m2/s', log_min_fit,0.9*log_max_fit,-3.5,0.01,format="%4.2f" )
    T_fit3 = 10 ** T_min_slider_value_fit3
    st.write('')
    st.write('')

    S_min_slider_value_fit3=st.slider('Third (log of) Storativity - unitless', log_min_fit,0.9*log_max_fit,-2.6,0.01,format="%4.2f" )
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
    st.write('')   
    
    diff_model1 = s_fit_noisy1 - s_test
    se_model1 = diff_model1**2
    rmse_model1 = np.sqrt(np.sum(se_model1))/len(s_test)

    diff_model2 = s_fit_noisy2 - s_test
    se_model2 = diff_model2**2
    rmse_model2 = np.sqrt(np.sum(se_model2))/len(s_test)

    diff_model3 = s_fit_noisy3 - s_test
    se_model3 = diff_model3**2
    rmse_model3 = np.sqrt(np.sum(se_model3))/len(s_test)

    st.write("The Root Mean Square Errors for the model1 is:  %7.4f" %rmse_model1)
    st.write("The Root Mean Square Errors for the model1 is:  %7.4f" %rmse_model2)
    st.write("The Root Mean Square Errors for the model1 is:  %7.4f" %rmse_model3)

    L_model1 = 1/rmse_model1
    L_model2 = 1/rmse_model2
    L_model3 = 1/rmse_model3
    L_sum = (L_model1 + L_model2 + L_model3)
    L_model1 = L_model1/L_sum
    L_model2 = L_model2/L_sum
    L_model3 = L_model3/L_sum
    
    st.write('')
    st.write('')
    st.write("The likelihood of model1 is:  %7.4f" %L_model1)
    st.write("The likelihood of model2 is:  %7.4f" %L_model2)
    st.write("The likelihood of model3 is:  %7.4f" %L_model3)

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
    s_Lw_mine = s_test_mine1 * L_model1 + s_test_mine2 * L_model2 + s_test_mine3 * L_model3   
    fig = plt.figure(figsize=(12,7))
    plt.plot(t2, s_test_mine1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
    plt.plot(t2, s_test_mine2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
    plt.plot(t2, s_test_mine3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
    plt.plot(t2, s_Lw_mine, linewidth=3., color='r', linestyle ='dashed', label=r'Lw')
    plt.xlabel(r'Time, years', fontsize=14)
    plt.ylabel(r'Drawdown at the mine', fontsize=14)
    plt.legend()
    st.pyplot(fig)

    s_test_town1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
    s_test_town2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
    s_test_town3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[1])   # in 
    s_Lw_town = s_test_town1 * L_model1 + s_test_town2 * L_model2 + s_test_town3 * L_model3   
    fig = plt.figure(figsize=(12,7))
    plt.plot(t2, s_test_town1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
    plt.plot(t2, s_test_town2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
    plt.plot(t2, s_test_town3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
    plt.plot(t2, s_Lw_town, linewidth=3., color='r', linestyle ='dashed', label=r'Lw')
    plt.xlabel(r'Time, years', fontsize=14)
    plt.ylabel(r'Drawdown at the town', fontsize=14)
    plt.legend()
    st.pyplot(fig)
    st.write('')
    st.write('')

    s_test_env1 = compute_s(T_fit1, S_fit1, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
    s_test_env2 = compute_s(T_fit2, S_fit2, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
    s_test_env3 = compute_s(T_fit3, S_fit3, t2*365 *24 *60 *60, 250 / 24. / 60. / 60., r_preds[2])   # in 
    s_Lw_env = s_test_env1 * L_model1 + s_test_env2 * L_model2 + s_test_env3 * L_model3       
    fig = plt.figure(figsize=(12,7))
    plt.plot(t2, s_test_env1, linewidth=3., color='b', linestyle ='solid', label=r'Model_1')
    plt.plot(t2, s_test_env2, linewidth=3., color='g', linestyle ='solid', label=r'Model_2')
    plt.plot(t2, s_test_env3, linewidth=3., color='k', linestyle ='solid', label=r'Model_3')
    plt.plot(t2, s_Lw_env, linewidth=3., color='r', linestyle ='dashed', label=r'Lw')
    plt.xlabel(r'Time, years', fontsize=14)
    plt.ylabel(r'Drawdown at the env', fontsize=14)
    plt.legend()
    st.pyplot(fig)

    st.write('')
    st.write('')
    st.write('Explore the parameter estimations.')
    st.write('Does a poorly fitted model have much impact on the likelihood-weighted predictions?')
    st.write('Discuss why this Bayesian approach helps to guard against erroneous fitting of a model to data.')
    st.write('')
    st.write('')
    st.write('')



# If there is time
    # add plots to show utilities for each stakeholder for each fit and for the likelihood weighted average
    # discuss whether stakeholders should use the Lweighted average
        # remember - what is the prior for this model!?
    # discuss why collecting additional data might be useful
    # discuss when you know that you don't need any more data
    
            
     
if a_slider_value==8:

    st.write('Outline, in bullet form, what you have learned in this part of the class.')
    st.write('')
    st.write('How do you imagine that what you have learned might influence your professional life?')
    st.write('')
    st.write('How do you imagine that what you have learned might influence your personal life?')
    st.write('')
    st.write('What was the most effective element of this part of the course?')
    st.write('')
    st.write('What could be improved?')
    st.write('')


    # technical text moved here    
    st.write(' ')
    st.write('---------------------------------------------------------------------------------------------')
    st.subheader('For those of you who are interested ... here is the math!')
    st.write(' ')
    st.title('Theis drawdown prediction - Fitting Formation parameter to measured data')
    st.write('This notebook demonstrate the application of the Theis principle for pumping test evaluation in confined, transient setups. The notebook is based on an Spreadsheet from Prof. Rudolf Liedl.')
    
    st.subheader('General situation')
    st.write('We consider a confined aquifer with constant transmissivity. If a well is pumping water out of the aquifer, radial flow towards the well is induced.')
    st.write('The calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined aquifer without further sinks and sources:')
    st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
    
    st.subheader('Mathematical model and solution')
    st.write('Charles V. Theis presented a solution for this by deriving')
    st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
    st.write('with the well function')
    st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
    st.write('and the dimensionless variable')
    st.latex(r'''u = \frac{Sr^2}{4Tt}''')
    st.write('This equations are not easy to solve. Historically, values for the well function were provided by tables or as so called type-curve. The type-curve matching with experimental data for pumping test analysis can be considered as one of the basic hydrogeological methods. However, modern computer provide an easier and more convinient way to solve the 1D radial flow equation based on the Theis approach. Subsequently, the Theis equation is solved with Python routines.')
