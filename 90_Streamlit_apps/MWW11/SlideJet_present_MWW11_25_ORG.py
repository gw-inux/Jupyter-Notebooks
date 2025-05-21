import os
import streamlit as st
import json
from pathlib import Path
from PIL import Image
from deep_translator import GoogleTranslator

import img2pdf
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.annotations import Text, FreeText

def generate_pdf(with_notes=False, text='Download pdf (no notes)'):
    # Convert all files ending in .png inside a directory
    imgs = []
    for fname in os.listdir(images_folder):
        if not fname.endswith('.png'):
            continue
        path = os.path.join(images_folder, fname)
        if os.path.isdir(path):
            continue
        imgs.append(path)

    with open(presentation_folder + '/presentation.pdf','wb') as f:
        f.write(img2pdf.convert(imgs))

    if with_notes:
        scale_pdf(presentation_folder + '/presentation.pdf', len(slide_data))
        add_notes(presentation_folder + '/presentation.pdf', slide_data)

    # Open file in memory to be able to save with download button
    with open(presentation_folder + '/presentation.pdf', 'rb') as pdf_file:
        PDFbyte = pdf_file.read()

    # Add download button
    with pcol3:
        # Save as presentation.pdf
        st.download_button(
            label=text,
            data=PDFbyte,
            file_name='presentation.pdf',
            mime='application/octet-stream',
            icon=':material/download:',
            type='primary'
        )

def add_notes(pdf_path, slide_data):
    # Fill the writer with the the already generated pdf
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    
    for i in range(len(slide_data)):
        #annotation = Text(
        #    text=slide_data[i]['notes'],
        #    rect=(20, 50, 20, 50) # rect – array of four integers [xLL, yLL, xUR, yUR] specifying the clickable rectangular area
        #    )

        # Create the annotation and add it
        annotation = FreeText(
            text=slide_data[i]['notes'],
            rect=(reader.pages[i].mediabox.width * 0.76, 0, reader.pages[i].mediabox.width, reader.pages[i].mediabox.height),  # rect – array of four integers [xLL, yLL, xUR, yUR] specifying the clickable rectangular area
            font="Arial",
            bold=True,
            italic=True,
            font_size="20pt",
            font_color="#000000",
            border_color="#000000",
            background_color="#FFFFFF",
        )

        # Set annotation flags to 4 for printable annotations.
        # See "AnnotationFlag" for other options, e.g. hidden etc.
        annotation.flags = 4

        writer.add_annotation(page_number=i, annotation=annotation)

    # Write the annotated file to disk
    with open(pdf_path, 'wb') as fp:
        writer.write(fp)   

def scale_pdf(pdf_path, nr_pages):
    # Read the input
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for i in range(nr_pages):
        page = reader.pages[i]

        # Scale
        # page.scale_by(0.5)
        op = Transformation().scale(sx=0.75, sy=0.75)
        page.add_transformation(op)

        # Write the result to a file        
        writer.add_page(page)
    with open(pdf_path, 'wb')as fp:
        writer.write(fp)

@st.cache_data(show_spinner=False)
def translate_notes(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"[Translation failed: {e}]"

# This is a generalized application to present PowerPoint slides and notes as slideshow through Streamlit
# You can adapt the script with header and path to a specific presentation. To do this, just replace the initial informations.

# --- Header content Copyright ---
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
   #"Colleague Name": [2],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
   #2: "Second Institution / Organization"
}
author_list = [f"{name}{''.join(f'<sup>{i}</sup>' for i in idxs)}" for name, idxs in authors.items()]
institution_text = " | ".join([f"<sup>{i}</sup> {inst}" for i, inst in institutions.items()])

### SlideJet - Present

# !! IF THE PRESENTATION IS PART OF A MULTIPAGE APP - THIS NEEDS TO BE REMOVED !!
# --- MUST be first: layout setup ---
if "layout_choice" in st.session_state:
    st.session_state.layout_choice_SJ = st.session_state.layout_choice  # use app-wide layout
elif "layout_choice_SJ" not in st.session_state:
    st.session_state.layout_choice_SJ = "centered"  # fallback

st.set_page_config(
    page_title="SlideJet - Present",
    page_icon="🚀",
    layout=st.session_state.layout_choice_SJ
    )
# !! REMOVE UNTIL HERE !!
    
################
# ADAPT HERE ###
################

# Folder to your presentation

presentation_folder = "90_Streamlit_apps/MWW11/slides/Fallstudien25_FS0_ORG"

# Presettings - Here you can adjust the application to your specific application

header_text = 'MWW11 - Fallstudien der Grundwasserbewirtschaftung'
subheader_text = 'Einführung, Organisation, Überblick'

