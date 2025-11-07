import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import streamlit as st
from streamlit_book import multiple_choice
import json

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

path_quest_final = "06_Groundwater_modeling/QUESTIONS/bc_intro_final_ass.json"

# Load questions
with open(path_quest_final, "r", encoding="utf-8") as f:
    quest_final = json.load(f)
    
# Functions
# RENDER ASSESSMENTS

def flip_assessment(section_id: str):
    """Flip the boolean flag for a given section_id."""
    key = f"exp_{section_id}"
    st.session_state[key] = not st.session_state.get(key, False)
    
def render_toggle_container(
    section_id: str,
    label: str,
    content_fn,                 # a function that renders the section contents when open
    *,
    default_open: bool = False,
    col_ratio=(25, 1),
    container_border: bool = True,
):
    """
    Renders a toggleable container with two buttons:
    - Left: text button with your label
    - Right: chevron button (▲/▼)
    Each section manages its own state via section_id.

    Parameters
    ----------
    section_id : unique id string, e.g., "general_01"
    label      : button label shown on the left
    content_fn : callable with no args that renders the open content
    default_open : initial open state (only used on first render)
    col_ratio  : column width ratio for (label_button, chevron_button)
    container_border : show a border around the section container
    """
    state_key = f"exp_{section_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_open

    with st.container(border=container_border):
        ass_c1, ass_c2 = st.columns(col_ratio)

        # Left button – same on_click toggler for consistency
        with ass_c1:
            st.button(label,key=f"btn_label_{section_id}",type="tertiary",on_click=flip_assessment,args=(section_id,))

        # Right chevron button – also toggles the same state
        with ass_c2:
            chevron = "▲" if st.session_state[state_key] else "▼"
            st.button(chevron,key=f"btn_chev_{section_id}",type="tertiary",on_click=flip_assessment,args=(section_id,))

        # Conditional content
        if st.session_state[state_key]:
            content_fn()
# --- Start here

st.title("Introduction to boundary conditions")
st.subheader("Visual explanation of types of boundary conditions", divider = "blue")

# ToDo: Show the boundary elements (like the defined head) clearly in the figures
# ToDo: add water triangle on surface water and groundwater
# ToDo: Add motivation, more explanation, and assessments

# ---------- Minimal, scenario-1-only visualization ----------
def intro_scenario1_block(bc_kind):
    # --- Fixed model settings (Scenario 1) ---
    L     = 2500.0            # domain length [m]
    hr    = 150.0             # specified head at x=L [m]
    hRiv  = 150.0             # external stage for head-dependent case [m]
    cRiv  = 9e-6              # FIXED conductance [m^2/s] (used only if "head-dependent" is toggled)
    zb    = hr - 150.0        # bottom elevation
    x     = np.linspace(0.0, L, 1000)
    
    key_suffix = bc_kind.replace(" ", "_").replace(".", "").replace("-", "_").lower()

    if bc_kind == "Head-dep. flux":
        riv = True
    else:
        riv = False
    # --- Three recharge states (mm/yr -> m/s) ---
    R_choices_mm = [-250, 0, 250]
    K_choices    = [5e-5, 1e-4, 5e-4]
    
    R_map = {f"{mm:+d} mm/yr": mm/1000/365.25/86400 for mm in R_choices_mm}
    K_labels = [f"{k:.0e} m/s" for k in K_choices]     # -> ['5e-05 m/s','1e-04 m/s','5e-04 m/s']
    K_map    = dict(zip(K_labels, K_choices))
    
    # ---------- UI (compact) ----------
    left, right = st.columns((2, 1), gap="large")
    
    with left:
        if bc_kind == "Recharge":
            # Fix R at +200 mm/yr; let user pick K
            K_label = st.radio(
                "Hydraulic conductivity ***K*** (3 steps)",
                K_labels,
                index=1,                      # default 5e-5 m/s
                horizontal=True,
                key=f"intro_K_choice_{key_suffix}",
            )
            K        = K_map[K_label]
            R_label  = "+250 mm/yr"
            R_active = R_map[R_label]
        else:
            # Pick R; keep K fixed at 5e-5
            R_label = st.radio(
                "Recharge ***R*** (3 steps)",
                list(R_map.keys()),
                index=1,                      # default 0 mm/yr
                horizontal=True,
                key=f"intro_R_choice_{key_suffix}",
            )
            R_active = R_map[R_label]
            K        = 5e-5
            K_label  = f"{K:.0e} m/s"        # for titles if you show K

