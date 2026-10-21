"""Start with the whole water cycle before focusing on its underground part."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import heading, show, next_page, source_links, expander, responsive_image
from core.figures import cycle
from core.sources import REVIEW_URL


def review_notice():
    """The development notice belongs only on the opening page."""
    with expander(tr("draft_notice")):
        md("draft_notice")
        st.link_button(tr("review_module"), REVIEW_URL)


heading("home", introduction=review_notice)
md("home")
st.subheader(tr("water_cycle_heading"), divider="blue")
md("home_cycle")
poster = ROOT / "assets/images" / f"water_cycle_{st.session_state.language}.jpg"
if poster.is_file():
    responsive_image(str(poster), caption=tr("cycle_title") + " · USGS")
else:
    st.info(tr("figure_placeholder"))
    show(cycle(tr))
    st.caption(tr("cycle_caption"))
st.link_button(
    tr("poster_link"), "https://www.usgs.gov/water-science-school/water-cycle-diagrams"
)
source_links("S1", "S13", "S14")
next_page("importance")
with expander(tr("facilitator")):
    md("facilitator")
