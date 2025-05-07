import streamlit as st

st.title('📃 Theory underlying SoilWaterRetention')

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Oriol Bertran": [2],
    "Daniel Fernàndez-Garcia": [2]
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
    2: "UPC Universitat Politècnica de Catalunya",
#   2: "Second Institution / Organization"
}

index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

#-----------------------------------------------#
# UNSATURATED ZONE                              #
#-----------------------------------------------#
st.markdown(
    """
    ## The concepts :books:  
    ### Unsaturated Zone
    In contrast to the *Saturated Zone*, where the porous medium is fully saturated with a single fluid of uniform properties (density, viscosity, and composition), the *Unsaturated Zone* contains—at least—two immiscible fluids that coexist: a wetting and non-wetting, such as water and air, respectively (**Figure 1a**). As shown in **Figure 1b**, the moisture content in the *Unsaturated Zone* is therefore less than 100%. The pressure head under saturated conditions is greater than one, equal to zero at the groundwater table, and negative in the unsaturated zone (**Figure 1c**).
    """
)

left_co, cent_co, last_co = st.columns((10, 80, 10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/freeze_cherry_2.png')
    st.markdown(
        r"Fig. 1- Groundwater conditions near the ground surface. (a) Saturated and unsaturated zone; (b) profile of moisture content versus depth; (c) pressure-head and. Adapted from Freeze and Cherry (1979)"
    )

#-----------------------------------------------#
# SURFACE TENSION AND WETTABILITY               #
#-----------------------------------------------#
st.markdown(
    """
    ### Surface tension and wettability
    
    **Surface tension** arises at the interface between two immiscible phases, such as water and air, within the pore spaces of soil (**Figure 2**). At this interface, water molecules are attracted both to each other (**cohesive forces**) and to solid surfaces (**adhesive forces**), forming curved menisci. These menisci generate **capillary pressure** that enables water to move upward (against gravity) from wetter zones to drier zones, where water is held more tightly by the soil matrix.
    """
)

left_co, cent_co, last_co = st.columns((10, 100, 10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/surface_tension_schema.png')
    st.markdown(
        r"**Fig. 2-** Surface tension schema."
    )

st.markdown(
    """   
    **Interfacial tension** $\\sigma_{ik}$, which is constant for a given pair of substances $i$ and $k$, can be understood as the amount of *work* required to overcome the **cohesive forces** between the molecules of each substance. In other words, it's the energy needed to **separate a unit area** of substance $i$ from substance $k$, effectively increasing the surface area of their interface. This force resists separation—and that resistance is what we call **surface tension** (**Figure 3**).
    """
)
    
left_co, cent_co, last_co = st.columns((1, 2, 1))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/surface_tension_bear.png')   
    st.markdown(
        r"**Fig. 3-** Interfacial tension. From Bear, J. (2013)."
    )
    
st.markdown(
    """   
    Molecules at the interface form a thin, *membrane-like* layer (**Figure 4**), that adjusts their geometry to minimize the occupied surface area. The amount of work needed to separate two substances, $W_{ik}$, is given by **Dupré's formula**:
    """
)

st.latex(r"W_{ik} = \sigma_{i} + \sigma_{k} - \sigma_{ik}")

left_co, cent_co, last_co = st.columns((10, 30, 10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/water_strider.jpg')
    st.markdown(
        r"**Fig. 4-** Water strider and the surface tension."
        )

st.markdown(
    """
     At equilibrium, the **contact angle** $\\theta$ between a liquid and a solid is defined by **Young's equation**:
    """
    )

st.latex(r"cos \theta = \frac{\sigma_{SG} - \sigma_{SL}}{\sigma_{GL}}")

st.markdown(
    """    
    Here, $\\sigma_{SG}$ is the solid–gas surface tension, $\\sigma_{SL}$ is the solid–liquid surface tension, and $\\sigma_{GL}$ is the liquid–gas surface tension.

    When $\\theta < 90^{\\circ}$, the liquid wets the surface and spreads out—it’s called a **wetting fluid** (adhesive forces dominate and the liquid spreads). When $\\theta > 90^{\\circ}$, the liquid does not spread—it’s a **non-wetting fluid** (cohesive forces dominate, and the liquid beads up forming droplets).

    In immiscible fluids, surface tension (**Figure 2**) plays an important role, introducing a key parameter: capillary pressure (also called capillary suction, $\\psi$), which is influenced by the soil-water content.
            
    :point_right: To learn more about surface tension, check this [video](https://www.youtube.com/watch?v=zMzqiAuOSz0) :clapper:
    """
)
    
#-----------------------------------------------#
# CAPILLARY PRESSURE                            #
#-----------------------------------------------#
st.markdown(
    """
    ### Capillary pressure

    **Capillary pressure** is the pressure difference between the non-wetting fluid and the wetting fluid. **Young–Laplace** equation relates capillary pressure to medium and fluid properties and to the degree of saturations as follows,
     """
)

st.latex(r"P_{c} = \frac{2\sigma cos\theta}{r}")

st.markdown(
    """
    Where $P_{c}$ is the capillary pressure (also called capillary suction); $\\sigma$ is surface tension of the liquid; $\\theta$ is the contact angle between liquid and solid; and $r$ is the radius of the curvature of the meniscus (effectively, pore radius). A **decrease in meniscus radius** ($r$) corresponds to an **increase in capillary pressure** ($P_{c}$): when a water-saturated soil drains, the water retreats into **smaller pores**, where it is held more tightly. This happens because **smaller pores have a higher surface-area-to-volume ratio**, meaning a greater proportion of the water is in contact with the solid surface. This amplifies surface tension effects, resulting in **stronger capillary forces** that resist gravity-driven drainage. On the other hand, an **increase in meniscus radius** corresponds to a **decrease in capillary pressure**: during imbibition, the wetting fluid advances into larger pores and displaces a nonwetting fluid by capillary forces alone. 
    
    The curvature of each meniscus reflects the local capillary pressure, which depends on the size and shape of the pore — the smallest radius of curvature occurs in the narrowest pores. As a result, draining smaller pores requires higher capillary pressures (more negative), while larger pores drain at lower capillary pressures. 
 
    When no water is entering or leaving the system, **capillary forces continue to act**: they pull water into and retain it within smaller pores. In fact, the **capillary suction in these fine pores is strong enough to hold the water against gravity**, which is why water can remain suspended in the soil even after drainage has stopped. Capillary pressure stops moving water upward into smaller pores when the capillary potential is balanced by other forces, primarily gravitational potential and matric potential.
        
    The relationship between the capillary pressure and saturations of two fluid phases that occupy the pores in the unsaturated zone, is known as the **retention curve**.
    
    :point_right: To know more about suction in capillary tubes, check this [video](https://www.youtube.com/watch?v=9gm81GghMrk) :clapper:
    """
)

st.markdown(
    """    
    ### Retention curve
    
    Retention curves—also known as capillary pressure curves—are graphical representations of the relationship between soil saturation and capillary pressure, showing how water is retained in the soil by capillary forces against gravity. Their shape depends on the soil material and the initial water distribution. These graphs show that as saturation decreases (such as during drainage), capillary pressure increases, which leads to a decrease in the interfacial surface area. On the other hand, when saturation increases (such as during imbibition), capillary pressure decreases, resulting in an increase in the interfacial surface area. 
    
    In **Figure 5**, we summarize some of the key concepts that retention curves can describe. The horizontal axis represents the **saturation level** (or **volumetric water content**) of the soil ($\\theta_{w}$), and the vertical axis shows the **capillary pressure head** ($h_{c}$). The two curves represent two different types of soil: a well-graded (heterogeneous) soil and a poorly-graded (homogeneous) soil.
    
     Point A on the poorly-graded soil curve indicates the **threshold capillary pressure head**—also known as the **entry pressure**. This represents the minimum pressure required for a non-wetting fluid (e.g., air or oil) to begin displacing the wetting fluid (typically water) and enter the largest pores of the soil once it has reached equilibrium in the process of drainage from saturation. As shown, this threshold can be reached with only a slight reduction in water content. The region between the water table (where capillary pressure is zero) and the point defined by the entry pressure is known as the **capillary fringe** (see also Figure 1a). This zone is nearly saturated, but the water is under negative pressure (suction).
    """
)

left_co, cent_co, last_co = st.columns((10, 50, 10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/retention_curve_mod.png')
    st.markdown(
    r"**Fig. 5-** Example of a retention curve for two types of soil, modified from Bear and Cheng (2010)."
    )

st.markdown(
    """ 
    Each soil type has its own **field capacity** ($\\theta_{fc}$), **wilting point** ($\\theta_{wp}$) and **residual water content** ($\\theta_{r}$). **Field capacity** is the water content of soil at which gravitational drainage has significantly slowed down, typically 2 to 3 days after rain or irrigation has ceased. This point is quantified through laboratory experiments and is typically set at around –100 to –300 cm of pressure head—about -1/10 to -1/3 bar (**Figure 6**). The **wilting point** is the water content at which plants can no longer extract water from the soil, typically around –15000 cm of pressure head—although this value can vary depending on the plant species. At this point, the suction force exerted by the plant roots is weaker than the soil’s water retention forces. As the soil dries beyond the wilting point, the water content approaches an asymptote—meaning that no further water will drain, even if the pressure head continues to decrease. This condition defines the **residual water content**, which refers to the minimum amount of water retained in the soil pores. The difference in water content between field capacity and the wilting point represents the available water for plant uptake.        
    """
)

left_co, cent_co, last_co = st.columns((10, 50, 10))  
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/field_capacity.png')
    st.markdown(
        r"**Fig. 6** – Indices describing the retention curves, where (i) $\theta_{fc}$ is the field capacity; "
        r"(ii) $\theta_{wp}$ represents the wilting point; (iii) $\theta_{r}$ is the residual water content; "
        r"and (iv) $\psi_{a}$ is the entry pressure. Adapted from Stephens, D. B. (2018)."
    )

st.markdown(
    """  
    Different behaviors in interfacial tension and wettability can occur during drainage or imbibition on a solid surface. These pore-scale processes can result in different retention curves for the same soil. A soil that starts fully saturated and undergoes drainage may exhibit a different retention curve than if that same soil starts completely dry and gradually becomes saturated during the imbibition process. As a result, we can observe different water contents for the same pressure value in the same soil, depending on the process the soil is undergoing. This phenomenon is known as **hysteresis**.
      
    :point_right: To know more about hysteresis, check this [video](https://www.youtube.com/watch?v=aaGJS5pAmp4) :clapper:
    """
)


st.markdown("---")

st.markdown(
    """
    ## The Formulation :abacus:
    
    In this following section, we show the constitutive equations that define soil-water retention curve models, specifically focusing on the formulation by [van Genuchten (1980)](https://www.researchgate.net/publication/250125437_A_Closed-form_Equation_for_Predicting_the_Hydraulic_Conductivity_of_Unsaturated_Soils1).
    
    ### Water content, $\\Theta$:
    
    - **Dimensionless water content**
    """
)

st.latex(r"\Theta = \frac{\theta - \theta_{r}}{\theta_{s} - \theta_{r}}")

st.markdown(
    r"""
    where,  

    $\theta$ soil-water content  
    $\theta_{s}$ saturated soil-water content  
    $\theta_{r}$ residual soil-water content  
    """
)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("- **Dimensionless water content related to the pressure head**")
st.latex(r"\Theta = \left[\frac{1}{1 + (\alpha h)^{n}}\right]")

st.markdown(
    r"""
    where,  

    $h$ pressure head, assumed positive
    $\alpha$ related to the inverse of air entry suction
    $n$ measure of pore-size distribution
    """
)


st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("- **By substituting the first equation into the second, we derive the retention curve as**")
st.latex(r"\theta = \theta_{r} + \frac{(\theta_{s} - \theta_{r})}{\left[1 + (\alpha h)^{n}\right]^{m}}, \quad m = 1 - \frac{1}{n}")

st.markdown(
    r"""
    where,  
    
    $m = 1 - \frac{1}{n}$ m controls the curvature or steepness of the soil-water retention curve
    """
)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Relative Hydraulic Conductivity, $K_{r}$:")
st.markdown("- **Relative Hydraulic Conductivity expressed in terms of the pressure head**")
st.latex(r"K_{r}(h) = \frac{\{ 1 - (\alpha h)^{n-1} \left[ 1 + (\alpha h)^{n} \right]^{-m} \}^{2}}{\left[1 + (\alpha h)^{n}\right]^{m/2}}, \quad m = 1 - \frac{1}{n}")

st.markdown("<br><br>", unsafe_allow_html=True)
# st.markdown("---")
st.markdown("- **Relative Hydraulic Conductivity expressed in terms of the dimensionless water content**")
st.latex(r"K_{r}(\Theta) = \Theta^{1/2} \left[1 - \left(1 - \Theta^{1/m}\right)^{m} \right]^{2}, \quad m = 1 - \frac{1}{n}, \quad 0 > m > 1")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Diffusivity, $D$:")
st.latex(r"D(\Theta) = \frac{(1 - m)K_s}{\alpha m (\theta_{s} - \theta_{r})} \Theta^{1/2 - 1/m} \left[\left( 1 - \Theta^{1/m} \right)^{-m} + \left( 1 - \Theta^{1/m} \right)^{m} - 2 \right]")


st.markdown(
    r"""
    where,  
    
    $K_{s}$ hydraulic conductivity at saturation, $K/K_{r}$
    """
)


"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_📈_▶️ The SWC interactive.py")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/CC_BY-SA_icon.png')
    
st.markdown('<span style="font-size: 15px;">*The online version of soilwaterretention is copyrighted by the author and distributed by* The Groundwater Project. *Please use* gw-project.org *links when you want to share* Groundwater Project *materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others.*</span>', 
            unsafe_allow_html=True)
