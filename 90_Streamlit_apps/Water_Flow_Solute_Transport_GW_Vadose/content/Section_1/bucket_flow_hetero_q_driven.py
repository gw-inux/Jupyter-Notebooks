import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.header('Head distribution in heterogeneous media')
st.subheader(
    '1D flow through a sand column with two hydraulic conductivities '
    '(Darcy flux q > 0 = upward)'
)

# --- Settings ---
base_level_ini = 0.0      # cm (bottom of sand column)
top_level_max = 100.0     # cm (top of bucket)
top_level_ini = 50.0      # cm (top of sand column)
specific_discharge_max = 0.5  # cm/s (maximum magnitude for slider)

# ToDo
# Log Slider
# Number input
# Finetuning / homogenize with the other apps

@st.fragment
def bucket_flow():
    # ---------- Session state initialization ----------
    if "top_level" not in st.session_state:
        st.session_state.top_level = top_level_ini
    if "base_level" not in st.session_state:
        st.session_state.base_level = base_level_ini
    if "z_measure" not in st.session_state:
        st.session_state.z_measure = 0.0
    if "specific_discharge" not in st.session_state:
        st.session_state.specific_discharge = 0.005
    if "number_input" not in st.session_state:
        st.session_state.number_input = False

    # Log10(K) range in m/s
    log_min1 = -4.0
    log_max1 = -1.0

    # ---------- Input controls ----------
    column1 = st.columns((1, 1), gap='large')

    # Left column: geometry
    with column1[0]:
        st.slider(
            '**Column top level** [cm]',
            0.0, top_level_max,
            st.session_state.top_level,
            1.0,
            key="top_level",
        )
        st.slider(
            '**Bucket bottom level** [cm]',
            0.0, top_level_max,
            st.session_state.base_level,
            1.0,
            key="base_level",
        )

    # Right column: measurement level, |q|, flow direction, and K
    with column1[1]:
        st.slider(
            ':red[**Elevation of measurement $z_{measure}$**] [cm]',
            0.0, top_level_max,
            st.session_state.z_measure,
            0.1,
            key="z_measure",
        )

        st.slider(
            ':green[**Specific discharge |q|**] [cm/s]',
            0.0, specific_discharge_max,
            st.session_state.specific_discharge,
            0.001,
            format="%4.3f",
            key="specific_discharge",
        )

        flow_dir = st.radio(
            "Flow direction (Darcy flux q, **positive upward**)",
            ("Upwards (from bottom to top)", "Downwards (from top to bottom)"),
            horizontal=True,
        )

        # Real Darcy flux q [cm/s]; positive upward by convention
        q_mag = st.session_state.specific_discharge
        if flow_dir.startswith("Upwards"):
            q = +q_mag
        else:
            q = -q_mag

        st.write(f"Chosen Darcy flux: q = {q: .4f} cm/s (positive = upward)")

        st.markdown("**Hydraulic conductivity (log$_{10} K$ in m/s)**")
        cK = st.columns(2, gap="small")

        with cK[0]:
            K1_log = st.slider(
                "Lower part",
                log_min1, log_max1,
                -2.0,
                0.01,
                format="%4.2f",
                key="K1_log",
            )
        with cK[1]:
            K2_log = st.slider(
                "Upper part",
                log_min1, log_max1,
                -2.0,
                0.01,
                format="%4.2f",
                key="K2_log",
            )

        # Convert log10(K) [m/s] to K [cm/s]
        K1_mps = 10 ** K1_log
        K2_mps = 10 ** K2_log
        K1 = K1_mps * 100.0
        K2 = K2_mps * 100.0

        st.write(f"**Lower part:** {K1_mps:5.2e} m/s")
        st.write(f"**Upper part:** {K2_mps:5.2e} m/s")

    # ---------- Use updated geometry ----------
    top_level = st.session_state.top_level
    base_level = st.session_state.base_level
    z_measure = st.session_state.z_measure

    # Ensure base ≤ top for the calculations
    if base_level > top_level:
        base_level, top_level = top_level, base_level

    # Interface between lower and upper part (here: mid-height of sand column)
    z_interface = 0.5 * (base_level + top_level)

    # ---------- Vertical profile ----------
    z = np.linspace(0.0, top_level_max, 200)  # whole bucket
    elevation_head = z.copy()                 # z as elevation head

    head = np.full_like(z, np.nan, dtype=float)       # total head h(z)
    pressure_head = np.full_like(z, np.nan, dtype=float)

    # Masks for the two layers (within saturated column)
    mask_lower = (z >= base_level) & (z <= z_interface)
    mask_upper = (z > z_interface) & (z <= top_level)

    # --- Darcy: q = -K dh/dz; -> dh/dz = -q/K ---
    # Boundary condition: h(base_level) = 0 cm (reference)
    # Lower layer:
    #   h(z) = 0 - (q/K1) * (z - base_level)
    head[mask_lower] = - (q / K1) * (z[mask_lower] - base_level)

    # Head at the interface
    h_interface = - (q / K1) * (z_interface - base_level)

    # Upper layer:
    #   h(z) = h_interface - (q/K2) * (z - z_interface)
    head[mask_upper] = h_interface - (q / K2) * (z[mask_upper] - z_interface)

    # Pressure head ψ = h - z, total head = h
    pressure_head = head - elevation_head
    total_head = head

    # ---------- Measurement point ----------
    if z_measure >= base_level:
        if z_measure <= z_interface:
            # Lower layer
            head_measure = - (q / K1) * (z_measure - base_level)
        else:
            # Upper layer
            h_interface = - (q / K1) * (z_interface - base_level)
            head_measure = h_interface - (q / K2) * (z_measure - z_interface)

        pressure_head_measure = head_measure - z_measure
        total_head_measure = head_measure
    else:
        pressure_head_measure = np.nan
        total_head_measure = np.nan

    # ---------- Virtual ponding head at the top of the column ----------
    # Total head at z = top_level
    if top_level >= base_level:
        if top_level <= z_interface:
            h_top = - (q / K1) * (top_level - base_level)
        else:
            h_interface = - (q / K1) * (z_interface - base_level)
            h_top = h_interface - (q / K2) * (top_level - z_interface)

        # At a free water surface, ψ = 0 => h = z
        # -> "ponding level" (if water continued) is z_pond = h_top
        z_pond = h_top
        ponding_head = h_top - top_level
    else:
        z_pond = np.nan
        ponding_head = np.nan

    # ---------- Plotting ----------
    fig, (ax_bucket, ax_profile) = plt.subplots(
        1, 2, figsize=(10, 6), width_ratios=[1, 2]
    )

    # --- Left: Water column (bucket) ---
    bucket_width = 4.0
    water_left = 0.0
    water_right = bucket_width

    # Sand-filled part
    z_fill_top = np.linspace(z_interface, top_level, 10)
    z_fill_bot = np.linspace(base_level, z_interface, 10)
    ax_bucket.fill_betweenx(z_fill_top, water_left, water_right, color='wheat', alpha=0.9)
    ax_bucket.fill_betweenx(z_fill_bot, water_left, water_right, color='sandybrown', alpha=0.9)

    # Bucket outline
    ax_bucket.plot([water_left, water_left], [0, top_level_max],
                   color='black', linewidth=4)  # left wall
    ax_bucket.plot([water_right, water_right], [0, top_level_max],
                   color='black', linewidth=4)  # right wall
    ax_bucket.plot([water_left, water_right], [base_level, base_level],
                   color='grey', linewidth=2)   # bottom line (of sand)

    # Layer interface
    ax_bucket.plot([water_left, water_right], [z_interface, z_interface],
                   color='black', linestyle='--', linewidth=1)

    ax_bucket.text((water_left + water_right) / 2,(base_level + z_interface) / 2, "K1", fontsize=12)
    ax_bucket.text((water_left + water_right) / 2,(z_interface + top_level) / 2, "K2", fontsize=12)

    # Triangle marker at top of column (water table inside column)
    ax_bucket.plot([(water_left + water_right) / 5], [top_level + 2], marker='v', color='navy', markersize=10)
    line_y1 = top_level - 2
    line_y2 = top_level - 4
    line_length = 0.2
    x_center = (water_left + water_right) / 5
    ax_bucket.plot([x_center - line_length, x_center + line_length],[line_y1, line_y1], color='navy', linewidth=1.5)
    ax_bucket.plot([x_center - line_length * 0.6, x_center + line_length * 0.6],[line_y2, line_y2], color='navy', linewidth=1.5)

    # Virtual ponding level (if within plot range)
    if np.isfinite(z_pond) and 0.0 <= z_pond <= top_level_max:
        ax_bucket.plot(
            [0, bucket_width], [z_pond, z_pond],
            color='lightskyblue', linestyle='--', linewidth=1
        )
        ax_bucket.text(
            bucket_width / 2,
            z_pond,
            "(Virtual)\nPonding level",
            fontsize=10,
            color='lightskyblue',
            va="center",
            ha="left"
        )

    elif np.isfinite(z_pond) and z_pond > top_level_max:
        ax_bucket.text(
            bucket_width / 2,
            top_level_max - 5,
            "Ponding level\noutside the plot",
            fontsize=10,
            color='lightskyblue',
            va="center",
            ha="left"
        )

    # Flow-direction arrow in the column
    arrow_y = 0.5 * (base_level + top_level)
    if q > 0:  # upward
        ax_bucket.arrow((water_left + water_right) * 0.2, arrow_y - 5, 0.0, 10.0, head_width=0.2, head_length=3.0, length_includes_head=True)
    elif q < 0:  # downward
        ax_bucket.arrow((water_left + water_right) * 0.2, arrow_y + 5, 0.0, -10.0, head_width=0.2, head_length=3.0, length_includes_head=True)

    # Pressure sensor at z_measure
    if base_level <= z_measure <= top_level:
        ax_bucket.plot(
            [(water_left + water_right) / 1.1],
            [z_measure],
            marker='o',
            color='red',
            markersize=10
        )
        ax_bucket.plot(
            [((water_left + water_right) / 1.1),
             ((water_left + water_right) / 1.1)],
            [z_measure, top_level],
            color='black',
            linewidth=1,
            linestyle='--'
        )
    else:
        ax_bucket.plot(
            [(water_left + water_right) / 1.1],
            [z_measure],
            marker='o',
            color='lightgrey',
            markersize=10
        )

    # Text label for the sand column
    ax_bucket.text(
        (water_left + water_right) / 2,
        base_level + 5,
        "Sand-filled\ncolumn",
        fontsize=12,
        color='black',
        ha='center',
        va='center',
        fontweight='bold'
    )

    ax_bucket.set_xlim(0, bucket_width)
    ax_bucket.set_ylim(0, top_level_max)
    ax_bucket.axis('off')
    ax_bucket.set_title("Water Column", fontsize=12)

    # --- Right: Head components ---
    ax_profile.plot(elevation_head, z, label="Elevation head z", color='grey')
    ax_profile.plot(pressure_head, z, label="Pressure head ψ", color='orange')
    ax_profile.plot(total_head, z, label="Total head h", color='blue')

    # Mark measurement point
    if base_level <= z_measure <= top_level:
        ax_profile.plot(z_measure, z_measure, 'o', color='grey')
        ax_profile.plot(pressure_head_measure, z_measure, 'ro')
        ax_profile.plot(total_head_measure, z_measure, 'o', color='blue')

    # Axis limits
    # Include some margin for negative heads if q/K is small
    finite_h = total_head[np.isfinite(total_head)]
    if finite_h.size > 0:
        h_min = min(np.min(finite_h), -10.0)
        h_max = max(np.max(finite_h), top_level_max + 10.0)
    else:
        h_min, h_max = -10.0, top_level_max + 10.0

    ax_profile.set_xlabel("Head [cm]")
    ax_profile.set_ylabel("Elevation [cm]")
    ax_profile.set_xlim(- 155, 155)
    ax_profile.set_ylim(0, top_level_max)
    ax_profile.set_title("Hydraulic Head Components")
    ax_profile.legend()

    st.pyplot(fig)

    # ---------- Text output ----------
    st.write('**Your pressure transducer measures:**')
    if base_level <= z_measure <= top_level:
        st.write(':orange[**Pressure head ψ**] (in cm) = %5.1f' % pressure_head_measure)
        st.write(':grey[**Elevation head z**] (in cm) = %5.1f' % z_measure)
        st.write(':blue[**Total head h**] (in cm) = %5.1f' % total_head_measure)
    else:
        st.write(':orange[**Pressure head ψ**] (in cm) = n. a. (Sensor outside saturated column)')
        st.write(':grey[**Elevation head z**] (in cm) = %5.1f' % z_measure)
        st.write(':blue[**Total head h**] (in cm) = n. a.')


bucket_flow()
