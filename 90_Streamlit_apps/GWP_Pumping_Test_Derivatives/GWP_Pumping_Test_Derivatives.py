import streamlit as st
import os


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def ui_text(en, **translations):
    """
    Return the UI text in the selected language.
    Falls back to English if no translation is available.
    """
    language = st.session_state.get("language", "en")
    return translations.get(language, en)


def _navigate_to(path: str):
    """Change page and scroll to the top on next render."""
    if path != st.session_state.selected_path:
        st.session_state.selected_path = path
        st.session_state.scroll_to_top = True
        st.session_state.prev_path = path
    st.rerun()


# --------------------------------------------------
# Application parameters
# --------------------------------------------------

DEFAULT_START_PAGE = "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_Start.py"


# --------------------------------------------------
# Session state initialization
# --------------------------------------------------

if "layout_choice" not in st.session_state:
    st.session_state.layout_choice = "centered"

if "language" not in st.session_state:
    st.session_state.language = "en"

if "selected_path" not in st.session_state:
    st.session_state.selected_path = DEFAULT_START_PAGE

if "prev_path" not in st.session_state:
    st.session_state.prev_path = st.session_state.selected_path

if "scroll_to_top" not in st.session_state:
    st.session_state.scroll_to_top = False


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Pumping Test Derivatives",
    page_icon="💦",
    layout=st.session_state.layout_choice,
)


# --------------------------------------------------
# Sidebar title
# --------------------------------------------------

st.sidebar.markdown(
    "## 🌳 :blue[" +
    ui_text(
        "Pumping Test Derivatives Module Navigation",
        de="Navigation im Modul Pumpversuch-Derivativanalyse",
        it="Navigazione del modulo sulle derivate nelle prove di pompaggio",
        es="Navegación del módulo de derivadas en ensayos de bombeo",
        pt="Navegação do módulo de derivadas em testes de bombeamento",
        fr="Navigation du module sur les dérivées des essais de pompage",
        zh="抽水试验导数分析模块导航",
    ) +
    "]"
)


# --------------------------------------------------
# CSS Styling
# --------------------------------------------------

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


# --------------------------------------------------
# Page definitions
# --------------------------------------------------

