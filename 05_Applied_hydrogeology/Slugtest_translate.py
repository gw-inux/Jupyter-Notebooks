import numpy as np
import pandas as pd
import streamlit as st
import io
import matplotlib.pyplot as plt
import re
from deep_translator import GoogleTranslator

### 1ST PART - Translation

def translate_text(text, target_language):
    """ Translates markdown and HTML text while preserving formatting. """

    if target_language == ORIGINAL_LANGUAGE_CODE:
        return text  # No translation needed

    translator = GoogleTranslator(source="auto", target=target_language)

    # Step 1: Preserve HTML content separately
    def translate_html(match):
        """ Translates only the inner text of HTML tags, preserving structure. """
        opening_tag, inner_text, closing_tag = match.groups()
        translated_inner_text = translator.translate(inner_text)  # Translate only inner text
        return f"{opening_tag}{translated_inner_text}{closing_tag}"

    html_pattern = r"(<[^>]+>)(.*?)(</[^>]+>)"
    text = re.sub(html_pattern, translate_html, text)

    # Step 2: Add spaces inside **bold** and *italic* before translation
    text_with_spaces = re.sub(r"(\*\*|\*)(\S.*?\S)(\*\*|\*)", r"\1 \2 \3", text)

    # Step 3: Split text into lines to preserve Markdown structure
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

    # Step 4: Remove spaces inside **bold** and *italic* after translation
    final_text = re.sub(r"(\*\*|\*) (.*?) (\*\*|\*)", r"\1\2\3", translated_text)

    return final_text

# Define the original language of the text (set by the app author)
ORIGINAL_LANGUAGE_CODE = "en"

# Dictionary with languages and their corresponding flags (Unicode flag emojis); eventually add more languages
languages = {
    "English 🇬🇧": "en",
    "Spanish 🇪🇸": "es",
    "French 🇫🇷": "fr",
    "German 🇩🇪": "de",
    "Italian 🇮🇹": "it",
    "Swedish 🇸🇪": "sv",
    "Catalan 🇦🇩": "ca",
    "Chinese (Simplified) 🇨🇳": "zh-CN",
    "Hindi 🇮🇳": "hi",
    "Arabic 🇸🇦": "ar",
    "Bengali 🇧🇩": "bn",
    "Portuguese 🇵🇹": "pt",
    "Russian 🇷🇺": "ru",
    "Japanese 🇯🇵": "ja",
    "Punjabi 🇵🇰": "pa",
    "Korean 🇰🇷": "ko",
    "Turkish 🇹🇷": "tr"
}

# Language selection
columns1 = st.columns((1, 1, 1), gap="large")
with columns1[1]:
    target_lang_name = st.selectbox("🌎 Choose the target language", list(languages.keys()))
target_lang = languages[target_lang_name]

