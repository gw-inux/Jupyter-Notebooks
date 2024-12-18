#--------------------------------------#
# Import libraries                     #
#--------------------------------------#
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from scipy import special
import warnings
warnings.filterwarnings("ignore")

#--------------------------------------#
# Streamlit title and text             #
#--------------------------------------#
st.title("Solute transport and the principle of superposition")
st.subheader(':rainbow[An example] data', divider="rainbow")

st.markdown("""
    ### The situation
    
    We have an aquifer with a saturated thickness of 20 m, porosity of 0.1, and hydraulic conductivity of 5 m/d. The river is completely contaminated by two pollution episodes separated by 5 days. In response to the pollution, chlorides enter the aquifer.

    The first pollution episode can be represented as a constant pulse with a concentration of 800 mg/L that lasts for 30 days. The second pollution episode is a constant pulse with a concentration of 600 mg/L that lasts for 40 days. After 80 days from the start of the pollution, the river returns to its initial chemical state (zero chlorides).
    
    It is assumed that chlorides are neither adsorbed nor degraded in the aquifer.
    """)
    
st.image('90_Streamlit_apps/GWP_1D_Conservative_Transport/assets/images/superposition_principle_figure.PNG', caption = "Case example.")

st.markdown("""
The following is requested:

**(A)** Calculate the travel time of the chlorides to point A.  
**(B)** Calculate the concentration of chlorides at point A after 440 days.
**(C)** Calculate the maximum concentration of chlorides that will reach point A.

""", unsafe_allow_html=True)

#--------------------------------------#
# Functions                            #
#--------------------------------------#
def advective_velocity(K, i, phi):
    """Calculates the advective velocity.

    Parameters
    ----------
    K : float
        hydraulic conductivity
    i : float
        hydraulic gradient, as the change in water level per unit of distance.
    phi : float
        porosity

    Returns
    -------
    float
        advective velocity
    """
    v = ((K*i))/phi
    return v

def travel_time(k1, i1, phi1, x1, k2, i2, phi2, x2):
    """Calculates the travel time with the velocities from the two Sectors.

    Parameters
    ----------
    k1 : float
        Hydraulic Conductivity from the first Sector
    i1 : float
        Hydraulic Gradient from the first Sector
    phi1 : float
        Porosity form the first Sector
    x1 : float
        Distance from the River to the second Sector
    k2 : float
        Hydraulic Conductivity from the second Sector
    i2 : float
        Hydraulic Gradient from the first Sector
    phi2 : float
        Porosity form the second Sector
    x2 : float
        Distance from the second Sector to the Point A

    Returns
    -------
    float(s)
        velocity in the first Sector; velocity in the second Sector; the travel time
    """
    
    v1 = advective_velocity(k1, i1, phi1)
    v2 = advective_velocity(k2, i2, phi2)    
    
    t = (x1/v1) + (x2/v2)
    
    return v1, v2, t   
    
def dispersivity(x):
    """Estimates dispersivity with a semi-empirical equation.

    Parameters
    ----------
    x : floar
        total distance from the river to Point A

    Returns
    -------
    float
        dispersivity
    """
    alpha = 0.83*(np.log10(x))**2.414
    return alpha
   
def dispersion(alpha, v):
    """Calculates the dispersion.

    Parameters
    ----------
    alpha : flaot
        dispersivity 
    v : float
        velocity

    Returns
    -------
    float
        dispersion
    """
    D = alpha * v
    return D

def oneD_continous_injection(Ci, x, v, t, D):
    """Function that calculates the concentration in a one-dimensional continous injection,
    with no adsorption or decay

    Parameters
    ----------
    Ci : float
        initial concentration
    x : float
        x position
    v : float
        velocity
    t : float
        time
    D : float
        dispersion

    Returns
    -------
    float
        concentration 
    """
    
    term1 = special.erfc((x - (v*t))/(np.sqrt(4*D*t)))
    term2 = np.exp((v*x)/D)
    term3 = special.erfc(x+(v*t)/np.sqrt(4*D*t))
       
    if (v*x)/D > 100:
        C = (Ci/2) * (term1)
    else:
        C = (Ci/2) * (term1 + term2 * term3)
    
    return C

