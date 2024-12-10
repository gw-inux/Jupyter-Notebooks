import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container

st.title('📃 Basic Theory underlying PumpingTestAnalysis')

st.subheader(':orange-background[The Theis, Neuman, and Hantush Jacob solution]', divider="orange")
st.markdown("""
            ### Introduction and Overview
            This part of the app provides a general overview about groundwater flow towards well. The basic principles for a quantitative description of the processes with mathematical equations are explained and derived. The individual details for specific solutions (like Theis, Hantush/Jacob, Neuman) are provided in the specific parts of the app.
            
            At the beginning, we provide an initial assessment with a few questions to allow you to understand your current state of knowledge.
"""
)

# Initial assessment
lc1, cc1, rc1 = st.columns([1,1,1])

with cc1:
    show_initial_assessment = st.toggle("**Show the initial assessment**")

if show_initial_assessment:
    columnsQ1 = st.columns((1,1), gap = 'large')
    
    with columnsQ1[0]:
        stb.single_choice(":orange[**Where do you find the hydraulic head within a confined aquifer?**]",
                  ["Below the aquifer top.", "Directly at the aquifer top.", "Above the aquifer top.", "A confined aquifer doesn't show a hydraulic head"],
                  2,success='CORRECT! This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think the situation.')
        stb.single_choice(":orange[**What is considered as transient state?**]",
                  ["The model represents a long-term average.", "The model changes over time.", "The model changes over space.", "When the model accounts for water abstraction."],
                  1,success='CORRECT! This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think the situation.')
    
    with columnsQ1[1]:
        stb.single_choice(":orange[**What is the equivalent to 0.001 m3/s?**]",
                  ["1 Liter per second", "10 Liters per second", "100 Liters per second", "1 000 Liters per second", "10 000 Liters per second"],
                  3,success='CORRECT! 1000 Liters are one m3', error='Not quite. Feel free to answer again.')             
"---"

st.markdown("""
            ### General situation
            We consider a homogeneous and isotropic aquifer. The aquifer can be confined, leady, or unconfined. If a well is pumping water out of the aquifer, radial flow towards the well is induced. To calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined or unconfined aquifer without further sinks and sources:
"""
)



st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
st.markdown("""
            ### Mathematical model and solution
            Charles V. Theis presented a solution for this by deriving
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.markdown("""
            with the well function
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.markdown("""
            and the dimensionless variable
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.markdown("""
            This equations are not easy to solve. Historically, values for the well function were provided by tables or as so called type-curve. The type-curve matching with experimental data for pumping test analysis can be considered as one of the basic hydrogeological methods. However, modern computer provide an easier and more convinient way to solve the 1D radial flow equation based on the Theis approach. Subsequently, the Theis equation is solved with Python routines.
"""
)            


columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    st.write()
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_📈_▶️ Transient_Flow to a Well.py")
