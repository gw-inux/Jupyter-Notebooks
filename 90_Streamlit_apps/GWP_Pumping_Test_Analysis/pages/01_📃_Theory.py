import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button

st.title('📃 Basic Theory')

st.header(':orange[Underlying the Pumping Test Analysis Application]')

st.subheader(':orange-background[Introduction and Overview]', divider="orange")
st.markdown("""
            This part of the application provides a general overview about groundwater flow toward a well. It explains the basic principles and provides a quantitative description of the process using basic groundwater flow equations. 
            
            The details of specific solutions (Theis, Hantush/Jacob, Neuman) are provided in separate sections of this application that are dedicated to each solution.
            
            We offer a few questions to allow you to assess the current state of your knowledge.
"""
)
# Initial assessment
   
with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1,1))
     
    with columnsQ1[0]:
        stb.single_choice(":orange[**What is the value of hydraulic head within a confined aquifer?**]",
                  ["Lower than the elevation of the aquifer top", "Equal to the elevation of the aquifer top", "Higher than the elevation of the aquifer top", "A confined aquifer doesn't show a hydraulic head"],
                  2,success='CORRECT! Confined aquifer heads are above the top of the aquifer. This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think about how confined and unconfined aquifers differ and feel free to answer again.')
        stb.single_choice(":orange[**What is considered as transient?**]",
                  ["A system with a constant long-term average", "A system in swhich head changes over time.", "A system in which head is different at different locations", "A system experiencing water abstraction."],
                  1,success='CORRECT! Head changes with time in a transient situation. This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think about the meaning of transient and feel free to answer again.')             
    with columnsQ1[1]:
        stb.single_choice(":orange[**What parameter is used to describe the ability of an aquifer to transmit water?**]",
                  ["Storativity", "Hydraulic head", "Transmissivity", "Specific storage"],
                  2,success='CORRECT! Transmissivity describes the ability of an aquifer to transmit water.', error='This is not correct. It may help to look up terms [by downloading the book: A Glossary of Hydrogeology](https://gw-project.org/books/a-glossary-of-hydrogeology/). Feel free to answer again.')
        stb.single_choice(":orange[**What is the equivalent to 0.001 m³/s?**]",
                  ["0.1 Liter per second", "1 Liter per second", "10 Liters per second", "100 Liters per second", "1000 Liters per second"],
                  1,success='CORRECT! 1000 Liters are one m³', error='This is not correct. Feel free to re-think this and/or look up the relationship between liters and cubic meters, and answer again.')  
"---"
st.subheader(':orange-background[General situation]', divider="orange")

st.markdown("""
            The mathematics included in this application consider only homogeneous and isotropic aquifers. Natural aquifers are not homogeneous nor isotropic (although they come close to isotropic in most instances), so in practice the procedures presented in this application are applied to heterogeneous and anisoptropic aquifers to glean average parameter values that are representative of bulk behavior of the system. The aquifer can be confined, leaky, or unconfined. 
            
            When a well pumps water out of an aquifer, water flows radially toward the well.
            
            The following video provides a conceptual overview of aquifer testing in different underground formations. It can be viewed by clicking below or accessed through the [Groundwater-Project website](https://gw-project.org/videos/concept-testing-confined-and-leaky-confined-aquifers/).
"""
)
st.video('https://www.youtube.com/watch?v=Bz3wh9RF0c4')

st.subheader(':orange-background[Mathematical description]', divider="orange")
st.markdown("""         
            #### The radial flow equation
            The radial gourndwater flow equation can be used to describe hydraulic head at a time $t$ and distance $r$ from a pumping well. This equation accounts for 1-dimensional, radial, transient flow toward a well that fully penetrates a confined or unconfined aquifer without any other sinks and sources of water.
"""
)
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')

st.markdown("""
            Charles V. Theis (1935) derived an equation describing drawdown $s$ with radial distance $r$ from the well as shown here.
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')

st.markdown("""
            with the well function as follows
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')

st.markdown("""
            and the dimensionless variable $u$ defined as:
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')

st.markdown("""
            #### Solving the equation
            This equation is not easy to solve. **Historically**, values for the well function were provided in **tables** or presented as a **type-curve** graph.
"""
) 
with st.expander(':orange[**Click here**] for further **information about Charles V. Theis** and his solution, including the **original communication** and a **video interview**'):
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
    While the **Theis solution** has been widely used for analyzing pumping tests in confined aquifers, it is based on several simplifying assumptions that can limit its applicability. The solution assumes the following.
    - that the aquifer is 
        - of infinite lateral extent
        - homogeneous
        - isotropic 
        - fully confined
    - the aquifer response to removal of water from the wll bore  is instantaneous
    - the well bore is infinitesimally small
    - the well fully penetrates the auifer

    Unlike the pristine system described by the Theis equation, in the field many aquifers are leaky, allowing water exchange with adjacent layers, or they are uncofnined, or exhibit anisotropy and heterogeneity. The Theis Solution does not account for these complexities.
    
    #### Further approaches to overcome the limitations of the Theis solution
    To address these limitations, **Hantush and Jacob (1955)** developed a solution that extends the Theis model to leaky aquifers, incorporating the effects of vertical leakage through semi-pervious confining layers. This modification allows for more accurate analysis in regions where aquitards are present.
    
    Further refinements were made by **Neuman (1972)**, who introduced solutions accounting for the delayed water level decline in unconfined aquifers, the vertical flow components in response to partially penetrating wells, and the delayed observation of aquifer drawdown due to removal of water from wellbore storage. These developments represent significant advancements over the Theis solution, enabling more realistic interpretations of pumping test data in a wider range of hydrogeological settings.
"""
)     

st.subheader(':orange-background[Intermediate conclusion and next steps]', divider="blue")
st.markdown('''
            Thus far, we investigated the theory of flow to a well.
            
            The next part of this application explores visual conceptualization of drawdown around a pumping well. You can move to the next section using either the side menu or the navigation buttons at the bottom of this page.
            '''
)

with st.expander('**Click here for some references**'):
    st.markdown("""
    Theis, C.V., 1935. The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage, Transactions of the American Geophysical Union, volume 16, pages 519-524.
    
    Hantush, M. S., & Jacob, C. E. (1955). Non-steady radial flow in an infinite leaky aquifer. Transactions, American Geophysical Union, 36(1), 95-100.
    
    Neuman, S. P. (1972). Theory of flow in unconfined aquifers considering delayed gravity response. Water Resources Research, 8(4), 1031-1045. DOI: 10.1029/WR008i004p01031
    
    [Kruseman, G.P., de Ridder, N.A., & Verweij, J.M.,  1991.](https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/) Analysis and Evaluation of Pumping Test Data, International Institute for Land Reclamation and Improvement, Wageningen, The Netherlands, 377 pages.
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