pages = [
    {
        "id": "introduction",
        "label": lambda: ui_text(
            "📕 Introduction",
            de="📕 Einführung",
            it="📕 Introduzione",
            es="📕 Introducción",
            pt="📕 Introdução",
            fr="📕 Introduction",
            zh="📕 引言",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/01_Theis_Deriv_Ini.py",
        "before": "topics",
        "after": "aquifer_types",
    },
    {
        "id": "confined_aquifer",
        "label": lambda: ui_text(
            "🔵 Confined Aquifer",
            de="🔵 Gespannter GWL",
            it="🔵 Acquifero confinato",
            es="🔵 Acuífero confinado",
            pt="🔵 Aquífero confinado",
            fr="🔵 Aquifère captif",
            zh="🔵 承压含水层",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/02_Theis_Deriv.py",
    },
    {
        "id": "semi_confined_aquifer",
        "label": lambda: ui_text(
            "🟢 Semi-confined Aquifer",
            de="🟢 Halbgespannter GWL",
            it="🟢 Acquifero semiconfinato",
            es="🟢 Acuífero semiconfinado",
            pt="🟢 Aquífero semiconfinado",
            fr="🟢 Aquifère semi-captif",
            zh="🟢 半承压含水层",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/03_Hantush_Deriv.py",
    },
    {
        "id": "unconfined_aquifer",
        "label": lambda: ui_text(
            "🟣 Unconfined Aquifer",
            de="🟣 Ungespannter GWL",
            it="🟣 Acquifero libero",
            es="🟣 Acuífero libre",
            pt="🟣 Aquífero livre",
            fr="🟣 Aquifère libre",
            zh="🟣 潜水含水层",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/04_Neuman_Deriv.py",
        "after": "applied_derivatives",
    },
    {
        "id": "boundary_effects",
        "label": lambda: ui_text(
            "🟠 Effect of Boundaries",
            de="🟠 Einfluss von Randbedingungen",
            it="🟠 Effetto dei limiti idraulici",
            es="🟠 Efecto de los límites hidráulicos",
            pt="🟠 Efeito dos limites hidráulicos",
            fr="🟠 Effet des limites hydrauliques",
            zh="🟠 边界条件的影响",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/05_Boundary_Deriv.py",
    },
    {
        "id": "measured_data",
        "label": lambda: ui_text(
            "🟡 Derivatives with Measured Data",
            de="🟡 Derivative mit Messdaten",
            it="🟡 Derivate con dati misurati",
            es="🟡 Derivadas con datos medidos",
            pt="🟡 Derivadas com dados medidos",
            fr="🟡 Dérivées avec données mesurées",
            zh="🟡 实测数据的导数分析",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/06_Applied_Deriv.py",
        "after": "further_resources",
    },
    {
        "id": "learning_more",
        "label": lambda: ui_text(
            "📚 Learning More",
            de="📚 Mehr erfahren",
            it="📚 Approfondimenti",
            es="📚 Para saber más",
            pt="📚 Saiba mais",
            fr="📚 Pour en savoir plus",
            zh="📚 进一步学习",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_LearningMore.py",
        "after": "additional_information",
    },
    {
        "id": "abbreviations",
        "label": lambda: ui_text(
            "📌 Abbreviations",
            de="📌 Abkürzungen",
            it="📌 Abbreviazioni",
            es="📌 Abreviaturas",
            pt="📌 Abreviações",
            fr="📌 Abréviations",
            zh="📌 缩略语",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_Abbreviations.py",
    },
    {
        "id": "references",
        "label": lambda: ui_text(
            "📖 References",
            de="📖 Literatur",
            it="📖 Riferimenti bibliografici",
            es="📖 Referencias",
            pt="📖 Referências",
            fr="📖 Références",
            zh="📖 参考文献",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_References.py",
    },
    {
        "id": "about",
        "label": lambda: ui_text(
            "ℹ️ About",
            de="ℹ️ Über dieses Modul",
            it="ℹ️ Informazioni",
            es="ℹ️ Acerca de",
            pt="ℹ️ Sobre",
            fr="ℹ️ À propos",
            zh="ℹ️ 关于",
        ),
        "path": "90_Streamlit_apps/GWP_Pumping_Test_Derivatives/content/GWP_Pumping_Test_Derivatives_About.py",
    },
]


# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------

st.sidebar.markdown("<div style='margin-top: 2.0rem;'></div>", unsafe_allow_html=True)

if st.sidebar.button(
    ui_text(
        "💦 Overview",
        de="💦 Überblick",
        it="💦 Panoramica",
        es="💦 Vista general",
        pt="💦 Visão geral",
        fr="💦 Vue d'ensemble",
        zh="💦 概览",
    ),
    key="btn_overview",
):
    _navigate_to(DEFAULT_START_PAGE)


for page in pages:

    if page.get("before") == "topics":
        st.sidebar.markdown(
            "### :blue[" +
            ui_text(
                "Choose from the topics below",
                de="Wählen Sie aus den folgenden Themen",
                it="Scegli tra gli argomenti seguenti",
                es="Elija entre los siguientes temas",
                pt="Escolha entre os tópicos abaixo",
                fr="Choisissez parmi les sujets ci-dessous",
                zh="从以下主题中选择",
            ) +
            "]"
        )

    label = page["label"]()
    path = page["path"]

    is_selected = st.session_state.selected_path == path
    display_label = f"{label} 👈" if is_selected else label

    if st.sidebar.button(display_label, key=f"btn_{page['id']}"):
        _navigate_to(path)

    if page.get("after") == "aquifer_types":
        st.sidebar.markdown(
            "**" +
            ui_text(
                "Aquifer Types",
                de="Grundwasserleitertypen (GWL)",
                it="Tipi di acquifero",
                es="Tipos de acuíferos",
                pt="Tipos de aquíferos",
                fr="Types d'aquifères",
                zh="含水层类型",
            ) +
            "**"
        )

    if page.get("after") == "applied_derivatives":
        st.sidebar.markdown(
            "**" +
            ui_text(
                "Applied Derivatives",
                de="Angewandte Derivativanalyse",
                it="Derivate applicate",
                es="Derivadas aplicadas",
                pt="Derivadas aplicadas",
                fr="Dérivées appliquées",
                zh="应用导数分析",
            ) +
            "**"
        )

    if page.get("after") == "further_resources":
        st.sidebar.markdown(
            "**" +
            ui_text(
                "Further Resources",
                de="Weitere Ressourcen",
                it="Ulteriori risorse",
                es="Recursos adicionales",
                pt="Recursos adicionais",
                fr="Ressources complémentaires",
                zh="更多资源",
            ) +
            "**"
        )

    if page.get("after") == "additional_information":
        st.sidebar.markdown(
            "**" +
            ui_text(
                "Additional Information",
                de="Zusätzliche Informationen",
                it="Informazioni aggiuntive",
                es="Información adicional",
                pt="Informações adicionais",
                fr="Informations complémentaires",
                zh="附加信息",
            ) +
            "**"
        )


# --------------------------------------------------
# Run selected page
# --------------------------------------------------

if st.session_state.selected_path:
    path = st.session_state.selected_path

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            exec(f.read(), globals())
    else:
        st.error(
            ui_text(
                f"❌ File not found: `{path}`",
                de=f"❌ Datei nicht gefunden: `{path}`",
                it=f"❌ File non trovato: `{path}`",
                es=f"❌ Archivo no encontrado: `{path}`",
                pt=f"❌ Arquivo não encontrado: `{path}`",
                fr=f"❌ Fichier introuvable : `{path}`",
                zh=f"❌ 未找到文件：`{path}`",
            )
        )


# --------------------------------------------------
# Language selector
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.markdown(
    "#### 🌍 " +
    ui_text(
        "Language",
        de="Sprache",
        it="Lingua",
        es="Idioma",
        pt="Idioma",
        fr="Langue",
        zh="语言",
    )
)

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


# --------------------------------------------------
# Layout switcher
# --------------------------------------------------

st.sidebar.markdown("---")

layout_options = ["centered", "wide"]

selected_layout = st.sidebar.radio(
    ui_text(
        "Page layout",
        de="Seitenlayout",
        it="Layout della pagina",
        es="Diseño de página",
        pt="Layout da página",
        fr="Mise en page",
        zh="页面布局",
    ),
    layout_options,
    index=layout_options.index(st.session_state.layout_choice),
)

if selected_layout != st.session_state.layout_choice:
    st.session_state.layout_choice = selected_layout
    st.rerun()