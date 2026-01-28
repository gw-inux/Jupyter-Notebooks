# hob_scatter_app.py
import io
from math import sqrt
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.metrics import mean_squared_error


RENAME_MAP = {
    "SIMULATED EQUIVALENT": "Simulated Head",
    "OBSERVED VALUE": "Observed Head",
    "OBSERVATION NAME": "Piezometer",
}

REQUIRED_COLS_RAW = set(RENAME_MAP.keys())

#---FUNCTIONS
def read_hob_out(uploaded_file) -> pd.DataFrame:
    raw_bytes = uploaded_file.getvalue()
    text = raw_bytes.decode("utf-8", errors="replace")
    lines = text.splitlines()

    if not lines:
        raise ValueError("Uploaded file is empty.")

    header = lines[0].strip()

    # Case 1: quoted header like: "SIMULATED EQUIVALENT" "OBSERVED VALUE" "OBSERVATION NAME"
    if '"' in header:
        colnames = re.findall(r'"([^"]+)"', header)
        if len(colnames) >= 3:
            # Read remaining lines as whitespace-separated data
            df = pd.read_csv(
                io.StringIO("\n".join(lines[1:])),
                sep=r"\s+",
                engine="python",
                names=colnames[:3],
                header=None,
            )
            return df

    # Case 2: fallback (non-quoted header or other formats)
    df = pd.read_csv(io.StringIO(text), sep=r"\s+", engine="python")
    return df

