# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import pandas as pd
import streamlit as st

st.title('Neuman parameter estimation')
st.subheader('Understanding the Neuman solution  for :blue[unconfined aquifers]', divider="blue")
st.markdown("""
            ALL OF THE FOLLOWING NEEDS TO BE ADAPTED
            
            #### General explanation and credit
            
            ### General situation
            We consider a aquifer with constant transmissivity. If a well is pumping water out of the aquifer, radial flow towards the well is induced. To calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within an unconfined aquifer without further sinks and sources:
"""
)
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
st.markdown("""
            ### Mathematical model and solution
            
            #### Theis solution for confined aquifers
            
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
            #### Neuman solution for unconfined aquifers
            
            ToDo: Provide explanation and theory here
"""
)
st.markdown("""
            This equations are not easy to solve. Historically, values for the well function were provided by tables or as so called type-curve. The type-curve matching with experimental data for pumping test analysis can be considered as one of the basic hydrogeological methods. However, modern computer provide an easier and more convinient way to solve the 1D radial flow equation based on the Theis approach. Subsequently, the Theis equation is solved with Python routines. The results for the measured data are graphically presented in an interactive plot.
            
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

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_min = -5
u_max = 4

u = np.logspace(u_min,u_max)
u_inv = 1/u
u_inv_a = [4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00, 4.00E+00, 8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01, 8.00E+01, 1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02, 1.40E+03, 2.40E+03, 4.00E+03, 8.00E+03]
u_inv_b = [1.40E-02, 2.40E-02, 4.00E-02, 8.00E-02, 1.40E-01, 2.40E-01, 4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00, 4.00E+00, 8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01, 8.00E+01, 1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02, 1.00E+03]

w_u = well_function(u)

# Neuman type curve data from tables

w_u_a = [[2.48E-02, 2.41E-02, 2.30E-02, 2.14E-02, 1.88E-02, 1.70E-02, 1.38E-02, 1.00E-02, 1.00E-02],
         [1.45E-01, 1.40E-01, 1.31E-01, 1.19E-01, 9.88E-02, 8.49E-02, 6.03E-02, 3.17E-02, 1.74E-02],
         [3.58E-01, 3.45E-01, 3.18E-01, 2.79E-01, 2.17E-01, 1.75E-01, 1.07E-01, 4.45E-02, 2.10E-02],
         [6.62E-01, 6.33E-01, 5.70E-01, 4.83E-01, 3.43E-01, 2.56E-01, 1.33E-01, 4.76E-02, 2.14E-02],
         [1.02E+00, 9.63E-01, 8.49E-01, 6.88E-01, 4.38E-01, 3.00E-01, 1.40E-01, 4.78E-02, 2.15E-02],
         [1.57E+00, 1.46E+00, 1.23E+00, 9.18E-01, 4.97E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [2.05E+00, 1.88E+00, 1.51E+00, 1.03E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [2.52E+00, 2.27E+00, 1.73E+00, 1.07E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [2.97E+00, 2.61E+00, 1.85E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [3.56E+00, 3.00E+00, 1.92E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [4.01E+00, 3.23E+00, 1.93E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [4.42E+00, 3.37E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [4.77E+00, 3.43E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.16E+00, 3.45E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.40E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.54E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.59E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02]]

w_u_b = [[5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.12E-01, 3.23E-01, 1.45E-01, 5.09E-02, 2.39E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.12E-01, 3.23E-01, 1.47E-01, 5.32E-02, 2.57E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.16E-01, 3.27E-01, 1.52E-01, 5.68E-02, 2.86E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.24E-01, 3.37E-01, 1.62E-01, 6.61E-02, 3.62E-02],
         [5.62E+00, 3.46E+00, 1.94E+00, 1.10E+00, 5.37E-01, 3.50E-01, 1.78E-01, 8.06E-02, 4.86E-02],
         [5.62E+00, 3.46E+00, 1.95E+00, 1.11E+00, 5.57E-01, 3.74E-01, 2.05E-01, 1.06E-01, 7.14E-02],
         [5.62E+00, 3.46E+00, 1.96E+00, 1.13E+00, 5.89E-01, 4.12E-01, 2.48E-01, 1.49E-01, 1.13E-01],
         [5.62E+00, 3.46E+00, 1.98E+00, 1.18E+00, 6.67E-01, 5.06E-01, 3.57E-01, 2.66E-01, 2.31E-01],
         [5.63E+00, 3.47E+00, 2.01E+00, 1.24E+00, 7.80E-01, 6.42E-01, 5.17E-01, 4.45E-01, 4.19E-01],
         [5.63E+00, 3.49E+00, 2.06E+00, 1.35E+00, 9.54E-01, 8.50E-01, 7.63E-01, 7.18E-01, 7.03E-01],
         [5.63E+00, 3.51E+00, 2.13E+00, 1.50E+00, 1.20E+00, 1.13E+00, 1.08E+00, 1.06E+00, 1.05E+00],
         [5.64E+00, 3.56E+00, 2.31E+00, 1.85E+00, 1.68E+00, 1.65E+00, 1.63E+00, 9.99E+02, 9.99E+02],
         [5.65E+00, 3.63E+00, 2.55E+00, 2.23E+00, 2.15E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.67E+00, 3.74E+00, 2.86E+00, 2.68E+00, 2.65E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.70E+00, 3.90E+00, 3.24E+00, 3.15E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.76E+00, 4.22E+00, 3.85E+00, 3.82E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.85E+00, 4.58E+00, 4.38E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [5.99E+00, 5.00E+00, 4.91E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [6.16E+00, 5.46E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [6.47E+00, 6.11E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
         [6.60E+00, 6.50E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02]]

t_a_NEU = [0]*len(u_inv_a)
s_a_NEU = [0]*len(u_inv_a)
t_b_NEU = [0]*len(u_inv_b)
s_b_NEU = [0]*len(u_inv_b)

# Select data
# Data from Viterbo 2023
m_time = [0.083333333, 1, 1.416666667, 2.166666667, 2.5, 2.916666667, 3.566666667, 3.916666667, 4.416666667, 4.833333333, 5.633333333, 6.516666667, 7.5, 8.916666667, 10.13333333, 11.16666667, 12.6, 16.5, 18.53333333, 22.83333333, 27.15, 34.71666667, 39.91666667, 48.21666667, 60.4, 72.66666667, 81.91666667, 94.66666667, 114.7166667, 123.5]
m_ddown = [0.04, 0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285, 0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415, 0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525, 0.53, 0.56, 0.57, 0.58]
# Parameters needed to solve Theis (From the SYMPLE example/excercise) !!! UPDATE !!!
r = 130       # m
b = 8.5       # m
Qs = 0.3/60   # m^3/s
Qd = Qs*60*60*24 # m^3/d

m_time_s = [i*60 for i in m_time] # time in seconds
num_times = len(m_time)

st.subheader(':green[Inverse parameter fitting]', divider="rainbow")

st.markdown("""
            Subsequently, you can modify the transmissivity and the storativity to fit the measured data to the Neuman type curves. For precise fitting, you can change the plot resolution with the toogle. Additionally, you can perform a prediction of drawdown for specific times/spaces.
"""
)

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
        Ss = 10 ** S_slider_value
        # Display the logarithmic value
        st.write("_Specific storage_ (dimensionless):** %5.2e" %Ss)
        refine_plot = st.toggle("**Refine** the range of the **Data matching plot**")
    with columns2[1]:
        SY = st.slider('Specific Yield', 0.01, 0.50, 0.25, 0.01, format="%4.2f")
        eta = st.selectbox("Eta",(1, 2, 3, 4, 5, 6, 7, 8, 9),)
        show_data = st.toggle("**Show measured data from Viterbo 2023**")
    
    # Compute K and SS to provide parameters for plausability check
    # (i.e. are the parameter in a reasonable range)
    K = T/b     # m/s
    S = Ss * b
    
    # Early (a) and late (b) Theis curve
    t_a_term = r**2 * S / 4 / T
    t_b_term = r**2 * SY / 4 / T
    s_term = Qs/(4 * np.pi * T)

    t_a = u_inv * t_a_term
    t_b = u_inv * t_b_term
    s = w_u * s_term

    # Early Neuman curve
    for x in range(0,len(u_inv_a)):
        t_a_NEU[x] = u_inv_a[x] * t_a_term
        s_a_NEU[x] = w_u_a[x][eta-1] * s_term
    
    # Late Neuman curve
    for x in range(0,len(u_inv_b)):
        t_b_NEU[x] = u_inv_b[x] * t_b_term
        if (w_u_b[x][eta-1] == 999):
            s_b_NEU[x] = well_function(1/u_inv_b[x]) * s_term
        else:
            s_b_NEU[x] = w_u_b[x][eta-1] * s_term
        
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(t_a, s, label=r'Computed drawdown early -Theis')
    ax.plot(t_b, s, label=r'Computed drawdown late -Theis')
    ax.plot(t_a_NEU, s_a_NEU, 'b--', label=r'Computed drawdown early - Neuman')
    ax.plot(t_b_NEU, s_b_NEU, '--', color='darkorange', label=r'Computed drawdown late - Neuman')
    if show_data:
        ax.plot(m_time_s, m_ddown,'ro', label=r'measured drawdown')
    plt.yscale("log")
    plt.xscale("log")
    if refine_plot:
        plt.axis([1E1,1E5,1E-3,1E+1])
    else:
        plt.axis([1E-1,1E8,1E-4,1E+1])
    ax.set(xlabel='t', ylabel='s',title='Neuman drawdown')
    ax.grid(which="both")
    plt.legend()
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
 
inverse()