#--------------------------------------#
# Two-column layout                    #
#--------------------------------------#
col1, col2 = st.columns(2)

#--------------------------------------#
# Inputs for Sector 1                  #
#--------------------------------------#
with col1:
    st.header("Sector 1")
    k1 = st.number_input("Hydraulic conductivity Sector 1 [m/d]:", min_value=0.0, value=0.0)
    x1 = st.number_input("Distance Sector 1 [m]:", min_value=2.0, value=2.0)
    i1 = st.number_input("Gradient Sector 1 [-]:", min_value=0.0000, value=0.0000, format = "%.4f")
    phi1 = st.number_input("Porosity Sector 1 [-]:", min_value=0.0, value=0.0)

#--------------------------------------#
# Inputs for Sector 2                  #
#--------------------------------------#
with col2:
    st.header("Sector 2")
    k2 = st.number_input("Hydraulic conductivity Sector 2 [m/d]:", min_value=0.0, value=0.0)
    x2 = st.number_input("Distance Sector 2 [m]:", min_value=2.0, value=2.0)
    i2 = st.number_input("Gradient Sector 2 [-]:", min_value=0.0000, value=0.0000, format = "%.4f")
    phi2 = st.number_input("Porosity Sector 2 [-]:", min_value=0.0, value=0.0)

#--------------------------------------#
# Button to perform calculations       #
#--------------------------------------#
if st.button("Click to Solve"):
    v1, v2, arrival_time = travel_time(k1, i1, phi1, x1, k2, i2, phi2, x2)
    total_distance = x1 + x2
    mean_velocity = total_distance / arrival_time
    alpha = dispersivity(total_distance)
    D = dispersion(alpha, mean_velocity)

    # Generate concentrations
    time = np.arange(1, 1001, 1)
    Ca = np.zeros(len(time))
    Cb = np.zeros(len(time))
    Cc = np.zeros(len(time))
    Cd = np.zeros(len(time))

    for t in range(len(Ca)):
        Ca[t] = oneD_continous_injection(800, total_distance, mean_velocity, time[t], D)
    for t in range(len(Ca)):
        if t > 30:
            Cb[t] = oneD_continous_injection(800, total_distance, mean_velocity, time[t] - 30, D)
    for t in range(len(Ca)):
        if t > 35:
            Cc[t] = oneD_continous_injection(600, total_distance, mean_velocity, time[t] - 35, D)
    for t in range(len(Ca)):
        if t > 75:
            Cd[t] = oneD_continous_injection(600, total_distance, mean_velocity, time[t] - 75, D)

    Ctot = Ca - Cb + Cc - Cd
    Ctot_list = list(Ctot)
    idx_max = Ctot_list.index(np.nanmax(Ctot_list))

    # Results
    st.subheader("Results:")
    st.write(f"A - The travel time to point A is **{arrival_time:.2f} days**")
    st.write(f"B - The concentration value on day 440 is **{Ctot[440]:.2f} mg/l**")
    st.write(f"C - The max concentration value is **{np.nanmax(Ctot_list):.2f} mg/l**")

    # Plot
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(time, Ctot, label=None)
    ax.scatter(time[idx_max], np.nanmax(Ctot), color="red", label="Max Concentration")
    ax.scatter(440, Ctot[440], color="blue", label="Concentration day 440")
    ax.axvline(440, color="blue", linestyle=":", label=None)
    ax.axhline(Ctot[440], color="blue", linestyle=":")
    ax.axvline(time[idx_max], color="red", linestyle=":", label=None)
    ax.axhline(np.nanmax(Ctot), color="red", linestyle=":")
    ax.set_xlabel("Time [days]")
    ax.set_ylabel("Concentration [mg/l]")
    ax.legend()
    st.pyplot(fig)