#    with right:
#        turn = st.toggle("Rotate to h–Q", value=False, key=f"intro_turn_{key_suffix}")
    turn = False
    
    # ---------- Helper: compute h(x) for a given R and boundary type ----------
    def head_profile(R, use_riv, K_val):
        if use_riv:
            # effective boundary head (from your original derivation)
            hr_riv = R * L / cRiv + hRiv
            phiL = 0.5 * K_val * (hr_riv - zb) ** 2
        else:
            phiL = 0.5 * K_val * (hr - zb) ** 2
        h = zb + np.sqrt(2.0 * (-R / 2.0 * (x**2 - L**2) + phiL) / K_val)
        return h

    # Active recharge (head profile shown on the LEFT)
    R_active = R_map[R_label]
    #K = 5e-5              # FIXED hydraulic conductivity [m/s]
    h_active = head_profile(R_active, riv, K)

    # ---------- Q–h curves (do not depend on R except their markers/points) ----------
    # 1) Specified head boundary (right)
    Q_defh = np.linspace(-400/1000/365.25/86400*L, 400/1000/365.25/86400*L, 10)
    h_defh = np.ones_like(Q_defh) * hr

    # 2a) No-flow (left boundary)
    h_nf = np.linspace(140, 160, 20)
    Q_nf = np.zeros_like(h_nf)

    # 2b) Recharge (per m²) at x=1250 m
    h_rch_axis = np.linspace(140, 160, 20)  # x-axis values for the horizontal line in Q–h
    # (the horizontal line's Q level will be set per-R)

    # 3) Head-dependent flux (right)
    h_rob_axis = np.linspace(140, 160, 20)
    Q_rob_axis = cRiv * (hRiv - h_rob_axis)

    # ---------- Points for all three recharge states (active colored, others grey) ----------
    # Colors consistent with your app
    color_active = {
        "No-flow": "darkorange",
        "Recharge": "green",
        "Specified head": "blue",
        "Head-dep. flux": "fuchsia",
    }
    grey = "#B0B0B0"

    # Prepare per-R point extractors
    def point_no_flow(R):
        # left boundary head (x≈0) for that R
        hR = head_profile(R, riv, K)[0]
        return 0.0, hR  # (Q, h) when rotated; otherwise (h, Q) we’ll swap later

    def point_recharge(R, K_val):
        """
        Compute the (Q, h) point for the recharge case.
        Q corresponds to the applied recharge rate (R),
        h is the hydraulic head at mid-domain, dependent on K.
        """
        h_mid = np.interp(L/2, x, head_profile(R, riv, K_val))
        return R, h_mid

    def point_specified_head(R):
        # head fixed at hr; Q responds to R (same expression as original)
        return R * L * (-1.0), hr

    def point_head_dep(R):
        # head at right boundary from profile for that R, flux via conductance
        hR = head_profile(R, True, K)[-1]  # ensure use of riv relation for point location
        return cRiv * (hRiv - hR), hR

    # Map the current bc_type to a point extractor and a curve drawer
    def collect_points_for_bc(kind):
        pts = []
        if kind == "Recharge":
            # For Recharge: vary K, R is fixed (+250 mm/yr)
            for K_val in K_choices:
                Qp, hp = point_recharge(R_map["+250 mm/yr"], K_val)
                pts.append((Qp, hp))
        else:
            # For all other BCs: vary R, K fixed
            for mm in R_choices_mm:
                R = R_map[f"{mm:+d} mm/yr"]
                if kind == "No-flow":
                    Qp, hp = point_no_flow(R)
                elif kind == "Specified head":
                    Qp, hp = point_specified_head(R)
                elif kind == "Head-dep. flux":
                    Qp, hp = point_head_dep(R)
                else:
                    Qp, hp = None, None
                pts.append((Qp, hp))
        return pts

    # ---------- Plotting ----------
    fig = plt.figure(figsize=(10, 5))
    gs = GridSpec(1, 2, width_ratios=[2, 1], wspace=0.85, figure=fig)
    axL = fig.add_subplot(gs[0, 0])
    axR = fig.add_subplot(gs[0, 1])
    pos = axR.get_position()
    axR.set_position([pos.x0, pos.y0 + pos.height * 0.25, pos.width, pos.height * 0.5])
    
    for ax in (axL, axR):
        ax.tick_params(axis='x', which='both', length=0)  # no x ticks
        ax.set_xticklabels([])                            # no x labels
        ax.set_xlabel(None)                               # no x-axis label
    
    # optional: cleaner frame for illustration feel
    for ax in (axL, axR):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    # LEFT: head profile for ACTIVE recharge only
    axL.plot(x, h_active, linewidth=2.5);
    axL.fill_between(x, 0, h_active, facecolor="lightblue", alpha=1, edgecolor="none")
    
    # --- Fixed land surface independent of h(x) ---
    surf_base = 150.0            # reference level in meters
    relief_max = 9.0             # peak height above 140 m
    u = np.clip(x / L, 0, 1)
    mound = relief_max * (1 - u)**0.25 * (0.8 + 0.1*np.cos(np.pi * np.clip(u, 0, 0.4) / 0.4))
    y_cap = surf_base + mound    # final land-surface curve (independent of h)
    
    # draw unsaturated zone and surface elevation
    axL.fill_between(
        x, h_active, y_cap,
        facecolor="#9c6b3d", edgecolor="#704214", linewidth=0.8, alpha=0.95, zorder=1
    )
    axL.plot(x, y_cap, color="#5e3b16", linewidth=1.2, zorder=1.1)
    
    # make sure the cap is visible in the current y-limits
    axL.set_ylim(140, max(160, (y_cap.max() + 0.5)))

    # ---- Optional pine tree on top of the land surface ----
    show_tree = True
    tree_path = "06_Groundwater_modeling/FIGS/tree-23.png"
    tree_x1    = 500
    tree_zoom1 = 0.4
    tree_x2    = 1100
    tree_zoom2 = 0.3
    
    if show_tree:
        try:
            img = plt.imread(tree_path)
            # y position: land-surface height at tree_x
            i = np.searchsorted(x, tree_x1)
            y_here = y_cap[min(max(i, 0), len(y_cap)-1)]
            oi1 = OffsetImage(img, zoom=tree_zoom1)
            oi2 = OffsetImage(img, zoom=tree_zoom2)
            ab1 = AnnotationBbox(
                oi1, (tree_x1, y_here),
                frameon=False, box_alignment=(0.5, 0.1),  # bottom-center sits on the surface
                xycoords='data'
            )
            ab2 = AnnotationBbox(
                oi2, (tree_x2, y_here),
                frameon=False, box_alignment=(0.5, 0.48),  # bottom-center sits on the surface
                xycoords='data'
            )
            axL.add_artist(ab1)
            axL.add_artist(ab2)
        except Exception as e:
            st.info(f"Could not load tree image from '{tree_path}': {e}")
    
    
    
    river_w = L * 0.15  # width of the surface-water block/extension outside the domain
    axL.set_xlim(-30, L + river_w)
    axL.set_ylim(140, 160)
    
    # boundaries
    axL.vlines(0, 0, 1000, color="moccasin", linewidth=8, alpha=0.7)     # no-flow at left
    
    # --- parameters for surface-water area ---
    river_base = 140.0
    river_stage = hr
    
    # 1) Aquifer extension
    x_ext = np.linspace(L, L + river_w, 30)
    y_ext = np.linspace(hRiv, hr, 30)
    
    # create a short curved path dipping into the water
    x_start = L
    y_start = y_cap[-1]
    x_rivbed = np.linspace(x_start, L + river_w, 30)
    y_rivbed = y_start - 8.0 * np.sin(np.linspace(0, np.pi/2, 30))

    # draw the riverbed outline
    axL.plot(x_rivbed, y_rivbed, color="darkblue", linewidth=1.8, zorder=3.3, clip_on=False)     
    
    # River water level
    axL.plot(
        x_ext, y_ext, color="darkblue", linewidth=2.0,
        solid_capstyle="round", zorder=3.2, clip_on=False
    )

    # fill below the riverbed with aquifer color to continue the subsurface
    axL.fill_between(
        x_rivbed, river_base, y_rivbed,
        facecolor="lightblue", edgecolor="none", alpha=1, zorder=2
    )        
