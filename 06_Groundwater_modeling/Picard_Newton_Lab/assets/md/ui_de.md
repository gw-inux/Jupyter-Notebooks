## title
Picard und Newton · Grundwasserströmung iterativ berechnen

## page_title
Picard und Newton · Grundwasserströmung

## s1
01 · Von der Wasserbilanz zur Iteration

## s2
02 · Ein idealisiertes Drei-Zellen-Modell

## s3
03 · Elf Zellen – ein gekoppeltes Modell

## preset
Voreinstellungen

## locked_preset_help
Die Beispiele nach Mehl (2006) verwenden die veröffentlichten Einstellungen für Grundwasserleiter und Evapotranspiration. Wählen Sie unter „Voreinstellungen“ einen der drei editierbaren gespannten oder ungespannten Fälle, um diese Optionen unter „Allgemeine Modelleinstellungen“ zu ändern.

## et_preset
Ungespannt · mit Evapotranspiration

## left
Vorgegebene Höhe links (m)

## right
Vorgegebene Höhe rechts (m)

## kl
K der linken Zelle (m/s)

## kc
K der mittleren Zelle (m/s)

## kr
K der rechten Zelle (m/s)

## initial
Starthöhe in der mittleren Zelle (m)

## unconfined
Ungespannter Grundwasserleiter

## et_enable
Evapotranspiration in der mittleren Zelle aktivieren

## et_surface
Höhenlage der ET-Oberfläche (m)

## et_depth
Extinktionstiefe (m)

## et_max
Maximale ET-Rate (mm/Jahr)

## recharge
Einheitliche Grundwasserneubildung (mm/Jahr)

## omega
Dämpfungsfaktor ω

## omega_help
Bei ω = 1 wird der volle Schritt übernommen. Ein kleinerer Wert verkürzt die Korrektur. Das kann die Konvergenz erleichtern, garantiert sie jedoch nicht.

## reset
Zurücksetzen

## reset_notice
Die Modelleinstellungen wurden geändert. Die Iterationen beginnen erneut.

## ready
Startwert

## running
Iteration läuft

## converged
Konvergiert

## singular
Singuläres Gleichungssystem. Setzen Sie den Versuch zurück oder ändern Sie die Starthöhe.

## dry
Schritt verworfen. Die Höhe liegt auf oder unter der Sohle.

## cycle
Zweierzyklus erkannt. Setzen Sie den Versuch zurück oder ändern Sie die Starthöhe.

## limit
Maximale Iterationszahl erreicht

## diverged
Die vorgeschlagene Höhe ist nicht endlich oder zu groß.

## status
{method} · {status} · angenommene Schritte: {steps}

## reference
Referenzhöhen und analytischer Vergleich

## no_reference
Für diese Einstellungen ließ sich keine Lösung mit wasserführenden Zellen unabhängig bestätigen. Prüfen Sie die Parameter.

## maps
Wie lese ich die Iterationsdiagramme?

## scalar_caption
Lesen Sie die aktuelle Höhe auf der waagerechten Achse ab. Dünne gepunktete orange Linien verbinden die Eingabewerte mit der Konstruktion. Durchgezogene orange Linien zeigen die Picard-Schritte bzw. die Newton-Tangenten. Bei Picard überträgt die Diagonale jede angenommene Höhe auf die Eingabeachse. Die senkrechte Linie an der aktuellen Höhe reicht von oben oder unten bis zur grünen Funktion. Sie zeigt den Funktionswert, ohne einen weiteren Schritt auszulösen. Bei Newton führt die Tangente zur Nulllinie. Der Zoom verändert ausschließlich den Ausschnitt.

## coupled_caption
Bei Picard zeigt die grüne Funktion den zuletzt angenommenen Schritt des gesamten Elf-Zellen-Modells. Die Funktion hängt von den übrigen Höhen ab und kann sich verändern. Alle angenommenen Höhen bleiben im Verlaufsdiagramm sichtbar. Das reduzierte Newton-Residuum ist für die gewählte Zelle und Modellkonfiguration fest. Daher können alle angenommenen Tangenten gemeinsam dargestellt werden.

## residuals
Konvergenz von Höhenänderung und Bilanzresiduum

