### Unabhängige Entscheidungen erzeugen Querstreuung

An jedem Stift bewegt sich ein Teilchen eine Reihe vorwärts und entweder nach links oder rechts. Die Entscheidungen sind unabhängig und haben jeweils die Wahrscheinlichkeit 1/2. **n** bezeichnet die Reihenzahl, **a** die Quer- und Längsschrittweite. Nach **K** Rechtsentscheidungen ist die Auslassposition

$$
K\sim\mathrm{Binomial}(n,1/2),\qquad X_n=a(2K-n).
$$

Aus der Anzahl möglicher Entscheidungsfolgen ergeben sich die exakten Auslasswahrscheinlichkeiten:

$$
\Pr[X_n=a(2k-n)]=\binom{n}{k}2^{-n},\qquad k=0,\ldots,n.
$$

Mittelwert und Varianz folgen aus der Summe unabhängiger vorzeichenbehafteter Schritte:

$$
\mathrm{E}[X_n]=0,\qquad \mathrm{Var}(X_n)=na^2,\qquad \sigma_x=a\sqrt{n}.
$$

Dies ist die Münzwurfversion des von [Yale Physics](https://yppsweb2.its.yale.edu/physics/demos/demomain.asp?id=4G10.10&task=viewdemo) veranschaulichten Galtonbrett-Prinzips. Die endliche Verteilung ist **binomial**, nicht exakt normalverteilt. Mit mehr unabhängigen Schritten verbessert sich die Normalapproximation, insbesondere außerhalb der Verteilungsränder. Mehr Teilchen bilden dieselbe Verteilung deutlicher ab; ihre theoretische Breite ändert sich dadurch nicht.

### Was feste Schrittzeiten zeigen

Dauert jeder Schritt **μ** Sekunden, durchläuft jedes Teilchen das Brett in

$$
T=n\mu,\qquad \mathrm{Var}(T)=0.
$$

Ein momentaner Impuls verteilt sich somit auf verschiedene Auslässe, erreicht diese aber überall gleichzeitig. Zu ganzzahligen Schrittzeiten vor dem Sammeln gilt für die Populationsvarianz

$$
\mathrm{Var}[X(t)]=2D_{T,\mathrm{board}}t,\qquad D_{T,\mathrm{board}}=\frac{a^2}{2\mu}.
$$

Dies ist ein effektiver transversaler Random-Walk-Koeffizient des idealen Bretts. Zwischen Knoten interpoliert die App die Bewegung zur Darstellung linear; der sichtbare kontinuierliche Weg ist keine Brownsche Bewegung. Der Koeffizient ist keine angepasste Bodendispersivität. Bei festem n verändert a sowohl die Streuung als auch die Abmessungen des Bretts.

**Vorhersage:** Eine Verdopplung von n vergrößert die Populationsstandardabweichung um √2. Eine Verdopplung der Teilchenzahl lässt diesen Populationswert unverändert.
