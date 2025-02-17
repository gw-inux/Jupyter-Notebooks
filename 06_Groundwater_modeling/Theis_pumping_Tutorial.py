# Loading the required Python libraries
import streamlit as st
from streamlit_extras.stodo import to_do

st.title('Tutorial: Numerical model of a pumping test')

st.subheader('Running a pumping test :orange[in a confined aquifer to compare with the Theis solution]', divider="orange")

st.markdown("""
            This app contains a tutorial with descriptions (as To-Do list) and videos on how to setup a MODFLOW model for pumping from a confined aquifer (see the following figure). The model generates data that are subsequently further processed by the PumpingTest app (https://gwp-pumping-test-analysis.streamlit.app/). The individual steps of the modeling process are provided in the following boxes that you can expand by clicking.
            
            The model (Confined_pumping.gpt) and the generated data (confined_pumping.csv) are available in GitHub (https://github.com/gw-inux/Jupyter-Notebooks/tree/main/90_Streamlit_apps/SYMPLE25/DATA)
           """)

lc0, cc0, rc0 = st.columns((20,60,20))
with cc0:
    st.image('06_Groundwater_modeling/FIGS/confined_aquifer_model.png', caption="The numerical model (extent is 2,000 x 2,000 x 20 m³) with the central abstraction well to simulate pumping from a confined aquifer. The colors indicate the drawdown after one day of pumping.")

# This are the links to the tutorial videos
videourl1 = 'https://youtu.be/0eS7sscSyVs'
videourl2 = 'https://youtu.be/SUkPsbF7J7s'
videourl3 = 'https://youtu.be/S6C3hZxmT4Q'
videourl4 = 'https://youtu.be/vPoDFphkR4o'
videourl5 = 'https://youtu.be/1s6yglVVDoI'
videourl6 = 'https://youtu.be/RuIMmfGMbWA'
videourl7 = 'https://youtu.be/Jn1hzE2gEG4'

# Create ToDos to proceed with the steps of the exercise

with st.expander(":blue[**Step 1: Discretization in space and time**] - Expand to see the instructions"):
    st.markdown("""
            **STEP 1: Discretization in space and time**
            This is the initial step of the model design. We start with the MODELMUSE initial screen. There you can define the specific numerical model and the initial discretization in space. Afterwards, in the MODFLOW main window, you can define the discretization of time.
           """)
    to_do(
        [(st.write, "Choose MODFLOW-2005 as numerical model.")],"td01",)
    to_do(
        [(st.write, "Define the spatial grid dimension.")],"td02",)
    to_do(
        [(st.write, "Define the discretization of time with two transient stress periods, each for 86,400 seconds.")], "td03",)
    st.video(videourl1)
        
with st.expander(":blue[**Step 2: Define structure and parameters**] - Expand to see the instructions"):
    st.markdown("""
            **STEP 2: Define structure and parameters**
            In the second step we define the structure (which is simply the idealized aquifer block) and the hydrogeologic parameters.
           """)
    to_do(
        [(st.write, "Go to 'Data/Edit Data Set' to check the hydraulic conductivity and modify the storativity.")],"td04",)
    to_do(
        [(st.write, "Go to 'Data/Edit Data Set' to define the initial head as 18 m (and therefore 18 m above the aquifer top, which is the top of layer 1).")], "td05",)
    to_do(
        [(st.write, "Go to 'Model/MODFLOW Layer Groups to check that the layer is 'confined'.")], "td06",)
    st.video(videourl2)
        
with st.expander(":blue[**Step 3: Boundary conditions**] - Expand to see the instructions"):
    st.markdown("""
            **STEP 3: Boundary conditions**
            The highly idealized model runs in transient state. Beginning from an initial situation, the abstraction well pumps water for 86,400 seconds with a rate of 0.01 m³/s. Additionally, we add two defined head boundary conditions at the left and right part of the model - those are not required for the current model task. However, possible water flow over these bounary conditions is documented in the listing file and helps to identify the possible interaction of the pumping well with the models boundaries.    
           """)
    to_do(
        [(st.write, "Go to 'MODFLOW/Packages and Programs' and activate the well boundary. Place one point object in the middle of model and define the time and rate of pumping.")],"td07",)
    to_do(
        [(st.write, "Go to 'MODFLOW/Packages and Programs' and activate the CHD boundary (Defined head boundary). Use a line object on the left and right side of the model. Define the head as 18 m (both, starting and ending head).")], "td08",)
    st.video(videourl3)
        
