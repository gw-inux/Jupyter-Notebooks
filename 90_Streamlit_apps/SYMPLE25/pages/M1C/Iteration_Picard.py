import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(page_title="Picard Iteration – Mehl (2006)", layout="centered")

st.title("Convergence Pattern")
st.header(":green[Picard Iteration] Scheme (Cobweb-Plot)", divider="green")

st.markdown(
    """
    Demonstrates the **Picard (successive substitution) iteration** for solving
    $h = f_p(h)$. The solution is where the curve, representing the model, intersects the diagonal $h$ = $h$.
    """
)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
TOL           = 0.001
DIVERGE_LIMIT = 1e4
MAX_ITER      = 50

# ─────────────────────────────────────────────
# Function definitions
# ─────────────────────────────────────────────

# --- Original Mehl default ---

def fp_mehl_default(h):
    """Mehl (2006) default: C/h^0.7  – monotone converging staircase"""
    alpha  = 0.70
    h_star = 0.55
    c      = h_star ** (1 + alpha)
    return c / (np.maximum(h, 1e-9) ** alpha)

def fp_mehl_slow(h):
    """Slow converging: C/h^0.3"""
    alpha  = 0.30
    h_star = 0.75
    c      = h_star ** (1 + alpha)
    return c / (np.maximum(h, 1e-9) ** alpha)

# --- Figure 1: piecewise with jump, converging staircase from right ---
# Curve rises steeply for small h, drops, then rises again as sqrt-like
# Approximation: two-piece function with a discontinuity near h=0.25
def fp_fig1(h):
    """
    Mehl Fig.1: piecewise function with a jump discontinuity.
    For h < 0.25 : steep rise  (mimics the left spike)
    For h >= 0.25: sqrt-like   (mimics the right gradual rise)
    Fixed point near h ≈ 1.0
    """
    h = np.atleast_1d(np.asarray(h, dtype=float))
    result = np.where(
        h < 0.25,
        1.3 / (np.maximum(h, 1e-9) ** 0.5),          # steep left branch
        0.55 * np.sqrt(np.maximum(h - 0.1, 1e-9)) + 0.35  # right branch
    )
    return np.clip(result, 0, 2.0)

# --- Figure 2: step function – diverging staircase ---
# Piecewise constant: high plateau for small h, low plateau for large h
# Starting value h_s ≈ 1.2 shown in figure, with label d
def fp_fig2(h):
    """
    Mehl Fig.2: step/piecewise-constant function.
    f_p(h) = 1.5  for h < 0.8
    f_p(h) = 1.0  for 0.8 <= h < 1.2
    f_p(h) = 0.5  for h >= 1.2
    Starting point h_s ≈ 1.2 (marked with arrow in figure).
    The iterate cycles: 1.2 → 0.5 → 1.5 → 0.5 → 1.5 → ...
    No stable fixed point → diverging/oscillating iteration.
    """
    h = np.atleast_1d(np.asarray(h, dtype=float))
    result = np.where(
        h < 0.8,  1.5,
        np.where(
            h < 1.2,  1.0,
                      0.5   # h >= 1.2
        )
    )
    return result.astype(float)

# --- Figure 3: decreasing hyperbola – oscillating inward spiral ---
# f_p(h) = K/h  with fixed point at h* = sqrt(K)
# Slope at fixed point = -K/h*^2 = -1  → borderline; use K slightly < h*^2
# Use K = 0.25 → h* = 0.5, slope = -1 exactly → use K=0.22 for |slope|<1
def fp_fig3(h):
    """
    Mehl Fig.3: f_p(h) = K/h  – oscillating convergence (inward rectangular spiral).
    Fixed point h* = sqrt(K). With K=0.25, h*=0.5, slope=-1 (borderline).
    Use K=0.22 so |slope|<1 and spiral converges.
    Points A(small h, ~0), B(small h, high fp), C(large h, high fp), D(large h, low fp).
    """
    K = 0.22
    return K / np.maximum(h, 1e-9)

