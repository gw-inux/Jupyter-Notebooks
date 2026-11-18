"""Scientific figures — never modify numerical states.

TABLE OF CONTENTS — search for the numbered section comments below.
  1. Shared colors, fixed view limits and zoom
  2. Three-cell flow arrows and geometry preview
  3. Cell-head marks, latest accepted method and model cross-section
  4. Scalar functions, reduced Newton balance and coupled step constructions
  5. Global convergence measures and selected-cell head history

Maintenance: shared styles and axis limits are below. Visible prose comes from
assets/md/ui.md. The numerical history is read-only, including when zooming.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import numpy as np
from .model import scalar_values, cell_slice, HEAD_TOL, FLOW_TOL
from .ui import load_ui
from .diagnostics import coupled_step, step_values, detail_tails

COLORS = {"Picard": "#27824a", "Newton": "#245caa"}
ORANGE = "#d17317"
BOUNDARY_WATER = "#9EC8DE"
BOUNDARY_HEAD = "#205389"
CELL_TEXT = "#405360"
CONVERGENCE_YLIM = (1e-12, 100.0)  # Shared log window; never changes with iterations.
QUANTITY_COLORS = {"flow": "#80549b", "change": "#986419"}
MEHL_HEAD_RANGE = (0.0, 2.0)  # Shared by the theory figures and section-2 presets.
MANUAL_ZOOM_WIDTHS = (1.0, 0.1, 0.01, 0.001, 1e-4, 1e-5)  # Full widths, in m.
MIN_AUTO_ZOOM_WIDTH = 0.001  # Automatic zoom is independent of manual stages.
plt.rcParams.update(
    {
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "figure.facecolor": "white",
    }
)


# 1. Shared styles and fixed views
def axes(size=(7.6, 3.5)):
    return plt.subplots(figsize=size, layout="constrained")


def method_style(method, active=False):
    """A larger open circle or dashed square marks a method just advanced."""
    return dict(
        color=COLORS[method],
        marker="o" if method == "Picard" else "s",
        markersize=(8 if method == "Picard" else 4) + (2 if active else 0),
        markerfacecolor="none" if method == "Picard" else COLORS[method],
        markeredgewidth=1.3 if method == "Picard" else 0.7,
        linestyle="-" if method == "Picard" else "--",
        linewidth=(1.4 if method == "Picard" else 1.1) + (1.1 if active else 0),
    )


def geometry_limits(model, start, final, cell=1, head_range=None):
    """Fixed diagnostic limits: independent of the initial and current estimates.

    For a system, only the independently solved neighboring heads define the
    scalar slice. ``start`` is retained for call compatibility, but is not used.
    """
    if head_range is None:
        head_range = (
            (0.0, 8.0)
            if model.n == 3
            else (0.0, float(max(model.top or 20.0, np.ceil(max(final) * 1.1))))
        )
    low, high = head_range
    local = model if model.n == 3 else cell_slice(model, final, cell)
    wetlow = max(low, local.bottom + 1e-7) if local.unconfined else low
    xs = np.linspace(wetlow, high, 240)
    extent = max(max(abs(scalar_values(local, x)[1]) for x in xs) * 1.12, 1e-16)
    return {"head": tuple(head_range), "residual": (-extent, extent)}


def auto_zoom_width(root, current, previous_width=None):
    """Hold the span until the head enters the inner 25% or leaves the window.

    On resizing, |current - root| is 2/3 of the half-width, except at the
    0.001 m minimum. The centre may move with a coupled Picard crossing;
    the remembered width is independent of that movement and of tolerances.
    """
    distance = abs(float(current) - float(root))
    if previous_width is not None:
        radius = previous_width / 2
        if 0.25 * radius <= distance <= radius:
            return previous_width
    return max(MIN_AUTO_ZOOM_WIDTH, 3.0 * distance)


def manual_zoom_width(current_width, closer):
    """Next permitted manual width from the currently displayed window."""
    if closer:
        return next(
            (w for w in MANUAL_ZOOM_WIDTHS if w < current_width * (1 - 1e-9)),
            MANUAL_ZOOM_WIDTHS[-1],
        )
    return next(
        (w for w in reversed(MANUAL_ZOOM_WIDTHS) if w > current_width * (1 + 1e-9)),
        MANUAL_ZOOM_WIDTHS[0],
    )


def zoom_limits(model, root, current, *, previous_width=None, width=None):
    """Centre a scalar view on its crossing; never clamp it to the full view.

    ``model`` is the local three-cell model used for scalar flow-axis limits.
    Coupled Newton figures fit their own reduced residual inside this window.
    An explicit width selects manual zoom; otherwise apply auto hysteresis.
    """
    mode = "manual" if width is not None else "auto"
    if width is None:
        width = auto_zoom_width(root, current, previous_width)
    window = (root - width / 2, root + width / 2)
    view = geometry_limits(
        model, None, [model.left, root, model.right], head_range=window
    )
    view["zoom_range"] = width
    view["zoom_mode"] = mode
    return view


def input_guide(ax, head, value, floor):
    """The same thin orange projection in both experiment sections."""
    (guide,) = ax.plot(
        [head, head], [floor, value], color=ORANGE, lw=0.55, ls=":", zorder=4
    )
    guide.set_gid("current_input_guide")
    ax.plot(head, value, "o", color=ORANGE, ms=4.5, zorder=6)


def head_axis_ticks(ax, limits):
    """Keep absolute heads legible at the two finest manual zoom stages."""
    ax.ticklabel_format(axis="x", useOffset=False, style="plain")
    if limits and limits.get("zoom_range", 1.0) < 0.001:
        ax.locator_params(axis="x", nbins=3)


def zoom_badge(ax, limits, text):
    if limits and "zoom_range" in limits:
        badge = ax.text(
            0.98,
            0.03,
            text["fig_zoom_range"].format(
                mode=text["zoom_" + limits.get("zoom_mode", "auto")],
                width=limits["zoom_range"],
            ),
            ha="right",
            va="bottom",
            fontsize=8,
            transform=ax.transAxes,
            bbox=dict(
                facecolor="#f6f8fa",
                edgecolor="#bec5cc",
                alpha=0.94,
                boxstyle="round,pad=0.25",
                linewidth=0.5,
            ),
            zorder=8,
        )
        badge.set_gid("zoom_range")


# 2. Three-cell sketch and interactive profile share the positive-flow convention.
def three_cell_flux_arrows(ax, dx, height):
    """Left flow reaches the central cell's left face; right flow leaves its right face."""
    for tail, tip, label in ((-0.12, 0.5, "$+Q_L$"), (1.5, 2.12, "$+Q_R$")):
        origin = (tail * dx, height)
        arrow = ax.annotate(
            "",
            (tip * dx, height),
            origin,
            arrowprops=dict(
                arrowstyle="->", color=CELL_TEXT, lw=1.2, shrinkA=0, shrinkB=0
            ),
            zorder=5,
        )
        arrow.set_gid("reference_flux_arrow")
        caption = ax.annotate(
            label,
            origin,
            xytext=(2, 3),
            textcoords="offset points",
            ha="left",
            va="bottom",
            color=CELL_TEXT,
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none", alpha=0.85),
            zorder=6,
        )
        caption.set_gid("flux_label")


