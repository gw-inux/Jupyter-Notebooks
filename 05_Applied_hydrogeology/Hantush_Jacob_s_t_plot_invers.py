# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import pandas as pd
import streamlit as st

st.title('Hantush Jacob parameter estimation')
st.subheader('Understanding the Hantush Jacob (1955) solution  for :blue[leaky aquifers]', divider="blue")
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
w_u = well_function(u)

u_HAN = [1.00E-05, 2.00E-05, 4.00E-05, 6.00E-05, 1.00E-04, 2.00E-04, 4.00E-04, 6.00E-04, 1.00E-03, 2.00E-03, 4.00E-03, 6.00E-03, 1.00E-02, 2.00E-02, 4.00E-02, 6.00E-02, 1.00E-01, 2.00E-01, 4.00E-01, 6.00E-01, 1 , 2]

t_HAN     = [0]*len(u_HAN)
s_HAN     = [0]*len(u_HAN)
u_inv_HAN = [0]*len(u_HAN)

for x in range(0,len(u_HAN)):
        u_inv_HAN[x] = 1/u_HAN[x]

# Hantush Jacob type curve data from tables

w_u_HAN = [[9.420E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.300E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.010E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [8.770E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [8.400E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [7.820E+00, 6.620E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [7.190E+00, 6.450E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [6.800E+00, 6.270E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [6.310E+00, 5.970E+00, 4.830E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 5.450E+00, 4.710E+00, 3.500E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 4.850E+00, 4.420E+00, 3.480E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 4.480E+00, 4.180E+00, 3.430E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 4.000E+00, 3.810E+00, 3.290E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 3.340E+00, 3.240E+00, 2.950E+00, 2.180E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 2.630E+00, 2.480E+00, 2.020E+00, 1.520E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 2.260E+00, 2.170E+00, 1.850E+00, 1.460E+00, 8.390E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 1.800E+00, 1.750E+00, 1.560E+00, 1.310E+00, 8.190E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 1.190E+00, 1.110E+00, 9.960E-01, 7.150E-01, 4.100E-01, 2.270E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 6.930E-01, 6.650E-01, 6.210E-01, 5.020E-01, 3.400E-01, 2.100E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 4.500E-01, 4.360E-01, 4.150E-01, 3.540E-01, 2.550E-01, 1.770E-01, 1.100E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 9.990E+02, 2.130E-01, 2.060E-01, 1.850E-01, 1.509E-01, 1.140E-01, 8.030E-02],
           [9.990E+02, 9.990E+02, 9.990E+02, 9.990E+02, 9.990E+02, 4.700E-02, 4.400E-02, 9.990E+02, 3.400E-02, 2.500E-02]]


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
        S = 10 ** S_slider_value
        # Display the logarithmic value
        st.write("_Storativity_ (dimensionless): %5.2e" %S)
        refine_plot = st.toggle("**Refine** the range of the **Data matching plot**")
    with columns2[1]:
        r_div_B_choice = st.selectbox("r/B",('0.01', '0.04', '0.1', '0.2', '0.4', '0.6', '1', '1.5', '2', '2.5'),)
        r_div_B_list = ['0.01', '0.04', '0.1', '0.2', '0.4', '0.6', '1', '1.5', '2', '2.5']
        r_div_B = r_div_B_list.index(r_div_B_choice)
        show_data = st.toggle("**Show measured data from Viterbo 2023**")
    
    # Compute K and SS to provide parameters for plausability check
    # (i.e. are the parameter in a reasonable range)
    K = T/b     # m/s
    
    # Theis curve
    t_term = r**2 * S / 4 / T
    s_term = Qs/(4 * np.pi * T)

    t = u_inv * t_term
    s = w_u * s_term

    # Hantush Jacob curve
    for x in range(0,len(u_HAN)):
        t_HAN[x] = u_inv_HAN[x] * t_term
        if (w_u_HAN[x][r_div_B] == 999):
            s_HAN[x] = well_function(1/u_inv_HAN[x]) * s_term
        else:
            s_HAN[x] = w_u_HAN[x][r_div_B] * s_term
        
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(t, s, label=r'Computed drawdown - Theis')
    ax.plot(t_HAN, s_HAN, 'b--', label=r'Computed drawdown - Hantush Jacob')
    ax.plot(m_time_s, m_ddown,'ro', label=r'measured drawdown')
    plt.yscale("log")
    plt.xscale("log")
    if refine_plot:
        plt.axis([1E1,1E5,1E-3,1E+1])
    else:
        plt.axis([1E-1,1E8,1E-4,1E+1])
    ax.set(xlabel='t', ylabel='s',title='Hantush Jacob drawdown')
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
