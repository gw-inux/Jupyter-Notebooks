#-- Check and install required packages if not already installed --#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_book as stb

st.title('Soil Water Retention curves 💦')

# Authors, institutions, and year
year = 2025 
authors = {
    "Oriol Bertran": [1],  # Author 1 belongs to Institution 1
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "UPC Barcelona",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

st.subheader(':rainbow-background[Soil Water Retention curves: explanation & exercise]', divider="rainbow")

st.markdown(""" 
            ### Some initial thoughts for the investigation
            This notebook illustrate the soil water retention curves with examples and exercises based on :blue-background[[van Genuchten (1980)](https://www.researchgate.net/publication/250125437_A_Closed-form_Equation_for_Predicting_the_Hydraulic_Conductivity_of_Unsaturated_Soils1)].
"""
)

# FUNCTIONS
def m_val(n):
    """Function that returns the value of "m"
    Parameters
    ----------
    n : float
        value of "n"
    Returns
    -------
    float
        value of "m"
    """
    m = 1 - (1/n)
    return m

def dimensionless_water_content(t, tr, ts):
    """Function that calculates the dimensionless water content. 
    Based on van Genuchten, 1980 (Eq. 2) 
    Parameters
    ----------
    t : float
        soil-water content
    tr : float
        residual values of soil-water content
    ts : float
        saturated values of soil-water content
    Returns
    -------
    float
        dimensionless water content
    """ 
    T_dim = (t - tr)/(ts - tr)      
    return T_dim


def water_content(alpha, h, n):  
    """Function that calculates the water content.  
    Based on van Genuchten, 1980 (Eq. 3)
    Parameters
    ----------
    alpha : float
        alpha parameter
    h : float
        head pressure (positive)
    n : float
        n parameter
    Returns
    -------
    float
        water content
    """  
    T = ((1 + (alpha*h)**(n)))**(-(m_val(n)))  
    return T

def soil_water_content(tr, ts, alpha, h, n):
    """Function that calculates the soil-water content. 
    Based on van Genuchten, 1980 (Eq. 21)
    Parameters
    ----------
    tr : float
        residual values of soil-water content
    ts : float
        saturated values of soil-water content
    alpha : float
        alpha parameter
    n : float
        n parameter  
    Returns
    -------
    float
        soil-water content
    """
    t = tr + ((ts - tr) / ((1 + (alpha*h)**(n))**m_val(n)))   

    return t  

def relative_hydraulic_conductivity(alpha, n, h, T):
    """Function that calculates the relative hydraulic conductivity. 
    Based on van Genuchten, 1980 (Eq. 8 and 9).
    Parameters
    ----------
    alpha : float
        alpha parameter
    n : float
        n parameter
    h : float 
        head pressure (positive)
    T : float
        water content
    Returns
    -------
    T: float
        _description_
    Kr_T: float
        relative hydraulic conductivity expressed in terms of the dimensionless water content
    Kr_h: float
        relative hydraulic conductivity expressed in terms of the head pressure   
    Raises
    ------
    ValueError
        If m value is not between 0 and 1
    """
    
    # Check that m_val(n) is within the expected range
    if not (0 < m_val(n) < 1):
        raise ValueError("Parameter 'm' out of range: must be between 0 and 1")

    #-- Relative hydraulic conductivity expressed in terms of the water content
    Y = (1 - T**(1 / m_val(n)))**m_val(n)
    Kr_T = T**0.5 * (1 - Y)**2                     
    
    #-- Relative hydraulic conductivity expressed in terms of the pressure head
    I = (1 - alpha * h)
    U = I**(n - 1)
    P = (1 + (alpha * h)**n)**(m_val(n) / 2)
    
    if I > 0:
        Kr_h = ((U * T)**2) / P 
    else:
        Kr_h = np.nan                        
    
    return Kr_T, Kr_h

def soil_water_diffusivity(Ks, n, ts, tr, T):
    """Function that calculates the soil water diffusivity.
    Based on van Genuchten, 1980 (Eq. 11).
    Parameters
    ----------
    Ks : float
        hydraulic conductivity at saturation
    n  : float
        n parameter
    ts : float
        satured soil-water content
    tr : float
        residual soil-water content
    T : float
        dimensionless water content
    Returns
    -------
    D_T : float
        soil water diffusivity
    """  
    I = ((1 - m_val(n))*Ks) / (alpha*m_val(n)*(ts - tr))
    L = T**(0.5 - (1/m_val(n)))
    Y = (1 - T**(1 / m_val(n)))**m_val(n)
    P = ((1/Y) + (Y) - 2)
    
    D_T = I * L * P                                        

    return D_T

#  
#Example from Van Genuchten 1980
#

# Given parameters:
tr = 0.10       # residual water content
ts = 0.50       # saturated water content
alpha = 0.005   # l/cm
n = 2.0         # shape parameter
Ks = 100        # cm/day

#-- Generate pressure head values:
h_values = np.logspace(0, 6, 100)  

#-- Calculate water content values
t_values = [soil_water_content(tr, ts, alpha, h, n) for h in h_values]
T_values = [water_content(alpha, h, n) for h in h_values]

#-- Calculate dimensionless water content and relative hydraulic conductivity
Kr_T, Kr_h = zip(*[relative_hydraulic_conductivity(alpha, n, h, T) for h, T in zip(h_values, T_values)])
Kr_T = list(Kr_T)  
Kr_h = list(Kr_h) 

#-- Calculate the soil-water diffusivity
D_T = [soil_water_diffusivity(Ks, n, ts, tr, T) for T in T_values]

#-- Plot the 3 figures
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 5))

