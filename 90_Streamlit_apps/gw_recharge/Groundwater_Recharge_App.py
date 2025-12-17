import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(page_title = "iNUX - Groundwater Recharge", page_icon="90_Streamlit_apps\gw_recharge\images\iNUX_wLogo.png")

pages={
    '👋 Intro':[
        st.Page('90_Streamlit_apps/gw_recharge/pages/01_Intro.py',title='The Groundwater Recharge App')],
    '🌱 Evapotranspiration':[
        st.Page('90_Streamlit_apps/gw_recharge/pages/02_ETP_Oudin.py',title='The Oudin-Method'),
        st.Page('90_Streamlit_apps/gw_recharge/pages/03_ETP_Haude.py', title='The Haude-Method'),
        st.Page('90_Streamlit_apps/gw_recharge/pages/04_ETP_PM.py', title='The Penman-Monteith-Method')],
    '🌧️ Groundwater Recharge':[st.Page('pages/05_Groundwater_Recharge.py', title='Groundwater Recharge')],
    '🪣 Linear Reservoir': [st.Page('pages/06_Linear_Reservoir.py', title='Linear Reservoir')],
    '📖 About': [
        st.Page('90_Streamlit_apps/gw_recharge/pages/07_About.py', title='The iNUX Project'),
        st.Page('90_Streamlit_apps/gw_recharge/pages/08_References.py', title='References')]
}
pg = st.navigation(pages)
add_page_title(pg)
pg.run()