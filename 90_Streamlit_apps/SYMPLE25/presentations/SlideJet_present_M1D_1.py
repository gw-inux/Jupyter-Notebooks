import os
import streamlit as st
import json
import img2pdf
import yaml
from pathlib import Path
from PIL import Image
from deep_translator import GoogleTranslator
from pypdf import PdfReader, PdfWriter, Transformation, PageObject, PaperSize
from pypdf.generic import RectangleObject
from pypdf.annotations import FreeText

# This is a generalized application to present PowerPoint slides and notes as slideshow through Streamlit.
# You can adapt the script with defining another YAML file (The YAML contain the paths, headers, and other information).

###########################
# EVENTUALLY ADAPT HERE:
#
# PART OF A MULTIPAGE-APP? REMOVE THE FOLLOWING LINE
#st.set_page_config(page_title="SlideJet - Present", page_icon="🚀")
#
###########################

# --- Print Title
st.title("Presentation Slides")

def validate_config(config):
    required_keys = ["presentation_folder", "header_text", "subheader_text"]
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing required keys in YAML: {', '.join(missing)}")


# --- Initialize reset mode ---
if "reset_mode" not in st.session_state:
    st.session_state.reset_mode = False
    
# --- Default YAML path ---
DEFAULT_YAML = "SYMPLE25_ M1D_TransportModeling_1_slidejet_config.yaml"

# --- Configuration loading / depending if it's the start or a reset ---
if "config" not in st.session_state or st.session_state.config is None:

    if st.session_state.reset_mode:
        # User wants to load a new YAML, show uploader
        st.session_state.config = None
        st.warning("Please upload a new SlideJet YAML file.")
        uploaded_yaml = st.file_uploader("Upload your slidejet_config.yaml", type=["yaml", "yml"])

        if uploaded_yaml is not None:
            try:
                st.session_state.config = yaml.safe_load(uploaded_yaml)
                validate_config(st.session_state.config)
            except yaml.YAMLError as e:
                st.error(f"YAML parsing error: {e}")
                st.stop()
            except ValueError as e:
                st.error(str(e))
                st.stop()
            st.session_state.reset_mode = False  # Done loading new config
            st.rerun()  # Restart to apply

        if st.session_state.config is None:
            st.stop()

    else:
        # Normal start: Try to load default YAML
        if os.path.exists(DEFAULT_YAML):
            with open(DEFAULT_YAML, "r") as f:
                st.session_state.config = yaml.safe_load(f)
        else:
            st.session_state.config = None

        if st.session_state.config is None:
            st.warning("No default YAML found. Please upload a SlideJet YAML file.")
            uploaded_yaml = st.file_uploader("Upload your slidejet_config.yaml", type=["yaml", "yml"])

            if uploaded_yaml is not None:
                try:
                    st.session_state.config = yaml.safe_load(uploaded_yaml)
                    validate_config(st.session_state.config)
                except yaml.YAMLError as e:
                    st.error(f"YAML parsing error: {e}")
                    st.stop()
                except ValueError as e:
                    st.error(str(e))
                    st.stop()
            if st.session_state.config is None:
                st.stop()



# Use config
config = st.session_state.config
presentation_folder = config["presentation_folder"]
header_text = config["header_text"]
subheader_text = config["subheader_text"]

# --- Authors and license ---
year = 2025 
authors = {"Thomas Reimann": [1], "Nils Wallenberg": [2]}
institutions = {1: "TU Dresden", 2: "University of Gothenburg"}

author_list = [f"{name}{''.join(f'<sup>{i}</sup>' for i in idxs)}" for name, idxs in authors.items()]
institution_text = " | ".join([f"<sup>{i}</sup> {inst}" for i, inst in institutions.items()])

