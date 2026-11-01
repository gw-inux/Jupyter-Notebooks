### What the models can show

The pinboard demonstrates how repeated pathway choices create transverse spreading. Independent variable travel times add longitudinal separation and a distribution of outlet arrival times. The grain network connects geometry to flow, route probabilities, and travel times using a transparent hydraulic surrogate.

### What remains an assumption

- The solute is conservative and passive. No sorption, reaction, density effects, or particle collisions are represented.
- The pinboard is a stochastic transport analogue; it does not solve rigid-body collisions or gravitational acceleration.
- Molecular diffusion and within-pore velocity profiles are not resolved. Complete mixing at network junctions is an imposed closure assumption, not a simulation of molecular mixing.
- Grain positions lie on a fixed lattice. Packing changes radii and pore openings, not mechanical rearrangement or compaction. The control is not measured porosity.
- Changing lattice spacing changes grain size **and the domain dimensions**. It is not an isolated grain-size experiment at fixed column size.
- The triangular network has one inlet and multiple equal-pressure outlets. Its flow distribution includes effects of this geometry and these boundaries.
- Cylindrical throats approximate pore constrictions; pore bodies have no storage or resistance. Hydraulic balance can be verified, but the network is not calibrated to a real soil.
- No dispersivity is inferred from the plots. A spatial width, a temporal width, and a dispersion coefficient are different quantities. Spreading alone does not establish molecular mixing.
- Finite samples fluctuate. The exact-reference curve and table refer to this mathematical model; they are not field observations.

### References and further reading

- [Yale Physics: Galton board](https://yppsweb2.its.yale.edu/physics/demos/demomain.asp?id=4G10.10&task=viewdemo) — the physical left/right experiment and binomial outlet distribution.
- [Wexler (1992), USGS TWRI 3-B7](https://pubs.usgs.gov/publication/twri03B7) — analytical solute transport and the distinction between advection, diffusion, and mechanical dispersion.
- [Saffman (1959), A theory of dispersion in a porous medium](https://doi.org/10.1017/S0022112059000672) — a classical random-step framework with variable directions and durations. The present model is not a reproduction of that theory.
- [OpenPNM: Simulating Single Phase Transport](https://openpnm.org/examples/tutorials/08_simulating_transport.html) — conductance, pressure boundary conditions, and the limits of simple cylindrical throat models. This app implements its own small network solver and does not require OpenPNM.
