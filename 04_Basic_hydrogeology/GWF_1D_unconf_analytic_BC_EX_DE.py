# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit_book as stb


st.title('Physikalische und Hydraulische Randbedingungen')

st.markdown(
    """
    ### Vorbemerkung
    Dieses Notebook erläutert den Unterschied zwischen physikalischen und hydraulischen Randbedingungen anhand eines einfach Beispiels. Mit den zugehörigen Aufgaben kann das Verhalten der einzelnen Randbedingungen näher untersucht werden.
    
    ### Lernziele:
    Nachdem Sie dieses Notebook erfolgreich bearbeitet haben, können Sie:
    * Die Unterschiede zwischen hydraulischen und physikalischen Randbedingungen für Grundwasserströmungsmodelle erläutern;
    * Disskutieren, mit welchen Möglichkeiten eine Grundwasserscheide für ein Grundwasserströmungsmodell berücksichtigt werden kann.
    
    ### Ausgangssituation - Konzeptionelles und mathematisches Modell
    Betrachtet wird ein ungespannter, homogener und isotroper Grundwasserleiter, der durch zwei Standgewässer begrenzt wird. Der Grundwasserleiter wird zusätzlich durch Grundwasserneubildung gespeist. Die Grundwasserhydraulik kann durch eine 1D Vereinfachung der allgemeinen Grundwasserströmungsgleichung beschrieben werden, für die folgende analytische Lösung existiert (siehe nachfolgende Abbildung)
"""
)
st.latex(r'''\frac{d}{dx}=(-hK\frac{dh}{dx})=R''')

st.markdown(
    """
    with
    - _x_ is spatial coordinate along flow,
    - _h_ is hydraulic head,
    - _K_ is hydraulic conductivity,
    - _R_ is recharge.
    
    Mit der Hilfe der folgenden Randbedingungen für _x_ = 0 and _x_ = _L_ kann die Gleichung gelöst werden:
"""
)
st.latex(r'''h(0) = h_0''')
st.latex(r'''h(L) = h_L''')

st.markdown(
    """
    Die Lösung der Gleichung für die Potentialhöhe h entlang der x-Koordinate lautet:
"""
)

st.latex(r'''h(x)=\sqrt{h_0^2-\frac{h_0^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}''')

left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('04_Basic_hydrogeology/FIGS/concept_1D_flow_unconfined.png', caption="Abbildung 1: Konzeptionelles Modell zur 1D Grundwasserströmung in einem ungespannten Grundwasserleiter.")

st.markdown(
    """
    ### Analytische Berechnung und Visualisierung der Ergebnisse:
    Mit der nachfolgenden Funktionalität wird die Lösung der Funktion interaktiv dargestellt. Es können die Parameter variiert werden, um die funktionalen Zusammenhänge zu analysieren. Veränderlich Parameter sind
    * Grundwasserneubildung _R_ in mm/a und
    * hydraulische Leitfähigkeit _K_ in m/s.
"""
)

"---"

# Input data

# Define the minimum and maximum for the logarithmic scale
log_min = -7.0 # Corresponds to 10^-7 = 0.0000001
log_max = 0.0  # Corresponds to 10^0 = 1

columns = st.columns((1,1), gap = 'large')

with columns[0]:
    y_scale = st.slider('Skalierung y-achse', 0,20,3,1)
    hl=st.slider('Definierte **Potentialhöhe LINKS**', 120,180,150,1)
    hr=st.slider('Definierte **Potentialhöhe RECHTS**', 120,180,152,1)
    L= st.slider('Länge', 0,7000,2500,10)


