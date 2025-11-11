🎯 **Learning Objectives**

This exercise is designed with the intent that, upon completion, you will be able to:

- Understand how the withdrawal–drawdown relationship is defined for MNW boundaries
- Explain the influence of CWC parameters ($A$, $B$, $C$, $P$)
- Differentiate between Q-target and H-target modes
- Compare well behavior for different types and magnitude of well loss 

🛠️ **Tasks**

1. **Explore Q–Δh Relationship**
   * Set: $A = 3$, $B = 3$, $C = 1.0$, $P = 2.0$
   * Use :blue[**Q-target**] mode
   * Vary $Q$ from $-0.01$ to $-0.5$ m³/s
   * 📝 Record where the curve steepens and explain the influence of the different parameters in CWC ($A$, $B$, $C$, and $P$)

2. **Test Parameter Sensitivity**
   * Set: $A = 1$, $B = 1$, $C = 1.0$, $P = 2.0$
   * Set $Q = -0.3$ m³/s in :blue[**Q-target**] mode
   * Enable the **second parameter set** 
   * Vary $A$, then systematically change $B$, $C$, and $P$ (ultimately setting all values to 4) and compare responses
   * 💭 Reflect on the role of linear versus nonlinear resistance.
       * Switch on/off the linear resistance by setting $A$ and $B$ to $0$.
       * Switch on/off the nonlinear resistance by setting $C$ to $0$.
   * 💭 Reflect on what parameter values would represent well-aging?

3. **Reverse Analysis with H-target**
   * Switch to :red[**H-target**] and make sure to use the initial parameter set: $A$ = $4$, $B$ = $4$, $C$ = $4$, $P$ = $4$
   * Set $Δh$ = $1$, $3$, $5$, $7$ m
   * Compare resulting $Q$ values across different parameter sets (e.g., to reflect an aged well).
   * At what Δh value does $Q$ have a larger withdrawal rate than $-0.2$ m³/s? How much does well-aging affect the efficiency?

_Use this exploration to build deeper insight into how MNW wells behave under variable design conditions._