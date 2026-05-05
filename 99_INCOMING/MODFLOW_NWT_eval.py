import os
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import flopy
import pandas as pd


st.set_page_config(page_title="MODFLOW-NWT 1D Unconfined Flow")

st.title("1D Unconfined Groundwater Flow with Recharge")

st.markdown(
    """
    This app uses **MODFLOW-NWT** to simulate steady 1D groundwater flow in a
    homogeneous, isotropic, unconfined aquifer between two specified-head boundaries.
    Areal recharge is applied from the top.
    
    The results from **MODFLOW-NWT** are compared to an analytical solution. 
    Additionally, the app allows computing the same situation with **MODFLOW-2005**.
    """
)

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "nwt_done" not in st.session_state:
    st.session_state.nwt_done = False

if "heads_nwt" not in st.session_state:
    st.session_state.heads_nwt = None

if "heads_2005" not in st.session_state:
    st.session_state.heads_2005 = None

if "model_signature" not in st.session_state:
    st.session_state.model_signature = None


# ------------------------------------------------------------
# Input
# ------------------------------------------------------------
st.header("Model setup")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Discretization"):
        length = st.number_input(
            "Model length L [m]",
            value=5000.0,
            min_value=100.0,
            step=100.0,
        )
        ncol = st.number_input(
            "Number of columns",
            value=101,
            min_value=5,
            step=10,
        )
        aquifer_bottom = st.number_input(
            "Aquifer bottom [m]",
            value=0.0,
            step=1.0,
        )

with col2:
    with st.expander("Parameter and BC's"):
        k = st.number_input(
            "Hydraulic conductivity K [m/d]",
            value=50.0,
            min_value=0.001,
            step=1.0,
        )
        recharge = st.number_input(
            "Recharge R [m/d]",
            value=0.001,
            step=0.0001,
            format="%.5f",
        )
        h_left = st.number_input(
            "Left specified head [m]",
            value=10.0,
            step=1.0,
        )
        h_right = st.number_input(
            "Right specified head [m]",
            value=50.0,
            step=1.0,
        )

with col3:
    with st.expander("Model settings"):
        exe_name = st.text_input(
            "MODFLOW-NWT executable",
            value="MODFLOW-NWT_64.exe",
        )
        exe_name_2005 = st.text_input(
            "MODFLOW-2005 executable",
            value="mf2005.exe",
        )


# ------------------------------------------------------------
# Current model signature
# ------------------------------------------------------------
current_signature = {
    "length": length,
    "ncol": int(ncol),
    "aquifer_bottom": aquifer_bottom,
    "k": k,
    "recharge": recharge,
    "h_left": h_left,
    "h_right": h_right,
}

inputs_match_results = (
    st.session_state.model_signature == current_signature
)

results_are_valid = (
    st.session_state.nwt_done
    and st.session_state.heads_nwt is not None
    and inputs_match_results
)


# ------------------------------------------------------------
# Buttons
# ------------------------------------------------------------
colr1, colr2, colr3, colr4 = st.columns(4)

with colr2:
    run_model_nwt = st.button("Run MODFLOW-NWT")

with colr3:
    run_model_2005 = st.button(
        "Run MODFLOW-2005",
        disabled=not results_are_valid,
    )

with colr4:
    show_scatter = st.toggle(
        "Show scatter plot",
        value=False,
        disabled=not results_are_valid,
    )


# ------------------------------------------------------------
# Grid
# ------------------------------------------------------------
ncol = int(ncol)

delr = length / (ncol - 1)
x = np.zeros(ncol)

for i in range(1, ncol):
    x[i] = x[i - 1] + delr

delc = 1.0
top = max(h_left, h_right) + 20.0


# ------------------------------------------------------------
# Analytical solution
# ------------------------------------------------------------
def analytical_head(x, L, h0, hL, K, R):
    """
    Dupuit analytical solution for steady unconfined 1D flow with recharge.

    h(x)^2 = h0^2 + [(hL^2 - h0^2)/L + (R/K) L] x - (R/K) x^2
    """
    h2 = (
        h0**2
        + ((hL**2 - h0**2) / L + (R / K) * L) * x
        - (R / K) * x**2
    )
    return np.sqrt(np.maximum(h2, 0.0))


h_ana = analytical_head(x, length, h_left, h_right, k, recharge)


