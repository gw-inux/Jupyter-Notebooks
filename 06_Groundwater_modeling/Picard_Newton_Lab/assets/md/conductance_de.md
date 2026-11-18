### Vom Darcy-Gesetz zum hydraulischen Leitwert

Eine gleichförmige Strömungsverbindung habe die Länge $L$, die hydraulische Leitfähigkeit $K$ und die senkrecht zur Strömung durchströmte Fläche $A_\perp$. Als positive Richtung wählen wir die Richtung vom Ort $i$ zum Ort $j$. Das Darcy-Gesetz lautet

$$
Q=-K A_\perp\frac{h_j-h_i}{L}.
$$

| Symbol | Bedeutung | Einheit |
|:--|:--|:--|
| $Q$ | Volumenstrom, positiv von $i$ nach $j$ | m³/s |
| $K$ | Hydraulische Leitfähigkeit | m/s |
| $A_\perp$ | Durchströmte Fläche senkrecht zur Strömungsrichtung | m² |
| $h_i$, $h_j$ | Hydraulische Höhen an den beiden Orten | m |
| $L$ | Abstand zwischen den beiden Orten | m |

Das Minuszeichen beschreibt die Strömung in Richtung abnehmender hydraulischer Höhe. Für $h_i>h_j$ ist der Gradient $(h_j-h_i)/L$ negativ. In der gewählten positiven Richtung ergibt sich also $Q>0$.

Bei horizontaler Strömung durch eine gesättigte Mächtigkeit $b$ und über eine Breite $w$ ergibt sich die senkrechte Querschnittsfläche aus der dreidimensionalen Skizze zu

$$
A_\perp=w b.
$$

Wir fassen die Materialeigenschaft und die Geometrie zum **hydraulischen Leitwert** $C$ zusammen. Damit gilt

$$
C=\frac{K A_\perp}{L}=\frac{K w b}{L},
\qquad
Q=-C(h_j-h_i).
$$

Der Leitwert hat die Einheit **m²/s**. Multipliziert mit einer Höhendifferenz in Metern ergibt er einen Volumenstrom in m³/s. Sein Wert hängt sowohl von der hydraulischen Leitfähigkeit als auch von Breite, gesättigter Mächtigkeit und Länge der Verbindung ab.

Stellen Sie sich zwei mit demselben Sand gefüllte Rinnen vor. Bei gleicher Länge und gleicher Höhendifferenz fließt durch die breitere gesättigte Rinne mehr Wasser. Beide Rinnen haben dieselbe hydraulische Leitfähigkeit, die breitere hat jedoch den größeren Leitwert.

Ein Zahlenbeispiel: Für $K=10^{-4}$ m/s, $w=10$ m, $b=5$ m und $L=100$ m ergeben sich $A_\perp=50$ m² und $C=5\times10^{-5}$ m²/s. Bei $h_i-h_j=2$ m beträgt der Volumenstrom $10^{-4}$ m³/s, also **0,1 L/s**. Halbiert sich allein die gesättigte Mächtigkeit, halbieren sich bei gleicher Höhendifferenz sowohl der Leitwert als auch der Volumenstrom. Die hydraulische Leitfähigkeit bleibt gleich.

#### Die Verbindung zwischen zwei Nachbarzellen

Auf dem Weg von einem Zellzentrum zum nächsten durchströmt das Wasser jeweils eine halbe Zelle. Jede Hälfte trägt zum Strömungswiderstand bei. Bei gleicher Zelllänge $\Delta x$ und gemeinsamer Breite $w$ addieren sich die Widerstände zu

$$
\frac{1}{C_{ij}}
=\frac{\Delta x/2}{K_i w b_i}
+\frac{\Delta x/2}{K_j w b_j}.
$$

Dabei ist $C_{ij}$ der Leitwert der Verbindung. $K_i,K_j$ sind die hydraulischen Leitfähigkeiten und $b_i,b_j$ die gesättigten Mächtigkeiten in den beiden Zellen. Mit den Transmissivitäten $T_i=K_i b_i$ und $T_j=K_j b_j$ in m²/s folgt

$$
C_{ij}=\frac{2T_iT_j}{T_i+T_j}\frac{w}{\Delta x}.
$$

Das Drei-Zellen-Modell verwendet also das harmonische Mittel der beiden Transmissivitäten. Eine schlecht durchlässige Zellhälfte kann den Durchfluss durch die gesamte Verbindung begrenzen, ähnlich einer Engstelle in einer sonst breiten Rinne. Haben beide Zellen dieselbe Leitfähigkeit und Mächtigkeit, vereinfacht sich der Ausdruck zu $C=Kwb/\Delta x$.
