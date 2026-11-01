"""Shared presentation helpers; no transport calculations or random sampling.

CODE MAP — refresh with python scripts/update_code_index.py
  L0025  apply_styles
  L0032  section
  L0039  show_figure
  L0055  focus_transport
END CODE MAP
"""
from contextlib import contextmanager
from pathlib import Path
import base64
import html
import io
import json

import streamlit as st
import streamlit.components.v1 as components

ASSETS=Path(__file__).resolve().parent.parent/'assets'
PREVIEW_WIDTH=80  # Percentage of the available width; actual transport stays 100%.
FIGURE_DPI=130


def apply_styles():
    """Only module-owned containers, buttons and figures are styled."""
    css=(ASSETS/'css/experiment.css').read_text()
    st.markdown('<style>'+css+'</style>',unsafe_allow_html=True)


@contextmanager
def section(key,label,*,expanded=False,tone='quiet'):
    """One expander convention; colour is independent of translated labels."""
    with st.container(key=f'disp_section_{tone}_{key}'):
        with st.expander(label,expanded=expanded):
            yield


def show_figure(figure,description,*,preview=False,element_id=None):
    """Reserve image space before decoding to avoid collapsing the page on rerun."""
    buffer=io.BytesIO()
    figure.savefig(buffer,format='png',dpi=FIGURE_DPI)
    width,height=(round(v*FIGURE_DPI) for v in figure.get_size_inches())
    encoded=base64.b64encode(buffer.getvalue()).decode('ascii')
    kind='dispersion-preview' if preview else 'dispersion-figure'
    identifier=f' id="{html.escape(element_id,quote=True)}"' if element_id else ''
    style=f' style="width:{PREVIEW_WIDTH}%;"' if preview else ''
    st.markdown(f'<figure class="{kind}"{identifier}{style}>'
                f'<img class="dispersion-plot" alt="{html.escape(description,quote=True)}" '
                f'width="{width}" height="{height}" src="data:image/png;base64,{encoded}">'
                '</figure>',unsafe_allow_html=True)
    figure.clear()


def focus_transport(element_id,section_id):
    """One scroll per new run; later animation frames never pull the user back.

    Wait for our new figure, then align the Observe heading so Run stays visible.
    The zero-height component uses only our own IDs; it does not change URLs or
    read input fields. Playback also works without this display enhancement.
    """
    script=(ASSETS/'js/focus_transport.js').read_text()
    script=script.replace('__TARGET_ID_JSON__',json.dumps(element_id))
    script=script.replace('__SECTION_ID_JSON__',json.dumps(section_id))
    components.html('<script>'+script+'</script>',height=0,tab_index=-1)
