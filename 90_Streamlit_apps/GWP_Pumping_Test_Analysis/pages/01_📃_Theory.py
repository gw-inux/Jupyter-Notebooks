import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button

st.title('📃 Basic Theory')

st.header(':orange[Underlying the Pumping Test Analysis App]')

st.subheader(':orange-background[Introduction and Overview]', divider="orange")
st.markdown("""
            This part of the application provides a general overview about groundwater flow towards a well. The basic principles for a quantitative description of the process with mathematical equations are explained and derived. The individual details for specific solutions (like Theis, Hantush/Jacob, Neuman) are provided in the specific parts of the application.
            
            We provide a few questions to allow you to assess the current state of your knowledge.
"""
)
# Initial assessment
   
with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1,1))
     
    with columnsQ1[0]:
        stb.single_choice(":orange[**Where do you find the hydraulic head within a confined aquifer?**]",
                  ["Below the aquifer top.", "Directly at the aquifer top.", "Above the aquifer top.", "A confined aquifer doesn't show a hydraulic head"],
                  2,success='CORRECT! Confined aquifer heads are above the top of the aquifer. This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think the situation.')
        stb.single_choice(":orange[**What is considered as transient state?**]",
                  ["The model represents a long-term average.", "The model changes over time.", "The model changes over space.", "When the model accounts for water abstraction."],
                  1,success='CORRECT! Head changes with time in a transient situation. This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think the situation.')             
    with columnsQ1[1]:
        stb.single_choice(":orange[**What parameter is used to describe the ability of an aquifer to transmit water?**]",
                  ["Storativity", "Hydraulic head", "Transmissivity", "Specific storage"],
                  2,success='CORRECT! Transmissivity describes the ability of an aquifer to transmit water.', error='This is not correct. Feel free to re-think this and/or look up terms and answer again.') 
        stb.single_choice(":orange[**What is the equivalent to 0.001 m³/s?**]",
                  ["1 Liter per second", "10 Liters per second", "100 Liters per second", "1 000 Liters per second", "10 000 Liters per second"],
                  0,success='CORRECT! 1000 Liters are one m³', error='This is not correct. Feel free to re-think this and/or look up the relationship between liters and cubic meters, and answer again.')  
"---"
st.subheader(':orange-background[General situation]', divider="orange")

st.markdown("""
            The mathematics included in this application consider only homogeneous and isotropic aquifers. Natural aquifers are not homogeneous nor isotropic (although they come close to isotropic in most instances), so in practice the procedures presented in this application are applied to heterogeneous and anisoptropic aquifers to glean average parameters representative of bulk behavior of the system. The aquifer can be confined, leaky, or unconfined. 
            
            If a well is pumping water out of the aquifer, water flows radially towards the well.
            
            The following video provides an conceptual overview about aquifer testing in different underground formations (_you can directly access the video through the Groundwater-Project Videos at https://gw-project.org/videos/concept-testing-confined-and-leaky-confined-aquifers/)
"""
)
st.video('https://www.youtube.com/watch?v=Bz3wh9RF0c4')

st.subheader(':orange-background[Mathematical description]', divider="orange")
st.markdown("""         
            #### Setting up the equation
            The following equation can be used to describe hydraulic head at a distance $r$ from the well. This equation accounts for 1-dimensional radial transient flow toward a fully penetrating well within a confined or unconfined aquifer without any other sinks and sources of water.
"""
)
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')

