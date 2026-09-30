import os
import html
import streamlit as st
import json
import img2pdf
import yaml
import markdown
from PIL import Image
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
st.set_page_config(page_title="SlideJet - Present", page_icon="🚀")

# --- Default YAML path, use / ---
#DEFAULT_YAML = "example.yaml"
DEFAULT_YAML = "90_Streamlit_apps/BGR26/2026_03_03_RinnenGRM_SJconfig.yaml"

# --- Proxy ID --- This should be
# an unique ID if the app is used
# multiple times in a multipage app (string required)
app_id = "app_01"
#
###########################

# --- FUNCTIONS ---

def validate_config(config):
    # Checks if the YAML config is complete. Warns the user if essential parts are missing.
    required_keys = ["presentation_folder", "header_text", "subheader_text"]
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing required keys in YAML: {', '.join(missing)}")


def _note_to_text(value):
    """Return note/translation content as text, tolerating older/custom JSON variants."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.replace("\r\n", "\n").replace("\r", "\n").replace("\x0b", "\n")
    if isinstance(value, dict):
        for key in ("text", "translation", "value"):
            if key in value:
                return _note_to_text(value.get(key))
        return json.dumps(value, ensure_ascii=False, indent=2)
    if isinstance(value, list):
        return "\n".join(_note_to_text(item) for item in value)
    return str(value)


def _translation_is_complete(slides, code):
    """True if every non-empty source note has a stored translation for code."""
    for slide in slides:
        source = _note_to_text(slide.get("notes", "")).strip()
        translations = slide.get("translations", {}) if isinstance(slide, dict) else {}
        if not isinstance(translations, dict):
            return False
        translated = _note_to_text(translations.get(code, "")).strip()
        if source and not translated:
            return False
    return True


def normalize_loaded_slidejet_json(raw_data):
    """Read historical SlideJet JSON v1 and multilingual JSON v2.

    Returns (slides, language_metadata, source_language, json_version).
    Only complete translation languages are exposed in the presenter selector.
    """
    if isinstance(raw_data, list):
        return raw_data, [], "auto", 1

    if not isinstance(raw_data, dict) or not isinstance(raw_data.get("slides"), list):
        raise ValueError(
            "Unsupported slide_data.json. Expected the historical slide list or a multilingual object with a 'slides' list."
        )

    slides = raw_data["slides"]
    source_language = raw_data.get("source_language", "auto")
    json_version = raw_data.get("slidejet_version", 2)

    declared = raw_data.get("languages", [])
    language_by_code = {}
    if isinstance(declared, list):
        for item in declared:
            if isinstance(item, dict) and item.get("code"):
                code = str(item["code"])
                language_by_code[code] = {
                    "code": code,
                    "name": str(item.get("name", code)),
                    "native_name": str(item.get("native_name", item.get("name", code))),
                    "direction": "rtl" if str(item.get("direction", "ltr")).lower() == "rtl" else "ltr",
                }

    # Be tolerant of manually edited v2 JSON where translations exist but
    # top-level language metadata was not updated.
    translation_codes = []
    for slide in slides:
        translations = slide.get("translations", {}) if isinstance(slide, dict) else {}
        if isinstance(translations, dict):
            for code in translations:
                if code not in translation_codes:
                    translation_codes.append(code)

    declared_order = [code for code in language_by_code if code in translation_codes]
    remaining_codes = [code for code in translation_codes if code not in declared_order]
    complete_codes = [
        code for code in declared_order + remaining_codes
        if _translation_is_complete(slides, code)
    ]
    languages = []
    for code in complete_codes:
        languages.append(
            language_by_code.get(
                code,
                {"code": code, "name": code, "native_name": code, "direction": "rtl" if code in {"ar", "ur", "fa", "he"} else "ltr"},
            )
        )

    return slides, languages, source_language, json_version


def load_slidejet_json(path):
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return normalize_loaded_slidejet_json(raw_data)


def language_display(language):
    name = language.get("name", language.get("code", ""))
    native = language.get("native_name", "")
    return f"{name} — {native}" if native and native != name else name


def language_direction(code, language_lookup=None):
    if language_lookup and code in language_lookup:
        return language_lookup[code].get("direction", "ltr")
    return "rtl" if code in {"ar", "ur", "fa", "he"} else "ltr"


def render_note(text, direction="ltr"):
    """Render notes as Markdown; use a plain-text fallback instead of crashing."""
    text = _note_to_text(text)
    direction = "rtl" if str(direction).lower() == "rtl" else "ltr"
    try:
        if direction == "rtl":
            html_note = markdown.markdown(text)
            st.markdown(
                f'<div dir="rtl" style="text-align: right;">{html_note}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(text)
    except Exception:
        # A malformed/custom note must never make the whole presentation fail.
        st.text(text)


def get_stored_translation(slide, language_code):
    if not language_code:
        return _note_to_text(slide.get("notes", ""))
    translations = slide.get("translations", {}) if isinstance(slide, dict) else {}
    if not isinstance(translations, dict):
        return ""
    return _note_to_text(translations.get(language_code, ""))


def _inline_markdown_to_reportlab(text):
    """Convert SlideJet's conservative inline Markdown subset to ReportLab markup."""
    escaped = html.escape(_note_to_text(text), quote=False)
    # Bold first, then italic. SlideJet Convert emits paragraph-level markers,
    # so these deliberately conservative expressions are sufficient and avoid
    # feeding unsupported HTML tags to ReportLab Paragraph.
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", escaped)
    return escaped


