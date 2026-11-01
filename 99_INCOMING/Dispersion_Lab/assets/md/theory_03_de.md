### Durchlaufzeit und Freisetzungszeit sind unterschiedliche Größen

Im Modus mit variablen Laufzeiten sind die Schrittzeiten unabhängige, positive lognormale Zufallsgrößen mit Mittelwert **μ** und Variationskoeffizient **c = Standardabweichung / Mittelwert**. Richtung und Schrittzeit werden unabhängig gezogen. Für eine standardnormalverteilte Größe Z verwendet der Code

$$
\tau=\mu\exp\!\left(\sigma_\ell Z-\frac{\sigma_\ell^2}{2}\right),\qquad \sigma_\ell^2=\ln(1+c^2).
$$

Damit gelten E[τ] = μ und Var(τ) = μ²c². Für die **Durchlaufzeit** T, gemessen von der individuellen Freisetzung bis zum Sammeln, folgt

$$
T=\sum_{j=1}^n\tau_j,\qquad \mathrm{E}[T]=n\mu,\qquad \mathrm{Var}(T)=n\mu^2c^2.
$$

Dies ist ein bewusst einfacher Random Walk, konzeptionell mit klassischen Zufallsschritt-Beschreibungen verwandt (Saffman, 1959). Die Lognormalverteilung ist eine didaktische Annahme, kein empirisches Gesetz für alle Böden. Korrelationen realer Porenströmungsgeschwindigkeiten können wichtig sein; korrelierte Continuous-Time Random Walks berücksichtigen diese zusätzliche Struktur (de Anna et al., 2013).

### Auch eine längere Zugabe verbreitert die Ankunftszeiten

**R** bezeichnet die Freisetzungszeit, **d** die Zugabedauer. R wird unabhängig von Weg und Durchlaufzeit gleichverteilt auf [0,d] gezogen; für einen Impuls ist R = 0. Die **Ankunftszeit** A wird seit Beginn der gesamten Zugabe gemessen:

$$
A=R+T,\qquad \mathrm{E}[A]=\frac d2+\mathrm{E}[T],\qquad
\mathrm{Var}(A)=\frac{d^2}{12}+\mathrm{Var}(T).
$$

Soweit Wahrscheinlichkeitsdichten existieren, ist die Ankunftsverteilung die Faltung von Freisetzungs- und Durchlaufzeitverteilung:

$$
f_A(t)=\int_0^t f_R(s)f_T(t-s)\,\mathrm{d}s.
$$

Bei fester Durchlaufzeit entsteht eine zeitlich verschobene Kopie des Zugabesignals. Eine endliche Zugabe kann die Auslasskurve somit **ohne Durchlaufzeitdispersion** verbreitern. Die App gibt mittlere Durchlaufzeit und mittlere Ankunftszeit getrennt an. Ein einzelner Balken für gleichzeitige Ankünfte stellt eine Punktmasse in einer endlichen Klasse dar; seine Höhe ist keine physikalische Spitzenkonzentration.

**Vorhersage:** Für n = 12, μ = 1 s und c = 0,6 beträgt die Durchlaufzeitvarianz 4,32 s². Eine Zugabedauer von 6 s erhöht die Ankunftszeitvarianz um weitere 3 s². Dies sind Populationswerte; kleine Stichproben schwanken.
