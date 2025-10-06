import streamlit as st
from pathlib import Path

def get_param(name: str):
    val = st.query_params.get(name)
    return val

def load_doc_text(doc_id: str) -> str:
    p = DOCS.get(doc_id)
    if not p:
        return f"**Unknown doc id:** `{doc_id}`"
    try:
        if p.is_file():
            return p.read_text(encoding="utf-8")
        else:
            return f"**Document not found:** `{p}`"
    except Exception as e:
        return f"**Error reading `{p}`:** {e}"
        
# ---------- document registry ----------
DOCS = {
    "ghb_intro": Path("docs/ghb_intro.md"),
    "example1":  Path("docs/example1.md"),
    "example2":  Path("docs/example2.md"),
}

FALLBACK_MD = """# Instructions

This is a minimal example.

**Steps:**
1. Define your general head boundary.
2. Specify conductance and reference head.
3. Run the model and interpret results.
"""

# ---------- decide mode BEFORE the first Streamlit call ----------
view = get_param("view")
doc  = get_param("doc")
is_doc_view = (view == "doc") and (doc in DOCS)

# Set page config ONCE and FIRST
title  = f"Instructions – {doc}" if is_doc_view else "Pop-out Example"
layout = "wide" if is_doc_view else "centered"
st.set_page_config(page_title=title, layout=layout)

# ---------- DOC VIEWER MODE: only the markdown ----------
if is_doc_view:
    st.markdown(load_doc_text(doc))
    st.stop()

# ---------- NORMAL APP MODE ----------
st.title("Demo: Pop-out Instructions (Markdown-only tab)")

with st.expander("📘 Instructions (GHB)"):
    st.link_button("🗔 Open in new tab", url="?view=doc&doc=ghb_intro")
    st.markdown(load_doc_text("ghb_intro") or FALLBACK_MD)

with st.expander("📘 Example 1"):
    st.link_button("🗔 Open in new tab", url="?view=doc&doc=example1")
    st.markdown(load_doc_text("example1"))

with st.expander("📘 Example 2"):
    st.link_button("🗔 Open in new tab", url="?view=doc&doc=example2")
    st.markdown(load_doc_text("example2"))
