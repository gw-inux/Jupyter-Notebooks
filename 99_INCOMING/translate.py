import streamlit as st
import re
from deep_translator import GoogleTranslator

st.title('🌍 Streamlit App Translation')

st.header(':rainbow[Test app for deep_translator]')

st.subheader(':rainbow-background[Feasibility of automatic translation in Streamlit Apps]')

# Function to preserve Markdown formatting during translation
def translate_markdown(markdown_text, target_language):
    try:
        translator = GoogleTranslator(source='auto', target=target_language)

        # Function to translate while keeping Markdown bold/italic intact
        def translate_with_formatting(match):
            original_text = match.group(2)  # Extract the text inside the formatting
            translated_text = translator.translate(original_text)  # Translate only the inner text
            return f"{match.group(1)}{translated_text}{match.group(1)}"  # Reconstruct with ** or *

        # Preserve bold (**bold**) and italic (*italic*) formatting
        formatted_text = re.sub(r"(\*\*|\*)(.*?)\1", translate_with_formatting, markdown_text)

        # Split text into lines to preserve Markdown headers
        lines = formatted_text.strip().split("\n")

        translated_lines = []
        for line in lines:
            if line.strip().startswith("#"):  # Preserve Markdown headers
                header_level = line.count("#")
                text_without_hash = line.lstrip("#").strip()
                translated_text = translator.translate(text_without_hash)
                translated_lines.append("#" * header_level + " " + translated_text)
            else:
                translated_lines.append(translator.translate(line))

        return "\n\n".join(translated_lines)  # Ensure proper Markdown spacing
    
    except Exception as e:
        st.error(f"❌ Translation failed: {e}")
        return markdown_text  # Return original text if translation fails

# Example Markdown text
Text1 = """
# 🍦 The Culture of Italian Gelato
Gelato is more than just ice cream in **Italy**—it is an essential part of daily life and a **symbol of Italian culture**. 

## 🍨 Differences Between Gelato and Ice Cream
- **Less fat**
- **Denser texture**
- **More intense flavor**

## 📍 Where to Find the Best Gelato
- [Gelateria del Teatro](https://www.gelateriadelteatro.it/) (Rome 🇮🇹)
- [Grom](https://www.grom.it/) (Various locations)
- [La Carraia](https://www.lacarraiagroup.eu/) (Florence 🇮🇹)
"""

# Language selection dropdown
languages = ['fr', 'es', 'it', 'ru']
target_lang = st.selectbox("🌎 Choose the target language", languages)

# Translate the text using Google Translator only
Text1_t = translate_markdown(Text1, target_lang)

# Display the translated Markdown properly
st.markdown(Text1_t)



## 🍦 The Culture of Italian Gelato
#Gelato is more than just ice cream in **Italy**—it is an essential part of daily life and a **symbol of Italian culture**. Unlike industrial ice cream, gelato is **crafted daily** in artisanal shops called _gelaterie_. 
#
#Walking through Italian streets, you will see locals and tourists enjoying gelato at any time of day. Many Italians consider gelato a **social activity**, a perfect excuse to take a break, walk around, and enjoy a refreshing treat. 
#
### 🍨 The Differences Between Gelato and Ice Cream
#Gelato is **not the same** as traditional ice cream. Some key differences include:
#- **Less fat**: Gelato is made with more **milk** and less **cream**, making it lower in fat.
#- **Denser texture**: It is churned at a **slower speed**, incorporating less air.
#- **More intense flavor**: With less fat, flavors are more pronounced and natural.
#
### 🍧 Popular Gelato Flavors in Italy
#Italy offers a wide variety of **classic and modern flavors**, including:
#
#### **Classic Flavors**
#- **Pistachio** (_Pistacchio_) 🌰
#- **Hazelnut** (_Nocciola_) 🌰
#- **Chocolate** (_Cioccolato_) 🍫
#- **Lemon** (_Limone_) 🍋
#- **Stracciatella** (vanilla with chocolate shavings) 🍦🍫
#
#### **Modern & Creative Flavors**
#- **Tiramisu** 🍰☕
#- **Ricotta & Fig** 🧀🍯
#- **Basil & Lemon** 🌿🍋
#- **Salted Caramel** 🍯🧂
#
### 📍 Where to Find the Best Gelato
#The best gelato comes from _gelaterie artigianali_ (artisan gelato shops). Look for these signs of **high-quality gelato**:
#- **Natural colors** (not overly bright or artificial)
#- **Seasonal flavors** using fresh ingredients
#- **Stored in covered metal containers** instead of high, colorful mountains
#
#Famous gelaterie include:
#- [Gelateria del Teatro](https://www.gelateriadelteatro.it/) (Rome 🇮🇹)
#- [Grom](https://www.grom.it/) (Various locations)
#- [La Carraia](https://www.lacarraiagroup.eu/) (Florence 🇮🇹)
#
### 🌍 The Worldwide Popularity of Gelato
#Italian gelato has gained **global popularity**, with artisanal gelaterie opening in:
#- 🇫🇷 **France** – Especially in Paris and the Riviera.
#- 🇩🇪 **Germany** – Many Italian immigrants brought gelato culture.
#- 🇺🇸 **United States** – Gelato shops are booming in major cities.
#- 🇯🇵 **Japan** – Creative flavors like **matcha gelato** are a hit.
#
#Whether in Italy or abroad, gelato remains a **beloved tradition** for people of all ages! 🍦✨
#"""
