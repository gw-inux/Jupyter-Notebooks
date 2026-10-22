"""Predict the size of the liquid freshwater store, then interpret it."""

import streamlit as st
from core.i18n import ROOT, tr, md
from core.ui import (
    heading,
    show,
    source_links,
    quiz_group,
    next_page,
    expander,
    responsive_image,
)
from core.figures import water_store

heading("importance")
st.subheader(tr("freshwater_heading"), divider="blue")
md("importance")
guess = st.slider(tr("guess"), 0, 100, 50, 5, key="freshwater_guess", format="%d%%")
# A dedicated container keeps this action centered even when columns stack on
# phones. The scoped amber style distinguishes discovery from teal navigation.
st.markdown(
    """<style>
.st-key-reveal_action [data-testid="stButton"] {display:flex; justify-content:center;}
.st-key-reveal_action .st-key-reveal_store {margin-inline:auto; max-width:100%;}
.st-key-reveal_action button {
 background:#F3C969; color:#263238; border:2px solid #A66A00;
 font-weight:700; padding:.6rem 1.1rem;
}
.st-key-reveal_action button:hover {background:#EAB64A; color:#263238; border-color:#805100;}
.st-key-reveal_action button:focus-visible {outline:3px solid #16778A; outline-offset:3px;}
</style>""",
    unsafe_allow_html=True,
)
with st.container(key="reveal_action"):
    if st.button("💡 " + tr("reveal"), key="reveal_store"):
        st.session_state["store_revealed"] = True
        st.session_state["revealed_guess"] = guess
if st.session_state.get("store_revealed", False):
    # Feedback refers to the prediction submitted with the reveal, not a slider
    # value reset by page cleanup. Seventy percent begins the encouraging band.
    submitted_guess = st.session_state.get("revealed_guess", guess)
    feedback = tr("guess_close" if submitted_guess >= 70 else "guess_far")
    st.info("**" + feedback + "** " + tr("scroll_result"))
    show(water_store(tr))
    st.caption(tr("waffle"))
    st.subheader(tr("meaning_heading"), divider="blue")
    md("importance_reveal")
    # Keep the prediction first; the wider inventory uses a different denominator.
    with expander(tr("distribution_heading")):
        md("water_distribution")
        responsive_image(
            str(ROOT / "assets/images/water_distribution_usgs.png"),
            caption=tr("distribution_credit"),
        )
    quiz_group("stores", "role", "limits")
source_links("S1", "S3", "S2", "S4")
next_page("pores")
