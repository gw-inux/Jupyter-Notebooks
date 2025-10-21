import json
import re
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET
import uuid
import streamlit as st

# -------------------------------
# QTI namespaces and registration
# -------------------------------
NS_QTI   = "http://www.imsglobal.org/xsd/imsqti_v2p1"
NS_IMSCP = "http://www.imsglobal.org/xsd/imscp_v1p1"
NS_XSI   = "http://www.w3.org/2001/XMLSchema-instance"
ET.register_namespace('',   NS_QTI)
ET.register_namespace('xsi', NS_XSI)

# -------------------------------
# Text transforms
# -------------------------------
_opt_prefix = re.compile(r"^\s*[A-Z]\)\s+")
_inline_math = re.compile(r"\$(?!\$)(.+?)\$(?!\$)")  # convert single-$ inline math to $$...$$

def to_double_dollar_math(s: str) -> str:
    # Convert $...$ to $$...$$, leave $$...$$ as-is
    return _inline_math.sub(r"$$\1$$", s)

def clean_option_text(s: str, strip_prefixes=True, convert_math=True) -> str:
    text = s
    if strip_prefixes:
        text = _opt_prefix.sub("", text)
    if convert_math:
        text = to_double_dollar_math(text)
    return text

def clean_general_text(s: str, convert_math=True) -> str:
    return to_double_dollar_math(s) if convert_math else s

