# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container

st.title('Transient Flow towards a well in a confined aquifer')

st.subheader(':blue-background[Understanding the response of an aquifer to pumping]', divider="blue")

st.markdown('''
            ### To start the investigation of the topic ...
            
            This notebook illustrate the drawdown in a confined aquifer in response to pumping.
            Subsequently, the Theis equation is solved with Python routines.
            
            **Before you use the Theis solution to compute the drawdown, think about the following questions:**
            '''
)
"---"

# Optional theory here
lc1, mc1, rc1 = st.columns([1,4,1])
with mc1:
    show_theory = st.button('Click here if you want to read more about the underlying theory')
    
if show_theory:
    st.markdown(
    """
    ## Required theory
    """
    )
    
st.markdown("CO<sub>2</sub>", unsafe_allow_html=True)
# Initial assessment

# Initial assessment

show_initial_assessment = st.checkbox("**Show the initial assessment**")
if show_initial_assessment:
    columnsQ1 = st.columns((1,1), gap = 'large')
    with columnsQ1[0]:
        stb.single_choice(":blue[**For which conditions is the Theis solution intended?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
        stb.single_choice(":blue[**Assume there is no recharge to the aquifer. What happend with the range of drawdown with ongoing time?**]",
                  ["The range of drawdown will reach a steady state.", "The range of drawdown will increase.", "The range of drawdown is not dependend of time", "The range of drawdown will decrease."],
                  1,success='CORRECT! Without recharge, the range of drawdown will increase.', error='Not quite. Without recharge, the range of drawdown will increase with ongoing time. Use the interactive plot to investigate this behavior.') 
    with columnsQ1[1]:
        stb.single_choice(":blue[**How much water is pumped out by a pumping rate of 0.001 m3/s?**]",
                  ["1000 liters per second.", "100 liters per second", "10 liters per second", "1 liter per second"],
                  3,success='CORRECT! 0.001 m3/s is equivalent to 1 liter per second.', error='Not quite. Keep in mind that 1,000 liters are equivalent to 1 m3.')
                  
            
"---"

# Create buttons with st.button and proceed with the steps of the exercise
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #00FF00;
        color: black;
    }""",
):
    if st.checkbox(':blue[**Proceed with Exercise Step 1**]'):
        st.markdown("""
            **STEP 1:**
            First we aim to investigate the drawdown in response to water abstraction as function of space and time.
            
           _To proceed_ (with the interactive plot):
            - Increase the pumping rate. What happens with the drawdown? You can use the slider 'Distance to show (m)' (middle column) to print specific values of drawdown.
            - Now use the toggle on the left side to 'Show drawdown vs time plot'. Modify the 'Distance to show (m)' and see how the drawdown vs time changes depending of the distance from the abstraction well.
"""
)
    if st.checkbox(':blue[**Proceed with Exercise Step 2**]'):
        st.markdown("""
            **STEP 2:**
            Now we investigate the sensitivity of the hydraulic conductivity _K_ and the storativity _S_ on the drawdown in response to a specific abstraction rate.
            
           _To proceed_:
            - Modify the Transmissivity. What happens?
            - Modify the Storativity. What happens?           
            
"""
)
    if st.checkbox(':blue[**Proceed with Exercise Step 3**]'):
        st.markdown("""
            **STEP 3:**
            
            Now you can use the interactive plot to compare two variants with different transmissivity and storativity. 
            
           _To proceed_:
            - Use the toggle 'Compute a second variant for comparison'.
            - Decrease the transmissivity and compare. Then increase the transmissivity and compare.
            - Decrease the storativity and compare. Then increase the storativity and compare.
