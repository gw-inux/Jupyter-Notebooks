# app_rectangular_chd_recharge.py

import shutil
import tempfile
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import flopy


st.set_page_config(page_title="MODFLOW-NWT rectangular recharge model")

st.title("Rectangular unconfined aquifer with recharge and CHD boundary")

st.markdown(
    """
    This app builds a simple steady-state **MODFLOW-NWT** model with:

    - one unconfined aquifer layer
    - recharge over the full model domain
    - one specified-head boundary at the eastern edge
    - optional pumping well
    """
)

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def make_package_registry(active_wel=False):
    """
    Registry for all packages that should appear in the water budget.
    Names must match MODFLOW listing-file budget names.
    """
    packages = [
        {
            "key": "Recharge",
            "label": "Recharge",
            "budget_in": "RECHARGE_IN",
            "budget_out": "RECHARGE_OUT",
        },
        {
            "key": "CHD",
            "label": "CHD",
            "budget_in": "CONSTANT_HEAD_IN",
            "budget_out": "CONSTANT_HEAD_OUT",
        },
    ]

    if active_wel:
        packages.append(
            {
                "key": "WEL",
                "label": "WEL",
                "budget_in": "WELLS_IN",
                "budget_out": "WELLS_OUT",
            }
        )

    return packages


def read_listing_budget(list_path, package_registry):
    """
    Read MODFLOW listing-file budget and return a standardized dictionary.
    """
    lst = flopy.utils.MfListBudget(str(list_path))
    incremental, cumulative = lst.get_dataframes()

    budget_df = incremental.iloc[-1]

    budget_values = {}

    for pkg in package_registry:
        key = pkg["key"]
        budget_values[f"{key} IN"] = budget_df.get(pkg["budget_in"], 0.0)
        budget_values[f"{key} OUT"] = budget_df.get(pkg["budget_out"], 0.0)

    budget_values["TOTAL IN"] = budget_df.get("TOTAL_IN", 0.0)
    budget_values["TOTAL OUT"] = budget_df.get("TOTAL_OUT", 0.0)
    budget_values["Percent discrepancy"] = budget_df.get("PERCENT_DISCREPANCY", np.nan)

    return budget_values


def make_boundary_features(nrow, ncol, delr, delc, active_wel=False, well_row=None, well_col=None):
    """
    Registry for map/preview plotting of active boundary features.
    Row and column numbers are user-facing 1-based indices.
    """
    features = []

    chd_cells = []
    for irow in range(1, nrow + 1):
        chd_cells.append((irow, ncol))

    features.append(
        {
            "key": "CHD",
            "label": "CHD",
            "cells": chd_cells,
            "marker": "s",
            "markersize": 5,
            "edgecolor": "red",
            "facecolor": "none",
        }
    )

    if active_wel:
        features.append(
            {
                "key": "WEL",
                "label": "WEL",
                "cells": [(well_row, well_col)],
                "marker": "o",
                "markersize": 7,
                "edgecolor": "black",
                "facecolor": "none",
            }
        )

    return features


def plot_boundary_features(ax, features, nrow, delr, delc):
    """
    Plot all registered boundary features.
    """
    plotted_labels = set()

    for feature in features:
        for row, col in feature["cells"]:
            x = (col - 0.5) * delr
            y = (nrow - row + 0.5) * delc

            label = feature["label"] if feature["label"] not in plotted_labels else None
            plotted_labels.add(feature["label"])

            ax.plot(
                x,
                y,
                marker=feature["marker"],
                markersize=feature["markersize"],
                markerfacecolor=feature["facecolor"],
                markeredgecolor=feature["edgecolor"],
                linestyle="None",
                label=label,
            )


def plot_model_grid(ax, nrow, ncol, delr, delc):
    """
    Plot model grid using direct matplotlib lines.
    """
    lx = ncol * delr
    ly = nrow * delc

    for xg in np.arange(0, lx + delr, delr):
        ax.plot([xg, xg], [0, ly], color="lightgray", linewidth=0.5)

    for yg in np.arange(0, ly + delc, delc):
        ax.plot([0, lx], [yg, yg], color="lightgray", linewidth=0.5)


