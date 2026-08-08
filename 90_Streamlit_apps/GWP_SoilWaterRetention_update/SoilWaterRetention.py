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

DEFAULT_START_PAGE = "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SoilWaterRetention_Start.py"


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
    page_title="Soil Water Retention",
    page_icon="💦",
    layout=st.session_state.layout_choice,
)


# --------------------------------------------------
# Sidebar title
# --------------------------------------------------

st.sidebar.markdown(
    "## 🌱 :blue[" +
    ui_text(
        "Soil Water Retention Module Navigation",
        de="Navigation im Soil Water Retention Modul",
        it="Navigazione del modulo Soil Water Retention",
        es="Navegación del módulo Soil Water Retention",
        pt="Navegação do módulo Soil Water Retention",
        fr="Navigation du module Soil Water Retention",
        zh="土壤水分保持模块导航",
        ar="التنقل في وحدة احتفاظ التربة بالماء",
        hi="मृदा जल धारण मॉड्यूल नेविगेशन",
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
        "id": "theory",
        "label": lambda: ui_text(
            "📝 Theory",
            de="📝 Theorie",
            it="📝 Teoria",
            es="📝 Teoría",
            pt="📝 Teoria",
            fr="📝 Théorie",
            zh="📝 理论",
            ar="📝 النظرية",
            hi="📝 सिद्धांत",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_Theory.py",
        "before": "topics",
    },
    {
        "id": "swrc_interactive",
        "label": lambda: ui_text(
            "📈 The SWRC interactive",
            de="📈 Die SWRC interaktiv",
            it="📈 La SWRC interattiva",
            es="📈 La SWRC interactiva",
            pt="📈 A SWRC interativa",
            fr="📈 La SWRC interactive",
            zh="📈 交互式 SWRC",
            ar="📈 منحنى SWRC التفاعلي",
            hi="📈 इंटरैक्टिव SWRC",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_SWRC_interactive.py",
    },
    {
        "id": "swrc_comparison",
        "label": lambda: ui_text(
            "📊 The SWRC in comparison",
            de="📊 Die SWRC im Vergleich",
            it="📊 La SWRC a confronto",
            es="📊 La SWRC en comparación",
            pt="📊 A SWRC em comparação",
            fr="📊 La SWRC en comparaison",
            zh="📊 SWRC 对比",
            ar="📊 مقارنة SWRC",
            hi="📊 SWRC की तुलना",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_SWRC in comparison.py",
        "after": "exercises",
    },
    {
        "id": "exercise_1",
        "label": lambda: ui_text(
            "🧪 SWRC Exercise 1",
            de="🧪 SWRC-Übung 1",
            it="🧪 Esercizio SWRC 1",
            es="🧪 Ejercicio SWRC 1",
            pt="🧪 Exercício SWRC 1",
            fr="🧪 Exercice SWRC 1",
            zh="🧪 SWRC 练习 1",
            ar="🧪 تمرين SWRC 1",
            hi="🧪 SWRC अभ्यास 1",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_Exercise_1.py",
    },
    {
        "id": "exercise_2",
        "label": lambda: ui_text(
            "🧪 SWRC Exercise 2",
            de="🧪 SWRC-Übung 2",
            it="🧪 Esercizio SWRC 2",
            es="🧪 Ejercicio SWRC 2",
            pt="🧪 Exercício SWRC 2",
            fr="🧪 Exercice SWRC 2",
            zh="🧪 SWRC 练习 2",
            ar="🧪 تمرين SWRC 2",
            hi="🧪 SWRC अभ्यास 2",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_Exercise_2.py",
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
            ar="📌 الاختصارات",
            hi="📌 संक्षिप्ताक्षर",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_Abbreviations.py",
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
            ar="📖 المراجع",
            hi="📖 संदर्भ",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_References.py",
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
            ar="ℹ️ حول الوحدة",
            hi="ℹ️ परिचय",
        ),
        "path": "90_Streamlit_apps/GWP_SoilWaterRetention_update/content/GWP_SWR_About.py",
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
        ar="💦 نظرة عامة",
        hi="💦 अवलोकन",
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
                ar="اختر من الموضوعات أدناه",
                hi="नीचे दिए गए विषयों में से चुनें",
            ) +
            "]"
        )

    label = page["label"]()
    path = page["path"]

    is_selected = st.session_state.selected_path == path
    display_label = f"{label} 👈" if is_selected else label

    if st.sidebar.button(display_label, key=f"btn_{page['id']}"):
        _navigate_to(path)

    if page.get("after") == "exercises":
        st.sidebar.markdown(
            "**" +
            ui_text(
                "Exercises",
                de="Übungen",
                it="Esercizi",
                es="Ejercicios",
                pt="Exercícios",
                fr="Exercices",
                zh="练习",
                ar="التمارين",
                hi="अभ्यास",
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
                ar="معلومات إضافية",
                hi="अतिरिक्त जानकारी",
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
                ar=f"❌ لم يتم العثور على الملف: `{path}`",
                hi=f"❌ फ़ाइल नहीं मिली: `{path}`",
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
        ar="اللغة",
        hi="भाषा",
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
    "🇸🇦": "ar",
    "🇮🇳": "hi",
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
        "ar": "لغة الوحدة: العربية",
        "hi": "मॉड्यूल की भाषा: हिन्दी",
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
        ar="تخطيط الصفحة",
        hi="पृष्ठ विन्यास",
    ),
    layout_options,
    index=layout_options.index(st.session_state.layout_choice),
)

if selected_layout != st.session_state.layout_choice:
    st.session_state.layout_choice = selected_layout
    st.rerun()