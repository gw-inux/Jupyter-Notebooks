import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title("Consideration of Evapotranspiration on Groundwater Ressources")
st.subheader("Theory and Concept of Evapotranspiration in MODFLOW", divider="green")

st.markdown("""
This app shows the effect of evapotranspiration in removing water from an aquifer according to Harbaugh (2005). The approach assumes:
- if heads are above a specific elevation named _ET surface_ ($SURF$), the evapotranspiration rate $RET$ is a user-defined maximum rate $EVTR$
""")
st.latex(r'''\text{RET} = \text{EVTR}, \quad h_{i,j,k} > \text{SURF}''')
st.markdown("""
- if heads are below the _ET surface_ ($SURF$) and exceeding a specific intervall (i.e., distance from _ET surface_) named the _extinction depth_ or cutoff depth ($EXDP$), the evapotranspiration rate $ETR$ from the groundwater becomes zero.
""")
st.latex(r'''\text{RET} = 0, \quad h_{i,j,k} < \text{SURF} - \text{EXDP}''')
st.markdown("""
- between these two thresholds, evapotranspiration increase linearly from the _extinction depth_ to the _ET surface_.
""")
st.latex(r'''\text{RET} = \text{EVTR} \frac{h_{i,j,k} - (\text{SURF} - \text{EXDP})}{\text{EXDP}}, \quad (\text{SURF} - \text{EXDP}) \leq h_{i,j,k} \leq \text{SURF}
''')
st.markdown("""
The volumetric discharge is computed by multiplying the evapotranspiration rate $RET$ by the cell area $\Delta x \Delta y$:
""")
st.latex(r'''Q_{ET} = RET \Delta x \Delta y''')



st.subheader("Interactive plot", divider="green")
st.markdown("""
The interactive plot allows you to investigate $Q_{ET}$ in dependence from the _ET surface_ and the _extinction depth_. You can turn the plot by using the toggle above the input widgets.
""")
# Main area inputs

turn = st.toggle('Toggle to turn the plot 90 degrees')

columns1 = st.columns((1,1), gap = 'large')
with columns1[0]:
    SURF = st.slider("**ET surface $SURF$**", min_value=-3.0, max_value=0.0, value=-1.0, step=0.1)
    EXDP = st.slider("**Extinction depth $EXDP$**", min_value=0.1, max_value=5.0, value=4.0, step=0.1)

with columns1[1]:
    EVTR_input = st.slider("**Maximum Evapotranspiration rate ($EVTR$ in mm/d)**", min_value=0.1, max_value=20.0, value=2.0, step=0.1)
    EVTR = EVTR_input/86400000
    AREA = st.number_input("**Cell Area ($\\Delta x \\Delta y$) in m2**", min_value=1.0, max_value=40000.0, value=10000.0, step=100.0)

QET_MAX = 0.0005

# Define aquifer head range
h_aq = np.linspace(-10, 0, 100)

RET = np.where(h_aq > SURF, EVTR, np.where(h_aq >= (SURF - EXDP), EVTR * (h_aq - (SURF - EXDP)) / EXDP, 0))

QET = RET*AREA

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))
if turn:
    ax.plot(QET, h_aq, label="$Q_{ET}$",color='blue', linewidth=3)
    ax.axhline(0, color='black', linewidth=5)
    ax.axhline(SURF, color='green', linestyle='--', label=f'$SURF$ in m a.s.l.= {SURF}')
    ax.axhline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP)}')
    arrow_x = 0.8 * QET_MAX  # horizontal position
    arrow_y_start = SURF
    arrow_y_end = (SURF - EXDP)

    ax.annotate(
        '', 
        xy=(arrow_x, arrow_y_end),       # arrowhead
        xytext=(arrow_x, arrow_y_start), # arrow base
        arrowprops=dict(
            arrowstyle='<->', color='black', lw=1.5, alpha=0.7
        )
    )
    ax.text(
        arrow_x + 0.05 * QET_MAX,
        (arrow_y_start + arrow_y_end) / 2,
        "EXDP",
        color='black',
        fontsize=10,
        ha='center'
    )
else:
    ax.plot(h_aq, QET, label="$Q_{ET}$",color='blue', linewidth=3)
    ax.axvline(0, color='black', linewidth=5)
    ax.axvline(SURF, color='green', linestyle='--', label=f'$SURF$ in m a.s.l.= {SURF}')
    ax.axvline((SURF-EXDP), color='red', linestyle='--', label=f'$(SURF-EXDP)$ in m = {(SURF-EXDP)}')
    
    arrow_y = 0.8 * QET_MAX  # horizontal position
    arrow_x_start = SURF
    arrow_x_end = (SURF - EXDP)

    ax.annotate(
        '', 
        xy=(arrow_x_end, arrow_y),       # arrowhead
        xytext=(arrow_x_start, arrow_y), # arrow base
        arrowprops=dict(
            arrowstyle='<->', color='black', lw=1.5, alpha=0.7
        )
    )
    ax.text(
        (arrow_x_start + arrow_x_end) / 2,
        arrow_y + 0.02 * QET_MAX,  # slight vertical offset
        "EXDP",
        color='black',
        fontsize=10,
        ha='center'
    )

# Labels and formatting
if turn:
    ax.set_ylabel("Heads in the aquifer system in m above sea level (a.s.l)", fontsize=10)
    ax.set_xlabel("Evapotranspiration loss from the aquifer ($Q_{ET}$) in m³/s", fontsize=10)
    ax.set_ylim(-10,0)
    ax.set_xlim(-0.1*QET_MAX, QET_MAX)
else:
    ax.set_xlabel("Heads in the aquifer system in m above sea level (a.s.l)", fontsize=10)
    ax.set_ylabel("Evapotranspiration loss from the aquifer ($Q_{ET}$) in m³/s", fontsize=10)
    ax.set_xlim(0,-10)
    ax.set_ylim(-0.1*QET_MAX, QET_MAX)
ax.set_title("Evapotranspiration losses", fontsize=12)

ax.grid(True)
ax.legend()
#ax.set_aspect('equal', adjustable='box')

# Add gaining/losing stream annotations
#ax.text(0.2, -0.005, "Gaining Stream", va='center',color='blue')
#ax.text(0.2, 0.005, "Losing Stream", va='center',color='green')

st.pyplot(fig)

'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