def three_schematic(labels=None, left=7.0, right=2.0, height=8.0):
    """Compact model preview; perspective faces sit behind the front section."""
    text = labels or load_ui("en")
    fig, ax = axes((6.2, 3.1))
    depth_x, depth_z = 0.20, 0.10 * height
    faces = [
        (
            [
                (-0.5, height),
                (2.5, height),
                (2.5 + depth_x, height + depth_z),
                (-0.5 + depth_x, height + depth_z),
            ],
            "#edf1f5",
        ),
        (
            [
                (2.5, 0),
                (2.5 + depth_x, depth_z),
                (2.5 + depth_x, height + depth_z),
                (2.5, height),
            ],
            "#d9e2e9",
        ),
    ]
    for points, color in faces:
        face = Polygon(
            points, closed=True, facecolor=color, edgecolor="#8D9AA5", lw=0.8, zorder=0
        )
        face.set_gid("preview_depth")
        ax.add_patch(face)
    for x in (0.5, 1.5):
        ax.plot(
            [x, x + depth_x],
            [height, height + depth_z],
            color="#8D9AA5",
            lw=0.7,
            zorder=0,
        )
    for i, head in enumerate((left, None, right)):
        ax.add_patch(
            Rectangle(
                (i - 0.5, 0), 1, height, fc="#F0EEE7", ec="#8D9AA5", lw=1, zorder=1
            )
        )
        if head is not None:
            ax.add_patch(
                Rectangle(
                    (i - 0.5, 0),
                    1,
                    min(head, height),
                    fc=BOUNDARY_WATER,
                    ec="none",
                    alpha=0.7,
                    zorder=2,
                )
            )
            ax.plot(
                [i - 0.5, i + 0.5], [head, head], color=BOUNDARY_HEAD, lw=1.7, zorder=3
            )
        ax.text(
            i,
            0.62 * height,
            "h = ?" if i == 1 else f"h = {head:g} m",
            ha="center",
            fontsize=12,
            weight="bold",
            zorder=4,
        )
        label = ax.text(
            i,
            0.96 * height,
            text["fig_cell"].format(cell=i + 1),
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
            fontstyle="italic",
            color=CELL_TEXT,
            zorder=5,
        )
        label.set_gid("cell_label")
        if i != 1:
            ax.text(
                i,
                0.45 * height,
                text["fig_specified"],
                ha="center",
                va="center",
                fontsize=8.5,
                color=CELL_TEXT,
                zorder=4,
            )
    three_cell_flux_arrows(ax, 1, 0.13 * height)
    ax.annotate(
        "",
        (1, 1.26 * height),
        (1, 1.03 * height),
        arrowprops=dict(arrowstyle="->", color="#7a4499", lw=1.3),
    )
    ax.text(1.15, 1.19 * height, text["fig_optional_et"], color="#7a4499", fontsize=9)
    ax.set(
        xlim=(-0.58, 2.78),
        ylim=(-0.05 * height, 1.31 * height),
        ylabel="$z$ (m)",
        xticks=[],
        yticks=[0, height],
    )
    ax.spines["bottom"].set_visible(False)
    return fig