## residual_caption
Grün steht für Picard, Blau für Newton. Quadrate zeigen das Bilanzresiduum (rechts, Achse und Grenzlinie violett), Kreise die Höhenänderung (links, ockerfarben). Beide logarithmischen Achsen reichen von 1E-12 bis 100. Sowohl max|Δh| < {head_tol:.0e} m als auch max|F| < {flow_tol:.0e} m³/s müssen erfüllt sein. Bei k = 0 gibt es noch keine Höhenänderung. Dreiecke zeigen Werte unterhalb (▼, einschließlich null) oder oberhalb (▲) des Ausschnitts an. Auch Grenzwerte außerhalb der Ansicht gelten. Die Größen geben keine Abweichung von der Referenzhöhe an.

## head_history
Verlauf der hydraulischen Höhe in Zelle {cell}

## head_history_caption
Höhe nach jedem angenommenen Schritt, beginnend mit dem Startwert bei k = 0. Die unabhängig berechnete Referenzhöhe dient dem visuellen Vergleich. Die Abbruchkriterien werden separat geprüft. k zählt Iterationen, keine Zeitschritte.

## off
Keine ET

## linear
Linearer ET-Bereich

## maximum
Maximale ET

## gradient
Gefälle erhöhen · rechte Randhöhe auf 0,5 m setzen

## heterogeneous
Drei Zonen mit unterschiedlichen Leitfähigkeiten

## zone1
Zone 1 · Zellen 1–5 · K (m/s)

## zone2
Zone 2 · Zelle 6 · K (m/s)

## zone3
Zone 3 · Zellen 7–11 · K (m/s)

## cell
Zelle auswählen (innere Zellen 2–10)

## initial_mode
Anfängliches Höhenprofil

## initial_linear
Linear zwischen den Randhöhen

## initial_uniform
Einheitliche Starthöhe im Modellinneren

## uniform_value
Einheitliche Starthöhe im Modellinneren (m)

## assess
Verständnis prüfen

## assessment_info
Wählen Sie alle zutreffenden Aussagen aus. Eine oder mehrere können richtig sein. Für jede korrekt ausgewählte oder korrekt nicht ausgewählte Aussage erhalten Sie einen Punkt. Für die volle Punktzahl müssen alle Entscheidungen richtig sein.

## check
Antwort prüfen

## score
Richtige Entscheidungen: {score}/{total}

## theory_quiz
Grundlagen

## three_quiz
Bilanz und Iteration im Drei-Zellen-Modell

## references
Quellen und Gültigkeitsbereich des Modells

## confined_preset
Gespannt · ohne Evapotranspiration

## unconfined_preset
Ungespannt · ohne Evapotranspiration

## learn_theory
Mehr erfahren · Herleitung der Picard- und Newton-Verfahren

## notes_three
Mehr erfahren · Modellannahmen und Versuchsvorschläge

## notes_grid
Mehr erfahren · Gesamtmodell und gekoppelte Iteration

## learn_three
Erkunden · Drei-Zellen-Modell und Evapotranspiration

## learn_grid
Erkunden · elf Zellen und ihre Kopplung

## language_proxy
Die Inhalte sind auf Deutsch und Englisch verfügbar. Fehlt eine Übersetzung, wird der englische Text angezeigt.

## closure
Konvergenzkriterien

## head_closure
Toleranz für die maximale Höhenänderung (m)

## flow_closure
Toleranz für das maximale Bilanzresiduum (m³/s)

## closure_help
Beide Kriterien müssen erfüllt sein. Voreingestellt sind 1E-4 m für die Höhenänderung und 1E-6 m³/s für das Bilanzresiduum. Bei den kleinen Volumenströmen in Mehls Beispielen kann das Residuum die Toleranz schon früh unterschreiten. Nach einer Änderung der Toleranzen wird der gespeicherte Zustand erneut geprüft. Gegebenenfalls können Sie die Iteration fortsetzen.

## sync
Synchron

## sync_help
Anfangs führt jede Startschaltfläche nur das zugehörige Verfahren aus. Bei „Synchron“ erhalten beide Schaltflächen einen gemeinsamen Rahmen. Jede verfügbare Schaltfläche startet dann beide verfügbaren Verfahren. Konvergierte oder abgebrochene Verfahren behalten ihren letzten Zustand.

## to_closure
Bis zur Konvergenz

