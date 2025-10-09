**Getting Started with the Interactive Plot** Instructions for :red[**Scenario 2**]: Recharge, Groundwater Divide, and Boundary Flow Response

:red[**Scenario 2**] allows you to explore the development of a groundwater divide under recharge conditions, and to investigate how hydraulic conductivity, boundary elevations, and model parameters influence both flow dynamics and _Q_-_h_ relationships.

**1. Modify Model Parameters**
- Click "Modify Model Parameters" in the Control Panel to begin.
- Increase the Recharge:
  - A red vertical line will appear in the plot, marking the location of the groundwater divide.
  - Green arrows will appear in the plot, indicating the direction and magnitude of recharge.
  - Adjust the Hydraulic Conductivity:
    - 🔽 Lower values create steeper gradients and form a distinct “groundwater mound”.
    - Use a very low hydraulic conductivity to clearly visualize this effect.

**2. Investigate Flow and Divide Behavior**
- The plot dynamically shows flow values across the boundaries. A negative Q indicates outflow at the boundary and a positive value indicates inflow.
- Click the middle tab in the INPUT CONTROLS to access Boundary Condition Parameters.
- Modify the elevation of the left specified head boundary:
  - 🔼 Increasing the left head: Shifts the groundwater divide to the left. This also increases the hydraulic gradient and flow at the right boundary. The flow at the boundary increases because the area (between the divide and the right boundary) that collects recharge is larger. 
  - If the flow magnitude at the left boundary becomes greater than 3x10⁻⁵ m³/s, use the toggle to increase the Q axis range.
  - 🔽 Decreasing the left head: Moves the divide to the right. Accordingly, reduces the contributing recharge area to the right boundary and lowers outflow.
  - Using a high 🔼 head on the left coupled with a low 🔽 recharge rate and a high 🔼 hydraulic conductivity results in flow through the aquifer from left to right at a rate higher than the inflowing recharge and there is no flow divide within the model.

**3. Explore the _Q_-_h_ Plot Dynamics**
- Activate the _Q_-_h_ Plot for the right specified head boundary:
  - A blue dot in the main plot highlights the boundary condition point.
  - The _Q_-_h_ plot shows this as a blue dot at a fixed head of 150 m.
- As you adjust the left specified head, observe how the blue dot moves:
  - 🔼 When the left head increases, the groundwater divide moves to the left and more recharge flows to the right boundary → the blue dot moves down, indicating higher outflow.
  - 🔽 When the left head decreases, the contributing area shrinks → the blue dot moves up, indicating reduced flow.

**4. Run Comparative Experiments**
- Switch between the different _Q_-_h_ plots to track how other boundaries behave.
- Vary the following parameters to better understand interactions:
  - Recharge
  - Hydraulic Conductivity
  - Left Boundary Head