# Loading the required Python libraries
import streamlit as st
from streamlit_extras.stodo import to_do

# also Interactive Documents 08-03-001

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Rudolf Liedl": [1] 
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
    
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

#--- User Interface

st.title('Modflow-2005/MODELMUSE Tutorial')
st.header('2D Steady State Groundwater Flow for a Synthetic Catchment')

st.subheader('Modeldesign with :green[MODFLOW-2005 and MODELMUSE]', divider="green")

st.markdown("""
            This app contains a tutorial with descriptions (as To-Do list) and videos on how to setup a MODFLOW model for 2D synthetic catchment (see the following figure). The individual steps of the modeling process are provided in the following boxes that you can expand by clicking.
           """)
with st.expander('**Click here to get access to :red[ressources used for the tutorial] (PDFs, Modelfiles, Images)**'):
    st.markdown("""          
            #### Ressources used for the tutorial
            - The background images are available on GitHub 
              - https://github.com/gw-inux/Jupyter-Notebooks/blob/main/06_Groundwater_modeling/FIGS/MAP_well.jpg
              - https://github.com/gw-inux/Jupyter-Notebooks/blob/main/06_Groundwater_modeling/FIGS/MAP_calib.jpg
            - The PDF File with the step-by-step tutorial is available on GitHub   
              - https://github.com/gw-inux/Jupyter-Notebooks/blob/main/06_Groundwater_modeling/DATA/TUTORIAL_2DSYNTH.pdf
            - The MODELMUSE model files (....gpt) is available on GitHub
              - https://github.com/gw-inux/Jupyter-Notebooks/blob/main/06_Groundwater_modeling/DATA/2D_Synthetic.gpt
           """)
    
lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('06_Groundwater_modeling/FIGS/2D_synthetic.png', caption="The synthetic catchment for the numerical model.")

# This are the links to the tutorial videos
videourl1 = 'https://youtu.be/H49fWN3D1H0'
videourl2 = 'https://youtu.be/5jDPDjX3GCE'
videourl3 = 'https://youtu.be/YF9dE1gWg3I'
videourl4 = 'https://youtu.be/2YjltpX2cKM'
videourl5 = 'https://youtu.be/cTUlaRniPcc'

# Create ToDos to proceed with the steps of the exercise

# STEP 1

with st.expander(":blue[**Step 1: Discretization in space and time**] - Expand to see the instructions"):
    st.markdown("""
            #### STEP 1: Discretization in space and time
            This is the initial step of the model design. We start with the MODELMUSE initial screen. There you can define the specific numerical model and the initial discretization in space. Afterwards, in the MODFLOW main window, you can define the discretization of time.
            
            #### Create a new model
           """)
    to_do(
        [(st.write, "Start MODELMUSE and “Create new MODFLOW model” and press “Next” until you can specify the grid.")],"td01",)
    to_do(
        [(st.write, "specify initial grid (difficult to be changed later!)."
        ,"\n - note: grid origin is at the upper left(!) corner, and length unit is meters (default)"
        ,"\n - modify y = 2500 for grid origin"
        ,"\n - set further input data: number of columns = 40, number of rows = 25, number of layers = 1, model_top = 265, upper aquifer = 250"
        ,"\n - Press “Finish”")],"td02",)
    to_do(
        [(st.write, "select “File” / “Save as” in the menu bar, and then save input data under a file name like “myfirstmodel” (or so) by using the format mmZLib.")], "td03",)
    st.markdown(""" 
            #### Import background image
           """)
    st.video(videourl1)
    
# STEP 2
    
