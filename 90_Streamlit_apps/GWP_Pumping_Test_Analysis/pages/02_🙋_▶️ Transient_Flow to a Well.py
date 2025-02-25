# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button
from streamlit_extras.stodo import to_do


st.title('🙋 Transient Flow toward a well in a confined aquifer')

st.header(':blue[Conceptualizing the response of a confined aquifer to pumping]')

st.subheader(':blue-background[Guidance and instructions for your own investigation]', divider="blue")
st.markdown('''
            Transient Flow toward a well in a confined aquifer is described here using the Theis Solution. You can use the subsequent instructions and the interactive plot to gain a profound understanding of the system behavior. 
            
            To start your investigation of the topic it is useful to think about the system using this **initial assessment**.
            '''
)
# Initial assessment
   
with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1,1))
    
    with columnsQ1[0]:
        stb.single_choice(":blue[**What conditions are applicable for use of the Theis equaiton?**]",
                  ["Steady state flow, confined aquifer", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT! The Theis Solution describes transeint flow to a well in a confined aquifer.', error='This is not correct ... You can learn more about the Theis Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 8](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
        stb.single_choice(":blue[**If there is no recharge to an aquifer how does the cone of depression behave with ongoing time?**]",
                  ["The cone of depression will reach a steady state", "The cone of depression continue to increase", "The cone of depression is not dependent on time", "The cone of depression will decrease"],
                  1,success='CORRECT! Without recharge, the cone of depression will increase.', error='This is not correct ... Without recharge, the cone of depression will increase with ongoing time. You can explore this by using the interactive tool to investigate this behavior. Feel free to answer again.') 
    with columnsQ1[1]:
        stb.single_choice(":blue[**How does storativity (_S_) influence the response of an aquifer to pumping?**]",
                  ["A higher storativity results in a slower drawdown response", "A higher storativity leads to more rapid flow to the well", "Storativity only affects steady-state conditions", "Storativity is not relevant for confined aquifers"],
                  0,success='CORRECT! A higher storativity results in a slower drawdown response', error='This is not correct ... You can use the interactive tool to explore this and learn more about Storativity [by downloading the book: Basic Hydrogeology - An Introduction to the Fundamentals of Groundwater Science​ and reading Section 5.3](https://gw-project.org/books/basic-hydrogeology/). Feel free to answer again.')  
        stb.single_choice(":blue[**Which of the following statements describes the drawdown at a point due to pumping in a confined aquifer?**]",
                  ["It decreases with time", "It increases with time", "It remains constant over time", "It is independent of the pumping rate"],
                  1,success='CORRECT! Drawdown continues to increase with time as pumping continues', error='This is not correct ...  You can use the interactive tool to explore this. Feel free to answer again.')

# Create ToDos to proceed with the steps of the exercise
st.markdown("""
            **STEP 1:**
            First we investigate drawdown around a pumping well in response to water abstraction as function of space and time.
           
           _This can be accomplished by adjusting the interactive inputs for the graphs to observe changes in drawdown as follows._
           """)
with st.expander(":blue[**To proceed with detailed instruction for Exercise  1**] click here"):
    to_do(
        [(st.write, "Increase Pumping rate _Q_. How do graphs and printout of drawdown change? Then, decrease pumping rate. How do drawdowns change? ")],"td01",)
    to_do(
        [(st.write, "Increase the observation 'Distance _r_ in meters' (middle column). How do graphs and values printed below the graphs change? Then, decrease the observation distance. How do drawdowns change?")], "td02",)
    to_do(
        [(st.write, "Increase the obervation 'Time _t_ in seconds' (middle column). How do the graphs and values printed below the graphs change? Then, decrease the observation time. How do drawdowns change?")], "td03",)

st.markdown("""
            **STEP 2:**
            Next, we investigate the sensitivity of drawdown caused by abstraction to changes in Transmissivity _T_ and storativity _S_.
            
           _This can be accomplished by adjusting the interactive inputs for the graphs to observe changes in drawdown as follows._
           """)
with st.expander(":blue[**To proceed with detailed instruction for Exercise  2**] click here"):
    to_do(
        [(st.write, "Modify the Transmissivity (third column). What happens?")],"td04",)
    to_do(
        [(st.write, "Modify the Storativity (third column). What happens?")], "td05",)

st.markdown("""
            **STEP 3:**
            The graphs can be used to compare drawdown for two different sets of Transmissivity and Storativity. 
            
           _This can be accomplished by turning on the toggle for 'Second set of _T_ and _S_ for comparison' and adjusting the interactive inputs for _T2_ and _S2_ that appear in the thrid column of inptus._
           """)
with st.expander(":blue[**To proceed with detailed instruction for Exercise  3**] click here"):
    to_do(
        [(st.write, "Toggle 'Second set of _T_ and _S_ for comparison' to the ON position (it will turn red). New data inputs will appear in the third column but the graphs will not change because the two data sets are identical.")],"td06",)
    to_do(
        [(st.write, "Choose a lower value for transmissivity _T2_ and compare the graph with the initial graph. Then choose a higher value for _T2_ and compare.")], "td07",) 
    to_do(
        [(st.write, "Choose a lower value for storativity _S2_ and compare the graph with the initial graph. Then choose a higher value for _S2_  compare.")], "td08",)        
"---"
st.subheader(':blue-background[Computation of drawdown]', divider="blue")
st.markdown('''
            The interactive graphs shown below demonstrate the response of a confined aquifer to pumping as described by the Theis Solution. The parameter values can be modified using the sliders. A toggle allows viewing of graphs for two sets of Transmissivity and Storativity at once. You can follow the exercises provided above, or explore on your own.
            '''
)

# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis
# (Here, the method computes the data for the well function. Those data can be used to generate a type curve.)

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s
    
# Fixed values
u_max = 1
r_max = 10000
u  = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]

max_s = 20
max_r = 1000

   
# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1
   
columns = st.columns((1,1,1), gap = 'large')

with columns[0]:
    with st.expander('Pumping rate, distance and time to plot'):
        Q = st.slider(f'**Pumping rate _Q_ (m³/s)**', 0.001,0.03,0.000,0.001,format="%5.3f")
        r_show = st.slider(f'**Distance _r_ in meters**',0,1000,100,1)
        t_show = st.slider(f'**Time _t_ in seconds**',0.001,86400.*7,86400.,600.,format="%5.0f")
    comparison = st.toggle('Second set of _T_ and _S_ for comparison')
with columns[1]:
    #Logaritmic T-Slider
    container = st.container()
    T_slider_value=st.slider('_(log of) Transmissivity T_', log_min1,log_max1,-3.0,0.01,format="%4.2f", key='T1' )
    T = 10 ** T_slider_value
    container.write("**_T_ in m²/s:** %5.2e" %T)
    #Logaritmic S-Slider
    container = st.container()
    S_slider_value=st.slider('_(log of) Storativity S_', log_min2,log_max2,-4.0,0.01,format="%4.2f", key='S1' )
    S = 10 ** S_slider_value
    container.write("**_S_ (dimensionless):** %5.2e" %S)    
with columns[2]:
    
    if comparison:
        container = st.container()
        T2_slider_value=st.slider('_(log of) Transmissivity T2_', log_min1,log_max1,-3.0,0.01,format="%4.2f", key='T2' )
        T2 = 10 ** T2_slider_value
        container.write("**_T2_ in m²/s:** %5.2e" %T2)
        #Logaritmic S-Slider
        container = st.container()
        S2_slider_value=st.slider('_(log of) Storativity S2_', log_min2,log_max2,-4.0,0.01,format="%4.2f", key='S2' )
        S2 = 10 ** S2_slider_value
        container.write("**_S2_ (dimensionless):** %5.2e" %S2)
        
    
# Range of temporal / spatial coordinate
r = np.linspace(1, max_r, 200)
r_neg = r * -1.0
t = np.linspace(1, 604800, 200)

# Compute drawdown for  1 and 2
s1 = compute_s(T, S, t_show, Q, r)
s2  = compute_s(T, S, t, Q, r_show)
if comparison:
    # Compute drawdown for  1_2
    s1_2 = compute_s(T2, S2, t_show, Q, r)
    s2_2 = compute_s(T2, S2, t, Q, r_show)

# Compute drawdown for a specific point
x_point = r_show
y_point = compute_s(T, S, t_show, Q, r_show)
x2_point = t_show
y2_point = compute_s(T, S, t_show, Q, r_show)

# Plotting and printing of results
fig=plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)    
plt.title('Drawdown vs Distance at seconds =  %8i' %x2_point, fontsize=16)
plt.plot(r, s1, linewidth=1., color='b', label=r'drawdown prediction')
plt.plot(r_neg, s1, linewidth=1, color='b')
if comparison:
    plt.plot(r, s1_2, linewidth=1., color='black', label=r'comparison', linestyle='dashed')
    plt.plot(r_neg, s1_2, linewidth=1, color='black', linestyle='dashed')
