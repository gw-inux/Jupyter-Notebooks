# Loading the required Python libraries
import streamlit as st
from streamlit_extras.stodo import to_do

st.title('Tutorial – Numerical computation of solute transport: Demonstration of MT3D applications')

st.header('2D solute transport in a uniform groundwater flow field using :green[MODFLOW-2005, MT3D, and MODELMUSE]')

st.subheader('Overview and orientationg', divider="green")

st.markdown(""" The **aim of the tutorial** is to provide an applied introduction in solute transport modeling with MODFLOW and MT3D. The applications consider two typical scenarios for an idealized groundwater catchment:
\n**:red[Scenario A]: Prediction of a :red[contamination from a continuous releasing source]** and
\n**:green[Scenario B]: Computation of a :green[solute pulse from a point source], and traveling of the solutes through the system**.

Both scenarios are idealized in such a way that solute transport can be also computed with analytical solutions. This approach allows the user to understand the system, and to compare the results from the numerical model with the ‘precise’ analytical solution. Accordingly, the user gets a proper understanding of the benefits and limitations of the different methods. The scenarios and models are subsequently described.

**This app contains** materials, explanations, descriptions (as To-Do list), and videos on how to setup a MODFLOW/MT3D model for a 2D idealized catchment (see the following figure). The individual steps of the modeling process are provided in the following boxes that you can expand by clicking.
            
#### Ressources used for the tutorial
- The PDF File with the step-by-step tutorial will be available on GitHub (_link to be provided_)
- The MODELMUSE model files (....gpt) will be available on GitHub (_link to be provided_)""")

lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport.png', caption="The synthetic catchment for the numerical model.")

st.subheader('General description of the model', divider = "green")
st.markdown("""The question and purpoose of the model, the conceptual model, and the numerical model are described in the subsequent section.""")
with st.expander(':green[**Click here for more details of the general description of the model**]'):
    st.markdown("""
        #### Question/Purpose of the model:
        \n**:red[Scenario A]:**	The general aims is the prediction and management of a contamination plume with constant release of solutes. To simulate the spreading of a solute from a point source in a confined, homogeneous and isotropic aquifer. The solute is introduced with a constant concentration. Observations exist in 100, 300, 500, and 1000 m distances.
        
        The situation is idealized and can be compared with the results of an analytical solution (2D solute transport from a continuous source with advection and dispersion). The analytical solution allows users to investigate the effects of different settings of the numerical model, like solution scheme and discretization.
        \n**:green[Scenario B]:**	The general aim of this version is to use the numerical models to simulate a tracer test to characterize the aquifer. The solute is injected with a given mass over a very short term. The injection is a point source, i.e., the tracer is inserted through a point source as a Dirac impulse (10 liters in 10 seconds, containing 1,000 g NaCl). The observation is in a distance of 30 m.
        
        #### Conceptual model:
        The confined aquifer is homogeneous and isotropic and sufficiently extents in horizontal direction. The thickness of the confined aquifer is constant. Groundwater flows in a steady and uniform flow field with a defined specific velocity _q_ with the hydraulic gradient _i_ = 0.005 and the hydraulic conductivity _K_ = 0.001 m/s:
        
        $q = -Ki$
        
        = 5E-6 m/s (0.432 m/d)
        
        The solute is introduced for the two situations:
        \n**:red[Scenario A]:**	Areal source with constant concentration; width of source is 100 m.
        \n**:green[Scenario B]:**	Point source with slug input. Total mass input is 1,000 g in 10 liters.
        
        #### Mathematical model and analytical solution
        The mathematical model and the analytical solution for both scenarios is provided by individual Streamlit apps.
        
        \n**:red[Scenario A]:** [https://transport-2d-continuous.streamlit.app/](https://transport-2d-continuous.streamlit.app/)
        \n**:green[Scenario B]:** [https://transport-2d-dirac.streamlit.app/](https://transport-2d-dirac.streamlit.app/)
        
        #### Numerical model – flow and transport:
        The basic model characteristics are 
        -	Spatial discretization:
            - One layer 2D domain
            - Model top at 0 m with an qquifer thickness of 10 m.
            - horizontal dimension 2500 x 1100 m2
            - initial cell size 100 x 100 m2
            - Aquifer thickness 10 m.
        -	Hydraulic conductivity K = 1E-3 m/s.
        -	Two defined head boundary conditions to establish the uniform flow field (west and east border). 
        
        \n**:red[Scenario A]:**
        -	Temporal discretization: one period, duration 86,400,000 seconds (1,000 days), steady state
        -	Source of contamination from x = 300 to 400 m (central row)
        -	Source as defined concentration boundary with c = 1 g/m3
        -	Observations in 100, 300, 500, and 1,000 m distance from the contamination.
        -	Investigation/Prediction of the contamination for the next 1000 days
        
        \n**:green[Scenario B]:**
        -	Temporal discretization: three periods
            - Period 1: duration 1 s, steady-state
            - Period 2 (injection): duration 10 s, transient
            - Period 3 (solute traveling): duration 4319990 s, transient
        -   Injection through a WEL boundary (injection well)
            - placed at x = 400 m (central row),
            - infiltration rate 0.001 m3/s for 10 seconds 
        - Injection concentration = 100,000 g/m3 (total mass 1,000 g)
        
        """)

