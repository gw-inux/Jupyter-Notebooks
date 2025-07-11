# Loading the required Python libraries
import streamlit as st
from streamlit_extras.stodo import to_do
import json
from streamlit_book import multiple_choice

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Navneet Sinha": [1],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)


def render_assessment(filename, title="📋 Assessment", max_questions=4):

    with open(filename, "r", encoding="utf-8") as f:
        questions = json.load(f)

    st.markdown(f"#### {title}")
    for idx in range(0, min(len(questions), max_questions), 2):
        col1, col2 = st.columns(2)
        for col, i in zip((col1, col2), (idx, idx+1)):
            if i < len(questions):
                with col:
                    q = questions[i]
                    st.markdown(f"**Q{i+1}. {q['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=q["options"],
                        success=q.get("success", "✅ Correct."),
                        error=q.get("error", "❌ Not quite.")
                    )


st.title('Tutorial – Numerical computation of solute transport: Demonstration of MT3D applications')

st.header('2D solute transport in a uniform groundwater flow field using :green[MODFLOW-2005, MT3D, and MODELMUSE]')

st.subheader('Overview and orientation', divider="green")

st.markdown(""" The **aim of the tutorial** is to provide an applied introduction to solute transport modeling using MODFLOW and MT3D. It covers two typical scenarios within an idealized groundwater catchment:
\n**:red[Scenario A]: Prediction of a :red[contamination from a continuous releasing source]** and
\n**:green[Scenario B]: Computation of a :green[solute pulse from a point source], and traveling of the solutes through the system**.
""")

lc0, rc0 = st.columns((1,1))
with lc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport.png', caption=":red[**Scenario A:**] The idealized situation for continous solute input.")
with rc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_tracer.png', caption=":green[**Scenario B:**]The idealized situation for a tracer test.")
st.markdown("""
Both scenarios are idealized in such a way that solute transport can also be computed with analytical solutions. This approach allows the user to understand the system and to compare the results from the numerical model with the ‘precise’ analytical solution. Accordingly, the user gains a proper understanding of the benefits and limitations of the different methods. The scenarios and models are subsequently described.

**This app contains:**
- Accompanying tutorial materials (e.g. excel sheet, gpt files, tutorial pdf, etc)  
- Explanations  
- Descriptions (as To-Do lists)  
- Videos on how to set up a MODFLOW and MT3D model for a 2D idealized catchment *(see the following figure)*.


The individual steps of the modeling process are provided in the following boxes, which you can expand by clicking.


            
#### 📦 Resources used for the tutorial
The following files are provided for use throughout the tutorial...
""")

with st.expander('**... click here to see and access the resources**'):
    st.markdown("""
    You can download the resources directly using the links below. They include MODELMUSE model files for different modeling steps and supporting spreadsheets for analysis and postprocessing
    - 📄 PDF file with step-by-step instructions
        - [2D_Transport_Step_01.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_01.pdf) — for step1
        - [2D_Transport_Step_02.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_02.pdf) — for step2
        - [2D_Transport_Step_03.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_03.pdf) — for step3
        - [2D_Transport_Step_03b.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_03b.pdf) — for step3b
        - [2D_Transport_Step_04.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_04.pdf) — for step4
        - [2D_Transport_Step_04b.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_04b.pdf) — for step4b
        - [2D_Transport_Step_05.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_05.pdf) — for step5
        - [2D_Transport_Step_06.pdf](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_06.pdf) — for step6
    - 💻 MODELMUSE model files:
        - [coarse.gpt (as ZIP file)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/coarse.zip) — for steps 1–3
        - [fine.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/fine.gpt) — for step 4
        - [Dirac.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/Dirac.gpt) — for step 5
        - [Dirac_Refined.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/Dirac_Refined.gpt) — for step 6
    - 📊 Spreadsheet for postprocessing:
        - [2DTransport_Tutorial.xlsx (with data)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2DTransport_Tutorial.xlsx)
        - [2DTransport_Tutorial_empty.xlsx (empty template)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2DTransport_Tutorial_empty.xlsx)""")

st.subheader('General description of the model', divider = "green")
st.markdown("""The question and purpoose of the model, the conceptual model, and the numerical model are described in the subsequent sections.""")

with st.expander(':green[**Click here for more details of the general description of the model**]'):
    
    st.markdown("""
    #### Question/Purpose of the model
    
    **🟥 Scenario A:** The general aim is the prediction and management of a contamination plume with constant release of solutes.The goal is to simulate the spreading of a solute from a point source in a confined, homogeneous, and isotropic aquifer. The solute is introduced with a constant concentration. Observations are made at distances of 100, 300, 500, and 1000 m.
    
    The situation is idealized and can be compared with the results of an analytical solution (2D solute transport from a continuous source with advection and dispersion). The analytical solution allows users to investigate the effects of different settings of the numerical model, such as the solution scheme and discretization.
    
    **🟩 Scenario B:** The general aim of this version is to use the numerical model to simulate a tracer test to characterize the aquifer. The solute is injected with a given mass over a very short period. The injection is a point source, i.e., the tracer is inserted through a point source as a Dirac impulse (10 liters in 10 seconds, containing 1,000 g NaCl). The observation is made at a distance of 30 m.
    
    ---
    
    #### Conceptual model
    
    The confined aquifer is homogeneous and isotropic and sufficiently extends in the horizontal direction. The thickness of the confined aquifer is constant. Groundwater flows in a steady and uniform flow field with a defined specific velocity *q*, based on:
    
    Hydraulic gradient: *i* = 0.005  
    Hydraulic conductivity: *K* = 0.001 m/s
    
    Equation:
    
    $$
    q = -Ki = -0.001 \\times 0.005 = 5 \\times 10^{-6} \\text{ m/s} \\; (0.432 \\text{ m/d})
    $$
    
    Solute input configurations:
    - **🟥 Scenario A:** Areal source with constant concentration; width of source is 100 m.
    - **🟩 Scenario B:** Point source with slug input. Total mass input is 1,000 g in 10 liters.
    
    ---
    
    #### Mathematical model and analytical solution
    
    The analytical solutions for both scenarios are provided in two dedicated Streamlit apps:
    
    - **🟥 Scenario A:** [transport-2d-continuous.streamlit.app](https://transport-2d-continuous.streamlit.app/)
    - **🟩 Scenario B:** [transport-2d-dirac.streamlit.app](https://transport-2d-dirac.streamlit.app/)
    
    ---
    
    #### Numerical model – flow and transport
    
    **Model characteristics:**
    - One-layer 2D domain
    - Model top at 0 m, aquifer thickness: 10 m
    - Horizontal extent: 2500 m × 1100 m
    - Initial cell size: 100 m × 100 m
    - Hydraulic conductivity *K* = 1×10⁻³ m/s
    - Specified-head boundaries on west and east edges
    
    ---
    
    **🟥 Scenario A:**
    - Temporal discretization: 1 period (steady state), duration 86,400,000 s (1,000 days)
    - Contamination source from *x* = 300 to 400 m (central row)
    - Defined concentration boundary: *c* = 1 g/m³
    - Observations at 100, 300, 500, and 1,000 m downstream
    - Purpose: Predict solute transport over 1,000 days
    
    **🟩 Scenario B:**
    - Temporal discretization: 3 periods  
      - Period 1: 1 s (steady-state)  
      - Period 2: 10 s (injection, transient)  
      - Period 3: 4,319,990 s (transport, transient)
    - Injection via WEL boundary (point source at *x* = 400 m, central row)
      - Infiltration rate: 0.001 m³/s for 10 s
      - Injection concentration: 100,000 g/m³ (i.e., 1,000 g in 10 L)
    """)
