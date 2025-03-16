# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import io
import streamlit as st

### 01 TITLE AND HEADER

st.title('🎯 The Theis solution for pumping test evaluation')

st.header(':blue[Manually parmater fitting with type-curve matching]')

st.subheader(':blue-background[Materials and Guidance for Theis Type-curve matching]', divider="blue")

### 02 INITIAL EXPLANATION
st.markdown('''
            Transient Flow toward a well in a confined aquifer is described here using the Theis Solution. You can use the subsequent materials and instructions to perform manual type-curve matching.
            '''
)

st.subheader(':blue-background[The Theis Type-curve]', divider="blue")
st.markdown('''
            The **Theis type curve plot** is a fundamental tool in hydrogeology for analyzing **transient groundwater flow** in response to well pumping. It is based on the **Theis solution**, which describes how drawdown evolves over time in a **confined aquifer**.
            
            By plotting **dimensionless drawdown** against **dimensionless time** on a logarithmic scale, the type curve provides a theoretical reference for evaluating aquifer properties. This approach is widely used to estimate **transmissivity (T)** and **storativity (S)** by matching field observations to the type curve.
            
            To determine the aquifer properties, the **Theis type curve** must be aligned with the measured data using a **matching point**—a reference point where both curves coincide. In this step, you can **define the matching point manually**, selecting a representative coordinate on the plot to scale the type curve accordingly. Typically, a **representative coordinate** is chosen where the curves overlap well and is often set to **simple values (e.g., 1, 10, or 100)** to make calculations easier and reduce errors in parameter estimation.
            
            Below, you can plot the Theis type curve with a user-defined matching point. You also have the option to download the figure for further study.  
            '''
)
### 03 INITIAL ASSESSMENTS

### 04 THEORY

### 05 FUNCTIONS

#Define a function, class, and object for Theis Well analysis

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

def deriv(t, tm, s, sm):
    #d = (s-sm)/(np.log(t)-np.log(tm))
    d=((t+tm)/2)*((s-sm)/(t-tm))
    return d
    
# Data for the type curve plot
u_max = 10
r_max = 1000000
u  = [u_max for x in range(r_max)]
um = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
um_inv = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]
w_um = [well_function(u_max/r_max) for x in range(r_max)]


### 07 COMPUTATION
#for x in range(1,r_max,1):
#    if x>0:
#        u[x] = x*u_max/r_max
#        u_inv[x] = 1/u[x]
#        w_u[x] = well_function(u[x])
    
# Define parameters
num_points = 100  # Adjust for desired resolution
u_min = 1e-6  # Set a small minimum u value to avoid division by zero
u_max = 10    # Adjust u_max based on problem constraints

# Use log-spaced values to cover a wide range efficiently
u = np.geomspace(u_min, u_max, num=num_points)  # Log-spaced values of u
u_inv = 1 / u
w_u = well_function(u)  # Assuming well_function is vectorized
    
### 08 PLOTTING
# Plotting the Theis curve

#W(u) is match_wu and 1/u is match_uinv

u_inv_values = [0.1, 1.0, 10, 100, 1000]
wu_values = [0.01, 0.1, 1.0, 10]

columns1 = st.columns((1,1), gap = 'large')
with columns1[0]:
    match_u_inv = st.select_slider('Select 1/u for the matchpoint', options= u_inv_values, value=1.0)
with columns1[1]:
    match_wu     =st.select_slider('Select w(u) for the matchpoint', options= wu_values, value=1.0)
        
matchgrid_x=[match_u_inv, match_u_inv]
matchgrid_y=[match_wu, match_wu]
matchgrid  =[0.001, 1000000]

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)  # adjust plot area
ax.plot(u_inv, w_u, color = 'black', linewidth = 2)
ax.plot(match_u_inv, match_wu,'ro',markersize=6)
ax.plot(matchgrid_x,matchgrid,color ='lime', linewidth = 1)
ax.plot(matchgrid,matchgrid_y,color = 'lime', linewidth = 1)
plt.yscale("log")
plt.xscale("log")
plt.axis([0.1,1E4,1E-2,1E+1])
ax.set(xlabel='1/u', ylabel='w(u)',
       title='Theis type curve for manual evaluation')
ax.grid(which="both",color='whitesmoke', linewidth=0.5)
ax.spines['top'].set_color('lightgrey')
ax.spines['bottom'].set_color('lightgrey')
ax.spines['right'].set_color('lightgrey')
ax.spines['left'].set_color('lightgrey')
ax.tick_params(which='both', colors='lightgrey')

st.pyplot(fig)

# Safe the figure
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format="png", dpi=300)
img_buffer.seek(0)  # Reset buffer position

