# Dispersion laboratory — review version 2.4.0

A multipage Streamlit teaching module connecting individual pathways to solute
spreading in space and time. The original regular pinboard, variable-time board,
and grey-grain hydraulic network are retained. The transport engine is unchanged from v2.3 except for navigation comments and the exported version
number. Both configurable pages allow 2–40 rows and start at 20. No numerical
equation or random stream changed.

## Start

Extract the ZIP, open a terminal in `Dispersion_Lab`, then run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Verified with Python 3.12 and Streamlit 1.50.0. Use a virtual environment.
After installing dependencies, no account, external service, or network access
is needed to run the app. External reference links are optional reading.

## Review sequence

1. **Overview:** orientation, with the complete possible pathway network.
2. **Principles and guided experiment:** basic physical processes, optional pinboard
   equations and a licensed Galton-board photograph. A fixed 20-row board starts
   with one marker; only the highlighted count (1–10) is adjustable. Every particle
   arrives at 20 s. Pegs are drawn below the pale decision nodes.
3. **Pinboard experiment:** choose regular or variable travel times; change rows
   (2–40), spacing, mean time and time CV; add background particles from the outset.
4. **Grain network:** change grain geometry and driving pressure. Decorative grains
   fill the rectangular surroundings, while the computed network stays triangular.
5. **References and model notes:** detailed equations, sources, limitations and a
   table mapping every setting to its location.

**Run highlighted particles starts animation immediately** for the full planned
cohort: H highlighted + HB blue background markers. N = H(1+B) ≤ 10,010. All carry
mass 1/N. A first run uses the configured seed (initially 42). After that, **Rerun highlighted
particles** draws a new realization: it advances the seed when the displayed seed
matches the previous run, or respects a seed explicitly changed by the user. Both
rerun buttons share this behavior. **Play** replays the existing calculated run.
Different samples can still share outlets; a new realization is not a promise of
a visibly different result. At an identical seed, the numerical engine retains
its reproducible prefix when the cohort size changes. Adding particles improves
sampling; it does not increase injected mass.

The setup preview is centred at 80% width in a subtle raised frame. The actual
transport board stays full width. Image dimensions reserve space during rerenders.
**Board and transport** follows **How to use this experiment**, followed by
**Particles and injection plan**. Muted blue, teal and sand mark the main steps;
advanced controls use light grey. The sidebar and language flags are unchanged.

An empty transport board is visible below **Observe the transport** before Run.
The Run button is outside expanders. Animation uses an eight-second display clock for the guided and pinboard pages
and a 60-second clock for the grain network by default; rendering and device speed can add a short delay. Model time is unchanged.
The collapsed **Progress through the experiment** expander contains Start, the progress bar, and Final result. Play and Pause sit together; Previous
step and Next step become available while paused. They follow the selected marker's
node events. The live bar becomes a seek slider when paused. Old slider events
cannot undo a later playback command. The two arrival plots follow the board,
side by side, including at the final result.

The guided page has no comparisons or downloads. Pinboard and grain experiments
combine **Repeat, compare, and download** in one expander: save the current run,
then use **Rerun with new particle realization**, styled like the main run button.
This calculates a new run and autoplays it; the saved comparison remains. Background counts use increments
of 50, up to 1,000 per highlighted marker. Extra display settings are collapsed.
Particle position and pathway details follow the results tools.

The pinboard retains its schematic vertical scale of two. The grain network uses
equal horizontal/vertical scales, so circular grains remain circular. Coordinates
and calculations remain unchanged; this is explicitly stated beside the preview.
The extra grains are decorative and do not alter flow or source geometry. An
area source has not been introduced: that remains a separate possible extension.

The Run button is directly under Observe the transport; other experiment widgets
remain in named expanders. The sidebar follows the Soil
Water Retention style: topic buttons, selected-page arrow, language flags, and
centered/wide layout. Native `st.navigation` provides stable page URLs.