# --- Figure 4: piecewise with a notch/dip – slow staircase from left ---
# Curve is mostly above diagonal but has a dip below near h≈0.5
# Then rises again; fixed point near h≈1.75
def fp_fig4(h):
    """
    Mehl Fig.4: piecewise with a dip/notch near h=0.5.
    Left of dip: rises steeply (spike near h=0.2)
    Dip region: drops below diagonal
    Right of dip: gradual sqrt-like rise toward fixed point ~1.75
    """
    h = np.atleast_1d(np.asarray(h, dtype=float))
    result = np.where(
        h < 0.20,
        1.5 / (np.maximum(h, 1e-9) ** 0.4),
        np.where(
            h < 0.55,
            -1.8 * (h - 0.20) + 0.75,               # descending dip
            0.60 * np.sqrt(np.maximum(h - 0.3, 1e-9)) + 0.25  # gradual rise
        )
    )
    return np.clip(result, 0, 2.0)

# --- Oscillating convergence (negative slope |s|<1) ---
def fp_oscillating(h):
    return -0.85 * (h - 0.55) + 0.55

# --- Oscillating divergence (negative slope |s|>1) ---
def fp_oscillating_div(h):
    return -1.4 * (h - 0.55) + 0.55

# --- Random linear ---
def fp_random_linear(h, slope, intercept):
    return slope * h + intercept

# --- Random nonlinear ---
def fp_random_nonlinear(h, a, b, c_coef):
    return a * np.sqrt(np.maximum(h, 1e-9)) + b * h + c_coef

# ─────────────────────────────────────────────
# Function menu
# ─────────────────────────────────────────────
FUNCTION_OPTIONS = {
    "MODEL 1 (Mehl 2006, default)":      "mehl_default",
    "MODEL 2 (Piecewise jump)":     "fig1",
    "MODEL 3 (Step function)":      "fig2",
    "MODEL 4 (Hyperbola)":          "fig3",
    "MODEL 5 (Piecewise notch)":    "fig4",
    "MODEL 6 (Slow)":               "mehl_slow",
    "MODEL 7 (conver)":             "oscillating",
    "MODEL 8 (diver)":              "oscillating_div",
    "MODEL 9 (Own para linear)":    "random_linear",
    "MODEL 10 (Own para nonlinear)":"random_nonlinear",
}

# ─────────────────────────────────────────────
# Controls – inline
# ─────────────────────────────────────────────
st.subheader("Choose :green[Example Model] and  :orange[Initial head]", divider = 'green')

col_a, col_b, col_c = st.columns(3)
with col_a:
    func_label = st.selectbox(
        "Choose iteration function f_p(h)",
        options=list(FUNCTION_OPTIONS.keys()),
        index=0,
    )
func_key = FUNCTION_OPTIONS[func_label]

rand_params = {}
if func_key == "random_linear":
    with col_b:
        rand_params["slope"]     = st.slider("Slope",     -2.0, 2.0,  0.6,  0.05)
        rand_params["intercept"] = st.slider("Intercept", -1.0, 1.5,  0.2,  0.05)
elif func_key == "random_nonlinear":
    with col_b:
        rand_params["a"]      = st.slider("Coeff a (√h)",   0.0, 1.5, 0.5, 0.05)
        rand_params["b"]      = st.slider("Coeff b (linear)",-1.0,1.0, 0.1, 0.05)
        rand_params["c_coef"] = st.slider("Constant c",      0.0, 1.0, 0.1, 0.05)

# Default starting values per figure (matching the paper)
DEFAULT_H0 = {
    "fig1":          0.75,
    "fig2":          1.20,
    "fig3":          1.30,
    "fig4":          0.20,
    "mehl_default":  1.25,
    "mehl_slow":     1.25,
    "oscillating":   1.25,
    "oscillating_div": 1.25,
    "random_linear": 1.25,
    "random_nonlinear": 1.25,
}

with col_c:
    h0 = st.slider(
        "Starting value h₀",
        min_value=0.05, max_value=1.90,
        value=DEFAULT_H0.get(func_key, 1.25),
        step=0.05,
        help="Initial guess placed on the x-axis."
    )