def plot_budget_bar_chart(budget, package_registry):
    """
    Generic budget plot for all active packages.
    """
    labels = []
    values = []
    colors = []
    hatches = []

    for pkg in package_registry:
        key = pkg["key"]
        labels.append(f"{key} IN")
        values.append(budget[f"{key} IN"])
        colors.append("tab:blue")
        hatches.append("")

    for pkg in package_registry:
        key = pkg["key"]
        labels.append(f"{key} OUT")
        values.append(-budget[f"{key} OUT"])
        colors.append("tab:orange")
        hatches.append("")

    labels.extend(["Total IN", "Total OUT"])
    values.extend([budget["TOTAL IN"], -budget["TOTAL OUT"]])
    colors.extend(["tab:green", "tab:red"])
    hatches.extend(["//", "//"])

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, color=colors)

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Flow rate [m³/d]", fontsize=12)
    ax.set_title("Complete water budget from MODFLOW listing file", fontsize=12)
    ax.tick_params(axis="x", rotation=30)

    for bar, value in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()

        if value >= 0:
            ax.text(x, y * 1.01, f"{value:.2f}", ha="center", va="bottom", fontsize=11)
        else:
            ax.text(x, y * 1.01, f"{value:.2f}", ha="center", va="top", fontsize=11)

    return fig


def budget_markdown(budget, package_registry):
    """
    Generic budget summary text.
    """
    lines = ["**Numerical budget summary from listing file**", ""]

    for pkg in package_registry:
        key = pkg["key"]
        label = pkg["label"]
        lines.append(f"- {label} IN: `{budget[f'{key} IN']:.4f} m³/d`")
        lines.append(f"- {label} OUT: `{budget[f'{key} OUT']:.4f} m³/d`")

    lines.append(f"- Total IN: `{budget['TOTAL IN']:.4f} m³/d`")
    lines.append(f"- Total OUT: `{budget['TOTAL OUT']:.4f} m³/d`")
    lines.append(f"- Percent discrepancy: `{budget['Percent discrepancy']:.4e} %`")

    return "\n".join(lines)


# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "model_done" not in st.session_state:
    st.session_state.model_done = False

if "heads" not in st.session_state:
    st.session_state.heads = None

if "budget_values" not in st.session_state:
    st.session_state.budget_values = None

if "model_info" not in st.session_state:
    st.session_state.model_info = {}

if "last_model_signature" not in st.session_state:
    st.session_state.last_model_signature = None


# ------------------------------------------------------------
# Model input
# ------------------------------------------------------------
st.header("Model setup")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Discretization", expanded=True):
        ncol = st.number_input("Number of columns", value=25, min_value=1, step=1)
        nrow = st.number_input("Number of rows", value=21, min_value=1, step=1)
        delr = st.number_input("Cell size x [m]", value=100.0, min_value=1.0, step=10.0)
        delc = st.number_input("Cell size y [m]", value=100.0, min_value=1.0, step=10.0)
        top = st.number_input("Aquifer top [m]", value=20.0, step=1.0)
        botm = st.number_input("Aquifer bottom [m]", value=0.0, step=1.0)

with col2:
    with st.expander("Parameters and boundary conditions", expanded=True):
        hk = st.number_input("Hydraulic conductivity [m/d]", value=10.0, min_value=0.0001, step=1.0)
        recharge_mm_a = st.number_input("Recharge [mm/a]", value=200.0, min_value=0.0, step=10.0)
        chd_head = st.number_input("Specified head east [m]", value=16.0, step=0.5)

        active_wel = st.checkbox("Activate pumping well", value=False)

        if active_wel:
            well_row = st.number_input(
                "Well row #",
                min_value=1,
                max_value=nrow,
                value=int((nrow + 1) / 2),
                step=1,
            )

            well_col = st.number_input(
                "Well column #",
                min_value=1,
                max_value=ncol,
                value=int((ncol + 1) / 2),
                step=1,
            )

            well_rate_abs = st.number_input(
                "Abstraction rate [m³/d]",
                value=100.0,
                min_value=0.0,
                step=10.0,
            )

            well_rate = -well_rate_abs

        else:
            well_row = int((nrow + 1) / 2)
            well_col = int((ncol + 1) / 2)
            well_rate_abs = 0.0
            well_rate = 0.0

with col3:
    with st.expander("Model settings", expanded=True):
        exe_name = st.text_input(
            "MODFLOW-NWT executable",
            value="MODFLOW-NWT_64.exe",
        )

        workspace_location = st.radio(
            "Model workspace",
            ["User/system temp folder", "Local folder next to script"],
            index=0,
        )

        delete_workspace_before_run = st.checkbox(
            "Delete existing model workspace before run",
            value=True,
        )