with columns[1]:
    R=st.slider('**Grundwasserneubildung** in mm/a', -500,500,0,10)
    K_slider_value=st.slider('(log) **Hydraulische Leitfähigkeit** in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_Hydraulische Leitfähigkeit_ in m/s: %5.2e" %K)
    
x = np.arange(0, L,L/1000)
R=R/1000/365.25/86400
h=(hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5
    
# PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x,h)
ax.set(xlabel='x (m)', ylabel='Druckpotential (m)',title='Potentialhöhe für die 1D ungespannte Grundwasserströmung')
ax.fill_between(x,0,h, facecolor='lightblue')
    
# BOUNDARY CONDITIONS hl, hr
ax.vlines(0, 0, hl, linewidth = 10, color='b')
ax.vlines(L, 0, hr, linewidth = 10, color='b')
    
# MAKE 'WATER'-TRIANGLE
y_range = abs((hl*(1-y_scale/100))-(hr*(1+y_scale/100)))
h_arrow = (hl**2-(hl**2-hr**2)/L*(L*0.96)+(R/K*(L*0.96)*(L-(L*0.96))))**0.5  #water level at arrow
ax.arrow(L*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L*0.015), head_length=(h_arrow*0.0015))
ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

#ARROWS FOR RECHARGE 
if R != 0:
    head_length=(R*86400*365.25*1000*0.002)*y_scale/2
    h_rch1 = (hl**2-(hl**2-hr**2)/L*(L*0.25)+(R/K*(L*0.25)*(L-(L*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
    ax.arrow(L*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch2 = (hl**2-(hl**2-hr**2)/L*(L*0.50)+(R/K*(L*0.50)*(L-(L*0.50))))**0.5  #water level at arrow for Recharge Postition 2
    ax.arrow(L*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch3 = (hl**2-(hl**2-hr**2)/L*(L*0.75)+(R/K*(L*0.75)*(L-(L*0.75))))**0.5  #water level at arrow for Recharge Position 3
    ax.arrow(L*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)

#Groundwater divide
max_y = max(h)
max_x = x[h.argmax()]
R_min_ms=K*abs(hl**2-hr**2)/L**2
if R>R_min_ms:
    plt.vlines(max_x,0,max_y, color="r")

plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
plt.xlim(-50,L+50)
plt.text(L, (hr*(1+y_scale/100))-0.1*y_range, r'GWN: {:.3e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='azure'),fontsize=12)
ax.grid()
st.pyplot(fig)

st.markdown(
    """
    ### Anleitung zur eigenen Untersuchung
    Stellen Sie mit Hilfe der Schieberegler die initialen Größen für die definierten Randpotentiale, die Grundwasserneubildung (GWN) _R_ und die hydraulische Leitfähigkeit _K_ ein
    * h_0 = 100 m
    * h_1 = 102 m
    * R = 200 mm/a und
    * K = 2e-5 m/s.
    
    ---
    
    #### Aufgabe/FRAGE 1:
    Es bildet sich eine Grundwasserscheide aus (rote Linie). Beschreiben Sie, in welche Richtung sich das aus der Grundwasserneubildung zuströmende Wasser bewegt.
    
    ---
    
    #### Aufgabe/FRAGE 2:    
    Die Situation soll im weiteren Verlauf mit einem numerischen Modell simuliert werden. Dazu werden drei mögliche Randbedingungen in Betracht gezogen, welche in Abbildung 2 mit A, B und C bezeichnet werden.
    Entscheiden Sie für die Randbedingungen A, B, und C (s. nachfolgende Abb. 2), ob es sich um physikalische oder hydraulische Randbedingungen handelt.
"""
)

left_co, cent_co, last_co = st.columns((5,60,5))
with cent_co:
    st.image('90_Streamlit_apps/GWBmC/assets/images/1D_unconfied_BC_4.png', caption="Abbildung 2: Konzeptionelles Modell zur 1D Grundwasserströmung in einem ungespannten Grundwasserleiter.")

column1 = st.columns((1,1,1))
with column1[0]:
    stb.single_choice("Randbedingung A: Handelt es sich um eine physikalische oder hydraulische Randbedingung?",
                  ["physikalische RB", "hydraulische RB"],
                  0,success='Korrekt!  Sehr gut erkannt', error='Leider nicht korrekt. Bitte beachten, dass die Lage von physikalische Randbedingungen nicht von den hydrologischen Eigenschaften abhängig sind.')
with column1[1]:
    stb.single_choice("Randbedingung B: Handelt es sich um eine physikalische oder hydraulische Randbedingung?",
                  ["physikalische RB", "hydraulische RB"],
                  1,success='Korrekt!  Sehr gut erkannt', error='Leider nicht korrekt. Bitte beachten, dass die Lage von physikalische Randbedingungen nicht von den hydrologischen Eigenschaften abhängig sind.')
with column1[2]:
    stb.single_choice("Randbedingung C: Handelt es sich um eine physikalische oder hydraulische Randbedingung?",
                  ["physikalische RB", "hydraulische RB"],
                  0,success='Korrekt!  Sehr gut erkannt', error='Leider nicht korrekt. Bitte beachten, dass die Lage von physikalische Randbedingungen nicht von den hydrologischen Eigenschaften abhängig sind.')
                  
st.markdown(
    """    
    
    ---
    
    #### Aufgabe/FRAGE 3:
    Abb. 3 zeigt ebenfalls zwei Modellvarianten (V1 und V2) - welche würden Sie für eine numerische Simulation empfehlen und warum?
"""
)

left_co, cent_co, last_co = st.columns((5,60,5))
with cent_co:
    st.image('90_Streamlit_apps/GWBmC/assets/images/1D_unconfied_BC_2.png', caption="Abbildung 3: Konzeptionelles Modell mit zwei verschiedenen Modellvarianten V1 und V2.")
    
stb.single_choice("Welche Modellvariante würden Sie wählen?",
                  ["Variante V1", "Variante V2", "V1 und V2 sind gleich gut geeignet"],
                  1,success='Korrekt!  Nach Möglichkeit sollte das Modell von physikalischen Randbedingungen begrenzt werden', error='Leider nicht korrekt. Bitte beachten Sie, dass physikalische Randbedingungen (wie die zwei Festpotentiale) bevorzugt werden sollten, da deren Lage nicht von den hydrologischen Eigenschaften abhängig ist.')
st.markdown(
    """ 
    ---
    #### Aufgabe/FRAGE 4:    
    In einem relativ trockenem Jahr reduziert sich die Grundwasserneubildung auf 100 mm/a. Welche Auswirkungen hat die reduzierte GWN für die Randbedingung B (siehe Abb. 2)? Diskutieren Sie kritisch!
    Stellen Sie diesen Wert mit den Schiebereglern der nachfolgenden interaktiven Abbildung ein und beschreiben Sie, wie sich die Wasserscheide verhält.
"""
)

columns3 = st.columns((1,1), gap = 'large')

with columns3[0]:
    y_scale = st.slider('Skalierung y-achse', 0,20,3,1, key=(8))
    hl=st.slider('Definierte **Potentialhöhe LINKS**', 120,180,150,1,key=(9))
    hr=st.slider('Definierte **Potentialhöhe RECHTS**', 120,180,152,1, key=(10))
    L= st.slider('Länge', 0,7000,2500,10, key=(11))


with columns3[1]:
    R=st.slider('**Grundwasserneubildung** in mm/a', -500,500,0,10, key=(12))
    K_slider_value=st.slider('(log) **Hydraulische Leitfähigkeit** in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" , key=(13))
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_Hydraulische Leitfähigkeit_ in m/s: %5.2e" %K)
    
x = np.arange(0, L,L/1000)
R=R/1000/365.25/86400
h=(hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5
    
# PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x,h)
ax.set(xlabel='x (m)', ylabel='Druckpotential (m)',title='Potentialhöhe für die 1D ungespannte Grundwasserströmung')
ax.fill_between(x,0,h, facecolor='lightgreen')
    
# BOUNDARY CONDITIONS hl, hr
ax.vlines(0, 0, hl, linewidth = 10, color='green')
ax.vlines(L, 0, hr, linewidth = 10, color='green')
    
# MAKE 'WATER'-TRIANGLE
y_range = abs((hl*(1-y_scale/100))-(hr*(1+y_scale/100)))
h_arrow = (hl**2-(hl**2-hr**2)/L*(L*0.96)+(R/K*(L*0.96)*(L-(L*0.96))))**0.5  #water level at arrow
ax.arrow(L*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L*0.015), head_length=(h_arrow*0.0015))
ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

#ARROWS FOR RECHARGE 
if R != 0:
    head_length=(R*86400*365.25*1000*0.002)*y_scale/2
    h_rch1 = (hl**2-(hl**2-hr**2)/L*(L*0.25)+(R/K*(L*0.25)*(L-(L*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
    ax.arrow(L*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch2 = (hl**2-(hl**2-hr**2)/L*(L*0.50)+(R/K*(L*0.50)*(L-(L*0.50))))**0.5  #water level at arrow for Recharge Postition 2
    ax.arrow(L*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch3 = (hl**2-(hl**2-hr**2)/L*(L*0.75)+(R/K*(L*0.75)*(L-(L*0.75))))**0.5  #water level at arrow for Recharge Position 3
    ax.arrow(L*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)

#Groundwater divide
max_y = max(h)
max_x = x[h.argmax()]
R_min_ms=K*abs(hl**2-hr**2)/L**2
if R>R_min_ms:
    plt.vlines(max_x,0,max_y, color="r")

plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
plt.xlim(-50,L+50)
plt.text(L, (hr*(1+y_scale/100))-0.1*y_range, r'GWN: {:.3e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='azure'),fontsize=12)
ax.grid()
st.pyplot(fig)

st.markdown(
    """    
    
    ---
    
    #### Aufgabe/FRAGE 5:
    Für die numerische Simulation stehen nur begrenzte Ressourcen zur Verfügung, so dass Modell V1 mit der geringeren räumlichen Ausdehnung verwendet wird. Bei dieser Entscheidung wurde davon ausgegangen, dass sich die Grundwasserneubildung nicht ändert.     
"""
)

stb.single_choice("Welche Art von Randbedingung schlagen Sie für B (siehe Abb. 2) vor?",
                  ["RR 1. Art (definierte Potentialhöhe", "RB 2. Art (definierter Volumenstrom)", "RB 2. Art (No-Flow)", "RB 3. Art (halbdurchlässiger Rand)"],
                  2,success='Sehr gut gewählt! In der nachfolgenden Aufgabe/Frage 6 können Sie sich nochmal ansehen, dass diese Art der Randbedingung von den absoluten Potentialhöhen unabhängig ist.', error=' Diese Variante ist nicht optimal. In der nachfolgenden Aufgabe/Frage 6 können Sie genauer analysieren, dass die Potentialhöhe der der Randbedingung von den absoluten Potentialhöhen abhängig ist.')

st.markdown(
    """    
    
    ---
    
    #### Aufgabe/FRAGE 6:
    Infolge von Maßnahmen zur Wasserbewirtschaftung wird das Druckpotential in den Randbedingungen A und B jeweils um einen Meter erhöht.
    Führen Sie diese Änderungen in der analyischen Lösung im nachstehenden interaktiven Diagramm mit Hilfe der Schieberegler durch. Beschreiben Sie die Änderung von Lage und Druckpotential der Grundwasserscheide.
    Diskutieren Sie kritisch Ihre Entscheidung in Frage 5 hinsichtlich der Art der RB, revidieren Sie diese gegebenfalls (siehe finale Frage unterhalb des Diagramms) und Begründen Sie ihre endgültige Auswahl.        
"""
)

columns2 = st.columns((1,1), gap = 'large')

with columns2[0]:
    y_scale = st.slider('Skalierung y-achse', 0,20,3,1, key=(2))
    hl=st.slider('Definierte **Potentialhöhe LINKS**', 120,180,150,1,key=(3))
    hr=st.slider('Definierte **Potentialhöhe RECHTS**', 120,180,152,1, key=(4))
    L= st.slider('Länge', 0,7000,2500,10, key=(5))


with columns2[1]:
    R=st.slider('**Grundwasserneubildung** in mm/a', -500,500,0,10, key=(6))
    K_slider_value=st.slider('(log) **Hydraulische Leitfähigkeit** in m/s', log_min,log_max,-4.0,0.01,format="%4.2f" , key=(7))
    # Convert the slider value to the logarithmic scale
    K = 10 ** K_slider_value
    # Display the logarithmic value
    st.write("_Hydraulische Leitfähigkeit_ in m/s: %5.2e" %K)
    
x = np.arange(0, L,L/1000)
R=R/1000/365.25/86400
h=(hl**2-(hl**2-hr**2)/L*x+(R/K*x*(L-x)))**0.5
    
# PLOT FIGURE
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x,h)
ax.set(xlabel='x (m)', ylabel='Druckpotential (m)',title='Potentialhöhe für die 1D ungespannte Grundwasserströmung')
ax.fill_between(x,0,h, facecolor='lightgrey')
    
# BOUNDARY CONDITIONS hl, hr
ax.vlines(0, 0, hl, linewidth = 10, color='orange')
ax.vlines(L, 0, hr, linewidth = 10, color='orange')
    
# MAKE 'WATER'-TRIANGLE
y_range = abs((hl*(1-y_scale/100))-(hr*(1+y_scale/100)))
h_arrow = (hl**2-(hl**2-hr**2)/L*(L*0.96)+(R/K*(L*0.96)*(L-(L*0.96))))**0.5  #water level at arrow
ax.arrow(L*0.96,(h_arrow+(h_arrow*0.002)), 0, -0.01, fc="k", ec="k", head_width=(L*0.015), head_length=(h_arrow*0.0015))
ax.hlines(y= h_arrow-(h_arrow*0.0005), xmin=L*0.95, xmax=L*0.97, colors='blue')   
ax.hlines(y= h_arrow-(h_arrow*0.001), xmin=L*0.955, xmax=L*0.965, colors='blue')

#ARROWS FOR RECHARGE 
if R != 0:
    head_length=(R*86400*365.25*1000*0.002)*y_scale/2
    h_rch1 = (hl**2-(hl**2-hr**2)/L*(L*0.25)+(R/K*(L*0.25)*(L-(L*0.25))))**0.5  #water level at arrow for Recharge Posotion 1
    ax.arrow(L*0.25,(h_rch1+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch2 = (hl**2-(hl**2-hr**2)/L*(L*0.50)+(R/K*(L*0.50)*(L-(L*0.50))))**0.5  #water level at arrow for Recharge Postition 2
    ax.arrow(L*0.50,(h_rch2+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)
    h_rch3 = (hl**2-(hl**2-hr**2)/L*(L*0.75)+(R/K*(L*0.75)*(L-(L*0.75))))**0.5  #water level at arrow for Recharge Position 3
    ax.arrow(L*0.75,(h_rch3+head_length), 0, -0.01, fc="k", ec="k", head_width=(head_length*300/y_scale), head_length=head_length)

#Groundwater divide
max_y = max(h)
max_x = x[h.argmax()]
R_min_ms=K*abs(hl**2-hr**2)/L**2
if R>R_min_ms:
    plt.vlines(max_x,0,max_y, color="r")

plt.ylim(hl*(1-y_scale/100),hr*(1+y_scale/100))
plt.xlim(-50,L+50)
plt.text(L, (hr*(1+y_scale/100))-0.1*y_range, r'GWN: {:.3e} m/s '.format(R), horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='azure'),fontsize=12)
ax.grid()
st.pyplot(fig)