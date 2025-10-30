import streamlit as st
import os

def _navigate_to(path: str):
    """Change page and scroll to the top on next render."""
    if path != st.session_state.selected_path:
        st.session_state.selected_path = path
        st.session_state.scroll_to_top = True    
        st.session_state.prev_path = path
    st.rerun()
    

# --- Application parameters ---
DEFAULT_START_PAGE = "90_Streamlit_apps/MWW01/content/GROWi26_Start.py"

# --- MUST be first: layout setup wide / centered ---
if "layout_choice" not in st.session_state:
    st.session_state.layout_choice = "centered"

st.set_page_config(page_title="GROWi26 App", page_icon="💦", layout=st.session_state.layout_choice)
st.sidebar.markdown("## 💧 :blue[GROWi26 Navigation]")

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
    "🔶 Einführung": {
        "--- Modellbeispiele 📖---": None,
        "1D GWF 💧": "90_Streamlit_apps/SYMPLE25/pages/00_OM/1D_GWF_Unconfined Recharge.py",
        "Well Capture 🌀": "90_Streamlit_apps/SYMPLE25/pages/00_OM/WellCapture.py",
        "--- Folien 🚀 ---": None,
        "T01: Einführung 📝": "90_Streamlit_apps/MWW01/SlideJet_Presentations/GWBmC_WS2526_V01_SJpresent.py",
    },
    "🔶 Konzeptionelles Modell": {
        "--- Modellbeispiele 📖---": None,
        "1D GWF 💧": "04_Basic_hydrogeology/GWF_1D_unconf_analytic_BC_EX_DE.py",
        "--- Folien 🚀---": None,
        "T02: Konzeptionelles Modell 📝": "90_Streamlit_apps/MWW01/SlideJet_Presentations/GWBmC_WS2526_V02_SJpresent.py",
    },
    "🔶 Grundwasserströmung": {
        "--- Modellbeispiele 📖---": None,
        "1D FD Schema 💧": "06_Groundwater_modeling/GWF_1D_conf_FD.py",
        "--- MODFLOW tutorials 📋 ---": None,
        "MODFLOW Pumping Test": "90_Streamlit_apps/SYMPLE25/pages/M1B/Theis_pumping_Tutorial.py",
        "2D Synthetic Modell": "90_Streamlit_apps/SYMPLE25/pages/M1C/Tutorial_2D_Synth.py",
        "--- Folien 🚀---": None,
        "T03: Numerische GW-Strömungsmod. 📝": "90_Streamlit_apps/MWW01/SlideJet_Presentations/GWBmC_WS2526_T03_Strömungsmodellierung_SJpresent.py",
    },
    "🔶 Transport": {
        "--- Folien 🚀---": None,
    },
    "🔶 Kalibrierung": {
        "--- Folien 🚀---": None,
    },
    "🔶 Anwendungen": {
        "--- Folien 🚀---": None,
    },
    "🔷 General Info": {
        "About": "90_Streamlit_apps/MWW01/content/GROWi26_About.py",
    }
}

# --- State tracking ---
if "active_section" not in st.session_state:
    st.session_state.active_section = None
if "selected_path" not in st.session_state:
    st.session_state.selected_path = DEFAULT_START_PAGE
    
# Space before the first button
st.sidebar.markdown("<div style='margin-top: 2.0rem;'></div>", unsafe_allow_html=True)

# --- Overview and About buttons (at top)
if st.sidebar.button("💦 Overview", key="btn_overview"):
#    st.session_state.selected_path = DEFAULT_START_PAGE
#    st.rerun()   
    _navigate_to(DEFAULT_START_PAGE)

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