recharge = recharge_mm_a / 1000.0 / 365.25  # mm/a -> m/d

package_registry = make_package_registry(active_wel=active_wel)
boundary_features = make_boundary_features(
    nrow=nrow,
    ncol=ncol,
    delr=delr,
    delc=delc,
    active_wel=active_wel,
    well_row=well_row,
    well_col=well_col,
)


# ------------------------------------------------------------
# Model signature
# ------------------------------------------------------------
current_model_signature = {
    "ncol": int(ncol),
    "nrow": int(nrow),
    "delr": float(delr),
    "delc": float(delc),
    "top": float(top),
    "botm": float(botm),
    "hk": float(hk),
    "recharge_mm_a": float(recharge_mm_a),
    "chd_head": float(chd_head),
    "exe_name": exe_name,
    "active_wel": bool(active_wel),
    "well_row": int(well_row),
    "well_col": int(well_col),
    "well_rate": float(well_rate),
}


# ------------------------------------------------------------
# Workspace
# ------------------------------------------------------------
modelname = "rect_chd_rch_nwt"

if workspace_location == "User/system temp folder":
    base_ws = Path(tempfile.gettempdir())
else:
    base_ws = Path(__file__).parent

ws = base_ws / "flopy_rect_chd_rch_nwt"


# Clear old results if model input was modified
if (
    st.session_state.last_model_signature is not None
    and current_model_signature != st.session_state.last_model_signature
):
    st.session_state.model_done = False
    st.session_state.heads = None
    st.session_state.budget_values = None
    st.session_state.model_info = {}


# ------------------------------------------------------------
# Model setup preview
# ------------------------------------------------------------
show_model_preview = st.toggle(
    "Show model setup preview",
    value=True,
)

if show_model_preview:

    st.subheader("Model setup preview")

    fig_prev, ax_prev = plt.subplots(figsize=(7, 5))

    lx = ncol * delr
    ly = nrow * delc

    plot_model_grid(ax_prev, nrow, ncol, delr, delc)
    plot_boundary_features(ax_prev, boundary_features, nrow, delr, delc)

    ax_prev.set_aspect("equal")
    ax_prev.set_xlim(0, lx)
    ax_prev.set_ylim(0, ly)
    ax_prev.set_xlabel("x [m]")
    ax_prev.set_ylabel("y [m]")
    ax_prev.set_title("Model grid and active boundary conditions")
    ax_prev.legend(loc="upper right")

    st.pyplot(fig_prev)

    st.markdown("#### Model information")

    with st.expander("Show the model information"):

        st.markdown(
            f"""
            **Grid**

            - Rows: `{nrow}`
            - Columns: `{ncol}`
            - Cell size x: `{delr:.2f} m`
            - Cell size y: `{delc:.2f} m`
            - Model length x: `{ncol * delr:.2f} m`
            - Model length y: `{nrow * delc:.2f} m`

            **Aquifer**

            - Layers: `1`
            - Aquifer type: `unconfined`
            - Top elevation: `{top:.2f} m`
            - Bottom elevation: `{botm:.2f} m`
            - Hydraulic conductivity K: `{hk:.4g} m/d`

            **Boundary conditions**

            - CHD boundary: `eastern model boundary`
            - CHD head: `{chd_head:.2f} m`
            - Recharge: `{recharge_mm_a:.2f} mm/a`
            - Recharge: `{recharge:.4e} m/d`

            **Well**

            - Well active: `{active_wel}`
            - Well row: `{well_row}`
            - Well column: `{well_col}`
            - Abstraction rate: `{well_rate_abs:.2f} m³/d`

            **Time discretization**

            - MODFLOW version: `MODFLOW-NWT`
            - Stress periods: `1`
            - Period length: `1.0 d`
            - Time steps: `1`
            - Simulation type: `steady state`
            """
        )


