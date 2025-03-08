import streamlit as st
import streamlit.components.v1 as components
import os
import math
import numpy as np
import matplotlib.pyplot as plt

# Define path to the Bokeh HTML file inside the "DATA" folder
html_file_path = os.path.join("99_INCOMING/DATA/Theis_Testing.html")

st.title("Bokeh HTML in Streamlit")

st.markdown("""
            This app is just a short demonstrator about options to implement Bokeh plots in Streamlit apps. 
            
            The options used here require the Bokeh plot as HTML file.
"""
)
st.subheader('First way of implementation: Choose the type of plot')

st.markdown("""
            With this option a user can choose which type of plot is shown. This could be useful for plots that are not intended to be modified by users
"""
)

# This are two example functions that generate an interactive plot
def some_streamlit_content(v):
    columns = st.columns((1,1), gap = 'large')
    with columns[0]:
        tr    = st.slider('residual water content (-)', 0.01, 0.4, 0.05, 0.01, key = 10+v)
        ts    = st.slider('saturated water content (-)', 0.15, 0.7, 0.30, 0.01, key = 20+v)   
    with columns[1]:
        alpha = st.slider('alpha (1/cm)', 0.01, 1., 0.1, 0.01, key = 30+v)
        n     = st.slider('n (-)', 1.01, 3., 1.2, 0.01, key = 40+v)
      
    plot4 = st.toggle('Plot k_r 1', key = 50+v)
    
    
    x_max = 300
        
    # intermediate results 
    m   = 1-1/n                                         # van Genuchten parameter
    PWP = tr + (ts - tr)/(1+(alpha*10**4.2)**n)**m      # permanent wilting point
    FC  = tr + (ts - tr)/(1+(alpha*10**1.8)**n)**m      # field capacity
    eFC = FC - PWP                                      # effective field capacity
    
    # model output
    t_plot  = []                                        # t  = theta = moisture content
    p_plot  = []                                        # p  = phi   = suction head
    kr_plot = []                                        # kr = rel. permeability
        
    for x in range (0, x_max):
        t = tr + (ts-tr)*x/(x_max-1)                    # [-] moisture content; please note that range counts up to x_max-1
        te = (t-tr)/(ts-tr)                             # [-] effective saturation      
        if x == 0:
            p     = 1E18                                # [cm] suction head
            kr    = 0                                   # [-] relative hydraulic conductivity
        else: 
            p     = ((te**(-1/m)-1)**(1/n))/alpha                      
            kr    = np.sqrt(te)*(1-(1-te**(1/m))**m)**2
        t_plot.append(t)
        p_plot.append(p)
        kr_plot.append(kr)
            
    fig = plt.figure(figsize=(9,6))
    ax  = fig.add_subplot()
    ax.plot(t_plot, p_plot, 'r', markersize=3)
    ax.vlines(x= tr, ymin=1e-1, ymax=1e+5, linestyle='--')      
    ax.hlines(y= 10**4.2, xmin=0, xmax=PWP, colors='g')    #upper green line
    ax.vlines(x= PWP, ymin=1e-1, ymax=10**4.2, colors='g')
    ax.hlines(y= 10**1.8, xmin=0, xmax=FC, colors='b')     #bottom green line
    ax.vlines(x= FC, ymin=1e-1, ymax=10**1.8, colors='b')
    ax.set(xlabel='water content [-]', ylabel ='suction head [cm]', xlim = [0, 0.7], ylim = [1e-1,1e+5], yscale = 'log' )
    ax.grid(which="both", color='grey',linewidth=0.5)
    st.pyplot(fig)
    
    if plot4 == 1:
        fig = plt.figure(figsize=(6,4))
        ax  = fig.add_subplot()
        ax.plot(t_plot, kr_plot, 'b', markersize = 3)
        ax.set(xlabel='water content [-]', ylabel='rel hydraulic conductivity [cm/d]', xlim = [0, 0.7], ylim = [0,1] )
        ax.grid(which="major", color='grey',linewidth=0.5)
        st.pyplot(fig)
        
    st.write('Van Genuchten             m:', '{:.5f}'.format(m) )
    st.write('Permanent Wilting Point PWP:', '{:.2f}'.format(PWP) )
    st.write('Field Capacity           FC:', '{:.2f}'.format(FC) )
    st.write('Eff. Field Capacity     eFC:', '{:.2f}'.format(eFC) )

def some_bokeh_content():
    # Read the HTML content
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            bokeh_html = f.read()
        
        # Wrap the HTML in a responsive div with dynamic height
        responsive_html = f"""
        <div style="width:100%; max-width:100%; overflow:hidden; display:flex; justify-content:center;">
            <div id="bokeh-container" style="width:100%; transform: scale(0.9); transform-origin: top left;">
                {bokeh_html}
            </div>
        </div>
        <script>
            function adjustHeight() {{
                let content = document.getElementById("bokeh-container");
                if (content) {{
                    let height = content.scrollHeight + "px";
                    window.parent.document.querySelector('iframe').style.height = height;
                }}
            }}
            window.onload = adjustHeight;
            window.onresize = adjustHeight;
        </script>
        """
    
        # Display Bokeh app inside Streamlit with full width & auto height
        components.html(responsive_html, height=1000)  # Set an initial height that adjusts dynamically
    
    
    except FileNotFoundError:
        st.error(f"File not found: {html_file_path}")

# Let the user decide what plot should be shown

bokeh = False
bokeh = st.toggle(':green[**Click here**] if you want to see the :rainbow[**Bokeh plot**] (_this may take a few seconds_)')

if bokeh:
    some_bokeh_content()    
else:
    some_streamlit_content(1)
    
st.subheader('Second way of implementation: Provide the Bokeh/Streamlit-Matplotlib as optional visualization')

st.markdown("""
            With this option a user can add one plot. This could be useful if there are many users (large audiences in classroom setting) or if the network connection is slow and Streamlit-Matplotlib works with a significant time lag.
"""
)

some_streamlit_content(2)
with st.expander(':green[**Click here**] if you additionally want to see the :rainbow[**Bokeh plot**] (_this may take a few seconds_)'):
    some_bokeh_content()