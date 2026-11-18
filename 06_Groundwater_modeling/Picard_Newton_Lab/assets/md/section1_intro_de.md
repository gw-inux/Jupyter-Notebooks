### Warum sind Picard- und Newton-Iterationen für die Grundwassermodellierung wichtig?

Stellen Sie sich vor, Sie untersuchen mit einem Grundwassermodell, wie sich ein Förderbrunnen auf einen ungespannten Grundwasserleiter auswirkt. Zunächst ergibt die Rechnung plausible hydraulische Höhen. Sie erhöhen die Förderrate. Plötzlich braucht das Modell wesentlich mehr Iterationen oder die Rechnung bricht ab. Wechseln Sie das Lösungsverfahren, kann die Rechnung wieder konvergieren, obwohl Sie weder die Eigenschaften des Grundwasserleiters noch die Randbedingungen geändert haben.

Wie lässt sich das erklären? Dazu müssen Sie wissen, warum das Modell die Berechnung wiederholt, weshalb eine stärkere Entnahme die Lösung erschweren kann und was die Konvergenzkriterien aussagen. Auch bei plausiblen Grundwasserständen kann die berechnete Wasserbilanz noch fehlerhaft sein. Umgekehrt kann das Strömungsproblem eine Lösung besitzen, selbst wenn ein Verfahren sie vom gewählten Startwert aus nicht findet.

**Picard und Newton verbessern schrittweise die geschätzten hydraulischen Höhen.** Beide Verfahren lösen dieselben Strömungsgleichungen. Sie unterscheiden sich darin, wie sie aus der aktuellen Näherung die nächste berechnen.

[Steffen Mehl (2006), *Use of Picard and Newton Iteration for Solving Nonlinear Ground Water Flow Equations*](https://doi.org/10.1111/j.1745-6584.2006.00207.x), zeigt die Unterschiede an einem Modell mit nur drei Zellen. An diesem Beispiel untersuchen wir, wann Newton besonders wirksam ist und weshalb die Wahl des Verfahrens von der jeweiligen Modellaufgabe abhängt.

### Lernziele

Vorausgesetzt werden Grundkenntnisse über die hydraulische Höhe (Standrohrspiegelhöhe), das Darcy-Gesetz, die hydraulische Leitfähigkeit sowie gespannte und ungespannte Grundwasserleiter. Kenntnisse numerischer Lösungsverfahren werden hier Schritt für Schritt aufgebaut.

Planen Sie für die Theorie und die kurzen Verständnisfragen **etwa 20–25 Minuten** ein. Anschließend können Sie

1. **erklären**, warum die Grundwasserströmungsgleichung nichtlinear sein kann und wie Picard und Newton im Drei-Zellen-Modell jeweils die nächste Näherung für die hydraulische Höhe berechnen,
2. **Iterationsdiagramme und Konvergenzkriterien interpretieren** und damit begründen, wann Newton schneller konvergieren kann und welche Rolle der Startwert spielt.

Für das **gesamte Modul mit beiden interaktiven Experimenten** sind etwa **60–75 Minuten** vorgesehen. Für weitere Szenarien oder die gemeinsame Diskussion der Fragen können Sie zusätzliche Zeit einplanen.
