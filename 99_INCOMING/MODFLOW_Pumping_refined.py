# app.py
import os
import shutil
import tempfile
import time

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import scipy.special
import flopy


# ------------------------------------------------------------
# Streamlit setup
# ------------------------------------------------------------
st.set_page_config(page_title="Transient Pumping Model")

if "model_results" not in st.session_state:
    st.session_state.model_results = None

if "last_model_signature" not in st.session_state:
    st.session_state.last_model_signature = None


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def well_function(u):
    return scipy.special.exp1(u)


def compute_theis_drawdown(Q_abs, T, S, r, t):
    r = max(r, 1e-6)
    t = np.asarray(t)

    s = np.zeros_like(t, dtype=float)
    valid = t > 0

    u = (S * r**2) / (4 * T * t[valid])
    s[valid] = (Q_abs / (4 * np.pi * T)) * well_function(u)

    return s


def prepare_model_workspace():
    base_temp = tempfile.gettempdir()
    model_ws = os.path.join(base_temp, "mf6_streamlit_workspace")

    if os.path.exists(model_ws):
        try:
            shutil.rmtree(model_ws)
        except PermissionError:
            time.sleep(0.3)
            shutil.rmtree(model_ws, ignore_errors=True)

    os.makedirs(model_ws, exist_ok=True)
    return model_ws


def create_refined_spacing(n, base_dx, center_index, reach, factor):
    spacing = []

    for i in range(n):
        if abs(i - center_index) <= reach:
            spacing.extend([base_dx / factor] * factor)
        else:
            spacing.append(base_dx)

    return np.array(spacing)


def plot_observation_symbol(ax, x, y):
    ax.plot(
        x, y,
        marker="o",
        markersize=8,
        markerfacecolor="none",
        markeredgecolor="blue"
    )
    ax.plot(
        x, y,
        marker="x",
        markersize=6,
        color="blue",
        label="Observation point"
    )


# ------------------------------------------------------------
# Page title
# ------------------------------------------------------------
st.title("Transient MODFLOW 6 Pumping Model")

st.markdown("""
Confined homogeneous aquifer with a central pumping well.  
The model is transient with one stress period of **1 day**.  
No external boundary conditions are assigned, so the model boundaries are no-flow.
""")


# ------------------------------------------------------------
# User settings
# ------------------------------------------------------------
st.subheader("Model settings")

perlen = 86400.0  # one day in seconds

