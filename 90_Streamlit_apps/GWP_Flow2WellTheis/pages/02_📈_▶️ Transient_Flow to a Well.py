# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb

st.title('Transient Flow towards a well in a confined aquifer')

st.subheader(':blue-background[Drawdown computation with the Theis solution]', divider="blue")

st.markdown('''
            ### To start the investigation of the topic ...
            
            This notebook illustrate the drawdown in a confined aquifer in response to pumping.
            Subsequently, the Theis equation is solved with Python routines.
            
            **Before you use the Theis solution to compute the drawdown, think about the following questions:**
            '''
            e<sup>2</sup> 
            e<sub>2</sub>
            H~2~O is a liquid. 2^10^ is 1024.
)

# Initial assessment

columnsQ1 = st.columns((1,1), gap = 'large')

with columnsQ1[0]:
    stb.single_choice(":rainbow[**For which conditions is the Theis solution intended?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
    stb.single_choice(":rainbow[**Question2?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
                  
with columnsQ1[1]:
    stb.single_choice(":rainbow[**Question3?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')             
    stb.single_choice(":rainbow[**Question4?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
"---"

st.markdown('''
            ### Computation of the drawdown
            The subsequent plot demonstrate the response of a confined aquifer to pumping. Start your investigations with increasing the pumping rate. See how the drawdown changes.
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
   
columns = st.columns((1,1), gap = 'large')

with columns[0]:
    max_s = st.slider(f'Drawdown range in the plot (m)',1,50,10,1)
    max_r = st.slider(f'Distance range in the plot (m)',10,10000,1000,1)
    x_search = st.slider(f'Distance for result printoutrange in the plot (m)',0,10000,0,1)
    t = st.slider(f'**Time (s)**',0,86400*7,86400,600)
    
with columns[1]:
    Q = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
    T_slider_value=st.slider('(log of) Transmissivity in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    T = 10 ** T_slider_value
    # Display the logarithmic value
    st.write("**Transmissivity in m2/s:** %5.2e" %T)
    S_slider_value=st.slider('(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    S = 10 ** S_slider_value
    # Display the logarithmic value
    st.write("**Storativity (dimensionless):** %5.2e" %S)

# Range of spatial coordinate
r = np.linspace(1, max_r, 200)
r_neg = r * -1.0
    
# Compute drawdown
s  = compute_s(T, S, t, Q, r)

# Compute drawdown for a specific point
x_point = x_search
y_point = compute_s(T, S, t, Q, x_search)
    
# Plotting and printing of results
fig=plt.figure(figsize=(10, 6))
    
plt.title('Drawdown prediction with Theis', fontsize=16)
plt.plot(r, s, linewidth=1., color='b', label=r'drawdown prediction')
plt.plot(r_neg, s, linewidth=1, color='b')
plt.fill_between(r,s,max_s, facecolor='lightblue')
plt.fill_between(r_neg,s,max_s, facecolor='lightblue')
plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='drawdown output') 
plt.xlabel(r'Distance from the well in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.legend()
plt.grid(True)

st.pyplot(fig)

st.write("DRAWDOWN output:")
st.write("Distance from the well (in m): %8.2f" %x_point)
st.write('Drawdown at this distance (in m):  %5.2f' %y_point)
st.write('Time (in sec): ',t)

st.markdown('''
            ### Follow-up steps for the investigation
            Now that you have an impression for the interactive plot we can move on to understand the system more in detail. We will guide this with the following questions:
            '''
)

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
        st.switch_page("pages/03_📈_▶️ Parameter Estimation.py")
