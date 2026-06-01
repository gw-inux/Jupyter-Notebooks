The Hantush-Jacob solution describes transient radial flow to a well pumping at a constant rate $Q$ in a semi-confined aquifer. In the form used here, storage within the semi-confining layer is neglected.

The drawdown is given by:

$$
s(r,t) = \frac{Q}{4\pi T} W(u, r/B)
$$

where

$$
u = \frac{r^2 S}{4 T t}
$$

and

$$
B = \sqrt{\frac{T b'}{K'}}
$$

is the leakage factor. Here, $b'$ is the thickness of the semi-confining layer and $K'$ is its vertical hydraulic conductivity.

The parameter

$$
\frac{r}{B}
$$

controls the influence of leakage on the pumping response. Small values of $r/B$ indicate weak leakage and behavior similar to the Theis solution, whereas larger values correspond to stronger leakage effects.

The Hantush-Jacob well function is defined as

$$
W(u,r/B)
=
\int_u^\infty
\frac{
\exp\left(
-x-\frac{(r/B)^2}{4x}
\right)
}{x}
\,dx
$$

The derivative of drawdown with respect to the natural logarithm of time is

$$
\frac{\partial s}{\partial \ln(t)}
=
t \frac{\partial s}{\partial t}
=
\frac{Q}{4\pi T}
\exp\left(
-u-\frac{(r/B)^2}{4u}
\right)
$$

For $r/B = 0$, the Hantush-Jacob solution reduces to the Theis solution and the derivative approaches the characteristic radial-flow plateau. For $r/B > 0$, leakage increasingly contributes water to the pumped aquifer, causing the late-time derivative to decline below the Theis plateau.

This characteristic decline is one of the most important diagnostic signatures of semi-confined aquifer behavior.