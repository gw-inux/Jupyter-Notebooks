# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button

st.title(':red[Explore Uncertainty] associated with using estimated parameters based on the Theis Solution for drawdown prediction')

st.markdown("""
            ### Introduction
            
            Randomly generated data are provided for fitting the Theis (1935) Solution to estimate the transmissivity and storativity of the aquifer.
            
            Then, in a subsequent step, the estimated parameters are used to predict drawdown at a user specified distance from the well for a user specified duration of pumping at a user dpecifed rate. 
            
            """)
            
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Pumping_Test_Analysis/assets/images/drawdown_aquifer.png', caption="Cross section of a pumped confined aquifer, Kruseman et al., 1991")
            
st.markdown("""
            
            The **objective of this exercise** is to estimate aquifer properties using the Theis solution and assess the accuracy of predictions made with these estimated parameters.
            
            Considering these **key questions** may help you to prepare for the exercise:
            - How does the accuracy of the estimated parameters affect drawdown predictions?
            - What are potential sources of error in parameter estimation?
            - How does uncertainty in the data influence predictions?
            
            It is useful to consider the initial assessment questions before proceding with the investigation.
"""
)

"---"   
# Initial assessment
lc0, mc0, rc0 = st.columns([1,2,1])
with mc0:
    show_initial_assessment = button('Show/Hide the initial **assessment**', key= 'button1')
    
