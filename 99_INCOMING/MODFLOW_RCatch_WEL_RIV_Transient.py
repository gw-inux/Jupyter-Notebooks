import shutil
import tempfile
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import flopy


st.set_page_config(page_title="iMODEL pumping")

st.title(":rainbow[iMODEL] - Pumping from an idealized catchment")

st.markdown(
    """
    This app builds a simple transient **MODFLOW-NWT** model with:

    - one confined aquifer layer
    - recharge over the full model domain
    - one specified-head boundary at the eastern edge
    - pumping well
    - optional river
    """
)

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def make_package_registry(active_wel=False, active_riv=False, active_transient=False):
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
        
    if active_riv:
        packages.append({
            "key": "RIV",
            "label": "RIV",
            "budget_in": "RIVER_LEAKAGE_IN",
            "budget_out": "RIVER_LEAKAGE_OUT",
        })
        
    if active_transient:   
        packages.append({        
            "key": "Storage",
            "label": "Storage",
            "budget_in": "STORAGE_IN",
            "budget_out": "STORAGE_OUT",
        })

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

def make_boundary_features(nrow, ncol, wel_cells=None, riv_cells=None):
    """
    Define active boundary features for plotting.
    Row and column numbers are user-facing 1-based indices.
    """

    features = []

    # CHD is always active at eastern boundary
    chd_cells = [(row, ncol) for row in range(1, nrow + 1)]

    features.append({
        "key": "CHD",
        "label": "CHD",
        "cells": chd_cells,
        "marker": "s",
        "markersize": 3,
        "edgecolor": "red",
        "facecolor": "none",
        "linecolor": "red",
    })

    if wel_cells is not None:
        features.append({
            "key": "WEL",
            "label": "WEL",
            "cells": wel_cells,
            "marker": "o",
            "markersize": 4,
            "edgecolor": "black",
            "facecolor": "none",
            "linecolor": "black",
        })

    if riv_cells is not None:
        features.append({
            "key": "RIV",
            "label": "RIV",
            "cells": riv_cells,
            "marker": "^",
            "markersize": 3,
            "edgecolor": "blue",
            "facecolor": "none",
            "linecolor": "blue",
        })

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
        ax.plot([xg, xg], [0, ly], color="silver", linewidth=0.5, alpha=0.4)

    for yg in np.arange(0, ly + delc, delc):
        ax.plot([0, lx], [yg, yg], color="silver", linewidth=0.5, alpha=0.4)

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
    ax.tick_params(axis="x", rotation=90)

    for bar, value in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()

        if value >= 0:
            ax.text(x, y * 1.01, f"{value:.0f}", ha="center", va="bottom", fontsize=11)
        else:
            ax.text(x, y * 1.01, f"{value:.0f}", ha="center", va="top", fontsize=11)

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

def make_particle_source_registry(boundary_features):
    sources = []

    for feature in boundary_features:
        sources.append(
            {
                "key": feature["key"],
                "label": feature["label"],
                "cells": feature["cells"],
            }
        )

    return sources
    
def make_circular_particle_offsets(n_particles, radius=0.25):
    """
    Return local MODPATH particle coordinates inside one cell.
    Coordinates are between 0 and 1.
    """
    if n_particles == 1:
        return [(0.5, 0.5)]

    offsets = [(0.5, 0.5)]

    n_ring = n_particles - 1
    angles = np.linspace(0, 2 * np.pi, n_ring, endpoint=False)

    for angle in angles:
        lx = 0.5 + radius * np.cos(angle)
        ly = 0.5 + radius * np.sin(angle)
        offsets.append((lx, ly))

    return offsets

