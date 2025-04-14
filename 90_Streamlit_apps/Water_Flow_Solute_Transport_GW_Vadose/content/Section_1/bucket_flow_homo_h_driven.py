import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.header('Head distribution in homogeneous media')
st.subheader('Head distribution in a bucket filled with water and sand and flowing groundwater, driven by a :green[**ponding water head**]')

# --- Settings ---
base_level_ini = 0.     # cm (bottom of bucket)
top_level_max = 75.
top_level_ini = 50.
ponding_head_ini = 5.0

   
# Callback function to update session state
def update_K():
    st.session_state.K_slider_value = st.session_state.K_input

@st.fragment
def bucket_flow():
    # Initialize for the first time
    if "top_level" not in st.session_state:
        st.session_state.top_level = 50.0
    if "base_level" not in st.session_state:
        st.session_state.base_level = 0.0
    if "z_measure" not in st.session_state:
        st.session_state.z_measure = 0.0
    if "ponding_head" not in st.session_state:
        st.session_state.ponding_head = 5.0
    if f"K_slider_value" not in st.session_state:
        st.session_state[f"K_slider_value"] = -4.0  # Default value (log of K)
    
    # --- Input slider ---
    
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -5.0 # K / Corresponds to 10^-7 = 0.0000001
    log_max1 = -2.0 # K / Corresponds to 10^0 = 1
    
    # Toggle to switch between slider and number-input mode
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $T$ and $S$")
        
    column1 = st.columns((1,1), gap = 'large')
    with column1[0]:
        st.slider('**Column top level**]', 0.0, top_level_max, top_level_ini, 1.0, key="top_level")
        st.slider('**Column bottom level**', 0.0, top_level_max, base_level_ini, 1.0, key="base_level")
    
    with column1[1]:
        st.slider(':red[**Elevation of measurement $z_{measure}$**]', 0.0, top_level_max, 0.0, 0.1,key="z_measure")
        st.slider(':green[**ponding head $h_p$**]', 0.0, 25.0, ponding_head_ini, 0.1 ,format="%4.2f", key="ponding_head")
        # Hydraulic conductivity
        container = st.container()
        if st.session_state.number_input:
            K_slider_value_new = st.number_input("_(log of) Hydraulic conductivity in m/s_", log_min1,log_max1, st.session_state["K_slider_value"], 0.01, format="%4.2f", key="K_input", on_change=update_K)
        else:
            K_slider_value_new = st.slider("_(log of) Hydraulic conductivity in m/s_", log_min1,log_max1, st.session_state["K_slider_value"], 0.01, format="%4.2f", key="K_input", on_change=update_K)
        st.session_state["K_slider_value"] = K_slider_value_new
        K_slider = 10 ** K_slider_value_new
        container.write("**Hydraulic conductivity in m/s:** %5.2e" %K_slider)
    
    K = K_slider * 100 # cm/m
    
    # q = - Ki
    # q = - K (h_bottom - hz)/(z-base_level)
    # q (z-base_level) / K - h_bottom = -hz
    # hz = h_bottom - q (z-base_level) / K  with h_bottom = 0t
    # hz = - q (z-base_level) / K 
    
    # Use values from session state
    top_level = st.session_state.top_level
    base_level = st.session_state.base_level
    z_measure = st.session_state.z_measure
    ponding_head = st.session_state.ponding_head
    specific_discharge = K * ponding_head/(top_level-base_level)
    
    # --- Generate vertical profile ---
    z_sand = np.linspace(0, top_level, 100)  # Full vertical profile
    z_pond = np.linspace(top_level, top_level+ponding_head, 100)  # Full vertical profile
    
    # --- Calculate head components ---
    elevation_head_sand = z_sand
    elevation_head_pond = z_pond
    pressure_head_sand = np.where(elevation_head_sand >= base_level, specific_discharge * (z_sand-base_level) / K, np.nan)
    pressure_head_pond = np.where(elevation_head_pond >= top_level, top_level+ponding_head - elevation_head_pond, np.nan)
    total_head_sand = np.where(elevation_head_sand >= base_level, pressure_head_sand + elevation_head_sand, np.nan)
    total_head_pond = np.where(elevation_head_pond >= top_level, pressure_head_pond + elevation_head_pond, np.nan)
    
    if (z_measure >= base_level):
        pressure_head_sand_measure = specific_discharge * (z_measure-base_level) / K
        total_head_measure = pressure_head_sand_measure + z_measure
    else:
        pressure_head_sand_measure = 0
        total_head_measure = 0
    
    # PLOT HERE
    # --- Create side-by-side plots ---
    fig, (ax_bucket, ax_profile) = plt.subplots(1, 2, figsize=(10, 6), width_ratios=[1, 2])
    
    # --- Left: Water column (bucket) ---
    bucket_width = 4  # cm
    water_left = 0
    water_right = bucket_width
    
    # sand fill
    z_fill_sand = np.linspace(base_level, top_level, 100)
    z_fill_water = np.linspace(top_level, top_level+ponding_head, 100)
    
    ax_bucket.fill_betweenx(z_fill_sand, water_left, water_right, color='brown', alpha=0.7)
    ax_bucket.fill_betweenx(z_fill_water, water_left, water_right, color='lightblue', alpha=0.7)
    
    # Bucket outline (left, right, bottom)
    ax_bucket.plot([water_left, water_left], [0, top_level_max+25], color='black', linewidth=4)  # left wall
    ax_bucket.plot([water_right, water_right], [0, top_level_max+25], color='black', linewidth=4)  # right wall
    ax_bucket.plot([water_left, water_right], [top_level, top_level], linestyle='dotted', color='black', linewidth=4)  # bottom line
    ax_bucket.plot([water_left, water_right], [base_level, base_level], linestyle='dotted', color='black', linewidth=4)  # bottom line
    
    # Triangle marker at water table (like ∇)
    ax_bucket.plot([(water_left + water_right) / 5],[top_level+ponding_head+2],marker='v',color='navy',markersize=10)
    
    # Horizontal lines below triangle
    line_y1 = top_level+ponding_head - 1  # slightly below triangle
    line_y2 = top_level+ponding_head - 2.5  # a bit further down
    
    line_length = 0.2
    x_center = (water_left + water_right) / 5
    
    # First line / Second line
    ax_bucket.plot([x_center - line_length, x_center + line_length],[line_y1, line_y1],color='navy',linewidth=1.5)
    ax_bucket.plot([x_center - line_length * 0.6, x_center + line_length * 0.6],[line_y2, line_y2],color='navy',linewidth=1.5)
    
    # Pressure sensor at z_measure (like *)
    # TODO ALSO CONSIDER SENSOR BELOW BOTTOM
    if base_level <= z_measure <= top_level:
        ax_bucket.plot([(water_left + water_right) / 1.1],[z_measure],marker='o',color='red',markersize=10)
        ax_bucket.plot([((water_left + water_right) / 1.1), ((water_left + water_right) / 1.1)], [z_measure, top_level], color='black', linewidth=1,linestyle='--')  # line of measurement sensor
    else:
        ax_bucket.plot([(water_left + water_right) / 1.1],[z_measure],marker='o',color='lightgrey',markersize=10)
        ax_bucket.plot([((water_left + water_right) / 1.1), ((water_left + water_right) / 1.1)], [z_measure, top_level], color='lightgrey', linewidth=1,linestyle='--')  # line of measurement sensor
        ax_bucket.text(
            (water_left + water_right) / 1.3,
            top_level+10,
            "Measurment \noutside the \nSand-filled \ncolumn",
            fontsize=12,
            color='red',
            ha='center',
            va='center',
        )
        
    # Text label
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
    
    # Finalize bucket plot
    ax_bucket.set_xlim(0, bucket_width)
    ax_bucket.set_ylim(0, top_level_max+25)
    ax_bucket.axis('off')
    ax_bucket.set_title("Water Column", fontsize=12)
    
    # --- Right: Head components ---
    ax_profile.plot(elevation_head_sand, z_sand, label="Elevation Head (z)", color='grey')
    ax_profile.plot(elevation_head_pond, z_pond, color='grey')
    ax_profile.plot(pressure_head_sand, z_sand, label="Pressure Head (ψ)", color='orange')
    ax_profile.plot(pressure_head_pond, z_pond, color='orange')
    ax_profile.plot(total_head_sand, z_sand, label="Total Head (h)", color='blue')
    ax_profile.plot(total_head_pond, z_pond, color='blue')
    if (z_measure <= top_level):
        ax_profile.plot(z_measure, z_measure, 'o', color='grey')
    if base_level <= z_measure <= top_level:
        ax_profile.plot(pressure_head_sand_measure, z_measure, 'ro')
        ax_profile.plot(total_head_measure, z_measure, 'o', color='blue')
    ax_profile.plot([0, 3*top_level_max + 5], [top_level, top_level],linestyle='dotted',  color='grey', linewidth=2)  # top line
    
    ax_profile.set_xlabel("Head [cm]")
    ax_profile.set_ylabel("Elevation [cm]")
    ax_profile.set_xlim(0, 1.5*top_level_max + 5)
    ax_profile.set_ylim(0, top_level_max+25)
    ax_profile.set_title("Hydraulic Head Components")
    
    #ax_profile.grid(True)
    ax_profile.legend()
    
    # --- Display in Streamlit ---
    st.pyplot(fig)
    st.write('**Your flow meter measure:**')
    st.write(':green[**Specific discharge**] (in cm/s) =%5.2e' %specific_discharge)
    st.write('**Your pressure transducer measure:**')
    if (z_measure >= base_level):
        st.write(':orange[**Pressure head**] (in cm) = %5.1f' %pressure_head_sand_measure)
    else:
        st.write(':orange[**Pressure head**] (in cm) = n. a. (Sensor below bottom)')
    st.write(':grey[**Elevation head**] (in cm) =%5.1f' %z_measure)
    if (z_measure >= base_level):
        st.write(':blue[**Total head**] (in cm) = %5.1f' %(pressure_head_sand_measure+z_measure))
    else:
        st.write(':blue[**Total head**] (in cm) = n. a. (Sensor below bottom)')
        
bucket_flow()