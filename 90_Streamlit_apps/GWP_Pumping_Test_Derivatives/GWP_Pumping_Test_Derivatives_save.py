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
DEFAULT_START_PAGE = "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_Start.py"

# --- MUST be first: layout setup wide / centered ---
if "layout_choice" not in st.session_state:
    st.session_state.layout_choice = "centered"

if "language" not in st.session_state:
    st.session_state.language = "en"
    
st.set_page_config(page_title="Pumping Test Derivatives", page_icon="💦", layout=st.session_state.layout_choice)
st.sidebar.markdown("## 🌳 :blue[Pumping Test Derivatives Module Navigation]")

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
    "📕 Introduction ":         "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/01_Theis_Deriv_Ini.py",
    "🔵 Confined Aquifer":      "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/02_Theis_Deriv.py",
    "🟢 Semi-confined Aquifer": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/03_Hantush_Deriv.py",
    "🟣 Unconfined Aquifer":    "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/04_Neuman_Deriv.py",
    "🟠 Effect of Boundaries":
    "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/05_Boundary_Deriv.py",
    "🟡 Derivatives with measured data":
    "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/06_Applied_Deriv.py",
    "📚 Learning More":         "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_LearningMore.py",
    "📌 Abbreviations":         "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_Abbreviations.py",
    "📖 References":            "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_References.py",
    "ℹ️ About":                 "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_About.py"
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
        st.sidebar.markdown("**Aquifer Types**")
     
    # After rendering "🟢 Unconfined Aquifer", insert a section label
    if "Unconfined" in label:
        st.sidebar.markdown("**Applied Derivatives**")
        
    # After rendering "🟢 Unconfined Aquifer", insert a section label
    if "measured" in label:
        st.sidebar.markdown("**Further Resources**")

    # After rendering "🟢 Unconfined Aquifer", insert a section label
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

# --------------------------------------------------
# Language selector
# --------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("#### 🌍 Language")

FLAG_DIR = "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/assets/images/flags"

flags = {
    "🇬🇧": "en",
    "🇩🇪": "de",
    "🇮🇹": "it",
    "🇪🇸": "es",
    "🇵🇹": "pt",
    "🇫🇷": "fr",
    "🇨🇳": "zh",
}

cols = st.sidebar.columns(len(flags))

for col, (flag, lang) in zip(cols, flags.items()):
    with col:
        if st.button(flag, key=f"lang_{lang}"):
            st.session_state.language = lang
            st.rerun()
        
st.sidebar.caption(
    {
        "en": "Module language: English",
        "de": "Modulsprache: Deutsch",
        "it": "Lingua del modulo: Italiano",
        "es": "Idioma del módulo: Español",
        "pt": "Idioma do módulo: Português",
        "fr": "Langue du module : Français",
        "zh": "模块语言：中文",
    }[st.session_state.language]
)

# --- Layout switcher at bottom of the sidebar ---
st.sidebar.markdown('---')
layout_options = ["centered", "wide"]
selected_layout = st.sidebar.radio("Page layout", layout_options, index=layout_options.index(st.session_state.layout_choice))
if selected_layout != st.session_state.layout_choice:
    st.session_state.layout_choice = selected_layout
    st.rerun()
