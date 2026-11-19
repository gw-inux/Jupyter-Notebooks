### Dalla legge di Darcy alla conduttanza

Consideriamo un collegamento uniforme di lunghezza $L$, conducibilità idraulica $K$ e sezione $A_\perp$ perpendicolare al flusso. Scegliamo come verso positivo quello dal punto $i$ al punto $j$. La legge di Darcy fornisce:

$$
Q=-K A_\perp\frac{h_j-h_i}{L}.
$$

| Simbolo | Significato | Unità |
|:--|:--|:--|
| $Q$ | Portata, positiva da $i$ verso $j$ | m³/s |
| $K$ | Conducibilità idraulica | m/s |
| $A_\perp$ | Area perpendicolare al flusso | m² |
| $h_i$, $h_j$ | Carichi idraulici nei due punti | m |
| $L$ | Distanza fra i punti | m |

Il segno negativo indica il flusso verso carichi decrescenti. Se $h_i>h_j$, il gradiente $(h_j-h_i)/L$ è negativo e $Q$ è positiva nel verso scelto.

Per il flusso orizzontale attraverso uno spessore saturo $b$ e una larghezza $w$, la sezione verticale dello schema tridimensionale è:

$$
A_\perp=w b.
$$

Raggruppiamo la proprietà del materiale e la geometria nella **conduttanza**, $C$:

$$
C=\frac{K A_\perp}{L}=\frac{K w b}{L},
\qquad
Q=-C(h_j-h_i).
$$

La conduttanza si misura in **m²/s**. Moltiplicandola per una differenza di carico in metri si ottiene una portata in m³/s. Non è quindi un altro nome della conducibilità idraulica: dipende anche da larghezza, spessore saturo e lunghezza del collegamento.

Pensate a due canali riempiti con la stessa sabbia. A parità di lunghezza e differenza di carico, quello saturo più largo lascia passare più acqua. La conducibilità non cambia, ma la conduttanza è maggiore.

Ad esempio, siano $K=10^{-4}$ m/s, $w=10$ m, $b=5$ m e $L=100$ m. Allora $A_\perp=50$ m² e $C=5\times10^{-5}$ m²/s. Con $h_i-h_j=2$ m si ottiene $10^{-4}$ m³/s, cioè **0.1 L/s**. Dimezzando lo spessore saturo a parità di tutte le altre grandezze e della differenza di carico, si dimezzano conduttanza e portata; la conducibilità resta invariata.

#### Collegare due celle adiacenti

Fra i centri di due celle l'acqua attraversa metà di ciascuna cella. Entrambe le metà oppongono resistenza. Per lunghezze uguali $\Delta x$ e larghezza comune $w$, le resistenze si sommano:

$$
\frac{1}{C_{ij}}
=\frac{\Delta x/2}{K_i w b_i}
+\frac{\Delta x/2}{K_j w b_j}.
$$

$C_{ij}$ è la conduttanza del collegamento; $K_i,K_j$ e $b_i,b_j$ sono conducibilità e spessori saturi delle due celle. Definendo le trasmissività $T_i=K_i b_i$ e $T_j=K_j b_j$, in m²/s:

$$
C_{ij}=\frac{2T_iT_j}{T_i+T_j}\frac{w}{\Delta x}.
$$

È l'espressione basata sulla media armonica delle trasmissività utilizzata nel modello a tre celle. Una semicella poco trasmissiva può limitare l'intero collegamento, come un restringimento limita il flusso in un canale più ampio. Con conducibilità e spessori uguali nelle due celle, si ritrova $C=Kwb/\Delta x$.
