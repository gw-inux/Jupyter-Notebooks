"""Picard & Newton Lab — standalone app and course page.

TABLE OF CONTENTS — search for the numbered section comments below.
  1. UI defaults, language, figure display and stored iteration histories
  2. Presets, remembered ET inputs, iteration callbacks and profile emphasis
  3. Shared experiment controls and output
     3a. Closure selectors and play/synchronize/reset toolbar
     3b. Compact status feedback and iteration/convergence figures
         Remembered auto/manual zoom (display state only)
     3c. Cached theory figures
  4. Section 1: illustrated derivation and assessment
  5. Section 2: idealized three-cell experiment and assessment
  6. Section 3: eleven-cell experiment and assessment
  7. Sources, scope and authorship

Maintenance: prose and theory-image placement are in assets/md/*.md;
assessments are in questions/<language>/*.json; reviewed figures are in assets/theory/.
Experiment plots are in plots.py; equations and stopping rules are in model.py.
UI defaults are passed
explicitly to the solver, whose standalone defaults remain unchanged.
Run: python -m streamlit run app.py
"""

from dataclasses import replace
from io import BytesIO
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit can execute this page from a course in a different repository folder.
# Import under the lab package name so a course can also have its own ui.py or model.py.
package_parent = str(Path(__file__).resolve().parent.parent)
if package_parent not in sys.path:
    sys.path.append(package_parent)

from Picard_Newton_Lab.model import (
    YEAR,
    FLOW_TOL,
    K_STEPS,
    initial_state,
    advance,
    refresh_closure,
    reference,
    analytical_heads,
    cell_slice,
    idealized_model,
    teaching_grid_model,
    mehl_model,
    mehl_initial_heads,
    MAX_STEPS,
)
from Picard_Newton_Lab.ui import (
    LANGUAGES,
    translator,
    load_ui,
    read_md,
    render_md,
    assessment,
    head_input,
    toolbar_style,
    settings_style,
    durable_toggle,
)
from Picard_Newton_Lab import plots

# 1. UI defaults and shared helpers
INITIAL_HEAD_STEP = 0.1  # m; retains the paper's exact starting values.
INITIAL_HEAD_CLOSURE = 1e-4  # m; flow closure uses FLOW_TOL (m³/s).

# Widget state is updated before each rerun, so the translated page title is
# available before drawing the selector. Configure the page before any UI.
lang = st.session_state.get("picard_newton_language", "en")
t = translator(lang)
# A course can set its own layout and sidebar. Standalone Streamlit defaults to centered.
st.set_page_config(page_title=t("page_title"), page_icon="💧")
st.selectbox(
    "🌐", list(LANGUAGES), format_func=LANGUAGES.get, key="picard_newton_language"
)
labels = load_ui(lang)
settings_style()
st.caption(t("language_proxy"))
st.title(t("title"))
st.info(read_md("intro", lang))


@st.cache_data(show_spinner=False)
def get_reference(model):
    return reference(model)


def show_figure(fig):
    st.pyplot(fig, width="stretch")
    plt.close(fig)


def section_heading(key, color, intro):
    st.subheader(f":{color}-background[{t(key)}]", divider=color)
    render_md(intro, lang)


def method_starts(start):
    """Accept one shared vector or the paper's two method-specific vectors."""
    return (
        start if isinstance(start, dict) else {m: start for m in ("Picard", "Newton")}
    )


def reset_zoom_views(key):
    """A new experiment starts both method panels in the ordinary full view."""
    for method in ("picard", "newton"):
        zoom_key = key + "_" + method + "_zoom"
        st.session_state[zoom_key] = False
        st.session_state.pop(zoom_key + "_view", None)


def histories(key, model, start, omega):
    # Closure criteria are intentionally excluded: they can resume saved heads.
    starts = method_starts(start)
    signature = (
        model.signature(),
        tuple(tuple(float(v) for v in starts[m]) for m in ("Picard", "Newton")),
        float(omega),
    )
    saved = st.session_state.get(key)
    if saved is None or saved["signature"] != signature:
        if saved is not None:
            st.caption(t("reset_notice"))
        # Reset both zoom modes with the same model/start/damping signature
        # that restarts the numerical experiment. Layout, cell and closure
        # changes do not enter this signature and keep their existing behavior.
        reset_zoom_views(key.removesuffix("_states"))
        st.session_state[key] = {
            "signature": signature,
            "methods": {
                method: initial_state(model, starts[method])
                for method in ("Picard", "Newton")
            },
        }
    return st.session_state[key]["methods"]


