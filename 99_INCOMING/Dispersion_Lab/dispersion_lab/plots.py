"""Matplotlib views; all numerical results come from model.py.

CODE MAP — refresh with python scripts/update_code_index.py
  L0036  _axes
  L0050  _board_base
  L0098  preview_figure
  L0116  empty_figure
  L0124  board_figure
  L0173  distribution_figure
END CODE MAP
"""
from functools import partial

import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Ellipse
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.ticker import MaxNLocator
import numpy as np

from .i18n import ui_text
from .model import Run, positions, node_id

BLUE = "#256c9b"
ORANGE = "#b56b26"
INK = "#314754"
GRAY = "#c7c7c4"


# 1. Board --------------------------------------------------------------------
HIGHLIGHT = ["#b56b26", "#793f84", "#2c7550", "#a63641", "#555555",
             "#8c6b18", "#62579b", "#257b79", "#a34878", "#504336"]


def _axes(ax, compact=False):
    ax.tick_params(labelsize=10 if compact else 9, colors=INK)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#aeb7bb")
    ax.set_facecolor("#ffffff")
    if compact:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
        ax.xaxis.label.set_fontsize(11)
        ax.yaxis.label.set_fontsize(11)


def _board_base(board, language, show_paths, compact):
    t = partial(ui_text, language=language)
    a, n = board.config.spacing_mm, board.config.rows
    fig = Figure(figsize=(7.0, 4.8 if board.network is not None else 7.6),
                 facecolor="white")
    ax = fig.subplots()
    fig.subplots_adjust(left=.13,right=.97,bottom=.09,top=.94)
    xy = board.xy*1e3
    if board.network is not None:
        # Decorative continuation of the dual lattice, outside the computed domain.
        # Its independent RNG never consumes any medium/particle simulation stream.
        rng=np.random.default_rng([board.config.medium_seed,23])
        actual={(round(x/a,6),round(y/a,6)) for x,y,_ in board.network.grains*1e3}
        circles=[]
        for row in range(n+1):
            for col in range(-n-2,n+3):
                x=(2*col-row+1)*a; y=row*a
                if abs(x)>(n+1)*a or (round(x/a,6),round(y/a,6)) in actual:
                    continue
                radius=a/np.sqrt(2)*board.config.packing*(1-board.config.grain_variation*rng.random())
                circles.append(Circle((x,y),radius))
        circles += [Circle((x*1e3, y*1e3), r*1e3) for x,y,r in board.network.grains]
        ax.add_collection(PatchCollection(circles, facecolor=GRAY,
                                         edgecolor="#969995", linewidth=.4))
    if show_paths:
        ax.add_collection(LineCollection(xy[board.edges], colors="#c5c8ca",
                                         linewidths=.5, alpha=.65, zorder=2))
    if board.network is None:
        nodes=xy[:node_id(n,0)]
        ax.scatter(*nodes.T, s=5, color="#d2d4d5", zorder=3)
        # Symbols are round on the 2:1 display; the route graph itself is unchanged.
        pegs=[Ellipse((x,y+.29*a),.42*a,.21*a) for x,y in nodes]
        ax.add_collection(PatchCollection(pegs,facecolor="#a58c70",edgecolor="#756854",linewidth=.4,zorder=3))
    ax.annotate(t("Injection", de="Zugabe"), xy=(0, 0), xytext=(0, -1.5*a),
                ha="center", color=INK, fontsize=10,
                arrowprops={"arrowstyle":"->", "color":INK, "lw":1})
    ax.scatter(*xy[node_id(n,0):].T, marker="s", s=35, facecolors="white",
               edgecolors=BLUE, linewidths=1, zorder=4)
    ax.set_xlim(-(n+1.9)*a, (n+1.9)*a)
    ax.set_ylim((n+1.2)*a, -(3.7 if n<6 else 3.0)*a)
    # The pinboard is schematic; grain circles must retain their physical shape.
    ax.set_aspect(1 if board.network is not None else 2, adjustable="box")
    ax.set_xlabel(t("Transverse position (mm)", de="Querposition (mm)"))
    ax.set_ylabel(t("Flowwise distance (mm)", de="Strecke in Fließrichtung (mm)"))
    _axes(ax, compact)
    return fig, ax