with st.expander(":blue[**Step 2: Structure & Parameters**] - Expand to see the instructions"):
    st.markdown("""
            #### STEP 2: Define structure and parameters
            In the second step we define the structure (which is simply the idealized aquifer block) and the hydrogeologic parameters.
            
            #### Enter Basic Aquifer Data
           """)
    to_do(
        [(st.write, "select “Data” / “Edit Data Sets” / “Required” in the menu bar.")],"td04",)
    to_do(
        [(st.write, "_[select “Layer definition” on the left side, then check “Model_Top” and “Upper_Aquifer_Bottom” (values should be 265 and 250, resp.)]._")],"td05",)
    to_do(
        [(st.write, "select “Hydrology”:"
        ,"\n - select “Kx” and set Kx = 0.005 (unit of hydraulic conductivity is m/s by default)")],"td06",)
    to_do(
        [(st.write, "select “Create rectangle object” in the graphical menu (= square two rows below “Customize”)."
        ,"\n - Click on the upper right corner of the grid in the top view with the left mouse button"
        ,"\n - Press the left mouse button again, keep it down, move the cursor to (2500, 1500), and release the left mouse button"
        ,"\n - name the object (like “small_K”)"
        ,"\n - select tab “Data Sets,” then move to “Required” / “Hydrology” / “Kx.”"
        ,"\n - replace 0.005 by 0.002 and press “OK.”")],"td07",)
        
    st.video(videourl2)    

# STEP 3
    
with st.expander(":blue[**Step 3: Boundary Conditions**] - Expand to see the instructions"):
    st.markdown("""
            #### STEP 3: Boundary conditions
            In the third step we define the boundary conditions.
            
            #### Set Defined Head Boundary Condition
           """)
    to_do(
        [(st.write, "select “Model” / “MODFLOW Packages and Programs” in the menu bar.")],"td08",)
        
    to_do(
        [(st.write, "select “Boundary conditions” / “Specified head” on the left side, then tick the sub-item “CHD” and press “OK.”.")],"td09",)
        
    to_do(
        [(st.write, "select “Create straight-line object” in the graphical menu (stairs-like symbol two rows below “Customize”).")],"td10",)
        
    to_do(
        [(st.write, "Click on the upper-left cell in the top view with the left mouse button, move the cursor to the lower-left cell, and double-click."
        ,"\n - name straight-line object, e.g., “inflowhead.”"
        ,"\n - select the tab “MODFLOW Features” and then “CHD.”"
        ,"\n - in the table: set starting time = -1, ending time = 0, starting head = 260, ending head = 260, and press “OK”.")],"td11",)
        
    to_do(
        [(st.write, "Click on the upper right cell in the top view with the left mouse button, move the cursor to the lower right cell, and double-click."
        ,"\n - name straight-line object, e.g., “outflowhead.”"
        ,"\n - select “MODFLOW Features” and “CHD.”"
        ,"\n - set starting time = -1 and ending time = 0"
        ,"\n - Click on the symbol “F()” below “Starting head.”"
        ,"\n - type the following expression into the input field (above “Logical operators”): interpolate (y, 256, 0, 254, 2500), press “OK”"
        ,"\n - repeat for “Ending head.”")],"td12",)
    
    st.markdown(""" 
            #### Set Recharge Boundary Condition
           """)
    to_do(
        [(st.write, "select “Model” / “MODFLOW Packages and Programs” in the menu bar.")],"td13",)
        
    to_do(
        [(st.write, "select “Boundary conditions” / “Specified flux” on the left side, then tick the sub-item “RCH” and press “OK”.")],"td14",)
        
    to_do(
        [(st.write, "select “Create rectangle object” for recharge zone containing inflow boundary."
        ,"\n - click on upper left corner of grid in top view with left mouse button; press left mouse button again, keep it down, move cursor to (2000, 0), and release left mouse button."
        ,"\n - name object (like “recharge_left”)."
        ,"\n - select “MODFLOW Features” and “RCH”."
        ,"\n - set starting time = -1, ending time = 0, and select “F()” below “Recharge rate”."
        ,"\n - type the following expression into the input field: 150/1000/365.25/86400 [no “=” required] (unit for recharge rate is according to space/time dimension of the model (m and s by default), i.e., conversion from mm/a is needed), press “OK,” and press “OK” again.")],"td15",)

    to_do(
        [(st.write, "select “Create rectangle object” for recharge zone containing outflow boundary."
        ,"\n - Click on the upper right corner of the grid in the top view with the left mouse button; press the left mouse button again, keep it down, move the cursor to (2000, 0), and release the left mouse button."
        ,"\n - name object (like “recharge_right”)."
        ,"\n - select “MODFLOW Features” and “RCH”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Recharge rate,” type the following expression into the input field: 200/1000/365.25/86400, press “OK,” and press “OK” again.")],"td16",)    
    
    
    st.markdown(""" 
            #### Set River Boundary Condition
           """)
        
    to_do(
        [(st.write, "select “Model” / “MODFLOW Packages and Programs” in the menu bar.")],"td17",)
        
    to_do(
        [(st.write, "select “Boundary conditions” / “Head-dependent flux” on the left side, then tick the sub-item “RIV” and press “OK.”.")],"td18",)
        
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
            #### Define Wells
           """)
        
    to_do(
        [(st.write, "select “Model” / “MODFLOW Packages and Programs” in the menu bar .")],"td20",)
        
    to_do(
        [(st.write, "select “Boundary conditions” / “Specified flux” on the left side, then tick the sub-item “WEL” and press “OK”.")],"td21",)
        
    to_do(
        [(st.write, "select “Create point object” (dot symbol two rows below “Navigation”) for the first well."
        ,"\n - click on the cell containing the well location (3050, 1450)."
        ,"\n - name point object (like “well 1”)."
        ,"\n - select “MODFLOW Features” and “WEL”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Pumping rate per unit length or area”, type the following expression into the in-put field: -2000/86400and press “OK” (Please do not forget the negative sign! Input corresponds to a pumping rate of 2000 m³/d.).")],"td22",)
        
    to_do(
        [(st.write, "select “Create point object” for the second well ."
        ,"\n - Click on the cell containing the well location (3050, 1450)."
        ,"\n - name point object (like “well 2”)."
        ,"\n - select “MODFLOW Features” and “WEL”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Pumping rate per unit length or area”, type the following expression into the in-put field: -5000/86400, and press “OK” (Please do not forget the negative sign! Input corresponds to a pumping rate of 5000 m³/d.).")],"td23",)        
        
    st.video(videourl3)
    
# STEP 4
    
with st.expander(":blue[**Step 4: Properties and Simulation**] - Expand to see the instructions"):
    st.markdown("""
            #### STEP 4: Properties and Simulation
            Once the inital model design is finish, we can define the numerical settings and run the simulation.
            
            #### Define Initial Head
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
    st.video(videourl4)
    
