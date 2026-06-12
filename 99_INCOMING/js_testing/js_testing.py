import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="HTML / JavaScript in Streamlit"
)

st.title("Non-reactive and Reactive Diffusive Transport ***DEMO***")
st.header("Spherical Diffusion", divider = 'blue')

st.markdown("""
***Application developed by A.J. Valocchi et al.*** - The original apps are available at https://hydrolab.illinois.edu/gw_applets/

This Streamlit app is a demonstrator of the user interface. The original Javascript is implemented through embedded html.
""") 

with st.expander(":red[**1**] :blue[**Overview of Models**]"):

    st.markdown("""
All three models use the analytical solutions of Crank (1975) for radial diffusion in a sphere. They differ in the initial and boundary conditions:

- **Model 1** — Diffusion into an initially empty sphere held at a constant outside concentration (*uptake*).

- **Model 2** — Diffusion out of a uniformly contaminated sphere into an infinite bath (*release*).

- **Model 3** — Two-phase process: the sphere is first loaded for time *t₀* using diffusion coefficient *D₂*, creating a non-uniform profile, then mass diffuses out with coefficient *D₁*.

Each model plots (i) the concentration profile *C(r,t)* at up to five snapshot times, and (ii) the fractional approach to equilibrium

$$
f(t)=\\frac{M_t}{M_\\infty}
$$
""")

with st.expander(":red[**2**]   :blue[**Model 1 — Diffusion into Empty Sphere from Infinite Bath**]", expanded=False):

    st.markdown(r"""
        At time zero the sphere is empty ($C_1 = 0$). The concentration outside the sphere is held constant at $C_0$ for all $t > 0$. Mass diffuses inward.
        
        **Concentration Profile**
        
        $$
        \frac{C-C_1}{C_0-C_1}
        =
        1
        +
        \frac{2a}{\pi r}
        \sum_{n=1}^{\infty}
        \frac{(-1)^n}{n}
        \sin\left(\frac{n\pi r}{a}\right)
        \exp\left(
        -\frac{Dn^2\pi^2 t}{a^2}
        \right)
        $$
        
        **Fractional Uptake**
        
        $$
        f
        =
        \frac{M_t}{M_\infty}
        =
        1
        -
        \frac{6}{\pi^2}
        \sum_{n=1}^{\infty}
        \frac{1}{n^2}
        \exp\left(
        -\frac{Dn^2\pi^2 t}{a^2}
        \right)
        $$
        """)

    left_co, cent_co, last_co = st.columns((10, 80, 10))
    with cent_co:
        st.image(
            "99_INCOMING/js_testing/fig01.png",
            caption="*Figure 1. Concentration profiles — diffusion into sphere (Model 1).*",
        )
        
    left_co2, cent_co2, last_co2 = st.columns((10, 80, 10))
    with cent_co2:
        st.image(
            "99_INCOMING/js_testing/fig02.png",
            caption="*Figure 2. Fractional approach to equilibrium (Model 1).*",
        )


with st.expander(":red[**3**]  :blue[**Model 2 — Diffusion Out of Uniformly Contaminated Sphere**]", expanded=False):

    st.markdown(r"""
At time zero the sphere is uniformly loaded at concentration $C_0$. The outside concentration is zero for all $t > 0$ (infinite bath). Mass diffuses outward.

**Concentration Profile**

$$
\frac{C}{C_0}
=
\frac{2a}{\pi r}
\sum_{n=1}^{\infty}
\frac{(-1)^{n+1}}{n}
\sin\left(\frac{n\pi r}{a}\right)
\exp\left(
-\frac{Dn^2\pi^2 t}{a^2}
\right)
$$

**Fractional Release**

$$
f_{\mathrm{rel}}
=
\frac{M_t}{M_0}
=
1
-
\frac{6}{\pi^2}
\sum_{n=1}^{\infty}
\frac{1}{n^2}
\exp\left(
-\frac{Dn^2\pi^2 t}{a^2}
\right)
$$

> **Note:** The expression for fractional release has the same mathematical form as the uptake equation in Model 1. Here, however, $M_t/M_0$ represents the fraction of the original mass remaining in the sphere.
""")