# TEXTS to translate
sections = {

    "part_01": """
Slug tests are quick and cost-effective field methods used to determine the hydraulic conductivity (K) of an aquifer. They involve a sudden change in water level within a well (either by adding or removing a known volume of water, or inserting/removing a slug) and measuring the subsequent water level recovery over time, see subsequent figure.
""",

    "part_02": """
            These tests are ideal for:
- Assessing aquifer properties in low-permeability formations.
- Situations where pumping tests are not feasible due to time or space constraints.
- Monitoring wells where minimal disturbance to the aquifer is desired.

Types of Slug Tests:
- Rising-head test: Water level rises after removal of a slug.
- Falling-head test: Water level falls after adding water or a slug.

**Why use slug tests?** They are fast, inexpensive, and suitable for small-scale investigations, making them a standard tool in hydrogeological site assessments.

The **Bouwer and Rice (1976) method** is a widely used approach to evaluate **slug test data**, especially in **partially penetrating wells** in **unconfined aquifers**. It relates the **water level recovery** to the **hydraulic conductivity** of the aquifer, accounting for well geometry and screen penetration.
""",

    "part_03": """
The hydraulic conductivity $K$ is calculated using:
""",

    "part_04": """
**Where:**
- $K$: Hydraulic conductivity (m/s)  
- $r_c$: Radius of the well casing (m) 
- $r_w$: Radius of the well screen (m)  
- $R_e$: Effective radius of influence (m)   
- $L$: Length of the well screen intersecting the aquifer (m)
- $t$: Elapsed time since the slug event (s)  
- $h_0$: Initial head displacement (m) 
- $h_t$: Head displacement at time $t$ (m)

**Estimating the Effective Radius $R_e$**
The **effective radius** $R_e$ depends on the well penetration, which depends on the thickness and conductivity of the the well pack, the fraction of the screen that is below the water table, anisotropy and skin effects:  
- **Fully penetrating well:**
""",

    "part_05": """
*(where $D$ is the saturated aquifer thickness)*  
            
- **Partially penetrating well:**
""",

    "part_06": """              
            - **For simplicity**, we use in this app:
            """,
            
    "part_07": """    
            Below you can choose the data for evaluation. You can upload your own data as *.CSV file with time (in seconds) and hydraulic head (in meters) separated by commas. Alternatively, you can choose preloaded data. 
            
            Once the data are loaded, you can modify the time offset and fit the hydraulic conductivity to the measured data.
           """,
    "fig_caption": "Schematic representation of a slug test where a slug of water is added to a well. Figure modified from Bouwer and Rice (1976).",
    "video_caption": "Video: Slugtest performed at the Varnum site (Sweden) by adding approximately 4 liter to a groundwater observation well.",
    "expander1": "**Click here to read more about the theory**",
    "header": "Evaluating slug tests in unconfined aquifers with the Bouwer & Rice method",
    "subheader1": "Introduction and Motivation - Multilingual version",
    "subheader2": "The Theory behind the Bouwer & Rice Method for Unconfined Aquifers",
    "subheader3": "Computation and Interactive Plot",
    "button1": """<div style="text-align: center; font-weight: bold; font-size: 125%"> What data should be used? </div>""",
    "selectbox": "**Please select the dataset**"
}

### TRANSLATION PART
# Initialize session state only once with None
st.session_state.setdefault("translated_sections", {key: None for key in sections.keys()})
st.session_state.setdefault("current_lang", ORIGINAL_LANGUAGE_CODE)  # Default is English

# Ensure placeholders are initialized with the original text if None
for key in sections.keys():
    if st.session_state["translated_sections"][key] is None:
        st.session_state["translated_sections"][key] = sections[key]  # Fallback to English

# Translate only when the language actually changes
if st.session_state["current_lang"] != target_lang:
    new_sections = {}

    # Translate Sections
    for key in sections:
        translated_text = translate_text(sections[key], target_lang)
        new_sections[key] = translated_text if translated_text else sections[key]  # Keep English if translation fails

    # Update translations in session state after all translations are done
    st.session_state["translated_sections"] = new_sections
    st.session_state["current_lang"] = target_lang  # ✅ Update stored language


# 2nd Part: Texts and explanations

st.title('Slugtest evaluation 📉')

# Two empty container to place the headings
st.header(st.session_state["translated_sections"].get("header", sections["header"]))
st.subheader(st.session_state["translated_sections"].get("subheader1", sections["subheader1"]))

# SECTION1 / TRANSLATION
part01_placeholder = st.empty()  # Section placeholder
           
lc0, rc0 = st.columns((1,1.3),gap = 'large')
with lc0:
    st.image('05_Applied_hydrogeology/FIGS/slug_unconfined.png', caption=st.session_state["translated_sections"].get("fig_caption", sections["fig_caption"]))

with rc0:
    st.video('https://youtu.be/GTq72oB0qZo')
    st.write(f'_{st.session_state["translated_sections"].get("video_caption", sections["video_caption"])}_')

st.subheader(st.session_state["translated_sections"].get("subheader2", sections["subheader2"]))

# Section 02 / Translation
part02_placeholder = st.empty()  # Section placeholder

