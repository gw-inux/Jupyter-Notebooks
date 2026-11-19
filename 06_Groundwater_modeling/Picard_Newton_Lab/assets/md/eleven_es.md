**Todo el experimento está acoplado.** Las 11 celdas tienen centros separados 100 m y anchura de 1 m. Los centros de contorno distan 1000 m; la recarga entra en las nueve celdas interiores resueltas. El acuífero libre predeterminado tiene base de 0 m, techo de 30 m, cargas de contorno de 18 y 8 m y conductividad de 1E-4 m/s. La comparación confinada utiliza una capa de 20 m, de −20 a 0 m. Elevar el techo modifica el problema físico cuando las cargas alcanzan el techo anterior; no es solo un ajuste gráfico.

La conductancia integra el espesor saturado y utiliza conductividad hidráulica armónica. Con $\Phi'(h)=b(h)$, el caudal a través de una cara es:

$$Q_{i+1/2}=K_{i+1/2}\frac{w}{\Delta x}\left[\Phi(h_i)-\Phi(h_{i+1})\right].$$

Bajo el techo, $\Phi=(h-z_b)^2/2$; por encima, el potencial es lineal y su pendiente coincide con el espesor total. Con K y recarga fijos, las ecuaciones discretas son lineales en el potencial, aunque siguen siendo no lineales en la carga. Las zonas de conductividad fija no impiden esta transformación.

**El panel de Picard** muestra la construcción aceptada más reciente del sistema completo sobre su propia función verde. Cada paso tiene una función a lo largo de su dirección de actualización completa. Se omiten las funciones y recorridos anteriores porque difieren del actual; el historial conserva todas las cargas aceptadas. La guía fina de puntos proyecta la carga actual desde el eje hasta la función. Si la carga seleccionada apenas cambia, se utiliza una sección que mantiene fijas las otras cargas de entrada, evitando dividir por un cambio diminuto. Una función plana en una sección concreta es posible y no demuestra que todo el problema vectorial sea lineal.

**El panel de Newton** muestra el residuo reducido de la celda seleccionada, en m³/s. Para la ley de flujo utilizada, eliminar los balances de las otras ocho celdas da:

$$f_{N,i}(h_i)=F_i^{\mathrm{red}}(h_i)=c_i-S_i\Phi(h_i),\qquad (F_i^{\mathrm{red}})'=-S_i b(h_i).$$

$c_i$ es el término fuente efectivo (m³/s) y $S_i$ un factor positivo (m/s) determinado por las conexiones con ambos contornos. Ambos son constantes para la celda y configuración seleccionadas. Para cada carga de prueba de la curva azul, las otras ocho cargas interiores toman valores que equilibran sus celdas. Repetir una carga de prueba produce, por tanto, la misma ordenada azul en cualquier iteración.

El punto naranja evalúa la curva en la carga actual. La tangente toca la curva en la carga utilizada para ese paso; su intersección con el eje proporciona la propuesta completa de Newton para la celda. La amortiguación acepta una fracción de la corrección. Si mantuviéramos las cargas vecinas en sus estimaciones actuales y variásemos solo la seleccionada, la curva local de balance podría desplazarse entre iteraciones. El gráfico de convergencia evalúa los nueve balances originales con las estimaciones reales. En la sección 2 solo es desconocida la carga central, de modo que $f_N(h)=F(h)$ procede directamente de su balance.

La tabla de referencia compara los casos homogéneos con la solución analítica 1D independiente en los centros. No aplica esa fórmula homogénea a casos heterogéneos. Los caudales de cara están en x = 50, 150, …, 950 m; su salida neta equilibra la recarga sobre las nueve áreas interiores.

El eje izquierdo de convergencia muestra la máxima variación de carga; el derecho, el máximo residuo. Ambos van de 1E-12 a 100. Los historiales reservan una iteración adicional después de la última aceptada. El detalle de carga aparece solo tras tres cambios consecutivos menores de un centímetro cerca de la referencia. Ambos criterios numéricos siguen siendo necesarios; esta vista no modifica tolerancias ni historial.

**Ampliación automática** centra la intersección de Picard con la diagonal o el cero del residuo de Newton. Al ajustar la escala, la carga actual queda a dos tercios del recorrido desde el centro hacia el borde de su lado. La anchura se mantiene hasta que la carga entra en el 25 % interior de la semianchura o sale de la ventana. La anchura total mínima es 0.001 m. La intersección de Picard puede desplazarse al cambiar las otras cargas y diferir de la referencia final; la ventana la sigue conservando su anchura.

**− Ampliar / + Ampliar** eligen anchuras totales manuales de 1, 0.1, 0.01, 0.001, 1E-4 y 1E-5 m y desactivan el modo automático. La anchura manual se conserva entre iteraciones y la intersección permanece centrada. La etiqueta indica modo y anchura. Activar el modo automático inicia un nuevo ajuste; desactivarlo restaura la vista completa. Cambiar entradas, cargas iniciales o amortiguación inicia un experimento nuevo con ambas vistas completas. El posprocesado permite alternar entre gráficos contiguos con controles compartidos y gráficos apilados de ancho completo con controles e historiales independientes. Estas opciones de visualización no cambian el modelo ni borran las iteraciones.