# ax1: Water content vs. Pressure head
ax1.plot(t_values, np.abs(h_values))
ax1.set_xlim(0, 0.6)
ax1.set_ylim(np.abs(h_values[0]), np.abs(h_values[-1]))
ax1.set_yscale('log')
ax1.set_xlabel(r'Water Content, $\Theta$')
ax1.set_ylabel(r'Pressure Head, $h$ [cm]')

# ax2: Water content vs. Relative Hydraulic Conductivity expressed in terms of water content
ax2.plot(t_values, Kr_T) 
ax2.set_yscale('log')
ax2.set_ylim(0.000001, 1)
ax2.set_xlim(0, 0.6)
ax2.set_xlabel(r'Water Content, $\Theta$')
ax2.set_ylabel(r'Relative Hydraulic Conductivity, $K_{r}$($\Theta$)')

# ax2: Water content vs. Relative Hydraulic Conductivity expressed in terms of pressure head
ax3.plot(np.abs(h_values), Kr_T) 
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlim(1, 10000)
ax3.set_ylim(0.000001, 1)
ax3.set_xlabel('Pressure Head, $h$ [cm] ')
ax3.set_ylabel(r'Relative Hydraulic Conductivity, $K_{r}($h$)$')

# ax4: Water content vs. Diffusivity
ax4.plot(t_values, D_T)
ax4.set_xlim(0, 0.6)
ax4.set_yscale('log')
ax4.set_ylim(1, 1000000)
ax4.set_xlabel(r'Water Content, $\Theta$')
ax4.set_ylabel(r'Diffusivity, $D$')

#plt.tight_layout()
st.pyplot(fig)

#
# Example for retention curves - Interactive plots
#


#-----------------------------------#
# From the table to a dataframe     #
#-----------------------------------#

#-- Sand Soil --#
sandSoil = pd.DataFrame()
sandSoil["Suction Pressure [hPa]"] = [1, 2, 3, 4, 8, 12, 17, 23, 32, 46, 65, 98, 148, 328, 726, 1217, 
                                      2175, 4330, 7576, 16796, 41464, 95973]
sandSoil["Water Content"] = [0.368, 0.365, 0.358, 0.348, 0.321, 0.293, 0.267, 0.240, 0.213, 0.185, 0.160, 
                             0.137, 0.119, 0.090, 0.074, 0.065, 0.059, 0.054, 0.051, 0.048, 0.046, 0.045]

#-- Silt Soil --#
siltSoil = pd.DataFrame()
siltSoil["Suction Pressure [hPa]"] = [1, 2, 6, 25, 49, 118, 235, 354, 488, 765, 1033, 1456, 2656, 4351, 
                                      6830, 13582, 26438, 45248, 98112, 199482, 396999, 958958]
