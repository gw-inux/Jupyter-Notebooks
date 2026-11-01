### Bezug zu Kontinuumsgleichungen des Stofftransports

Für ein gesättigtes Medium mit konstanter mobiler Porosität, stationärer inkompressibler Strömung, einen konservativen verdünnten Stoff und geeignete Mittelung ist die Advektions-Dispersions-Gleichung (ADE) eine übliche Kontinuumsbeschreibung:

$$
\frac{\partial C}{\partial t}+\mathbf{v}\cdot\nabla C
=\nabla\cdot(\mathbf{D}\nabla C).
$$

C ist die gelöste Konzentration, **v** die mittlere Porenwassergeschwindigkeit (nicht der Darcy-Fluss), **D** der Dispersionstensor. In einem homogenen Medium mit Strömung in z-Richtung, Querkoordinate x und konstanten Koeffizienten folgt

$$
\frac{\partial C}{\partial t}+v\frac{\partial C}{\partial z}
=D_L\frac{\partial^2C}{\partial z^2}+D_T\frac{\partial^2C}{\partial x^2}.
$$

Ein üblicher konstitutiver Ansatz ist $D_L$ = $\alpha_L$|v| + $D_{m,\mathrm{eff}}$ und $D_T$ = $\alpha_T$|v| + $D_{m,\mathrm{eff}}$. Dispersionskoeffizienten D haben die Einheit Länge²/Zeit, Dispersivitäten α die Einheit Länge. Die effektive molekulare Diffusion $D_{m,\mathrm{eff}}$ berücksichtigt Einschränkungen durch das poröse Medium. Diese Beziehungen dienen der Einordnung; das Modul löst diese ADE **nicht** und gibt $\alpha_L$ und $\alpha_T$ nicht vor (Wexler, 1992).

### Räumliche Varianz ist keine Ankunftszeitvarianz

Für einen Kontinuumsimpuls im unbegrenzten Raum mit konstanten Koeffizienten wächst die longitudinale Ortsvarianz mit $2D_Lt$. Für eine andere Beobachtungsgröße – die erstmalige Ankunft an einer absorbierenden Ebene im Abstand L bei Start bei null, stromaufwärts unbegrenztem Gebiet, konstantem v > 0 und $D_L$ – gelten die Momente

$$
\mathrm{E}[T]=\frac Lv,\qquad \mathrm{Var}(T)=\frac{2D_LL}{v^3}.
$$

Diese Identitäten setzen bestimmte Randbedingungen und Beobachtungsgrößen voraus (Probability Distribution Explorer, Inverse Gaussian distribution). Als mathematische Illustration ergäbe ein Abgleich mit den Galtonbrett-Momenten bei L = na und v = a/μ

$$
D_{L,\mathrm{moment}}=\frac{\mathrm{Var}(T)v^3}{2L}=\frac{a^2c^2}{2\mu}.
$$

Dies ist nur eine **Analogie durch Momentenabgleich**. Die Durchlaufzeitverteilung des Bretts wird dadurch nicht zur ADE-Erstankunftsverteilung; eine Summe lognormaler Schrittzeiten ist im Allgemeinen nicht invers-gaußverteilt. Das Modul zeigt deshalb Breiten und Momente, ohne diesen Ausdruck als geschätzten Bodendispersionskoeffizienten auszugeben. Selbst für diese Analogie muss bei endlicher Zugabe zunächst deren Beitrag von der Durchlaufzeitvarianz getrennt werden.

### Warum endliche Netzwerke nicht Ficksch sein müssen

Bijeljic und Blunt (2006) zeigen, dass eine asymptotische Dispersionsbeschreibung den Transport durch viele Poren erfordern kann; ihr Netzwerk berücksichtigt Advektion und molekulare Diffusion explizit. Das vorliegende Brett besitzt nur 2–40 Reihen in beiden konfigurierbaren Modellen und verwendet einfachere Physik. Ein glatt wirkendes Histogramm belegt weder ein asymptotisches Regime noch gaußförmigen Transport oder skalenunabhängige Dispersivität. Der einzelne Einlass, die sich verbreiternde Dreiecksgeometrie und die Auslässe mit gleichem Druck beeinflussen die Antwort des Kornnetzwerks.
