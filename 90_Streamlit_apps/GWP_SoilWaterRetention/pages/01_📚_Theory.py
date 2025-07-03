import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import json
from streamlit_book import multiple_choice

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

# FUNCTIONS
def m_val(n):
    """Function that returns the value of "m"
    Parameters
    ----------
    n : float
        value of "n"
    Returns
    -------
    float
        value of "m"
    """
    m = 1 - (1/n)
    return m


def water_content(alpha, h, n):  
    """Function that calculates the water content.  
    Based on van Genuchten, 1980 (Eq. 3)
    Parameters
    ----------
    alpha : float
        alpha parameter
    h : float
        head pressure (positive)
    n : float
        n parameter
    Returns
    -------
    float
        water content
    """  
    T = ((1 + (alpha*h)**(n)))**(-(m_val(n)))  
    return T

def soil_water_content(tr, ts, alpha, h, n):
    """Function that calculates the soil-water content. 
    Based on van Genuchten, 1980 (Eq. 21)
    Parameters
    ----------
    tr : float
        residual values of soil-water content
    ts : float
        saturated values of soil-water content
    alpha : float
        alpha parameter
    n : float
        n parameter  
    Returns
    -------
    float
        soil-water content
    """
    t = tr + ((ts - tr) / ((1 + (alpha*h)**(n))**m_val(n)))   

    return t  

def relative_hydraulic_conductivity(alpha, n, h, T):
    """Function that calculates the relative hydraulic conductivity. 
    Based on van Genuchten, 1980 (Eq. 8 and 9).
    Parameters
    ----------
    alpha : float
        alpha parameter
    n : float
        n parameter
    h : float 
        head pressure (positive)
    T : float
        water content
    Returns
    -------
    T: float
        _description_
    Kr_T: float
        relative hydraulic conductivity expressed in terms of the dimensionless water content
    Kr_h: float
        relative hydraulic conductivity expressed in terms of the head pressure   
    Raises
    ------
    ValueError
        If m value is not between 0 and 1
    """
    
    # Check that m_val(n) is within the expected range
    if not (0 < m_val(n) < 1):
        raise ValueError("Parameter 'm' out of range: must be between 0 and 1")

    #-- Relative hydraulic conductivity expressed in terms of the water content
    Y = (1 - T**(1 / m_val(n)))**m_val(n)
    Kr_T = T**0.5 * (1 - Y)**2                     
    
    #-- Relative hydraulic conductivity expressed in terms of the pressure head
    I = (1 - alpha * h)
    U = I**(n - 1)
    P = (1 + (alpha * h)**n)**(m_val(n) / 2)
    
    if I > 0:
        Kr_h = ((U * T)**2) / P 
    else:
        Kr_h = np.nan                        
    
    return Kr_T, Kr_h

def soil_water_diffusivity(Ks, n, ts, tr, T):
    """Function that calculates the soil water diffusivity.
    Based on van Genuchten, 1980 (Eq. 11).
    Parameters
    ----------
    Ks : float
        hydraulic conductivity at saturation
    n  : float
        n parameter
    ts : float
        satured soil-water content
    tr : float
        residual soil-water content
    T : float
        dimensionless water content
    Returns
    -------
    D_T : float
        soil water diffusivity
    """  
    I = ((1 - m_val(n))*Ks) / (alpha*m_val(n)*(ts - tr))
    L = T**(0.5 - (1/m_val(n)))
    Y = (1 - T**(1 / m_val(n)))**m_val(n)
    P = ((1/Y) + (Y) - 2)
    
    D_T = I * L * P                                        

    return D_T
    
def render_assessment(filename, title="📋 Assessment", max_questions=4):

    with open(filename, "r", encoding="utf-8") as f:
        questions = json.load(f)

    st.markdown(f"#### {title}")
    for idx in range(0, min(len(questions), max_questions), 2):
        col1, col2 = st.columns(2)
        for col, i in zip((col1, col2), (idx, idx+1)):
            if i < len(questions):
                with col:
                    q = questions[i]
                    st.markdown(f"**Q{i+1}. {q['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=q["options"],
                        success=q.get("success", "✅ Correct."),
                        error=q.get("error", "❌ Not quite.")
                    )

videourl1 = 'https://youtu.be/zMzqiAuOSz0'
videourl2 = 'https://youtu.be/9gm81GghMrk'
videourl3 = 'https://youtu.be/aaGJS5pAmp4'

