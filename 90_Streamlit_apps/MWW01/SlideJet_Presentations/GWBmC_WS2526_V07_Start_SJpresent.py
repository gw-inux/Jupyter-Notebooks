import os
import streamlit as st
import json
import img2pdf
import yaml
import markdown
from PIL import Image
from deep_translator import GoogleTranslator
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

# This is a generalized application to present PowerPoint slides and notes as slideshow through Streamlit.
# You can adapt the script with defining another YAML file (The YAML contain the paths, headers, and other information).

###########################
# EVENTUALLY ADAPT HERE:

# PART OF A MULTIPAGE-APP?
# THEN REMOVE THE FOLLOWING LINE
# st.set_page_config(page_title="SlideJet - Present", page_icon="🚀")

# --- Default YAML path, use / ---
#DEFAULT_YAML = "example.yaml"
DEFAULT_YAML = "MWW01/SlideJet_Presentations/GWBmC_WS2526_V07_Start_SJconfig.yaml"

# --- Proxy ID --- This should be
# an unique ID if the app is used
# multiple times in a multipage app (string required)
app_id = "app_17"
#
###########################

# --- FUNCTIONS ---

def validate_config(config):
    # Checks if the YAML config is complete. Warns the user if essential parts are missing.
    required_keys = ["presentation_folder", "header_text", "subheader_text"]
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing required keys in YAML: {', '.join(missing)}")

def translate_notes(text, target_lang):
    # Translate the text with GOOGLE translate
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"[Translation failed: {e}]"

def generate_pdf(slides, img_folder, pres_folder, trans_lan, with_notes=False, text='Download PDF'):
    imgs = [os.path.join(img_folder, os.path.basename(slide['image'])) for slide in slides]
    
    if with_notes:
        # Prepare notes (translated if selected)
        for slide in slides:
            note = slide['notes']
            if trans_lan:
                if "translated_notes" not in slide:
                    slide["translated_notes"] = translate_notes(note, trans_lan)
        
        # Output file name with language and notes indicator
        pres_name = os.path.basename(pres_folder)
        lang_suffix = f"_{trans_lan}" if trans_lan else "_original"
        filename = f"{pres_name}_with_notes{lang_suffix}.pdf"
        
        output_pdf = os.path.join(pres_folder, filename)

        add_notes_with_overlay(
            slides=slides,
            images=imgs,
            output_pdf=output_pdf,
            trans_lan=trans_lan,
            font_size=11,
            line_spacing=16,
            text_color=colors.black,
            bg_color=colors.white
        )

    else:
        # Standard PDF without notes using img2pdf
        pres_name = os.path.basename(pres_folder)
        filename = f"{pres_name}_without_notes.pdf"
        output_pdf = os.path.join(pres_folder, filename)

        with open(output_pdf, 'wb') as f:
            f.write(img2pdf.convert(imgs))
    
    # Provide download
    with open(output_pdf, 'rb') as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(
        label=text,
        data=PDFbyte,
        file_name=filename,
        mime='application/octet-stream',
        icon=':material/download:',
        type='primary'
    )

