"""Original teaching diagrams. Exact scientific geometry, qualitative displays."""

import re
import base64
from pathlib import Path
from functools import lru_cache
from matplotlib.font_manager import FontProperties, fontManager
from textwrap import fill
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
_HINDI = re.compile("[\u0900-\u097f]")
_CHINESE = re.compile("[\u3400-\u9fff]")
_FONTS = Path(__file__).resolve().parents[1] / "assets/fonts"


def plot_text(value):
    """Keep logical Unicode order; the browser shapes Arabic in SVG output."""
    return value


def needs_browser_text(fig):
    return any(
        _ARABIC.search(text.get_text()) or _HINDI.search(text.get_text())
        for text in fig.findobj(Text)
    )


@lru_cache(maxsize=2)
def _font_family(filename):
    fontManager.addfont(str(_FONTS / filename))
    return FontProperties(fname=str(_FONTS / filename)).get_name()


def prepare_fonts(fig):
    """Bundled OFL fonts: no installation or additional Python dependency."""
    for text in fig.findobj(Text):
        value = text.get_text()
        filename = (
            "NotoSansDevanagari-Regular.ttf"
            if _HINDI.search(value)
            else "NotoSansSC-Regular.otf" if _CHINESE.search(value) else None
        )
        if filename:
            text.set_fontproperties(
                FontProperties(
                    family=[_font_family(filename), "DejaVu Sans"],
                    size=text.get_fontsize(),
                )
            )


@lru_cache(maxsize=1)
def _hindi_font_css():
    data = base64.b64encode(
        (_FONTS / "NotoSansDevanagari-Regular.ttf").read_bytes()
    ).decode("ascii")
    return (
        "@font-face{font-family:GWDevanagari;src:url(data:font/ttf;base64,"
        + data
        + ") format('truetype');}"
    )


def browser_svg(fig):
    """Export real SVG text so the browser handles Arabic shaping and bidi.

    Uses only Python's standard library and the existing Matplotlib dependency.
    No reversed strings, presentation-form substitution or scripts. Hindi uses
    a bundled OFL font embedded in the SVG, with no remote font request.
    Switching direction also swaps start/end anchors to retain physical label
    alignment (especially left-aligned legend labels beside their swatches).
    """
    prepare_fonts(fig)
    with _SVG_LOCK, rc_context({"svg.fonttype": "none"}):
        buffer = StringIO()
        fig.savefig(buffer, format="svg")
        root = ET.fromstring(buffer.getvalue())
        ET.register_namespace("", _SVG_NS)
        ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        if any(_HINDI.search(text.get_text()) for text in fig.findobj(Text)):
            ET.SubElement(root, f"{{{_SVG_NS}}}style").text = _hindi_font_css()
        for node in root.iter(f"{{{_SVG_NS}}}text"):
            if _HINDI.search("".join(node.itertext())):
                node.set(
                    "style",
                    node.get("style", "")
                    + ";font-family:GWDevanagari,'Noto Sans Devanagari',sans-serif",
                )
                node.set("lang", "hi")
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
            node.set(
                "lang",
                "fa" if re.search("[پچژگکۍی]", "".join(node.itertext())) else "ar",
            )
            if node.text:
                # Keep percentages and value/unit groups together in LTR order
                # inside RTL labels. The browser handles Unicode isolates.
                node.text = re.sub(
                    r"≈?\d+(?:[.,]\d+)*(?:%|\s+(?:m³/d|kg/m³|km²|m³|m²|mL|m\b))",
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
    fig, ax = axes((7, 5.8))
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
        bbox_to_anchor=(0.5, -0.02),
        frameon=False,
        fontsize=13,
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
    fig, ax = axes((8, 4.5))
    ax.set(xlim=(0, 7), ylim=(-0.15, 3.15), aspect="equal")
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
        loc="upper left",
        bbox_to_anchor=(0.64, 0.94),
        frameon=False,
        fontsize=12,
    )
    # Results belong to the same visual object as the volume comparison.
    # Native Streamlit text equivalents remain in the details expander.
    for y, label, value, gid in [
        (0.58, t("pore_volume"), f"{pore:g} mL", "cup_pore_result"),
        (
            0.29,
            t("porosity_value"),
            f"{porosity_value * 100:.1f}%",
            "cup_porosity_result",
        ),
    ]:
        ax.text(
            0.67,
            y,
            plot_text(label),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=12,
            color=INK,
        )
        ax.text(
            0.67,
            y - 0.10,
            value,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=18,
            weight="bold",
            color=BLUE,
            gid=gid,
        )
    return fig


