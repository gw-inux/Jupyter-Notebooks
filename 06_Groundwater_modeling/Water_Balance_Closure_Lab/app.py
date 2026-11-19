"""MWW01 · Water-balance closure · v0.2.0

Contents
1. Language and page setup
2. Experiment state and explicit iteration steps
3. Model settings and mode controls
4. Cross-section with cell-aligned readouts
5. Equations, concise computation details and attribution
"""
from base64 import b64encode
from html import escape
from io import BytesIO
import json
from pathlib import Path

import streamlit as st

from hydraulics import (BUDGET_TOL_PCT, DAY, HEAD_TOL, LEFT, RIGHT, budget,
                        conductances, newton, picard, residual_derivative)
from plots import cross_section, delta_label, number

# 1. Language and page setup
HERE = Path(__file__).resolve().parent
LANGUAGES = {"en": "English", "de": "Deutsch", "es": "Español", "it": "Italiano",
             "hi": "हिन्दी", "zh": "中文", "ar": "العربية"}
state = st.session_state
state.setdefault("language", "en")
labels = json.loads((HERE / "text" / state.language / "ui.json").read_text(encoding="utf-8"))


def t(key, **values):
    return labels[key].format(**values)


def lesson(name):
    st.markdown((HERE / "text" / state.language / f"{name}.md").read_text(encoding="utf-8"))


def tex_number(value):
    """Write scientific notation as an unambiguous power of ten in equations."""
    mantissa, marker, exponent = f"{value:.6g}".partition("e")
    if marker:
        return rf"{mantissa}\times10^{{{int(exponent)}}}"
    return mantissa


st.set_page_config(page_title=t("title") + " · MWW01", page_icon="💧", layout="centered")
st.html((HERE / "style.css").read_text(encoding="utf-8"))
# Keep model geometry left-to-right. Only prose and textual labels use RTL.
if state.language == "ar":
    st.html("""<style>
    .st-key-content [data-testid="stMarkdownContainer"] {direction:rtl; text-align:right;}
    .st-key-content .katex {direction:ltr; unicode-bidi:isolate;}
    .st-key-content [data-testid="stLatex"] {direction:ltr; text-align:center;}
    </style>""")
st.columns([2, 1])[1].selectbox(t("language"), options=list(LANGUAGES),
                               format_func=LANGUAGES.get, key="language")

# 2. Experiment state and explicit iteration steps
state.setdefault("start", LEFT)
state.setdefault("trial", LEFT)
state.setdefault("history", [LEFT])
state.setdefault("unconfined", True)
state.setdefault("mode", "balance")
state.setdefault("last_newton", None)


def restart():
    state.start = round(state.start, 4)
    state.trial = state.start
    state.trial_slider = state.start
    state.trial_entry = state.start
    state.history = [state.start]
    state.last_newton = None


def set_trial(source):
    state.trial = round(state[source], 4)
    state.trial_slider = state.trial
    state.trial_entry = state.trial
    state.last_newton = None


def advance_picard():
    state.history.append(picard(state.history[-1], state.conductivity, state.unconfined))


def previous():
    state.history.pop()


def advance_newton():
    old = state.trial
    updated, fraction = newton(old, state.conductivity, state.unconfined)
    state.last_newton = (old, updated, fraction)
    state.trial = updated
    state.trial_slider = updated
    state.trial_entry = updated