# ─────────────────────────────────────────────
# Active function dispatcher
# ─────────────────────────────────────────────
def get_fp(h):
    h = np.asarray(h, dtype=float)
    if   func_key == "fig1":             return fp_fig1(h)
    elif func_key == "fig2":             return fp_fig2(h)
    elif func_key == "fig3":             return fp_fig3(h)
    elif func_key == "fig4":             return fp_fig4(h)
    elif func_key == "mehl_default":     return fp_mehl_default(h)
    elif func_key == "mehl_slow":        return fp_mehl_slow(h)
    elif func_key == "oscillating":      return fp_oscillating(h)
    elif func_key == "oscillating_div":  return fp_oscillating_div(h)
    elif func_key == "random_linear":
        return fp_random_linear(h, rand_params["slope"], rand_params["intercept"])
    elif func_key == "random_nonlinear":
        return fp_random_nonlinear(h, rand_params["a"], rand_params["b"], rand_params["c_coef"])

# ─────────────────────────────────────────────
# Session state – reset when settings change
# ─────────────────────────────────────────────
reset_trigger = (
    st.session_state.get("h0_prev")      != h0
    or st.session_state.get("func_prev") != func_key
    or st.session_state.get("rp_prev")   != str(rand_params)
)

if "h_vals" not in st.session_state or reset_trigger:
    st.session_state.h_vals    = [h0]
    st.session_state.h0_prev   = h0
    st.session_state.func_prev = func_key
    st.session_state.rp_prev   = str(rand_params)
    st.session_state.stopped   = False

h_vals  = st.session_state.h_vals
stopped = st.session_state.stopped

st.subheader("Interactive plot", divider = 'green')

# ─────────────────────────────────────────────
# Buttons
# ─────────────────────────────────────────────
btn1, btn2 = st.columns(2)
with btn1:
    next_btn  = st.button("▶ Proceed/Iterate", use_container_width=True)
with btn2:
    reset_btn = st.button("🔄 Reset",          use_container_width=True)

if reset_btn:
    st.session_state.h_vals  = [h0]
    st.session_state.stopped = False
    h_vals  = [h0]
    stopped = False

if next_btn and not stopped:
    h_current = h_vals[-1]
    try:
        h_new = float(np.atleast_1d(get_fp(h_current))[0])
    except Exception:
        h_new = np.nan

    if not np.isfinite(h_new) or abs(h_new) > DIVERGE_LIMIT:
        h_new = float(np.clip(h_new if np.isfinite(h_new) else DIVERGE_LIMIT,
                               -DIVERGE_LIMIT, DIVERGE_LIMIT))
        st.session_state.stopped = True

    st.session_state.h_vals.append(h_new)
    h_vals = st.session_state.h_vals

    if abs(h_new - h_current) < TOL or len(h_vals) - 1 >= MAX_ITER:
        st.session_state.stopped = True
    stopped = st.session_state.stopped

