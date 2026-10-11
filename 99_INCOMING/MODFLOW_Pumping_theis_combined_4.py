import os
import shutil
import tempfile

import flopy
import matplotlib.pyplot as plt
import numpy as np
import scipy.special
import streamlit as st


# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "model_results" not in st.session_state:
    st.session_state.model_results = None

if "last_model_signature" not in st.session_state:
    st.session_state.last_model_signature = None


# ------------------------------------------------------------
# Reusable parameter input helper
# ------------------------------------------------------------
def parameter_input(
    label,
    *,
    key,
    min_value,
    max_value,
    default,
    number_mode,
    scale="linear",
    number_format="%.2e",
    log_steps_per_decade=20,
):
    """Render one parameter with a shared slider/number-input mode.

    The physical value is stored independently from the active widget so one
    global switch can change all parameter widgets between slider and number
    input without changing their values.
    """
    value_key = f"{key}__value"
    number_key = f"_{key}__number"
    slider_key = f"_{key}__slider"

    if value_key not in st.session_state:
        st.session_state[value_key] = float(default)

    current = float(st.session_state[value_key])
    current = min(max(current, float(min_value)), float(max_value))
    st.session_state[value_key] = current

    def _update_from_number():
        value = float(st.session_state[number_key])
        st.session_state[value_key] = min(max(value, float(min_value)), float(max_value))

    def _update_from_slider():
        st.session_state[value_key] = float(st.session_state[slider_key])

    if number_mode:
        magnitude = 10.0 ** np.floor(np.log10(max(current, float(min_value))))
        number_step = max(float(min_value), magnitude / 10.0)
        st.session_state[number_key] = current
        st.number_input(
            label,
            min_value=float(min_value),
            max_value=float(max_value),
            step=float(number_step),
            format=number_format,
            key=number_key,
            on_change=_update_from_number,
        )
    else:
        if scale == "log":
            decades = np.log10(float(max_value)) - np.log10(float(min_value))
            n_steps = int(round(decades * int(log_steps_per_decade))) + 1
            options = [
                float(v)
                for v in np.logspace(
                    np.log10(float(min_value)),
                    np.log10(float(max_value)),
                    n_steps,
                )
            ]
            # Preserve arbitrary direct-input values when switching back.
            if not any(np.isclose(current, v, rtol=1e-12, atol=0.0) for v in options):
                options.append(current)
                options.sort()
            st.session_state[slider_key] = current
            st.select_slider(
                label,
                options=options,
                key=slider_key,
                format_func=lambda value: f"{value:.2e}",
                on_change=_update_from_slider,
            )
        else:
            st.session_state[slider_key] = current
            st.slider(
                label,
                min_value=float(min_value),
                max_value=float(max_value),
                key=slider_key,
                on_change=_update_from_slider,
            )

    return float(st.session_state[value_key])


# ------------------------------------------------------------
# Analytical and synthetic-data helpers
# ------------------------------------------------------------
def well_function(u):
    """Theis well function W(u) = E1(u)."""
    return scipy.special.exp1(u)


def compute_theis_drawdown(Q_abs, T, S, r, t):
    """
    Compute Theis drawdown for a confined aquifer.

    Parameters
    ----------
    Q_abs : float
        Positive pumping rate [m3/s].
    T : float
        Transmissivity [m2/s].
    S : float
        Storativity [-].
    r : float
        Radial distance from pumping well [m]. Must be > 0.
    t : array-like
        Time since pumping started [s].
    """
    if Q_abs < 0:
        raise ValueError("Q_abs must be non-negative.")
    if T <= 0:
        raise ValueError("Transmissivity T must be positive.")
    if S <= 0:
        raise ValueError("Storativity S must be positive.")
    if r <= 0:
        raise ValueError("Theis solution requires an observation distance r > 0.")

    t = np.asarray(t, dtype=float)
    s = np.zeros_like(t, dtype=float)

    valid = t > 0
    u = (S * r**2) / (4.0 * T * t[valid])
    s[valid] = (Q_abs / (4.0 * np.pi * T)) * well_function(u)

    return s


def build_k_field(k, nrow, ncol, use_random_k, factor_min=0.5, factor_max=2.0, seed=42):
    """Return a homogeneous or reproducible cellwise-random K field."""
    if k <= 0:
        raise ValueError("Hydraulic conductivity K must be positive.")
    if nrow < 1 or ncol < 1:
        raise ValueError("The model grid must contain at least one row and one column.")

    if not use_random_k:
        return np.full((nrow, ncol), float(k), dtype=float)

    if factor_min <= 0 or factor_max <= 0:
        raise ValueError("K multipliers must be positive.")
    if factor_min > factor_max:
        raise ValueError("Minimum K multiplier cannot exceed maximum K multiplier.")

    rng = np.random.default_rng(int(seed))
    factors = rng.uniform(float(factor_min), float(factor_max), size=(nrow, ncol))
    return float(k) * factors