st.title('📚 Theory underlying SoilWaterRetention')
st.header('The concepts 📖')
#-----------------------------------------------#
# UNSATURATED ZONE                              #
#-----------------------------------------------#
st.subheader(':blue-background[An initial overview about the unsaturated Zone]', divider = 'blue')
st.markdown("""
#### 💡 Motivation and Introducuion

- Why does water cling to tiny pores in soil and resist gravity?  
- What makes sandy soils drain quickly while clay holds on to every drop?  
- How can we translate invisible capillary forces into meaningful quantities for water management?

This section of the module covers the physics behind water in unsaturated soils. You’ll explore how surface tension, wettability, and capillary pressure shape the movement and retention of water — and why these principles are foundational in hydrology, agriculture, and groundwater modeling. By understanding these mechanisms, you’ll be better equipped to predict infiltration, plant water availability, and the impact of soil texture on water storage and movement within the **unsaturates zone**.

In contrast to the *Saturated Zone*, where the porous medium is fully saturated with a single fluid of uniform properties (density, viscosity, and composition), the **Unsaturated Zone** contains—at least—two immiscible fluids that coexist: a wetting and non-wetting, such as water and air, respectively (**Figure 1a**). As shown in **Figure 1b**, the moisture content in the *Unsaturated Zone* is therefore less than 100%. The pressure head under saturated conditions is greater than one, equal to zero at the groundwater table, and negative in the unsaturated zone (**Figure 1c**).
""")

left_co, cent_co, last_co = st.columns((10, 80, 10))
with cent_co:
    st.image('90_Streamlit_apps/GWP_SoilWaterRetention/assets/images/freeze_cherry_2.png')
    st.markdown(
        r"Fig. 1- Groundwater conditions near the ground surface. (a) Saturated and unsaturated zone; (b) profile of moisture content versus depth; (c) pressure-head and. Adapted from Freeze and Cherry (1979)"
    )
st.markdown("""
#### 🎯 Learning Objectives – Theory module

By the end of this section, you will be able to:

- Explain the physical origin of surface tension and wettability and their influence on water behavior in soil pores.
- Describe the concept of capillary pressure and its relationship with pore size and water retention.
- Acknowledge the van Genuchten’s formulation to calculate water content, hydraulic conductivity, and diffusivity.
- Distinguish between water content, relative conductivity, and diffusivity — and understand how they change with soil texture.
- Recognize how unsaturated zone theory underpins applications in irrigation, groundwater recharge, and soil management.
""")
#-----------------------------------------------#
# SURFACE TENSION AND WETTABILITY               #
#-----------------------------------------------#
st.subheader('Surface tension and wettability', divider = 'blue')
st.markdown(
    """
    Why can water rise in fine soil pores, defying gravity? What determines whether water spreads over grains or retreats into droplets?
    
    At the pore scale, curved fluid interfaces form due to cohesive and adhesive forces, creating menisci that generate capillary pressure. Wettability — governed by surface tension and contact angle — controls how water enters, moves through, and is retained in the unsaturated soil.
    """
)
with st.expander(':rainbow[**Click here to read more about the theoretical aspects of surface tension and wettability**]'):
    st.markdown(
        """
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
                
        :point_right: To learn more about surface tension, check the following video [direct link](https://www.youtube.com/watch?v=zMzqiAuOSz0) :clapper:
        """
    )
    
    st.video(videourl1) 

with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/theory_ass_01.json", title="Surface tension and wettability – self assessment")
    
