from pathlib import Path
import re

# Make docs/ relative to THIS file, not the working directory
DOCS_DIR = (Path(__file__).parent / "docs").resolve()
DOCS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED = re.compile(r"^[A-Za-z0-9_\-]+\.md$")

def read_md(doc_name: str) -> str:
    if not doc_name or not ALLOWED.match(doc_name):
        return f"**Invalid document name:** `{doc_name}`"
    p = (DOCS_DIR / doc_name).resolve()
    try:
        if DOCS_DIR not in p.parents:
            return f"**Access denied:** `{doc_name}`"
        if not p.exists() or not p.is_file():
            return f"**Document not found:** `{doc_name}`"
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"**Error reading `{doc_name}`:** {e}"
