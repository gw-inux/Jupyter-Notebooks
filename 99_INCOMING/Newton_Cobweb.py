import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(page_title="Newton Iteration – Mehl (2006)", layout="centered")

st.title("Newton Iteration – Convergence Pattern")
st.markdown(
    """
    **Based on:** Mehl, S.W. (2006). *Use of Picard and Newton Iteration for Solving
    Nonlinear Ground Water Flow Equations.* Groundwater, 44(4), 583–594.

    Demonstrates **Newton's method** for solving `f_n(h) = 0`. Each iteration draws a
    **tangent line** at the current point; its x-intercept becomes the next iterate.
    """
)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
TOL           = 0.001
DIVERGE_LIMIT = 1e4
MAX_ITER      = 50

# ─────────────────────────────────────────────
# Residual functions  f_n(h)  and derivatives  f_n'(h)
# ─────────────────────────────────────────────

def fn_mehl(h, hL, hR, KL, KR):
    """
    Mehl (2006) three-node unconfined aquifer residual.
    f_n(h) = KL*hL*h - KL*h^2 - KR*h^2 + KR*hR*h
           = h*(KL*hL + KR*hR) - h^2*(KL + KR)
    Root at h* = (KL*hL + KR*hR) / (KL + KR)
    """
    return KL * hL * h - KL * h**2 - KR * h**2 + KR * hR * h

def dfn_mehl(h, hL, hR, KL, KR):
    """Analytical derivative of fn_mehl."""
    return KL * hL - 2.0 * KL * h - 2.0 * KR * h + KR * hR

def fn_cubic(h, a, b, c, d):
    return a*h**3 + b*h**2 + c*h + d

def dfn_cubic(h, a, b, c, d):
    return 3*a*h**2 + 2*b*h + c

def fn_sine(h):
    return np.sin(3*h) - 0.5*h + 0.3

def dfn_sine(h):
    return 3*np.cos(3*h) - 0.5

def fn_exp(h):
    return np.exp(-2*h) - h + 0.5

def dfn_exp(h):
    return -2*np.exp(-2*h) - 1.0

def fn_quad(h, a, root):
    return a*(h - root)**2 - 0.3

def dfn_quad(h, a, root):
    return 2*a*(h - root)

# ─────────────────────────────────────────────
# Function menu
# ─────────────────────────────────────────────
FUNCTION_OPTIONS = {
    "Mehl (2006) – Three-node unconfined aquifer  (parametric)": "mehl",
    "Cubic polynomial  f_n = a·h³ + b·h² + c·h + d":            "cubic",
    "Sine-based  f_n = sin(3h) − 0.5h + 0.3":                   "sine",
    "Exponential  f_n = e^(−2h) − h + 0.5":                     "exp",
    "Quadratic  f_n = a·(h − root)² − 0.3":                     "quad",
}

# ─────────────────────────────────────────────
# Controls – inline, no sidebar
# ─────────────────────────────────────────────
st.markdown("#### ⚙️ Settings")

col_a, col_b = st.columns(2)
with col_a:
    func_label = st.selectbox(
        "Choose residual function f_n(h)",
        options=list(FUNCTION_OPTIONS.keys()),
        index=0,
    )
func_key = FUNCTION_OPTIONS[func_label]

# ── Parameter panels ────────────────────────────────────────────────
mehl_params  = {"hL": 4.0,  "hR": 0.1,  "KL": 0.005, "KR": 100.0}
cubic_params = {"a":  1.0,  "b": -1.5,  "c":  0.5,   "d":   0.1 }
quad_params  = {"a":  2.0,  "root": 0.75}

