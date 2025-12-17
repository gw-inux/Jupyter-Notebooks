import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pyet
import pandas as pd

# Page intro
st.header('Potential Evapotranspiration (ETP)')

selected_data = st.session_state.data

st.subheader(':violet-background[Introduction]', divider="violet")
st.markdown('''The Penman-Monteith equation (1) is a method to estimate potential evapotranspiration from a vegetated surface. 
    It was proposed by John Monteith in 1965, who developed the method based on the work of Howard Penman. Penman developed a equation combining energy balance and mass transfer.              
    In May 1990 the FAO held a consultation, in cooperation with other international organisations, to reassess common methods within the field of crop water requirements. 
    They came up with an adaptation (2) on the original Penman-Monteith equation. This equation requires data for wind speed, humidity, solar radiation and air temperature.
    For better compatibility the measurements should be taken at a standardised height of 2m. Else the measured values must be corrected.
    This method was developed, based on the assumption of a continuous grass surface as well as constant water supply.
    Further information can be found in the electronic version of the following FAO paper by Allen et al. (1998): [Crop Evapotranspiration](https://www.fao.org/4/x0490e/x0490e06.htm#chapter%202%20%20%20fao%20penman%20monteith%20equation). ''')

st.subheader(':violet-background[The \'original\' Penman-Monteith formula]', divider="violet")
st.latex(r'ETP_{PM} = \frac{\Delta*(R_n - G) + \rho_a*c_p*\frac{(e_s-e_a)}{r_a}}{\Delta + \lambda (1+ \frac{r_s}{r_a})} (1)')
st.markdown(r'''
        - $R_n$...net radiation
        - $G$... soil heat flux
        - $(e_s-e_a)$...vapour pressure deficit of the air
        - $\rho_a$...mean air density at constant pressure
        - $c_p$...specific heat of the air
        - $\Delta$...slope of the saturation vapour pressure temperature relationship
        - $\lambda$...psychometric constant
        - $r_s, r_a$...bulk surface and aerodynamic resistance''')

st.subheader(':violet-background[The adapted \'FAO-56\' version]', divider="violet")
st.latex(r'ETP_{PM_{FAO-56}} = \frac{0.408 \Delta (R_n-G)+\lambda \frac{900}{T+273}u_2(e_s-e_a)}{\Delta+\lambda(1+0.34u_2)} (2)')
st.markdown(r'''
        - $R_n$...net radiation
        - $G$... soil heat flux
        - $T$...mean daily air temperature at 2m height 
        - $u_2$...wind speed at 2m height
        - $e_s$...saturation vapour pressure
        - $e_a$...actual vapour pressure
        - $(e_s-e_a)$...vapour pressure deficit of the air
        - $\Delta$...slope of the vapoure pressure curve ?
        - $\lambda$...psychometric constant''')

st.subheader(':violet-background[Results]', divider="violet")
# ETP Pennman-Monteith - plot
fig3, ax3= plt.subplots(figsize=(12,5))
fig3.suptitle('ETP (Penman-Monteith) for Graz', fontsize=16)

rs_MJperm2=selected_data['rs']/1000000 #for the calculation the solar radiation is needed in MJ/m2
wind_2m=selected_data['wind_speed']*4.87/(np.log((67.8*20)-5.42)) #as the wind mesurements at uni-graz are taken higher the wind messurements need to be adjustet (~ 20 m above ground surface)

with st.expander('click here to take a look at the data, edit or save as csv'):
    st.session_state.ETP.PM = st.data_editor(st.session_state.ETP.PM)

ax3.set_title(f'from {min(st.session_state.ETP.index):%d-%m-%Y} to {max(st.session_state.ETP.index):%d-%m-%Y}')
## plot ETP
l31=ax3.plot(st.session_state.ETP.index, st.session_state.ETP.PM, color='darkblue', label='Evapotranspration, Pennman-Monteith', zorder=10)
ax3.set_ylabel(' $ETP_{pm}$ [mm/d] ')
ax3.spines['top'].set_visible(False)
## st.pills so the user can choose which additional data is shown
options3= ['wind', 'temperature', 'solar radiation', 'relative humidity']
selection3= st.pills('select (input) data to show in the plot:', options3, selection_mode='multi')
## plot wind
if 'wind' in selection3:
    ax32=ax3.twinx()
    l32=ax32.plot(st.session_state.ETP.index, wind_2m, color='orchid', label='Wind speed', ls='--', linewidth=0.7, zorder=2)
    ax32.set_ylabel('wind [m/s]')
    ax32.spines['top'].set_visible(False)
## plot T_a
if 'temperature' in selection3:
    ax33=ax3.twinx()
    ax33.spines.right.set_position(("axes", 1.08))
    l33=ax33.plot(st.session_state.ETP.index, selected_data['T_a'], color='goldenrod', label='Average temperature', ls='--', linewidth=0.7, zorder=2)
    ax33.set_ylabel(r'$T_{a}$ [°C]')
    ax33.spines['top'].set_visible(False)
## plot rs
if 'solar radiation' in selection3:
    ax34=ax3.twinx()
    ax34.spines.right.set_position(("axes", 1.16))
    l34=ax34.plot(st.session_state.ETP.index, rs_MJperm2, color='darkorange', label='Incoming solar radiation', ls='--', linewidth=0.7, zorder=2)
    ax34.set_ylabel(r'solar radiation [MJ/m²]')
    ax34.spines['top'].set_visible(False)
## plot h
if 'relative humidity' in selection3:
    ax35=ax3.twinx()
    ax35.spines.right.set_position(("axes", 1.26))
    l35=ax35.plot(st.session_state.ETP.index, selected_data['rel_h_a'], color='mediumseagreen', label='Average relative hunidity', ls='--', linewidth=0.7, zorder=2)
    ax35.set_ylabel(r'average relative hunidity [%]')
    ax35.spines['top'].set_visible(False)

fig3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=4)
ax3.spines['top'].set_visible(False)

fig3.tight_layout()
st.pyplot(fig3)

# Navigation at the bottom of the side - useful for mobile phone users     
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\03_ETP_Haude.py")
with columnsN1[1]:
    st.subheader(':violet[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\05_Groundwater_Recharge.py")