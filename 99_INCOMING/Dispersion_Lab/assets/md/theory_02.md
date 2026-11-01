### Independent choices create transverse spreading

At every pin, a marker moves one row forward and either left or right. Each decision is independent, with probability 1/2. Let **n** be the number of rows and **a** the horizontal and flowwise increment. After **K** rightward choices, the outlet position is

$$
K\sim\mathrm{Binomial}(n,1/2),\qquad X_n=a(2K-n).
$$

Counting the possible decision sequences gives the exact outlet probabilities:

$$
\Pr[X_n=a(2k-n)]=\binom{n}{k}2^{-n},\qquad k=0,\ldots,n.
$$

The mean and variance follow by adding independent signed increments:

$$
\mathrm{E}[X_n]=0,\qquad \mathrm{Var}(X_n)=na^2,\qquad \sigma_x=a\sqrt{n}.
$$

This is the coin-toss version of the Galton-board principle illustrated by [Yale Physics](https://yppsweb2.its.yale.edu/physics/demos/demomain.asp?id=4G10.10&task=viewdemo). The finite distribution is **binomial**, not exactly Gaussian. A normal approximation improves as the number of independent steps increases, especially away from the tails. Adding more particles samples a fixed distribution more clearly; it does not change its theoretical width.

### What fixed times do—and do not—show

If each step lasts **μ** seconds, every marker traverses the board in

$$
T=n\mu,\qquad \mathrm{Var}(T)=0.
$$

An instantaneous pulse therefore spreads across outlets but arrives everywhere at the same time. At integer step times before collection, the population variance satisfies

$$
\mathrm{Var}[X(t)]=2D_{T,\mathrm{board}}t,\qquad D_{T,\mathrm{board}}=\frac{a^2}{2\mu}.
$$

This is an effective transverse random-walk coefficient for the ideal board. Between nodes, the app linearly interpolates the motion for visualization; the displayed continuous trajectory is not a Brownian path. The coefficient is not a fitted soil dispersivity. With fixed n, changing a changes both the spread and the physical board dimensions.

**Prediction:** doubling n increases the population standard deviation by √2; doubling the number of markers leaves that population value unchanged.
