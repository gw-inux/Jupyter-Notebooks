import streamlit as st
import pandas as pd
import numpy as np
import pyet

st.subheader(':blue-background[Welcome to the "Groundwater Recharge App !" 👋]', divider="blue")

st.markdown("""
            This app will allow you to learn more about Evapotranspiration, Groundwater Recharge and the Runoff from a Linear Reservoir.
            For better visualisation different methods are applied to meteorological data from the City of Graz (Austria).
            """
            
)
st.subheader(':blue-background[Where does the data come from ?]', divider="blue")

col1, col2=st.columns(2)
with col1:
    st.markdown("""
            The data used as an example is provided by the **Meterological Station of the Universitiy of Graz**. 
            To see where the University is located you can zoom out from the map on the right (Fig 1).
                
            Those, and similar data sets for other locations in Austria, are also available from the Geosphere Data Hub (https://data.hub.geosphere.at/).
            The exact data used within this app is shown in Table 1.  
            
            The app uses data regarding:
            - temperature 🌡️ 
            - precipitation 🌧️
            - humidity 💧
            - wind speed 🌬️ 
            - and solar radiation 🌤️
        """
        )
df= pd.DataFrame({
    'lat':[47.08],
    'long':[15.448056]
})

with col2:
    st.map(df, latitude= 'lat', longitude='long', color='#4292C6', height=350)
    st.write(':gray[*Figure 1: Map showing the location of the Meterological Station of the Universitiy of Graz.*]')

data = pd.read_csv('90_Streamlit_apps/gw_recharge/data/UniGraz1990-2020.csv', index_col=0, parse_dates=True)
st.write(''':gray[*Table 1: Head of the provided DataFrame, where: T_14...Temperature at 14:00 [°C],
    T_a...average Tamperature [°C],
    rel_h_14...relative humidity messured at 14:00 [%],
    rel_h_a...average relative humidity [%],
    wind_speed...average wind speed [$m/s$],
    rs...solar radiation [$J/cm²$], 
    precip...Sum of precipitation over 24 hours [$mm$]*]''')
st.write(data.head())


# User input for observation period
## look for the oldest and newest data within the given dataframe
min_date = data.index.min()
max_date = data.index.max()

st.subheader(':blue-background[Select your measurement period:]', divider="blue")
st.write('''To define the time period, you would like to observe, use the date input widget below. 
         We recommend to choose a duration of approximately one year, however shorter or longer time periods can be observed as well. 
         Just keep in mind that more data might need more time processing.''')

col1, col2 = st.columns(2)
selected_timespan = st.date_input('👇 here you can select a time periode 👇',value=('2020-01-01','2020-12-31'), min_value=min_date, max_value=max_date, format='YYYY-MM-DD')
selected_data = data.loc[selected_timespan[0]:selected_timespan[1]]
st.session_state.data=data.loc[selected_timespan[0]:selected_timespan[1]]
st.session_state.ETP = pd.DataFrame(index=st.session_state.data.index)
st.session_state.ETA = pd.DataFrame(index=st.session_state.data.index)
st.session_state.gw_recharge = pd.DataFrame(index=st.session_state.data.index)

# calculating data that needs to be available from multiple pages and saving data in session state
lat_graz = 47.076668*np.pi/180  # in rad
ETP_oudin=pyet.oudin(selected_data['T_a'], lat_graz)
st.session_state.ETP.Oudin = ETP_oudin

ETP_haude=pyet.haude(selected_data['T_14'], selected_data['rel_h_14'])
ETP_Haude=ETP_haude.clip(0,7)
st.session_state.ETP.Haude = ETP_Haude

rs_MJperm2=selected_data['rs']/100 #for the calculation the solar radiation is needed in MJ/m2
wind_2m=selected_data['wind_speed']*4.87/(np.log((67.8*20)-5.42)) #as the wind mesurements at uni-graz are taken higher the wind messurements need to be adjustet (~ 20 m above ground surface)
ETP_pm=pyet.pm_fao56(tmean=selected_data['T_a'], wind=wind_2m, rs=rs_MJperm2, lat=lat_graz, rh=selected_data['rel_h_a'], elevation=366 )
st.session_state.ETP.PM = ETP_pm


# Navigation at the bottom of the side - useful for mobile phone users     
columnsN1 = st.columns((1,1,1), gap = 'large')

with columnsN1[1]:
    st.subheader(':blue[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("'90_Streamlit_apps\\gw_recharge\\pages\\02_ETP_Oudin.py")
