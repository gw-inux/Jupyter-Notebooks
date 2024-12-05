import streamlit as st


st.set_page_config(
    page_title="SYMPLE25",
    page_icon="💦",
)

st.sidebar.success("☝️ Select a page above. ☝️")

symple25app = st.Page("pages/SYMPLE25APP.py", title="📃 SYMPLE25 App")
gfw_1D_unconf_rech_OM = st.Page("pages/GWF/1D_GWF_Unconfined Recharge.py", title="📈 ▶️ 1D GWF unconfined with recharge")
well_capture_OM = st.Page("pages/GWF/WellCapture.py", title="📈 ▶️ Well Capture")
about = st.Page("pages/About.py", title="👉 About")

pg = st.navigation(
    {
        "Overview": [symple25app],
        "Orientation meeting": [gfw_1D_unconf_rech_OM, well_capture_OM],
        "About": [about],
    }
)

pg.run()
