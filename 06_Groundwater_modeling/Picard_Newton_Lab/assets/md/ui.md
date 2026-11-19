## title
Picard & Newton · Groundwater iteration lab

## page_title
Picard & Newton Lab

## s1
01 · From the water balance to the iteration

## s2
02 · An idealized three-cell model

## s3
03 · Eleven cells: increasing complexity

## preset
Suggested pre-settings

## locked_preset_help
The Mehl (2006) cases use the published aquifer and evapotranspiration settings. To enable these toggles under General model settings, choose one of the three editable Confined or Unconfined cases in Suggested pre-settings.

## et_preset
Unconfined · with evapotranspiration

## left
Left prescribed head (m)

## right
Right prescribed head (m)

## kl
K, left cell (m/s)

## kc
K, central cell (m/s)

## kr
K, right cell (m/s)

## initial
Initial central head (m)

## unconfined
Unconfined aquifer

## et_enable
Enable evapotranspiration in the central cell

## et_surface
ET surface elevation (m)

## et_depth
Extinction depth (m)

## et_max
Maximum ET rate (mm/year)

## recharge
Uniform recharge (mm/year)

## omega
Damping factor ω

## omega_help
1 = full step. A smaller value reduces the proposed correction. It does not guarantee convergence.

## reset
Reset

## reset_notice
Changed model settings: iteration histories restarted.

## ready
Initial guess

## running
Iterating

## converged
Converged

## singular
Singular linear system; reset or change the initial head

## dry
Step rejected: head at or below the aquifer bottom

## cycle
Two-step cycle detected; reset or change the initial head

## limit
Iteration limit reached

## diverged
Non-finite or excessively large proposed head

## status
{method}: {status} · accepted steps: {steps}

## reference
Reference heads · analytical comparison

## no_reference
No wet solution was independently verified for these settings. Review the parameters.

## maps
Click here for additional explanation about the Cobweb Plot

## scalar_caption
Read the current head on the horizontal axis. Thin dotted orange lines connect inputs to the iteration construction; solid orange segments show the Picard cobweb or Newton tangents. Picard transfers each accepted update to the diagonal. The solid vertical segment at the current Picard head reaches the function value from above or below; it shows the current evaluation, without accepting another update. Newton follows the residual tangent to zero. Axes stay fixed unless you enable zoom. Zoom changes the view only.

## coupled_caption
The eleven-cell Picard panel shows the latest accepted construction on its own full-system head function. That function changes with the other heads; all accepted heads remain in the history plots. Newton's reduced flow residual is fixed for this model and can show all accepted tangents.

## residuals
Convergence: head change and flow residual

## residual_caption
Green = Picard; blue = Newton. Squares = flow residual (right, purple axis and closure); circles = head change (left, ochre axis and closure). Both log axes stay at 1E-12–100. Both max|Δh| < {head_tol:.0e} m and max|F| < {flow_tol:.0e} m³/s must pass. No head change exists at k = 0. Edge triangles mark values below (▼, including zero) or above (▲) the view. Limits outside the view still apply. These measures are not errors relative to the reference head.

## head_history
Head history in cell {cell}

## head_history_caption
Actual head after each accepted update, with the initial guess at k = 0. The independent true head is a visual reference; it is not used as an iteration stopping test. k counts accepted updates, not time steps.

## off
No ET

## linear
Linear ET interval

## maximum
Maximum ET

## gradient
Increase gradient · right head to 0.5 m

## heterogeneous
Add three conductivity zones

## zone1
Zone 1 · cells 1–5 · K (m/s)

## zone2
Zone 2 · cell 6 · K (m/s)

## zone3
Zone 3 · cells 7–11 · K (m/s)

## cell
Cell to investigate (interior cells 2–10)

## initial_mode
Initial head profile

## initial_linear
Linear between boundaries

## initial_uniform
Uniform interior head

## uniform_value
Uniform initial interior head (m)

## assess
Check your understanding

