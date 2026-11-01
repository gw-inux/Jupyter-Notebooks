### Follow the pressure gradient, not just the downward axis

The grain network is a pressure-driven flow model. At each connection, the code uses

$$
Q_{ij}=g_{ij}(P_i-P_j),\qquad g_{ij}>0.
$$

A particle follows outgoing water flow, so pressure decreases along every traversed connection. With heterogeneous conductances, a lower-pressure neighbour can lie slightly **upward on the drawing**. This is a local detour, not motion against the calculated flow. The downward coordinate describes distance along the board; it is not an elevation-head term. A pressure-driven network formulation is described in the [OpenPNM transport documentation](https://openpnm.org/examples/tutorials/08_simulating_transport.html); our app uses its own solver and the stated simplified boundary conditions.

### A slow connection can look like a pause

Connection travel time is water-filled throat volume divided by flow magnitude:

$$
\tau_e=\frac{\pi r_e^2 L_e}{|Q_e|}.
$$

A small but nonzero flow can therefore produce a long, finite travel time. Movement is interpolated continuously between node times. The animation covers the latest arrival in the complete run; with many particles, a rare slow path can make most particles arrive early and leave a few moving very slowly. Overlapping blue markers can also obscure individual motion.

**To inspect a path:** pause, use Previous step / Next step, then open the pathway details at the bottom. The table includes node pressure and connection travel time. Pressure must decrease even along an upward segment. The checks require positive travel times, no repeated nodes, arrival at an outlet, and conserved mass. These are checks of this idealized network, not a validation against a measured soil. No trapping, sorption, or diffusion into immobile pores has been introduced.

### Why most particles can arrive early on the display

Grain-network playback now starts with **60 screen seconds**. Model time still runs linearly from zero to the latest arrival. A rare, very slow connection can stretch this time range; a longer display does not remove that difference in physical travel times.

A reproducible check with 20 rows, a = 1 mm, grain-size factor 0.75, variation 0.25, pressure difference 0.5 Pa, grain seed 7, particle seed 42, a pulse and 10,010 particles gave a median arrival of about **423 s**, a 95th percentile of **772 s**, and a latest arrival of **5,897 s**. The latest particle took **no upward steps**. It spent about **90%** of its transit time in one downward connection with a pressure drop of only 0.000051 Pa. No sampled path revisited a node.

For that particular sample, 95% of particles have arrived by about **7.9 screen seconds** on the 60-second display, compared with about 1.0 screen second on an eight-second display. Other seeds and settings give different values. The independently checked pressure solve and travel-time equations support a low-flow explanation, not an endless loop. This model omits molecular diffusion and immobile-pore exchange; its late tail is not a calibrated prediction for a real soil. Use Pause and the node-step buttons to inspect individual passages.
