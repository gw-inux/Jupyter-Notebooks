import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import gw_recharge_functions as func

# Page intro
st.header('Potential Evapotranspiration (ETP)')

# ETP Oudin - theory
st.subheader(':orange-background[Introduction]', divider="orange")
st.markdown('In 2005 Oudin et al. published a simple model estimating the potential evapotranspiration. This model does only rely on extraterrestrial radiation and mean daily air temperature. Due to the little data requirement, the method can easily be performed and data availability should not become a big problem. However, there might be a loss in accuracy due to the simplifications.')
st.subheader(':orange-background[The Oudin Formula]', divider="orange")
st.markdown(f"<p style='font-size:25px;'>{'Formula'}</p>", unsafe_allow_html=True)
st.latex(r'ETP = E_r  \frac{T_a+5}{100} [\frac{mm}{d}]')
st.markdown('''
        - ETP...Evapotranspiration [$mm/d$] \n
        - $E_r$...Evaporation due to extraterrestrial radiation [$mm/d$] \n
        - $T_a$...Average Temperature [°C] \n\n
        ''')
st.markdown(f"<p style='font-size:25px;'>{'Evaporation due to extraterrestrial radiation'}</p>", unsafe_allow_html=True)

st.latex(r'E_r = \frac{R_e}{\lambda  \rho} [\frac{mm}{d}]')
st.write('''
         - $E_r$...Evaporation due to the extraterrestrial radiation [$mm/d$] \n
         - $R_e$...Extraterrestrial radiation [$MJ/(mm^2*d)$] \n
         - $\lambda$...Evaporation heat of water (= 2,45 [$MJ/k$]) \n
         - $\rho$...Density of water ( = 1 [$kg/l$]) \n
         ''')

st.subheader(':orange-background[Results]', divider="orange")
selected_data = st.session_state.data
# ETP Oudin - plot
fig1, ax1= plt.subplots(figsize=(12,5))
fig1.suptitle('ETP (Oudin) for Graz', fontsize=16)
E_r, R_e= func.evaporation_from_radiation(lat=47.076668,doy=selected_data.index.dayofyear)

## save the data in session state to access from all pages
#if 'oudin' not in st.session_state:

with st.expander('click here to take a look at the data, edit or save as csv'):
    st.session_state.ETP.Oudin= st.data_editor(st.session_state.ETP.Oudin)

# st.pills so the user can deside which additional data gets shown
options1=['extraterrestrial radiation', 'temperature']
selection1 = st.pills('Select additional input data to plot:', options1, selection_mode='multi')
#ax.plot(selected_data.index,PET_oudin)
ax1.set_title(f'from {min(st.session_state.ETP.Oudin.index):%d-%m-%Y} to {max(st.session_state.ETP.index):%d-%m-%Y}')
## plot ETP
l11=ax1.plot(st.session_state.ETP.index, st.session_state.ETP.Oudin, color='darkorange', label='Evapotranspration, Oudin et al. (2005)', zorder=10)
ax1.set_ylabel(r'$ETP_{Oudin}$ [mm/d]')
## plot E_r
if 'extraterrestrial radiation' in selection1:
    ax12=ax1.twinx()
    l12=ax12.plot(st.session_state.ETP.index, E_r, color='gold', label=r'Extraterrestrial radiation ($E_{r}$)', linewidth=0.7, ls='--', zorder=2)
    ax12.set_ylabel(r'$E_{r}$ [mm/d]')
    ax12.spines['top'].set_visible(False)
## plot T_avg
if 'temperature' in selection1:
    ax13=ax1.twinx()
    ax13.spines.right.set_position(("axes", 1.08))
    l13=ax13.plot(st.session_state.ETP.index, selected_data['T_a'], color='goldenrod', label=r'Average temperature $T_{a}$', linewidth=0.7, ls='--', zorder=2)
    ax13.set_ylabel(r'$T_a$ [°C]')
    ax13.spines['top'].set_visible(False)

fig1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=4)
ax1.spines['top'].set_visible(False)

fig1.tight_layout()
st.pyplot(fig1)


# Navigation at the bottom of the side - useful for mobile phone users     
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\01_Intro.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\03_ETP_Haude.py")