def add_notes_with_overlay(slides, images, output_pdf, trans_lan=None, font_size=12, line_spacing=16, 
                           margin_left=2*cm, margin_top=2*cm, margin_bottom=2*cm, margin_right=2*cm, 
                           notes_height_ratio=0.3, text_color=colors.black, bg_color=colors.whitesmoke):
    """
    Generates a PDF where each page has:
    - The slide image in the upper part
    - Both original and translated speaker notes in the bottom part (if translation is selected)

    Parameters:
    - slides: List of slide dicts (with 'notes' and optional 'translated_notes')
    - images: List of slide image paths
    - output_pdf: Output PDF path
    - trans_lan: Translation language code (e.g., 'de', 'es') or None for original only
    - font_size: Font size for notes
    - line_spacing: Line spacing in notes
    - margin_left, margin_top, margin_bottom, margin_right: Margins in cm
    - notes_height_ratio: Fraction of page height for notes (e.g., 0.3 = 30% for notes)
    - text_color: Text color for notes
    - bg_color: Background color for notes section
    """
    doc = SimpleDocTemplate(output_pdf, pagesize=A4,
                            leftMargin=margin_left, rightMargin=margin_right,
                            topMargin=margin_top, bottomMargin=margin_bottom)
    elements = []
    width, height = A4

    styles = getSampleStyleSheet()
    notes_style = ParagraphStyle(
        'NotesStyle',
        parent=styles['Normal'],
        fontSize=font_size,
        leading=line_spacing,
        textColor=text_color,
        backColor=bg_color,
    )

    for slide, img_path in zip(slides, images):
        # --- Image placement with aspect ratio preserved ---
        available_width = width - margin_left - margin_right
        available_height = (height - margin_top - margin_bottom) * (1 - notes_height_ratio)

        img = RLImage(img_path)
        scale_w = available_width / img.imageWidth
        scale_h = available_height / img.imageHeight
        scale_factor = min(scale_w, scale_h)

        img.drawWidth = img.imageWidth * scale_factor
        img.drawHeight = img.imageHeight * scale_factor

        # Center image horizontally if there's remaining space
        img_h_space = (available_width - img.drawWidth) / 2 if available_width > img.drawWidth else 0
        if img_h_space > 0:
            elements.append(Spacer(img_h_space, 0))
        elements.append(img)

        # Spacer between image and notes
        elements.append(Spacer(1, 0.5*cm))

        # --- Prepare notes ---
        original_note = slide['notes']
        original_md = f"**Original Notes:**\n\n{original_note}"

        if trans_lan:
#            if "translated_notes" not in slide:
#                slide["translated_notes"] = translate_notes(original_note, trans_lan)
#            trans_note = slide["translated_notes"]
            trans_note = translate_notes(original_note, trans_lan)

            trans_md = f"**Translated Notes ({trans_lan})**\n\n{trans_note}"
            combined_md = trans_md + "<br/><br/>" + original_md
        else:
            combined_md = original_md

        # Convert markdown to HTML then Paragraph
        html_note = markdown.markdown(combined_md).replace("\n", "<br/>")
        elements.append(Paragraph(html_note, notes_style))

        # Page break after each slide
        #elements.append(Spacer(1, 2*cm))
        elements.append(PageBreak())

    doc.build(elements)

# --- Print Title
#st.title("Presentation Slides")

# --- Define keys ---
reset_key = f"{app_id}_reset_mode"
config_key = f"{app_id}_config"
slide_data_key = f"{app_id}_slide_data"
presentation_folder_key = f"{app_id}_presentation_folder"
images_folder_key = f"{app_id}_images_folder"
header_text_key = f"{app_id}_header_text"
subheader_text_key = f"{app_id}_subheader_text"
default_yaml_key = f"{app_id}_default_yaml"

# --- Initialize reset mode ---
if reset_key not in st.session_state:
    st.session_state[reset_key] = False
    
if default_yaml_key not in st.session_state:
    st.session_state[default_yaml_key] = DEFAULT_YAML

# --- Configuration loading / depending if it's the start or a reset ---
if config_key not in st.session_state or st.session_state[config_key] is None:

    if st.session_state[reset_key]:
        # User wants to load a new YAML, show uploader
        st.session_state[config_key] = None
        st.warning("Please upload a new SlideJet YAML file. Alternatively, you can use the Default YAML again.")
        
        uploaded_yaml = st.file_uploader("Upload your slidejet_config.yaml", type=["yaml", "yml"])

        if uploaded_yaml is not None:
            try:
                st.session_state[config_key] = yaml.safe_load(uploaded_yaml)
                validate_config(st.session_state[config_key])
            except yaml.YAMLError as e:
                st.error(f"YAML parsing error: {e}")
                st.stop()
            except ValueError as e:
                st.error(str(e))
                st.stop()
            st.session_state[reset_key] = False  # Done loading new config
            st.rerun()  # Restart to apply
        
        col1, col2, col3 = st.columns((1,1,1))
        with col2:
            if st.button("🔄 Use Default YAML again"):
                try:
                    with open(st.session_state[default_yaml_key], "r", encoding="utf-8") as f:
                        st.session_state[config_key] = yaml.safe_load(f)
                    validate_config(st.session_state[config_key])
                    st.session_state[reset_key] = False
                    st.success("Default YAML loaded.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading default YAML: {e}")
                    st.stop()

        if st.session_state[config_key] is None:
            st.stop()

    else:
        # Normal start: Try to load default YAML
        if os.path.exists(DEFAULT_YAML):
            with open(DEFAULT_YAML, "r") as f:
                st.session_state[config_key] = yaml.safe_load(f)
        else:
            st.session_state[config_key] = None

        if st.session_state[config_key] is None:
            st.warning("No default YAML found. Please upload a SlideJet YAML file.")
            uploaded_yaml = st.file_uploader("Upload your slidejet_config.yaml", type=["yaml", "yml"])

            if uploaded_yaml is not None:
                try:
                    st.session_state[config_key] = yaml.safe_load(uploaded_yaml)
                    validate_config(st.session_state[config_key])
                except yaml.YAMLError as e:
                    st.error(f"YAML parsing error: {e}")
                    st.stop()
                except ValueError as e:
                    st.error(str(e))
                    st.stop()

