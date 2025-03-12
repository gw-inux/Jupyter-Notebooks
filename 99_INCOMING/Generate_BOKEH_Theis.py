import numpy as np
import scipy.special
from scipy.interpolate import interp1d
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, Slider, CustomJS
from bokeh.layouts import column, row

# 📌 Precomputed Lookup Table for Theis Well Function W(u)
u_values = np.logspace(-15, 3, 2000)  # Ensuring proper range
w_values = scipy.special.exp1(u_values)  # Compute W(u) using scipy

# Interpolation function for W(u)
well_function_interp = interp1d(u_values, w_values, kind="linear", fill_value="extrapolate")

# 📌 Define the Theis Function
def theis_curve(T, S, r, t, Q):
    u = (r**2 * S) / (4 * T * t)
    w_u = well_function_interp(u)  # Use interpolated lookup table
    return (Q / (4 * np.pi * T)) * w_u

# 📌 Create the Output HTML File
output_file("bokeh_theis_interactive.html")

# 📌 Define Initial Values
t = np.logspace(-1, 5, 100)  # Time range (log scale, 0.1s to 100,000s)
Q_init, T_init, S_init, r_init = 0.3 / 60, 1e-3, 1e-4, 120  # Initial values

# 📌 Compute Initial Theis Curve
s_init = theis_curve(T_init, S_init, r_init, t, Q_init)

# 📌 Measured Data (Ideal case for parameter estimation)
measured_t = np.array([1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 14, 18, 24, 30, 40, 50, 60, 100, 120]) * 60  # Convert min to sec
measured_s = np.array([0.66, 0.87, 0.99, 1.11, 1.21, 1.36, 1.49, 1.59, 1.75, 1.86, 1.97, 2.08, 2.20, 2.36, 2.49, 2.65, 2.78, 2.88, 3.16, 3.28])

# 📌 Store Data in ColumnDataSource for Updates
source = ColumnDataSource(data=dict(t=t, s=s_init))
measured_source = ColumnDataSource(data=dict(t=measured_t, s=measured_s))

# 📌 Create the Bokeh Figure
p = figure(title="Theis Solution - Parameter Estimation",
           x_axis_label="Time (s)",
           y_axis_label="Drawdown (m)",
           x_axis_type="log",
           y_axis_type="log",
           width=800,
           height=500)

p.line('t', 's', source=source, line_width=2, color="blue", legend_label="Theis Drawdown")
p.circle('t', 's', source=measured_source, size=6, color="red", legend_label="Measured Data")  # ✅ Add measured data

# 📌 Fix Axis Limits to Match Streamlit
p.y_range.start = 1e-4
p.y_range.end = 1e1
p.x_range.start = 1e-1
p.x_range.end = 1e5

# Convert lookup table into JavaScript-friendly lists
u_values_js = "[" + ",".join([f"{val:.5e}" for val in u_values]) + "]"
w_values_js = "[" + ",".join([f"{val:.5e}" for val in w_values]) + "]"

# 📌 Sliders (logarithmic values for T and S)
sliders = {
    "T": Slider(start=-7, end=0, value=np.log10(T_init), step=0.01, title="log(T) (m²/s)"),
    "S": Slider(start=-7, end=0, value=np.log10(S_init), step=0.01, title="log(S)"),
}

# 📌 JavaScript Callback for Interactivity (Uses Lookup Table)
callback_code = """
    function interpolate(x, xArray, yArray) {
        // Linear interpolation function for lookup table
        if (x <= xArray[0]) return yArray[0];
        if (x >= xArray[xArray.length - 1]) return yArray[yArray.length - 1];

        let i = 0;
        while (xArray[i] < x) i++;
        
        let x1 = xArray[i - 1], x2 = xArray[i];
        let y1 = yArray[i - 1], y2 = yArray[i];

        return y1 + ((y2 - y1) / (x2 - x1)) * (x - x1);
    }

    // Precomputed lookup table from Python
    var u_values = %s;
    var well_values = %s;

    var Q = %f;
    var r = %f;
    var t = source.data['t'];  // Get time values

    var T_val = Math.pow(10, T_slider.value);  // Convert log(T) back
    var S_val = Math.pow(10, S_slider.value);  // Convert log(S) back
    var s = [];

    for (var i = 0; i < t.length; i++) {
        var u = (r * r * S_val) / (4 * T_val * t[i]);
        var w_u = interpolate(u, u_values, well_values);
        s.push((Q / (4 * Math.PI * T_val)) * w_u);
    }

    source.data['s'] = s;
    source.change.emit();
""" % (u_values_js, w_values_js, Q_init, r_init)  # ✅ Fix f-string issue

callback = CustomJS(args={**{f"{k}_slider": v for k, v in sliders.items()}, "source": source}, code=callback_code)

# 📌 Link Sliders to Callback
for slider in sliders.values():
    slider.js_on_change("value", callback)

# 📌 Layout Configuration
layout = column(row(*sliders.values()), p)

# 📌 Save as Standalone HTML
save(layout)

print("✅ Interactive Bokeh HTML saved as 'bokeh_theis_interactive.html'")
