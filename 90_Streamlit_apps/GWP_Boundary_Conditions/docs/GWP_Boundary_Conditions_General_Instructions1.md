**Getting Started with the Interactive Plot** Instructions for :green[**Scenario 1**]: Exploring Model Behavior and _Q_-_h_ Relationships

Use the interactive tools in :green[**Scenario 1**] to investigate how model parameters and boundary conditions affect hydraulic head distributions and boundary flows. Follow the steps below to explore key relationships and system behavior.

**1. Modify Model Parameters**
- Open the INPUT CONTROLS and click "Click to Modify Model Parameters".
- Begin by increasing (or decreasing) the Recharge rate.
- Observe how the hydraulic head distribution changes throughout the domain.
- Next, adjust the Hydraulic Conductivity (K):
   - 🔽 Lower values result in steeper gradients due to the reduced transmissivity (As K is decreased: for positive recharge, heads rise and for negative recharge heads decline).
   - 🔼 Higher values result in lower gradients due to increased transmissivity (As K is increased: for positive recharge, heads decline and for negative recharge heads rise).
- Proceed with a higher hydraulic conductivity and note the changes in head profiles.

**2. Activate and Explore the _Q_-_h_ Plot**
- Navigate to the INPUT CONTROLS and click "Click for the _Q_-_h_ plot".
- Select the No-flow _Q_-_h_ plot for display.
- The red dot in the _Q_-_h_ plot represents the flow and head at the location of the dot in the model shown in the upper figure.
- With the No-flow _Q_-_h_ plot selected, this point corresponds to the no-flow boundary on the left and updates as parameter values are changed.
- The black line shows how $Q_{in}$ varies as head at the no-flow boundary varies from 140 to 160 m. The flow is always zero because it is a no flow boundary.

**3. Analyze Parameter Sensitivity**
- Vary the recharge and observe how the red dot shifts vertically:
    - For the No-Flow Boundary, the flow remains constant at zero, while the head adjusts with changing parameters. When using a relatively high hydraulic conductivity, the calculated head at the boundary does not substantially change.
    - Lower the hydraulic conductivity and again observe the effect on head and the red dot location.

**4. Explore Head-dependent (River) Boundaries**
- Return to the INPUT CONTROLS, activate the Head-dependent flux boundary, and then activate the _Q_-_h_ plot for the Head-dependent flux Boundary.
- While the Head-dependent flux Boundary is active:
  - Adjust Recharge and note how both hydraulic head and flow change.
  - Modify the Head-dependent flux Conductance (_the units of the conductance are m²/s, this is explained in the :violet[**RIV**] section of the module._): Observe the head changes in the model and the different appearance of the ***Q-h*** plot. This demonstrates some characteristics of head-dependent boundaries. The next step considers the application of these boundary conditions.
  
**5. Understand the Role of Head-Dependent Boundaries in Applied Groundwater Modelling** 

Head-dependent boundaries (such as River, General Head, or Drain boundaries) are commonly used to simulate interactions between an aquifer and external systems, where the flow across the boundary is not fixed, but governed by a conductance term and the difference in between the groundwater head calculated at the boundary and the boundary elevation or head of the external system (_this is explained more in the sections :orange[**GHB**], :violet[**RIV**], :green[**DRN**] of this module_).

The use of these boundaries can be considered in two fundamentally different ways depending on the modeling context, first:

**a) During Model Calibration or Model Setup:** One might have field data indicating the groundwater discharge to the river (for example 1.6x10⁻⁵ m³/s per meter length of river). Given that the river (head-dependent flux boundary) is the only outlet of the model, the recharge rate can be calculated by dividing the discharge by the surface area of the model (2500 m by 1 m). Then, the hydraulic conductivity and conductance can be adjusted until the model heads match the measured field heads.

To explore this behavior:
- Set the boundary on the right side of the model to a specified head.
- Set the recharge to a value of (approximately) 200 mm/yr.
- Use the toggle to show the ***Q-h*** plot of the specified head boundary (on the right side). The blue dot represents the outflow at the boundary.
- Modify the hydraulic conductivity and the recharge to see how the Q-h plot reacts (focus on the blue dot that represents the head and flow at the boundary).
- Reset the recharge to a value of (approximately) 200 mm/yr.
- Now toggle in the middle section of the :green[INPUT CONTROLS] for the :violet[Head-dependent flux BC]. Make sure that the ***Q-h*** plot for the Head-dependent flux boundary is active. The magenta-dot represents the outflow and head at the boundary.
- Assess the difference between the Specified head and the Head-dependent flux boundary by setting and resetting the :violet[Head-dependent flux BC] toggle and study the ***Q-h*** plot with the value of aquifer hydraulic conductivity set higher than the conductance of the head-dependent flux boundary. The flow, which is solely a function of the recharge, is identical but the head at the boundary is increased if the :violet[Head-dependent flux BC] is active AND the conductance value is less than the aquifer hydraulic conductivity (the same would be the case for other head-dependent boundary conditions like :orange[**GHB**] or :green[**DRN**]). If the conductance is higher than the aquifer hydraulic conductivity, then including the river bed does not change the heads in the system. If the conductance is much lower than the aquifer hydraulic conductivity then there is a steep gradient between the aquifer head calculated at the boundary and the Head-dependent flux boundary (river) stage.
- It is useful to experiment with values of conductance $C_{B}$ and observe how the heads in the model and the ***Q–h*** relationship change.

A second way to use the Head-dependent flux (river) boundary: 

**b) Once the Model is Calibrated such that the values of Recharge and Conductance are no longer adjusted:** If other outlets are added to the system (e.g., abstraction wells, drains) the heads in the model will be a result of all the model boundary conditions and parameter values. In consequence, the previously calibrated, and then specified, conductance will control how much of the recharge flows to the Head-dependent flux boundary. The discharge will also depend on the location and properties of the other outlets. Such cases are discussed in the :orange[**GHB**], :violet[**RIV**], and :green[**DRN**] sections of this module. Further instructions for exploring the influence of boundary conditions are provided in those sections.