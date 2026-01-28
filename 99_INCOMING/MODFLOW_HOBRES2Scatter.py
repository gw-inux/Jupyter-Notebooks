# hob_scatter_app.py
import io
from math import sqrt
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import streamlit as st

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1]  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- Functions

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

#def read_res_file(uploaded_file) -> pd.DataFrame:
#    raw_bytes = uploaded_file.getvalue()
#    text = raw_bytes.decode("utf-8", errors="replace")
#    df = pd.read_csv(io.StringIO(text), sep=r"\s+", engine="python")
#    # normalize column names (strip spaces)
#    df.columns = [str(c).strip() for c in df.columns]
#    return df
    
def read_res_file(uploaded_file) -> pd.DataFrame:
    raw_bytes = uploaded_file.getvalue()
    text = raw_bytes.decode("utf-8", errors="replace")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    if not lines:
        raise ValueError("Uploaded RES file is empty.")

    # Read header normally (whitespace split)
    header_tokens = lines[0].split()
    ncol = len(header_tokens)

    rows = []
    for ln in lines[1:]:
        toks = ln.split()

        # Fix known issue: "Cov. Mat." split into two tokens -> merge into one
        # Only apply when we have one extra token compared to header
        if len(toks) == ncol + 1:
            for i in range(len(toks) - 1):
                if toks[i] == "Cov." and toks[i + 1] == "Mat.":
                    toks = toks[:i] + ["Cov. Mat."] + toks[i + 2:]
                    break

        # If still mismatching, skip line (robust handling)
        if len(toks) != ncol:
            continue

        rows.append(toks)

    df = pd.DataFrame(rows, columns=header_tokens)
    df.columns = [str(c).strip() for c in df.columns]
    return df

    
def standardize_for_scatter(df: pd.DataFrame, file_kind: str) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    if file_kind == "hob":
        # existing HOB rename
        missing = REQUIRED_COLS_RAW - set(df.columns)
        if missing:
            raise ValueError(
                "Could not find expected columns in file. Missing: "
                + ", ".join(sorted(missing))
                + "\n\nColumns found: "
                + ", ".join(map(str, df.columns))
            )

        df.rename(columns=RENAME_MAP, inplace=True)
        if "Piezometer" in df.columns:
            df.set_index("Piezometer", inplace=True)
        df["Residual"] = df["Simulated Head"] - df["Observed Head"]

    elif file_kind == "res":
        # expected columns from RES file (as in your example)
        needed = {"Name", "Measured", "Modelled"}
        missing = needed - set(df.columns)
        if missing:
            raise ValueError(
                "RES file must contain columns: Name, Measured, Modelled. Missing: "
                + ", ".join(sorted(missing))
                + "\n\nColumns found: "
                + ", ".join(map(str, df.columns))
            )

        df.rename(
            columns={
                "Name": "Piezometer",
                "Measured": "Observed Head",
                "Modelled": "Simulated Head",
            },
            inplace=True,
        )

        if "Piezometer" in df.columns:
            df.set_index("Piezometer", inplace=True)

        # --- Coerce key columns to numeric (handles "na", "Cov. Mat.", etc.)
        for col in ["Observed Head", "Simulated Head", "Residual", "Weight"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows where we can't plot (Observed/Simulated must be numeric)
        df = df.dropna(subset=["Observed Head", "Simulated Head"]).copy()

        # If residual missing/invalid, recompute
        if "Residual" not in df.columns or df["Residual"].isna().all():
            df["Residual"] = df["Simulated Head"] - df["Observed Head"]
        else:
            df["Residual"] = df["Residual"].fillna(df["Simulated Head"] - df["Observed Head"])

        # Use provided residual if present, otherwise compute
        if "Residual" not in df.columns:
            df["Residual"] = df["Simulated Head"] - df["Observed Head"]

    else:
        raise ValueError("Unknown file_kind")

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

    return df, df_fil

def make_scatter_figure(df_fil: pd.DataFrame, title: str, me: float, mae: float, rmse: float,
                        obs_label: str, sim_label: str, unit: str, alphas=None, dotsize = int):
                            
    fig, ax = plt.subplots(figsize=(8, 7))
    
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

    ax.plot(x, x, linestyle="solid")
    ax.plot(x, x + 0.5, linestyle="dashed", linewidth=0.8, alpha=0.4)
    ax.plot(x, x - 0.5, linestyle="dashed", linewidth=0.8, alpha=0.4)
    
    # Determine symmetric color scale based on residuals
    max_abs_res = np.max(np.abs(df_fil["Residual"].values))
    cbar_lim = np.ceil(max_abs_res)

    out_txt = "\n".join((
        rf"$ME = {me:.3f}$ {unit}",
        rf"$MAE = {mae:.3f}$ {unit}",
        rf"$RMSE = {rmse:.3f}$ {unit}",
    ))

    # Place textbox relative to current axis range (like your example)
    x_pos = data_min + 0.95 * (data_max - data_min)
    y_pos = data_min + 0.05 * (data_max - data_min)

    ax.text(
        x_pos, y_pos, out_txt,
        ha="right", va="bottom",
        bbox=dict(boxstyle="square", facecolor="linen", alpha=0.9),
        fontsize=14
    )

    # Colormap + normalization for residual coloring
    cmap = cm.get_cmap()  # default matplotlib colormap
    norm = mcolors.Normalize(vmin=-cbar_lim, vmax=cbar_lim)

    # RGBA colors from residuals
    colors = cmap(norm(df_fil["Residual"].values))

    # Apply per-point alpha if provided
    if alphas is not None:
        colors[:, 3] = np.clip(alphas, 0.0, 1.0)
        
    sc = ax.scatter(
        df_fil["Observed Head"],
        df_fil["Simulated Head"],
        marker="o",
        c=colors,
        s=dotsize,
    )

    ax.set_xlim(data_min, data_max)
    ax.set_ylim(data_min, data_max)
    ax.set_aspect("equal", adjustable="box")

# Colorbar from ScalarMappable (since scatter uses RGBA colors)
    sm = cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])  # needed for some matplotlib versions
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label(f"Residual ({unit})", fontsize=14)

    ax.grid(True)
    ax.set_title(f"{title}", fontsize=16)
    ax.set_xlabel(f"{obs_label} ({unit})", fontsize=14)
    ax.set_ylabel(f"{sim_label} ({unit})", fontsize=14)
    
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
st.set_page_config(page_title="HOB RES Scatter")
st.title("MODFLOW HOB RES Scatter Plot (Observed vs Simulated)")

