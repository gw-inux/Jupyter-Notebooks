import streamlit as st
import os

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
        font-size: 1rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        margin-top: -1rem;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(44, 123, 229, 0.1) !important;
        color: inherit !important;
        border-radius: 5px !important;
    }
    .subheader-label {
        font-style: italic;
        color: black;
        font-size: 1rem;
        text-decoration: underline;
        margin-left: 2.5rem;
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
    "🔶 General information": {
        "Overview 📖": "90_Streamlit_apps/GWP_Boundary_Conditions/content/GWP_BC_1D_unconf_analytic_noflow.py",
    },
    "🔶 Boundary Conditions": {
        "GHB": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_GHB.py",
        "RIV": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_RIV.py",
        "DRN": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_DRN.py",
        "ET": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_ET.py",
        "MNW": "90_Streamlit_apps/GWP_Boundary_Conditions/content/Q_h_plot_MNW.py",
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
                display_label = f"🟢 **{label}**" if is_selected else label
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
