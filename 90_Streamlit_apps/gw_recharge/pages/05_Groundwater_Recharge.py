import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import gw_recharge_functions as func

# Page intro
st.header('Estimating actual evapotranspiration and groundwater recharge using a soil water balance model')
st.subheader(':blue-background[Introduction]', divider="blue")

st.markdown('''          
    We use a simple soil water balance model to obtain estimates of groundwater recharge (Fig 1). A very brief description is given below, more details are provided by the FAO Irrigation and Drainage Paper No. 56 (available at https://www.fao.org/4/x0490e/x0490e00.htm).''')

col1, col2= st.columns(2)
with col1:
    st.image('images\water_balance_crop.png', caption='Fig.1: Water balance of the root zone (modified after FAO Irrigation and Drainage Paper No. 56)')            
with col2:
    st.markdown('''            
        The soil water storage is replenished if precipitation (if appropriate, reduced by runoff) exceeds potential evapotranspiration. 
        If the replenishment results in an exceedence of the field capactiy of the soil, water percolates downward and - if it reaches the water table - becomes groundwater recharge.
        If precipition is less than evapotranspiration, the soil water storage is depleted. The total available water ($TAW$) that can be stored in the root zone is defined by the difference between the water content at the field capacity and at the wilting point (see Fig. 1).''')                         

st.markdown('''
        However, only part of the water stored in the soil is readily available ($RAW$). If the $RAW$ has been removed from the soil, the root water uptake is reduced and thus actual evapotranspiration ($ETA$) is lower than potential evapotranspiration ($ETP$); 
        here we assume the reduction of evapotranspiration can be described by a linear function (Fig. 2).
        For each day, the model adds the difference between precipitation and actual evapotranspiration to the value of the amount of water that is in the root zone at the beginning of the day, yielding the starting value for the calulation of the subsuqent day.
            ''')

st.image('90_Streamlit_apps\gw_recharge\images\water_stress.png', caption='Fig.2: Linear reduction function describing how actual evapotranspiration decreases in proportion to the amount of water remaining in the soil water storage (modified after FAO Irrigation and Drainage Paper No. 56)')

st.subheader(':blue-background[Groundwater Recharge]', divider="blue")
col1, col2, col3 = st.columns(3)
with col1:
    TAW=st.slider('TAW', 0, 200, 100,1)
with col2:
    p = st.slider('p', 0.5, 1., 0.7, 0.01)

data = st.session_state.data
precip = data['precip']

gw_recharge_Haude, ETA_Haude, S_B_A_Haude= func.run_recharge_simulation(TAW, p, st.session_state.ETP.Haude, precip)
gw_recharge_Haude_cum=np.cumsum(gw_recharge_Haude)
st.session_state.ETA.Haude = ETA_Haude
st.session_state.gw_recharge.Haude=gw_recharge_Haude

gw_recharge_Oudin, ETA_Oudin, S_B_A_Oudin= func.run_recharge_simulation(TAW, p, st.session_state.ETP.Oudin, precip)
gw_recharge_Oudin_cum=np.cumsum(gw_recharge_Oudin)
st.session_state.gw_recharge.Oudin=gw_recharge_Oudin
st.session_state.ETA.Oudin = ETA_Oudin

gw_recharge_PM, ETA_PM, S_B_A_PM= func.run_recharge_simulation(TAW, p, st.session_state.ETP.PM, precip)
gw_recharge_PM_cum=np.cumsum(gw_recharge_PM)
st.session_state.gw_recharge.PM=gw_recharge_PM
st.session_state.ETA.PM = ETA_PM


# st.pills to select the ETP
ETP_options=['Oudin', 'Haude', 'Penman-Monteith']
ETP_selection=st.radio('Select with which ETP data you want to continue:', ETP_options, horizontal=True, )
# get data 
if ETP_selection=='Oudin':
    gw_recharge=gw_recharge_Oudin
    ETA=ETA_Oudin
    S_B_A=S_B_A_Oudin
    ETP= st.session_state.ETP.Oudin
elif ETP_selection=='Haude':
    gw_recharge=gw_recharge_Haude
    ETA=ETA_Haude
    S_B_A=S_B_A_Haude
    ETP=st.session_state.ETP.Haude
else:
    gw_recharge=gw_recharge_PM
    ETA=ETA_PM
    S_B_A=S_B_A_PM
    ETP=st.session_state.ETP.PM
data = st.session_state.data
precip = data['precip']

# defining the size and spacing
fig = plt.figure(figsize=(14, 8))

ax1=plt.subplot2grid((6,5),(0,0), colspan=3, rowspan=2)
ax2=plt.subplot2grid((6,5),(2,0), colspan=3, rowspan=2)
ax3=plt.subplot2grid((6,5),(4,0), colspan=3, rowspan=2)
ax_right1=plt.subplot2grid((6,5),(0,3), colspan=2, rowspan=3)
ax_right2=plt.subplot2grid((6,5),(3,3), colspan=2, rowspan=3)

# Now plot the data
## plot the precipitation
ax1.bar(data.index, precip.values, color='skyblue', label='precipitation', width=1)
ax1.set_ylim(max(precip), 0)  # This inverts the y-axis

## plot the ETP
ax2.plot(data.index, ETP, color='goldenrod', label='ETP')