with st.expander('**Show the initial assessment** - to assess your existing knowledge'):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_general_behavior.json", title="📋 Initial assessment")


st.subheader('Step-by-step tutorials to build the model with MODELMUSE', divider = "green")
st.markdown("""In the following you will find step-by-step instructions to build the flow- and transport model with MODELMUSE. Each step comes with a screencast video that shows the individual steps, and a 'ToDo' list with the essential steps. The full description of the tutorial is provided by a PDF document [for download here](www.link.com).

---

### :red[Scenario A - continuous source]

The first four steps will cover :red[**Scenario A - continuous source of solutes**]. The numerical model results will be compared to an analytical solution for a continuous point source that is shown in the subsequent figure.

💥 Try the [Streamlit App for 2D Transport with a continuous source here](https://transport-2d-continuous.streamlit.app/).""")

lc1, cc1, rc1 = st.columns((1,10,1))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport_continuous.png', caption="The synthetic catchment for the numerical model.")

# This are the links to the tutorial videos
videourl1 = 'https://youtu.be/nurSikcY4LQ'
videourl2 = 'https://youtu.be/D7a0goqD66c'
videourl3 = 'https://youtu.be/GXLGnDr0Jf0'
videourl3b = 'https://youtu.be/Opl3YpbiX-g'
videourl4 = 'https://youtu.be/NQHGZfaThXs'
videourl4b = 'https://youtu.be/U13EwH-cubY'
videourl5 = 'https://youtu.be/gNfuM5iWFMs'
videourl6 = 'https://youtu.be/tQXZmCfXEd8'

# Create ToDos to proceed with the steps of the exercise

# STEP 1
st.markdown("""
#### :red[STEP 1:] Setting up the flow model.
**Aim:** Design an idealized flow model for the confined aquifer resulting in defined uniform flow.
""")
with st.expander('🧠 **Show the initial assessment to prepare for STEP 1** - to assess your existing knowledge'):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step1.json", title="📋 Step 1 – Initial assessment")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 1**]"):
    st.markdown("""  
    This step walks you through the complete setup of a confined aquifer model using **ModelMuse** and prepares it for **particle tracking** with MODPATH.
    The following instructions are available as [PDF Document for download.](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_01.pdf)
    
    #### Directory Setup (Recommended)

    Organize your simulation files by creating separate folders:
    ```
    /Coarse/ - coarse_FD/
             - coarse_MOC/
    /Fine/   - fine_FD/
             - fine_MOC/
    ```
    This helps in comparing different solver methods and grid resolutions.
    
    #### 1. Initial model design
    """)

    to_do(
        [(st.write, "**Step 1.1 Launch and Configure ModelMuse.**"
        ,"\n - Open **ModelMuse**."
        ,"\n - Select :red[_Create New MODFLOW Model_] then click :red[_Next_]."
        ,"\n - Keep default units (meters and seconds)."
        ,"\n - Under description, type :red[_2D Transport Model_]."
        ,"\n - Click :red[_Next_].")],"td001",)

    to_do(
        [(st.write, "**Step 1.2 Model selection and initial grid definition**"
        ,"\n - Select :red[_MODFLOW version: MODFLOW-2005_]"),
        (st.code, """
        Number of Columns: 25       Width of each column: 100
        Number of Rows: 11          Width of each row: 100
        Number of Layers: 1
        Model Top = 0
        Aquifer Base = -10"""),
        (st.write, "- Click :red[_Finish_] to generate the grid."),],"td002",)
        
    to_do(
        [(st.write, "**Step 1.3 Time and Solver Settings.**"
         ,"\n - Go to :red[_Model > MODFLOW Time_]:"),
         (st.code, """
         Starting Time: 0
         Ending Time: 86400000
         Max First Time Step Length: 86400000"""),
         (st.write, "- Click :red[_OK_]."),], "td003")




    to_do(
        [(st.write, "**Step 1.4 Activate Packages and Set K**"
        ,"\n - Go to :red[_Model > MODFLOW Packages and Programs_]."
        ,"\n - Under :red[_Boundary Conditions_], select :red[_Specified Head > CHD_]  and Click :red[_OK_]."
        ,"\n - Go to :red[_Data > Edit Data Sets > Required > Hydrology_]"),
        (st.code, """set Kx = 0.001"""),
        (st.write,"- Click :red[_Apply_] and Click :red[_Close_].")], "td004")

    to_do(
   	   [(st.write, "**Step 1.5 Boundary Conditions**"
         ,"\n - **Left boundary:** Use the line tool to create a vertical line on the left edge, name it :red[_left_CHD_]."
         ,"\n - Go to :red[_MODFLOW Features > CHD_]."),
        (st.code, """
        Start Time: 0
        End Time: 86400000
        Starting Head: 22
        Ending Head: 22"""),
        (st.write, "- Click :red[_OK_]."
         ,"\n - **Right boundary:** Repeat the same steps, name it :red[_right_CHD_]."
         ,"\n - Go to :red[_MODFLOW Features > CHD_]"),
         (st.code, """
         Start Time: 0
         End Time: 86400000
         Starting Head: 10
         Ending Head: 10"""),
         (st.write,"- Click :red[_OK_].")],"td005")


    st.markdown("#### ⚠️ Note on Warnings")
    st.info("ModelMuse might show a **georeferencing warning**. You can safely ignore this if you're working with conceptual models.")
    
    st.markdown("""
    #### Running the model and postprocessing of results
    """)
    
    to_do(
        [(st.write, " **Step 1.6 Run MODFLOW**"
        ,"\n - Click green triangle to run MODFLOW."
        ,"\n - Save as :red[_coarse.nam_] in the appropriate folder."
        ,"\n - Verify results via :red[_ModelMonitor_] (green smiley = success), then review listing file.")], "td006")

    to_do(
        [(st.write, "**Step 1.7 Configure MODPATH**"
        ,"\n - Go to :red[_Model > MODFLOW Packages and Programs > Post Processors>MODPATH_]."
        ,"\n - :red[_Enable MODPATH_]."),
        (st.code, """
        Set Version: 6
        Reference Time: 0 
        Output Mode: Pathlines
        Tracking Direction: Forward """),
        (st.write, " Under the tab  :red[_Version 6 & 7 Options_]"
        ,"\n - Select from the dropdown :red[_StopOption = Stop at termination points (Steady State)_]."
        ,"\n - Click :red[_OK_] ")], "td007")

    to_do(
        [(st.write, " **Step 1.8 Place Particles**"
        ,"\n - Select object tool, double-click :red[_left_CHD_]."
        ,"\n - Go to :red[_MODFLOW Features > MODPATH_], choose :red[_Inititial Particle Placement_] set it to :red[_Grid_]"
		,"\n - Click :red[_OK_].")], "td008")

    to_do(
        [(st.write, " **Step 1.9 Output + Final Run**"
        ,"\n - Go to :red[_MODFLOW Output Control > Head_] set :red[_External File Type_]  to :red[_Binary_]."
        ,"\n - Save model :red[_(Ctrl+S)_], then click triangle to re-run."
        ,"\n - Ignore MODPATH v7 warning if prompted since we are using v6.")], "td009")

    to_do(
        [(st.write, " **Step 1.10 Visualize Pathlines**"
        ,"\n - Click :red[_Data Visualization > MODPATH Pathlines_]."
        ,"\n - Load the :red[_.path_] Click :red[_Apply_] Click :red[_Close_].")], "td010")

    st.markdown("""#### Video tutorial for Step 1
    The video shows all steps as a screencast. 
    """)

    st.video(videourl1)
    
    st.markdown("""
    #### Conclusion:
    The flow model is defined. Particle tracking enables the verification of flow. With the listing file, we can understand the model and analyze/quantify the flows. This step covered all steps in the model design for a numerical flow model.
    
    You've now created and simulated a simple MODFLOW-2005 flow model with defined head boundaries (CHD package) and particle tracking using MODPATH. This uniform flow model forms the foundation for the subsequent solute transport analysis.
    """)
 