## to_closure_help
Aktivieren Sie diese Option und starten Sie anschließend ein Verfahren, um bis zur Konvergenz oder zu einem erkannten Abbruchgrund zu rechnen. Das Umschalten allein löst keine Berechnung aus. Bei „Synchron“ gilt die Auswahl für beide verfügbaren Verfahren.

## play_method
▶ {method}

## converged_method
✓ {method}

## stopped_method
■ {method}

## play_help
Einen Iterationsschritt für {methods} versuchen.

## run_help
{methods} bis zur Konvergenz oder bis zu einem erkannten Abbruchgrund ausführen.

## stopped_help
{method} · {status}

## outside_view
{method} · Die aktuelle Höhe von {head:.3f} m liegt außerhalb dieses Ausschnitts. Im Höhenverlauf bleibt der Wert erhalten.

## advanced
Erweiterte Einstellung · Dämpfung

## advanced_help
Die vorgeschlagene Höhenkorrektur wird mit ω multipliziert. Ein Wert unter 1 verkürzt den Schritt. Dies kann die Konvergenz erleichtern.

## conductivity_help
Zur Auswahl stehen je Zehnerpotenz die Faktoren 1 und 5: 10⁻⁶, 5×10⁻⁶, …, 10⁻³ m/s.

## fig_cell
Zelle {cell}

## fig_cell_number
Zellnummer

## fig_specified
Feste Höhe

## fig_final
Referenzhöhe

## fig_top
Oberkante: {top:g} m

## fig_bottom
Sohle: {bottom:g} m

## conductance_heading
1 · Aus Höhendifferenzen Volumenströme bestimmen

## balance_heading
2 · Die Wasserbilanz aufstellen

## picard_heading
3 · Die Bilanz für Picard umstellen

## newton_heading
4 · Die Bilanz für Newton linearisieren

## compare_heading
Durchgerechnete Beispiele aus Mehl (2006)

## convergence_heading
Wann kann die Iteration enden?

## fig_optional_et
Optionale ET

## fig_recharge
Grundwasserneubildung

## current_head
Aktuelle Höhe: **{head:.3f} m**

## zoom
Auto-Zoom

## zoom_auto
Auto-Zoom

## zoom_manual
Manueller Zoom

## zoom_help
Zentriert den Schnittpunkt mit der Diagonalen (Picard) bzw. der Nulllinie (Newton). Nach dem Anpassen liegt die aktuelle Höhe etwa zwei Drittel des Wegs von der Mitte zum Rand auf ihrer Seite. Die Breite bleibt bestehen, bis der Abstand zur Mitte unter 25 % der halben Breite fällt oder die Höhe den Ausschnitt verlässt. Die kleinste automatische Gesamtbreite ist 0,001 m. Ausschalten stellt die Gesamtansicht wieder her. Mit − Zoom / + Zoom wählen Sie die Breite manuell. Änderungen an Modellparametern oder Startwerten stellen die Gesamtansicht wieder her. Der Zoom beeinflusst die berechneten Höhen nicht.

## zoom_in
+ Zoom

## zoom_out
− Zoom

## zoom_in_help
Vergrößern: nächstkleinere Gesamtbreite aus 1, 0,1, 0,01, 0,001, 1E-4 und 1E-5 m. Der Auto-Zoom wird ausgeschaltet. Die Breite bleibt über die Iterationen fest und der Schnittpunkt in der Mitte. Geänderte Modellparameter oder Startwerte stellen die Gesamtansicht wieder her.

## zoom_out_help
Verkleinern: nächstgrößere Gesamtbreite aus 1E-5, 1E-4, 0,001, 0,01, 0,1 und 1 m. Der Auto-Zoom wird ausgeschaltet. Die Breite bleibt über die Iterationen fest und der Schnittpunkt in der Mitte. Geänderte Modellparameter oder Startwerte stellen die Gesamtansicht wieder her.

## general_settings
Allgemeine Modelleinstellungen

## initial_boundary
Anfangs- und Randbedingungen

## aquifer_parameters
Grundwasserleiter und ET

## uniform_k
Einheitliche Leitfähigkeit K (m/s)

## grid_quiz
Gekoppelte Iteration und Nichtlinearität

## paper_case
Abbildungspaar aus Mehl (2006)

## paper_smooth
Glatte Bilanz ohne ET · Abbildungen 2 und 3

## paper_et
Abschnittsweise definierte ET · Abbildungen 5 und 6

