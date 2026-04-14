# comment added to test pushing on GitHub

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
st.subheader("Step 01 - Interactive discovery of :blue[Darcy's Law]", divider="blue")

st.markdown("""
#### Notes for Instructors

There are detailed notes for instructors that help you to implement the app in your own educational activities.

""")
with st.expander(':blue[**Click here**] to read the **Notes for Instructors**'):
    st.markdown(
        """       
        - Lead a discussion about how dewatering might affect nearby stakeholders.  Good examples include the water supply for a nearby town and a stream that is important to an environmental group.
        
        - Introduce Henry Darcy and show a simplified version of his experiment.  Have students reason their way to Darcys Law.
        
        - Turn the column on its side, explore why the gradient will be constant along the column.
        
        - Convert the column to a constant rectangular cross section.  Then reason through why the gradient would not change along the column.
        
        - Introduce transient flow.  First, show two constant gradient condtions, same inflow H, two different outflow H values.
        
        - Reason through how the gradient would change in time from higher to lower inflow H with step change at boundary.
        
        - Convert the column to a decreasing cross sectional area towards outflow.  Then reason through why the gradient would change along the column under steady state flow .
        
        - Show two steady state conditions for column with a decreasing cross sectional area towards outflow with same inflow H, two different outflow H values.
        
        - Reason through how the gradient would change in time from higher to lower inflow H with step change at boundary.
        
        - Show a cross section of a well in an aquifer - you decide if you want to show that it is confined for the sake of accuracy versus simplicity.
        
        - Draw analogy of radial flow towards a well and decreasing area 1D case shown previously.
        
        - Talk through the transient response of an aquifer to pumping.
        
        - Relate this to distant effects of pumping through time.
        
        - Show a supply well and discuss why a decreased water level could be detrimental.
        
        - Show a groundwater-connected stream and discuss why a decreased water level could be detrimental.
    """) 

##################################################################################
# Interactive discovery of Darcy's Law
##################################################################################

st.header("Interactive discovery of Darcy's Law", divider = 'green')
st.markdown(
    """
    Henry Darcy is perhaps the most famous hydrogeologist of all time!
    
    You can find his Wikipedia page here: https://en.wikipedia.org/wiki/Henry_Darcy.

    Let's repeat his famous experiments as a mental exercise.
    
    Imagine that you have a cylinder, full of a porous and permeable material.
    
    It is oriented vertically.  The vertical length is _L_.  The cross sectional area is constant and equal to _A_.
    You maintain water ponded to a certain height above the top of the sand, _h<sub>top</sub>_, at the top of the column.
    The bottom of the column is connected to a hose.  All water flows through the hose, not through anywhere else at the bottom ofthe column.
    The open end of the hose is a height, _h<sub>bottom</sub>_, above the bottom of the column.
    
    Before you use the model to check your answers, do you think that there would be more or less flow if the following change was made with everything else being held constant?
    
    Area increased, length increased, ponded height at the top of the column increased, height of the bottom of the outflow tube increased?
    
    Once you have made your predictions, use the model below to check them!
    """, unsafe_allow_html=True
) 

A_min = 10.0 # minimum cross sectional area, cm3
A_max = 40.0  # maximum cross sectional area, cm3
L_min = 0.5 # minimum length, cm
L_max = 25.0  # maximum length, cm
h_top_min = 0.0 # minimum ponding at top of column, cm
h_top_max = 20.0  # maximum ponding at top of column, cm
h_bottom_min = 0.0 # minimum ponding at top of column, cm
h_bottom_max = 20.0  # maximum ponding at top of column, cm
K_min = 0.0001 # minimum K in cm/s
K_max = 0.01  # maximum K in cm/s

columns = st.columns((1,1), gap = 'large')
    
with columns[0]:
    A_slider_value=st.slider('Cross sectional area in cm2', A_min,A_max,(A_min + A_max) / 2,(A_max - A_min)/10,format="%4.2f" )
    h_bottom_slider_value=st.slider('Height of bottom of tube above bottom of column in cm', h_bottom_min,h_bottom_max,(h_bottom_min + h_bottom_max) / 2,(h_bottom_max - h_bottom_min)/10,format="%4.2f" )

with columns[1]:
    L_slider_value=st.slider('Length in the direction of flow in cm', L_min,L_max,(L_min + L_max) / 2,(L_max - L_min)/10,format="%4.2f" )
    h_top_slider_value=st.slider('Ponded height of water at top of column in cm', h_top_min,h_top_max,h_top_min,(h_top_max - h_top_min)/10,format="%4.2f" )

# Compute flow
Q = -K_max * A_slider_value * (h_bottom_slider_value - h_top_slider_value - L_slider_value ) / L_slider_value   # in cm3/s

st.write('')   
st.write('')   
st.write("The downward flow rate in cm3/min is: ", Q*60.00)

