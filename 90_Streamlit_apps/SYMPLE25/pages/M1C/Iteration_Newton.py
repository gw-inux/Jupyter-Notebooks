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
# Deactive in multipage apps
# st.set_page_config(page_title="Newton Iteration – Mehl (2006)", layout="centered")

st.title("Convergence Pattern")
st.header(":blue[Newton Iteration] Scheme", divider="blue")
st.markdown(
    """
    This interactive application  demonstrates the Newton-Raphson iteration scheme (Newton solver). The :blue[line] in the plot below represents the model $f_n(h)$. Each iteration draws a **tangent line** at the current point and the resulting x-intercept becomes the head for the next iteration step. The scheme aims to find the point, where the model becomes zero, i.e., $f_n(h) = 0$.
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

def f_mehl(h, hL, hR, KL, KR):
    """
    Mehl (2006) three-node unconfined aquifer residual.
    f_n(h) = KL*hL*h - KL*h^2 - KR*h^2 + KR*hR*h
           = h*(KL*hL + KR*hR) - h^2*(KL + KR)
    Root at h* = (KL*hL + KR*hR) / (KL + KR)
    """
    return KL * hL * h - KL * h**2 - KR * h**2 + KR * hR * h

def df_mehl(h, hL, hR, KL, KR):
    """Analytical derivative of f_mehl."""
    return KL * hL - 2.0 * KL * h - 2.0 * KR * h + KR * hR

def f_cubic(h, a, b, c, d):
    return a*h**3 + b*h**2 + c*h + d

def df_cubic(h, a, b, c, d):
    return 3*a*h**2 + 2*b*h + c

def f_sine(h):
    return np.sin(3*h) - 0.5*h + 0.3

def df_sine(h):
    return 3*np.cos(3*h) - 0.5

def f_exp(h):
    return np.exp(-2*h) - h + 0.5

def df_exp(h):
    return -2*np.exp(-2*h) - 1.0

def f_quad(h, a, root):
    return a*(h - root)**2 - 0.3

def df_quad(h, a, root):
    return 2*a*(h - root)

# ─────────────────────────────────────────────
# Function menu
# ─────────────────────────────────────────────
FUNCTION_OPTIONS = {
    "MODEL 1 (Mehl 2006)": "mehl",
    "MODEL 2 (Poly)":      "cubic",
    "MODEL 3 (SIN)":       "sine",
    "MODEL 4 (EXP)":       "exp",
    "MODEL 5 (QUAD)":      "quad",
}

# ─────────────────────────────────────────────
# Controls – inline, no sidebar
# ─────────────────────────────────────────────
st.subheader("Choose :blue[Example Model] and  :orange[Initial head]", divider = 'blue')

col_a, col_b = st.columns(2)
with col_a:
    func_label = st.selectbox(
        "Choose :green[example model]",
        options=list(FUNCTION_OPTIONS.keys()),
        index=0,
    )
func_key = FUNCTION_OPTIONS[func_label]

# ── Parameter panels ────────────────────────────────────────────────
mehl_params  = {"hL": 4.0,  "hR": 0.1,  "KL": 0.005, "KR": 100.0}
cubic_params = {"a":  1.0,  "b": -1.5,  "c":  0.5,   "d":   0.1 }
quad_params  = {"a":  2.0,  "root": 0.75}

if func_key == "mehl":
    mehl_params["hL"] = 2.0
    mehl_params["KL"] = 0.002
    mehl_params["hR"] = 0.8
    mehl_params["KR"] = 0.9
    
    # Show analytical root
    h_star_mehl = (mehl_params["KL"]*mehl_params["hL"]
                   + mehl_params["KR"]*mehl_params["hR"]) \
                  / (mehl_params["KL"] + mehl_params["KR"])
#   st.info(f"Analytical root: h* = **{h_star_mehl:.4f}**")

elif func_key == "cubic":
    cubic_params["a"] = 0.7
    cubic_params["b"] = -1.2
    cubic_params["c"] = 0.3
    cubic_params["d"] = -0.45

elif func_key == "quad":
    quad_params["a"]    = st.slider("a",    0.5, 5.0, 2.0, 0.1)
    quad_params["root"] = st.slider("root", 0.1, 1.8, 0.75, 0.05)

# ── Starting value ───────────────────────────────────────────────────
DEFAULT_H0 = {
    "mehl":  1.70,
    "cubic": 1.50,
    "sine":  1.42,
    "exp":   1.50,
    "quad":  1.40,
}

with col_b:
    h0 = st.slider(
        ":blue[Initial head $h_0$]",
        min_value=0.05, max_value=1.95,
        value=DEFAULT_H0.get(func_key, 1.70),
        step=0.05,
    )

# ─────────────────────────────────────────────
# Active function dispatchers
# ─────────────────────────────────────────────
def get_fn(h):
    h = np.asarray(h, dtype=float)
    if   func_key == "mehl":  return f_mehl(h, **mehl_params)
    elif func_key == "cubic": return f_cubic(h, **cubic_params)
    elif func_key == "sine":  return f_sine(h)
    elif func_key == "exp":   return f_exp(h)
    elif func_key == "quad":  return f_quad(h, **quad_params)

def get_dfn(h):
    h = np.asarray(h, dtype=float)
    if   func_key == "mehl":  return df_mehl(h, **mehl_params)
    elif func_key == "cubic": return df_cubic(h, **cubic_params)
    elif func_key == "sine":  return df_sine(h)
    elif func_key == "exp":   return df_exp(h)
    elif func_key == "quad":  return df_quad(h, **quad_params)

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

st.subheader("Interactive plot", divider = 'blue')


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
    h_k = h_vals[-1]
    try:
        f_k  = float(get_fn(h_k))
        df_k = float(get_dfn(h_k))
        if abs(df_k) < 1e-12:
            raise ZeroDivisionError("Derivative ≈ 0 – Newton step undefined.")
        h_new = h_k - f_k / df_k          # Newton update
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
    f_plot = get_fn(h_plot).astype(float)
except Exception:
    f_plot = np.zeros_like(h_plot)

# Collect all y-values that will appear in the plot (curve values + all f_n(h_k) for current iterates)
all_f_vals = list(f_plot)
for h in h_vals:
    try:
        all_f_vals.append(float(get_fn(h)))
    except Exception:
        pass

# Also include tangent line endpoints for y-range
tangent_y_vals = []
for i in range(len(h_vals) - 1):
    h_k = h_vals[i]
    try:
        f_k  = float(get_fn(h_k))
        tangent_y_vals += [f_k, 0.0]
    except Exception:
        pass

all_y = [v for v in all_f_vals + tangent_y_vals if np.isfinite(v)]

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
        f_k = float(get_fn(h_k))
    except Exception:
        break
    # Vertical drop from x-axis to curve at h_k
    vertical_segs.append(([h_k,  h_k ], [0.0,  f_k]))
    # Tangent from curve point to x-axis intercept
    tangent_segs.append( ([h_k,  h_k1], [f_k, 0.0 ]))


# ─────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 7))

# Clip curve for display only (don't clip tangent endpoints)
f_plot_clipped = np.clip(f_plot, y_lo - 0.5, y_hi + 0.5)
ax.plot(h_plot, f_plot_clipped, color="dodgerblue", linewidth=1.5, label=r"$f_n(h)$")

# Zero line
ax.axhline(0, color="lime", linewidth=1.0)

# Vertical drops
for xs, ys in vertical_segs:
    ax.plot(xs, ys, "k--", color="black", linewidth=1.0)

# Tangent lines
for idx, (xs, ys) in enumerate(tangent_segs):
    label = "convergence pattern" if idx == 0 else None
    ax.plot(xs, ys, color="magenta", linewidth=1.0, label=label)

# Starting point: dot on curve + dashed vertical from x-axis
h_start = h_vals[0]
try:
    f_start = float(get_fn(h_start))
except Exception:
    f_start = 0.0

ax.plot([h_start, h_start], [f_start, -1.5], "k--", color = "dodgerblue", linewidth=1.0, alpha=0.5)
ax.plot(h_start, f_start, "ko", markersize=8, zorder=6)
ax.annotate(
    f"$h_0$ = {h_start:.2f}",
    xy=(h_start, f_start),
    xytext=(h_start + 0.04, f_start + 0.02 * (y_hi - y_lo)),
    fontsize=12, color="black"
)

# Current iterate marker
n_iter = len(h_vals) - 1
if n_iter >= 1:
    h_last = h_vals[-1]
    if abs(h_last) < DIVERGE_LIMIT:
        try:
            f_last = float(get_fn(h_last))
        except Exception:
            f_last = 0.0
        ax.plot(h_last, f_last, "ro", markersize=6, zorder=5,
                label=f"current $h$ = {h_last:.4f}")

# Root marker – analytical for Mehl, numerical otherwise
#try:
#    if func_key == "mehl":
#        h_root = (mehl_params["KL"] * mehl_params["hL"]
#                  + mehl_params["KR"] * mehl_params["hR"]) \
#                 / (mehl_params["KL"] + mehl_params["KR"])
#        ax.axvline(h_root, color="red", linestyle="--", linewidth=1.0, alpha=0.7)
#        ax.plot(h_root, 0, "r*", markersize=12, zorder=7,
#                label=f"Root h*={h_root:.4f}")
#    else:
#        h_scan  = np.linspace(0.01, 1.99, 5000)
#        f_scan = get_fn(h_scan)
#        sc_idx  = np.where(np.diff(np.sign(f_scan)))[0]
#        if len(sc_idx) > 0:
#            roots = []
#            for sc in sc_idx:
#                h_lo, h_hi = h_scan[sc], h_scan[sc+1]
#                for _ in range(50):
#                    h_mid = (h_lo + h_hi) / 2
#                    if get_fn(h_mid) * get_fn(h_lo) < 0:
#                        h_hi = h_mid
#                    else:
#                        h_lo = h_mid
#                roots.append((h_lo + h_hi) / 2)
#            h_root = min(roots, key=lambda r: abs(r - h0))
#            ax.axvline(h_root, color="red", linestyle="--",
#                       linewidth=1.0, alpha=0.7)
#            ax.plot(h_root, 0, "r*", markersize=12, zorder=7,
#                    label=f"Root h*≈{h_root:.4f}")
#except Exception:
#    pass

# Status text box
sty = STATUS_STYLE.get(status, STATUS_STYLE["start"])
status_text = (
    f"{sty['symbol']} {sty['label']}\n"
    f"k = {n_iter}  |  h = {h_vals[-1]:.4f}"
)
ax.text(
    0.03, 0.97, status_text,
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment="top",
    color=sty["color"],
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
              edgecolor=sty["color"], linewidth=1.5)
)

ax.set_xlim(0, 2)
ax.set_ylim(-1.5, 1)
ax.set_xlabel("h", fontsize=12)
ax.set_ylabel(r"$f_n(h)$", fontsize=12)
ax.set_title("Convergence Pattern - Newton Iteration",
             fontsize=14)
ax.legend(fontsize=12, loc="upper right")
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
        f_val  = f"{float(get_fn(h)):.6f}"
        df_val = f"{float(get_dfn(h)):.6f}"
        step    = (f"{-float(get_fn(h))/float(get_dfn(h)):.6f}"
                   if i < len(h_vals)-1 else "—")
    except Exception:
        f_val = df_val = step = "error"
    dh_val = f"{abs(h_vals[i] - h_vals[i-1]):.6f}" if i > 0 else "—"
    rows.append({
        "k":           i,
        "h_k":         f"{h:.6f}",
        "f_n(h_k)":    f_val,
        "f_n'(h_k)":   df_val,
        "Newton step": step,
        "|Δh|":        dh_val,
    })

st.table(rows)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')