with st.expander("Spatial discretization", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        lx = st.number_input("Model length x [m]", value=2000, min_value=100, step=10)

    with col2:
        ly = st.number_input("Model length y [m]", value=2000, min_value=100, step=10)

    with col3:
        dx = st.number_input("Base grid size Δx = Δy [m]", value=100, min_value=10, step=10)


with st.expander("Grid refinement", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        refine_reach = st.number_input(
            "Refinement reach from well [base rows/columns]",
            value=2,
            min_value=0,
            step=1
        )

    with col2:
        refine_factor = st.number_input(
            "Refinement factor",
            value=2,
            min_value=1,
            step=1
        )


with st.expander("Aquifer and pumping parameters", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        k = st.number_input("Hydraulic conductivity K [m/s]", value=1e-4, format="%.2e")
        ss = st.number_input("Specific storage Ss [1/m]", value=1e-5, format="%.2e")

    with col2:
        thickness = st.number_input("Aquifer thickness [m]", value=20.0)
        h_ini = st.number_input("Initial head [m]", value=30.0)

    with col3:
        q_well_input = st.number_input(
            "Pumping rate [m³/s]",
            value=0.02,
            min_value=0.001,
            max_value=0.1,
            step=0.001,
            format="%.3f"
        )
        q_well = -q_well_input

        nstp = st.number_input(
            "Number of time steps",
            value=24,
            min_value=1,
            step=1
        )


# ------------------------------------------------------------
# Derived grid with local refinement
# ------------------------------------------------------------
ncol_base = int(lx / dx)
nrow_base = int(ly / dx)

well_col_base = ncol_base // 2
well_row_base = nrow_base // 2

delr = create_refined_spacing(
    n=ncol_base,
    base_dx=dx,
    center_index=well_col_base,
    reach=refine_reach,
    factor=refine_factor
)

delc = create_refined_spacing(
    n=nrow_base,
    base_dx=dx,
    center_index=well_row_base,
    reach=refine_reach,
    factor=refine_factor
)

ncol = len(delr)
nrow = len(delc)

lx_eff = np.sum(delr)
ly_eff = np.sum(delc)

x_edges = np.concatenate(([0], np.cumsum(delr)))
y_edges = np.concatenate(([0], np.cumsum(delc)))

x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

well_x_target = lx_eff / 2
well_y_target = ly_eff / 2

well_col = int(np.argmin(np.abs(x_centers - well_x_target)))
well_row = int(np.argmin(np.abs(y_centers - well_y_target)))

well_x = x_centers[well_col]
well_y = y_centers[well_row]


# ------------------------------------------------------------
# Observation point
# ------------------------------------------------------------
st.subheader("Observation point")

col1, col2 = st.columns(2)

with col1:
    obs_row = st.number_input(
        "Observation row",
        value=well_row,
        min_value=0,
        max_value=nrow - 1,
        step=1
    )

with col2:
    obs_col = st.number_input(
        "Observation column",
        value=well_col,
        min_value=0,
        max_value=ncol - 1,
        step=1
    )

obs_row = int(obs_row)
obs_col = int(obs_col)

obs_plot_x = x_centers[obs_col]
obs_plot_y = y_centers[obs_row]

r_obs = np.sqrt((obs_plot_x - well_x) ** 2 + (obs_plot_y - well_y) ** 2)


# ------------------------------------------------------------
# Grid information and plot
# ------------------------------------------------------------
st.markdown("#### Model grid")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.write(f"Base grid: **{nrow_base} rows × {ncol_base} columns**")
    st.write(f"Refined grid: **{nrow} rows × {ncol} columns**")
    st.write(f"Effective model size: **{lx_eff:.1f} m × {ly_eff:.1f} m**")
    st.write(f"Base cell size: **{dx:.1f} m × {dx:.1f} m**")
    st.write(f"Minimum cell size: **{dx / refine_factor:.1f} m**")
    st.write(f"Well cell: row **{well_row}**, column **{well_col}**")
    st.write(f"Observation cell: row **{obs_row}**, column **{obs_col}**")
    st.write(f"Distance well–observation point: **{r_obs:.2f} m**")

with col2:
    fig, ax = plt.subplots(figsize=(5, 5))

    for x in x_edges:
        ax.plot([x, x], [0, ly_eff], color="lightgray", linewidth=0.5)

    for y in y_edges:
        ax.plot([0, lx_eff], [y, y], color="lightgray", linewidth=0.5)

    ax.plot(well_x, well_y, "ro", label="Pumping well")
    plot_observation_symbol(ax, obs_plot_x, obs_plot_y)

    ax.set_aspect("equal")
    ax.set_xlim(0, lx_eff)
    ax.set_ylim(0, ly_eff)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.legend(fontsize=10)

    st.pyplot(fig)


# ------------------------------------------------------------
# MODFLOW model
# ------------------------------------------------------------
def run_transient_model():
    model_ws = prepare_model_workspace()

    sim = flopy.mf6.MFSimulation(
        sim_name="transient_pumping",
        version="mf6",
        exe_name="mf6",
        sim_ws=model_ws,
    )

    flopy.mf6.ModflowTdis(
        sim,
        time_units="SECONDS",
        nper=1,
        perioddata=[(perlen, int(nstp), 1.0)],
    )

    flopy.mf6.ModflowIms(
        sim,
        complexity="SIMPLE",
        outer_dvclose=1e-6,
        inner_dvclose=1e-6,
    )

    gwf = flopy.mf6.ModflowGwf(
        sim,
        modelname="gwf_model",
        save_flows=True,
    )

    flopy.mf6.ModflowGwfdis(
        gwf,
        nlay=1,
        nrow=nrow,
        ncol=ncol,
        delr=delr,
        delc=delc,
        top=h_ini,
        botm=[h_ini - thickness],
    )

    flopy.mf6.ModflowGwfic(
        gwf,
        strt=h_ini,
    )

    flopy.mf6.ModflowGwfnpf(
        gwf,
        icelltype=0,
        k=k,
        k33=k,
        save_specific_discharge=True,
    )

    flopy.mf6.ModflowGwfsto(
        gwf,
        iconvert=0,
        ss=ss,
        sy=0.0,
        steady_state={0: False},
        transient={0: True},
    )

    flopy.mf6.ModflowGwfwel(
        gwf,
        stress_period_data=[
            [(0, well_row, well_col), q_well]
        ],
    )

    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord="gwf_model.hds",
        budget_filerecord="gwf_model.cbc",
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
    )

    sim.write_simulation()
    success, buff = sim.run_simulation()

    if not success:
        raise RuntimeError("MODFLOW 6 did not terminate normally.")

    hds = flopy.utils.HeadFile(os.path.join(model_ws, "gwf_model.hds"))

    times = np.array(hds.get_times())
    heads = []

    for t in times:
        head = hds.get_data(totim=t)[0]
        heads.append(head)

    heads = np.array(heads)
    hds.close()

    obs_heads = heads[:, obs_row, obs_col]
    final_head = heads[-1]
    final_drawdown = h_ini - final_head
    obs_drawdown = h_ini - obs_heads

    return times, heads, obs_heads, final_head, final_drawdown, obs_drawdown


# ------------------------------------------------------------
# Simulation results
# ------------------------------------------------------------
st.header("Simulation results")

show_theis = st.toggle("Show Theis solution", value=False)

theis_available = False

if show_theis:
    T_theis = k * thickness
    S_theis = ss * thickness
    Q_theis = abs(q_well)

    time_theis = np.linspace(perlen / 100, perlen, 100)

    theis_drawdown = compute_theis_drawdown(
        Q_abs=Q_theis,
        T=T_theis,
        S=S_theis,
        r=r_obs,
        t=time_theis
    )

    theis_head = h_ini - theis_drawdown
    theis_available = True


current_model_signature = {
    "lx": lx,
    "ly": ly,
    "dx": dx,
    "refine_reach": int(refine_reach),
    "refine_factor": int(refine_factor),
    "k": k,
    "ss": ss,
    "thickness": thickness,
    "h_ini": h_ini,
    "q_well": q_well,
    "nstp": int(nstp),
    "obs_row": obs_row,
    "obs_col": obs_col,
}

if (
    st.session_state.last_model_signature is not None
    and current_model_signature != st.session_state.last_model_signature
):
    st.session_state.model_results = None


col_run1, col_run2 = st.columns([1, 3])

with col_run1:
    run_clicked = st.button("▶ Run MODFLOW")

with col_run2:
    status = st.empty()


if run_clicked:
    try:
        status.info("🔄 Building and running the model...")

        with st.spinner("MODFLOW simulation"):
            times, heads, obs_heads, final_head, final_drawdown, obs_drawdown = run_transient_model()

        st.session_state.model_results = {
            "times": times,
            "heads": heads,
            "obs_heads": obs_heads,
            "final_head": final_head,
            "final_drawdown": final_drawdown,
            "obs_drawdown": obs_drawdown,
            "x_centers": x_centers,
            "y_centers": y_centers,
            "well_x": well_x,
            "well_y": well_y,
            "obs_plot_x": obs_plot_x,
            "obs_plot_y": obs_plot_y,
        }

        st.session_state.last_model_signature = current_model_signature

        status.success("✅ MODFLOW 6 simulation finished successfully.")

    except Exception as e:
        status.error("❌ Simulation failed.")
        st.error(str(e))
        st.info(
            "Please check that the MODFLOW 6 executable `mf6` is installed "
            "and available in your system PATH."
        )


# ------------------------------------------------------------
# Time-series plot
# ------------------------------------------------------------
if theis_available or st.session_state.model_results is not None:
    st.subheader("Model results")

    st.markdown("#### Head and drawdown at the observation point")

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(7, 6), sharex=True)

    if st.session_state.model_results is not None:
        res = st.session_state.model_results

        times_mf = res["times"]
        obs_heads_mf = res["obs_heads"]
        obs_drawdown_mf = res["obs_drawdown"]

        axes[0].plot(
            times_mf / 3600,
            obs_heads_mf,
            marker="o",
            linestyle="None",
            markerfacecolor="none",
            markeredgecolor="blue",
            label="MODFLOW 6"
        )

        axes[1].plot(
            times_mf / 3600,
            obs_drawdown_mf,
            marker="o",
            linestyle="None",
            markerfacecolor="none",
            markeredgecolor="blue",
            label="MODFLOW 6"
        )

    if theis_available:
        axes[0].plot(
            time_theis / 3600,
            theis_head,
            linestyle="--",
            label="Theis"
        )

        axes[1].plot(
            time_theis / 3600,
            theis_drawdown,
            linestyle="--",
            label="Theis"
        )

    axes[0].set_title("Head over time")
    axes[0].set_ylabel("Head [m]")
    axes[0].set_xlim(0, 24)
    axes[0].set_ylim(top=h_ini)
    axes[0].legend()

    axes[1].set_title("Drawdown over time")
    axes[1].set_xlabel("Time [h]")
    axes[1].set_ylabel("Drawdown [m]")
    axes[1].set_xlim(0, 24)
    axes[1].set_ylim(bottom=0)
    axes[1].legend()

    plt.tight_layout()
    st.pyplot(fig)


# ------------------------------------------------------------
# Final spatial plots
# ------------------------------------------------------------
if st.session_state.model_results is not None:
    res = st.session_state.model_results

    final_head = res["final_head"]
    final_drawdown = res["final_drawdown"]

    X, Y = np.meshgrid(res["x_centers"], res["y_centers"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Final hydraulic head")

        fig, ax = plt.subplots(figsize=(6, 5))
        c = ax.contourf(X, Y, final_head, levels=20)
        ax.contour(X, Y, final_head, colors="black", linewidths=0.5)

        ax.plot(res["well_x"], res["well_y"], "ro", label="Pumping well")
        plot_observation_symbol(ax, res["obs_plot_x"], res["obs_plot_y"])

        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend()

        fig.colorbar(c, ax=ax, label="Head [m]")
        st.pyplot(fig)

    with col2:
        st.markdown("#### Final drawdown")

        fig, ax = plt.subplots(figsize=(6, 5))
        c = ax.contourf(X, Y, final_drawdown, levels=20)
        ax.contour(X, Y, final_drawdown, colors="black", linewidths=0.5)

        ax.plot(res["well_x"], res["well_y"], "ro", label="Pumping well")
        plot_observation_symbol(ax, res["obs_plot_x"], res["obs_plot_y"])

        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend()

        fig.colorbar(c, ax=ax, label="Drawdown [m]")
        st.pyplot(fig)