# ------------------------------------------------------------
# MODFLOW 6 model
# ------------------------------------------------------------
def run_transient_model(
    *,
    perlen,
    nstp,
    nrow,
    ncol,
    dx,
    h_ini,
    thickness,
    k_array,
    ss,
    well_row,
    well_col,
    q_well,
    obs_row,
    obs_col,
):
    """Build, run, and read one transient confined MODFLOW 6 simulation."""
    model_ws = tempfile.mkdtemp(prefix="mf6_pumping_")

    try:
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
            perioddata=[(float(perlen), int(nstp), 1.0)],
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
            nrow=int(nrow),
            ncol=int(ncol),
            delr=float(dx),
            delc=float(dx),
            top=float(h_ini),
            botm=[float(h_ini) - float(thickness)],
        )

        flopy.mf6.ModflowGwfic(gwf, strt=float(h_ini))

        flopy.mf6.ModflowGwfnpf(
            gwf,
            icelltype=0,  # confined
            k=k_array,
            k33=k_array,
            save_specific_discharge=True,
        )

        flopy.mf6.ModflowGwfsto(
            gwf,
            iconvert=0,
            ss=float(ss),
            sy=0.0,
            steady_state={0: False},
            transient={0: True},
        )

        flopy.mf6.ModflowGwfwel(
            gwf,
            stress_period_data=[[(0, int(well_row), int(well_col)), float(q_well)]],
        )

        flopy.mf6.ModflowGwfoc(
            gwf,
            head_filerecord="gwf_model.hds",
            budget_filerecord="gwf_model.cbc",
            saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
        )

        sim.write_simulation()
        success, _ = sim.run_simulation()
        if not success:
            raise RuntimeError("MODFLOW 6 did not terminate normally.")

        head_path = os.path.join(model_ws, "gwf_model.hds")
        hds = flopy.utils.HeadFile(head_path)
        try:
            times = np.asarray(hds.get_times(), dtype=float)
            heads = np.asarray([hds.get_data(totim=t)[0] for t in times])
        finally:
            hds.close()

        obs_heads = heads[:, int(obs_row), int(obs_col)]
        final_head = heads[-1]
        final_drawdown = float(h_ini) - final_head
        obs_drawdown = float(h_ini) - obs_heads

        return {
            "times": times,
            "heads": heads,
            "obs_heads": obs_heads,
            "final_head": final_head,
            "final_drawdown": final_drawdown,
            "obs_drawdown": obs_drawdown,
        }

    finally:
        shutil.rmtree(model_ws, ignore_errors=True)


def generate_irregular_measurement_times(perlen, rng, n_min=18, n_max=30):
    """Generate slightly irregular manual-style measurement times over the full period."""
    if perlen <= 0:
        raise ValueError("Simulation period must be positive.")
    if n_min < 2 or n_max < n_min:
        raise ValueError("Invalid measurement-count limits.")

    n_measurements = int(rng.integers(int(n_min), int(n_max) + 1))
    first_time = rng.uniform(0.005, 0.02) * float(perlen)
    base = np.linspace(first_time, float(perlen), n_measurements)
    nominal_dt = (float(perlen) - first_time) / max(n_measurements - 1, 1)
    jitter = rng.uniform(-0.35, 0.35, size=n_measurements) * nominal_dt
    times = np.sort(np.clip(base + jitter, first_time, float(perlen)))
    times[0] = first_time
    times[-1] = float(perlen)

    # Enforce strict monotonicity in the unlikely event that clipping/jitter
    # produces coincident points.
    for idx in range(1, len(times)):
        if times[idx] <= times[idx - 1]:
            times[idx] = min(float(perlen), times[idx - 1] + 1.0)
    times[-1] = float(perlen)
    return times