# STEP 5
    
with st.expander(":blue[**Step 5: Postprocessing**] - Expand to see the instructions"):
    st.markdown("""
            #### STEP 5: Postprocessing
            In the fifth and final step we perform the postprocessing of the model computation.
            
            #### Check Model Run
           """)
           
    to_do(
        [(st.write, "Once MODELMONITOR is closed, the listing file is opened; check budget in output listing (it’s located near the end of the file – check closure of water balance and if the budget terms are reasonable).")],"td031",)

    to_do(
        [(st.write, "close output listing and the black “command prompt” window.")],"td032",)
        
    st.markdown(""" 
            #### Plot Heads
           """) 
           
    to_do(
        [(st.write, "select “Import and display model results” (colored symbol below “Data”).")],"td033",)
        
    to_do(
        [(st.write, "select model file *.fhd.")],"td034",)
        
    to_do(
        [(st.write, "select “Contour grid” and press “OK”.")],"td035",)
        
    to_do(
        [(st.write, "select “Update the existing data sets with new values” (not needed in very first try).")],"td036",)
        
    to_do(
        [(st.write, "check hydraulic head isolines.")],"td037",)  
        
    st.markdown(""" 
            #### Prepare Particle Tracking
           """)         
           
    to_do(
        [(st.write, "select “Model” / “MODFLOW Output Control” / “Head”, set external file type = binary, and press “OK”.")],"td038",)
        
    to_do(
        [(st.write, "select “Model” / “MODFLOW Packages and Programs” in the menu bar, then go to “Post processors” / “MODPATH”.")],"td039",)
        
    to_do(
        [(st.write, "set: MODPATH version 7; “Output mode” = Pathlines & time series, “Reference time for simulation” = 0, “Tracking direction” = backward, and press “OK”.")],"td040",)
        
    to_do(
        [(st.write, "go to submenu “Version 6 & 7 options and set End of particle tracking (StopOption) stop at termination points.")],"td041",)
        
    to_do(
        [(st.write, "go to submenu “Output times” and set Method of specifying times to “Specified times; set “Number of times” to 4 and define suitable times (time unit is seconds) like 864000, 2592000, 4320000, 8640000 (10, 30, 50, and 100 days).")],"td042",)      
        
    st.markdown(""" 
            #### Carry Out Particle Tracking Using MODPATH
           """)        
           
    to_do(
        [(st.write, "zoom in near well locations, select “Select objects” (the red cursor), and double-click on point object “well1”."
        ,"\n - select “MODFLOW Features” / “MODPATH”"
        ,"\n - select “initial particle placement” and “cylinder”"
        ,"\n - set number of particles around cylinder = 20 and press “OK”")],"td043",)
        
    to_do(
        [(st.write, "double click on point object “well2”."
        ,"\n - select “MODFLOW Features” / “MODPATH”"
        ,"\n - select “initial particle placement” and “cylinder”"
        ,"\n - set number of particles around cylinder = 20 and press “OK”")],"td044",)
        
    to_do(
        [(st.write, "select “File” / “Save” (no model archive needs to be created).")],"td045",)
        
    to_do(
        [(st.write, "select “Run MODFLOW-2005” by clicking on the green triangle below “Grid” (only necessary for the first run to generate the necessary binary head file).")],"td046",)
        
    to_do(
        [(st.write, "select “Run MODFLOW-2005” by clicking on the black triangle below “Grid” and select “Export MODPATH Input Files”.")],"td047",) 
        
    to_do(
        [(st.write, "confirm the file name to save MODPATH input files (*.mpn) and run MODPATH.")],"td048",)
        
    to_do(
        [(st.write, "check and close output listing, close the black command prompt window.")],"td049",)
        
    to_do(
        [(st.write, "select “Data visualization” (colored symbol to the right of the middle in the second row of symbols)."
        ,"\n - select “MODPATH Pathlines” / “Basic”"
        ,"\n - set “MODPATH pathline file” = *.pth"
        ,"\n - select “Options”"
        ,"\n - set Color by = “None”, press “Apply”, and press “Close”")],"td050",)
        
    to_do(
        [(st.write, "check pathlines.")],"td051",)
        
    to_do(
        [(st.write, "select “File” / “Save” (no model archive needs to be created), change porosity according to step a), and repeat steps f) – k).")],"td052",) 
        
    st.markdown("""
            (Please note that another MODFLOW run needs to be carried out before MODPATH is started if other parameters, which affect the flow behavior, were changed.)
           """) 
        
    st.video(videourl5)
    
