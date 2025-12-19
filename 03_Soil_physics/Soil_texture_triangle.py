import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from matplotlib._cm import _Set3_data
from mpltern.datasets import soil_texture_classes
from io import BytesIO


# Authors, institutions, and year
year = 2025 
authors = {
    "Steffen Birk": [1],  # Author 1 belongs to Institution 1
    "Edith Griesser": [1]
}
institutions = {
    1: "Universität Graz, Institut für Erdwissenschaften"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface


# -----------------------------
# Helpers (ported from notebook)
# -----------------------------
def calculate_centroid(vertices: np.ndarray) -> np.ndarray:
    """Calculate the centroid of a polygon."""
    roll0 = np.roll(vertices, 0, axis=0)
    roll1 = np.roll(vertices, 1, axis=0)
    cross = np.cross(roll0, roll1)
    area = 0.5 * np.sum(cross)
    return np.sum((roll0 + roll1) * cross[:, None], axis=0) / (6.0 * area)

def plot_soil_texture_classes(ax):
    """Plot soil texture classes polygons + labels + grid styling."""
    classes = soil_texture_classes
    for (key, value), color in zip(classes.items(), _Set3_data):
        tn0, tn1, tn2 = np.array(value).T
        patch = ax.fill(tn0, tn1, tn2, ec="k", fc=color, alpha=0.6, zorder=2.1)
        centroid = calculate_centroid(patch[0].get_xy())
        label = key[::-1].replace(" ", "\n", 1)[::-1].capitalize()
        ax.text(centroid[0], centroid[1], label, ha="center", va="center", transform=ax.transData)

    ax.taxis.set_major_locator(MultipleLocator(10.0))
    ax.laxis.set_major_locator(MultipleLocator(10.0))
    ax.raxis.set_major_locator(MultipleLocator(10.0))
    ax.taxis.set_minor_locator(AutoMinorLocator(2))
    ax.laxis.set_minor_locator(AutoMinorLocator(2))
    ax.raxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(which="major", linewidth=1)
    ax.grid(which="minor", linewidth=0.4)

    ax.set_tlabel("Clay (%)")
    ax.set_llabel("Sand (%)")
    ax.set_rlabel("Silt (%)")
    ax.taxis.set_ticks_position("tick2")
    ax.laxis.set_ticks_position("tick2")
    ax.raxis.set_ticks_position("tick2")

def random_point_5pct() -> tuple[int, int, int]:
    """Random point with 5%-increments as in notebook."""
    clay = np.random.randint(0, 21) * 5
    sand = np.random.randint(0, (100 - clay) // 5 + 1) * 5
    silt = 100 - clay - sand
    return clay, sand, silt

@st.cache_data(show_spinner=False)
def render_triangle_png(rand_values: tuple[int, int, int]) -> bytes:
    """Render the soil texture triangle + random point to PNG bytes (cached)."""
    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw={"projection": "ternary", "ternary_sum": 100.0},
    )

    plot_soil_texture_classes(ax)

    clay, sand, silt = rand_values
    ax.plot(clay, sand, silt, "ro", zorder=2.5)

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")  # dpi 150 is usually enough
    plt.close(fig)
    return buf.getvalue()

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Soil Texture Classes")

st.title("Soil texture classes")
st.header("Investigate the soil texture triangle", divider='blue')

st.markdown(
    """
This app illustrates how the percentages of **sand**, **silt**, and **clay** determine the **soil texture class**
and how these can be read from a **soil texture triangle** (e.g., FAO 2006).

On the left you see a ternary soil texture diagram. The :red[**red dot**] represents a soil sample.
Your task is to enter the correct percentages of clay, sand, and silt for this sample.
"""
)

# ---- session state init ----
if "rand_values" not in st.session_state:
    st.session_state.rand_values = random_point_5pct()

if "message" not in st.session_state:
    st.session_state.message = "Enter values and check your guess."

if "solved" not in st.session_state:
    st.session_state.solved = False

# ---- layout ----
left, right = st.columns([2,1], gap="large")

with right:
    st.subheader("Your guess", divider="green")

    clay = st.number_input("% Clay", min_value=0, max_value=100, value=0, step=1)
    sand = st.number_input("% Sand", min_value=0, max_value=100, value=0, step=1)
    silt = st.number_input("% Silt", min_value=0, max_value=100, value=0, step=1)

with left:
    st.subheader("Soil texture triangle", divider="orange")
    st.image(render_triangle_png(st.session_state.rand_values), use_container_width=True)

col_check = st.columns((1.5,1,1,))
with col_check[1]:
    check = st.button("Check guess")

if check:
    rv_clay, rv_sand, rv_silt = st.session_state.rand_values

    correct = (clay == rv_clay) and (sand == rv_sand) and (silt == rv_silt)

    if correct:
        st.session_state.solved = True
        st.session_state.message = "Congratulations!"

    else:
        st.session_state.solved = False
        st.session_state.message = (
            f"Your guess for Clay: {clay} % is {'correct' if clay == rv_clay else 'incorrect'}  \n"
            f"Your guess for Sand: {sand} % is {'correct' if sand == rv_sand else 'incorrect'}  \n"
            f"Your guess for Silt: {silt} % is {'correct' if silt == rv_silt else 'incorrect'}  \n"
            ":red[Please try again.]"
        )

st.subheader("Feedback", divider="rainbow")
if st.session_state.solved:
    st.success("Solved! You can restart to try a new point.")
st.write(st.session_state.message)

col_check2 = st.columns((1.5,1,1,))
with col_check2[1]:
    restart = st.button("Restart")

# ---- actions ----
if restart:
    st.session_state.rand_values = random_point_5pct()
    st.session_state.message = "Game restarted! Please enter new values."
    st.session_state.solved = False
    st.rerun()



# ---- references / license ----
with st.expander("Show **References**"):
    st.markdown("""
    - FAO (2006): *Guidelines for soil description*, 4th ed. Food and Agricultural Organization of the United Nations, Rome.
    - Ikeda, Yuji (2024): *yuzie007/mpltern: 1.0.4 (1.0.4)*. Zenodo. https://doi.org/10.5281/zenodo.11068993
    """)

st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')