# 3. Reference saturation is fixed; current iterates are line/symbol overlays.
def cell_head_line(ax, x, heads, dx, **style):
    """Horizontal cell-head marks, with optional symbols at cell centres."""
    heads = np.asarray(heads)
    empty = np.full(len(x), np.nan)
    xs = np.column_stack((x - 0.5 * dx, x, x + 0.5 * dx, empty)).ravel()
    ys = np.column_stack((heads, heads, heads, empty)).ravel()
    (line,) = ax.plot(xs, ys, markevery=list(range(1, len(xs), 4)), **style)
    return line


def profile(model, ref, states, selected, labels=None, *, active_methods=()):
    """Plot specified and iterated heads; emphasis changes only the drawing style."""
    text = labels or load_ui("en")
    three = model.n == 3
    fig, ax = axes((8.6, 4.3 if three else 4.1))
    x = np.arange(model.n) * model.dx
    bottom = model.bottom
    mehl = three and model.top is None
    top = (
        model.top
        if model.top is not None
        else (5.0 if mehl else max(8.0, max(ref) * 1.15))
    )
    upper = max(8.0 if three else 20.0, top, float(max(ref))) if not mehl else 5.0
    pad = 0.055 * (upper - bottom)
    span = top - bottom
    number_y = bottom - 1.10 * pad
    # High recharge at low K can compress the layer to just a few text lines.
    # Keep its boundary name inside and put the numeric value above the layer.
    shallow_frame = not three and span < 0.30 * (upper - bottom)
    caption_fraction = 0.35 if three else (0.5 if shallow_frame else 0.17)
    zones = len(set(model.conductivity)) > 1 and not three
    for i in range(model.n):
        left = x[i] - model.dx / 2
        ax.add_patch(
            Rectangle((left, bottom), model.dx, span, fc="#F0EEE7", ec="none", zorder=0)
        )
        wet_top = np.clip(ref[i], bottom, top) if model.unconfined else top
        fill = (
            BOUNDARY_WATER
            if i in (0, model.n - 1)
            else (
                ("#dcebdc" if i < 5 else "#ede3bb" if i == 5 else "#c8def0")
                if zones
                else "#B9DEF1"
            )
        )
        water = Rectangle(
            (left, bottom),
            model.dx,
            wet_top - bottom,
            fc=fill,
            ec="none",
            alpha=0.65 if i in (0, model.n - 1) else 0.85,
            zorder=1,
        )
        water.set_gid("reference_water_" + str(i))
        ax.add_patch(water)
        frame = Rectangle(
            (left, bottom), model.dx, span, fill=False, ec="#808991", lw=1.25, zorder=2
        )
        frame.set_gid("aquifer_cell")
        ax.add_patch(frame)
        label_artist = ax.text(
            x[i],
            number_y,
            str(i + 1),
            ha="center",
            va="center",
            fontsize=12 if three else 10.5,
            fontstyle="italic",
            color=CELL_TEXT,
            zorder=5,
        )
        label_artist.set_gid("cell_label")
        if i in (0, model.n - 1):
            ax.text(
                x[i],
                bottom + caption_fraction * span,
                (
                    text["fig_specified"]
                    if three
                    else text["fig_specified"].replace(" ", "\n")
                ),
                ha="center",
                va="center",
                fontsize=11 if three else 8,
                color=CELL_TEXT,
                zorder=5,
            )
            label_height = bottom + 0.62 * span
            boundary_head = model.left if i == 0 else model.right
            if shallow_frame:
                label_height = max(top, boundary_head) + 0.35 * pad
            elif not three and abs(label_height - boundary_head) < 2 * pad:
                label_height = min(top - 2 * pad, boundary_head + 2.5 * pad)
            head_label = ax.text(
                x[i],
                label_height,
                (
                    f"h = {boundary_head:g} m"
                    if three
                    else f"$h =$\n${boundary_head:g}$ m"
                ),
                ha="center",
                va="bottom" if shallow_frame else "center",
                fontsize=16 if three else 10.5,
                weight="bold",
                zorder=5,
            )
            head_label.set_gid("specified_head_value")
    boundary_line = cell_head_line(
        ax,
        x[[0, -1]],
        [model.left, model.right],
        model.dx,
        color=BOUNDARY_HEAD,
        lw=1.8,
        zorder=3,
    )
    boundary_line.set_gid("specified_heads")
    cell_head_line(
        ax,
        x[1:-1],
        ref[1:-1],
        model.dx,
        color="#59656f",
        lw=1.8,
        ls=(0, (3, 2)),
        label=text["fig_final"],
        zorder=3,
    )
    for method, state in states.items():
        cell_head_line(
            ax,
            x[1:-1],
            state["heads"][-1][1:-1],
            model.dx,
            **method_style(method, method in active_methods),
            label=method,
            zorder=4 if method == "Picard" else 5,
        )
    # Physical height of the reference water column in the selected cell.
    wet = max(0.0, min(ref[selected], top) - bottom)
    if three:
        # Reserve a low band for the labels even when the confined roof is
        # well below the specified heads and the layer appears shallow.
        three_cell_flux_arrows(ax, model.dx, bottom + min(0.35 * wet, 0.07 * span))
    else:
        ax.add_patch(
            Rectangle(
                (x[selected] - model.dx / 2, bottom),
                model.dx,
                span,
                fill=False,
                ec=ORANGE,
                lw=1.5,
                zorder=3,
            )
        )
        for face, label in ((selected - 1, "$+Q_L$"), (selected, "$+Q_R$")):
            mid = (x[face] + x[face + 1]) / 2
            height = bottom + 0.35 * wet
            arrow = ax.annotate(
                "",
                (mid + 0.18 * model.dx, height),
                (mid - 0.18 * model.dx, height),
                arrowprops=dict(arrowstyle="->", color="#515b63", lw=1.1),
            )
            arrow.set_gid("reference_flux_arrow")
            ax.text(
                mid, bottom + 0.65 * wet, label, ha="center", va="center", fontsize=11
            )
    # Mehl has no aquifer roof; its fixed 5 m viewing limit does not cap T.
    if model.recharge > 0:
        for i in range(1, model.n - 1):
            ax.annotate(
                "",
                (x[i], top + 0.1 * pad),
                (x[i], top + 1.2 * pad),
                arrowprops=dict(arrowstyle="->", color="#245caa", lw=1),
            )
        ax.text(
            x[model.n // 2],
            top + 1.45 * pad,
            text["fig_recharge"],
            ha="center",
            fontsize=12,
            color="#245caa",
        )
    if three and model.et_max > 0:
        ax.annotate(
            "",
            (x[1], top - 0.8 * pad if mehl else top + 1.2 * pad),
            (x[1], top - 3.5 * pad if mehl else top - 0.8 * pad),
            arrowprops=dict(arrowstyle="->", color="#7a4499", lw=1.3),
        )
        ax.text(
            x[1] + 12,
            top - 2 * pad if mehl else top + 0.4 * pad,
            "$E(h)$",
            fontsize=14,
            color="#7a4499",
        )
    ax.text(
        (x[1] if shallow_frame else x[0]) - model.dx / 2 + 3,
        top + 0.2 * pad if mehl else top + 1.45 * pad,
        text["fig_top" if model.top is not None else "fig_display_top"].format(top=top),
        fontsize=12,
        color="#566976",
        va="bottom",
    )
    # Align both margin notes in data height, independently of the view limits.
    margin = ax.get_yaxis_transform()
    ax.text(
        1.02,
        bottom,
        text["fig_bottom"].format(bottom=bottom),
        transform=margin,
        fontsize=10.5,
        color=CELL_TEXT,
        va="bottom",
    )
    ax.text(
        1.02,
        number_y,
        text["fig_cell_number"],
        transform=margin,
        fontsize=9.5,
        fontstyle="italic",
        color=CELL_TEXT,
        va="center",
    )
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=12, frameon=False)
    ax.set(
        xlim=(x[0] - model.dx / 2, x[-1] + model.dx / 2),
        ylim=(bottom - 1.9 * pad, 5.0 if mehl else upper + 2.1 * pad),
        xlabel="$x$ (m)",
        ylabel=r"$h,\ z$ (m)",
    )
    ax.tick_params(labelsize=14 if three else 13)
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    ax.grid(False)
    return fig


