"""Teaching pages, reusable in any parent Streamlit module.

CODE MAP — refresh with python scripts/update_code_index.py
  L0021  markdown
  L0028  illustration
  L0035  overview
  L0050  principles
  L0065  references
END CODE MAP
"""
from pathlib import Path
import streamlit as st
import re
from .i18n import content
from .presentation import apply_styles, section
from .ui import tr, experiment

FIGURES=Path(__file__).resolve().parent.parent/"assets"/"figures"


def markdown(name):
    text=content(name,st.session_state.get("language","en"))
    for index,part in enumerate(re.split(r"\$\$(.*?)\$\$",text,flags=re.S)):
        if part.strip():
            st.latex(part.strip()) if index%2 else st.markdown(part.strip())


def illustration(name,caption):
    language=st.session_state.get("language","en")
    path=FIGURES/(name+("_de" if language=="de" else "")+".png")
    if path.is_file():
        st.image(str(path),caption=caption,width="stretch")


def overview():
    st.title(tr("Dispersion laboratory","Dispersionslabor"))
    # Opening-page review panel, following the Groundwater Discovery module.
    apply_styles()
    with section("review_notice",tr(":red[**Draft material · currently under review**]",
                                   ":red[**Entwurf · derzeit in Begutachtung**]"),tone="review"):
        markdown("review_notice")
    st.subheader(tr("Follow a particle. Observe a plume.","Ein Teilchen verfolgen. Eine Stoffwolke beobachten."),divider="blue")
    markdown("start_01")
    illustration("space_time",tr("One choice changes a pathway; many choices reveal a distribution. Original schematic, not measured data.",
                                 "Eine Entscheidung verändert einen Weg; viele Entscheidungen zeigen eine Verteilung. Eigene schematische Darstellung, keine Messdaten."))
    with st.expander(tr("Learning objectives and suggested sequence","Lernziele und empfohlener Ablauf"),expanded=True):
        markdown("start_02")


def principles():
    st.title(tr("Principles and guided experiment","Grundlagen und geführtes Experiment"))
    st.subheader(tr("Physical processes and model assumptions","Physikalische Prozesse und Modellannahmen"),divider="blue")
    markdown("theory_01")
    with st.expander(tr("The physical Galton board","Das physische Galtonbrett")):
        st.image(str(FIGURES/"GaltonBoard.png"),width=330)
        markdown("galton_credit")
    with st.expander(tr("The pinboard principle and its equations","Das Galtonbrett-Prinzip und seine Gleichungen")):
        markdown("theory_02")
        illustration("binomial",tr("Exact outlet probabilities of the ideal board.","Exakte Auslasswahrscheinlichkeiten des idealen Bretts."))
    st.subheader(tr("Guided experiment · follow 1–10 particles","Geführtes Experiment · 1–10 Teilchen verfolgen"),divider="green")
    markdown("guided_01")
    experiment("guided",guided=True)


def references():
    st.title(tr("References and model notes","Quellen und Modellhinweise"))
    st.subheader(tr("Scientific basis and interpretation","Wissenschaftliche Grundlage und Interpretation"),divider="blue")
    markdown("references")
    for name,en,de,fig in [
        ("theory_03","Arrival times and injection","Ankunftszeiten und Zugabe","arrival"),
        ("theory_04","Grain-network equations","Gleichungen des Kornnetzwerks","grain"),
        ("theory_05","Continuum interpretation","Kontinuumsinterpretation",None),
        ("theory_06","Mass markers and model limits","Massenteilchen und Modellgrenzen",None),
    ]:
        with st.expander(tr(en,de)):
            markdown(name)
            if fig:illustration(fig,tr("Original teaching illustration.","Eigene Lehrabbildung."))
    with st.expander(tr("Where are the settings?","Wo befinden sich die Einstellungen?"),expanded=True):
        markdown("settings_map")
    with st.expander(tr("Scope and verification","Geltungsbereich und Überprüfung")):
        markdown("scope")
