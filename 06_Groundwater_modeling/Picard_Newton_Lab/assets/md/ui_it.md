## title
Picard e Newton · Laboratorio iterativo del flusso sotterraneo
## page_title
Laboratorio Picard e Newton
## s1
01 · Dal bilancio idrico all'iterazione
## s2
02 · Modello idealizzato a tre celle
## s3
03 · Undici celle: complessità crescente
## preset
Configurazioni suggerite
## locked_preset_help
I casi di Mehl (2006) usano le impostazioni pubblicate di acquifero ed evapotraspirazione. Per abilitare questi interruttori nelle impostazioni generali, scegliete uno dei tre casi modificabili confinati o liberi.
## et_preset
Libero · con evapotraspirazione
## left
Carico assegnato a sinistra (m)
## right
Carico assegnato a destra (m)
## kl
K, cella sinistra (m/s)
## kc
K, cella centrale (m/s)
## kr
K, cella destra (m/s)
## initial
Carico centrale iniziale (m)
## unconfined
Acquifero libero
## et_enable
Attiva l'evapotraspirazione nella cella centrale
## et_surface
Quota della superficie di ET (m)
## et_depth
Profondità di estinzione (m)
## et_max
Tasso massimo di ET (mm/anno)
## recharge
Ricarica uniforme (mm/anno)
## omega
Fattore di smorzamento ω
## omega_help
1 = passo completo. Un valore minore riduce la correzione proposta, senza garantire la convergenza.
## reset
Reimposta
## reset_notice
Impostazioni del modello modificate: storici iterativi riavviati.
## ready
Stima iniziale
## running
Iterazione in corso
## converged
Convergenza raggiunta
## singular
Sistema lineare singolare; reimpostare o cambiare il carico iniziale
## dry
Passo rifiutato: carico al fondo dell'acquifero o inferiore
## cycle
Rilevato un ciclo di due passi; reimpostare o cambiare il carico iniziale
## limit
Limite di iterazioni raggiunto
## diverged
Carico proposto non finito o eccessivamente grande
## status
{method}: {status} · passi accettati: {steps}
## reference
Carichi di riferimento · confronto analitico
## no_reference
Per queste impostazioni non è stata verificata indipendentemente una soluzione con celle non asciutte. Rivedete i parametri.
## maps
Premere per approfondire il diagramma a ragnatela
## scalar_caption
Leggete il carico attuale sull'asse orizzontale. Le linee arancioni sottili punteggiate collegano gli ingressi alla costruzione; i segmenti continui mostrano la ragnatela di Picard o le tangenti di Newton. Picard trasferisce ogni aggiornamento accettato sulla diagonale. Il segmento verticale al carico attuale raggiunge la funzione dall'alto o dal basso e ne mostra la valutazione senza accettare un altro passo. Newton segue la tangente del residuo fino a zero. Gli assi restano fissi salvo lo zoom, che cambia solo la vista.
## coupled_caption
Il pannello di Picard a undici celle mostra l'ultima costruzione accettata sulla propria funzione del sistema completo. La funzione cambia con gli altri carichi; gli storici conservano tutti i valori accettati. Il residuo ridotto di Newton è fisso per questo modello e può mostrare tutte le tangenti accettate.
## residuals
Convergenza: variazione di carico e residuo di portata
## residual_caption
Verde = Picard; blu = Newton. Quadrati = residuo di portata (asse e soglia destri, viola); cerchi = variazione di carico (sinistri, ocra). Entrambi gli assi logaritmici restano fra 1E-12 e 100. Devono valere max|Δh| < {head_tol:.0e} m e max|F| < {flow_tol:.0e} m³/s. A k = 0 non esiste una variazione di carico. I triangoli segnalano valori sotto (▼, incluso zero) o sopra (▲) la vista. Le soglie esterne restano valide. Queste misure non sono errori rispetto al carico di riferimento.
## head_history
Storico del carico nella cella {cell}
## head_history_caption
Carico effettivo dopo ogni aggiornamento accettato, con stima iniziale a k = 0. Il riferimento indipendente è una guida visiva, non un criterio di arresto. k conta aggiornamenti accettati, non passi temporali.
## off
ET assente
## linear
Intervallo lineare di ET
## maximum
ET massima
## gradient
Aumenta il gradiente · carico destro a 0.5 m
## heterogeneous
Aggiungi tre zone di conducibilità
## zone1
Zona 1 · celle 1–5 · K (m/s)
## zone2
Zona 2 · cella 6 · K (m/s)
## zone3
Zona 3 · celle 7–11 · K (m/s)
## cell
Cella da esaminare (interne 2–10)
## initial_mode
Profilo iniziale dei carichi
## initial_linear
Lineare fra i contorni
## initial_uniform
Carico interno uniforme
## uniform_value
Carico iniziale interno uniforme (m)
## assess
Verifica la comprensione
## assessment_info
Selezionate tutte le affermazioni corrette (una o più). Qui si assegna un punto soltanto per ogni opzione corretta selezionata. Opzioni non selezionate o errate non danno punti; non vi sono penalità. La risposta è pienamente corretta solo se sono selezionate tutte le opzioni corrette e nessuna errata. Nello schema OPAL/ONYX adottato in questo corso si assegna un punto anche per ogni opzione errata correttamente lasciata non selezionata.
## check
Verifica la risposta
## score
Punti per selezioni corrette: {score}/{total}
## answer_full
Pienamente corretta
## answer_partial
Parzialmente corretta
## answer_wrong
Errata
## assessment_details
Opzioni errate selezionate: {incorrect}. Opzioni corrette ancora mancanti: {missing}. Il solo punteggio non dimostra la piena correttezza.
## theory_quiz
Fondamenti
## three_quiz
Bilancio e iterazione a tre celle
## references
Riferimenti e ambito del modello
## confined_preset
Confinato · senza evapotraspirazione
## unconfined_preset
Libero · senza evapotraspirazione
## learn_theory
Approfondimento · derivare Picard e Newton
## notes_three
Approfondimento · ipotesi ed esperimenti suggeriti
## notes_grid
Approfondimento · modello completo e aggiornamenti accoppiati
## learn_three
Esplora · modello a tre celle ed evapotraspirazione
## learn_grid
Esplora · undici celle e complessità crescente
## language_proxy
Contenuti disponibili in inglese, tedesco, francese, spagnolo, italiano, hindi, arabo e cinese semplificato. Le traduzioni mancanti sono sostituite dall'inglese.
## closure
Criteri di convergenza
## head_closure
Tolleranza sulla massima variazione di carico (m)
## flow_closure
Tolleranza sul massimo residuo di portata (m³/s)
## closure_help
Entrambi i controlli devono essere soddisfatti. Valori predefiniti: 1E-4 m e 1E-6 m³/s. Nei casi di Mehl (2006) a piccole portate, il residuo può essere accettabile prima che il carico si stabilizzi. Cambiare le soglie rivaluta l'iterata salvata e può riavviare il calcolo.
## sync
Sincronizza
## sync_help
Inizialmente disattivo: ogni pulsante avanza il proprio metodo. Attivatelo per raggruppare i due pulsanti; uno qualsiasi dei pulsanti attivi avanza entrambi i metodi disponibili. I metodi convergenti o arrestati restano invariati.
## to_closure
Esegui fino a convergenza
## to_closure_help
Scegliete il calcolo completo e premete un pulsante attivo. Questo interruttore da solo non esegue né reimposta il modello. Con sincronizzazione, entrambi i metodi disponibili proseguono fino a convergenza o a una condizione di arresto diagnosticata.
## play_method
▶ {method}
## converged_method
✓ {method}
## stopped_method
■ {method}
## play_help
Tenta un aggiornamento per {methods}.
## run_help
Prosegui {methods} fino a convergenza o a una condizione di arresto.
## stopped_help
{method}: {status}.
## outside_view
{method}: il carico attuale di {head:.3f} m è fuori vista. Il valore numerico è conservato nello storico.
## advanced
Opzione avanzata · smorzamento
## advanced_help
Lo smorzamento moltiplica la correzione proposta per ω. Un valore inferiore a 1 accorcia il passo; può favorire la convergenza, ma non la garantisce.
## conductivity_help
Scegliete 1 o 5 per ogni ordine di grandezza: 10⁻⁶, 5×10⁻⁶, …, 10⁻³ m/s.
## fig_cell
Cella {cell}
## fig_cell_number
Numero di cella
## fig_specified
Carico assegnato
## fig_final
Carico di riferimento
## fig_top
Tetto dell'acquifero: {top:g} m
## fig_bottom
Fondo: {bottom:g} m
## conductance_heading
1 · Dalle differenze di carico alle portate
## balance_heading
2 · Formulare il bilancio idrico
## picard_heading
3 · Riorganizzare il bilancio per Picard
## newton_heading
4 · Linearizzare il bilancio per Newton
## compare_heading
Esempi di Mehl (2006)
## convergence_heading
Decidere quando arrestare il calcolo
## fig_optional_et
ET opzionale
## fig_recharge
Ricarica
## current_head
Carico attuale: **{head:.3f} m**
## zoom
Zoom automatico
## zoom_auto
Zoom automatico
## zoom_manual
Zoom manuale
## zoom_help
Centra l'intersezione con la diagonale (Picard) o con lo zero (Newton). Inizialmente il carico attuale si trova a due terzi della distanza dal centro al bordo vicino. La larghezza resta fissa finché la distanza dal centro scende sotto il 25 % della semilarghezza; aumenta se il carico esce dalla finestra. L'ampiezza minima totale è 0.001 m. Disattivate lo zoom automatico per la vista completa o usate − Zoom / + Zoom per ampiezze manuali. Cambiare input o carichi iniziali ripristina la vista completa. Lo zoom non modifica i carichi calcolati.
## zoom_in
+ Zoom
## zoom_out
− Zoom
## zoom_in_help
Zoom manuale: seleziona l'ampiezza totale immediatamente minore fra 1, 0.1, 0.01, 0.001, 1E-4 e 1E-5 m. Disattiva l'automatismo e mantiene l'ampiezza fra iterazioni, con intersezione centrata. Cambiare input o carichi iniziali ripristina la vista completa.
## zoom_out_help
Riduzione manuale: seleziona l'ampiezza totale immediatamente maggiore fra 1E-5, 1E-4, 0.001, 0.01, 0.1 e 1 m. Disattiva l'automatismo e mantiene l'ampiezza fra iterazioni, con intersezione centrata. Cambiare input o carichi iniziali ripristina la vista completa.
## general_settings
Impostazioni generali del modello
## initial_boundary
Condizioni iniziali e al contorno
## aquifer_parameters
Parametri dell'acquifero e di ET
## uniform_k
K uniforme (m/s)
## grid_quiz
Iterazione accoppiata e non linearità
## paper_case
Coppia di figure di Mehl (2006)
## paper_smooth
Bilancio regolare libero · figure 2 e 3
## paper_et
Bilancio a tratti con ET · figure 5 e 6
## true_head_column
h di riferimento (m)
## hydraulic_parameters
Parametri dell'acquifero
## mehl_smooth_preset
Mehl (2006) · libero senza ET · figure 2 e 3
## mehl_et_preset
Mehl (2006) · libero con ET · figure 5 e 6
## use_paper_case
Usa questo caso di Mehl (2006) nella sezione 2
## initial_picard
Carico centrale iniziale · Picard (m)
## initial_newton
Carico centrale iniziale · Newton (m)
## mehl_conductivity
| Cella | K (equivalente in m/giorno) |
|:--|--:|
| 1 | {kl:g} |
| 2 | {kc:g} |
| 3 | {kr:g} |
## mehl_k_help
Le conducibilità dell'articolo sono interpretate in m/giorno e convertite internamente in m/s, come nella sezione 1.
## fig_display_top
Limite grafico: {top:g} m
## model_preview
Anteprima del modello
## head_check_wait
Controllo della variazione di carico: disponibile dopo il primo passo.
## head_check
Max |Δh| = {value:.2e} m; soglia {threshold:.0e} m — {result}.
## flow_check
Max |F| = {value:.2e} m³/s; soglia {threshold:.0e} m³/s — {result}.
## criterion_met
✓ soddisfatto
## criterion_unmet
non ancora soddisfatto
## fig_residual_method
{method} · residuo di portata
## fig_change_method
{method} · variazione di carico
## fig_head_method
{method} · carico
## fig_true_head_history
Carico di riferimento ({head:.3f} m)
## fig_flow_closure
Tolleranza di portata ({value:.0e} m³/s)
## fig_head_closure
Tolleranza di carico ({value:.0e} m)
## fig_head_axis
Carico nella cella {cell} (m)
## slider_input
Usa il cursore per il carico iniziale
## iteration_summary
**h = {head:.3f} m** · k = {steps} · {status}
## analytical_head_column
h analitico (m)
## analytical_difference_column
Riferimento − analitico (m)
## analytical_unavailable
Il confronto analitico omogeneo non è disponibile con conducibilità eterogenea o ET.
## coupled_map_help
La curva blu di Newton mostra lo squilibrio della cella selezionata equilibrando le altre otto celle a ogni carico di tentativo. Ne risulta una curva fissa per quella cella e configurazione. Il punto arancione indica la stima attuale. Ogni tangente raggiunge la proposta completa di Newton; lo smorzamento può accorciare il passo accettato. Il grafico di convergenza usa gli squilibri ai nove carichi effettivi.

Il pannello di Picard mostra l'ultimo aggiornamento accettato dei nove carichi. Curva verde e intersezione con la diagonale possono muoversi al variare degli altri carichi. Se il carico selezionato cambia pochissimo, la curva mantiene fissi gli altri ingressi. Gli storici conservano tutti i carichi accettati.
## fig_step_fraction
Frazione di passo $\alpha$
## fig_iteration_axis
Iterazione $k$
## fig_head_detail
Vicino al riferimento · < 1 cm
## postprocessing
Opzioni di postprocessamento
## side_by_side
Mostra i grafici affiancati
## fig_zoom_range
{mode} su intervallo di carico di {width:.3g} m
## foundations_quiz
Perché occorre iterare
## conductance_quiz
Conduttanza e flusso di Darcy
## balance_quiz
Bilancio idrico e non linearità
## et_quiz
Evapotraspirazione della falda
## picard_quiz
Iterazione di Picard
## newton_quiz
Iterazione di Newton
## mehl_quiz
Interpretare gli esempi di Mehl (2006)
## author_credit
Sviluppato da **Thomas Reimann** (2026) · TUD Dresden University of Technology · The Groundwater Project · basato su [Mehl (2006)](https://doi.org/10.1111/j.1745-6584.2006.00207.x)