with st.expander(st.session_state["translated_sections"].get("expander1", sections["expander1"])):
 
    # Translation of section 3
    part03_placeholder = st.empty()  # Section placeholder

    st.latex(r'''K = \frac{r_c^2 \ln\left(\frac{R_e}{r_w}\right)}{2L} \cdot \frac{1}{t} \cdot \ln\left(\frac{h_t}{h_0}\right)''')
 
    # Translation of section 4
    part04_placeholder = st.empty()  # Section placeholder        
    
    st.latex(r'''R_e = \frac{D}{2}''')
            
    # Translation of section 5
    part05_placeholder = st.empty()  # Section placeholder 
    
    st.latex(r'''R_e = 1.1L + r_w''')     
    
    # Translation of section 6
    part06_placeholder = st.empty()  # Section placeholder 
            
    st.latex(r'''R_e = L''')
    
st.subheader(st.session_state["translated_sections"].get("subheader3", sections["subheader3"]))
    
# Translation of section 7
part07_placeholder = st.empty()  # Section placeholder

# **Ensure content placeholders do not disappear**
part01_placeholder.markdown(st.session_state["translated_sections"].get("part_01", sections["part_01"]))
part02_placeholder.markdown(st.session_state["translated_sections"].get("part_02", sections["part_02"]))
part03_placeholder.markdown(st.session_state["translated_sections"].get("part_03", sections["part_03"]))
part04_placeholder.markdown(st.session_state["translated_sections"].get("part_04", sections["part_04"]))
part05_placeholder.markdown(st.session_state["translated_sections"].get("part_05", sections["part_05"]))
part06_placeholder.markdown(st.session_state["translated_sections"].get("part_06", sections["part_06"]))
part07_placeholder.markdown(st.session_state["translated_sections"].get("part_07", sections["part_07"]))

# 3rd part COMPUTATION HERE

# Available Data / Choose data
# Select data
columns = st.columns((1,4,1), gap = 'large')
with columns[1]:
    st.markdown(st.session_state["translated_sections"].get("button1", sections["button1"]), unsafe_allow_html=True) 
           
    datasource = st.selectbox(st.session_state["translated_sections"].get("selectbox", sections["selectbox"]),
    ("Data from random properties with added noise", "Load your own CSV dataset", "Varnum (SWE) 2018 - R4", "Viterbo (ITA) 2024"), key = 'Data')
with columns[1]:
    if(st.session_state.Data =="Load your own CSV dataset"):
        slugsize = st.number_input("Slug size in cm³ (1 liter = 1000 cm³)", value = 700,step=1)
        h_static = st.number_input("Static water level (hydraulic head) in m", value = 0., step=0.01)
    
