import streamlit as st
import streamlit_book as stb
from streamlit_extras.stodo import to_do

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


st.markdown(
    """
    ---
    ### Self-check questions 💦
 
"""
)
st.write('')
st.write('')
question1 = "What is a trade=off plot?"
options1 = "A tool to determine how much you may get for your used car.", "A plot that compares the utilties of two or more stakeholders for different proposed actions, such as two pumping rates.", "A tool to predict the drawdown as a function of distance and time."
answer_index1 = 1
stb.single_choice(question1, options1, answer_index1, success='Correct!  Trade off plots are based on predicted outcomes for multiple possible actions, each of which is subjected to the utility curve for each stakeholder.', error='Incorrect - while this is a useful tool it is not a trade-off plot.', button='Check answer')

st.write('')
st.write('')
question1 = "What is the Pareto Front?"
options2 = "Clouds that form before a winter storm.", "The collection of possible solutions based on utility trade-off.", "The collection of best solutions based on utility trade-off."
answer_index2 = 2
stb.single_choice(question1, options2, answer_index2, success='Correct!  Pareto-optimal solutions form the Pareto front and they can only be improved upon for one stakeholder at the cost of lower utility for another stakeholder.', error='Incorrect - depending upon your choice, those are cumulous clouds or that is a trade=off plot.', button='Check answer')

st.write('')
st.write('')
question3 = "Did Pareto have a beard?"
options3 = "Yes, he is pictured with a huge bushy beard.", "No, Pareto is an acronym, he wasn't a real person.", "Pareto lived before the development of cameras, so no one knows if he had a beard."
answer_index3 = 0
stb.single_choice(question3, options3, answer_index3, success='Correct!  Have a look at his Wikipedia page, it is pretty fascinating!', error='Incorrect - he was a real person, with a real beard.  He lived after cameras were invented and, after all, people could have painted him!', button='Check answer')

st.write('')
st.write('')
question4 = "Which is the most correct statement?"
options4 = "Pareto optimization finds the best solution.", "Pareto optimization finds the best set of trade-off solutions.", "Pareto optimization is too complicated to ever be used in practice."
answer_index4 = 1
stb.single_choice(question4, options4, answer_index4, success='Correct!  You still need to decide which Pareto-optimal solution is most acceptable among stakeholders, but you can eliminate all suboptimal trade-off solutions!', error='Incorrect - Pareto optimization is used all the time, even if you do not realize that you are doing it.  But it does not necessarily find a single best solution.', button='Check answer')

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