#    # Fill the river
#    axL.fill_between(
#        x_ext, 140.0, y_ext,
#        facecolor="deepskyblue", edgecolor="none", alpha=0.75,
#        zorder=1.0, clip_on=False
#    )
    if riv:
        
        # Fill the river
        axL.fill_between(
            x_ext, 140.0, y_ext,
            facecolor="deepskyblue", edgecolor="none", alpha=0.75,
            zorder=1.0, clip_on=False
            )
            
        # right: head-dependent + external stage indicator (thin fuchsia line)
        hr_riv = R_active * L / cRiv + hRiv
        
        # draw line representing conductance
        if hr_riv > 150:
            axL.vlines(L - 5,150, hr_riv, color="fuchsia", linewidth=3, zorder=3)
        
        # fill the dewatered area (only where riverbed lies above river stage)
        mask = y_rivbed > hr_riv
        
        if np.any(mask):
            axL.fill_between(
                x_rivbed[mask], hr_riv, y_rivbed[mask],
                facecolor="#9c6b3d", edgecolor="none", alpha=1.0, zorder=2
            )
        
        # draw the riverbed outline
        axL.plot(x_rivbed, y_rivbed, color="fuchsia", linewidth=3, zorder=3.3, clip_on=False)  
    
    else: 
        # Fill the river
        axL.fill_between(
            x_ext, 140.0, y_ext,
            facecolor="aqua", edgecolor="none", alpha=0.75,
            zorder=1.0, clip_on=False        
            )

    # Mark the x-position that Q–h “samples” for Recharge (mid-domain)
    if bc_kind == "Recharge":
        axL.plot(L*0.35, np.interp(L*0.35, x, h_active), "go", ms=9, zorder=5);
    elif bc_kind == "No-flow":
        axL.plot(0, h_active[0], "o", color="darkorange", ms=9, zorder=5);
    elif bc_kind == "Specified head":
        axL.plot(L, hr, "bo", ms=9, zorder=5);
    elif bc_kind == "Head-dep. flux":
        axL.plot(L, head_profile(R_active, True, K)[-1], "o", color="fuchsia", ms=9, zorder=5);

    # Arrows and visuals
    # Recharge
    sgn1 = np.sign(R_active)      # +: downward arrows; -: upward; 0: none
    if sgn1 != 0:
        xs = np.array([0.20*L, 0.50*L, 0.8*L])     # three positions
        d  = 2.0                                    # arrow half-length (increased for visibility)
        for xi in xs:
            yi = np.interp(xi, x, h_active)         # height at xi
            # define direction
            if sgn1 > 0:  # positive R → downward
                xytext, xy = (xi, yi + d), (xi, yi - d)
            else:         # negative R → upward
                xytext, xy = (xi, yi - d), (xi, yi + d)
            axL.annotate(
                "",
                xy=xy, xytext=xytext,
                arrowprops=dict(
                    arrowstyle="-|>,head_width=0.6,head_length=2",  # larger arrowhead
                    lw=2,
                    facecolor="goldenrod",    # fill color
                    edgecolor="burlywood",     # outline color
                    shrinkA=0, shrinkB=0,     # no shrink at ends
                ),
                zorder=5
            )
    # Groundwater-Surface water 
    sgn2 = np.sign(R_active)  # +: toward river (right); -: toward aquifer (left)
    y0 = hr-6                 # vertical position relative to river stage
    x0 = L+30                    # start at boundary
    d  = river_w*0.9       # arrow half-length in x-direction

    # Define direction
    if sgn1 != 0:
        if sgn2 > 0:   # positive recharge → groundwater to river
            xytext, xy = (x0 - d, y0), (x0 + d, y0)
        else:          # negative recharge → river to groundwater
            xytext, xy = (x0 + d, y0), (x0 - d, y0)
    
        axL.annotate(
            "",
            xy=xy, xytext=xytext,
            arrowprops=dict(
                arrowstyle="-|>,head_width=0.75,head_length=3",
                lw=3,
                facecolor="turquoise",     # same fill color as recharge arrows
                edgecolor="lightseagreen",  # same outline color
                shrinkA=0, shrinkB=0,
            ),
            zorder=6
        )

    # RIGHT: Q–h plot
    flow_label = "flow into the groundwater (m³/s)" # was "+ is flow INTO the model, $Q_{in}$ (m³/s)"
    if bc_kind == "None":
        axR.axis("off")
        axR.text(0.5, 0.5, "No Q–h plot selected", ha="center", va="center", transform=axR.transAxes)
    else:
        # draw curve for the chosen boundary type
        if bc_kind == "No-flow":
            flow_label = "+ is flow INTO the groundwater from \nthe LEFT BOUNDARY $Q_{in}$ (m³/s)"
            if turn:
                axR.plot(Q_nf, h_nf, color="black", linewidth=3);
                axR.set_ylabel("hydraulic head (m)")
                axR.set_xlabel(flow_label)
                axR.set_ylim(140, 160)
                axR.set_xlim(-1, 1)
                axR.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            else:
                axR.plot(h_nf, Q_nf, color="black", linewidth=3);
                axR.set_xlabel("hydraulic head (m)")
                axR.set_ylabel(flow_label)
                axR.set_xlim(140, 160)
                axR.set_ylim(-1, 1)
        elif bc_kind == "Recharge":
            flow_label = "+ is flow INTO the groundwater from \nSURFACE RECHARGE $Q_{in}$ (m³/s)"
            Q_recharge = 250 / 1000 / 365.25 / 86400   # [m/s]
            if turn:
                axR.axvline(Q_recharge, color="black", linewidth=3);  # keep axis consistent
                # Will just place points at (Q=R, h=…)
                axR.set_ylabel("hydraulic head (m)")
                axR.set_xlabel(flow_label)
                axR.set_ylim(145, 155)
                axR.set_xlim(-400/1000/365.25/86400, 400/1000/365.25/86400)
                axR.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            else:
                axR.axhline(Q_recharge, color="black", linewidth=3);     # cosmetic for axis
                axR.set_xlabel("hydraulic head (m)")
                axR.set_ylabel(flow_label)
                axR.set_xlim(145, 155)
                axR.set_ylim(-400/1000/365.25/86400, 400/1000/365.25/86400)
                axR.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
        elif bc_kind == "Specified head":
            flow_label = "+ is flow INTO the groundwater from \nthe LAKE $Q_{in}$ (m³/s)"
            if turn:
                axR.plot(Q_defh, h_defh, color="black", linewidth=3);
                axR.set_ylabel("hydraulic head (m)")
                axR.set_xlabel(flow_label)
                axR.set_ylim(140, 160)
                axR.set_xlim(-400/1000/365.25/86400*L, 400/1000/365.25/86400*L)
                axR.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            else:
                axR.plot(h_defh, Q_defh, color="black", linewidth=3);
                axR.set_xlabel("hydraulic head (m)")
                axR.set_ylabel(flow_label)
                axR.set_xlim(140, 160)
                axR.set_ylim(-400/1000/365.25/86400*L, 400/1000/365.25/86400*L)
                axR.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
        elif bc_kind == "Head-dep. flux":
            flow_label = "+ is flow INTO the groundwater from \nthe RIVER $Q_{in}$ (m³/s)"
            if turn:
                axR.plot(Q_rob_axis, h_rob_axis, color="black", linewidth=3);
                axR.set_ylabel("hydraulic head (m)")
                axR.set_xlabel(flow_label)
                axR.set_ylim(140, 160)
                axR.set_xlim(-400/1000/365.25/86400*L, 400/1000/365.25/86400*L)
                axR.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
            else:
                axR.plot(h_rob_axis, Q_rob_axis, color="black", linewidth=3);
                axR.set_xlabel("hydraulic head (m)")
                axR.set_ylabel(flow_label)
                axR.set_xlim(140, 160)
                axR.set_ylim(-400/1000/365.25/86400*L, 400/1000/365.25/86400*L)
                axR.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))

        # --- Active index & draw points ---
        if bc_kind == "Recharge":
            pts = collect_points_for_bc(bc_kind)
            active_idx = K_choices.index(K)  # active K value
        else:
            pts = collect_points_for_bc(bc_kind)
            active_idx = R_choices_mm.index(int(R_label.replace(" mm/yr", "")))
        
        for i, (Qp, hp) in enumerate(pts):
            if Qp is None:
                continue
            color = color_active[bc_kind] if i == active_idx else grey
            if turn:
                axR.plot(Qp, hp, "o", color=color, ms=8, zorder=5)
            else:
                axR.plot(hp, Qp, "o", color=color, ms=8, zorder=5)

        if not turn:
            axR.axhline(0, color="grey", linestyle="--", linewidth=0.8)
            axR.axvline(150, color="grey", linestyle="--", linewidth=0.8)
        else:
            axR.axvline(0, color="grey", linestyle="--", linewidth=0.8)
            axR.axhline(150, color="grey", linestyle="--", linewidth=0.8)

        # Titles
        ttl = {
            "No-flow":        ("Q–h", "h–Q")[turn] + ": Specified flow (No-flow) ",
            "Recharge":       ("Q–h", "h–Q")[turn] + ": Specified flow (Recharge per m²)",
            "Specified head": ("Q–h", "h–Q")[turn] + ": Specified head           ",
            "Head-dep. flux": ("Q–h", "h–Q")[turn] + ": Head-dependent flux      ",
        }.get(bc_kind, "")
        if ttl:
            axR.set_title(ttl, pad=10)

    st.pyplot(fig)
    plt.close(fig)