# 2. Suggested pre-settings and callbacks (run before plots on the next rerun)
def apply_three_preset():
    preset = st.session_state.get("three_preset", "mehl_smooth")
    paper = preset.startswith("mehl_")
    base = mehl_model(preset[5:]) if paper else idealized_model(preset)
    st.session_state.update(
        three_left=base.left,
        three_right=base.right,
        three_h0=4.0,
        three_kl=1e-4,
        three_kc=1e-4,
        three_kr=1e-4,
        three_unconfined=base.unconfined,
        three_et=base.et_max > 0,
    )
    if paper:
        starts = mehl_initial_heads(preset[5:])
        st.session_state.update(
            three_h0_picard=starts["Picard"][1],
            three_h0_newton=starts["Newton"][1],
            three_head_exp=int(np.log10(INITIAL_HEAD_CLOSURE)),
            three_flow_exp=int(np.log10(FLOW_TOL)),
        )
        reset_zoom_views("three")
    values = {
        "surface": base.et_surface,
        "depth": base.et_depth,
        "etmax": base.et_max * 1000 * YEAR if paper else 1000.0,
    }
    st.session_state["three_et_values"] = values
    for name, value in values.items():
        st.session_state["three_" + name] = value


def use_paper_case():
    st.session_state["three_preset"] = "mehl_" + st.session_state["paper_case"]
    apply_three_preset()
    st.session_state.pop("three_states", None)


def remember_et(name):
    st.session_state["three_et_values"][name] = st.session_state["three_" + name]


def advance_methods(
    state_key, model, methods, omega, head_tol, flow_tol, full_run=False
):
    """Run the requested methods and emphasize accepted updates in the three-cell profile."""
    experiment = st.session_state[state_key]
    states = experiment["methods"]
    before = {method: len(states[method]["heads"]) for method in methods}
    for _ in range(MAX_STEPS if full_run else 1):
        for method in methods:
            advance(
                model,
                states[method],
                method,
                omega,
                head_tol=head_tol,
                flow_tol=flow_tol,
            )
        if all(states[m]["status"] not in ("ready", "running") for m in methods):
            break
    if model.n == 3:
        experiment["profile_methods"] = tuple(
            m for m in methods if len(states[m]["heads"]) > before[m]
        )


def reset_methods(state_key, model, start, methods=("Picard", "Newton")):
    starts = method_starts(start)
    experiment = st.session_state[state_key]
    for method in methods:
        experiment["methods"][method] = initial_state(model, starts[method])
    if "profile_methods" in experiment:
        experiment["profile_methods"] = tuple(
            m for m in experiment["profile_methods"] if m not in methods
        )


def apply_gradient():
    if st.session_state["grid_gradient"]:
        st.session_state["grid_right_saved"] = st.session_state.get("grid_right", 8.0)
        st.session_state["grid_right"] = 0.5
    else:
        st.session_state["grid_right"] = st.session_state.get("grid_right_saved", 8.0)


# 3. Shared experiment controls and output
# 3a. Closure in model setup; one control row above the function plots


def closure_values(key):
    return (
        10.0
        ** st.session_state.get(key + "_head_exp", int(np.log10(INITIAL_HEAD_CLOSURE))),
        10.0 ** st.session_state.get(key + "_flow_exp", int(np.log10(FLOW_TOL))),
    )


def scientific(value):
    return f"{value:.0e}".replace("e-0", "E-").replace("e+0", "E+")


def closure_inputs(key):
    st.session_state.setdefault(key + "_head_exp", int(np.log10(INITIAL_HEAD_CLOSURE)))
    st.session_state.setdefault(key + "_flow_exp", int(np.log10(FLOW_TOL)))
    with st.expander(t("closure"), key=key + "_closure"):
        st.select_slider(
            t("head_closure"),
            options=list(range(-8, -1)),
            format_func=lambda e: scientific(10.0**e),
            key=key + "_head_exp",
        )
        st.select_slider(
            t("flow_closure"),
            options=list(range(-15, -5)),
            format_func=lambda e: scientific(10.0**e),
            key=key + "_flow_exp",
        )
        st.caption(t("closure_help"))


