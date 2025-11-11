🎯 **Learning Objectives**

This exercise is designed with the intent that, upon completion, you will be able to:

- Understand how MNW represents nonlinear resistance between groundwater and a well
- Interpret how discharge and drawdown change for different parameterizations
- Explain how MNW behavior differs from other boundary conditions (e.g., WEL, RCH, DRN, RIV)
- Identify cases where turbulence is dominant

🛠️ **Tasks**

1. **Well Head Response to Discharge**
   * Use :blue[**Q-target**] mode
   * Set: $A = 0.5$, $B = 0.05$, $C = 1.0$, $P = 2.0$
   * Vary $Q$ from $-0.05$ to $-0.8$ m³/s
   * 📝 Record $h_{well}$ and compute the drawdown: $\Delta h = h_{gw} - h_{well}$

2. **Effect of Parameter Variation**
   * Starting with the CWC settings from step 1, for a few values of Q, make the following changes and note the drawdown
     * Double $A$
     * Double $B$
     * Double $C$
     * Increase $P$ to $2.5$ or $3.0$
   * 📝 Record how each change affects drawdown for a given $Q$
   * Which parameters cause nonlinear increases in $Q$?

3. **Explore H-target Mode**
   * Retaining the final settings for CWC from step 2, set drawdown to $Δh$ = $2.0$ m, then in a few steps, lower it to $0.5$ m
     * 📝 Record how discharge changes (hint: when the $Q$ value is out of the axis range as is the case for $Δh$ = $2.0$ m, the value of $Q$ can be determined from the legend)

4. **Conceptual Comparison**
   * When is the MNW behavior close to behaving like:
     - a constant $Q$ source (WEL)?
     - a linear head-dependent boundary (RIV)?
   * What role does the parameter $P$ play in making an MNW boundary behave differently?

🧠 Reflect: What happens if you set $A$ = $0$? When is turbulence (nonlinear loss) dominant?