# ---- Explanation and plots ----

st.markdown("""

#### 💡 Motivation - What are boundary conditions in groundwater modeling?
Boundary conditions define how the groundwater system interacts with its surroundings.

They describe whether water can **enter** or **leave** the model domain, for example, through **recharge**, **rivers**, **lakes**, or **impermeable barriers**.""")

columns_fig0 = st.columns((1,4,1))
with columns_fig0[1]:
    st.image('06_Groundwater_modeling/FIGS/stream_groundwater_BC.png')

st.markdown("""

It is essential to understand the concept behind the different boundary conditions. This understanding is required to 'translate' physical and hydrological elements of the real world into model elements.

With the app you can build **intuition** for how Type I/II/III boundaries behave, and how this behavior can be described by discharge-head relations (_Q–h_-plots). You will learn how boundary conditions reflect system characteristics, and you will gain an understanding of the general characteristics of **groundwater–surface water interaction**.


#### 🎯 Learning Objectives
By engaging with this application, you will be able to:
- **Explain** the general characteristics of the different boundary types.
- **Distinguish** Type I (specified head), Type II (specified flux), and Type III (head-dependent flux) boundaries and name typical use cases.
- **Predict qualitatively** the boundary condition behavior with a **Q–h** plot.
- **Discuss** how the different boundary conditions can reflect heads and flows of real systems.""")