with st.expander(":blue[**Step 4: Properties and Simulation**] - Expand to see the instructions"):
    st.markdown("""
            **Step 4: Properties and Simulation**
            Once the inital model design is finish, we can define the numerical settings and run the simulation. For the idealized numerical model, we can rely on the presettings of the numerical solver.            
           """)
    to_do(
        [(st.write, "Go to 'MODEL / MODFLOW Program locations' and eventually choose the ..._dbl_... version of the code (= compiled with double precision; not mandatory but this improves the numerical stability) .")],"td09",)
    to_do(
        [(st.write, "Use the green triangle to run the simulation.")], "td10",)
    st.video(videourl4)
        
with st.expander(":blue[**Step 5a: Postprocessing - Visualizing hydraulic heads**] - Expand to see the instructions"):
    st.markdown("""
            **STEP 5a: Postprocessing - Visualizing hydraulic heads**
            After the successful model run we visualize the computed heads with MODELMUSE and the 3D Model Viewer.
           """)
    to_do(
        [(st.write, "Import the model results and visualize the computed hydraulic heads.")],"td11",)
    to_do(
        [(st.write, "Use the 3D ModelViewer to see a 3D representation of the model together with an animation (not mandatory GW_Chart to access and plot the results in 50 distance of the pumping well.")], "td12",)
    st.video(videourl5)
        
with st.expander(":blue[**Step 5b: Postprocessing with GW_Chart**] - Expand to see the instructions"):
    st.markdown("""
            **STEP 5b: Postprocessing with GW_Chart**
            
           """)
    to_do(
        [(st.write, "Use GW_Chart to access and plot the results in 50 distance of the pumping well.")], "td13",)
    st.video(videourl6)    
with st.expander(":blue[**Step 5c: Export model data**], **processing model data, and importing in the** :red[**Pumping Test App**] - Expand to see the instructions"):
    st.markdown("""
            **STEP 5c: Export model data, process model data, and importing in the PumpingTest App (https://gwp-pumping-test-analysis.streamlit.app/)**
            
           """)
    to_do(
        [(st.write, "Copy the data from GW_Chart to a spreadsheet calculation like Excel.")],"td14",)
    to_do(
        [(st.write, "Modify the time that was given as seconds in MODFLOW to minutes as required by the PumpingTest App.")],"td15",)
    to_do(
        [(st.write, "Copy the data to an text editor. Replace the _TAB_ (space between the numbers) by a comma and save the file with the ending *.csv.")], "td16",)
    to_do(
        [(st.write, "Open the data in the PumpingTest App (https://gwp-pumping-test-analysis.streamlit.app/) and adapt the parameters pumping rate (0.01 m³/s) and distance of the observation to the pumping well (50 m). Then do the parameter fitting - the results in the app should reflect your model parameters (storativity and transmissivity = hydr. conductivity x thickness of the aquifer).")], "td17",)
    st.video(videourl7)
    
st.subheader('Possible next steps for your own investigation', divider = 'blue')
    
st.markdown("""
            So far, the model reflect the idealized conditions that are required for the Theis solution. In the next steps, you can modify the numerical model in order to investigate the effect on the 'measured' data (i.e., the data that your MODFLOW model produces) in comparison to the Theis solution. Possible modifications can be:
            - adding anisotropy (Kx is different from Ky),
            - increasing the pumping time so that the cone of drawdown reaches the boundary,
            - adding layers with different hydrogeologic parameters to your model,
            - adding heterogeneity to the hydrogeologic parameters,
            - make your model unconfined (lowering the CHD heads and the initial head to a value less then the aquifer top, which is 0),
            - (...)
           """)