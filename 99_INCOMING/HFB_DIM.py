import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Dimensionierung von Horizontalfilterbrunnen")
st.header("Hydraulisch aktive Fläche für verschiedene Filterlängen.", divider = 'green')

# Constants
st.markdown("""
#### :green[EINGABE Bereich für PARAMETER]
""")
columns1 = st.columns((1,1))
with columns1[0]:
    B = st.slider('Überschnittbohrung $B$ in m', 0.1, 2.0, 0.8, 0.05)
lengths = [6, 12, 20, 25, 30, 50, 80, 100, 150, 200, 300, 400]
#fkh_values = [1.0, 1.5, 2.0, 2.5]
with columns1[1]:
    fkh_min, fkh_max = st.slider("Bereich für FKh (m)", 0.5, 5.0, (1.0, 2.5), 0.1)
    fkh_step = st.slider("Schrittweite ΔFKh (m)", 0.1, 1.0, 0.5, 0.1)

fkh_values = np.arange(fkh_min, fkh_max + fkh_step, fkh_step).round(2)


# Compute area
data = {f"FKh={fkh} m": [B * fkh * 2 * l for l in lengths] for fkh in fkh_values}
df = pd.DataFrame(data, index=lengths)
df.index.name = "Filterlänge (m)"


# Plot with categorical x-axis (rubrics)
st.subheader("Ergebnisse und Interaktive Grafik: Fläche vs. Filterlänge (Rubrikenachse)", divider = 'green')

with st.expander(' Für die **Anzeige der tabellarischen Flächen :red[hier klicken]**'):
    st.dataframe(df)
fig, ax = plt.subplots()

# Convert numeric lengths to strings for categorical axis
rubrics = [str(l) for l in lengths]

for col in df.columns:
    ax.plot(rubrics, df[col], label=col, marker="o")

ax.set_xlabel("Filterlänge (m)")
ax.set_ylabel("Hydraulisch wirksame Oberfläche (m²)")
ax.set_ylim(0, 2500)
ax.legend(loc="upper left")
ax.grid(True, axis='y')
st.pyplot(fig)
