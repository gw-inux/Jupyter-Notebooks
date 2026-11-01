# Grain-network travel-time review — version 2.4

30 October 2026. Numerical checks of the existing idealized teaching model.

The renewed checks found no equation, unit, radius/diameter or routing error in the tested cases. Long arrivals are caused primarily by small flow through particular connections. They do not require repeated up/down cycling: the latest particle in the default 20-row cohort travelled downward at every step.

## Equations and independent checks

For a cylindrical throat of radius r, length L, dynamic viscosity μ and pressure drop ΔP:

$$
g=\frac{\pi r^4}{8\mu L},\qquad Q=g\Delta P,\qquad
\bar v=\frac{|Q|}{\pi r^2},\qquad
\tau=\frac{L}{\bar v}=\frac{\pi r^2L}{|Q|}=\frac{8\mu L^2}{r^2|\Delta P|}.
$$

Internal units are m, Pa, s and m³/s; μ = 0.001 Pa s. The surface gap is a **diameter**; the code divides by two before using r in the fourth-power conductance law. The cylinder law is consistent with the cylindrical-throat size factor and viscosity division in the official [OpenPNM 3.5.2 size-factor source](https://github.com/PMEAL/OpenPNM/blob/v3.5.2/openpnm/models/geometry/hydraulic_size_factors/_funcs.py) and [hydraulic-conductance source](https://github.com/PMEAL/OpenPNM/blob/v3.5.2/openpnm/models/physics/hydraulic_conductance/_funcs.py). The app has its own solver; OpenPNM's additional pore-body terms are not included here.

The audit checked:

- An independent dense positive-definite pressure solve against the implemented sparse solve, across nine configurations spanning 2–40 rows, grain factors 0.5–0.9, variations 0–0.4, pressures 0.05–2 Pa and two grain seeds. These are representative and boundary cases, not an exhaustive sweep.
- Connection times against the independent equivalent expression L/mean velocity; outgoing probabilities against their flow fractions; normalized nodal and inlet/outlet balances; and exact mean transit against flowing pore volume/inlet flow.
- A two-row uniform network against a closed-form solution, for three grain-factor/pressure combinations. Each intermediate pressure is P_in/3; Q_in = 4gP_in/3; every path's total transit is 4.5V/(gP_in). This checks geometric and hydraulic factors without using the general moment recursion as its reference.
- Three complete 10,010-particle cohorts: strictly decreasing pressure, positive finite connection times, no revisited nodes, outlet termination and conserved particle mass. Existing regression tests also check continuous interpolation along actual upward and slow connections.

Worst discrepancies over the nine hydraulic cases were 3.00 × 10⁻¹⁵ for pressure relative to inlet pressure, 5.08 × 10⁻¹⁵ for flow differences relative to inlet flow, 6.66 × 10⁻¹⁶ for equivalent connection-time formulas, and 1.52 × 10⁻¹⁴ for inlet/outlet imbalance. These values support numerical consistency within floating-point precision.

## Reproducible samples

All three cohorts use a = 1 mm, ΔP = 0.5 Pa, grain seed 7, particle seed 42, pulse injection and 10 highlighted + 10,000 background markers.

| Rows | Grain factor / variation | Median arrival (s) | 95th percentile (s) | Latest arrival (s) | Slowest connection on latest path (s) | Share of latest path time |
|---:|---|---:|---:|---:|---:|---:|
| 20 | 0.75 / 0.25 | 423.18 | 771.87 | 5,897.22 | 5,321.29 | 90.23% |
| 40 | 0.75 / 0.25 | 2,031.81 | 4,069.03 | 10,941.11 | 5,999.31 | 54.83% |
| 40 | 0.90 / 0.40 | 3,750.61 | 7,862.21 | 89,973.83 | 86,228.29 | 95.84% |

In the first case, the latest path has 20 connections, all downward. Its slowest connection runs from z = 14 to 15 mm, with r ≈ 0.2427 mm, ΔP ≈ 5.104 × 10⁻⁵ Pa and |Q| ≈ 4.919 × 10⁻¹⁴ m³/s. The connection is not especially narrow; the small pressure drop makes its flow very slow. In the third case, the dominant slow connection points upward on the drawing but still follows decreasing pressure. None of the 30,030 sampled paths contains a repeated node.

The route rule follows outgoing flow, not gravity or the plotted z sign. In this steady network, strict pressure descent prevents cycles. Locally upward segments can lengthen a route, but an upward coordinate increment is not itself the cause of a long residence time.

## What the longer playback does

The grain-network default is now 60 screen seconds, while guided/pinboard defaults remain eight. For a linear display clock,

$$
t_{\mathrm{screen}}=D_{\mathrm{screen}}\,t_{\mathrm{model}}/t_{\max}.
$$

For the 20-row sample above, 95% of particles arrive by about 7.85 screen seconds with D = 60, compared with 1.05 screen seconds with D = 8. The 60-second duration slows the visible movement but does not remove the skewed arrival-time distribution. A movie on the same clock would have the same relative timing.

No paths were shortened, no slow arrivals clipped and no physical times rescaled. Pause and Previous/Next step remain available to inspect exact node events.

## Interpretation and limits

This is an advection-only network of equivalent tubes with zero-volume, perfectly mixed junctions. It omits molecular diffusion, pore-body storage, exchange with immobile water, adsorption and trapping mechanisms. Near-stagnant advection can therefore give very long times; that result is internally consistent without being a calibrated prediction for real soil. Diffusion could be important in a real low-flow region, but adding it would be a separate physical-model extension requiring new assumptions and validation.

Reproduce the audit with:

```bash
python scripts/audit_travel_times.py travel_time_audit.json
python -m pytest -q tests/test_model.py -k two_row
```

Unrounded results are supplied in `travel_time_audit_v2_4.json`. Existing equations and transport random streams are unchanged.
