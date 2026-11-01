### Galtonbrett: Ort und Zeit sind getrennte Mechanismen

Für n Reihen beträgt jeder unabhängige Querschritt +a oder −a mit Wahrscheinlichkeit 1/2. Mit K Entscheidungen nach rechts gilt

$$
K\sim\mathrm{Binomial}(n,1/2),\qquad X=a(2K-n),
$$

$$
\mathrm{E}[X]=0,\qquad \mathrm{Var}(X)=na^2.
$$

Das regelmäßige Brett hat die feste Schrittzeit μ. Im Modus mit variablen Zeiten ist jede Schrittzeit τ unabhängig lognormalverteilt mit Mittelwert μ und Variationskoeffizient c. Weg- und Zeitziehungen sind unabhängig. Die Parameter der Lognormalverteilung sind

$$
\sigma_\ell^2=\ln(1+c^2),\qquad m_\ell=\ln(\mu)-\sigma_\ell^2/2.
$$

Bei c = 0 verwendet der Code exakt feste Zeiten. Für die gesamte Durchlaufzeit T gilt

$$
\mathrm{E}[T]=n\mu,\qquad \mathrm{Var}(T)=n\mu^2c^2.
$$

Bei unabhängiger, zwischen 0 und der Dauer d gleichverteilter Freisetzungszeit R hat die Ankunftszeit A = R + T die Momente

$$
\mathrm{E}[A]=d/2+n\mu,\qquad \mathrm{Var}(A)=d^2/12+n\mu^2c^2.
$$

Für einen Impuls ist R = 0. Bei endlich vielen Schritten muss die Verteilung nicht gaußförmig sein. Eine zeitliche Streuung am Auslass ist noch kein longitudinaler Dispersionskoeffizient.

### Kornnetzwerk: Geometrie, Strömung, dann Transport

Die Porenknoten liegen auf demselben Rautengitter mit Quer- und Längsschritt a. Die Kornmittelpunkte bilden das duale Gitter. Ihr nächster Abstand beträgt √2a. Die Kornradien sind

$$
R_g=\frac{a}{\sqrt{2}}\,\kappa(1-vU_g),\qquad U_g\sim\mathrm{Uniform}(0,1),
$$

wobei κ der Packungsparameter und v die Korngrößenvariation ist. Die zulässigen Bereiche halten die Körner getrennt. Aus den beiden Körnern neben einer Verbindung folgen der äquivalente Röhrenradius und die Länge:

$$
r_e=\frac{\sqrt{2}a-R_{g1}-R_{g2}}{2},\qquad L_e=\sqrt{2}a.
$$

Diese Zuordnung ist eine ausdrücklich gewählte geometrische Lehrannahme. Die Kreisröhre ist ein Ersatz für den Strömungsweg, nicht der genaue Querschnitt zwischen realen Körnern. κ ist keine Porosität. Eine Erhöhung von v ändert auch den mittleren Kornradius; sie variiert nicht nur die Streuung bei festem Mittelwert.

Für die Wasserviskosität μw = 0,001 Pa s ergeben sich Hagen–Poiseuille-Leitwert und Durchfluss zu

$$
g_e=\frac{\pi r_e^4}{8\mu_wL_e},\qquad Q_{ij}=g_e(P_i-P_j).
$$

Am Einlass liegt das Druckpotenzial ΔP an, an jedem Auslass null. Alle inneren Knoten erfüllen

$$
\sum_j Q_{ij}=0.
$$

Nicht verbundene Außenränder sind undurchlässig. Die Darstellung zeigt ein ebenes Netzwerk von oben nach unten; die vertikale Koordinate ist keine geodätische Höhe. Das vorgegebene Druckpotenzial treibt die Strömung an. Ein zusätzlicher Schwerkrafteinfluss wird nicht berechnet.

An einem Knoten sind die Wahrscheinlichkeiten der ausgehenden Wege proportional zu den ausgehenden Wasserströmen. Dies setzt sofortige vollständige Durchmischung in einem Knoten ohne Aufenthaltsvolumen voraus. Jedes Teilchen bewegt sich mit der querschnittsgemittelten Geschwindigkeit durch die Verbindung:

$$
p_{ij}=\frac{Q_{ij}}{\sum_{k:Q_{ik}>0}Q_{ik}},\qquad
u_e=\frac{|Q_e|}{\pi r_e^2},\qquad
\tau_e=\frac{\pi r_e^2L_e}{|Q_e|}.
$$

Nur positive ausgehende Ströme gehen in die Wegwahrscheinlichkeit ein. Teilchen folgen immer abnehmendem Druck, auch wenn ein Weg auf dem Bildschirm örtlich nach oben führt. Durchflusslose Verbindungen werden nicht gewählt. Der Druck nimmt entlang eines Wegs strikt ab; daher sind keine Umläufe möglich.

Exakte Auslasswahrscheinlichkeiten und Laufzeitmomente werden unabhängig von der Teilchenstichprobe rekursiv im strömungsgerichteten Graphen berechnet. Die exakte mittlere Durchlaufzeit entspricht außerdem **durchströmtem Röhrenvolumen / Zufluss**. Dies ermöglicht numerische Verifikation, keine Validierung an einem realen Boden.

### Massenbilanz und Einordnung

Die normierte Gesamtmasse ist 1, die Teilchenmasse 1/N. Zu jeder Zeit gilt: noch nicht freigesetzte + im Brett befindliche + gesammelte Teilchen = N. Die räumlichen Balken zeigen gesammelte Masse je Auslass. Die Höhen des Ankunftszeit-Histogramms sind Anzahl/(N × Klassenbreite), in s⁻¹; das vollständige Histogramm integriert sich zu 1. Diese Größen sind keine im Porenraum vorliegenden Konzentrationen.

Die angezeigten Standardabweichungen verwenden den Divisor N (empirische Verteilung), nicht den Divisor N−1 des unverzerrten Schätzers. Die Tabellenreferenzen beschreiben die Modellpopulation. Ein einzelnes Teilchen hat zwangsläufig die empirische Streuung null, auch wenn die Streuung der Population positiv ist.