# 4. Fixed-axis iteration geometry, with thin dotted input projections
def geometry(
    model, state, method, root, omega=1.0, diagnostic=False, limits=None, labels=None
):
    text = labels or load_ui("en")
    fig, ax = axes((4.0, 3.5))
    hs = np.array(state["heads"])[:, 1]
    limits = limits or geometry_limits(
        model, state["heads"][0], [model.left, root, model.right]
    )
    low, high = limits["head"]
    wetlow = max(model.bottom + 1e-7, low) if model.unconfined else low
    cuts = [wetlow, high]
    if model.unconfined and model.top is not None and wetlow < model.top < high:
        cuts.append(model.top)
    if model.et_max > 0:
        cuts += [
            v
            for v in (model.et_surface - model.et_depth, model.et_surface)
            if wetlow < v < high
        ]
    for n, (a, b) in enumerate(zip(sorted(cuts)[:-1], sorted(cuts)[1:])):
        xs = np.linspace(a + 1e-10, b - 1e-10, 180)
        vals = np.array([scalar_values(model, x) for x in xs])
        ys = vals[:, 0 if method == "Picard" else 1]
        ax.plot(
            xs,
            ys,
            color=COLORS[method],
            lw=1.8,
            label=(
                (r"$f_P(h)$" if method == "Picard" else r"$f_N(h)=F(h)$")
                if n == 0
                else None
            ),
        )
        if method == "Picard" and omega < 1 and not diagnostic:
            ax.plot(
                xs,
                xs + omega * (ys - xs),
                color=ORANGE,
                lw=1,
                ls=":",
                label=r"$g_{P,\omega}$" if n == 0 else None,
            )
    if method == "Picard":
        ax.plot(
            [low, high], [low, high], color="#777", ls="--", lw=0.85, label=r"$y=h$"
        )
    else:
        ax.axhline(0, color="#777", ls="--", lw=0.85)
    ax.axvline(root, color="#adb3b8", ls=":", lw=0.7)
    if not diagnostic:
        ax.plot(
            root,
            root if method == "Picard" else 0,
            "o",
            color="#8b9399",
            ms=3.5,
            label=text["fig_final"],
        )
        for k, (a, b) in enumerate(zip(hs[:-1], hs[1:])):
            fp, fn, dfn = scalar_values(model, a)
            if method == "Picard":
                # Solid cobweb; the initial axis-to-curve projection is dotted.
                if k:
                    ax.plot([a, a], [a, b], color=ORANGE, lw=0.85)
                else:
                    ax.plot([a, a], [low, b], color=ORANGE, lw=0.55, ls=":")
                ax.plot([a, b], [b, b], color=ORANGE, lw=0.85)
            else:
                full = a - fn / dfn if dfn else a
                ax.plot([a, a], [0, fn], color=ORANGE, ls=":", lw=0.55)
                ax.plot([a, full], [fn, 0], color=ORANGE, lw=0.85)
                if omega < 1:
                    ax.plot(
                        [b, b], [fn + dfn * (b - a), 0], color=ORANGE, lw=0.55, ls=":"
                    )
        if state["rejected"] is not None:
            last = hs[-1]
            rejected = state["rejected"][1]
            fp, fn, _ = scalar_values(model, last)
            ax.plot(
                rejected,
                rejected if method == "Picard" else 0,
                "x",
                color="#b42222",
                ms=7,
            )
            if method == "Newton":
                ax.plot([last, rejected], [fn, 0], color="#b42222", lw=0.8, ls=":")
            else:
                ax.plot(
                    [last, last, rejected],
                    [last, rejected, rejected],
                    color="#b42222",
                    lw=0.8,
                    ls=":",
                )
    last = hs[-1]
    fp, fn, _ = scalar_values(model, last)
    current = fp if method == "Picard" else fn
    if method == "Picard" and not diagnostic and len(hs) > 1:
        # Finish the evaluation at the current head, even when approached from
        # above. This is not another accepted update or a transfer to y = h.
        (evaluation,) = ax.plot(
            [last, last], [last, current], color=ORANGE, lw=0.85, zorder=5
        )
        evaluation.set_gid("current_picard_evaluation")
    # The guide is subordinate to the curve and actual iteration construction.
    floor = limits["head"][0] if method == "Picard" else limits["residual"][0]
    input_guide(ax, last, current, floor)
    if model.et_max > 0:
        for v in (model.et_surface - model.et_depth, model.et_surface):
            ax.axvline(v, color="#b6bdc3", ls="--", lw=0.6)
    ax.set(
        xlim=(low, high),
        ylim=limits["head"] if method == "Picard" else limits["residual"],
        xlabel=r"$h$ (m)",
        ylabel=r"$f_P$ (m)" if method == "Picard" else r"$f_N=F$ (m³/s)",
    )
    if method == "Newton":
        ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
    else:
        ax.ticklabel_format(axis="y", useOffset=False, style="plain")
    head_axis_ticks(ax, limits)
    zoom_badge(ax, limits, text)
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.02),
        ncols=2,
        fontsize=10,
        frameon=False,
        borderaxespad=0,
    )
    return fig


