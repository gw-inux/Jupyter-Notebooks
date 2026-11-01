"""Soil Water Retention translation convention, with English fallback.

CODE MAP — refresh with python scripts/update_code_index.py
  L0026  ui_text
  L0034  load_md
  L0050  content
END CODE MAP
"""
from pathlib import Path
import re

MD_ROOT = Path(__file__).resolve().parent.parent / "assets" / "md"
LANGUAGES = {
    "en": ("🇬🇧", "English", "Module language: English"),
    "de": ("🇩🇪", "Deutsch", "Modulsprache: Deutsch"),
    "it": ("🇮🇹", "Italiano", "Lingua del modulo: Italiano"),
    "es": ("🇪🇸", "Español", "Idioma del módulo: Español"),
    "pt": ("🇵🇹", "Português", "Idioma do módulo: Português"),
    "fr": ("🇫🇷", "Français", "Langue du module : Français"),
    "zh": ("🇨🇳", "中文", "模块语言：中文"),
    "ar": ("🇸🇦", "العربية", "لغة الوحدة: العربية"),
    "hi": ("🇮🇳", "हिन्दी", "मॉड्यूल की भाषा: हिन्दी"),
}


def ui_text(en: str, *, language: str | None = None, **translations) -> str:
    """Use shared session state unless called by a pure plotting function."""
    if language is None:
        import streamlit as st
        language = st.session_state.get("language", "en")
    return translations.get(language) or en


def load_md(MD_DIR: Path, filename: str, language: str = "en") -> str:
    """Same API and search order as the Soil Water Retention update.

    Example: theory_01_de.md, then theory_01.md. Paths are relative to this
    package, not the working directory. Only code-owned basenames are accepted.
    """
    if not re.fullmatch(r"[A-Za-z0-9_-]+\.md", filename):
        raise ValueError("Invalid Markdown filename.")
    base = Path(filename)
    if language in LANGUAGES and language != "en":
        translated = Path(MD_DIR) / f"{base.stem}_{language}{base.suffix}"
        if translated.is_file():
            return translated.read_text(encoding="utf-8")
    return (Path(MD_DIR) / filename).read_text(encoding="utf-8")


def content(name: str, language: str = "en") -> str:
    return load_md(MD_ROOT, name + ".md", language)