#-----------------------------------------------#
# CAPILLARY PRESSURE                            #
#-----------------------------------------------#
st.subheader('Capillary pressure', divider = 'blue')
st.markdown(
    """
    Why does water in soil remain suspended in fine pores—even after rainfall stops? What governs the resistance to drainage and the movement of moisture against gravity?
    
    Capillary pressure arises from the curvature of fluid interfaces in soil pores and plays a central role in determining how water is retained, redistributed, and drained in the unsaturated zone.
     """
)
with st.expander(':rainbow[**Click here to read more about the theoretical aspects of capillary pressure**]'):
    st.markdown(
        """
        **Capillary pressure** is the pressure difference between the non-wetting fluid and the wetting fluid. **Young–Laplace** equation relates capillary pressure to medium and fluid properties and to the degree of saturations as follows,
         """
    )
    
    st.latex(r"P_{c} = \frac{2\sigma cos\theta}{r}")
    
    st.markdown(
        """
        Where $P_{c}$ is the capillary pressure (also called capillary suction); $\\sigma$ is surface tension of the liquid; $\\theta$ is the contact angle between liquid and solid; and $r$ is the radius of the curvature of the meniscus (effectively, pore radius). The following interactive figure visualizes capillary rise based on the Young–Laplace equation.
        """
    )
    
    # PLOT CAPILlARY RISE
    
    lc0, rc0 = st.columns((2,1), gap="large")
    
    # Constants
    sigma = 0.072  # Surface tension of water [N/m]
    theta = 0      # Contact angle [radians] for complete wetting
    cos_theta = np.cos(theta)
    rho = 1000     # Density of water [kg/m^3]
    g = 9.81       # Gravitational acceleration [m/s^2]
    
    
    # Slider to choose radius in micrometers
    with lc0:
        st.markdown("""
        With the following slider you can modify the pore radius (_you can also use the left/right arrow keys on your keyboard_).
        
        The plot illustrates the capillary rise. See what happens if you increase and decrease the pore radius.
        """)
        r_mm = st.slider("Pore radius (mm)", min_value=0.005, max_value=1.5, value=0.2, step=0.005, format="%.3f")
    
    # Calculate capillary rise height in meters
    h_m = (2 * sigma * cos_theta) / (r_mm * 1e-3 * rho * g)
    
    # Plot setup
    fig, ax = plt.subplots(figsize=(4, 5))
    x = [-r_mm, r_mm]
    y = [0, h_m]
    
    # Fill capillary rise area
    ax.fill_betweenx([0, h_m], -r_mm, r_mm, color='blue', alpha=0.6, label=f'Capillary rise = {h_m*100:.1f} cm')
    
    # Tube walls
    ax.axvline(x=-r_mm, color='grey')
    ax.axvline(x= r_mm, color='grey')
    
    # Axes and labels
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, max(1, h_m*1.2))
    ax.tick_params(axis='both', labelsize=14)
    ax.set_xlabel("Tube cross-section (mm)", fontsize = 14)
    ax.set_ylabel("Capillary rise height (m)", fontsize = 14)
    ax.set_title("Capillary Rise vs. Tube Radius", fontsize = 16)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.1), borderaxespad=0, ncol=1, frameon=False, fontsize = 14)   
    
    with rc0:
        st.pyplot(fig)
        
    st.markdown(
        """
        A **decrease in meniscus radius** ($r$) corresponds to an **increase in capillary pressure** ($P_{c}$): when a water-saturated soil drains, the water retreats into **smaller pores**, where it is held more tightly. This happens because **smaller pores have a higher surface-area-to-volume ratio**, meaning a greater proportion of the water is in contact with the solid surface. This amplifies surface tension effects, resulting in **stronger capillary forces** that resist gravity-driven drainage. On the other hand, an **increase in meniscus radius** corresponds to a **decrease in capillary pressure**: during imbibition, the wetting fluid advances into larger pores and displaces a nonwetting fluid by capillary forces alone. 
        
        The curvature of each meniscus reflects the local capillary pressure, which depends on the size and shape of the pore — the smallest radius of curvature occurs in the narrowest pores. As a result, draining smaller pores requires higher capillary pressures (more negative), while larger pores drain at lower capillary pressures. 
     
        When no water is entering or leaving the system, **capillary forces continue to act**: they pull water into and retain it within smaller pores. In fact, the **capillary suction in these fine pores is strong enough to hold the water against gravity**, which is why water can remain suspended in the soil even after drainage has stopped. Capillary pressure stops moving water upward into smaller pores when the capillary potential is balanced by other forces, primarily gravitational potential and matric potential.
            
        The relationship between the capillary pressure and saturations of two fluid phases that occupy the pores in the unsaturated zone, is known as the **retention curve**.
        
        :point_right: To know more about suction in capillary tubes, check the following video [direct link](https://www.youtube.com/watch?v=9gm81GghMrk) :clapper:
        """
    )
       
    st.video(videourl2)
    
with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/theory_ass_02.json", title="Capillary pressure – self assessment")
    
