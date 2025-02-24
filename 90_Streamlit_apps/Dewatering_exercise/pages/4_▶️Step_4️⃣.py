import streamlit as st
import streamlit_book as stb

st.markdown(
    """
    ### Dewatering exercise 💦
    ---
    ## Step 4
    * Discuss how stakeholders can use utility to find a compromise decision for the dewatering rate.
    * Consider that the values of _T_, _S_, and the distances to the stakeholder interests are known and correct.
    * Use any tools that have been shown to you previously to explore the utilities of different pumping rates for all stakeholders.    
    * You should agree upon the utility curves for each stakeholder before you begin your analyses.    
    * You should work as a class, with each person exploring two different Q values that you decide upon collectively.
    * Produce a common table with Q and utility for each stakeholder.
    * Once you have your table complete, discuss how you can use it to choose the best Q from those that you examined.
    * Who was Pareto?  Check out Vilfredo Pareto on Wikipedia!
    * What is the Pareto Principle?  Think of some examples of its application!
    * Introduce Pareto optimization generally and discuss how it could be applied to this problem for the mine and the town.

    
    
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
question3 = "Which is the most correct statement?"
options3 = "Pareto optimization finds the best solution.", "Pareto optimization finds the best set of trade-off solutions.", "Pareto optimization is too complicated to ever be used in practice."
answer_index3 = 1
stb.single_choice(question3, options3, answer_index3, success='Correct!  You still need to decide which Pareto-optimal solution is most acceptable among stakeholders, but you can eliminate all suboptimal trade-off solutions!', error='Incorrect - Pareto optimization is used all the time, even if you do not realize that you are doing it.  But it does not necessarily find a single best solution.', button='Check answer')