if func_key == "mehl":
    with col_b:
        st.markdown("**Aquifer parameters**")
        c1, c2 = st.columns(2)
        with c1:
            mehl_params["hL"] = st.number_input("h_L", value=2.0,  step=0.1, format="%.3f")
            mehl_params["KL"] = st.number_input("K_L", value=0.003, step=0.001, format="%.4f")
        with c2:
            mehl_params["hR"] = st.number_input("h_R", value=0.6,  step=0.1, format="%.3f")
            mehl_params["KR"] = st.number_input("K_R", value=0.8,  step=0.1, format="%.3f")
        # Show analytical root
        h_star_mehl = (mehl_params["KL"]*mehl_params["hL"]
                       + mehl_params["KR"]*mehl_params["hR"]) \
                      / (mehl_params["KL"] + mehl_params["KR"])
        st.info(f"Analytical root: h* = **{h_star_mehl:.4f}**")

elif func_key == "cubic":
    with col_b:
        cubic_params["a"] = st.slider("a (h³)", -3.0, 3.0,  1.0, 0.1)
        cubic_params["b"] = st.slider("b (h²)", -3.0, 3.0, -1.5, 0.1)
        cubic_params["c"] = st.slider("c (h)",  -2.0, 2.0,  0.5, 0.1)
        cubic_params["d"] = st.slider("d",      -1.0, 1.0,  0.1, 0.05)

elif func_key == "quad":
    with col_b:
        quad_params["a"]    = st.slider("a",    0.5, 5.0, 2.0, 0.1)
        quad_params["root"] = st.slider("root", 0.1, 1.8, 0.75, 0.05)

# ── Starting value ───────────────────────────────────────────────────
DEFAULT_H0 = {
    "mehl":  1.70,
    "cubic": 1.50,
    "sine":  1.20,
    "exp":   1.50,
    "quad":  1.40,
}

col_c, _ = st.columns(2)
with col_c:
    h0 = st.slider(
        "Starting value h₀",
        min_value=0.05, max_value=1.95,
        value=DEFAULT_H0.get(func_key, 1.70),
        step=0.05,
    )

st.caption(f"**Fixed settings:** tolerance = {TOL} | max iterations = {MAX_ITER}")

# ─────────────────────────────────────────────
# Active function dispatchers
# ─────────────────────────────────────────────
def get_fn(h):
    h = np.asarray(h, dtype=float)
    if   func_key == "mehl":  return fn_mehl(h, **mehl_params)
    elif func_key == "cubic": return fn_cubic(h, **cubic_params)
    elif func_key == "sine":  return fn_sine(h)
    elif func_key == "exp":   return fn_exp(h)
    elif func_key == "quad":  return fn_quad(h, **quad_params)

def get_dfn(h):
    h = np.asarray(h, dtype=float)
    if   func_key == "mehl":  return dfn_mehl(h, **mehl_params)
    elif func_key == "cubic": return dfn_cubic(h, **cubic_params)
    elif func_key == "sine":  return dfn_sine(h)
    elif func_key == "exp":   return dfn_exp(h)
    elif func_key == "quad":  return dfn_quad(h, **quad_params)

# ─────────────────────────────────────────────
# Session state – reset when settings change
# ─────────────────────────────────────────────
state_key = f"{func_key}_{h0}_{mehl_params}_{cubic_params}_{quad_params}"

if "h_vals" not in st.session_state or st.session_state.get("state_key") != state_key:
    st.session_state.h_vals    = [h0]
    st.session_state.state_key = state_key
    st.session_state.stopped   = False

h_vals  = st.session_state.h_vals
stopped = st.session_state.stopped

# ─────────────────────────────────────────────
# Buttons
# ─────────────────────────────────────────────
btn1, btn2 = st.columns(2)
with btn1:
    next_btn  = st.button("▶ Next Iteration", use_container_width=True)
with btn2:
    reset_btn = st.button("🔄 Reset",          use_container_width=True)

if reset_btn:
    st.session_state.h_vals  = [h0]
    st.session_state.stopped = False
    h_vals  = [h0]
    stopped = False

