# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb

st.title('Theis parameter estimation and drawdown prediction')

st.subheader(':red-background[Fitting aquifer parameter to randomly generated data]', divider="red")

# Initial assessment

show_initial_assessment = st.toggle("**Show the initial assessment**")
if show_initial_assessment:
    columnsQ1 = st.columns((1,1), gap = 'large')
    
    with columnsQ1[0]:
        stb.single_choice(":red[**For which conditions is the Theis solution intended?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
        stb.single_choice(":red[**Question2?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
                  
    with columnsQ1[1]:
        stb.single_choice(":red[**Question3?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')             
        stb.single_choice(":red[**Question4?**]",
                  ["Answer1.", "Answer2", "Answer3", "Answer4"],
                  1,success='CORRECT!   ...', error='Not quite. ... If required, you can read again about transmissivity _T_ in the following ressources _reference to GWP books...')
"---"
st.markdown("""
            ### Computation of the drawdown
            Subsequently, the Theis equation is solved with Python routines. The interactive plot demonstrate the response of a confined aquifer to pumping. The results for the measured data are graphically presented in an interactive plot as red dots.
            
            Start your investigations with increasing the pumping rate. See how the drawdown changes. Modify the transmissivity _**T**_ and the storativity _**S**_ to fit the measured data to the well function.

            **Select the data below!** 
"""     
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
    
def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s
    
# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_min = -5
u_max = 4

u = np.logspace(u_min,u_max)
u_inv = 1/u
w_u = well_function(u)

# Select and generate data
columns = st.columns((10,80,10), gap = 'large')
with columns[1]:
    datasource = st.selectbox("**What data should be used?**",
    ("Random data with noise", "Synthetic textbook data"), key = 'Data')

if (st.session_state.Data == "Synthetic textbook data"):
    # Data from SYMPLE exercise
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    # Parameters needed to solve Theis (From the SYMPLE example/excercise)
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d
    m_time_s = [i*60 for i in m_time] # time in seconds
    num_times = len(m_time_s)
    
elif(st.session_state.Data == "Random data with noise"):
    r = 120       # m
    b = 10       # m
    Qs = 1.0/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d
    
    T_random = 1.23E-4*b*np.random.randint(1, 10000)/100
    S_random = 1E-5*b*np.random.randint(1, 10000)/100
    st.session_state.T_random = T_random
    st.session_state.S_random = S_random
    
    m_time_all  = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,35,40,45,50,55,60,70,80,90,100,110,120,130,140,150,160,170,180,210,240,270,300,330,360,420,480,540,600,660,720,780,840,900]
    m_time_all_s = [i*60 for i in m_time_all] # time in seconds
    m_ddown_all = [compute_s(T_random, S_random, i, Qs, r)*np.random.randint(80, 120)/100 for i in m_time_all_s] # time in seconds
    
    n_samples = np.random.randint(24, 49)
    m_time_s = m_time_all_s[:n_samples]
    num_times = len(m_time_s)
    m_ddown = m_ddown_all[:n_samples]
    # Parameters needed to solve Theis (From the SYMPLE example/excercise) !!! UPDATE !!!


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
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        T_slider_value=st.slider('(log of) **Transmissivity** in m2/s', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        T = 10 ** T_slider_value
        st.write("_Transmissivity_ in m2/s: %5.2e" %T)
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR STORATIVIT
        S_slider_value=st.slider('(log of) **Storativity**', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        S = 10 ** S_slider_value
        st.write("_Storativity_ (dimensionless):** %5.2e" %S)
        refine_plot = st.toggle("**Refine** the range of the **Theis matching plot**")
    with columns2[1]:
        prediction = st.toggle('Do the prediction')
        if prediction:
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
            auto_y = st.toggle("Adjust the range of drawdown plotting", value = True)

    if (st.session_state.Data == "Random data with noise"):
        columns4 = st.columns((1,1,1), gap = 'large')
        with columns4[1]:
            show_truth = st.toggle(":rainbow[Tell me how I did the inverse fitting!]")
        
    # Theis curve
    t_term = r**2 * S / 4 / T
    s_term = Qs/(4 * np.pi * T)

    t1 = u_inv * t_term
    s1 = w_u * s_term
    
    if prediction:
        # PLOT DRAWDOWN VS TIME
        # Range of delta_h / delta_l values (hydraulic gradient)
        t2 = np.linspace(1, max_t, 100)
        t2_h = t2/3600
        t2_d = t2/86400
        t2_mo = t2/2629800
        max_s = 30

        # Compute s for prediction h
        s  = compute_s(T, S, t2, Q_pred, r_pred)
        # Compute s for a specific point
        x_point = t_search
        y_point = compute_s(T, S, t_search, Q_pred, r_pred)

        if(st.session_state.Data == "Random data with noise"):
            # Compute true s for prediction
            true_s  = compute_s(T_random, S_random, t2, Q_pred, r_pred)
            true_y_point = compute_s(T_random, S_random, t_search, Q_pred, r_pred)
            
        fig = plt.figure(figsize=(12,7))
        ax = fig.add_subplot(1, 2, 1)
        #ax.plot(u_inv, w_u)
        ax.plot(t1, s1, label=r'Computed drawdown - Theis')
        #ax.plot(um_inv[:num_times], w_um[:num_times],'ro')
        ax.plot(m_time_s, m_ddown,'ro', label=r'synthetic drawdown with random noise')
        plt.yscale("log")
        plt.xscale("log")
        if refine_plot:
            plt.axis([1,1E5,1E-2,10])
        else:
            plt.axis([1,1E7,1E-4,1E+4])
            ax.text((2),1.8E-4,'Coarse plot - Refine for final fitting')
        plt.xlabel(r'time t in (s)', fontsize=14)
        plt.ylabel(r'drawdown s in (m)', fontsize=14)
        plt.title('Theis drawdown', fontsize=16)
        ax.grid(which="both")
        plt.legend(('well function','measured'))

        ax = fig.add_subplot(1, 2, 2)
        if per_pred <= 3:
            plt.plot(t2, s, linewidth=3., color='r', label=r'Drawdown prediction')
            if(st.session_state.Data == "Random data with noise"):
                if show_truth:
                    plt.plot(t2, true_s, linewidth=3., color='g', label=r'Drawdown prediction with "true" parameters')
                    plt.plot(t_search,true_y_point, marker='o', color='g',linestyle ='None', label='"true" drawdown output')            
            plt.plot(t_search,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
            plt.xlabel(r'Time in sec', fontsize=14)
            plt.xlim(0, max_t)
        elif per_pred <= 7:
            plt.plot(t2_h, s, linewidth=3., color='r', label=r'Drawdown prediction')
            if(st.session_state.Data == "Random data with noise"):
                if show_truth:
                    plt.plot(t2_h, true_s, linewidth=3., color='g', label=r'Drawdown prediction with "true" parameters')   
                    plt.plot(t_search_h,true_y_point, marker='o', color='g',linestyle ='None', label='"true" drawdown output')
            plt.plot(t_search_h,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
            plt.xlabel(r'Time in hours', fontsize=14)
            plt.xlim(0, max_t/3600)
        elif per_pred <= 366:
            plt.plot(t2_d, s, linewidth=3., color='r', label=r'Drawdown prediction')
            if(st.session_state.Data == "Random data with noise"):
                if show_truth:
                    plt.plot(t2_d, true_s, linewidth=3., color='g', label=r'Drawdown prediction with "true" parameters') 
                    plt.plot(t_search_d,true_y_point, marker='o', color='g',linestyle ='None', label='"true" drawdown output')            
            plt.plot(t_search_d,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
            plt.xlabel(r'Time in days', fontsize=14)
            plt.xlim(0, max_t/86400)
        else:
            plt.plot(t2_mo, s, linewidth=3., color='r', label=r'Drawdown prediction')
            if(st.session_state.Data == "Random data with noise"):
                if show_truth:
                    plt.plot(t2_mo, true_s, linewidth=3., color='g', label=r'Drawdown prediction with "true" parameters')
                    plt.plot(t_search_mo,true_y_point, marker='o', color='g',linestyle ='None', label='"true" drawdown output')            
            plt.plot(t_search_mo,y_point, marker='o', color='b',linestyle ='None', label='drawdown output')
            plt.xlabel(r'Time in months', fontsize=14)
            plt.xlim(0, max_t/2629800)

        if auto_y:
            plt.ylim(bottom=0, top=None)
        else:
            plt.ylim(bottom=0, top=max_s)
        ax.invert_yaxis()
        plt.ylabel(r'Drawdown in m', fontsize=14)
        plt.title('Drawdown prediction with Theis', fontsize=16)
        plt.legend()
        plt.grid(True)
        st.pyplot(fig)
    else:
        fig = plt.figure(figsize=(10,7))
        ax = fig.add_subplot(1, 1, 1)
        #ax.plot(u_inv, w_u)
        ax.plot(t1, s1, label=r'Computed drawdown - Theis')
        #ax.plot(um_inv[:num_times], w_um[:num_times],'ro')
        ax.plot(m_time_s, m_ddown,'ro', label=r'synthetic drawdown with random noise')
        plt.yscale("log")
        plt.xscale("log")
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        if refine_plot:
            plt.axis([1E0,1E4,1E-2,1E+1])
        else:
            plt.axis([1,1E7,1E-4,1E+2])
            ax.text((2),1.8E-4,'Coarse plot - Refine for final fitting')
        ax.grid(which="both")
        plt.xlabel(r'time t in (s)', fontsize=14)
        plt.ylabel(r'drawdown s in (m)', fontsize=14)
        plt.title('Theis drawdown', fontsize=16)
        plt.legend(fontsize=14)
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
        if(st.session_state.Data == "Random data with noise"):
            if show_truth:
                st.write("**'True' Transmissivity T** = ","% 10.2E"% st.session_state.T_random, " m^2/s.")
                st.write("_Your fitting success is:  %5.2f_" %(T/T_random*100), " %")
                st.write("**'True' Storativity    S** = ","% 10.2E"% st.session_state.S_random, "[-].")    
                st.write("_Your fitting success is:  %5.2f_" %(S/S_random*100), " %")

    with columns3[1]:
        if prediction:
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
            if(st.session_state.Data == "Random data with noise"):
                if show_truth:
                    st.write("Predicted drawdown ...(in m) with 'true' parameters:  %5.2f" %true_y_point)
                    st.write("Difference (in m):  %5.2f" %(true_y_point-y_point))

inverse()

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/05_📈_▶️ Neuman_solution.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/07_📈_▶️ Pumping Test Analysis.py")