# Use config
config = st.session_state[config_key]
# Store the config values into specific session keys
st.session_state[presentation_folder_key] = config["presentation_folder"]
st.session_state[header_text_key] = config["header_text"]
st.session_state[subheader_text_key] = config["subheader_text"]

# --- Streamlit App Content ---

# --- Initialize session state ---
if slide_data_key not in st.session_state:
    st.session_state[slide_data_key] = None
if presentation_folder_key not in st.session_state or st.session_state[presentation_folder_key] is None:
    st.session_state[presentation_folder_key] = presentation_folder
if images_folder_key not in st.session_state or st.session_state[images_folder_key] is None:
    st.session_state[images_folder_key] = os.path.join(st.session_state[presentation_folder_key], "images")

# --- Load slides ---
JSON_file = os.path.join(st.session_state[presentation_folder_key], "slide_data.json")

if st.session_state[slide_data_key] is None:
    if os.path.exists(JSON_file):
        with open(JSON_file, "r") as f:
            st.session_state[slide_data_key] = json.load(f)
    else:
        config_file = st.file_uploader("**Default presentation not found.** This likely happens if the path to the files is corrupt or missing. Please upload your slidejet_config.yaml file.", type=["yaml", "yml"])
        
        if config_file is not None:
            try:
                st.session_state[config_key] = yaml.safe_load(config_file)
                validate_config(st.session_state[config_key])
            except Exception as e:
                st.error(f"Error loading config: {e}")
                st.stop()
            
            config = st.session_state[config_key]
            st.session_state[presentation_folder_key] = config["presentation_folder"]
            st.session_state[images_folder_key] = os.path.join(config["presentation_folder"], "images")
            st.session_state[header_text_key] = config.get("header_text", "Presentation Title")
            st.session_state[subheader_text_key] = config.get("subheader_text", "Subtitle")
        
            JSON_file = os.path.join(st.session_state[presentation_folder_key], "slide_data.json")
            try:
                with open(JSON_file, "r") as f:
                    st.session_state[slide_data_key] = json.load(f)
            
                # This belongs in the SUCCESS block
                first_image = st.session_state[slide_data_key][0]["image"]
                image_path = os.path.join(st.session_state[images_folder_key], os.path.basename(first_image))
                if not os.path.exists(image_path):
                    st.warning(f"Image `{image_path}` not found. Please check your images folder.")
            
            except Exception as e:
                st.error(f"Error loading slide_data.json: {e}")
                st.stop()

# --- Print Title and Header 
st.header(f':blue[{st.session_state[header_text_key]}]')
st.subheader(st.session_state[subheader_text_key], divider='blue')

# --- Language selection ---
languages = {
    "🇬🇧 English": "en",
    "🇪🇸 Spanish": "es",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇮🇹 Italian": "it",
    "🇸🇪 Swedish": "sv",
    "🇩🇰 Danish": "da",
    "🇳🇴 Norwegian": "no",
    "🇷🇺 Russian": "ru",
    "🇨🇳 Chinese (Simplified)": "zh-CN",
    "🇮🇳 Hindi": "hi",
    "🇧🇩 Bengali": "bn",
    "🇺🇾 Urdu": "ur",    
    "🇦🇪 Arabic": "ar",
    "🇯🇵 Japanese": "ja",
    "🇰🇷 Korean": "ko",
    "🇻🇳 Vietnamese": "vi",
    "🇹🇷 Turkish": "tr",
    "🇵🇹 Portuguese": "pt",
    "🇵🇱 Polish": "pl",
    "🇳🇱 Dutch": "nl", 
    "🇮🇩 Indonesian": "id",
    "🇹🇭 Thai": "th",
}

