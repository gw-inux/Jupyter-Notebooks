## title
Picard et Newton · Laboratoire d'itération en hydrogéologie

## page_title
Laboratoire Picard et Newton

## s1
01 · Du bilan en eau à l'itération

## s2
02 · Un modèle idéalisé à trois mailles

## s3
03 · Onze mailles : une complexité accrue

## preset
Configurations proposées

## locked_preset_help
Les cas de Mehl (2006) utilisent les paramètres d'aquifère et d'évapotranspiration de la publication. Pour activer ces options dans les paramètres généraux, choisissez l'un des trois cas modifiables en nappe captive ou libre.

## et_preset
Nappe libre · avec évapotranspiration

## left
Charge imposée à gauche (m)

## right
Charge imposée à droite (m)

## kl
K, maille gauche (m/s)

## kc
K, maille centrale (m/s)

## kr
K, maille droite (m/s)

## initial
Charge initiale au centre (m)

## unconfined
Aquifère à nappe libre

## et_enable
Activer l'ET au centre

## et_surface
Cote de la surface d'ET (m)

## et_depth
Profondeur d'extinction (m)

## et_max
Taux maximal d'ET (mm/an)

## recharge
Recharge uniforme (mm/an)

## omega
Facteur d'amortissement ω

## omega_help
1 = correction entière. Une valeur inférieure réduit la correction proposée, sans garantir la convergence.

## reset
Reset

## reset_notice
Paramètres du modèle modifiés : les historiques d'itération ont été réinitialisés.

## ready
Estimation initiale

## running
Itération en cours

## converged
Convergence atteinte

## singular
Système linéaire singulier ; réinitialisez ou modifiez la charge initiale

## dry
Pas rejeté : charge au niveau du fond de l'aquifère ou en dessous

## cycle
Cycle de période deux détecté ; réinitialisez ou modifiez la charge initiale

## limit
Nombre maximal d'itérations atteint

## diverged
Charge proposée non finie ou excessivement élevée

## status
{method} : {status} · pas acceptés : {steps}

## reference
Charges de référence · comparaison analytique

## no_reference
Aucune solution conservant les mailles en eau n'a été vérifiée indépendamment pour ces paramètres. Vérifiez la configuration.

## maps
Comprendre les diagrammes d'itération

## scalar_caption
Lisez la charge actuelle sur l'axe horizontal. Les fines lignes pointillées orange relient les valeurs d'entrée à la construction ; les segments orange continus montrent l'itération de Picard ou les tangentes de Newton. Picard reporte chaque mise à jour acceptée sur la diagonale. Le segment vertical continu à la charge actuelle rejoint la fonction par le haut ou le bas : il représente l'évaluation actuelle, sans accepter de nouvelle mise à jour. Newton suit la tangente au résidu jusqu'à zéro. Les axes restent fixes sauf si vous activez le zoom, qui ne modifie que la vue.

## coupled_caption
Pour les onze mailles, le diagramme de Picard montre la dernière construction acceptée sur sa propre fonction de mise à jour du système complet. Cette fonction évolue avec les autres charges ; toutes les charges acceptées restent dans les historiques. Le résidu de débit réduit de Newton est fixe pour ce modèle et peut montrer toutes les tangentes acceptées.

## residuals
Convergence : variation de charge et résidu de débit

## residual_caption
Vert = Picard ; bleu = Newton. Carrés = résidu de débit (axe et seuil violets à droite) ; cercles = variation de charge (axe et seuil ocres à gauche). Les deux axes logarithmiques restent entre 1E-12 et 100. Il faut satisfaire à la fois max|Δh| < {head_tol:.0e} m et max|F| < {flow_tol:.0e} m³/s. Aucune variation de charge n'est définie à k = 0. Les triangles signalent les valeurs sous la limite (▼, zéro compris) ou au-dessus (▲). Un seuil hors de la vue reste applicable. Ces grandeurs ne sont pas les erreurs par rapport à la charge de référence.

## head_history
Historique de la charge dans la maille {cell}

## head_history_caption
Charge après chaque mise à jour acceptée, avec l'estimation initiale à k = 0. La charge de référence indépendante sert de repère visuel ; elle n'intervient pas dans le critère d'arrêt. k compte les mises à jour acceptées, pas les pas de temps.

## off
Sans ET

## linear
Intervalle linéaire d'ET

## maximum
ET maximale

## gradient
À droite : 0,5 m

## heterogeneous
Trois zones de K

## zone1
Zone 1 · mailles 1–5 · K (m/s)

## zone2
Zone 2 · maille 6 · K (m/s)

## zone3
Zone 3 · mailles 7–11 · K (m/s)

## cell
Maille à étudier (mailles intérieures 2–10)

## initial_mode
Profil initial des charges

## initial_linear
Linéaire entre les limites

## initial_uniform
Charge intérieure uniforme

## uniform_value
Charge initiale uniforme à l'intérieur (m)

## assess
Auto-évaluation