st.markdown(
    """
Upload a `*.hob_out` file from the MODFLOW **Head Observation (HOB)** package.
The app computes residuals and RMSE, filters “dry” simulated heads (`<= -10000`),
and produces a scatter plot colored by residual.
"""
)

st.header("Plot settings")

uploaded = st.file_uploader(
    "Upload MODFLOW HOB output (*.hob_out) or residual file (*.res)",
    type=["hob_out", "res", "out", "txt", "dat", "csv"],
    accept_multiple_files=False,
)

default_title = "Scatterplot for "
if uploaded is not None and hasattr(uploaded, "name"):
    default_title = f"Scatterplot for {uploaded.name}"

title = st.text_input("**Plot title** _(modify if required)_", value=default_title)


if not uploaded:
    st.info("Please upload a `*.hob_out` file to start.")
    st.stop()

try:
    # --- Detect file type by extension
    fname = uploaded.name.lower()
    is_res = fname.endswith(".res")

    if is_res:
        df_raw = read_res_file(uploaded)

        # Group selection if available and >1 group
        selected_group = None
        if "Group" in df_raw.columns:
            groups = sorted(df_raw["Group"].astype(str).unique())
            if len(groups) > 1:
                selected_group = st.selectbox("Select observation group", groups, index=0)
                df_raw = df_raw[df_raw["Group"].astype(str) == selected_group].copy()
            else:
                selected_group = groups[0]
        obs_type = st.radio("Observation type", options=["Heads", "Discharges"], horizontal=True)
        if obs_type == "Heads":
            obs_label, sim_label, unit = "Measured head", "Modelled head", "m"
        else:
            obs_label, sim_label, unit = "Measured discharge", "Modelled discharge", "m³/s"
            
        df_all = standardize_for_scatter(df_raw, file_kind="res")

        # For RES: no "dry" filter by default (apply only if values exist)
        df_fil = df_all.copy()

    else:
        obs_label, sim_label, unit = "Observed head", "Simulated head", "m"
        df_raw = read_hob_out(uploaded)
        df_all = standardize_for_scatter(df_raw, file_kind="hob")

        # HOB dry filter (your original logic)
        df_fil = df_all[df_all["Simulated Head"] > -10000].copy()
    
    dotsize = st.slider('Adjust dot size', 1, 50, 25, 1)
    
    me, mae, rmse = compute_statistics(df_fil["Observed Head"].values, df_fil["Simulated Head"].values)

    # Quick stats
    residuals = df_fil["Residual"].astype(float)
    
    # --- Optional alpha from Weight (RES only, if numeric)
    alphas = None
    if is_res and ("Weight" in df_fil.columns):
        w = pd.to_numeric(df_fil["Weight"], errors="coerce")
        if w.notna().any():
            wmin, wmax = float(w.min()), float(w.max())
            if wmax > wmin:
                wnorm = (w - wmin) / (wmax - wmin)   # 0..1
                alphas = (0.2 + 0.8 * wnorm).fillna(1.0).to_numpy()
            else:
                # all weights identical -> no need to vary alpha
                alphas = None
                
    fig = make_scatter_figure(df_fil, title=title, me=me, mae=mae, rmse=rmse,obs_label=obs_label, sim_label=sim_label, unit=unit, alphas=alphas, dotsize=dotsize)
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
        st.write(f"Mean residual (ME): {residuals.mean():.3f} {unit}")
        st.write(f"Mean absolute error (MAE): {np.abs(residuals).mean():.3f} {unit}")
        st.write(f"Root mean square error (RMSE): {rmse:.3f} {unit}")
        st.write(f"Residual standard deviation: {residuals.std(ddof=1):.3f} {unit}")
        min_res_id = residuals.idxmin()
        max_res_id = residuals.idxmax()
    
        st.write(f"Minimum residual: {residuals.min():.3f} {unit} (Observation: {min_res_id})")
        st.write(f"Maximum residual: {residuals.max():.3f} {unit} (Observation: {max_res_id})")
    
    with st.expander('Open to see the processed data'):
        st.write("Preview (first rows)")
        st.dataframe(df_all.head(20), use_container_width=True)

except Exception as e:
    st.error("Could not process the uploaded file.")
    st.exception(e)

st.markdown('---')

columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')