#-----------------------------------------------#
# Retention curve                               #
#-----------------------------------------------#
st.subheader('Retention curve', divider = 'blue')
st.markdown(
    """ 
    How much water remains in the soil after infiltration? When does it become unavailable to plants?
    
    The soil water retention curve links water content to capillary suction — revealing how strongly water is held, how much is available, and when it becomes inaccessible. Understanding this curve is key to managing irrigation, estimating recharge, and predicting plant water stress.
    """
)
with st.expander(':rainbow[**Click here to read more about the theoretical aspects of the retention curve**]'):
    st.markdown(
        """
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
          
        :point_right: To know more about hysteresis, check the following video [direct link](https://www.youtube.com/watch?v=aaGJS5pAmp4) :clapper:
        """
    )
    st.video(videourl3)
    
with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/theory_ass_03.json", title="Capillary pressure – self assessment")
    
st.subheader("Applications in Agriculture 🌱", divider="blue")
st.markdown("""
    Understanding the soil water retention curve is essential for effective **irrigation planning**, **crop management**, and **drought risk assessment**. Key agricultural concepts includes **Field capacity, Permanent Wilting Point, and more.
    """
)

with st.expander(':rainbow[**Click here to read more about the applications in agriculture**]'):
    st.markdown("""
    
    - **Field Capacity ($\\theta_{fc}$)**  
      The water content at which excess gravitational water has drained and the soil holds water against gravity. Typically defined at a pressure head of –100 to –300 cm.
    
    - **Permanent Wilting Point ($\\theta_{wp}$)**  
      The lower limit of plant-available water. Below this moisture level, plants cannot exert enough suction to extract water from the soil. Defined at around –15,000 cm of pressure head.
    
    - **effective Field capacity**
      
      The difference between field capacity and wilting point, sometimes also refered to as Available Water Capacity (AWC)
      $$
      \\text{eFC} = \\theta_{fc} - \\theta_{wp}
      $$  
      This is the amount of water accessible to plants.
    
    These quantities help farmers and agronomists optimize irrigation schedules, improve yield, and prevent water stress. They also aid in designing retention strategies for drought-resilient agriculture.
    """)