st.subheader("💧 Understanding Boundary Conditions", divider="green")

st.markdown("""
Before we get into the mathematical implications of boundary conditions it’s important to have some examples of natural features that can be represented by each type of boundary condition.

#### 🌍 Field examples of features represented by boundary conditions:

**For a location** where the hydraulic head is specified, we can represent it as a

:orange[**Type I (specified head):**]
- **Large Lake/Major River** with a relatively constant water level (head)
- **Reservoir** with a water level maintained at a fixed elevation for water management purposes
- **Adjacent Aquifer** beyond the model domain with a stable head and a source of water""")
columns_fig1 = st.columns((1,1,1))
with columns_fig1[0]:
    st.image('06_Groundwater_modeling/FIGS/Lake01.jpg')
    st.markdown(":orange[*Large lake with no resistance between the lake and the groundwater.*]")
with columns_fig1[1]:
    st.image('06_Groundwater_modeling/FIGS/Sea02.jpg')
    st.markdown(":orange[*The sea and a hard rock aquifer with no resistance between the sea and the groundwater.*]")
with columns_fig1[2]:
    st.image('06_Groundwater_modeling/FIGS/Sea03.jpg')
    st.markdown(":orange[*The sea and a sandy beach with no resistance between the sea and the groundwater.*]")

