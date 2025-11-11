import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title = "iNUX - Green Ampt", page_icon="04_Basic_hydrogeology/FIGS/iNUX_wLogo.png")
# Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Grießer": [1],
    "Matthias Hausleber": [1]
}
institutions = {
    1: "Department of Earth Sciences, University of Graz"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title('Green-Ampt-Model for Infiltration')

with st.expander("Show explanation"):
        st.markdown(" Figure 1 shows a situation where the rainfall rate was greater than the infiltration rate " \
        "such that ponding occured and water infiltrates into the soil. " \
        "A similar situation occurs in experiments with double ring infiltrometers (Figure 2). ")

        st.image("04_Basic_hydrogeology/FIGS/Green_Ampt_Model.png", caption="Figure 1: Soil water profile for the case of ponding (a). Volumetric water content as a function of soil depth for a (b) 'real situation' and (c) assumptions underlying the Green-Ampt equation.")
        st.image("04_Basic_hydrogeology/FIGS/Doppelring-Infiltrometer.jpg", caption='Figure 2: Double Ring Infiltrometer', width=350)

        st.markdown("In these experiments, two concentric rings, which are partially inserted into the soil, " \
        "are filled with water. The water in the outer ring is intended to prevent lateral flow. " \
        "Therefore, we assume vertical infiltration in the inner ring as an approximation. " \
        "As a result of the ponding, a wetting front moves downward in the soil. " \
        r"In the wetted zone above the wetting front, the soil is saturated and has a water content $\theta_0$ close " \
        "to saturation (field saturated). " \
        r"Below this, the soil still has its initial water content $\theta_i$. " \
        "There is a (positive) pressure potential $h_0$ at the soil surface due to the ponding, "
        "and a (negative) matrix potential $h_f$ at the moisture front due to the unsaturated conditions. ")
        st.markdown("The conceptual model described above simplifies the distribution of the water content and " \
        "the matrix potential in the soil. Depending on the soil properties, the transition from field saturation to " \
        "initial conditions is less abrupt. However, the simplified assumption of a sharp wetting front allows " \
        "the derivation of a mathematical relationship between the cumulative infiltration $I(t)$ and " \
        "the time $t$ since the infiltration began:")
        st.latex(r'''I(t) - \Delta\theta \Delta h \ln \left( 1 + \frac{I(t)}{\Delta h} \right) = K_s t''')
        st.markdown(r"where $K_s$ is the hydraulic conductivity in the wetted zone and $\Delta\theta = \theta_0 - \theta_i$ and $\Delta h = h_0 - h_f$.")
        st.markdown("Although this equation cannot be solved for $I(t)$, we can solve it for $t$ "
        "and thus calculate and visualize the cumulative infiltration $I(t)$ for given values of the time $t$: ")
        st.latex(r'''t = \frac{I(t) - \Delta\theta \Delta h \ln \left(1 + \frac{I(t)}{\Delta\theta \Delta h} \right)}{K_s}''')
        st.markdown("To understand which and how the model parameters control the infiltration process, "
        "it is helpful to change the individual parameter values and examine the effects "
        "on the cumulative infiltration and the infiltration rate. "
        "The latter is obtained by divding the change of the cumulative infiltration in a short time intervall "
        "through the length of this time intervall.")

# TODO: notation for theta, delta latex?
with st.expander('Show variable descriptions'):
        st.latex(r'''\theta_0 \text{...water content in the soil before infiltration starts}''')
        st.latex(r'''\theta_i \text{...Water content after infiltration}''')
        st.latex(r'''\Delta \theta \text{...$theta_0 - theta_i$}''')
        st.latex(r'''h_0 \text{...Matrix potential at the ground surface}''')
        st.latex(r'''h_f \text{...Matrix potential at the wetting front}''')
        st.latex(r'''\Delta h \text{...$h_0 - h_f$}''')
        st.latex(r'''K_s \text{...Hydraulic conductivity of the saturated soil in the wetted zone}''')



with st.expander("Show typical parameter values"):
        st.markdown( r""" *Table 1: Typical parameter values (after Chin, D.A.: Water-Resources Enginieering, 2013).
        Please note that for the use in this app, the values of $K_s$ need to be transformed from mm/h to mm/min.
        The (field-)saturated water content $\theta_0$ can be approximated by value of porosity, 
        the initial water content $\theta_i$ is likely to range between field capacity and wilting point, 
        with the field capacitiy representing conditions a few days after a rain event and the wilting point 
        those after a long drought.* """)
        st.markdown(""" 
                | USD soil-texture class | Hydraulic conductivity [mm/h] | Suction head matrix potential [mm] | Porosity [-] | Field capacity [-] | Wilting point [-] |
                |------------|:--------------------------------------:|:-----------------:|:-------------:|:-------------:|:----------:|
                | Sand | 120 | -49 bis -150 | 0,437 | 0,062 | 0,024 |
                | Loamy sand | 30 | -61 bis -250 | 0,437 | 0,105 | 0,047 |
                | Sandy Loam | 11 | -110 bis -250 | 0,453 | 0,190 | 0,085 |
                | Loam | 3 | -89 bis -350 | 0,463 | 0,232 | 0,116 |
                | Silt Loam | 7 | -170 | 0,501 | 0,284 | 0,135 |
                | Sandy clay loam | 2 | -220 | 0,398 | 0,244 | 0,136 |
                | Clay loam | 1 | -210 | 0,464 | 0,310 | 0,187 |
                | silty clay loam | 1 | -270 | 0,471 | 0,342 | 0,210 |
                | Sandy clay | 1 | -240 | 0,430 | 0,321 | 0,221 |
                | Silty clay | 1 | -290 | 0,479 | 0,371 | 0,251 |
                | Clay | 0,3 | -320 bis -1000 | 0,475 | 0,378 | 0,265 |""",unsafe_allow_html=True,)


# Interactive Input
col3, col4, col5 = st.columns(3)
with col3:
        hf_h0 = st.slider(r'$h_f - h_0 \, \text{[mm]}$',-1000,500,[-600,0],1,key='hf_h0')
with col4:
        thetai_theta0 = st.slider(r'$\theta_i-\theta_0 \, \text{[-]}$' , 0.,0.5,[0.1,0.4],0.01,key='thetai_theta0')

log_options = np.round(np.concatenate([
    [v for v in np.arange(0.005, 0.01, 0.0001) if int(v * 1e4) % 10 == 0],  
    np.arange(0.01, 0.1, 0.01), 
    np.arange(0.1, 1, 0.1),    
    np.arange(1, 6, 1)         
]), decimals=4)

with col5:
        Ks = st.select_slider(r'$K_s \, \text{[mm/min]}$',log_options, value=0.5, key='Ks')

# Green Ampt Modell
def t_for_It(I_t, d_theta, d_h, Ks):                                                    
        return (I_t - d_theta * d_h * np.log(1+ (I_t/(d_theta*d_h))))/Ks                                    

def long_time_approximation(Ks, x):                                                          
        it_long = np.array([Ks]*len(x))                                                                  
        return it_long
  
def infiltration_rate(new_t, t, I_t):                                         
        y2 = np.interp(new_t, t, I_t)                                                                          
        i_t = np.diff(y2)
        return i_t

hf, h0 = hf_h0
theta_i, theta_0 = thetai_theta0
delta_theta = round(abs(theta_0-theta_i),2)
delta_h = round(abs(hf-h0),2)

I_t = np.arange(0.1, 1000, 0.1)                                                                     
t = t_for_It(I_t, delta_theta, delta_h, Ks) 
t2 = np.arange(round(t[0], 1), round(t[-1], 1), 0.01)                                       
i_t = infiltration_rate(t2, t, I_t)                                               
i_t_long = long_time_approximation(Ks, t2)                                             

# Plot
fig, (ax1, ax2) = plt.subplots(2, figsize=(8,8))

# plotting infiltration on one axis 
ax1.plot(t, I_t, color='black', 
    label='I(t): delta_h:{}, delta_theta:{:.2f}, Ks:{}'.format(delta_h, delta_theta, Ks), linewidth=1)                                      
        
ax1.set_title(label='Green-Ampt Infiltration Model', fontsize=20, loc= 'center')                 
ax1.set_xlim(0, 185)
ax1.set_xlabel('time [min]', fontsize=10)                                                         
ax1.set_ylabel('cummulative infiltration [mm/min]', fontsize=10)
ax1.grid(which = "major", linewidth = 1)                                                         
ax1.grid(which = "minor", linewidth = 0.2)
ax1.minorticks_on()
ax1.legend(loc='best')

# plotting infiltration rate and hydraulic conductivity as long time approximation in the second one
ax2.plot(t2[1:-5], i_t[0:-5]*100, color='black',
        label='i(t): delta_h:{}, delta_theta:{:.2f}, Ks:{}'.format(delta_h, delta_theta, Ks), linewidth=1)       
ax2.plot(t2, i_t_long, 'red', linestyle='--',                                         
        label='Long time approximation ~ Ks [mm/min]')
                                                                                   
ax2.set_xlim(0, 185)
ax2.set_yscale('log')                                                                                   
ax2.set_xlabel('time [min]', fontsize=10)                                                               
ax2.set_ylabel('infiltration rate [mm/min]', fontsize=10)
ax2.grid(which = "major", linewidth = 1)                                                               
ax2.grid(which = "minor", linewidth = 0.2)
ax2.minorticks_on()
ax2.legend(loc='best')  

if st.button('save line'):
        params = [I_t, t, i_t, t2, i_t_long, Ks, delta_theta, delta_h]
        if 'params' not in st.session_state:
            st.session_state['params'] = []
        st.session_state['params'].append(params)

if 'params' in st.session_state and st.session_state['params']:
    for i in st.session_state['params']:
        saved_I_t, saved_t, saved_i_t, saved_t2, saved_i_t_long, saved_Ks, saved_delta_theta, saved_delta_h = i
        ax1.plot(saved_t, saved_I_t, linestyle=':', 
                         label='I(t): delta_h:{}, delta_theta:{:.2f}, Ks:{}'.format(saved_delta_h, saved_delta_theta, saved_Ks), linewidth=1)
        ax1.legend(loc='best')

        ax2.plot(saved_t2[1:-5], saved_i_t[0:-5]*100, linestyle=':',
                         label='i(t): delta_h:{}, delta_theta:{:.2f}, Ks:{}'.format(saved_delta_h, saved_delta_theta, saved_Ks), linewidth=1)       
        
        ax2.plot(saved_t2, saved_i_t_long, linestyle='--', alpha=0.5, 
                         label='Long time approximation ~ Ks [mm/min]')
        ax2.legend(loc='best')


st.pyplot(fig)
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('04_Basic_hydrogeology/FIGS/CC_BY-SA_icon.png')