def run_modpath_from_existing_model(
    ws,
    modelname,
    mp_exe_name,
    tracking_direction,
    particles_per_cell,
    selected_particle_sources,
    particle_sources,
    porosity=0.30,
):
    """
    Run MODPATH 7 from an existing MODFLOW-NWT model.
    MODFLOW is not rerun.
    """

    ws = Path(ws)
    mp_name = f"{modelname}_mp"

    mf_loaded = flopy.modflow.Modflow.load(
        f"{modelname}.nam",
        model_ws=str(ws),
        exe_name=None,
        version="mfnwt",
        check=False,
        forgive=False,
    )

    mp = flopy.modpath.Modpath7(
        modelname=mp_name,
        flowmodel=mf_loaded,
        exe_name=mp_exe_name,
        model_ws=str(ws),
    )

    flopy.modpath.Modpath7Bas(
        mp,
        porosity=porosity,
    )

    # Build particle locations
    partlocs = []
    localx = []
    localy = []
    localz = []
    
    particle_offsets = make_circular_particle_offsets(
        particles_per_cell,
        radius=0.25,
    )
    
    particle_source_lookup = {}
    particle_id = 0
    
    for src in particle_sources:
        if src["key"] in selected_particle_sources:
            for row, col in src["cells"]:
                for lx, ly in particle_offsets:
                    partlocs.append((0, row - 1, col - 1))
                    localx.append(lx)
                    localy.append(ly)
                    localz.append(0.5)
    
                    particle_source_lookup[particle_id] = src["key"]
                    particle_id += 1
    
    particle_data = flopy.modpath.ParticleData(
        partlocs,
        structured=True,
        localx=localx,
        localy=localy,
        localz=localz,
        drape=0,
    )

    selected_cells = []

    for src in particle_sources:
        if src["key"] in selected_particle_sources:
            selected_cells.extend(src["cells"])

    for src in particle_sources:
        if src["key"] in selected_particle_sources:
            for row, col in src["cells"]:
                for lx, ly in particle_offsets:
                    partlocs.append((0, row - 1, col - 1))
                    localx.append(lx)
                    localy.append(ly)
                    localz.append(0.5)
    
                    particle_source_lookup[particle_id] = src["key"]
                    particle_id += 1

    particle_group = flopy.modpath.ParticleGroup(
        particlegroupname="boundary_particles",
        particledata=particle_data,
        filename=f"{mp_name}.sloc",
    )

    flopy.modpath.Modpath7Sim(
        mp,
        simulationtype="pathline",
        trackingdirection=tracking_direction.lower(),
        weaksinkoption="pass_through",
        weaksourceoption="pass_through",
        budgetoutputoption="summary",
        particlegroups=[particle_group],
    )

    mp.write_input()
    success, buff = mp.run_model(silent=True)

    if not success:
        raise RuntimeError("MODPATH did not terminate normally:\n" + "\n".join(buff[-20:]))

    pathline_file = ws / f"{mp_name}.mppth"
    pth = flopy.utils.PathlineFile(str(pathline_file))
    pathlines = pth.get_alldata()

    return pathlines, particle_source_lookup

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

if "pathlines" not in st.session_state:
    st.session_state.pathlines = None
    
if "particle_source_lookup" not in st.session_state:
    st.session_state.particle_source_lookup = None

if "transient_head_ts" not in st.session_state:
    st.session_state.transient_head_ts = None

if "transient_head_csv" not in st.session_state:
    st.session_state.transient_head_csv = None


# ------------------------------------------------------------
# Model input
# ------------------------------------------------------------
st.header("Model setup")

with st.expander("Model settings", expanded=True):
    exe_name = st.text_input("MODFLOW-NWT executable", value="MODFLOW-NWT_64.exe")
    workspace_location = st.radio(
        "Model workspace",
        ["User/system temp folder", "Local folder next to script"],
        index=0,
    )
    delete_workspace_before_run = st.checkbox(
        "Delete existing model workspace before run",
        value=True,
    )

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Discretization", expanded=True):
        ncol = st.number_input("Number of columns", value=61, min_value=1, step=1)
        nrow = st.number_input("Number of rows", value=61, min_value=1, step=1)
        delr = st.number_input("Cell size x [m]", value=50, min_value=1, step=10)
        delc = st.number_input("Cell size y [m]", value=50, min_value=1, step=10)
        #top = st.number_input("Aquifer top [m]", value=20.0, step=1.0)
        top = 10
        #botm = st.number_input("Aquifer bottom [m]", value=0.0, step=1.0)
        botm = 0
        
    active_transient = st.toggle("Run transient simulation", value=False)
    
    if active_transient:
        with st.expander("Transient settings", expanded=True):
            transient_perlen = st.number_input(
                "Transient period length [d]",
                min_value=1.0,
                value=3.0,
                step=1.0,
            )
    
            transient_nstp = st.number_input(
                "Number of time steps",
                min_value=1,
                value=72,
                step=1,
            )
    
            transient_tsmult = st.number_input(
                "Time step multiplier",
                min_value=1.0,
                value=1.05,
                step=0.1,
            )
    else:
        transient_perlen = 1.0
        transient_nstp = 1
        transient_tsmult = 1.0

