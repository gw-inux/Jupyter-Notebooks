import streamlit as st

# Initialize session state for value and toggle state
if "input_value" not in st.session_state:
    st.session_state["input_value"] = 50  # Default value
if "use_slider" not in st.session_state:
    st.session_state["use_slider"] = True  # Default to slider

# Toggle between slider and number input
st.session_state["use_slider"] = st.toggle("Use Slider", value=st.session_state["use_slider"])

# Display the appropriate input widget without changing the value
if st.session_state["use_slider"]:
    new_value = st.slider("Select a number", 0, 100, st.session_state["input_value"])
else:
    new_value = st.number_input("Enter a number", 0, 100, value=st.session_state["input_value"])

# Update the stored value without overwriting it when switching widgets
st.session_state["input_value"] = new_value

st.write(f"Current Value: **{st.session_state['input_value']}**")