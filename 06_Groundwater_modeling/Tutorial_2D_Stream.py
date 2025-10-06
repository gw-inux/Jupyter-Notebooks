# --- Streamlit app: Stream–Aquifer Exercise for the Boundary Condition Module ---
# Requirements: streamlit, streamlit-extras (stodo)
# Save as: app_stream_bc_exercise.py

import streamlit as st
from streamlit_extras.stodo import to_do

# ----------------------------
# Title & overview
# ----------------------------
st.title("🛠️ Exercise")
st.header("2D Steady-State :blue[Stream–Groundwater] Interaction in an Idealized Catchment")
st.subheader("Representing streams in :blue[MODFLOW & ModelMuse] 💻", divider="blue")

# ----------------------------
# Motivation & Learning Objectives
# ----------------------------

st.markdown("""
#### 💡 Motivation - Exercise to understand options to account for streams in MODFLOW

Streams are common :blue[**physical boundaries**] in groundwater systems. Their diverse interactions with the groundwater make them ideal for demonstrating the full range of **MODFLOW boundary condition packages**.

This exercise helps to understand the strengths and limitations of each approach in relation to specific conceptual characteristics of the stream. It complements the boundary conditions introduced in this module and uses a simple, diagnostic scenario to highlight the implications of different implementation choices. Detailed :green[**tutorials and screencast videos**] help to follow the exercise with your own device

The exercise is inspired by *Reilly (2001) – System and Boundary Conceptualization in Groundwater Flow Simulations (USGS TWRI 3–B8)*.
""")

lc0, cc0, rc0 = st.columns((20,80,20))
with cc0:
    st.image('06_Groundwater_modeling/FIGS/stream_groundwater.png', caption="Idealized representation of streams in grounwater systems - acting as sinks/discharge areas. Figure from Winter et al. (1998).")

st.markdown("""
#### 🎯 Learning Objectives
By engaging with this exercise of the interactive module, you will be able to:

1. Explain how the different boundary conditions types can represent different conceptualizations of the stream-aquifer.

2. Identify which MODFLOW boundary packages can represent a stream under different conceputal assumptions.

3. Implement and compare alternative stream representations in a simple, steady-state model.

4. Evaluate implications for simulated heads, fluxes, and the water balance.
""")

st.markdown("""
#### 🧪 Some background information about conceptual ways of implementing streams in MODFLOW

Stream can appear in various ways in groundwater systems, for example as gaining streams, loosing streams, or even loosing streams that are disconnected from the groundwater. Depending on the conceptual model, various different boundary conditions can be used to represent a stream in a groundwater model. 
""")
lc1, cc1, rc1 = st.columns((20,80,20))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/Winter_streams.png', caption="The synthetic catchment for the numerical model.")
with st.expander("Click here to see :blue[**Options for Implementing a Stream in MODFLOW**] – Packages at a glance"):
    st.markdown("""
| **Option** | **Concept** | **Typical MODFLOW package(s)** | **Example from the real world** |
|------------|-------------|--------------------------------|---------------------------------|
| **1. Specified Head (Type 1)** | Stream stage is fixed and imposed directly. | **CHD** | Large stream that is in direct contact with the groundwater |
| **2. Specified Flow (Type 2)** | Prescribe inflow/outflow independent of head. | **WEL** | Loosing stream with known loss rate |
| **3. Head-Dependent (Type 3)** | Exchange ∝ head difference via conductance. | **RIV**, **GHB** | Stream that ... |
| **4a. Strictly gaining stream** | One-way outflow from aquifer to stream. | **DRN** | Stream in a flat area without surface runoff, only groundwater feeds the stream |
| **4b. Gaining & losing (possible disconnection)** | Fixed stage; infiltration capped below bed. | **RIV** | Stream in a mountain area with large gradient |
| **4c. Stage computed (routing)** | Routed flow; stage solved; drying possible. | **SFR** *(outlook only here)* | Stream that ... |
""")

st.markdown("""
#### 🧊 The underlying conceptual model and transfer into an initial numerical model

Stream can appear in various ways in groundwater systems, for example as gaining streams, loosing streams, or even loosing streams that are disconnected from the groundwater. Depending on the conceptual model, various different boundary conditions can be used to represent a stream in a groundwater model. 
""")