# OPTIONALLY STEPS
    
with st.expander(":blue[**OPTIONALLY Steps: Some further things to do**] - Expand to see the instructions"):
    st.markdown("""
            #### Optionally STEPs: Some further things To Do
            You can do further optional steps with the finished model.
            
            #### Optionally Refine Grid
           """)
    to_do(
        [(st.write, "learn about buttons “Delete grid lines”, “Drag grid lines”, “Add vertical grid line”, “Add horizontal grid line” and “Subdivide grid cells” (left group in second row of symbols).")],"td053",)
    to_do(
        [(st.write, "zoom in near well locations, select “Subdivide grid cells”, mark both cells containing a well, set “subdivide each column into” = 2, “subdivide each row into” = 2, and press “OK” (Note: The “layers” section has to remain unchanged!).")],"td054",)
    to_do(
        [(st.write, "repeat the previous step several times to split a subsequently increasing number of columns and rows.")],"td055",)
    to_do(
        [(st.write, "zoom in near well 1, select “Delete grid lines” and click on the intersection of grid lines at the well location.")],"td056",)
    to_do(
        [(st.write, "select “Subdivide grid cells”, mark the cell containing well 1, set “subdivide each column into” = 3, “subdivide each row into” = 3, and press “OK”.")],"td057",)
    to_do(
        [(st.write, "zoom in near well 2, select “Delete grid lines” and click on the gridline passing through the well location.")],"td058",)
    to_do(
        [(st.write, "select “Subdivide grid cells”, mark the cell containing well 2, set “subdivide each row into” = 3, and press “OK”.")],"td059",)
    to_do(
        [(st.write, "choose “Restore default 2D view” and learn about buttons to hide/show the 2D gridlines (on the very right in the second row of symbols).")],"td060",)        
        
st.markdown('---')

# --- Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')