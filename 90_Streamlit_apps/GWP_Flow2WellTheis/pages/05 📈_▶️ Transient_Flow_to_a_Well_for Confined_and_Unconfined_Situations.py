# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb

st.title('Theis drawdown prediction for confined and unconfined aquifers')

st.subheader(':green-background[Drawdown comparison in response to water abstraction]', divider="green")

st.markdown(""" 
            ### Some initial thoughts for the investigation
            This notebook illustrate the drawdown in a confined and an unconfined aquifer in response to pumping.
"""
)
# Initial assessment

columnsQ1 = st.columns((1,1), gap = 'large')

with columnsQ1[0]:
    stb.single_choice(":green[**For which conditions is the Theis solution intended?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
    stb.single_choice(":green[**Question2?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
                  
with columnsQ1[1]:
    stb.single_choice(":green[**Question3?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')             
    stb.single_choice(":green[**Question4?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
"---"
st.markdown("""
            ### Correction of the drawdown for unconfined aquifers
            
            Jacob (in Kruseman and de Ridder 1994) proposed an conrrection of the Theis drawdown to account for unconfined aquifers.
            """
)
st.latex(r'''s' = s - \frac{s^2}{2b}''')
st.markdown('''
            With a reformulation, this allows to compute the drawdown of unconfined aquifers as
            '''
)
st.latex(r'''s = b - b \sqrt{1 - \frac{2s'}{b}}''')
st.markdown("""
            ### Computation
            Subsequently, the Theis equation for confined and unconfined conditions is solved with Python routines. The interactive plot demonstrate the response of both systems to pumping side-by-side.
            
            Start your investigations with increasing the pumping rate. See how the drawdown changes. Modify the transmissivity _**T**_, the specific yield _**SY**_, and the storativity _**S**_ to understand how these parameters affect the drawdown.

"""     
)

"---"

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

def compute_s_unconfined(T, SY, t, Q, r, b):
    S_u = SY*b
    u = theis_u(T, S_u, r, t)
    s = theis_s(Q, T, u)
    s_u = b - b * np.sqrt(1-2*s/b)
    return s_u

# This is the function to plot the graph with the data     

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1

   
columns_i1 = st.columns((1,8,1), gap = 'large')

with columns_i1[1]:
    st.write('**General parameter of the plot**')
    max_s = st.slider(f':grey-background[Drawdown range in the plot (m)]',1,50,10,1)
    max_r = st.slider(f':grey-background[Distance range in the plot (m)]',10,2000,1000,1)
    t = st.slider(f'**Time (s)**',0,86400*7,86400,600)
    x_search = st.slider(f'Distance for result printout in the plot (m)',1,2000,10,1)
    Q = st.slider(f'**Pumping rate (m^3/s)**', 0.001,0.100,0.000,0.001,format="%5.3f")
    T_slider_value=st.slider('(log of) **Transmissivity in m2/s**', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    T = 10 ** T_slider_value
    # Display the logarithmic value
    st.write("_Transmissivity in m2/s:_ %5.2e" %T)

columns_i2 = st.columns((3,1,3), gap = 'large')

with columns_i2[0]:
    st.write('**Parameter of the unconfined aquifer**')
    b = st.slider(f'**Thickness** of the unconfined aquifer',1.,100.,10.,0.01)
    SY = st.slider(f'**Specific yield (/)**',0.01,0.60,0.25,0.01)
    # Display the Storativity
    st.write("_Storativity (dimensionless):_ %5.2e" %(SY*b))

with columns_i2[2]:
    st.write('**Parameter of the confined aquifer**')
    S_slider_value=st.slider('(log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    S = 10 ** S_slider_value
    # Display the logarithmic value
    st.write("_Storativity (dimensionless):_ %5.2e" %S)

# Range of delta_h / delta_l values (hydraulic gradient)
r = np.linspace(1, max_r, 200)
r_neg = r * -1.0
    
# Compute Q for each hydraulic gradient
s  = compute_s(T, S, t, Q, r)
s_u  = compute_s_unconfined(T, SY, t, Q, r, b)

# Compute s for a specific point
x_point = x_search
x_point_u = x_search*-1
y_point = compute_s(T, S, t, Q, x_point)
y_point_u = compute_s_unconfined(T, SY, t, Q, x_point_u, b)

textstr1 =('Unconfined')
textstr2 =('Confined (above aquifer top)')
    
# Plotting
fig =plt.figure(figsize=(10, 6))

plt.title('Drawdown prediction with Theis', fontsize=16)    
plt.plot(r, s, linewidth=1.5, color='r', label=r'drawdown prediction confined')
plt.plot(r_neg, s, linewidth=0.25, color='r', linestyle='dashed')
plt.plot(r, s_u, linewidth=0.25, color='b', linestyle='dashed')
plt.plot(r_neg, s_u, linewidth=1.5, color='b',label=r'drawdown prediction unconfined')
plt.fill_between(r,s,max_s, facecolor='lightgrey')
plt.fill_between(r_neg,s_u,max_s, facecolor='lightblue')
plt.xlim(-max_r, max_r)
plt.ylim(max_s,-5)
plt.plot(x_point,y_point, marker='o', color='r',linestyle ='None', label='drawdown output confined') 
plt.plot(x_point_u,y_point_u, marker='o', color='b',linestyle ='None', label='drawdown output unconfined') 
plt.xlabel(r'Distance from the well in m', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.text(-max_r*0.9, max_s*0.9, textstr1, fontsize=14,
        verticalalignment='top')
plt.text(max_r*0.25, max_s*0.9, textstr2, fontsize=14,
        verticalalignment='top')
plt.legend()
#plt.grid(True)

st.pyplot(fig)

# Result output below the interactive plot    
columns2 = st.columns((2.0,5.0,0.1))

with columns2[1]:
    if Q==0:
        st.write(":red[**Abstraction rate 0 - START PUMPING!**]")
    else:
        st.write("**Pumping with Q (in m3/s):** %8.3f" %Q)
    st.write("**DRAWDOWN output:**")
    st.write("Distance from the well (in m): %8.2f" %x_point)
    st.write("Time (in sec): %8i" %t)
    st.write('Transmissivity in m2/s:  %5.2e' %T)
    st.write('Hydraulic conductivity:  %5.2e' %(T/b))

columns3 = st.columns((1,1), gap = 'large')

with columns3[0]:
    st.write(":green[**Unconfined**]")
    st.write('Storativity:  %5.2e' %(SY*b))    
    st.write('Drawdown at this distance (in m):  %5.2f' %y_point_u)

with columns3[1]:
    st.write(":blue[**Confined**]")
    st.write('Storativity:  %5.2e' %S)
    st.write('Drawdown at this distance (in m):  %5.2f' %y_point)
    
"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/04_📈_▶️ Real Data Parameter Estimation.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/06_👉_About.py")
        
