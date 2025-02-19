import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title('Slugtest evaluation')

st.subheader('Evaluating slug test in :orange[unconfined aquifers with the Bouwer & Rice method]', divider="orange")

st.markdown("""
            ### Introduction and Motivation
            Slug tests are quick and cost-effective field methods used to determine the hydraulic conductivity (K) of an aquifer. They involve a sudden change in water level within a well (either by adding or removing a known volume of water, or inserting/removing a slug) and measuring the subsequent water level recovery over time, see subsequent figure.
            
            These tests are ideal for:
            - Assessing aquifer properties in low-permeability formations.
            - Situations where pumping tests are not feasible due to time or space constraints.
            - Monitoring wells where minimal disturbance to the aquifer is desired.
            
            Types of Slug Tests:
            - Rising-head test: Water level rises after removal of a slug.
            - Falling-head test: Water level falls after adding water or a slug.
            
            **Why use slug tests?** They are fast, inexpensive, and suitable for small-scale investigations, making them a standard tool in hydrogeological site assessments.
           """)
           
lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('05_Applied_hydrogeology/FIGS/slug_confined.png', caption="Schematic representation of a slug test where a slug of water is added to a well. Figure from Kruseman and DeRidder - a Groundwater Project preserved book (https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/).")

with st.expander('The Theory behind the Bouwer & Rice Method for Unconfined Aquifers'):
    st.markdown("""
            ### The Theory behinf the Bouwer & Rice Method for Unconfined Aquifers
            
            The **Bouwer and Rice (1976) method** is a widely used approach to evaluate **slug test data**, especially in **partially penetrating wells** in **unconfined aquifers**. It relates the **water level recovery** to the **hydraulic conductivity** of the aquifer, accounting for well geometry and screen penetration.
            
            The hydraulic conductivity $K$ is calculated using:
            """)
    st.latex(r'''K = \frac{r_c^2 \ln\left(\frac{R_e}{r_w}\right)}{2L} \cdot \frac{1}{t} \cdot \ln\left(\frac{h_t}{h_0}\right)''')

    st.markdown("""        
            **Where:**
            - $K$: Hydraulic conductivity (m/s)  
            - $r_c$: Radius of the well casing (m) 
            - $r_w$: Radius of the well screen (m)  
            - $R_e$: Effective radius of influence (m)   
            - $L$: Length of the well screen intersecting the aquifer (m)
            - $t$: Elapsed time since the slug event (s)  
            - $h_0$: Initial head displacement (m) 
            - $h_t$: Head displacement at time $t$ (m)
            
            **Estimating the Effective Radius $R_e$**
            The **effective radius** $R_e$ depends on the **well penetration**:  
            - **Fully penetrating well:**
            """)
    st.latex(r'''R_e = \frac{D}{2}''')
    
    st.markdown("""  
            *(where $D$ is the saturated aquifer thickness)*  
            
            - **Partially penetrating well:**  
            $R_e = 1.1L + r_w$       
            
            Reference: Bouwer, H., & Rice, R. C. (1976). A slug test for determining hydraulic conductivity of unconfined aquifers with completely or partially penetrating wells. Water Resources Research, 12(3), 423-428.
           """)
    
"---"

# Computation

# Fixed values

L = 2.1
tmax = 300
m_time = []
m_head = []

# User defined values

# LOAD CSV / Initialize
uploaded_file = st.file_uploader("Choose a CSV file for evaluation (time in seconds / normalized heads in meters)")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    m_time = list(df.iloc[:,0].values)
    m_head = list(df.iloc[:,1].values)
    
# Define the minimum and maximum for the logarithmic scale
log_min = -6.0 # Corresponds to 10^-7 = 0.0000001
log_max =  -2.0  # Corresponds to 10^0 = 1

lc1, rc1 = st.columns((1,1))
with lc1:
    with st.expander('Provide well parameter'):
        rc = st.number_input("well casing radius", value = 0.025,step=.001, format="%.3f")
        rw = st.number_input("well screen radius", value = 0.085,step=.001, format="%.3f")
    


with rc1:
    # Log slider with input and print
    t_off = st.slider('**Time offset** in s', 0, 60, 0, 1)
    container = st.container()
    K_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min,log_max,-3.0,0.01,format="%4.2f" )
    K = 10 ** K_slider_value
    container.write("**Hydraulic conductivity in m/s:** %5.2e" %K)

# Calculation
F = 2 * np.pi * L/np.log(L/rw)
prq = np.pi * rc**2
t = np.arange(0, tmax, 1)

t_plot=[]
for i in t:
  t_plot.append(i+t_off)

exp_decay = np.exp(-F/prq*K*t)

# Plot figure
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot()
ax.plot(t_plot,exp_decay, color='magenta', label='computed')
ax.plot(m_time,m_head, 'bo', label='measured')
plt.axis([0,tmax,0,1])

plt.xlabel(r'time t in (s)', fontsize=14)
plt.ylabel(r'H/Ho', fontsize=14)
plt.title('Slugtest evaluation (positive slug)', fontsize=16)
plt.legend(fontsize=14)

st.pyplot(fig=fig)