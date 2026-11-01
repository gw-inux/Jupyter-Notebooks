### Connection to continuum solute-transport equations

For a saturated medium with constant mobile porosity, steady incompressible flow, a conservative dilute solute, and appropriate averaging, a common continuum description is the advection–dispersion equation (ADE):

$$
\frac{\partial C}{\partial t}+\mathbf{v}\cdot\nabla C
=\nabla\cdot(\mathbf{D}\nabla C).
$$

Here C is dissolved concentration, **v** the mean pore-water velocity (not Darcy flux), and **D** the dispersion tensor. In a uniform medium with flow along z and transverse coordinate x, constant coefficients give

$$
\frac{\partial C}{\partial t}+v\frac{\partial C}{\partial z}
=D_L\frac{\partial^2C}{\partial z^2}+D_T\frac{\partial^2C}{\partial x^2}.
$$

A common constitutive representation is $D_L$ = $\alpha_L$|v| + $D_{m,\mathrm{eff}}$ and $D_T$ = $\alpha_T$|v| + $D_{m,\mathrm{eff}}$. Dispersion coefficients D have units of length²/time; dispersivities α have units of length. Effective molecular diffusion $D_{m,\mathrm{eff}}$ accounts for porous-medium restrictions. These continuum relations provide context; the module does **not** solve this ADE or prescribe $\alpha_L$ and $\alpha_T$ (Wexler, 1992).

### A spatial variance is not an arrival-time variance

For an unbounded, constant-coefficient continuum pulse, longitudinal spatial variance grows as $2D_Lt$. For a different observable—the first-passage time to an absorbing plane at distance L starting at zero with an unbounded upstream domain, constant v > 0, and $D_L$—the moments are

$$
\mathrm{E}[T]=\frac Lv,\qquad \mathrm{Var}(T)=\frac{2D_LL}{v^3}.
$$

These identities concern specific boundary conditions and observables (Probability Distribution Explorer, Inverse Gaussian distribution). As a mathematical illustration, matching the pinboard moments with L = na and v = a/μ would give

$$
D_{L,\mathrm{moment}}=\frac{\mathrm{Var}(T)v^3}{2L}=\frac{a^2c^2}{2\mu}.
$$

This is only a **moment-matched analogy**. It does not make the board's transit-time distribution the ADE first-passage distribution; a sum of lognormal step times is generally not inverse Gaussian. The module therefore reports widths and moments, without presenting this expression as an estimated soil dispersion coefficient. Arrival-time variance from a finite injection must first be separated from transit-time variance even for that analogy.

### Why finite networks may not be Fickian

Bijeljic and Blunt (2006) show that an asymptotic dispersion description can require transport through many pores; their network explicitly includes advection and molecular diffusion. The present board has only 2–40 rows in either configurable mode and uses simpler physics. A smooth-looking histogram does not establish an asymptotic regime, Gaussian transport, or a scale-independent dispersivity. The single inlet, widening triangular geometry, and equal-pressure outlet boundary all influence the grain-network response.
