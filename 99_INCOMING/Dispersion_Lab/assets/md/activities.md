### A sequence for careful comparisons

1. **Routes before statistics:** use the fixed experiment with one marker, then ten. Predict the next decision and explain why arrival times are identical.
2. **Sampling:** in Pinboard experiment, run ten highlighted particles. Set 50, 100, then 1,000 background particles each and rerun. Each rerun draws a new sample. Does the sampled outlet distribution approach the model reference?
3. **Transit-time spread:** save a regular-board comparison. Switch to variable times without changing geometry or mean step time. Explain why the outlet-position reference is unchanged while arrival times spread.
4. **Source duration:** compare impulse and finite-duration injection at zero time CV. Check that the mean transit time stays fixed while the arrival-time distribution changes.
5. **Geometry and flow:** open Grain network. Inspect the static preview before running. Change the grain-size factor at zero grain variation, then vary the pressure. Compare your predictions with the flow and transit-time results.
6. **One change at a time:** introduce grain variability, remembering that this also changes mean grain size. Keep the grain seed fixed when exploring particle sampling; use a recorded particle seed for paired comparisons of a single physical change.

Before interpreting a difference, identify the observable: outlet position, transit time, arrival time, or a normalized mass fraction. None of these alone is a molecular mixing measure.

For a paired comparison, first save a run and note its seed. Rerun once, then change the physical setting and enter the saved run’s seed explicitly. This reproduces its random choices under the new conditions; Play alone replays the current result.
