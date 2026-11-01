### Von der Korngeometrie zum idealisierten hydraulischen Netzwerk

Die Version mit grauen Körnern verwendet ein dreieckiges Rautengitter von Porenknoten. Die Kornmittelpunkte liegen auf dessen dualem Gitter. Bei Gitterinkrement a beträgt der Abstand benachbarter Kornmittelpunkte √2a. Die Kornradien sind

$$
R_g=\frac{a}{\sqrt{2}}\kappa(1-vU_g),\qquad U_g\sim\mathrm{Uniform}(0,1).
$$

κ ist der **Korngrößenfaktor** (bisher Packungsparameter), v die Korngrößenvariation. Ein größeres κ verengt Öffnungen. Ein größeres v verbreitert die Radiusverteilung und verringert zugleich ihren Mittelwert, E[Rg] = aκ(1−v/2)/√2. Keiner dieser Parameter ist eine gemessene Porosität; die Kornmittelpunkte bleiben fest, eine mechanische Verdichtung findet nicht statt.

Für die beiden Körner neben einer Verbindung e wird der **Oberflächenabstand als Durchmesser einer kreisförmigen Röhre** angesetzt:

$$
r_e=\frac{\sqrt{2}a-R_{g1}-R_{g2}}2,\qquad L_e=\sqrt{2}a.
$$

Dies ist die geometrische Ersatzannahme der App, nicht die exakte Öffnung oder der Widerstand einer realen dreidimensionalen Pore. Porenkörper haben weder Speicherraum noch zusätzlichen Widerstand. Leitwertbasierte Netzwerke und einfache zylindrische Porenverbindungen beschreibt die offizielle OpenPNM-Dokumentation; diese App verwendet einen eigenen Löser.

### Erst Wasserströmung, dann Stofftransport

Für die dynamische Wasserviskosität $\mu_w$ = 0,001 Pa s ergeben sich Röhrenleitwert und vorzeichenbehafteter Durchfluss zu

$$
g_e=\frac{\pi r_e^4}{8\mu_wL_e},\qquad Q_{ij}=g_e(P_i-P_j),\qquad \sum_jQ_{ij}=0.
$$

Die letzte Gleichung gilt an jedem inneren Knoten. Am Einlass ist das Druckpotential ΔP, an allen Auslässen null. Über die äußeren Seiten gibt es keine Verbindungen. Die nach unten gerichtete Koordinate ist die Strecke in Fließrichtung, **keine geodätische Höhe**; Gravitation wird nicht zusätzlich angesetzt. Die Vorbereitungsvorschau bewegt keinen Stoff, berechnet aber bereits die stationäre Wasserströmung.

Ein ausgehender Weg wird entsprechend seinem Anteil am ausgehenden Durchfluss gewählt. Jede Verbindung wird mit der mittleren Querschnittsgeschwindigkeit durchlaufen:

$$
p_{ij}=\frac{Q_{ij}}{\sum_{k:Q_{ik}>0}Q_{ik}},\qquad
u_e=\frac{|Q_e|}{\pi r_e^2},\qquad \tau_e=\frac{\pi r_e^2L_e}{|Q_e|}.
$$

Dies setzt momentane vollständige Mischung an volumenlosen Knoten voraus. Molekulare Mischung und Geschwindigkeitsprofile in Röhren werden nicht simuliert. Die Wegwahl ist deshalb eine Modellannahme, keine Aussage, dass reale Porenknoten stets vollständig durchmischt sind. Die Strömung folgt abnehmendem Druck; eine Verbindung kann in der Zeichnung lokal nach oben zeigen, ohne eine Schleife zu bilden. Verbindungen ohne Durchfluss werden nicht gewählt.

### Unabhängige Modellreferenzen

Exakte Auslasswahrscheinlichkeiten und die ersten beiden Durchlaufzeitmomente werden rekursiv auf dem druckgerichteten Graphen berechnet. Für die erwartete verbleibende Durchlaufzeit mᵢ und ihr zweites Moment sᵢ, mit null an den Auslässen, gilt

$$
m_i=\sum_jp_{ij}(\tau_{ij}+m_j),\qquad
s_i=\sum_jp_{ij}(\tau_{ij}^2+2\tau_{ij}m_j+s_j).
$$

Die Varianz am Einlass ist s₀−m₀². Eine unabhängige Kontrolle ist m₀ = durchströmtes Röhrenvolumen / Zufluss. Unter der angegebenen Mischungsannahme entsprechen die Auslasswahrscheinlichkeiten den Wasserflussanteilen der Auslässe. Diese Prüfungen verifizieren die mathematische Implementierung; sie validieren die Geometrieannahme nicht anhand eines Bodens.

**Vorhersage:** Eine Verdopplung von ΔP verdoppelt Durchflüsse und halbiert Durchlaufzeiten; Wegwahrscheinlichkeiten bleiben gleich. Bei identischen Körnern verringert eine Halbierung aller Röhrenradien den Durchfluss um den Faktor 16 und erhöht die Durchlaufzeit bei festem Druck um den Faktor vier. Beachten Sie die ausgegebene Poren-Reynolds-Zahl Re = 2ρur/$\mu_w$ (ρ = 1000 kg/m³); bei Re nahe oder über 1 ist schleichende Strömung nicht gesichert.