# Subsequently, the lowland example is introduced. The idea is to have a stream that is only fed by groundwater. The second scenario (highlands) will be with a much steeper stream that is partially gaining and loosing

with st.expander(" Click here to read more about the :blue[**Scenario**] – Idealized rectangular catchment"):
    lc2, cc2, rc2 = st.columns((20,80,20))
    with cc2:
        st.image('06_Groundwater_modeling/FIGS/V1_LOW_concept.png', caption="The synthetic catchment for the numerical model.") 
    st.markdown("""
    
    
     :rainbow[***Brief description of the conceptual model***]
        
    The conceptual model represents a highly idealized groundwater catchment and can be briefly described with the following key points:
    
    **Space and Time**
    - The idealized catchments has a rectangular area with the dimension 3100 m x 5100 m.
    - The earth surface is (in average) at 10 m. The aquifer bottom is at -50 m.
    - The time is considered as steady-state.
    
    **Structure and Parameters**
    - One homogeneous and isotropic aquifer composed of sand with *K* = 1E-4 m/s.
    
    **Boundary Conditions**
    - The catchment is bounded on the east by the :blue[**sea**], represented by a first type boundary condition (assuming that the sea is in direct hydraulical contact with the groundwater). The seawater level is at 0 m.
    - All other outer boundaries are :red[**no-flow**].
    - From the top, the model receives uniform areal (diffuse) :green[**groundwater recharge**].
    - The :blue[**stream**] is centrally placed and flows straight through the catchment. The head in the stream at the origin is 1m. The stream reaches the sea with a head of 0.
    - A water abstraction well is placed beside the stream with a distance of about 200 m.
    - For :red[**simplicity**], the conceptual model does :red[**NOT account for evapotranspiration FROM groundwater**].
    
    **Further Characteristics**
    - The catchment is flat and surface runoff can be neglected. The stream is solely fed by groundwater (gaining stream).
    
    :rainbow[***Brief description of the initial numerical model***]
    
    **Space and Time**
    - The model is rectangular and composed of 51 columns and 31 rows with a cell width of 100 m x 100 m.
    - The aquifer is represented by one layer with the top at 10 m and the bottom at -50 m.
    - The model time is set to steady-state.
    
    **Structure and Parameters**
    - The hydraulic conductivity *K* of homogeneous and isotropic aquifer is set to 1E-4 m/s.
    - The aquifer is considered as unconfined
    
    **Boundary Conditions**
    - The :blue[**sea**] is represented by the **CHD package** with a specified head of 0 m. The **CHD** boundary is set in the last column of the model grid at the east.
    - All other outer boundary conditions are No-Flow.
    - The :green[**groundwater recharge**] is 
      - defined over an area of 5000 m x 3100 m (the model area except the CHD cells at the eastern boundary)
      - with an areal rate of 6.45E-9 m/s (around 200 mm/a),
      - resulting in a total inflow of 0.1 m3/s.
    - The :blue[**stream**] 
      - is initially implemented with the RIV package.
      - The head of the stream is linearly interpolated from 1.0 m to 0.0 m (from the origin to the sea).
      - The conductance of the stream is set to 1E-5 m/s.
    - The :black[**abstraction well**]
      - is implemented by the WEL package.
      - The abstraction rate varies through the different scenarios from 0.01 m3/s (10% of RCH x Area) to 0.05 m3/s to 0.11 m3/s (110% of RCH x Area)
      
    **Software and solution**
    - Various versions of MODFLOW can be used for the exercise. The subsequent tutorial and screencasts were done with MODFLOW-2005 (Harbaugh 2005).
      
    """)

st.subheader("Instructions and Tutorials to implement streams in MODFLOW 💻", divider="blue")

st.markdown("""
#### 🧊 How to Implement a Stream in MODFLOW with ModelMuse

In the following, we provide instructions and explanations on how to design a numerical model that represents a stream. The tutorial is based on MODFLOW-2005 using the graphical user interface ModelMuse, but the same model design principles can be applied with any other interface for the MODFLOW family of codes.

In the screencast, we demonstrate a variant where the stream is represented using the RIV package. Alternative formulations include the GHB and DRN packages.

:red[**Before working with the numerical model, it is important to reflect on the conceptual situation. By clarifying how the stream interacts with the groundwater system, we can better formulate our expectations of the model results.**]
""")



