import streamlit as st

st.header('Content')

st.markdown(
    """
    ### Overview about the interactive tools associated to the book chapter
    Book Chapter
    
    1. **Review of saturated flow - hydrostatic and 1D steady state**
    * a. Head distribution in a bucket full of water
    * b. Head distribution in a bucket full of sand - hydrostatic
    * c. Head distribution in a bucket full of sand - steady state, Type I top and bottom, homogeneous
    * d. Head distribution in a bucket full of sand - steady state, Type II top and Type I bottom, homogeneous
    * e. Head distribution in a bucket full of sand - steady state, Type II top and Type I bottom, heterogeneous
    * f. Horizontal, steady state, Type II left and Type I right
    * g. Horizontal, steady state, Type II left and Type I right - use to explain unconfined condition, nonlinearity
    2. **Review of saturated flow** - 1D transient
    * a Head distribution in a bucket full of sand - transient between steady states, Type I top and bottom, homogeneous
    * b Head distribution in a bucket full of sand - transient between steady states, Type II top and Type I bottom, homogeneous
    * c Horizontal, 1D, Type II left and Type I right - use to explain confined aquifer response to pumping
    * dHorizontal, 1D, Type II left and Type I right - use to explain unconfined aquifer response to pumping
    3. **Review of saturated flow - 2D**
    * a Head distribution in a bucket full of sand - steady state, 2D from a point, spreading and symmetry
    4. Review of transport during steady state 1D saturated flow    
    * a Pulse release, advection only
    * b Pulse release, advection, diffusion, dispersion
    * c Pulse release, retardation
    * d Pulse release, add decay
    5. Unsaturated flow - hydrostatic
    * a Head distribution in a bucket full of sand - hydrostatic, zero pressure at base - soil type
    * b Head distribution in a bucket full of sand - hydrostatic, zero pressure at base - change in length of water between two steady state water table depths
    * c Head distribution in a bucket full of sand - hydrostatic, zero pressure at base - reduced storage due to shallow water table
    6. Unsaturated flow - 1D steady state    
    * a Unit gradient flow
    * b Head distribution in a bucket full of sand - steady state, Type I top and bottom, homogeneous
    * c Head distribution in a bucket full of sand - steady state, Type II top and Type I bottom, homogeneous
    * d Head distribution in a bucket full of sand - steady state, Type II top and Type I bottom, heterogeneous
    * e Horizontal, steady state, Type II left and Type I right, nonlinearity, nonzero flow in capillary fringe
    * f Horizontal, steady state, Type II left and Type I right 
    7. Unsaturated flow 1D transient    
    * a Sharp wetting front
    * b Internal drainage with free draining bottom boundary
    * c Full Richards solution between steady states - infiltration vs time from constant head
    * d Full Richards solution between steady states - smooth wetting fronts
    8. Unsaturated flow - 2D    
    * a Head distribution in a bucket full of sand - steady state, 2D from a point, spreading and symmetry
    9. Special topics in unsaturated flow
    * a Evaporation
    * b Root uptake
    * c Structured (dual porosity) soils
    10. Transport during steady state 1D unsaturated flow    
    * a Pulse release, advection only - effect of water content on velocity
    * b Pulse release, advection, diffusion, dispersion - effect of water content on dispersivity
    * c Pulse release, retardation - effect of partial saturation on retardation/sorption
    * d Pulse release, add decay - effect of partial saturation on decay
"""
)