with st.expander(":red[**4**]  :blue[**Model 3 — Diffusion Out of Non-Uniformly Contaminated Sphere**]", expanded=False):

    st.markdown(r"""
The sphere is first loaded for time $t_0$ using diffusion coefficient $D_2$ (from an outside bath at concentration $C_0$), creating a non-uniform initial concentration profile. The outside concentration is then set to zero and mass diffuses out with coefficient $D_1$ for additional time $t$.

**Step 1 — Loaded Profile after Uptake**

After loading for time $t_0$ with $D_2$ (using Model 1 equations), the initial condition for release is

$$
C_{\mathrm{load}}(r,t_0)
=
C_0
\left[
1
+
\frac{2a}{\pi r}
\sum_{m=1}^{\infty}
\frac{(-1)^m}{m}
\sin\left(\frac{m\pi r}{a}\right)
\exp\left(
-\frac{D_2 m^2 \pi^2 t_0}{a^2}
\right)
\right]
$$

**Step 2 — Fourier Coefficients for Release**

The loaded profile is decomposed into a Fourier sine series. Using the orthogonality of $\sin(n\pi r/a)$ on $[0,a]$, the Fourier coefficients are

$$
B_n
=
\frac{2C_0a}{\pi n}
(-1)^{n+1}
\left[
1
-
\exp\left(
-\frac{D_2 n^2 \pi^2 t_0}{a^2}
\right)
\right]
$$

**Step 3 — Release Profile and Fractional Fill**

The concentration profile during release is

$$
C(r,t)
=
\frac{1}{r}
\sum_{n=1}^{\infty}
B_n
\sin\left(\frac{n\pi r}{a}\right)
\exp\left(
-\frac{D_1 n^2 \pi^2 t}{a^2}
\right)
$$

The fraction of sphere filled (mass remaining relative to the maximum possible mass) is

$$
f_{\mathrm{fill}}(t)
=
\frac{3}{C_0a^3}
\sum_{n=1}^{\infty}
B_n
\frac{a^2(-1)^{n+1}}{n\pi}
\exp\left(
-\frac{D_1 n^2 \pi^2 t}{a^2}
\right)
$$
""")

with st.expander(":red[**5**]  :blue[**Governing Equation and Boundary Conditions**]", expanded=False):

    st.markdown(r"""
All three models are governed by the radial diffusion equation in spherical coordinates:

$$
\frac{\partial C}{\partial t}
=
D
\left(
\frac{\partial^2 C}{\partial r^2}
+
\frac{2}{r}
\frac{\partial C}{\partial r}
\right)
$$

Symmetry at the sphere center requires

$$
\left.
\frac{dC}{dr}
\right|_{r=0}
=
0
$$

> **Analytical solution:** The series solutions presented in Models 1–3 are exact analytical solutions of the diffusion equation for their respective initial and boundary conditions, as derived by Crank (1975). The infinite series converge rapidly for $t > 0$ and are truncated at $n = 150$ terms in the applet.
""")

with st.expander(":green[**Show the Javascript applet**]", expanded=True):
    # --------------------------------------------------
    # Scale control
    # --------------------------------------------------
    scale = st.slider(
        "HTML scale",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
    )
    
    # --------------------------------------------------
    # Load HTML file
    # --------------------------------------------------
    html_file = Path("99_INCOMING/js_testing/spherical-standalone.html")
    
    if html_file.exists():
        html_code = html_file.read_text(encoding="utf-8")
    
        scaled_html = f"""
        <div style="
            transform: scale({scale});
            transform-origin: top left;
            width: {100/scale:.1f}%;
        ">
            {html_code}
        </div>
        """
    
        components.html(
            scaled_html,
            height=int(700 * scale),
            scrolling=True,
        )
    
    else:
        st.warning("No spherical-standalone.html file found.")
    
with st.expander(":red[**6**]  :blue[**Symbol Definitions**]", expanded=False):

    st.markdown(r"""
| Symbol | Definition |
|---------|------------|
| $C$ | Concentration inside the sphere |
| $C_0$ | Boundary concentration (outside sphere or initial inside, depending on model) |
| $C_1$ | Initial concentration inside sphere (= 0 for Models 1 & 2) |
| $a$ | Sphere radius |
| $r$ | Radial distance from center ($0 \le r \le a$) |
| $t$ | Time |
| $D$ | Diffusion coefficient (Models 1 & 2) |
| $D_1$ | Diffusion coefficient for release phase (Model 3) |
| $D_2$ | Diffusion coefficient for uptake/loading phase (Model 3) |
| $t_0$ | Loading time (Model 3) |
| $M_t$ | Mass in sphere at time $t$ |
| $M_\infty$ | Equilibrium mass (fully loaded) |
| $f$ | Fractional approach to equilibrium (uptake) or fractional release |
| $B_n$ | Fourier sine series coefficients for Model 3 release (Eq. 6) |
""")
    
with st.expander(":red[**7**]  :blue[**References**]", expanded=False):

    st.markdown("""
Crank, J. (1975). *The Mathematics of Diffusion*, 2nd ed. Oxford University Press, Oxford.
""")