if (st.session_state.Data == "Varnum (SWE) 2018 - R4"):
    slugsize = 700
    h_static = 0
    rc_ini = 0.03
    rw_ini = 0.07
    L_ini = 2.
    # Data and parameter from Varnum (SWE) 2018 - R4
    m_time = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287] # time in minutes
    
    m_head = [0.00000,0.01131,0.09161,0.14633,0.17548,0.18678,0.19570,0.20284,0.20879,0.21057,0.21236,0.21414,0.21414,0.21355,0.21355,0.21355,0.21355,0.21355,0.21355,0.21355,0.21176,0.21176,0.21176,0.21057,0.21057,0.20820,0.20879,0.20700,0.20463,0.20522,0.20522,0.20106,0.20106,0.19927,0.19749,0.19749,0.19570,0.19570,0.19392,0.19392,0.19213,0.18857,0.18976,0.18797,0.18619,0.18619,0.18441,0.18262,0.18084,0.17905,0.17905,0.17727,0.17548,0.17370,0.17191,0.17191,0.17013,0.16834,0.16834,0.16596,0.16417,0.16061,0.16239,0.16061,0.15882,0.15882,0.15704,0.15525,0.15347,0.15525,0.15168,0.15168,0.14990,0.14811,0.14633,0.14633,0.14098,0.14276,0.14038,0.13919,0.13741,0.13562,0.13562,0.13562,0.13384,0.13146,0.13146,0.12968,0.12789,0.12789,0.12611,0.12611,0.12254,0.12254,0.12075,0.12075,0.12075,0.11897,0.11719,0.11540,0.11540,0.11362,0.11362,0.11183,0.11005,0.11005,0.10826,0.10826,0.10589,0.10589,0.10589,0.10410,0.10232,0.10410,0.10232,0.10053,0.09875,0.09875,0.09696,0.09696,0.09518,0.09518,0.09518,0.09340,0.09340,0.09161,0.09101,0.09101,0.08923,0.08923,0.08744,0.08744,0.08566,0.08566,0.08387,0.08387,0.08209,0.08209,0.08209,0.08030,0.08030,0.07852,0.07852,0.07673,0.07673,0.07673,0.07495,0.07495,0.07316,0.07316,0.07316,0.07316,0.07138,0.07138,0.06960,0.06960,0.06960,0.06960,0.06781,0.06781,0.06544,0.06544,0.06365,0.06365,0.06365,0.06365,0.06365,0.06187,0.06187,0.06187,0.06008,0.05830,0.05830,0.05651,0.05830,0.05651,0.05651,0.05651,0.05473,0.05294,0.05473,0.05473,0.05294,0.05294,0.05294,0.05294,0.05116,0.05116,0.04937,0.05116,0.05116,0.04937,0.04937,0.04937,0.04759,0.04937,0.04581,0.04581,0.04759,0.04759,0.04759,0.04581,0.04581,0.04581,0.04581,0.04402,0.04402,0.04402,0.04402,0.04402,0.04224,0.04224,0.04165,0.04224,0.04224,0.04224,0.04224,0.04045,0.04045,0.04045,0.03867,0.03867,0.03867,0.03867,0.03867,0.03688,0.03688,0.03451,0.03688,0.03451,0.03451,0.03451,0.03451,0.03451,0.03272,0.03272,0.03272,0.03451,0.03272,0.03272,0.03094,0.03094,0.03272,0.03094,0.03094,0.03094,0.02915,0.03094,0.02915,0.02915,0.02915,0.02915,0.02915,0.02915,0.02737,0.02737,0.02737,0.02737,0.02558,0.02558,0.02558,0.02558,0.02558,0.02558,0.02558,0.02558,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02202,0.02202,0.02202,0.02202,0.02202,0.02202,0.02202,0.02202,0.02023,0.02023,0.02023,0.02023,0.02023]
elif(st.session_state.Data =="Viterbo (ITA) 2024"):
    slugsize = 1000
    h_static = 26.49
    rc_ini = 0.05
    rw_ini = 0.07
    L_ini = 15.
    # Data and parameter from Viterbo (ITA) 2024
    m_time = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185] # time in minutes  
    m_head = [26.4868,26.4849,26.4831,26.4831,26.4849,26.4913,26.5051,26.5308,26.5473,26.5647,26.5775,26.5876,26.5968,26.6004,26.6032,26.6032,26.6004,26.6004,26.5949,26.5913,26.5848,26.5793,26.5757,26.5693,26.5647,26.5619,26.5564,26.5555,26.5528,26.5473,26.5473,26.5454,26.5408,26.5427,26.5408,26.5399,26.539,26.539,26.5363,26.5344,26.5363,26.5335,26.5344,26.5326,26.5298,26.528,26.5298,26.5271,26.528,26.5271,26.5271,26.5234,26.5234,26.5207,26.5207,26.5207,26.5198,26.517,26.5179,26.5143,26.5152,26.5143,26.5133,26.5133,26.5115,26.5106,26.5106,26.5088,26.5088,26.5078,26.5088,26.5078,26.5078,26.5051,26.506,26.5051,26.5051,26.5051,26.5051,26.5023,26.5042,26.5023,26.5051,26.5042,26.5023,26.5023,26.5023,26.5014,26.5014,26.5014,26.5014,26.5014,26.5014,26.4996,26.4996,26.5014,26.4996,26.4978,26.4978,26.4987,26.4996,26.4987,26.4987,26.4987,26.4987,26.4987,26.4987,26.4978,26.4987,26.4987,26.4987,26.4978,26.4987,26.4978,26.4987,26.4978,26.4978,26.4978,26.4987,26.4978,26.4978,26.4987,26.4959,26.4959,26.495,26.4959,26.4959,26.495,26.4959,26.495,26.4959,26.4932,26.495,26.495,26.495,26.4932,26.495,26.4959,26.4932,26.4959,26.4932,26.495,26.4932,26.495,26.4932,26.4932,26.495,26.4923,26.4923,26.4932,26.4923,26.4932,26.4932,26.4923,26.495,26.495,26.4923,26.495,26.4923,26.495,26.495,26.4932,26.4932,26.495,26.4932,26.4932,26.4932,26.4932,26.495,26.4923,26.4913,26.4932,26.4932,26.4932,26.4932,26.4932,26.4923,26.4923,26.4923,26.4923,26.4923,26.4932,26.4932,26.4932,26.4932,26.4932]
