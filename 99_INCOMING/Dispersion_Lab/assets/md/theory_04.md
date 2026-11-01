### From grain geometry to an idealized hydraulic network

The grey-grain version retains a triangular diamond lattice of pore nodes. Grain centres lie on its dual lattice. For lattice increment a, neighbouring grain centres are separated by √2a. Grain radii are defined by

$$
R_g=\frac{a}{\sqrt{2}}\kappa(1-vU_g),\qquad U_g\sim\mathrm{Uniform}(0,1).
$$

Here κ is the **grain-size factor** (formerly the packing control) and v the grain-size variation. Larger κ narrows gaps. Larger v broadens the radius distribution while also reducing its mean, E[Rg] = aκ(1−v/2)/√2. Neither control is measured porosity; grains stay on fixed centres and are not mechanically compacted.

For the two grains flanking edge e, the **surface gap is mapped to a circular tube diameter**:

$$
r_e=\frac{\sqrt{2}a-R_{g1}-R_{g2}}2,\qquad L_e=\sqrt{2}a.
$$

This is the app's geometric surrogate, not the exact aperture or resistance of a real three-dimensional pore. Pore bodies have zero storage and no added resistance. Conductance-based network modelling and simple cylindrical throat approximations are described in the official OpenPNM documentation; this app uses its own solver.

### Solve water flow before moving solute

For dynamic water viscosity $\mu_w$ = 0.001 Pa s, the ideal tube conductance and signed flow are

$$
g_e=\frac{\pi r_e^4}{8\mu_wL_e},\qquad Q_{ij}=g_e(P_i-P_j),\qquad \sum_jQ_{ij}=0.
$$

The last equation applies at every internal node. Inlet pressure potential is ΔP; every outlet is held at zero. There are no connections across the outer sides. The downward coordinate is flowwise distance, **not elevation head**; gravity is not added separately. No solute is moved in the preparation preview, although the steady water-flow field is already calculated.

An outgoing route is sampled with its fraction of the outgoing flow, and each throat is traversed at its cross-sectional mean velocity:

$$
p_{ij}=\frac{Q_{ij}}{\sum_{k:Q_{ik}>0}Q_{ik}},\qquad
u_e=\frac{|Q_e|}{\pi r_e^2},\qquad \tau_e=\frac{\pi r_e^2L_e}{|Q_e|}.
$$

This imposes instantaneous complete mixing at zero-volume junctions. Molecular mixing and velocity profiles within tubes are not simulated. The routing rule is therefore a model closure, not a claim that pore junctions always mix completely. The flow always follows decreasing pressure; a local edge can point upward on the drawing without forming a loop. Zero-flow throats are excluded.

### Independent model references

Exact outlet probabilities and first two transit-time moments are computed recursively on the pressure-directed graph. For expected remaining transit time mᵢ and second moment sᵢ, with zero values at outlets,

$$
m_i=\sum_jp_{ij}(\tau_{ij}+m_j),\qquad
s_i=\sum_jp_{ij}(\tau_{ij}^2+2\tau_{ij}m_j+s_j).
$$

The inlet variance is s₀−m₀². A separate check is m₀ = flowing throat volume / inlet flow. Outlet probabilities also equal outlet water-flux fractions under the stated mixing rule. These checks verify the mathematical implementation; they do not validate the geometric surrogate against a soil.

**Prediction:** doubling ΔP doubles flows and halves transit times while preserving route probabilities. With identical grains, reducing every tube radius by half reduces flow by 16 and increases transit time by four at fixed pressure. Check the reported throat Reynolds number, Re = 2ρur/$\mu_w$ (ρ = 1000 kg/m³); creeping-flow conditions are not assured if Re approaches or exceeds 1.
