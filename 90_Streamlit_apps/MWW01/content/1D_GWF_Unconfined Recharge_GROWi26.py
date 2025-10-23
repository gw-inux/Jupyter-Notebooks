# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container

st.title('Initial example for :green[System Understanding through Model Analysis]')

st.markdown(
    """
    The aim of this tools is to provide an initial example of a model application. For this reason, the app considers a idealized scenario of a possible accident in a groundwater catchment. The analysis is done with an analytical solution of a groundwater flow model. This model allows to gain system understanding for the investigated aquifer, and to answer simple questions regarding groundwater management.
    """
)
st.header('Analytical solution for 1D unconfined flow with two defined head boundaries', divider="green")
st.markdown(
    """
    The app computes **1D groundwater flow** in an unconfined, homogeneous, and isotropic aquifer that is bounded by two defned head boundaries. The aquifer receives groundwater recharge from the top.
    
    Subsequently, you will find 
    - A short description of the initial situation that serve for an exercise,
    - Some explanation of the underlying theory of the 1D analytical groundwater flow model,
    - The exercise with questions, directions for the analysis including an interactive plot.
    """
)
st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_001.jpg', caption="Fig 01: Sketch of the model.")

st.subheader('Initial situation and challenge (management task)')
st.markdown(
    """
    We consider an area that is mainly composed of thick sandy aquifers. In the area are several large lakes, see figure. On the land surface between two lakes happend an car accident that results in the possible release of harmful substances in the underground. For that reasons, a very quick initial evaluation of the situation is required.
    
    """
)
left_co1, right_co1 = st.columns((1,1))
with left_co1:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_002.jpg', caption="Fig 02: Top view of the area, showing the close proximity of active open pit mines and post-mining lakes. The spatial extent of the areal view is several 10s of kilometers.")
with right_co1:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_003.jpg', caption="Fig 03: Picture from the inside of an open pit mine, showing the geological composition of the underground, which is mainly thick sandy structures.")
"---"

lc1, mc1, rc1 = st.columns([1,4,1])
with mc1:
    show_theory = st.button('Click here if you want to read more about the underlying theory')
    
if show_theory:
    st.subheader('Conceptual model')
    st.markdown(
        """
        The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by two defined-head boundary conditions on the in- and outflow part. From the top, the aquifer receives uniform groundwater recharge.
        """
    )

    st.subheader('Mathematical model')
    st.markdown("""The equation for 1D groundwater flow in a homogeneous aquifer is""")
    st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')
    st.markdown(
        """
        with
        - _x_ is spatial coordinate along flow,
        - _h_ is hydraulic head,
        - _K_ is hydraulic conductivity,
        - _R_ is recharge.
    
        A solution for the equation can be obtained with two boundary conditions at _x_ = 0 and _x_ = _L_:
        """
    )

    st.latex(r'''h(0) = h_0''')
    st.latex(r'''h(L) = h_L''')
    st.markdown(
        """
        The solution for hydraulic head _h_ along _x_ is
        """
    )
    st.latex(r'''h(x)=\sqrt{h_0^2-\frac{h_0^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}''')
"---"

st.subheader('Own investigation (exercise)')
st.markdown(
    """
    Now we take a closer look on the remaining land area between two post-mining laks (Fig 04, the lakes are represented by the organge and green dot.). We assume that on a street an accident occured. To investigate the situation, we apply a 1D groundwater model for an unconfined aquifer (see Fig. 01). The model is placed between the two lakes as indicated by the pink line in Fig. 04. The distance between the two lakes is fixed to _L_ = 2500 m.
    
    """
)

left_co2, right_co2 = st.columns((1,1))
with left_co2:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_004.jpg', caption="Fig 04: Top view of the section between two post-mining lakes.")
with right_co2:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_005.jpg', caption="Fig 05: The groundwater model for the investigated situation.")


# Initial assessment

lc2, mc2, rc2 = st.columns([2,3,1])
with mc2:
    show_initial_assessment = st.button("**Show the initial questions**")