## assessment_info
Sélectionnez toutes les propositions exactes (une ou plusieurs). Dans ce laboratoire, chaque proposition exacte sélectionnée rapporte un point. Les propositions non sélectionnées ou erronées ne rapportent aucun point ; aucun point n'est retiré. La réponse n'est entièrement correcte que si toutes les propositions exactes, et aucune proposition erronée, sont sélectionnées. Dans le barème OPAL/ONYX utilisé pour ce cours, ne pas sélectionner une proposition erronée rapporte également un point.

## check
Vérifier

## score
Points pour les choix exacts : {score}/{total}

## answer_full
Entièrement correcte

## answer_partial
Partiellement correcte

## answer_wrong
Incorrecte

## assessment_details
Propositions erronées sélectionnées : {incorrect}. Propositions exactes encore manquantes : {missing}. Le nombre de points ne suffit pas à établir que la réponse est entièrement correcte.

## theory_quiz
Principes

## three_quiz
Trois mailles

## references
Références et portée du modèle

## confined_preset
Nappe captive · sans évapotranspiration

## unconfined_preset
Nappe libre · sans évapotranspiration

## learn_theory
Approfondir · établir les itérations de Picard et Newton

## notes_three
Approfondir · hypothèses et expériences proposées

## notes_grid
Approfondir · modèle complet et mises à jour couplées

## learn_three
Explorer · trois mailles et évapotranspiration

## learn_grid
Explorer · onze mailles et complexité accrue

## language_proxy
Le contenu est disponible en anglais, allemand, français, espagnol, italien, hindi, arabe et chinois simplifié. Les traductions manquantes sont remplacées par l'anglais.

## closure
Critères de convergence

## head_closure
Tolérance sur la variation maximale de charge (m)

## flow_closure
Tolérance sur le résidu maximal de débit (m³/s)

## closure_help
Les deux critères doivent être satisfaits. Valeurs par défaut : 1E-4 m pour la variation de charge et 1E-6 m³/s pour le résidu de débit. Dans les cas à faibles débits de Mehl (2006), le résidu peut respecter le seuil avant que la charge se stabilise. Modifier les tolérances réévalue l'état sauvegardé et peut permettre de reprendre le calcul.

## sync
Sync

## sync_help
Désactivé au départ : chaque bouton fait avancer sa propre méthode. Activez cette option pour regrouper les deux boutons dans un même cadre ; chacun fait alors avancer les deux méthodes disponibles. Les méthodes ayant convergé ou atteint une condition d'arrêt restent inchangées.

## to_closure
Calcul complet

## to_closure_help
Choisissez un calcul complet plutôt qu'une seule mise à jour, puis appuyez sur un bouton actif. Ce commutateur seul ne lance ni ne réinitialise le modèle. Avec Sync, les deux méthodes disponibles avancent jusqu'à convergence ou jusqu'à une condition d'arrêt identifiée.

## play_method
▶ {method}

## converged_method
✓ {method}

## stopped_method
■ {method}

## play_help
Tenter une mise à jour pour {methods}.

## run_help
Poursuivre {methods} jusqu'à convergence ou jusqu'à une condition d'arrêt identifiée.

## stopped_help
{method} : {status}.

## outside_view
{method} : la charge actuelle {head:.3f} m est hors de cette vue. Sa valeur numérique reste dans l'historique.

## advanced
Option avancée · amortissement

## advanced_help
L'amortissement multiplie la correction proposée par ω. Une valeur inférieure à 1 réduit le pas numérique ; cela peut faciliter la convergence sans la garantir.

## conductivity_help
Choisissez 1 ou 5 dans chaque ordre de grandeur : 10⁻⁶, 5×10⁻⁶, …, 10⁻³ m/s.

## fig_cell
Maille {cell}

## fig_cell_number
N° de maille

## fig_specified
Charge imposée

## fig_final
Charge de référence

## fig_top
Toit de l'aquifère : {top:g} m

## fig_bottom
Fond : {bottom:g} m

## conductance_heading
1 · Relier les différences de charge aux débits

## balance_heading
2 · Établir le bilan en eau

## picard_heading
3 · Réarranger le bilan pour Picard

## newton_heading
4 · Linéariser le bilan pour Newton

## compare_heading
Exemples de Mehl (2006)

## convergence_heading
Décider quand arrêter le calcul

## fig_optional_et
ET facultative

## fig_recharge
Recharge

## current_head
Charge actuelle : **{head:.3f} m**

## zoom
Auto-zoom

## zoom_auto
Auto-zoom

## zoom_manual
Zoom manuel

## zoom_help
Centrer l'intersection de la fonction avec la diagonale (Picard) ou avec la ligne de résidu nul (Newton). Au premier ajustement, la charge actuelle se situe aux deux tiers de la distance du centre au bord situé de son côté. Conserver la largeur jusqu'à ce que sa distance au centre soit inférieure à 25 % de la demi-largeur ; élargir si la charge sort de la fenêtre. La largeur totale minimale est de 0,001 m. Désactivez Auto-zoom pour retrouver la vue complète, ou utilisez − Zoom / + Zoom pour choisir une largeur manuelle. Modifier les paramètres ou les charges initiales rétablit la vue complète. Le zoom ne modifie jamais les charges calculées.