siltSoil["Water Content"] = [0.422, 0.422, 0.421, 0.417, 0.412, 0.395, 0.366, 0.342, 0.319, 0.285, 0.260, 
                             0.236, 0.195, 0.167, 0.143, 0.113, 0.089, 0.074, 0.057, 0.045, 0.035, 0.026]


#-----------------------------------#
# Resolution and plot               # 
#-----------------------------------#

st.markdown(
            """
            ### Exercise
            Given the suction pressure and water content data for two soil types—sand and silt—determine the best-fitting parameters.
            """
)

data = {
        "Sand Soil |ψ| [hPa]": [1, 2, 3, 4, 8, 12, 17, 23, 32, 46, 65, 98, 148, 328, 726, 1217, 2175, 4330, 7576, 16796, 41464, 95973],
        "θ (Sand)": [0.368, 0.365, 0.358, 0.348, 0.321, 0.293, 0.267, 0.240, 0.213, 0.185, 0.160, 0.137, 0.119, 0.090, 0.074, 0.065, 0.059, 0.054, 0.051, 0.048, 0.046, 0.045],
        "Silt Soil |ψ| [hPa]": [1, 2, 6, 25, 49, 118, 235, 354, 488, 765, 1033, 1456, 2656, 4351, 6830, 13582, 26438, 45248, 98112, 199482, 396999, 958958],
        "θ (Silt)": [0.422, 0.422, 0.421, 0.417, 0.412, 0.395, 0.366, 0.342, 0.319, 0.285, 0.260, 0.236, 0.195, 0.167, 0.143, 0.113, 0.089, 0.074, 0.057, 0.045, 0.035, 0.026]
        }

# Convert to DataFrame
df = pd.DataFrame(data)

# Display the table with markdown
st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

st.markdown(
            """
            #### Parameters
            θr : Residual soil-water content of the soil
            θs : Satured soil-water content of the soil
            α : alpha parameter, related to the inverse of the air entry suction
            n : n parameter, is a mesure of the pore-size distribution
            """
)

columns_i1 = st.columns((1,1), gap = 'large')

with columns_i1[0]:
    tr_sand = st.slider(f':green-background[θr sand]',0.0,0.5,0.2,0.001)
    ts_sand = st.slider(f':green-background[θs sand]',0.0,0.5,0.2,0.001)
    alpha_sand = st.slider(f':green-background[α sand]',0.0,0.1,0.05,0.0001)
    n_sand = st.slider(f':green-background[n sand]',0.0,5.0,2.5,0.05)

with columns_i1[1]:
    tr_silt = st.slider(f':blue-background[θr silt]',0.0,0.5,0.3,0.001)
    ts_silt = st.slider(f':blue-background[θs silt]',0.0,0.5,0.3,0.001)
    alpha_silt = st.slider(f':blue-background[α silt]',0.0,0.1,0.05,0.0001)
    n_silt = st.slider(f':blue-background[n silt]',0.0,5.0,2.5,0.05)   

#-- Generating the range of head values
h_values = np.logspace(0, 6, 100)
      
#-- Calculating the soil-water content for both soild
t_sand = [soil_water_content(tr_sand, ts_sand, alpha_sand, h, n_sand) for h in h_values]
t_silt = [soil_water_content(tr_silt, ts_silt, alpha_silt, h, n_silt) for h in h_values]
    
#-- Plotting the results
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(sandSoil["Water Content"], sandSoil["Suction Pressure [hPa]"], 'o', mfc='none', 
        c="green", label="Observations Sand Soil")
ax.plot(siltSoil["Water Content"], siltSoil["Suction Pressure [hPa]"], 'o', mfc='none',
        c="blue", label="Observations Silt Soil")   
ax.plot(t_sand, h_values, 
        c="green", label="Model Sand Soil")
ax.plot(t_silt, h_values, 
        c="blue", label="Model Silt Soil")
ax.set_xlim(0, 0.5)
ax.set_ylim(1, 1000000)
ax.set_yscale('log')
ax.set_xlabel(r'Water Content, $\Theta$')
ax.set_ylabel('Suction Pressure [hPa]')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig.tight_layout()
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
st.pyplot(fig)

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/03_📈_▶️ The SWC in comparison.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/05_📈_▶️ SWC_Exercise_2.py")
   
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
