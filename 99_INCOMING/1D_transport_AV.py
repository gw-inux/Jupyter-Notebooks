# transport_1d_app.py
# Java -> Python port (functional / non-OOP style)

import io
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.special import erfcx

ZERO = 1e-18

# Java-style method ids
INST_PULS = 0
FRST_CONT = 1
FRST_PULS = 2
THRD_CONT = 3
THRD_DECA = 4


# ----------------------------
# Numerics helpers
# ----------------------------
def xerf(a, b):
    """
    Stable computation of exp(a) * erfc(b) via:
    exp(a)*erfc(b) = exp(a - b^2) * erfcx(b)
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.exp(a - b * b) * erfcx(b)


def safe_nonzero(x):
    x = np.asarray(x, dtype=float)
    return np.where(x == 0.0, ZERO, x)


# ----------------------------
# A1 / A2 / A3 / H / M (ported from Java)
# ----------------------------
def A1(x, t, p):
    U = np.sqrt(p["pore_wtr_vel"] ** 2 + 4.0 * p["disp_coef"] * p["Rf"] * (p["lambda"] - p["alpha"]))
    denom = 2.0 * np.sqrt(p["disp_coef"] * p["Rf"] * t)

    term1 = (p["pore_wtr_vel"] / (p["pore_wtr_vel"] + U)) * xerf(
        x * (p["pore_wtr_vel"] - U) / (2.0 * p["disp_coef"]),
        (p["Rf"] * x - U * t) / denom,
    )
    term2 = (p["pore_wtr_vel"] / (p["pore_wtr_vel"] - U)) * xerf(
        x * (p["pore_wtr_vel"] + U) / (2.0 * p["disp_coef"]),
        (p["Rf"] * x + U * t) / denom,
    )
    term3 = (p["pore_wtr_vel"] ** 2 / (2.0 * p["disp_coef"] * p["Rf"] * (p["lambda"] - p["alpha"]))) * xerf(
        p["pore_wtr_vel"] * x / p["disp_coef"] + (p["alpha"] - p["lambda"]) * t,
        (p["Rf"] * x + p["pore_wtr_vel"] * t) / denom,
    )
    return term1 + term2 + term3


def A2(x, t, p):
    denom = 2.0 * np.sqrt(p["disp_coef"] * p["Rf"] * t)
    value = 0.5 * xerf(0.0, (p["Rf"] * x - p["pore_wtr_vel"] * t) / denom)
    value = value + np.sqrt(p["pore_wtr_vel"] ** 2 * t / (np.pi * p["disp_coef"] * p["Rf"])) * np.exp(
        -((p["Rf"] * x - p["pore_wtr_vel"] * t) ** 2) / (4.0 * p["disp_coef"] * p["Rf"] * t)
    )
    value = value - 0.5 * (
        1.0
        + (p["pore_wtr_vel"] * x / p["disp_coef"])
        + (p["pore_wtr_vel"] ** 2 * t / (p["disp_coef"] * p["Rf"]))
    ) * xerf(
        p["pore_wtr_vel"] * x / p["disp_coef"],
        (p["Rf"] * x + p["pore_wtr_vel"] * t) / denom,
    )
    return value


def A3(x, t, p):
    denom = 2.0 * np.sqrt(p["disp_coef"] * t)
    value = 0.5 * xerf(0.0, (x - p["pore_wtr_vel"] * t) / denom)
    value = value + np.sqrt(p["pore_wtr_vel"] ** 2 * t / (np.pi * p["disp_coef"])) * np.exp(
        -((x - p["pore_wtr_vel"] * t) ** 2) / (4.0 * p["disp_coef"] * t)
    )
    value = value - 0.5 * (
        1.0 + (p["pore_wtr_vel"] * x / p["disp_coef"]) + (p["pore_wtr_vel"] ** 2 * t / p["disp_coef"])
    ) * xerf(
        p["pore_wtr_vel"] * x / p["disp_coef"],
        (x + p["pore_wtr_vel"] * t) / denom,
    )
    return value


def H(x, t, p):
    # Java uses mu=0
    mu = 0.0
    if p["pore_wtr_vel"] > 0.0:
        u = p["pore_wtr_vel"] * np.sqrt(1.0 + 4.0 * mu * p["disp_coef"] / (p["pore_wtr_vel"] ** 2))
    else:
        u = 0.0

    denom = np.sqrt(p["disp_coef"] * p["Rf"] * t)
    return 0.5 * xerf(
        0.5 * (p["pore_wtr_vel"] - u) * x / p["disp_coef"],
        0.5 * (p["Rf"] * x - u * t) / denom,
    ) + 0.5 * xerf(
        0.5 * (p["pore_wtr_vel"] + u) * x / p["disp_coef"],
        0.5 * (p["Rf"] * x + u * t) / denom,
    )


def M(x, t, Ci, p):
    mu = 0.0
    denom = np.sqrt(p["disp_coef"] * p["Rf"] * t)
    return -Ci * np.exp(-mu * t / p["Rf"]) * (
        0.5 * xerf(0.0, 0.5 * (p["Rf"] * x - p["pore_wtr_vel"] * t) / denom)
        + 0.5 * xerf(p["pore_wtr_vel"] * x / p["disp_coef"], 0.5 * (p["Rf"] * x + p["pore_wtr_vel"] * t) / denom)
    ) + Ci * np.exp(-mu * t / p["Rf"])


# ----------------------------
# Curve computation (ported logic)
# ----------------------------
def compute_curve(method, p):
    """
    Returns x, y, x_label, title
    """
    n = int(p["num_pts"]) + 1
    if n < 2:
        n = 2

    disp = float(p["disp_coef"])
    Rf = float(p["Rf"])
    v = float(p["pore_wtr_vel"])

    # auto-scaling rules (per Java)
    xtmin, xtmax = float(p["xtmin"]), float(p["xtmax"])

    if method in (FRST_CONT, THRD_CONT, FRST_PULS, THRD_DECA):
        if p["fixed_position"] and p["auto_scale"]:
            xtmin = p["fix_pos_val"] ** 2 / (36.0 * disp) if disp != 0 else 0.0
            xtmax = p["fix_pos_val"] ** 2 / (0.01 * disp) if disp != 0 else 0.0
        if (not p["fixed_position"]) and p["auto_scale"]:
            xtmin = 0.0
            xtmax = 6.0 * np.sqrt(disp * p["fix_tim_val"])

    # build x-grid
    if p["fixed_position"]:
        if method == INST_PULS and p["auto_scale"]:
            tau = np.linspace(0.0, 2.0 * p["fix_pos_val"] / (v if v != 0 else ZERO), n)
        elif (method != INST_PULS) and p["auto_scale"] and (v / Rf) >= 0.0005:
            tau = np.linspace(0.0, 2.0 * p["fix_pos_val"] / ((v / Rf) if (v / Rf) != 0 else ZERO), n)
        elif (method in (FRST_PULS, THRD_DECA)) and p["auto_scale"] and v >= 0.0005:
            tau = np.linspace(0.0, 2.0 * p["fix_pos_val"] / (v if v != 0 else ZERO), n)
        else:
            tau = np.linspace(xtmin, xtmax, n)

        x = safe_nonzero(tau)
        x_label = "Time"
    else:
        if method == INST_PULS and p["auto_scale"]:
            xx = np.linspace(0.0, 2.0 * p["fix_tim_val"] * v, n)
        elif (method != INST_PULS) and p["auto_scale"] and (v / Rf) >= 0.0005:
            xx = np.linspace(0.0, 2.0 * (v / Rf) * p["fix_tim_val"], n)
        elif (method in (FRST_PULS, THRD_DECA)) and p["auto_scale"] and v >= 0.0005:
            xx = np.linspace(0.0, 2.0 * v * p["fix_tim_val"], n)
        else:
            xx = np.linspace(xtmin, xtmax, n)

        x = safe_nonzero(xx)
        x_label = "Distance"

    y = np.zeros_like(x, dtype=float)

    # ---- method branches
    if method == INST_PULS:
        if p["fixed_position"]:
            Pe = v * p["fix_pos_val"] / disp if disp != 0 else 0.0
            theta = v * x / (p["fix_pos_val"] * Rf) if (p["fix_pos_val"] * Rf) != 0 else 0.0
            y = (p["mass_sol"] / p["xsect_area"]) / (Rf * 2.0 * p["poros"] * np.sqrt(np.pi * disp / Rf * x)) * np.exp(
                -((1.0 - theta) ** 2) * Pe / (4.0 * theta)
            )
            title = "Instantaneous pulse (fixed position)"
        else:
            Pe = v * x / disp if disp != 0 else 0.0
            theta = v * p["fix_tim_val"] / (x * Rf)
            y = (p["mass_sol"] / p["xsect_area"]) / (Rf * 2.0 * p["poros"] * np.sqrt(np.pi * disp / Rf * p["fix_tim_val"])) * np.exp(
                -((1.0 - theta) ** 2) * Pe / (4.0 * theta)
            )
            title = "Instantaneous pulse (fixed time)"

    elif method in (FRST_CONT, THRD_CONT):
        disp_adj = disp / Rf if Rf != 0 else disp
        v_adj = v / Rf if Rf != 0 else v

        if p["fixed_position"]:
            Pe = v_adj * p["fix_pos_val"] / disp_adj if disp_adj != 0 else 0.0
            theta = v_adj * x / p["fix_pos_val"] if p["fix_pos_val"] != 0 else 0.0
            denom = 2.0 * np.sqrt(disp_adj * x) / p["fix_pos_val"] if p["fix_pos_val"] != 0 else ZERO

            if method == FRST_CONT:
                y = 0.5 * (p["c_t"] - p["c_x"]) * (xerf(0.0, (1.0 - theta) / denom) + xerf(Pe, (1.0 + theta) / denom)) + p["c_x"]
                title = "First type (continuous input) – fixed position"
            else:
                y = (p["c_t"] - p["c_x"]) * (
                    0.5 * xerf(0.0, (1.0 - theta) / denom)
                    + np.sqrt(v_adj * v_adj * x / (np.pi * disp_adj)) * np.exp(-((1.0 - theta) ** 2) * Pe / (4.0 * theta))
                    - 0.5 * (1.0 + Pe + (v_adj * v_adj * x / disp_adj)) * xerf(Pe, (1.0 + theta) / denom)
                ) + p["c_x"]
                title = "Third type (continuous input) – fixed position"

        else:
            Pe = v_adj * x / disp_adj if disp_adj != 0 else 0.0
            theta = v_adj * p["fix_tim_val"] / x
            denom = 2.0 * np.sqrt(disp_adj * p["fix_tim_val"]) / x

            if method == FRST_CONT:
                y = 0.5 * (p["c_t"] - p["c_x"]) * (xerf(0.0, (1.0 - theta) / denom) + xerf(Pe, (1.0 + theta) / denom)) + p["c_x"]
                title = "First type (continuous input) – fixed time"
            else:
                y = (p["c_t"] - p["c_x"]) * (
                    0.5 * xerf(0.0, (1.0 - theta) / denom)
                    + np.sqrt(v_adj * v_adj * p["fix_tim_val"] / (np.pi * disp_adj))
                    * np.exp(-((1.0 - theta) ** 2) * Pe / (4.0 * theta))
                    - 0.5 * (1.0 + Pe + (v_adj * v_adj * p["fix_tim_val"] / disp_adj)) * xerf(Pe, (1.0 + theta) / denom)
                ) + p["c_x"]
                title = "Third type (continuous input) – fixed time"

    elif method == FRST_PULS:
        if p["fixed_position"]:
            tau = x
            y = np.where(
                tau < p["critical_time"],
                p["c_t"] * H(p["fix_pos_val"], tau, p) + M(p["fix_pos_val"], tau, p["c_x"], p),
                p["c_t"] * H(p["fix_pos_val"], tau, p) + M(p["fix_pos_val"], tau, p["c_x"], p)
                - (p["c_t"] - p["c_x"]) * H(p["fix_pos_val"], tau - p["critical_time"], p),
            )
            title = "First order finite-duration input – fixed position"
        else:
            xx = x
            t = p["fix_tim_val"]
            y = np.where(
                t < p["critical_time"],
                p["c_t"] * H(xx, t, p) + M(xx, t, p["c_x"], p),
                p["c_t"] * H(xx, t, p) + M(xx, t, p["c_x"], p)
                - (p["c_t"] - p["c_x"]) * H(xx, t - p["critical_time"], p),
            )
            title = "First order finite-duration input – fixed time"

    elif method == THRD_DECA:
        if p["fixed_position"]:
            tau = x

            if p["alpha"] == 0.0 and p["lambda"] == 0.0 and p["Rf"] == 1.0:
                base = A3(p["fix_pos_val"], tau, p)
                base_shift = A3(p["fix_pos_val"], tau - p["critical_time"], p)
            elif p["alpha"] == 0.0 and p["lambda"] == 0.0:
                base = A2(p["fix_pos_val"], tau, p)
                base_shift = A2(p["fix_pos_val"], tau - p["critical_time"], p)
            elif p["alpha"] == p["lambda"]:
                base = np.exp(-p["alpha"] * tau) * A2(p["fix_pos_val"], tau, p)
                base_shift = (np.exp(-p["alpha"] * (tau - p["critical_time"])) * A2(p["fix_pos_val"], tau - p["critical_time"], p)) * np.exp(
                    -p["alpha"] * p["critical_time"]
                )
            else:
                base = np.exp(-p["alpha"] * tau) * A1(p["fix_pos_val"], tau, p)
                base_shift = (np.exp(-p["alpha"] * (tau - p["critical_time"])) * A1(p["fix_pos_val"], tau - p["critical_time"], p)) * np.exp(
                    -p["alpha"] * p["critical_time"]
                )

            y = np.where(
                tau < p["critical_time"],
                (p["c_t"] - p["c_x"]) * base + p["c_x"],
                (p["c_t"] - p["c_x"]) * (base - base_shift) + p["c_x"],
            )
            title = "Third order with decay – fixed position"

        else:
            xx = x
            t = p["fix_tim_val"]

            if p["alpha"] == 0.0 and p["lambda"] == 0.0 and p["Rf"] == 1.0:
                base = A3(xx, t, p)
                base_shift = A3(xx, t - p["critical_time"], p) if t >= p["critical_time"] else 0.0
            elif p["alpha"] == 0.0 and p["lambda"] == 0.0:
                base = A2(xx, t, p)
                base_shift = A2(xx, t - p["critical_time"], p) if t >= p["critical_time"] else 0.0
            elif p["alpha"] == p["lambda"]:
                base = np.exp(-p["alpha"] * t) * A2(xx, t, p)
                base_shift = (
                    (np.exp(-p["alpha"] * (t - p["critical_time"])) * A2(xx, t - p["critical_time"], p)) * np.exp(-p["alpha"] * p["critical_time"])
                    if t >= p["critical_time"]
                    else 0.0
                )
            else:
                base = np.exp(-p["alpha"] * t) * A1(xx, t, p)
                base_shift = (
                    (np.exp(-p["alpha"] * (t - p["critical_time"])) * A1(xx, t - p["critical_time"], p)) * np.exp(-p["alpha"] * p["critical_time"])
                    if t >= p["critical_time"]
                    else 0.0
                )

            y = (p["c_t"] - p["c_x"]) * base + p["c_x"] if t < p["critical_time"] else (p["c_t"] - p["c_x"]) * (base - base_shift) + p["c_x"]
            title = "Third order with decay – fixed time"

    else:
        raise ValueError(f"Unsupported method id: {method}")

    y = np.maximum(np.asarray(y, dtype=float), 0.0)
    return np.asarray(x, float), y, x_label, title


# ----------------------------
# Streamlit app
# ----------------------------
st.set_page_config(page_title="1D Transport Curves")
st.title("1D Solute Transport")
st.subheader('Transfer from JAVA from *eq_sorption_decay*', divider = 'green')

st.markdown("The subsequent app is the transfer of the JAVA code from http://hydrolab.illinois.edu/gw_applets/. The apps are not yet optimized for the Streamlit User Interface")

st.subheader('Interactive plot', divider = 'green')
def main():

    
    if "latest_curve" not in st.session_state:
        st.session_state.latest_curve = None

#UI - NEEDS REVISION

#    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1.2])
    c1, c2 = st.columns([1,1])
    with c1:
        method_labels = {
            INST_PULS: "Instantaneous pulse",
            FRST_CONT: "First type (continuous)",
            FRST_PULS: "First type (finite duration)",
            THRD_CONT: "Third type (continuous)",
            THRD_DECA: "Third type (with decay)",
        }
        method = st.selectbox("Model method", options=list(method_labels.keys()), format_func=lambda k: method_labels[k])
        fixed_position = st.radio(
            "Plot mode",
            options=[True, False],
            format_func=lambda v: "Fixed position (x fixed → plot vs time)" if v else "Fixed time (t fixed → plot vs distance)",
        )
        auto_scale = st.checkbox("Auto scale x-range", value=True)
    
    with c2:
        disp_coef = st.number_input("Dispersion coefficient", value=1.0, min_value=0.0, format="%.6g")
        pore_wtr_vel = st.number_input("Pore water velocity", value=1.0, format="%.6g")
        use_retard = st.checkbox("Use retardation factor (Rf)", value=False)
        Rf = st.number_input("Rf", value=1.0, min_value=1e-12, format="%.6g", disabled=not use_retard)
        #num_pts = st.number_input("Number of points", value=200, min_value=10, max_value=5000, step=10)
        num_pts = 100
    st.markdown('---')
    
    c3, c4 = st.columns([1,1])
    with c3:
        fix_pos_val = st.number_input("Fixed position value (x)", value=10.0, min_value=0.0, format="%.6g", disabled=not fixed_position)
        fix_tim_val = st.number_input("Fixed time value (t)", value=10.0, min_value=0.0, format="%.6g", disabled=fixed_position)
        if auto_scale:
            xtmin, xtmax = 0.0, 0.0
            st.caption("Manual x-range hidden because auto-scale is enabled.")
        else:
            xtmin = st.number_input("x-range min", value=0.0, format="%.6g")
            xtmax = st.number_input("x-range max", value=100.0, format="%.6g")
    with c4:
        # defaults
        mass_sol, xsect_area, poros = 1.0, 1.0, 0.25
        c_t, c_x, critical_time = 1.0, 0.0, 10.0
        alpha, lambda_ = 0.0, 0.0
        if method == INST_PULS:
            mass_sol = st.number_input("Mass of solute", value=1.0, format="%.6g")
            xsect_area = st.number_input("Cross-sectional area", value=1.0, min_value=1e-12, format="%.6g")
            poros = st.number_input("Porosity", value=0.25, min_value=1e-12, max_value=1.0, format="%.6g")
        else:
            c_t = st.number_input("c_t (boundary concentration)", value=1.0, format="%.6g")
            c_x = st.number_input("c_x (initial concentration)", value=0.0, format="%.6g")
            if method in (FRST_PULS, THRD_DECA):
                critical_time = st.number_input("Critical time (pulse duration)", value=10.0, min_value=0.0, format="%.6g")
            if method == THRD_DECA:
                alpha = st.number_input("alpha", value=0.0, min_value=0.0, format="%.6g")
                lambda_ = st.number_input("lambda", value=0.0, min_value=0.0, format="%.6g")
        st.write("")
    
    c5, c6, c7 = st.columns([1,1,1])
    with c6:
        compute = st.button("Compute (replace latest)", type="primary")
    with c7:
        clear = st.button("Clear latest curve")

    if clear:
        st.session_state.latest_curve = None

    if compute:
        p = {
            "disp_coef": float(disp_coef),
            "Rf": float(Rf if use_retard else 1.0),
            "pore_wtr_vel": float(pore_wtr_vel),
            "num_pts": int(num_pts),
            "fixed_position": bool(fixed_position),
            "fix_pos_val": float(fix_pos_val),
            "fix_tim_val": float(fix_tim_val),
            "auto_scale": bool(auto_scale),
            "xtmin": float(xtmin),
            "xtmax": float(xtmax),
            "mass_sol": float(mass_sol),
            "xsect_area": float(xsect_area),
            "poros": float(poros),
            "c_t": float(c_t),
            "c_x": float(c_x),
            "critical_time": float(critical_time),
            "alpha": float(alpha),
            "lambda": float(lambda_),
        }

        x, y, x_label, title = compute_curve(method, p)
        st.session_state.latest_curve = {"x": x, "y": y, "x_label": x_label, "title": title, "params": p, "method": method}

    curve = st.session_state.latest_curve
    if curve is None:
        st.info("No curve computed yet.")
        return

    x = curve["x"]
    y = curve["y"]

    out1, out2 = st.columns([2.2, 1.0])

    with out1:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel(curve["x_label"])
        ax.set_ylabel("Concentration")
        ax.set_title(curve["title"])
        ax.grid(True)
        st.pyplot(fig, clear_figure=True)

    with out2:
        st.write("Probe (slider)")
        x_min, x_max = float(np.min(x)), float(np.max(x))
        probe = st.slider("Probe at x", min_value=x_min, max_value=x_max, value=(x_min + x_max) / 2.0)
        y_probe = float(np.interp(probe, x, y))
        st.write("Interpolated concentration", f"{y_probe:.6g}")

    with st.expander('Click here to see data'):
        st.write("Latest curve data")
        show_n = st.number_input("Rows to show", min_value=10, max_value=int(len(x)), value=min(50, int(len(x))), step=10)
        st.dataframe(
            {"x": x[: int(show_n)], "c": y[: int(show_n)]},
            use_container_width=True,
            hide_index=True,
        )
        buf = io.StringIO()
        buf.write("x,c\n")
        for xi, yi in zip(x, y):
            buf.write(f"{xi},{yi}\n")
        st.download_button(
            "Download CSV (latest curve)",
            data=buf.getvalue().encode("utf-8"),
            file_name="latest_curve.csv",
            mime="text/csv",
        )


main()