def step_controls(key, state_key, model, states, start, omega, head_tol, flow_tol):
    """Mode switches only change the next click; they never run or reset a solver."""
    play_col, sync_col, run_col, reset_col = st.columns(
        [2.6, 1.0, 1.3, 0.8], gap="xsmall", vertical_alignment="center"
    )
    with sync_col:
        sync = durable_toggle(t("sync"), key=key + "_sync", help=t("sync_help"))
    with run_col:
        full_run = durable_toggle(
            t("to_closure"), key=key + "_to_closure", help=t("to_closure_help")
        )
    active = tuple(m for m, s in states.items() if s["status"] in ("ready", "running"))
    # A shared frame identifies synchronized operation without merging buttons.
    # Stable container/widget keys preserve both histories when modes change.
    toolbar_style(key, sync)
    with play_col.container(border=False, key=key + "_play_group"):
        buttons = st.columns(2, gap="xsmall", wrap=False)
    for col, method in zip(buttons, ("Picard", "Newton")):
        status = states[method]["status"]
        available = method in active
        methods = active if sync else (method,)
        label = (
            "play_method"
            if available
            else "converged_method" if status == "converged" else "stopped_method"
        )
        col.button(
            t(label, method=method),
            key=key + "_" + method.lower() + "_step",
            type="primary" if available else "secondary",
            width="stretch",
            disabled=not available,
            help=(
                t("run_help" if full_run else "play_help", methods=" + ".join(methods))
                if available
                else t("stopped_help", method=method, status=t(status))
            ),
            on_click=advance_methods,
            args=(state_key, model, methods, omega, head_tol, flow_tol, full_run),
        )
    reset_col.button(
        t("reset"),
        icon="🔄",
        key=key + "_reset",
        width="stretch",
        on_click=reset_methods,
        args=(state_key, model, start),
    )


# 3b. Compact feedback, function plots and convergence histories
def iteration_feedback(method, state, current):
    """One result line; detailed criteria remain in the convergence plots."""
    st.markdown(
        t(
            "iteration_summary",
            head=current,
            status=t(state["status"]),
            steps=len(state["heads"]) - 1,
        )
    )
    if state["status"] not in ("ready", "running", "converged"):
        st.warning(
            t(
                "status",
                method=method,
                status=t(state["status"]),
                steps=len(state["heads"]) - 1,
            )
        )


def postprocessing_inputs(key):
    with st.expander(t("postprocessing"), key=key + "_postprocessing"):
        st.toggle(t("side_by_side"), value=True, key=key + "_side_by_side")


def individual_controls(
    key, state_key, model, states, start, method, omega, head_tol, flow_tol
):
    """A method's full-width controls affect only that method's saved history."""
    prefix = key + "_" + method.lower()
    run_col, mode_col, reset_col = st.columns(
        [1.4, 1.2, 0.7], vertical_alignment="center"
    )
    with mode_col:
        full_run = durable_toggle(
            t("to_closure"), key=prefix + "_to_closure", help=t("to_closure_help")
        )
    state = states[method]
    active = state["status"] in ("ready", "running")
    label = (
        "play_method"
        if active
        else (
            "converged_method" if state["status"] == "converged" else "stopped_method"
        )
    )
    run_col.button(
        t(label, method=method),
        key=prefix + "_step",
        width="stretch",
        type="primary" if active else "secondary",
        disabled=not active,
        on_click=advance_methods,
        args=(state_key, model, (method,), omega, head_tol, flow_tol, full_run),
    )
    toolbar_style(prefix, False)
    reset_col.button(
        t("reset"),
        icon="🔄",
        key=prefix + "_reset",
        width="stretch",
        on_click=reset_methods,
        args=(state_key, model, start, (method,)),
    )


def history_output(states, ref, cell, head_tol, flow_tol):
    st.markdown("**" + t("residuals") + "**")
    show_figure(plots.convergence(states, flow_tol, head_tol=head_tol, labels=labels))
    st.markdown("**" + t("head_history", cell=cell + 1) + "**")
    show_figure(
        plots.head_history(states, cell=cell, true_head=ref[cell], labels=labels)
    )


