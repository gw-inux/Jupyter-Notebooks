"""The Arabic output must retain real text and need no shaping packages."""

import base64
import xml.etree.ElementTree as ET
import pytest
from matplotlib.figure import Figure
from streamlit.testing.v1 import AppTest
from core import figures as f
from core.i18n import TEXT
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://www.w3.org/2000/svg"}


@pytest.mark.parametrize(
    "factory",
    [
        lambda t: f.water_store(t),
        lambda t: f.pores(False, t),
        lambda t: f.sample_cup(400, 240, t),
        lambda t: f.beach(3, 0.08, True, t),
        lambda t: f.cycle(t),
        lambda t: f.lens(0.7, t),
        lambda t: f.river(24, "river_deep", "losing", True, t),
    ],
)
def test_arabic_diagrams_are_live_unicode_svg(factory):
    fig = factory(lambda k: TEXT[k]["ar"])
    assert f.needs_browser_text(fig)
    root = ET.fromstring(f.browser_svg(fig))
    assert root.tag == "{" + NS["s"] + "}svg"
    assert root.get("viewBox")
    labels = root.findall(".//s:text", NS)
    arabic = [
        node
        for node in labels
        if any("\u0600" <= c <= "\u06ff" for c in "".join(node.itertext()))
    ]
    assert arabic
    for node in arabic:
        assert "direction: rtl" in node.get("style", "")
        assert "unicode-bidi: embed" in node.get("style", "")
        # Labels are kept in logical order, without pre-shaped presentation forms.
        assert not any("\ufb50" <= c <= "\ufeff" for c in "".join(node.itertext()))
    assert not root.findall(".//s:script", NS)


def test_rtl_anchor_conversion_preserves_physical_alignment():
    fig = Figure()
    ax = fig.subplots()
    for x, align in [(0.2, "left"), (0.5, "center"), (0.8, "right")]:
        ax.text(x, 0.5, "المياه الجوفية", ha=align)
    root = ET.fromstring(f.browser_svg(fig))
    styles = [
        n.get("style")
        for n in root.findall(".//s:text", NS)
        if n.text == "المياه الجوفية"
    ]
    assert len(styles) == 3
    for style, anchor in zip(styles, ["end", "middle", "start"]):
        assert "text-anchor: " + anchor in style
    assert not f.needs_browser_text(f.cycle(lambda k: TEXT[k]["en"]))


def test_numeric_groups_keep_their_left_to_right_order():
    svg = f.browser_svg(f.water_store(lambda k: TEXT[k]["ar"]))
    root = ET.fromstring(svg)
    labels = ["".join(node.itertext()) for node in root.findall(".//s:text", NS)]
    assert any("\u2066≈99%\u2069" in label for label in labels)
    assert any("\u2066≈1%\u2069" in label for label in labels)
    for lang in ["ar", "fa"]:
        pumped = f.browser_svg(f.lens(0.8, lambda k: TEXT[k][lang], 29.5, True))
        assert "\u206629.50 m³/d\u2069" in pumped


def test_streamlit_serves_real_svg_without_rasterising_arabic():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.session_state["language"] = "ar"
    at.run()
    at.switch_page("content/beach.py").run()
    assert not at.exception
    # Cycle, beach and river use live SVG image data, not PNG.
    urls = [im.url for element in at.get("imgs") for im in element.proto.imgs]
    assert len(urls) == 3
    for url in urls:
        assert url.startswith("data:image/svg+xml;base64,")
        root = ET.fromstring(base64.b64decode(url.split(",", 1)[1]))
        assert any(node.get("lang") == "ar" for node in root.findall(".//s:text", NS))