def cup_step(step):
    """Three schematic experiment panels; captions are native translated text.

    The dry and wet views share one contacting grain arrangement. Adding
    water fills its existing spaces without changing the sample height.
    The drawings are procedural illustrations, not measured porosity samples.
    """
    if step not in (1, 2, 3):
        raise ValueError("Cup experiment step must be 1, 2 or 3.")
    fig, ax = axes((3.6, 3.7))
    ax.set(xlim=(0, 3.6), ylim=(-0.2, 3.7), aspect="equal")
    ax.axis("off")
    if step == 3:
        ax.add_patch(
            Rectangle(
                (0.55, 0.2), 2.5, 3.0, facecolor="#F7FAFB", edgecolor=INK, linewidth=2
            )
        )
        ax.add_patch(Rectangle((1.25, 3.0), 1.1, 0.35, facecolor=INK, edgecolor="none"))
        # Colored recording lines and a percentage mark indicate comparing
        # the measured water and total volumes; the caption states the method.
        for y, color in [(2.45, SAND), (1.95, BLUE)]:
            ax.plot([0.9, 2.65], [y, y], color=color, lw=7, solid_capstyle="round")
        ax.text(
            1.8,
            0.85,
            "%",
            ha="center",
            va="center",
            fontsize=45,
            weight="bold",
            color=INK,
        )
        return fig
    if step == 2:
        ax.add_patch(
            Rectangle((0.3, 0), 2.4, 2.4, facecolor="#B9DFEA", edgecolor="none")
        )
    for row in range(6):
        for column in range(4):
            ax.add_patch(
                Ellipse(
                    (0.6 + column * 0.6, 0.2 + row * 0.4),
                    0.6,
                    0.4,
                    facecolor=SAND,
                    edgecolor="#8C7248",
                    lw=1,
                )
            )
    ax.plot([0.3, 0.3, 2.7, 2.7], [2.6, 0, 0, 2.6], color=INK, lw=2.5)
    ax.plot([0.1, 2.9], [2.4, 2.4], color=INK, ls="--", lw=1.3)
    for y in [0.4, 0.8, 1.2, 1.6, 2.0]:
        ax.plot([0.3, 0.47], [y, y], color=INK, lw=1.2)
    if step == 1:
        ax.annotate(
            "",
            xy=(2.8, 2.4),
            xytext=(3.3, 3.1),
            arrowprops={"arrowstyle": "-|>", "color": ORANGE, "lw": 2},
        )
    else:
        ax.add_patch(
            Polygon(
                [(2.6, 3.55), (3.3, 3.3), (3.0, 2.8), (2.4, 3.05)],
                facecolor="#B9DFEA",
                edgecolor=INK,
                lw=1.5,
            )
        )
        ax.annotate(
            "",
            xy=(2.05, 2.45),
            xytext=(2.4, 3.05),
            arrowprops={"arrowstyle": "-|>", "color": BLUE, "lw": 2.3},
        )
    return fig