def zoom_view(zoom_key, context, iteration, local, center, current, limits):
    """Keep each panel's viewport separate from its numerical iteration state."""
    record = st.session_state.setdefault(zoom_key + "_view", {})
    if record.get("context") != context or iteration < record.get("iteration", 0):
        record.pop("auto_width", None)
    record.update(context=context, iteration=iteration)
    if st.session_state.get(zoom_key, False):
        view = plots.zoom_limits(
            local, center, current, previous_width=record.get("auto_width")
        )
        record["auto_width"] = view["zoom_range"]
    elif "manual_width" in record:
        view = plots.zoom_limits(local, center, current, width=record["manual_width"])
    else:
        view = limits
    record["shown_width"] = view.get("zoom_range", view["head"][1] - view["head"][0])
    return view


def change_auto_zoom(zoom_key):
    # Enabling auto starts a fresh fit; disabling it restores the full view.
    record = st.session_state.setdefault(zoom_key + "_view", {})
    record.pop("auto_width", None)
    record.pop("manual_width", None)


def change_manual_zoom(zoom_key, closer):
    record = st.session_state[zoom_key + "_view"]
    record["manual_width"] = plots.manual_zoom_width(record["shown_width"], closer)
    record.pop("auto_width", None)
    st.session_state[zoom_key] = False


def zoom_controls(zoom_key, view):
    """A compact row below either plot, with identical keys in both layouts."""
    auto, zoom_out, zoom_in = st.columns(
        [1.6, 1, 1], gap="xxsmall", vertical_alignment="center"
    )
    with auto:
        st.toggle(
            t("zoom"),
            key=zoom_key,
            help=t("zoom_help"),
            on_change=change_auto_zoom,
            args=(zoom_key,),
        )
    width = view.get("zoom_range", view["head"][1] - view["head"][0])
    for col, closer, label, disabled in (
        (
            zoom_out,
            False,
            "zoom_out",
            width >= plots.MANUAL_ZOOM_WIDTHS[0] * (1 - 1e-9),
        ),
        (
            zoom_in,
            True,
            "zoom_in",
            width <= plots.MANUAL_ZOOM_WIDTHS[-1] * (1 + 1e-9),
        ),
    ):
        col.button(
            t(label),
            key=zoom_key + ("_in" if closer else "_out"),
            help=t(label + "_help"),
            width="stretch",
            disabled=disabled,
            on_click=change_manual_zoom,
            args=(zoom_key, closer),
        )


def iteration_output(
    key,
    state_key,
    model,
    states,
    start,
    ref,
    cell,
    omega,
    diagnostic=False,
    head_range=None,
):
    head_tol, flow_tol = closure_values(key)
    for state in states.values():
        refresh_closure(state, head_tol, flow_tol)
    limits = plots.geometry_limits(model, start, ref, cell, head_range)
    beside = st.session_state.get(key + "_side_by_side", True)
    if beside:
        step_controls(key, state_key, model, states, start, omega, head_tol, flow_tol)
    # Different layouts share the same iteration state and plotting functions.
    columns = st.columns(2) if beside else [st.container(), st.container()]
    local = cell_slice(model, ref, cell) if diagnostic else model
    for col, (method, state) in zip(columns, states.items()):
        with col.container(gap="xxsmall"):
            st.markdown("**" + method + "**")
            if not beside:
                individual_controls(
                    key,
                    state_key,
                    model,
                    states,
                    start,
                    method,
                    omega,
                    head_tol,
                    flow_tol,
                )
            current = state["heads"][-1][cell]
            zoom_key = key + "_" + method.lower() + "_zoom"
            zooming = st.session_state.get(
                zoom_key, False
            ) or "manual_width" in st.session_state.get(zoom_key + "_view", {})
            if zooming:
                center = (
                    plots.matching_head(
                        model, state, method, ref[cell], cell, omega, limits
                    )
                    if diagnostic
                    else ref[cell]
                )
            else:
                center = ref[cell]
            view = zoom_view(
                zoom_key,
                (st.session_state[state_key]["signature"], cell),
                len(state["heads"]) - 1,
                local,
                center,
                current,
                limits,
            )
            figure = (
                plots.coupled_geometry(
                    model, state, method, ref[cell], cell, omega, view, labels
                )
                if diagnostic
                else plots.geometry(
                    model,
                    state,
                    method,
                    ref[cell],
                    omega,
                    limits=view,
                    labels=labels,
                )
            )
            if not beside:
                figure.set_size_inches(7.6, 4.0)
            show_figure(figure)
            zoom_controls(zoom_key, view)
            iteration_feedback(method, state, current)
            if not view["head"][0] <= current <= view["head"][1]:
                st.warning(t("outside_view", method=method, head=current))
            if state["rejected"] is not None:
                st.code(
                    "ĥ = "
                    + np.array2string(np.asarray(state["rejected"])[1:-1], precision=3)
                    + " m",
                    language=None,
                )
            if not beside:
                history_output({method: state}, ref, cell, head_tol, flow_tol)
    if beside:
        history_output(states, ref, cell, head_tol, flow_tol)