columns5 = st.columns((1,1,1), gap = 'large')
with columns5[1]:
    # Add download button
    st.download_button(
        label=":green[**Download**] **Theis Type Curve**",
        data=img_buffer,
        file_name="Theis_type_curve.png",
        mime="image/png"
        )
        
# PLOTTING DATA

st.subheader(':blue-background[Loading and plotting measured data]', divider="blue")
st.markdown('''
            To analyze field data with the **Theis type curve**, you can either **upload your own dataset** or use **predefined measurement data**. Once the data are loaded, you have the option to **download the dataset** for manual type curve matching. The plot can be displayed using **linear or semi-logarithmic axes**, allowing for flexible visualization of the drawdown behavior.  
            '''
)

### 06 READ AND PREPARE DATA

# TODO ALLOW CSV / MORE DATA (RANDOM GENERATED)
# Select data and solution
columns12 = st.columns((1,1), gap = 'large')
with columns12[0]:
    datasource = st.selectbox("**What data should be used?**",
    ("Synthetic textbook data", "Load own CSV dataset"))
if (datasource == "Synthetic textbook data"):
    # Data and parameter from SYMPLE exercise
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d
elif(st.session_state.Data =="Load own CSV dataset"):
    # Initialize
    m_time = []
    m_ddown = []
    r = 100       # m
    b = 10        # m
    Qs = 0.005    # m^3/s
    Qd = 100      # m^3/d
    uploaded_file = st.file_uploader("Choose a file (subsequently you can add the aquifer thicknes, the pumping rate and the distance between well and observation). The required data format for the CSV-file is time in minutes and drawdown in meters, both separated by a comma.")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        m_time = list(df.iloc[:,0].values)
        m_ddown = list(df.iloc[:,1].values)
        st.write(df)
        if st.toggle('Pumping rate input in m^3/h'):
            Qs_slider = st.number_input(f'**Pumping rate (m³/h)** for the **pumping test**', 0.1,100.,10.,0.01,format="%5.2f")
            Qs = Qs_slider/3600
        else:
            Qs = st.number_input(f'**Pumping rate (m³/s)** for the **pumping test**', 0.001,0.100,0.005,0.001,format="%5.3f")
        r = st.number_input(f'**Distance** (m) from the **well** for the **observation**', 1,1000,100,1)
        b = st.number_input(f'**average Aquifer thickness** (m)', 1.,200.,10.,0.01)
        Qd = Qs*60*60*24 # m^3/d

semilog = st.toggle('Switch from log-log to semi-log plot')
# Parameter for the measured data plot

t_max = len(m_time)
d = [0 for x in range(t_max)]

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)  # adjust plot area
ax.plot(m_time, m_ddown,'bo', markersize=3)
if semilog:
    plt.xscale("log")
else:
    plt.xscale("log")
    plt.yscale("log")
plt.axis([0.1,1E4,1E-2,1E+1])
ax.set(xlabel='time t (min)', ylabel='drawdown s (m)',
       title='Measured data')
ax.grid(which="both", color='grey',linewidth=0.5)

st.pyplot(fig)

# Safe the figure
# Convert figure to a BytesIO object
img_buffer = io.BytesIO()
fig.savefig(img_buffer, transparent='true', format="png", dpi=300)
img_buffer.seek(0)  # Reset buffer position

columns6 = st.columns((1,1,1), gap = 'large')
with columns6[1]:
    # Add download button
    st.download_button(
        label=":green[**Download**] **Measured Data for Theis**",
        data=img_buffer,
        file_name="measured_data_Theis.png",
        mime="image/png"
        )
        
st.subheader(':red[Computing Transmissivity and Storativity]')        
st.markdown('''
            In this part you can input the data that you got from the Theis Type curve matching and compute the Transmissivity $T$ and the Storativity $S$.
            '''
)
time_input = st.number_input('Time (min) from the type curve plot', 0.,1000., 1., 0.1)
ddown = st.number_input('Drawdown (m) from the type curve plot', 0.,1000., 1., 0.1)
time = time_input*60

transmissivity = Qs/4/np.pi/ddown*match_wu
storativity = 4*transmissivity*(time/r/r)/match_u_inv

if st.button('Show the computed results'):
    st.write("- Transmissivity **$T$ = % 10.2E"% transmissivity, " m²/s**")
    st.write("- Storativity **$S$ = % 10.2E"% storativity, "[dimensionless]**")
# TODO - NUMBER INPUT AND EVALUATION
# fig.savefig(img_buffer,  transparent='true',format="png", dpi=300)
# TODO - INSTRUCTION HOW TO USE (MAYBE SCREENCAST)