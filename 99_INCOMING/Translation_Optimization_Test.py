import streamlit as st
import re
import unicodedata
import random
import string
from deep_translator import GoogleTranslator

# ✅ Generate a unique random sequence for each term
def generate_random_key():
    """Creates a truly random sequence to act as a placeholder."""
    return ''.join(random.choices(string.ascii_letters + string.digits + "{}^/", k=10))
    
# ✅ Store random placeholders directly in `technical_terms`
technical_terms = {
    "slug test": generate_random_key(),
    "hydraulic conductivity": generate_random_key(),
    "aquifer": generate_random_key(),
    "pumping test": generate_random_key()
}

st.write(technical_terms)

# ✅ Reverse lookup dictionary to get the original term from the placeholder
decryption_map = {v: k for k, v in technical_terms.items()}  # Reverse map for decoding

# ✅ Define correct translations for technical terms per language
translations_dict = {
    "de": {  # German 🇩🇪
        "slug test": "Slug-Test",
        "hydraulic conductivity": "hydraulische Leitfähigkeit",
        "aquifer": "Grundwasserleiter",
        "pumping test": "Pumpversuch"
    },
    "fr": {  # French 🇫🇷
        "slug test": "essai de slug",
        "hydraulic conductivity": "conductivité hydraulique",
        "aquifer": "aquifère",
        "pumping test": "essai de pompage"
    },
    "es": {  # Spanish 🇪🇸
        "slug test": "prueba de slug",
        "hydraulic conductivity": "conductividad hidráulica",
        "aquifer": "acuífero",
        "pumping test": "prueba de bombeo"
    },
    "ca": {  # Catalan 🇦🇩
        "slug test": "prova de slug",
        "hydraulic conductivity": "conductivitat hidràulica",
        "aquifer": "aqüífer",
        "pumping test": "prova de bombeig"
    },
    "it": {  # Italian 🇮🇹
        "slug test": "test di slug",
        "hydraulic conductivity": "conducibilità idraulica",
        "aquifer": "acquifero",
        "pumping test": "test di pompaggio"
    },
    "zh-CN": {  # Chinese 🇨🇳
        "slug test": "slug 测试",
        "hydraulic conductivity": "水力传导率",
        "aquifer": "含水层",
        "pumping test": "抽水试验"
    },
    "ja": {  # Japanese 🇯🇵
        "slug test": "スラッグ試験",
        "hydraulic conductivity": "水理伝導率",
        "aquifer": "帯水層",
        "pumping test": "揚水試験"
    }
}

def remove_accents(input_str):
    """Removes accents and normalizes Unicode characters for consistent replacement."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def translate_text(text, target_language):
    """Translates text while protecting technical terms using true random encoding."""
    
    # 1️⃣ **Replace technical terms with randomized placeholders**
    for term, placeholder in technical_terms.items():
        text = re.sub(rf'\b{re.escape(term)}\b', placeholder, text, flags=re.IGNORECASE)

    # 2️⃣ **Translate the text**
    if target_language == "en":  # No translation needed for English
        return text

    translator = GoogleTranslator(source="auto", target=target_language)
    translated_text = translator.translate(text)

    # 3️⃣ **Normalize accents before replacing placeholders**
    normalized_text = remove_accents(translated_text)

    # 4️⃣ **Replace placeholders with correct translations**
    if target_language in translations_dict:
        for placeholder, original_term in decryption_map.items():
            # Get the correct translation for the technical term
            correct_translation = translations_dict[target_language].get(original_term, original_term)
            # Replace placeholder with translated term
            normalized_text = re.sub(re.escape(placeholder), correct_translation, normalized_text, flags=re.IGNORECASE)

    return normalized_text.strip()

# ✅ **Test Cases**
original_text = "A slug test is used to determine the hydraulic conductivity of an aquifer."
translated_de = translate_text(original_text, "de")  
translated_fr = translate_text(original_text, "fr")
translated_es = translate_text(original_text, "es")  
translated_ca = translate_text(original_text, "ca")  
translated_it = translate_text(original_text, "it")  
translated_zh = translate_text(original_text, "zh-CN")  
translated_ja = translate_text(original_text, "ja")

st.write("🔹 Deutsch:", translated_de)
st.write("🔹 Français:", translated_fr)
st.write("🔹 Español:", translated_es)
st.write("🔹 Català:", translated_ca)
st.write("🔹 Italiano:", translated_it)
st.write("🔹 中文 (Simplified Chinese):", translated_zh)
st.write("🔹 日本語 (Japanese):", translated_ja)
