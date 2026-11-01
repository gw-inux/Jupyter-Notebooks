# Movie and smoother-playback assessment — version 2.4

30 October 2026. Recommendation: retain the present player for this revision. A smoother browser-rendered animation is feasible as a separate, optional enhancement.

## What the current app does

A run computes complete particle paths, release times and node-arrival times once. Playback interpolates positions between those events and draws the board and arrival distributions at the chosen model time. Play, Pause and seeking do not recompute transport. A new realization invokes the numerical model again.

The present interface refreshes at a nominal 0.8-second interval. The animation is therefore a sequence of scientific snapshots, and the underlying trajectory data are already suitable for smoother interpolation.

## Options

| Option | Benefits | Additional work or limits |
|---|---|---|
| Keep the current player | Retains existing controls, exact node stepping, tables, plots and language handling | Modest frame rate; server redraws figures |
| Render an MP4 after each calculation | Smooth playback with ordinary video play/pause and seeking; convenient export | Render and encode many frames; extra startup delay and encoder dependency; custom synchronization for existing controls and statistics |
| Animate the computed data in the browser | Smooth display without producing thousands of raster figures; exact model-time/node selection can be retained | A small dedicated renderer and player, serialized path data, synchronization with statistics/inspection, and numerical/visual parity tests |

The official [Streamlit 1.50 st.video documentation](https://docs.streamlit.io/1.50.0/develop/api-reference/media/st.video) supports video display, starting/ending times, looping and autoplay. It does not expose callbacks for the current playback time or an API to bind the existing Streamlit Pause and node-step buttons directly to the native player. MDN documents [native video controls](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video) and [currentTime seeking](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime); those mechanisms can be controlled inside a custom browser component.

A pre-rendered video also samples model time into a finite number of frames. The existing Previous/Next buttons select exact node-event times. Preserving that scientific inspection behavior would require a time mapping and, where an event falls between video frames, an exact redraw or another overlay—not simply replacing the plot with st.video.

## Measured cost of a straightforward export

A small local benchmark rendered six representative board-plus-distribution frame pairs per configuration, using 10 highlighted + 10,000 background particles and the existing 130-dpi renderer.

| Grain rows | Mean render time per frame pair | Frames for 60 s at 24 fps | Extrapolated rendering time |
|---:|---:|---:|---:|
| 20 | 0.429 s | 1,440 | 618 s ≈ 10.3 min |
| 40 | 0.613 s | 1,440 | 883 s ≈ 14.7 min |

These are extrapolations from a small sample on this execution environment, not a full movie export, a performance guarantee or a lower bound. They exclude encoding and delivery. Reusing artists, caching the static background or reducing resolution could substantially reduce the cost. Nevertheless, calling the current renderer for every movie frame would add an undesirable wait to each interactive experiment.

Reproduce with `python scripts/benchmark_playback.py benchmark.json`. Raw measurements are in `video_render_benchmark_v2_4.json`.

## Suggested future approach

If smoother motion becomes a priority, prototype browser-side interpolation using the already verified trajectories. A canvas can retain the static board and redraw moving markers on the browser's animation cycle; [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) supplies display-timed updates. Use elapsed timestamps, not frame counts, as the clock. Keep the model's finite event times, arrival statistics and random realization unchanged.

Before replacing the current view, verify at least: positions at known times and node events; pause/seek/resume; all 10,010 markers; final histograms and saved comparisons; mobile and EN/DE controls; page changes and tab suspension; and reproducible data exports. Statistics may need fewer visual refreshes than moving markers, while remaining tied to the same model-time value.

This is a manageable feature, but it is a separate implementation and verification task rather than a minor display setting. No video, new rendering engine, encoder dependency or timing transformation has been added in this release. The 60-second grain default and existing exact step controls address the immediate usability request.

Smoother frames would not remove the compression caused by a very late arrival: a movie using the same linear time range still shows most particles early. That is a time-scale interpretation issue, addressed separately in the travel-time review.