def generate_random_field_measurements(
    *,
    perlen,
    nrow,
    ncol,
    dx,
    h_ini,
    thickness,
    well_row,
    well_col,
    q_well,
    obs_row,
    obs_col,
    seed=123,
    noise_percent=3.0,
    k_min=1e-5,
    k_max=1e-2,
    ss_min=1e-6,
    ss_max=1e-2,
    k_factor_min=0.5,
    k_factor_max=2.0,
    hidden_nstp=192,
):
    """Create one fixed synthetic dataset from a heterogeneous hidden MODFLOW model.

    A scalar reference K and uniform Ss define the hidden aquifer parameters.
    The actual hidden K field is cellwise heterogeneous around that reference K.
    Measurements are sampled at irregular times from the hidden MODFLOW response
    and then perturbed with Gaussian noise.
    """
    if thickness <= 0:
        raise ValueError("Aquifer thickness must be positive.")
    if k_min <= 0 or k_max <= 0 or k_min > k_max:
        raise ValueError("Hidden K limits must be positive and ordered.")
    if ss_min <= 0 or ss_max <= 0 or ss_min > ss_max:
        raise ValueError("Hidden Ss limits must be positive and ordered.")
    if noise_percent < 0:
        raise ValueError("Noise level cannot be negative.")

    rng = np.random.default_rng(int(seed))
    k_reference_true = 10.0 ** rng.uniform(np.log10(float(k_min)), np.log10(float(k_max)))
    ss_true = 10.0 ** rng.uniform(np.log10(float(ss_min)), np.log10(float(ss_max)))

    factors = rng.uniform(float(k_factor_min), float(k_factor_max), size=(int(nrow), int(ncol)))
    k_field_true = np.clip(k_reference_true * factors, float(k_min), float(k_max))

    hidden_result = run_transient_model(
        perlen=float(perlen),
        nstp=max(int(hidden_nstp), 2),
        nrow=int(nrow),
        ncol=int(ncol),
        dx=float(dx),
        h_ini=float(h_ini),
        thickness=float(thickness),
        k_array=k_field_true,
        ss=float(ss_true),
        well_row=int(well_row),
        well_col=int(well_col),
        q_well=float(q_well),
        obs_row=int(obs_row),
        obs_col=int(obs_col),
    )

    measurement_times = generate_irregular_measurement_times(float(perlen), rng)

    hidden_times = np.concatenate(([0.0], np.asarray(hidden_result["times"], dtype=float)))
    hidden_drawdown = np.concatenate(([0.0], np.asarray(hidden_result["obs_drawdown"], dtype=float)))
    drawdown_clean = np.interp(measurement_times, hidden_times, hidden_drawdown)

    noise_fraction = float(noise_percent) / 100.0
    max_clean = float(np.max(drawdown_clean)) if drawdown_clean.size else 0.0
    noise_scale = noise_fraction * max_clean
    noise = rng.normal(loc=0.0, scale=noise_scale, size=drawdown_clean.shape)
    drawdown_noisy = np.maximum(drawdown_clean + noise, 0.0)
    head_noisy = float(h_ini) - drawdown_noisy

    # Fixed axes belong to the measurement realization, not to the current calibration.
    max_measurement_drawdown = float(np.max(np.concatenate([drawdown_clean, drawdown_noisy])))
    if max_measurement_drawdown <= 0.0:
        max_measurement_drawdown = 1e-6
    drawdown_upper = 1.50 * max_measurement_drawdown

    return {
        "k_reference_true": float(k_reference_true),
        "k_field_true": k_field_true,
        "k_field_min": float(np.min(k_field_true)),
        "k_field_max": float(np.max(k_field_true)),
        "k_field_mean": float(np.mean(k_field_true)),
        "k_field_geomean": float(np.exp(np.mean(np.log(k_field_true)))),
        "ss_true": float(ss_true),
        "S_true": float(ss_true) * float(thickness),
        "times": measurement_times,
        "drawdown_clean": drawdown_clean,
        "drawdown_noisy": drawdown_noisy,
        "head_noisy": head_noisy,
        "plot_limits": {
            "head": (float(h_ini) - drawdown_upper, float(h_ini)),
            "drawdown": (0.0, drawdown_upper),
        },
        "setup": {
            "perlen": float(perlen),
            "nrow": int(nrow),
            "ncol": int(ncol),
            "dx": float(dx),
            "h_ini": float(h_ini),
            "thickness": float(thickness),
            "well_row": int(well_row),
            "well_col": int(well_col),
            "q_well": float(q_well),
            "obs_row": int(obs_row),
            "obs_col": int(obs_col),
            "noise_percent": float(noise_percent),
            "seed": int(seed),
        },
    }


# ------------------------------------------------------------
# Streamlit page
# ------------------------------------------------------------
st.set_page_config(page_title="MODFLOW 6 Pumping Model – Theis Comparison")

st.title("Transient MODFLOW 6 Pumping Model")
st.markdown(
    """
This app simulates pumping from a **confined aquifer** with MODFLOW 6 and compares
head and drawdown at an observation point with the analytical **Theis solution**.
The MODFLOW model has one transient stress period of **1 day** and no-flow outer
boundaries.
"""
)
st.info(
    "Local execution requires MODFLOW 6 (`mf6` / `mf6.exe`) to be installed "
    "and available on the system PATH."
)
st.caption(
    "Theis assumes an infinite, homogeneous confined aquifer and a line-source well. "
    "The finite MODFLOW grid, no-flow boundaries, and finite well cell can therefore "
    "produce deviations, especially close to the well and at late time."
)


