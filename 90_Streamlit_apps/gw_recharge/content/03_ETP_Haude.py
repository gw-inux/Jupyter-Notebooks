import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

# Page intro
st.header('Potential Evapotranspiration (ETP)')

# ETP Haude - theory
st.subheader(':green-background[Introduction]', divider="green")
st.markdown('''Already in 1954 Haude published a method to estimate potential evapotranspiration. 
            This model only requires air temperature and humidity, both measured at 14:00, as input data.
            Further there is a parameter considering monthly variations of crop. 
            The method is better used for longer time periods as the results on a short period (days) are too inaccurate. 
            Results for the potential evapotranspiration higher than 7 get cut as those are energetically not possible.''')

st.subheader(':green-background[The Haude Formula]', divider="green")
st.markdown(f"<p style='font-size:25px;'>{'Formula'}</p>", unsafe_allow_html=True)
st.latex(r'ETP = k  E  ( 1 - \frac{F_{14}}{100}) \leq 7')
st.markdown('''
        - $k$...monthly changing crop coefficient $[mm/d*hPa]$ \n
        - $E$... saturation vapour pressure $[hPa]$ \n
        - $F_{14}$...relative humidity at 14:00 $[\%]$ \n\n
            ''')
st.markdown(f"<p style='font-size:25px;'>{'Haude Factor'}</p>", unsafe_allow_html=True)
st.latex(r'E = 6.108*10^{\frac{7.5 T_{14}}{237.3+T_{14}}}')
st.markdown('- T...Temperature at 14:00 $[C°]$ \n')

st.subheader(':green-background[Results]', divider="green")
# ETP Oudin - plot
selected_data = st.session_state.data
fig2, ax2= plt.subplots(figsize=(12,5))
fig2.suptitle('ETP (Haude) for Graz', fontsize=16)

with st.expander('click here to take a look at the data, edit or save as csv'):
    st.session_state.ETP.Haude = st.data_editor(st.session_state.ETP.Haude)

#ax.plot(selected_data.index,PET_oudin)
ax2.set_title(f'from {min(st.session_state.ETP.index):%d-%m-%Y} to {max(st.session_state.ETP.index):%d-%m-%Y}')

# st.pills so the user can deside which additional data gets shown
options2= ['relative humidity', 'temperature']
selection2= st.pills('select data to show in the plot:', options2, selection_mode='multi')

## plot ETP
l21=ax2.plot(st.session_state.ETP.index, st.session_state.ETP.Haude, color='darkgreen', label='Evapotranspiration, Haude', zorder=10)
ax2.set_ylabel('$ETP_{Haude}$ [mm/d]')

## plot rel_h_14
if 'relative humidity' in selection2:
    ax22=ax2.twinx()
    l22=ax22.plot(st.session_state.ETP.index, selected_data['rel_h_14'], color='mediumseagreen', label='relative humidity at 14:00', linewidth=0.7, ls='--', zorder=2)
    ax22.set_ylabel(r'$h_{14}$ [%]')
    ax22.spines['top'].set_visible(False)
## plot T_14
if 'temperature' in selection2:
    ax23=ax2.twinx()
    ax23.spines.right.set_position(("axes", 1.08))
    l23=ax23.plot(st.session_state.ETP.index, selected_data['T_14'], color='yellowgreen', label='temperature at 14:00', linewidth=0.7, ls='--', zorder=2)
    ax23.set_ylabel(r'$T_{14}$ [°C]')
    ax23.spines['top'].set_visible(False)

fig2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=4)
ax2.spines['top'].set_visible(False)

fig2.tight_layout()
st.pyplot(fig2)

# Navigation at the bottom of the side - useful for mobile phone users     
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\02_ETP_Oudin.py")
with columnsN1[1]:
    st.subheader(':green[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\04_ETP_PM.py")