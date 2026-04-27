import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("Picard Iteration: Interactive Cobweb Plot")

st.markdown("""
This app demonstrates the fixed-point Picard iteration

$$
h_{i+1} = f_p(h_i)
$$

The solution is reached when

$$
h = f_p(h)
$$

Each click on **Next iteration** performs one Picard step.
""")

# ------------------------------------------------------------
# Fixed-point functions
# ------------------------------------------------------------
def mehl_like_function(h):
    """
    Current illustrative function.
    Fixed point near h = 0.547.
    """
    a = 811537 / 7795000
    b = 2400894320517 / 7595253125000
    c = 162459 / 974375
    return a + b / (h + c)


def weakly_convergent_function(h):
    """
    Smooth convergent function.
    """
    return 0.45 + 0.35 * np.exp(-2.0 * h)


def oscillating_function(h):
    """
    Function that may lead to oscillating convergence.
    """
    return 1.1 - 0.8 * h


def divergent_function(h):
    """
    Function that tends to diverge for many starting values.
    """
    return 0.2 + 1.25 * h


def random_convergent_function(h):
    """
    Example of a nonlinear random-looking but stable function.
    """
    return 0.55 + 0.25 * np.sin(3.0 * h) * np.exp(-0.7 * h)


def random_unstable_function(h):
    """
    Example of a nonlinear function that may diverge or oscillate.
    """
    return 0.4 + 1.15 * np.sin(1.8 * h)


functions = {
    "Mehl-like function, fixed point near h = 0.547": mehl_like_function,
    "Weakly convergent function": weakly_convergent_function,
    "Oscillating function": oscillating_function,
    "Divergent function": divergent_function,
    "Random convergent nonlinear function": random_convergent_function,
    "Random unstable nonlinear function": random_unstable_function,
}

# ------------------------------------------------------------
# Controls, no sidebar
# ------------------------------------------------------------
st.subheader("Settings")

col1, col2, col3 = st.columns(3)

with col1:
    selected_function = st.selectbox(
        "Choose fixed-point function",
        list(functions.keys())
    )

with col2:
    h0 = st.slider(
        "Starting value h₀",
        min_value=0.0,
        max_value=2.0,
        value=0.1,
        step=0.01
    )

with col3:
    max_iter = st.slider(
        "Maximum number of iterations",
        min_value=1,
        max_value=50,
        value=20
    )

tol = st.number_input(
    "Convergence tolerance",
    min_value=1e-8,
    max_value=1e-1,
    value=1e-4,
    format="%.1e"
)

fp = functions[selected_function]

# ------------------------------------------------------------
# Reset if settings change
# ------------------------------------------------------------
settings = (selected_function, h0)

if "settings" not in st.session_state:
    st.session_state.settings = settings

if "h_values" not in st.session_state:
    st.session_state.h_values = [h0]

if settings != st.session_state.settings:
    st.session_state.settings = settings
    st.session_state.h_values = [h0]

# ------------------------------------------------------------
# Buttons
# ------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Next iteration"):
        if len(st.session_state.h_values) <= max_iter:
            h_old = st.session_state.h_values[-1]
            h_new = fp(h_old)
            st.session_state.h_values.append(float(h_new))

with col2:
    if st.button("Run to maximum iterations"):
        while len(st.session_state.h_values) <= max_iter:
            h_old = st.session_state.h_values[-1]
            h_new = fp(h_old)
            st.session_state.h_values.append(float(h_new))

            if abs(h_new - h_old) < tol:
                break

with col3:
    if st.button("Reset"):
        st.session_state.h_values = [h0]

# ------------------------------------------------------------
# Diagnose iteration status
# ------------------------------------------------------------
def diagnose_status(values, tol=1e-4):
    if len(values) < 3:
        return "not enough iterations yet"

    diffs = np.abs(np.diff(values))

    if diffs[-1] < tol:
        return "converging"

    if len(diffs) >= 4:
        recent = diffs[-4:]

        if recent[-1] < recent[0]:
            return "converging"

        if recent[-1] > recent[0]:
            return "diverging"

    if len(values) >= 5:
        signs = np.sign(np.diff(values[-5:]))
        sign_changes = np.sum(signs[1:] != signs[:-1])

        if sign_changes >= 3:
            return "oscillating"

    return "unclear"

status = diagnose_status(st.session_state.h_values, tol)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------
h_plot = np.linspace(0, 2, 500)
fp_plot = fp(h_plot)

fig, ax = plt.subplots(figsize=(7, 6))

ax.plot(h_plot, fp_plot, color="gray", lw=2.5, label=r"$h=f_p(h)$")
ax.plot(h_plot, h_plot, color="black", linestyle=":", lw=2.5, label=r"$h=h$")

h_vals = st.session_state.h_values

# First vertical line starts at the x-axis
if len(h_vals) > 1:
    h_start = h_vals[0]
    h_next = h_vals[1]

    ax.plot(
        [h_start, h_start],
        [0, h_next],
        color="black",
        lw=1.5
    )

    ax.plot(
        [h_start, h_next],
        [h_next, h_next],
        color="black",
        lw=1.5
    )

# Remaining cobweb lines
for i in range(1, len(h_vals) - 1):
    h_old = h_vals[i]
    h_new = h_vals[i + 1]

    ax.plot(
        [h_old, h_old],
        [h_old, h_new],
        color="black",
        lw=1.5
    )

    ax.plot(
        [h_old, h_new],
        [h_new, h_new],
        color="black",
        lw=1.5
    )

# Starting point on x-axis
ax.scatter(h_vals[0], 0, color="black", zorder=5)
ax.text(h_vals[0], 0.04, r"$h_0$", ha="center")

# Current point on identity line
ax.scatter(h_vals[-1], h_vals[-1], color="black", zorder=5)

ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_xlabel("h")
ax.set_ylabel(r"$f_p(h)$")
ax.set_title("Cobweb plot of Picard iteration")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ------------------------------------------------------------
# Status below plot
# ------------------------------------------------------------
if status == "converging":
    st.success("Status: converging")
elif status == "diverging":
    st.error("Status: diverging")
elif status == "oscillating":
    st.warning("Status: oscillating")
else:
    st.info(f"Status: {status}")

# ------------------------------------------------------------
# Iteration table
# ------------------------------------------------------------
st.subheader("Iteration history")

table = []

for i, value in enumerate(h_vals):
    if i == 0:
        table.append({
            "iteration": i,
            "h": value,
            "|hᵢ - hᵢ₋₁|": np.nan
        })
    else:
        table.append({
            "iteration": i,
            "h": value,
            "|hᵢ - hᵢ₋₁|": abs(h_vals[i] - h_vals[i - 1])
        })

df = pd.DataFrame(table)
st.dataframe(df, hide_index=True)

# ------------------------------------------------------------
# Short interpretation
# ------------------------------------------------------------
st.markdown("""
### Interpretation

- A vertical line represents the computation of the next Picard value  
  $h_{i+1} = f_p(h_i)$.
- A horizontal line transfers this value back to the identity line  
  $h = h$.
- Repeated steps show whether the iteration approaches a fixed point,
  moves away from it, or oscillates.
""")