if next_btn and not stopped:
    h_k = h_vals[-1]
    try:
        fn_k  = float(get_fn(h_k))
        dfn_k = float(get_dfn(h_k))
        if abs(dfn_k) < 1e-12:
            raise ZeroDivisionError("Derivative ≈ 0 – Newton step undefined.")
        h_new = h_k - fn_k / dfn_k          # Newton update
    except Exception as e:
        st.error(f"Newton step failed at h={h_k:.6f}: {e}")
        h_new = np.nan

    if not np.isfinite(h_new) or abs(h_new) > DIVERGE_LIMIT:
        h_new = float(np.clip(
            h_new if np.isfinite(h_new) else DIVERGE_LIMIT,
            -DIVERGE_LIMIT, DIVERGE_LIMIT
        ))
        st.session_state.stopped = True

    st.session_state.h_vals.append(h_new)
    h_vals = st.session_state.h_vals

    if abs(h_new - h_k) < TOL or len(h_vals) - 1 >= MAX_ITER:
        st.session_state.stopped = True
    stopped = st.session_state.stopped

# ─────────────────────────────────────────────
# Status detection
# ─────────────────────────────────────────────
def detect_status(h_vals, tol, diverge_limit):
    n = len(h_vals)
    if n < 2:
        return "start"

    dh     = [h_vals[i] - h_vals[i-1] for i in range(1, n)]
    abs_dh = [abs(d) for d in dh]

    if abs(h_vals[-1]) >= diverge_limit:
        return "diverging"
    if abs_dh[-1] < tol:
        return "converged"
    if n < 5:
        return "iterating"

    window_signed = dh[-min(8, len(dh)):]
    window_abs    = abs_dh[-min(8, len(abs_dh)):]
    signs = [int(np.sign(d)) for d in window_signed if abs(d) > 1e-12]

    is_alternating = (
        len(signs) >= 4
        and all(signs[i] != signs[i+1] for i in range(len(signs)-1))
    )

    def is_shrinking(seq):
        if len(seq) < 2:
            return True
        mid = len(seq) // 2
        first_mean  = sum(seq[:mid])  / max(mid, 1)
        second_mean = sum(seq[mid:])  / max(len(seq)-mid, 1)
        return second_mean < first_mean and seq[-1] < seq[0]

    if is_alternating:
        evens = window_abs[0::2]
        odds  = window_abs[1::2]
        if is_shrinking(evens) and is_shrinking(odds):
            return "converging"
        else:
            return "oscillating"

    if len(signs) >= 4:
        n_flips    = sum(1 for i in range(len(signs)-1) if signs[i] != signs[i+1])
        flip_ratio = n_flips / (len(signs)-1)
        if flip_ratio >= 0.75:
            evens = window_abs[0::2]
            odds  = window_abs[1::2]
            if is_shrinking(evens) and is_shrinking(odds):
                return "converging"
            return "oscillating"

    half = len(window_abs) // 2
    if half >= 1:
        first_mean  = sum(window_abs[:half]) / half
        second_mean = sum(window_abs[half:]) / (len(window_abs)-half)
        return "converging" if second_mean < first_mean else "diverging"

    return "converging" if abs_dh[-1] < abs_dh[-2] else "diverging"

status = detect_status(h_vals, TOL, DIVERGE_LIMIT)

STATUS_STYLE = {
    "start":       dict(color="gray",       symbol="○", label="Waiting"),
    "iterating":   dict(color="steelblue",  symbol="…", label="Iterating"),
    "converging":  dict(color="green",      symbol="↘", label="Converging"),
    "converged":   dict(color="darkgreen",  symbol="✓", label="Converged"),
    "oscillating": dict(color="darkorange", symbol="↔", label="Oscillating"),
    "diverging":   dict(color="crimson",    symbol="↗", label="Diverging"),
}

# ─────────────────────────────────────────────
# Compute plot range – auto-scale to data + curve
# ─────────────────────────────────────────────
h_plot = np.linspace(0.01, 2.0, 800)
try:
    fn_plot = get_fn(h_plot).astype(float)
except Exception:
    fn_plot = np.zeros_like(h_plot)

# Collect all y-values that will appear in the plot
# (curve values + all f_n(h_k) for current iterates)
all_fn_vals = list(fn_plot)
for h in h_vals:
    try:
        all_fn_vals.append(float(get_fn(h)))
    except Exception:
        pass

