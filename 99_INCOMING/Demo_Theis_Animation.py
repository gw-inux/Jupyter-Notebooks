from scipy.special import exp1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st

# -------------------------
# Functions
# -------------------------
def theis_drawdown(Q, T, r, S, t):
    # avoid division by zero
    t = np.maximum(t, 1e-30)
    u = (r ** 2) * S / (4.0 * T * t)
    u = np.maximum(u, 1e-30)  # exp1(0) -> inf; keep finite
    wu = exp1(u)
    return (Q / (4.0 * np.pi * T)) * wu

def get_drawdown(wells, t, xg, yg, T, S):
    dd = np.zeros_like(xg, dtype=float)
    for name, xw, yw, rate in wells:
        r = np.sqrt((xg - xw) ** 2 + (yg - yw) ** 2)
        dd += theis_drawdown(rate, T, r, S, t)
    return dd
    
def parse_wells(txt: str):
    wells = []
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        name, xw, yw, rate = line.split()
        wells.append((name, float(xw), float(yw), float(rate)))
    return wells

def animate(i):
    # remove old contour artists safely
    for c in ax.collections[:]:
        c.remove()

    t = float(times[i])
    ax.set_title(f"Time = {t:.2f} days")

    s = get_drawdown(well_list, t, xg, yg, T, S)
    ax.contourf(xg, yg, s, levels=levels)
    return ax.collections  # safest return for FuncAnimation

# -------------------------
# User Interface
# -------------------------
st.set_page_config(page_title="Theis superposition animation")
st.title("Theis drawdown animation (multi-well superposition)")

well_text = """WELL1 49988.2 40903.66 605.0
WELL2 42195.49 5996.99 12.0
WELL3 14583.68 15884.9 716.0
WELL4 34448.56 27964.24 334.0
WELL5 22419.85 31224.71 100.0
WELL6 32417.15 4822.61 439.0
WELL7 16320.24 13385.98 694.0
WELL8 45323.84 36436.13 651.0
WELL9 28248.69 39668.15 558.0
WELL10 11045.92 31436.03 418.0
WELL11 10566.4 8672.29 730.0
WELL12 695.16 33597.84 268.0
WELL13 9036.03 2583.99 312.0
WELL14 44124.26 35123.48 483.0
WELL15 22434.9 35106.7 845.0
WELL16 22566.33 33533.98 506.0
WELL17 2285.95 1383.14 62.0
"""

well_list = parse_wells(well_text)

st.subheader("Parameters")

columns1 = st.columns((1,1,1))

with columns1[0]:
    T = st.number_input("Transmissivity T [ft²/day]", value=1000.0, min_value=1e-6, format="%.6g")
    S = st.number_input("Storativity S [-]", value=1e-4, min_value=1e-12, format="%.6g")
    
with columns1[1]:
    t_min = st.number_input("t min [days]", value=1.0, min_value=1e-6, format="%.6g")
    t_max = st.number_input("t max [days]", value=99.0, min_value=1e-6, format="%.6g")
    n_frames = st.slider("Frames", 10, 200, 99)
    interval_ms = st.slider("Frame interval [ms]", 20, 500, 100)

with columns1[2]:
    xmin = st.number_input("xmin", value=-50000.0, format="%.6g")
    xmax = st.number_input("xmax", value=100000.0, format="%.6g")
    ymin = st.number_input("ymin", value=-50000.0, format="%.6g")
    ymax = st.number_input("ymax", value=100000.0, format="%.6g")
    nxy = st.slider("Grid resolution (n x n)", 50, 400, 200)

# Build grid
x = np.linspace(xmin, xmax, int(nxy))
y = np.linspace(ymin, ymax, int(nxy))
xg, yg = np.meshgrid(x, y)

# Time vector
times = np.linspace(t_min, t_max, int(n_frames))

# Compute a robust level range once (based on last frame)
# This avoids "levels too small" issues and keeps the color scale stable.
s_last = get_drawdown(well_list, times[-1], xg, yg, T, S)
s_max = float(np.nanmax(s_last))
# avoid degenerate levels
s_max = max(s_max, 1e-12)
levels = np.linspace(0.0, s_max, 25)

# -------------------------
# Matplotlib animation -> HTML for Streamlit
# -------------------------
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, aspect="equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
title = ax.set_title("Time = -")

# initial frame
ax.contourf(xg, yg, np.zeros_like(xg), levels=levels)

anim = animation.FuncAnimation(fig, animate, frames=len(times), interval=interval_ms, blit=False)

html = anim.to_jshtml()

plt.close(fig)

# Render in Streamlit
st.components.v1.html(html, height=700, scrolling=False)

with st.expander("Show wells table"):
    st.code(well_text)
