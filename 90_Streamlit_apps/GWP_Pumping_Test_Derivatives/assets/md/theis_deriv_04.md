The Theis solution describes transient radial flow to a well pumping at a constant rate $Q$ in a confined aquifer. It forms the basis for many pumping-test evaluation methods and provides a useful reference for understanding drawdown derivatives.

The drawdown at distance $r$ and time $t$ is given by:

$$
s(r,t) = \frac{Q}{4\pi T} W(u)
$$

where $T$ is transmissivity, $S$ is storativity, and

$$
u = \frac{r^2 S}{4 T t}
$$

is the dimensionless time parameter.

The drawdown derivative is obtained by differentiating drawdown with respect to the natural logarithm of time:

$$
\frac{\partial s}{\partial \ln(t)}
=
t \frac{\partial s}{\partial t}
=
\frac{Q}{4\pi T} e^{-u}
$$

At early time, the derivative changes as the cone of depression develops around the pumping well. At late time, the parameter $u$ becomes small and $e^{-u}$ approaches unity. The derivative therefore approaches a constant value:

$$
d = \frac{Q}{4\pi T}
$$

This constant derivative plateau is a characteristic feature of infinite-acting radial flow and one of the most important signatures in pumping-test interpretation. Because the plateau depends directly on transmissivity, it provides valuable information for parameter estimation.