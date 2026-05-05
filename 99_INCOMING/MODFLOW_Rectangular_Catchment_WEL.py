# app_rectangular_chd_recharge.py

import os
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
    - 25 columns in x-direction
    - 21 rows in y-direction
    - recharge over the full model domain
    - one specified-head boundary at the eastern edge
    """
)

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
    # Grid
    for xg in np.arange(0, lx + delr, delr):
        ax_prev.plot([xg, xg], [0, ly], color="lightgray", linewidth=0.5)
    for yg in np.arange(0, ly + delc, delc):
        ax_prev.plot([0, lx], [yg, yg], color="lightgray", linewidth=0.5)
        
    # CHD cells along eastern boundary
    for irow in range(nrow):
        x_chd = (ncol - 0.5) * delr
        y_chd = (nrow - irow - 0.5) * delc
        ax_prev.plot(
            x_chd,
            y_chd,
            "s",
            markersize=5,
            markerfacecolor="none",
            markeredgecolor="red",
            label="CHD" if irow == 0 else None,
        )
        
    if active_wel:
        x_well = (well_col - 0.5) * delr
        y_well = (nrow - well_row + 0.5) * delc
    
        ax_prev.plot(
            x_well,
            y_well,
            "o",
            markersize=7,
            markerfacecolor="none",
            markeredgecolor="black",
            label="WEL",
        )
    
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
            - **Well**
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

    # CHD at eastern boundary, last column
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
    
    st.session_state.model_done = True
    st.session_state.heads = heads
    st.session_state.last_model_signature = current_model_signature

    # ------------------------------------------------------------
    # Read budget from listing file
    # ------------------------------------------------------------
    list_path = ws / f"{modelname}.list"
    
    lst = flopy.utils.MfListBudget(str(list_path))
    incremental, cumulative = lst.get_dataframes()
    
    # Get final steady-state budget row
    budget_df = incremental.iloc[-1]
    
    # MODFLOW listing file names are usually uppercase
    rch_in = budget_df.get("RECHARGE_IN", 0.0)
    rch_out = budget_df.get("RECHARGE_OUT", 0.0)
    
    chd_in = budget_df.get("CONSTANT_HEAD_IN", 0.0)
    chd_out = budget_df.get("CONSTANT_HEAD_OUT", 0.0)
    
    if active_wel:
        wel_in = budget_df.get("WELLS_IN", 0.0)
        wel_out = budget_df.get("WELLS_OUT", 0.0)
    
    total_in = budget_df.get("TOTAL_IN", 0.0)
    total_out = budget_df.get("TOTAL_OUT", 0.0)
    percent_discrepancy = budget_df.get("PERCENT_DISCREPANCY", np.nan)
    
    # Store results
    
    if active_wel:
        st.session_state.budget_values = {
            "Recharge IN": rch_in,
            "Recharge OUT": rch_out,
            "CHD IN": chd_in,
            "CHD OUT": chd_out,
            "WEL IN": wel_in,
            "WEL OUT": wel_out,
            "TOTAL IN": total_in,
            "TOTAL OUT": total_out,
            "Percent discrepancy": percent_discrepancy,
        }
        
    else:
        st.session_state.budget_values = {
            "Recharge IN": rch_in,
            "Recharge OUT": rch_out,
            "CHD IN": chd_in,
            "CHD OUT": chd_out,
            "TOTAL IN": total_in,
            "TOTAL OUT": total_out,
            "Percent discrepancy": percent_discrepancy,
        }
    
    
    st.session_state.model_info = {
        "nrow": nrow,
        "ncol": ncol,
        "delr": delr,
        "delc": delc,
        "top": top,
        "botm": botm,
        "chd_head": chd_head,
        "workspace": str(ws),
        "activate_well": active_wel,
        "well_row": well_row,
        "well_col": well_col,
        "well_rate": well_rate,
        "well_rate_abs": well_rate_abs,
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
    info = st.session_state.model_info

    nrow = info["nrow"]
    ncol = info["ncol"]
    delr = info["delr"]
    delc = info["delc"]
    top = info["top"]
    botm = info["botm"]
    if active_wel:
        active_wel = info["activate_well"]
        well_row = info["well_row"]
        well_col = info["well_col"]
        well_rate_abs = info["well_rate_abs"]

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
    
    # Contours only work for true 2D grids
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
    
    # Plot grid
    for xg in np.arange(0, ncol * delr + delr, delr):
        ax.plot([xg, xg], [0, nrow * delc], color="lightgray", linewidth=0.5)
    
    for yg in np.arange(0, nrow * delc + delc, delc):
        ax.plot([0, ncol * delr], [yg, yg], color="lightgray", linewidth=0.5)
    
    # Mark CHD cells at eastern boundary
    for irow in range(nrow):
        x_chd = (ncol - 0.5) * delr
        y_chd = (nrow - irow - 0.5) * delc
        ax.plot(
            x_chd,
            y_chd,
            "s",
            markersize=4,
            markerfacecolor="none",
            markeredgecolor="red",
        )
    
    if active_wel:
        x_well = (well_col - 0.5) * delr
        y_well = (nrow - well_row + 0.5) * delc
    
        ax.plot(
            x_well,
            y_well,
            "o",
            markersize=7,
            markerfacecolor="none",
            markeredgecolor="black",
            label="WEL",
        )
    
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
    
    if show_horizontal or show_vertical:
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
    
    budget = st.session_state.budget_values
    
    if active_wel:
        labels = [
            "Recharge IN",
            "CHD IN",
            "WEL IN",
            "Recharge OUT",
            "CHD OUT",
            "WEL OUT",
            "Total IN",
            "Total OUT",
        ]
        values = [
            budget["Recharge IN"],
            budget["CHD IN"],
            budget["WEL IN"],
            -budget["Recharge OUT"],
            -budget["CHD OUT"],
            -budget["WEL OUT"],
            budget["TOTAL IN"],
            -budget["TOTAL OUT"],
        ]
        # Define colors
        colors = [
            "tab:blue",
            "tab:blue",
            "tab:blue",
            "tab:orange",
            "tab:orange",
            "tab:orange",
            "tab:green",
            "tab:red",
        ]
        
        hatches = ["", "", "", "", "", "", "//", "//"]
    else:
        labels = [
            "Recharge IN",
            "CHD IN",
            "Recharge OUT",
            "CHD OUT",
            "Total IN",
            "Total OUT",
        ]
        values = [
            budget["Recharge IN"],
            budget["CHD IN"],
            -budget["Recharge OUT"],
            -budget["CHD OUT"],
            budget["TOTAL IN"],
            -budget["TOTAL OUT"],
        ]
        # Define colors
        colors = [
            "tab:blue",   # Recharge IN
            "tab:blue",   # CHD IN
            "tab:orange", # Recharge OUT
            "tab:orange", # CHD OUT
            "tab:green",  # Total IN
            "tab:red",    # Total OUT
        ]
        hatches = ["", "", "", "", "//", "//"]
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))

    bars = ax2.bar(labels, values, color=colors)
    
    # Apply hatching only to TOTAL bars
    
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
        
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("Flow rate [m³/d]", fontsize=12)
    ax2.set_title("Complete water budget from MODFLOW listing file", fontsize=12)
    
    ax2.tick_params(axis="x", rotation=30)
    
    # Add values above / below bars
    for bar, value in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
    
        if value >= 0:
            ax2.text(
                x,
                y*1.01,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=11,
            )
        else:
            ax2.text(
                x,
                y*1.01,
                f"{value:.2f}",
                ha="center",
                va="top",
                fontsize=11,
            )
    
    st.pyplot(fig2)
    
    if active_wel:
            st.markdown(
                f"""
                **Numerical budget summary from listing file**
            
                - Recharge IN: `{budget["Recharge IN"]:.4f} m³/d`
                - Recharge OUT: `{budget["Recharge OUT"]:.4f} m³/d`
                - CHD IN: `{budget["CHD IN"]:.4f} m³/d`
                - CHD OUT: `{budget["CHD OUT"]:.4f} m³/d`
                - WEL IN: `{budget["WEL IN"]:.4f} m³/d`
                - WEL OUT: `{budget["WEL OUT"]:.4f} m³/d`
                - Total IN: `{budget["TOTAL IN"]:.4f} m³/d`
                - Total OUT: `{budget["TOTAL OUT"]:.4f} m³/d`
                - Percent discrepancy: `{budget["Percent discrepancy"]:.4e} %`
                """
            )
    else:
        
        st.markdown(
            f"""
            **Numerical budget summary from listing file**
        
            - Recharge IN: `{budget["Recharge IN"]:.4f} m³/d`
            - Recharge OUT: `{budget["Recharge OUT"]:.4f} m³/d`
            - CHD IN: `{budget["CHD IN"]:.4f} m³/d`
            - CHD OUT: `{budget["CHD OUT"]:.4f} m³/d`
            - Total IN: `{budget["TOTAL IN"]:.4f} m³/d`
            - Total OUT: `{budget["TOTAL OUT"]:.4f} m³/d`
            - Percent discrepancy: `{budget["Percent discrepancy"]:.4e} %`
            """
        )