def matching_head(model, state, method, reference_head, cell, omega, limits):
    """Find the displayed Picard curve's diagonal crossing for zoom centring.

    Its crossing can differ from the global reference while neighbors change.
    The reduced Newton residual always has the reference head as its zero.
    """
    if method == "Newton":
        return reference_head
    from scipy.optimize import brentq

    try:
        step = coupled_step(model, state, method, cell, omega)
        if step["use_alpha"]:
            return reference_head
        xs = np.unique(
            np.r_[np.linspace(*limits["head"], 100), step["x0"], step["xend"]]
        )
        ys = step_values(model, step, xs) - xs
        roots = [float(x) for x, y in zip(xs, ys) if y == 0]
        for a, b, fa, fb in zip(xs[:-1], xs[1:], ys[:-1], ys[1:]):
            if np.isfinite(fa) and np.isfinite(fb) and fa * fb < 0:
                roots.append(
                    brentq(lambda h: step_values(model, step, [h])[0] - h, a, b)
                )
        return (
            min(roots, key=lambda h: abs(h - reference_head))
            if roots
            else reference_head
        )
    except (np.linalg.LinAlgError, ValueError):
        return reference_head


def coupled_geometry(
    model, state, method, root, cell, omega=1.0, limits=None, labels=None
):
    """Scalar-style constructions from accepted full-system steps only.

    Newton's reduced residual is fixed and can carry its accepted history.
    Picard shows only the latest accepted construction and its own function;
    earlier functions differ. All accepted heads remain in the history plots.
    """
    text = labels or load_ui("en")
    fig, ax = axes((4.0, 3.5))
    bounds = limits["head"] if limits else (0.0, max(30.0, root * 1.1))
    try:
        step = coupled_step(model, state, method, cell, omega)
        accepted_indices = range(len(state["heads"]) - 1)
        if method == "Picard":
            # A rejected proposal uses a new base curve, so even the last
            # accepted step would belong to a different Picard function.
            accepted_indices = accepted_indices[-1:] if step["accepted"] else []
        accepted = [
            coupled_step(
                model,
                dict(state, heads=state["heads"][: k + 2], rejected=None),
                method,
                cell,
                omega,
            )
            for k in accepted_indices
        ]
    except np.linalg.LinAlgError:
        ax.text(0.5, 0.5, text["singular"], ha="center", transform=ax.transAxes)
        return fig
    low, high = (-0.25, 1.25) if step["use_alpha"] else bounds
    xs = np.unique(np.r_[np.linspace(low, high, 240), step["x0"], step["xend"]])
    xs = xs[(xs >= low) & (xs <= high)]
    ys = step_values(model, step, xs)
    ax.plot(
        xs,
        ys,
        color=COLORS[method],
        lw=1.8,
        label=(
            r"$f_{P,i}^{(k)}$"
            if method == "Picard"
            else r"$f_{N,i}=F_i^{\mathrm{red}}$"
        ),
    )[0].set_gid("coupled_curve")
    if method == "Picard":
        inputs = (
            step["base"][cell] + xs * step["direction"][cell]
            if step["use_alpha"]
            else xs
        )
        ax.plot(
            xs,
            inputs,
            color="#777",
            ls="--",
            lw=0.85,
            label=r"$h_i(\alpha)$" if step["use_alpha"] else r"$y=h_i$",
        )
        if step["omega"] < 1:
            ax.plot(
                xs,
                inputs + step["omega"] * (ys - inputs),
                color=ORANGE,
                ls=":",
                lw=1,
                label=r"$g_{P,\omega}$",
            )
        ax.set(ylim=bounds, ylabel=r"$f_{P,i}$ (m)")
        ax.ticklabel_format(axis="y", useOffset=False, style="plain")
    else:
        ax.axhline(0, color="#777", ls="--", lw=0.85)
        # Fit the visible residual, not off-screen early iterates, when zooming.
        finite = np.r_[ys[np.isfinite(ys)], 0.0]
        span = max(float(np.ptp(finite)), 1e-16)
        ax.set(
            ylim=(min(finite) - 0.12 * span, max(finite) + 0.12 * span),
            ylabel=r"$f_{N,i}=F_i^{\mathrm{red}}$ (m³/s)",
        )
        ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
    if method == "Newton" and not step["use_alpha"]:
        ax.axvline(root, color="#adb3b8", ls=":", lw=0.7)
        ax.plot(root, 0, "o", color="#8b9399", ms=3.5)
    # A degenerate step-fraction view cannot share the older head-axis paths.
    shown = accepted[-1:] if step["use_alpha"] else accepted
    for index, item in enumerate(shown):
        if item["use_alpha"] != step["use_alpha"]:
            continue
        a, b = item["x0"], item["xend"]
        last = index == len(shown) - 1
        if method == "Picard":
            start_head = item["base"][cell]
            end_head = start_head + item["omega"] * item["direction"][cell]
            if item["k"] == 0:
                ax.plot([a, a], [bounds[0], end_head], color=ORANGE, lw=0.55, ls=":")
                path_x, path_y = [a, b], [end_head, end_head]
            else:
                path_x, path_y = [a, a, b], [start_head, end_head, end_head]
            ax.plot(path_x, path_y, color=ORANGE, lw=0.85, zorder=4)[0].set_gid(
                "coupled_picard_step"
            )
        else:
            f0 = item["residual"]
            ax.plot([a, a], [0, f0], color=ORANGE, ls=":", lw=0.55)
            ax.plot([a, item["xfull"]], [f0, 0], color=ORANGE, lw=0.85, zorder=4)[
                0
            ].set_gid(
                "coupled_newton_tangent"
                if last
                else "past_newton_tangent_" + str(item["k"])
            )
            if item["omega"] < 1:
                ax.plot(
                    [b, b],
                    [f0 + item["slope"] * (b - a), 0],
                    color=ORANGE,
                    ls=":",
                    lw=0.55,
                )
    current_x = step["xend"] if step["accepted"] else step["x0"]
    current_y = step_values(model, step, [current_x])[0]
    if method == "Picard" and accepted:
        ax.plot(
            [current_x, current_x],
            [state["heads"][-1][cell], current_y],
            color=ORANGE,
            lw=0.85,
            zorder=5,
        )[0].set_gid("current_picard_evaluation")
    input_guide(ax, current_x, current_y, ax.get_ylim()[0])
    # Failed proposals remain visibly rejected, never counted as accepted steps.
    if state["rejected"] is not None and not step["use_alpha"]:
        bad = state["rejected"][cell]
        ax.plot(bad, bad if method == "Picard" else 0, "x", color="#b42222", ms=7)
    ax.set(
        xlim=(low, high),
        xlabel=text["fig_step_fraction"] if step["use_alpha"] else r"$h_i$ (m)",
    )
    head_axis_ticks(ax, None if step["use_alpha"] else limits)
    if not step["use_alpha"]:
        zoom_badge(ax, limits, text)
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.02),
        ncols=2,
        fontsize=10,
        frameon=False,
        borderaxespad=0,
    )
    return fig


