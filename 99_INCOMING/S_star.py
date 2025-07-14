import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from scipy.integrate import quad

st.title("Interactive Integral Calculator")
st.header("for S*(α, β)", divider = 'green')

st.subheader('Equation', divider = 'green')
st.markdown(r"""
$$
S^*(\alpha, \beta) = \int_0^1 \mathrm{erf}\left(\frac{\alpha}{\sqrt{\tau}}\right) \cdot \mathrm{erf}\left(\frac{\beta}{\sqrt{\tau}}\right) d\tau
$$
""")
st.subheader('Interactive plot', divider = 'green')
st.markdown(r"""
Use the sliders to set $\alpha$ and $\beta$ and visualize the integrand.
""")
# Sliders for input
alpha = st.slider("Alpha (α)", -3.0, 3.0, 1.0, 0.1)
beta = st.slider("Beta (β)", -3.0, 3.0, 1.0, 0.1)

# Define S_star as a single function (no nested integrand)
def S_star(alpha, beta):
    integrand = lambda tau: erf(alpha / np.sqrt(tau)) * erf(beta / np.sqrt(tau)) if tau > 0 else 0
    result, _ = quad(integrand, 0, 1, limit=200, epsabs=1e-10, epsrel=1e-10)
    return result

# Compute the integral
result = S_star(alpha, beta)



# Plot the integrand
tau_vals = np.linspace(1e-5, 1, 300)
integrand_vals = erf(alpha / np.sqrt(tau_vals)) * erf(beta / np.sqrt(tau_vals))

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(tau_vals, integrand_vals, lw=2)
ax.set_xlabel(r'$\tau$')
ax.set_ylabel(r'Integrand: $\mathrm{erf}\left(\frac{\alpha}{\sqrt{\tau}}\right) \cdot \mathrm{erf}\left(\frac{\beta}{\sqrt{\tau}}\right)$')
ax.set_title("Integrand vs. τ")
ax.set_ylim(-1, 1)  # Keep y-axis limits fixed
ax.set_xlim(-0, 1)  # Keep y-axis limits fixed
ax.grid(True)

st.pyplot(fig)

st.markdown(f"#### Result: $S^*({alpha}, {beta})$ = **{result:.6f}**")