with st.expander('**📋 Final assessment – Review what you learned in Step 1**'):
    render_assessment(
        filename="06_Groundwater_modeling/QUESTIONS/final_2D_trans_step1.json",
        title="📋 Final assessment",
        max_questions=6
    )
 
# STEP 2
st.markdown("""
#### :red[STEP 2:] Setting up the transport model with the FD scheme

**Aim:**
- Setting up the transport model with the FD scheme.
- Performing an initial solute transport simulation.
- Running the FD method. Postprocessing the results and analyzing the simulation.
""")
  

with st.expander("🧠 **Initial Assessment – Step 2**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step2.json", "Initial Assessment for Step 2")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 2**]"):
    st.markdown("""
    The following instructions are available as [PDF Document for download.](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_02.pdf)
    
    **Setting Up the Transport Model**
    """)
    to_do(
    [
        (st.write, "**Step 2.1 – Activating Solute Transport Packages**"
         "\n - Navigate to: :red[_Model > MODFLOW Packages and Programs > Groundwater Transport (Expand)_]."
         "\n - Select :red[_MT3DMS or MT3D-USGS_]."
         "\n - From the list, enable the following packages: :red[_BTN_], :red[_ADV_], :red[_DSP_], :red[_SSM_], :red[_GCG_] ."
         "\n - Update key settings in these packages as follows:"),
        
        (st.code, """
		BTN Package:
		- Under MT3D Options, set MT3D version to: MT3DMS
		ADV Package:
		- Advection 1 > Advection Solution Scheme: Standard Finite Difference"""),

        (st.write, "- Note: Other solution schemes will be explored in future steps."
           "\n - Click :red[_OK_] to close the packages window."),],"td011")

    to_do(
    [
    (st.write, "**Step 2.2 – Configuring Transport Model Time Discretization**"
     "\n - When prompted to configure MT3D time settings, proceed as follows:"
     "\n - Go to :red[_Model > MODFLOW Time_]."
     "\n - Choose :red[_MT3DMS_] or :red[_MT3D-USGS_]."
     "\n - Set the following parameters:"), 

        (st.code, """
		Starting Time: 0
		Ending Time: 86400000
		Initial Time Step: 86400
		Max Transport Steps per Flow Step: 1000"""),

    (st.write, "- Click :red[_OK_] to apply the settings."),],"td012")

    to_do(
    [
    (st.write, "**Step 2.3 – Defining Contaminant Source and Observation Points**"
     "\n\n🔴 **Source Definition**"
     "\n - Click :red[_Create point object_] (dot icon below the scissors)."
     "\n - Place the source at: :red[_6th row, 4th column_]."
     "\n - Name the object: :red[_source_]."
     "\n - Go to :red[_MODFLOW Features > SSM_], then configure the following:"),
    
    (st.code, """
	✔ Check: Specified Concentration
	✔ Starting Time: 0
	✔ Ending Time: 86400000
	✔ Chem concentration: 1

	If text fields appear inactive:
	- Double click to activate.
	- Or: Set “Number of times” to 1 in the bottom-left to enable input."""),

    (st.write, "- Click :red[_OK_] to save the source configuration."
               "\n\n🔎 **Observation Points**"
               "\n - Place observation points in :red[_6th row_] at the following columns:"
               "\n   - Col 5 → 100 m"
               "\n   - Col 7 → 300 m"
               "\n   - Col 9 → 500 m"
               "\n   - Col 14 → 1000 m"
               "\n - Repeat the following for each point:"),
    
    (st.code, """
	1. Select: Create point object
	2. Click on the appropriate cell
	3. Name the object (e.g., Obs100)
	4. Go to: Data Sets > Required > MT3DMS or MT3D-USGS
	5. Check: MT3DMS_Observation_Location → set to TRUE
	6. Click OK""")],"td013")

    to_do(
    [
    (st.write, "**Step 2.4 – Setting Longitudinal Dispersivity**"
     "\n - Go to :red[_Data > Edit Data Sets > Required_]."
     "\n - Expand :red[_MT3DMS, MT3D-USGS or GWT_]."
     "\n - Locate :red[_Longitudinal_Dispersivity_] and set the value:"),
    
    (st.code, "Longitudinal_Dispersivity = 10"),

    (st.write, "- Click :red[_Apply_], then click :red[_Close_]."),],"td014")

    to_do(
    [
    (st.write, "**Step 2.5 – Executing the Simulation**"
     "\n\n⚠️ **Note:** Before running the transport model, re-run the flow model to generate the :red[_.ftl_] (Flow Transport Link) file. This is required due to new boundary and source inputs."
     
     "\n\n▶️ **Running MODFLOW**"
     "\n - Click the green triangle below the Grid toolbar."
     "\n - Navigate to: :red[_Coarse/coarse_FD/_]."
     "\n - Save the model as: :red[_coarse.nam_]."
     "\n - Run the simulation."
     
     "\n\n💧 **Running MT3DMS**"
     "\n - Click the dropdown next to the green triangle."
     "\n - Select :red[_Export MT3D Input Files_]."
     "\n - Save as: :red[_coarse.mtnam_]."
     "\n - Use :red[_ModelMonitor_] to check for success."
     "\n - Review the listing file and close the command window."),
    
    (st.markdown, "**✅ Checklist:**"),
    
    (st.code, """
	✔ Check percent discrepancy in `.lst` file
	✔ Note simulation run time
	✔ Review `.MTO` file for observation data:
	Format: [Time step, Cumulative time, Layer (K), Row (I), Column (J), Concentration]""")],"td015")

    to_do(
    [
    (st.write, "**Step 2.6 – Comparing Against Analytical Solution**"
     "\n - Open the provided Excel sheet."
     "\n - Go to the :red[_Coarse_] worksheet."
     "\n - Copy and paste contents of the :red[_.mto_] file into the appropriate section."
     "\n - View the superimposed plot of numerical vs. analytical results at all observation points."),],"td016")

    to_do(
    [
    (st.write, "**Step 2.7 – Visualizing the Results**"
     "\n - Click :red[_Import and display result_] (colored icon next to the green run button)."
     "\n - Navigate to :red[_Coarse_FD/_] and double-click the :red[_.ucn_] file."
     "\n - Select the **final transport time step**."
     "\n - In the :red[_Select Model Results to Import_] window:"
     "\n   - Initially, the :red[_Classification_] dropdown shows :red[_Model Result_], and the adjacent :red[_Prefix_] field is disabled."),
    
    (st.code, """
	1. Change Classification = User Define
	2. Enter Prefix: FD_Coarse
	3. Select: Contour Grid
	4. Click OK"""),

    (st.write, "💡 **Note:** :red[_.UCN_] files store full-domain concentration data in binary format, "
               "while :red[_.MTO_] files contain data only at specified observation points.")],"td017")



    st.markdown("""
    #### Video tutorial of step 2
    The video shows all steps as a screencast. 
    """)
    st.video(videourl2)    
 
    st.markdown("""
    #### Conclusions:
    The computed concentrations and breakthrough curves look reasonable. The mass balance is considered as plausible with minimum discrepancy. The runtime of the numerical transport model can be quantified.
    """)

