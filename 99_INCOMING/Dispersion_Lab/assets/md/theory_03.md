### Travel time and release time are different quantities

In variable-time mode, step times are independent positive lognormal variables with mean **μ** and coefficient of variation **c = standard deviation / mean**. Direction and step time are sampled independently. For a standard normal variable Z, the code uses

$$
\tau=\mu\exp\!\left(\sigma_\ell Z-\frac{\sigma_\ell^2}{2}\right),\qquad \sigma_\ell^2=\ln(1+c^2).
$$

Thus E[τ] = μ and Var(τ) = μ²c². For the **transit time** T, measured from a particle's own release to its collection,

$$
T=\sum_{j=1}^n\tau_j,\qquad \mathrm{E}[T]=n\mu,\qquad \mathrm{Var}(T)=n\mu^2c^2.
$$

This is a deliberately simple random-walk construction, related conceptually to classical random-step descriptions (Saffman, 1959). The lognormal choice is an instructional assumption, not an empirical law for all soils. Real pore-flow velocity correlations can matter; correlated continuous-time random walks address this additional structure (de Anna et al., 2013).

### A longer injection also broadens arrival times

Let **R** denote release time and **d** the injection duration. R is sampled uniformly on [0,d], independently of route and transit time; for an impulse, R = 0. The **arrival time** A is measured from the start of the whole injection:

$$
A=R+T,\qquad \mathrm{E}[A]=\frac d2+\mathrm{E}[T],\qquad
\mathrm{Var}(A)=\frac{d^2}{12}+\mathrm{Var}(T).
$$

Where probability densities exist, the arrival distribution is the convolution of the release distribution and the transit-time distribution:

$$
f_A(t)=\int_0^t f_R(s)f_T(t-s)\,\mathrm{d}s.
$$

For fixed transit time, this reduces to a shifted copy of the injection signal. A finite injection can therefore broaden the outlet record **without any transit-time dispersion**. The app reports both mean transit time and mean arrival time to keep this distinction visible. A single histogram bar for simultaneous arrivals represents a point mass using a finite bin; its height is not a physical peak concentration.

**Prediction:** with n = 12, μ = 1 s and c = 0.6, transit-time variance is 4.32 s². Adding a 6 s injection contributes another 3 s² to arrival-time variance. These are population values; a small sample fluctuates.