with col2:
    with st.expander("Parameters and boundary conditions", expanded=True):
        #hk = st.number_input("Hydraulic conductivity [m/d]", value=50.0, min_value=0.0001, step=1.0)
        hk_mps = st.number_input(
            "Hydraulic conductivity [m/s]",
            value=1e-4,
            min_value=1e-6,
            format="%.2e",
        )
        
        hk = hk_mps * 86400.0
        recharge_mm_a = st.number_input("Recharge [mm/a]", value=50.0, min_value=0.0, step=10.0)
        chd_head = st.number_input("Specified head east [m]", value=26.0, min_value=11.0, step=0.1)
        sy = 0.25
        #ss = 1e-5
        ss = st.number_input("Specific storage [1/m]", value=1e-4, format="%.1e")

with col3:
    
    active_wel = st.checkbox("Activate pumping well", value=False)
    active_riv = st.checkbox("Activate river boundary", value=False)
    
    wel_cells = None
    riv_cells = None

    if active_wel:
        with st.expander("Setup WEL"):
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
                value=int((ncol + 1) / 2)+10,
                step=1,
            )
            if active_transient:
                well_rate_abs_steady = st.number_input(
                    "Abstraction rate during initial steady period [m³/d]",
                    value=0.0,
                    min_value=0.0,
                    step=10.0,
                )
            
                well_rate_abs_transient = st.number_input(
                    "Abstraction rate during transient period [m³/d]",
                    value=1000.0,
                    min_value=0.0,
                    step=10.0,
                )
            
                well_rate_steady = -well_rate_abs_steady
                well_rate_transient = -well_rate_abs_transient
            
            else:
                well_rate_abs = st.number_input(
                    "Abstraction rate [m³/d]",
                    value=1000.0,
                    min_value=0.0,
                    step=10.0,
                )
                well_rate = -well_rate_abs
            wel_cells = [(well_row, well_col)]
    
    if active_riv:
        with st.expander("Setup RIV"):
            river_row = st.number_input(
                "River row #",
                min_value=1,
                max_value=nrow,
                value=int((nrow + 1) / 2)+4,
                step=1,
            )
        
            river_length_cols = st.number_input(
                "River length [number of columns]",
                min_value=1,
                max_value=ncol,
                value=ncol,
                step=1,
            )
        
            river_gradient = st.number_input(
                "River head gradient [m/m]",
                value=0.0001,
                min_value=0.0,
                step=0.00001,
                format="%.5f",
            )
        
            riverbed_offset = st.number_input(
                "River bottom below river head [m]",
                value=1.0,
                min_value=0.0,
                step=0.1,
            )
        
            river_conductance = st.number_input(
                "River conductance per cell [m²/d]",
                value=5.0,
                min_value=0.0,
                step=10.0,
            )
            
        riv_cells = []

        if active_riv:
            river_start_col = ncol - river_length_cols + 1
            river_end_col = ncol
        
            riv_cells = [
                (river_row, col)
                for col in range(river_start_col, river_end_col + 1)
            ]
            
    with st.expander("Observation point"):
        obs_row = st.number_input(
            "Observation row #",
            min_value=1,
            max_value=nrow,
            value=int((nrow + 1) / 2),
            step=1,
        )
    
        obs_col = st.number_input(
            "Observation column #",
            min_value=1,
            max_value=ncol,
            value=max(1, int((ncol+1)/2)+12 ),
            step=1,
        )

recharge = recharge_mm_a / 1000.0 / 365.25  # mm/a -> m/d

package_registry = make_package_registry(
    active_wel=active_wel,
    active_riv=active_riv,
    active_transient=active_transient,
)

boundary_features = make_boundary_features(
    nrow=nrow,
    ncol=ncol,
    wel_cells=wel_cells,
    riv_cells=riv_cells,
)

# ------------------------------------------------------------
# Observation point feature
# ------------------------------------------------------------
obs_cells = [(obs_row, obs_col)]