# ------------------------------------------------------------
# Run model
# ------------------------------------------------------------
if st.button("Run MODFLOW-NWT model"):

    if delete_workspace_before_run and ws.exists():
        shutil.rmtree(ws)

    ws.mkdir(parents=True, exist_ok=True)

    mf = flopy.modflow.Modflow(
        modelname,
        exe_name=exe_name,
        model_ws=str(ws),
        version="mfnwt",
    )

    nlay = 1
    nper = 1

    # DIS
    flopy.modflow.ModflowDis(
        mf,
        nlay=nlay,
        nrow=nrow,
        ncol=ncol,
        delr=delr,
        delc=delc,
        top=top,
        botm=botm,
        nper=nper,
        perlen=[1.0],
        nstp=[1],
        steady=[True],
    )

    # BAS
    ibound = np.ones((nlay, nrow, ncol), dtype=int)
    strt = np.full((nlay, nrow, ncol), chd_head)

    flopy.modflow.ModflowBas(
        mf,
        ibound=ibound,
        strt=strt,
    )

    # UPW: unconfined aquifer
    flopy.modflow.ModflowUpw(
        mf,
        laytyp=1,
        hk=hk,
        vka=hk,
        ipakcb=53,
    )

    # CHD at eastern boundary
    chd_spd = []
    for irow in range(nrow):
        chd_spd.append([0, irow, ncol - 1, chd_head, chd_head])

    flopy.modflow.ModflowChd(
        mf,
        stress_period_data={0: chd_spd},
    )

    # Recharge over full domain
    flopy.modflow.ModflowRch(
        mf,
        rech=recharge,
        ipakcb=53,
    )

    # Optional pumping well
    if active_wel:
        wel_spd = {
            0: [
                [0, well_row - 1, well_col - 1, well_rate]
            ]
        }

        flopy.modflow.ModflowWel(
            mf,
            stress_period_data=wel_spd,
            ipakcb=53,
        )

    # Solver
    flopy.modflow.ModflowNwt(
        mf,
        headtol=1e-6,
        fluxtol=500,
        maxiterout=100,
        linmeth=1,
        options="SIMPLE",
    )

    # Output control
    flopy.modflow.ModflowOc(
        mf,
        stress_period_data={
            (0, 0): ["save head", "save budget", "print budget"]
        },
        compact=True,
    )

    mf.write_input()
    success, buff = mf.run_model(silent=True)

    if not success:
        st.error("MODFLOW-NWT did not terminate normally.")
        st.text("\n".join(buff[-20:]))
        st.stop()

    # Read heads
    hds_path = ws / f"{modelname}.hds"
    headobj = flopy.utils.HeadFile(str(hds_path))
    heads = headobj.get_data(kstpkper=(0, 0))[0]

    # Read budget
    list_path = ws / f"{modelname}.list"
    budget_values = read_listing_budget(list_path, package_registry)

    # Store results
    st.session_state.model_done = True
    st.session_state.heads = heads
    st.session_state.last_model_signature = current_model_signature
    st.session_state.budget_values = budget_values

    st.session_state.model_info = {
        "nrow": nrow,
        "ncol": ncol,
        "delr": delr,
        "delc": delc,
        "top": top,
        "botm": botm,
        "chd_head": chd_head,
        "workspace": str(ws),
        "active_wel": active_wel,
        "well_row": well_row,
        "well_col": well_col,
        "well_rate": well_rate,
        "well_rate_abs": well_rate_abs,
        "package_registry": package_registry,
        "boundary_features": boundary_features,
    }

    col_note1, col_note2 = st.columns(2)

    with col_note1:
        st.success("MODFLOW-NWT model finished successfully.")

    with col_note2:
        st.info(f"Model files written to: `{ws}`")


