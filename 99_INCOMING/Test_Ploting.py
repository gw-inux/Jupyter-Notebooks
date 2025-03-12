import streamlit as st
import numpy as np
import streamlit.components.v1 as components
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, Range1d
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
x_min = st.slider("Minimum x", -10, 0, -5)
x_max = st.slider("Maximum x", 1, 10, 5)
a = st.slider("Parameter a", 0.1, 5.0, 1.0)

# ✅ Compute function
x = np.linspace(x_min, x_max, 200)
y = a * np.sin(x)

# ✅ Fixed y-axis limits
y_min, y_max = -5, 5  # Adjust based on expected range

st.subheader('Bokeh')

with st.expander('Show BOKEH as :rainbow[HTML] in Streamlit'):
    some_bokeh_content()

with st.expander('Show BOKEH in Streamlit'):
    # ✅ Use ColumnDataSource for efficient updates
    source = ColumnDataSource(data=dict(x=x, y=y))
    
    # ✅ Create Bokeh figure
    p = figure(
        title="Bokeh Interactive Plot",
        x_axis_label="x",
        y_axis_label="f(x)",
        width=700,
        height=500,
        background_fill_color="white",
        border_fill_color="white",
    )
    
    # ✅ Matplotlib-like line styling
    p.line('x', 'y', source=source, line_width=2, color="blue", legend_label=f"f(x) = {a} * sin(x)")
    
    # ✅ Set grid, axes, and range like Matplotlib
    p.y_range = Range1d(y_min, y_max)  # Fixed y-axis
    p.xgrid.grid_line_color = "lightgray"
    p.ygrid.grid_line_color = "lightgray"
    p.outline_line_color = None  # Removes frame for cleaner look
    p.legend.label_text_font_size = "12pt"
    
    # ✅ Display Bokeh figure in Streamlit
    st.bokeh_chart(p)

st.subheader(' Show PLOTLY')

with st.expander('Show PLOTLY'):
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

st.subheader('Show Matplotlib')

with st.expander('Show MATPLOTLIB'):
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