# -------------------------------
# QTI builders
# -------------------------------
def make_item_xml(
    title: str,
    stem: str,
    choices: list[tuple[str, str]],          # [(choice_id, text), ...]
    correct_ids: list[str],
    success_text: str,
    error_text: str,
    shuffle: bool = True
):
    """
    Build a QTI 2.1 assessmentItem that matches the LMS sample wiring:
    - Multiple-response (cardinality="multiple", maxChoices="0")
    - FEEDBACKBASIC set in grading branch, then FEEDBACKMODAL selected after
    - modalFeedback nodes for correct/incorrect
    """
    item_id = f"item-{uuid.uuid4()}"
    item = ET.Element(ET.QName(NS_QTI, "assessmentItem"), {
        ET.QName(NS_XSI, "schemaLocation"):
            "http://www.imsglobal.org/xsd/imsqti_v2p1 "
            "http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p1.xsd",
        "identifier": item_id,
        "title": title,
        "adaptive": "false",
        "timeDependent": "false"
    })

    # responseDeclaration
    rd = ET.SubElement(item, ET.QName(NS_QTI, "responseDeclaration"),
                       {"identifier": "RESPONSE_1", "cardinality": "multiple", "baseType": "identifier"})
    cr = ET.SubElement(rd, ET.QName(NS_QTI, "correctResponse"))
    for cid in correct_ids:
        v = ET.SubElement(cr, ET.QName(NS_QTI, "value"))
        v.text = cid

    # outcomes
    for ident, baseType, default in [
        ("SCORE", "float", "0"),
        ("MAXSCORE", "float", "1"),
        ("MINSCORE", "float", "0"),
        ("FEEDBACKBASIC", "identifier", "empty"),
    ]:
        od = ET.SubElement(item, ET.QName(NS_QTI, "outcomeDeclaration"),
                           {"identifier": ident, "cardinality": "single", "baseType": baseType})
        dv = ET.SubElement(od, ET.QName(NS_QTI, "defaultValue"))
        ET.SubElement(dv, ET.QName(NS_QTI, "value")).text = default

    ET.SubElement(item, ET.QName(NS_QTI, "outcomeDeclaration"),
                  {"identifier": "FEEDBACKMODAL", "cardinality": "multiple", "baseType": "identifier", "view": "testConstructor"})

    # itemBody
    body = ET.SubElement(item, ET.QName(NS_QTI, "itemBody"))
    ET.SubElement(body, ET.QName(NS_QTI, "p")).text = stem
    ci = ET.SubElement(body, ET.QName(NS_QTI, "choiceInteraction"),
                       {"responseIdentifier": "RESPONSE_1", "shuffle": "true" if shuffle else "false", "maxChoices": "0"})
    for cid, text in choices:
        sc = ET.SubElement(ci, ET.QName(NS_QTI, "simpleChoice"), {"identifier": cid})
        ET.SubElement(sc, ET.QName(NS_QTI, "p")).text = text

    # modalFeedback nodes
    fb_ok_id  = f"id-{uuid.uuid4()}"
    fb_err_id = f"id-{uuid.uuid4()}"
    for fid, txt in [(fb_ok_id, success_text), (fb_err_id, error_text)]:
        mf = ET.SubElement(item, ET.QName(NS_QTI, "modalFeedback"),
                           {"identifier": fid, "outcomeIdentifier": "FEEDBACKMODAL", "showHide": "show"})
        ET.SubElement(mf, ET.QName(NS_QTI, "p")).text = txt

    # responseProcessing (matches your working LMS example)
    rp = ET.SubElement(item, ET.QName(NS_QTI, "responseProcessing"))

    # 0) If empty -> FEEDBACKBASIC = empty
    rc0 = ET.SubElement(rp, ET.QName(NS_QTI, "responseCondition"))
    rif0 = ET.SubElement(rc0, ET.QName(NS_QTI, "responseIf"))
    isnull = ET.SubElement(rif0, ET.QName(NS_QTI, "isNull"))
    ET.SubElement(isnull, ET.QName(NS_QTI, "variable"), {"identifier": "RESPONSE_1"})
    act0 = ET.SubElement(rif0, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "FEEDBACKBASIC"})
    ET.SubElement(act0, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = "empty"

    # 1) Exact match -> SCORE = SCORE + MAXSCORE; FEEDBACKBASIC = correct
    rc1 = ET.SubElement(rp, ET.QName(NS_QTI, "responseCondition"))
    rif1 = ET.SubElement(rc1, ET.QName(NS_QTI, "responseIf"))
    match = ET.SubElement(rif1, ET.QName(NS_QTI, "match"))
    ET.SubElement(match, ET.QName(NS_QTI, "variable"), {"identifier": "RESPONSE_1"})
    ET.SubElement(match, ET.QName(NS_QTI, "correct"), {"identifier": "RESPONSE_1"})
    so1 = ET.SubElement(rif1, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "SCORE"})
    summ = ET.SubElement(so1, ET.QName(NS_QTI, "sum"))
    ET.SubElement(summ, ET.QName(NS_QTI, "variable"), {"identifier": "SCORE"})
    ET.SubElement(summ, ET.QName(NS_QTI, "variable"), {"identifier": "MAXSCORE"})
    so2 = ET.SubElement(rif1, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "FEEDBACKBASIC"})
    ET.SubElement(so2, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = "correct"

    # 2) Else -> SCORE = 0; FEEDBACKBASIC = incorrect
    relse = ET.SubElement(rc1, ET.QName(NS_QTI, "responseElse"))
    so3 = ET.SubElement(relse, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "SCORE"})
    ET.SubElement(so3, ET.QName(NS_QTI, "baseValue"), {"baseType": "float"}).text = "0"
    so4 = ET.SubElement(relse, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "FEEDBACKBASIC"})
    ET.SubElement(so4, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = "incorrect"

    # 3) FEEDBACKBASIC == correct -> add correct modal id
    rc2 = ET.SubElement(rp, ET.QName(NS_QTI, "responseCondition"))
    rif2 = ET.SubElement(rc2, ET.QName(NS_QTI, "responseIf"))
    match2 = ET.SubElement(rif2, ET.QName(NS_QTI, "match"))
    ET.SubElement(match2, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = "correct"
    ET.SubElement(match2, ET.QName(NS_QTI, "variable"), {"identifier": "FEEDBACKBASIC"})
    so5 = ET.SubElement(rif2, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "FEEDBACKMODAL"})
    mult_ok = ET.SubElement(so5, ET.QName(NS_QTI, "multiple"))
    ET.SubElement(mult_ok, ET.QName(NS_QTI, "variable"), {"identifier": "FEEDBACKMODAL"})
    ET.SubElement(mult_ok, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = fb_ok_id

    # 4) FEEDBACKBASIC == incorrect -> add incorrect modal id
    rc3 = ET.SubElement(rp, ET.QName(NS_QTI, "responseCondition"))
    rif3 = ET.SubElement(rc3, ET.QName(NS_QTI, "responseIf"))
    match3 = ET.SubElement(rif3, ET.QName(NS_QTI, "match"))
    ET.SubElement(match3, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = "incorrect"
    ET.SubElement(match3, ET.QName(NS_QTI, "variable"), {"identifier": "FEEDBACKBASIC"})
    so6 = ET.SubElement(rif3, ET.QName(NS_QTI, "setOutcomeValue"), {"identifier": "FEEDBACKMODAL"})
    mult_bad = ET.SubElement(so6, ET.QName(NS_QTI, "multiple"))
    ET.SubElement(mult_bad, ET.QName(NS_QTI, "variable"), {"identifier": "FEEDBACKMODAL"})
    ET.SubElement(mult_bad, ET.QName(NS_QTI, "baseValue"), {"baseType": "identifier"}).text = fb_err_id

    return item_id, item

def make_manifest_xml(item_filenames: list[str]) -> ET.Element:
    ET.register_namespace('', NS_IMSCP)
    ET.register_namespace('xsi', NS_XSI)
    manifest = ET.Element(ET.QName(NS_IMSCP, "manifest"), {
        ET.QName(NS_XSI, "schemaLocation"):
            "http://www.imsglobal.org/xsd/imscp_v1p1 "
            "http://www.imsglobal.org/xsd/imscp_v1p1.xsd "
            "http://www.imsglobal.org/xsd/imsqti_v2p1 "
            "http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p1.xsd",
        "identifier": "manifestID"
    })
    metadata = ET.SubElement(manifest, ET.QName(NS_IMSCP, "metadata"))
    ET.SubElement(metadata, "schema").text = "QTIv2.1 Package"
    ET.SubElement(metadata, "schemaversion").text = "1.0.0"
    ET.SubElement(manifest, ET.QName(NS_IMSCP, "organizations"))
    resources = ET.SubElement(manifest, ET.QName(NS_IMSCP, "resources"))
    for fname in item_filenames:
        rid = "res_" + Path(fname).stem.replace('-', '_')
        res = ET.SubElement(resources, ET.QName(NS_IMSCP, "resource"), {
            "identifier": rid,
            "type": "imsqti_item_xmlv2p1",
            "href": fname
        })
        ET.SubElement(res, ET.QName(NS_IMSCP, "file"), {"href": fname})
    return manifest

def json_to_qti_zip(
    json_bytes: bytes,
    strip_prefixes=True,
    convert_math=True,
    shuffle=True,
    item_prefix: str = "Item",
) -> bytes:
    """
    Convert a JSON (array of items) into a QTI 2.1 zip (in-memory).
    """
    items = json.loads(json_bytes.decode("utf-8"))

    buf = BytesIO()
    zf = ZipFile(buf, "w", ZIP_DEFLATED)

    item_filenames = []

    for idx, q in enumerate(items, start=1):
        # Build choices & correct set
        choices_text = list(q["options"].keys())
        choices_bools = list(q["options"].values())
        choice_ids = [f"ID_{i+1}" for i in range(len(choices_text))]
        # Apply transforms
        stem = clean_general_text(q["question"], convert_math=convert_math)
        choices = [(cid, clean_option_text(txt, strip_prefixes=strip_prefixes, convert_math=convert_math))
                   for cid, txt in zip(choice_ids, choices_text)]
        correct_ids = [cid for cid, ok in zip(choice_ids, choices_bools) if ok]

        # Build item
        title = f"{item_prefix}_{idx:02d}"
        success_text = clean_general_text(q.get("success",""), convert_math=convert_math)
        error_text   = clean_general_text(q.get("error",""),   convert_math=convert_math)
        item_id, item_xml = make_item_xml(title, stem, choices, correct_ids, success_text, error_text, shuffle=shuffle)

        # Write item XML into zip
        item_filename = f"{item_id}.xml"
        item_filenames.append(item_filename)
        xml_bytes = ET.tostring(item_xml, encoding="utf-8", xml_declaration=True)
        zf.writestr(item_filename, xml_bytes)

    # Manifest
    manifest_xml = make_manifest_xml(item_filenames)
    manifest_bytes = ET.tostring(manifest_xml, encoding="utf-8", xml_declaration=True)
    zf.writestr("imsmanifest.xml", manifest_bytes)
    zf.close()
    return buf.getvalue()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="JSON → QTI 2.1 Converter", page_icon="🧩", layout="centered")
st.title("🧩 JSON → QTI 2.1 Converter")

st.markdown(
    """
Upload one JSON file containing an array of multiple-choice items:

```json
[
  {
    "question": "… (can include **markdown** and $$\\LaTeX$$) …",
    "options": {
      "Option text A": true,
      "Option text B": false,
      "Option text C": true
    },
    "success": "Feedback shown when *all* correct choices are selected.",
    "error":   "Feedback shown otherwise."
  }
]
"""
)

uploaded = st.file_uploader("Upload JSON file", type=["json"])
col1, col2, col3, col4 = st.columns(4)
with col1:
    strip_prefixes = st.checkbox("Strip A)/B) prefixes", value=True)
with col2:
    convert_math = st.checkbox("Convert LATEX codes", value=True)
with col3:
    shuffle = st.checkbox("Shuffle choices  in the final QTI items", value=True)
with col4:
    item_prefix = st.text_input("Item name prefix", value="Item")

if uploaded is not None:
    try:
        raw = uploaded.read()
        data = json.loads(raw.decode("utf-8"))
        assert isinstance(data, list), "Top level must be a JSON array of items."
        if data:
            assert "question" in data[0] and "options" in data[0], "Each item must have 'question' and 'options'."
    
        if st.button("Convert to QTI ZIP"):
            zip_bytes = json_to_qti_zip(raw, strip_prefixes=strip_prefixes, convert_math=convert_math, shuffle=shuffle, item_prefix=item_prefix,)
            st.success("QTI package created.")
            st.download_button("📦 Download QTI ZIP", data=zip_bytes, file_name="qti_items.zip", mime="application/zip")
    except Exception as e:
        st.error(f"Could not parse/convert JSON: {e}")