# ------------------------------------------------------------
# User settings
# ------------------------------------------------------------
st.subheader("Model settings")

perlen = 86400.0  # one day [s]

# One global input-mode switch, matching the pattern used in the other modules.
number_input_general = st.toggle(
    "Use number input instead of sliders",
    key="number_input_general",
    help="Switch K and Ss together between logarithmic sliders and direct number input.",
)

# Widget state is updated before the rerun. Reading this key here suppresses the
# visible random-K option immediately while the calibration exercise is active.
calibration_active = bool(st.session_state.get("show_measured", False))
if calibration_active:
    st.session_state["random_k"] = False

if "k_field_generation" not in st.session_state:
    st.session_state.k_field_generation = 0
if "measurement_generation" not in st.session_state:
    st.session_state.measurement_generation = 0
if "measured_result" not in st.session_state:
    st.session_state.measured_result = None
if "calibration_revealed" not in st.session_state:
    st.session_state.calibration_revealed = False

# Invalidate synthetic observations created by older app versions.
stored_measurement = st.session_state.measured_result
required_measurement_keys = {
    "k_reference_true",
    "k_field_true",
    "ss_true",
    "S_true",
    "times",
    "drawdown_noisy",
    "head_noisy",
    "plot_limits",
    "setup",
}
if stored_measurement is not None and not required_measurement_keys.issubset(stored_measurement):
    st.session_state.measured_result = None
    st.session_state.calibration_revealed = False

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Spatial discretization", expanded=True):
        lx = st.number_input("Model length x [m]", value=2100, min_value=100, step=10)
        ly = st.number_input("Model length y [m]", value=2100, min_value=100, step=10)
        dx = st.number_input(
            "Uniform grid size Δx = Δy [m]",
            value=100,
            min_value=1,
            max_value=int(min(lx, ly)),
            step=10,
        )

        ncol = max(1, int(lx / dx))
        nrow = max(1, int(ly / dx))
        lx_eff = ncol * dx
        ly_eff = nrow * dx

        well_row = nrow // 2
        well_col = ncol // 2
        well_x = (well_col + 0.5) * dx
        well_y = (well_row + 0.5) * dx

with col2:
    with st.expander("Aquifer parameters", expanded=True):
        k = parameter_input(
            "Hydraulic conductivity K [m/s]",
            key="hydraulic_conductivity",
            min_value=1e-5,
            max_value=1e-2,
            default=1e-4,
            number_mode=number_input_general,
            scale="log",
            number_format="%.2e",
            log_steps_per_decade=20,
        )
        ss = parameter_input(
            "Specific storage Ss [1/m]",
            key="specific_storage",
            min_value=1e-6,
            max_value=1e-2,
            default=1e-5,
            number_mode=number_input_general,
            scale="log",
            number_format="%.2e",
            log_steps_per_decade=20,
        )
        thickness = st.number_input("Aquifer thickness [m]", value=20.0, min_value=0.01)
        h_ini = st.number_input("Initial head [m]", value=30.0)

        k_factor_min = 0.5
        k_factor_max = 2.0
        random_seed_base = 42
        random_seed = 42

        if calibration_active:
            random_k = False
            st.caption(
                "The visible random K-field option is unavailable during the calibration "
                "exercise. The synthetic measurements already represent a hidden heterogeneous aquifer."
            )
        else:
            random_k = st.toggle("Use random K field", key="random_k")

        if random_k:
            k_factor_min = st.number_input(
                "Minimum K multiplier", value=0.5, min_value=0.01, step=0.1
            )
            k_factor_max = st.number_input(
                "Maximum K multiplier", value=2.0, min_value=0.01, step=0.1
            )
            random_seed_base = st.number_input(
                "K-field base random seed", value=42, min_value=0, step=1
            )
            if st.button("Regenerate random K field", key="regenerate_k_field"):
                st.session_state.k_field_generation += 1

            random_seed = int(random_seed_base) + int(st.session_state.k_field_generation)
            st.caption(f"Random-field realization: {st.session_state.k_field_generation + 1}")

with col3:
    with st.expander("Well, observation, and stress data", expanded=True):
        nstp = st.number_input("Number of time steps", value=24, min_value=1, step=1)
        q_well_input = st.number_input(
            "Pumping rate [m³/s]",
            value=0.02,
            min_value=0.001,
            max_value=0.1,
            step=0.001,
            format="%.3f",
        )
        q_well = -float(q_well_input)

        st.write("Observation point")
        default_obs_row = well_row
        default_obs_col = min(well_col + 1, ncol - 1)

        obs_row = int(
            st.number_input(
                "Obs row", value=default_obs_row, min_value=0, max_value=nrow - 1, step=1
            )
        )
        obs_col = int(
            st.number_input(
                "Obs col", value=default_obs_col, min_value=0, max_value=ncol - 1, step=1
            )
        )

        obs_plot_x = (obs_col + 0.5) * dx
        obs_plot_y = (obs_row + 0.5) * dx
        r_obs = float(np.hypot(obs_plot_x - well_x, obs_plot_y - well_y))