def _markdown_to_reportlab_html(text):
    """Render SlideJet Markdown safely in the existing PDF-with-notes workflow.

    Supported constructs match what SlideJet Convert generates: paragraphs,
    bold/italic text, bulleted lists, numbered lists, and nested indentation.
    Unknown Markdown remains escaped plain text rather than breaking PDF output.
    """
    lines = _note_to_text(text).split("\n")
    output = []

    for raw_line in lines:
        if not raw_line.strip():
            output.append("<br/>")
            continue

        bullet_match = re.match(r"^(\s*)[-+*]\s+(.*)$", raw_line)
        numbered_match = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", raw_line)

        if bullet_match:
            indent_spaces = len(bullet_match.group(1).replace("\t", "    "))
            level = max(0, indent_spaces // 4)
            prefix = "&nbsp;" * (level * 4) + "&#8226;&nbsp;"
            output.append(prefix + _inline_markdown_to_reportlab(bullet_match.group(2)) + "<br/>")
        elif numbered_match:
            indent_spaces = len(numbered_match.group(1).replace("\t", "    "))
            level = max(0, indent_spaces // 4)
            prefix = "&nbsp;" * (level * 4) + html.escape(numbered_match.group(2)) + ".&nbsp;"
            output.append(prefix + _inline_markdown_to_reportlab(numbered_match.group(3)) + "<br/>")
        else:
            output.append(_inline_markdown_to_reportlab(raw_line) + "<br/>")

    return "".join(output)


def generate_pdf(slides, img_folder, pres_folder, trans_lan, with_notes=False, text='Download PDF'):
    imgs = [os.path.join(img_folder, os.path.basename(slide['image'])) for slide in slides]

    if with_notes:
        # Translations are read from slide_data.json; no runtime API call is made.
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

    with open(output_pdf, 'rb') as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(
        label=text,
        data=PDFbyte,
        file_name=filename,
        mime='application/pdf',
        icon=':material/download:',
        type='primary'
    )


def add_notes_with_overlay(slides, images, output_pdf, trans_lan=None, font_size=12, line_spacing=16,
                           margin_left=2*cm, margin_top=2*cm, margin_bottom=2*cm, margin_right=2*cm,
                           notes_height_ratio=0.3, text_color=colors.black, bg_color=colors.whitesmoke):
    """Generate a PDF with slide image plus stored speaker notes."""
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
        available_width = width - margin_left - margin_right
        available_height = (height - margin_top - margin_bottom) * (1 - notes_height_ratio)

        img = RLImage(img_path)
        scale_w = available_width / img.imageWidth
        scale_h = available_height / img.imageHeight
        scale_factor = min(scale_w, scale_h)
        img.drawWidth = img.imageWidth * scale_factor
        img.drawHeight = img.imageHeight * scale_factor

        img_h_space = (available_width - img.drawWidth) / 2 if available_width > img.drawWidth else 0
        if img_h_space > 0:
            elements.append(Spacer(img_h_space, 0))
        elements.append(img)
        elements.append(Spacer(1, 0.5*cm))

        original_note = str(slide.get('notes', '') or '')
        original_md = f"**Original Notes:**\n\n{original_note}"

        if trans_lan:
            trans_note = get_stored_translation(slide, trans_lan)
            trans_md = f"**Translated Notes ({trans_lan})**\n\n{trans_note}"
            combined_md = trans_md + "<br/><br/>" + original_md
        else:
            combined_md = original_md

        # Use the same conservative Markdown subset as the web presenter while
        # avoiding unsupported <ul>/<li> HTML in ReportLab Paragraph.
        html_note = _markdown_to_reportlab_html(combined_md)
        elements.append(Paragraph(html_note, notes_style))
        elements.append(PageBreak())

    doc.build(elements)


PDF_COMPLEX_SCRIPT_LANGUAGES = {"zh-Hans", "hi", "ar", "fa", "bn", "ur", "ja", "ko", "th"}

# --- USER INTERFACE

# --- Define keys ---
reset_key = f"{app_id}_reset_mode"
config_key = f"{app_id}_config"
slide_data_key = f"{app_id}_slide_data"
presentation_folder_key = f"{app_id}_presentation_folder"
images_folder_key = f"{app_id}_images_folder"
header_text_key = f"{app_id}_header_text"
subheader_text_key = f"{app_id}_subheader_text"
default_yaml_key = f"{app_id}_default_yaml"
language_metadata_key = f"{app_id}_language_metadata"
source_language_key = f"{app_id}_source_language"
json_version_key = f"{app_id}_json_version"
language_select_key = f"{app_id}_speaker_language"

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
if language_metadata_key not in st.session_state:
    st.session_state[language_metadata_key] = []
if source_language_key not in st.session_state:
    st.session_state[source_language_key] = "auto"
if json_version_key not in st.session_state:
    st.session_state[json_version_key] = 1
if presentation_folder_key not in st.session_state or st.session_state[presentation_folder_key] is None:
    st.session_state[presentation_folder_key] = presentation_folder
if images_folder_key not in st.session_state or st.session_state[images_folder_key] is None:
    st.session_state[images_folder_key] = os.path.join(st.session_state[presentation_folder_key], "images")

# --- Load slides ---
JSON_file = os.path.join(st.session_state[presentation_folder_key], "slide_data.json")

def _load_json_into_session(json_path):
    slides, language_metadata, source_language, json_version = load_slidejet_json(json_path)
    st.session_state[slide_data_key] = slides
    st.session_state[language_metadata_key] = language_metadata
    st.session_state[source_language_key] = source_language
    st.session_state[json_version_key] = json_version


if os.path.exists(JSON_file):
    try:
        # slide_data.json is authoritative. Reload it on every Streamlit rerun so
        # deployed updates are picked up without additional hash/signature state.
        _load_json_into_session(JSON_file)
    except Exception as e:
        st.error(f"Error loading slide_data.json: {e}")
        st.stop()
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
            _load_json_into_session(JSON_file)

            if st.session_state[slide_data_key]:
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
language_metadata = st.session_state[language_metadata_key]
language_lookup = {item["code"]: item for item in language_metadata if item.get("code")}
available_language_codes = list(language_lookup.keys())

st.markdown(""" 
    **About the SlideJet presentation:** _Navigate the slides using the +/- buttons or enter a slide number._
""")

# --- Show slides ---
if st.session_state[slide_data_key]:
    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 1

    original_option = "__slidejet_original__"
    language_options = [original_option] + available_language_codes
    if st.session_state.get(language_select_key) not in language_options:
        st.session_state[language_select_key] = original_option

    selected_language = st.selectbox(
        "**Speaker-note language:**",
        options=language_options,
        key=language_select_key,
        format_func=lambda code: (
            "🌐 Original Notes"
            if code == original_option
            else language_display(language_lookup.get(code, {"code": code, "name": code}))
        ),
    )
    target_lang = None if selected_language == original_option else selected_language

    num_slides = len(st.session_state[slide_data_key])
    lc, cc, rc = st.columns((1,3,1))
    with cc:
        st.session_state["slide_index"] = st.number_input(f'**Select slide to show** (1–{num_slides})', 1, num_slides)

    selected_slide = st.session_state[slide_data_key][st.session_state["slide_index"] - 1]
    image_path = os.path.join(st.session_state[images_folder_key], os.path.basename(selected_slide["image"]))
    st.image(image_path)

    note_text = _note_to_text(selected_slide.get("notes", ""))
    if target_lang:
        selected_meta = language_lookup[target_lang]
        translated = get_stored_translation(selected_slide, target_lang)
        st.markdown(f"**Translated Notes ({language_display(selected_meta)}):**")
        render_note(translated, selected_meta.get("direction", "ltr"))
        with st.expander("Show original notes"):
            render_note(
                note_text,
                language_direction(st.session_state[source_language_key], language_lookup),
            )
    else:
        st.markdown("**Notes:**")
        render_note(
            note_text,
            language_direction(st.session_state[source_language_key], language_lookup),
        )

    if target_lang in PDF_COMPLEX_SCRIPT_LANGUAGES:
        st.caption(
            "The selected language is displayed in the web presentation. The current ReportLab PDF-with-notes renderer "
            "may require a later Unicode font/shaping upgrade for this script."
        )

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
