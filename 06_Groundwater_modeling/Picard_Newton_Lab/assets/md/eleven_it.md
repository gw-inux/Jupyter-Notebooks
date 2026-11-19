**L'intero esperimento è accoppiato.** Le 11 celle hanno distanza fra centri di 100 m e larghezza di 1 m. I centri di contorno distano 1000 m; la ricarica entra nelle nove celle interne risolte. Il caso libero predefinito ha fondo a 0 m, tetto a 30 m, carichi al contorno di 18 e 8 m e conducibilità di 1E-4 m/s. Il confronto confinato resta uno strato di 20 m, da −20 a 0 m. Un tetto più alto modifica il problema fisico quando i carichi raggiungono il tetto precedente: non è soltanto una scelta grafica.

La conduttanza integra lo spessore saturo e usa conducibilità armonica. Con $\Phi'(h)=b(h)$, la portata attraverso una faccia è:

$$Q_{i+1/2}=K_{i+1/2}\frac{w}{\Delta x}\left[\Phi(h_i)-\Phi(h_{i+1})\right].$$

Sotto il tetto, $\Phi=(h-z_b)^2/2$; sopra, il potenziale è lineare con pendenza uguale allo spessore totale. Con K e ricarica fissi, le equazioni discrete sono lineari nel potenziale, ma restano non lineari nel carico. Zone di conducibilità fissa non impediscono questa trasformazione.

**Il pannello di Picard** mostra l'ultima costruzione accettata dell'intero sistema sulla propria funzione verde. Ogni passo possiede una funzione lungo la propria direzione completa di aggiornamento. Funzioni e percorsi precedenti sono omessi perché differiscono da quello attuale; gli storici conservano tutti i carichi accettati. La guida punteggiata proietta il carico attuale dall'asse al valore della funzione. Se il carico selezionato cambia pochissimo, una sezione mantiene fissi gli altri carichi di ingresso, evitando una divisione per un cambiamento molto piccolo. Una funzione piatta su una sezione è possibile e non dimostra la linearità dell'intero problema vettoriale.

**Il pannello di Newton** mostra il residuo ridotto della cella selezionata in m³/s. Eliminando gli altri otto bilanci dalla legge di flusso utilizzata si ottiene:

$$f_{N,i}(h_i)=F_i^{\mathrm{red}}(h_i)=c_i-S_i\Phi(h_i),\qquad (F_i^{\mathrm{red}})'=-S_i b(h_i).$$

$c_i$ è il termine sorgente efficace (m³/s) e $S_i$ un fattore positivo (m/s) determinato dai collegamenti ai due contorni. Entrambi sono fissi per cella e configurazione. Per ogni carico di tentativo della curva blu, gli altri otto carichi assumono valori che equilibrano le rispettive celle. Ripetere lo stesso carico restituisce quindi la stessa ordinata blu a ogni iterazione.

Il punto arancione valuta la curva al carico attuale. La tangente la tocca al carico usato per quel passo; la sua intercetta fornisce la proposta completa di Newton per la cella. Lo smorzamento ne accetta una frazione. Mantenendo invece i vicini alle stime attuali e variando solo il carico selezionato, si otterrebbe una curva locale che potrebbe spostarsi fra iterazioni. Il grafico di convergenza valuta i nove bilanci originali alle stime effettive. Nella sezione 2 è incognito solo il carico centrale: la curva $f_N(h)=F(h)$ discende direttamente dal suo bilancio.

La tabella confronta i casi omogenei con la soluzione analitica 1D indipendente ai centri. La formula omogenea non viene applicata ai casi eterogenei. Le portate di faccia sono a x = 50, 150, …, 950 m; l'uscita netta bilancia la ricarica sulle nove aree interne.

L'asse sinistro della convergenza mostra la massima variazione di carico, il destro il massimo residuo. Entrambi vanno da 1E-12 a 100. Gli storici lasciano spazio a un'iterazione oltre l'ultima accettata. Il dettaglio del carico compare solo dopo tre variazioni consecutive inferiori al centimetro vicino al riferimento. Entrambi i criteri restano necessari; il dettaglio non cambia tolleranze né storico.

**Zoom automatico** centra l'intersezione Picard/diagonale o lo zero del residuo di Newton. Al ridimensionamento, il carico attuale si trova a due terzi della distanza fra centro e bordo dal proprio lato. La larghezza resta invariata finché il carico entra nel 25 % interno della semilarghezza o esce dalla finestra. La larghezza totale minima è 0.001 m. L'intersezione di Picard può muoversi con gli altri carichi e differire dal riferimento finale; la finestra la segue mantenendo la larghezza.

**− Zoom / + Zoom** selezionano larghezze totali manuali di 1, 0.1, 0.01, 0.001, 1E-4 e 1E-5 m e disattivano il modo automatico. La larghezza resta fissa fra iterazioni e l'intersezione centrata. L'etichetta indica modalità e ampiezza. Riattivare lo zoom automatico avvia un nuovo adattamento; disattivarlo ripristina la vista completa. Cambiare input, carichi iniziali o smorzamento avvia un nuovo esperimento con entrambe le viste complete. Il postprocessamento permette grafici affiancati con controlli comuni oppure impilati a tutta larghezza con controlli e storici indipendenti. Queste scelte visive non modificano il modello né cancellano le iterate.
