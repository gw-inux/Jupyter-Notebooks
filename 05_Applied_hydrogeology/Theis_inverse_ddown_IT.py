# Importazione delle librerie Python necessarie
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st

st.title('Predizione di abbassamento con Theis')
st.subheader(':green[Adattamento del]  parametro della formazione :red[ai dati misurati]', divider="rainbow")
st.markdown("""
            Questo documento interattivo consente di applicare il principio di Theis per la valutazione del test di pompaggio in configurazioni transitorie confinate. Il notebook è basato su un foglio di calcolo del Prof. Rudolf Liedl.
            
            ### Situazione generale
            Consideriamo un acquifero confinato con trasmissività costante. Se un pozzo pompa acqua dall'acquifero, viene indotto un flusso radiale verso il pozzo. Per calcolare la situazione idraulica, può essere utilizzata la seguente equazione semplificata di flusso. Questa equazione considera il flusso radiale 1D transitorio verso un pozzo completamente penetrante in un acquifero confinato senza ulteriori sink e fonti:
"""
)
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
st.markdown("""
            ### Modello matematico e soluzione
            Charles V. Theis ha presentato una soluzione derivando
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.markdown("""
            con la funzione del pozzo
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.markdown("""
            e la variabile adimensionale
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.markdown("""
            Queste equazioni non sono facili da risolvere. Storicamente, i valori per la funzione del pozzo erano forniti da tabelle o come curve di tipo. L'abbinamento delle curve di tipo con i dati sperimentali per l'analisi del test di pompaggio è considerato uno dei metodi base dell'idrogeologia. Tuttavia, i moderni computer forniscono un modo più semplice per risolvere l'equazione di flusso radiale 1D basata sull'approccio di Theis. Successivamente, l'equazione di Theis viene risolta con routine Python. I risultati per i dati misurati sono presentati graficamente in un grafico interattivo.
            
            I punti rossi rappresentano i dati misurati.
            
            Modifica la trasmissività _**T**_ e la storatività _**S**_ per adattare i dati misurati alla funzione del pozzo.
"""
)

# Funzioni necessarie per l'analisi del pozzo di Theis
def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T, S, r, t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def theis_wu(Q, T, s):
    wu = s * 4. * np.pi * T / Q
    return wu

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_max = 1
r_max = 100000
u  = [u_max for x in range(r_max)]
um = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
um_inv = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]
w_um = [well_function(u_max/r_max) for x in range(r_max)]

for x in range(1,r_max,1):
    if x>0:
        u[x] = x*u_max/r_max
        u_inv[x] = 1/u[x]
        w_u[x] = well_function(u[x])
# Seleziona i dati
datasource = st.selectbox(
    "Quali dati dovrebbero essere utilizzati?",
    ("Dati sintetici da libro di testo", "Viterbo 2023"),
)

# Definizione dei dati misurati per ogni sorgente selezionabile
if (datasource == "Dati sintetici da libro di testo"):
    # Data from SYMPLE exercise
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    minutes = True
    # Parameters needed to solve Theis (From the SYMPLE example/excercise)
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*24 # m^3/d
elif(datasource == "Viterbo 2023"):
    # Data from Viterbo 2023
    m_time = [0.083333333, 1, 1.416666667, 2.166666667, 2.5, 2.916666667, 3.566666667, 3.916666667, 4.416666667, 4.833333333, 5.633333333, 6.516666667, 7.5, 8.916666667, 10.13333333, 11.16666667, 12.6, 16.5, 18.53333333, 22.83333333, 27.15, 34.71666667, 39.91666667, 48.21666667, 60.4, 72.66666667, 81.91666667, 94.66666667, 114.7166667, 123.5]
    m_ddown = [0.04, 0.09, 0.12, 0.185, 0.235, 0.22, 0.26, 0.3, 0.31, 0.285, 0.34, 0.4, 0.34, 0.38, 0.405, 0.38, 0.385, 0.415, 0.425, 0.44, 0.44, 0.46, 0.47, 0.495, 0.54, 0.525, 0.53, 0.56, 0.57, 0.58]
    minutes = True
    # Parameters needed to solve Theis (From the SYMPLE example/excercise) !!! UPDATE !!!
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*24 # m^3/d

# CONVERT TIME TO SECONDS
if minutes:
    m_time_s = [i*60 for i in m_time] # time in seconds
else:
    m_time_s = [i for i in m_time] # time in seconds
num_times = len(m_time)

# This is the function to plot the graph with the data     

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1

# Slider e impostazioni di input

columns = st.columns((1, 1), gap='large')

with columns[0]:
    T_slider_value = st.slider('(logaritmo di) Trasmissività in m2/s', -7.0, 0.0, -3.0, 0.01, format="%4.2f")
    T = 10 ** T_slider_value
    st.write("**Trasmissività in m2/s:** %5.2e" % T)
    S_slider_value = st.slider('(logaritmo di) Storativity', -7.0, 0.0, -4.0, 0.01, format="%4.2f")
    S = 10 ** S_slider_value
    st.write("**Storativity (senza unità):** %5.2e" % S)
with columns[1]:
    Q_pred = st.slider(f'**Seleziona la portata (m^3/s) per la previsione**', 0.001, 0.100, Qs, 0.001, format="%5.3f")
    r_pred = st.slider(f'**Seleziona la distanza (m) dal pozzo per la previsione**', 1, 1000, r, 1)
    per_pred = st.slider(f'**Seleziona la durata del periodo di previsione (giorni)**', 1, 3652, 3, 1)
    max_t = 86400*per_pred
    if per_pred <= 3:
        t_search = st.slider(f'**Select the value of time (s) for printout**', 1,max_t,1,1)
    elif per_pred <= 7:
        t_search_h = st.slider(f'**Select the value of time (hours) for printout**', 1.,24.*per_pred,1.)
        t_search = t_search_h*3600
    elif per_pred <= 366:
        t_search_d = st.slider(f'**Select the value of time (days) for printout**', 1.,per_pred*1.0,1.)
        t_search = t_search_d*86400
    else:
        t_search_mo = st.slider(f'**Select the value of time (months) for printout**', 1.,per_pred/30.4375,1.)
        t_search = t_search_mo*2629800
    auto_y = st.toggle("Adatta l'intervallo di abbassamento nel grafico")

max_s = 20

# PLOT MEASURED DATA
x = 0
for t1 in m_time_s:
    um[x] = theis_u(T,S,r,t1)
    um_inv[x] = 1/um[x]
    w_um[x] = theis_wu(Qs,T,m_ddown[x])
    x = x+1

# PLOT DRAWDOWN VS TIME

# Range of delta_h / delta_l values (hydraulic gradient)
t2 = np.linspace(1, max_t, 100)
t2_h = t2/3600
t2_d = t2/86400
t2_mo = t2/2629800

# Calcolo del drawdown
s  = compute_s(T, S, t2, Q_pred, r_pred)

# Compute s for a specific point
x_point = t_search
y_point = compute_s(T, S, t_search, Q_pred, r_pred)

fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(1, 2, 1)
ax.plot(u_inv, w_u)
ax.plot(um_inv[:num_times], w_um[:num_times],'ro')
plt.yscale("log")
plt.xscale("log")
plt.axis([1,1E5,1E-2,1E+2])
plt.xlabel(r'1/u', fontsize=14)
plt.ylabel(r'w(u)', fontsize=14)
plt.title('Theis Abbassamento', fontsize=16)
ax.grid(which="both")
plt.legend(('well function','Dati misurati'))

ax = fig.add_subplot(1, 2, 2)
if per_pred <= 3:
    plt.plot(t2, s, linewidth=3., color='r', label=r'Previsione di abbassamento')
    plt.plot(t_search,y_point, marker='o', color='b',linestyle ='None', label="Risultato dell'abbassamento")
    plt.xlabel(r'Tempo in sec', fontsize=14)
    plt.xlim(0, max_t)
elif per_pred <= 7:
    plt.plot(t2_h, s, linewidth=3., color='r', label=r'Previsione di abbassamento')
    plt.plot(t_search_h,y_point, marker='o', color='b',linestyle ='None', label="Risultato dell'abbassamento")
    plt.xlabel(r'Tempo in hours', fontsize=14)
    plt.xlim(0, max_t/3600)
elif per_pred <= 366:
    plt.plot(t2_d, s, linewidth=3., color='r', label=r'Previsione di abbassamento')
    plt.plot(t_search_d,y_point, marker='o', color='b',linestyle ='None', label="Risultato dell'abbassamento")
    plt.xlabel(r'Tempo in days', fontsize=14)
    plt.xlim(0, max_t/86400)
else:
    plt.plot(t2_mo, s, linewidth=3., color='r', label=r'Previsione di abbassamento')
    plt.plot(t_search_mo,y_point, marker='o', color='b',linestyle ='None', label="Risultato dell'abbassamento")
    plt.xlabel(r'Tempo in months', fontsize=14)
    plt.xlim(0, max_t/2629800)

#plt.ylim(max_s, 0)
if auto_y:
    plt.ylim(bottom=0, top=None)
else:
    plt.ylim(bottom=0, top=max_s)
ax.invert_yaxis()
plt.plot(x_point,y_point, marker='o', color='b',linestyle ='None', label='drawdown output') 
plt.ylabel(r'Abbassamento (m)', fontsize=14)
plt.title('Predizione di abbassamento con Theis', fontsize=16)
plt.legend()
plt.grid(True)
    
st.pyplot(fig)


# Informazioni di stima e previsione
columns2 = st.columns((1, 1), gap='medium')
with columns2[0]:
    st.write("**Stima dei parametri**")
    st.write("Distanza di misura dal pozzo (in m): %3i" % r)
    st.write("Portata di misura (in m^3/s): %5.3f" % Qs)
    st.write("Spessore della formazione b = ", "%5.2f" % b, " m")
    st.write("Trasmissività T = ", "%10.2E" % T, " m^2/s")
    st.write("(Cond. idraulica K) = ", "%10.2E" % (T / b), " m^2/s")
    st.write("Storativity S = ", "%10.2E" % S, "[-]")
with columns2[1]:
    st.write("**Previsione**")
    st.write("Distanza di previsione dal pozzo (in m): %3i" % r_pred)
    st.write("Portata di previsione (in m^3/s): %5.3f" % Q_pred)
    st.write("Tempo dall'inizio della pompata (in s): %3i" % per_pred)