st.markdown("""
#### 🧊 Tutorial with step-by-step instructions and screencast videos

Next, you will find the tutorial files. The resulting model is provided as MODELMUSE file. Further, you can download the written instructions as PDF file.
""")
# TODO: Provide GPT files and PDF's

# ----------------------------
# STEP 1
# ----------------------------
with st.expander(":blue[**Step 1: Discretization in space and time**] – Expand for instructions"):
    st.markdown("""
#### STEP 1: Discretization in space and time
We set up a single-layer, steady-state model to isolate the water balance and boundary interactions.
""")
    to_do([(st.write, "Start ModelMuse and create a new MODFLOW-2005 model.")], "td01")
    to_do([(st.write,
            "Define grid: columns = **51** at **100 m**, rows = **31** at **100 m**, layers = **1** "
            "(top = **10 m**, bottom = **−50 m**).")], "td02")
    to_do([(st.write,
            "Define time: **1** stress period, **duration = 1 s**, **Steady-state = True**.")], "td03")
    st.markdown("""
**Quick checks**  
- Cells: \\(51\\times31\\times1 = 1{,}581\\)  
- Domain size: \\(L_x=5100\\,\\text{m},\\ L_y=3100\\,\\text{m}\\)  
- **Recharge area (excl. CHD column)**: \\(A = 5000\\times3100 = 15{,}500{,}000\\,\\text{m}^2\\)  
- Recharge for \\(Q_{in}=0.1\\): \\(R \\approx 0.1/15{,}500{,}000 \\approx 6.45\\times10^{-9}\\,\\text{m s}^{-1} \\approx 203\\,\\text{mm yr}^{-1}\\).
""")

# ----------------------------
# STEP 2
# ----------------------------
with st.expander(":blue[**Step 2: Structure & Parameters**] – Expand for instructions"):
    st.markdown("""
#### STEP 2: Define structure and parameters
We model a single unconfined layer with uniform hydraulic properties for the baseline.
""")
    to_do([(st.write, "Open **Data → Edit Data Sets**.")], "td04")
    to_do([(st.write, "In **Layer definition**, set the layer to **Convertible (unconfined)**.")], "td05")
    to_do([(st.write,
            "In **Hydrology → Kx**, confirm **Kx = 1e−4 m/s**; set **Ky = Kx**, **Kz = Kx** (anisotropy = 1).")], "td06")
    to_do([(st.write,
            "Storage note: the run is **steady-state**; **Sy** and **Ss** do not affect the solution (keep defaults).")], "td07")
    st.markdown("""
**Sanity check**  
Saturated thickness \\(b = 10 - (−50) = 60\\,\\text{m}\\) → Transmissivity \\(T = Kb = 6\\times10^{-3}\\,\\text{m}^2\\,\\text{s}^{-1}\\).
""")

# ----------------------------
# STEP 3
# ----------------------------
with st.expander(":blue[**Step 3: Boundary Conditions**] – Expand for instructions"):
    st.markdown("#### STEP 3: Boundary Conditions")

    st.markdown("##### A) SetDefinedHeadBoundaryCondition (CHD)")
    to_do([(st.write, "Open **Model → MODFLOW Packages and Programs…**.")], "td08")
    to_do([(st.write, "Left panel: **Boundary Conditions → Specified Head** → tick **CHD** → **OK**.")], "td09")
    to_do([(st.write,
            "Toolbar: **Create Straight Object**. In **Top view**, **click the upper-right cell**, move straight down to the **lower-right cell**, and **double-click** "
            "to finish (east boundary). Name the object, e.g., **C**.")], "td10")
    to_do([(st.write,
            "Open the object → **MODFLOW Features → CHD**. Set **StartingTime = 0**, **EndingTime = 1**, "
            "**StartingHead = 0**, **EndingHead = 0** → **OK**.")], "td11")

    st.markdown("##### B) SetRechargeBoundaryCondition (RCH)")
    to_do([(st.write, "Open **Model → MODFLOW Packages and Programs…**.")], "td12")
    to_do([(st.write, "Left panel: **Boundary Conditions → Specified Flux** → tick **RCH** → **OK**.")], "td13")
    to_do([(st.write,
            "Toolbar: **Create Rectangle Object**. In **Top view**, drag from the **upper-left** corner to the **lower-right corner of column 50** "
            "(exclude the CHD column). Name the object, e.g., **Recharge**.")], "td14")
    to_do([(st.write,
            "Open object → **MODFLOW Features → RCH**. Set **StartingTime = 0**, **EndingTime = 1**. "
            "Click the function (ƒ) next to **Recharge rate** and enter: **0.1 / (5000 * 3100)** (units: m/s) → **OK**, **OK**.")], "td15")

    st.markdown("##### C) SetRiverBoundaryCondition (RIV)")
    to_do([(st.write, "Open **Model → MODFLOW Packages and Programs…**.")], "td16")
    to_do([(st.write, "Left panel: **Boundary Conditions → Head-Dependent Flux** → tick **RIV** → **OK**.")], "td17")
    to_do([(st.write,
            "Toolbar: **Create Polyline Object**. In **Top view**, click **row 16, column 11**; move east along row 16 and **double-click in column 50** "
            "(adjacent to CHD). Name the object, e.g., **River**.")], "td18")