def detect_status(h_vals, tol, diverge_limit):
    """
    Status detection logic:

    CONVERGED   : |Δh| < tol
    DIVERGING   : |h| exceeds diverge_limit  OR  |Δh| is growing
    OSCILLATING : signs of Δh alternate AND the amplitude (|Δh|) is NOT
                  shrinking — i.e., comparing every-other step (same sign)
                  the values stay roughly constant or grow
    CONVERGING  : |Δh| is shrinking — regardless of whether signs alternate
                  (covers both monotone convergence and oscillatory convergence)
    ITERATING   : fewer than 4 steps, too early to classify
    """
    n = len(h_vals)

    # ── Not enough data ──────────────────────────────────────────────
    if n < 2:
        return "start"

    dh      = [h_vals[i] - h_vals[i-1] for i in range(1, n)]   # signed
    abs_dh  = [abs(d) for d in dh]                              # unsigned

    # ── Hard divergence ──────────────────────────────────────────────
    if abs(h_vals[-1]) >= diverge_limit:
        return "diverging"

    # ── Converged ────────────────────────────────────────────────────
    if abs_dh[-1] < tol:
        return "converged"

    # ── Need at least 4 steps for reliable pattern detection ─────────
    if n < 5:
        return "iterating"

    # Use last min(8, len) values for the window
    window_signed = dh[-min(8, len(dh)):]
    window_abs    = abs_dh[-min(8, len(abs_dh)):]

    # ── Check if signs alternate (geometric oscillation present) ─────
    signs = [int(np.sign(d)) for d in window_signed if abs(d) > 1e-12]
    is_alternating = (
        len(signs) >= 4
        and all(signs[i] != signs[i + 1] for i in range(len(signs) - 1))
    )

    if is_alternating:
        # ── Separate into two interleaved subsequences by sign ───────
        # Even-indexed steps (e.g. all negative jumps)
        # Odd-indexed  steps (e.g. all positive jumps)
        # If BOTH subsequences are shrinking → converging (oscillatory)
        # If either subsequence is flat/growing → true oscillation
        evens = window_abs[0::2]   # every other value starting at 0
        odds  = window_abs[1::2]   # every other value starting at 1

        def is_shrinking(seq):
            """True if the sequence has a clear downward trend."""
            if len(seq) < 2:
                return True   # can't tell, assume shrinking
            # Compare mean of first half vs second half
            mid = len(seq) // 2
            first_mean  = sum(seq[:mid])       / max(mid, 1)
            second_mean = sum(seq[mid:])       / max(len(seq) - mid, 1)
            # Also check last vs first value
            overall_drop = seq[-1] < seq[0]
            return second_mean < first_mean and overall_drop

        evens_shrink = is_shrinking(evens)
        odds_shrink  = is_shrinking(odds)

        if evens_shrink and odds_shrink:
            # Amplitude is shrinking on both sides → converging
            return "converging"
        else:
            # Amplitude is stable or growing → true oscillation
            return "oscillating"

    # ── Non-alternating: converging vs diverging ──────────────────────
    # Compare mean |Δh| of first half vs second half of window
    half = len(window_abs) // 2
    if half >= 1:
        first_mean  = sum(window_abs[:half]) / half
        second_mean = sum(window_abs[half:]) / (len(window_abs) - half)
        if second_mean < first_mean:
            return "converging"
        else:
            return "diverging"

    # ── Fallback ──────────────────────────────────────────────────────
    return "converging" if abs_dh[-1] < abs_dh[-2] else "diverging"



status = detect_status(h_vals, TOL, DIVERGE_LIMIT)

# ─────────────────────────────────────────────
# Status display config
# ─────────────────────────────────────────────
STATUS_STYLE = {
    "start":       dict(color="gray",        symbol="○", label="Waiting"),
    "iterating":   dict(color="steelblue",   symbol="…", label="Iterating"),
    "converging":  dict(color="green",       symbol="↘", label="Converging"),
    "converged":   dict(color="darkgreen",   symbol="✓", label="Converged"),
    "oscillating": dict(color="darkorange",  symbol="↔", label="Oscillating"),
    "diverging":   dict(color="crimson",     symbol="↗", label="Diverging"),
}

# ─────────────────────────────────────────────
# Build cobweb path
# ─────────────────────────────────────────────
cobweb_x, cobweb_y = [], []

if len(h_vals) >= 1:
    h_start = h_vals[0]
    try:
        fp0 = float(np.atleast_1d(get_fp(h_start))[0])
    except Exception:
        fp0 = 0.0

    cobweb_x += [h_start, h_start]
    cobweb_y += [0.0,     fp0    ]

    if len(h_vals) >= 2:
        cobweb_x += [h_vals[1], h_vals[1]]
        cobweb_y += [fp0,       h_vals[1]]

    for i in range(1, len(h_vals) - 1):
        h_cur  = h_vals[i]
        h_next = h_vals[i + 1]
        try:
            fp_cur = float(np.atleast_1d(get_fp(h_cur))[0])
        except Exception:
            break
        cobweb_x += [h_cur,  h_cur ]
        cobweb_y += [h_cur,  fp_cur]
        cobweb_x += [h_next, h_next]
        cobweb_y += [fp_cur, h_next]

# ─────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 7))

h_plot = np.linspace(0.02, 2.0, 500)
try:
    fp_plot = np.clip(
        np.atleast_1d(get_fp(h_plot)).astype(float),
        -0.5, 3.0
    )
except Exception:
    fp_plot = np.zeros_like(h_plot)

# Curve = 'MODEL'
ax.plot(h_plot, fp_plot, color="blue", linewidth=1.8, label=r"$h=f_p(h)$")

# Diagonal
ax.plot([0, 2], [0, 2], "k--", linewidth=1.2, label=r"$h=h$  (diagonal)")