plt.fill_between(r,s1,max_s, facecolor='lightblue')
plt.fill_between(r_neg,s1,max_s, facecolor='lightblue')
plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='drawdown plotted & printed below graph') 
plt.xlabel(r'Distance from well in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.title('Drawdown vs Time at meters =  %8i' %x_point, fontsize=16)
plt.plot(t, s2, linewidth=1., color='r', label=r'drawdown prediction')
if comparison:
    plt.plot(t, s2_2, linewidth=1., color='black', label=r'drawdown prediction', linestyle='dashed')
plt.fill_between(t,s2,max_s, facecolor='mistyrose')
plt.plot(x2_point,y2_point, marker='o', color='b',linestyle ='None', label='drawdown ') 
plt.xlim(0, 86400*7)
plt.ylim(max_s,-5)
plt.xlabel(r'time in s', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.xticks(np.arange(0, 7*86400, step=86400))  # Set label locations.
plt.legend()
plt.grid(True)

st.pyplot(fig)

st.write('**Drawdown**  =  %5.2f' %y_point, ' m at _r_ = %8.2f' %x_point, ' m and time =  %8i' %x2_point, ' sec')

st.subheader(':blue-background[Continued investigation]', divider="blue")
st.markdown('''
            Having gained an overview of the interactive graphs, we move on to exploring the system more in detail as guided by the following questions.
            '''
)
# Second assessment

with st.expander(":green[**Show/Hide the second assessment**]"):
    # Assessment to guide users through the interactive plot
    stb.single_choice(":blue[**How does the drawdown change at one specific distance from the well if storativity is decreased**]",
                  ["Drawdown is less", "Drawdown is more", "Drawdown is not affected"],
                  1,success='CORRECT!  ... when all else is equal, a lower value of storativity wil result in more drawdown.', error='This is not correct ...  You can use the interactive tool to explore this and learn more about Storativity [by downloading the book: Basic Hydrogeology - An Introduction to the Fundamentals of Groundwater Science​ and reading Section 5.3](https://gw-project.org/books/basic-hydrogeology/). Feel free to answer again.')
    stb.single_choice(":blue[**If the estimated transmissivity _T_ is too low, how will the predicted drawdown compare to the true drawdown?**]",
                  ["The predicted drawdown will be too small", "The predicted drawdown will remain unchanged", "The predicted drawdown will be too large", "The predicted drawdown will be too large close to the well and too small far from the well"],
                  3,success='CORRECT! ... the low transmissivity will require a higher gradient to accomodate flow through the aquifer surrounding the well screen, so predicted drawdown will be larger than true drawdown near the well. This results in more of the pumped volume being extracted from storage near the well bore, thus less of the volume will be drawn from storage further away resulting in less drawdown at larger distances from the well. It may not be possible to observe this on the application graph for every combination of parameter values entered in this application because the r distance on the graph is limited to 1000 m and the distance where drawdown transitions from overestimation to underestimation may be further than 1000 m from the well. If you are unable to see the transition, then decreasing the values input for time and/or distance might bring the transition zone into view.', error='This is partially correct because the low transmissivity will require a higher gradient to accomodate flow through the aquifer surrounding the well screen, so predicted drawdown will be larger than true drawdown near the well. This results in more of the pumped volume being extrated from storage near the well bore, thus less of the volume will be drawn from storage further away resulting in less drawdown at larger distances from the well. At some location depending on the combination of parameter values the drawdown may be the same for both cases. It may not be possible to observe this on the application graph for every combination of parameter values entered in this application because the r distance is limited to 1000 m and the distance where drawdown transitions from overestimation to underestimation may be further away than 1000 m. If that is the case, decresing the values input for time and/or distance might bring the transition zone into view. Feel free to answer again.')

st.subheader(':blue-background[Intermediate conclusion and next steps]', divider="blue")
st.markdown('''
            Thus far, we investigated flow to a well in a confined aquifer, and showed the Theis solution can be used to calculate drawdown in response to pumping for a specific place and time.
            
            The next part of this application demonstrates how to estimate aquifer parameter values using drawdown data measured near a pumping well. You can move to the next section using either the side menu or the navigation buttons at the bottom of this page.
            '''
)
"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1))
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/01_📃_Theory.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/03_🟠_▶️ Theis_solution.py")