def beach(x_hole, depth, reveal, t):
    fig, ax = axes((8, 4.3))
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
    ax.text(
        -5,
        -0.065,
        plot_text(t("sea_label")),
        ha="center",
        va="center",
        fontsize=13,
        color=INK,
    )
    # Keep the material label clear of the two new inland intermediate holes.
    beach_label_x, beach_label_y = (9, 0.07) if 11 <= x_hole <= 16.5 else (15, 0.16)
    ax.text(
        beach_label_x,
        beach_label_y,
        plot_text(t("sandy_beach")),
        ha="center",
        fontsize=13,
        color=INK,
    )
    if reveal:
        ax.text(
            13, -0.39, plot_text(t("groundwater")), ha="center", fontsize=13, color=INK
        )
    # Original schematic boat: horizontal/vertical dimensions are decorative.
    ax.add_patch(
        Polygon(
            [(-6.5, 0.025), (-3.8, 0.025), (-4.3, -0.015), (-6, -0.015)],
            color="#6B6571",
        )
    )
    ax.plot([-5.2, -5.2], [0.025, 0.39], color=INK, lw=1.2)
    ax.add_patch(
        Polygon(
            [(-5.3, 0.36), (-5.3, 0.08), (-6.35, 0.08)],
            facecolor="white",
            edgecolor=BLUE,
            lw=1,
        )
    )
    ax.add_patch(
        Polygon(
            [(-5.05, 0.30), (-5.05, 0.08), (-4, 0.08)],
            facecolor="#F4D39A",
            edgecolor=ORANGE,
            lw=1,
        )
    )
    ux = 21
    ug = BEACH_GROUND_SLOPE * ux
    ax.plot([ux, ux], [ug, ug + 0.24], color="#8C7248", lw=1.6)
    ax.add_patch(
        Polygon(
            [(ux - 1.6, ug + 0.18), (ux, ug + 0.31), (ux + 1.6, ug + 0.18)],
            facecolor="#DC886A",
            edgecolor="#A95C47",
            lw=1,
        )
    )
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
        fontsize=13,
        arrowprops={"arrowstyle": "->", "color": INK},
    )
    ax.set(xlim=(-8, 22), ylim=(-0.58, 0.85))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=1,
        fontsize=12,
    )
    return fig


def cycle(t):
    """Selected pathway in the global water cycle; not a full water budget."""
    fig, ax = axes((9, 6.3))
    ax.set(xlim=(0, 10), ylim=(0, 5))
    ax.axis("off")
    land_x = np.array([0, 2, 4, 6, 7, 8, 10])
    land_z = np.array([2.3, 2.3, 2.05, 1.65, 1.4, 1.12, 0.75])
    ax.fill_between(land_x, 0, land_z, color="#F1E8D5")
    ax.fill_between([7, 8, 10], [1.4, 1.12, 0.75], 1.4, color="#96D6E5")
    x = np.linspace(0, 7, 281)
    head = cycle_head(x)
    ax.fill_between(x, 0, head, color="#A2D0DF")
    ax.fill_between([7, 8, 10], 0, [1.4, 1.12, 0.75], color="#A2D0DF")
    ax.plot(x, head, color=BLUE, lw=2)
    # Hydraulic divide, not an impermeable wall. The head profile is flat here.
    ax.plot([0, 0], [0, 2.5], ls="--", color=INK, lw=2, clip_on=False)
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
    arrow((4.7, 2.08), (6.8, 1.55), -0.08)
    arrow((3.5, 0.8), (7.8, 1.25), 0.1)
    arrow((0.65, 0.65), (2.6, 0.65))
    for xx, yy, key in [
        (8.2, 3.0, "evaporation"),
        (5.5, 4.65, "clouds"),
        (2.0, 3.45, "rain"),
        (1.6, 1.95, "recharge_simple"),
        (6.2, 2.55, "runoff"),
        (5.0, 0.4, "flow"),
        (8.7, 1.2, "surface_water"),
    ]:
        ax.text(
            xx,
            yy,
            plot_text(fill(t(key), width=21)),
            ha="center",
            va="center",
            fontsize=13,
            color=INK,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 3},
        )
    ax.set_ylim(-0.65, 5)
    return fig


