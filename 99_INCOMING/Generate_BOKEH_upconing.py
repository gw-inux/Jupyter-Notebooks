import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, Slider, CustomJS, Select
from bokeh.layouts import column, row

# 📌 Define the Upconing Function
def upconing(x, Q, K, d_pre, rho_f, rho_s, n):
    t = np.inf
    z = (1/(x**2/d_pre**2+1)**0.5 - 1/(x**2/d_pre**2 + (1 + ((rho_s - rho_f)/rho_f) * K * t / (n * d_pre * (2 + (rho_s - rho_f)/rho_f)))**2)**0.5) * \
        Q / (2 * np.pi * d_pre * K * ((rho_s - rho_f)/rho_f))
    return z

# 📌 Create the Output HTML File
output_file("bokeh_upconing_multi_interactive.html")

# 📌 Define Initial Values
x = np.linspace(-1000, 1000, 300)
data_sets = {
    "Scenario 1": {"Q": 100, "K": 50, "d_pre": 10, "rho_f": 1000, "rho_s": 1025, "n": 0.15},
    "Scenario 2": {"Q": 200, "K": 30, "d_pre": 15, "rho_f": 1000, "rho_s": 1030, "n": 0.2},
    "Scenario 3": {"Q": 150, "K": 40, "d_pre": 12, "rho_f": 1000, "rho_s": 1018, "n": 0.12}
}

# 📌 Compute Initial Concentrations
z_init = {key: upconing(x, **values) for key, values in data_sets.items()}

# 📌 Store Data in ColumnDataSource for Updates
sources = {key: ColumnDataSource(data=dict(x=x, z=z_init[key])) for key in data_sets.keys()}

# 📌 Create the Bokeh Figure
p = figure(title="Upconing of the Saltwater Interface",
           x_axis_label="Distance from Well (m)",
           y_axis_label="Height above initial water table (m)",
           width=800, height=500)

colors = ["blue", "green", "red"]

# 📌 Plot each dataset
lines = {}
for (name, source), color in zip(sources.items(), colors):
    lines[name] = p.line('x', 'z', source=source, line_width=2.5, color=color, legend_label=name)

# 📌 Sliders for User Inputs
sliders = {
    "Q": Slider(start=0, end=5000, value=100, step=10, title="Freshwater Discharge (Q) in m³/d"),
    "K": Slider(start=1, end=100, value=50, step=1, title="Hydraulic Conductivity (K) in m/d"),
    "d_pre": Slider(start=0.5, end=100, value=10, step=0.1, title="Pre-pumping Distance (d_pre) in m"),
    "rho_f": Slider(start=950, end=1050, value=1000, step=1, title="Freshwater Density (ρ_f) in kg/m³"),
    "rho_s": Slider(start=950, end=1050, value=1025, step=1, title="Saltwater Density (ρ_s) in kg/m³"),
    "n": Slider(start=0.05, end=0.4, value=0.15, step=0.01, title="Porosity (n)")
}

# 📌 Dropdown menu for selecting dataset
dataset_select = Select(title="Choose Scenario", value="Scenario 1", options=list(data_sets.keys()))

# 📌 JavaScript Callback for Interactivity
callback_code = """
    var dataset = dataset_select.value;
    var x = sources[dataset].data['x'];
    var z = sources[dataset].data['z'];
    
    var Q = Q_slider.value;
    var K = K_slider.value;
    var d_pre = d_pre_slider.value;
    var rho_f = rho_f_slider.value;
    var rho_s = rho_s_slider.value;
    var n = n_slider.value;
    
    var pi = Math.PI;
    var t = Infinity;
    var density_ratio = (rho_s - rho_f) / rho_f;
    
    for (var i = 0; i < x.length; i++) {
        var x_val = x[i];
        var term1 = 1 / Math.sqrt((x_val*x_val)/(d_pre*d_pre) + 1);
        var term2 = 1 / Math.sqrt((x_val*x_val)/(d_pre*d_pre) + Math.pow(1 + (density_ratio * K * t) / (n * d_pre * (2 + density_ratio)), 2));
        z[i] = (term1 - term2) * (Q / (2 * pi * d_pre * K * density_ratio));
    }

    sources[dataset].change.emit();
"""

callback = CustomJS(args={**{f"{k}_slider": v for k, v in sliders.items()},
                          "dataset_select": dataset_select,
                          "sources": sources}, code=callback_code)

# 📌 Link Sliders to Callback
for slider in sliders.values():
    slider.js_on_change("value", callback)

dataset_select.js_on_change("value", callback)

# 📌 Layout Configuration
layout = column(dataset_select, row(*sliders.values()), p)

# 📌 Save as Standalone HTML
save(layout)

print("✅ Interactive Multi-Scenario Bokeh HTML saved as 'bokeh_upconing_multi_interactive.html'")