st.markdown("""
**For a location** where the flux across the boundary is specified and the hydraulic head adjusts accordingly, we can represent it as

:green[**Type II (specified flux)**]
- **A well** with a known pumping rate for agricultural or municipal use
- **Recharge** infiltration of precipitation to the water table
- **Impermeable material** is physical barrier to flow that forms a no-flow boundary such as a contact with low-permeability bedrock (e.g., granite mountains)
- **A groundwater flow line** forms a no-flow boundary in a steady flow field
- **A groundwater divide** forms a no-flow boundary in a steady flow system""")

columns_fig2 = st.columns((1,1,1))
with columns_fig2[0]:
    st.image('06_Groundwater_modeling/FIGS/Well01.jpg')
    st.markdown(":green[*An abstraction well in a mining area.*]")
with columns_fig2[1]:
    st.image('06_Groundwater_modeling/FIGS/Precipitation01.jpg')
    st.markdown(":green[*Precipitation resulting in groundwater recharge.*]")
with columns_fig2[2]:
    st.image('06_Groundwater_modeling/FIGS/Evapo01.jpg')
    st.markdown(":green[*Evapotranspiration resulting in water flow from underground to the atmosphere.*]")
    
st.markdown("""
**For a location** where water exchange occurs through a resistance layer and depends on the head difference between the boundary and the aquifer, we can represent it as a

:violet[**Type III (head-dependent flux):**]
- **Stream/Aquifer Interaction** where flow into or out of the aquifer depends on the difference between the stream stage and the groundwater head as well as the conductance of the streambed material
- **Springs** that flow when the water table intersects the ground surface
- **Drains** that keep water levels from getting too high in agricultural fields, or keep a foundation dry
- **Underground mine shafts and tunnels** where inflow needs to be estimated to design pump systems to keep the mine dewatered
- **Evapotranspiration** where water discharges to the surface at a rate that depends on the depth of the water table
- **A semi-permeable barrier** such as a clay liner that separates the groundwater system from leachate""")