def preview_figure(board, highlighted=3, language="en", compact=True):
    """Staging tray is schematic: particles have not entered the board."""
    t = partial(ui_text, language=language)
    fig, ax = _board_base(board, language, True, compact)
    ax.set_title(t("Initial board · no transport", de="Ausgangszustand · kein Transport"),
                 loc="left", fontsize=12, color=INK)
    # A wider grain domain needs extra tray clearance at equal x/y scales.
    headroom=max(4.8,.155*board.config.rows) if board.network is not None else 4.8
    ax.set_ylim((board.config.rows+1.2)*board.config.spacing_mm, -headroom*board.config.spacing_mm)
    # A separate tray above the inlet has no spatial-coordinate interpretation.
    for i in range(highlighted):
        x = .5 + (i-(highlighted-1)/2)*.065
        ax.text(x, .975, str(i+1), transform=ax.transAxes, ha="center", va="center",
                color="white", fontsize=8,
                bbox={"boxstyle":"circle,pad=.25", "fc":HIGHLIGHT[i], "ec":"none"})
    return fig


def empty_figure(board, language="en"):
    """Same axes and geometry as playback, without a tray, paths or particles."""
    t=partial(ui_text,language=language)
    fig,ax=_board_base(board,language,True,False)
    ax.set_title(t("Transport board · ready",de="Transportbrett · bereit"),loc="left",fontsize=12,color=INK)
    return fig


def board_figure(run: Run, time: float, language="en", traces=True,
                 show_paths=True, display_limit=None, compact=False,
                 highlighted=1, selected=0) -> Figure:
    """Draw every active background marker and numbered highlighted markers.

    Coincident positions remain coincident; grouped labels identify all particles.
    Collected highlighted markers remain at their outlet. Waiting ones stay hidden.
    display_limit is retained for v1 callers; None displays the entire background.
    """
    t = partial(ui_text, language=language)
    fig, ax = _board_base(run, language, show_paths, compact)
    xy = run.xy*1e3
    highlighted = min(highlighted, run.config.particles)
    sample = np.arange(highlighted, run.config.particles)
    if display_limit is not None and len(sample)>display_limit:
        sample = sample[np.linspace(0,len(sample)-1,display_limit,dtype=int)]
    _, points = positions(run,time,sample)
    if len(points):
        ax.scatter(*(points*1e3).T, s=12, color=BLUE, alpha=.38,
                   edgecolors="none", zorder=5)
    order = [i for i in range(highlighted) if i != selected]+[selected]
    grouped = {}
    for i in order:
        if i >= highlighted or time < run.release[i]:
            continue
        past = np.flatnonzero(run.times[i] <= time)
        line = xy[run.paths[i,past]]
        _, moving = positions(run,time,[i])
        point = moving[0]*1e3 if len(moving) else xy[run.exit_nodes[i]]
        if len(moving):
            line = np.vstack((line,point))
        if traces:
            ax.plot(*line.T, color=HIGHLIGHT[i], lw=2.2 if i==selected else 1.1,
                    alpha=1 if i==selected else .65, zorder=6 if i==selected else 4)
        ax.scatter(*point, s=52 if i==selected else 32,
                   marker="D" if i==selected else "o", color=HIGHLIGHT[i],
                   edgecolors="white", linewidths=.6, zorder=8)
        grouped.setdefault(tuple(point),[]).append(i+1)
    for point, ids in grouped.items():
        label=",".join(map(str,sorted(ids)))
        ax.annotate(label,point,xytext=(-5 if point[0]<0 else 5,6),
                    ha="right" if point[0]<0 else "left",textcoords="offset points",fontsize=8,
                    color=INK,zorder=9,bbox={"fc":"white","ec":"none","alpha":.8,"pad":.4})
    ax.set_title(t("Particle positions", de="Teilchenpositionen")+f" · t = {time:.3g} s",
                 loc="left", fontsize=12, color=INK)
    return fig


