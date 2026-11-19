"""Matplotlib cross-section. Plot symbols use the same SI notation in all languages.

Contents
1. Colours and numerical labels
2. Cross-section and observation-well casings

The app renders translated cell names and readouts as browser text aligned
with the cell centres. Browser text supports Chinese, Devanagari and Arabic
shaping without additional plotting fonts or language-specific dependencies.
"""
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse, Rectangle

from hydraulics import (BASE, DX, LEFT, RIGHT, ROOF, WATER_TABLE_BASE,
                        WATER_TABLE_TOP, budget)

# 1. Colours and numerical labels
MUTED = "#526775"
BLUE = "#205984"
TEAL = "#126B60"
WARM = "#995324"
LINE = "#A8B9C1"


def number(value, *, signed=False, digits=4):
    """Compact readout that preserves small, nonzero values."""
    if value == 0:
        return "0"
    return format(value, f"{'+' if signed else ''}.{digits}g").replace("-", "−")


def delta_label(change):
    if change and abs(change) < 0.0001:
        return number(change, signed=True)
    return (f"{change:+.4f}" if change else "0.0000").replace("-", "−")


# 2. Cross-section and observation-well casings
def cross_section(head, conductivity, unconfined, history=None, *, narrow=False):
    """Readout HTML matches the desktop and phone plot margins."""
    fig = Figure(figsize=(4.5, 2.75) if narrow else (8.1, 2.9), facecolor="white")
    ax = fig.subplots()
    fig.subplots_adjust(left=.105 if narrow else .085, right=.99, bottom=.04, top=.96)
    bottom = WATER_TABLE_BASE if unconfined else BASE
    top = WATER_TABLE_TOP if unconfined else ROOF
    ax.set(xlim=(-DX/2, 2.5*DX), ylim=(bottom-.12, 5.55 if unconfined else 4.95))
    ax.set_ylabel("z (m)", color=MUTED, fontsize=10, labelpad=3)
    ax.set_yticks([0, 1, 2, 3, 4, 5] if unconfined else [-2, 0, 1, 2, 3, 4])
    ax.tick_params(axis="y", colors=MUTED, labelsize=9, length=0)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#EBF0F2", linewidth=.7)
    for i, level in enumerate((LEFT, head, RIGHT)):
        x, edge = i*DX, (i-.5)*DX
        color = TEAL if i == 1 else BLUE
        water = "#B8DFD7" if i == 1 else "#B9D5E6"
        ax.add_patch(Rectangle((edge, bottom), DX, top-bottom,
                               facecolor="#F8F3E9" if unconfined else water,
                               edgecolor=LINE, linewidth=1))
        if unconfined:
            ax.add_patch(Rectangle((edge+.5, bottom), DX-1, level-bottom,
                                   facecolor=water, edgecolor="none"))
        else:
            # Casing extends into the aquifer. Slots indicate the screened
            # interval. The elliptical rim makes the open standpipe visible.
            tube_bottom, rim = bottom+.3, 4.5
            ax.add_patch(Rectangle((x-4, tube_bottom), 8, rim-tube_bottom,
                                   facecolor="white", edgecolor=MUTED, linewidth=1, zorder=3))
            ax.add_patch(Rectangle((x-3, tube_bottom), 6, level-tube_bottom,
                                   facecolor=water, edgecolor="none", zorder=3))
            for screen in (-1.45, -1.15, -.85, -.55):
                ax.plot([x-4.5, x-2.8], [screen]*2, color=MUTED, lw=.8, zorder=4)
                ax.plot([x+2.8, x+4.5], [screen]*2, color=MUTED, lw=.8, zorder=4)
            ax.add_patch(Ellipse((x, rim), 8, .17, facecolor="white", edgecolor=MUTED,
                                 linewidth=1, zorder=4))
        if i == 1 and history is not None and len(history) > 1:
            ax.plot([x-32, x+32], [history[-2]]*2, "--", lw=1.3,
                    color="#677985", zorder=4)
        half_mark = 43 if unconfined else 14
        ax.plot([x-half_mark, x+half_mark], [level]*2, color=color, lw=2, zorder=5)
        ax.plot(x, level, "o", ms=5, color=color, zorder=6)
        label = f"{level:.6f} m" if i == 1 else f"{level:.0f} m"
        ax.annotate(label, (x, level), xytext=(0, 7), textcoords="offset points",
                    ha="center", color=color, weight="bold", fontsize=9 if narrow else 10,
                    bbox=dict(boxstyle="round,pad=.14", fc="white", ec="none", alpha=.94),
                    zorder=7)
    ax.axhline(bottom, color="#7F7662", lw=2)
    ax.axhline(top, color=MUTED, lw=1.3)
    # These mathematical labels apply to both aquifer geometries.
    ax.text(2.47*DX, top+.13, rf"$z_t={top:g}$ m", ha="right", va="bottom",
            fontsize=8, color=MUTED, bbox=dict(fc="white", ec="none", pad=.4), zorder=8)
    ax.text(2.47*DX, bottom+.12, rf"$z_b={bottom:g}$ m", ha="right", va="bottom",
            fontsize=8, color=MUTED, bbox=dict(fc="white", ec="none", pad=.4), zorder=8)
    if history is None:
        qin, qout, _, _ = budget(head, conductivity, unconfined)
        arrow_y = bottom + (0.33 if unconfined else 0.48) * (RIGHT-bottom if unconfined else ROOF-bottom)
        for face, flow in zip((DX/2, 1.5*DX), (qin, qout)):
            if flow > 0:
                half_length = 19 * flow / max(qin, qout)
                ax.annotate("", (face+half_length, arrow_y), (face-half_length, arrow_y),
                            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2,
                                            shrinkA=0, shrinkB=0, mutation_scale=11), zorder=6)
    return fig