# Build the visible MODFLOW K field after all controls are known.
k_field_error = None
try:
    k_array = build_k_field(
        k=k,
        nrow=nrow,
        ncol=ncol,
        use_random_k=random_k,
        factor_min=k_factor_min,
        factor_max=k_factor_max,
        seed=random_seed,
    )
except ValueError as exc:
    k_field_error = str(exc)
    k_array = np.full((nrow, ncol), float(k), dtype=float)
    st.error(k_field_error)


# ------------------------------------------------------------
# Grid information and visualization
# ------------------------------------------------------------
with st.expander("Model grid and model information", expanded=True):
    col_grid_info, col_grid_plot = st.columns([1, 1.5])

    with col_grid_info:
        st.write(f"Number of rows: **{nrow}**")
        st.write(f"Number of columns: **{ncol}**")
        st.write(f"Model size: **{lx_eff:.1f} m × {ly_eff:.1f} m**")
        st.write(f"Cell size: **{dx:.1f} m × {dx:.1f} m**")
        st.write(f"Well: row **{well_row}**, column **{well_col}**")
        st.write(f"Observation: row **{obs_row}**, column **{obs_col}**")
        st.write(f"Distance well–observation: **{r_obs:.2f} m**")

        if random_k:
            st.write(f"K min: **{np.min(k_array):.2e} m/s**")
            st.write(f"K max: **{np.max(k_array):.2e} m/s**")
            st.write(f"K mean: **{np.mean(k_array):.2e} m/s**")

        if r_obs == 0:
            st.warning(
                "The observation point is in the pumping-well cell. MODFLOW can still run, "
                "but the analytical Theis comparison requires r > 0."
            )

    with col_grid_plot:
        fig, ax = plt.subplots(figsize=(5, 5))

        if random_k:
            x_edges = np.arange(0, lx_eff + dx, dx)
            y_edges = np.arange(0, ly_eff + dx, dx)
            c = ax.pcolormesh(x_edges, y_edges, k_array, shading="flat")
            fig.colorbar(c, ax=ax, label="K [m/s]")

        for x in np.arange(0, lx_eff + dx, dx):
            ax.plot([x, x], [0, ly_eff], color="lightgray", linewidth=0.5)
        for y in np.arange(0, ly_eff + dx, dx):
            ax.plot([0, lx_eff], [y, y], color="lightgray", linewidth=0.5)

        ax.plot(well_x, well_y, "ro", label="Pumping well")
        ax.plot(
            obs_plot_x,
            obs_plot_y,
            marker="o",
            markersize=8,
            markerfacecolor="none",
            markeredgecolor="blue",
        )
        ax.plot(
            obs_plot_x,
            obs_plot_y,
            marker="x",
            markersize=6,
            color="blue",
            linestyle="None",
            label="Observation point",
        )

        ax.set_aspect("equal")
        ax.set_xlim(0, lx_eff)
        ax.set_ylim(0, ly_eff)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend(fontsize=10)
        st.pyplot(fig)
        plt.close(fig)


# ------------------------------------------------------------
# Simulation and comparison controls
# ------------------------------------------------------------
st.header("Simulation results")

current_model_signature = {
    "lx": float(lx),
    "ly": float(ly),
    "dx": float(dx),
    "k": float(k),
    "ss": float(ss),
    "thickness": float(thickness),
    "h_ini": float(h_ini),
    "q_well": float(q_well),
    "nstp": int(nstp),
    "obs_row": int(obs_row),
    "obs_col": int(obs_col),
    "random_k": bool(random_k),
    "k_factor_min": float(k_factor_min) if random_k else None,
    "k_factor_max": float(k_factor_max) if random_k else None,
    "random_seed": int(random_seed) if random_k else None,
}

if (
    st.session_state.last_model_signature is not None
    and current_model_signature != st.session_state.last_model_signature
):
    # A parameter change is not evaluated until MODFLOW is run again.
    st.session_state.model_results = None
    if calibration_active:
        st.session_state.calibration_revealed = False

col_compare, col_run, col_status = st.columns([2.7, 1.8, 3.0])

