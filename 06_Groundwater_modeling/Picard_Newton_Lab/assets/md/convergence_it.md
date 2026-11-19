Una correzione piccola non basta: il bilancio può essere ancora insoddisfacente. Controllate **sia** la massima variazione assoluta di carico **sia** il massimo residuo assoluto di portata. Le tolleranze sono regolabili; i valori predefiniti sono rispettivamente $10^{-4}$ m e $10^{-6}$ m³/s.

**Perché un altro passo dopo che il residuo soddisfa il criterio?** L'ultima variazione di carico può ancora superare la propria soglia. In un problema lineare, il primo passo può raggiungere la soluzione con residuo nullo, ma con una grande variazione dalla stima iniziale. Un secondo passo senza cambiamento conferma il criterio sul carico. Nei casi di Mehl (2006) a piccole portate, anche la stima iniziale può rispettare 1E-6 m³/s pur presentando un errore di carico significativo. Il solo controllo della portata è quindi insufficiente.

Il grafico mostra la massima variazione di carico sull'asse logaritmico sinistro e il massimo residuo su quello destro. Entrambe le scale restano fra $10^{-12}$ e $100$ nelle rispettive unità. Il viola identifica asse e soglia della portata; l'ocra quelli della variazione di carico. I quadrati rappresentano residui, i cerchi variazioni di carico; verde e blu indicano rispettivamente Picard e Newton. I triangoli ai bordi segnalano valori esterni: verso il basso per quelli inferiori al limite, compreso zero, e verso l'alto per quelli superiori. Una tolleranza esterna alla vista rimane valida ed è riportata in legenda.

La variazione di carico si calcola fra iterazioni accettate; non si attribuisce un valore fittizio alla stima iniziale. Un grafico separato mostra il carico effettivo della cella selezionata e quello di riferimento. Quest'ultimo è un riferimento visivo: l'iterazione non utilizza l'errore rispetto alla soluzione nota come criterio di arresto.

Per una funzione scalare regolare di Picard, $|f'_P(h^*)|<1$ è una condizione sufficiente di convergenza locale: stime abbastanza vicine si avvicinano alla soluzione. $f'_P$ è la derivata adimensionale della funzione di aggiornamento rispetto al carico in ingresso. Una pendenza locale negativa alterna il segno dell'errore. Newton può convergere quadraticamente vicino a una radice regolare con derivata non nulla: l'errore residuo può ridursi molto rapidamente. Un carico iniziale inadatto o un cambio di tratto di ET possono impedire la convergenza. Nessun metodo è sempre superiore.

Con più carichi incogniti, ogni iterazione esterna risolve un sistema matriciale accoppiato:

$$\mathbf A(\mathbf h^k)\widehat{\mathbf h}_P^{k+1}=\mathbf b(\mathbf h^k),\qquad
\mathbf J(\mathbf h^k)\Delta\mathbf h=-\mathbf F(\mathbf h^k).$$

$\mathbf h^k$ è il vettore dei carichi interni attuali (m); $\widehat{\mathbf h}_P^{k+1}$ contiene quelli proposti da Picard (m) e $\Delta\mathbf h$ le correzioni di Newton (m). $\mathbf A$ contiene le conduttanze fisse e le pendenze attive delle condizioni al contorno (m²/s); $\mathbf b$ i corrispondenti termini di contorno e sorgente (m³/s). $\mathbf F$ contiene i residui delle celle (m³/s); $\mathbf J$ è la matrice jacobiana delle loro derivate rispetto ai carichi incogniti (m²/s).

Qui i sistemi lineari sono risolti direttamente. Non viene mostrata una storia di iterazioni interne del risolutore lineare.