# --- Streamlit App Content ---
st.title("Presentation Slides")
st.header(f':red-background[{header_text}]')
st.subheader(subheader_text, divider='red')

st.markdown(""" 
    You can move through the slides with the **+/- button**. Alternatively, you can switch directly to a slide by inserting the slide number. There is an optin to translate the speaker notes of the slides to your favorite language. If you translate the speaker notes, the original text is still available below the translation. Finally, you can use the toggle to switch to a vertical layout to adapt the appearance of the application to your device. 
        """)

# Define the default folder - the structure is fix and provided by the convert_ppt_slides.py application
JSON_file = os.path.join(presentation_folder, "slide_data.json")
images_folder = os.path.join(presentation_folder, "images")

# Language selection
# --- Language options with flags ---
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

# Set 'None' as the default for original, assuming no fixed source language
language_names = ["🌐 Original Notes"] + list(languages.keys())

# Initialize
slide_data = None  # Initialize

# Open files - first, check if default JSON exists
if os.path.exists(JSON_file):
    #st.success(f"Found slide data in `{JSON_file}`. Loading automatically.")
    with open(JSON_file, "r") as f:
        slide_data = json.load(f)
else:
    # Upload any file inside the desired folder
    uploaded_file = st.file_uploader("Select any file inside your target folder", type=None)

    if uploaded_file is not None:
        # Get folder path from uploaded file (only possible locally)
        uploaded_path = Path(uploaded_file.name)
        presentation_folder = str(uploaded_path.parent)

        JSON_file = os.path.join(presentation_folder, "slide_data.json")
        images_folder = os.path.join(presentation_folder, "images")

        st.write(f"Detected folder: `{presentation_folder}`")
        st.write(JSON_file)

        # Try to load JSON from the newly detected folder
        if os.path.exists(JSON_file):
            with open(JSON_file, "r") as f:
                slide_data = json.load(f)
        else:
            st.error(f"No `slide_data.json` found in `{presentation_folder}`.")

# Only continue if slide data was loaded
if slide_data:
    
    # Start with the first slide
    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 1

    num_slides = len(slide_data)
    
    # Layout and Language selection    
    lc, cc, rc = st.columns((1,1,1))
    with lc:
        # --- Layout toggle switch ---
        # !! IF THE PRESENTATION IS PART OF A MULTIPAGE APP - THIS NEEDS TO BE REMOVED !!
        wide_mode = st.toggle("Use wide layout", value=(st.session_state.layout_choice_SJ == "wide"))
        new_layout = "wide" if wide_mode else "centered"
        
        if new_layout != st.session_state.layout_choice_SJ:
            st.session_state.layout_choice_SJ = new_layout
            st.rerun()
        # !! REMOVE UNTIL HERE !!
        vertical = st.toggle('Toggle to show notes below slides')
    with cc:
        selected_lang_display = st.selectbox("Language for speaker notes", options=language_names)
    with rc:
        st.write('Number of slides in the presentation: %3i' %num_slides)
        
    # None = no translation
    target_lang = None if selected_lang_display == "🌐 Original Notes" else languages[selected_lang_display]
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
            st.session_state["slide_index"] = st.number_input('Slide number to show', 1, num_slides)

    # Display slides
    selected_slide = slide_data[st.session_state["slide_index"] - 1]
    image_path = os.path.join(images_folder, os.path.basename(selected_slide["image"]))

    note_text = selected_slide["notes"]

    if target_lang:
        translated_text = translate_notes(note_text, target_lang)

    if vertical:
        st.image(image_path)
        if target_lang:
            st.write(f"**Translated Notes ({selected_lang_display})**\n\n{translated_text}")
            with st.expander("Show original notes"):
                st.write(note_text)
        else:
            st.write(f"**Notes:**\n\n{note_text}")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.image(image_path)
        with col2:
            if target_lang:
                st.write(f"**Translated Notes ({selected_lang_display})**\n\n{translated_text}")
                with st.expander("Show original notes"):
                    st.write(note_text)
            else:
                st.write(f"**Notes:**\n\n{note_text}")

    ### Download presentation as pdf ###
    # Navigation buttons
    pcol1, pcol2, pcol3 = st.columns([3, 1, 3])
    with pcol1:    
        if st.button('Prepare pdf (no notes) for download'):
            generate_pdf()
        
        if st.button('Prepare pdf (with notes) for download'):
            generate_pdf(True, 'Download pdf (with notes)')

else:
    st.warning("No slide data loaded yet.")

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    try:
        st.image(Image.open("FIGS/CC_BY-SA_icon.png"))
    except FileNotFoundError:
        st.image("https://raw.githubusercontent.com/gw-inux/SlideJet/main/FIGS/CC_BY-SA_icon.png")