# 3. Model settings and mode controls
with st.container(key="content"):
    st.title(t("title"))
    lesson("intro")
    st.toggle(t("unconfined"), key="unconfined", on_change=restart, help=t("unconfined_help"))
    st.radio(t("mode_label"), options=["balance", "picard"],
             format_func=lambda mode: t(mode + "_mode"), horizontal=True,
             key="mode", on_change=restart, help=t("mode_help"))
    with st.expander("**" + t("settings") + "**", key="settings"):
        k_col, start_col = st.columns(2)
        k_col.number_input(t("conductivity"), min_value=1e-8, max_value=1.0, value=1e-4,
                           step=1e-5, format="%.4e", key="conductivity")
        start_col.number_input(t("start"), min_value=RIGHT, max_value=LEFT,
                               step=.0001, format="%.4f", key="start", on_change=restart)
        st.number_input(t("head_tolerance"), min_value=1e-8, max_value=1.0, value=HEAD_TOL,
                        step=.0001, format="%.1e", key="head_tolerance", help=t("tolerance_help"))
        st.caption(t("geometry"))
        st.caption(t("unconfined_geometry" if state.unconfined else "confined_geometry"))
        st.button(t("restart"), key="restart", on_click=restart)

    is_picard = state.mode == "picard"
    if is_picard:
        st.subheader(":blue-background[" + t("picard_heading") + "]", divider="blue")
        st.markdown(t("picard_instruction"))
        history = state.history
        head = history[-1]
        stepped = len(history) > 1
        closed = stepped and abs(head-history[-2]) <= state.head_tolerance
        back, forward = st.columns([1, 2])
        back.button("− " + t("previous"), key="previous", on_click=previous,
                    disabled=not stepped, width="stretch")
        forward.button(t("update" if stepped else "compute"), key="advance_picard",
                       on_click=advance_picard, disabled=closed, type="primary", width="stretch")
    else:
        st.subheader(":green-background[" + t("balance_heading") + "]", divider="green")
        st.markdown(t("balance_instruction"))
        state.setdefault("trial_slider", state.trial)
        state.setdefault("trial_entry", state.trial)
        slider, entry = st.columns([2, 1], vertical_alignment="center")
        slider.slider(t("trial_slider"), min_value=RIGHT, max_value=LEFT, step=.0001,
                      format="%.4f", key="trial_slider", on_change=set_trial, args=("trial_slider",))
        entry.number_input(t("trial_entry"), min_value=RIGHT, max_value=LEFT, step=.0001,
                           format="%.6f", key="trial_entry", on_change=set_trial, args=("trial_entry",))
        head, history = state.trial, None
        qin, qout, residual, pct = budget(head, state.conductivity, state.unconfined)
        closed = abs(pct) <= BUDGET_TOL_PCT
        st.button(t("newton_button"), key="advance_newton", on_click=advance_newton,
                  disabled=closed, type="primary")

    # 4. Cross-section with cell-aligned readouts
    def section_image(narrow):
        fig = cross_section(head, state.conductivity, state.unconfined, history, narrow=narrow)
        buffer = BytesIO()
        fig.savefig(buffer, format="svg")
        return "data:image/svg+xml;base64," + b64encode(buffer.getvalue()).decode("ascii")

    if is_picard:
        change = head-history[-2] if stepped else None
        readouts = [t("step", n=len(history)-1) + " · " + t("head_change"),
                    delta_label(change) if stepped else "—"]
        detail = t("within" if closed else "above") if stepped else t("initial")
        detail_html = escape(detail)
        ledger = ('<div class="head-ledger"><div>' + escape(readouts[0]) + '</div>'
                  '<strong dir="ltr">' + escape(readouts[1]) + (' m' if stepped else '') + '</strong></div>')
        if stepped:
            ledger += f'<div class="head-pair" dir="ltr">{history[-2]:.6f} → {head:.6f} m</div>'
    else:
        status_key = "exact" if residual == 0 else ("within" if closed else
                     ("in_exceeds" if residual > 0 else "out_exceeds"))
        detail_html = (f'<bdi dir="ltr">{escape(number(pct, signed=True))}%</bdi>'
                       f' · <bdi dir="auto">{escape(t(status_key))}</bdi>')
        ledger = '<div class="budget-row">'
        for label, value in ((t("inflow"), number(qin*DAY, digits=6)),
                             (t("residual"), number(residual*DAY, signed=True)),
                             (t("outflow"), number(qout*DAY, digits=6))):
            ledger += (f'<div><div dir="auto">{escape(label)}</div>'
                       f'<strong dir="ltr">{escape(value)}</strong><span dir="ltr">m³/d</span></div>')
        ledger += '</div>'
    alt = t("plot_alt", head=f"{head:.6f}")
    direction = "rtl" if state.language == "ar" else "ltr"
    st.html(f'''<section class="closure-section" dir="{direction}">
      <div class="cell-names"><b dir="auto">{escape(t("fixed_head"))}</b>
        <b dir="auto">{escape(t("middle_cell"))}</b><b dir="auto">{escape(t("fixed_head"))}</b></div>
      <img class="desktop" src="{section_image(False)}" alt="{escape(alt)}">
      <img class="phone" src="{section_image(True)}" alt="{escape(alt)}">
      <div class="ledger {'met' if closed else 'open'}">{ledger}
        <div class="closure-status">{detail_html}</div>
      </div>
    </section>''')
    st.caption(t("plot_caption"))
    if is_picard:
        st.caption(t("head_caption", tolerance=number(state.head_tolerance)))
    else:
        st.caption(t("budget_caption", tolerance=number(BUDGET_TOL_PCT)))

    # 5. Equations, concise computation details and attribution
    if is_picard:
        st.latex(r"h_{k+1}=\frac{C_L(h_k)\,h_L+C_R(h_k)\,h_R}{C_L(h_k)+C_R(h_k)}")
    lesson("unconfined" if state.unconfined else "confined")
    with st.expander("**" + t("details") + "**", key="details"):
        lesson("picard" if is_picard else "newton")
        if is_picard:
            if stepped:
                h_old = history[-2]
                c_left, c_right = conductances(h_old, state.conductivity, state.unconfined)
                st.caption(t("last_update"))
                st.latex(rf"h_k={h_old:.8f}\,\mathrm{{m}},\quad C_L={tex_number(c_left)}\,\mathrm{{m^2/s}},\quad C_R={tex_number(c_right)}\,\mathrm{{m^2/s}}")
                st.latex(rf"h_{{k+1}}={head:.8f}\,\mathrm{{m}},\quad \Delta h={tex_number(head-h_old)}\,\mathrm{{m}}")
            else:
                st.caption(t("first_compute"))
        else:
            st.latex(r"R(h)=Q_L(h)-Q_R(h),\qquad \Delta h_N=-\frac{R(h_k)}{R'(h_k)},\qquad h_{k+1}=h_k+\alpha\Delta h_N")
            st.latex(r"R'(h)=-\frac{2KW}{\Delta x}(h-z_b)" if state.unconfined else
                     r"R'(h)=-\frac{2KWb}{\Delta x}")
            if state.last_newton is not None:
                old, updated, fraction = state.last_newton
                old_residual = budget(old, state.conductivity, state.unconfined)[2]
                slope = residual_derivative(old, state.conductivity, state.unconfined)
                st.caption(t("last_update"))
                st.latex(rf"R(h_k)={tex_number(old_residual)}\,\mathrm{{m^3/s}},\quad R'(h_k)={tex_number(slope)}\,\mathrm{{m^2/s}}")
                st.latex(rf"h_{{k+1}}={old:.8f}+{fraction:g}\,({tex_number(-old_residual/slope)})={updated:.8f}\,\mathrm{{m}}")
                if fraction < 1:
                    st.info(t("newton_damping", fraction=number(fraction)))
        lesson("closure")
    st.divider()
    st.caption(t("footer"))
