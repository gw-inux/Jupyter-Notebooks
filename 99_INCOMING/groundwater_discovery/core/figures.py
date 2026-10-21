"""Original teaching diagrams. Exact scientific geometry, qualitative displays."""

import re
from io import StringIO
from threading import RLock
import xml.etree.ElementTree as ET
import numpy as np
from matplotlib import rc_context
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon
from matplotlib.text import Text
from core.models import (
    beach_hole,
    grain_centres,
    lens_profile,
    island_surface,
    sample_volumes,
    cycle_head,
    cup_dimensions,
    BEACH_GROUND_SLOPE,
    BEACH_WATER_SLOPE,
)

BLUE = "#197F9E"
SAND = "#DEC796"
INK = "#253B47"
ORANGE = "#CE7831"
_SVG_LOCK = RLock()
_SVG_NS = "http://www.w3.org/2000/svg"
_ARABIC = re.compile("[\u0600-\u06ff]")


def plot_text(value):
    """Keep logical Unicode order; the browser shapes Arabic in SVG output."""
    return value


def needs_browser_text(fig):
    return any(_ARABIC.search(text.get_text()) for text in fig.findobj(Text))


def browser_svg(fig):
    """Export real SVG text so the browser handles Arabic shaping and bidi.

    Uses only Python's standard library and the existing Matplotlib dependency.
    No reversed strings, presentation-form substitution, scripts or web fonts.
    Switching direction also swaps start/end anchors to retain physical label
    alignment (especially left-aligned legend labels beside their swatches).
    """
    with _SVG_LOCK, rc_context({"svg.fonttype": "none"}):
        buffer = StringIO()
        fig.savefig(buffer, format="svg")
        root = ET.fromstring(buffer.getvalue())
        ET.register_namespace("", _SVG_NS)
        ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        for node in root.iter(f"{{{_SVG_NS}}}text"):
            if not _ARABIC.search("".join(node.itertext())):
                continue
            style = dict(
                item.strip().split(":", 1)
                for item in node.get("style", "").split(";")
                if ":" in item
            )
            anchor = style.get("text-anchor", node.get("text-anchor", "start")).strip()
            style["text-anchor"] = {"start": "end", "end": "start", "middle": "middle"}[
                anchor
            ]
            style["direction"] = "rtl"
            style["unicode-bidi"] = "embed"
            node.set(
                "style",
                "; ".join(f"{key}: {value.strip()}" for key, value in style.items()),
            )
            node.set("lang", "ar")
            if node.text:
                # Keep scientific percentages such as ≈99% in LTR order inside
                # the RTL label. Unicode isolates are handled by the renderer.
                node.text = re.sub(
                    r"≈?\d+(?:[.,]\d+)?%",
                    lambda match: "\u2066" + match.group(0) + "\u2069",
                    node.text,
                )
        return ET.tostring(root, encoding="unicode")


def axes(figsize=(9, 4.5)):
    fig = Figure(figsize=figsize, layout="constrained")
    ax = fig.subplots()
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=10, colors=INK)
    return fig, ax