# 3c. Theory images
@st.cache_data(show_spinner=False)
def theory_images(preset, head_tol, flow_tol, labels):
    """Mehl Figures 2/3 or 5/6: original heads, conductivity ratios and starts.

    Apply a chosen, consistent SI scaling to the paper's numerical parameters.
    Roots and updates are invariant under the common residual scale factor.
    Show the complete current evaluation segment as well as accepted updates.
    """
    images = []
    model = mehl_model(preset)
    ref, _ = reference(model)
    limits = plots.geometry_limits(model, None, ref, head_range=plots.MEHL_HEAD_RANGE)
    for method, start in mehl_initial_heads(preset).items():
        state = initial_state(model, start)
        for _ in range(MAX_STEPS):
            advance(model, state, method, head_tol=head_tol, flow_tol=flow_tol)
            if state["status"] not in ("ready", "running"):
                break
        figure = plots.geometry(
            model, state, method, ref[1], limits=limits, labels=labels
        )
        stream = BytesIO()
        figure.savefig(stream, format="png", dpi=180)
        plt.close(figure)
        images.append(stream.getvalue())
    return images


# 4. Illustrated derivation: editable Markdown and iNUX checks; details folded
section_heading("s1", "blue", "section1_intro")
with st.expander(t("learn_theory"), expanded=False, key="theory_section"):
    for page, bank in [
        ("foundations", "foundations"),
        ("conductance", "conductance"),
        ("balance", "balance"),
        ("evapotranspiration", "et"),
        ("picard", "picard"),
        ("newton", "newton"),
    ]:
        render_md(page, lang)
        assessment(bank, lang, t)
    st.markdown("**" + t("compare_heading") + "**")
    render_md("compare", lang)
    # Resend the selected label after translation. Otherwise the browser can send
    # the previous language's label on the next click instead of the stored case.
    st.session_state["paper_case"] = st.session_state.get("paper_case", "smooth")
    paper_case = st.selectbox(
        t("paper_case"),
        ["smooth", "et"],
        format_func=lambda v: t("paper_" + v),
        key="paper_case",
    )
    render_md("mehl_" + paper_case, lang)
    images = theory_images(paper_case, INITIAL_HEAD_CLOSURE, FLOW_TOL, labels)
    for col, method, figure in zip(st.columns(2), ("Picard", "Newton"), images):
        col.markdown("**" + method + "**")
        col.image(figure, width="stretch")
    st.button(t("use_paper_case"), key="use_paper_case", on_click=use_paper_case)
    assessment("mehl", lang, t)
    st.markdown("**" + t("convergence_heading") + "**")
    render_md("convergence", lang)
    assessment("theory", lang, t)
    render_md("next_steps", lang)


# 5. Idealized three-cell experiment
section_heading("s2", "green", "section2_intro")
if "three_left" not in st.session_state:
    st.session_state.setdefault("three_preset", "mehl_smooth")
    apply_three_preset()
with st.columns([1, 5, 1])[1]:
    st.caption(t("model_preview"))
    show_figure(
        plots.three_schematic(
            labels,
            left=st.session_state["three_left"],
            right=st.session_state["three_right"],
            height=(
                5.0
                if st.session_state.get("three_preset", "").startswith("mehl_")
                else 8.0
            ),
        )
    )