# --- Functions ---
@st.cache_data(show_spinner=False)
def translate_notes(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"[Translation failed: {e}]"

def patch_translations_if_missing(slide_data, target_lang, translate_func):
    if not target_lang:
        return slide_data
    for slide in slide_data:
        if "translated_notes" not in slide:
            try:
                slide["translated_notes"] = translate_func(slide["notes"], target_lang)
            except Exception as e:
                slide["translated_notes"] = f"[Translation failed: {e}]"
    return slide_data

def add_notes(pdf_path, slide_data, target_lang):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)

    for i, slide in enumerate(slide_data):
        notes_to_add = slide['notes']
        if target_lang and "translated_notes" in slide:
            notes_to_add += "\n\n" + slide["translated_notes"]
        elif target_lang:
            trans_notes = translate_notes(notes_to_add, target_lang)
            notes_to_add += "\n\n" + trans_notes

        annotation = FreeText(
            text=notes_to_add,
            rect=(60, 25, 0.9 * reader.pages[i].mediabox.width, reader.pages[i].mediabox.height * 0.5),
            font="Arial", bold=False, italic=False, font_size="11pt",
            font_color="#000000", border_color="#FFFFFF", background_color="#FFFFFF",
        )
        annotation.flags = 4
        writer.add_annotation(i, annotation)

    with open(pdf_path, 'wb') as fp:
        writer.write(fp)

def pdf_as_portrait(pdf_path, nr_pages):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for i in range(nr_pages):
        page = reader.pages[i]
        A4_w, A4_h = PaperSize.A4.width, PaperSize.A4.height
        h, w = float(page.mediabox.height), float(page.mediabox.width)
        margin_pt = 2.5 * 72 / 2.54

        scale_factor = min((A4_w - 2 * margin_pt) / w, (A4_h - margin_pt) / h)
        x_offset = (A4_w - w * scale_factor) / 2
        y_offset = A4_h - h * scale_factor - margin_pt

        transform = Transformation().scale(scale_factor, scale_factor).translate(x_offset, y_offset)
        page.add_transformation(transform)

        page_A4 = PageObject.create_blank_page(width=A4_w, height=A4_h)
        page.cropbox = RectangleObject((0, 0, A4_w, A4_h))
        page.mediabox = RectangleObject((0, 0, A4_w, A4_h))
        page_A4.merge_page(page)
        writer.add_page(page_A4)

    with open(pdf_path, 'wb') as fp:
        writer.write(fp)

#def generate_pdf(slides, img_folder, pres_folder, trans_lan, with_notes=False, text='Download pdf (no notes)'):
#    imgs = [os.path.join(img_folder, os.path.basename(slide['image'])) for slide in slides]
#    out_path = os.path.join(pres_folder, 'presentation.pdf')
#    with open(out_path, 'wb') as f:
#        f.write(img2pdf.convert(imgs))
#
#    pdf_as_portrait(out_path, len(slides))
#    if with_notes:
#        patch_translations_if_missing(slides, trans_lan, translate_notes)
#        add_notes(out_path, slides, trans_lan)
#
#    with open(out_path, 'rb') as pdf_file:
#        PDFbyte = pdf_file.read()
#
#    st.download_button(label=text, data=PDFbyte, file_name='presentation.pdf', mime='application/octet-stream', icon=':material/download:', type='primary')

def generate_pdf(slides, img_folder, pres_folder, trans_lan, with_notes=False, text='Download PDF'):
    imgs = [os.path.join(img_folder, os.path.basename(slide['image'])) for slide in slides]

    presentation_name = os.path.basename(os.path.normpath(pres_folder))
    lang_suffix = f"_{trans_lan}" if trans_lan else "_original"
    notes_suffix = "_with_notes" if with_notes else "_no_notes"

    output_filename = f"{presentation_name}{notes_suffix}{lang_suffix}.pdf"
    out_path = os.path.join(pres_folder, output_filename)

    with open(out_path, 'wb') as f:
        f.write(img2pdf.convert(imgs))

    pdf_as_portrait(out_path, len(slides))

    if with_notes:
        patch_translations_if_missing(slides, trans_lan, translate_notes)
        add_notes(out_path, slides, trans_lan)

    with open(out_path, 'rb') as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(
        label=text, 
        data=PDFbyte, 
        file_name=output_filename, 
        mime='application/octet-stream', 
        icon=':material/download:', 
        type='primary'
    )

# --- Streamlit App Content ---

# --- Initialize session state ---
if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False
if "slide_data" not in st.session_state:
    st.session_state.slide_data = None
if "presentation_folder" not in st.session_state or st.session_state.presentation_folder is None:
    st.session_state.presentation_folder = presentation_folder
if "images_folder" not in st.session_state or st.session_state.images_folder is None:
    st.session_state.images_folder = os.path.join(st.session_state.presentation_folder, "images")