# ------------------------------------------------------------
# Post-processing
# ------------------------------------------------------------
if st.session_state.model_done:

    heads = st.session_state.heads
    budget = st.session_state.budget_values
    info = st.session_state.model_info

    nrow = info["nrow"]
    ncol = info["ncol"]
    delr = info["delr"]
    delc = info["delc"]
    top = info["top"]
    botm = info["botm"]

    active_wel = info["active_wel"]
    well_row = info["well_row"]
    well_col = info["well_col"]

    package_registry = info["package_registry"]
    boundary_features = info["boundary_features"]

    # ------------------------------------------------------------
    # Cross-section controls
    # ------------------------------------------------------------
    st.header("Hydraulic heads and cross sections")

    col_sec1, col_sec2, col_sec3 = st.columns(3)

    with col_sec1:
        show_horizontal = st.checkbox(
            "Show horizontal W-E section",
            value=True,
        )

        show_vertical = st.checkbox(
            "Show vertical N-S section",
            value=False,
        )

    with col_sec2:
        selected_row = st.number_input(
            "Row # for W-E section",
            min_value=1,
            max_value=nrow,
            value=int((nrow + 1) / 2),
            step=1,
        )

    with col_sec3:
        selected_col = st.number_input(
            "Column # for N-S section",
            min_value=1,
            max_value=ncol,
            value=int((ncol + 1) / 2),
            step=1,
        )

    # ------------------------------------------------------------
    # Head plot
    # ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    x_edges = np.linspace(0, ncol * delr, ncol + 1)
    y_edges = np.linspace(0, nrow * delc, nrow + 1)

    c = ax.pcolormesh(
        x_edges,
        y_edges,
        heads[::-1, :],
        shading="auto",
    )

    if nrow >= 2 and ncol >= 2:
        x = np.linspace(delr / 2, ncol * delr - delr / 2, ncol)
        y = np.linspace(delc / 2, nrow * delc - delc / 2, nrow)
        X, Y = np.meshgrid(x, y)

        contours = ax.contour(
            X,
            Y,
            heads[::-1, :],
            colors="black",
            linewidths=0.6,
        )
        ax.clabel(contours, fmt="%.2f", fontsize=8)

    plot_model_grid(ax, nrow, ncol, delr, delc)
    plot_boundary_features(ax, boundary_features, nrow, delr, delc)

    # Mark selected horizontal west-east section
    if show_horizontal:
        y_section = (nrow - selected_row + 0.5) * delc
        ax.plot(
            [0, ncol * delr],
            [y_section, y_section],
            linewidth=2.5,
            linestyle="-",
            label=f"W-E section, row {selected_row}",
        )

    # Mark selected vertical north-south section
    if show_vertical:
        x_section = (selected_col - 0.5) * delr
        ax.plot(
            [x_section, x_section],
            [0, nrow * delc],
            linewidth=2.5,
            linestyle="--",
            label=f"N-S section, column {selected_col}",
        )

    ax.set_aspect("equal")
    ax.set_xlim(0, ncol * delr)
    ax.set_ylim(0, nrow * delc)

    ax.set_title("Simulated hydraulic head [m]")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")

    ax.legend(loc="upper right")

    fig.colorbar(c, ax=ax, label="Head [m]")
    st.pyplot(fig)

    # ------------------------------------------------------------
    # Cross-section plot(s)
    # ------------------------------------------------------------
    if show_horizontal or show_vertical:

        st.subheader("Cross-section plots")

        if show_horizontal:
            irow = selected_row - 1
            x = (np.arange(ncol) + 0.5) * delr
            h = heads[irow, :]

            fig_h, ax_h = plt.subplots(figsize=(8, 4))

            ax_h.plot(x, h, marker="o", label="Hydraulic head")
            ax_h.plot([x[0], x[-1]], [top, top], linestyle="--", label="Aquifer top")
            ax_h.plot([x[0], x[-1]], [botm, botm], linestyle="--", label="Aquifer bottom")

            ax_h.set_title(f"Horizontal west-east cross section, row {selected_row}")
            ax_h.set_xlabel("x [m]")
            ax_h.set_ylabel("Elevation / head [m]")
            ax_h.grid(True, alpha=0.3)
            ax_h.legend()

            st.pyplot(fig_h)

        if show_vertical:
            icol = selected_col - 1
            y = (np.arange(nrow) + 0.5) * delc
            h = heads[::-1, icol]

            fig_v, ax_v = plt.subplots(figsize=(8, 4))

            ax_v.plot(y, h, marker="o", label="Hydraulic head")
            ax_v.plot([y[0], y[-1]], [top, top], linestyle="--", label="Aquifer top")
            ax_v.plot([y[0], y[-1]], [botm, botm], linestyle="--", label="Aquifer bottom")

            ax_v.set_title(f"Vertical north-south cross section, column {selected_col}")
            ax_v.set_xlabel("y [m]")
            ax_v.set_ylabel("Elevation / head [m]")
            ax_v.grid(True, alpha=0.3)
            ax_v.legend()

            st.pyplot(fig_v)

    # ------------------------------------------------------------
    # Water budget
    # ------------------------------------------------------------
    st.header("Water budget")

    fig_budget = plot_budget_bar_chart(budget, package_registry)
    st.pyplot(fig_budget)

    st.markdown(budget_markdown(budget, package_registry))