st.subheader('Step-by-step tutorials to build the model with MODELMUSE', divider = "green")
st.markdown("""In the following you will find step-by-step instructions to build the flow- and transport model with MODELMUSE. Each step comes with a screencast video that shows the individual steps, and a 'ToDo' list with the essential steps. The full description of the tutorial is provided by a PDF document [for download here](www.link.com).

#### Scenario A - continuous source

The first three steps will cover :red[**Scenario A - continuous source of solutes**]. The numerical model results will be compared to an analytical solution for a continuous point source that is shown in the subsequent figure, [link to the resource here](https://transport-2d-continuous.streamlit.app/).""")

lc1, cc1, rc1 = st.columns((20,60,20))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport_continuous.png', caption="The synthetic catchment for the numerical model.")

# This are the links to the tutorial videos
videourl1 = 'https://youtu.be/nurSikcY4LQ'
videourl2 = 'https://youtu.be/D7a0goqD66c'
videourl3 = 'https://youtu.be/GXLGnDr0Jf0'
videourl3b = 'https://youtu.be/eVihqCz_6lQ'
videourl4 = 'https://youtu.be/zVY2GwFgP3c'
videourl5 = 'https://youtu.be/siDaOcjkm54'
videourl6 = 'https://youtu.be/f7d1CDT8koQ'

# Create ToDos to proceed with the steps of the exercise

# STEP 1

with st.expander(":red[**Step 1: Setting up the flow model.**] - Expand to see the instructions"):
    st.markdown("""
    ### STEP 1: Setting up the flow model.
    **Aim:** Design an idealized flow model for the confined aquifer resulting in defined uniform flow.
    
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
    
    #### Initial model design
    """)
#    st.markdown("#### 1. Launch and Configure ModelMuse")
#    to_do([
#        (st.write, "Open **ModelMuse**."),
#        (st.write, "Select **Create New MODFLOW Model**, then click **Next**."),
#        (st.write, "Keep default units (meters, seconds). Under description, type `2D Transport Model`. Click **Next**."),
#    ], "td001")

    to_do(
        [(st.write, "1. Launch and Configure ModelMuse."
        ,"\n - Open **ModelMuse**."
        ,"\n - Select **Create New MODFLOW Model**, then click **Next**."
        ,"\n - Keep default units (meters, seconds). Under description, type `2D Transport Model`. Click **Next**.")],"td001",)

    to_do(
        [(st.write, "2. Model selection and initial grid definition"
        ,"\n - Select 'MODFLOW version: MODFLOW-2005'"
        ,"\n - Columns: 25 (Width = 100), Rows: 11 (Width = 100), Layers: 1."
        ,"\n - Model Top = 0, Aquifer Base = -10"
        ,"\n - Click **Finish** to generate the grid.")],"td002",)
        
    to_do(
        [(st.write, "3. Time and Solver Settings."
        ,"\n - Go to **Model > MODFLOW Time**:"
        ,"\n - Starting Time: `0`, Ending Time: `86400000`"
        ,"\n - Max First Time Step Length: `86400000` → Click **OK**.")], "td003")

    to_do(
        [(st.write, "4. Activate Packages and Set K"
        ,"\n - Go to **Model > MODFLOW Packages and Programs**."
        ,"\n - Enable **Specified Head (CHD)** under Boundary Conditions → Click **OK**."
        ,"\n - Go to **Data > Edit Data Sets > Required > Hydrology**, set `Kx = 0.001` → Apply and Close.")], "td004")

    to_do(
        [(st.write, "5. Boundary Conditions"
        ,"\n - **Left boundary:** Use line tool to create vertical line on left edge, name it `left_CHD`."
        ,"\n - Go to MODFLOW Features > CHD → Set Start/End Time: `0` to `86400000`, Head: `22` → OK."
        ,"\n - **Right boundary:** Same process, name `right_CHD`."
        ,"\n - Set Start/End Head to `10`. MODFLOW Features > CHD → OK.")], "td005")

    st.markdown("#### ⚠️ Note on Warnings")
    st.info("ModelMuse might show a **georeferencing warning**. You can safely ignore this if you're working with conceptual models.")
    
    st.markdown("""
    #### Running the model and postprocessing of results
    """)
    
    to_do(
        [(st.write, "6. Run MODFLOW"
        ,"\n - Click green triangle to run MODFLOW."
        ,"\n - Save as `coarse.nam` in the appropriate folder."
        ,"\n - Verify results via ModelMonitor (green smiley = success), then review listing file.")], "td006")

    to_do(
        [(st.write, "7. Configure MODPATH"
        ,"\n - Go to **Model > MODFLOW Packages and Programs > Post Processors**."
        ,"\n - Enable **MODPATH**. Set Version: 6, Output Mode: Pathlines, Direction: Forward."
        ,"\n - Under Version Options: `StopOption = Stop at termination points (Steady State)`.")], "td007")

    to_do(
        [(st.write, "8. Place Particles"
        ,"\n - Select object tool, double-click `left_CHD`."
        ,"\n - Go to MODFLOW Features > MODPATH, choose `Grid` placement → OK.")], "td008")

    to_do(
        [(st.write, "9. Output + Final Run"
        ,"\n - Go to **MODFLOW Output Control > Head**, set to **Binary**."
        ,"\n - Save model (Ctrl+S), then click triangle to re-run."
        ,"\n - Ignore MODPATH v7 warning if prompted — we use v6.")], "td009")

    to_do(
        [(st.write, "10. Visualize Pathlines"
        ,"\n - Click **Data Visualization > MODPATH Pathlines**."
        ,"\n - Load the `.path` file → Apply → Close.")], "td010")

    st.markdown("""#### Video tutorial for Step 1
    The video shows all steps as a screencast. 
    """)

    st.video(videourl1)
    
    st.markdown("""
    #### Conclusion:
    The flow model is defined. Particle tracking enables the verification of flow. With the listing file, we can understand the model and analyze/quantify the flows. This step covered all steps in the model design for a numerical flow model.
    
    You've now created and simulated a simple MODFLOW-2005 flow model with defined head boundaries (CHD package) and particle tracking using MODPATH. This uniform flow model forms the foundation for the subsequent solute transport analysis.
    """)
    