with st.expander('🧠 **Show some questions for self-assessment** - to assess your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/theory_ass_04.json", title="Capillary pressure – self assessment")
    
#-----------------------------------------------#
# The formulation                               #
#-----------------------------------------------#

st.header('The Formulation :abacus:')

st.markdown(
    """
    In this section, we introduce key parameters that describe how water behaves in unsaturated soils. We have a closer look on **Water content ($\\theta$)**, **Relative hydraulic conductivity ($K_r$)**, **Hydraulic diffusivity ($D$)**. Together, these functions define the **soil water retention behavior** and are central to solving flow and transport equations in the vadose zone.
    """
)

st.subheader('Parameters and Equations', divider = 'blue')
st.markdown(
    """
    #### Water content
    
    Tells us *how much water* is present in the soil at a given time. It's essential for quantifying storage, plant availability, and evaporation potential.
    """
)
with st.expander("**Click here to see further details**"):
    st.markdown(
        """       
        It is required to derive a relationship between water content and pressure head. To interpret the retention and conductivity functions, it's important to understand the physical meaning of the involved parameters, accordingly, you will find some definition and explanation next to the used parameters.
        
        **Water content**
        
        Water content refers to the volume of water $V_w$ held in the soil per unit volume of soil $V_t$. It is expressed as:
        """
    )
    st.latex(r"\theta = \frac{V_w}{V_t}")
    st.markdown(
        """
        In the context of unsaturated soils, $\\theta$ ranges between the residual water content ($\\theta_r$), below which water is no longer mobile or plant-accessible, and the saturated water content ($\\theta_s$), where all pores are filled with water.
        
        Understanding how $\\theta$ varies with pressure head or suction is key to modeling soil-water behavior, especially for predicting plant-available water and infiltration dynamics. The van Genuchten model describes this relationship through a nonlinear function known as the retention curve.

        **Dimensionless Water Content**
        
        The dimensionless water content **$\\Theta$** is a normalized form of water content between 0 and 1:
        """
    )
    st.latex(r"\Theta = \frac{\theta - \theta_{r}}{\theta_{s} - \theta_{r}}")
    
    st.markdown(
        """
        where,  
        
        - **$\\theta_{s}$** (*Saturated water content*): The maximum volumetric water content the soil can hold; corresponds to fully saturated pores.
    
        - **$\\theta_{r}$** (*Residual water content*): The minimum water content remaining in the soil after extensive drying—water is held tightly and is unavailable to plants.
    
         - **$\\theta$** (*Water content*): The actual volumetric water content under current conditions.
    
    
        **Dimensionless water content related to the pressure head**
        """
    )
    st.latex(r"\Theta = \left[\frac{1}{1 + (\alpha h)^{n}}\right]")
    
    st.markdown(
        """
        where,  
    
        - **$h$** (*Pressure head*): Describes the suction required to remove water from the soil; positive in the unsaturated zone, expressed in cm of water.
        - **$\\alpha$** (*Inverse of air-entry suction*): Controls when the largest pores begin to drain. Larger $\\alpha$ values indicate coarser soils that release water at lower suction.
        - **$n$** (*Pore size distribution*): A shape parameter reflecting how evenly pore sizes are distributed. Higher values mean a narrower distribution of pore sizes.
    
        By substituting the first equation into the second, we derive the Soil Water Retention Curve as
        """
    )
    
    st.latex(r"\theta = \theta_{r} + \frac{(\theta_{s} - \theta_{r})}{\left[1 + (\alpha h)^{n}\right]^{m}}")
    
    st.markdown(
        """
        where,  
        
        - **$m$** (*Model exponent*): Given by $m = 1 - \\frac{1}{n}$, this controls the steepness of the retention curve.
        
        The parameter $m$ controls the curvature or steepness of the soil-water retention curve.
        
        The SWRC finally allows to related water content with pressure head, and is essential to describe the soil water in the unsaturated zone.
        """
    )

st.markdown(
    """
    #### Relative Hydraulic Conductivity $K_{r}$
    
    Describes *how easily water moves* through unsaturated soil. It decreases as the soil dries and is critical for modeling infiltration, drainage, and irrigation performance.
    """
)
with st.expander("**Click here to see further details**"):
    st.markdown(
    """ 
    **Relative Hydraulic Conductivity expressed in terms of the pressure head**
    """
    )
    st.latex(r"K_{r}(h) = \frac{\{ 1 - (\alpha h)^{n-1} \left[ 1 + (\alpha h)^{n} \right]^{-m} \}^{2}}{\left[1 + (\alpha h)^{n}\right]^{m/2}}")
    
    st.markdown(
        """
        **Relative Hydraulic Conductivity expressed in terms of the dimensionless water content**
        """
    )
    
    st.latex(r"K_{r}(\Theta) = \Theta^{1/2} \left[1 - \left(1 - \Theta^{1/m}\right)^{m} \right]^{2}, \quad m = 1 - \frac{1}{n}, \quad 0 > m > 1")

st.markdown(
    """
    #### Hydraulic Diffusivity $D$
    
    The hydraulic diffusivity **$D(\\Theta)$** describes how water content gradients propagate through soil over time. It combines changes in water content and conductivity to capture how *quickly moisture redistributes* in the soil. It governs the speed of drying or wetting fronts.
    """
)
with st.expander("**Click here to see further details**"):
    st.latex(r"D(\Theta) = \frac{(1 - m)K_s}{\alpha m (\theta_{s} - \theta_{r})} \Theta^{1/2 - 1/m} \left[\left( 1 - \Theta^{1/m} \right)^{-m} + \left( 1 - \Theta^{1/m} \right)^{m} - 2 \right]")
    
    st.markdown(
        """
        where,  
        
        - **$K_s$** (*Saturated hydraulic conductivity*): The rate at which water moves through fully saturated soil, expressed in cm/day or mm/h.
        - **$K_r$** (*Relative hydraulic conductivity*): The fraction of $K_s$ available under current moisture conditions. Two equivalent expressions exist: in terms of $\\Theta$ and in terms of $h$.
        """
    )
    
    st.subheader('Vizualisation of the relationsships for different soil materials', divider = 'blue')
st.markdown(
    """       
    The subsequent plots show the relationships between the different measures. You can choose to plot the relationsships for different soil materials.
    """
)
columns = st.columns((2,1), gap = 'large')
with columns[0]:
    st.markdown(""" 
            The plots illustrate the soil water retention curve and the relationships between water content, hydraulic conductivity, and diffusivity based on :blue-background[[van Genuchten (1980)](https://www.researchgate.net/publication/250125437_A_Closed-form_Equation_for_Predicting_the_Hydraulic_Conductivity_of_Unsaturated_Soils1)].
"""
)

# Three different soils, incl. th example from Van Genuchten 1980

soil_profiles = {
"Loam (default, from Van Genuchten (1980))": {
"θr": 0.10,
"θs": 0.50,
"α": 0.005,
"n": 2.0,
"Ks": 100,
"color": "orange"
},
"Sand": {
"θr": 0.05,
"θs": 0.40,
"α": 0.035,
"n": 2.7,
"Ks": 500,
"color": "green"
},
"Clay": {
"θr": 0.12,
"θs": 0.56,
"α": 0.001,
"n": 1.3,
"Ks": 10,
"color": "red"
}
}

with columns[1]:
    # Selection of dataset
    selected_profile = st.selectbox("Select soil type", list(soil_profiles.keys()))
    params = soil_profiles[selected_profile]
    color = params["color"]

tr = params["θr"]
ts = params["θs"]
alpha = params["α"]
n = params["n"]
Ks = params["Ks"]

#-- Generate pressure head values:
h_values = np.logspace(0, 6, 100)  

#-- Calculate water content values
t_values = [soil_water_content(tr, ts, alpha, h, n) for h in h_values]
T_values = [water_content(alpha, h, n) for h in h_values]

#-- Calculate dimensionless water content and relative hydraulic conductivity
Kr_T, Kr_h = zip(*[relative_hydraulic_conductivity(alpha, n, h, T) for h, T in zip(h_values, T_values)])
Kr_T = list(Kr_T)  
Kr_h = list(Kr_h) 

#-- Calculate the soil-water diffusivity
D_T = [soil_water_diffusivity(Ks, n, ts, tr, T) for T in T_values]

#-- Plot the 3 figures
#fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 5))
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(9, 3), constrained_layout=True)

