**Getting Started with the Interactive Plot**
 
Before starting the exercise, it is helpful to follow these steps to explore GHB behavior (you may want to use the toggle switch to allow number rather than slider input):

**1) Start with $H_{B}$ = 8 m, $h_{gw}$ = 10 m, and $C_{B}$ = 1x10⁻² m²/s**

* Vary **groundwater head $h_{gw}$** and observe how **flow $Q_B$** changes in magnitude and direction.  
 * Use the slider to vary $C_B$ and notice how the **slope of the $Q$–$h$ curve** changes.
 * Toggle “Compute conductance” then enter values for $K$, $A_B$, and $L_B$ to calculate $C_B=\frac{KA_B}{L_B}$ and notice how the **slope of the $Q$–$h$ curve** changes.
 
**2) Consider the Role of Head-Dependent Boundaries in Applied Groundwater Modeling**
 
Depending on the modeling objective, head-dependent boundaries like GHB can be considered in two different ways, delineated under (a) and (b) here.
 
**a) During Model Calibration or Setup:** Assume that the discharge is known from field data (so the recharge is determined by dividing the discharge by the surface area of the model) and the general head boundary is the only outlet of the model. Then, given head values in the groundwater system, the values of hydraulic conductivity and GHB conductance can be calibrated. **This situation is discussed in the introduction** and can be accessed by clicking on the **:red[📕 Introduction] button** on the left menu, then scrolling down and choosing **Show the :rainbow[interactive] plot for Scenario 1**, then scrolling down below the plot to open the :green[**Instructions**] and finally **scrolling down to Step 5a**.
 
**b) After the model is calibrated such that the hydraulic conductivity, recharge, and river bed conductance are specified:** If other outlets are added to the system (e.g., abstraction wells, drains) the heads in the model will be a result of all the model boundary conditions and parameter values. In consequence, the previously calibrated, and then specified, conductance will control how much of the recharge flows to the :orange[**GHB**] boundary. The discharge will also depend on the location and properties of the other outlets. Here we investigate this behavior for the :orange[**General Head Boundary GHB**]. Other head dependent boundaries like :violet[**RIV**] and :green[**DRN**] follow similar principles.
    
The subsequent exercise is designed to help you build intuition for how GHB parameters control flow.  Feel free to further investigate the interactive plot on your own.