# Cobweb path
if len(cobweb_x) > 2:
    ax.plot(cobweb_x, cobweb_y, "k-", linewidth=1.0, color = "darkviolet", label="convergence pattern")

# Starting point on x-axis
#ax.plot(h_vals[0], 0, "ko", markersize=7, zorder=6)
ax.annotate(
    f"h₀ ={h_vals[0]:.2f}",
    xy=(h_vals[0], 0),
    xytext=(h_vals[0] + 0.04, 0.07),
    fontsize=8, color="black"
)

# Current head marker
if len(h_vals) > 1:
    h_last = h_vals[-1]
    if abs(h_last) < DIVERGE_LIMIT:
        ax.plot(h_last, h_last, "bo", markersize=5, zorder=5,
                label=f"Current h={h_last:.4f}")
else:
    h_plot = h_vals[0]
    ax.plot(h_plot, 0, "bs", markersize=7, zorder=5, label=f"Starting h={h_plot:.4f}")
    
        

# Known fixed points
FIXED_POINTS = {
    "mehl_default":    0.55,
    "mehl_slow":       0.75,
    "oscillating":     0.55,
    "oscillating_div": 0.55,
    "fig3":            (0.22 ** 0.5),   # sqrt(K)
}
if func_key in FIXED_POINTS:
    fp_fix = FIXED_POINTS[func_key]
    ax.plot(fp_fix, fp_fix, "r*", markersize=0, zorder=7,
            label=f"Solution: h ≈ {fp_fix:.3f}")

# ── Status text in plot ──────────────────────
sty   = STATUS_STYLE.get(status, STATUS_STYLE["start"])
n_iter = len(h_vals) - 1
status_text = (
    f"{sty['symbol']} {sty['label']}\n"
    f"k = {n_iter}  |  h = {h_vals[-1]:.4f}"
)
ax.text(
    0.03, 0.97, status_text,
    transform=ax.transAxes,
    fontsize=12, fontweight="bold",
    verticalalignment="top",
    color=sty["color"],
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
              edgecolor=sty["color"], linewidth=1.5, alpha=0.9)
)

ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_xlabel("h", fontsize=12)
ax.set_ylabel(r"$f_p(h)$", fontsize=12)
ax.set_title("Convergence Pattern - Picard Iteration", fontsize=14)
ax.legend(fontsize=12, loc="upper right")

st.pyplot(fig)

# ─────────────────────────────────────────────
# Status banner below plot
# ─────────────────────────────────────────────
st.markdown("#### 📊 Iteration Status")

if status in ("start", "iterating"):
    st.info(
        f"🔵 **{sty['label']}** – iteration {n_iter}, h = {h_vals[-1]:.6f}."
        + (" Press ▶ to begin." if status == "start" else " Collecting pattern data…")
    )
elif status == "converging":
    st.success(f"🟢 **Converging** – iteration {n_iter}, h = {h_vals[-1]:.6f}. |Δh| is consistently **decreasing**.")
elif status == "converged":
    st.success(f"✅ **Converged** after {n_iter} iteration(s)! h* ≈ **{h_vals[-1]:.6f}**  (|Δh| < {TOL})")
elif status == "oscillating":
    st.warning(f"🟡 **Oscillating** – iteration {n_iter}, h = {h_vals[-1]:.6f}. |Δh| **alternates** up/down around the fixed point.")
elif status == "diverging":
    st.error(f"🔴 **Diverging** – iteration {n_iter}, h = {h_vals[-1]:.6f}. |Δh| is consistently **increasing**.")

# ─────────────────────────────────────────────
# Iteration history table
# ─────────────────────────────────────────────
st.markdown("#### 📋 Iteration History")

rows = []
for i, h in enumerate(h_vals):
    try:
        fp_val = f"{float(np.atleast_1d(get_fp(h))[0]):.6f}" if i < len(h_vals)-1 else "—"
    except Exception:
        fp_val = "error"
    dh_val = f"{abs(h_vals[i] - h_vals[i-1]):.6f}" if i > 0 else "—"
    rows.append({"k": i, "h_k": f"{h:.6f}", "f_p(h_k)": fp_val, "|Δh|": dh_val})

st.table(rows)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')