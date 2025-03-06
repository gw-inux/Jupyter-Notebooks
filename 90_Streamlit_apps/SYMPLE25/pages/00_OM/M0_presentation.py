import os
import streamlit as st
import json

# Define the fixed folder where JSON and images are stored
FIXED_FOLDER = "90_Streamlit_apps/SYMPLE25/SLIDES/SYMPLE25_M0_INTRO"  # Adjust this path if needed
JSON_FILE = os.path.join(FIXED_FOLDER, "slide_data.json")
IMAGE_FOLDER = os.path.join(FIXED_FOLDER, "images")

st.title("Presentation Slides")
st.header(':blue-background[Module M0 - Introduction]')
st.subheader('Orientation Meeting', divider = 'blue')

# Load slide data JSON directly (no checks)
with open(JSON_FILE, "r") as f:
    slide_data = json.load(f)

# Store slide index in session state to prevent re-running on navigation
if "slide_index" not in st.session_state:
    st.session_state["slide_index"] = 1  # Start at first slide

# Navigation buttons
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("⬅ Previous", key="prev_button"):
        st.session_state["slide_index"] = max(1, st.session_state["slide_index"] - 1)

with col3:
    if st.button("Next ➡", key="next_button"):
        st.session_state["slide_index"] = min(len(slide_data), st.session_state["slide_index"] + 1)

# Display slides
if slide_data:
    num_slides = len(slide_data)

    # Slider for direct selection
    slide_index = st.slider("Slide", 1, num_slides, st.session_state["slide_index"])

    # Update session state if slider is used
    if slide_index != st.session_state["slide_index"]:
        st.session_state["slide_index"] = slide_index

    # Get selected slide
    selected_slide = slide_data[st.session_state["slide_index"] - 1]

    # Construct the image path
    image_path = os.path.join(IMAGE_FOLDER, os.path.basename(selected_slide["image"]))

    # Display Slide Image and Notes
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(image_path, use_column_width=True)
    with col2:
        st.write(f"**Notes:**\n\n{selected_slide['notes']}")



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