if show_initial_assessment:
    stb.single_choice(":green[Assume a situation **without recharge** (recharge is zero, e.g., after a long and dry summer). You intend to compute the hydraulic heads _h(x)_ in the underground. **How much is the influence of the hydraulic conductivity _K_ on the solution?**]",
                  ["Very high influence", "High influence", "Intermediate influence", "Minor influence", "No influence"],
                  4,success='CORRECT! You will see this in the next steps.', error='This is not correct. In the next steps we will further investiage this behaviour.')
    stb.single_choice(":green[Now assume a situation **with** average annual **recharge**. **To which lake** will the possible contamination move?]",
                  ["To the lake on the left", "To the lake on the right", "The possible contamination will not move", "The flow direction can be to the left or to the right"],
                  3,success='CORRECT! We will do this in the next steps.', error='This option is not suitable. Re-Think the situation.')    
    stb.single_choice(":green[What is a **typical ammount for groundwater recharge** (in moderate climate like Middle Europe)?]",
                  ["1000 mm/a", "500 mm/a", "200 mm/a", "50 mm/a", "5 mm/a"],
                  2,success='CORRECT! This is a reasonable approximation.', error='This is not correct. Please consider an average precipitation of 700 mm/a and evapotranspiration of 500 mm/a.')

"---"

# Create buttons with st.button and proceed with the steps of the exercise
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #00FF00;
        color: black;
    }""",
):
    if st.button('Proceed with Exercise Step 1'):
        st.markdown("""
            **STEP 1:**
            First we aim to investigate the sensitivity of the hydraulic conductivity _K_ on hydraulic heads _h_ without recharge.
            
           _To proceed_ (with the interactive plot):
            - Modify the hydraulic conductivity. What happens?
"""
)
    if st.button('Proceed with Exercise Step 2'):
        st.markdown("""
            **STEP 2:**
            Now we aim to investigate the sensitivity of the hydraulic conductivity _K_ on hydraulic heads _h_ with recharge.
            
           _To proceed_:
            - First set a reasonable value for groundwater recharge _R_,
            - Now, modify the hydraulic conductivity again. What happens?
            - Further reduce the hydraulic conductivity to small values. What happens?
            - Eventually, go back to the initial assessment (the questions above) and re-answer.
"""
)
    if st.button('Proceed with Exercise Step 3'):
        st.markdown("""
            **STEP 3:**
            
            Now you can use the interactive plot for your own investigations. 
            
           _To proceed_:
            - Modify the different parameters and see the reaction.