def lens(peak_head, t, pumping=0.0, pumping_scenario=False):
    """Fixed-scale centerline section of the circular island (core.coastal)."""
    from core.coastal import ISLAND, island_profile, freshwater_volume

    radius = ISLAND.radius_m
    r = np.unique(np.r_[0, np.geomspace(ISLAND.well_radius_m, radius, 450)])
    x = np.r_[-r[:0:-1], r]
    h, z = island_profile(x, peak_head, pumping)
    natural_h, natural_z = island_profile(x, peak_head)
    ground = island_surface(x, radius)
    fig, ax = axes((10, 5.6))
    bottom = -61
    ax.fill_between(
        x, bottom, -z, color="#689FC8", hatch="//", edgecolor="#5589B1", linewidth=0
    )
    ax.fill_between(x, -z, h, color="#B8E5EB")
    ax.fill_between(x, h, ground, color="#EBDDCA")
    for lo, hi in [(-1.3 * radius, -radius), (radius, 1.3 * radius)]:
        sx = np.linspace(lo, hi, 100)
        bed = -0.04 * (np.abs(sx) - radius)
        ax.fill_between(
            sx,
            bottom,
            bed,
            color="#689FC8",
            hatch="//",
            edgecolor="#5589B1",
            linewidth=0,
        )
        ax.fill_between(sx, bed, 0, color="#8DC7E4")
        ax.plot(sx, bed, color="#806B4A", lw=1.5)
    ax.axhline(0, color=BLUE, ls=":", lw=1.2, label=plot_text(t("sea")))
    ax.plot(x, ground, color="#806B4A", lw=2, label=plot_text(t("land_surface")))
    if pumping_scenario:
        ax.plot(
            x,
            natural_h,
            color="#75818A",
            ls="--",
            lw=1.4,
            label=plot_text(t("without_pumping")),
        )
        ax.plot(x, -natural_z, color="#75818A", ls="--", lw=1.4)
    ax.plot(x, h, color="#16888F", lw=2.3, label=plot_text(t("water_table")))
    ax.plot(x, -z, color="#215780", lw=2.3, label=plot_text(t("interface")))
    # Natural reference values move into a compact lower-right legend. The
    # lower margin is reserved below the deepest interface (40 m), so this
    # panel never hides the fresh/saltwater boundary. Pumping comparisons
    # remain available as native Streamlit metrics below the figure.
    values = (
        plot_text(t("without_pumping"))
        + "\n"
        + plot_text(t("legend_head"))
        + f": {peak_head:.1f} m\n"
        + plot_text(t("legend_depth"))
        + f": {peak_head * ISLAND.alpha:.1f} m\n"
        + plot_text(t("legend_volume"))
        + f": {freshwater_volume(peak_head):,.0f} m³"
    )
    ax.text(
        0.98,
        0.025,
        values,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=11,
        linespacing=1.2,
        color=INK,
        bbox={
            "facecolor": "white",
            "edgecolor": "#9DB8C7",
            "alpha": 0.96,
            "boxstyle": "round,pad=0.45",
        },
        gid="lens_reference_values",
    )
    ax.text(
        0.98,
        0.97,
        plot_text(t("island_area")) + "\n1 km²",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=13,
        color=INK,
    )
    ax.annotate(
        plot_text(t("freshwater")),
        xy=(
            -0.5 * radius,
            -float(island_profile([0.5 * radius], peak_head, pumping)[1][0]) / 2,
        ),
        xytext=(-0.9 * radius, -19),
        ha="center",
        fontsize=13,
        color=INK,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
        arrowprops={"arrowstyle": "->", "color": INK},
    )
    ax.text(
        -0.75 * radius,
        -53,
        plot_text(t("saltwater")),
        ha="center",
        fontsize=13,
        color="#123753",
    )
    if pumping_scenario:
        # A symbolic well, not a representation of screen depth or construction.
        ax.plot([0, 0], [5, -1.6], color=INK, lw=4)
        ax.annotate(
            "",
            xy=(0.22 * radius, 7),
            xytext=(0, 5),
            arrowprops={"arrowstyle": "-|>", "color": ORANGE, "lw": 2.5},
        )
        ax.text(
            0,
            9,
            plot_text(t("pumping_well")) + f" · {pumping:.2f} m³/d",
            ha="center",
            fontsize=13,
            color=INK,
        )
    else:
        ax.annotate(
            plot_text(t("land_surface")),
            xy=(0, 3),
            xytext=(0, 9),
            ha="center",
            fontsize=13,
            arrowprops={"arrowstyle": "->", "color": INK},
        )
    ax.set(xlim=(-1.3 * radius, 1.3 * radius), ylim=(bottom, 18))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=2,
        fontsize=12,
    )
    return fig


