import streamlit as st
from streamlit_extras.stodo import to_do
import json
from streamlit_book import multiple_choice
from Dewatering_app_utils import read_md
from Dewatering_app_utils import flip_assessment
from Dewatering_app_utils import render_toggle_container
from Dewatering_app_utils import prep_log_slider

# ToDo:
#    - number input
#    - log slider
#    - revise UI

# Authors, institutions, and year
year = 2025 
authors = {
    "Ty Ferré": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "University of Arizona, Hydrology and Atmospheric Sciences"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# ---------- path to questions for the assessments (direct path)
path_quest_final = "90_Streamlit_apps/Dewatering_exercise_v2/questions/page4_final.json"

# Load questions
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
#--- User Interface

st.title('Dewatering exercise 💦')
st.subheader("Step 04 - Finding Compromise", divider="blue")

# I found U slightly confusing because it is also used in the Theis context

if st.toggle('Show additional **Notes for instructors**'):
    to_do(
    [(st.write, "Lead a discussion to examine tradeoffs.  Think of everyday examples and more complex examples.")],
    "td01",)
    to_do(
    [(st.write, "In each case, you need to balance the cost/benefit or the relative costs and benefits of multiple actions.")],
    "td02",)
    to_do(
    [(st.write, "This requires that you have some way to predict the impacts of the actions and then to value those impacts - good and bad.")],
    "td03",)
    to_do(
    [(st.write, "Conduct the in class exercise to form a Q vs utility curve for different stakeholders.  Can you define the best Q for each stakeholder?")],
    "td04",)
    to_do(
    [(st.write, "Then ask how they could find the best Q considering any two stakeholders, forming a utility tradeoff plot.")],
    "td05",)
    to_do(
    [(st.write, "Introduce Pareto, the man, (see Vilfredo Pareto on Wikipedia) and then talk about the set of optimal tradeoff conditions for any two stakeholders.")],
    "td06",)
    to_do(
    [(st.write, "Introduce the Pareto principle - the 80/20 Rule - ask them to come up with examples and explain why it is a powerful idea.")],
    "td07",)
    to_do(
    [(st.write, "Generalize to describe Pareto optimality.  Ideally, bring this back to the everyday examples that students offered at the start of class.")],
    "td08",)
    to_do(
    [(st.write, "Discuss how Pareto optimality can be applied to the mine dewatering and similar problems.")],
    "td09",)
    


st.markdown(
    """
    * Discuss how stakeholders can use utility to find a compromise decision for the dewatering rate.
    * Consider that the values of _T_, _S_, and the distances to the stakeholder interests are known and correct.
    * Use any tools that have been shown to you previously to explore the utilities of different pumping rates for all stakeholders.    
    * You should agree upon the utility curves for each stakeholder before you begin your analyses.    
    * You should work as a class, with each person exploring two different Q values that you decide upon collectively.
    * Produce a common table with Q and utility for each stakeholder.
    * Once you have your table complete, discuss how you can use it to choose the best Q from those that you examined for any two stakeholders.

    
    
    #### Assignment after step 4. 📑
    👉 Plot the utility for the mine against the utility for the town using a point for each dewatering rate considered in class.
    
    👉 Explain the meaning of the Pareto Front.
    
    👉 Choose one pumping rate that is not on the front and explain in a clear paragraph why it is not among the optimal pumping rates.
    
    ---
"""
)

# --- FINAL ASSESSMENT ---
def content_final():
    st.markdown("""#### 🧠 Final assessment""")
    st.info("These questions test your understanding after working through this page.")

    for i in range(0, len(quest_final), 2):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )

        if i + 1 < len(quest_final):
            with col2:
                st.markdown(f"**Q{i+2}. {quest_final[i+1]['question']}**")
                multiple_choice(
                    question=" ",
                    options_dict=quest_final[i+1]["options"],
                    success=quest_final[i+1].get("success", "✅ Correct."),
                    error=quest_final[i+1].get("error", "❌ Not quite.")
                )

# Render final assessment
render_toggle_container(
    section_id="page_04",
    label="✅ **Show the final assessment** - to self-check your **understanding**",
    content_fn=content_final,
    default_open=False,
)

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
