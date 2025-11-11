#### :red[🧭 Getting Started]

Follow these steps to explore threshold-controlled withdrawal behavior in MNW (if you prefer there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider):

**1. Start by setting the following values** 
  * $Q-target = -0.5$ m
  * $h_{gw} = 10$ m
  * Limiting head $h_{lim} = 5.0$ m
  * CWC parameters: $A = 3$, $B = 3$, $C = 3$, and $P = 3$ to represent a well with significant losses

**2. Step through values of Q** 
  * Vary withdrawal rate $Q$ from -0.1 to -0.9 m³/s
  * Observe how $h_{well}$ responds to withdrawal
  * Identify where the well head $h_{well}$ reaches the threshold head $h_{lim}$

**3. Explore Threshold Activation** 
  * Increase the withdrawal rate _Q_ beyond the point where $h_{well} = h_{lim}$
  * Note that the current _Q_ (represented by the dot in the plot) is automatically reduced to keep $h_{well} = h_{min}$

**4. Explore Withdrawal Limits**  
  * Set the limiting head $h_{lim}$ to 5.0 m and the groundwater head $h_{gw}$ to 15.0 m. Set the withdrawal rate to 0.5 m³/s. With these settings, the system is in proper operation.
  * Toggle **Apply withdrawal thresholds** to automatically switch off/on the pump then the Qmn and Qmx will appear on the plot as solid and dashed black lines
  * Set Qmn and Qmx to -0.05 and -0.2 m³/s
  * Now, lower the groundwater head $h_{gw}$ in steps down to 5.1 m. The groundwater head can be lowered by various mechanisms with the most common likely being withdrawal from  neighboring wells.
  * While lowering the groundwater head, observe how the adjusted withdrawal rate - represented by the dot in the plot - is affected.
  * Once the groundwater head reaches 5.1 m, gradually raise the head back to 15.0 m and observe the adjusted withdrawal rate (dot in the plot).

**5. Modify Parameters**
  * Try different values for $A$, $B$, $C$, and $P$
  * Vary Q (Q-target), Δh (H-target), groundwater head $h_{gw}$ and threshold head $h_{lim}$, and investigate the MNW behavior with the interactive plot.

💡 This exercise facilitates understanding of how operational constraints (like prevention of water level dropping below a pump) interact with well head-loss to adjust the simulated flow rate so a model cannot represent more withdrawal of water than the well design will allow.