with st.expander(t("learn_three"), expanded=True, key="three_section"):
    # Keep the preset ID and refresh its translated browser label on every rerun.
    st.session_state["three_preset"] = st.session_state["three_preset"]
    preset = st.selectbox(
        t("preset"),
        ["mehl_smooth", "mehl_et", "confined", "unconfined", "et"],
        format_func=lambda v: t(v + "_preset"),
        key="three_preset",
        on_change=apply_three_preset,
    )
    paper = preset.startswith("mehl_")
    if paper:
        paper_model = mehl_model(preset[5:])
        render_md("mehl_experiment", lang)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**" + t("general_settings") + "**")
        preset_help = t("locked_preset_help") if paper else None
        unconf = st.toggle(
            t("unconfined"), key="three_unconfined", disabled=paper, help=preset_help
        )
        et_on = st.toggle(
            t("et_enable"), key="three_et", disabled=paper, help=preset_help
        )
        closure_inputs("three")
        postprocessing_inputs("three")
    with c2.expander(t("initial_boundary"), expanded=False, key="three_boundary"):
        hl = st.number_input(
            t("left"),
            min_value=0.01 if paper else 0.5,
            max_value=8.0,
            step=0.01 if paper else 0.5,
            key="three_left",
            disabled=paper,
        )
        hr = st.number_input(
            t("right"),
            min_value=0.01 if paper else 0.5,
            max_value=8.0,
            step=0.01 if paper else 0.5,
            key="three_right",
            disabled=paper,
        )
        if paper:
            starts = {
                method: [
                    paper_model.left,
                    head_input(
                        t("initial_" + method.lower()),
                        minimum=0.01,
                        maximum=8.0,
                        default=mehl_initial_heads(preset[5:])[method][1],
                        step=INITIAL_HEAD_STEP,
                        key="three_h0_" + method.lower(),
                        t=t,
                    ),
                    paper_model.right,
                ]
                for method in ("Picard", "Newton")
            }
        else:
            h0 = head_input(
                t("initial"),
                minimum=0.5,
                maximum=8.0,
                default=4.0,
                step=INITIAL_HEAD_STEP,
                key="three_h0",
                t=t,
            )
    with c3.expander(t("aquifer_parameters"), expanded=False, key="three_aquifer"):
        if paper:
            st.markdown(
                t(
                    "mehl_conductivity",
                    **dict(
                        zip(
                            ("kl", "kc", "kr"),
                            np.asarray(paper_model.conductivity) * 86400,
                        )
                    ),
                )
            )
            st.caption(t("mehl_k_help"))
        else:
            kvals = tuple(
                st.select_slider(
                    t(name),
                    options=K_STEPS,
                    format_func=scientific,
                    key="three_" + name,
                    help=t("conductivity_help"),
                )
                for name in ("kl", "kc", "kr")
            )
        values = st.session_state["three_et_values"]
        if et_on:
            for name in ("surface", "depth", "etmax"):
                st.session_state["three_" + name] = values[name]
            st.number_input(
                t("et_surface"),
                min_value=0.01 if paper else 0.5,
                max_value=8.0,
                step=0.01 if paper else 0.5,
                disabled=paper,
                key="three_surface",
                on_change=remember_et,
                args=("surface",),
            )
            st.number_input(
                t("et_depth"),
                min_value=0.01 if paper else 0.5,
                max_value=8.0,
                step=0.01 if paper else 0.5,
                disabled=paper,
                key="three_depth",
                on_change=remember_et,
                args=("depth",),
            )
            st.number_input(
                t("et_max"),
                min_value=0.0,
                max_value=5000.0,
                step=0.01 if paper else 100.0,
                disabled=paper,
                key="three_etmax",
                on_change=remember_et,
                args=("etmax",),
            )
    model = (
        paper_model
        if paper
        else replace(
            idealized_model("unconfined" if unconf else "confined"),
            conductivity=kvals,
            left=hl,
            right=hr,
            et_max=values["etmax"] / 1000 / YEAR if et_on else 0.0,
            et_surface=values["surface"],
            et_depth=values["depth"],
        )
    )
    ref, verified = get_reference(model)
    if not verified:
        st.warning(t("no_reference"))
    else:
        start = starts if paper else [model.left, h0, model.right]
        states = histories("three_states", model, start, 1.0)
        with st.container(border=True):
            show_figure(
                plots.profile(
                    model,
                    ref,
                    states,
                    1,
                    labels,
                    active_methods=st.session_state["three_states"].get(
                        "profile_methods", ()
                    ),
                )
            )
        iteration_output(
            "three",
            "three_states",
            model,
            states,
            start,
            ref,
            1,
            1.0,
            head_range=plots.MEHL_HEAD_RANGE if paper else (0.0, 8.0),
        )
    assessment("three", lang, t)


