# streamlit run this_file.py
import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np

st.set_page_config(page_title="FD Stencil", layout="centered")
st.title("Finite-Difference Stencil (3D cells)")

# ---------- Sidebar controls ----------
st.sidebar.header("Display options")
center_color  = st.sidebar.color_picker("Center edge color", "#1f77b4")
neighbor_color= st.sidebar.color_picker("Neighbor edge color", "#BFC7D5")
diag_on       = st.sidebar.checkbox("Show center diagonals (dashed)", True)
lw_center     = st.sidebar.slider("Center edge width", 1.5, 5.0, 2.8, 0.1)
lw_neigh      = st.sidebar.slider("Neighbor edge width", 0.6, 3.0, 1.4, 0.1)
gap           = st.sidebar.slider("Gap between cells", 0.0, 0.2, 0.05, 0.01)
elev          = st.sidebar.slider("Elevation", 0, 60, 22, 1)
azim          = st.sidebar.slider("Azimuth", -180, 180, -55, 1)

# NEW: labeling controls
st.sidebar.header("Labels")
show_labels   = st.sidebar.checkbox("Show labels", True)
fs            = st.sidebar.slider("Font size", 8, 24, 11, 1)
show_axes_lbl = st.sidebar.checkbox("Show axis denotation (i, j, k)", True)

# ---------- Helpers ----------
def box_edges(x0, y0, z0, dx=1, dy=1, dz=1):
    x1, y1, z1 = x0+dx, y0+dy, z0+dz
    v = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    return [
        (v[0],v[1]),(v[1],v[2]),(v[2],v[3]),(v[3],v[0]),  # bottom
        (v[4],v[5]),(v[5],v[6]),(v[6],v[7]),(v[7],v[4]),  # top
        (v[0],v[4]),(v[1],v[5]),(v[2],v[6]),(v[3],v[7])   # verticals
    ]

def add_box(ax, origin, size=(1,1,1), color="#9aa4b2", lw=1.4, alpha=1.0, zorder=1):
    segs = box_edges(*origin, *size)
    ax.add_collection3d(Line3DCollection(segs, colors=color, linewidths=lw, alpha=alpha, zorder=zorder))

# ---------- Figure ----------
fig = plt.figure(figsize=(7.0, 6.0))
ax = fig.add_subplot(111, projection='3d')

L = 1.0
step = L + gap

# origins
O   = np.array([0,0,0])
OxP = O + np.array([ step,0,0])   # (i+1,j,k)
OxM = O + np.array([-step,0,0])   # (i-1,j,k)
OyP = O + np.array([0, step,0])   # (i,j+1,k)
OyM = O + np.array([0,-step,0])   # (i,j-1,k)
OzP = O + np.array([0,0, step])   # (i,j,k+1)
OzM = O + np.array([0,0,-step])   # (i,j,k-1)

# neighbors
for org in [OxP, OxM, OyP, OyM, OzP, OzM]:
    add_box(ax, org, size=(L,L,L), color=neighbor_color, lw=lw_neigh)

# center
add_box(ax, O, size=(L,L,L), color=center_color, lw=lw_center)

# optional diagonals
if diag_on:
    x0,y0,z0 = O
    x1,y1,z1 = x0+L, y0+L, z0+L
    diag = [
        [(x0,y0,z0),(x1,y1,z1)],
        [(x0,y0,z1),(x1,y1,z0)],
        [(x0,y1,z0),(x1,y0,z1)],
        [(x1,y0,z0),(x0,y1,z1)]
    ]
    ax.add_collection3d(Line3DCollection(diag, colors="#777", linewidths=1.2, linestyles="dashed", alpha=0.8))

# ---------- Labels (edge denotation) ----------
if show_labels:
    # Center-cell label on an edge (top-front edge midpoint)
    ax.text(L*0.5, L, L+0.03, r"$i,j,k$", ha="center", va="bottom", fontsize=fs)

    # Place neighbor labels on the *shared-face* edges relative to center:
    # +i and -i faces (midpoints of those vertical edges)
    ax.text(L+gap/2, L*0.5, L+0.03, r"$i{+}1,j,k$", ha="center", va="bottom", fontsize=fs)  # +i side (right)
    ax.text(-gap/2,  L*0.5, L+0.03, r"$i{-}1,j,k$", ha="center", va="bottom", fontsize=fs)  # -i side (left)

    # +j and -j faces
    ax.text(L*0.5, L+gap/2, L+0.03, r"$i,j{+}1,k$", ha="center", va="bottom", fontsize=fs)  # +j side (back)
    ax.text(L*0.5, -gap/2,  L+0.03, r"$i,j{-}1,k$", ha="center", va="bottom", fontsize=fs)  # -j side (front)

    # +k and -k faces (top & bottom centers)
    ax.text(L*0.5, L*0.5, L+gap/2+L+0.03, r"$i,j,k{+}1$", ha="center", va="bottom", fontsize=fs)  # above top face
    ax.text(L*0.5, L*0.5, -gap/2,          r"$i,j,k{-}1$", ha="center", va="top",    fontsize=fs)

# Axis denotation (i, j, k) along scene axes
if show_axes_lbl:
    # Simple arrows are tricky in mplot3d; use text anchors near axes ends instead
    pad = step + L
    ax.text(pad+0.2, 0, 0, r"$i$", fontsize=fs+1)
    ax.text(0, pad+0.2, 0, r"$j$", fontsize=fs+1)
    ax.text(0, 0, pad+0.2, r"$k$", fontsize=fs+1)

# ---------- View & tidy ----------
ax.view_init(elev=elev, azim=azim)
ax.set_box_aspect((1,1,1))
pad = step + L
ax.set_xlim(-pad, pad+L)
ax.set_ylim(-pad, pad+L)
ax.set_zlim(-pad, pad+L)

# Remove ticks, panes, spines
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.set_ticks([])
ax.set_xlabel(""); ax.set_ylabel(""); ax.set_zlabel("")
ax.grid(False)
ax.xaxis.pane.set_visible(False)
ax.yaxis.pane.set_visible(False)
ax.zaxis.pane.set_visible(False)
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
st.pyplot(fig)
