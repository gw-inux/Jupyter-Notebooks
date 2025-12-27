import streamlit as st
# ty comment

st.set_page_config(
    page_title="Dewatering exercise by Ty Ferre",
    page_icon="💦",
)

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
st.write("# Welcome to the Dewatering exercise! 👋")

st.sidebar.success("Select a step above.")

st.header('Finding A Compromise Solution: Mine Dewatering 💦', divider='green')

st.markdown(
    """
    This notebook is designed to guide non-experts through the use of groundwater models to answer a water resources question.
    
    It is presented in **eight steps**, with an **assignment** given after every second step.
    
    Use the sidebar to choose the step to activate

    TRY AGAIN?
"""
)

st.subheader('The Steps ️️🔢', divider='green')
st.markdown(
    """
    **Step** 1️⃣ ▶️ General discussion of how surrounding stakeholders might be affected by mine dewatering - qualitative discussion of the response of an aquifer to pumping.
    
    **Step** 2️⃣ ▶️ Quantitative predictions of drawdown versus distance and time for different Q, T, and S.
    
    **Step** 3️⃣ ▶️ Convert drawdown to utility for three stakeholders.
    
    **Step** 4️⃣ ▶️ Introducing Pareto optimization of pumping among stakeholders.
    
    **Step** 5️⃣ ▶️ Putting Pareto optimization in practice.
    
    **Step** 6️⃣ ▶️ Perform a pumping test on data with error to infer T and S with uncertainty.
    
    **Step** 7️⃣ ▶️ Bayesian multimodel analysis.
    
    **Step** 8️⃣ ▶️ Reality: why these methods are almost never used!
        
    ---
"""
)
  
st.subheader("The Assignments 📃 (Ty's comment)", divider='green')
st.markdown("""
    **Encourage students to read the assignments before they are assigned!**
    
    #### **Assignment after step 2.**
    * Produce three curves of _s(t)_ out to two years, one at the distance relevant for each stakeholder, on the same axes.
    * Explain in a clear paragraph why they all have the same general shape, but they are different in the details.
    * Discuss your understanding at this time of the role of a hydrogeologist in negotiating water issues related to dewatering.
    
    #### **Assignment after step 4.**
    * Plot the utility for the mine against the utility for the town using a point for each dewatering rate considered in class.
    * Explain the meaning of the Pareto Front.
    * Choose one pumping rate that is not on the front and explain in a clear paragraph why it is not among the optimal pumping rates.
    
    #### **Assignment after step 6.**
    * How should each stakeholder decide which fit to trust?
    * Can you think of an objective way to find the best model?  What are the limitations to this approach?
    * Can you think of an objective way to use all three models?
    * Comment on the value of improving data quality for hydrogeologic analyses.
    * What are the risks or potential costs of poor data quality?
    
    #### **Assignment after step 8.**
    * Self-reflection – what did you learn in this part of the class?
    * Do you expect that you might use what you learned in your career?  In your personal life?
    * How could this section have been improved?
""")

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')