"""Product identity and developer details, matching the related GWP modules."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import heading, centered_link, responsive_image
from core.sources import REVIEW_URL

heading("about", learning=False)
st.subheader(tr("about_description"), divider="blue")
md("about_description")
_, center, _ = st.columns([1, 2, 1])
with center:
    responsive_image(str(ROOT / "assets/images/gwp_logo.png"))
centered_link("The Groundwater Project ↗", "https://gw-project.org/", "gwp")
st.subheader(tr("about_development"), divider="blue")
md("about_development")
st.subheader(tr("about_author"), divider="blue")
photo, biography = st.columns([1, 3])
with photo:
    responsive_image(
        str(ROOT / "assets/images/thomasreimann.png"), caption="Thomas Reimann"
    )
with biography:
    md("about_author")
st.subheader(tr("about_contact"), divider="blue")
md("about_contact")
centered_link(tr("review_module"), REVIEW_URL, "review")
