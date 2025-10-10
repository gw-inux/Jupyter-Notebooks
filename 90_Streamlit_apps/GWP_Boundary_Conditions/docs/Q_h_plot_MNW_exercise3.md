🎯 **Learning Objectives**

This exercise is designed with the intent that, upon completion, you will be able to:

- Explain how threshold head limits influence MNW discharge behavior
- Identify the conditions for which withdrawal is reduced to protect a wells
- Analyze how nonlinear head losses and operational limits combine to define feasible withdrawal rates
- Understand the role of Qmn and Qmx in the MNW implementation

🛠️ **Exercise Instructions**

1. **Locate Threshold Activation Point**
   * Set: $A = 1$, $B = 1$, $C = 1$ $P = 1$, $h_{gw} = 10$ m, $h_{lim} = 7$ m
   * Increase Q from 0.2 to 1.0 m³/s
   * 📝 Identify the Q at which $h_{well} = h_{lim}$ — call this $Q_{lim}$

2. **Test Effect of Nonlinearity and Exponent P**
   * Starting again with: Q to 0.5 m³/s, $h_{gw} = 10$ m, $h_{lim} = 7$ m $A = 1$, $B = 1$, $C = 1$ $P = 1$
   * Increase $C$ to 2 and repeat the test
   * Increase $P$ to 2 and repeat the test
   * How does $Q_{lim}$ change?
   * Is the threshold reached earlier or later?
   * Why does a higher $P$ allow a higher flow rate?

3. **Apply Qmn and Qmx Limits**
   * Starting again with: Q to 0.5 m³/s, $h_{gw} = 10$ m, $h_{lim} = 7$ m $A = 1$, $B = 1$, $C = 1$ $P = 1$
   * Set Qmn = 0.1 m³/s and Qmx = 0.2 m³/s
   * Try to reach the value of Qmn by lowering the groundwater head and take notice of the groundwater head when withdrawal stops.
   * Now, increase the groundwater head in steps up to 10.0 m and notice the value of groundwater head when withdrawal starts again. Consider why withdrawal stops and starts at different values of groundwater head.
   * Double the parameter for linear well loss $B$ and repeat the procedure. Quantify the changes in terms of groundwater heads for switching off/on the withdrawal.

💭 Reflect:
- When is the threshold head the limiting factor?
- How do Qmn and Qmx affect the value of practical withdrawal?
- How is this behavior affected by the value of CWC with respect to the individual processes that control CWC (aquifer loss, linear and nonlinear well loss).

This exploration prepares you to interpret MNW behavior in model calibration and design tasks.