# ----------------------------
# STEP 4
# ----------------------------
with st.expander(":blue[**Step 4: River Attributes & Simulation**] – Expand for instructions"):
    st.markdown("""
#### STEP 4: RIV attributes, run, and diagnostics
Assign a simple but defensible parameterization to produce gaining/losing behavior with capped infiltration.
""")
    to_do([(st.write,
            "Open **River** object → **MODFLOW Features → RIV**. In the table: **StartingTime = 0**, **EndingTime = 1**.")], "td19")
    to_do([(st.write,
            "Set **River Stage = 1.0 m**, **River Bottom = 0.0 m**, **Conductance = 0.02 m²/s**. "
            "→ **OK**.")], "td20")
    to_do([(st.write,
            "Save the model and **Run MODFLOW-2005**. After convergence, open the listing and check the **Global Water Budget**.")], "td21")
    to_do([(st.write,
            "Mass-balance target at steady state: **Q_in ≈ 0.1 m³/s**; **Q_stream + Q_sea ≈ 0.1 m³/s**; **|ε|/Q_in ≤ 0.1%**.")], "td22")
    to_do([(st.write,
            "Inspect **cell-by-cell flows**: verify mixed gaining/losing along the reach and capped infiltration where heads < 0 m.")], "td23")

    st.markdown("""
**Notes**  
- The chosen **Stage (1 m)** and **Bottom (0 m)** place the stream between land surface (10 m) and sea level (0 m), enabling both gaining and losing exchange.  
- **Conductance** comes from \\( C = K_{bed} W L / M \\); here, \\(K_{bed}=1e−6\\,\\text{m/s}\\), \\(M=0.5\\,\\text{m}\\), \\(W=L=100\\,\\text{m}\\) → \\(C=0.02\\,\\text{m}^2/\\text{s}\\).
""")

# ----------------------------
# OPTIONAL VARIANTS (not implemented here)
# ----------------------------
with st.expander(":blue[**Optional Variants (for comparison)**] – Not required for this exercise"):
    st.markdown("""
- **DRN variant (4a):** Replace RIV with **DRN** (elevation ≈ 0 m; analogous conductance). Strictly gaining behavior (one-way outflow).
- **CHD-stream line (1):** Represent the stream as a **CHD** line along row 16 and compare heads/fluxes.
- **WEL variant (2):** Impose a specified seepage (positive/negative) along the reach with **WEL**.
- **SFR outlook (4c):** Route streamflow, solve stage, allow drying; not part of this exercise but relevant for dynamic channel hydraulics.
""")

# ----------------------------
# Videos (placeholders)
# ----------------------------
with st.expander(":blue[**Video demonstrations**] – Short walkthroughs (placeholders)"):
    st.markdown("""
We recommend 2–4 short clips: (1) grid & parameters, (2) BCs & river setup, (3) run & budget check, (4) interpretation.
""")
    # If you have actual URLs, replace below:
    # st.video("https://youtu.be/your_video_1")
    # st.video("https://youtu.be/your_video_2")

# ----------------------------
# End
# ----------------------------
st.info("✅ Tip: Keep a copy of this baseline. Use it to test how BC choices redistribute outflows between stream and sea while preserving the global water balance.")
