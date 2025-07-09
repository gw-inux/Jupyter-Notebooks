import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="Water Table Fluctuation (WTF) Method")

# --------- TITLE ---------
st.title("Water Table Fluctuation (WTF) Method")
st.subheader('Theory')
st.markdown(
    "Analyze a head time series using falling-limb extrapolation" \
    " and the WTF recharge estimate (multiple peaks)."
)
st.markdown("---")

# --------- INPUT MODE ---------
mode = st.selectbox(
    "Choose data source:",
    ["Example Series", "Upload CSV"],
    key="mode_select"
)

# --------- DATA SELECTION ---------
head = []
time = None
if mode == "Example Series":
    # Example datasets
    def generate_synthetic():
        t = np.arange(0, 60)
        series = 7.0 + 0.2*np.sin(2*np.pi*t/30) - 0.005*t
        series += 0.3*np.exp(-0.5*((t-20)/3)**2)
        series += 0.2*np.exp(-0.5*((t-40)/4)**2)
        return list(series)

    measured1 = [6.8,6.75,6.7,6.65,6.6,6.58,6.6,6.64,6.7,6.78,
                 6.85,6.9,6.95,6.9,6.85,6.8,6.75,6.7,6.68,6.7,
                 6.75,6.8,6.85,6.9,6.95,7.0,7.05,7.08,7.1,7.12,
                 7.1,7.05,7.0]
    measured2 = [7.0,6.98,6.95,6.9,6.85,6.8,6.78,6.8,6.85,6.9,
                 6.95,7.0,7.05,7.1,7.15,7.2,7.18,7.12,7.05,6.98,
                 6.92,6.88,6.85,6.83,6.82,6.85,6.9,6.95,7.0,7.05,
                 7.1,7.15]
    measured3 = [6.9,6.85,6.8,6.75,6.7,6.65,6.6,6.58,6.6,6.63,
                 6.7,6.78,6.85,6.9,6.95,7.0,7.05,7.1,7.15,7.18,
                 7.2,7.18,7.15,7.12,7.1,7.08,7.05,7.0,6.95,6.9,
                 6.85,6.8]
    datasets = {
        "Synthetic": generate_synthetic(),
        "Measured 1": measured1,
        "Measured 2": measured2,
        "Measured 3": measured3
    }
    selection = st.selectbox("Select example series:", list(datasets.keys()), key="example_select")
    head = datasets[selection]
    time = np.arange(len(head))
elif mode == "Upload CSV":
    uploaded = st.file_uploader("Upload CSV (date, head)", type=["csv"], key="uploader")
    if not uploaded:
        st.info("Awaiting CSV upload...")
        st.stop()
    # Read CSV
    try:
        df = pd.read_csv(uploaded, sep=';', parse_dates=[0], dayfirst=True)
    except:
        df = pd.read_csv(uploaded, parse_dates=[0], dayfirst=True)
    if df.shape[1] < 2:
        st.error("CSV must have at least 2 columns: date and head.")
        st.stop()
    df.columns = ['date', 'head'] + list(df.columns[2:])
    df = df[['date', 'head']].dropna()
    df['head'] = pd.to_numeric(df['head'].astype(str).str.replace(',','.'), errors='coerce')
    df.dropna(inplace=True)
    head = df['head'].tolist()
    time = df['date']
else:
    st.error("Unknown mode selection.")
    st.stop()

