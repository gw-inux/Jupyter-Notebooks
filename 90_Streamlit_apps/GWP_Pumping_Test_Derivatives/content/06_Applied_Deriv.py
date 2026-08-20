# Loading the required Python libraries
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullFormatter
import numpy as np
import pandas as pd
import streamlit as st

from GWP_Pumping_Test_Derivatives_utils import load_css
from applied_derivative_utils import (
    clean_time_drawdown,
    conceptual_model_response,
    compute_log_derivative,
    default_conceptual_initial,
    detect_plateau,
    fit_conceptual_model,
    format_parameter_summary,
    hampel_flags,
    log_reduce,
    moving_average,
    plateau_transmissivity,
    savgol_smooth,
)

# ------------------------------------------------------------
# Authors, institutions, and year
# ------------------------------------------------------------

year = 2026
authors = {"Thomas Reimann": [1, 2]}
institutions = {
    1: "The Groundwater Project",
    2: "TU Dresden, Institute for Groundwater Management",
}

author_list = []
for name, indices in authors.items():
    superscript = ",".join(str(i) for i in indices)
    author_list.append(f"{name}<sup>{superscript}</sup>")

institution_list = []
for i, inst in institutions.items():
    institution_list.append(f"<sup>{i}</sup> {inst}")
institution_text = ", ".join(institution_list)

# ------------------------------------------------------------
# Paths (retain project convention, with a local fallback)
# ------------------------------------------------------------

APP_ROOT = Path("90_Streamlit_apps/GWP_Pumping_Test_Derivatives")
if not APP_ROOT.exists():
    APP_ROOT = Path(__file__).resolve().parents[1]

CSS_DIR = APP_ROOT / "assets" / "css"
DATA_DIR = APP_ROOT / "assets" / "data"
APPLIED_DATA_DIR = DATA_DIR / "applied"

load_css(CSS_DIR, "segment_control_Theis_Deriv_Ini.css")

# ------------------------------------------------------------
# Constants / labels
# ------------------------------------------------------------

TIME_FACTORS = {
    "seconds": 1.0,
    "minutes": 60.0,
    "hours": 3600.0,
    "days": 86400.0,
}

DERIVATIVE_METHODS = {
    "Logarithmic difference": "log_difference",
    "Renard et al. (2009)": "renard2009",
    "Neighbouring points": "neighboring_points",
    "Bourdet et al. (1989)": "bourdet1989",
    "Spane & Wurstner (1993)": "spane_wurstner1993",
}

SOLUTIONS = ["Theis", "Hantush-Jacob", "Neuman delayed yield"]
BOUNDARIES = ["No boundary", "Specified-head boundary", "No-flow boundary"]
INNER_EFFECTS = ["None", "Skin", "Wellbore storage", "Wellbore storage + skin"]
DATA_LOCATIONS = ["Observation well", "Pumping well"]
OBSERVATION_GEOMETRIES = [
    "Between pumping well and boundary",
    "Away from boundary",
    "Parallel to boundary",
]

SOLUTION_EXPLANATIONS = {
    "Theis": "Confined, homogeneous aquifer response; T and S are fitted.",
    "Hantush-Jacob": "Leaky confined response; T, S, and leakage factor B are fitted.",
    "Neuman delayed yield": "Unconfined delayed-yield response; T, elastic storativity Sₐ, specific yield Sᵧ, and β are fitted.",
}

# ------------------------------------------------------------
# Small UI / calculation helpers
# ------------------------------------------------------------




def _workflow_navigation(labels: list[str]):
    """Render persistent tab-like workflow navigation.

    The visible segmented control deliberately uses a *temporary widget key*
    while the selected step is mirrored into a separate persistent Session
    State key.  This follows Streamlit's recommended pattern for state that must
    survive widget cleanup/reconstruction.  It is especially important here
    because changing controls inside Steps 2--4 triggers a full app rerun.

    The numerical/calculation branches are unchanged: only the selected step is
    executed after each rerun.
    """
    state_key = "applied_workflow_step"
    widget_key = "_applied_workflow_step_widget"

    # Persistent application state.  Keep this independent from the widget's
    # own state so that a widget reconstruction cannot send the workflow back
    # to Step 1.
    current = st.session_state.get(state_key, labels[0])
    if current not in labels:
        current = labels[0]
    st.session_state[state_key] = current

    # Restore the widget from persistent state only when its own state is absent
    # or invalid.  Do not overwrite it on normal reruns: Streamlit first writes
    # the user's new widget value into Session State before rerunning the page.
    widget_value = st.session_state.get(widget_key)
    if widget_value not in labels:
        st.session_state[widget_key] = current

    def _remember_workflow_step():
        value = st.session_state.get(widget_key)
        if value in labels:
            st.session_state[state_key] = value

    selected = st.segmented_control(
        "Workflow step",
        options=labels,
        key=widget_key,
        on_change=_remember_workflow_step,
        label_visibility="collapsed",
    )

    # The callback runs before the page rerun.  The assignment below is an
    # additional compatibility safeguard for Streamlit versions where callback
    # timing around dynamically executed page files can differ.
    if selected in labels:
        st.session_state[state_key] = selected
    else:
        selected = st.session_state[state_key]

    containers = [st.container() for _ in labels]
    active = [selected == label for label in labels]
    return containers, active


def _read_example_metadata() -> pd.DataFrame:
    return pd.read_csv(APPLIED_DATA_DIR / "dataset_metadata.csv")


@st.cache_data
def _read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def _to_csv_bytes(frame: pd.DataFrame) -> bytes:
    return frame.to_csv(index=False).encode("utf-8")


