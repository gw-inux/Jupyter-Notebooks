# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st

# also Interactive Documents 06-04-006
# ToDo:
#    - K log slider
#    - number input

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Rudolf Liedl": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface

st.title('Theis drawdown prediction')
st.header('Fitting Formation parameter to measured data and predict the drawdown', divider = 'green')
st.markdown("""
            This interactive document allows to apply the Theis principle for pumping test evaluation in confined, transient setups. The notebook is based on an Spreadsheet from Prof. Rudolf Liedl.
            
            ### General situation
            We consider a confined aquifer with constant transmissivity. If a well is pumping water out of the aquifer, radial flow towards the well is induced. To calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined aquifer without further sinks and sources:
"""
)
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
st.markdown("""
            ### Mathematical model and solution
            Charles V. Theis presented a solution for this by deriving
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.markdown("""
            with the well function
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.markdown("""
            and the dimensionless variable
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.markdown("""
            This equations are not easy to solve. Historically, values for the well function were provided by tables or as so called type-curve. The type-curve matching with experimental data for pumping test analysis can be considered as one of the basic hydrogeological methods. However, modern computer provide an easier and more convinient way to solve the 1D radial flow equation based on the Theis approach. Subsequently, the Theis equation is solved with Python routines. The results for the measured data are graphically presented in an interactive plot.
"""
)            

st.subheader('Interactive plot', divider = 'green')

st.markdown("""           
            The red dots are the measured data.
            
            Modify the transmissivity _**T**_ and the storativity _**S**_ to fit the measured data to the well function.
            
            **Select the data below!**
"""
) 
# Computation

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

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_max = 1
r_max = 100000
u  = [u_max for x in range(r_max)]
um = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
um_inv = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]
w_um = [well_function(u_max/r_max) for x in range(r_max)]

for x in range(1,r_max,1):
    if x>0:
        u[x] = x*u_max/r_max
        u_inv[x] = 1/u[x]
        w_u[x] = well_function(u[x])

# Data from SYMPLE exercise
m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
# Parameters needed to solve Theis (From the SYMPLE example/excercise)
r = 120       # m
b = 8.5       # m
Qs = 0.3/60   # m^3/s
Qd = Qs*60*60*24 # m^3/d

m_time_s = [i*60 for i in m_time] # time in seconds
num_times = len(m_time)


@st.fragment
def inverse():
    # This is the function to plot the graph with the data     
    # Get input data
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
    log_max2 = 0.0  # S / Corresponds to 10^0 = 1
   
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        T_slider_value=st.slider('(log of) **Transmissivity** in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        T = 10 ** T_slider_value
        # Display the logarithmic value
        st.write("_Transmissivity_ in m2/s: %5.2e" %T)
        S_slider_value=st.slider('(log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        # Convert the slider value to the logarithmic scale
        S = 10 ** S_slider_value
        # Display the logarithmic value
        st.write("_Storativity_ (dimensionless):** %5.2e" %S)
        refine_theis = st.toggle("**Refine** the range of the **Theis matching plot**")
    with columns2[1]:
        Q_pred = st.slider(f'**Pumping rate** (m^3/s) for the **prediction**', 0.001,0.100,Qs,0.001,format="%5.3f")
        r_pred = st.slider(f'**Distance** (m) from the **well** for the **prediction**', 1,1000,r,1)
        per_pred = st.slider(f'**Duration** of the **prediction period** (days)',1,3652,3,1) 
        max_t = 86400*per_pred
        if per_pred <= 3:
            t_search = st.slider(f'**Select the value of time (s) for printout**', 1,max_t,1,1)
        elif per_pred <= 7:
            t_search_h = st.slider(f'**Select the value of time (hours) for printout**', 1.,24.*per_pred,1.)
            t_search = t_search_h*3600
        elif per_pred <= 366:
            t_search_d = st.slider(f'**Select the value of time (days) for printout**', 1.,per_pred*1.0,1.)
            t_search = t_search_d*86400
        else:
            t_search_mo = st.slider(f'**Select the value of time (months) for printout**', 1.,per_pred/30.4375,1.)
            t_search = t_search_mo*2629800
        auto_y = st.toggle("Adjust the range of drawdown plotting")

    # PLOT MEASURED DATA
    max_s = 20
    x = 0
    for t1 in m_time_s:
        um[x] = theis_u(T,S,r,t1)
        um_inv[x] = 1/um[x]
        w_um[x] = theis_wu(Qs,T,m_ddown[x])
        x = x+1

    # PLOT DRAWDOWN VS TIME
    # Range of delta_h / delta_l values (hydraulic gradient)
    t2 = np.linspace(1, max_t, 100)
    t2_h = t2/3600
    t2_d = t2/86400
    t2_mo = t2/2629800

    # Compute s for prediction
    s  = compute_s(T, S, t2, Q_pred, r_pred)

    # Compute s for a specific point
    x_point = t_search
    y_point = compute_s(T, S, t_search, Q_pred, r_pred)
    
    fig = plt.figure(figsize=(12,7))
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(u_inv, w_u)
    ax.plot(um_inv[:num_times], w_um[:num_times],'ro')
    plt.yscale("log")
    plt.xscale("log")
    if refine_theis:
        plt.axis([1,1E5,1E-2,1E+2])
    else:
        plt.axis([1e-1,1E7,1E-4,1E+4])
        ax.text((2E-1),5E+3,'Coarse plot - Refine for final fitting')
    plt.xlabel(r'1/u', fontsize=14)
    plt.ylabel(r'w(u)', fontsize=14)
    plt.title('Theis drawdown', fontsize=16)
    ax.grid(which="both")
    plt.legend(('well function','measured'))

    ax = fig.add_subplot(1, 2, 2)
    if per_pred <= 3:
        plt.plot(t2, s, linewidth=3., color='r', label=r'Drawdown prediction')
        plt.plot(t_search,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
        plt.xlabel(r'Time in sec', fontsize=14)
        plt.xlim(0, max_t)
    elif per_pred <= 7:
        plt.plot(t2_h, s, linewidth=3., color='r', label=r'Drawdown prediction')
        plt.plot(t_search_h,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
        plt.xlabel(r'Time in hours', fontsize=14)
        plt.xlim(0, max_t/3600)
    elif per_pred <= 366:
        plt.plot(t2_d, s, linewidth=3., color='r', label=r'Drawdown prediction')
        plt.plot(t_search_d,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
        plt.xlabel(r'Time in days', fontsize=14)
        plt.xlim(0, max_t/86400)
    else:
        plt.plot(t2_mo, s, linewidth=3., color='r', label=r'Drawdown prediction')
        plt.plot(t_search_mo,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
        plt.xlabel(r'Time in months', fontsize=14)
        plt.xlim(0, max_t/2629800)

    #plt.ylim(max_s, 0)
    if auto_y:
        plt.ylim(bottom=0, top=None)
    else:
        plt.ylim(bottom=0, top=max_s)
    ax.invert_yaxis()
    #plt.plot(x_point,y_point, marker='o', color='b',linestyle ='None', label='drawdown output') 
    plt.ylabel(r'Drawdown in m', fontsize=14)
    plt.title('Drawdown prediction with Theis', fontsize=16)
    plt.legend()
    plt.grid(True)
    
    st.pyplot(fig)

    columns3 = st.columns((1,1), gap = 'medium')
    with columns3[0]:
        st.write("**Parameter estimation**")
        st.write("Distance of measurement from the well (in m): %3i" %r)
        st.write("Pumping rate of measurement (in m^3/s): %5.3f" %Qs)
        st.write("Thickness of formation b = ","% 5.2f"% b, " m")
        st.write("Transmissivity T = ","% 10.2E"% T, " m^2/s")
        st.write("(Hydr. cond. K) = ","% 10.2E"% (T/b), " m^2/s")
        st.write("Storativity    S = ","% 10.2E"% S, "[-]")

    with columns3[1]:
        st.write("**Prediction**")
        st.write("Distance of prediction from the well (in m): %3i" %r_pred)
        st.write("Pumping rate of prediction (in m^3/s): %5.3f" %Q_pred)
        st.write("Time since pumping start (in s): %3i" %x_point)
        if per_pred <= 3:
            st.write("Time since pumping start (in s): %3i" %t_search)
        elif per_pred <= 7:
            st.write("Time since pumping start (in hours): %5.2f" %t_search_h)
        elif per_pred <= 366:
            st.write("Time since pumping start (in days): %5.2f" %t_search_d)
        else:
            st.write("Time since pumping start (in months): %5.2f" %t_search_mo)
        st.write("Predicted drawdown at this distance and time (in m):  %5.2f" %y_point)
inverse()

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')