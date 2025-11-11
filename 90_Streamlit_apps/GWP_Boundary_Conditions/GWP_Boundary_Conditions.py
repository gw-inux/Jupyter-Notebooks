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
DEFAULT_START_PAGE = "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_Boundary_Conditions_Start.py"

# --- MUST be first: layout setup wide / centered ---
if "layout_choice" not in st.session_state:
    st.session_state.layout_choice = "centered"

st.set_page_config(page_title="Boundary Conditions Module", page_icon="💦", layout=st.session_state.layout_choice)
st.sidebar.markdown("## 🌳 :green[Boundary Condition Module Navigation]")

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
    "📕 Introduction ": "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_BC_QHGeneral.py",
    "🟠 GHB": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_GHB.py",
    "🟣 RIV": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_RIV.py",
    "🟢 DRN": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_DRN.py",
    "🟡 MNW": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_MNW.py",
    "🔵 EVT": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_EVT.py",
    "📚 Learning More": "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_BC_LearningMore.py",
    "📌 Abbreviations": "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_BC_Abbreviations.py",
    "📖 References": "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_BC_References.py",
    "ℹ️ About": "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_About.py"
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
#    st.session_state.selected_path = DEFAULT_START_PAGE
#    st.rerun()   
    _navigate_to(DEFAULT_START_PAGE)

# --- Sidebar navigation ---
for label, path in pages.items():
    if "Introduction" in label:
        st.sidebar.markdown("### :blue[Choose from the topics below]")
    is_selected = st.session_state.selected_path == path
    clean_label = label.strip()
    display_label = f"{clean_label} 👈" if is_selected else clean_label
    if st.sidebar.button(display_label, key=f"btn_{label}"):
#        st.session_state.selected_path = path
#        st.rerun()
        _navigate_to(path)
        
    # After rendering "Introduction 📖", insert a section label
    if "Introduction" in label:
        st.sidebar.markdown("**MODFLOW Boundary Conditions**")
        
    # After rendering "🔵 EVT", insert a section label
    if "EVT" in label:
        st.sidebar.markdown("**Further Resources**")

    # After rendering "🔵 EVT", insert a section label
    if "📚 Learning More" in label:
        st.sidebar.markdown("**Additional Information**")
        
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
