# Water-balance closure

MWW01 · TU Dresden · Version 0.2.0

Developed by Dr.-Ing. Thomas Reimann for TU Dresden and The Groundwater Project.

## Launch

Extract the ZIP and open a terminal in the folder containing `app.py`. With Python 3.11 or newer, run

```shell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Classroom demonstration

The app starts in English with an unconfined aquifer, homogeneous K = 10⁻⁴ m/s, boundary heads of 4 and 1 m, and an initial middle-cell head of 4 m.

- In **Water balance / Newton**, adjust the head manually in 0.0001 m increments or use **Compute one Newton step**. Each correction uses the full flow-residual derivative. If needed, the correction is halved until it stays within the boundary-head interval and decreases the residual magnitude. The details expander displays the actual calculation and any damping.
- In **Head computation / Picard**, select **Compute the middle cell**. Subsequent clicks use **Update with the next iteration step**. The plot reports the change from the previous head. The previous-step button retraces the calculation.
- Set **Head-change tolerance** in **Model settings**. The head-change criterion uses the absolute change between successive Picard heads. The water-balance view uses the existing 0.01% relative budget tolerance. Both methods solve the same balance, and either method can in general be checked with both criteria.
- Turn off **Unconfined flow** to see the confined case. Equal, constant conductances give 2.5 m in one update. A second Picard update confirms zero head change.

Changing the activity, aquifer type or starting head resets both experiments to the selected starting head. Changing language retains the current calculation. Changing the head tolerance re-evaluates the current Picard step. Changing homogeneous K rescales the flows and retains the current heads.

The unconfined calculation uses arithmetic-mean saturated thickness at each face. Its equilibrium head is √8.5 m ≈ 2.915476 m. The diagram has a base at 0 m and top at 5 m. All permitted heads lie below the top. The confined aquifer has a base at −2 m and top at 0 m. Cell-centre spacing is 100 m and out-of-plane width is 1 m.

## Editing and translations

`app.py` contains the interface and iteration state. `hydraulics.py` contains Darcy discharges, the Picard update and the Newton derivative and correction. `plots.py` draws the cross-section and observation wells. Each Python file includes a table of contents.

`text/en/` contains the original English text. Parallel `de`, `es`, `it`, `hi`, `zh` and `ar` folders contain German, Spanish, Italian, Hindi, Simplified Chinese and Arabic. Each folder includes a `ui.json` for interface labels and Markdown files for teaching text. Keep JSON keys and formatting placeholders identical across languages. Equations are shared in the Python code and Markdown mathematical notation.

Translated figure labels are browser text aligned with the same cell centres as the Matplotlib figure. This supports script shaping and font fallback for Hindi, Chinese and Arabic. Arabic prose reads right-to-left while the physical left/right arrangement and mathematical expressions keep their standard orientation. `style.css` controls the responsive layout.

Calculations use m, s and m³/s internally. The budget readout shows m³/d. Numeric values retain full floating-point precision, with compact formatting for display.