'---'
st.markdown(
    """

    Now imagine the same column turned on its side, so that it extends horizontally.  What was the top is the left, the bottom became the right.

    Before you use the model to check your answers, answer these questions.
 
    Do you think that the flow will have the same dependence on _A_, _L_, _h<sub>top</sub>_, and _h<sub>bottom</sub>_ that it did for the vertical column?
    
    If you set the slider bars to the same values for the vertical and horizontal columns, will they have the same flow?

    Once you have made your predictions, use the model below to check them!

    """, unsafe_allow_html=True
)   

columns = st.columns((1,1), gap = 'large')
    
with columns[0]:
    A_slider_value1=st.slider('Area in cm2', A_min,A_max,(A_min + A_max) / 2,(A_max - A_min)/10,format="%4.2f" )
    h_bottom_slider_value1=st.slider('Ponded height of water at left end of column in cm', h_bottom_min,h_bottom_max,(h_bottom_min + h_bottom_max) / 2,(h_bottom_max - h_bottom_min)/10,format="%4.2f" )

with columns[1]:
    L_slider_value1=st.slider('Distance in the direction of flow in cm', L_min,L_max,(L_min + L_max) / 2,(L_max - L_min)/10,format="%4.2f" )
    h_top_slider_value1=st.slider('Ponded height of water at right end of column in cm', h_top_min,h_top_max,h_top_min,(h_top_max - h_top_min)/10,format="%4.2f" )

# Compute flow
Q = -K_max * A_slider_value1 * (h_top_slider_value1 - h_bottom_slider_value1) / L_slider_value1   # in cm3/s

st.write('')   
st.write('')   
st.write("The flow rate to the right in cm3/min is: ", Q * 60.)





st.markdown(
    """
    ---
    ### Self-check questions 💦
 
"""
)
st.write('')
st.write('')
question1 = "Choose the most correct answer."
options1 = "Flow occurs from high hydraulic head to low hydraulic head.", "Flow occurs from high pressure to low pressure.", "Flow occurs from lowh hydraulic head to high hydraulic head."
answer_index1 = 0
stb.single_choice(question1, options1, answer_index1, success='Correct!  Flow occurs from high total energy, or hydraulic head, to low total energy.', error='Incorrect - you need to consider the total energy, both elevation and pressure head, and flow occurs from high to low total energy.', button='Check answer')

st.write('')
st.write('')
question2 = "Considering a vertical soil column, identify the three things that would increase the steady state flow, with all else held constant."
options2 = "Increased cross sectional area, length, and hydraulic head gradient.", "Increased cross sectional area and hydraulic head gradient and decreased K.", "Increased cross sectional area, K, and hydraulic head gradient."
answer_index2 = 2
stb.single_choice(question2, options2, answer_index2, success='Correct!  Darcys Law is Q= -KA dH/dL, an increase in K, A, and dH/dL would cause Q to increase.', error='Incorrect - Darcys Law is Q= -KA dH/dL, a decrease in K or L would cause flow to decrease.', button='Check answer')

st.write('')
st.write('')
question3 = "Why does Darcys Law include a negative sign?"
options3 = "Because Darcy saw increased flow as a bad thing.", "Because uphill is defined as a positive gradient, but water flows downhill.", "Because the derivative of a gradient is negative."
answer_index3 = 1
stb.single_choice(question3, options3, answer_index3, success='Correct!  The negative sign is just to account for our convention when defining the gradient.', error='Incorrect - Darcy had no problem with more flow and do not be fooled by fancy math statements!', button='Check answer')

st.write('')
st.write('')
question4 = "Why does the gradient decrease with distance from a pumping well?"
options4 = "Because you are farther from the well.", "Because flow to the well is radially convergent, so the same flow has to pass through a smaller cross sectional area.", "Because pumping decreases K near the well."
answer_index4 = 1
stb.single_choice(question4, options4, answer_index4, success='Correct!  This is just like what you would see if you considered flow through a column that got narrower in the direction of flow!', error='Incorrect - it is true, but not informative, that you are farther from the well as you get farther from the well - and it is also potentially true that the pumping decreases K, but that is not the simplest answer!', button='Check answer')

st.write('')
st.write('')
question5 = "How can you get water out of something while it remains fully water-saturated?"
options5 = "By decreasing the porosity, like squeezing a sponge.", "Magic.", "By causing the water to expand."
answer_index5 = 0
stb.single_choice(question5, options5, answer_index5, success='Correct!  This is the best answer for hydrogeologic applications - the decreased water pressure allows the medium to collapse a little bit.', error='Incorrect - Magic?  Really?  Also, water is very, very incompressible - it is very hard to change the density of water by changing the water pressure.', button='Check answer')

st.write('')
st.write('')
question6 = "Why might a nearby environmental group be concerned about dewatering operations at a mine?"
options6 = "The noise of the pumps could affect wildlife.", "The pumping might cause water to flow towards the mine.", "Pumping might lower the water table, which could make it more difficult for plants to get water while also decreasing flow in streams."
answer_index6 = 2
stb.single_choice(question6, options6, answer_index6, success='Correct!  This lowering the water table decreases plant-available water and can cause streams to lose water to the subsurface.', error='Incorrect - pumps might be noisy, but this is not their main impact and water flowing toward the well is not a direct problem in most cases.', button='Check answer')

st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