with st.expander("📋 **Final Assessment – Step 2**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step2.json", "Final Assessment for Step 2", max_questions=6)









    
# STEP 3
st.markdown("""
#### :red[STEP 3:] Running the transport simulation with the MOC scheme
**Aim:** Changing the solution algorithm to the MOC scheme: Performing an solute transport simulation with MOC. Optimizing the MOC method. Postprocessing the results and analyzing the simulation.
""")  

with st.expander("🧠 **Initial Assessment – Step 3**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step3.json", "Initial Assessment for Step 3")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 3**]"):
    st.markdown("""In the previous step, the transport model used the **Standard Finite Difference (FD)** solver. We now shift focus to the **Method of Characteristics (MOC)**, which is designed to reduce numerical dispersion. By disabling physical dispersion (setting dispersivity to 0), we can isolate solver effects and fine-tune key parameters like particle count and movement limits. This helps us compare MOC results with analytical benchmarks.
	The following instructions are als available as PDF Document for download: [Step 3a (Modeling)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_03.pdf) and [Step 3b (Post Processing)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_03b.pdf)
    """)

    to_do(
    [
    (st.write, "**Step 3.1 – Changing the Solver to MOC**"
     "\n - Navigate to: :red[_Model > MODFLOW Packages and Programs > Groundwater Transport > MT3DMS or MT3D-USGS > ADV_]."
     "\n - In the :red[_Advection1_] section, change the :red[_Advection Solution Scheme_] to: :red[_Method of Characteristics (MOC)_]."
     "\n - Click :red[_OK_] to apply the changes."),],"td018")

        
    to_do(
    [
    (st.write, "**Step 3.2 – Running MODFLOW and MT3DMS with MOC Solver**"
     "\n\n▶️ **Running MODFLOW**"
     "\n - Click the green triangle below the Grid icon."
     "\n - Save the model in :red[_Coarse/coarse_MOC/_] as :red[_coarse.nam_]."
     "\n - Confirm and run the simulation."

     "\n\n💧 **Running MT3DMS**"
     "\n - Click the dropdown next to the green triangle."
     "\n - Select :red[_Export MT3D Input Files_]."
     "\n - Save the input as :red[_coarse.mtnam_] in :red[_Coarse/coarse_MOC/_]."
     "\n\n✅ **Checklist:**"),
    
    (st.code, """
    ✔ Verify percent discrepancy in `.lst` file
    ✔ Record simulation runtime for comparison""")],"td019")

        
    to_do(
    [
    (st.write, "**Step 3.3 – Visualizing the Results**"
     "\n - Click :red[_Import and display result_] (colored icon next to the simulation run button)."
     "\n - Navigate to :red[_Coarse_MOC/_] and select the :red[_.ucn_] file."
     "\n - Choose the **final transport time step**."
     "\n - In the :red[_Select Model Results to Import_] window:"
     "\n   - Classification will default to :red[_Model Result_], and the :red[_Prefix_] field will be inactive."),
    
    (st.code, """
    1. Change Classification = User Define
    2. Enter Prefix: Coarse_MOC
    3. Select: Contour Grid
    4. Click OK""")],"td020")

        
    to_do(
    [
    (st.write, "**Step 3.4 – Comparing Against Analytical Solution**"
     "\n - Open the :red[_.MTO_] file in :red[_Coarse_MOC/_] and copy its contents."
     "\n - Launch the Excel analysis sheet and go to the :red[_Coarse_] worksheet."
     "\n - Paste the data to view the overlaid numerical vs. analytical plots for all observation points."),],"td021")

        

    
    st.markdown(""" 
    #### Optimizing the MOC Solver
    """)

    to_do(
    [
    (st.write, "**Step 3.5 – Iteration 1: Increasing Particle Settings**"
     "\n - Navigate to: :red[_Model > MODFLOW Packages and Programs > Groundwater Transport > MT3DMS or MT3D-USGS > ADV_]."
     "\n - Under :red[_Advection1_], adjust the following:"),
    
    (st.code, """
    Initial particles per cell (DCEPS / NPH): 10 → 16
    Maximum total moving particles (MXPART): 75,000 → 250,000"""),

    (st.write, "- Under :red[_Advection2_], increase:"),
    
    (st.code, "Maximum particles per cell (NPMAX): 20 → 200"),

    (st.write, "- Click :red[_OK_] to apply the changes."
               "\n - Since the solver type hasn’t changed, re-running the flow model is not required."
               "\n - Repeat: :red[_Running MT3DMS_], :red[_Visualizing Results_], and :red[_Comparing Against Analytical Solution_]."),],"td022")

    to_do(
    [
    (st.write, "**Step 3.6 – Iteration 2: Disabling Dispersion**"
     "\n - Go to: :red[_Data > Edit Data Sets > Required_]."
     "\n - Expand :red[_MT3DMS_, _MT3D-USGS_, or _GWT_]."
     "\n - Locate :red[_Longitudinal Dispersivity_] and set it to:"),
    
    (st.code, "Longitudinal_Dispersivity = 0"),

    (st.write, "- Repeat: :red[_Running MT3DMS_], :red[_Visualizing Results_], and :red[_Comparing Against Analytical Solution_]."),],"td023")

    to_do(
    [
    (st.write, "**Step 3.7 – Iteration 3: Further Increasing Particle Density**"
     "\n - Navigate again to: :red[_ADV > Advection1_]."
     "\n - Update the following:"),
    
    (st.code, "Initial particles per cell (DCEPS / NPH): 16 → 32"),

    (st.write, "- Repeat: :red[_Running MT3DMS_], :red[_Visualizing Results_], and :red[_Comparing Against Analytical Solution_]."),],"td024")

    to_do(
    [
    (st.write, "**Step 3.8 – Iteration 4: Re-enabling Dispersion**"
     "\n - Go to: :red[_Data > Edit Data Sets > Required_]."
     "\n - Expand :red[_MT3DMS_, _MT3D-USGS_, or _GWT_]."
     "\n - Reset the following:"),
    
    (st.code, "Longitudinal_Dispersivity = 10"),

    (st.write, "- Repeat: :red[_Running MT3DMS_], :red[_Visualizing Results_], and :red[_Comparing Against Analytical Solution_]."
               "\n - Press :red[_Ctrl + S_] to save the model."),],"td025")

    st.markdown(""" 
    #### Post-Processing and Visualization
    """)

    to_do(
    [
    (st.write, "**Step 3.9 – Using the Streamlit App for Analytical Visualization**"
     "\n - Launch the analytical app: *2D Solute Transport: Continuous Source in Uniform 1D Flow* using the provided link."
     "\n - Input the same parameters as your numerical model."),
    
    (st.code, """
    Source concentration: 1 g/m³
    Source width (Y): 100 m
    Longitudinal dispersivity (αx): 10 m
    Specific discharge (q): 0.432 m/day
    Porosity (n): 0.25
    Dispersivity ratio (αx/αy): 10
    Time: 1000 days"""),
    (st.write," Under :red[_Adjust Plot_] menu set:"),
    (st.code, """
    • Max Conc of plot (g/m³): 1
    • Max extension in x direction: 2100
    • Max extension in y direction: 550
    • Toggle: Show isolines instead of contour """),

    (st.write, "- Take a screenshot of the resulting plot once it appears."),],"td026")

    to_do(
    [
    (st.write, "**Step 3.10 – Importing the Analytical Image into ModelMuse**"
     "\n - Open your model in ModelMuse."
     "\n - Go to :red[_File > Import > Image_] and select the screenshot you saved."
     "\n - Map the anchor points as follows:"),
    
    (st.code, """
    Bottom-Left Anchor Point:
    Image: (0, -550) → Model: (400, 1100)
    Top-Right Anchor Point:
    Image: (2100, 550) → Model: (2500, 0)"""),

    (st.write, "- Press :red[_OK_] to place the image."
               "\n - Optional: Toggle grid lines using the :red[_Show/Hide 2D Grid Lines_] icon."),],"td027")

    to_do(
    [
    (st.write, "**Step 3.11 – Visualizing and Comparing Analytical & Numerical Results**"
     "\n\n🔁 **Overlaying Results**"
     "\n - Click :red[_Data Visualization_] (colored icon in toolbar)."
     "\n - If :red[_MODPATH Pathlines_] is enabled, uncheck :red[_Show Pathlines_] and press :red[_OK_]."

     "\n\n📊 **Comparing with Analytical Solution**"
     "\n - Go to :red[_Data Visualization > Contour Data > User Defined > 3D Data_]."
     "\n - Select the relevant dataset (e.g., :red[_FD_Coarse_])."
     "\n - Click :red[_Apply_], then :red[_Close_]."

     "\n\n💡 *Tip:* Use this overlay to evaluate where your numerical result diverges from the analytical benchmark."),],"td028")

    to_do(
    [
    (st.write, "**Step 3.12 – Save Your Work**"
     "\n - Press :red[_Ctrl + S_] to save your model setup."),],"td029")

    to_do(
[
    (st.write, "**Step 3.13 – Quantitative Comparison of Breakthrough Curves**\n\nSo far, you've overlaid the analytical image on your numerical model to evaluate results visually. Now we'll compare **concentration vs. time** data directly using observation points and Excel plots."),
    
    (st.write, "🔹 **Export Analytical Data from the Streamlit App**"
     "\n - In the Streamlit analytical app, define observation points at the same distances used in your numerical model."
     "\n - Once set, download the resulting CSV containing time series concentration data."),

    (st.write, "🔹 **Organize the Data in Excel**"
     "\n - Open the provided Excel analysis sheet."
     "\n - Paste the downloaded analytical CSV data into the dedicated :red[_Analytical_] section."
     "\n - Open your numerical model’s :red[_.MTO_] file and copy the data."
     "\n - Paste it into the :red[_Numerical_] section of the same Excel sheet."),
    
    (st.write, "🔹 **Compare the Results**"
     "\n - Use the preconfigured Excel plots to compare breakthrough curves at each observation point."
     "\n - Analyze the overlap and discrepancies between the numerical and analytical results."),

    (st.write, "💡 **This step allows you to validate your model quantitatively** and assess the impact of grid size, dispersion, and solver type.")],"td029a")


    
    st.markdown("""
    #### Video tutorial of step 3
    
    The first video tutorial demonstrate the model design for the 2D solute transport computation with MOC.
    """)
    
    st.video(videourl3)
    
    st.markdown(""" 
    The second video tutorial demonstrate some advanced post processing of the numerical solute transport model.
    """)
    
    st.video(videourl3b)