elif(st.session_state.Data =="Load your own CSV dataset"):
    # LOAD CSV / Initialize
    m_time = []
    m_head = []
    rc_ini = 0.025
    rw_ini = 0.07
    L_ini = 2.
    uploaded_file = st.file_uploader("Choose a CSV file for evaluation (time in seconds / normalized heads in meters)")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        m_time = list(df.iloc[:,0].values)
        m_head = list(df.iloc[:,1].values)
    st.write('Overview about loaded data', m_head)
elif(st.session_state.Data =="Data from random properties with added noise"):
    # Generate Random Data
    slugsize = 700
    h_static = 0
    rc_ini = 0.03
    rw_ini = 0.07
    L_ini = 2.
    # Random data
    m_time = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300] # time in minutes
    # Empty heads file - computed later
    m_head = []
    K_random = 1.23E-6*np.random.randint(1, 10000)/100
    st.session_state.K_random = K_random
    F_random = 2 * np.pi * L_ini/np.log(L_ini/rw_ini)
    prq_random = np.pi * rc_ini**2 
    t_off_random = np.random.randint(1, 15)
    m_head_random = [np.exp(-F_random/prq_random*K_random*t) for t in m_time]
    
    
    # Compute measured data with noise
    # The noise is computed at the beginning with the max noise (as percentage) and subsequently, the noise is normalized by a strenght (ranging from 1.0 to 0.0 -> full noise to no noise)
    max_noise = 50 # max noise - should not be smaller than 20 - see input slider 
    # Compute ranom noise
    m_noise = [np.random.randint((100-max_noise), (100+max_noise))/100 for i in m_time]
    
    st.session_state.max_noise = max_noise
    st.session_state.m_noise = m_noise
    st.session_state.m_head_random = m_head_random

st.session_state.m_time = m_time
st.session_state.m_head = m_head
"---"
# Computation

def compute_statistics(measured, computed):
    # Calculate the number of values
    n = len(measured)

    # Initialize a variable to store the sum of squared differences
    total_me = 0
    total_mae = 0
    total_rmse = 0

    # Loop through each value
    for i in range(n): # Add the squared difference to the total
        total_me   += (computed[i] - measured[i])
        total_mae  += (abs(computed[i] - measured[i]))
        total_rmse += (computed[i] - measured[i])**2

    # Calculate the me, mae, mean squared error
    me = total_me / n
    mae = total_mae / n
    meanSquaredError = total_rmse / n

    # Raise the mean squared error to the power of 0.5 
    rmse = (meanSquaredError) ** (1/2)
    return me, mae, rmse