with col_compare:
    show_measured = st.toggle("Calibration exercise / synthetic measured data", key="show_measured")

    show_theis = False
    if not show_measured:
        show_theis = st.toggle("Show Theis solution", value=False)

    measurement_seed_base = 123
    noise_percent = 3.0
    regenerate_measurements = False

    if show_measured:
        with st.expander("Synthetic measurement settings"):
            measurement_seed_base = st.number_input(
                "Synthetic-data base random seed", value=123, min_value=0, step=1
            )
            noise_percent = st.number_input(
                "Measurement noise [%]", value=3.0, min_value=0.0, max_value=100.0, step=0.5
            )
            regenerate_measurements = st.button(
                "Regenerate random measurements", key="regenerate_measurements"
            )
            st.caption(
                "The measurements come from a hidden MODFLOW model with a heterogeneous "
                "random K field. They remain unchanged while you modify calibration parameters. "
                "Only this button generates a new hidden aquifer and a new irregular measurement schedule."
            )
            st.caption(
                "Hidden K values are constrained to 1e-5–1e-2 m/s and hidden Ss to "
                "1e-6–1e-2 1/m."
            )
            st.caption(f"Measurement realization: {st.session_state.measurement_generation + 1}")

with col_run:
    run_clicked = st.button("▶ Run MODFLOW", disabled=(k_field_error is not None))

with col_status:
    status = st.empty()


# ------------------------------------------------------------
# Synthetic measured reality: hidden heterogeneous MODFLOW model
# ------------------------------------------------------------
measured_result = None
if show_measured:
    if regenerate_measurements:
        st.session_state.measurement_generation += 1
        st.session_state.measured_result = None
        st.session_state.calibration_revealed = False

    if st.session_state.measured_result is None:
        if r_obs <= 0:
            st.warning(
                "Synthetic measured data are unavailable because the observation distance is zero."
            )
        else:
            effective_measurement_seed = (
                int(measurement_seed_base) + int(st.session_state.measurement_generation)
            )
            try:
                with st.spinner("Generating hidden heterogeneous MODFLOW measurements..."):
                    st.session_state.measured_result = generate_random_field_measurements(
                        perlen=perlen,
                        nrow=nrow,
                        ncol=ncol,
                        dx=dx,
                        h_ini=h_ini,
                        thickness=thickness,
                        well_row=well_row,
                        well_col=well_col,
                        q_well=q_well,
                        obs_row=obs_row,
                        obs_col=obs_col,
                        seed=effective_measurement_seed,
                        noise_percent=noise_percent,
                        k_min=1e-5,
                        k_max=1e-2,
                        ss_min=1e-6,
                        ss_max=1e-2,
                        k_factor_min=0.5,
                        k_factor_max=2.0,
                        hidden_nstp=max(192, 4 * int(nstp)),
                    )
            except Exception as exc:
                st.session_state.measured_result = None
                st.error("The synthetic measurement run failed.")
                st.error(str(exc))
                st.info(
                    "Synthetic measurements now require MODFLOW 6 because the hidden reality "
                    "is generated with a heterogeneous MODFLOW model."
                )

    measured_result = st.session_state.measured_result

    if measured_result is not None:
        setup = measured_result["setup"]
        setup_changed = any(
            [
                int(setup["nrow"]) != int(nrow),
                int(setup["ncol"]) != int(ncol),
                not np.isclose(float(setup["dx"]), float(dx)),
                not np.isclose(float(setup["h_ini"]), float(h_ini)),
                not np.isclose(float(setup["thickness"]), float(thickness)),
                not np.isclose(float(setup["q_well"]), float(q_well)),
                int(setup["well_row"]) != int(well_row),
                int(setup["well_col"]) != int(well_col),
                int(setup["obs_row"]) != int(obs_row),
                int(setup["obs_col"]) != int(obs_col),
            ]
        )
        if setup_changed:
            st.warning(
                "The current measured dataset was generated with a different model geometry, "
                "stress, observation location, initial head, or thickness. The measurements "
                "have intentionally been kept unchanged. Restore the original setup or use "
                "‘Regenerate random measurements’ before interpreting the calibration."
            )


# ------------------------------------------------------------
# Visible homogeneous/optional-random MODFLOW run
# ------------------------------------------------------------
if run_clicked:
    try:
        status.info("Building and running MODFLOW 6...")
        with st.spinner("MODFLOW simulation"):
            st.session_state.model_results = run_transient_model(
                perlen=perlen,
                nstp=nstp,
                nrow=nrow,
                ncol=ncol,
                dx=dx,
                h_ini=h_ini,
                thickness=thickness,
                k_array=k_array,
                ss=ss,
                well_row=well_row,
                well_col=well_col,
                q_well=q_well,
                obs_row=obs_row,
                obs_col=obs_col,
            )
        st.session_state.last_model_signature = current_model_signature
        if show_measured:
            st.session_state.calibration_revealed = False
        status.success("✅ MODFLOW 6 simulation finished.")

    except Exception as exc:
        st.session_state.model_results = None
        status.error("❌ Simulation failed.")
        st.error(str(exc))
        st.info(
            "Please check that the MODFLOW 6 executable `mf6` is installed "
            "and available in your system PATH."
        )


