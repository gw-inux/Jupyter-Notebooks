from bokeh.plotting import figure, output_file, save
from bokeh.models import Slider, ColumnDataSource, CustomJS, Legend, LegendItem
from bokeh.layouts import column, row
import numpy as np

# Define function (EXACTLY like Matplotlib & Plotly)
def f(x, a=1):
    return a * np.sin(x)

# Generate initial data
x = np.linspace(-5, 5, 200)  # ✅ Start from -5 to 5
y = f(x)

# Create Bokeh ColumnDataSource
source = ColumnDataSource(data={'x': x, 'y': y})

# ✅ Create figure with PERFECT Matplotlib & Streamlit styling
p = figure(title="Interactive Function Plot", width=700, height=450)

# ✅ Match Matplotlib color & line style
line = p.line('x', 'y', source=source, line_width=2, color="#1f77b4")

# ✅ Fix y-axis range to match Matplotlib
p.y_range.start = -5
p.y_range.end = 5

# ✅ Match Matplotlib axis ticks (exact number)
p.xaxis.ticker.desired_num_ticks = 7
p.yaxis.ticker.desired_num_ticks = 7

# ✅ Match Matplotlib grid style (gray, dashed)
p.xgrid.grid_line_color = "gray"
p.ygrid.grid_line_color = "gray"
p.xgrid.grid_line_dash = [4, 4]
p.ygrid.grid_line_dash = [4, 4]
p.xgrid.grid_line_alpha = 0.6
p.ygrid.grid_line_alpha = 0.6

# ✅ Set fonts & sizes to match Matplotlib/Streamlit
p.title.text_font_size = "16pt"
p.xaxis.axis_label = "x"
p.yaxis.axis_label = "y"
p.xaxis.axis_label_text_font_size = "14pt"
p.yaxis.axis_label_text_font_size = "14pt"
p.xaxis.major_label_text_font_size = "12pt"
p.yaxis.major_label_text_font_size = "12pt"

# ✅ Fix legend (EXACT Matplotlib style)
legend = Legend(items=[LegendItem(label="f(x) = a * sin(x)", renderers=[line])])
legend.label_text_font_size = "12pt"
legend.border_line_width = 1
legend.border_line_color = "black"
legend.background_fill_alpha = 0.6
p.add_layout(legend, "top_right")

# ✅ Streamlit-style Sliders (Red line, rounded **dot** handle)
slider_a = Slider(start=0.1, end=5, value=1, step=0.1, title="Amplitude (a)", bar_color="red")
slider_xmin = Slider(start=-10, end=0, value=-5, step=0.1, title="Min x", bar_color="red")
slider_xmax = Slider(start=5, end=15, value=5, step=0.1, title="Max x", bar_color="red")

# **✅ JavaScript callback for interactivity**
callback = CustomJS(args=dict(source=source, slider_a=slider_a, slider_xmin=slider_xmin, slider_xmax=slider_xmax), code="""
    var data = source.data;
    var a = slider_a.value;
    var xmin = slider_xmin.value;
    var xmax = slider_xmax.value;
    
    var x = [];
    var y = [];
    var step = (xmax - xmin) / 200;
    
    for (var i = 0; i <= 200; i++) {
        var val = xmin + i * step;
        x.push(val);
        y.push(a * Math.sin(val));
    }
    
    data['x'] = x;
    data['y'] = y;
    source.change.emit();
""")

# Link sliders to callback
slider_a.js_on_change('value', callback)
slider_xmin.js_on_change('value', callback)
slider_xmax.js_on_change('value', callback)

# ✅ Save as standalone HTML
output_file("bokeh_streamlit_perfect.html")
layout = column(slider_a, row(slider_xmin, slider_xmax), p)  # ✅ Sliders above the plot
save(layout)

print("🚀 Bokeh standalone HTML file generated: bokeh_streamlit_perfect.html")
