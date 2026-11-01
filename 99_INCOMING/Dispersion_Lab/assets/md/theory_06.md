### Highlighted and background particles carry the same mass

Let H be the number of highlighted particles (1–10) and B the number of background particles per highlighted particle (0–1000). The total is

$$
N=H(1+B),\qquad m_p=\frac1N.
$$

There are H numbered markers and HB blue background markers, at most 10,010 in total. Background markers are independent samples of the same transport process; they are **not clones** of a visible path. Highlighting is a display choice and has no effect on motion or mass.

At a fixed particle seed, the numerical engine preserves the release times and complete trajectories of the first H markers when B changes. The interface normally advances the seed on Rerun to draw a new realization; enter an earlier sample’s recorded seed to reproduce it. Play replays the current sample. The total normalized injected mass remains 1, so each marker's statistical weight changes to 1/N. This is an increase in sampling resolution, not an additional physical dose. With independent samples, typical sampling errors decrease approximately as N⁻¹ᐟ²; more particles do not create stronger dispersion.

### Read the plots as mass distributions

At every time, the model partitions all markers into three disjoint groups:

$$
N_{\mathrm{waiting}}+N_{\mathrm{inside}}+N_{\mathrm{collected}}=N.
$$

The spatial bars give collected mass per outlet, $n_k/N$. In temporal bin b with width $\Delta t_b$, the plotted height is

$$
h_b=\frac{n_b}{N\Delta t_b}.
$$

Its units are s⁻¹. The complete histogram has area 1; an incomplete histogram integrates to the collected fraction. This is a normalized arrival mass rate, not a resident concentration. Converting it to an outlet concentration would require injected mass and water discharge, with a consistent flux-averaging convention. Those conversions are not implemented here.

The exact reference describes the probability distribution of this model. Empirical standard deviations use division by N, appropriate to the plotted empirical distribution. They are not N−1 estimates. With one marker, the empirical width is zero even when the population width is positive. Ten markers are useful for understanding paths, not for establishing a smooth distribution.

### Limits to keep in view

The marker model omits sorption, reaction, density effects, collisions, explicit molecular diffusion, and diffusion into immobile regions. The grain model additionally omits pore-body storage, pore-body hydraulic resistance, and velocity profiles within throats. Instantaneous junction mixing is imposed rather than resolved. Thus spatial spreading, node redistribution, and molecular homogenization must not be treated as interchangeable processes (Dentz et al., 2023).

Parameter changes can affect several quantities together: spacing changes board size, grain variation changes mean size as well as variability, and pressure changes velocity. State what was held constant before attributing an observed change to a single mechanism.