The initial board is always stationary. Changing physical settings hides the
old trajectories and shows the new empty transport board until a new run; it cannot overlay old paths on new geometry.
Saved comparisons remain available. Guided, pinboard and grain experiments have
separate state. Language/navigation changes pause playback and retain progress.

A newly calculated run brings **Observe the transport** into view once, keeping
the Run/Rerun button visible, including a run started from the comparison expander. Later animation frames do not reposition the
page. This enhancement uses a small zero-height HTML component that targets the
module's own heading anchor after its new figure is ready; it does not change URLs, navigation or transport. The run
callback commits the complete result before rendering, avoiding an intermediate
empty page. Playback and statistics remain functional without browser scripting.

All active background markers are drawn; coincident particles overlap truthfully.
Highlighted particles have numbers and distinct colours; the selected path is
thicker. Their table exposes status, release/arrival time, final outlet, and the
complete selected node sequence. Collected highlighted markers stay at outlets.

## Files

| File or folder | Purpose |
|---|---|
| `app.py` | Standalone multipage entry point |
| `dispersion_lab/navigation.py` | Sidebar shell and language controls |
| `dispersion_lab/pages.py` | Overview, principles, guided experiment, references |
| `dispersion_lab/ui.py` | Configurable experiment, staged controls, playback, exports |
| `dispersion_lab/experiment.py` | Preview, reproducible seed policy, background expansion and paused stepping |
| `dispersion_lab/presentation.py` | Shared figure, expander and one-time scroll helpers |
| `assets/css/experiment.css`, `assets/js/focus_transport.js` | Scoped appearance and one-time run focus |
| `CODE_GUIDE.md`, `CODE_INDEX.md` | Manual-edit guidance and exact source line index |
| `dispersion_lab/model.py` | Original numerical engine and exact model references |
| `dispersion_lab/plots.py` | Stationary board, trajectories, outlet distributions |
| `dispersion_lab/i18n.py` | Soil Water Retention-style translation helpers |
| `content/` | Thin page wrappers for file-based host navigation |
| `assets/md/` | English source and `_de.md` translations |
| `assets/figures/` | Four original illustrations, EN/DE, PNG/SVG, plus attributed CC BY-SA photograph |
| `review/Theory_Review_v2_0.docx` | Preserved previous theory review; its UI mapping describes v2.0 |
| `review/Theory_Review.md`, `Theory_Review_de.md` | Editable compiled EN/DE text |
| `scripts/` | Reproducible figure and review-document generation |
| `tests/` | Scientific invariants and Streamlit integration tests |
| `VERIFICATION.txt` | Actual checks, environment, and limits |

Internal numerical units are m, s, Pa, and m³/s. Plots use mm and s. JSON keys and
CSV column names remain language-neutral machine identifiers in English.

## Multilingual convention — same as Soil Water Retention update

The shell uses the shared `st.session_state["language"]` value and the same flag
order: EN, DE, IT, ES, PT, FR, ZH, AR, HI. The helpers have the same calling pattern:

```python
ui_text("English label", de="Deutsche Beschriftung", fr="Libellé français")
load_md(MD_DIR, "theory_01.md", st.session_state.language)
```

Markdown lookup is `theory_01_<language>.md`, then the English `theory_01.md`.
Paths are resolved from the package location, not from the working directory.
**Complete scientific text, experiment controls, and axes are supplied in English
and German.** Navigation labels support all nine languages; the other seven
currently use the documented English fallback for scientific content and controls.
The sidebar states this explicitly. Add translated Markdown suffix files and
keyword translations to extend coverage without changing navigation or state.

## Integration into a larger multipage app

The parent owns `st.set_page_config`, `st.navigation`, and the language selector.
Copy `dispersion_lab/` and `assets/` together; place that parent directory on the
Python import path. Register the callables alongside existing module pages:

```python
from dispersion_lab.pages import overview, principles, references
from dispersion_lab.ui import render_page, render_pinboard

# Register with the host's existing st.navigation call:
module_pages = [
    st.Page(overview, title="Dispersion overview", url_path="dispersion"),
    st.Page(principles, title="Principles", url_path="dispersion-principles"),
    st.Page(render_pinboard, title="Pinboard", url_path="dispersion-pinboard"),
    st.Page(render_page, title="Grain network", url_path="dispersion-explore"),
    st.Page(references, title="References", url_path="dispersion-references"),
]
```

See the executable `multipage_example.py`. It demonstrates parent-owned native
navigation; do not call the standalone `run_module()` inside another navigation
router. Hosts with execution-based page loaders can use the wrappers in `content/`.
The shared language key is intentional; experiment states use `disp_guided`, `disp_pinboard` and
`disp_explore`, with namespaced widget keys. Use one instance of each per session.

## Results and model interpretation

Comparisons, exact-reference statistics, CSV, and JSON remain on the pinboard and
grain pages. Playback controls remain on all three experiment pages.
Statistics and downloads describe the entire calculated run, even during early
playback. Saved curves also show the complete saved experiment. Temporal histogram
height is count/(N × bin width); complete area is 1. These are normalized arrival
mass rates, not resident concentrations. Standard deviations describe the empirical
distribution (division by N). No soil dispersivity is fitted.

The grain-size factor is the previous packing control with a clearer name. It is
not measured porosity. Grain variability changes both variability and mean radius.
Spacing changes grain scale and domain size. The triangular geometry and imposed
pressure boundaries affect results. Cylindrical throats, mean tube velocities,
and instantaneous node mixing remain stated teaching assumptions. Molecular
diffusion, reaction, within-pore profiles, and pore-body storage are not resolved.
Local upward motion in the grain drawing is possible when the next node has lower
pressure. Slow connections have small flow and therefore long finite travel times.
Neither behavior is suppressed. A bilingual explanation and pressure/travel-time
columns in the pathway details make these effects inspectable. See
`review/Travel_Time_Review_v2_4.md` for the renewed independent hydraulic and
travel-time checks, including three 10,010-particle cohorts.
Verification confirms the equations as implemented; it is not field validation.

## Movie feasibility

A movie can provide smoother rendering and native play/pause/seeking, but converting
each run into a full video is not a small drop-in change. Exact particle-node steps,
live arrival plots and the existing Streamlit controls need synchronization.
The current renderer took about 0.43–0.61 s per board-plus-distributions frame in a
small local benchmark. A naive 60 s / 24 fps export would therefore take roughly
10–15 minutes just to render, before encoding. This is a measured-current-renderer
estimate, not a lower bound for an optimized implementation.

The current player is retained. If smoother playback is needed later, a browser
animation interpolating the already computed trajectories is the more promising
option; it would need a separate implementation and parity checks. A video would
not itself remove the temporal compression caused by a rare late arrival. See
`review/Playback_Assessment_v2_4.md` for the assessment and sources.

## Verification and regenerating illustrations

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/make_figures.py
python scripts/build_review.py --markdown-only
python scripts/update_code_index.py
```

`build_review.py` additionally requires Pandoc and python-docx; neither is an app
runtime dependency. It compiles the same Markdown used in the app into a Word
document with native equations and creates bilingual review Markdown. Calculated figures are
original. The Galton-board photograph is by Mark Hebner (CC BY-SA 4.0); attribution
is in the app and assets/figures/THIRD_PARTY_LICENSES.txt. The Word file from v2.0
is preserved as a versioned reference; current v2.4 text is in Markdown. See `VERIFICATION.txt`
for browser and document checks actually completed for this release.

Optional browser reproduction (tested with Playwright 1.51.0 and Chromium 134):

```bash
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py
```

Every Python source file includes a line-numbered code map. After manual edits,
run `python scripts/update_code_index.py` to refresh those maps and `CODE_INDEX.md`.
Run `python scripts/update_code_index.py --check` to detect stale line numbers.

The browser script uses localhost only, starts and stops both example servers,
and writes temporary QA output outside the source tree.
