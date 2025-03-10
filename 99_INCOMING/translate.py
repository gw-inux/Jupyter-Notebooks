import streamlit as st
import re
from deep_translator import GoogleTranslator

st.title('🌍 Streamlit App Translation')

st.header(':rainbow[Test app for deep_translator]')

st.subheader(':rainbow-background[Feasibility of automatic translation in Streamlit Apps]')

# Function to translate Markdown text while preserving bold/italic formatting
def translate_markdown(markdown_text, target_language):
    try:
        translator = GoogleTranslator(source='auto', target=target_language)

        # ✅ Step 1: Add spaces inside **bold** and *italic* before translation
        text_with_spaces = re.sub(r"(\*\*|\*)(\S.*?\S)(\*\*|\*)", r"\1 \2 \3", markdown_text)

        # ✅ Step 2: Split text into lines to preserve Markdown structure
        lines = text_with_spaces.strip().split("\n")

        translated_lines = []
        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("#"):  # ✅ Preserve headers (even multiple ##)
                header_level = len(stripped_line) - len(stripped_line.lstrip("#"))  # Count #
                text_without_hash = stripped_line.lstrip("#").strip()  # Remove #
                translated_text = translator.translate(text_without_hash)  # Translate only text
                translated_lines.append("#" * header_level + " " + translated_text)  # Rebuild header
            else:
                translated_lines.append(translator.translate(stripped_line))

        translated_text = "\n\n".join(translated_lines)  # Ensure proper spacing

        # ✅ Step 3: Remove spaces inside **bold** and *italic* after translation
        final_text = re.sub(r"(\*\*|\*) (.*?) (\*\*|\*)", r"\1\2\3", translated_text)

        return final_text
    
    except Exception as e:
        st.error(f"❌ Translation failed: {e}")
        return markdown_text  # Return original text if translation fails

# ✅ Split the long Markdown text into multiple sections
text1 = """
# 🍦 The Culture of Italian Gelato
Gelato is more than just ice cream in **Italy**—it is an essential part of daily life and a **symbol of Italian culture**. 
Unlike industrial ice cream, gelato is **crafted daily** in artisanal shops called _gelaterie_.
"""

text2 = """
## 🍨 The Differences Between Gelato and Ice Cream
Gelato is **not the same** as traditional ice cream. Some key differences include:
- **Less fat**: Gelato is made with more **milk** and less **cream**, making it lower in fat.
- **Denser texture**: It is churned at a **slower speed**, incorporating less air.
- **More intense flavor**: With less fat, flavors are more pronounced and natural.
"""

text3 = """
## 🍧 Popular Gelato Flavors in Italy
Italy offers a wide variety of **classic and modern flavors**, including:

### **Classic Flavors**
- **Pistachio** (_Pistacchio_) 🌰
- **Hazelnut** (_Nocciola_) 🌰
- **Chocolate** (_Cioccolato_) 🍫
- **Lemon** (_Limone_) 🍋
- **Stracciatella** (vanilla with chocolate shavings) 🍦🍫

### **Modern & Creative Flavors**
- **Tiramisu** 🍰☕
- **Ricotta & Fig** 🧀🍯
- **Basil & Lemon** 🌿🍋
- **Salted Caramel** 🍯🧂
"""

text4 = """
## 📍 Where to Find the Best Gelato
The best gelato comes from _gelaterie artigianali_ (artisan gelato shops). Look for these signs of **high-quality gelato**:
- **Natural colors** (not overly bright or artificial)
- **Seasonal flavors** using fresh ingredients
- **Stored in covered metal containers** instead of high, colorful mountains

Famous gelaterie include:
- [Gelateria del Teatro](https://www.gelateriadelteatro.it/) (Rome 🇮🇹)
- [Grom](https://www.grom.it/) (Various locations)
- [La Carraia](https://www.lacarraiagroup.eu/) (Florence 🇮🇹)
"""

text5 = """
## 🌍 The Worldwide Popularity of Gelato
Italian gelato has gained **global popularity**, with artisanal gelaterie opening in:
- 🇫🇷 **France** – Especially in Paris and the Riviera.
- 🇩🇪 **Germany** – Many Italian immigrants brought gelato culture.
- 🇺🇸 **United States** – Gelato shops are booming in major cities.
- 🇯🇵 **Japan** – Creative flavors like **matcha gelato** are a hit.

Whether in Italy or abroad, gelato remains a **beloved tradition** for people of all ages! 🍦✨
"""

# ✅ Language selection dropdown
languages = ['fr', 'es', 'it', 'ru']
target_lang = st.selectbox("🌎 Choose the target language", languages)

# ✅ Translate each section separately
translated_text1 = translate_markdown(text1, target_lang)
translated_text2 = translate_markdown(text2, target_lang)
translated_text3 = translate_markdown(text3, target_lang)
translated_text4 = translate_markdown(text4, target_lang)
translated_text5 = translate_markdown(text5, target_lang)

# ✅ Display the translated sections
st.markdown(translated_text1)
st.markdown(translated_text2)
st.markdown(translated_text3)
st.markdown(translated_text4)
st.markdown(translated_text5)