## true_head_column
Referenzhöhe h (m)

## hydraulic_parameters
Eigenschaften des Grundwasserleiters

## mehl_smooth_preset
Mehl (2006) · ungespannt ohne ET · Abbildungen 2 und 3

## mehl_et_preset
Mehl (2006) · ungespannt mit ET · Abbildungen 5 und 6

## use_paper_case
Dieses Beispiel aus Mehl (2006) in Abschnitt 2 übernehmen

## initial_picard
Starthöhe in der mittleren Zelle · Picard (m)

## initial_newton
Starthöhe in der mittleren Zelle · Newton (m)

## mehl_conductivity
| Zelle | K (umgerechnet in m/d) |
|:--|--:|
| 1 | {kl:g} |
| 2 | {kc:g} |
| 3 | {kr:g} |

## mehl_k_help
Die Leitfähigkeitswerte aus der Veröffentlichung werden wie in Abschnitt 1 als m/d interpretiert und für die Rechnung in m/s umgerechnet.

## fig_display_top
Darstellungsgrenze: {top:g} m

## model_preview
Modellvorschau

## head_check_wait
Die Höhenänderung lässt sich ab dem ersten Schritt prüfen.

## head_check
Max. |Δh| = {value:.2e} m · Grenzwert {threshold:.0e} m · {result}.

## flow_check
Max. |F| = {value:.2e} m³/s · Grenzwert {threshold:.0e} m³/s · {result}.

## criterion_met
✓ erfüllt

## criterion_unmet
noch nicht erfüllt

## fig_residual_method
{method} · Bilanzresiduum

## fig_change_method
{method} · Höhenänderung

## fig_head_method
{method} · hydraulische Höhe

## fig_true_head_history
Referenzhöhe ({head:.3f} m)

## fig_flow_closure
Bilanztoleranz ({value:.0e} m³/s)

## fig_head_closure
Höhentoleranz ({value:.0e} m)

## fig_head_axis
Hydraulische Höhe in Zelle {cell} (m)

## slider_input
Schieberegler für die Starthöhe verwenden

## iteration_summary
**h = {head:.3f} m** · k = {steps} · {status}

## analytical_head_column
Analytische Höhe h (m)

## analytical_difference_column
Referenz − analytische Lösung (m)

## analytical_unavailable
Der analytische Vergleich für den homogenen Fall ist bei heterogener Leitfähigkeit oder ET nicht verfügbar.

## coupled_map_help
Für jeden Punkt auf der blauen Newton-Kurve erfüllen die übrigen acht inneren Zellen ihre Wasserbilanz. Die Kurve der gewählten Zelle bleibt deshalb bei unveränderten Modellparametern fest. Der orangefarbene Punkt markiert die aktuelle Näherung. Die Tangente liefert den vollen Newton-Vorschlag. Bei Dämpfung wird nur ein Teil der Korrektur angenommen. Das Konvergenzdiagramm prüft die Bilanzen an den neun tatsächlich berechneten Höhen.

Bei Picard sehen Sie den zuletzt angenommenen Schritt für alle neun Höhen. Die grüne Funktion und ihr Schnittpunkt mit der Diagonalen können sich mit den übrigen Höhen verschieben. Ändert sich die ausgewählte Höhe kaum, werden die anderen Eingangshöhen für diese Kurve festgehalten. Die Verlaufsdiagramme zeigen alle angenommenen Höhen.

## fig_step_fraction
Schrittanteil $\alpha$

## fig_iteration_axis
Iteration $k$

## fig_head_detail
Nahe der Referenz · < 1 cm

## postprocessing
Darstellungsoptionen

## side_by_side
Diagramme nebeneinander anzeigen

## fig_zoom_range
{mode} · Höhenbereich {width:.3g} m

## foundations_quiz
Warum iterieren?

## conductance_quiz
Hydraulischer Leitwert und Darcy-Gesetz

## balance_quiz
Wasserbilanz und Nichtlinearität

## et_quiz
Evapotranspiration aus dem Grundwasser

## picard_quiz
Picard-Iteration

## newton_quiz
Newton-Iteration

## mehl_quiz
Mehls Beispiele interpretieren

## author_credit
Entwickelt von **Thomas Reimann** (2026) · Technische Universität Dresden · The Groundwater Project