# ------------------------------------------------------------
# Build and run MODFLOW-NWT model
# ------------------------------------------------------------
def build_and_run_model():
    ws = tempfile.mkdtemp()
    modelname = "nwt_1d_recharge"

    m = flopy.modflow.Modflow(
        modelname=modelname,
        exe_name=exe_name,
        version="mfnwt",
        model_ws=ws,
    )

    flopy.modflow.ModflowDis(
        m,
        nlay=1,
        nrow=1,
        ncol=ncol,
        nper=1,
        delr=delr,
        delc=delc,
        top=top,
        botm=aquifer_bottom,
        steady=True,
        itmuni=4,
        lenuni=2,
    )

    ibound = np.ones((1, 1, ncol), dtype=int)
    ibound[0, 0, 0] = -1
    ibound[0, 0, -1] = -1

    strt = np.ones((1, 1, ncol)) * ((h_left + h_right) / 2)
    strt[0, 0, 0] = h_left
    strt[0, 0, -1] = h_right

    flopy.modflow.ModflowBas(m, ibound=ibound, strt=strt)

    flopy.modflow.ModflowUpw(
        m,
        laytyp=1,
        hk=k,
        vka=k,
        sy=0.15,
        ss=1e-5,
        ipakcb=53,
    )

    rech_array = np.ones((1, ncol)) * recharge
    flopy.modflow.ModflowRch(m, rech=rech_array)

    flopy.modflow.ModflowNwt(
        m,
        headtol=1e-6,
        fluxtol=500.0,
        maxiterout=100,
        thickfact=1e-5,
        linmeth=1,
        iprnwt=0,
        ibotav=0,
        options="COMPLEX",
    )

    flopy.modflow.ModflowOc(
        m,
        stress_period_data={(0, 0): ["save head", "save budget"]},
        compact=True,
    )

    m.write_input()
    success, buff = m.run_model(silent=True)

    if not success:
        return None, ws, buff

    hds = flopy.utils.HeadFile(os.path.join(ws, modelname + ".hds"))
    heads = hds.get_data(kstpkper=(0, 0))[0, 0, :]

    return heads, ws, buff


# ------------------------------------------------------------
# Build and run MODFLOW-2005 model
# ------------------------------------------------------------
def build_and_run_model_2005():
    ws = tempfile.mkdtemp()
    modelname = "mf2005_1d_recharge"

    m = flopy.modflow.Modflow(
        modelname=modelname,
        exe_name=exe_name_2005,
        version="mf2005",
        model_ws=ws,
    )

    flopy.modflow.ModflowDis(
        m,
        nlay=1,
        nrow=1,
        ncol=ncol,
        nper=1,
        delr=delr,
        delc=delc,
        top=top,
        botm=aquifer_bottom,
        steady=True,
        itmuni=4,
        lenuni=2,
    )

    ibound = np.ones((1, 1, ncol), dtype=int)
    ibound[0, 0, 0] = -1
    ibound[0, 0, -1] = -1

    strt = np.ones((1, 1, ncol)) * ((h_left + h_right) / 2)
    strt[0, 0, 0] = h_left
    strt[0, 0, -1] = h_right

    flopy.modflow.ModflowBas(m, ibound=ibound, strt=strt)

    flopy.modflow.ModflowLpf(
        m,
        laytyp=1,
        hk=k,
        vka=k,
        sy=0.15,
        ss=1e-5,
        ipakcb=53,
    )

    rech_array = np.ones((1, ncol)) * recharge
    flopy.modflow.ModflowRch(m, rech=rech_array)

    flopy.modflow.ModflowPcg(
        m,
        hclose=1e-6,
        rclose=1e-3,
        mxiter=100,
        iter1=50,
    )

    flopy.modflow.ModflowOc(
        m,
        stress_period_data={(0, 0): ["save head", "save budget"]},
        compact=True,
    )

    m.write_input()
    success, buff = m.run_model(silent=True)

    if not success:
        return None, ws, buff

    hds = flopy.utils.HeadFile(os.path.join(ws, modelname + ".hds"))
    heads = hds.get_data(kstpkper=(0, 0))[0, 0, :]

    return heads, ws, buff


# ------------------------------------------------------------
# Run models
# ------------------------------------------------------------
if run_model_nwt:
    heads_nwt, ws_nwt, buff_nwt = build_and_run_model()

    if heads_nwt is None:
        st.error("MODFLOW-NWT did not terminate normally.")
        st.text("\n".join(buff_nwt[-30:]))
    else:
        st.session_state.heads_nwt = heads_nwt
        st.session_state.heads_2005 = None
        st.session_state.nwt_done = True
        st.session_state.model_signature = current_signature

        st.success("MODFLOW-NWT run completed.")
        st.rerun()


if run_model_2005:
    heads_2005, ws_2005, buff_2005 = build_and_run_model_2005()

    if heads_2005 is None:
        st.error("MODFLOW-2005 did not terminate normally.")
        st.text("\n".join(buff_2005[-30:]))
    else:
        st.session_state.heads_2005 = heads_2005
        st.success("MODFLOW-2005 run completed.")


# ------------------------------------------------------------
# Re-check result validity after possible rerun
# ------------------------------------------------------------
inputs_match_results = (
    st.session_state.model_signature == current_signature
)

results_are_valid = (
    st.session_state.nwt_done
    and st.session_state.heads_nwt is not None
    and inputs_match_results
)