with st.expander("📋 **Final Assessment – Step 3**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step3.json", "Final Assessment for Step 3", max_questions=6)
	
	
	
	
	
	
	
	
	
	
	
	
	
# STEP 4

st.markdown("""
#### :red[STEP 4:] Refining the grid size and re-running the FD and MOC simulations.
**Aim:** Adapting the spatial discretization. Running the simulation with FD and MOC. Understand the effect of the grid size on the results of the computation. Postprocessing the results and analyzing the simulation.
The following instructions are als available as [PDF Document for download: Step4 (modeling)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_04.pdf) and [Step4b (postprocessing)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_04b.pdf)
""")  

with st.expander("🧠 **Initial Assessment – Step 4**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step4.json", "Initial Assessment for Step 4")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 4**]"):
    st.markdown(""" #### GRID REFINEMENT
    To improve simulation accuracy, we refine the grid in the plume region. The coarse **100 × 100 m cells are subdivided into 10 × 10 m** cells. The **source is redefined** as a 100 × 100 m rectangle spread across multiple refined cells. **Observation points are shifted** to maintain correct spacing from the new source boundary. These changes enhance resolution and better align the numerical model with analytical results.
    """)
    to_do(
    [
    (st.write, "**Step 4.1 – Refine the Grid**"
     "\n - Click the :red[_Subdivide Grid Cells_] icon."
     "\n - Select **rows 5–7 and columns 3–25** where the plume spreads."
     "\n - In the dialog box, set:"),
    (st.code, """
    From Column: 3 → Through Column: 25
    Subdivide each column into: 10
    From Row: 5 → Through Row: 7
    Subdivide each row into: 10"""),
    (st.write, "- Click :red[_OK_] to apply. Region is now 10m × 10m cells."),], "td030")

    to_do(
    [
    (st.write, "**Step 4.2 – Redefine the Source**"
     "\n - Use the :red[_Create Rectangle Object_] tool."
     "\n - Draw and name the object :red[_source_]."
     "\n - Under :red[_Vertices_], enter:"),
    (st.code, """
    (300, -500)
    (400, -500)
    (400, -600)
    (300, -600)
    (300, -500) (to close the rectangle)"""),
    (st.write, "- Go to :red[_MODFLOW Features > SSM_]. Set:"),
    (st.code, """
    Check Specified Concentration
    Starting Time: 0
    Ending Time: 86400000
    Chem Concentration: 1
    """),
    (st.write, "- Set :red[_Number of times_] = 1 if fields are inactive. Click :red[_OK_]."),], "td031")

    to_do(
    [
    (st.write, "**Step 4.3 – Update Observation Points**"
     "\n - Adjust x-coordinates by +50 m (y remains unchanged):"),
    (st.code, """
    Obs100:  x = 450 → 500
    Obs300:  x = 650 → 700
    Obs500:  x = 850 → 900
    Obs1000: x = 1350 → 1400"""),
    (st.write, "- For each point, open :red[_Vertices_] tab and update x-coordinates."),], "td032")