if show_initial_assessment:
    columnsQ1 = st.columns((1,1), gap = 'large')
    
    with columnsQ1[0]:
        stb.single_choice(":blue[**What conditions are appropriate for use of the Theis Solution?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, semiconfined aquifer",
                  "Transient flow, semiconfined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  1,success='CORRECT! Theis is designed for transient flow in a fully confined aquifer', error='This is not correct. You can learn more about the Theis Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 8](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
      
        stb.single_choice(":blue[**What is the main goal of fitting pumping test data to curves describing drawdown in response to pumping?**]",
                  ["To determine unknown aquifer properties from observed data", "To predict the future pumping rate of a well", "To measure the depth of the groundwater table", "To calculate the hydraulic gradient"],
                  0,success='CORRECT! to determine unknown aquifer properties from observed data', error='This is not correct. You can learn more about the goal of fitting pumping test data to type curves by exploring the previous pages of this Pumping Test Analysis application. Feel free to answer again.')      
                  
        stb.single_choice(":blue[**If the estimated transmissivity (T) is too low, how will the predicted drawdown compare to the true drawdown?**]",
                  ["The predicted drawdown will be too small", "The predicted drawdown will remain unchanged", "The predicted drawdown will be too large", "The predicted drawdown will be too large or too small depending on the distance from the well"],
                  3,success='CORRECT!The predicted drawdown will be too large near the well, too small far from the well and may be correct at one point between the near and far field', error='This is not completely correct. Feel free to answer again.')
        
    with columnsQ1[1]:        
        stb.single_choice(":blue[**What role does curve fitting to pumping test data play in the process of estimating aquifer parameters?**]",
                  ["It predicts future rainfall effects on groundwater levels", "It determines the total groundwater storage in the aquifer", "It estimates the pumping rate required for full aquifer depletion", "It helps visually compare theoretical and observed drawdown curves"],
                  3,success='CORRECT! It helps visually compare theoretical models and observed drawdown data', error='This is not correct. It may help to consider how veiwing the curves and data on the same graph was useful on previous pages of this application. Feel free to answer again.')  
 
        stb.single_choice(":blue[**Why is it important to compare predicted drawdown using estimated parameters with the true drawdown?**]",
                  ["To determine the maximum sustainable pumping rate", "To evaluate the accuracy of the parameter estimation process", "To find out if the aquifer is unconfined or confined", "To measure the recharge rate of the aquifer"],
                  1,success='CORRECT! To evaluate the accuracy of the parameter estimation process', error='This is not correct. It may help to think a bit more about the value of comparing predictions with true evants. Feel free to answer again.')
                  
        stb.single_choice(":blue[**Which parameters are estimated using the Theis solution and pumping test data?**]",
                  ["Hydraulic Conductivity and Porosity", "Transmissivity and Storativity", "Specific Yield and Permeability", "Pumping Rate and Aquifer Thickness"],
                  1,success='CORRECT! Transmissivity and Storativity', error='This is not correct. It may help to visit the Theis Solution page of this application and rethink your answer. Feel free to answer again.')   
                
"---"
st.markdown("""
            ### Parameter estimation and drawdown prediction

            In this section, you can **adjust the values of transmissivity and storativity until the Theis curve of drawdown versus time that is calculated and plotted on the graph matches the data**. The match indicates that the selected values are a reasonable representation of the aquifer properties.
            
            Each time that you select "Random data with noise", a new set of drawdown versus time data will be generated using a pumping rate of Q = 0.017 m³/s, an observation well at r = 120 m, and assuming a random value for T and S.
            
            The generated "measured" data are presented as red dots on the graph. For more precise matching, you can zoom in by using the toogle switch. Also you can elect to show data from a longer pumping test.
           
            These steps can be followed to estimate parameter values and make a prediction of drawdown and assess the quality of the prediction:
            - Step 1: Estimate the values of _T_ and _S_ by adjusting the sliders until the Theis curve, calculated using those values, matches the "measured" data. Zooming in and/or opting to toggle the 'Provide data for a longer period of pumping' may help you find a better fit.
            - Step 2: Toggle 'Make the prediction'
            - Step 3: Select the values of pumping rate, duration, and distance from the well that you are interested in for the prediction of future drawdown. For example, you might select:
                - Pumping rate for the prediction of 0.04 m³/s
                - Distance from the pumping well of 500 m
                - Duration of prediction period of 5 years (entered as 1825 days).
            - Step 3: Compare predictions using true versus estimated parameters (slider 'How accurate are the parameter value estimates?')
            - Step 4: Make note of how close your prediction is to the "true" system generated for this case and whether it is better or worse for shorter or longer distance and/or time. Consider whether the fit obtained using data from a longer test made much improvement in the predictino and, if so, in what way.
            - Step 5: While the prediction graph is open, experiment with adjusting the estimated _T_ and _S_ to observe how subtle chnges in estimated parameters impact the prediction.
           
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
    
    m_time_all  = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,35,40,45,50,55,60,70,80,90,100,110,120,130,140,150,160,170,180,210,240,270,300,330,360,420,480,540,600,660,720,780,840,900, 960, 1020, 1080, 1140, 1200, 1260, 1320, 1380, 1440, 1500]
    m_time_all_s = [i*60 for i in m_time_all] # time in seconds
    m_ddown_all = [compute_s(st.session_state.T_random, st.session_state.S_random, i, Qs, r)*np.random.randint(80, 120)/100 for i in m_time_all_s] # time in seconds
    
    n_samples_long = np.random.randint (35, 49)
    n_samples_short = np.random.randint (16, 22)


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
        container = st.container()
        T_slider_value=st.slider('_(log of) Transmissivity in m²/s_', log_min1,log_max1,-3.0,0.01,format="%4.2f" )
        T = 10 ** T_slider_value
        container.write("**Transmissivity in m²/s:** %5.2e" %T)
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR STORATIVIT
        container = st.container()
        S_slider_value=st.slider('_(log of) Storativity_', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
        S = 10 ** S_slider_value
        container.write("**Storativity (dimensionless):** %5.2e" %S)
        if(st.session_state.Data == "Random data with noise"):
            long = st.toggle('**Provide data for a longer pumping test**')
        refine_plot = st.toggle("**Zoom in** on the **data in the graph**")
    with columns2[1]:
        prediction = st.toggle('**Make the prediction**')
        if prediction:
            Q_pred = st.slider(f'**Pumping rate** (m³/s) for the **prediction**', 0.001,0.100,Qs,0.001,format="%5.3f")
            r_pred = st.slider(f'**Distance** (m) from the **well** for the **prediction**', 1,1000,r,1)
            per_pred = st.slider(f'**Duration** of the **prediction period** (days)',1,3652,3,1) 
            max_t = 86400*per_pred
            if per_pred <= 3:
                t_search = st.slider(f'**Select time (s) for printout below graph**', 1,max_t,1,1)
            elif per_pred <= 7:
                t_search_h = st.slider(f'**Select time (hours) for printout below graph**', 1.,24.*per_pred,1.)
                t_search = t_search_h*3600
            elif per_pred <= 366:
                t_search_d = st.slider(f'**Select time (days) for printout below graph**', 1.,per_pred*1.0,1.)
                t_search = t_search_d*86400
            else:
                t_search_mo = st.slider(f'**Select time (months) for printout below graph**', 1.,per_pred/30.4375,1.)
                t_search = t_search_mo*2629800
            auto_y = st.toggle("Adjust the range of drawdown plotting", value = True)

    if (st.session_state.Data == "Random data with noise"):
        columns4 = st.columns((1,1,1), gap = 'large')
        with columns4[1]:
            show_truth = st.toggle(":rainbow[How accurate are the parameter value estimates?]")
        
    if long:
        n_samples = n_samples_long
    else:
        n_samples = n_samples_short
    m_time_s = m_time_all_s[:n_samples]
    num_times = len(m_time_s)
    m_ddown = m_ddown_all[:n_samples]
        
        
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
        st.write("**Estimated Parameters**")
        st.write("**Distance of measurement from the well r = %3i" %r," m**")
        st.write("**Pumping rate of measurement Q = %5.3f" %Qs," m³/s**")
        st.write("**Thickness of formation b = %5.2f" % b, " m**")
        st.write("**Transmissivity T = %10.2E" %T, " m²/s**")
        st.write("**Hydraulic Conductivity K = %10.2E" %(T/b), " m²/s**")
        st.write("**Storativity S = %10.2E" %S, "[-]**")
        if(st.session_state.Data == "Random data with noise"):
            if show_truth:
                st.write("**'True' Transmissivity T = % 10.2E"% st.session_state.T_random, " m²/s**")
                st.write("_Your fitting success is:  %5.2f_" %(T/T_random*100), " %")
                st.write("**'True' Storativity    S = % 10.2E"% st.session_state.S_random, "[-]**")    
                st.write("_Your fitting success is:  %5.2f_" %(S/S_random*100), " %")

    with columns3[1]:
        if prediction:
            st.write("**Prediction**")
            st.write("**Distance of measurement from the well r = %3i" %r_pred," m**")
            st.write("**Pumping rate of prediction Q = %5.3f" %Q_pred," m³/s**")
            st.write("**Time since pumping started = %3i" %x_point," s**")
            if per_pred <= 3:
                st.write("**Time since pumping started t = %3i" %t_search," s**")
            elif per_pred <= 7:
                st.write("**Time since pumping started t = %5.2f" %t_search_h," hrs**")
            elif per_pred <= 366:
                st.write("**Time since pumping started t = %5.2f" %t_search_d," days**")
            else:
                st.write("**Time since pumping started t = %5.2f" %t_search_mo," months**")
            st.write("**Predicted drawdown at r and t  %5.2f" %y_point," m**")
            if(st.session_state.Data == "Random data with noise"):
                if show_truth:
                    st.write("**Predicted drawdown with 'true' parameters:  %5.2f" %true_y_point," m**")
                    st.write("**Difference**:  %5.2f" %(true_y_point-y_point)," m**")

inverse()

st.markdown (
    """   
    :blue
    ___
"""
) 

st.markdown("""
            ### Considering these **key questions** may help you process your experience and findings resulting from this exercise
            
            - How does accuracy of the estimated parameters affect drawdown predictions?
            - What are potential sources of error in estimating parameters by curve matching?
            - How does error in the data influence predictions?
"""
)

st.markdown (
    """   
    :green
    ___
"""
)     
st.markdown("""
[Kruseman, G.P., de Ridder, N.A., & Verweij, J.M.,  1991.](https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/) Analysis and Evaluation of Pumping Test Data, International Institute for Land Reclamation and Improvement, Wageningen, The Netherlands, 377 pages.
"""
)     
st.markdown("""
Theis, C.V., 1935. The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage, Transactions of the American Geophysical Union, volume 16, pages 519-524.
"""
)       

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/06_🎯_▶️ Pumping Test Analysis.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/08_👉_About.py")