# STEP 2
    
with st.expander(":red[**Step 2: Setting up the transport model with the FD scheme.**] - Expand to see the instructions"):
    st.markdown("""
    #### STEP 2: Setting up the transport model with the FD scheme
    **Aim:** Performing an initial solute transport simulation. Running the FD method. Postprocessing the results and analyzing the simulation.
            
    #### Substep 2
    """)
    to_do(
        [(st.write, "...")],"td04",)
    to_do(
        [(st.write, "...")],"td05",)
    to_do(
        [(st.write, "...")],"td06",)
    to_do(
        [(st.write, "...")],"td07",)

    st.markdown("""
    #### Video tutorial of step 2
    The video shows all steps as a screencast. 
    """)
    st.video(videourl2)    
 
    st.markdown("""
    #### Conclusions:
    The computed concentrations and breakthrough curves look reasonable. The mass balance is considered as plausible with minimum discrepancy. The runtime of the numerical transport model can be quantified.
    """)

# STEP 3
    
with st.expander(":red[**Step 3: Setting up the transport model with the MOC scheme**] - Expand to see the instructions"):
    st.markdown("""
    #### STEP 3: Setting up the transport model with the MOC scheme
            
    #### Substep 1
    """)
    to_do(
        [(st.write, "...")],"td08",)
        
    to_do(
        [(st.write, "...")],"td09",)
        
    to_do(
        [(st.write, "...")],"td10",)
        
    to_do(
        [(st.write, "...")],"td11",)
        
    to_do(
        [(st.write, "...")],"td12",)
    
    st.markdown(""" 
    #### Substep 2
    """)
    to_do(
        [(st.write, "...")],"td13",)
        
    to_do(
        [(st.write, "...")],"td14",)
        
    to_do(
        [(st.write, "...")],"td15",)

    to_do(
        [(st.write, "select “Create rectangle object” for recharge zone containing outflow boundary."
        ,"\n - Click on the upper right corner of the grid in the top view with the left mouse button; press the left mouse button again, keep it down, move the cursor to (2000, 0), and release the left mouse button."
        ,"\n - name object (like “recharge_right”)."
        ,"\n - select “MODFLOW Features” and “RCH”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Recharge rate,” type the following expression into the input field: 200/1000/365.25/86400, press “OK,” and press “OK” again.")],"td16",)    
    
    st.markdown(""" 
    #### Substep 3
    """)
        
    to_do(
        [(st.write, "...")],"td17",)
        
    to_do(
        [(st.write, "...")],"td18",)
        
    to_do(
        [(st.write, "select “Create polyline object” (symbol consisting of three line segments, two rows below “View”) for river."
        ,"\n - Click on the lower-left corner in the top view with the left mouse button, move the cursor to (2500, 1500), and double-click."
        ,"\n - name polyline object (like “river”)."
        ,"\n - select “MODFLOW Features” and “RIV”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “River stage,” type the following expression into the input field: interpolate (x, 260, 0, 258, 2500), and press “OK.”."
        ,"\n - select “F()” below “Conductance per unit length or area,” type the following expression into the input field: 1000/86400, and press “OK” (This corresponds to a streambed conductance of 1000 m²/d.)."
        ,"\n - select “F()” below “River bottom,” type the following expression into the input field: interpolate (x, 255, 0, 253, 2500), press “OK,” and press “OK” again (This corresponds to a water depth of 5 m.).")],"td19",)
        
    st.markdown(""" 
    #### Substep 4
    """)
        
    to_do(
        [(st.write, "...")],"td20",)
        
    to_do(
        [(st.write, "...")],"td21",)
        
    to_do(
        [(st.write, "...")],"td22",)
        
    to_do(
        [(st.write, "select “Create point object” for the second well ."
        ,"\n - Click on the cell containing the well location (3050, 1450)."
        ,"\n - name point object (like “well 2”)."
        ,"\n - select “MODFLOW Features” and “WEL”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Pumping rate per unit length or area”, type the following expression into the in-put field: -5000/86400, and press “OK” (Please do not forget the negative sign! Input corresponds to a pumping rate of 5000 m³/d.).")],"td23",)        

    st.markdown("""
    #### Video tutorial of step 3
    
    The first video tutorial demonstrate the model design for the 2D solute transport computation with MOC.
    """)
    
    st.video(videourl3)
    
    st.markdown(""" 
    The second video tutorial demonstrate some advanced post processing of the numerical solute transport model.
    """)
    
    st.video(videourl3b)