def _data_signature(*items) -> str:
    payload = json.dumps(items, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _positive_log_bounds(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    good = values[np.isfinite(values) & (values > 0)]
    if len(good) == 0:
        return 0.0, 1.0
    return float(np.log10(good.min())), float(np.log10(good.max()))


def _log_range_slider(label: str, t: np.ndarray, default=None, key=None):
    lo, hi = _positive_log_bounds(t)
    if hi <= lo:
        hi = lo + 0.1
    if default is None:
        default = (lo, hi)
    default = (
        float(np.clip(default[0], lo, hi)),
        float(np.clip(default[1], lo, hi)),
    )
    if default[0] > default[1]:
        default = (default[1], default[0])

    # Range-slider state can survive a change in dataset or processing. Clamp
    # an existing state before rendering so it can never sit outside the new
    # data range and cause a widget-state error.
    if key is not None and key in st.session_state:
        stored = st.session_state[key]
        if isinstance(stored, (tuple, list)) and len(stored) == 2:
            stored = (
                float(np.clip(stored[0], lo, hi)),
                float(np.clip(stored[1], lo, hi)),
            )
            if stored[0] > stored[1]:
                stored = (stored[1], stored[0])
            st.session_state[key] = stored

    values = st.slider(label, lo, hi, default, 0.05, key=key)
    return 10.0 ** values[0], 10.0 ** values[1]


def _default_processing_config() -> dict:
    """Return the deliberately defensive processing defaults."""
    return {
        "exclude_flags": False,
        "use_reduction": False,
        "points_per_decade": 18,
        "smoothing": "None",
        "smooth_window": 1,
        "derivative_label": "Logarithmic difference",
        "L": 0.20,
        "n_neighbors": 2,
    }


def _processing_config() -> dict:
    """Return persistent processing settings, including currently visible widgets.

    Streamlit removes widget-state keys when a widget is no longer rendered.
    Therefore the Step 2 choices are mirrored into the non-widget
    ``applied_processing_settings`` dictionary.  Steps 3 and 4 always read that
    persistent dictionary and cannot silently fall back to defaults after a
    rerun.
    """
    cfg = _default_processing_config()
    saved = st.session_state.get("applied_processing_settings", {})
    if isinstance(saved, dict):
        cfg.update({k: saved[k] for k in cfg if k in saved})

    # When Step 1/2 widgets are currently rendered, their live values override
    # the saved copy. This makes the helper usable before and after persistence.
    widget_map = {
        "exclude_flags": "applied_exclude_flags",
        "use_reduction": "applied_use_reduction",
        "points_per_decade": "applied_points_per_decade",
        "smoothing": "applied_smoothing",
        "derivative_label": "applied_derivative_label",
        "L": "applied_L",
        "n_neighbors": "applied_neighbors",
    }
    for field, widget_key in widget_map.items():
        if widget_key in st.session_state:
            cfg[field] = st.session_state[widget_key]

    smoothing = str(cfg.get("smoothing", "None"))
    cfg["smoothing"] = smoothing
    if smoothing == "Moving average":
        if "applied_moving_window" in st.session_state:
            cfg["smooth_window"] = int(st.session_state["applied_moving_window"])
        else:
            cfg["smooth_window"] = int(saved.get("smooth_window", 7)) if isinstance(saved, dict) else 7
    elif smoothing == "Savitzky-Golay (advanced)":
        if "applied_savgol_window" in st.session_state:
            cfg["smooth_window"] = int(st.session_state["applied_savgol_window"])
        else:
            cfg["smooth_window"] = int(saved.get("smooth_window", 9)) if isinstance(saved, dict) else 9
    else:
        cfg["smooth_window"] = 1

    cfg["exclude_flags"] = bool(cfg["exclude_flags"])
    cfg["use_reduction"] = bool(cfg["use_reduction"])
    cfg["points_per_decade"] = int(cfg["points_per_decade"])
    cfg["derivative_label"] = str(cfg["derivative_label"])
    cfg["L"] = float(cfg["L"])
    cfg["n_neighbors"] = int(cfg["n_neighbors"])
    return cfg


def _persist_processing_config(cfg: dict | None = None) -> dict:
    """Store Step 1/2 processing choices under a non-widget Session State key."""
    if cfg is None:
        cfg = _processing_config()
    clean_cfg = _default_processing_config()
    clean_cfg.update({k: cfg[k] for k in clean_cfg if k in cfg})
    st.session_state["applied_processing_settings"] = clean_cfg
    return clean_cfg


def _processing_caption(cfg: dict) -> str:
    """Human-readable summary of the exact processing carried into later steps."""
    density = "off"
    if cfg["use_reduction"]:
        density = f"on ({cfg['points_per_decade']} points/log-decade)"

    smoothing = cfg["smoothing"]
    if smoothing != "None":
        smoothing = f"{smoothing} (window {cfg['smooth_window']})"

    derivative = cfg["derivative_label"]
    method = DERIVATIVE_METHODS.get(derivative, "log_difference")
    if method in {"bourdet1989", "spane_wurstner1993"}:
        derivative = f"{derivative} (L={cfg['L']:.2f})"
    elif method == "neighboring_points":
        derivative = f"{derivative} ({cfg['n_neighbors']} point(s) per side)"

    return (
        "Using the Step 2 settings unchanged — "
        f"outlier exclusion: **{'on' if cfg['exclude_flags'] else 'off'}**; "
        f"log-time reduction: **{density}**; smoothing: **{smoothing}**; "
        f"derivative: **{derivative}**."
    )


def _process_data(clean_t, clean_s, flags) -> dict:
    """Apply the settings last chosen in Step 1/2.

    This helper is deliberately called only inside the active workflow tab.
    """
    cfg = _processing_config()
    t = np.asarray(clean_t, dtype=float)
    s = np.asarray(clean_s, dtype=float)

    if cfg["exclude_flags"] and np.any(flags):
        t = t[~flags]
        s = s[~flags]

    if cfg["use_reduction"]:
        proc_t, proc_s0 = log_reduce(t, s, points_per_decade=cfg["points_per_decade"])
    else:
        proc_t, proc_s0 = t.copy(), s.copy()

    if cfg["smoothing"] == "Moving average":
        proc_s = moving_average(proc_s0, cfg["smooth_window"])
    elif cfg["smoothing"] == "Savitzky-Golay (advanced)":
        proc_s = savgol_smooth(proc_s0, cfg["smooth_window"], 2)
    else:
        proc_s = proc_s0.copy()

    derivative_method = DERIVATIVE_METHODS.get(cfg["derivative_label"], "log_difference")
    deriv_t, deriv = compute_log_derivative(
        proc_t,
        proc_s,
        method=derivative_method,
        L=cfg["L"],
        n_neighbors=cfg["n_neighbors"],
        positive_only=False,
    )

    return {
        "config": cfg,
        "proc_t": proc_t,
        "proc_s0": proc_s0,
        "proc_s": proc_s,
        "deriv_t": deriv_t,
        "deriv": deriv,
    }


def _plain_log_tick(value, _position=None):
    """Return a mathtext-free base-10 label for a logarithmic major tick.

    Some older Matplotlib/Anaconda combinations can produce malformed mathtext
    tick labels during ``tight_layout`` (for example ``$\\mathdefault{10^{1}}$ ^``).
    Unicode superscripts preserve the familiar ``10^n`` appearance while
    avoiding the mathtext parser entirely. Axis scaling and limits are unchanged.
    """
    if not np.isfinite(value) or value <= 0:
        return ""
    exponent = np.log10(value)
    rounded = int(np.rint(exponent))
    if not np.isclose(exponent, rounded, atol=1e-10, rtol=0.0):
        return ""
    superscript = str(rounded).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"10{superscript}"


def _set_compatible_log_tick_format(ax):
    """Apply log tick formatters that are safe across Matplotlib versions."""
    formatter = FuncFormatter(_plain_log_tick)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(FuncFormatter(_plain_log_tick))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())


def _workflow_plot(
    clean_t,
    clean_s,
    *,
    proc_t=None,
    proc_s=None,
    deriv_t=None,
    deriv=None,
    outlier_flags=None,
    show_outliers=False,
    selected_period=None,
    fit_period=None,
    manual_curve=None,
    fitted_curve=None,
    title="Data and diagnostic response",
):
    """Use one consistent diagnostic plot throughout the workflow.

    Axis limits are determined exclusively from measured/processed data and the
    measured derivative.  Manual or automatically fitted model curves therefore
    cannot rescale Step 4, which keeps its view directly comparable with Step 3.
    """
    fig, ax = plt.subplots(figsize=(9.3, 5.8))

    clean_t = np.asarray(clean_t, dtype=float)
    clean_s = np.asarray(clean_s, dtype=float)
    raw_mask = np.isfinite(clean_t) & np.isfinite(clean_s) & (clean_t > 0) & (clean_s > 0)

    # Collect measured-data values before adding model curves. These values set
    # the fixed plotting window used after all artists have been drawn.
    x_data = [clean_t[raw_mask]]
    y_data = [clean_s[raw_mask]]

    ax.loglog(
        clean_t[raw_mask],
        clean_s[raw_mask],
        ".",
        ms=3.0,
        alpha=0.35,
        label="cleaned measured drawdown",
    )

    if show_outliers and outlier_flags is not None:
        flags_arr = np.asarray(outlier_flags, dtype=bool)
        if flags_arr.shape == clean_t.shape:
            out_mask = raw_mask & flags_arr
            if np.any(out_mask):
                ax.loglog(
                    clean_t[out_mask],
                    clean_s[out_mask],
                    linestyle="None",
                    marker="x",
                    ms=7.0,
                    mew=1.4,
                    zorder=6,
                    label="possible local outlier (Hampel)",
                )

    if proc_t is not None and proc_s is not None:
        pt = np.asarray(proc_t, dtype=float)
        ps = np.asarray(proc_s, dtype=float)
        mask = np.isfinite(pt) & np.isfinite(ps) & (pt > 0) & (ps > 0)
        if np.any(mask):
            x_data.append(pt[mask])
            y_data.append(ps[mask])
        ax.loglog(pt[mask], ps[mask], "o-", ms=3.1, lw=1.0, label="processed drawdown")

    if deriv_t is not None and deriv is not None:
        dt = np.asarray(deriv_t, dtype=float)
        dd = np.asarray(deriv, dtype=float)
        mask = np.isfinite(dt) & np.isfinite(dd) & (dt > 0) & (dd > 0)
        if np.any(mask):
            x_data.append(dt[mask])
            y_data.append(dd[mask])
        ax.loglog(dt[mask], dd[mask], "o-", ms=3.0, lw=1.0, label=r"measured derivative $ds/d\ln(t)$")

    if selected_period is not None:
        p0, p1 = selected_period
        ax.axvspan(p0, p1, alpha=0.10, label="Step 3 selected period")

    # Keep the automatic-fit window deliberately unobtrusive. A small double
    # arrow at the bottom of the axes is enough to show the interval.
    if fit_period is not None:
        f0, f1 = fit_period
        if f0 > 0 and f1 > f0:
            ax.annotate(
                "",
                xy=(f1, 0.035),
                xytext=(f0, 0.035),
                xycoords=ax.get_xaxis_transform(),
                arrowprops={"arrowstyle": "<->", "lw": 0.9, "alpha": 0.75},
                annotation_clip=True,
            )

    if manual_curve is not None:
        mt, ms, md, label = manual_curve
        mt = np.asarray(mt, dtype=float)
        ms = np.asarray(ms, dtype=float)
        md = np.asarray(md, dtype=float)
        m1 = np.isfinite(mt) & np.isfinite(ms) & (mt > 0) & (ms > 0)
        m2 = np.isfinite(mt) & np.isfinite(md) & (mt > 0) & (md > 0)
        ax.loglog(mt[m1], ms[m1], "-", lw=2.0, label=f"manual {label} drawdown")
        ax.loglog(mt[m2], md[m2], "--", lw=1.8, label=f"manual {label} derivative")

    if fitted_curve is not None:
        ft, fs, fd, label = fitted_curve
        ft = np.asarray(ft, dtype=float)
        fs = np.asarray(fs, dtype=float)
        fd = np.asarray(fd, dtype=float)
        m1 = np.isfinite(ft) & np.isfinite(fs) & (ft > 0) & (fs > 0)
        m2 = np.isfinite(ft) & np.isfinite(fd) & (ft > 0) & (fd > 0)
        ax.loglog(ft[m1], fs[m1], "-", lw=2.5, label=f"automatic {label} drawdown")
        ax.loglog(ft[m2], fd[m2], "--", lw=2.2, label=f"automatic {label} derivative")

    # Lock axes to measured/processed data so changing manual fit sliders does
    # not make the diagnostic plot jump or zoom. Step 3 and Step 4 therefore
    # use identical limits whenever the Step 2 processing settings are equal.
    x_good = np.concatenate([arr for arr in x_data if len(arr)]) if any(len(arr) for arr in x_data) else np.array([])
    y_good = np.concatenate([arr for arr in y_data if len(arr)]) if any(len(arr) for arr in y_data) else np.array([])
    if len(x_good):
        xlog = np.log10(x_good)
        xspan = max(float(np.max(xlog) - np.min(xlog)), 0.5)
        xmargin = max(0.05, 0.025 * xspan)
        ax.set_xlim(10.0 ** (float(np.min(xlog)) - xmargin), 10.0 ** (float(np.max(xlog)) + xmargin))
    if len(y_good):
        ylog = np.log10(y_good)
        yspan = max(float(np.max(ylog) - np.min(ylog)), 0.5)
        ymargin = max(0.08, 0.04 * yspan)
        ax.set_ylim(10.0 ** (float(np.min(ylog)) - ymargin), 10.0 ** (float(np.max(ylog)) + ymargin))

    # Use plain-text major tick labels. This is intentionally applied after
    # log scaling and axis-limit locking so it only affects rendering, not any
    # hydraulic calculation or the view established in Steps 1--4.
    _set_compatible_log_tick_format(ax)

    ax.set_xlabel("Elapsed time [s]")
    ax.set_ylabel("Drawdown / derivative [m]")
    ax.set_title(title)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _diagnostic_hints(t, s, td, d, plateau) -> list[str]:
    hints = []
    td = np.asarray(td, dtype=float)
    d = np.asarray(d, dtype=float)
    mask = np.isfinite(td) & np.isfinite(d) & (td > 0) & (d > 0)
    td2, d2 = td[mask], d[mask]
    if len(td2) < 8:
        return ["The derivative contains too few positive points for a stable pattern check."]

    x = np.log10(td2)
    y = np.log10(d2)
    n_tail = max(5, len(td2) // 6)
    late_slope = float(np.polyfit(x[-n_tail:], y[-n_tail:], 1)[0])

    if plateau:
        dp = plateau["d_median"]
        late_ratio = float(np.median(d2[-n_tail:]) / dp)
        after = d2[td2 > plateau["t_end"]]
        if plateau["decades"] >= 0.6 and abs(plateau["slope"]) < 0.2:
            hints.append("A nearly horizontal derivative interval is present; it is a candidate infinite-radial-flow period.")
        if len(after) >= 5 and late_slope < -0.55 and late_ratio < 0.7:
            hints.append("The late derivative turns strongly downward. Leakage or a specified-head boundary are plausible alternatives.")
        if len(after) >= 5 and 1.55 <= late_ratio <= 2.6 and abs(late_slope) < 0.35:
            hints.append("The late derivative approaches roughly twice the selected plateau, which is characteristic of one no-flow boundary.")
        min_ratio = float(np.nanmin(d2) / dp)
        if min_ratio < 0.55 and 0.65 <= late_ratio <= 1.4:
            hints.append("A derivative depression followed by a return toward the plateau can be compatible with delayed yield or another dual-storage process.")

    if not hints:
        hints.append("No single diagnostic signature is sufficiently strong for an automatic conclusion. Test alternative conceptual models and use site information.")
    return hints


def _manual_log_slider(label, key, lo, hi, default, unit=""):
    default_log = float(np.log10(default))
    # A key can persist while the selected conceptual model changes. Clamp a
    # previously stored value before rendering the slider so switching models
    # cannot leave Session State outside the new physical parameter bounds.
    if key in st.session_state:
        st.session_state[key] = float(np.clip(st.session_state[key], float(lo), float(hi)))
    log_value = st.slider(label, float(lo), float(hi), default_log, 0.05, key=key)
    value = 10.0 ** log_value
    st.caption(f"Current value: **{value:.4g}{(' ' + unit) if unit else ''}**")
    return value


def _manual_parameter_controls(
    solution,
    boundary,
    r,
    T_hint,
    observation_position,
    inner_effects="None",
):
    """Render manual/pre-fit controls and return a physically complete parameter dict."""
    initial = default_conceptual_initial(
        solution, boundary, r, T_hint=T_hint, inner_effects=inner_effects
    )
    params = {}

    c1, c2, c3 = st.columns(3)
    with c1:
        params["T"] = _manual_log_slider(
            "log₁₀ T [m²/s]", "applied_manual_logT", -8.0, -1.0, initial["T"], "m²/s"
        )

    if solution in {"Theis", "Hantush-Jacob"}:
        with c2:
            params["S"] = _manual_log_slider(
                "log₁₀ S [-]", "applied_manual_logS", -8.0, -0.3, initial["S"]
            )

    if solution == "Hantush-Jacob":
        with c3:
            params["B"] = _manual_log_slider(
                "log₁₀ B [m]", "applied_manual_logB", -0.3, 6.0, initial["B"], "m"
            )

    if solution == "Neuman delayed yield":
        with c2:
            params["S_a"] = _manual_log_slider(
                "log₁₀ Sₐ [-]", "applied_manual_logSa", -8.0, -1.7, initial["S_a"]
            )
        with c3:
            params["S_y"] = _manual_log_slider(
                "log₁₀ Sᵧ [-]", "applied_manual_logSy", -3.0, -0.2, initial["S_y"]
            )
        c4, _ = st.columns(2)
        with c4:
            params["beta"] = _manual_log_slider(
                "log₁₀ β at evaluation distance [-]",
                "applied_manual_logbeta",
                -4.0,
                1.0,
                initial["beta"],
            )
        if params["S_y"] <= 5.0 * params["S_a"]:
            st.warning("Sᵧ is not much larger than Sₐ. The delayed-yield parameterization may be difficult to interpret.")

    if inner_effects != "None":
        with st.container(border=True):
            st.markdown("##### Inner-boundary parameters")
            i1, i2 = st.columns(2)
            if inner_effects in {"Wellbore storage", "Wellbore storage + skin"}:
                with i1:
                    params["rc"] = _manual_log_slider(
                        "log₁₀ effective storage radius r_c [m]",
                        "applied_manual_logrc",
                        float(np.log10(0.005)),
                        float(np.log10(5.0)),
                        initial["rc"],
                        "m",
                    )
            if inner_effects in {"Skin", "Wellbore storage + skin"}:
                with i2:
                    skin_default = float(initial["skin"])
                    skin_min = 0.0 if inner_effects == "Wellbore storage + skin" else -10.0
                    if "applied_manual_skin" in st.session_state:
                        st.session_state["applied_manual_skin"] = float(
                            np.clip(st.session_state["applied_manual_skin"], skin_min, 100.0)
                        )
                    params["skin"] = st.slider(
                        "Skin factor S_F [-]",
                        float(skin_min),
                        100.0,
                        max(skin_default, skin_min),
                        0.5,
                        key="applied_manual_skin",
                    )
                    if inner_effects == "Wellbore storage + skin":
                        st.caption(
                            "Combined storage + skin uses S_F ≥ 0. Negative skin remains available in the skin-only case."
                        )

    if boundary != "No boundary":
        with st.container(border=True):
            st.markdown("##### Outer-boundary distance")
            if observation_position == "Between pumping well and boundary":
                dmin = max(float(r) * 1.001, 0.5)
            else:
                dmin = 0.5
            d0 = max(initial["D"], dmin * 1.01)
            log_min = float(np.log10(dmin))
            log_default = float(np.log10(d0))
            if "applied_manual_logD" in st.session_state:
                st.session_state["applied_manual_logD"] = float(
                    np.clip(st.session_state["applied_manual_logD"], log_min, 6.0)
                )
            log_D = st.slider(
                "log₁₀ D [m]",
                log_min,
                6.0,
                float(np.clip(log_default, log_min, 6.0)),
                0.05,
                key="applied_manual_logD",
            )
            params["D"] = 10.0 ** log_D
            st.caption(f"Current outer-boundary distance: **{params['D']:.4g} m**")

    return params


def _model_effect_note(
    solution,
    boundary,
    result,
    Q,
    r,
    observation_position,
    inner_effects="None",
):
    params = result["params"]
    notes = []
    if boundary != "No boundary":
        p0 = dict(params)
        p0.pop("D", None)
        base_s, _ = conceptual_model_response(
            solution,
            "No boundary",
            result["time_fit"],
            Q,
            r,
            p0,
            observation_position=observation_position,
            inner_effects=inner_effects,
        )
        effect = float(np.max(np.abs(result["prediction_fit"] - base_s))) / max(
            float(np.max(np.abs(result["prediction_fit"]))), 1e-12
        )
        if effect < 0.05:
            notes.append("Outer-boundary effect <5% in the fit window; D is poorly resolved.")

    if solution == "Hantush-Jacob":
        shared_inner = {}
        if "rc" in params:
            shared_inner["rc"] = params["rc"]
        if "skin" in params:
            shared_inner["skin"] = params["skin"]
        theis_params = {"T": params["T"], "S": params["S"], **shared_inner}
        theis_s, _ = conceptual_model_response(
            "Theis",
            "No boundary",
            result["time_fit"],
            Q,
            r,
            theis_params,
            observation_position=observation_position,
            inner_effects=inner_effects,
        )
        h_params = {"T": params["T"], "S": params["S"], "B": params["B"], **shared_inner}
        h_s, _ = conceptual_model_response(
            "Hantush-Jacob",
            "No boundary",
            result["time_fit"],
            Q,
            r,
            h_params,
            observation_position=observation_position,
            inner_effects=inner_effects,
        )
        effect = float(np.max(np.abs(h_s - theis_s))) / max(float(np.max(np.abs(h_s))), 1e-12)
        if effect < 0.05:
            notes.append("Leakage effect <5% in the fit window; B is poorly resolved.")

    if inner_effects != "None":
        base_inner = dict(params)
        base_inner.pop("rc", None)
        base_inner.pop("skin", None)
        try:
            no_inner_s, _ = conceptual_model_response(
                solution,
                boundary,
                result["time_fit"],
                Q,
                r,
                base_inner,
                observation_position=observation_position,
                inner_effects="None",
            )
            inner_effect = float(np.max(np.abs(result["prediction_fit"] - no_inner_s))) / max(
                float(np.max(np.abs(result["prediction_fit"]))), 1e-12
            )
            if inner_effect < 0.05:
                notes.append("Inner-boundary effect <5% in the fit window; well parameters are poorly resolved.")
        except Exception:
            pass
        if "skin" in params and abs(float(params["skin"])) < 0.2:
            notes.append("The fitted skin factor is close to zero; a distinct skin effect is not resolved.")

    return " ".join(notes)


# ------------------------------------------------------------
# Page heading and orientation
# ------------------------------------------------------------

st.header(":rainbow[Derivatives with measured and own data]", divider="rainbow")
st.markdown(
    """
This section applies the diagnostic-plot workflow to measured or uploaded data. The sequence is deliberately separated into four steps: first inspect the measurements, then explore reduction/smoothing and the derivative, then define the hydraulically meaningful period, and only then fit analytical models.

The default processing is intentionally **defensive**: no statistical outlier is removed, no log-time reduction is applied, and no smoothing is applied. This makes the influence of each processing choice visible instead of hiding it in a preset.
"""
)

# ------------------------------------------------------------
# Shared data source setup (lightweight and needed by every tab)
# ------------------------------------------------------------

with st.expander("**Data source and test information**", expanded=True):
    source = st.segmented_control(
        "**Data source**",
        ["Example dataset", "Upload own CSV"],
        default="Example dataset",
        key="applied_source",
    )

    metadata_row = None
    truth = {}
    source_description = ""
    uploaded = None

    if source == "Example dataset":
        metadata = _read_example_metadata()
        labels = metadata["label"].tolist()
        selected_label = st.selectbox(
            "**Example**",
            labels,
            index=0,
            key="applied_example_label",
            help="Teaching datasets are stored as CSV files under assets/data/applied.",
        )
        metadata_row = metadata.loc[metadata["label"] == selected_label].iloc[0]
        raw_df = _read_csv(str(APPLIED_DATA_DIR / metadata_row["file"]))
        time_col = "time_s"
        value_col = "drawdown_m"
        time_factor = 1.0
        values_are = "Drawdown"
        Q = float(metadata_row["Q_m3s"])
        r = float(metadata_row["r_m"])
        source_description = str(metadata_row["notes"])
        for c in metadata.columns:
            if c.startswith("true_") and pd.notna(metadata_row[c]):
                truth[c.removeprefix("true_")] = float(metadata_row[c])

        c1, c2, c3 = st.columns((2.2, 1, 1))
        with c1:
            st.info(source_description)
        with c2:
            st.metric("Pumping rate Q", f"{Q:.4g} m³/s")
        with c3:
            st.metric("Observation distance r", f"{r:.4g} m")

    else:
        template = pd.DataFrame(
            {
                "time": [1, 2, 5, 10, 20, 50, 100],
                "drawdown": [0.002, 0.006, 0.015, 0.028, 0.043, 0.065, 0.082],
            }
        )
        st.download_button(
            "Download a minimal CSV template",
            data=_to_csv_bytes(template),
            file_name="pumping_test_template.csv",
            mime="text/csv",
        )
        uploaded = st.file_uploader(
            "**Upload CSV**",
            type=["csv", "txt"],
            key="applied_upload",
            help="Use elapsed time since pumping started plus drawdown, water level, or head.",
        )
        if uploaded is None:
            st.info("Upload a CSV to continue with your own data, or switch back to an example dataset.")
            st.stop()
        try:
            raw_df = pd.read_csv(uploaded)
        except Exception as exc:
            st.error(f"The CSV could not be read: {exc}")
            st.stop()
        if raw_df.shape[1] < 2:
            st.error("The uploaded file must contain at least two columns.")
            st.stop()

        st.dataframe(raw_df.head(12), use_container_width=True, hide_index=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            time_col = st.selectbox("**Time column**", raw_df.columns.tolist(), index=0, key="applied_time_col")
            time_unit = st.selectbox("**Time unit**", list(TIME_FACTORS), index=0, key="applied_time_unit")
            time_factor = TIME_FACTORS[time_unit]
        with c2:
            value_candidates = [c for c in raw_df.columns if c != time_col]
            value_col = st.selectbox("**Measured-value column**", value_candidates, index=0, key="applied_value_col")
            values_are = st.selectbox(
                "**Measured values represent**",
                ["Drawdown", "Water level / head"],
                key="applied_values_are",
            )
        with c3:
            Q = st.number_input(
                "**Pumping rate Q [m³/s]**",
                min_value=1e-10,
                value=0.001,
                format="%.6g",
                key="applied_Q",
            )
            r = st.number_input(
                "**Observation distance r [m]**",
                min_value=1e-6,
                value=30.0,
                format="%.6g",
                key="applied_r",
            )

    time_raw_numeric = pd.to_numeric(raw_df[time_col], errors="coerce").to_numpy(dtype=float) * time_factor
    value_raw_numeric = pd.to_numeric(raw_df[value_col], errors="coerce").to_numpy(dtype=float)

    if values_are == "Water level / head":
        finite_values = value_raw_numeric[np.isfinite(value_raw_numeric)]
        if len(finite_values) == 0:
            st.error("No numeric water-level values were found in the selected column.")
            st.stop()
        baseline_default = float(finite_values[0])
        c1, c2 = st.columns((1, 2))
        with c1:
            baseline = st.number_input(
                "**Reference water level/head before pumping**",
                value=baseline_default,
                format="%.8g",
                key="applied_baseline",
            )
        with c2:
            direction = st.radio(
                "**Convention**",
                [
                    "Head/elevation decreases during pumping",
                    "Depth below reference increases during pumping",
                ],
                horizontal=True,
                key="applied_head_direction",
            )
        if direction.startswith("Head"):
            drawdown_raw_numeric = baseline - value_raw_numeric
        else:
            drawdown_raw_numeric = value_raw_numeric - baseline
    else:
        drawdown_raw_numeric = value_raw_numeric

# Mandatory cleaning is shared by all steps: it only handles values that cannot
# be used mathematically (missing/non-numeric, nonpositive time, duplicate time).
clean_t, clean_s, cleaning_report = clean_time_drawdown(time_raw_numeric, drawdown_raw_numeric)
if len(clean_t) < 8:
    st.error("Fewer than 8 valid positive-time observations remain after basic cleaning.")
    st.stop()

# Hampel candidates are cheap to calculate and are never removed by default.
flags = hampel_flags(clean_s, window=9, n_sigma=4.0)

source_id = metadata_row["file"] if metadata_row is not None else getattr(uploaded, "name", "upload")
dataset_signature = _data_signature(
    source,
    source_id,
    len(clean_t),
    float(clean_t[0]),
    float(clean_t[-1]),
    float(np.round(np.nansum(clean_s), 10)),
    float(Q),
    float(r),
)
if st.session_state.get("applied_dataset_signature") != dataset_signature:
    # Reset only results/ranges that depend on the actual dataset. Processing
    # preferences remain unchanged so a user can apply the same settings to a
    # new dataset deliberately.
    for key in [
        "applied_plateau_range",
        "applied_fit_range",
        "applied_primary_fit_bundle",
        "applied_compare_bundle",
    ]:
        st.session_state.pop(key, None)
    st.session_state["applied_dataset_signature"] = dataset_signature

# ------------------------------------------------------------
# Tab-like workflow selector (same approach as earlier sections)
# ------------------------------------------------------------

workflow_labels = [
    "1. Inspect data",
    "2. Filter & derivative",
    "3. Select flow period",
    "4. Fit solutions",
]
(step1, step2, step3, step4), workflow_active = _workflow_navigation(workflow_labels)

# ------------------------------------------------------------
# STEP 1
# ------------------------------------------------------------

if workflow_active[0]:
    with step1:
        st.subheader(":blue[Step 1 — Inspect the measurements]")
        st.markdown(
            "Only mathematically unusable values are removed automatically. Statistical outliers are **not** removed unless you explicitly choose to exclude them after inspection."
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows supplied", f"{cleaning_report.rows_input:,}")
        m2.metric("Usable rows", f"{cleaning_report.rows_output:,}")
        m3.metric("Missing/non-numeric removed", cleaning_report.removed_non_numeric_or_missing)
        m4.metric("Hampel candidates", int(flags.sum()))

        saved_cfg = _processing_config()
        c1, c2 = st.columns(2)
        with c1:
            show_flags = st.toggle(
                "Flag possible local outliers",
                value=True,
                key="applied_show_flags",
                help="Candidates are marked in the plot only; they are not removed automatically.",
            )
        with c2:
            # Never keep a hidden exclusion active. If candidate display is
            # switched off again, later steps revert to the defensive setting.
            if not show_flags:
                st.session_state["applied_exclude_flags"] = False
            st.checkbox(
                "Exclude flagged candidates in later steps",
                value=bool(saved_cfg["exclude_flags"]),
                key="applied_exclude_flags",
                disabled=not show_flags,
                help="Keep this off unless the flagged values are clearly measurement errors.",
            )
        _persist_processing_config()

        _workflow_plot(
            clean_t,
            clean_s,
            outlier_flags=flags,
            show_outliers=show_flags,
            title="Step 1: measured drawdown before optional filtering",
        )

        review = pd.DataFrame({"time_s": clean_t, "drawdown_m": clean_s})
        review["hampel_candidate"] = flags
        if show_flags:
            st.caption("Review the marked candidates against field notes or logger behavior before excluding anything.")
        with st.expander("**Show/hide the measurement table**", expanded=False):
            st.dataframe(review, use_container_width=True, hide_index=True)

        nonpositive_drawdown = int(np.sum(~np.isfinite(clean_s) | (clean_s <= 0)))
        if nonpositive_drawdown:
            st.warning(
                f"{nonpositive_drawdown} cleaned drawdown value(s) are zero or negative. They remain in the table but cannot be displayed on a logarithmic drawdown axis."
            )

# ------------------------------------------------------------
# STEP 2
# ------------------------------------------------------------

if workflow_active[1]:
    with step2:
        st.subheader(":blue[Step 2 — Explore filtering and derivative calculation]")
        st.markdown(
            "The initial settings intentionally apply **no data reduction and no smoothing**, with the simplest logarithmic difference derivative. Increase processing only when the diagnostic signal cannot be interpreted robustly."
        )

        saved_cfg = _processing_config()
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("##### A. Data density")
                use_reduction = st.toggle(
                    "Reduce data in log-time",
                    value=bool(saved_cfg["use_reduction"]),
                    key="applied_use_reduction",
                )
                st.slider(
                    "Points per log-decade",
                    5,
                    50,
                    int(saved_cfg["points_per_decade"]),
                    1,
                    key="applied_points_per_decade",
                    disabled=not use_reduction,
                )
            with col2:
                st.markdown("##### B. Drawdown smoothing")
                smoothing_options = ["None", "Moving average", "Savitzky-Golay (advanced)"]
                saved_smoothing = saved_cfg["smoothing"] if saved_cfg["smoothing"] in smoothing_options else "None"
                smoothing = st.selectbox(
                    "Smoothing method",
                    smoothing_options,
                    index=smoothing_options.index(saved_smoothing),
                    key="applied_smoothing",
                )
                if smoothing == "Moving average":
                    st.slider(
                        "Moving-average order/window",
                        1,
                        31,
                        int(np.clip(saved_cfg["smooth_window"], 1, 31)),
                        2,
                        key="applied_moving_window",
                    )
                elif smoothing == "Savitzky-Golay (advanced)":
                    st.slider(
                        "Savitzky-Golay window",
                        5,
                        31,
                        int(np.clip(saved_cfg["smooth_window"], 5, 31)),
                        2,
                        key="applied_savgol_window",
                    )
            with col3:
                st.markdown("##### C. Derivative")
                derivative_options = list(DERIVATIVE_METHODS)
                saved_derivative = saved_cfg["derivative_label"] if saved_cfg["derivative_label"] in derivative_options else derivative_options[0]
                derivative_label = st.selectbox(
                    "Derivative method",
                    derivative_options,
                    index=derivative_options.index(saved_derivative),
                    key="applied_derivative_label",
                )
                method = DERIVATIVE_METHODS[derivative_label]
                if method in {"bourdet1989", "spane_wurstner1993"}:
                    st.slider(
                        "L-spacing [log₁₀ cycles]",
                        0.05,
                        1.0,
                        float(np.clip(saved_cfg["L"], 0.05, 1.0)),
                        0.05,
                        key="applied_L",
                    )
                elif method == "neighboring_points":
                    st.slider(
                        "Neighbouring points per side",
                        1,
                        12,
                        int(np.clip(saved_cfg["n_neighbors"], 1, 12)),
                        1,
                        key="applied_neighbors",
                    )

        _persist_processing_config()
        processed = _process_data(clean_t, clean_s, flags)
        cfg = processed["config"]
        proc_t = processed["proc_t"]
        proc_s = processed["proc_s"]
        deriv_t = processed["deriv_t"]
        deriv = processed["deriv"]

        st.caption(
            f"Current processing: **{len(clean_t):,}** cleaned measurements → **{len(proc_t):,}** drawdown points. "
            f"Reduction: **{'on' if cfg['use_reduction'] else 'off'}**; smoothing: **{cfg['smoothing']}**; derivative: **{cfg['derivative_label']}**."
        )

        _workflow_plot(
            clean_t,
            clean_s,
            proc_t=proc_t,
            proc_s=proc_s,
            deriv_t=deriv_t,
            deriv=deriv,
            title="Step 2: effect of processing on drawdown and derivative",
        )

        compare = st.toggle(
            "Compare alternative filtering strengths",
            value=False,
            key="applied_compare_filtering",
        )
        if compare:
            st.caption(
                "A hydraulic feature is more convincing when it persists over several reasonable settings rather than appearing only after aggressive smoothing."
            )
            c1, c2 = st.columns(2)
            with c1:
                fig, ax = plt.subplots(figsize=(7.0, 4.8))
                base_t = proc_t
                base_s = processed["proc_s0"]
                for window in [1, 3, 7, 13]:
                    sm = base_s if window == 1 else moving_average(base_s, window)
                    mask = sm > 0
                    ax.loglog(base_t[mask], sm[mask], label=f"moving average {window}")
                ax.set_xlabel("Elapsed time [s]")
                ax.set_ylabel("Drawdown [m]")
                ax.grid(True, which="both", alpha=0.25)
                ax.legend(fontsize=8)
                st.pyplot(fig)
                plt.close(fig)
            with c2:
                fig, ax = plt.subplots(figsize=(7.0, 4.8))
                for label in ["Logarithmic difference", "Bourdet et al. (1989)", "Spane & Wurstner (1993)"]:
                    method0 = DERIVATIVE_METHODS[label]
                    td0, d0 = compute_log_derivative(
                        proc_t,
                        proc_s,
                        method=method0,
                        L=cfg["L"],
                        n_neighbors=cfg["n_neighbors"],
                    )
                    mask = d0 > 0
                    ax.loglog(td0[mask], d0[mask], label=label)
                ax.set_xlabel("Elapsed time [s]")
                ax.set_ylabel(r"Derivative $ds/d\ln(t)$ [m]")
                ax.grid(True, which="both", alpha=0.25)
                ax.legend(fontsize=8)
                st.pyplot(fig)
                plt.close(fig)

# ------------------------------------------------------------
# STEP 3
# ------------------------------------------------------------

if workflow_active[2]:
    with step3:
        st.subheader(":blue[Step 3 — Identify and select the relevant flow period]")
        st.markdown(
            "Use the derivative to identify a possible infinite-radial-flow period. The selected interval is shown both in the plot and in the data table so the chosen observations remain transparent."
        )

        processed = _process_data(clean_t, clean_s, flags)
        proc_t = processed["proc_t"]
        proc_s = processed["proc_s"]
        deriv_t = processed["deriv_t"]
        deriv = processed["deriv"]
        cfg = processed["config"]
        st.caption(_processing_caption(cfg))

        # The plateau search is an aid only. With unfiltered high-frequency data,
        # evaluate a reduced diagnostic copy to keep the active tab responsive.
        detect_mask = np.isfinite(deriv_t) & np.isfinite(deriv) & (deriv_t > 0) & (deriv > 0)
        detect_t = deriv_t[detect_mask]
        detect_d = deriv[detect_mask]
        if len(detect_t) > 260:
            detect_t, detect_d = log_reduce(detect_t, detect_d, points_per_decade=30)
        plateau_auto = detect_plateau(detect_t, detect_d)

        lo_log, hi_log = _positive_log_bounds(proc_t)
        span = hi_log - lo_log
        if plateau_auto:
            suggested = (float(plateau_auto["t_start"]), float(plateau_auto["t_end"]))
            default_log = (np.log10(suggested[0]), np.log10(suggested[1]))
            st.info(
                f"Automatic aid: a candidate plateau was found from about {suggested[0]:.3g} to {suggested[1]:.3g} s. "
                "Treat this only as a starting suggestion and verify it visually."
            )
        else:
            default_log = (lo_log + 0.35 * span, lo_log + 0.60 * span)
            st.warning("No sufficiently stable plateau was found automatically. Select a plausible period manually.")

        p_start, p_end = _log_range_slider(
            "**Selected flow period [log-time control]**",
            proc_t,
            default=default_log,
            key="applied_plateau_range",
        )

        p_mask = (deriv_t >= p_start) & (deriv_t <= p_end) & np.isfinite(deriv) & (deriv > 0)
        if np.sum(p_mask) >= 3:
            plateau_d = float(np.median(deriv[p_mask]))
            plateau_slope = float(np.polyfit(np.log10(deriv_t[p_mask]), np.log10(deriv[p_mask]), 1)[0])
            T_plateau = plateau_transmissivity(Q, plateau_d)
            plateau_selected = {
                "t_start": p_start,
                "t_end": p_end,
                "d_median": plateau_d,
                "slope": plateau_slope,
                "decades": np.log10(p_end / p_start),
            }
            c1, c2, c3 = st.columns(3)
            c1.metric("Median derivative d", f"{plateau_d:.4g} m")
            c2.metric("Log-log slope", f"{plateau_slope:+.3f}")
            c3.metric("T = Q/(4πd)", f"{T_plateau:.3g} m²/s")
            if abs(plateau_slope) > 0.25:
                st.warning("The selected derivative period is not very flat. Treat the plateau transmissivity cautiously.")
        else:
            plateau_selected = None
            T_plateau = None
            st.warning("The selected period contains fewer than three positive derivative values.")

        _workflow_plot(
            clean_t,
            clean_s,
            proc_t=proc_t,
            proc_s=proc_s,
            deriv_t=deriv_t,
            deriv=deriv,
            selected_period=(p_start, p_end),
            title="Step 3: selected flow period within the diagnostic plot",
        )

        data_table = pd.DataFrame({"time_s": proc_t, "drawdown_processed_m": proc_s})
        data_table["in_selected_period"] = (proc_t >= p_start) & (proc_t <= p_end)
        if len(deriv_t) >= 2:
            positive_interp = (deriv_t > 0) & np.isfinite(deriv_t) & np.isfinite(deriv)
            if np.sum(positive_interp) >= 2:
                data_table["derivative_ds_dln_t_m"] = np.interp(
                    np.log(proc_t),
                    np.log(deriv_t[positive_interp]),
                    deriv[positive_interp],
                    left=np.nan,
                    right=np.nan,
                )
            else:
                data_table["derivative_ds_dln_t_m"] = np.nan
        else:
            data_table["derivative_ds_dln_t_m"] = np.nan

        st.markdown("##### Data with the selected period")
        st.dataframe(data_table, use_container_width=True, hide_index=True)

        if plateau_selected:
            st.session_state["applied_plateau_summary"] = {
                **plateau_selected,
                "T": T_plateau,
                "dataset_signature": dataset_signature,
            }
        else:
            st.session_state.pop("applied_plateau_summary", None)

        with st.container(border=True):
            st.markdown("##### Diagnostic hints to test — not automatic conclusions")
            for item in _diagnostic_hints(proc_t, proc_s, deriv_t, deriv, plateau_selected):
                st.markdown(f"- {item}")
            st.caption(
                "Hydrogeology, well construction, pumping history, and mapped boundaries are required to distinguish models that have similar derivative shapes."
            )

# ------------------------------------------------------------
# STEP 4
# ------------------------------------------------------------

if workflow_active[3]:
    with step4:
        st.subheader(":blue[Step 4 — Manually pre-fit, then refine the selected model]")
        st.markdown(
            "Choose the underlying aquifer solution, then add an **outer boundary** if required. For pumping-well data you can additionally activate **wellbore storage**, **well skin**, or both as inner boundaries. First adjust all parameters manually and inspect drawdown and derivative; the automatic fit then starts from exactly these manual values."
        )

        processed = _process_data(clean_t, clean_s, flags)
        proc_t = processed["proc_t"]
        proc_s = processed["proc_s"]
        deriv_t = processed["deriv_t"]
        deriv = processed["deriv"]
        cfg = processed["config"]
        st.caption(_processing_caption(cfg))

        plateau_summary = st.session_state.get("applied_plateau_summary")
        if plateau_summary and plateau_summary.get("dataset_signature") == dataset_signature:
            selected_period = (plateau_summary["t_start"], plateau_summary["t_end"])
            T_hint = float(plateau_summary["T"]) if plateau_summary.get("T") else None
        else:
            selected_period = None
            T_hint = None

        c1, c2, c3 = st.columns(3)
        with c1:
            solution = st.selectbox(
                "**Underlying aquifer solution**",
                SOLUTIONS,
                index=0,
                key="applied_fit_solution",
            )
            st.caption(SOLUTION_EXPLANATIONS[solution])
        with c2:
            boundary = st.selectbox(
                "**Outer boundary**",
                BOUNDARIES,
                index=0,
                key="applied_fit_boundary",
            )
        with c3:
            data_location = st.selectbox(
                "**Measurement location**",
                DATA_LOCATIONS,
                index=0,
                key="applied_data_location",
                help="Wellbore storage and well skin are inner boundaries of the pumping well and should only be activated for pumping-well measurements.",
            )

        if data_location == "Observation well":
            model_r = float(r)
            inner_effects = "None"
            if boundary != "No boundary":
                observation_position = st.selectbox(
                    "**Observation geometry relative to the outer boundary**",
                    OBSERVATION_GEOMETRIES,
                    index=0,
                    key="applied_observation_position",
                    help="The straight outer-boundary distance cannot be inferred from r alone without a geometric assumption.",
                )
            else:
                observation_position = "Between pumping well and boundary"
                st.caption(
                    f"Observation-well analysis uses the supplied distance r = **{model_r:.4g} m**. "
                    "Wellbore storage and skin are not applied to observation-well data."
                )
        else:
            observation_position = "At pumping well"
            with st.container(border=True):
                st.markdown("##### Pumping-well geometry and inner boundaries")
                p1, p2, p3 = st.columns(3)
                with p1:
                    model_r = st.number_input(
                        "Effective screen radius r_w [m]",
                        min_value=0.005,
                        max_value=5.0,
                        value=0.10,
                        step=0.01,
                        format="%.3f",
                        key="applied_pumping_rw",
                        help="For pumping-well evaluation this radius replaces the observation-well distance r.",
                    )
                with p2:
                    storage_on = st.radio(
                        "Wellbore storage",
                        options=["Off", "On"],
                        index=0,
                        horizontal=True,
                        key="applied_inner_storage_on",
                    ) == "On"
                with p3:
                    skin_on = st.radio(
                        "Well skin",
                        options=["Off", "On"],
                        index=0,
                        horizontal=True,
                        key="applied_inner_skin_on",
                    ) == "On"

                if storage_on and skin_on:
                    inner_effects = "Wellbore storage + skin"
                elif storage_on:
                    inner_effects = "Wellbore storage"
                elif skin_on:
                    inner_effects = "Skin"
                else:
                    inner_effects = "None"

                st.caption(
                    f"Active inner boundaries: **{inner_effects}**. "
                    + (
                        "The supplied example datasets were created as observation-well examples; use pumping-well mode for your own pumping-well data or for deliberate sensitivity exploration."
                        if source == "Example dataset"
                        else "The pumping-well radius and selected inner boundaries are used consistently for manual and automatic fitting."
                    )
                )

            if solution == "Neuman delayed yield" and storage_on:
                st.warning(
                    "For Neuman delayed yield, the finite-well storage option uses a bounded confined-elastic composite based on Sₐ for the storage-dominated early phase and transitions to the established Neuman response at later time. "
                    "It is intentionally marked as an approximation rather than a full finite-diameter Neuman solution."
                )

        st.markdown("##### Manual pre-fit parameters")
        manual_params = _manual_parameter_controls(
            solution,
            boundary,
            model_r,
            T_hint,
            observation_position,
            inner_effects=inner_effects,
        )

        if (
            boundary != "No boundary"
            and observation_position == "Between pumping well and boundary"
            and manual_params["D"] <= model_r
        ):
            st.error("For this observation geometry, D must be greater than r.")
            st.stop()

        try:
            manual_s, manual_d = conceptual_model_response(
                solution,
                boundary,
                proc_t,
                Q,
                model_r,
                manual_params,
                observation_position=observation_position,
                inner_effects=inner_effects,
            )
            model_label = f"{solution} + {boundary}"
            if inner_effects != "None":
                model_label += f" + {inner_effects}"
            manual_curve = (
                proc_t,
                manual_s,
                manual_d,
                model_label,
            )
        except Exception as exc:
            manual_curve = None
            st.error(f"The manual model could not be evaluated: {exc}")

        st.markdown("##### Automatic-fit time range")
        fit_start, fit_end = _log_range_slider(
            "Time range used by the automatic drawdown fit",
            proc_t,
            default=_positive_log_bounds(proc_t),
            key="applied_fit_range",
        )
        fit_mask = (
            (proc_t >= fit_start)
            & (proc_t <= fit_end)
            & np.isfinite(proc_s)
            & (proc_s >= 0)
        )
        fit_t = proc_t[fit_mask]
        fit_s = proc_s[fit_mask]

        fit_signature = _data_signature(
            dataset_signature,
            processed["config"],
            solution,
            boundary,
            data_location,
            model_r,
            observation_position,
            inner_effects,
            fit_start,
            fit_end,
            manual_params,
        )

        run_fit = st.button(
            "**Automatic fit from the manual parameters**",
            type="primary",
            disabled=(manual_curve is None or len(fit_t) < 8),
            key="applied_run_primary_fit",
        )
        if run_fit:
            with st.spinner(f"Fitting {solution} with {boundary}..."):
                try:
                    result = fit_conceptual_model(
                        solution,
                        boundary,
                        fit_t,
                        fit_s,
                        Q,
                        model_r,
                        initial=manual_params,
                        T_hint=T_hint,
                        observation_position=observation_position,
                        inner_effects=inner_effects,
                    )
                    st.session_state["applied_primary_fit_bundle"] = {
                        "signature": fit_signature,
                        "result": result,
                    }
                except Exception as exc:
                    st.session_state["applied_primary_fit_bundle"] = {
                        "signature": fit_signature,
                        "error": str(exc),
                    }

        bundle = st.session_state.get("applied_primary_fit_bundle")
        fit_result = None
        if bundle and bundle.get("signature") == fit_signature:
            if "error" in bundle:
                st.error(f"Automatic fit failed: {bundle['error']}")
            else:
                fit_result = bundle.get("result")
        elif bundle:
            st.info("The data, model, fit range, or manual starting parameters changed. Run the automatic fit again to update the result.")

        fitted_curve = None
        if fit_result:
            fitted_s, fitted_d = conceptual_model_response(
                solution,
                boundary,
                proc_t,
                Q,
                model_r,
                fit_result["params"],
                observation_position=observation_position,
                inner_effects=inner_effects,
            )
            fitted_curve = (
                proc_t,
                fitted_s,
                fitted_d,
                model_label,
            )

        _workflow_plot(
            clean_t,
            clean_s,
            proc_t=proc_t,
            proc_s=proc_s,
            deriv_t=deriv_t,
            deriv=deriv,
            selected_period=selected_period,
            fit_period=(fit_start, fit_end),
            manual_curve=manual_curve,
            fitted_curve=fitted_curve,
            title="Step 4: data, manual pre-fit, and automatic model fit",
        )

        if fit_result:
            st.markdown("##### Automatic-fit result")
            pcols = st.columns(min(5, len(fit_result["params"])))
            for i, (name, value) in enumerate(fit_result["params"].items()):
                if name == "T":
                    text = f"{value:.4g} m²/s"
                elif name in {"B", "D", "rc"}:
                    text = f"{value:.4g} m"
                else:
                    text = f"{value:.4g}"
                pcols[i % len(pcols)].metric(name, text)
            st.caption(
                f"RMSE = {fit_result['rmse']:.4g} m; MAE = {fit_result['mae']:.4g} m; AICc = {fit_result['aicc']:.2f}; nonlinear evaluations = {fit_result['nfev']}."
            )
            note = _model_effect_note(
                solution,
                boundary,
                fit_result,
                Q,
                model_r,
                observation_position,
                inner_effects,
            )
            if note:
                st.warning(note)
            if T_hint and "T" in fit_result["params"]:
                rel = 100.0 * (fit_result["params"]["T"] - T_hint) / T_hint
                st.caption(
                    f"Independent Step 3 plateau estimate: T = {T_hint:.3g} m²/s. Automatic model fit: {fit_result['params']['T']:.3g} m²/s ({rel:+.1f}% difference)."
                )

        with st.expander("**Optional: screen alternative solution/boundary combinations**", expanded=False):
            st.markdown(
                "This retains the earlier model-comparison functionality, but it is intentionally secondary to the manual conceptual-model choice. "
                "The selected measurement location and inner-boundary assumption are held fixed while the aquifer solution and outer boundary are screened. Select only hydrogeologically plausible alternatives."
            )
            combo_options = [f"{sol} | {bnd}" for sol in SOLUTIONS for bnd in BOUNDARIES]
            default_compare = [
                "Theis | No boundary",
                "Theis | Specified-head boundary",
                "Hantush-Jacob | No boundary",
            ]
            compare_choices = st.multiselect(
                "Alternative combinations",
                combo_options,
                default=default_compare,
                key="applied_compare_choices",
            )
            compare_signature = _data_signature(
                dataset_signature,
                processed["config"],
                fit_start,
                fit_end,
                compare_choices,
                data_location,
                model_r,
                observation_position,
                inner_effects,
            )
            if st.button(
                "Fit selected alternatives",
                disabled=(not compare_choices or len(fit_t) < 8),
                key="applied_run_compare",
            ):
                results = []
                progress = st.progress(0.0, text="Fitting alternatives...")
                for j, choice in enumerate(compare_choices):
                    sol, bnd = choice.split(" | ", 1)
                    try:
                        result = fit_conceptual_model(
                            sol,
                            bnd,
                            fit_t,
                            fit_s,
                            Q,
                            model_r,
                            T_hint=T_hint,
                            observation_position=observation_position,
                            inner_effects=inner_effects,
                        )
                        results.append(result)
                    except Exception as exc:
                        results.append({"model": choice, "solution": sol, "boundary": bnd, "error": str(exc)})
                    progress.progress((j + 1) / len(compare_choices), text=f"Completed {j + 1}/{len(compare_choices)}")
                progress.empty()
                st.session_state["applied_compare_bundle"] = {
                    "signature": compare_signature,
                    "results": results,
                }

            compare_bundle = st.session_state.get("applied_compare_bundle")
            if compare_bundle and compare_bundle.get("signature") == compare_signature:
                rows = []
                for result in compare_bundle.get("results", []):
                    if "error" in result:
                        rows.append(
                            {
                                "Solution": result["solution"],
                                "Boundary": result["boundary"],
                                "Inner boundaries": inner_effects,
                                "RMSE [m]": np.nan,
                                "MAE [m]": np.nan,
                                "AICc": np.nan,
                                "Parameters": f"FIT FAILED: {result['error']}",
                                "Interpretation check": "",
                            }
                        )
                        continue
                    note = _model_effect_note(
                        result["solution"],
                        result["boundary"],
                        result,
                        Q,
                        model_r,
                        observation_position,
                        inner_effects,
                    )
                    rows.append(
                        {
                            "Solution": result["solution"],
                            "Boundary": result["boundary"],
                            "Inner boundaries": inner_effects,
                            "RMSE [m]": result["rmse"],
                            "MAE [m]": result["mae"],
                            "AICc": result["aicc"],
                            "Parameters": format_parameter_summary(result["params"]),
                            "Interpretation check": note,
                        }
                    )
                comparison = pd.DataFrame(rows)
                if len(comparison) and comparison["AICc"].notna().any():
                    comparison = comparison.sort_values("AICc", na_position="last").reset_index(drop=True)
                    aicc_min = float(comparison["AICc"].min())
                    comparison.insert(
                        comparison.columns.get_loc("AICc") + 1,
                        "ΔAICc",
                        comparison["AICc"] - aicc_min,
                    )
                st.dataframe(comparison, use_container_width=True, hide_index=True)
                st.caption(
                    "Numerical ranking does not resolve conceptual non-uniqueness. Reject alternatives that conflict with stratigraphy, well construction, or known hydraulic boundaries."
                )
                st.download_button(
                    "Download alternative-fit comparison as CSV",
                    data=_to_csv_bytes(comparison),
                    file_name="pumping_test_model_comparison.csv",
                    mime="text/csv",
                )

        st.markdown("##### Export and conclusion")
        export_df = pd.DataFrame({"time_s": proc_t, "drawdown_processed_m": proc_s})
        if len(deriv_t) >= 2:
            valid = np.isfinite(deriv_t) & np.isfinite(deriv) & (deriv_t > 0)
            if np.sum(valid) >= 2:
                export_df["derivative_ds_dln_t_m"] = np.interp(
                    np.log(proc_t),
                    np.log(deriv_t[valid]),
                    deriv[valid],
                    left=np.nan,
                    right=np.nan,
                )
            else:
                export_df["derivative_ds_dln_t_m"] = np.nan
        else:
            export_df["derivative_ds_dln_t_m"] = np.nan
        if selected_period:
            export_df["in_step3_selected_period"] = (
                (proc_t >= selected_period[0]) & (proc_t <= selected_period[1])
            )

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "Download processed data as CSV",
                data=_to_csv_bytes(export_df),
                file_name="pumping_test_processed_derivative.csv",
                mime="text/csv",
            )
        with c2:
            if source == "Example dataset":
                example_bytes = (APPLIED_DATA_DIR / metadata_row["file"]).read_bytes()
                st.download_button(
                    "Download the selected raw example CSV",
                    data=example_bytes,
                    file_name=str(metadata_row["file"]),
                    mime="text/csv",
                )

        st.info(
            "A defensible conclusion should report the processing settings, the selected flow period, the independent plateau-based T where appropriate, the conceptual solution and boundary assumption, the fitted parameters, and any remaining non-uniqueness."
        )

        if source == "Example dataset":
            with st.expander("**Reveal the example's generating model and parameters**", expanded=False):
                st.warning("Use these hidden values only after attempting the interpretation.")
                st.write(f"Expected conceptual model: **{metadata_row['expected_model']}**")
                if truth:
                    st.write(format_parameter_summary(truth))
                if str(metadata_row["source_type"]).startswith("report-inspired"):
                    st.caption(
                        "The parameters reproduce the scale and characteristic timing described in the report, but the CSV values are synthetic teaching data rather than reconstructed original field measurements."
                    )

# ------------------------------------------------------------
# References and footer
# ------------------------------------------------------------

with st.expander("**References and data provenance used for this section**", expanded=False):
    st.markdown(
        """
- Hekel, U., Englert, A., Gaißer, J., Landig, F., Maier, R., Neukum, C. & Leven, C. *Pumpversuchsauswertung mittels Diagnostischer Plots – Ein Leitfaden für Praxis und Lehre* (final draft supplied with this module development).
- Theis, C. V. (1935). The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage.
- Hantush, M. S. & Jacob, C. E. (1955). Non-steady radial flow in an infinite leaky aquifer.
- Neuman, S. P. (1972, 1974, 1975). Delayed-response solutions for unconfined aquifers.
- Bourdet, D., Ayoub, J. A. & Pirard, Y. M. (1989). Use of pressure derivative in well-test interpretation.
- Spane, F. A. & Wurstner, S. K. (1993). DERIV: A computer program for calculating pressure derivatives for use in hydraulic test analysis.

The downloadable examples are deterministic synthetic teaching datasets. The first case is report-inspired and is not presented as the unavailable original Schussental field-data file.
"""
    )

st.markdown("---")
columns_lic = st.columns((4, 1, 1))
with columns_lic[0]:
    st.markdown(
        f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}',
        unsafe_allow_html=True,
    )
with columns_lic[1]:
    st.image(APP_ROOT / "assets" / "images" / "gw_logo_horiz-mini.png")
with columns_lic[2]:
    st.image(APP_ROOT / "assets" / "images" / "CC_BY-SA_icon.png")
st.markdown(
    """
    <div style="font-size:0.85em;">
    <i>
    <a href="https://gw-project.org/" target="_blank">The Groundwater Project</a>
    is a nonprofit organization with one full-time staff and over 1000 volunteers.
    Please help us by referring to
    <a href="https://gw-project.org/interactive-education/" target="_blank">The Groundwater Project Educational Tools</a>
    when sharing this app with others.
    </i>
    </div>
    """,
    unsafe_allow_html=True,
)