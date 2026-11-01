### Was die Modelle zeigen können

Das Galtonbrett zeigt, wie wiederholte Wegentscheidungen Querausbreitung erzeugen. Unabhängige variable Laufzeiten ergänzen die Trennung in Fließrichtung und eine Verteilung der Ankunftszeiten. Das Kornnetzwerk verknüpft Geometrie, Strömung, Wegwahrscheinlichkeiten und Laufzeiten über ein nachvollziehbares hydraulisches Ersatzmodell.

### Welche Annahmen bleiben

- Der gelöste Stoff ist konservativ und passiv. Sorption, Reaktion, Dichteeffekte und Teilchenkollisionen werden nicht dargestellt.
- Das Galtonbrett ist ein stochastisches Transportanalogon; Starrkörperkollisionen und die Erdbeschleunigung werden nicht berechnet.
- Molekulare Diffusion und Geschwindigkeitsprofile innerhalb der Poren werden nicht aufgelöst. Vollständige Mischung an Netzknoten ist eine vorgegebene Modellannahme, keine Simulation molekularer Durchmischung.
- Die Kornpositionen liegen auf einem festen Gitter. Der Packungsparameter ändert Radien und Öffnungen, keine mechanische Umlagerung oder Verdichtung. Er ist keine gemessene Porosität.
- Ein anderer Gitterabstand ändert Korngröße **und Gebietsabmessungen**. Dies ist kein isoliertes Korngrößenexperiment bei fester Säulengröße.
- Das dreieckige Netzwerk besitzt einen Einlass und mehrere Auslässe mit gleichem Druck. Seine Strömungsverteilung enthält Einflüsse dieser Geometrie und Randbedingungen.
- Kreisförmige Röhren nähern Porenverengungen an; Porenkörper haben weder Speicher noch Widerstand. Die hydraulische Bilanz ist überprüfbar, das Netzwerk aber nicht für einen realen Boden kalibriert.
- Aus den Grafiken wird keine Dispersivität abgeleitet. Räumliche Breite, zeitliche Breite und Dispersionskoeffizient sind unterschiedliche Größen. Ausbreitung allein belegt keine molekulare Durchmischung.
- Endliche Stichproben schwanken. Exakte Referenzkurve und Tabelle gelten für dieses mathematische Modell; sie sind keine Feldbeobachtungen.

### Quellen und weiterführende Literatur

- [Yale Physics: Galton board](https://yppsweb2.its.yale.edu/physics/demos/demomain.asp?id=4G10.10&task=viewdemo) — das physische Links-/Rechts-Experiment und die binomialverteilten Auslässe.
- [Wexler (1992), USGS TWRI 3-B7](https://pubs.usgs.gov/publication/twri03B7) — analytischer Stofftransport und die Unterscheidung zwischen Advektion, Diffusion und mechanischer Dispersion.
- [Saffman (1959), A theory of dispersion in a porous medium](https://doi.org/10.1017/S0022112059000672) — klassischer Ansatz mit zufälligen Schritten unterschiedlicher Richtung und Dauer. Das vorliegende Modell bildet diese Theorie nicht vollständig nach.
- [OpenPNM: Simulating Single Phase Transport](https://openpnm.org/examples/tutorials/08_simulating_transport.html) — Leitwerte, Druckrandbedingungen und Grenzen einfacher Röhrenmodelle. Diese App enthält einen eigenen kleinen Netzwerklöser und benötigt OpenPNM nicht.
