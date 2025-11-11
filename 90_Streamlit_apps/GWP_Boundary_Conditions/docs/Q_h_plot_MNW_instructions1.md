#### :blue[🧭 Getting Started]

Before starting the exercise, it is helpful to follow these steps to familiarize yourself MNW:

**1. To start exploring, enter a value of $3$ for $A$, $B$, $C$, and $P$ to represent a well with significant losses**
   * The default is :blue[**Q-target**] mode with $Q = -0.5$ m³/s
   * Observe the drawdown between $h_{gw}$ and $h_{well}$
   * Modify the withdrawal rate to investigate the response in the interactive plot. A higher withdrawal rate causes more head decline in the well.

**2. Switch to H-target**
   * Toggle to :red[**H-target**] mode and $Q$ will be reset to the default $-0.5$ m³/s 
   * Vary drawdown Δh from $0.5$ to $8.0$ m
   * Observe how $Q$ responds to increasing drawdown. The relationship is the same, but now setting $h_{well}$ produces the related value of $Q$, instead of setting $Q$ to obtain the value of $h_{well}$.

**3. Compare Parameter Sets**
   * Toggle to **modify CWC parameters** and the default values will be shown
   * Assuming the first set of values is still $3$ for $A$, $B$, $C$, and $P$
   * Now, in the CWC menu, toggle to define a **second parameter set** and try a less restrictive case (if you prefer there is a toggle button under **Modify Plot Controls** that allows you to type in values instead of using the slider):
     * e.g., $A = 1.0$, $B = 0.2$, $C = 2.0$, $P = 2.5$
   * Compare the resulting Q–Δh relationships.

_Use the plot orientation toggle for alternate layouts._