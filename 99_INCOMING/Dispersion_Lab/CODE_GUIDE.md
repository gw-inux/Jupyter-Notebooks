# Manual editing guide

The module separates the numerical model, experiment orchestration, plots and
presentation. Each Python source file begins with a code map containing exact line
numbers, including nested playback callbacks. `CODE_INDEX.md` collects those maps.
After editing, refresh with `python scripts/update_code_index.py`; use `--check`
to detect stale references. The updater changes module docstrings only.

| Change | Edit here | Guidance |
|---|---|---|
| Default particle counts, row count, per-page playback duration | `dispersion_lab/ui.py` → `session` | Guided physical values are also explicit in `experiment`; update its bilingual explanatory text consistently. |
| Board/particle/injection controls and order | `ui.py` → `parameter_controls`, `particle_controls`, `injection_controls`, `experiment` | All stages share these helpers. The fixed guided page omits board and injection controls. |
| First Run and subsequent Rerun | `ui.py` → `run_experiment`; `experiment.py` → `realization_config` | Both rerun buttons call the same function. Play uses the stored result. Seed advancement is deterministic and independent of the numerical random streams. |
| Pause, seek and node stepping | `ui.py` → `playback`; `experiment.py` → `step_fraction` | Preserve revisioned slider keys and the read-only live bar; delayed events must not override later commands. |
| Preview width, export resolution, reserved image dimensions | `presentation.py` → constants and `show_figure` | Preview is 80%; the full transport view stays 100%. Reserve width/height to avoid page collapse while decoding a new image. |
| Expander tints, frame and button colours | `assets/css/experiment.css` | Rules use module-owned names; avoid global typography or sidebar styles. Main roles: blue, teal, sand; advanced tools: quiet grey. |
| One-time focus on Observe the transport | `presentation.py` → `focus_transport`; `assets/js/focus_transport.js` | Each calculation gets its own figure ID. Once ready, scroll to the page’s Observe heading so Run stays visible; do not refocus on every animation frame or alter URLs. The zero-height component handles display only. |
| Shape and scale of boards | `plots.py` → `_board_base` | Grain network has equal x/y scaling. Pinboard's vertical stretch is schematic. Do not alter numerical coordinates to achieve a visual change. |
| Arrival plots | `plots.py` → `distribution_figure` | Keep normalized mass accounting and the complete-run bin edges stable during playback. |
| Governing equations and random sampling | `model.py` | No UI imports. Preserve scientific tests; require a separate scientific review for physics changes. |
| Scientific text, instructions and translations | `assets/md/`; `dispersion_lab/i18n.py` | English filename, translated suffix, English fallback. Keep display math between `$$` delimiters and use `pages.markdown` to render it. |
| Page registry, sidebar and language flags | `navigation.py`; `content/`; `pages.py` | Shared language state and existing Soil Water Retention convention are retained. |
| Reusable parent integration | `multipage_example.py` | The parent owns page configuration and navigation. Copy `dispersion_lab/` and `assets/` together. |

A first calculation uses the displayed seed. If Rerun sees the same seed as the
current run, it advances that seed by one (wrapping after 1,000,000). A different
seed entered explicitly is respected. For a paired comparison with an earlier
sample, enter that earlier sample's recorded seed. For example: save seed 42,
rerun to seed 43, then change one physical parameter and enter 42 to compare with
the saved run. Play always replays the current sample without resampling.

To verify edits:

```bash
python scripts/update_code_index.py
python scripts/update_code_index.py --check
python -m pytest -q
python tests/browser_smoke.py
```

The browser test additionally needs Playwright and Chromium. It checks full and
parent launchers, first/repeated runs, scroll focus, quiet styling, previews,
plot persistence, downloads and language changes. Screenshots are temporary QA
files and are not needed by the app.
