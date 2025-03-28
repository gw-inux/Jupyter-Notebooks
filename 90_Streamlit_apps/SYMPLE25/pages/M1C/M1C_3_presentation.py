import os
import streamlit as st
import json
from pathlib import Path

# This is a generalized application to present Powerpoint slides and notes as slideshow through Streamlit
# You can adapt the script with header and path to a specific presentation. To do this, just replace the initial informations.

###
# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line
###

# Presettings - Here you can adjust the application to your specific application
header_text = 'Module M1C - Numerical Modeling of Flow'
subheader_text = 'System of Equations and Solvers'
presentation_folder = "90_Streamlit_apps/SYMPLE25/SLIDES/SYMPLE25_M1C_3"

#
st.title("Presentation Slides")
st.header(':red-background[Module M1C - Numerical Modeling of Flow]')
st.subheader('System of Equations and Solvers', divider='red')

st.markdown(""" 
    You can move through the slides with the _Previous_/_Next_ button. Alternatively, you can switch through the slides with the slider. Finally, you can use the toggle to switch to an vertical layout to eventually adapt the app to your device. 
        """)

# Define the default folder - the structure is fix and provided by the convert_ppt_slides.py application
JSON_file = os.path.join(presentation_folder, "slide_data.json")
images_folder = os.path.join(presentation_folder, "images")

# Initialize
slide_data = None  # Initialize

# Open files - first, check if default JSON exists
if os.path.exists(JSON_file):
    #st.success(f"Found slide data in `{JSON_file}`. Loading automatically.")
    with open(JSON_file, "r") as f:
        slide_data = json.load(f)
else:
    # Let user upload any file inside the desired folder
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
    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 1
    
    vertical = st.toggle('Toggle here for vertical layout')    
    # Display slides
    num_slides = len(slide_data)
    slide_index = st.slider("Choose the slide to show (or use the buttons below)", 1, num_slides, st.session_state["slide_index"])
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("👈 Previous", key="prev_button"):
            st.session_state["slide_index"] = max(1, st.session_state["slide_index"] - 1)

    with col3:
        if st.button("Next 👉", key="next_button"):
            st.session_state["slide_index"] = min(len(slide_data), st.session_state["slide_index"] + 1)


    if slide_index != st.session_state["slide_index"]:
        st.session_state["slide_index"] = slide_index

    selected_slide = slide_data[st.session_state["slide_index"] - 1]
    image_path = os.path.join(images_folder, os.path.basename(selected_slide["image"]))

    if vertical:
        st.image(image_path)
        st.write(f"**Notes:**\n\n{selected_slide['notes']}")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.image(image_path)
        with col2:
            st.write(f"**Notes:**\n\n{selected_slide['notes']}")
else:
    st.warning("No slide data loaded yet.")

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
    
##import os
##import streamlit as st
##import json
##from pathlib import Path
##
### Define the fixed folder where JSON and images are stored
##FIXED_FOLDER = "90_Streamlit_apps/SYMPLE25/SLIDES/SYMPLE25_M1A_1"  # Adjust this path if needed
##JSON_FILE = os.path.join(presentation_folder, "slide_data.json")
##IMAGE_FOLDER = os.path.join(FIXED_FOLDER, "images")
##
##st.title("Presentation Slides")
##st.header(':red-background[Module M1A - Review of key topics]')
##st.subheader('Storage and Flow of water', divider = 'red')
##
### Load slide data JSON directly (no checks)
##
### Check if the default JSON file exists
##st.write(os.path.exists(JSON_FILE))
##if os.path.exists(JSON_FILE):
##    st.success(f"Found slide data in `{JSON_FILE}`. Loading automatically.")
##    with open(JSON_FILE, "r") as f:
##        slide_data = json.load(f)
##else:
##    uploaded_file = st.file_uploader("Select any file inside your target folder", type=None)
##
##    if uploaded_file is not None:
##        uploaded_path = Path(uploaded_file.name)
##        FIXED_FOLDER = str(uploaded_path.parent)
##       
##        JSON_FILE = os.path.join(FIXED_FOLDER, "slide_data.json")
##        IMAGE_FOLDER = os.path.join(FIXED_FOLDER, "images")
##        
##        st.write(f"Detected folder: {FIXED_FOLDER}")
##
##with open(JSON_FILE, "r") as f:
##    slide_data = json.load(f)
##
### Store slide index in session state to prevent re-running on navigation
##if "slide_index" not in st.session_state:
##    st.session_state["slide_index"] = 1  # Start at first slide
##
### Navigation buttons
##col1, col2, col3 = st.columns([1, 3, 1])
##with col1:
##    if st.button("👈 Previous", key="prev_button"):
##        st.session_state["slide_index"] = max(1, st.session_state["slide_index"] - 1)
##
##with col3:
##    if st.button("Next 👉", key="next_button"):
##        st.session_state["slide_index"] = min(len(slide_data), st.session_state["slide_index"] + 1)
##
### Display slides
##if slide_data:
##    num_slides = len(slide_data)
##
##    # Slider for direct selection
##    slide_index = st.slider("Slide", 1, num_slides, st.session_state["slide_index"])
##
##    # Update session state if slider is used
##    if slide_index != st.session_state["slide_index"]:
##        st.session_state["slide_index"] = slide_index
##
##    # Get selected slide
##    selected_slide = slide_data[st.session_state["slide_index"] - 1]
##
##    # Construct the image path
##    image_path = os.path.join(IMAGE_FOLDER, os.path.basename(selected_slide["image"]))
##
##    # Display Slide Image and Notes
##    if st.toggle('Click here for vertical layout'):
##        st.image(image_path)
##        st.write(f"**Notes:**\n\n{selected_slide['notes']}")
##    else:
##        col1, col2 = st.columns([3, 1])
##        with col1:
##            st.image(image_path)
##        with col2:
##            st.write(f"**Notes:**\n\n{selected_slide['notes']}")


#import os
#import streamlit as st
#import json
#
## Define the fixed folder where JSON and images are stored
#FIXED_FOLDER = "90_Streamlit_apps/SYMPLE25/SLIDES/SYMPLE25_M0_INTRO"  # Adjust this path if needed
#JSON_FILE = os.path.join(FIXED_FOLDER, "slide_data.json")
#IMAGE_FOLDER = os.path.join(FIXED_FOLDER, "images")
#
#st.title("Presentation Slides")
#st.header(':blue-background[Module M0 - Introduction]')
#st.subheader('Orientation Meeting', divider = 'blue')
#
## Load slide data JSON directly (no checks)
#with open(JSON_FILE, "r") as f:
#    slide_data = json.load(f)
#
## Display slides
#if slide_data:
#    # Get total slides count
#    num_slides = len(slide_data)
#
#    # Slider for navigation
#    slide_index = st.slider("Slide", 1, num_slides, 1)
#
#    # Get selected slide
#    selected_slide = slide_data[slide_index - 1]
#
#    # Construct the image path
#    image_path = os.path.join(IMAGE_FOLDER, os.path.basename(selected_slide["image"]))
#
#    # Display Slide Image and Notes
#    if st.toggle('Click here for vertical layout'):
#        st.image(image_path)
#        st.write(f"**Notes:**\n\n{selected_slide['notes']}")
#    else:
#        col1, col2 = st.columns([3, 1])
#        with col1:
#            st.image(image_path)
#        with col2:
#            st.write(f"**Notes:**\n\n{selected_slide['notes']}")
