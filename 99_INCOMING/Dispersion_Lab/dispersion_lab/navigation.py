"""Sidebar and multilingual shell following the Soil Water Retention update.

CODE MAP — refresh with python scripts/update_code_index.py
  L0015  page_definitions
  L0025  language_selector
  L0048  run_module
END CODE MAP
"""
import streamlit as st
from .i18n import LANGUAGES, ui_text
from .pages import overview, principles, references
from .ui import render_page, render_pinboard, tr


def page_definitions():
    return [
        ("overview",overview,ui_text("💧 Overview",de="💧 Überblick",it="💧 Panoramica",es="💧 Vista general",pt="💧 Visão geral",fr="💧 Vue d’ensemble",zh="💧 概览",ar="💧 نظرة عامة",hi="💧 अवलोकन")),
        ("principles",principles,ui_text("📝 Principles and guided experiment",de="📝 Grundlagen und geführtes Experiment",it="📝 Principi ed esperimento guidato",es="📝 Principios y experimento guiado",pt="📝 Princípios e experiência guiada",fr="📝 Principes et expérience guidée",zh="📝 原理与引导实验",ar="📝 المبادئ والتجربة الموجهة",hi="📝 सिद्धांत और निर्देशित प्रयोग")),
        ("pinboard",render_pinboard,ui_text("🔹 Pinboard experiment",de="🔹 Galtonbrett-Experiment",it="🔹 Esperimento di Galton",es="🔹 Experimento de Galton",pt="🔹 Experiência de Galton",fr="🔹 Expérience de Galton",zh="🔹 钉板实验",ar="🔹 تجربة لوحة غالتون",hi="🔹 पिनबोर्ड प्रयोग")),
        ("explore",render_page,ui_text("🧪 Grain network",de="🧪 Kornnetzwerk",it="🧪 Esplora e modifica",es="🧪 Explorar y modificar",pt="🧪 Explorar e modificar",fr="🧪 Explorer et modifier",zh="🧪 探索与修改",ar="🧪 الاستكشاف والتعديل",hi="🧪 अन्वेषण और संशोधन")),
        ("references",references,ui_text("📖 References and model notes",de="📖 Quellen und Modellhinweise",it="📖 Riferimenti e note sul modello",es="📖 Referencias y notas del modelo",pt="📖 Referências e notas do modelo",fr="📖 Références et notes du modèle",zh="📖 参考文献与模型说明",ar="📖 المراجع وملاحظات النموذج",hi="📖 संदर्भ और मॉडल टिप्पणियाँ")),
    ]


def language_selector():
    st.session_state.setdefault("language","en")
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 🌍 "+ui_text("Language",de="Sprache",it="Lingua",es="Idioma",pt="Idioma",fr="Langue",zh="语言",ar="اللغة",hi="भाषा"))
    cols=st.sidebar.columns(len(LANGUAGES))
    for col,(code,(flag,name,caption)) in zip(cols,LANGUAGES.items()):
        if col.button(flag,key=f"lang_{code}"):
            st.session_state.language=code
            for page in ("guided","pinboard","explore"):
                if "disp_"+page in st.session_state:
                    st.session_state["disp_"+page]["playing"]=False
            st.rerun()
    st.sidebar.caption(LANGUAGES.get(st.session_state.language,LANGUAGES["en"])[2])
    if st.session_state.language not in ("en","de"):
        st.sidebar.caption(ui_text("Scientific text and experiment controls currently use English fallback.",
            it="Il testo scientifico e i controlli dell’esperimento sono attualmente disponibili in inglese.",
            es="El texto científico y los controles del experimento se muestran por ahora en inglés.",
            pt="O texto científico e os controlos da experiência são atualmente apresentados em inglês.",
            fr="Le texte scientifique et les commandes de l’expérience sont actuellement affichés en anglais.",
            zh="科学文本和实验控件目前回退至英语。",ar="يُعرض النص العلمي وعناصر التحكم في التجربة حاليًا باللغة الإنجليزية.",
            hi="वैज्ञानिक पाठ और प्रयोग नियंत्रण फिलहाल अंग्रेज़ी में दिखाए जाते हैं।"))


def run_module():
    st.session_state.setdefault("language","en")
    st.session_state.setdefault("layout_choice","centered")
    definitions=page_definitions()
    pages=[st.Page(fn,title=label,url_path=ident,default=ident=="overview") for ident,fn,label in definitions]
    active=st.navigation(pages,position="hidden")
    st.sidebar.markdown("## 💧 :blue["+tr("Dispersion laboratory navigation","Navigation im Dispersionslabor")+"]")
    st.markdown("""<style>
    section[data-testid="stSidebar"] .stButton button {
      background:none;border:none;text-align:left;font-weight:700;padding:.3rem .35rem;
    }
    section[data-testid="stSidebar"] .stButton button:hover {background:rgba(44,123,229,.1);}
    </style>""",unsafe_allow_html=True)
    for (ident,fn,label),page in zip(definitions,pages):
        if ident=="principles":
            st.sidebar.markdown("### :blue["+tr("Choose a topic","Thema auswählen")+"]")
        if ident=="references":
            st.sidebar.markdown("**"+tr("Additional information","Zusätzliche Informationen")+"**")
        selected=active.url_path==page.url_path
        if st.sidebar.button(label+(" 👈" if selected else ""),key=f"nav_{ident}"):
            for name in ("guided","pinboard","explore"):
                if "disp_"+name in st.session_state:
                    st.session_state["disp_"+name]["playing"]=False
            st.switch_page(page)
    language_selector()
    st.sidebar.markdown("---")
    chosen=st.sidebar.radio(tr("Page layout","Seitenlayout"),["centered","wide"],
                            index=["centered","wide"].index(st.session_state.layout_choice))
    if chosen!=st.session_state.layout_choice:
        st.session_state.layout_choice=chosen;st.rerun()
    active.run()