# 6. Eleven cells: every iteration solves all nine interior heads
section_heading("s3", "orange", "section3_intro")
with st.expander(t("learn_grid"), expanded=False, key="grid_section"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**" + t("general_settings") + "**")
        u = st.toggle(t("unconfined"), value=True, key="grid_unconfined")
        g = st.toggle(
            t("gradient"), value=False, key="grid_gradient", on_change=apply_gradient
        )
        het = st.toggle(t("heterogeneous"), value=False, key="grid_heterogeneous")
        closure_inputs("grid")
        postprocessing_inputs("grid")
        with st.expander(t("advanced"), key="grid_damping"):
            st.markdown(t("advanced_help"))
            omega = st.slider(
                t("omega"),
                0.05,
                1.0,
                1.0,
                0.05,
                help=t("omega_help"),
                key="grid_omega",
            )
    with c2.expander(t("initial_boundary"), expanded=False, key="grid_boundary"):
        hl = st.number_input(
            t("left"),
            min_value=0.5,
            max_value=20.0,
            value=18.0,
            step=0.5,
            key="grid_left",
        )
        hr = st.number_input(
            t("right"),
            min_value=0.5,
            max_value=20.0,
            value=8.0,
            step=0.5,
            disabled=g,
            key="grid_right",
        )
        recharge = st.number_input(
            t("recharge"),
            min_value=0.0,
            max_value=1000.0,
            value=150.0,
            step=25.0,
            key="grid_recharge",
        )
        initial_mode = st.radio(
            t("initial_mode"),
            ["initial_linear", "initial_uniform"],
            format_func=t,
            key="grid_initial_mode",
        )
        uniform = head_input(
            t("uniform_value"),
            minimum=0.5,
            maximum=30.0,
            default=12.0,
            step=INITIAL_HEAD_STEP,
            disabled=initial_mode == "initial_linear",
            key="grid_uniform",
            t=t,
        )
    with c3.expander(t("hydraulic_parameters"), expanded=False, key="grid_aquifer"):
        conductivity = st.select_slider(
            t("uniform_k"),
            options=K_STEPS,
            value=1e-4,
            format_func=scientific,
            key="grid_k",
            disabled=het,
        )
        zones = tuple(
            st.select_slider(
                t("zone" + str(i + 1)),
                options=K_STEPS,
                value=value,
                format_func=scientific,
                disabled=not het,
                key="zone_" + str(i),
            )
            for i, value in enumerate((1e-6, 1e-4, 1e-3))
        )
    model = teaching_grid_model(u, g, het, recharge, zones, conductivity, hl, hr)
    ref, verified = get_reference(model)
    if not verified:
        st.warning(t("no_reference"))
    else:
        start = np.linspace(model.left, model.right, model.n)
        if initial_mode == "initial_uniform":
            start[1:-1] = uniform
        states = histories("grid_states", model, start, omega)
        cell = (
            st.slider(t("cell"), 2, 10, 6, key="grid_cell", help=t("coupled_map_help"))
            - 1
        )
        with st.container(border=True):
            show_figure(plots.profile(model, ref, states, cell, labels))
        with st.expander(t("reference"), key="grid_reference"):
            reference_data = {
                "i": range(1, model.n + 1),
                "x (m)": np.arange(model.n) * model.dx,
                "K (m/s)": model.conductivity,
                t("true_head_column"): ref,
            }
            exact = analytical_heads(model)
            if exact is not None:
                reference_data[t("analytical_head_column")] = exact
                reference_data[t("analytical_difference_column")] = ref - exact
            st.dataframe(
                pd.DataFrame(reference_data),
                hide_index=True,
                width="stretch",
                column_config={
                    "K (m/s)": st.column_config.NumberColumn(format="%.2e"),
                    t("true_head_column"): st.column_config.NumberColumn(format="%.3f"),
                    t("analytical_head_column"): st.column_config.NumberColumn(
                        format="%.3f"
                    ),
                    t("analytical_difference_column"): st.column_config.NumberColumn(
                        format="%.2e"
                    ),
                },
            )
            if exact is None:
                st.caption(t("analytical_unavailable"))
        iteration_output(
            "grid",
            "grid_states",
            model,
            states,
            start,
            ref,
            cell,
            omega,
            diagnostic=True,
        )
    assessment("grid", lang, t)

# 7. Sources, scope and authorship
with st.expander(t("references"), key="scope_section"):
    render_md("scope", lang)

st.divider()
st.caption(t("author_credit"))