def water_store(t):
    fig, ax = axes((7, 4.7))
    for i in range(100):
        ax.add_patch(
            Rectangle(
                (i % 10, 9 - i // 10), 0.84, 0.84, facecolor=BLUE if i < 99 else ORANGE
            )
        )
    ax.set(xlim=(-0.2, 10), ylim=(-0.2, 10), aspect="equal")
    ax.axis("off")
    ax.legend(
        handles=[
            Rectangle(
                (0, 0), 1, 1, color=BLUE, label=plot_text(t("groundwater") + " ≈99%")
            ),
            Rectangle(
                (0, 0), 1, 1, color=ORANGE, label=plot_text(t("other_liquid") + " ≈1%")
            ),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        fontsize=10,
    )
    return fig


def pores(saturated, t):
    fig, ax = axes((8, 3.1))
    fill = "#B9DFEA" if saturated else "#F3F1EB"
    ax.set_facecolor(fill)
    for cx, cy in grain_centres():
        ax.add_patch(
            Ellipse(
                (cx, cy), 1, 0.56, facecolor=SAND, edgecolor="#8C7248", linewidth=1.5
            )
        )
    ax.set(xlim=(0.3, 8.7), ylim=(0.05, 2.5), aspect="equal", xticks=[], yticks=[])
    ax.legend(
        handles=[
            Ellipse((0, 0), 1, 0.56, facecolor=SAND, label=plot_text(t("grains"))),
            Rectangle(
                (0, 0),
                1,
                1,
                facecolor=fill,
                edgecolor=INK,
                label=plot_text(t("pore_water") if saturated else t("air")),
            ),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=2,
        frameon=False,
    )
    return fig


def volume(n, t):
    fig, ax = axes((8, 1.9))
    ax.barh([0], [(1 - n) * 100], height=0.5, color=SAND, label=plot_text(t("grains")))
    ax.barh(
        [0],
        [n * 100],
        height=0.5,
        left=[(1 - n) * 100],
        color=BLUE,
        label=plot_text(t("pore_water")),
    )
    ax.set(
        xlim=(0, 100), ylim=(-0.4, 1), yticks=[], xlabel=plot_text(t("volume_fraction"))
    )
    ax.legend(loc="upper center", ncol=2, frameon=False)
    return fig


def sample_cup(bulk, solid, t):
    """A growing open cup; colored areas are proportional to input volumes.

    The whole outline grows with the sample. Fixed plotting limits preserve
    size comparisons; there is no pre-drawn maximum-capacity container.
    The colors are a volume comparison, not physically separated layers.
    """
    pore, porosity_value = sample_volumes(bulk, solid)
    width, height = cup_dimensions(bulk)
    fig, ax = axes((8, 3.8))
    ax.set(xlim=(0, 7), ylim=(-0.15, 4.15), aspect="equal")
    ax.axis("off")
    if porosity_value is None:
        return fig  # The page shows an explanatory message instead of a plot.

    left = 2.1 - width / 2
    solid_height = height * solid / bulk
    pore_height = height * pore / bulk
    ax.add_patch(
        Rectangle(
            (left, 0),
            width,
            solid_height,
            facecolor=SAND,
            edgecolor="none",
            gid="solid_volume",
        )
    )
    ax.add_patch(
        Rectangle(
            (left, solid_height),
            width,
            pore_height,
            facecolor="#A2D0DF",
            edgecolor="none",
            gid="pore_volume",
        )
    )
    ax.plot(
        [left, left, left + width, left + width],
        [height, 0, 0, height],
        color=INK,
        lw=2.5,
    )
    ax.text(2.1, height + 0.15, f"{bulk:g} mL", ha="center", color=INK, fontsize=12)
    ax.legend(
        handles=[
            Rectangle((0, 0), 1, 1, facecolor=SAND, label=plot_text(t("solid_short"))),
            Rectangle(
                (0, 0), 1, 1, facecolor="#A2D0DF", label=plot_text(t("pore_volume"))
            ),
        ],
        loc="center left",
        bbox_to_anchor=(0.64, 0.55),
        frameon=False,
        fontsize=10,
    )
    return fig


def beach(x_hole, depth, reveal, t):
    fig, ax = axes((9, 3.7))
    x = np.linspace(-8, 22, 601)
    ground = BEACH_GROUND_SLOPE * x
    ax.fill_between(x, -0.6, ground, color="#F1E8D5")
    sea = x <= 0
    land = x >= 0
    ax.fill_between(x[sea], ground[sea], 0, color="#B9E1EE")
    ax.axhline(0, color=BLUE, ls=":", lw=1.2, label=plot_text(t("sea")))
    if reveal:
        ax.fill_between(x[sea], -0.6, ground[sea], color="#A2D0DF")
        h = BEACH_WATER_SLOPE * x[land]
        ax.fill_between(x[land], -0.6, h, color="#A2D0DF")
        ax.plot(x[land], h, color=BLUE, lw=2, label=plot_text(t("water_table")))
        for xx in [7, 13, 19]:
            ax.annotate(
                "",
                xy=(xx - 2, -0.18),
                xytext=(xx, -0.18),
                arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.4},
            )
    ax.plot(x, ground, color="#93743F", lw=1.8, label=plot_text(t("sand_surface")))
    g, h, b, w = beach_hole(x_hole, depth)
    half = 0.55
    # Erase a real open-topped excavation, including the sloping surface line.
    hole = Polygon(
        [
            (x_hole - half, BEACH_GROUND_SLOPE * (x_hole - half) + 0.006),
            (x_hole - half, b),
            (x_hole + half, b),
            (x_hole + half, BEACH_GROUND_SLOPE * (x_hole + half) + 0.006),
        ],
        facecolor="white",
        edgecolor="none",
        zorder=5,
    )
    ax.add_patch(hole)
    if reveal and w > 1e-12:
        ax.add_patch(
            Rectangle(
                (x_hole - half, b),
                2 * half,
                w,
                facecolor="#59B3D2",
                edgecolor="none",
                zorder=6,
            )
        )
    ax.plot(
        [x_hole - half, x_hole - half, x_hole + half, x_hole + half],
        [
            BEACH_GROUND_SLOPE * (x_hole - half),
            b,
            b,
            BEACH_GROUND_SLOPE * (x_hole + half),
        ],
        color=INK,
        lw=1.4,
        zorder=7,
    )
    ax.annotate(
        plot_text(t("hole")),
        xy=(x_hole, g + 0.01),
        xytext=(x_hole, 0.65),
        ha="center",
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": INK},
    )
    ax.set(xlim=(-8, 22), ylim=(-0.58, 0.85))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=3,
        fontsize=9,
    )
    return fig


def cycle(t):
    """Selected pathway in the global water cycle; not a full water budget."""
    fig, ax = axes((10, 4.8))
    ax.set(xlim=(0, 10), ylim=(0, 5))
    ax.axis("off")
    land_x = np.array([0, 2, 4, 6, 7, 8, 10])
    land_z = np.array([2.2, 2.3, 2.0, 1.65, 1.4, 0.8, 0.5])
    ax.fill_between(land_x, 0, land_z, color="#F1E8D5")
    ax.fill_between([7, 8, 10], [1.4, 0.8, 0.5], 1.4, color="#96D6E5")
    x = np.linspace(0, 7, 281)
    head = cycle_head(x)
    ax.fill_between(x, 0, head, color="#A2D0DF")
    ax.fill_between([7, 8, 10], 0, [1.4, 0.8, 0.5], color="#A2D0DF")
    ax.plot(x, head, color=BLUE, lw=2)
    # Hydraulic divide, not an impermeable wall. The head profile is flat here.
    ax.plot([0, 0], [0, 2.5], ls="--", color=INK, lw=2, clip_on=False)
    ax.annotate(
        plot_text(t("divide")),
        xy=(0, 2.1),
        xytext=(0.2, 2.7),
        ha="left",
        fontsize=9,
        color=INK,
        arrowprops={"arrowstyle": "-", "color": INK},
    )
    ax.text(
        0.08,
        -0.35,
        plot_text(t("no_flow")),
        ha="left",
        va="center",
        fontsize=9,
        color=INK,
    )
    ax.plot(land_x, land_z, color="#93743F", lw=1.5)
    for cx, cy, r in [(3.1, 4, 0.38), (3.5, 4.2, 0.48), (4, 4.1, 0.42), (4.4, 4, 0.32)]:
        ax.add_patch(Circle((cx, cy), r, facecolor="#DCE6EB", edgecolor="none"))

    def arrow(start, end, rad=0):
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={
                "arrowstyle": "-|>",
                "color": BLUE,
                "lw": 2.8,
                "mutation_scale": 16,
                "connectionstyle": f"arc3,rad={rad}",
            },
        )

    arrow((8.6, 1.42), (4.9, 4.1), 0.32)
    for xx in [3.1, 3.7, 4.3]:
        arrow((xx, 3.5), (xx, 2.5))
    for xx in [3.1, 4.3]:
        # Percolation arrows cross the unsaturated zone and end at its base:
        # groundwater recharge occurs when the water reaches the water table.
        ground = np.interp(xx, land_x, land_z)
        arrow((xx, ground + 0.12), (xx, float(cycle_head(xx))))
    arrow((3.5, 0.8), (7.8, 1.25), 0.1)
    arrow((0.65, 0.65), (2.6, 0.65))
    for xx, yy, key in [
        (8.7, 3.0, "evaporation"),
        (5.5, 4.65, "clouds"),
        (1.0, 3.25, "rain"),
        (5.3, 2.35, "recharge_simple"),
        (5.0, 0.4, "flow"),
        (9.1, 1.1, "surface_water"),
    ]:
        ax.text(
            xx,
            yy,
            plot_text(t(key)),
            ha="center",
            va="center",
            fontsize=10,
            color=INK,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 3},
        )
    ax.set_ylim(-0.65, 5)
    return fig