# ax1: Water content vs. Pressure head
ax1.plot(t_values, np.abs(h_values),color=color, label=selected_profile)
ax1.set_xlim(0, 0.6)
ax1.set_ylim(np.abs(h_values[0]), np.abs(h_values[-1]))
ax1.set_yscale('log')
ax1.set_xlabel(r'Water Content, $\Theta$')
ax1.set_ylabel(r'Pressure Head, $h$ [cm]')

# ax2: Water content vs. Relative Hydraulic Conductivity expressed in terms of water content
ax2.plot(t_values, Kr_T,color=color, label=selected_profile) 
ax2.set_yscale('log')
ax2.set_ylim(0.000001, 1)
ax2.set_xlim(0, 0.6)
ax2.set_xlabel(r'Water Content, $\Theta$')
ax2.set_ylabel(r'Relative Hydraulic Conductivity, $K_{r}$($\Theta$)')

# ax2: Water content vs. Relative Hydraulic Conductivity expressed in terms of pressure head
ax3.plot(np.abs(h_values), Kr_T,color=color, label=selected_profile) 
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlim(1, 10000)
ax3.set_ylim(0.000001, 1)
ax3.set_xlabel('Pressure Head, $h$ [cm] ')
ax3.set_ylabel(r'Relative Hydraulic Conductivity, $K_{r}($h$)$')

# ax4: Water content vs. Diffusivity
ax4.plot(t_values, D_T,color=color, label=selected_profile)
ax4.set_xlim(0, 0.6)
ax4.set_yscale('log')
ax4.set_ylim(1, 1000000)
ax4.set_xlabel(r'Water Content, $\Theta$')
ax4.set_ylabel(r'Diffusivity, $D$')

#plt.tight_layout()
st.pyplot(fig)

st.subheader('🧾 Conclusion and Final Assessment', divider = 'blue')
st.markdown("""
    Understanding the physical principles of soil water retention is essential for quantifying water availability in unsaturated soils. Concepts such as capillarity, wettability, and retention curves provide the theoretical backbone for modeling water movement and storage. This foundation prepares you to interpret real-world soil behavior and to apply mathematical models with confidence and clarity.
    """
)

with st.expander('🧠 **Show the final assessment** - to evaluate your understanding'):
    render_assessment("90_Streamlit_apps/GWP_SoilWaterRetention/assets/questions/theory_ass_05.json", title="Theory section - final assessment", max_questions=6)

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_📈_The SWRC interactive.py")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
    
st.markdown('<span style="font-size: 15px;">*The online version of soilwaterretention is copyrighted by the author and distributed by* The Groundwater Project. *Please use* gw-project.org *links when you want to share* Groundwater Project *materials with others. It is not permissible to make GW-Project documents available on other websites nor to send copies of the files directly to others.*</span>', 
            unsafe_allow_html=True)