# --- Load slides ---
JSON_file = os.path.join(st.session_state.presentation_folder, "slide_data.json")

if st.session_state.slide_data is None:
    if os.path.exists(JSON_file):
        with open(JSON_file, "r") as f:
            st.session_state.slide_data = json.load(f)
    else:
        config_file = st.file_uploader("**Default presentation not found.** This likely happens if the path to the files is corrupt or missing. Please provide the correct path to the *.json file by an YAML file.Please upload your slidejet_config.yaml file.", type=["yaml", "yml"])
        if config_file is not None:
            try:
                config = yaml.safe_load(config_file)
                st.session_state.presentation_folder = config["presentation_folder"]
                st.session_state.images_folder = config["images_folder"]
                st.session_state.header_text = config.get("header_text", header_text)
                st.session_state.subheader_text = config.get("subheader_text", subheader_text)

                JSON_file = os.path.join(st.session_state.presentation_folder, "slide_data.json")

                with open(JSON_file, "r") as f:
                    st.session_state.slide_data = json.load(f)

                first_image = st.session_state.slide_data[0]["image"]
                image_path = os.path.join(st.session_state.images_folder, os.path.basename(first_image))
                if not os.path.exists(image_path):
                    st.warning(f"Image `{image_path}` not found. Please check your images folder.")
            except Exception as e:
                st.error(f"Error loading config or slide data: {e}")

# --- Print Title and Header 
st.header(f':red-background[{st.session_state.get("header_text", header_text)}]')
st.subheader(st.session_state.get("subheader_text", subheader_text), divider='red')

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
if st.session_state.slide_data:
    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 1

    selected_lang_display = st.selectbox("**Speaker notes can be translated.** Please choose the language:", options=language_names)
    target_lang = None if selected_lang_display == "🌐 Original Notes" else languages[selected_lang_display]

    num_slides = len(st.session_state.slide_data)
    lc, cc, rc = st.columns((1,3,1))
    with cc:
        st.session_state["slide_index"] = st.number_input(f'**Select slide to show** (1–{num_slides})', 1, num_slides)

    selected_slide = st.session_state.slide_data[st.session_state["slide_index"] - 1]
    image_path = os.path.join(st.session_state.images_folder, os.path.basename(selected_slide["image"]))
    st.image(image_path)

    note_text = selected_slide["notes"]
    if target_lang:
        if "translated_notes" not in selected_slide:
            selected_slide["translated_notes"] = translate_notes(note_text, target_lang)
        st.write(f"**Translated Notes** ({selected_lang_display})\n\n{selected_slide['translated_notes']}")
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
            generate_pdf(st.session_state.slide_data, st.session_state.images_folder, st.session_state.presentation_folder, target_lang, with_notes=True, text='Download pdf (with notes)')
    with pcol3:
        if st.button('Prepare pdf :orange[(**without notes**)] for download'):
            generate_pdf(st.session_state.slide_data, st.session_state.images_folder, st.session_state.presentation_folder, target_lang)

else:
    st.warning("The presentation is not loaded yet.")

'---'
st.markdown(":grey[**Presentation Management**]")

if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

with st.expander('🔄 :red[**CLICK HERE**] if you want to load another presentation'):
    st.warning("Are you sure you want to load another presentation? **If yes**, you will be able to select another presentation through a YAML-file. However, **this will remove the current presentation** from memory.")

    col1, col2, col3 = st.columns((3,4,2))
    with col2:
        if st.button("✅ Yes, load new presentation"):
            st.session_state.reset_mode = True
            st.session_state.confirm_reset = False
            st.session_state.config = None
            st.session_state.slide_data = None
            st.session_state.presentation_folder = None
            st.session_state.images_folder = None
            st.rerun()

# --- Footer ---
'---'
columns_lic = st.columns((2,1))
with columns_lic[0]:
    st.markdown(f'**SlideJet developed by** <br> {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.markdown('**Open-source license for SlideJet:**', unsafe_allow_html=True)
    try:
        st.image(Image.open("FIGS/CC_BY-SA_icon.png"))
    except FileNotFoundError:
        st.image("https://raw.githubusercontent.com/gw-inux/SlideJet/main/FIGS/CC_BY-SA_icon.png")