# 5. Actual convergence measures, then a separate selected-cell head history
def history_style(method, quantity):
    """Color identifies the method; symbol identifies the physical quantity."""
    flow = quantity == "flow"
    return dict(
        color=COLORS[method],
        marker="s" if flow else "o",
        markersize=(
            (6 if method == "Picard" else 4)
            if flow
            else (7 if method == "Picard" else 5)
        ),
        markerfacecolor=COLORS[method] if flow else "none",
        markeredgewidth=1.1,
        linestyle="-" if flow else "--",
        linewidth=1.2,
    )


def mark_outside_convergence_range(ax, steps, values, color, method):
    """Mark clipped points at the edge; leave their numerical series unchanged."""
    steps, values = np.asarray(steps), np.asarray(values)
    for bound, outside, marker in (
        (CONVERGENCE_YLIM[0], values < CONVERGENCE_YLIM[0], "v"),
        (CONVERGENCE_YLIM[1], values > CONVERGENCE_YLIM[1], "^"),
    ):
        if np.any(outside):
            ax.plot(
                steps[outside],
                np.full(np.count_nonzero(outside), bound),
                linestyle="none",
                marker=marker,
                color=color,
                markersize=7 if method == "Picard" else 4,
                clip_on=False,
                zorder=4,
            )


