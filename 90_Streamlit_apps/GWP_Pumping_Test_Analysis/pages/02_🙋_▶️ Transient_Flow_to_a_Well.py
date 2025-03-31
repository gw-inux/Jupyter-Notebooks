# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button
from streamlit_extras.stodo import to_do

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title('🙋 Transient Flow toward a well in a confined aquifer')

st.header(':blue[Conceptualizing the drawdown response to pumping in a confined aquifer]')

st.subheader(':blue-background[Guidance for investigation]', divider="blue")
st.markdown('''
            Transient Flow toward a well in a confined aquifer is described here using the Theis Solution. You can use the subsequent instructions and the interactive plot to gain an understanding of the system behavior. 
            
            When starting an investigation of this topic it is useful to think about the system using this **initial assessment**.
            '''
)
# Initial assessment
   
with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1,1))
    
    with columnsQ1[0]:
        stb.single_choice(":blue[**What conditions are applicable for use of the Theis equaiton?**]",
                  ["Steady state flow, confined aquifer", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT! The Theis Solution describes transient flow to a well in a confined aquifer.', error='This is not correct ... You can learn more about the Theis Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 8](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
        stb.single_choice(":blue[**If there is no recharge to an aquifer how does the cone of depression behave with ongoing time?**]",
                  ["The cone of depression will reach a steady state", "The cone of depression continue to increase", "The cone of depression is not dependent on time", "The cone of depression will decrease"],
                  1,success='CORRECT! Without recharge, the cone of depression will increase.', error='This is not correct ... Without recharge, the cone of depression will increase with ongoing time. You can explore this by using the interactive tool to investigate this behavior. Feel free to answer again.') 
    with columnsQ1[1]:
        stb.single_choice(":blue[**How does storativity ($S$) influence the response of an aquifer to pumping?**]",
                  ["A higher storativity results in a slower drawdown response", "A higher storativity leads to more rapid flow to the well", "Storativity only affects steady-state conditions", "Storativity is not relevant for confined aquifers"],
                  0,success='CORRECT! A higher storativity results in a slower drawdown response', error='This is not correct ... You can use the interactive tool to explore this and learn more about Storativity [by downloading the book: Basic Hydrogeology - An Introduction to the Fundamentals of Groundwater Science​ and reading Section 5.3](https://gw-project.org/books/basic-hydrogeology/). Feel free to answer again.')  
        stb.single_choice(":blue[**Which of the following statements describes the drawdown at a point due to pumping in a confined aquifer?**]",
                  ["It decreases with time", "It increases with time", "It remains constant over time", "It is independent of the pumping rate"],
                  1,success='CORRECT! Drawdown continues to increase with time as pumping continues', error='This is not correct ...  You can use the interactive tool to explore this. Feel free to answer again.')

# Create ToDos to proceed with the steps of the exercise
st.markdown("""
            **STEP 1:**
            First we investigate drawdown around a pumping well in response to water abstraction as a function of space and time.
                       
           _This can be accomplished by adjusting the interactive inputs (using a slider or a typed number, depending on the toggle switch) for the graphs in the section below titled "Computation of drawdown" to observe changes in drawdown as is described for Exercise 1 below._
           
           **This specific case is conceptualized as a thin confined aquifer with initial head 20 meters above its top, so if the parameter values result in drawdown of 20 meters or more at the pumping well, then a portion of the graphs will be white, indicating the results are NOT VALID.**
           """)
with st.expander(":blue[**To proceed with detailed instruction for Exercise  1**] click here"):
    to_do(
        [(st.write, "Increase the Pumping rate $Q$. How do the graphs and the value of drawdown printed below the graphs change? Next, decrease the Pumping rate. How does drawdown change? ")],"td01",)
    to_do(
        [(st.write, "Increase the distance of the observation from the well 'Distance $r$ in meters'. The location, time, and the magnitude of drawdown are indicated by the dots on the graphs and their values are printed below the graphs. How do they change? Then, decrease the observation distance. How does drawdown change?")], "td02",)
    to_do(
        [(st.write, "Increase the time after pumping begins that the observation is made 'Time $t$ in seconds'. The location, time, and the magnitude of drawdown are indicated by the dots on the graphs and their values are printed below the graphs. How does drawdown change? Then, decrease the observation time. How does drawdown change?")], "td03",)

st.markdown("""
            **STEP 2:**
            Next, we investigate the sensitivity of drawdown caused by abstraction to changes in Transmissivity $T$ and Storativity $S$.
            
           _This can be accomplished by adjusting the interactive inputs for the graphs to observe changes in drawdown as follows._
           """)
with st.expander(":blue[**To proceed with detailed instruction for Exercise  2**] click here"):
    to_do(
        [(st.write, "Modify the Transmissivity (second input column). What happens?")],"td04",)
    to_do(
        [(st.write, "Modify the Storativity (second input column). What happens?")], "td05",)

st.markdown("""
            **STEP 3:**
            The graphs can be used to compare drawdown for two different sets of Transmissivity and Storativity. 
            
           _This can be accomplished by turning on the toggle for 'Second set of $T$ and $S$ for comparison' and adjusting the interactive inputs for $T2$ and $S2$ that appear in a third column of inputs._
           """)
with st.expander(":blue[**To proceed with detailed instruction for Exercise  3**] click here"):
    to_do(
        [(st.write, "For a given selection of values for $Q$, $r$, and $t$, toggle 'Second set of $T$ and $S$ for comparison' to the ON position (it will turn red). New data inputs will appear in a third column. When the values  of $T$ and $T2$ and/or $S$ and $S2$ differ, two sets of curves will appear. Only one curve will appear on each graph if the values are the same because the drawdowns will be identical. If there is no drawdown, check to see if the pumping rate $Q$ is 0")],"td06",)
    to_do(
        [(st.write, "Choose a lower value for transmissivity $T2$ and compare the curve with the curve for the initial value of $T$. Then choose a value for $T2$ that is higher than $T$ and compare.")], "td07",) 
    to_do(
        [(st.write, "Toggle the 'Second set of $T$ and $S$ for comparison' to the OFF position and then back ON in order to reset the values to your initial values. Then, choose a lower value for storativity $S2$ and compare the curve with the curve for the initial value of $S$. Then choose a value for $S2$ that is higher than $S$ and compare.")], "td08",)        
"---"
st.subheader(':blue-background[Computation of drawdown]', divider="blue")
st.markdown('''
            The interactive graphs shown below demonstrate the response of a confined aquifer to pumping as described by the Theis Solution. The parameter values can be modified using the sliders. A toggle allows viewing of graphs for two sets of Transmissivity and Storativity at once. You can follow the exercises provided above, or explore on your own.
            
           **If the graphs are completely white with no curves, it is likely that the selected parameters have caused unreasonably large drawdown (greater than the 20-meters which in this case would indicate and impossible situation because the initial water level is only 20 meters above the top of a thin confined aquifer. Checking the values of drawdown, distance, and time printed below the graphs and adjust the inputs until drawdown is less than 20 meters.**
            
            **If the drawdown is zero, check the pumping rate $Q$ to be sure it is greater than zero.**
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
    
    
# Callback function to update session state
def update_T():
    st.session_state.T_slider_value = st.session_state.T_input
def update_S():
    st.session_state.S_slider_value = st.session_state.S_input
def update_T2():
    st.session_state.T2_slider_value = st.session_state.T2_input
def update_S2():
    st.session_state.S2_slider_value = st.session_state.S2_input
def update_Q():
    st.session_state.Q = st.session_state.Q_input
    
# Initialize session state for value and toggle state
st.session_state.T_slider_value = -3.0
st.session_state.S_slider_value = -4.0
st.session_state.T2_slider_value = -3.0
st.session_state.S2_slider_value = -4.0
st.session_state.Q = 0.000
st.session_state.number_input = False  # Default to number_input

# Fixed values
u_max = 1
r_max = 10000
u  = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]

max_s = 20
max_r = 1000

# Define the part of the code that is re-run with each user interaction

@st.fragment
def transient_flow_well():
    # Get input data
    # Define the minimum and maximum for the logarithmic scale 
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
    log_max2 = 0.0  # S / Corresponds to 10^0 = 1
       
    # Toggle to switch between slider and number-input mode
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $T$ and $S$") 
       
    columns = st.columns((1,1,1), gap = 'medium')
    with columns[0]:
        if st.session_state.number_input:
            Q = st.number_input(f'**Pumping rate $Q$ (m³/s)**', 0.000,0.03,st.session_state["Q"],0.001,format="%5.3f", key="Q_input", on_change=update_Q)
        else:
            Q = st.slider(f'**Pumping rate $Q$ (m³/s)**', 0.000,0.03,st.session_state["Q"],0.001,format="%5.3f", key="Q_input", on_change=update_Q)
        r_show = st.slider(f'**Distance $r$ in meters**',0,1000,100,1)
        t_show = st.slider(f'**Time $t$ in seconds**',0.001,86400.*7,86400.,600.,format="%5.0f")
    with columns[1]:
        #Logaritmic T-Slider
        container = st.container()
        if st.session_state.number_input:
            T_slider_value_new = st.number_input("_(log of) Transmissivity $T$_", log_min1,log_max1, st.session_state["T_slider_value"], 0.01, format="%4.2f", key="T_input", on_change=update_T)
        else:
            T_slider_value_new = st.slider("_(log of) Transmissivity $T$_", log_min1, log_max1, st.session_state["T_slider_value"], 0.01, format="%4.2f", key="T_input", on_change=update_T)
        st.session_state["T_slider_value"] = T_slider_value_new
        T = 10 ** T_slider_value_new
        container.write("**$T$ in m²/s:** %5.2e" %T)
        #Logaritmic S-Slider
        container = st.container()
        if st.session_state.number_input:
            S_slider_value_new=st.number_input('_(log of) Storativity $S$_', log_min2, log_max2, st.session_state["S_slider_value"],0.01,format="%4.2f", key="S_input", on_change=update_S)
        else:
            S_slider_value_new=st.slider('_(log of) Storativity $S$_', log_min2,log_max2, st.session_state["S_slider_value"],0.01,format="%4.2f", key="S_input", on_change=update_S)
        st.session_state["S_slider_value"] = S_slider_value_new
        S = 10 ** S_slider_value_new
        container.write("**$S$ (dimensionless):** %5.2e" %S)    
        comparison = st.toggle('Second set of $T$ and $S$ for comparison')
    with columns[2]:
        
        if comparison:
            container = st.container()
            if st.session_state.number_input:
                T2_slider_value_new = st.number_input("_(log of) Transmissivity $T2$_", log_min1,log_max1, st.session_state["T2_slider_value"], 0.01, format="%4.2f", key="T2_input", on_change=update_T2)
            else:
                T2_slider_value_new = st.slider("_(log of) Transmissivity $T2$_", log_min1, log_max1, st.session_state["T2_slider_value"], 0.01, format="%4.2f", key="T2_input", on_change=update_T2)
            st.session_state["T2_slider_value"] = T2_slider_value_new
            T2 = 10 ** T2_slider_value_new
            container.write("**$T2$ in m²/s:** %5.2e" %T2)
            #Logaritmic S-Slider
            container = st.container()
            if st.session_state.number_input:
                S2_slider_value_new=st.number_input('_(log of) Storativity $S2$_', log_min2, log_max2, st.session_state["S2_slider_value"],0.01,format="%4.2f", key="S2_input", on_change=update_S2)
            else:
                S2_slider_value_new=st.slider('_(log of) Storativity $S2$_', log_min2,log_max2, st.session_state["S2_slider_value"],0.01,format="%4.2f", key="S2_input", on_change=update_S2)
            st.session_state["S2_slider_value"] = S2_slider_value_new
            S2 = 10 ** S2_slider_value_new
            container.write("**$S2$ (dimensionless):** %5.2e" %S2)
            
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
    plt.plot(r, s1, linewidth=1., color='b', label=r'drawdown')
    plt.plot(r_neg, s1, linewidth=1, color='b')
    if comparison:
        plt.plot(r, s1_2, linewidth=1., color='black', label=r'drawdown for T2 & S2', linestyle='dashed')
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
    plt.plot(t, s2, linewidth=1., color='r', label=r'drawdown')
    if comparison:
        plt.plot(t, s2_2, linewidth=1., color='black', label=r'drawdown for T2 & S2', linestyle='dashed')
    plt.fill_between(t,s2,max_s, facecolor='mistyrose')
    plt.plot(x2_point,y2_point, marker='o', color='b',linestyle ='None', label='drawdown plotted & printed below graph') 
    plt.xlim(0, 86400*7)
    plt.ylim(max_s,-5)
    plt.xlabel(r'time in s', fontsize=14)
    plt.ylabel(r'Drawdown in m', fontsize=14)
    plt.xticks(np.arange(0, 7*86400, step=86400))  # Set label locations.
    plt.legend()
    plt.grid(True)
    
    st.pyplot(fig)
    
    st.write('**Drawdown  =  %5.2f' %y_point, ' m at distance = %8.2f' %x_point, ' m and time =  %8i' %x2_point, ' sec**')
    
transient_flow_well()

st.subheader(':blue-background[Continued investigation]', divider="blue")
st.markdown('''
            Having gained an overview of drawdown around a well using the interactive graphs, we move on to exploring the system in more detail as guided by the following questions.
            '''
)
# Second assessment

with st.expander(":green[**Show/Hide the second assessment**]"):
    # Assessment to guide users through the interactive plot
    stb.single_choice(":blue[**How does the drawdown change at one specific distance from the well if storativity is decreased?**]",
                  ["Drawdown is less", "Drawdown is more", "Drawdown is not affected"],
                  1,success='CORRECT! When all else is equal, a lower value of storativity will result in more drawdown.', error='This is not correct ...  You can use the interactive tool to explore this and learn more about Storativity [by downloading the book: Basic Hydrogeology - An Introduction to the Fundamentals of Groundwater Science​ and reading Section 5.3](https://gw-project.org/books/basic-hydrogeology/). Feel free to answer again.')
    stb.single_choice(":blue[**If the estimated transmissivity $T$ is too low, how will the predicted drawdown compare to the true drawdown?**]",
                  ["The predicted drawdown will be too small", "The predicted drawdown will remain unchanged", "The predicted drawdown will be too large", "The predicted drawdown will be too large close to the well and too small far from the well"],
                  3,success='CORRECT! ... the low transmissivity will require a higher gradient to accommodate flow through the aquifer surrounding the well screen, so predicted drawdown will be larger than true drawdown near the well. This results in more of the pumped volume being extracted from storage near the well bore, thus less of the volume will be drawn from storage further away resulting in less drawdown at larger distances from the well. It may not be possible to observe this on the application graph for every combination of parameter values entered in this application because the r distance on the graph is limited to 1000 m and the distance where drawdown transitions from overestimation to underestimation may be further than 1000 m from the well. If you are unable to see the transition, then decreasing the values input for time and/or distance might bring the transition zone into view.', error='This is partially correct because the low transmissivity will require a higher gradient to accommodate flow through the aquifer surrounding the well screen, so predicted drawdown will be larger than true drawdown near the well. This results in more of the pumped volume being extracted from storage near the well bore, thus less of the volume will be drawn from storage further away resulting in less drawdown at larger distances from the well. At some location depending on the combination of parameter values the drawdown may be the same for both cases. It may not be possible to observe this on the application graph for every combination of parameter values entered in this application because the r distance is limited to 1000 m and the distance where drawdown transitions from overestimation to underestimation may be further away than 1000 m. If that is the case, decreasing the values input for time and/or distance might bring the transition zone into view. Feel free to answer again.')

st.subheader(':blue-background[Next steps]', divider="blue")
st.markdown('''

            Thus far, we investigated flow to a well in a confined aquifer, and showed the Theis solution can be used to calculate drawdown in response to pumping for a specific place and time.
            
            The next part of this application demonstrates how to estimate aquifer parameter values using drawdown data measured near a pumping well. You can move to the next section using either the menu on the left side or the navigation buttons at the bottom of this page.
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

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')