# FD Solver

    to_do(
    [
    (st.write, "**Step 4.4 – Run with Finite Difference Solver**"
     "\n - Change solver to :red[_Standard Finite Difference_] under ADV."),
    (st.write, "- Run MODFLOW in :red[_Fine/Fine_FD/_], name as :red[_Fine.nam_]."),
    (st.write, "- Export MT3D Input Files as :red[_Fine.mtnam_]. Monitor simulation."),
    (st.write, "- Visualize :red[_.ucn_] result and import as: :red[_Fine_FD_]."),
    (st.write, "- Paste :red[_.MTO_] output in Excel under :red[_Fine_] sheet to compare with analytical solution."),], "td033")

# MOC Solver

    to_do(
    [
    (st.write, "**Step 4.5 – Run with Method of Characteristics Solver**"
     "\n - Change solver to :red[_Method of Characteristics (MOC)_] under ADV."),
    (st.write, "- Run MODFLOW in :red[_Fine/Fine_MOC/_], name as :red[_Fine.nam_]."),
    (st.write, "- Export MT3D Input Files as :red[_Fine.mtnam_]. Monitor simulation."),
    (st.write, "- Visualize :red[_.ucn_] result and import as: :red[_Fine_MOC_]."),
    (st.write, "- Paste :red[_.MTO_] output in Excel under :red[_Fine_] sheet to compare with analytical solution."),], "td034")

    to_do(
    [
    (st.write, "**Step 4.6 – Breakthrough Curve Comparison with Refined Grid**"
     "\n - Use the Streamlit analytical app to define observation points based on the refined source boundary."
     "\n - Download the resulting CSV with analytical concentrations."
     "\n - Paste the data into the :red[_Fine_] sheet in the provided Excel template."
     "\n - Copy :red[_.MTO_] output from both FD and MOC simulations into the same sheet."
     "\n - Use the plots to compare numerical and analytical breakthrough curves.")],"td034b")

    st.markdown(""" **Zero Dispersion Case with MOC (Refined Grid)** """)

    to_do(
    [
    (st.write, "**Step 4.7 – Zero Dispersion Case with MOC (Refined Grid)**"),

    (st.write, "🔹 **Set Longitudinal Dispersivity to Zero**"
     "\n - Go to :red[_Data > Edit Data Sets > Required_]."
     "\n - Expand :red[_MT3DMS_], :red[_MT3D-USGS_], or :red[_GWT_]."
     "\n - Locate :red[_Longitudinal_Dispersivity_] and set it to **0**."
     "\n - Leave all other model settings unchanged."),

    (st.write, "🔹 **Run the Model**"
     "\n - Run MODFLOW again in :red[_Fine/Fine_MOC/_] as :red[_Fine.nam_]."
     "\n - Export MT3D input files as :red[_Fine.mtnam_] in the same folder."
     "\n - Monitor the simulation and check the listing file for errors."),

    (st.write, "🔹 **Compare with Analytical Solution**"
     "\n - Launch the Streamlit app for continuous transport."
     "\n - Set Longitudinal Dispersivity to 0."
     "\n - Observe the sharp solute front in the analytical result."),

    (st.write, "🔹 **Visualize Numerical Results in ModelMuse**"
     "\n - Import the :red[_.UCN_] file from this run."
     "\n - View isoconcentration contours."
     "\n - Toggle off background image if needed for clarity."),

    (st.write, "🔹 **Analyze Breakthrough Curves**"
     "\n - Load the :red[_.MTO_] file into the Excel sheet."
     "\n - Paste it into the appropriate :red[_Fine_] section."
     "\n - Observe sharp concentration jumps – indicating pure advection."),

    (st.write, "🔹 **(Optional)** Reset :red[_Longitudinal_Dispersivity_] back to **10 m** for future runs.")],"td034c")




        
    st.markdown("""
    #### Video tutorial of step 4
    
    The first video tutorial demonstrate the model design and the computation for FD and MOC.
    """)
    
    st.video(videourl4)    
    
    st.markdown(""" 
    The second video tutorial demonstrate some advanced post processing of the numerical solute transport model.
    """)
    st.video(videourl4b)  