def convergence(states, flow_tol=FLOW_TOL, *, head_tol=HEAD_TOL, labels=None):
    """Global balance residual and accepted head changes; neither is head error."""
    text = labels or load_ui("en")
    fig, head_ax = axes((7.6, 3.7))
    flow_ax = head_ax.twinx()
    flow_ax.spines["right"].set_visible(True)
    flow_ax.spines["left"].set_visible(False)
    for ax, quantity, side in (
        (head_ax, "change", "left"),
        (flow_ax, "flow", "right"),
    ):
        # Fix both scales before adding artists, including at k = 0 when no
        # head-change observation exists. Colors identify quantities, not methods.
        ax.set_yscale("log")
        ax.set_ylim(CONVERGENCE_YLIM)
        ax.set_yticks([100.0, 1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12])
        ax.tick_params(axis="y", which="both", colors=QUANTITY_COLORS[quantity])
        ax.yaxis.label.set_color(QUANTITY_COLORS[quantity])
        ax.spines[side].set_color(QUANTITY_COLORS[quantity])
    changes = {
        method: np.max(np.abs(np.diff(state["heads"], axis=0)), axis=1)
        for method, state in states.items()
    }
    for method, state in states.items():
        (flow,) = flow_ax.plot(
            range(len(state["residual"])),
            np.maximum(state["residual"], 1e-18),
            **history_style(method, "flow"),
            label=text["fig_residual_method"].format(method=method),
        )
        flow.set_gid("flow_residual_" + method)
        # k = 0 has no previous iterate, so no head change is fabricated there.
        (change,) = head_ax.plot(
            range(1, len(state["heads"])),
            np.maximum(changes[method], 1e-18),
            **history_style(method, "change"),
            label=text["fig_change_method"].format(method=method),
        )
        change.set_gid("head_change_" + method)
        mark_outside_convergence_range(
            flow_ax,
            range(len(state["residual"])),
            state["residual"],
            COLORS[method],
            method,
        )
        mark_outside_convergence_range(
            head_ax,
            range(1, len(state["heads"])),
            changes[method],
            COLORS[method],
            method,
        )
    flow_ax.axhline(
        flow_tol,
        color=QUANTITY_COLORS["flow"],
        ls=":",
        lw=1,
        label=text["fig_flow_closure"].format(value=flow_tol),
    ).set_gid("flow_closure")
    head_ax.axhline(
        head_tol,
        color=QUANTITY_COLORS["change"],
        ls="-.",
        lw=1,
        label=text["fig_head_closure"].format(value=head_tol),
    ).set_gid("head_closure")
    last = max(len(s["residual"]) - 1 for s in states.values())
    head_ax.set(
        xlim=(0, last + 1),
        xlabel=text["fig_iteration_axis"],
        ylabel=r"$\max_i|\Delta h_i|$ (m)",
    )
    flow_ax.set_ylabel(r"$\max_i|F_i|$ (m³/s)")
    head_ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    handles, names = head_ax.get_legend_handles_labels()
    h, n = flow_ax.get_legend_handles_labels()
    # Each legend column is one quantity, with matching method colors.
    head_ax.legend(
        handles[:2] + h[:2] + handles[2:] + h[2:],
        names[:2] + n[:2] + names[2:] + n[2:],
        loc="lower left",
        bbox_to_anchor=(0, 1.06),
        ncols=3,
        fontsize=9,
        frameon=False,
        borderaxespad=0,
    )
    return fig


