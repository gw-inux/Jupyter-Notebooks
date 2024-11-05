import streamlit as st
import streamlit_book as stb

st.markdown(
    """
    ### Dewatering exercise 💦
    ---
    ## Step 01
    
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

                  