def process_hob_df(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Renames columns, computes residuals, filters dry cells, computes RMSE.
    Returns:
      - df_all: full processed df (with Residual, index by Piezometer if available)
      - df_fil: filtered df (dry removed)
      - rmse: RMSE on filtered data
    """
    # Rename if those columns exist
    missing = REQUIRED_COLS_RAW - set(df.columns)
    if missing:
        raise ValueError(
            "Could not find expected columns in file. Missing: "
            + ", ".join(sorted(missing))
            + "\n\nColumns found: "
            + ", ".join(map(str, df.columns))
        )

    df = df.copy()
    df.rename(columns=RENAME_MAP, inplace=True)

    # Index by piezometer name if present
    if "Piezometer" in df.columns:
        df.set_index("Piezometer", inplace=True)

    # Residual
    df["Residual"] = df["Simulated Head"] - df["Observed Head"]

    # Filter dry simulated heads
    df_fil = df[df["Simulated Head"] > -10000].copy()

    # RMSE computed on filtered data
    rmse = sqrt(mean_squared_error(df_fil["Observed Head"].values, df_fil["Simulated Head"].values))
    rmse = round(rmse, 3)

    return df, df_fil, rmse

def make_scatter_figure(df_fil: pd.DataFrame, title: str):
    fig = plt.figure(figsize=(8, 7))
    
    data_min_raw = min(
        df_fil["Observed Head"].min(),
        df_fil["Simulated Head"].min(),
    )
    data_max_raw = max(
        df_fil["Observed Head"].max(),
        df_fil["Simulated Head"].max(),
    )
    
    data_range = data_max_raw - data_min_raw
    pad = 0.10 * data_range
    
    data_min = data_min_raw - pad
    data_max = data_max_raw + pad

    x = np.linspace(data_min, data_max, 200)

    plt.plot(x, x, linestyle="solid")
    plt.plot(x, x + 0.5, linestyle="dashed")
    plt.plot(x, x - 0.5, linestyle="dashed")
    
    # Determine symmetric color scale based on residuals
    max_abs_res = np.max(np.abs(df_fil["Residual"].values))
    cbar_lim = np.ceil(max_abs_res)

    # --- Calibration statistics textbox (ME / MAE / RMSE)
    measured = df_fil["Observed Head"].values
    computed = df_fil["Simulated Head"].values
    me, mae, rmse = compute_statistics(measured, computed)

    out_txt = "\n".join((
        rf"$ME = {me:.3f}$ m",
        rf"$MAE = {mae:.3f}$ m",
        rf"$RMSE = {rmse:.3f}$ m",
    ))

    # Place textbox relative to current axis range (like your example)
    x_pos = data_min + 0.95 * (data_max - data_min)
    y_pos = data_min + 0.05 * (data_max - data_min)

    plt.text(
        x_pos, y_pos, out_txt,
        ha="right", va="bottom",
        bbox=dict(boxstyle="square", facecolor="linen", alpha=0.9),
        fontsize=14
    )


    sc = plt.scatter(
        df_fil["Observed Head"],
        df_fil["Simulated Head"],
        marker="o",
        c=df_fil["Residual"],
        vmin=-cbar_lim,
        vmax= cbar_lim,
    )

    plt.xlim(data_min, data_max)
    plt.ylim(data_min, data_max)
    plt.gca().set_aspect("equal", adjustable="box")

    cbar = plt.colorbar(sc)
    cbar.set_label("Residual (m)", fontsize=14)

    plt.grid(True)
    plt.title(f"{title}", fontsize=16)
    plt.xlabel("Observed Head (m)", fontsize=14)
    plt.ylabel("Simulated Head (m)", fontsize=14)
    
    ax = plt.gca()
    ax.tick_params(axis="both", labelsize=14)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    fig.tight_layout()
    return fig

def fig_to_png_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()

# Postprocessing statistics
def compute_statistics(measured, computed):
    # Calculate the number of values
    n = len(measured)

    # Initialize a variable to store the sum of squared differences
    total_me = 0
    total_mae = 0
    total_rmse = 0

    # Loop through each value
    for i in range(n): # Add the squared difference to the total
        total_me   += (computed[i] - measured[i])
        total_mae  += (abs(computed[i] - measured[i]))
        total_rmse += (computed[i] - measured[i])**2

    # Calculate the me, mae, mean squared error
    me = total_me / n
    mae = total_mae / n
    meanSquaredError = total_rmse / n

    # Raise the mean squared error to the power of 0.5 
    rmse = (meanSquaredError) ** (1/2)
    return me, mae, rmse
    
# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="HOB Scatter")
st.title("MODFLOW HOB Scatter Plot (Observed vs Simulated)")

st.markdown(
    """
Upload a `*.hob_out` file from the MODFLOW **Head Observation (HOB)** package.
The app computes residuals and RMSE, filters “dry” simulated heads (`<= -10000`),
and produces a scatter plot colored by residual.
"""
)

st.header("Plot settings")
title = st.text_input("Plot title", value="HOB scatter")
#vmin = st.number_input("Residual color scale min (m)", value=-3.0, step=0.5)
#vmax = st.number_input("Residual color scale max (m)", value=3.0, step=0.5)

uploaded = st.file_uploader(
    "Upload MODFLOW HOB output (*.hob_out)",
    type=["hob_out", "out", "txt", "dat", "csv"],
    accept_multiple_files=False,
)

if not uploaded:
    st.info("Please upload a `*.hob_out` file to start.")
    st.stop()

try:
    df_raw = read_hob_out(uploaded)
    df_all, df_fil, rmse = process_hob_df(df_raw)

    # Quick stats
    residuals = df_fil["Residual"].astype(float)
    stats = pd.DataFrame(
        {
            "N (filtered)": [len(df_fil)],
            "RMSE (m)": [rmse],
            "Mean residual (m)": [round(residuals.mean(), 3)],
            "Median residual (m)": [round(residuals.median(), 3)],
            "Std residual (m)": [round(residuals.std(ddof=1), 3) if len(residuals) > 1 else np.nan],
            "Min residual (m)": [round(residuals.min(), 3)],
            "Max residual (m)": [round(residuals.max(), 3)],
        }
    )

    fig = make_scatter_figure(df_fil, title=title)
    st.pyplot(fig, clear_figure=False)
    
    png_bytes = fig_to_png_bytes(fig)
    
    safe_title = title.strip().replace(" ", "_")
    
    st.download_button(
        label="Download figure (PNG)",
        data=png_bytes,
        file_name=f"{safe_title}.png",
        mime="image/png",
    )

    with st.expander('Open to see more calibration statistics'):
        st.write("**Calibration statistics**")
    
        st.write(f"Number of observations (filtered): {len(df_fil)}")
        st.write(f"Mean residual (ME): {residuals.mean():.3f} m")
        st.write(f"Mean absolute error (MAE): {np.abs(residuals).mean():.3f} m")
        st.write(f"Root mean square error (RMSE): {rmse:.3f} m")
        st.write(f"Residual standard deviation: {residuals.std(ddof=1):.3f} m")
        min_res_id = residuals.idxmin()
        max_res_id = residuals.idxmax()
    
        st.write(
            f"Minimum residual: {residuals.min():.3f} m "
            f"(Observation: {min_res_id})"
        )
        st.write(
            f"Maximum residual: {residuals.max():.3f} m "
            f"(Observation: {max_res_id})"
        )
    
    with st.expander('Open to see the processed data'):
        st.write("Preview (first rows)")
        st.dataframe(df_all.head(20), use_container_width=True)

except Exception as e:
    st.error("Could not process the uploaded file.")
    st.exception(e)
