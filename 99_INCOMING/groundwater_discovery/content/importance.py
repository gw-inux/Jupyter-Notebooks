"""Predict the size of the liquid freshwater store, then interpret it."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import heading, show, source_links, quiz_group, next_page, expander
from core.figures import water_store

heading("importance")
st.subheader(tr("freshwater_heading"), divider="blue")
md("importance")
st.slider(tr("guess"), 0, 100, 50, 5, key="freshwater_guess", format="%d%%")
if st.button(tr("reveal"), key="reveal_store"):
    st.session_state["store_revealed"] = True
if st.session_state.get("store_revealed", False):
    show(water_store(tr))
    st.caption(tr("waffle"))
    st.subheader(tr("meaning_heading"), divider="blue")
    md("importance_reveal")
    # Keep the prediction first; the wider inventory uses a different denominator.
    with expander(tr("distribution_heading")):
        md("water_distribution")
        st.image(
            str(ROOT / "assets/images/water_distribution_usgs.png"),
            caption=tr("distribution_credit"),
            width=620,
        )
    quiz_group("stores", "role", "limits")
source_links("S1", "S2", "S14", "S18")
next_page("pores")