# Also include tangent line endpoints for y-range
tangent_y_vals = []
for i in range(len(h_vals) - 1):
    h_k = h_vals[i]
    try:
        fn_k  = float(get_fn(h_k))
        tangent_y_vals += [fn_k, 0.0]
    except Exception:
        pass

all_y = [v for v in all_fn_vals + tangent_y_vals if np.isfinite(v)]

if all_y:
    y_min_data = min(all_y)
    y_max_data = max(all_y)
    y_pad      = max(0.15 * (y_max_data - y_min_data), 0.1)
    y_lo       = y_min_data - y_pad
    y_hi       = y_max_data + y_pad
else:
    y_lo, y_hi = -1.5, 1.0

# ─────────────────────────────────────────────
# Build Newton convergence pattern
# For each step k → k+1:
#   • Vertical:  (h_k, 0) → (h_k, f_n(h_k))      [drop to curve]
#   • Tangent:   (h_k, f_n(h_k)) → (h_{k+1}, 0)  [tangent to x-axis]
# ─────────────────────────────────────────────
tangent_segs  = []   # (xs, ys) for tangent lines
vertical_segs = []   # (xs, ys) for vertical drops

for i in range(len(h_vals) - 1):
    h_k  = h_vals[i]
    h_k1 = h_vals[i+1]
    try:
        fn_k = float(get_fn(h_k))
    except Exception:
        break
    # Vertical drop from x-axis to curve at h_k
    vertical_segs.append(([h_k,  h_k ], [0.0,  fn_k]))
    # Tangent from curve point to x-axis intercept
    tangent_segs.append( ([h_k,  h_k1], [fn_k, 0.0 ]))

# ─────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6.5))

# Clip curve for display only (don't clip tangent endpoints)
fn_plot_clipped = np.clip(fn_plot, y_lo - 0.5, y_hi + 0.5)
ax.plot(h_plot, fn_plot_clipped, color="gray", linewidth=2.0, label=r"$f_n(h)$")

# Zero line
ax.axhline(0, color="black", linewidth=1.0)

# Vertical drops
for xs, ys in vertical_segs:
    ax.plot(xs, ys, color="black", linewidth=1.4)

# Tangent lines
for idx, (xs, ys) in enumerate(tangent_segs):
    label = "convergence pattern" if idx == 0 else None
    ax.plot(xs, ys, color="black", linewidth=1.4, label=label)

# Starting point: dot on curve + dashed vertical from x-axis
h_start = h_vals[0]
try:
    fn_start = float(get_fn(h_start))
except Exception:
    fn_start = 0.0

ax.plot([h_start, h_start], [0.0, fn_start],
        "k--", linewidth=0.9, alpha=0.5)
ax.plot(h_start, fn_start, "ko", markersize=7, zorder=6)
ax.annotate(
    f"h₀={h_start:.2f}",
    xy=(h_start, fn_start),
    xytext=(h_start + 0.04, fn_start + 0.02 * (y_hi - y_lo)),
    fontsize=8, color="black"
)

# Current iterate marker (blue circle on curve)
n_iter = len(h_vals) - 1
if n_iter >= 1:
    h_last = h_vals[-1]
    if abs(h_last) < DIVERGE_LIMIT:
        try:
            fn_last = float(get_fn(h_last))
        except Exception:
            fn_last = 0.0
        ax.plot(h_last, fn_last, "bo", markersize=7, zorder=5,
                label=f"Current h={h_last:.4f}")

