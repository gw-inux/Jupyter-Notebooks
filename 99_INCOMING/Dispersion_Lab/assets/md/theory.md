### Pinboard: position and time are separate mechanisms

For n rows, each independent lateral step is +a or −a with probability 1/2. With K rightward choices,

$$
K\sim\mathrm{Binomial}(n,1/2),\qquad X=a(2K-n),
$$

$$
\mathrm{E}[X]=0,\qquad \mathrm{Var}(X)=na^2.
$$

The regular board has a fixed step time μ. In variable-time mode, each step time τ is an independent lognormal variate with mean μ and coefficient of variation c. Route and time draws are independent. The lognormal parameters are

$$
\sigma_\ell^2=\ln(1+c^2),\qquad m_\ell=\ln(\mu)-\sigma_\ell^2/2.
$$

If c = 0 the code uses fixed times exactly. The total transit time T has

$$
\mathrm{E}[T]=n\mu,\qquad \mathrm{Var}(T)=n\mu^2c^2.
$$

For independent release time R uniformly distributed between 0 and duration d, arrival time A = R + T has

$$
\mathrm{E}[A]=d/2+n\mu,\qquad \mathrm{Var}(A)=d^2/12+n\mu^2c^2.
$$

For an instantaneous pulse, R = 0. A finite-step distribution need not be Gaussian. Temporal spread at the outlet is not itself a longitudinal dispersion coefficient.

### Grain network: geometry, flow, then transport

Pore nodes use the same diamond lattice, with horizontal and flowwise step a. Grain centres form its dual lattice. Nearest grain-centre distance is √2a. Grain radii are

$$
R_g=\frac{a}{\sqrt{2}}\,\kappa(1-vU_g),\qquad U_g\sim\mathrm{Uniform}(0,1),
$$

where κ is the packing control and v is the grain-size variation. The allowed ranges keep grains separate. For the two grains flanking a throat, its equivalent tube radius is

$$
r_e=\frac{\sqrt{2}a-R_{g1}-R_{g2}}{2},\qquad L_e=\sqrt{2}a.
$$

This mapping is a stated geometric teaching assumption. The circular tube is an equivalent conduit, not the exact cross-section between real grains. κ is not porosity. Increasing v also changes the mean grain radius; it does not isolate variance at a fixed mean.

For water viscosity μw = 0.001 Pa s, the Hagen–Poiseuille conductance and flow are

$$
g_e=\frac{\pi r_e^4}{8\mu_wL_e},\qquad Q_{ij}=g_e(P_i-P_j).
$$

The inlet has pressure potential ΔP; every outlet has zero pressure potential. All internal nodes satisfy

$$
\sum_j Q_{ij}=0.
$$

Unconnected outer boundaries carry no flow. The diagram is a planar network drawn from top to bottom; its vertical coordinate is not an elevation head. The imposed pressure potential drives flow. No additional gravitational forcing is calculated.

At a junction, outgoing route probabilities are proportional to outgoing water flows. This assumes instantaneous complete mixing at a node with zero residence volume. A marker moves through each throat at its cross-sectional mean velocity:

$$
p_{ij}=\frac{Q_{ij}}{\sum_{k:Q_{ik}>0}Q_{ik}},\qquad
u_e=\frac{|Q_e|}{\pi r_e^2},\qquad
\tau_e=\frac{\pi r_e^2L_e}{|Q_e|}.
$$

Only positive outgoing flows enter the probability. Markers always follow decreasing pressure, even if a local path points upward on the screen. Zero-flow throats are not sampled. Pressure decreases strictly along a trajectory, so trajectories cannot loop.

Exact outlet probabilities and travel-time moments are calculated by recursion through this flow-directed graph, independently of the particle sample. The exact mean transit time also satisfies **flowing throat volume / inlet flow**. These provide numerical verification, not validation against a real soil.

### Mass accounting and interpretation

Total normalized mass is 1, with marker mass 1/N. At any time, counts not yet released + counts in the board + counts collected = N. The spatial bars give collected mass per outlet. Arrival-time histogram heights are counts/(N × bin width), in s⁻¹; the full histogram integrates to 1. These quantities are not resident concentration.

The displayed sample standard deviations use division by N (the empirical distribution), not the N−1 unbiased estimator. Table references describe the model population. One marker necessarily has zero empirical spread, even if the population spread is positive.