language_names = ["🌐 Original Notes"] + list(languages.keys())

st.markdown(""" 
    **About the SlideJet presentation:** _Navigate the slides using the +/- buttons or enter a slide number._
""")

# --- Show slides ---
if st.session_state[slide_data_key]:
    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 1

    selected_lang_display = st.selectbox("**Speaker notes can be translated.** Please choose the language:", options=language_names)
    target_lang = None if selected_lang_display == "🌐 Original Notes" else languages[selected_lang_display]

    num_slides = len(st.session_state[slide_data_key])
    lc, cc, rc = st.columns((1,3,1))
    with cc:
        st.session_state["slide_index"] = st.number_input(f'**Select slide to show** (1–{num_slides})', 1, num_slides)

    selected_slide = st.session_state[slide_data_key][st.session_state["slide_index"] - 1]
    image_path = os.path.join(st.session_state[images_folder_key], os.path.basename(selected_slide["image"]))
    st.image(image_path)

    note_text = selected_slide["notes"]
    if target_lang:
        translated = translate_notes(note_text, target_lang)
        st.write(f"**Translated Notes** ({selected_lang_display})\n\n{translated}")
        with st.expander("Show original notes"):
            st.write(note_text)
    else:
        st.write(f"**Notes:**\n\n{note_text}")

    # --- Download buttons ---
    '---'
    st.markdown(""" 
    #### Download:
    _Subsequently you can generate a PDF file :green[with] or :orange[without] notes for download. After selection, the file will be generated and subsequently provided for local download._
""")
    pcol1, pcol2, pcol3 = st.columns([5, 1, 5])
    with pcol1:
        if st.button('Prepare pdf :green[(**with notes**)] for download'):
            generate_pdf(st.session_state[slide_data_key], st.session_state[images_folder_key], st.session_state[presentation_folder_key], target_lang, with_notes=True, text='Download pdf (with notes)')
    with pcol3:
        if st.button('Prepare pdf :orange[(**without notes**)] for download'):
            generate_pdf(st.session_state[slide_data_key], st.session_state[images_folder_key], st.session_state[presentation_folder_key], target_lang)

else:
    st.warning("The presentation is not loaded yet.")

#'---'
#st.markdown(":grey[**Presentation Management**]")
#
#with st.expander('🔄 :red[**CLICK HERE**] if you want to load another presentation'):
#    st.warning("Are you sure you want to load another presentation? **If yes**, you will be able to select another presentation through a YAML-file. However, **this will remove the current presentation** from memory.")
#
#    col1, col2, col3 = st.columns((3,4,2))
#    with col2:
#        if st.button("✅ Yes, load new presentation"):
#            st.session_state[reset_key] = True
#            st.session_state[config_key] = None
#            st.session_state[slide_data_key] = None
#            st.session_state[presentation_folder_key] = None
#            st.session_state[images_folder_key] = None
#            st.rerun()

# --- Footer (Authors and Copyright)---
'---'
year = 2025 
authors = {"Thomas Reimann": [1], "Nils Wallenberg": [2]}
institutions = {1: "TU Dresden", 2: "University of Gothenburg"}

author_list = [f"{name}{''.join(f'<sup>{i}</sup>' for i in idxs)}" for name, idxs in authors.items()]
institution_text = " | ".join([f"<sup>{i}</sup> {inst}" for i, inst in institutions.items()])
columns_lic = st.columns((2,1))

with columns_lic[0]:
    st.markdown(f'**SlideJet developed by** <br> {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.markdown('**Open-source license for SlideJet:**', unsafe_allow_html=True)
    try:
        st.image(Image.open("FIGS/CC_BY-SA_icon.png"))
    except FileNotFoundError:
        st.image("https://raw.githubusercontent.com/gw-inux/SlideJet/main/FIGS/CC_BY-SA_icon.png")
