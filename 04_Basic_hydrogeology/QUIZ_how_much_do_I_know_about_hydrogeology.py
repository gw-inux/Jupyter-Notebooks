import streamlit as st
from streamlit_book import multiple_choice
import json

# Authors, institutions, and year
year = 2025 
authors = {
    "Roland Barthel": [1],
    "Thomas Reimann": [2],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "University of Gothenburg, Department of Earth Sciences",
    2: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

path_quest_final = "04_Basic_hydrogeology/questions/how_much_know_hydrogeology.json"

# Load questions
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
# Functions
# RENDER ASSESSMENTS

def flip_assessment(section_id: str):
    """Flip the boolean flag for a given section_id."""
    key = f"exp_{section_id}"
    st.session_state[key] = not st.session_state.get(key, False)
    
def render_toggle_container(
    section_id: str,
    label: str,
    content_fn,                 # a function that renders the section contents when open
    *,
    default_open: bool = False,
    col_ratio=(25, 1),
    container_border: bool = True,
):
    """
    Renders a toggleable container with two buttons:
    - Left: text button with your label
    - Right: chevron button (▲/▼)
    Each section manages its own state via section_id.

    Parameters
    ----------
    section_id : unique id string, e.g., "general_01"
    label      : button label shown on the left
    content_fn : callable with no args that renders the open content
    default_open : initial open state (only used on first render)
    col_ratio  : column width ratio for (label_button, chevron_button)
    container_border : show a border around the section container
    """
    state_key = f"exp_{section_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_open

    with st.container(border=container_border):
        ass_c1, ass_c2 = st.columns(col_ratio)

        # Left button – same on_click toggler for consistency
        with ass_c1:
            st.button(label,key=f"btn_label_{section_id}",type="tertiary",on_click=flip_assessment,args=(section_id,))

        # Right chevron button – also toggles the same state
        with ass_c2:
            chevron = "▲" if st.session_state[state_key] else "▼"
            st.button(chevron,key=f"btn_chev_{section_id}",type="tertiary",on_click=flip_assessment,args=(section_id,))

        # Conditional content
        if st.session_state[state_key]:
            content_fn()
# --- Start here

st.title("QUIZ")
st.subheader("How much do I know about Hydrogeology?", divider = "blue")

st.markdown("""
#### Preface
This survey, “How much do I know about Hydrogeology?”, was originally developed by Roland Barthel (University of Gothenburg) to assess the prior knowledge of students with different educational backgrounds in hydrogeology, so that course contents could be adjusted accordingly. Over time, the test has also proven valuable for assessing students’ knowledge directly after the course and again about one year later, in order to see how understanding develops and is retained.

Intro to learners: The survey consists of multiple-choice questions covering key hydrogeological concepts (e.g., groundwater flow, aquifer properties, recharge, chemistry, and catchment processes). For each question, you will see the possible answers and, after responding, feedback explaining why an answer is correct or incorrect. The aim is not only to “test” you, but to help you reflect on your current understanding, identify gaps, and support both you and your teachers in improving learning and teaching in hydrogeology.
""")

# --- ASSESSMENT ---
def content_quiz():
    st.markdown("#### How much do I know about Hydrogeology?")
    st.info("These questions test and reflect your current understanding of hydrogeology. At the bottom of the quiz you will find statistics about your performance. You can reset the quiz for a fresh start with the Reset button 🔄")

    # --- Reset button ---
    if st.button("🔄 Reset quiz"):
        # Remove all stored selections for this quiz
        for k in list(st.session_state.keys()):
            if k.startswith("q_"):
                del st.session_state[k]
        st.rerun()

    total_questions = len(quest_final)
    total_answered = 0
    total_correct = 0

    for i, q in enumerate(quest_final):
        st.markdown(f"**Q{i+1}. {q['question']}**")

        # --- INSERT FIGURE FOR SPECIFIC QUESTION ---
        if i == 51:   # Q52 → index 51
            st.image("04_Basic_hydrogeology/FIGS/Q52.jpg", caption="Figure for Question 53")
        
        options = list(q["options"].keys())
        correct_options = [opt for opt, is_correct in q["options"].items() if is_correct]

        # Unique key per question
        widget_key = f"q_{i}_selection"

        # --- SINGLE-CORRECT: use radio ---
        if len(correct_options) == 1:
            selection = st.radio(
                "Select one answer:",
                ["-- select an option --"] + options,
                key=widget_key,
                index=0,
            )

            if selection != "-- select an option --":
                total_answered += 1
                if selection == correct_options[0]:
                    total_correct += 1
                    st.success(q.get("success", "Correct."))
                else:
                    st.error(q.get("error", "Not quite."))

        # --- MULTI-CORRECT: use multiselect ---
        else:
            selection = st.multiselect(
                "",
                options,
                key=widget_key,
                placeholder="Choose all suitable options",
            )

            if selection:  # user selected at least one option
                total_answered += 1
                if set(selection) == set(correct_options):
                    total_correct += 1
                    st.success(q.get("success", "Correct."))
                else:
                    st.error(q.get("error", "Not quite."))

        st.markdown("---")  # separator between questions

    # --- Score summary at bottom ---
    st.subheader("Your Score")
    st.write(f"Answered questions: **{total_answered} / {total_questions}**")
    st.write(f"Correct answers: **{total_correct}**")
    if total_answered > 0:
        st.write(f"Accuracy: **{100 * total_correct / total_answered:.1f}%**")



            
# Render final assessment
render_toggle_container(
    section_id="quiz01",
    label="✅ **Show the Quiz** - to self-check your **understanding**",
    content_fn=content_quiz,
    default_open=False,
)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('04_Basic_hydrogeology/FIGS/CC_BY-SA_icon.png')