# ------------------------------------------------------------
# Calibration completion / reveal
# ------------------------------------------------------------
calibration_run_current = (
    show_measured
    and measured_result is not None
    and st.session_state.model_results is not None
    and st.session_state.last_model_signature == current_model_signature
)

if show_measured and measured_result is not None:
    st.markdown("#### Calibration exercise")
    st.caption(
        "Adjust the homogeneous K and Ss values and press **Run MODFLOW** to evaluate each "
        "parameter set against the measured data. The Theis solution and hidden parameters "
        "remain unavailable during calibration."
    )

    if not calibration_run_current:
        st.caption("Run MODFLOW with the current parameter values before finishing the calibration.")

    if st.button(
        "Show me how I did",
        key="show_calibration_result",
        disabled=not calibration_run_current,
    ):
        st.session_state.calibration_revealed = True


# ------------------------------------------------------------
# Theis solution
# ------------------------------------------------------------
theis_result = None

if not show_measured and show_theis:
    if r_obs <= 0:
        st.warning("The Theis curve is unavailable because the observation distance is zero.")
    else:
        time_theis = np.linspace(perlen / 100.0, perlen, 100)
        theis_drawdown = compute_theis_drawdown(
            Q_abs=abs(q_well),
            T=float(k) * float(thickness),
            S=float(ss) * float(thickness),
            r=r_obs,
            t=time_theis,
        )
        theis_result = {
            "times": time_theis,
            "drawdown": theis_drawdown,
            "head": float(h_ini) - theis_drawdown,
            "label": "Theis",
        }
        if random_k:
            st.caption(
                "The Theis curve uses the entered homogeneous reference K and Ss, while the "
                "MODFLOW run uses the random cellwise K field."
            )

elif (
    show_measured
    and st.session_state.calibration_revealed
    and calibration_run_current
):
    # Use exactly the parameter set from the accepted MODFLOW calibration run.
    calibrated_signature = st.session_state.last_model_signature
    time_theis = np.linspace(perlen / 100.0, perlen, 100)
    theis_drawdown = compute_theis_drawdown(
        Q_abs=abs(float(calibrated_signature["q_well"])),
        T=float(calibrated_signature["k"]) * float(calibrated_signature["thickness"]),
        S=float(calibrated_signature["ss"]) * float(calibrated_signature["thickness"]),
        r=r_obs,
        t=time_theis,
    )
    theis_result = {
        "times": time_theis,
        "drawdown": theis_drawdown,
        "head": float(calibrated_signature["h_ini"]) - theis_drawdown,
        "label": "Theis (calibrated homogeneous parameters)",
    }


# ------------------------------------------------------------
# Time-series results
# ------------------------------------------------------------
if (
    theis_result is not None
    or measured_result is not None
    or st.session_state.model_results is not None
):
    st.subheader("Model results")
    st.markdown("#### Head and drawdown at the observation point")

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(7, 6), sharex=True)

    if st.session_state.model_results is not None:
        res = st.session_state.model_results
        axes[0].plot(
            res["times"] / 3600.0,
            res["obs_heads"],
            marker="o",
            linestyle="None",
            markerfacecolor="none",
            markeredgecolor="blue",
            label="MODFLOW 6",
        )
        axes[1].plot(
            res["times"] / 3600.0,
            res["obs_drawdown"],
            marker="o",
            linestyle="None",
            markerfacecolor="none",
            markeredgecolor="blue",
            label="MODFLOW 6",
        )

    if theis_result is not None:
        axes[0].plot(
            theis_result["times"] / 3600.0,
            theis_result["head"],
            linestyle="--",
            label=theis_result["label"],
        )
        axes[1].plot(
            theis_result["times"] / 3600.0,
            theis_result["drawdown"],
            linestyle="--",
            label=theis_result["label"],
        )

    if measured_result is not None:
        # Thin connecting line emphasizes the manual measurement sequence while
        # retaining individual measurement markers.
        axes[0].plot(
            measured_result["times"] / 3600.0,
            measured_result["head_noisy"],
            marker="s",
            linestyle="-",
            linewidth=0.8,
            markersize=4,
            markerfacecolor="none",
            markeredgecolor="black",
            label="Synthetic measured data",
        )
        axes[1].plot(
            measured_result["times"] / 3600.0,
            measured_result["drawdown_noisy"],
            marker="s",
            linestyle="-",
            linewidth=0.8,
            markersize=4,
            markerfacecolor="none",
            markeredgecolor="black",
            label="Synthetic measured data",
        )

    axes[0].set_title("Head over time")
    axes[0].set_ylabel("Head [m]")
    axes[0].set_xlim(0, perlen / 3600.0)
    axes[0].legend()

    axes[1].set_title("Drawdown over time")
    axes[1].set_xlabel("Time [h]")
    axes[1].set_ylabel("Drawdown [m]")
    axes[1].set_xlim(0, perlen / 3600.0)
    axes[1].legend()

    if measured_result is not None:
        # These axes belong to the measurement realization and never change
        # during a calibration sequence.
        axes[0].set_ylim(*measured_result["plot_limits"]["head"])
        axes[1].set_ylim(*measured_result["plot_limits"]["drawdown"])
    else:
        axes[0].set_ylim(top=h_ini)
        axes[1].set_ylim(bottom=0)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ------------------------------------------------------------