# Everything inside the fragment is re-computed with every input change
@st.fragment
def slug():
    # Fixed values
    tmax = 300

    # User defined values
    # Define the minimum and maximum for the logarithmic scale
    log_min = -6.0 # Corresponds to 10^-7 = 0.0000001
    log_max =  -2.0  # Corresponds to 10^0 = 1

    lc1, rc1 = st.columns((1,1))
    with lc1:
        if(st.session_state.Data =="Load your own CSV dataset"):
            with st.expander('**Provide well parameter**'):
                rc = st.number_input("well casing radius", value = rc_ini,step=.0001, format="%.4f")
                rw = st.number_input("well screen radius", value = rw_ini,step=.001, format="%.3f")
                L  = st.number_input("Lenght of the well screen", value = L_ini,step=.1, format="%.1f")
        else:
            # Well parameter are fix for random data and provided data sets
            rc = rc_ini
            rw = rw_ini
            L  = L_ini
            st.markdown("""
            The plotted data are based on
            - $r_c$ = 0.03 m
            - $r_w$ = 0.07 m
            - $L$ = 2.0 m
            """)
        if(st.session_state.Data =="Data from random properties with added noise"):
            def_noise = st.toggle("**Define the noise** in the measured data")
            if def_noise:
                noise_slider = st.slider('Relative random error, percent', 0, st.session_state.max_noise, 20, 1)
                noise_strength = noise_slider/st.session_state.max_noise
            else:
                noise_strength = 20/st.session_state.max_noise
            # Compute heads with noise - Multiply each value to add noise and normalize the noise according to the noise strength
            m_head_noise = [head * (1 + noise_strength * (noise - 1 ))  for head, noise in zip(st.session_state.m_head_random, st.session_state.m_noise)]
            # Create a DataFrame
            df = pd.DataFrame({'Time': st.session_state.m_time, 'Hydraulic Head': m_head_noise})
            output_csv = df.to_csv(index=False).encode('utf-8')
            st.download_button('Download Random data as CSV', output_csv, file_name="random_data_slug.csv", mime='text/csv')
        scatter = st.toggle('**Show scatter plot**')
    
    with rc1:
        # Log slider with input and print
        with st.expander('**Scale of plot and time offset**'):
            t_off = st.slider('**Time offset $t_{off}$** in s', 0, 60, 0, 1)
            x_plot = st.number_input('**Max x-value in plot** in s (up to 21600)', 60, 21600, 300, 30)
        container = st.container()
        K_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min,log_max,-3.0,0.01,format="%4.2f" )
        K = 10 ** K_slider_value
        container.write("**Hydraulic conductivity in m/s:** %5.2e" %K)
    
    columns = st.columns((1,4,1), gap = 'large')
    with columns[1]:
        if(st.session_state.Data =="Data from random properties with added noise"):
            show_truth = st.toggle(":rainbow[How accurate are the parameter value estimates?]")
    
    # Calculation
    # For random data, the initial head increase due to the slug is randomly computed
    if(st.session_state.Data =="Data from random properties with added noise"):
        H0 = st.session_state.m_head_random[0]
    else:
        H0 = 0.01*slugsize/np.pi/(rc*100)**2
    F = 2 * np.pi * L/np.log(L/rw)
    prq = np.pi * rc**2
    t = np.arange(0, tmax, 1)

    # Generate the time for plotting - with offset
    t_plot=[]
    for i in t:
        t_plot.append(i+t_off)
    
    # Generate the normalized heads for the plot
    h_norm = []
    if(st.session_state.Data =="Data from random properties with added noise"):
        for i in m_head_noise:
            h_norm.append((i-h_static)/H0)
    else:
        for i in st.session_state.m_head:
            h_norm.append((i-h_static)/H0)
    
    # Compute the function 
    exp_decay = np.exp(-F/prq*K*t)
    
    # Compute point data for scatter plot 
    scatter_computed = [0 if i < t_off else np.exp(-F/prq*K*(i-t_off)) for i in st.session_state.m_time]
    
    max_s = 1
    # Plot figure
    fig = plt.figure(figsize=(12,14))
    ax = fig.add_subplot(2,1,1)
    # Info-Box
    props   = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    out_txt = '\n'.join((       
                         r'$K$ (m/s) = %10.2E' % (K, ),
                         r'$t_{off}$ (s) = %4i' % (t_off, )))
    ax.plot(t_plot,exp_decay, color='magenta', label='computed')
    plt.plot(st.session_state.m_time,h_norm, 'bo', mfc='none', label='measured')
    plt.axis([0,x_plot,0,1])

    plt.xlabel(r'time t in (s)', fontsize=14)
    plt.ylabel(r'H/Ho', fontsize=14)
    plt.title('Slugtest evaluation (positive slug)', fontsize=16)
    plt.text(0.97, 0.15,out_txt, horizontalalignment='right', transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    plt.legend(fontsize=14)

    if scatter:
        x45 = [0,200]
        y45 = [0,200]
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x45,y45, '--')
        ax.plot(h_norm, scatter_computed,  'ro', label=r'measured')
        me, mae, rmse = compute_statistics(h_norm, scatter_computed)
        plt.title('Scatter plot', fontsize=16)
        plt.xlabel(r'Measured s in m', fontsize=14)
        plt.ylabel(r'Computed s in m', fontsize=14)
        plt.ylim(0, max_s)
        plt.xlim(0, max_s)
        out_txt = '\n'.join((
                             r'$ME = %.3f$ m' % (me, ),
                             r'$MAE = %.3f$ m' % (mae, ),
                             r'$RMSE = %.3f$ m' % (rmse, ))) 
        plt.text(0.97*max_s, 0.05*max_s, out_txt, horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='wheat'), fontsize=14)
    
    st.pyplot(fig=fig)
    
    # Safe the figure
    # Convert figure to a BytesIO object
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)  # Reset buffer position
    
    columns5 = st.columns((1,1,1), gap = 'large')
    with columns5[1]:
        # Add download button
        st.download_button(
            label=":green[**Download**] **Figure**",
            data=img_buffer,
            file_name="Slug_BouwerRice_Evalutation.png",
            mime="image/png"
)
    
    if(st.session_state.Data =="Data from random properties with added noise"):
        if show_truth:
            st.write("**'True' hydraulic conductivity _K_ = % 5.2e"% st.session_state.K_random, " m²/s**")
            st.write("**log of 'True' hydraulic conductivity = % 4.2f**"% np.log10(st.session_state.K_random))
            #st.write("_Your Fit Accuracy Ratio is:  %5.2f_" %(K/st.session_state.K_random*100), " %")
            st.markdown("""
            The result of your fitting is presented as the **:red[Relative Absolute Error] (RAE)** 
            """)
            st.latex(r'''\text{RAE} = \frac{|K_{fitted} - K_{true}|}{K_{true}}''')
            st.write("**RAE:  %5.2f**" %((K-st.session_state.K_random)/st.session_state.K_random*100), " %")
    else:
        st.write("Slugsize = %5.2f_"% slugsize, ' cm³')
        st.write("Initial water level $H_0$ = %5.3f"% H0, ' m')

slug()

columns6 = st.columns((1,1,1), gap = 'large')
with columns6[1]:
    if(st.session_state.Data =="Data from random properties with added noise"):
        st.button('**Regenerate data**')

with st.expander('**Click here for some references**'):
    st.markdown("""    
                Bouwer, H., & Rice, R. C. (1976). A slug test for determining hydraulic conductivity of unconfined aquifers with completely or partially penetrating wells. [Water Resources Research, 12(3), 423-428.](https://doi.org/10.1029/WR012i003p00423)
            
                [Kruseman, G.P., de Ridder, N.A., & Verweij, J.M.,  1991.](https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/) Analysis and Evaluation of Pumping Test Data, International Institute for Land Reclamation and Improvement, Wageningen, The Netherlands, 377 pages.
                
                The  interactive app is based on an idea from Prof. Masaki Hayashi.
                """)