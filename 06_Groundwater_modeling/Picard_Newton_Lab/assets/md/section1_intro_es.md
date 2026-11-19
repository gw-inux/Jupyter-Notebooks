### ¿Por qué deben comprender las iteraciones de Picard y Newton quienes modelizan las aguas subterráneas?

Imagine que ha construido un modelo para evaluar el bombeo en un acuífero libre. Al principio obtiene cargas hidráulicas plausibles. Al aumentar el caudal de bombeo, el cálculo necesita muchas más iteraciones o se detiene sin converger. Cambiar el método de resolución puede restablecer la convergencia, aunque las propiedades del acuífero y las condiciones de contorno sigan siendo las mismas.

Para interpretar este comportamiento, hay que comprender por qué se repiten los cálculos, cómo el bombeo puede dificultar la resolución y qué indican los criterios de convergencia. Una distribución de cargas plausible no demuestra por sí sola que se satisfagan las ecuaciones de flujo. Del mismo modo, la falta de convergencia no implica necesariamente que el problema físico carezca de solución.

**Las iteraciones de Picard y Newton son dos procedimientos para mejorar sucesivamente las estimaciones de carga hidráulica.** Buscan una solución de las mismas ecuaciones, pero calculan las actualizaciones de manera diferente.

[Steffen Mehl (2006), *Use of Picard and Newton Iteration for Solving Nonlinear Ground Water Flow Equations*](https://doi.org/10.1111/j.1745-6584.2006.00207.x), muestra su comportamiento con un modelo sencillo de tres celdas. Seguimos este enfoque para entender cuándo Newton puede resultar especialmente eficaz y por qué ningún método es el mejor en todas las situaciones.

### Qué aprenderá

Se presuponen conocimientos básicos de carga hidráulica, ley de Darcy, conductividad hidráulica y acuíferos confinados y libres. No se requieren conocimientos previos de métodos numéricos.

Reserve aproximadamente **20–25 minutos para la teoría y las preguntas breves**. Al terminar debería poder:

1. **Explicar** por qué una ecuación de flujo subterráneo puede ser no lineal y cómo Picard y Newton calculan estimaciones sucesivas de carga en un modelo de tres celdas.
2. **Interpretar** sus diagramas de iteración y criterios de convergencia, incluida la mayor rapidez de Newton en algunos casos y la ausencia de una garantía de convergencia desde cualquier estimación inicial.

Reserve aproximadamente **60–75 minutos para el módulo completo**, incluidos los dos experimentos interactivos. Repetir escenarios y debatir las preguntas puede requerir más tiempo.
