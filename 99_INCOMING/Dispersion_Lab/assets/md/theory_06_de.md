### Hervorgehobene und Hintergrundteilchen tragen dieselbe Masse

H bezeichnet die Zahl hervorgehobener Teilchen (1–10), B die Zahl der Hintergrundteilchen je hervorgehobenem Teilchen (0–1000). Insgesamt gilt

$$
N=H(1+B),\qquad m_p=\frac1N.
$$

Es gibt H nummerierte und HB blaue Hintergrundteilchen, zusammen höchstens 10.010. Hintergrundteilchen sind unabhängige Stichproben desselben Transportprozesses, **keine Kopien** eines sichtbaren Wegs. Die Hervorhebung dient nur der Darstellung und beeinflusst weder Bewegung noch Masse.

Bei festem Teilchenstartwert erhält der numerische Rechenkern die Freisetzungszeiten und vollständigen Wege der ersten H Teilchen, wenn B geändert wird. Die Oberfläche erhöht bei erneutem Start normalerweise den Startwert für eine neue Realisierung; geben Sie zum Reproduzieren den notierten Startwert einer früheren Stichprobe ein. Abspielen wiederholt die aktuelle Stichprobe. Die normierte Gesamtzugabemasse bleibt 1; das statistische Gewicht jedes Teilchens wird daher zu 1/N. Dies erhöht die Stichprobenauflösung, nicht die physikalisch zugegebene Masse. Bei unabhängigen Stichproben nehmen typische Stichprobenfehler ungefähr mit N⁻¹ᐟ² ab; mehr Teilchen erzeugen keine stärkere Dispersion.

### Die Grafiken als Massenverteilungen lesen

Zu jeder Zeit zerlegt das Modell alle Teilchen in drei disjunkte Gruppen:

$$
N_{\mathrm{waiting}}+N_{\mathrm{inside}}+N_{\mathrm{collected}}=N.
$$

Die räumlichen Balken zeigen die gesammelte Masse je Auslass, $n_k/N$. In Zeitklasse b mit Breite $\Delta t_b$ beträgt die dargestellte Höhe

$$
h_b=\frac{n_b}{N\Delta t_b}.
$$

Ihre Einheit ist s⁻¹. Das vollständige Histogramm hat die Fläche 1; ein unvollständiges integriert sich zum bereits gesammelten Anteil. Es handelt sich um eine normierte Ankunftsmassenrate, nicht um eine residente Konzentration. Eine Umrechnung in Auslasskonzentration benötigte Zugabemasse und Wasserdurchfluss mit einer konsistenten flussgewichteten Mittelung. Diese Umrechnung ist hier nicht implementiert.

Die exakte Referenz beschreibt die Wahrscheinlichkeitsverteilung dieses Modells. Empirische Standardabweichungen werden passend zur dargestellten empirischen Verteilung mit Division durch N berechnet. Es sind keine N−1-Schätzer. Ein einzelnes Teilchen hat die empirische Breite null, auch wenn die Populationsbreite positiv ist. Zehn Teilchen helfen beim Verständnis der Wege, belegen aber keine glatte Verteilung.

### Modellgrenzen beachten

Nicht enthalten sind Sorption, Reaktion, Dichteeffekte, Kollisionen, explizite molekulare Diffusion und Diffusion in immobile Bereiche. Das Kornmodell vernachlässigt zusätzlich Speicherraum und hydraulischen Widerstand der Porenkörper sowie Geschwindigkeitsprofile in Porenverbindungen. Momentane Knotenmischung wird vorausgesetzt, nicht aufgelöst. Räumliche Ausbreitung, Umverteilung am Knoten und molekulare Homogenisierung sind daher unterschiedliche Prozesse (Dentz et al., 2023).

Parameteränderungen können mehrere Größen gleichzeitig beeinflussen: Der Gitterabstand verändert die Brettgröße, die Kornvariation neben der Variabilität auch die mittlere Größe und der Druck die Geschwindigkeit. Benennen Sie konstant gehaltene Größen, bevor Sie eine beobachtete Änderung einem einzelnen Mechanismus zuordnen.