## assessment_info
Select all correct statements (one or more). In this lab, only selected correct options earn points: one point each. Unselected and incorrect options earn no points; there are no deductions. Fully correct means all correct options selected and no incorrect options selected. In the OPAL/ONYX scoring scheme used in this course, correctly leaving an incorrect option unselected also earns one point.

## check
Check answer

## score
Points for correct selections: {score}/{total}

## answer_full
Fully correct

## answer_partial
Partially correct

## answer_wrong
Incorrect

## assessment_details
Incorrect options selected: {incorrect}. Correct options still missing: {missing}. Points alone do not establish full correctness.

## theory_quiz
Foundations

## three_quiz
Three-cell balance and iteration

## references
References and model scope

## confined_preset
Confined · without evapotranspiration

## unconfined_preset
Unconfined · without evapotranspiration

## learn_theory
Learn more · derive Picard and Newton

## notes_three
Learn more · assumptions and suggested experiments

## notes_grid
Learn more · the full model and coupled updates

## learn_three
Explore · the three-cell model and evapotranspiration

## learn_grid
Explore · eleven cells and increasing complexity

## language_proxy
Content is available in English, German, French, Spanish, Italian, Hindi, Arabic and Simplified Chinese. Missing translations use English.

## closure
Closure criteria

## head_closure
Maximum head-change closure (m)

## flow_closure
Maximum flow-residual closure (m³/s)

## closure_help
Both checks must pass. Defaults are 1E-4 m for head change and 1E-6 m³/s for flow residual. In the small-flow cases in Mehl (2006), the flow check can pass before the head settles. Changing closure reassesses the saved iterate and can resume a run.

## sync
Sync

## sync_help
Initially off: each play button advances its own method. Turn on to link both buttons inside one frame; either active button then advances both available methods. Converged or stopped methods remain unchanged.

## to_closure
Run to closure

## to_closure_help
Choose a full run instead of a single update, then press an active play button. This toggle alone does not run or reset the model. With Sync on, both available methods run to closure or a diagnosed stopping condition.

## play_method
▶ {method}

## converged_method
✓ {method}

## stopped_method
■ {method}

## play_help
Attempt one update for {methods}.

## run_help
Continue {methods} to closure or a diagnosed stopping condition.

## stopped_help
{method}: {status}.

## outside_view
{method}: current head {head:.3f} m is outside this view. Its numerical value is retained in the history.

## advanced
Advanced option · damping

## advanced_help
Damping multiplies a proposed correction by ω. A value below 1 takes a shorter numerical step; this can help convergence but does not guarantee it.

## conductivity_help
Choose 1 or 5 within each decade: 10⁻⁶, 5×10⁻⁶, …, 10⁻³ m/s.

## fig_cell
Cell {cell}

## fig_cell_number
Cell number

## fig_specified
Specified head

## fig_final
Reference head

## fig_top
Aquifer top: {top:g} m

## fig_bottom
Bottom: {bottom:g} m

## conductance_heading
1 · Turn head differences into flows

## balance_heading
2 · Assemble the water balance

## picard_heading
3 · Rearrange the balance for Picard

## newton_heading
4 · Linearize the balance for Newton

## compare_heading
Worked examples from Mehl (2006)

## convergence_heading
Decide when to stop

## fig_optional_et
Optional ET

## fig_recharge
Recharge

## current_head
Current head: **{head:.3f} m**

## zoom
Auto-zoom

## zoom_auto
Auto-zoom

## zoom_manual
Manual zoom

## zoom_help
Centre the function's crossing with the diagonal (Picard) or zero line (Newton). Initially, the current head lies two-thirds of the way from the centre to the nearer edge. Keep the width until its distance from the centre is less than 25% of the half-width; expand if the head leaves the window. The minimum full width is 0.001 m. Switch auto-zoom off to restore the full view, or use − Zoom / + Zoom for manual widths. Changing model inputs or initial heads restores the full view. Zoom never changes the computed heads.

## zoom_in
+ Zoom

## zoom_out
− Zoom

## zoom_in_help
Manual zoom in: choose the next smaller full head range from 1, 0.1, 0.01, 0.001, 1E-4 and 1E-5 m. This switches auto-zoom off and keeps the selected width across iterations. The function crossing stays centred. Changing the model inputs or initial heads restores the full view.