"""
)

st.markdown('''
            ### Computation of the drawdown
            The subsequent interactive plot demonstrate the response of a confined aquifer to pumping. You can modify the settings and parameters of the interactive plot with the sliders and toggles above. You can follow the instructions of the exercises, or you can do your own investigations.
            '''
)

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

# (Here, the method computes the data for the well function. Those data can be used to generate a type curve.)
u_max = 1
r_max = 10000
u  = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s

# This is the function to plot the graph with the data     

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1
   
columns = st.columns((1,1,1), gap = 'large')

with columns[0]:
    Q = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.03,0.000,0.001,format="%5.3f")
    show_time = st.toggle('Show drawdown vs time plot')
    comparison = st.toggle('Compute a second variant for comparison')
    max_s = 20
    max_r = 1000

with columns[1]:
    r_show = st.slider(f'Distance to show (m)',0,1000,100,1)
    t_show = st.slider(f'**Time to show(s)**',0,86400*7,86400,600) 
    
with columns[2]:
    #Logaritmic T-Slider
    T_slider_value=st.slider('(log of) **Transmissivity _T_**', log_min1,log_max1,-3.0,0.01,format="%4.2f", key='T1' )
    T = 10 ** T_slider_value
    st.write("**_T in m2/s:_** %5.2e" %T)
    if comparison:
        T2_slider_value=st.slider('(log of) **Transmissivity _T2_**', log_min1,log_max1,-3.0,0.01,format="%4.2f", key='T2' )
        T2 = 10 ** T2_slider_value
        st.write("**_T2 in m2/s:_** %5.2e" %T2)
    #Logaritmic S-Slider
    S_slider_value=st.slider('(log of) **Storativity _S_**', log_min2,log_max2,-4.0,0.01,format="%4.2f", key='S1' )
    S = 10 ** S_slider_value
    st.write("**_S (dimensionless):_** %5.2e" %S)
    if comparison:
        #Logaritmic S-Slider
        S2_slider_value=st.slider('(log of) **Storativity _S2_**', log_min2,log_max2,-4.0,0.01,format="%4.2f", key='S2' )
        S2 = 10 ** S2_slider_value
        st.write("**_S2 (dimensionless):_** %5.2e" %S2)
        
    
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
plt.title('Drawdown along distance with Theis', fontsize=16)
plt.plot(r, s1, linewidth=1., color='b', label=r'drawdown prediction')
plt.plot(r_neg, s1, linewidth=1, color='b')
if comparison:
    plt.plot(r, s1_2, linewidth=1., color='black', label=r'comparison', linestyle='dashed')
    plt.plot(r_neg, s1_2, linewidth=1, color='black', linestyle='dashed')
plt.fill_between(r,s1,max_s, facecolor='lightblue')
plt.fill_between(r_neg,s1,max_s, facecolor='lightblue')
plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='drawdown output') 
plt.xlabel(r'Distance from the well in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
if not show_time: 
    plt.axis('off')
if show_time:    
    plt.title('Drawdown vs time with Theis', fontsize=16)
    plt.plot(t, s2, linewidth=1., color='r', label=r'drawdown prediction')
    if comparison:
        plt.plot(t, s2_2, linewidth=1., color='black', label=r'drawdown prediction', linestyle='dashed')
    plt.fill_between(t,s2,max_s, facecolor='mistyrose')
    plt.plot(x2_point,y2_point, marker='o', color='b',linestyle ='None', label='drawdown output') 
    plt.xlim(0, 86400*7)
    plt.ylim(max_s,-5)
    plt.xlabel(r'time in s', fontsize=14)
    plt.ylabel(r'Drawdown in m', fontsize=14)
    plt.legend()
    plt.grid(True)

st.pyplot(fig)

st.write("**DRAWDOWN output:**")
st.write("Distance from the well (in m): %8.2f" %x_point)
st.write('Time (in sec): %8i' %x2_point)
st.write('Drawdown at this distance (in m):  %5.2f' %y_point)


st.markdown('''
            ### Follow-up steps for the investigation
            Now that you have an impression for the interactive plot we can move on to understand the system more in detail. We will guide this with the following questions:
            '''
)
# Second assessment

show_second_assessment = st.toggle("**Show the second assessment**")
if show_second_assessment:
    # Assessment to guide users through the interactive plot
    stb.single_choice(":green[**QuestionI1?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
    stb.single_choice(":green[**QuestionI2?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
    stb.single_choice(":green[**QuestionI3?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')

st.markdown('''
            ### Intermediate conclusion and next steps
            So far, we investigated the flow to a well in a confined aquifer. We saw how the Theis solution can be used to calculate the drawdown in response to pumping for a specific place and time.
            
            In the next part of the application, we will see how we can derive the parameters of the aquifer with measured data. Move to the next section by using the sidemenu or the subsequent buttons.
            '''
)
"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/01_📃_Theory.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/03_📈_▶️ Theis_solution.py")