"""
)
st.subheader('Computation and visualization')
st.markdown(
    """
    Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge _R_ (in mm/a) and the hydraulic conductivity _K_ (in m/s).
    """
)

# Input data
# Define the minimum and maximum for the logarithmic scale
log_min = -7.0  # Corresponds to 10^-7 = 0.0000001
log_max =  0.0  # Corresponds to 10^0 = 1

log_min2 = -5.0 # Corresponds to 10^-7 = 0.0000001
log_max2 =  3.0 # Corresponds to 10^0 = 1

columns = st.columns((1,1,1), gap = 'large')

with columns[0]:
    y_scale = st.slider('Scaling y-axis', 0,20,3,1)

    
with columns[1]:
    hl=st.slider('LEFT defined head', 120,180,102,1)
    hr=st.slider('RIGHT defined head', 120,180,101,1)
    #L= st.slider('Length', 0,7000,2500,10)
    L = 2500


with columns[2]:
    if st.toggle('K in m/d'):
        # Input, convert the slider value to the logarithmic scale and display
        K_slider_valued=st.slider('(log of) **Hydraulic conductivity** _K_ in m/d', log_min2,log_max2,-2.0,0.01,format="%4.2f")
        Kd = (10 ** K_slider_valued)*86400
        st.write("**_K_ in m/d:** %5.2e" %Kd)
        K = Kd/86400
    else:
        # Input, convert the slider value to the logarithmic scale and display
        K_slider_value=st.slider('(log of) **Hydraulic conductivity** _K_ in m/s', log_min,log_max,-4.0,0.01,format="%4.2f")
        K = 10 ** K_slider_value
        st.write("**_K_ in m/s:** %5.2e" %K)    
    R = st.slider('**Recharge** _R_ in mm/a', 0,500,0,10)
    
x = np.arange(0, L,L/1000)
R = R/1000/365.25/86400
h = (hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5
    
# PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.title('Hydraulic head for 1D unconfined flow', fontsize=16)
ax.plot(x,h)
plt.xlabel(r'x in m', fontsize=14)
plt.ylabel(r'hydraulic head in m', fontsize=14)
ax.fill_between(x,0,h, facecolor='lightblue')
    
# Show BOUNDARY CONDITIONS hl, hr
ax.vlines(0, 0, hl, linewidth = 10, color='orange')
ax.vlines(L, 0, hr, linewidth = 10, color='lime')
    
# MAKE 'WATER'-TRIANGLE
h_arrow = (hl**2-(hl**2-hr**2)/L*(L*0.96)+(R/K*(L*0.96)*(L-(L*0.96))))**0.5  #water level at arrow
ax.arrow(L*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L*0.015), head_length=(h_arrow*0.0015))
ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

#ARROWS FOR RECHARGE 
if R != 0:
    head_length=(R*86400*365.25*1000*0.002)*y_scale/2
    h_rch1 = (hl**2-(hl**2-hr**2)/L*(L*0.25)+(R/K*(L*0.25)*(L-(L*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
    ax.arrow(L*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch2 = (hl**2-(hl**2-hr**2)/L*(L*0.50)+(R/K*(L*0.50)*(L-(L*0.50))))**0.5  #water level at arrow for Recharge Postition 2
    ax.arrow(L*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch3 = (hl**2-(hl**2-hr**2)/L*(L*0.75)+(R/K*(L*0.75)*(L-(L*0.75))))**0.5  #water level at arrow for Recharge Position 3
    ax.arrow(L*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)

#Groundwater divide
max_y = max(h)
max_x = x[h.argmax()]
R_min_ms = K*abs(hl**2-hr**2)/L**2
if R>R_min_ms:
    plt.vlines(max_x,0,max_y, color="r")
plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
plt.xlim(-50,L+50)
plt.text(L, (hl*1.016), 'R: {:.2e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='lightgrey'))
st.pyplot(fig)

"---"

st.subheader('Concluding remarks')

left_co3, right_co3 = st.columns((1.5,1))
with left_co3:
    st.markdown(
        """
        This app demonstrate a simple problem analysis with a groundwater model. In the example, we can identify the individual steps of the groundwater modeling workflow, shown in the following Fig 06.
    
        1. Question and purpose: The question and purpose of our analysis was 
        - to gain system understanding (sensitivity of hydrogeological parameters like hydraulic conductivity _K_ and boundary conditions like recharge _R_),
        - to answer the question, in which direction/lake a possible contamination move.
        
        Based on these (initial) questions and the idealized purpose of the model, we define a suitable and adequate conceptual model.
        """
)

with right_co3:
    st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_006.jpg', caption="Fig 06: Typical workflow for groundwater modeling (according to Anderson et al. 2015.")

st.markdown(
    """    
    2. Conceptual model: We use a very simple and idealized conceptual model. The underground is represented by one homogeneous and isotropic structure. The boundary conditions on both sides are the lakes - implemented as defined head (1st type) boundaries. In addition, there is groundwater recharge (2nd type boundary condition) from the top.
    
    The conceptual model (Fig 06) provides a qualitative description of the system. Subsequently, we need a quantitative solution.
    """
)
st.image('90_Streamlit_apps/SYMPLE25/assets/images/GWF/GWF_007.jpg', caption="Fig 07: The conceptual model for the situation.")

st.markdown(
    """
    3. Mathematical model: The mathematical model for our situation is an adapted version of the general 3D groundwater flow equation. In our case, we can simplify the groundwater flow equation for our conditions:
    - 1D groundwater flow (along x-axis),
    - homogeneous and isotropic aquifer,
    - groundwater recharge as source term.
   
   With this, the groundwater flow equation writes (see explanation above):
    """
)
st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')

st.markdown(
    """
    with suitable boundary conditions, the analytical solution ('groundwater model') of the 1D groundwater flow equation is:
    """
)
st.latex(r'''h(x)=\sqrt{h_0^2-\frac{h_0^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}''')

st.markdown(
    """
    We used the groundwater model to investigate and analyze our scenario. For this reason, we applied the interactive plot as user-interface to our model.
    """
)

"---"