# Calibration comparison after reveal
# ------------------------------------------------------------
if (
    show_measured
    and measured_result is not None
    and st.session_state.calibration_revealed
    and calibration_run_current
):
    st.markdown("#### Calibration result")

    calibrated_signature = st.session_state.last_model_signature
    k_calibrated = float(calibrated_signature["k"])
    ss_calibrated = float(calibrated_signature["ss"])
    s_calibrated = ss_calibrated * float(calibrated_signature["thickness"])

    k_reference_true = float(measured_result["k_reference_true"])
    ss_true = float(measured_result["ss_true"])
    s_true = float(measured_result["S_true"])

    k_error = 100.0 * (k_calibrated - k_reference_true) / k_reference_true
    s_error = 100.0 * (s_calibrated - s_true) / s_true

    col_k, col_s = st.columns(2)
    with col_k:
        st.metric(
            "Calibrated homogeneous K [m/s]",
            f"{k_calibrated:.3e}",
            delta=f"{k_error:+.1f}% relative to reference K",
        )
        st.write(f"Hidden reference K: **{k_reference_true:.3e} m/s**")
        st.caption(
            "The synthetic aquifer is heterogeneous, so it has no single exact K. "
            f"Hidden field range: {measured_result['k_field_min']:.3e}–"
            f"{measured_result['k_field_max']:.3e} m/s; geometric mean: "
            f"{measured_result['k_field_geomean']:.3e} m/s."
        )

    with col_s:
        st.metric(
            "Calibrated storativity S [-]",
            f"{s_calibrated:.3e}",
            delta=f"{s_error:+.1f}% relative to truth",
        )
        st.write(f"Hidden storativity S: **{s_true:.3e}**")
        st.caption(
            f"Calibrated Ss = {ss_calibrated:.3e} 1/m; hidden Ss = {ss_true:.3e} 1/m. "
            "The comparison uses S = Ss × aquifer thickness, consistent with Theis."
        )

    st.info(
        "The calibrated MODFLOW model and the revealed Theis solution both use homogeneous "
        "parameters. The synthetic measurements were generated from a heterogeneous random-K "
        "MODFLOW model, so the best-fitting homogeneous K is not expected to reproduce every "
        "measurement exactly or to equal every K value in the hidden field."
    )


# ------------------------------------------------------------
# Spatial MODFLOW results
# ------------------------------------------------------------
if st.session_state.model_results is not None:
    res = st.session_state.model_results
    final_head = res["final_head"]
    final_drawdown = res["final_drawdown"]

    x = np.linspace(dx / 2.0, lx_eff - dx / 2.0, ncol)
    y = np.linspace(dx / 2.0, ly_eff - dx / 2.0, nrow)
    X, Y = np.meshgrid(x, y)

    col_head, col_drawdown = st.columns(2)

    with col_head:
        st.markdown("#### Final hydraulic head")
        fig, ax = plt.subplots(figsize=(6, 5))
        c = ax.contourf(X, Y, final_head, levels=20)
        ax.contour(X, Y, final_head, colors="black", linewidths=0.5)
        ax.plot(well_x, well_y, "ro", label="Pumping well")
        ax.plot(obs_plot_x, obs_plot_y, "bo", label="Observation point")
        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend()
        fig.colorbar(c, ax=ax, label="Head [m]")
        st.pyplot(fig)
        plt.close(fig)

    with col_drawdown:
        st.markdown("#### Final drawdown")
        fig, ax = plt.subplots(figsize=(6, 5))
        c = ax.contourf(X, Y, final_drawdown, levels=20)
        ax.contour(X, Y, final_drawdown, colors="black", linewidths=0.5)
        ax.plot(well_x, well_y, "ro", label="Pumping well")
        ax.plot(obs_plot_x, obs_plot_y, "bo", label="Observation point")
        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend()
        fig.colorbar(c, ax=ax, label="Drawdown [m]")
        st.pyplot(fig)
        plt.close(fig)
