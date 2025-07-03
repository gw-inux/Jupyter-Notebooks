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

st.markdown(""" The **aim of the tutorial** is to provide an applied introduction in solute transport modeling with MODFLOW and MT3D. The applications consider two typical scenarios for an idealized groundwater catchment:
\n**:red[Scenario A]: Prediction of a :red[contamination from a continuous releasing source]** and
\n**:green[Scenario B]: Computation of a :green[solute pulse from a point source], and traveling of the solutes through the system**.
""")

lc0, rc0 = st.columns((1,1))
with lc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport.png', caption=":red[**Scenario A:**] The idealized situation for continous solute input.")
with rc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_tracer.png', caption=":green[**Scenario B:**]The idealized situation for a tracer test.")
st.markdown("""
Both scenarios are idealized in such a way that solute transport can be also computed with analytical solutions. This approach allows the user to understand the system, and to compare the results from the numerical model with the ‘precise’ analytical solution. Accordingly, the user gets a proper understanding of the benefits and limitations of the different methods. The scenarios and models are subsequently described.

**This app contains** materials, explanations, descriptions (as To-Do list), and videos on how to setup a MODFLOW/MT3D model for a 2D idealized catchment (see the following figure). The individual steps of the modeling process are provided in the following boxes that you can expand by clicking.
            
#### 📦 Resources used for the tutorial
The following files are provided for use throughout the tutorial...
""")

with st.expander('**... click here to see and access the ressources**'):
    st.markdown("""You can download the ressources directly using the links below. They include MODELMUSE model files for different modeling steps and supporting spreadsheets for analysis and postprocessing
    \n- 📄 PDF file with step-by-step instructions (_link to be provided_)
    - 💻 MODELMUSE model files:
        - [coarse.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/coarse.gpt) — for steps 1–3
        - [fine.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/fine.gpt) — for step 4
        - [Dirac.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/Dirac.gpt) — for step 5
        - [Dirac_Refined.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/Dirac_Refined.gpt) — for step 6
    - 📊 Spreadsheet for postprocessing:
        - [2DTransport_Tutorial.xlsx (with data)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2DTransport_Tutorial.xlsx)
        - [2DTransport_Tutorial_empty.xlsx (empty template)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2DTransport_Tutorial_empty.xlsx)""")

st.subheader('General description of the model', divider = "green")
st.markdown("""The question and purpoose of the model, the conceptual model, and the numerical model are described in the subsequent section.""")

