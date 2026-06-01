import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import scipy.special
import scipy.optimize


# --------------------------------------------------
# Streamlit page
# --------------------------------------------------
st.set_page_config(page_title="Neuman type curve checker")

st.title("Neuman type curve checker")

st.markdown(
    """
This small app is intended to check and visualize the implemented Neuman type-curve tables.
It plots the tabulated functions \(W(u_A, \\beta)\) and \(W(u_B, \\beta)\) for selected beta values.

For comparison with classical Neuman type-curve plots, the type-B curves can be shifted
onto a common time axis using the storage ratio \(S_y/S_a\).
"""
)


# --------------------------------------------------
# Current implemented beta subset
# --------------------------------------------------
beta_values = np.array([0.001, 0.01, 0.06, 0.2, 0.6, 1.0, 2.0, 4.0, 6.0])
beta_labels = [f"{b:g}" for b in beta_values]


# --------------------------------------------------
# Reduced W(u_A, beta) table
# --------------------------------------------------
u_inv_a = np.array([
    4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00, 4.00E+00,
    8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01, 8.00E+01,
    1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02, 1.40E+03,
    2.40E+03, 4.00E+03, 8.00E+03
])

w_u_a = np.array([
    [2.48E-02, 2.41E-02, 2.30E-02, 2.14E-02, 1.88E-02, 1.70E-02, 1.38E-02, 1.00E-02, 1.00E-02],
    [1.45E-01, 1.40E-01, 1.31E-01, 1.19E-01, 9.88E-02, 8.49E-02, 6.03E-02, 3.17E-02, 1.74E-02],
    [3.58E-01, 3.45E-01, 3.18E-01, 2.79E-01, 2.17E-01, 1.75E-01, 1.07E-01, 4.45E-02, 2.10E-02],
    [6.62E-01, 6.33E-01, 5.70E-01, 4.83E-01, 3.43E-01, 2.56E-01, 1.33E-01, 4.76E-02, 2.14E-02],
    [1.02E+00, 9.63E-01, 8.49E-01, 6.88E-01, 4.38E-01, 3.00E-01, 1.40E-01, 4.78E-02, 2.15E-02],
    [1.57E+00, 1.46E+00, 1.23E+00, 9.18E-01, 4.97E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [2.05E+00, 1.88E+00, 1.51E+00, 1.03E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [2.52E+00, 2.27E+00, 1.73E+00, 1.07E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [2.97E+00, 2.61E+00, 1.85E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [3.56E+00, 3.00E+00, 1.92E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [4.01E+00, 3.23E+00, 1.93E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [4.42E+00, 3.37E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [4.77E+00, 3.43E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [5.16E+00, 3.45E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [5.40E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [5.54E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [5.59E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
    [5.62E+00, 3.46E+00, 1.94E+00, 1.08E+00, 5.07E-01, 3.17E-01, 1.41E-01, 4.78E-02, 2.15E-02],
])


# --------------------------------------------------
# Reduced W(u_B, beta) table
# --------------------------------------------------
u_inv_b = np.array([
    1.40E-02, 2.40E-02, 4.00E-02, 8.00E-02, 1.40E-01,
    2.40E-01, 4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00,
    4.00E+00, 8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01,
    8.00E+01, 1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02,
    1.00E+03
])

w_u_b = np.array([
    [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.12E-01, 3.23E-01, 1.45E-01, 5.09E-02, 2.39E-02],
    [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.12E-01, 3.23E-01, 1.47E-01, 5.32E-02, 2.57E-02],
    [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.16E-01, 3.27E-01, 1.52E-01, 5.68E-02, 2.86E-02],
    [5.62E+00, 3.46E+00, 1.94E+00, 1.09E+00, 5.24E-01, 3.37E-01, 1.62E-01, 6.61E-02, 3.62E-02],
    [5.62E+00, 3.46E+00, 1.94E+00, 1.10E+00, 5.37E-01, 3.50E-01, 1.78E-01, 8.06E-02, 4.86E-02],
    [5.62E+00, 3.46E+00, 1.95E+00, 1.11E+00, 5.57E-01, 3.74E-01, 2.05E-01, 1.06E-01, 7.14E-02],
    [5.62E+00, 3.46E+00, 1.96E+00, 1.13E+00, 5.89E-01, 4.12E-01, 2.48E-01, 1.49E-01, 1.13E-01],
    [5.62E+00, 3.46E+00, 1.98E+00, 1.18E+00, 6.67E-01, 5.06E-01, 3.57E-01, 2.66E-01, 2.31E-01],
    [5.63E+00, 3.47E+00, 2.01E+00, 1.24E+00, 7.80E-01, 6.42E-01, 5.17E-01, 4.45E-01, 4.19E-01],
    [5.63E+00, 3.49E+00, 2.06E+00, 1.35E+00, 9.54E-01, 8.50E-01, 7.63E-01, 7.18E-01, 7.03E-01],
    [5.63E+00, 3.51E+00, 2.13E+00, 1.50E+00, 1.20E+00, 1.13E+00, 1.08E+00, 1.06E+00, 1.05E+00],
    [5.64E+00, 3.56E+00, 2.31E+00, 1.85E+00, 1.68E+00, 1.65E+00, 1.63E+00, 9.99E+02, 9.99E+02],
    [5.65E+00, 3.63E+00, 2.55E+00, 2.23E+00, 2.15E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [5.67E+00, 3.74E+00, 2.86E+00, 2.68E+00, 2.65E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [5.70E+00, 3.90E+00, 3.24E+00, 3.15E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [5.76E+00, 4.22E+00, 3.85E+00, 3.82E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [5.85E+00, 4.58E+00, 4.38E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [5.99E+00, 5.00E+00, 4.91E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [6.16E+00, 5.46E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [6.47E+00, 6.11E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
    [6.60E+00, 6.50E+00, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02, 9.99E+02],
])


# --------------------------------------------------
# Full Neuman type-curve data
# Blank cells in the printed table are represented as np.nan.
# --------------------------------------------------
nan = np.nan

beta_values_full = np.array([
    0.001, 0.004, 0.01, 0.03, 0.06, 0.1, 0.2, 0.4, 0.6,
    0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0
])

beta_labels_full = [f"{b:g}" for b in beta_values_full]


# --------------------------------------------------
# Full W(u_A, beta) table
# --------------------------------------------------
u_inv_a_full = np.array([
    4.00E-01, 8.00E-01, 1.40E+00, 2.40E+00, 4.00E+00,
    8.00E+00, 1.40E+01, 2.40E+01, 4.00E+01, 8.00E+01,
    1.40E+02, 2.40E+02, 4.00E+02, 8.00E+02, 1.40E+03,
    2.40E+03, 4.00E+03, 8.00E+03, 1.40E+04
])

w_u_a_full = np.array([
    [2.48E-02, 2.43E-02, 2.41E-02, 2.35E-02, 2.30E-02, 2.24E-02, 2.14E-02, 1.99E-02, 1.88E-02, 1.79E-02, 1.70E-02, 1.53E-02, 1.38E-02, 1.25E-02, 1.13E-02, 9.33E-03, 7.72E-03, 6.39E-03, 5.30E-03],
    [1.45E-01, 1.42E-01, 1.40E-01, 1.36E-01, 1.31E-01, 1.27E-01, 1.19E-01, 1.08E-01, 9.88E-02, 9.15E-02, 8.49E-02, 7.13E-02, 6.03E-02, 5.11E-02, 4.35E-02, 3.17E-02, 2.34E-02, 1.74E-02, 1.31E-02],
    [3.58E-01, 3.52E-01, 3.45E-01, 3.31E-01, 3.18E-01, 3.04E-01, 2.79E-01, 2.44E-01, 2.17E-01, 1.94E-01, 1.75E-01, 1.36E-01, 1.07E-01, 8.46E-02, 6.78E-02, 4.45E-02, 3.02E-02, 2.10E-02, 1.51E-02],
    [6.62E-01, 6.48E-01, 6.33E-01, 6.01E-01, 5.70E-01, 5.40E-01, 4.83E-01, 4.03E-01, 3.43E-01, 2.96E-01, 2.56E-01, 1.82E-01, 1.33E-01, 1.01E-01, 7.67E-02, 4.76E-02, 3.13E-02, 2.14E-02, 1.52E-02],
    [1.02E+00, 9.92E-01, 9.63E-01, 9.05E-01, 8.49E-01, 7.92E-01, 6.88E-01, 5.42E-01, 4.38E-01, 3.60E-01, 3.00E-01, 1.99E-01, 1.40E-01, 1.03E-01, 7.79E-02, 4.78E-02, nan,      2.15E-02, nan],
    [1.57E+00, 1.52E+00, 1.46E+00, 1.35E+00, 1.23E+00, 1.12E+00, 9.18E-01, 6.59E-01, 4.97E-01, 3.91E-01, 3.17E-01, 2.03E-01, 1.41E-01, nan,      nan,      nan,      nan,      nan,      nan],
    [2.05E+00, 1.97E+00, 1.88E+00, 1.70E+00, 1.51E+00, 1.34E+00, 1.03E+00, 6.90E-01, 5.07E-01, 3.94E-01, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [2.52E+00, 2.41E+00, 2.27E+00, 1.99E+00, 1.73E+00, 1.47E+00, 1.07E+00, 6.96E-01, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [2.97E+00, 2.80E+00, 2.61E+00, 2.22E+00, 1.85E+00, 1.53E+00, 1.08E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [3.56E+00, 3.30E+00, 3.00E+00, 2.41E+00, 1.92E+00, 1.55E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [4.01E+00, 3.65E+00, 3.23E+00, 2.48E+00, 1.93E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [4.42E+00, 3.93E+00, 3.37E+00, 2.49E+00, 1.94E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [4.77E+00, 4.12E+00, 3.43E+00, 2.50E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [5.16E+00, 4.26E+00, 3.45E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [5.40E+00, 4.29E+00, 3.46E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [5.54E+00, 4.30E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [5.59E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [5.62E+00, nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan],
    [5.62E+00, 4.30E+00, 3.46E+00, 2.50E+00, 1.94E+00, 1.55E+00, 1.08E+00, 6.96E-01, 5.07E-01, 3.94E-01, 3.17E-01, 2.03E-01, 1.41E-01, 1.03E-01, 7.79E-02, 4.78E-02, 3.13E-02, 2.15E-02, 1.52E-02],
])


# --------------------------------------------------
# Full W(u_B, beta) table
# --------------------------------------------------
u_inv_b_full = np.array([
    4.00E-04, 8.00E-04, 1.40E-03, 2.40E-03, 4.00E-03,
    8.00E-03, 1.40E-02, 2.40E-02, 4.00E-02, 8.00E-02,
    1.40E-01, 2.40E-01, 4.00E-01, 8.00E-01, 1.40E+00,
    2.40E+00, 4.00E+00, 8.00E+00, 1.40E+01, 2.40E+01,
    4.00E+01, 8.00E+01, 1.40E+02, 2.40E+02, 4.00E+02
])

w_u_b_full = np.array([
    [5.62E+00, 4.30E+00, 3.46E+00, 2.50E+00, 1.94E+00, 1.56E+00, 1.09E+00, 6.97E-01, 5.08E-01, 3.95E-01, 3.18E-01, 2.04E-01, 1.42E-01, 1.03E-01, 7.80E-02, 4.79E-02, 3.14E-02, 2.15E-02, 1.53E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      7.81E-02, 4.80E-02, 3.15E-02, 2.16E-02, 1.53E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      1.03E-01, 7.83E-02, 4.81E-02, 3.16E-02, 2.17E-02, 1.54E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      nan,      1.04E-01, 7.85E-02, 4.84E-02, 3.18E-02, 2.19E-02, 1.56E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      6.97E-01, 5.08E-01, 3.95E-01, 3.18E-01, 2.04E-01, 1.42E-01, 1.04E-01, 7.89E-02, 4.87E-02, 3.21E-02, 2.21E-02, 1.58E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      6.97E-01, 5.09E-01, 3.96E-01, 3.19E-01, 2.05E-01, 1.43E-01, 1.05E-01, 7.99E-02, 4.96E-02, 3.29E-02, 2.28E-02, 1.64E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      6.98E-01, 5.10E-01, 3.97E-01, 3.21E-01, 2.07E-01, 1.45E-01, 1.07E-01, 8.14E-02, 5.09E-02, 3.41E-02, 2.39E-02, 1.73E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      7.00E-01, 5.12E-01, 3.99E-01, 3.23E-01, 2.09E-01, 1.47E-01, 1.09E-01, 8.38E-02, 5.32E-02, 3.61E-02, 2.57E-02, 1.89E-02],
    [nan,      nan,      nan,      nan,      nan,      nan,      nan,      7.03E-01, 5.16E-01, 4.03E-01, 3.27E-01, 2.13E-01, 1.52E-01, 1.13E-01, 8.79E-02, 5.68E-02, 3.93E-02, 2.86E-02, 2.15E-02],
    [nan,      nan,      nan,      nan,      nan,      1.56E+00, 1.09E+00, 7.10E-01, 5.24E-01, 4.12E-01, 3.37E-01, 2.24E-01, 1.62E-01, 1.24E-01, 9.80E-02, 6.61E-02, 4.78E-02, 3.62E-02, 2.84E-02],
    [nan,      nan,      nan,      nan,      1.94E+00, 1.56E+00, 1.10E+00, 7.20E-01, 5.37E-01, 4.25E-01, 3.50E-01, 2.39E-01, 1.78E-01, 1.39E-01, 1.13E-01, 8.06E-02, 6.12E-02, 4.86E-02, 3.98E-02],
    [nan,      nan,      nan,      2.50E+00, 1.95E+00, 1.57E+00, 1.11E+00, 7.37E-01, 5.57E-01, 4.47E-01, 3.74E-01, 2.65E-01, 2.05E-01, 1.66E-01, 1.40E-01, 1.06E-01, 8.53E-02, 7.14E-02, 6.14E-02],
    [nan,      nan,      nan,      2.51E+00, 1.96E+00, 1.58E+00, 1.13E+00, 7.63E-01, 5.89E-01, 4.83E-01, 4.12E-01, 3.07E-01, 2.48E-01, 2.10E-01, 1.84E-01, 1.49E-01, 1.28E-01, 1.13E-01, 1.02E-01],
    [5.62E+00, 4.30E+00, 3.46E+00, 2.52E+00, 1.98E+00, 1.61E+00, 1.18E+00, 8.29E-01, 6.67E-01, 5.71E-01, 5.06E-01, 4.10E-01, 3.57E-01, 3.23E-01, 2.98E-01, 2.66E-01, 2.45E-01, 2.31E-01, 2.20E-01],
    [5.63E+00, 4.31E+00, 3.47E+00, 2.54E+00, 2.01E+00, 1.66E+00, 1.24E+00, 9.22E-01, 7.80E-01, 6.97E-01, 6.42E-01, 5.62E-01, 5.17E-01, 4.89E-01, 4.70E-01, 4.45E-01, 4.30E-01, 4.19E-01, 4.11E-01],
    [5.63E+00, 4.31E+00, 3.49E+00, 2.57E+00, 2.06E+00, 1.73E+00, 1.35E+00, 1.07E+00, 9.54E-01, 8.89E-01, 8.50E-01, 7.92E-01, 7.63E-01, 7.45E-01, 7.33E-01, 7.18E-01, 7.09E-01, 7.03E-01, 6.99E-01],
    [5.63E+00, 4.32E+00, 3.51E+00, 2.62E+00, 2.13E+00, 1.83E+00, 1.50E+00, 1.29E+00, 1.20E+00, 1.16E+00, 1.13E+00, 1.10E+00, 1.08E+00, 1.07E+00, 1.07E+00, 1.06E+00, 1.06E+00, 1.05E+00, 1.05E+00],
    [5.64E+00, 4.35E+00, 3.56E+00, 2.73E+00, 2.31E+00, 2.07E+00, 1.85E+00, 1.72E+00, 1.68E+00, 1.66E+00, 1.65E+00, 1.64E+00, 1.63E+00, 1.63E+00, 1.63E+00, 1.63E+00, 1.63E+00, 1.63E+00, 1.63E+00],
    [5.65E+00, 4.38E+00, 3.63E+00, 2.88E+00, 2.55E+00, 2.37E+00, 2.23E+00, 2.17E+00, 2.15E+00, 2.15E+00, 2.14E+00, 2.14E+00, 2.14E+00, 2.14E+00, 2.14E+00, 2.14E+00, 2.14E+00, 2.14E+00, 2.14E+00],
    [5.67E+00, 4.44E+00, 3.74E+00, 3.11E+00, 2.86E+00, 2.75E+00, 2.68E+00, 2.66E+00, 2.65E+00, 2.65E+00, 2.65E+00, 2.65E+00, 2.64E+00, 2.64E+00, 2.64E+00, 2.64E+00, 2.64E+00, 2.64E+00, 2.64E+00],
    [5.70E+00, 4.52E+00, 3.90E+00, 3.40E+00, 3.24E+00, 3.18E+00, 3.15E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00, 3.14E+00],
    [5.76E+00, 4.71E+00, 4.22E+00, 3.92E+00, 3.85E+00, 3.83E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00, 3.82E+00],
    [5.85E+00, 4.94E+00, 4.58E+00, 4.40E+00, 4.38E+00, 4.38E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00, 4.37E+00],
    [5.99E+00, 5.23E+00, 5.00E+00, 4.92E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00, 4.91E+00],
    [6.16E+00, 5.59E+00, 5.46E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00, 5.42E+00],
])


# --------------------------------------------------
# Replace 999 values in W(u_B, beta)
# --------------------------------------------------
def replace_999_with_theis(u_inv_values, w_table):
    """
    Replace 999 placeholders with the Theis well function exp1(1/u_inv).

    NaN values are kept as NaN because they represent blank cells in the
    printed table.
    """
    w_clean = w_table.astype(float).copy()

    for i, u_inv_value in enumerate(u_inv_values):
        replacement = scipy.special.exp1(1.0 / u_inv_value)

        for j in range(w_clean.shape[1]):

            if np.isnan(w_clean[i, j]):
                continue

            if np.isclose(w_clean[i, j], 999.0) or np.isclose(w_clean[i, j], 9.99E2):
                w_clean[i, j] = replacement

    return w_clean

# --------------------------------------------------
# Combine Neuman A- and B-type curves into single curves
# --------------------------------------------------

def build_combined_neuman_table(
    u_inv_a_values,
    w_a_table,
    u_inv_b_values,
    w_b_table,
    beta_labels,
    storage_ratio=1e4,
):
    """
    Build combined Neuman type curves from A- and B-branch tables.

    A branch:
        x_A = 1/u_A

    B branch:
        x_B = (S_y / S_a) * 1/u_B

    For each beta value, the overlap is identified by the closest W-value
    between the A and B branches in log space.

    The actual transition is made at:

        transition_x = max(x_A_overlap, x_B_overlap_shifted)

    This prevents the B branch from being inserted too early for small beta
    values, while avoiding artificial averaged transition points that can
    create kinks for large beta values.
    """

    x_a_all = np.asarray(u_inv_a_values, dtype=float)
    x_b_all = np.asarray(u_inv_b_values, dtype=float) * storage_ratio

    combined_records = []
    overlap_records = []

    for j, beta_label in enumerate(beta_labels):

        y_a_all = np.asarray(w_a_table[:, j], dtype=float)
        y_b_all = np.asarray(w_b_table[:, j], dtype=float)

        valid_a = (
            np.isfinite(x_a_all)
            & np.isfinite(y_a_all)
            & (x_a_all > 0)
            & (y_a_all > 0)
        )

        valid_b = (
            np.isfinite(x_b_all)
            & np.isfinite(y_b_all)
            & (x_b_all > 0)
            & (y_b_all > 0)
        )

        xa = x_a_all[valid_a]
        ya = y_a_all[valid_a]

        xb = x_b_all[valid_b]
        yb = y_b_all[valid_b]

        original_a_indices = np.where(valid_a)[0]
        original_b_indices = np.where(valid_b)[0]

        if len(xa) == 0 or len(xb) == 0:
            continue

        # --------------------------------------------------
        # Sort both branches by x
        # --------------------------------------------------
        sort_a = np.argsort(xa)
        sort_b = np.argsort(xb)

        xa = xa[sort_a]
        ya = ya[sort_a]
        original_a_indices = original_a_indices[sort_a]

        xb = xb[sort_b]
        yb = yb[sort_b]
        original_b_indices = original_b_indices[sort_b]

        # --------------------------------------------------
        # Identify A/B overlap by closest W-value in log space
        # --------------------------------------------------
        log_ya = np.log10(ya)
        log_yb = np.log10(yb)

        diff_matrix = np.abs(log_ya[:, None] - log_yb[None, :])

        ia, ib = np.unravel_index(
            np.nanargmin(diff_matrix),
            diff_matrix.shape,
        )

        overlap_x_a = xa[ia]
        overlap_x_b = xb[ib]

        overlap_w_a = ya[ia]
        overlap_w_b = yb[ib]

        # --------------------------------------------------
        # Important:
        # Transition is controlled by the common x-axis.
        # This avoids inserting B too early.
        # --------------------------------------------------
        transition_x = max(overlap_x_a, overlap_x_b)

        use_a = xa <= transition_x
        use_b = xb > transition_x

        # --------------------------------------------------
        # Add A branch up to transition
        # --------------------------------------------------
        for x_val, w_val in zip(xa[use_a], ya[use_a]):
            combined_records.append(
                {
                    "beta": beta_label,
                    "x": x_val,
                    "W": w_val,
                    "source": "A",
                }
            )

        # --------------------------------------------------
        # Add B branch after transition
        # --------------------------------------------------
        for x_val, w_val in zip(xb[use_b], yb[use_b]):
            combined_records.append(
                {
                    "beta": beta_label,
                    "x": x_val,
                    "W": w_val,
                    "source": "B",
                }
            )

        # --------------------------------------------------
        # Diagnostics
        # --------------------------------------------------
        last_a_x = xa[use_a][-1] if np.any(use_a) else np.nan
        last_a_w = ya[use_a][-1] if np.any(use_a) else np.nan

        first_b_x = xb[use_b][0] if np.any(use_b) else np.nan
        first_b_w = yb[use_b][0] if np.any(use_b) else np.nan

        overlap_records.append(
            {
                "beta": beta_label,
                "A_index_overlap": int(original_a_indices[ia]),
                "B_index_overlap": int(original_b_indices[ib]),
                "x_A_overlap": overlap_x_a,
                "x_B_overlap_shifted": overlap_x_b,
                "transition_x_used": transition_x,
                "W_A_overlap": overlap_w_a,
                "W_B_overlap": overlap_w_b,
                "log10_W_difference": abs(
                    np.log10(overlap_w_a) - np.log10(overlap_w_b)
                ),
                "last_A_x_used": last_a_x,
                "last_A_W_used": last_a_w,
                "first_B_x_used": first_b_x,
                "first_B_W_used": first_b_w,
                "jump_ratio_B_over_A": (
                    first_b_w / last_a_w
                    if np.isfinite(first_b_w)
                    and np.isfinite(last_a_w)
                    and last_a_w > 0
                    else np.nan
                ),
                "number_A_points_used": int(np.sum(use_a)),
                "number_B_points_used": int(np.sum(use_b)),
            }
        )

    df_long = pd.DataFrame(combined_records)
    df_overlap = pd.DataFrame(overlap_records)

    if df_long.empty:
        return pd.DataFrame(), df_long, df_overlap

    # --------------------------------------------------
    # Wide table:
    # one x-axis column, one column per beta value
    # --------------------------------------------------
    df_wide = (
        df_long
        .pivot_table(
            index="x",
            columns="beta",
            values="W",
            aggfunc="mean",
        )
        .sort_index()
        .reset_index()
    )

    ordered_cols = ["x"] + [b for b in beta_labels if b in df_wide.columns]
    df_wide = df_wide[ordered_cols]

    return df_wide, df_long, df_overlap

# --------------------------------------------------
# Equation-based Neuman evaluator
# --------------------------------------------------
def safe_brentq(func, a, b, args=(), maxiter=100):
    """
    Safe wrapper around scipy.optimize.brentq.
    Returns np.nan if no root can be found.
    """
    try:
        fa = func(a, *args)
        fb = func(b, *args)

        if not np.isfinite(fa) or not np.isfinite(fb):
            return np.nan

        if fa * fb > 0:
            return np.nan

        return scipy.optimize.brentq(
            func,
            a,
            b,
            args=args,
            maxiter=maxiter,
        )

    except Exception:
        return np.nan


def gamma0_equation(gamma0, y, sigma):
    """
    Root equation for gamma_0:

    sigma * gamma0 * sinh(gamma0)
    - (y² - gamma0²) * cosh(gamma0) = 0
    """
    return (
        sigma * gamma0 * np.sinh(gamma0)
        - (y**2 - gamma0**2) * np.cosh(gamma0)
    )


def gamman_equation(gamma_n, y, sigma):
    """
    Root equation for gamma_n:

    sigma * gamma_n * sin(gamma_n)
    + (y² + gamma_n²) * cos(gamma_n) = 0
    """
    return (
        sigma * gamma_n * np.sin(gamma_n)
        + (y**2 + gamma_n**2) * np.cos(gamma_n)
    )


def compute_gamma_arrays(y_values, sigma, n_terms):
    """
    Compute gamma_0 and gamma_n roots for all y values.

    gamma_0 is in:
        0 < gamma_0 < y

    gamma_n is in:
        (2n - 1) * pi/2 < gamma_n < n*pi
    """
    y_values = np.asarray(y_values, dtype=float)

    gamma0_values = np.full_like(y_values, np.nan, dtype=float)
    gamman_values = np.full((n_terms, len(y_values)), np.nan, dtype=float)

    eps = 1e-10

    for i, y in enumerate(y_values):

        if y <= 0:
            continue

        # gamma_0 root
        a0 = eps
        b0 = y * (1.0 - 1e-8)

        gamma0_values[i] = safe_brentq(
            gamma0_equation,
            a0,
            b0,
            args=(y, sigma),
        )

        # gamma_n roots
        for n in range(1, n_terms + 1):

            an = (2 * n - 1) * np.pi / 2.0 + eps
            bn = n * np.pi - eps

            gamman_values[n - 1, i] = safe_brentq(
                gamman_equation,
                an,
                bn,
                args=(y, sigma),
            )

    return gamma0_values, gamman_values


def neuman_W_from_equations(
    beta,
    sigma,
    ts,
    y_values,
    gamma0_values,
    gamman_values,
    dD=0.0,
    lD=1.0,
    observation_mode="Piezometer",
    zD=0.5,
    z1D=0.0,
    z2D=1.0,
):
    """
    Evaluate dimensionless Neuman drawdown W from the provided equations.

    The returned value corresponds to:

        W = s_D = 4*pi*T*s / Q

    Parameters
    ----------
    beta : float
        Neuman beta parameter.

    sigma : float
        sigma = S / Sy.

    ts : float
        dimensionless time with respect to elastic storage:
        ts = T t / (S r²)

    y_values : ndarray
        integration variable.

    gamma0_values, gamman_values : ndarray
        precomputed roots.

    dD, lD : float
        dimensionless top and bottom of pumping well screen.

    observation_mode : str
        "Piezometer" uses equations (6) and (7).
        "Observation well average" uses equations (8) and (9).

    zD : float
        dimensionless piezometer elevation above aquifer base.

    z1D, z2D : float
        bottom and top of observation well screen for averaged observation.
    """

    y = np.asarray(y_values, dtype=float)
    gamma0 = np.asarray(gamma0_values, dtype=float)
    gamman = np.asarray(gamman_values, dtype=float)

    n_terms = gamman.shape[0]

    # --------------------------------------------------
    # Pumping well screen factors
    # --------------------------------------------------
    screen0 = np.ones_like(y)

    valid_g0 = np.isfinite(gamma0) & (gamma0 > 0)

    screen0[valid_g0] = (
        np.sinh(gamma0[valid_g0] * (1.0 - dD))
        - np.sinh(gamma0[valid_g0] * (1.0 - lD))
    ) / (
        (lD - dD) * np.sinh(gamma0[valid_g0])
    )

    # --------------------------------------------------
    # u0 term
    # --------------------------------------------------
    u0 = np.zeros_like(y)

    if np.any(valid_g0):

        g0 = gamma0[valid_g0]
        yy = y[valid_g0]

        denominator0 = (
            yy**2
            + (1.0 + sigma) * g0**2
            - ((yy**2 - g0**2) ** 2) / sigma
        )

        storage_term0 = 1.0 - np.exp(
            -ts * beta * (yy**2 - g0**2)
        )

        if observation_mode == "Piezometer":

            obs0 = np.cosh(g0 * zD) / np.cosh(g0)

        else:

            obs0 = (
                np.sinh(g0 * z2D)
                - np.sinh(g0 * z1D)
            ) / (
                (z2D - z1D) * np.cosh(g0)
            )

        u0[valid_g0] = (
            storage_term0
            * obs0
            * screen0[valid_g0]
            / denominator0
        )

    # --------------------------------------------------
    # un terms
    # --------------------------------------------------
    un_sum = np.zeros_like(y)

    for n in range(1, n_terms + 1):

        gamma_n = gamman[n - 1, :]

        valid_gn = np.isfinite(gamma_n) & (gamma_n > 0)

        if not np.any(valid_gn):
            continue

        gn = gamma_n[valid_gn]
        yy = y[valid_gn]

        denominator_n = (
            yy**2
            - (1.0 + sigma) * gn**2
            - ((yy**2 + gn**2) ** 2) / sigma
        )

        storage_term_n = 1.0 - np.exp(
            -ts * beta * (yy**2 + gn**2)
        )

        # Pumping well screen factor
        screen_n = (
            np.sin(gn * (1.0 - dD))
            - np.sin(gn * (1.0 - lD))
        ) / (
            (lD - dD) * np.sin(gn)
        )

        if observation_mode == "Piezometer":

            obs_n = np.cos(gn * zD) / np.cos(gn)

        else:

            obs_n = (
                np.sin(gn * z2D)
                - np.sin(gn * z1D)
            ) / (
                (z2D - z1D) * np.cos(gn)
            )

        un = np.zeros_like(y)
        un[valid_gn] = (
            storage_term_n
            * obs_n
            * screen_n
            / denominator_n
        )

        un_sum += un

    # --------------------------------------------------
    # Integral
    # --------------------------------------------------
    integrand = (
        4.0
        * y
        * scipy.special.j0(y * np.sqrt(beta))
        * (u0 + un_sum)
    )
    
    valid_integrand = np.isfinite(integrand)
    
    W = np.trapz(
        integrand[valid_integrand],
        y[valid_integrand],
    )
    
    return W

# --------------------------------------------------
# Select reduced or full data set
# --------------------------------------------------
st.subheader("Data source")

data_source = st.radio(
    "Choose Neuman type-curve table",
    [
        "Reduced implementation subset",
        "Full tabulated data",
    ],
    index=0,
    horizontal=True,
)

if data_source == "Reduced implementation subset":
    beta_values_active = beta_values
    beta_labels_active = beta_labels

    u_inv_a_active = u_inv_a
    w_u_a_active = w_u_a

    u_inv_b_active = u_inv_b
    w_u_b_active = w_u_b

else:
    beta_values_active = beta_values_full
    beta_labels_active = beta_labels_full

    u_inv_a_active = u_inv_a_full
    w_u_a_active = w_u_a_full

    u_inv_b_active = u_inv_b_full
    w_u_b_active = w_u_b_full


# --------------------------------------------------
# Clean selected W(u_B, beta) table
# --------------------------------------------------
w_u_b_clean = replace_999_with_theis(
    u_inv_b_active,
    w_u_b_active,
)


# --------------------------------------------------
# DataFrames for inspection
# --------------------------------------------------
df_a = pd.DataFrame(
    w_u_a_active,
    index=u_inv_a_active,
    columns=beta_labels_active,
)
df_a.index.name = "1/u_A"

df_b_raw = pd.DataFrame(
    w_u_b_active,
    index=u_inv_b_active,
    columns=beta_labels_active,
)
df_b_raw.index.name = "1/u_B"

df_b_clean = pd.DataFrame(
    w_u_b_clean,
    index=u_inv_b_active,
    columns=beta_labels_active,
)
df_b_clean.index.name = "1/u_B"


# --------------------------------------------------
# Plot controls
# --------------------------------------------------
st.subheader("Plot type curves")

col1, col2, col3, col4 = st.columns(4)

with col1:
    default_betas = (
        beta_labels
        if data_source == "Reduced implementation subset"
        else ["0.001", "0.01", "0.06", "0.2", "0.6", "1", "2", "4", "6"]
    )

    selected_betas = st.multiselect(
        "Select beta values",
        beta_labels_active,
        default=default_betas,
    )

with col2:
    table_choice = st.radio(
        "Table to plot",
        ["W(u_A, beta)", "W(u_B, beta)", "Both"],
        index=2,
    )

with col3:
    use_clean_b = st.toggle(
        "Replace 999 values in W(u_B, beta)",
        value=True,
    )

with col4:
    axis_mode = st.radio(
        "x-axis mode",
        [
            "Raw table axis",
            "Common Neuman type-curve axis",
        ],
        index=1,
    )

    log_storage_ratio = 4.0

storage_ratio = 10 ** log_storage_ratio

if axis_mode == "Common Neuman type-curve axis":
    st.info(
        rf"Type-B curves are shifted by \(S_y/S_a = {storage_ratio:.1e}\): "
        rf"\(x_B = (S_y/S_a) \cdot 1/u_B\)."
    )
else:
    st.info(
        "Raw table axis selected: type-A curves are plotted against 1/u_A, "
        "and type-B curves are plotted directly against 1/u_B."
    )

selected_indices = [beta_labels_active.index(b) for b in selected_betas]

# --------------------------------------------------
# Build combined single type-curve table
# --------------------------------------------------
combined_table, combined_long, overlap_table = build_combined_neuman_table(
    u_inv_a_values=u_inv_a_active,
    w_a_table=w_u_a_active,
    u_inv_b_values=u_inv_b_active,
    w_b_table=w_u_b_clean if use_clean_b else w_u_b_active,
    beta_labels=beta_labels_active,
    storage_ratio=storage_ratio,
)

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 7))

if table_choice in ["W(u_A, beta)", "Both"]:
    for j in selected_indices:

        valid = np.isfinite(w_u_a_active[:, j])

        ax.plot(
            u_inv_a_active[valid],
            w_u_a_active[valid, j],
            marker="o",
            markersize=4,
            linestyle="-",
            linewidth=1.5,
            label=rf"$W(u_A,\beta)$, $\beta$={beta_labels_active[j]}",
        )

if table_choice in ["W(u_B, beta)", "Both"]:
    w_b_plot = w_u_b_clean if use_clean_b else w_u_b_active

    if axis_mode == "Common Neuman type-curve axis":
        x_b = u_inv_b_active * storage_ratio
    else:
        x_b = u_inv_b_active

    for j in selected_indices:

        valid = np.isfinite(w_b_plot[:, j])

        ax.plot(
            x_b[valid],
            w_b_plot[valid, j],
            marker="s",
            markersize=4,
            linestyle="--",
            linewidth=1.5,
            label=rf"$W(u_B,\beta)$, $\beta$={beta_labels_active[j]}",
        )

ax.set_xscale("log")
ax.set_yscale("log")

if axis_mode == "Common Neuman type-curve axis":
    ax.set_xlabel(
        rf"common type-curve time axis: $1/u_A$ and $(S_y/S_a)\,1/u_B$, "
        rf"$S_y/S_a$ = {storage_ratio:.1e}"
    )
else:
    ax.set_xlabel(r"raw inverse dimensionless time: $1/u_A$ or $1/u_B$")

ax.set_ylabel(r"well function value $W(u,\beta)$")

ax.set_title(f"Neuman type-curve table check - {data_source}")
ax.grid(which="both", alpha=0.5)

if axis_mode == "Common Neuman type-curve axis":
    ax.set_xlim(1e-1, 1e5)
    ax.set_ylim(1e-3, 1e1)

ax.legend(fontsize=8, ncol=2)

fig.tight_layout()
st.pyplot(fig)


# --------------------------------------------------
# Optional raw table inspection
# --------------------------------------------------
with st.expander("Show W(u_A, beta) table"):
    st.dataframe(df_a)

with st.expander("Show raw W(u_B, beta) table"):
    st.dataframe(df_b_raw)

with st.expander("Show cleaned W(u_B, beta) table with 999 values replaced"):
    st.dataframe(df_b_clean)

# --------------------------------------------------
# Plot combined single type curves
# --------------------------------------------------
st.subheader("Combined single Neuman type curves")

fig_combined, ax_combined = plt.subplots(figsize=(11, 7))

for beta_label in selected_betas:

    if beta_label not in combined_table.columns:
        continue

    x_combined = combined_table["x"].values
    y_combined = combined_table[beta_label].values

    valid = np.isfinite(x_combined) & np.isfinite(y_combined)

    ax_combined.plot(
        x_combined[valid],
        y_combined[valid],
        marker="o",
        markersize=4,
        linewidth=1.5,
        label=rf"$\beta$={beta_label}",
    )

ax_combined.set_xscale("log")
ax_combined.set_yscale("log")

ax_combined.set_xlim(1e-1, 1e5)
ax_combined.set_ylim(1e-3, 1e1)

ax_combined.set_xlabel(
    rf"combined type-curve x-axis, using $S_y/S_a$ = {storage_ratio:.1e}"
)
ax_combined.set_ylabel(r"well function value $W(u,\beta)$")

ax_combined.set_title("Combined Neuman type curves")
ax_combined.grid(which="both", alpha=0.5)
ax_combined.legend(fontsize=9, ncol=2)

fig_combined.tight_layout()
st.pyplot(fig_combined)

# --------------------------------------------------
# Equation-based evaluation
# --------------------------------------------------
st.subheader("Equation-based evaluation of Neuman type curves")

evaluate_equations = st.toggle(
    "Evaluate Neuman equations",
    value=False,
)

if evaluate_equations:

    col_eq1, col_eq2, col_eq3, col_eq4 = st.columns(4)

    with col_eq1:
        selected_eq_betas = st.multiselect(
            "Beta values for equation evaluation",
            beta_labels_active,
            default=[
                b for b in ["0.001", "0.01", "0.06", "0.2", "0.6", "1", "2", "4", "6"]
                if b in beta_labels_active
            ],
        )

        observation_mode = st.radio(
            "Observation type",
            [
                "Piezometer",
                "Observation well average",
            ],
            index=1,
        )

    with col_eq2:
        log_sigma = st.slider(
            r"log10 sigma, $\log_{10}(S/S_y)$",
            min_value=-6.0,
            max_value=-1.0,
            value=-4.0,
            step=0.1,
        )

        sigma = 10 ** log_sigma

        st.write(rf"$\sigma = S/S_y$ = {sigma:.1e}")
        st.write(rf"$S_y/S = 1/\sigma$ = {1/sigma:.1e}")

    with col_eq3:
        n_terms = st.slider(
            "Number of gamma_n terms",
            min_value=1,
            max_value=20,
            value=8,
            step=1,
        )

        n_y = st.slider(
            "Number of integration y-values",
            min_value=100,
            max_value=1200,
            value=400,
            step=50,
        )

        y_max = st.slider(
            "Maximum y for numerical integration",
            min_value=10.0,
            max_value=150.0,
            value=60.0,
            step=5.0,
        )

    with col_eq4:
        n_x = st.slider(
            "Number of x-values",
            min_value=10,
            max_value=80,
            value=35,
            step=5,
        )

        zD = st.slider(
            "Piezometer elevation zD",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            disabled=(observation_mode != "Piezometer"),
        )

        z1D = st.slider(
            "Observation screen bottom z1D",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
            disabled=(observation_mode != "Observation well average"),
        )

        z2D = st.slider(
            "Observation screen top z2D",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.05,
            disabled=(observation_mode != "Observation well average"),
        )

    # Pumping well screen
    st.markdown("#### Pumping well screen")

    col_screen1, col_screen2 = st.columns(2)

    with col_screen1:
        dD = st.slider(
            "Dimensionless depth to top of pumping well screen dD",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
        )

    with col_screen2:
        lD = st.slider(
            "Dimensionless depth to bottom of pumping well screen lD",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.05,
        )

    if lD <= dD:
        st.error("lD must be larger than dD.")
        st.stop()

    if observation_mode == "Observation well average" and z2D <= z1D:
        st.error("z2D must be larger than z1D.")
        st.stop()

    # --------------------------------------------------
    # Numerical setup
    # --------------------------------------------------
    st.markdown("#### Numerical evaluation")

    y_values = np.concatenate(
        [
            np.geomspace(1e-5, 1.0, max(50, n_y // 4)),
            np.linspace(1.0, y_max, max(50, 3 * n_y // 4)),
        ]
    )

    x_values = np.logspace(-1, 5, n_x)

    # For the equation, x = 1/u_A = 4 * ts
    ts_values = x_values / 4.0

    with st.spinner("Computing gamma roots and evaluating Neuman equations..."):

        gamma0_values, gamman_values = compute_gamma_arrays(
            y_values=y_values,
            sigma=sigma,
            n_terms=n_terms,
        )

        equation_results = {}

        for beta_label in selected_eq_betas:

            beta = float(beta_label)

            W_values = []

            for ts in ts_values:

                W = neuman_W_from_equations(
                    beta=beta,
                    sigma=sigma,
                    ts=ts,
                    y_values=y_values,
                    gamma0_values=gamma0_values,
                    gamman_values=gamman_values,
                    dD=dD,
                    lD=lD,
                    observation_mode=observation_mode,
                    zD=zD,
                    z1D=z1D,
                    z2D=z2D,
                )

                W_values.append(W)

            equation_results[beta_label] = np.asarray(W_values)

    # --------------------------------------------------
    # Plot comparison
    # --------------------------------------------------
    fig_eq, ax_eq = plt.subplots(figsize=(11, 7))

    # Plot combined table curves first
    for beta_label in selected_eq_betas:

        if beta_label not in combined_table.columns:
            continue

        x_tab = combined_table["x"].values
        y_tab = combined_table[beta_label].values

        valid_tab = np.isfinite(x_tab) & np.isfinite(y_tab)

        ax_eq.plot(
            x_tab[valid_tab],
            y_tab[valid_tab],
            marker="o",
            markersize=4,
            linewidth=1.5,
            label=rf"table, $\beta$={beta_label}",
        )

    # Plot equation curves
    for beta_label, W_values in equation_results.items():

        valid_eq = np.isfinite(W_values) & (W_values > 0)

        ax_eq.plot(
            x_values[valid_eq],
            W_values[valid_eq],
            linestyle="--",
            linewidth=2.0,
            label=rf"equation, $\beta$={beta_label}",
        )

    ax_eq.set_xscale("log")
    ax_eq.set_yscale("log")

    ax_eq.set_xlim(1e-1, 1e5)
    ax_eq.set_ylim(1e-3, 1e1)

    ax_eq.set_xlabel(r"common type-curve x-axis $1/u_A = 4t_s$")
    ax_eq.set_ylabel(r"dimensionless drawdown $W = s_D$")

    ax_eq.set_title(
        rf"Table values and equation-based Neuman evaluation, $\sigma$ = {sigma:.1e}"
    )

    ax_eq.grid(which="both", alpha=0.5)
    ax_eq.legend(fontsize=8, ncol=2)

    fig_eq.tight_layout()
    st.pyplot(fig_eq)

    # --------------------------------------------------
    # Result table
    # --------------------------------------------------
    df_equation = pd.DataFrame(
        {
            "x": x_values,
            **{
                f"equation_beta_{beta_label}": values
                for beta_label, values in equation_results.items()
            },
        }
    )

    with st.expander("Show equation-based values"):
        st.dataframe(df_equation)

    with st.expander("Show gamma-root diagnostics"):
        df_gamma = pd.DataFrame(
            {
                "y": y_values,
                "gamma0": gamma0_values,
            }
        )

        for n in range(n_terms):
            df_gamma[f"gamma_{n+1}"] = gamman_values[n, :]

        st.dataframe(df_gamma)
            
# --------------------------------------------------
# Notes
# --------------------------------------------------
st.markdown(
    """
### Notes

- The reduced implementation uses a subset of the full Kruseman/de Ridder table.
- The full table includes additional beta values such as 0.004, 0.03, 0.1, 0.4, 0.8, 1.5, 2.5, 3, 5, and 7.
- Values marked as `999` or `9.99E+02` are placeholders. They can be replaced by the corresponding Theis well-function value.
- Blank cells in the printed full table are represented as `NaN` and are skipped in the plot.
- For comparison with classical Neuman type-curve diagrams, the type-B curves should be shifted by the storage ratio \(S_y/S_a\).
"""
)