## title
Picard y Newton · Laboratorio de iteración del flujo subterráneo
## page_title
Laboratorio Picard y Newton
## s1
01 · Del balance de agua a la iteración
## s2
02 · Modelo idealizado de tres celdas
## s3
03 · Once celdas: mayor complejidad
## preset
Ajustes iniciales sugeridos
## locked_preset_help
Los casos de Mehl (2006) utilizan los ajustes publicados de acuífero y evapotranspiración. Para activar estos interruptores en Ajustes generales del modelo, seleccione uno de los tres casos editables de acuífero confinado o libre.
## et_preset
Libre · con evapotranspiración
## left
Carga prescrita izquierda (m)
## right
Carga prescrita derecha (m)
## kl
K, celda izquierda (m/s)
## kc
K, celda central (m/s)
## kr
K, celda derecha (m/s)
## initial
Carga central inicial (m)
## unconfined
Acuífero libre
## et_enable
Activar evapotranspiración en la celda central
## et_surface
Cota de la superficie de ET (m)
## et_depth
Profundidad de extinción (m)
## et_max
Tasa máxima de ET (mm/año)
## recharge
Recarga uniforme (mm/año)
## omega
Factor de amortiguación ω
## omega_help
1 = paso completo. Un valor menor reduce la corrección propuesta, sin garantizar la convergencia.
## reset
Reiniciar
## reset_notice
Han cambiado los ajustes del modelo: se reinician los historiales.
## ready
Estimación inicial
## running
Iterando
## converged
Convergencia alcanzada
## singular
Sistema lineal singular; reinicie o cambie la carga inicial
## dry
Paso rechazado: carga en la base del acuífero o por debajo
## cycle
Se detectó un ciclo de dos pasos; reinicie o cambie la carga inicial
## limit
Límite de iteraciones alcanzado
## diverged
Carga propuesta no finita o excesiva
## status
{method}: {status} · pasos aceptados: {steps}
## reference
Cargas de referencia · comparación analítica
## no_reference
No se ha verificado independientemente una solución con celdas húmedas para estos ajustes. Revise los parámetros.
## maps
Pulse para ampliar la explicación del diagrama de telaraña
## scalar_caption
Lea la carga actual en el eje horizontal. Las líneas naranjas finas de puntos conectan las entradas con la construcción iterativa; los tramos continuos muestran la telaraña de Picard o las tangentes de Newton. Picard transfiere cada actualización aceptada a la diagonal. El tramo vertical continuo en la carga actual llega a la función desde arriba o abajo: muestra la evaluación actual sin aceptar otro paso. Newton sigue la tangente del residuo hasta cero. Los ejes permanecen fijos salvo que active la ampliación, que solo cambia la vista.
## coupled_caption
El panel de Picard de once celdas muestra la construcción aceptada más reciente sobre su propia función del sistema completo. Esta cambia con las otras cargas; los historiales conservan todos los valores aceptados. El residuo reducido de Newton es fijo para este modelo y permite mostrar todas las tangentes aceptadas.
## residuals
Convergencia: variación de carga y residuo de caudal
## residual_caption
Verde = Picard; azul = Newton. Cuadrados = residuo de caudal (eje y límite derechos, morados); círculos = variación de carga (izquierdos, ocres). Ambos ejes logarítmicos permanecen entre 1E-12 y 100. Deben cumplirse max|Δh| < {head_tol:.0e} m y max|F| < {flow_tol:.0e} m³/s. No hay variación de carga en k = 0. Los triángulos indican valores inferiores (▼, incluido cero) o superiores (▲) a la vista. Las tolerancias externas siguen aplicándose. Estas magnitudes no son errores respecto a la carga de referencia.
## head_history
Historial de carga en la celda {cell}
## head_history_caption
Carga real tras cada actualización aceptada, incluida la estimación inicial en k = 0. La referencia independiente es una guía visual, no un criterio de parada. k cuenta actualizaciones aceptadas, no pasos temporales.
## off
Sin ET
## linear
Tramo lineal de ET
## maximum
ET máxima
## gradient
Aumentar gradiente · carga derecha a 0.5 m
## heterogeneous
Añadir tres zonas de conductividad
## zone1
Zona 1 · celdas 1–5 · K (m/s)
## zone2
Zona 2 · celda 6 · K (m/s)
## zone3
Zona 3 · celdas 7–11 · K (m/s)
## cell
Celda de estudio (interiores 2–10)
## initial_mode
Perfil inicial de cargas
## initial_linear
Lineal entre contornos
## initial_uniform
Carga interior uniforme
## uniform_value
Carga interior inicial uniforme (m)
## assess
Compruebe su comprensión
## assessment_info
Seleccione todas las afirmaciones correctas (una o varias). Aquí solo las opciones correctas seleccionadas puntúan: un punto cada una. Las opciones no seleccionadas o incorrectas no puntúan; no se descuentan puntos. Una respuesta es totalmente correcta solo si selecciona todas las correctas y ninguna incorrecta. En el sistema OPAL/ONYX utilizado en este curso, también se concede un punto por cada opción incorrecta que se deja correctamente sin seleccionar.
## check
Comprobar respuesta
## score
Puntos por selecciones correctas: {score}/{total}
## answer_full
Totalmente correcta
## answer_partial
Parcialmente correcta
## answer_wrong
Incorrecta
## assessment_details
Opciones incorrectas seleccionadas: {incorrect}. Opciones correctas que faltan: {missing}. La puntuación por sí sola no implica una respuesta totalmente correcta.
## theory_quiz
Fundamentos
## three_quiz
Balance e iteración de tres celdas
## references
Referencias y alcance del modelo
## confined_preset
Confinado · sin evapotranspiración
## unconfined_preset
Libre · sin evapotranspiración
## learn_theory
Aprender más · deducir Picard y Newton
## notes_three
Aprender más · hipótesis y experimentos sugeridos
## notes_grid
Aprender más · modelo completo y actualizaciones acopladas
## learn_three
Explorar · modelo de tres celdas y evapotranspiración
## learn_grid
Explorar · once celdas y mayor complejidad
## language_proxy
Hay contenido en inglés, alemán, francés, español, italiano, hindi, árabe y chino simplificado. Las traducciones ausentes se sustituyen por inglés.
## closure
Criterios de convergencia
## head_closure
Tolerancia de máxima variación de carga (m)
## flow_closure
Tolerancia de máximo residuo de caudal (m³/s)
## closure_help
Deben cumplirse ambos criterios. Valores predeterminados: 1E-4 m para carga y 1E-6 m³/s para caudal. En los casos de caudales pequeños de Mehl (2006), el residuo puede cumplir antes de estabilizarse la carga. Cambiar tolerancias reevalúa la iteración guardada y permite reanudarla.
## sync
Sincronizar
## sync_help
Inicialmente desactivado: cada botón avanza su método. Actívelo para agrupar ambos botones; cualquiera de los activos avanza ambos métodos disponibles. Los convergidos o detenidos permanecen sin cambios.
## to_closure
Ejecutar hasta convergencia
## to_closure_help
Seleccione la ejecución completa y pulse un botón activo. Este interruptor por sí solo no ejecuta ni reinicia el modelo. Con sincronización, ambos métodos disponibles avanzan hasta converger o hasta una condición de parada diagnosticada.
## play_method
▶ {method}
## converged_method
✓ {method}
## stopped_method
■ {method}
## play_help
Intentar una actualización de {methods}.
## run_help
Continuar {methods} hasta convergencia o una condición de parada.
## stopped_help
{method}: {status}.
## outside_view
{method}: la carga actual, {head:.3f} m, está fuera de esta vista. Su valor se conserva en el historial.
## advanced
Opción avanzada · amortiguación
## advanced_help
La amortiguación multiplica la corrección propuesta por ω. Un valor menor que 1 acorta el paso; puede favorecer la convergencia, pero no la garantiza.
## conductivity_help
Seleccione 1 o 5 en cada orden de magnitud: 10⁻⁶, 5×10⁻⁶, …, 10⁻³ m/s.
## fig_cell
Celda {cell}
## fig_cell_number
Número de celda
## fig_specified
Carga prescrita
## fig_final
Carga de referencia
## fig_top
Techo del acuífero: {top:g} m
## fig_bottom
Base: {bottom:g} m
## conductance_heading
1 · Convertir diferencias de carga en caudales
## balance_heading
2 · Formular el balance de agua
## picard_heading
3 · Reordenar el balance para Picard
## newton_heading
4 · Linealizar el balance para Newton
## compare_heading
Ejemplos de Mehl (2006)
## convergence_heading
Decidir cuándo detenerse
## fig_optional_et
ET opcional
## fig_recharge
Recarga
## current_head
Carga actual: **{head:.3f} m**
## zoom
Ampliación automática
## zoom_auto
Ampliación automática
## zoom_manual
Ampliación manual
## zoom_help
Centra la intersección con la diagonal (Picard) o el cero (Newton). Al ajustar, la carga actual queda a dos tercios del recorrido entre centro y borde próximo. La anchura se conserva hasta que su distancia al centro sea menor del 25 % de la semianchura; aumenta si la carga sale de la ventana. La anchura total mínima es 0.001 m. Desactive el modo automático para volver a la vista completa o use − Ampliar / + Ampliar para anchuras manuales. Cambiar entradas o cargas iniciales restaura la vista completa. La ampliación no cambia las cargas calculadas.
## zoom_in
+ Ampliar
## zoom_out
− Ampliar
## zoom_in_help
Ampliación manual: siguiente intervalo total menor entre 1, 0.1, 0.01, 0.001, 1E-4 y 1E-5 m. Desactiva el modo automático y conserva la anchura entre iteraciones. La intersección permanece centrada. Cambiar entradas o cargas iniciales restaura la vista completa.
## zoom_out_help
Reducción manual: siguiente intervalo total mayor entre 1E-5, 1E-4, 0.001, 0.01, 0.1 y 1 m. Desactiva el modo automático y conserva la anchura entre iteraciones. La intersección permanece centrada. Cambiar entradas o cargas iniciales restaura la vista completa.
## general_settings
Ajustes generales del modelo
## initial_boundary
Condiciones iniciales y de contorno
## aquifer_parameters
Parámetros del acuífero y de ET
## uniform_k
K uniforme (m/s)
## grid_quiz
Iteración acoplada y no linealidad
## paper_case
Par de figuras de Mehl (2006)
## paper_smooth
Balance suave de acuífero libre · figuras 2 y 3
## paper_et
Balance por tramos con ET · figuras 5 y 6
## true_head_column
h de referencia (m)
## hydraulic_parameters
Parámetros del acuífero
## mehl_smooth_preset
Mehl (2006) · libre sin ET · figuras 2 y 3
## mehl_et_preset
Mehl (2006) · libre con ET · figuras 5 y 6
## use_paper_case
Usar este caso de Mehl (2006) en la sección 2
## initial_picard
Carga central inicial · Picard (m)
## initial_newton
Carga central inicial · Newton (m)
## mehl_conductivity
| Celda | K (equivalente en m/día) |
|:--|--:|
| 1 | {kl:g} |
| 2 | {kc:g} |
| 3 | {kr:g} |
## mehl_k_help
Las conductividades del artículo se interpretan aquí en m/día y se convierten internamente a m/s, igual que en la sección 1.
## fig_display_top
Límite de representación: {top:g} m
## model_preview
Vista previa del modelo
## head_check_wait
Criterio de variación de carga: disponible tras el primer paso.
## head_check
Máx. |Δh| = {value:.2e} m; límite {threshold:.0e} m — {result}.
## flow_check
Máx. |F| = {value:.2e} m³/s; límite {threshold:.0e} m³/s — {result}.
## criterion_met
✓ cumplido
## criterion_unmet
aún no cumplido
## fig_residual_method
{method} · residuo de caudal
## fig_change_method
{method} · variación de carga
## fig_head_method
{method} · carga
## fig_true_head_history
Carga de referencia ({head:.3f} m)
## fig_flow_closure
Tolerancia de caudal ({value:.0e} m³/s)
## fig_head_closure
Tolerancia de carga ({value:.0e} m)
## fig_head_axis
Carga en celda {cell} (m)
## slider_input
Usar deslizador para la carga inicial
## iteration_summary
**h = {head:.3f} m** · k = {steps} · {status}
## analytical_head_column
h analítica (m)
## analytical_difference_column
Referencia − analítica (m)
## analytical_unavailable
La comparación analítica homogénea no está disponible con conductividad heterogénea ni ET.
## coupled_map_help
La curva azul de Newton representa el desequilibrio de la celda seleccionada cuando las otras ocho están equilibradas para cada carga de prueba. Así se obtiene una curva fija para esa celda y configuración. El punto naranja muestra la estimación actual. Cada tangente alcanza la propuesta completa de Newton; la amortiguación puede acortar el paso aceptado. La convergencia utiliza los desequilibrios de las nueve cargas reales.

El panel de Picard muestra la última actualización aceptada de las nueve cargas. Su curva verde y su intersección con la diagonal pueden moverse al cambiar las otras cargas. Si la seleccionada apenas varía, la curva mantiene fijas las otras cargas de entrada. Los historiales conservan todos los valores aceptados.
## fig_step_fraction
Fracción de paso $\alpha$
## fig_iteration_axis
Iteración $k$
## fig_head_detail
Cerca de la referencia · < 1 cm
## postprocessing
Opciones de posprocesado
## side_by_side
Mostrar gráficos lado a lado
## fig_zoom_range
{mode}: intervalo de carga de {width:.3g} m
## foundations_quiz
Por qué es necesaria la iteración
## conductance_quiz
Conductancia y flujo de Darcy
## balance_quiz
Balance de agua y no linealidad
## et_quiz
Evapotranspiración del agua subterránea
## picard_quiz
Iteración de Picard
## newton_quiz
Iteración de Newton
## mehl_quiz
Interpretar los ejemplos de Mehl (2006)
## author_credit
Desarrollado por **Thomas Reimann** (2026) · TUD Dresden University of Technology · The Groundwater Project · basado en [Mehl (2006)](https://doi.org/10.1111/j.1745-6584.2006.00207.x)