# 2. Outlet distributions ------------------------------------------------------
def distribution_figure(run: Run, time: float, language="en", baseline: Run | None=None,
                        bins=25, stacked=False) -> Figure:
    t = partial(ui_text, language=language)
    fig = Figure(figsize=(4.6, 6.8) if stacked else (8.2, 3.5),facecolor="white")
    if stacked:
        fig.subplots_adjust(left=.20,right=.96,bottom=.10,top=.94,hspace=.50)
    else:
        fig.subplots_adjust(left=.13,right=.97,bottom=.19,top=.88,wspace=.50)
    axes = fig.subplots(2, 1) if stacked else fig.subplots(1, 2)
    ax, bt = axes
    n, a = run.config.rows, run.config.spacing_mm
    x = (2*np.arange(n+1)-n)*a
    collected = run.arrival <= time
    counts = np.bincount(run.exit_nodes[collected]-node_id(n, 0), minlength=n+1)
    ax.bar(x, counts/run.config.particles, width=1.45*a, color=BLUE, alpha=.72,
           label=t("Collected so far", de="Bisher gesammelt"))
    ax.plot(x, run.reference["outlet_probability"], "o--", color=INK,
            markersize=4, markerfacecolor="none", lw=1,
            label=t("Exact final reference", de="Exakte Endverteilung"))
    full_outlets = np.bincount(run.exit_nodes-node_id(n, 0), minlength=n+1)/run.config.particles
    spatial_peak = max(full_outlets.max(), run.reference["outlet_probability"].max())
    if baseline is not None:
        bn, ba = baseline.config.rows, baseline.config.spacing_mm
        bx = (2*np.arange(bn+1)-bn)*ba
        hist = np.bincount(baseline.exit_nodes-node_id(bn, 0), minlength=bn+1)
        spatial_peak = max(spatial_peak, hist.max()/baseline.config.particles)
        ax.plot(bx, hist/baseline.config.particles, "s-", color=ORANGE,
                markerfacecolor="none", markersize=3, lw=1,
                label=t("Saved run (complete)", de="Gespeichert (vollständig)"))
    ax.set_xlabel(t("Outlet position (mm)", de="Position am Auslass (mm)"))
    ax.set_ylabel(t("Fraction of injected mass (–)", de="Anteil der Zugabemasse (–)"))
    ax.set_title(t("Where does it arrive?", de="Wo kommt es an?"), loc="left", fontsize=11)
    ax.set_ylim(0, spatial_peak*1.3)
    ax.legend(loc="upper left", fontsize=9 if stacked else 7, frameon=False)
    # Bins and limits depend on the complete experiment, not the animation frame.
    # The ordinate is counts / N / bin width: the complete integral equals one.
    end = max(run.end_time, baseline.end_time if baseline is not None else 0.)
    edges = np.linspace(0, end*1.04, bins+1)
    width = np.diff(edges)
    full = np.histogram(run.arrival, bins=edges)[0]/run.config.particles/width
    arrived = np.histogram(run.arrival[collected], bins=edges)[0]/run.config.particles/width
    bt.bar(edges[:-1], arrived, width=width, align="edge", color=BLUE, alpha=.72,
           label=t("Collected so far", de="Bisher gesammelt"))
    if baseline is not None:
        ref = np.histogram(baseline.arrival, bins=edges)[0]/baseline.config.particles/width
        bt.stairs(ref, edges, color=ORANGE, lw=1.2,
                  label=t("Saved run (complete)", de="Gespeichert (vollständig)"))
        peak = max(full.max(), ref.max())
    else:
        peak = full.max()
    bt.axvline(time, color=INK, ls=":", lw=1)
    bt.set_xlim(0, end*1.04)
    bt.set_ylim(0, peak*1.25 if peak else 1.)
    bt.set_xlabel(t("Time since injection began (s)", de="Zeit seit Beginn der Zugabe (s)"))
    bt.set_ylabel(t("Mass fraction per second (s⁻¹)", de="Massenanteil pro Sekunde (s⁻¹)"))
    bt.set_title(t("When does it arrive?", de="Wann kommt es an?"), loc="left", fontsize=11)
    bt.legend(loc="upper left", fontsize=9 if stacked else 7, frameon=False)
    for axis in axes:
        _axes(axis, stacked)
    return fig