def head_history(states, *, cell=1, true_head, labels=None):
    """Selected-cell heads from k = 0 onward, against the independent solution."""
    text = labels or load_ui("en")
    tails = detail_tails(states, cell, true_head)
    if tails:
        fig, (ax, detail) = plt.subplots(1, 2, figsize=(9.0, 3.4), layout="constrained")
    else:
        fig, ax = axes((7.6, 3.1))
    values = [true_head]
    for method, state in states.items():
        heads = np.asarray(state["heads"])[:, cell]
        values.extend(heads)
        style = history_style(method, "head")
        style["linestyle"] = "-" if method == "Picard" else "--"
        (line,) = ax.plot(
            range(len(heads)),
            heads,
            **style,
            label=text["fig_head_method"].format(method=method),
        )
        line.set_gid("head_history_" + method)
    ax.axhline(
        true_head,
        color="#59656f",
        ls=(0, (3, 2)),
        lw=1.8,
        label=text["fig_true_head_history"].format(head=true_head),
        zorder=1,
    ).set_gid("true_head_history")
    last = max(len(s["heads"]) - 1 for s in states.values())
    margin = max(0.05, 0.12 * (max(values) - min(values)))
    ax.set(
        xlim=(0, last + 1),
        ylim=(min(values) - margin, max(values) + margin),
        xlabel=text["fig_iteration_axis"],
        ylabel=text["fig_head_axis"].format(cell=cell + 1),
    )
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.ticklabel_format(axis="y", useOffset=False, style="plain")
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.06),
        ncols=3,
        fontsize=9,
        frameon=False,
        borderaxespad=0,
    )
    if tails:
        # The left panel retains every sample. The detail shows only methods
        # with three consecutive sub-centimetre updates near the reference.
        zoom_values = [true_head]
        first = min(int(k[0]) for k, h in tails.values())
        for method, (k, h) in tails.items():
            style = history_style(method, "head")
            style["linestyle"] = "-" if method == "Picard" else "--"
            detail.plot(k, h, **style, label=method)[0].set_gid("head_detail_" + method)
            zoom_values.extend(h)
        detail.axhline(true_head, color="#59656f", ls=(0, (3, 2)), lw=1.5)
        span = max(zoom_values) - min(zoom_values)
        pad = max(span * 0.2, 1e-8)
        detail.set(
            xlim=(first, last + 1),
            ylim=(min(zoom_values) - pad, max(zoom_values) + pad),
            xlabel=text["fig_iteration_axis"],
            ylabel=text["fig_head_axis"].format(cell=cell + 1),
        )
        detail.text(
            0.02,
            0.97,
            text["fig_head_detail"],
            transform=detail.transAxes,
            va="top",
            fontsize=9,
        )
        detail.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        detail.ticklabel_format(axis="y", useOffset=False, style="plain")
        detail.legend(
            loc="lower left",
            bbox_to_anchor=(0, 1.06),
            ncols=2,
            fontsize=9,
            frameon=False,
            borderaxespad=0,
        )
        ax.legend(
            loc="lower left",
            bbox_to_anchor=(0, 1.06),
            ncols=1,
            fontsize=8,
            frameon=False,
            borderaxespad=0,
        )
        ax.axvspan(first, last + 1, color="#dbe4ed", alpha=0.3, zorder=0)
    return fig