columns_fig3 = st.columns((1,1,1))
with columns_fig3[0]:
    st.image('06_Groundwater_modeling/FIGS/Lake03.jpg')
    st.markdown(":violet[*A lake with vegetation at the shore line, with a layer of resistive, fine-grained material between the lake and the groundwater.*]")
with columns_fig3[1]:
    st.image('06_Groundwater_modeling/FIGS/Lake04.jpg')
    st.markdown(":violet[*A lake that is partially dewatered, showing the resistive, fine-grained layer at the lake bottom.*]")
with columns_fig3[2]:
    st.image('06_Groundwater_modeling/FIGS/River01.jpg')
    st.markdown(":violet[*A river with a layer of resistive, fine-grained material between the river water and the groundwater.*]")
    
st.markdown("""
#### Background:

Without boundary conditions, the groundwater flow equation could not be solved, because the equation is only a general solution to flow through a porous medium. We need to define how the system behaves at the limits of its domain and apply those boundary conditions to formulate a specific solution that can be solved.

""")
    
columns_fig4 = st.columns((1,4,1))
with columns_fig4[1]:
    st.image('06_Groundwater_modeling/FIGS/GWF_EX01.jpg')

st.markdown("""
To illustrate the idea, consider the **one-dimensional steady-state flow equation**, for a situation as shown in the figure above _(an unconfined groundwater system with one no-flow boundary and one specified head or optionally a head-dependent flux boundary)_:

$ \\frac{d}{dx} K \\frac{dh}{dx} = 0$

where *K* is the hydraulic conductivity and *h* is the hydraulic head. 

**If we include recharge, *R*, and define the aquifer thickness as equal to the head by assuming the bottom of the aquifer is horizontal at an elevation of zero to account for the unconfined condition, then the one-dimensional steady-state flow equation becomes:**

$ \\frac{d}{dx}(-hK\\frac{dh}{dx})=R$

To solve this equation for $h(x)$, we define the head or flow at each end of the domain and a uniform flow over the length of the system. These are the **boundary conditions**.
""")

st.subheader("🟧 Type I – Specified Head (Dirichlet Condition", divider = "orange")
st.markdown("""
A **Type I** boundary condition assigns a defined hydraulic head at the boundary, such as the specified water level of a large lake or reservoir.  

The aquifer can either **discharge into** or **receive water from** the specified head boundary depending on the internal head gradient.  

The head remains constant, while the direction and rate of flow adapt to the hydraulic head difference.

**For this example, flow on the left side is 0 m³/s, head of the lake is 150 m, and *K* of the aquifer is 5x10⁻⁵ m/s, while the user varies recharge to be zero or +/- 250 mm/yr (i.e., +/- 8 x 10⁻⁹ m³/s which is 250 mm/yr over the 2500 m long system).**

**The model calculates the hydraulic heads required to drive the selected recharge to the lake for this hydraulic conductivity.**
""")
intro_scenario1_block("Specified head")

