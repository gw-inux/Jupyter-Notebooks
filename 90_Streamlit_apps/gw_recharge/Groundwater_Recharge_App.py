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
DEFAULT_START_PAGE = "90_Streamlit_apps/gw_recharge/content/00_Overview.py"

# --- MUST be first: layout setup wide / centered ---
if "layout_choice" not in st.session_state:
    st.session_state.layout_choice = "centered"
    
st.set_page_config(page_title = "iNUX - Groundwater Recharge", page_icon="90_Streamlit_apps\gw_recharge\images\iNUX_wLogo.png", layout=st.session_state.layout_choice)
st.sidebar.markdown("## 🌱 :blue[Groundwater Recharge Module Navigation]")

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

# --- Flat page definitions ---
pages = {
    "👋 Intro": {
        "The Groundwater Recharge App": "90_Streamlit_apps/gw_recharge/content/01_Intro.py",
    },
    "🌱 Evapotranspiration": {
        "The Oudin-Method": "90_Streamlit_apps/gw_recharge/content/02_ETP_Oudin.py",
        "The Haude-Method": "90_Streamlit_apps/gw_recharge/content/03_ETP_Haude.py",
        "The Penman-Monteith-Method": "90_Streamlit_apps/gw_recharge/content/04_ETP_PM.py",
    },
    "🌧️ Groundwater Recharge and Runoff": {
        "Soil Water Balance": "90_Streamlit_apps/gw_recharge/content/05_Groundwater_Recharge.py",
        "Linear Reservoir": "90_Streamlit_apps/gw_recharge/content/06_Linear_Reservoir.py",
    },
    "📖 About": {
    "The iNUX Project": "90_Streamlit_apps/gw_recharge/content/07_About.py",
    "References": "90_Streamlit_apps/gw_recharge/content/08_References.py",
    }
}

# --- State tracking ---
if "selected_path" not in st.session_state:
    st.session_state.selected_path = DEFAULT_START_PAGE
if "prev_path" not in st.session_state:
    st.session_state.prev_path = st.session_state.selected_path
if "scroll_to_top" not in st.session_state:
    st.session_state.scroll_to_top = False

# Space before the first button
st.sidebar.markdown("<div style='margin-top: 2.0rem;'></div>", unsafe_allow_html=True)

# --- Overview and About buttons (at top)
if st.sidebar.button("💦 Overview", key="btn_overview"): 
    _navigate_to(DEFAULT_START_PAGE)

# --- Sidebar navigation ---
for section, items in pages.items():
    st.sidebar.markdown(f"### {section}")

    for page_label, page_path in items.items():
        is_selected = (st.session_state.selected_path == page_path)
        display_label = f"{page_label} 👈" if is_selected else page_label

        # Use a safe, stable key (avoid emojis/spaces in keys if you like)
        key = f"btn__{section}__{page_label}"

        if st.sidebar.button(display_label, key=key):
            _navigate_to(page_path)

    st.sidebar.markdown("---")
        
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