# ------------------------------------------------------------
# Display results
# ------------------------------------------------------------
if results_are_valid:

    heads_nwt = st.session_state.heads_nwt
    heads_2005 = st.session_state.heads_2005

    error_nwt = h_ana - heads_nwt
    rmse_nwt = np.sqrt(np.mean(error_nwt**2))

    if heads_2005 is not None:
        error_2005 = h_ana - heads_2005
        rmse_2005 = np.sqrt(np.mean(error_2005**2))

    # ------------------------------------------------------------
    # Main plot
    # ------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(9, 6))

    ax1.plot(
        x,
        h_ana,
        label="Analytical head",
        color="blue",
    )

    ax1.plot(
        x,
        heads_nwt,
        marker="o",
        linestyle="None",
        markerfacecolor="none",
        markeredgecolor="violet",
        markersize=6,
        label="MF-NWT head",
        alpha=0.8,
    )

    if heads_2005 is not None:
        ax1.plot(
            x,
            heads_2005,
            marker="x",
            linestyle="None",
            markeredgecolor="lime",
            markersize=4,
            label="MF-2005 head",
            alpha=0.8,
        )

    ax1.set_xlabel("Distance along model [m]", fontsize = 12)
    ax1.set_ylabel("Head [m]", fontsize = 12)
    ax1.set_xlim(0, length)

    ax2 = ax1.twinx()

    ax2.plot(
        x,
        error_nwt,
        label="Error MF-NWT",
        linestyle="--",
        color="violet",
    )

    if heads_2005 is not None:
        ax2.plot(
            x,
            error_2005,
            label="Error MF-2005",
            linestyle="--",
            color="lime",
        )

    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_ylabel("Head error analytical - numerical [m]", fontsize = 12)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        fontsize = 12,
        loc="upper right",
    )

    st.pyplot(fig)

    # ------------------------------------------------------------
    # Optional scatter plot
    # ------------------------------------------------------------
    if show_scatter:
        fig_scatter, ax = plt.subplots(figsize=(9, 9))

        min_head = min(np.min(h_ana), np.min(heads_nwt))
        max_head = max(np.max(h_ana), np.max(heads_nwt))

        if heads_2005 is not None:
            min_head = min(min_head, np.min(heads_2005))
            max_head = max(max_head, np.max(heads_2005))

        ax.plot(
            [min_head, max_head],
            [min_head, max_head],
            color="black",
            lw=1,
            label="1:1 line",
        )

        ax.scatter(
            h_ana,
            heads_nwt,
            facecolors="none",
            edgecolors="violet",
            label=f"MF-NWT, RMSE = {rmse_nwt:.4f} m",
        )

        if heads_2005 is not None:
            ax.scatter(
                h_ana,
                heads_2005,
                marker="x",
                color="lime",
                label=f"MF-2005, RMSE = {rmse_2005:.4f} m",
            )

        ax.set_xlabel("Analytical head [m]", fontsize = 12)
        ax.set_ylabel("Numerical head [m]", fontsize = 12)
        ax1.set_xlim(min(h_left, h_right), max(h_left, h_right)*1.1)
        ax1.set_ylim(min(h_left, h_right), max(h_left, h_right)*1.1)
        ax.set_aspect("equal", adjustable="box")
        ax.legend(fontsize = 12)

        st.pyplot(fig_scatter)

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    st.subheader("Numerical comparison")

    if heads_2005 is not None:
        c1, c2, c3, c4, c5, c6 = st.columns(6)

        c1.write("Max. abs. error NWT [m]")
        c1.write(f"{np.max(np.abs(error_nwt)):.4f}")

        c2.write("Mean abs. error NWT [m]")
        c2.write(f"{np.mean(np.abs(error_nwt)):.4f}")

        c3.write("RMSE NWT [m]")
        c3.write(f"{rmse_nwt:.4f}")

        c4.write("Max. abs. error 2005 [m]")
        c4.write(f"{np.max(np.abs(error_2005)):.4f}")

        c5.write("Mean abs. error 2005 [m]")
        c5.write(f"{np.mean(np.abs(error_2005)):.4f}")

        c6.write("RMSE 2005 [m]")
        c6.write(f"{rmse_2005:.4f}")

    else:
        c1, c2, c3 = st.columns(3)

        c1.write("Max. abs. error NWT [m]")
        c1.write(f"{np.max(np.abs(error_nwt)):.4f}")

        c2.write("Mean abs. error NWT [m]")
        c2.write(f"{np.mean(np.abs(error_nwt)):.4f}")

        c3.write("RMSE NWT [m]")
        c3.write(f"{rmse_nwt:.4f}")

    # ------------------------------------------------------------
    # Data table
    # ------------------------------------------------------------
    st.subheader("Selected results")

    data = {
        "x [m]": x,
        "Analytical head [m]": h_ana,
        "MODFLOW-NWT head [m]": heads_nwt,
        "Error NWT [m]": error_nwt,
    }

    if heads_2005 is not None:
        data["MODFLOW-2005 head [m]"] = heads_2005
        data["Error MODFLOW-2005 [m]"] = error_2005
        data["NWT - MODFLOW-2005 [m]"] = heads_nwt - heads_2005

    df = pd.DataFrame(data)
    st.dataframe(df.round(4), use_container_width=True)

else:
    if st.session_state.nwt_done:
        st.warning(
            "The model setup has changed. Please run MODFLOW-NWT again "
            "before displaying or comparing results."
        )
    else:
        st.info("Adjust the parameters and press **Run MODFLOW-NWT**.")