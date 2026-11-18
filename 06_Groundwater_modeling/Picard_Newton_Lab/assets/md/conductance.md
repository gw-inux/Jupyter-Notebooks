### From Darcy's law to conductance

Start with a uniform flow connection of length $L$, hydraulic conductivity $K$, and cross-sectional area $A_\perp$ perpendicular to the flow direction. Take the positive direction from location $i$ to location $j$. Darcy's law gives

$$
Q=-K A_\perp\frac{h_j-h_i}{L}.
$$

| Symbol | Meaning | Unit |
|:--|:--|:--|
| $Q$ | Discharge, positive from $i$ toward $j$ | m³/s |
| $K$ | Hydraulic conductivity | m/s |
| $A_\perp$ | Area perpendicular to flow | m² |
| $h_i$, $h_j$ | Hydraulic heads at the two locations | m |
| $L$ | Distance between the locations | m |

The negative sign expresses flow down the hydraulic gradient. If $h_i>h_j$, the gradient $(h_j-h_i)/L$ is negative and $Q$ is positive in our chosen direction.

For horizontal flow through saturated thickness $b$ and width $w$, the vertical flow area shown in the three-dimensional sketch is

$$
A_\perp=w b.
$$

We can group the material property and geometry into the **conductance**, $C$:

$$
C=\frac{K A_\perp}{L}=\frac{K w b}{L},
\qquad
Q=-C(h_j-h_i).
$$

Conductance has units of **m²/s**. Multiplying it by a head difference in metres gives discharge in m³/s. Conductance is therefore not another name for hydraulic conductivity: it also depends on the width, saturated thickness, and length of the connection.

Think of two channels filled with the same sand. For the same length and head difference, a wider saturated channel allows more water to pass. Its hydraulic conductivity is unchanged, but its conductance is larger.

For example, let $K=10^{-4}$ m/s, $w=10$ m, $b=5$ m, and $L=100$ m. Then $A_\perp=50$ m² and $C=5\times10^{-5}$ m²/s. With $h_i-h_j=2$ m, the discharge is $10^{-4}$ m³/s, or **0.1 L/s**. If the saturated thickness halves while the other quantities and head difference remain unchanged, the conductance and discharge halve; the hydraulic conductivity does not change.

#### Connecting two neighboring cells

Between adjacent cell centers, water passes through half of each cell. Each half-cell contributes resistance to flow. With equal cell lengths $\Delta x$ and common width $w$, their resistances add:

$$
\frac{1}{C_{ij}}
=\frac{\Delta x/2}{K_i w b_i}
+\frac{\Delta x/2}{K_j w b_j}.
$$

Here $C_{ij}$ is the connection conductance; $K_i,K_j$ and $b_i,b_j$ are the hydraulic conductivities and saturated thicknesses in the two cells. Defining their transmissivities as $T_i=K_i b_i$ and $T_j=K_j b_j$, in m²/s, gives

$$
C_{ij}=\frac{2T_iT_j}{T_i+T_j}\frac{w}{\Delta x}.
$$

This is the harmonic-transmissivity expression used in the three-cell model. A poorly transmitting half-cell can limit the whole connection, just as a narrow section can restrict flow through a wider channel. If both cells have the same conductivity and thickness, the expression reduces to $C=Kwb/\Delta x$.