## zoom_out_help
Manual zoom out: choose the next larger full head range from 1E-5, 1E-4, 0.001, 0.01, 0.1 and 1 m. This switches auto-zoom off and keeps the selected width across iterations. The function crossing stays centred. Changing the model inputs or initial heads restores the full view.

## general_settings
General model settings

## initial_boundary
Initial & boundary conditions

## aquifer_parameters
Aquifer & ET parameters

## uniform_k
Uniform K (m/s)

## grid_quiz
Coupled iteration and nonlinearity

## paper_case
Mehl (2006) figure pair

## paper_smooth
Smooth unconfined balance · Figures 2 and 3

## paper_et
Piecewise balance with ET · Figures 5 and 6

## true_head_column
Reference h (m)

## hydraulic_parameters
Aquifer parameters

## mehl_smooth_preset
Mehl (2006) · unconfined without ET · Figures 2 and 3

## mehl_et_preset
Mehl (2006) · unconfined with ET · Figures 5 and 6

## use_paper_case
Use this Mehl (2006) case in section 2

## initial_picard
Initial central head · Picard (m)

## initial_newton
Initial central head · Newton (m)

## mehl_conductivity
| Cell | K (m/day equivalent) |
|:--|--:|
| 1 | {kl:g} |
| 2 | {kc:g} |
| 3 | {kr:g} |

## mehl_k_help
The paper's conductivity numbers are interpreted here as m/day and converted internally to m/s, exactly as in section 1.

## fig_display_top
Display limit: {top:g} m

## model_preview
Model preview

## head_check_wait
Head-change check: available after the first update.

## head_check
Max |Δh| = {value:.2e} m; limit {threshold:.0e} m — {result}.

## flow_check
Max |F| = {value:.2e} m³/s; limit {threshold:.0e} m³/s — {result}.

## criterion_met
✓ met

## criterion_unmet
not yet met

## fig_residual_method
{method} · flow residual

## fig_change_method
{method} · head change

## fig_head_method
{method} · head

## fig_true_head_history
Reference head ({head:.3f} m)

## fig_flow_closure
Flow closure ({value:.0e} m³/s)

## fig_head_closure
Head closure ({value:.0e} m)

## fig_head_axis
Head in cell {cell} (m)

## slider_input
Use slider for initial head

## iteration_summary
**h = {head:.3f} m** · k = {steps} · {status}

## analytical_head_column
Analytical h (m)

## analytical_difference_column
Reference − analytical (m)

## analytical_unavailable
The homogeneous analytical comparison is unavailable for heterogeneous conductivity or ET.

## coupled_map_help
The blue Newton curve shows the selected cell’s flow imbalance when the other eight interior cells balance at each trial head. This gives one fixed curve for the selected cell and setup. The orange dot marks the current estimate. Each tangent reaches the full Newton proposal, and damping can shorten the accepted step. The convergence plot uses the flow imbalances at the actual nine heads.

The Picard panel shows the latest accepted full nine-head update. Its green curve and diagonal crossing can move as the other heads change. When the selected head barely moves, the Picard curve holds the other input heads fixed. The history plots retain all accepted heads.


## fig_step_fraction
Step fraction $\alpha$

## fig_iteration_axis
Iteration $k$

## fig_head_detail
Near reference · < 1 cm

## postprocessing
Postprocessing options

## side_by_side
Show plots side-by-side

## fig_zoom_range
{mode} on {width:.3g} m head range

## foundations_quiz
Why iteration is needed

## conductance_quiz
Conductance and Darcy flow

## balance_quiz
Water balance and nonlinearity

## et_quiz
Groundwater evapotranspiration

## picard_quiz
Picard iteration

## newton_quiz
Newton iteration

## mehl_quiz
Interpreting Mehl (2006)

## author_credit
Developed by **Thomas Reimann** (2026) · TUD Dresden University of Technology · The Groundwater Project · based on [Mehl (2006)](https://doi.org/10.1111/j.1745-6584.2006.00207.x)