st.markdown("""
            Charles V. Theis (1935) derived an equation describing drawdown $s$ with radial distance $r$ from the well.
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')

st.markdown("""
            with the well function
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')

st.markdown("""
            and the dimensionless variable $u$
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')

st.markdown("""
            #### Solving the equation
            This equation is not easy to solve. **Historically**, values for the well function were provided by **tables**, or were presented as a **type-curve** of drawdown as a function of time around a well.
"""
) 
with st.expander(':orange[**Click here**] for further **ressources about Charles V. Theis** and his solution like the **original communication** and a **video interview!**'):
    st.markdown("""
            The following information is a short exercpt from IAH's The Hydrogeologist Time Capsule (https://timecapsule.iah.org/).
            
            _... In 1935, Charles V. Theis published a brief article that was the first transient solution for groundwater flow toward a well. He did so by understanding the vital analogy between groundwater flow and heat transfer. As John Bredehoeft says: "It takes real genius to see the basic form of the underlying theory – this was Theis’ contribution". Today, the Theis transient pump test solution is used by all hydrogeologists for well test interpretation. It is one of the many consequences of his discovery. The Theis legacy is not limited to the transient theory. He was one of the first scientists to emphasize the importance of geological heterogeneity._
            
            _Further information about Theis’ life and discoveries is available in the references provided below._
            
            - The original correspondence about C.V. Theis' solution can be read here: https://timecapsule.iah.org/wp-content/uploads/2021/10/TheisLubin.pdf
            - Selected Contributions to Ground-Water Hydrology by C.V. Theis, and a Review of His Life and Work. U.S. GEOLOGICAL SURVEY WATER-SUPPLY PAPER 2415 https://pubs.usgs.gov/wsp/2415/report.pdf
            
            _The subsequent video gives an impression of Charles V. Theis and his contributions to hydrogeology_
            _(**Recording date**: 1985/11/13, **Recording location**: Albuquerque, New Mexico, USA, **Interview**: John Bredehoeft,  **Production**: Ben Jones, **Editing**: Sylvain Tissot & Philippe Renard)_. 
    """
    ) 
    st.video('https://youtu.be/AEq-jvl0GMw?si')
    st.markdown("""
            For more insights and information, you can access the **full page of the IAH Time capsule about Charles V. Theis** at https://timecapsule.iah.org/person/charles-vernon-theis/
    """
    ) 
    
st.markdown("""            
            Plotting field measurements of drawdown over time during a pumping test on graph paper and matching it to the type curve to estimate transmissivity $T$ and storativity $S$ is a time-tested hydrogeological method.
            
            **Today** however, rather than physically plotting data on paper, we use **computer codes** to match the data to the type curve because it is easier and more convenient. 
            
            Nevertheless, it is best practice to view the data in graphical form whether it is plotted by hand or by a computer because the shape of the curve provides insight to the nature of the groundwater system and sometimes plotting the data reveals errors in the data.
                  
            Subsequently, in this application, the Theis equation is solved using Python codes.
"""
) 
st.subheader(':orange-background[Limitations and extensions]', divider="orange")           

st.markdown (
    """   
    #### Limitations of the Theis solution
    While the **Theis solution** has been widely used for analyzing pumping tests in confined aquifers, it is based on several simplifying assumptions that can limit its applicability. The solution assumes
    - that the aquifer is 
        - infinite,
        - homogeneous,
        - isotropic, and 
        - fully confined,
    - instantaneous well discharge,
    - no wellbore storage
    - no partial penetration effects.

    In real-world scenarios, many aquifers are leaky, allowing water exchange with adjacent layers, or exhibit anisotropy and heterogeneity, which the Theis solution does not account for.
    
    #### Further approaches to overcome the limitations of the Theis solution
    To address these limitations, **Hantush and Jacob (1955)** developed a solution that extends the Theis model to leaky aquifers, incorporating the effects of vertical leakage through semi-pervious confining layers. This modification allows for more accurate analysis in regions where aquitards are present.
    
    Further refinements were made by **Neuman (1972)**, who introduced a solution accounting for partial well penetration, wellbore storage, and vertical flow components within the aquifer. The Neuman solution is particularly valuable for unconfined aquifers where delayed gravity drainage and vertical flow to the well significantly influence drawdown behavior. These developments represent significant advancements over the Theis solution, enabling more realistic interpretations of pumping test data in a wider range of hydrogeological settings.
    ___
"""
)
with st.expander('Click here for some references'):
    st.markdown("""
    Theis, C.V., 1935. The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage, Transactions of the American Geophysical Union, volume 16, pages 519-524.
    
    Hantush, M. S., & Jacob, C. E. (1955). Non-steady radial flow in an infinite leaky aquifer. Transactions, American Geophysical Union, 36(1), 95-100.
    
    Neuman, S. P. (1972). Theory of flow in unconfined aquifers considering delayed gravity response. Water Resources Research, 8(4), 1031-1045. DOI: 10.1029/WR008i004p01031
    """
)   

"---"         

columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    st.write()
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_🙋_▶️ Transient_Flow to a Well.py")