# STEP 4
with st.expander(":red[**Step 4: Properties and Simulation**] - Expand to see the instructions"):
    st.markdown("""
    #### STEP 4:
            
    #### Substep 1
    """)
    to_do(
        [(st.write, "select “Data” / “Edit Data Sets” / “Required” in the menu bar.")],"td24",)
        
    to_do(
        [(st.write, "select “Modflow_Initial_Head”, then set initial head = 257, press “Apply” and press “Close” .")],"td25",)
    
    st.markdown(""" 
            #### Run Simulation / MODFLOW
           """)    
        
    to_do(
        [(st.write, "select “File” / “Save” (no model archive needs to be created) .")],"td26",)
        
    to_do(
        [(st.write, "select “Run MODFLOW-2005” by clicking on the green triangle below “Grid”.")],"td27",)
        
    to_do(
        [(st.write, "confirm the file name to save MODFLOW input files (*.nam where “*” stands for the model name).")],"td28",)
        
    to_do(
        [(st.write, "check information from ModelMonitor (“green smileys” – hopefully …).")],"td29",)
        
    to_do(
        [(st.write, "close ModelMonitor window .")],"td30",)
        
    st.markdown("""
    #### Video tutorial of step 4
    """)
    
    st.video(videourl4)    

st.markdown("""#### Scenario B - pulse injection (Dirac)

The following two steps will cover :green[**Scenario B - pulse injection (tracer test)**]. The numerical model results will be compared to an analytical solution for a continuous point source that is shown in the subsequent figure, [link to the resource here](https://transport-2d-dirac.streamlit.app/).""")

lc1, cc1, rc1 = st.columns((20,60,20))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport_pulse.png', caption="The synthetic catchment for the numerical model.")

    
    
# STEP 5
    
with st.expander(":green[**Step 5: Postprocessing**] - Expand to see the instructions"):
    st.markdown("""
    #### STEP 5:
            
    #### Substep 1
    """)
    to_do(
        [(st.write, "...")],"td031",)

    to_do(
        [(st.write, "...")],"td032",)
        
    st.markdown("""
    #### Video tutorial of step 5
    """)
            
    st.video(videourl5)
    
# STEP 6
    
with st.expander(":green[**Step 6: Refining the Dirac-pulse model**] - Expand to see the instructions"):
    st.markdown("""
    #### STEP 6: Refining the Dirac-pulse model
            
    #### Substep 1
    """)
    to_do(
        [(st.write, "...")],"td033",)

    to_do(
        [(st.write, "...")],"td034",)
        
    st.markdown("""
    #### Video tutorial of step 6
    """)
            
    st.video(videourl6)
    
# OPTIONALLY STEPS
    
with st.expander(":green[**OPTIONALLY Steps: Some further things to do**] - Expand to see the instructions"):
    st.markdown("""
            #### Optionally STEPs: Some further things To Do
            You can do further optional steps with the finished model.
            
            #### Optionally use other transport algorithms
           """)
    to_do(
        [(st.write, "...")],"td053",)      