def head_detail(peak_head, t):
    """Enlarged natural water-table detail, in metres, with the lens colours.

    This shows the left half of the same circular island, from shore to centre.
    The interface lies below the cropped view. Fixed limits keep slider changes
    visually comparable; no change is made to the regional model.
    """
    from core.coastal import ISLAND, island_profile

    fig, ax = axes((4.6, 2.9))
    distance = np.linspace(0, 1, 180)
    radius = (1 - distance) * ISLAND.radius_m
    head, _ = island_profile(radius, peak_head)
    ground = island_surface(radius, ISLAND.radius_m)
    ax.fill_between(distance, -0.5, head, color="#B8E5EB")
    ax.fill_between(distance, head, ground, color="#EBDDCA")
    ax.fill_between([-0.3, 0], -0.5, 0, color="#8DC7E4")
    ax.plot(distance, ground, color="#806B4A", lw=2)
    ax.plot(distance, head, color="#16888F", lw=2.3, gid="detail_water_table")
    ax.axhline(0, color=BLUE, ls=":", lw=1.2, gid="detail_sea_level")
    ax.plot([1, 1.12], [peak_head, peak_head], color="#16888F", ls="--", lw=1)
    ax.annotate(
        "",
        xy=(1.1, peak_head),
        xytext=(1.1, 0),
        arrowprops={
            "arrowstyle": "<->",
            "color": "#16888F",
            "lw": 1.7,
            "shrinkA": 0,
            "shrinkB": 0,
            "mutation_scale": min(10, max(3, 30 * peak_head)),
        },
    )
    ax.text(
        1.15,
        max(0.22, peak_head / 2),
        f"h = {peak_head:.1f} m",
        fontsize=12,
        ha="left",
        va="center",
        color="#16888F",
        gid="detail_head_value",
    )
    ax.text(
        0.65, 3.35, plot_text(t("land_surface")), fontsize=11, ha="center", color=INK
    )
    ax.annotate(
        plot_text(fill(t("water_table"), 22)),
        xy=(0.65, float(island_profile(0.35 * ISLAND.radius_m, peak_head)[0])),
        xytext=(0.38, 1.65),
        fontsize=11,
        ha="center",
        color="#16888F",
        arrowprops={"arrowstyle": "->", "color": "#16888F", "lw": 1},
    )
    ax.text(-0.15, -0.32, plot_text(t("sea")), ha="center", fontsize=10, color=INK)
    ax.set(xlim=(-0.45, 1.8), ylim=(-0.6, 3.8))
    ax.axis("off")
    return fig