# Root marker – analytical for Mehl, numerical otherwise
try:
    if func_key == "mehl":
        h_root = (mehl_params["KL"] * mehl_params["hL"]
                  + mehl_params["KR"] * mehl_params["hR"]) \
                 / (mehl_params["KL"] + mehl_params["KR"])
        ax.axvline(h_root, color="red", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.plot(h_root, 0, "r*", markersize=12, zorder=7,
                label=f"Root h*={h_root:.4f}")
    else:
        h_scan  = np.linspace(0.01, 1.99, 5000)
        fn_scan = get_fn(h_scan)
        sc_idx  = np.where(np.diff(np.sign(fn_scan)))[0]
        if len(sc_idx) > 0:
            roots = []
            for sc in sc_idx:
                h_lo, h_hi = h_scan[sc], h_scan[sc+1]
                for _ in range(50):
                    h_mid = (h_lo + h_hi) / 2
                    if get_fn(h_mid) * get_fn(h_lo) < 0:
                        h_hi = h_mid
                    else:
                        h_lo = h_mid
                roots.append((h_lo + h_hi) / 2)
            h_root = min(roots, key=lambda r: abs(r - h0))
            ax.axvline(h_root, color="red", linestyle="--",
                       linewidth=1.0, alpha=0.7)
            ax.plot(h_root, 0, "r*", markersize=12, zorder=7,
                    label=f"Root h*≈{h_root:.4f}")
except Exception:
    pass

# Status text box
sty = STATUS_STYLE.get(status, STATUS_STYLE["start"])
status_text = (
    f"{sty['symbol']} {sty['label']}\n"
    f"k = {n_iter}  |  h = {h_vals[-1]:.4f}"
)
ax.text(
    0.03, 0.97, status_text,
    transform=ax.transAxes,
    fontsize=10, fontweight="bold",
    verticalalignment="top",
    color=sty["color"],
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
              edgecolor=sty["color"], linewidth=1.5, alpha=0.9)
)

ax.set_xlim(0, 2)
ax.set_ylim(y_lo, y_hi)
ax.set_xlabel("h", fontsize=13)
ax.set_ylabel(r"$f_n(h)$", fontsize=13)
ax.set_title("Newton Iteration – Tangent Line Convergence Pattern\n(Mehl, 2006)",
             fontsize=12)
ax.legend(fontsize=9, loc="upper right")
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ─────────────────────────────────────────────
# Status banner
# ─────────────────────────────────────────────
st.markdown("#### 📊 Iteration Status")

if status in ("start", "iterating"):
    st.info(
        f"🔵 **{sty['label']}** – iteration {n_iter}, h = {h_vals[-1]:.6f}."
        + (" Press ▶ to begin." if status == "start" else " Collecting pattern data…")
    )
elif status == "converging":
    st.success(f"🟢 **Converging** – iteration {n_iter}, h = {h_vals[-1]:.6f}. |Δh| consistently **decreasing**.")
elif status == "converged":
    st.success(f"✅ **Converged** after {n_iter} iteration(s)! h* ≈ **{h_vals[-1]:.6f}**  (|Δh| < {TOL})")
elif status == "oscillating":
    st.warning(f"🟡 **Oscillating** – iteration {n_iter}, h = {h_vals[-1]:.6f}. |Δh| alternates without shrinking.")
elif status == "diverging":
    st.error(f"🔴 **Diverging** – iteration {n_iter}, h = {h_vals[-1]:.6f}. |Δh| consistently **increasing**.")

# ─────────────────────────────────────────────
# Iteration history table
# ─────────────────────────────────────────────
st.markdown("#### 📋 Iteration History")

rows = []
for i, h in enumerate(h_vals):
    try:
        fn_val  = f"{float(get_fn(h)):.6f}"
        dfn_val = f"{float(get_dfn(h)):.6f}"
        step    = (f"{-float(get_fn(h))/float(get_dfn(h)):.6f}"
                   if i < len(h_vals)-1 else "—")
    except Exception:
        fn_val = dfn_val = step = "error"
    dh_val = f"{abs(h_vals[i] - h_vals[i-1]):.6f}" if i > 0 else "—"
    rows.append({
        "k":           i,
        "h_k":         f"{h:.6f}",
        "f_n(h_k)":    fn_val,
        "f_n'(h_k)":   dfn_val,
        "Newton step": step,
        "|Δh|":        dh_val,
    })

st.table(rows)