## plot the ETR
ax2.plot(data.index, ETA, color='tomato', label='ETA')

## plot the soil moisture storage
ax3.plot(data.index, S_B_A, color='steelblue', label='soil water storage')
ax4 = ax3.twinx()

## plot the groundwater flux
ax4.bar(data.index, gw_recharge, color='navy', label='groundwater recharge', width=1)
    
## plot cumulative distribution of precipitation and gw_flux
## create cumulativ data
cumulative_precip = np.cumsum(precip.values)
cumulative_gw_recharge = np.cumsum(gw_recharge)
## plotting on the top right 
ax_right1.plot(data.index, cumulative_precip, color='skyblue', label='cumulative precipitation')
ax_right1.plot(data.index, cumulative_gw_recharge, color='navy', label='cumulative groundwater recharge')
## save the annual total (last value of the arrays)
annual_total_precip = cumulative_precip[-1]
annual_total_gw_recharge = cumulative_gw_recharge[-1]

## plot cumulative distribution of ETP and ETR
## creating cumulativ data
cumulative_ETP = np.cumsum(ETP)
cumulative_ETA = np.cumsum(ETA)
## plotting on the bottom right
ax_right2.plot(data.index, cumulative_ETP, color='goldenrod', label='cumulative ETP')
ax_right2.plot(data.index, cumulative_ETA, color='tomato', label='cumulative ETA')
global annual_total_ETA, annual_total_ETP
## save the annual total (last value of the arrays)
annual_total_ETA = cumulative_ETA[-1]
annual_total_ETP = cumulative_ETP[-1]

# add labels and legend
##left
ax1.set_ylabel('precipitation (mm/d)')
ax2.set_ylabel('ETP and ETA (mm/d)')
ax3.set_ylabel('soil water storage (mm)')
ax4.set_ylabel('groundwater recharge (mm/d)')
ax1.legend(loc='best',frameon = False)
ax2.legend(loc='best', frameon = False)
ax3.legend(bbox_to_anchor=(0.15,0.02), loc='lower left', bbox_transform=fig.transFigure, frameon = False)
ax4.legend(bbox_to_anchor=(0.31,0.02), loc='lower left', bbox_transform=fig.transFigure, frameon = False)
##right
ax_right1.set_ylabel('precipitation and gw recharge (mm/d)')
ax_right2.set_ylabel('ETP and ETA (mm/d)') 
ax_right1.legend(loc='upper left', frameon = False)
ax_right2.legend(loc='best', frameon = False) 

annual_gwrc_precip = f'total annual:\n precipitation = {annual_total_precip:.2f}[mm]\n gw recharge = {annual_total_gw_recharge:.2f}[mm]'
annual_ETP_ETA = f'total annual:\n ETA = {annual_total_ETA:.2f}[mm] \n ETP = {annual_total_ETP:.2f}[mm]'
    
fig.text(0.67,0.84,annual_gwrc_precip)
fig.text(0.88,0.13, annual_ETP_ETA)
plt.tight_layout()
st.pyplot(fig)





st.subheader(':blue-background[The impact of different ETP-models on the results for groundwater recharge]', divider="blue")

fig2= plt.figure(figsize=(8,7))
ax21=plt.subplot2grid((6,1),(0,0), colspan=1, rowspan=1)
ax22=plt.subplot2grid((6,1),(1,0), colspan=1, rowspan=1)
ax23=plt.subplot2grid((6,1),(2,0), colspan=1, rowspan=1)
ax24=plt.subplot2grid((6,1),(3,0), colspan=1, rowspan=3)

max_gwr=np.max([gw_recharge_Haude, gw_recharge_Oudin, gw_recharge_PM])

ax21.bar(st.session_state.ETP.index, gw_recharge_Haude, color='forestgreen', label='ETP: Haude')
ax21.set_xticks([])
ax21.set_ylim(0,max_gwr)
ax21.legend(loc='upper left', frameon=False)
ax21.yaxis.tick_right()

ax22.set_ylabel('groundwater recharge [mm/d]')
ax22.bar(st.session_state.ETP.index, gw_recharge_Oudin, color='darkorange', label='ETP: Oudin')
ax22.set_xticks([])
ax22.set_ylim(0,max_gwr)
ax22.legend(loc='upper left', frameon=False)
ax22.yaxis.tick_right()

ax23.bar(st.session_state.ETP.index, gw_recharge_PM, color='mediumpurple', label='ETP: Pennman-Monteith')
ax23.set_xticks([])
ax23.set_ylim(0,max_gwr)
ax23.legend(loc='upper left', frameon=False)
ax23.yaxis.tick_right()

ax24.set_ylabel('cum. groundwater recharge [mm]')
ax24.plot(st.session_state.ETP.index, gw_recharge_Haude_cum, color='forestgreen')
ax24.plot(st.session_state.ETP.index, gw_recharge_Oudin_cum, color='darkorange')
ax24.plot(st.session_state.ETP.index, gw_recharge_PM_cum, color='mediumpurple')
ax24.legend(loc='upper left', frameon=False)
ax24.yaxis.tick_right()
st.pyplot(fig2)

# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\04_ETP_PM.py")
with columnsN1[1]:
    st.subheader(':blue[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\06_Linear_Reservoir.py")