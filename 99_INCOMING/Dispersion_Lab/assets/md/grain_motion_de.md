### Dem Druckgefälle folgen, nicht nur der Abwärtsrichtung

Das Kornnetzwerk beschreibt eine druckgetriebene Strömung. Für jede Verbindung gilt im Code

$$
Q_{ij}=g_{ij}(P_i-P_j),\qquad g_{ij}>0.
$$

Ein Teilchen folgt dem ausströmenden Wasser; daher nimmt der Druck entlang jeder durchlaufenen Verbindung ab. Bei heterogenen Leitwerten kann ein Nachbarknoten mit geringerem Druck auf der Zeichnung etwas **weiter oben** liegen. Das ist ein lokaler Umweg, keine Bewegung gegen die berechnete Strömung. Die Abwärtskoordinate beschreibt die Strecke entlang des Bretts und ist kein Term der geodätischen Höhe. Die druckgetriebene Netzwerkformulierung ist in der [OpenPNM-Transportdokumentation](https://openpnm.org/examples/tutorials/08_simulating_transport.html) erläutert; unsere App verwendet einen eigenen Löser und die angegebenen vereinfachten Randbedingungen.

### Eine langsame Verbindung kann wie ein Stillstand wirken

Die Durchlaufzeit einer Verbindung ist das wassergefüllte Porenkanalvolumen geteilt durch den Durchflussbetrag:

$$
\tau_e=\frac{\pi r_e^2 L_e}{|Q_e|}.
$$

Ein kleiner, aber von null verschiedener Durchfluss kann daher eine lange, endliche Durchlaufzeit erzeugen. Zwischen den Knotenzeiten wird die Bewegung kontinuierlich interpoliert. Die Animation umfasst die späteste Ankunft des gesamten Laufs. Bei vielen Teilchen kann ein seltener langsamer Weg dazu führen, dass die meisten früh ankommen und einige langsam weiterlaufen. Überlagerte blaue Punkte können einzelne Bewegungen zusätzlich verdecken.

**Einen Weg prüfen:** Pausieren Sie, nutzen Sie Vorheriger Schritt / Nächster Schritt und öffnen Sie unten die Wegdetails. Die Tabelle enthält Knotendruck und Durchlaufzeit der Verbindung. Auch bei einem Aufwärtsschritt muss der Druck abnehmen. Geprüft werden positive Laufzeiten, keine wiederholten Knoten, Ankunft an einem Auslass und Massenerhaltung. Dies überprüft das idealisierte Netzwerk, nicht dessen Eignung für einen gemessenen Boden. Festhalten, Sorption oder Diffusion in immobile Poren wurden nicht ergänzt.

### Warum die meisten Teilchen früh in der Darstellung ankommen können

Die Wiedergabe im Kornnetzwerk beginnt jetzt mit **60 Bildschirmsekunden**. Die Modellzeit verläuft weiterhin linear von null bis zur spätesten Ankunft. Eine seltene, sehr langsame Verbindung kann diese Zeitspanne vergrößern; eine längere Darstellung beseitigt den Unterschied der physikalischen Laufzeiten nicht.

Eine reproduzierbare Prüfung mit 20 Reihen, a = 1 mm, Korngrößenfaktor 0,75, Variation 0,25, Druckdifferenz 0,5 Pa, Kornstartwert 7, Teilchenstartwert 42, Impulszugabe und 10.010 Teilchen ergab einen Median von etwa **423 s**, ein 95. Perzentil von **772 s** und eine späteste Ankunft von **5.897 s**. Das späteste Teilchen machte **keinen Aufwärtsschritt**. Es verbrachte etwa **90 %** seiner Durchlaufzeit in einer einzigen abwärts gerichteten Verbindung mit nur 0,000051 Pa Druckabfall. Kein Stichprobenweg besuchte einen Knoten erneut.

In dieser Stichprobe sind 95 % der Teilchen nach etwa **7,9 Bildschirmsekunden** der 60-Sekunden-Darstellung angekommen, gegenüber etwa 1,0 Bildschirmsekunde bei acht Sekunden Wiedergabe. Andere Startwerte und Einstellungen liefern andere Werte. Die unabhängig geprüfte Drucklösung und die Laufzeitgleichungen stützen die Erklärung durch geringen Durchfluss, nicht durch eine Endlosschleife. Molekulare Diffusion und Austausch mit immobilen Poren sind nicht enthalten; der späte Verteilungsausläufer ist keine kalibrierte Vorhersage für einen realen Boden. Nutzen Sie Pause und die Knotenschritte zur Betrachtung einzelner Passagen.