with st.expander(':green[**Click here for more details of the general description of the model**]'):
    
    st.markdown("""
    #### Question/Purpose of the model
    
    **🟥 Scenario A:** The general aim is the prediction and management of a contamination plume with constant release of solutes. To simulate the spreading of a solute from a point source in a confined, homogeneous and isotropic aquifer. The solute is introduced with a constant concentration. Observations exist at 100, 300, 500, and 1000 m distances.
    
    The situation is idealized and can be compared with the results of an analytical solution (2D solute transport from a continuous source with advection and dispersion). The analytical solution allows users to investigate the effects of different settings of the numerical model, like solution scheme and discretization.
    
    **🟩 Scenario B:** The general aim of this version is to use the numerical model to simulate a tracer test to characterize the aquifer. The solute is injected with a given mass over a very short term. The injection is a point source, i.e., the tracer is inserted through a point source as a Dirac impulse (10 liters in 10 seconds, containing 1,000 g NaCl). The observation is at a distance of 30 m.
    
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
        [(st.write, "**Step1.1 Launch and Configure ModelMuse.**"
        ,"\n - Open **ModelMuse**."
        ,"\n - Select `Create New MODFLOW Model` then click `Next`."
        ,"\n - Keep default units (meters and seconds)."
		,"\n - Under description, type `2D Transport Model`."
		,"\n - Click `Next`.")],"td001",)

    to_do(
        [(st.write, "**Step1.2 Model selection and initial grid definition**"
        ,"\n - Select `MODFLOW version: MODFLOW-2005`"),
        (st.code, """
		Number of Columns: 25       Width of each column: 100
		Number of Rows: 11          Width of each row: 100
		Number of Layers: 1
		Model Top = 0
		Aquifer Base = -10"""),
        (st.write, "- Click `Finish` to generate the grid."),],"td002",)
        
    to_do(
        [(st.write, "**Step1.3 Time and Solver Settings.**"
         ,"\n - Go to `Model > MODFLOW Time`:"),
         (st.code, """ 
		 Starting Time: 0
		 Ending Time: 86400000
		 Max First Time Step Length: 86400000"""),
         (st.write, "- Click `OK`."),], "td003")




    to_do(
        [(st.write, "**Step1.4 Activate Packages and Set K**"
        ,"\n - Go to `Model > MODFLOW Packages and Programs`."
        ,"\n - Under `Boundary Conditions`, select `Specified Head > CHD`  and Click `OK`."
        ,"\n - Go to `Data > Edit Data Sets > Required > Hydrology`"),
		 (st.code, """set Kx = 0.001"""),
		 (st.write,"- Click `Apply` and Click `Close`.")], "td004")

    to_do(
   	   [(st.write, "**Step1.5 Boundary Conditions**"
         ,"\n - **Left boundary:** Use the line tool to create a vertical line on the left edge, name it `left_CHD`."
         ,"\n - Go to `MODFLOW Features > CHD`."),
        (st.code, """
		Start Time: 0
		End Time: 86400000
		Starting Head: 22
		Ending Head: 22"""),
        (st.write, "- Click `OK`."
         ,"\n - **Right boundary:** Repeat the same steps, name it `right_CHD`."
		 ,"\n - Go to `MODFLOW Features > CHD`"),
		(st.code, """
		Start Time: 0
		End Time: 86400000
		Starting Head: 10
		Ending Head: 10"""),
		(st.write,"- Click `OK`.")],"td005")


    st.markdown("#### ⚠️ Note on Warnings")
    st.info("ModelMuse might show a **georeferencing warning**. You can safely ignore this if you're working with conceptual models.")
    
    st.markdown("""
    #### Running the model and postprocessing of results
    """)
    
    to_do(
        [(st.write, " **Step1.6 Run MODFLOW**"
        ,"\n - Click green triangle to run MODFLOW."
        ,"\n - Save as `coarse.nam` in the appropriate folder."
        ,"\n - Verify results via ModelMonitor (green smiley = success), then review listing file.")], "td006")

    to_do(
        [(st.write, "**Step1.7 Configure MODPATH**"
        ,"\n - Go to `Model > MODFLOW Packages and Programs > Post Processors>MODPATH`."
        ,"\n - `Enable MODPATH`."),
		(st.code, """
		Set Version: 6
		Reference Time: 0 
		Output Mode: Pathlines
		Tracking Direction: Forward """),
		(st.write, " Under the tab  `Version 6 & 7 Options`"
		,"\n - Select from the dropdown `StopOption = Stop at termination points (Steady State)`."
		,"\n - Click `OK` ")], "td007")

    to_do(
        [(st.write, " **Step1.8 Place Particles**"
        ,"\n - Select object tool, double-click `left_CHD`."
        ,"\n - Go to `MODFLOW Features > MODPATH`, choose `Inititial Particle Placement` set it to `Grid`"
		,"\n - Click `OK`.")], "td008")

    to_do(
        [(st.write, " **Step1.9 Output + Final Run**"
        ,"\n - Go to `MODFLOW Output Control > Head` set `External File Type`  to `Binary`."
        ,"\n - Save model `(Ctrl+S)`, then click triangle to re-run."
        ,"\n - Ignore MODPATH v7 warning if prompted since we are using v6.")], "td009")

    to_do(
        [(st.write, " **Step1.10 Visualize Pathlines**"
        ,"\n - Click **Data Visualization > MODPATH Pathlines**."
        ,"\n - Load the `.path` Click `Apply` Click `Close`.")], "td010")

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
**Aim:** Setting up the transport model with the FD scheme: Performing an initial solute transport simulation. Running the FD method. Postprocessing the results and analyzing the simulation.
""")  

