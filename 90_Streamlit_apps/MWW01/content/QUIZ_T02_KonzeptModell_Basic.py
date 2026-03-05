import streamlit as st
from streamlit_book import multiple_choice
import json

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

path_quest_final = "90_Streamlit_apps/MWW01/questions/T02_MCQ_A.json"

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

st.title("QUIZ I (Basic Version")
st.subheader("Thema 2 - Konzeptionelle Modelle", divider = "blue")

st.markdown("""
#### Vorbemerkung
Mit diesem Quiz können Sie Ihre Kentnisse zum Thema 2: Konzeptionelle Modell prüfen.
""")

# --- ASSESSMENT ---
import streamlit as st

def content_quiz():
    st.markdown("#### Quiz - T02: Konzeptionelle Modelle?")
    st.info("These questions test and reflect your current understanding of conceptual models.  \nAt the bottom of the quiz you will find statistics about your performance.  \nYou can reset the quiz for a fresh start with the Reset button 🔄.")

    # --- initialize reset token ---
    if "quiz_reset_token" not in st.session_state:
        st.session_state.quiz_reset_token = 0

    # --- Reset button (before widgets) ---
    if st.button("🔄 Reset quiz"):
        st.session_state.quiz_reset_token += 1  # change widget keys
        st.rerun()

    token = st.session_state.quiz_reset_token

    total_questions = len(quest_final)
    total_answered = 0
    total_correct = 0

    for i, q in enumerate(quest_final):
        st.markdown(f"**Q{i+1}. {q['question']}**")
    
        options = list(q["options"].keys())
        correct_options = [opt for opt, val in q["options"].items() if val]
    
        # keys that persist per question + reset token
        sel_key = f"q_{i}_sel_{token}"
        sub_key = f"q_{i}_submitted_{token}"
        ok_key  = f"q_{i}_is_correct_{token}"
    
        # --- FORM: prevents instant evaluation ---
        with st.form(key=f"form_{i}_{token}", border=False):
    
            if len(correct_options) == 1:
                selection = st.radio(
                    "Select one answer:",
                    options,
                    key=sel_key,
                    index=None,
                )
            else:
                # Multi-correct needs multi select (or checkboxes)
                selection = st.multiselect(
                    "Select all that apply:",
                    options,
                    key=sel_key,
                )
    
            submitted = st.form_submit_button("✅ Submit answer")
    
        # --- evaluate ONLY after submit ---
        if submitted:
            st.session_state[sub_key] = True
    
            if len(correct_options) == 1:
                is_correct = (selection == correct_options[0])
            else:
                is_correct = (set(selection) == set(correct_options))
    
            st.session_state[ok_key] = is_correct
    
        # --- show feedback only if submitted before (persist across reruns) ---
        if st.session_state.get(sub_key, False):
            total_answered += 1
            if st.session_state.get(ok_key, False):
                total_correct += 1
                st.success(q.get("success", "Correct."))
            else:
                st.error(q.get("failure", "Not quite."))
    
        st.markdown("---")

    # --- Score summary ---
    st.subheader("Your Score")
    st.write(f"Answered: **{total_answered} / {total_questions}**")
    st.write(f"Correct: **{total_correct}**")
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