boundary_features.append({
    "key": "OBS",
    "label": "OBS",
    "cells": obs_cells,
    "marker": "x",
    "markersize": 4,
    "edgecolor": "purple",
    "facecolor": "purple",
    "linecolor": "purple",
})

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
    "active_riv": bool(active_riv),
    "active_transient": bool(active_transient),
    "obs_row": int(obs_row),
    "obs_col": int(obs_col),
}

if active_wel:
    current_model_signature.update({
        "well_row": int(well_row),
        "well_col": int(well_col),
    })
    if active_transient:
        current_model_signature.update({
            "well_rate_steady": float(well_rate_steady),
            "well_rate_transient": float(well_rate_transient),
        })
    else:
        current_model_signature.update({
            "well_rate": float(well_rate),
        })

if active_riv:
    current_model_signature.update({
        "river_row": int(river_row),
        "river_length_cols": int(river_length_cols),
        "river_gradient": float(river_gradient),
        "riverbed_offset": float(riverbed_offset),
        "river_conductance": float(river_conductance),
    })
    
if active_transient:
    current_model_signature.update({
        "transient_perlen": float(transient_perlen),
        "transient_nstp": int(transient_nstp),
        "transient_tsmult": float(transient_tsmult),
    })

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
    st.session_state.particle_source_lookup = None
    st.session_state.budget_values = None
    st.session_state.model_info = {}
    st.session_state.pathlines = None
    st.session_state.transient_head_ts = None
    st.session_state.transient_head_csv = None


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

        model_info_text = f"""
        **Grid**
        
        - Rows: `{nrow}`
        - Columns: `{ncol}`
        - Cell size x: `{delr:.2f} m`
        - Cell size y: `{delc:.2f} m`
        - Model length x: `{ncol * delr:.2f} m`
        - Model length y: `{nrow * delc:.2f} m`
        
        **Aquifer**
        
        - Layers: `1`
        - Aquifer type: `confined`
        - Top elevation: `{top:.2f} m`
        - Bottom elevation: `{botm:.2f} m`
        - Aquifer thickness: `{top - botm:.2f} m`
        - Hydraulic conductivity K: `{hk:.4g} m/d`
        
        **Boundary conditions**
        
        - CHD boundary: `eastern model boundary`
        - CHD head: `{chd_head:.2f} m`
        - Recharge: `{recharge_mm_a:.2f} mm/a`
        - Recharge: `{recharge:.4e} m/d`
        """
        
        if active_wel:
            if active_transient:
                model_info_text += f"""
        
        **Well**
        
        - Well active: `True`
        - Well row: `{well_row}`
        - Well column: `{well_col}`
        - Abstraction rate initial steady period: `{well_rate_abs_steady:.2f} m³/d`
        - Abstraction rate transient period: `{well_rate_abs_transient:.2f} m³/d`
        """
            else:
                model_info_text += f"""
        
        **Well**
        
        - Well active: `True`
        - Well row: `{well_row}`
        - Well column: `{well_col}`
        - Abstraction rate: `{well_rate_abs:.2f} m³/d`
        """
        
        else:
            model_info_text += """
        
        **Well**
        
        - Well active: `False`
        """
        
        if active_riv:
            model_info_text += f"""
        
        **River**
        
        - River active: `True`
        - River row: `{river_row}`
        - River length: `{river_length_cols}` cells
        - River gradient: `{river_gradient:.4f} m/m`
        - River bottom offset: `{riverbed_offset:.2f} m`
        - River conductance per cell: `{river_conductance:.2f} m²/d`
        """
        
        else:
            model_info_text += """
        
        **River**
        
        - River active: `False`
        """
        
        model_info_text += """
        
        **Time discretization**
        
        - MODFLOW version: `MODFLOW-NWT`
        - Stress periods: `1`
        - Period length: `1.0 d`
        - Time steps: `1`
        - Simulation type: `steady state`
        """
        
        st.markdown(model_info_text)


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
    if active_transient:
        nper = 2
        perlen = [1.0, transient_perlen]
        nstp = [1, int(transient_nstp)]
        tsmult = [1.0, transient_tsmult]
        steady = [True, False]
    else:
        nper = 1
        perlen = [1.0]
        nstp = [1]
        tsmult = [1.0]
        steady = [True]

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
        perlen=perlen,
        nstp=nstp,
        tsmult=tsmult,
        steady=steady,
    )

    # BAS
    ibound = np.ones((nlay, nrow, ncol), dtype=int)
    strt = np.full((nlay, nrow, ncol), chd_head)

    flopy.modflow.ModflowBas(
        mf,
        ibound=ibound,
        strt=strt,
    )

    # UPW: confined aquifer
    flopy.modflow.ModflowUpw(
        mf,
        laytyp=0,
        hk=hk,
        vka=hk,
        ss=ss,
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
    
        if active_transient:
            wel_spd = {
                0: [[0, well_row - 1, well_col - 1, well_rate_steady]],
                1: [[0, well_row - 1, well_col - 1, well_rate_transient]],
            }
        else:
            wel_spd = {
                0: [[0, well_row - 1, well_col - 1, well_rate]]
            }
    
        flopy.modflow.ModflowWel(
            mf,
            stress_period_data=wel_spd,
            ipakcb=53,
        )

    # Optional river boundary
    if active_riv:
        riv_spd = []
    
        for row, col in riv_cells:
            # Distance from eastern CHD boundary
            distance_from_east = (ncol - col) * delr
    
            river_head = chd_head + river_gradient * distance_from_east
            river_bottom = river_head - riverbed_offset
    
            riv_spd.append([
                0,              # layer
                row - 1,        # zero-based row
                col - 1,        # zero-based column
                river_head,
                river_conductance,
                river_bottom,
            ])
    
        flopy.modflow.ModflowRiv(
            mf,
            stress_period_data={0: riv_spd},
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
    oc_data = {
        (0, 0): ["save head", "save budget", "print budget"]
    }
    
    if active_transient:
        for kstp in range(int(transient_nstp)):
            oc_data[(1, kstp)] = ["save head", "save budget"]
    
        oc_data[(1, int(transient_nstp) - 1)] = [
            "save head",
            "save budget",
            "print budget",
        ]
    
    flopy.modflow.ModflowOc(
        mf,
        stress_period_data=oc_data,
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
    
    # define final result
    if active_transient:
        result_kstpkper = (int(transient_nstp) - 1, 1)
        result_label = (
            f"end of transient period, "
            f"stress period 2, "
            f"time step {int(transient_nstp)}"
        )
    else:
        result_kstpkper = (0, 0)
        result_label = "steady-state period"
    
    heads = headobj.get_data(kstpkper=result_kstpkper)[0]
    
    # then extract transient time series
    transient_head_ts = None
    transient_head_csv = None
    
    if active_transient:
        times = np.array(headobj.get_times())
    
        well_heads = None
        obs_heads = []
    
        if active_wel:
            well_heads = []
    
        for kstpkper in headobj.get_kstpkper():
            h = headobj.get_data(kstpkper=kstpkper)[0]
    
            if active_wel:
                well_heads.append(h[well_row - 1, well_col - 1])
    
            obs_heads.append(h[obs_row - 1, obs_col - 1])
    
        transient_head_ts = {
            "time_days": times,
            "obs_heads": np.array(obs_heads),
            "well_heads": np.array(well_heads) if active_wel else None,
        }
    
        csv_lines = ["time_days,head_observation_m"]
    
        if active_wel:
            csv_lines[0] += ",head_well_m"
    
        for i, t in enumerate(times):
            line = f"{t},{transient_head_ts['obs_heads'][i]}"
    
            if active_wel:
                line += f",{transient_head_ts['well_heads'][i]}"
    
            csv_lines.append(line)
    
        transient_head_csv = "\n".join(csv_lines)
        
    st.session_state.transient_head_ts = transient_head_ts
    st.session_state.transient_head_csv = transient_head_csv

    # Read budget
    list_path = ws / f"{modelname}.list"
    budget_values = read_listing_budget(list_path, package_registry)

    # Store results
    model_info = {
        "nrow": nrow,
        "ncol": ncol,
        "delr": delr,
        "delc": delc,
        "top": top,
        "botm": botm,
        "chd_head": chd_head,
        "workspace": str(ws),
        "package_registry": package_registry,
        "boundary_features": boundary_features,
        "active_wel": active_wel,
        "active_riv": active_riv,
        "active_transient": active_transient,
        "transient_perlen": transient_perlen,
        "transient_nstp": transient_nstp,
        "transient_tsmult": transient_tsmult,
        "result_kstpkper": result_kstpkper,
        "result_label": result_label,
        "modelname": modelname,
    }

    if active_wel:
        model_info.update({
            "well_row": well_row,
            "well_col": well_col,
            "wel_cells": wel_cells,
        })
    
        if active_transient:
            model_info.update({
                "well_rate_steady": well_rate_steady,
                "well_rate_transient": well_rate_transient,
                "well_rate_abs_steady": well_rate_abs_steady,
                "well_rate_abs_transient": well_rate_abs_transient,
            })
        else:
            model_info.update({
                "well_rate": well_rate,
                "well_rate_abs": well_rate_abs,
            })
    
    if active_riv:
        model_info.update({
            "river_row": river_row,
            "river_length_cols": river_length_cols,
            "river_gradient": river_gradient,
            "riverbed_offset": riverbed_offset,
            "river_conductance": river_conductance,
            "riv_cells": riv_cells,
        })
    
    st.session_state.model_done = True
    st.session_state.heads = heads
    st.session_state.last_model_signature = current_model_signature
    st.session_state.budget_values = budget_values
    st.session_state.model_info = model_info

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
    active_riv = info["active_riv"]
    
    well_row = None
    well_col = None
    riv_cells = None
    
    if active_wel:
        well_row = info["well_row"]
        well_col = info["well_col"]
    
    if active_riv:
        riv_cells = info["riv_cells"]

    package_registry = info["package_registry"]
    boundary_features = info["boundary_features"]
    
    feature_color = {
        feature["key"]: feature.get("linecolor", feature["edgecolor"])
        for feature in boundary_features
    }
    
    result_label = info.get("result_label", "previous model run / result label not stored")
    
    st.caption(f"Results shown for: {result_label}")
    
    # ------------------------------------------------------------
    # Cross-section controls
    # ------------------------------------------------------------
    
    out_col1, out_col2 = st.columns(2)
    
    with out_col1:
        with st.expander("Hydraulic heads and cross sections"):

            show_horizontal = st.checkbox(
                "Show horizontal W-E section",
                value=True,
            )
    
            show_vertical = st.checkbox(
                "Show vertical N-S section",
                value=False,
            )

            selected_row = st.number_input(
                "Row # for W-E section",
                min_value=1,
                max_value=nrow,
                value=int((nrow + 1) / 2),
                step=1,
            )
 
            selected_col = st.number_input(
                "Column # for N-S section",
                min_value=1,
                max_value=ncol,
                value=int((ncol + 1) / 2),
                step=1,
            )

    # ------------------------------------------------------------
    # Particle tracking controls
    # ------------------------------------------------------------
    with out_col2:
        with st.expander("Particle tracking"):
    
            active_modpath = st.checkbox(
                "Activate particle tracking",
                value=False,
            )
    
            if active_modpath:
                mp_exe_name = st.text_input(
                    "MODPATH executable",
                    value="mpath7.exe",
                )
                tracking_direction = st.radio(
                    "Tracking direction",
                    ["Forward", "Backward"],
                    index=1,
                    horizontal=True,
                )
                particles_per_cell = st.number_input(
                    "Particles per boundary cell",
                    min_value=1,
                    max_value=25,
                    value=4,
                    step=1,
                )
    
                particle_sources = make_particle_source_registry(boundary_features)
            
                selected_particle_sources = st.multiselect(
                    "Particle starting locations",
                    options=[src["key"] for src in particle_sources],
                    default=[src["key"] for src in particle_sources],
                )
            
                current_particle_signature = {
                    "mp_exe_name": mp_exe_name,
                    "tracking_direction": tracking_direction,
                    "particles_per_cell": int(particles_per_cell),
                    "selected_particle_sources": tuple(selected_particle_sources),
                }
    
                if "last_particle_signature" not in st.session_state:
                    st.session_state.last_particle_signature = None
            
                if (
                    st.session_state.last_particle_signature is not None
                    and current_particle_signature != st.session_state.last_particle_signature
                ):
                    st.session_state.pathlines = None
            
                run_modpath = st.button("Run MODPATH particle tracking")
            
                if run_modpath:
                    try:
                        with st.spinner("Running MODPATH particle tracking..."):
                            pathlines, particle_source_lookup = run_modpath_from_existing_model(
                                ws=info["workspace"],
                                modelname=info["modelname"],
                                mp_exe_name=mp_exe_name,
                                tracking_direction=tracking_direction,
                                particles_per_cell=particles_per_cell,
                                selected_particle_sources=selected_particle_sources,
                                particle_sources=particle_sources,
                                porosity=0.30,
                            )
            
                        st.session_state.pathlines = pathlines
                        st.session_state.particle_source_lookup = particle_source_lookup
                        st.session_state.last_particle_signature = current_particle_signature
                        st.success("MODPATH particle tracking finished successfully.")
            
                    except Exception as e:
                        st.error("MODPATH particle tracking failed.")
                        st.error(str(e))
            
            else:
                st.session_state.pathlines = None
                st.session_state.particle_source_lookup = None
            
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
        alpha=0.5,
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
            linewidths=0.8,
        )
        ax.clabel(contours, fmt="%.2f", fontsize=8)

    plot_model_grid(ax, nrow, ncol, delr, delc)
    plot_boundary_features(ax, boundary_features, nrow, delr, delc)

    if st.session_state.pathlines is not None:
    
        pathlines = st.session_state.pathlines
        particle_source_lookup = st.session_state.particle_source_lookup
        plotted_pathline_labels = set()
    
        for pathline in pathlines:
            particle_id = pathline["particleid"][0]
            source_key = particle_source_lookup.get(particle_id, "Unknown")
            color = feature_color.get(source_key, "gray")
    
            label = None
            if source_key not in plotted_pathline_labels:
                label = f"{source_key} pathlines"
                plotted_pathline_labels.add(source_key)
    
            ax.plot(
                pathline["x"],
                pathline["y"],
                linewidth=0.75,
                alpha=0.6,
                color=color,
#                label=label,
            )
    
#            ax.plot(
#                pathline["x"][0],
#                pathline["y"][0],
#                marker=".",
#                markersize=4,
#                color=color,
#                linestyle="None",
#            )
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
    # Head over time plot(s)
    # ------------------------------------------------------------
  
    if info["active_transient"]:
    
        st.subheader("Transient head development")
    
        ts = st.session_state.transient_head_ts
        
        # ToDo: The first steady-state period needs to be excluded
        if ts is not None:
            fig_ts, ax_ts = plt.subplots(figsize=(8, 4))
            fig_ts2, ax_ts2 = plt.subplots(figsize=(8, 4))
    
            ax_ts.plot(
                ts["time_days"]-1,
                ts["obs_heads"],
                marker="o",
                markersize = 3,
                lw = 1,
                color = 'seagreen',
                label="Observation point",
            )
    
            if ts["well_heads"] is not None:
                ax_ts2.plot(
                    ts["time_days"]-1,
                    ts["well_heads"],
                    marker="s",
                    markersize = 3,
                    lw = 1,
                    color = 'blue',
                    label="Pumping well",
                )
    
            ax_ts.set_xlabel("Time [d]")
            ax_ts.set_xlim(0, transient_perlen)
            ax_ts.set_ylabel("Hydraulic head [m]")
            ax_ts.set_title("Transient hydraulic head at observation well")
            #ax_ts.grid(True, alpha=0.3)
            ax_ts.legend()

            ax_ts2.set_xlabel("Time [d]")
            ax_ts2.set_xlim(0, transient_perlen)
            ax_ts2.set_ylabel("Hydraulic head [m]")
            ax_ts2.set_title("Transient hydraulic head at pumping well")
            #ax_ts2.grid(True, alpha=0.3)
            ax_ts2.legend()
            
            st.pyplot(fig_ts)
            st.pyplot(fig_ts2)
    
            st.download_button(
                label="Download transient head data as CSV",
                data=st.session_state.transient_head_csv,
                file_name="transient_head_timeseries.csv",
                mime="text/csv",
            )    
        
    # ------------------------------------------------------------
    # Water budget
    # ------------------------------------------------------------
    # TODO - Differentiate of cumulative, last time step, development over time
    st.header("Water budget")

    fig_budget = plot_budget_bar_chart(budget, package_registry)
    st.pyplot(fig_budget)

    st.markdown(budget_markdown(budget, package_registry))