with st.expander("📋 **Final Assessment – Step 4**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step4.json", "Final Assessment for Step 4", max_questions=6)
    
st.markdown("""
---
### :green[Scenario B - pulse injection (Dirac)]

The following two steps will cover :green[**Scenario B - pulse injection (tracer test)**]. The numerical model results will be compared to an analytical solution for a continuous point source that is shown in the subsequent figure.

💥 Try the [Streamlit App for 2D Transport for a Dirac injection pulse here](https://transport-2d-dirac.streamlit.app/).""")

lc1, cc1, rc1 = st.columns((1,10,1))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport_pulse.png', caption="The synthetic catchment for the numerical model.")
	
	


     
# STEP 5
st.markdown("""
#### :green[STEP 5:] Adapting the existing model to simulate a tracer test - solute input as Dirac pulse. Running the FD and MOC simulations.
**Aim:** Adapt an model to reflect a different scenario. Implement an injection well for the Dirac pulse scenario. 
""")  

with st.expander("🧠 **Initial Assessment – Step 5**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step5.json", "Initial Assessment for Step 5")

with st.expander("🛠️ :green[**Expand to see the instructions and screencast video for STEP 5**]"):
    st.markdown("""
    In this section we simulate a Dirac pulse—a brief injection of solute mass over a short
    duration—and analyze its transport behavior using both Finite Difference (FD) and Method
    of Characteristics (MOC) solvers. The results will be compared against an analytical solution
    generated through a specialized Streamlit application.
    The following instructions are als available as [PDF Document for download.](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_05.pdf)
    """)

    to_do(
    [
    (st.write, "**Step 5.1 – Setup for Dirac Pulse Injection**"),

    (st.write, "🔹 **Duplicate Refined Model**"
     "\n - Save your refined model into a new folder: :green[_Dirac_FD/_]."
     "\n - Save as: :green[_Dirac.nam_] to preserve previous configurations."),

    (st.write, "🔹 **Configure Flow Time Discretization (3 Periods)**"
     "\n - Go to :green[_Model > MODFLOW Time_] and set :green[_Number of Stress Periods = 3_]."
     "\n - Use the following values:"),
    (st.code, """
    Period 1 (Steady-State):
    Start Time: -1
    End Time: 0
    Max Step Length: 1
    Time Step Multiplier: 1

    Period 2 (Injection):
    Start Time: 0
    End Time: 10
    Max Step Length: 10
    Time Step Multiplier: 1

    Period 3 (Transport):
    Start Time: 10
    End Time: 4320000
    Max Step Length: 7200
    Time Step Multiplier: 1.2
    """),
    (st.write, "🔹 **Configure Transport Time Discretization (3 Periods)**"
     "\n - Go to :green[_Model > MODFLOW Time_] > :green[_MT3DMS_] or :green[_MT3D-USGS_]."
     "\n - Set :green[_Number of MT3DMS Periods = 3_], and use the following values:"),
    (st.code, """
    Period 1 (Steady-State):
    Start Time: -1
    End Time:  0
    Initial Time Step: 86400
    Max Transport Steps: 1000
    Time Step Multiplier: 1
    Max Step Size: 0

    Period 2 (Injection):
    Start Time: 0
    End Time: 10
    Initial Time Step: 10
    Max Transport Steps: 1000
    Time Step Multiplier: 1
    Max Step Size: 0

    Period 3 (Transport):
    Start Time: 10
    End Time: 4320000
    Initial Time Step: 7200
    Max Transport Steps: 1000
    Time Step Multiplier: 1
    Max Step Size: 0
    """),

    (st.write, "🔹 **Set Longitudinal Dispersivity**"),
    (st.code, "Longitudinal_Dispersivity = 5"),

    (st.write, "🔹 **Update Boundary Conditions**"
     "\n - Edit both CHD boundary objects."
     "\n - Set time range: :green[_-1 to 4320000_] seconds."),

    (st.write, "🔹 **Define Injection Well Source**"
     "\n - Enable :green[_Well_] package under Boundary Conditions."
     "\n - Disable :green[_MODPATH_] (under Post Processors)."
     "\n - Create a new point object named :green[_solute_injection_] at (400, -550)."
     "\n - In the WELL tab, enter this schedule:"),
    (st.code, """
    Start     End     Rate (m³/s)
    -1        0       0
    0         10      0.001
    10        4320000 0
    """),

    (st.write, " - Under :green[_SSM_], enter concentration schedule:"),
    (st.code, """
    Start     End     Concentration (mg/L)
    -1        0       0
    0         10      100000
    10        4320000 0
    """),

    (st.write, "🔹 **Place Observation Point**"
     "\n - Add a point object at (430, -550) and name it :green[_Obs30_]."
     "\n - Under :green[_MT3DMS_Observation_Location_], set to :green[_TRUE_]."),

    (st.write, "🔹 **Select FD Solver and Run Simulation**"
     "\n - Go to :green[_ADV > Advection1 > Scheme = Standard Finite Difference_]."
     "\n - Save and run MODFLOW in :green[_Dirac/Dirac_FD/_] as :green[_Dirac.nam_]."
     "\n - Export MT3D input as :green[_Dirac.mtnam_] and run it."),

    (st.write, "🔹 **Visualize and Analyze FD Results**"
     "\n - Load final :green[_.UCN_] file and observe solute pulse movement."
     "\n - Paste :green[_.MTO_] data into :green[_Dirac_] worksheet in Excel."
     "\n - Review breakthrough curve (FD simulation)."),

    (st.write, "🔹 **Repeat for MOC Solver**"
     "\n - Change advection scheme to :green[_MOC_]."
     "\n - Save and run in :green[_Dirac/Dirac_MOC/_], same file names."
     "\n - Export MT3D, run, and paste :green[_.MTO_] data into Excel."),

    (st.write, "🔹 **Compare with Analytical Solution using Streamlit App**"
     "\n - Enter the following parameters in the Streamlit app:"),
    (st.code, """
    Released Mass: 1000 g
    Specific Discharge: 0.432 m/d
    Source equivalent to model cell: ✅ (enabled for 10 m aquifer thickness)
    Longitudinal Dispersivity: 5 m
    Breakthrough Curve Extraction Distance: 30 m
    Maximum Time: 100 days
    Concentration Range: 1 g/m³
    """),

    (st.write, "🔹 **Interpret Results**"
     "\n - MOC curve matches analytical closely with a sharp front."
     "\n - FD shows numerical dispersion and smearing."),],"td091")

    st.markdown("""
    #### Video tutorial of step 5
    """)

    st.video(videourl5)