def lens(peak_head, t):
    """One cross section with land, seabed, freshwater and saline groundwater.

    Same coordinate transform for all curves. Fixed axes across comparisons.
    This is an island, unlike the half-coast in the supplied reference module.
    """
    fig, ax = axes((10, 4.8))
    x = np.linspace(-100, 100, 801)
    h, z = lens_profile(x, peak_head)
    ground = island_surface(x)
    ax.fill_between(
        x, -36, -z, color="#689FC8", hatch="//", edgecolor="#5589B1", linewidth=0
    )
    ax.fill_between(x, -z, h, color="#B8E5EB")
    ax.fill_between(x, h, ground, color="#EBDDCA")
    for lo, hi in [(-132, -100), (100, 132)]:
        sx = np.linspace(lo, hi, 100)
        bed = -0.14 * (np.abs(sx) - 100)
        ax.fill_between(
            sx, -36, bed, color="#689FC8", hatch="//", edgecolor="#5589B1", linewidth=0
        )
        ax.fill_between(sx, bed, 0, color="#8DC7E4")
        ax.plot(sx, bed, color="#806B4A", lw=1.5)
    ax.axhline(0, color=BLUE, ls=":", lw=1.2, label=plot_text(t("sea")))
    ax.plot(x, ground, color="#806B4A", lw=2, label=plot_text(t("land_surface")))
    ax.plot(x, h, color="#16888F", lw=2, label=plot_text(t("water_table")))
    ax.plot(x, -z, color="#215780", lw=2.3, label=plot_text(t("interface")))
    ax.text(0, -4, plot_text(t("freshwater")), ha="center", color=INK, fontsize=11)
    ax.text(
        0, -34, plot_text(t("saltwater")), ha="center", color="#123753", fontsize=11
    )
    ax.annotate(
        plot_text(t("land_surface")),
        xy=(0, 3),
        xytext=(0, 7.2),
        ha="center",
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": INK},
    )
    ax.set(xlim=(-132, 132), ylim=(-36, 10))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=2,
        fontsize=9,
    )
    return fig