with st.expander("🧠 **Initial Assessment – Step 2**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step2.json", "Initial Assessment for Step 2")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 2**]"):
    st.markdown("""
    **Setting Up the Transport Model**
    """)
    to_do(
    [
        (st.write, "**Step 2.1 – Activating Solute Transport Packages**"
         "\n - Navigate to: `Model > MODFLOW Packages and Programs > Groundwater Transport (Expand)`."
         "\n - Select `MT3DMS or MT3D-USGS`."
         "\n - From the list, enable the following packages: `BTN`, `ADV`, `DSP`, `SSM`, `GCG`."
         "\n - Update key settings in these packages as follows:"),
        
        (st.code, """
		BTN Package:
		- Under MT3D Options, set MT3D version to: MT3DMS
		ADV Package:
		- Advection 1 > Advection Solution Scheme: Standard Finite Difference"""),

        (st.write, "- Note: Other solution schemes will be explored in future steps."
                   "\n - Click `OK` to close the packages window."),],"td011")

    to_do(
    [
        (st.write, "**Step 2.2 – Configuring Transport Model Time Discretization**"
         "\n - When prompted to configure MT3D time settings, proceed as follows:"
         "\n - Go to `Model > MODFLOW Time`."
         "\n - Choose `MT3DMS` or `MT3D-USGS`."
         "\n - Set the following parameters:"),
        
        (st.code, """
		Starting Time: 0
		Ending Time: 86400000
		Initial Time Step: 86400
		Max Transport Steps per Flow Step: 1000"""),

        (st.write, "- Click `OK` to apply the settings."),],"td012")

    to_do(
    [
        (st.write, "**Step 2.3 – Defining Contaminant Source and Observation Points**"
         "\n\n🔴 **Source Definition**"
         "\n - Click `Create point object` (dot icon below the scissors)."
         "\n - Place the source at: `6th row, 4th column`."
         "\n - Name the object: `source`."
         "\n - Go to `MODFLOW Features > SSM`, then configure the following:"),
        
        (st.code, """
		✔ Check: Specified Concentration
		✔ Starting Time: 0
		✔ Ending Time: 86400000
		✔ Chem concentration: 1

		💡 If text fields appear inactive:
		- Double-click to activate.
		- Or: Set “Number of times” to 1 in the bottom-left to enable input."""),

        (st.write, "- Click `OK` to save the source configuration."
                   "\n\n🔎 **Observation Points**"
                   "\n - Place observation points in `6th row` at the following columns:"
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
         "\n - Go to `Data > Edit Data Sets > Required`."
         "\n - Expand `MT3DMS, MT3D-USGS or GWT`."
         "\n - Locate `Longitudinal_Dispersivity` and set the value:"),
        
        (st.code, "Longitudinal_Dispersivity = 10"),

        (st.write, "- Click `Apply`, then click `Close`."),],"td014")

    to_do(
    [
        (st.write, "**Step 2.5 – Executing the Simulation**"
         "\n\n⚠️ **Note:** Before running the transport model, re-run the flow model to generate the `.ftl` (Flow Transport Link) file. This is required due to new boundary and source inputs."
         
         "\n\n▶️ **Running MODFLOW**"
         "\n - Click the green triangle below the Grid toolbar."
         "\n - Navigate to: `Coarse/coarse_FD/`."
         "\n - Save the model as: `coarse.nam`."
         "\n - Run the simulation."
         
         "\n\n💧 **Running MT3DMS**"
         "\n - Click the dropdown next to the green triangle."
         "\n - Select `Export MT3D Input Files`."
         "\n - Save as: `coarse.mtnam`."
         "\n - Use ModelMonitor to check for success."
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
         "\n - Go to the `Coarse` worksheet."
         "\n - Copy and paste contents of the `.mto` file into the appropriate section."
         "\n - View the superimposed plot of numerical vs. analytical results at all observation points."),],"td016"
)

    to_do(
    [
        (st.write, "**Step 2.7 – Visualizing the Results**"
         "\n - Click `Import and display result` (colored icon next to the green run button)."
         "\n - Navigate to `Coarse_FD/` and double-click the `.ucn` file."
         "\n - Select the **final transport time step**."
         "\n - In the `Select Model Results to Import` window:"
         "\n   - Initially, the `Classification` dropdown shows `Model Result`, and the adjacent `Prefix` field is disabled."),
        
        (st.code, """
		1. Change Classification = User Define
		2. Enter Prefix: FD_Coarse
		3. Select: Contour Grid
		4. Click OK"""),

        (st.write, "💡 **Note:** `.UCN` files store full-domain concentration data in binary format, "
                   "while `.MTO` files contain data only at specified observation points.")],"td017")


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
	""")

    to_do(
    [
        (st.write, "**Step 3.1 – Changing the Solver to MOC**"
         "\n - Navigate to: `Model > MODFLOW Packages and Programs > Groundwater Transport > MT3DMS or MT3D-USGS > ADV`."
         "\n - In the `Advection1` section, change the `Advection Solution Scheme` to: `Method of Characteristics (MOC)`."
         "\n - Click `OK` to apply the changes."),],"td018")

        
    to_do(
    [
        (st.write, "**Step 3.2 – Running MODFLOW and MT3DMS with MOC Solver**"
         "\n\n▶️ **Running MODFLOW**"
         "\n - Click the green triangle below the Grid icon."
         "\n - Save the model in `Coarse/coarse_MOC/` as `coarse.nam`."
         "\n - Confirm and run the simulation."

         "\n\n💧 **Running MT3DMS**"
         "\n - Click the dropdown next to the green triangle."
         "\n - Select `Export MT3D Input Files`."
         "\n - Save the input as `coarse.mtnam` in `Coarse/coarse_MOC/`."
         "\n\n✅ **Checklist:**"),
        
        (st.code, """
		✔ Verify percent discrepancy in `.lst` file
		✔ Record simulation runtime for comparison""")],"td019")

        
    to_do(
    [
        (st.write, "**Step 3.3 – Visualizing the Results**"
         "\n - Click `Import and display result` (colored icon next to the simulation run button)."
         "\n - Navigate to `Coarse_MOC/` and select the `.ucn` file."
         "\n - Choose the **final transport time step**."
         "\n - In the `Select Model Results to Import` window:"
         "\n   - Classification will default to `Model Result`, and the `Prefix` field will be inactive."),
        
        (st.code, """
		1. Change Classification = User Define
		2. Enter Prefix: Coarse_MOC
		3. Select: Contour Grid
		4. Click OK""")],"td020")

        
    to_do(
    [
        (st.write, "**Step 3.4 – Comparing Against Analytical Solution**"
         "\n - Open the `.MTO` file in `Coarse_MOC/` and copy its contents."
         "\n - Launch the Excel analysis sheet and go to the `Coarse` worksheet."
         "\n - Paste the data to view the overlaid numerical vs. analytical plots for all observation points."),],"td021")

        

    
    st.markdown(""" 
    ####  Optimizing the MOC Solver
    """)
    to_do(
    [
        (st.write, "**Step 3.5 – Iteration 1: Increasing Particle Settings**"
         "\n - Navigate to: `Model > MODFLOW Packages and Programs > Groundwater Transport > MT3DMS or MT3D-USGS > ADV`."
         "\n - Under `Advection1`, adjust the following:"),
        
        (st.code, """
		Initial particles per cell (DCEPS / NPH): 10 → 16
		Maximum total moving particles (MXPART): 75,000 → 250,000"""),

        (st.write, "- Under `Advection2`, increase:"),
        
        (st.code, "Maximum particles per cell (NPMAX): 20 → 200"),

        (st.write, "- Click `OK` to apply the changes."
                   "\n - 💡 Since the solver type hasn’t changed, re-running the flow model is not required."
                   "\n - ✅ Repeat: `Running MT3DMS`, `Visualizing Results`, and `Comparing Against Analytical Solution`."),],"td022")

        
    to_do(
    [
        (st.write, "**Step 3.6 – Iteration 2: Disabling Dispersion**"
         "\n - Go to: `Data > Edit Data Sets > Required`."
         "\n - Expand `MT3DMS`, `MT3D-USGS`, or `GWT`."
         "\n - Locate `Longitudinal Dispersivity` and set it to:"),
        
        (st.code, "Longitudinal_Dispersivity = 0"),

        (st.write, "- ✅ Repeat: `Running MT3DMS`, `Visualizing Results`, and `Comparing Against Analytical Solution`."),],"td023")

        
    to_do(
    [
        (st.write, "**Step 3.7 – Iteration 3: Further Increasing Particle Density**"
         "\n - Navigate again to: `ADV > Advection1`."
         "\n - Update the following:"),
        
        (st.code, "Initial particles per cell (DCEPS / NPH): 16 → 32"),

        (st.write, "- ✅ Repeat: `Running MT3DMS`, `Visualizing Results`, and `Comparing Against Analytical Solution`."),],"td024")


    to_do(
    [
        (st.write, "**Step 3.8 – Iteration 4: Re-enabling Dispersion**"
         "\n - Go to: `Data > Edit Data Sets > Required`."
         "\n - Expand `MT3DMS`, `MT3D-USGS`, or `GWT`."
         "\n - Reset the following:"),
        
        (st.code, "Longitudinal_Dispersivity = 10"),

        (st.write, "- ✅ Repeat: `Running MT3DMS`, `Visualizing Results`, and `Comparing Against Analytical Solution`."
                   "\n - 💾 Press `Ctrl + S` to save the model."),],"td025")
    
    
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

        (st.write, "- Take a screenshot of the resulting plot once it appears."),],"td026")

        
    to_do(
    [
        (st.write, "**Step 3.10 – Importing the Analytical Image into ModelMuse**"
         "\n - Open your model in ModelMuse."
         "\n - Go to `File > Import > Image` and select the screenshot you saved."
         "\n - Map the anchor points as follows:"),
        
        (st.code, """
		Top-Left Anchor Point:
		Image: (0, 400) → Model: (400, 0)
		Bottom-Right Anchor Point:
		Image: (2000, -400) → Model: (2400, -1100)"""),

        (st.write, "- Press `OK` to place the image."
                   "\n - Optional: Toggle grid lines using the `Show/Hide 2D Grid Lines` icon."),],"td027")

        
    to_do(
    [
        (st.write, "**Step 3.11 – Visualizing and Comparing Analytical & Numerical Results**"
         "\n\n🔁 **Overlaying Results**"
         "\n - Click `Data Visualization` (colored icon in toolbar)."
         "\n - If `MODPATH Pathlines` is enabled, uncheck `Show Pathlines` and press `OK`."

         "\n\n📊 **Comparing with Analytical Solution**"
         "\n - Go to `Data Visualization > Contour Data > User Defined > 3D Data`."
         "\n - Select the relevant dataset (e.g., `FD_Coarse`)."
         "\n - Click `Apply`, then `Close`."

         "\n\n💡 *Tip:* Use this overlay to evaluate where your numerical result diverges from the analytical benchmark."),],"td028")

    to_do(
    [
        (st.write, "**Step 3.12 – Save Your Work**"
         "\n - Press `Ctrl + S` to save your model setup."),],"td029")
        
    
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
         "\n - Click the `Subdivide Grid Cells` icon."
         "\n - Select **rows 5–7 and columns 3–25** where the plume spreads."
         "\n - In the dialog box, set:"),
        (st.code, """
		From Column: 3 → Through Column: 25
		Subdivide each column into: 10
		From Row: 5 → Through Row: 7
		Subdivide each row into: 10"""),
		(st.write, "- Click `OK` to apply. Region is now 10m × 10m cells."),], "td030")
    to_do(
    [
        (st.write, "**Step 4.2 – Redefine the Source**"
         "\n - Use the `Create Rectangle Object` tool."
         "\n - Draw and name the object `source`."
         "\n - Under `Vertices`, enter:"),
        (st.code, """
		(300, -500)
		(400, -500)
		(400, -600)
		(300, -600)
		(300, -500) (to close the rectangle)"""),
        (st.write, "- Go to `MODFLOW Features > SSM`. Set:"),
        (st.code, """
		Check Specified Concentration
		Starting Time: 0
		Ending Time: 86400000
		Chem Concentration: 1
		"""),
        (st.write, "- Set `Number of times` = 1 if fields are inactive. Click `OK`."),], "td031")


    to_do(
    [
        (st.write, "**Step 4.3 – Update Observation Points**"
         "\n - Adjust x-coordinates by +50 m (y remains unchanged):"),
        (st.code, """
		Obs100:  x = 450 → 500
		Obs300:  x = 650 → 700
		Obs500:  x = 850 → 900
		Obs1000: x = 1350 → 1400"""),
        (st.write, "- For each point, open `Vertices` tab and update x-coordinates."),], "td032")


# FD Solver

    to_do(
    [
        (st.write, "**Step 4.4 – Run with Finite Difference Solver**"
         "\n - Change solver to `Standard Finite Difference` under ADV."),
        (st.write, "- Run MODFLOW in `Fine/Fine_FD/`, name as `Fine.nam`."),
        (st.write, "- Export MT3D Input Files as `Fine.mtnam`. Monitor simulation."),
        (st.write, "- Visualize `.ucn` result and import as:`Fine_FD`."),
        (st.write, "- Paste `.MTO` output in Excel under `Fine` sheet to compare with analytical solution."),], "td033")


# MOC Solver

    to_do(
    [
        (st.write, "**Step 4.5 – Run with Method of Characteristics Solver**"
         "\n - Change solver to `Method of Characteristics (MOC)` under ADV."),
        (st.write, "- Run MODFLOW in `Fine/Fine_MOC/`, name as `Fine.nam`."),
        (st.write, "- Export MT3D Input Files as `Fine.mtnam`. Monitor simulation."),
        (st.write, "- Visualize `.ucn` result and import as: `Fine_MOC`."),
        (st.write, "- Paste `.MTO` output in Excel under `Fine` sheet to compare with analytical solution."),], "td034")

        
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
	
	
#Video 4b,5 and 6 Remain. Rest all are updated. 03 July 2025. Navneet Sinha	

    
    
# STEP 5
st.markdown("""
#### :green[STEP 5:] Adapting the existing model to simulate a tracer test - solute input as Dirac pulse. Running the FD and MOC simulations.
**Aim:** Adapt an model to reflect a different scenario. Implement an injection well for the Dirac pulse scenario. 
""")  

with st.expander("🧠 **Initial Assessment – Step 5**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step5.json", "Initial Assessment for Step 5")

with st.expander("🛠️ :green[**Expand to see the instructions and screencast video for STEP 5**]"):
    st.markdown("""
    More about step 5
    """)
    to_do(
        [(st.write, "...")],"td091",)

    to_do(
        [(st.write, "...")],"td092",)
        
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
    More about step 6
    """)
    to_do(
        [(st.write, "...")],"td093",)

    to_do(
        [(st.write, "...")],"td094",)
        
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