import streamlit as st
import streamlit_book as stb

st.header('Checking different options to include quizzes')


st.write('Option one is to use another library. With this, the quizzes are directly in the document.')
stb.single_choice("Darcy's Law: Choose the most correct response",
                  ["Darcy's Law is Q = -KA dH/dL where A is the cross sectional area perpendicular to flow with the units of length squared.", "Darcy's Law is Q = KA dH/dL where Q is the flow with units of length per time.", 
                  "Darcy's Law is Q = KA dH/dL where Q is the flow with units of length cubed per time"],
                  0,success='CORRECT!  A has units of length squared per time, Q has length cubed per time, K has length per time, and the gradient is unitless or length per length.  You also remembered the negative sign!', error='Not quite. A has units of length squared per time, Q has length cubed per time, K has length per time, and the gradient is unitless or length per length.  Also remember the negative sign to account for the fact that flow occurs in the direction opposite to the gradient because of how the gradient is defined!.')

st.write('')                  
st.write('')                  
st.write('Option two is using a dedicated assessment system. This give a much higher degree of options. Further, questions can be used in many other contexts')        
st.link_button('Start Quiz', 'https://bildungsportal.sachsen.de/opal/auth/RepositoryEntry/46740799560')
                  
                  