import streamlit as st
import os

# --- Application parameters ---
DEFAULT_START_PAGE = "90_Streamlit_apps/SYMPLE25/pages/ORG/SYMPLE25APP.py"

# --- MUST be first: layout setup wide / centered ---
if "layout_choice" not in st.session_state:
    st.session_state.layout_choice = "centered"

st.set_page_config(page_title="SYMPLE25 App", page_icon="💦", layout=st.session_state.layout_choice)
st.sidebar.markdown("## 🌳 :green[SYMPLE25 Navigation]")

# --- CSS Styling ---
st.markdown("""
    <style>
    section[data-testid="stSidebar"] button {
        background: none !important;
        border: none !important;
        padding: 0.3rem 0.6rem !important;
        text-align: left !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        margin-top: -1rem;
    }
    section[data-testid="stSidebar"] button:focus,
    section[data-testid="stSidebar"] button:active,
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(44, 123, 229, 0.1) !important;
        border-radius: 5px !important;
    }
    .subheader-label {
        font-style: italic;
        color: black;
        font-size: 1rem;
        text-decoration: underline;
        margin-left: 1.5rem;
        margin-top: -0.5rem;
        margin-bottom: 0.5rem;
    }
    section[data-testid="stSidebar"] .block-container .stButton {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    section[data-testid="stSidebar"] button {
        line-height: 1.1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Pages definition / The content of your application / Header are with the target 'None' ---
pages = {
    "🔶 Orientation meeting": {
        "--- Initial Model examples 📖---": None,
        "1D GWF 💧": "90_Streamlit_apps/SYMPLE25/pages/00_OM/1D_GWF_Unconfined Recharge.py",
        "Well Capture 🌀": "90_Streamlit_apps/SYMPLE25/pages/00_OM/WellCapture.py",
        "--- Presentations 📖 ---": None,
        "Presentation: 📝 M0": "90_Streamlit_apps/SYMPLE25/presentations/SlideJet_present_M0.py",
    },
    "🔶 M1A - Basics": {
        "--- 📖_Parameters ---": None,
        "_K_ and _S_: Flow to Well": "90_Streamlit_apps/SYMPLE25/pages/M1A/Flow2Well_transient_unconfined_confined_basics.py",
        "--- 📖_Motion laws ---": None,
        "Heat Transport": "90_Streamlit_apps/SYMPLE25/pages/M1A/Heat_transport_flow_1D_basics.py",
        "1D Transport": "90_Streamlit_apps/SYMPLE25/pages/M1A/Transport_1D_AD_basics.py",
        "1D Flow": "90_Streamlit_apps/SYMPLE25/pages/M1A/GWF_1D_unconf_analytic_noflow_calib_basics.py",
        "--- 📊_Budgets and Balances ---": None,
        "Radioactive Decay": "90_Streamlit_apps/SYMPLE25/pages/M1A/Radioactive_Decay_basics.py",
        "--- 📖_Presentations ---": None,
        "Presentation: 📝 M1A_1": "90_Streamlit_apps/SYMPLE25/pages/M1A/M1A_1_presentation.py",
    },
    "🔶 M1B - Data processing": {
        "--- 🔨_Hydrogeologic testing ---": None,
        "Slug test evaluation": "05_Applied_hydrogeology/Slugtest_translate.py",
        "--- 📋_MODFLOW tutorials ---": None,
        "MODFLOW Pumping Test": "90_Streamlit_apps/SYMPLE25/pages/M1B/Theis_pumping_Tutorial.py",
    },
    "🔶 M1C - Flow modeling": {
        "--- 🧮_General Numerics ---": None,
        "1D Confined FD": "90_Streamlit_apps/SYMPLE25/pages/M1C/GWF_1D_conf_FD.py",
        "Modflow Time Step Multiplier": "06_Groundwater_modeling/Timestep_Multiplier.py",
        "--- 💻_MODFLOW boundary conditions ---": None,
        "RIV boundary": "06_Groundwater_modeling/Q_h_plot_RIV.py",
        "EVT boundary": "06_Groundwater_modeling/Q_h_plot_ET.py",
        "GHB boundary": "06_Groundwater_modeling/Q_h_plot_GHB.py",
        "--- 📈_Calibration ---": None,
        "1D Unconf Calib": "90_Streamlit_apps/SYMPLE25/pages/Calibration/GWF_1D_unconf_analytic_calib.py",
        "1D NoFlow Calib": "90_Streamlit_apps/SYMPLE25/pages/Calibration/GWF_1D_unconf_analytic_noflow_calib.py",
        "--- 📖_Presentations ---": None,
        "Presentation: 📝 M1C_3": "90_Streamlit_apps/SYMPLE25/pages/M1C/M1C_3_presentation.py",
    },
    "🔶 M1D - Transport modeling": {
        "--- 📝_Analytical solutions ---": None,
        "1D Transport with Advection/Dispersion": "05_Applied_hydrogeology/Transport_1D_AD_ST.py",
        "2D Transport - Adv./Disp. - Dirac source": "05_Applied_hydrogeology/Transport_2D_Dirac_pulse.py",
        "2D Transport - Adv./Disp. - Continuous source": "05_Applied_hydrogeology/Transport_2D_Continous.py",
        "--- 📋_MODFLOW/MT3D tutorials ---": None,
        "2D Solute transport tutorial": "06_Groundwater_modeling/Tutorial_2D_Transport.py",
        "--- 📖_Presentations ---": None,
        "Presentation: 📝 M1D_1": "90_Streamlit_apps/SYMPLE25/presentations/SlideJet_present_M1D_1.py",
    },
    "🔶 M1E - Model design": {
        "--- 📋_MODFLOW tutorials ---": None,
        "2D Synthetic": "90_Streamlit_apps/SYMPLE25/pages/M1C/Tutorial_2D_Synth.py",
    },
    "🔷 General Info": {
        "About": "90_Streamlit_apps/SYMPLE25/pages/ORG/About.py",
        "About SYMPLE": "90_Streamlit_apps/SYMPLE25/pages/ORG/About_SYMPLE.py",
    }
}

# --- State tracking ---
if "active_section" not in st.session_state:
    st.session_state.active_section = None
if "selected_path" not in st.session_state:
    st.session_state.selected_path = DEFAULT_START_PAGE

# --- Overview page ---
if st.sidebar.button("💦 Overview", key="btn_overview"):
    st.session_state.active_section = None
    st.session_state.selected_path = DEFAULT_START_PAGE
    st.rerun()

# --- Section menu + subpage logic ---
for section, subpages in pages.items():
    if st.sidebar.button(section, key=f"btn_{section}"):
        st.session_state.active_section = section
        # Auto-select first real subpage
        for label, path in subpages.items():
            if path is not None:
                st.session_state.selected_path = path
                break
        st.rerun()

    if st.session_state.active_section == section:
        for label, path in subpages.items():
            if path is None:
                st.sidebar.markdown(f"<div class='subheader-label'>{label.replace('---', '').strip()}</div>", unsafe_allow_html=True)
            else:
                is_selected = st.session_state.selected_path == path
                display_label = f"👉 {label}" if is_selected else label
                indent, content = st.sidebar.columns([0.1, 0.9])
                with content:
                    if st.button(display_label, key=f"{section}_{label}"):
                        st.session_state.selected_path = path
                        st.rerun()

# --- Run selected page ---
if st.session_state.selected_path:
    path = st.session_state.selected_path
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            exec(f.read(), globals())
    else:
        st.error(f"❌ File not found: `{path}`")

# --- Layout switcher at bottom of the sidebar ---
st.sidebar.markdown('---')
layout_options = ["centered", "wide"]
selected_layout = st.sidebar.radio("Page layout", layout_options, index=layout_options.index(st.session_state.layout_choice))
if selected_layout != st.session_state.layout_choice:
    st.session_state.layout_choice = selected_layout
    st.rerun()
