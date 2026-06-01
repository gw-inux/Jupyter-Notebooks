The Theis solution describes transient radial flow to a well pumping at a
constant rate $Q$ in a confined aquifer.

The drawdown is:

$$
s(r,t) = \frac{Q}{4\pi T} W(u)
$$

with

$$
u = \frac{r^2 S}{4 T t}
$$

The derivative of drawdown with respect to the natural logarithm of time is:

$$
\frac{\partial s}{\partial \ln(t)}
=
t \frac{\partial s}{\partial t}
=
\frac{Q}{4\pi T} e^{-u}
$$

For late time, $u$ becomes small and $e^{-u}$ approaches 1. Therefore, the
derivative approaches the plateau:

$$
d = \frac{Q}{4\pi T}
$$

This relationship is useful because the plateau value directly depends on
transmissivity.