# --------- SMOOTHING & PEAK-FINDING OPTIONS (CSV ONLY) ---------
apply_smooth = False
use_scipy_peaks = False
if mode == "Upload CSV":
    st.markdown("---")
    st.markdown("### Data Processing Options (CSV)")
    apply_smooth = st.checkbox("Apply Savitzky-Golay smoothing", value=True)
    if apply_smooth:
        win = st.slider("Smoothing window length (odd)", 3, min( int(len(head)//2)*2-1, 51), 7, 2)
        poly = st.slider("Smoothing polynomial order", 2, 5, 2)
    use_scipy_peaks = st.checkbox("Use SciPy peak detection", value=True)
    if use_scipy_peaks:
        prom = st.slider("Peak prominence (m)", 0.0, float(max(head)-min(head)), 0.05)
        dist = st.slider("Min distance between peaks (days)", 1, len(head)//2, 7)

# Prepare head array for detection
head_array = np.array(head)
if apply_smooth:
    # ensure window <= len and odd
    win = min(win, len(head_array) if len(head_array)%2 else len(head_array)-1)
    if win % 2 == 0:
        win -= 1
    smooth_head = savgol_filter(head_array, window_length=win, polyorder=poly)
else:
    smooth_head = head_array

# --------- INPUT PARAMETERS ---------
st.markdown("---")
st.markdown("### Method Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    alpha_display = st.container()
    log_alpha = st.slider(
        "log₁₀(Recession Constant α)",
        min_value=-5.0,
        max_value=-1.0,
        value=-1.7,
        step=0.1,
        format="%.1f"
    )
    alpha = 10 ** log_alpha
    alpha_display.markdown(f"**Current α:** {alpha:.5f}")
with col2:
    Sy = st.slider("Specific Yield (Sy)", 0.01, 0.5, 0.2)
with col3:
    thr = st.slider("Min rise to count peak (m)", 0.0, 1.0, 0.05, 0.01)

# --------- ADAPTIVE WINDOW TOGGLE ---------
adaptive = st.checkbox("Use adaptive event window", value=False)
if adaptive:
    start_idx, end_idx = st.slider(
        "Select window day index range:",
        0, len(head)-1, (0, len(head)-1), 1
    )
    # restrict arrays
    head_proc = smooth_head[start_idx:end_idx+1]
    time_proc = time[start_idx:end_idx+1]
else:
    head_proc = smooth_head
    time_proc = time

# --------- PEAK DETECTION ---------
if use_scipy_peaks:
    peaks, props = find_peaks(head_proc, prominence=prom, distance=dist)
else:
    diff = np.diff(head_proc)
    peaks = [i+1 for i in range(len(diff)-1) if diff[i]>0 and diff[i+1]<0]

# --------- EVENT PROCESSING ---------
# Prepare offset for adaptive window
offset = start_idx if adaptive else 0

# Detect events and compute per-peak recession baselines
events = []
baselines = []
prev_end_idx = 0

# diffs on processed head
diffs = np.diff(head_proc)

for p_idx in peaks:
    # rising limb within segment
    seg_diff = diffs[prev_end_idx:p_idx]
    rise_pos = np.where(seg_diff > 0)[0]
    if rise_pos.size == 0:
        prev_end_idx = p_idx
        continue
    rise_rel = int(rise_pos[0])
    start_rel = prev_end_idx + rise_rel + 1
    # identify h0_rel as max head in falling segment before rise
    fall_seg = head_proc[prev_end_idx:start_rel]
    if fall_seg.size > 0:
        h0_rel = prev_end_idx + int(np.argmax(fall_seg))
    else:
        h0_rel = start_rel - 1
    # map to global indices
    h0_global = h0_rel + offset
    p_global = p_idx + offset
    # find first fall after peak in processed series
    fall_after = np.where(diffs[p_idx:] < 0)[0]
    if fall_after.size > 0:
        end_rel = p_idx + int(fall_after[0]) + 1
    else:
        end_rel = head_proc.size - 1
    end_global = end_rel + offset
    # observed rise threshold: from start to peak
    start_global = start_rel + offset
    obs_dh = head[p_global] - head[start_global]
    if obs_dh < thr:
        prev_end_idx = p_idx
        continue
    # compute delta h from recession baseline
    dh = head[p_global] - head[h0_global] * np.exp(-alpha * (p_global - h0_global))
    # build baseline segment
    length = end_global - h0_global + 1
    t_seg = np.arange(length)
    baseline = head[h0_global] * np.exp(-alpha * t_seg)
    baselines.append((h0_global, p_global, baseline))
    events.append({'day': p_global, 'h0': h0_global, 'Δh': dh, 'recharge': Sy * dh * 1000})
    prev_end_idx = p_idx


# --------- PLOTTING ---------
st.markdown("### 📈 Groundwater Head & Recessions")
fig, ax = plt.subplots(figsize=(10,5))
if apply_smooth:
    ax.plot(time, smooth_head, color='green', label='Smoothed', linewidth=3)
    ax.plot(time, head, color='gray', marker='o', markersize=2, alpha=0.6, label='Observed')
else:
    ax.plot(time, head, marker='o', markersize=2, label='Observed')
# if adaptive window, show start/end lines and limit x-axis
if adaptive:
    # determine window bounds
    x0 = time_proc.iloc[0] if hasattr(time_proc, 'iloc') else time_proc[0]
    x1 = time_proc.iloc[-1] if hasattr(time_proc, 'iloc') else time_proc[-1]
    # plot vertical lines
    ax.axvline(x0, color='black', linestyle='-.', linewidth=1, label='Window start')
    ax.axvline(x1, color='black', linestyle='-.', linewidth=1, label='Window end')
    # set x-limits with 10% padding
    try:
        # datetime axis
        delta = x1 - x0
        pad = delta * 0.1
        ax.set_xlim(x0 - pad, x1 + pad)
    except:
        # numeric axis
        xmin, xmax = x0, x1
        pad = (xmax - xmin) * 0.1
        ax.set_xlim(xmin - pad, xmax + pad)
for h0,p,baseline in baselines:
    idxs = np.arange(h0, h0+len(baseline))
    ax.plot(time.iloc[idxs] if hasattr(time, 'iloc') else idxs,
            baseline, '--', label=f'Recession {h0}→{p}')
for ev in events:
    d = ev['day']; h_ext = head[ev['h0']]*np.exp(-alpha*(d-ev['h0']))
    ax.scatter(time[d], head[d], color='red')
    ax.vlines(time[d], h_ext, head[d], color='gray', linestyle='--', linewidth=1)
hmin, hmax = min(head), max(head)
ax.set_ylim(bottom=hmin - 2*(hmax - hmin), top=hmax + 0.1*(hmax - hmin))
ax.set_xlabel('Time'); ax.set_ylabel('Head (m)')
ax.legend(); st.pyplot(fig)

# --------- SUMMARY ---------
st.markdown("### 📊 Recharge Events")
if events:
    total_recharge = sum(ev['recharge'] for ev in events)
    for ev in events:
        st.write(f"- Day {ev['day']} (h₀={ev['h0']}): Δh={ev['Δh']:.3f} m → {ev['recharge']:.1f} mm")
    st.markdown(f"**Total recharge (sum of all events): {total_recharge:.1f} mm**")
else:
    st.write("No peaks above threshold.")