st.subheader("🟩 Type II – Specified Flux (Neumann Condition)", divider = "green")
st.markdown("""
A **Type II** boundary condition prescribes a specified flux or head gradient across the boundary. 
 
Typical examples include **recharge** through the soil surface or **abstraction** by a pumping well.  

**For this example, flow on the left side is 0 m³/s, head of the lake is 150 m, and recharge *R* is 8 x 10⁻⁹ m³/s (i.e., 250 mm/yr over the 2500 m long system), while the user varies hydraulic conductivity to be 5 x 10⁻⁵, 1 x 10⁻⁴, or 5 x 10⁻⁴ m/s.**

**The model calculates the hydraulic heads required to drive the recharge to the lake given the selected hydraulic conductivity.**
""")
intro_scenario1_block("Recharge")
st.subheader("🔻 Type II – Specified Flux (Neumann Condition) - Special Case: :red[No-Flow]")
st.markdown("""
The no-flow condition defines that at the boundary no water enters or leaves the groundwater. In the subsequent figure this is the case for the left boundary. There is no variation in the general setup in comparison to the previous situations: The hydraulic conductivity of the aquifer is 5x10⁻⁵ m/s. The groundwater is in direct contact with the lake on the right side with the lake head specified as 150 m above reference, and **recharge can be modified for three situations**.
""")

intro_scenario1_block("No-flow")

st.subheader("🟪 Type III – Head-Dependent Flux (Robin [Mixed] Condition)", divider = "violet")
st.markdown("""
A **Type III** boundary condition links the flux to the difference between the groundwater head *h* and an external head *H* (for instance, a river, lake, or drain).
  
It combines aspects of the first two types and is therefore also called a **mixed** or **Robin** boundary condition.  

The relationship is expressed as

$q = C (h - H)$

where *C* is the **conductance** of the interface (for example, a riverbed separating the aquifer from the river water).  

When groundwater is **higher** than the boundary head, flow occurs **toward** the boundary; when both are **equal**, there is **no net exchange**; and when groundwater is **lower**, water moves **from** the boundary into the groundwater. 
 
Such conditions are widely used to represent **dynamic interactions** between groundwater and surface water bodies.

**For this example, we consider the surface water to be a river that is separated from the groundwater by a  layer that has been clogged with fine particles and thus has low permeability. Flow on the left side is 0 m³/s, head of the river is 150 m, *K* of the aquifer is 5 x 10⁻⁵ m/s, and conductance of the river bed is 9 x 10⁻⁶ m²/s while the user varies recharge to be zero or +/- 250 mm/yr (i.e., +/- 8 x 10⁻⁹ m³/s which is 250 mm/yr over the 2500 m long system).**

**The model calculates the hydraulic heads required to drive the selected recharge to the river for this hydraulic conductivity and river bed conductance.**
""")

intro_scenario1_block("Head-dep. flux")

# --- FINAL ASSESSMENT ---
def content_final_bc_intro():
    st.markdown("""#### 🧠 Final assessment""")
    st.info("These questions test your conceptual understanding after working with the application.")
    
    # Render questions in a 2x4 grid (row-wise)
    for row in [(0, 1), (2, 3), (4, 5),(6, 7)]:
        col1, col2 = st.columns(2)

        with col1:
            i = row[0]
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )

        with col2:
            i = row[1]
            st.markdown(f"**Q{i+1}. {quest_final[i]['question']}**")
            multiple_choice(
                question=" ",
                options_dict=quest_final[i]["options"],
                success=quest_final[i].get("success", "✅ Correct."),
                error=quest_final[i].get("error", "❌ Not quite.")
            )
            
# Render final assessment
render_toggle_container(
    section_id="bc_intro01",
    label="✅ **Show the final assessment** - to self-check your **understanding**",
    content_fn=content_final_bc_intro,
    default_open=False,
)
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((4,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('06_Groundwater_modeling/FIGS/CC_BY-SA_icon.png')