## zoom_in
+ Zoom

## zoom_out
− Zoom

## zoom_in_help
Zoom manuel avant : choisir la largeur totale immédiatement inférieure parmi 1, 0,1, 0,01, 0,001, 1E-4 et 1E-5 m. Auto-zoom est désactivé et la largeur reste fixe au fil des itérations. L'intersection reste centrée. Modifier les paramètres ou les charges initiales rétablit la vue complète.

## zoom_out_help
Zoom manuel arrière : choisir la largeur totale immédiatement supérieure parmi 1E-5, 1E-4, 0,001, 0,01, 0,1 et 1 m. Auto-zoom est désactivé et la largeur reste fixe au fil des itérations. L'intersection reste centrée. Modifier les paramètres ou les charges initiales rétablit la vue complète.

## general_settings
Paramètres généraux

## initial_boundary
Conditions initiales et aux limites

## aquifer_parameters
Paramètres de l'aquifère et de l'ET

## uniform_k
K uniforme (m/s)

## grid_quiz
Itération couplée

## paper_case
Paire de figures de Mehl (2006)

## paper_smooth
Bilan régulier en nappe libre · figures 2 et 3

## paper_et
Bilan par morceaux avec ET · figures 5 et 6

## true_head_column
h de référence (m)

## hydraulic_parameters
Paramètres de l'aquifère

## mehl_smooth_preset
Mehl (2006) · nappe libre sans ET · figures 2 et 3

## mehl_et_preset
Mehl (2006) · nappe libre avec ET · figures 5 et 6

## use_paper_case
Charger en section 2

## initial_picard
Charge initiale au centre · Picard (m)

## initial_newton
Charge initiale au centre · Newton (m)

## mehl_conductivity
| Maille | K (équivalent en m/jour) |
|:--|--:|
| 1 | {kl:g} |
| 2 | {kc:g} |
| 3 | {kr:g} |

## mehl_k_help
Les valeurs de conductivité de la publication sont interprétées ici en m/jour et converties en m/s dans le calcul, exactement comme en section 1.

## fig_display_top
Limite d'affichage : {top:g} m

## model_preview
Aperçu du modèle

## head_check_wait
Contrôle de la variation de charge : disponible après la première mise à jour.

## head_check
Max |Δh| = {value:.2e} m ; seuil {threshold:.0e} m — {result}.

## flow_check
Max |F| = {value:.2e} m³/s ; seuil {threshold:.0e} m³/s — {result}.

## criterion_met
✓ satisfait

## criterion_unmet
pas encore satisfait

## fig_residual_method
{method} · résidu de débit

## fig_change_method
{method} · variation de charge

## fig_head_method
{method} · charge

## fig_true_head_history
Charge de référence ({head:.3f} m)

## fig_flow_closure
Seuil du résidu ({value:.0e} m³/s)

## fig_head_closure
Seuil de variation ({value:.0e} m)

## fig_head_axis
Charge dans la maille {cell} (m)

## slider_input
Curseur

## iteration_summary
**h = {head:.3f} m** · k = {steps} · {status}

## analytical_head_column
h analytique (m)

## analytical_difference_column
Référence − analytique (m)

## analytical_unavailable
La comparaison analytique homogène n'est pas disponible avec une conductivité hétérogène ou avec l'ET.

## coupled_map_help
La courbe bleue de Newton représente le déséquilibre de débit de la maille choisie lorsque les huit autres mailles intérieures sont à l'équilibre pour chaque charge d'essai. On obtient une courbe fixe pour cette maille et cette configuration. Le point orange marque l'estimation actuelle. Chaque tangente donne la proposition complète de Newton ; l'amortissement peut réduire le pas accepté. Le diagramme de convergence utilise les déséquilibres calculés aux neuf charges effectivement estimées.

Le diagramme de Picard montre la dernière mise à jour acceptée des neuf charges. Sa courbe verte et son intersection avec la diagonale peuvent se déplacer lorsque les autres charges changent. Si la charge choisie varie très peu, la courbe de Picard maintient les autres charges d'entrée fixes. Les historiques conservent toutes les charges acceptées.

## fig_step_fraction
Fraction du pas $\alpha$

## fig_iteration_axis
Itération $k$

## fig_head_detail
Près de la référence · < 1 cm

## postprocessing
Options d'affichage

## side_by_side
Côte à côte

## fig_zoom_range
{mode} sur {width:.3g} m de charge

## foundations_quiz
Pourquoi itérer ?

## conductance_quiz
Conductance et Darcy

## balance_quiz
Bilan en eau

## et_quiz
Évapotranspiration

## picard_quiz
Itération de Picard

## newton_quiz
Itération de Newton

## mehl_quiz
Mehl (2006)

## author_credit
Développé par **Thomas Reimann** (2026) · TUD Dresden University of Technology · The Groundwater Project · d'après [Mehl (2006)](https://doi.org/10.1111/j.1745-6584.2006.00207.x)
