Una corrección pequeña no basta: el balance todavía puede ser deficiente. Compruebe **ambos** criterios: la máxima variación absoluta de carga y el máximo valor absoluto del residuo de caudal. Los experimentos permiten elegir sus tolerancias. Los valores predeterminados son $10^{-4}$ m y $10^{-6}$ m³/s, respectivamente.

**¿Por qué otra actualización después de cumplir el criterio de residuo?** La última variación de carga puede seguir superando su tolerancia. En un problema lineal, la primera actualización puede alcanzar la solución con residuo nulo, aunque el cambio desde la estimación inicial sea grande. Una segunda actualización sin cambio confirma el criterio de carga. En los ejemplos de caudales pequeños de Mehl (2006), incluso la estimación inicial puede cumplir 1E-6 m³/s y tener todavía un error considerable de carga. Cumplir solo el criterio de caudal no basta.

El gráfico muestra la máxima variación de carga en el eje logarítmico izquierdo y el máximo residuo en el derecho. Ambas escalas permanecen entre $10^{-12}$ y $100$, en sus unidades respectivas. El morado identifica el eje y el límite de caudal; el ocre, los de variación de carga. Los cuadrados representan residuos y los círculos variaciones de carga; el verde identifica Picard y el azul Newton. Los triángulos de borde señalan valores fuera de la vista: hacia abajo si quedan por debajo del límite inferior, incluido cero, y hacia arriba si superan el superior. Una tolerancia elegida fuera de la vista sigue aplicándose y aparece en la leyenda.

La variación de carga se calcula entre iteraciones aceptadas; no se inventa un valor para la estimación inicial. Otro gráfico inferior muestra la carga real de la celda seleccionada y la de referencia. Esta última sirve de guía visual: el método no utiliza el error respecto a esa solución conocida como criterio de parada.

Para una función escalar suave de Picard, $|f'_P(h^*)|<1$ es una condición suficiente de convergencia local: estimaciones suficientemente cercanas se aproximan a la solución. $f'_P$ es la derivada de la función de actualización respecto a la carga de entrada y es adimensional. Una pendiente local negativa alterna el signo del error. Newton puede converger cuadráticamente cerca de una raíz suave con derivada no nula: el error restante puede disminuir muy rápidamente. Una carga inicial inadecuada o el cambio de tramo de ET pueden impedir la convergencia. Ningún método es universalmente superior.

Para varias cargas desconocidas, cada iteración externa resuelve un sistema matricial acoplado:

$$\mathbf A(\mathbf h^k)\widehat{\mathbf h}_P^{k+1}=\mathbf b(\mathbf h^k),\qquad
\mathbf J(\mathbf h^k)\Delta\mathbf h=-\mathbf F(\mathbf h^k).$$

$\mathbf h^k$ es el vector de cargas interiores actuales (m); $\widehat{\mathbf h}_P^{k+1}$ contiene las cargas propuestas por Picard (m), y $\Delta\mathbf h$ las correcciones de Newton (m). $\mathbf A$ contiene las conductancias fijas y las pendientes activas de las condiciones de contorno (m²/s); $\mathbf b$ contiene los términos correspondientes de contorno y fuentes (m³/s). $\mathbf F$ contiene los residuos de las celdas (m³/s), y $\mathbf J$ es su matriz jacobiana de derivadas respecto a las cargas desconocidas (m²/s).

Estos sistemas lineales se resuelven aquí directamente. No se muestra una historia de iteraciones internas de un solver lineal.
