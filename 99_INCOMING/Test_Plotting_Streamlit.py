import streamlit as st
import numpy as np
import streamlit.components.v1 as components
from bokeh.plotting import figure
from streamlit_bokeh import streamlit_bokeh
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64

# Define path to the Bokeh HTML file inside the "DATA" folder
html_file_path = os.path.join("99_INCOMING/DATA/bokeh_interactive.html")

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



st.title("Interactive Function Plot (Plotly)")

# ✅ Define sliders

columns = st.columns((1,1))
with columns[0]:
    x_min = st.slider("Minimum x", -10, 0, -5)
with columns[1]:
    x_max = st.slider("Maximum x", 1, 10, 5)
a = st.slider("Parameter a", 0.1, 5.0, 1.0)

# ✅ Compute function
x = np.linspace(x_min, x_max, 200)
y = a * np.sin(x)

# ✅ Fixed y-axis limits
y_min, y_max = -5, 5  # Adjust based on expected range

st.subheader('Show :violet[PLOTLY]')

with st.expander(':red[**Show/Collapse**] the PLOTLY plot]'):
    # ✅ Plotly interactive figure
    fig = go.Figure()
    
    # ✅ Matplotlib-style line properties
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name=f"f(x) = {a} * sin(x)",
        line=dict(
            color="blue",   # Matplotlib's default blue
            width=2,        # Thicker lines
            dash="solid"    # Solid line style
        )
    ))
    
    # ✅ Update layout to resemble Matplotlib
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="f(x)",
        xaxis=dict(showgrid=True, zeroline=True, gridcolor="lightgray"),  # Light grid lines
        yaxis=dict(showgrid=True, zeroline=True, range=[y_min, y_max], gridcolor="lightgray"),  # Fixed y-axis
        template="simple_white",  # Matplotlib-like clean background
        font=dict(size=14),  # Font similar to Matplotlib default
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins
        showlegend=True,
        legend=dict(x=0.7, y=0.95)
    )
    
    st.plotly_chart(fig)

st.subheader('Show :blue[Matplotlib]')

with st.expander(':red[**Show/Collapse**] the MATPLOTLIB plot'):
    # ✅ Efficient plotting
    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"f(x) = {a} * sin(x)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.set_ylim(y_min, y_max)  # ✅ Fixed y-axis
    ax.grid(True)
    
    # ✅ Display figure
    st.pyplot(fig)
    
st.subheader('Show :green[Streamlit-Bokeh]')
with st.expander(':red[**Show/Collapse**] the Streamlit-Bokeh plot'):

    # Generate data
    x = np.linspace(-5, 5, 100)
    y = a * np.sin(x)
    
    # Create Bokeh figure
    p = figure(title="Sine Function", x_axis_label="x", y_axis_label="f(x)", x_range=(x_min, x_max), y_range=(-5, 5), width=600, height=400)
    p.grid.grid_line_alpha = 0.3
    p.line(x, y, legend_label="f(x) = 1.0 * sin(x)", line_width=2)
    
    # Display in Streamlit
    streamlit_bokeh(p, use_container_width=True, key="plot1")
    

st.subheader('Show :rainbow[BOKEH interactive html]')

with st.expander(':red[**Show/Collapse**] BOKEH as :rainbow[HTML] in Streamlit'):
    some_bokeh_content()