**The whole experiment is coupled.** The 11 cells have 100 m centre spacing and 1 m width. The prescribed boundary centres are 1000 m apart; recharge enters the nine solved interior cells. The default unconfined aquifer has bottom 0 m, top 30 m, boundary heads 18 and 8 m, and conductivity 1E-4 m/s. The confined comparison remains a 20 m thick layer from −20 to 0 m. A higher roof changes the physical problem when heads reach the former roof; it is not just a graphical setting.

The eleven-cell conductance integrates wet thickness and uses harmonic hydraulic conductivity. With $\Phi'(h)=b(h)$, face flow is

$$Q_{i+1/2}=K_{i+1/2}\frac{w}{\Delta x}\left[\Phi(h_i)-\Phi(h_{i+1})\right].$$

Below the roof, $\Phi=(h-z_b)^2/2$; above it, the potential is linear with slope equal to the full thickness. For this fixed-K, fixed-recharge model the discrete equations are linear in potential. They remain nonlinear in head. Fixed conductivity zones do not remove this transform.

**The Picard panel** shows the latest accepted full-system construction on its own green head function. Each step has a function along its own full update direction. Earlier functions and paths are omitted here because they differ from the current function; all accepted heads remain in the history plots. The thin dotted guide projects the current head from the axis to its function value. When the selected head barely changes, a selected-head slice holds the other input heads fixed, avoiding division by that small change. A flat function on a selected cut is possible and does not prove that the whole vector problem is linear.

**The Newton panel** shows the selected cell’s reduced flow residual in m³/s. For the face-flow law used here, eliminating the other eight cell balances gives

$$f_{N,i}(h_i)=F_i^{\mathrm{red}}(h_i)=c_i-S_i\Phi(h_i),\qquad (F_i^{\mathrm{red}})'=-S_i b(h_i).$$

Here $c_i$ is the effective source term (m³/s) and $S_i$ is a positive factor (m/s) determined by the connections to the two boundaries. Both are fixed for the selected cell and model setup. At each trial head on the blue curve, the other eight interior heads take the values that balance their cells. Repeating a trial head therefore gives the same blue ordinate at every iteration.

The orange dot evaluates this curve at the current head. The tangent touches the curve at the head used for that step, and its intercept gives the selected cell’s full Newton proposal. Damping accepts a fraction of that correction. If we held the neighboring heads at their current estimates and varied only the selected head, the resulting local balance curve could move from one iteration to the next. The convergence plot evaluates all nine original cell balances at the actual head estimates. In section 2 the middle head is the only unknown, so its blue curve $f_N(h)=F(h)$ follows directly from that cell’s balance.

The reference table compares homogeneous runs with the independent 1D analytical solution at cell centres. It does not apply that homogeneous formula to heterogeneous cases. Cell-face flows lie at x = 50, 150, …, 950 m, and their net outflow balances recharge over the nine interior cell areas.

The left convergence axis shows maximum head change; the right shows maximum flow residual. Both log axes span 1E-12 to 100. The histories extend one iteration beyond the latest accepted update. A head-history detail panel appears only for a sustained tail of three sub-centimetre selected-cell changes near the reference. Both numerical closure criteria remain required; this extra view changes neither tolerance nor iteration history.


**Auto-zoom** centres the displayed Picard/diagonal crossing or Newton residual zero. On resizing, the current head lies two-thirds of the way from the centre to the edge on its side. The width then stays unchanged until the head is within the inner 25% of the half-width, or leaves the window. The minimum full width is 0.001 m. The Picard crossing can move as the other heads change and can differ from the final reference; the window follows that crossing while retaining its width.

**− Zoom / + Zoom** select manual full widths of 1, 0.1, 0.01, 0.001, 1E-4 and 1E-5 m and turn auto-zoom off. Manual width stays fixed across iterations; the crossing stays centred. The badge identifies the mode and width. Switching auto-zoom on starts a fresh fit; switching it off restores the full view. Changing the model inputs, initial heads or damping starts a new experiment with both panels in the full view. Postprocessing options switch between the shared side-by-side comparison and stacked, full-width method panels with independent controls and histories. These display choices do not change the model or erase its iterates.