def density_principle(t, head_above_sea=0.8):
    """Coastal pressure-balance schematic with connected comparison columns.

    The slider specifies h at the comparison column, not at the inland edge.
    The below-sea geometry uses z = 40 h for 1000/1025 kg/m³ water densities.
    Positive elevations are magnified eightfold so the small freshwater head
    is readable; the translated caption makes this unequal scaling explicit.
    The U-shaped columns are a conceptual pressure comparison, not pumping
    infrastructure. The separate island/pumping calculation is unchanged.
    """
    if not np.isfinite(head_above_sea) or not 0.1 <= head_above_sea <= 1.0:
        raise ValueError("Freshwater head must be between 0.1 and 1.0 m.")
    fig, ax = axes((10, 5.5))
    coast, inland, bottom = 3.4, 10.0, -60.0
    salt_x, fresh_x = 1.2, 7.2
    head_scale = 8.0
    saline, fresh = "#689FC8", "#B8E5EB"
    land_x = np.unique(np.r_[np.linspace(coast, inland, 301), fresh_x])
    sea_x = np.linspace(0, coast, 181)

    def freshwater_head(x):
        # Prescribed smooth coastal shape, not a recharge/flow solution.
        u = (np.asarray(x) - coast) / (inland - coast)
        column_u = (fresh_x - coast) / (inland - coast)
        return head_above_sea * (1 - np.exp(-u / 0.7)) / (1 - np.exp(-column_u / 0.7))

    head = freshwater_head(land_x)
    water_table = head_scale * head
    interface = -40 * head
    land = 14.5 * (1 - np.exp(-(land_x - coast))) + 0.3 * (land_x - coast)
    seabed = -31 * ((coast - sea_x) / coast) ** 0.85

    # Continuous sea, seabed and shore; fresh water occupies connected pores
    # beneath the water table. The sharp interface is an idealisation.
    ax.fill_between(sea_x, bottom, seabed, color=saline)
    ax.fill_between(sea_x, seabed, 0, color="#8DC7E4")
    ax.fill_between(land_x, bottom, interface, color=saline)
    ax.fill_between(land_x, interface, water_table, color=fresh)
    ax.fill_between(land_x, water_table, land, color="#EBDDCA")
    ax.plot(sea_x, seabed, color="#9A8058", lw=2.3)
    ax.plot(
        land_x,
        land,
        color="#9A8058",
        lw=2.3,
        label=plot_text(t("land_surface")),
        gid="density_land",
    )
    ax.plot(sea_x, np.zeros_like(sea_x), color=BLUE, lw=2.3)
    ax.plot(
        [0, inland],
        [0, 0],
        color=INK,
        ls=":",
        lw=1.3,
        label=plot_text(t("sea")),
        gid="density_sea_datum",
    )
    ax.plot(
        land_x,
        water_table,
        color=BLUE,
        lw=2.5,
        label=plot_text(t("water_table")),
        gid="density_water_table",
    )
    ax.plot(
        land_x,
        interface,
        color="#344E78",
        lw=2.2,
        label=plot_text(t("interface")),
        gid="density_interface",
    )

    # Two open columns share the same comparison depth. At the right-hand
    # interface point, salt water of depth z balances fresh water of depth z+h.
    local_head = float(freshwater_head(fresh_x))
    top, foot = head_scale * local_head, -40 * local_head
    tube_x, tube_y = [salt_x, salt_x, fresh_x, fresh_x], [1.8, foot, foot, top + 1.8]
    ax.plot(tube_x, tube_y, color=INK, lw=12, solid_joinstyle="round", zorder=5)
    ax.plot(tube_x, tube_y, color="white", lw=8.5, solid_joinstyle="round", zorder=6)
    ax.plot(
        [salt_x, salt_x, fresh_x],
        [0, foot, foot],
        color=saline,
        lw=5.5,
        solid_joinstyle="round",
        solid_capstyle="butt",
        zorder=7,
        gid="density_salt_column",
    )
    ax.plot(
        [fresh_x, fresh_x],
        [foot, top],
        color=BLUE,
        lw=5.5,
        solid_capstyle="butt",
        zorder=7,
        gid="density_fresh_column",
    )
    ax.plot(fresh_x, foot, "o", color=INK, ms=5, zorder=8)

    # Dashed guides and dimension arrows refer to this one inland location,
    # not to the maximum head at the right edge of the coastal section.
    dimension_x = 9.65
    for level in [top, foot]:
        ax.plot([fresh_x, dimension_x], [level, level], color=INK, ls="--", lw=1)
    for y0, y1, symbol in [(0, top, "h"), (foot, 0, "z")]:
        ax.annotate(
            "",
            xy=(dimension_x, y1),
            xytext=(dimension_x, y0),
            arrowprops={
                "arrowstyle": "<->",
                "color": INK,
                "lw": 1.5,
                "shrinkA": 0,
                "shrinkB": 0,
                "mutation_scale": min(10, max(2, 2 * (y1 - y0))),
            },
        )
        ax.text(
            dimension_x + 0.15,
            max(2.4, (y0 + y1) / 2) if symbol == "h" else (y0 + y1) / 2,
            symbol,
            fontsize=16,
            ha="left",
            va="center",
            color=INK,
        )
    fresh_label = plot_text(fill(t("freshwater"), 17)) + "\nρf = 1000 kg/m³"
    label_x = 8.35
    label_head = float(freshwater_head(label_x))
    label_mid = (head_scale - 40) * label_head / 2
    if head_above_sea >= 0.4:
        ax.text(
            label_x,
            label_mid,
            fresh_label,
            ha="center",
            va="center",
            fontsize=13,
            color=INK,
        )
    else:
        # A thin freshwater wedge needs an explicit callout: the label must
        # not appear to identify the saltwater underneath it as freshwater.
        ax.annotate(
            fresh_label,
            xy=(label_x, label_mid),
            xytext=(label_x, -19),
            ha="center",
            va="center",
            fontsize=13,
            color=INK,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.95},
            arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.3},
        )
    ax.text(
        2.5,
        -51,
        plot_text(fill(t("saltwater"), 23)) + "\nρs = 1025 kg/m³",
        ha="center",
        va="center",
        fontsize=13,
        color=INK,
    )
    ax.text(1.7, 6.5, plot_text(t("sea_label")), ha="center", fontsize=14, color=INK)
    ax.set(xlim=(-0.1, 10.3), ylim=(bottom, 20.5))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=2,
        fontsize=12,
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

    fig, ax = axes((10, 4.5))
    x = np.linspace(0, RIVER_BANK, 401)
    ground = river_ground(x)
    head = river_head(x, regime)
    bed, base = -0.8, -1.5

    # Continuous bank/bed profile, with surface water as the common datum.
    sx = np.linspace(RIVER_BANK, 100, 161)
    riverbed = bed * (1 - np.exp(-(sx - RIVER_BANK) / 4))
    ax.fill_between(x, base, ground, color="#EBDDCA")
    ax.fill_between(sx, base, riverbed, color="#EBDDCA")
    ax.fill_between(sx, riverbed, 0, color="#8DC7E4")
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
        ax.fill_between(sx, base, riverbed, color="#A2D0DF")
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
    ax.fill_between(x, ground - 0.09, ground, color="#B6A080", alpha=0.8, zorder=3)
    ax.plot(x, ground, color="#718557", lw=2, label=plot_text(t("land_surface")))
    for tree_x, scale in [(10, 1.05), (39, 1.0), (61, 0.95)]:
        # New intermediate stops must not put a decorative tree over the hole.
        if abs(tree_x - x_hole) < 3.5:
            tree_x -= 4
        _pine_tree(ax, tree_x, float(river_ground(tree_x)), scale)
    ax.plot(sx, riverbed, color="#93743F", lw=2)
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
        xytext=(x_hole, 2.10),
        ha="center",
        fontsize=13,
        arrowprops={"arrowstyle": "->", "color": INK},
    )
    ax.text(
        90,
        0.28,
        plot_text(fill(t("river_label"), 19, break_long_words=False)),
        ha="center",
        fontsize=13,
        color=INK,
    )
    aquifer_label_x = 48 if x_hole < 35 else 23
    soil_label_x = 48 if x_hole > 60 else 70
    ax.text(
        aquifer_label_x,
        -0.65,
        plot_text(fill(t("sandy_aquifer"), 22, break_long_words=False)),
        ha="center",
        fontsize=13,
        color=INK,
    )
    ax.annotate(
        plot_text(t("soil")),
        xy=(soil_label_x + 4, float(river_ground(soil_label_x + 4)) - 0.04),
        xytext=(soil_label_x, 1.65),
        fontsize=13,
        ha="center",
        arrowprops={"arrowstyle": "-", "color": INK},
        color=INK,
    )
    # Mirror only the drawing: surface water left, inland right, as at the beach.
    # The original coordinates and all observation/head calculations are retained.
    ax.set(xlim=(100, 0), ylim=(base, 2.4))
    ax.axis("off")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        frameon=False,
        ncol=2,
        fontsize=12,
    )
    return fig