def _pine_tree(ax, x, ground, scale=1.0):
    """Small landscape cue only; vegetation has no hydraulic model effect."""
    ax.plot([x, x], [ground, ground + 0.16 * scale], color="#766044", lw=2, zorder=4)
    for base, height, half_width in [
        (0.10, 0.23, 2.0),
        (0.21, 0.21, 1.6),
        (0.31, 0.19, 1.15),
    ]:
        ax.add_patch(
            Polygon(
                [
                    (x - half_width * scale, ground + base * scale),
                    (x + half_width * scale, ground + base * scale),
                    (x, ground + (base + height) * scale),
                ],
                facecolor="#4D8068",
                edgecolor="#365E4B",
                lw=0.7,
                zorder=4,
            )
        )


def river(x_hole, depth, regime, reveal, t):
    """Wide connected-river cross section and one hypothetical observation.

    Geometry and outcomes come from core.river. The land/water transformation
    stays fixed between scenarios; changing depth never changes local head.
    """
    from core.river import RIVER_BANK, river_ground, river_head, river_observation

    fig, ax = axes((11, 3.6))
    x = np.linspace(0, RIVER_BANK, 401)
    ground = river_ground(x)
    head = river_head(x, regime)
    bed, base = -0.8, -1.5

    # Ground and cut-bank river channel, with river level as the common datum.
    ax.fill_between(x, base, ground, color="#EBDDCA")
    ax.fill_between([RIVER_BANK, 100], base, bed, color="#EBDDCA")
    ax.fill_between([RIVER_BANK, 100], bed, 0, color="#8DC7E4")
    # Extend the surface-water level inland as a REFERENCE, not a water surface.
    ax.plot(
        [0, RIVER_BANK],
        [0, 0],
        color="#6D8494",
        ls=":",
        lw=1.6,
        label=plot_text(t("river_water_level")),
        gid="surface_level_reference",
    )
    if reveal:
        ax.fill_between(x, base, head, color="#A2D0DF")
        ax.fill_between([RIVER_BANK, 100], base, bed, color="#A2D0DF")
        ax.plot(
            x,
            head,
            color=BLUE,
            lw=2.4,
            label=plot_text(t("water_table")),
            gid="groundwater_table",
        )
        for left, right in [(5, 17), (38, 50), (66, 86)]:
            start, end = (left, right) if regime == "gaining" else (right, left)
            # The final arrow crosses the submerged bank, not dry land.
            ax.annotate(
                "",
                xy=(end, -0.5 if right == 86 else -1.15),
                xytext=(start, -0.5 if right == 86 else -1.15),
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": BLUE,
                    "lw": 2.5,
                    "mutation_scale": 15,
                },
            )
    ax.fill_between(x, ground - 0.025, ground, color="#CDDDBA", zorder=3)
    ax.plot(x, ground, color="#718557", lw=2, label=plot_text(t("land_surface")))
    for tree_x, scale in [(10, 0.85), (44, 0.8), (61, 0.7)]:
        _pine_tree(ax, tree_x, float(river_ground(tree_x)), scale)
    ax.plot(
        [RIVER_BANK, RIVER_BANK, 100], [ground[-1], bed, bed], color="#93743F", lw=2
    )
    ax.plot([RIVER_BANK, 100], [0, 0], color=BLUE, lw=2.4, gid="surface_water_level")

    # A virtual open hole avoids suggesting that real deep digging is needed.
    observation = river_observation(x_hole, depth, regime)
    half_width = 1.0
    left, right = x_hole - half_width, x_hole + half_width
    left_top, right_top = float(river_ground(left)), float(river_ground(right))
    ax.add_patch(
        Polygon(
            [
                (left, left_top + 0.02),
                (left, observation.bottom),
                (right, observation.bottom),
                (right, right_top + 0.02),
            ],
            facecolor="white",
            edgecolor="none",
            zorder=5,
        )
    )
    if reveal and observation.water_depth > 0:
        ax.add_patch(
            Rectangle(
                (left, observation.bottom),
                2 * half_width,
                observation.water_depth,
                facecolor="#59B3D2",
                edgecolor="none",
                zorder=6,
                gid="observation_water",
            )
        )
    ax.plot(
        [left, left, right, right],
        [left_top, observation.bottom, observation.bottom, right_top],
        color=INK,
        lw=1.5,
        zorder=7,
    )
    ax.annotate(
        plot_text(t("virtual_hole")),
        xy=(x_hole, observation.ground + 0.03),
        xytext=(x_hole, 1.85),
        ha="center",
        fontsize=11,
        arrowprops={"arrowstyle": "->", "color": INK},
    )
    ax.text(90, 0.28, plot_text(t("river_label")), ha="center", fontsize=11, color=INK)
    ax.set(xlim=(0, 100), ylim=(base, 2.12))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=2,
        fontsize=11,
    )
    return fig