with st.expander("📋 **Final Assessment – Step 5**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step5.json", "Final Assessment for Step 5", max_questions=6)

    
# STEP 6
st.markdown("""
#### :green[STEP 6:] Refining the existing model for the tracer test and re-running the FD and MOC simulations.
**Aim:** Understand the effect of the spatial discretization. Adapt the Dirac pulse model and evaluate the performance and accuracy by comparing the results with an analytical solution. 
""")  

with st.expander("🧠 **Initial Assessment – Step 6**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step6.json", "Initial Assessment for Step 6")

with st.expander("🛠️ :green[**Expand to see the instructions and screencast video for STEP 6**]"):
    st.markdown("""
    In this section we continue our work with the Dirac point source model, introducing a refined
 computational grid to better capture near-source transport dynamics. We will focus on
 increasing grid resolution in the inlet and observation zone, and then compare the results from
 two advection schemes: Standard Finite Difference (FD) and the Method of Characteristics
 (MOC). The following instructions are als available as [PDF Document for download.](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2D_Transport_Step_05.pdf)
    """)


    to_do(
    [
    (st.write, "**Step 6.1 – Refined Grid Simulation for Dirac Pulse**"),

    (st.write, "🔹 **Save a New Model Version**"
             "\n - Save the current model into a new folder: :green[_Dirac_refined/_]."
             "\n - Use :green[_File > Save As_] to make a clean copy."),

    (st.write, "🔹 **Refine Grid in Source and Observation Zone**"
             "\n - Click the :green[_Subdivide Grid Cells_] icon."
             "\n -  Using your cursor, select the area of the model where the plume is expected to spread—this corresponds to rows 17 to 21 and columns 22 to 36."
             "\n - In the dialog, apply the following values:"),
    (st.code, """\
    From Row: 17
    Through Row: 21
    Subdivide each row into: 5

    From Column: 22
    Through Column: 36
    Subdivide each column into: 5
    """),

    (st.write, "- **This reduces the cell size from 10 m to 2 m in region where refinement is applied.**"),

    (st.write, "🔹 **Define Source and Observation Points**"
             "\n - Use the :green[_Vertices_] tab to enter precise coordinates:"),
    (st.code, """\
    Source:    (400, -550)
    Obs30:     (430, -550)
    Obs50:     (450, -550)
    Obs100:    (500, -550)
    """),

    (st.write, "🔹 **Run Simulation with Finite Difference (FD)**"
    "\n - Set advection scheme to :green[_Standard Finite Difference_]."
    "\n - Save model in :green[_dirac_refined_fd/_] and run MODFLOW."
    "\n - Export MT3D input files and run MT3DMS."
    "\n - Check listing file: mass balance error should be minimal."),

    (st.write, "🔹 **Run Simulation with MOC**"
    "\n - Change advection scheme to :green[_Method of Characteristics (MOC)_]."
    "\n - Save model in :green[_dirac_refined_moc/_]."
    "\n - Run MODFLOW and MT3DMS again."),

    (st.write, "🔹 **Post-Processing and Comparison**"
    "\n - Import :green[_.UCN_] files for each run and select final time step."
    "\n - Copy :green[_.MTO_] files into the :green[_Dirac_refined_] sheet in Excel."
    "\n - Ensure observation points align correctly."),

    (st.write, "🔹 **Compare with Analytical Solution**"
	"\n - Open the 2D Dirac Streamlit App and enter:"),
    (st.code, """\
	Breakthrough Distance: 30 m
	Released Mass: 1000 g
	Specific Discharge: 0.432 m/d
	Longitudinal Dispersivity: 5 m
	Source equivalent to model cell: ✅
	Max Time: 100 days
	Concentration Range: 1 g/m³
	"""),

    (st.write, "- Download CSV and paste into Excel alongside FD and MOC results."),

    (st.write, "🔹 **Interpretation**"
	"\n - MOC shows near-perfect match with analytical, minor oscillations."
	"\n - FD shows moderate dispersion with a smeared pulse.")],"td092")
    

        
    st.markdown("""
    #### Video tutorial of step 6
    """)
            
    st.video(videourl6)

with st.expander("📋 **Final Assessment – Step 6**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step6.json", "Final Assessment for Step 6", max_questions=6)
  
# OPTIONALLY STEPS
    
# STEP 6
st.markdown("""
---
#### :rainbow[OPTIONALLY STEPs:] Some further things to do.
**Aim:** Starting with own investigations. Extending the existing modles and solutions. 
""")  
with st.expander(":rainbow[**Expand to see the instructions**]"):
    st.markdown("""
            #### Optionally STEPs: Further Investigations
            
            These steps are designed to expand your modeling skills and deepen your understanding of solute transport processes, numerical methods, and model performance. They complement the main tutorial and offer opportunities for independent exploration.
            
            **1. Compare alternative numerical solution methods**
            **Aim:** Explore the differences between available advection schemes in MT3D and understand their effects on model behavior.
            - Switch between FD, MOC, TVD, MMOC, and HMOC schemes in the ADV package.
            - Compare plume shapes, breakthrough curves (with the spreadsheet and the analytical solution), and mass balance errors.
            - Evaluate numerical dispersion and runtime across methods.
            
            **2. Introduce heterogeneity in hydraulic conductivity**
            **Aim:** Investigate how spatial heterogeneity influences flow paths and solute transport.
            - Create zones or layers with varying hydraulic conductivity.
            - Implement block-wise structures or similar.
            - Visualize plume deformation and preferential pathways; also by using MODPATH.
            - Compare with results from a homogeneous setup.
            
            **3. Evaluate model performance under varying grid resolutions**
            **Aim:** Quantify the effect of discretization on numerical dispersion and computational cost.
            - Test multiple cell sizes (e.g., 100 m → 10 m → 2 m).
            - Monitor Peclet number and mass balance errors.
            - Use the analytical solution to quantify numerical error.
            - Plot error vs. cell size for FD and MOC.
            
            **4. Implement vertical layering (pseudo-3D)**
            **Aim:** Simulate simplified vertical transport and understand layer interactions.
            - Add a second or third model layer.
            - Vary vertical conductivity and dispersion.
            - Simulate upward or downward leakage.
            - Assess if the added complexity improves realism.
            
            **5. Design and interpret synthetic monitoring networks**
            **Aim:** Improve skills in selecting and interpreting monitoring locations.
            - Place observation wells at strategic distances and angles.
            - Analyze breakthrough curves and concentration time series.
            - Evaluate the representativeness of monitoring data relative to the full plume.
           """)     
           
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')