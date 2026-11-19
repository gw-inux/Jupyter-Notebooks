### De la ley de Darcy a la conductancia

Partimos de una conexión uniforme de longitud $L$, conductividad hidráulica $K$ y área transversal $A_\perp$ perpendicular al flujo. Tomamos como sentido positivo el que va del punto $i$ al punto $j$. La ley de Darcy establece:

$$
Q=-K A_\perp\frac{h_j-h_i}{L}.
$$

| Símbolo | Significado | Unidad |
|:--|:--|:--|
| $Q$ | Caudal, positivo de $i$ hacia $j$ | m³/s |
| $K$ | Conductividad hidráulica | m/s |
| $A_\perp$ | Área perpendicular al flujo | m² |
| $h_i$, $h_j$ | Cargas hidráulicas en ambos puntos | m |
| $L$ | Distancia entre los puntos | m |

El signo negativo expresa que el flujo sigue el gradiente hidráulico descendente. Si $h_i>h_j$, el gradiente $(h_j-h_i)/L$ es negativo y $Q$ es positivo en el sentido elegido.

Para flujo horizontal a través de un espesor saturado $b$ y una anchura $w$, el área vertical de la figura tridimensional es:

$$
A_\perp=w b.
$$

Agrupamos la propiedad del material y la geometría en la **conductancia**, $C$:

$$
C=\frac{K A_\perp}{L}=\frac{K w b}{L},
\qquad
Q=-C(h_j-h_i).
$$

La conductancia tiene unidades de **m²/s**. Al multiplicarla por una diferencia de carga en metros se obtiene un caudal en m³/s. No es, por tanto, otro nombre para la conductividad hidráulica: también depende de la anchura, el espesor saturado y la longitud de la conexión.

Imagine dos canales rellenos de la misma arena. A igual longitud y diferencia de carga, el canal saturado más ancho transmite más agua. Su conductividad no cambia, pero su conductancia es mayor.

Por ejemplo, sean $K=10^{-4}$ m/s, $w=10$ m, $b=5$ m y $L=100$ m. Entonces $A_\perp=50$ m² y $C=5\times10^{-5}$ m²/s. Con $h_i-h_j=2$ m, el caudal es $10^{-4}$ m³/s, es decir, **0.1 L/s**. Si el espesor saturado se reduce a la mitad y las demás magnitudes y la diferencia de carga permanecen constantes, la conductancia y el caudal también se reducen a la mitad; la conductividad no cambia.

#### Conexión entre dos celdas vecinas

Entre centros contiguos, el agua atraviesa la mitad de cada celda. Ambas mitades ofrecen resistencia al flujo. Para longitudes iguales $\Delta x$ y una anchura común $w$, las resistencias se suman:

$$
\frac{1}{C_{ij}}
=\frac{\Delta x/2}{K_i w b_i}
+\frac{\Delta x/2}{K_j w b_j}.
$$

$C_{ij}$ es la conductancia de la conexión; $K_i,K_j$ y $b_i,b_j$ son las conductividades y los espesores saturados de ambas celdas. Definiendo sus transmisividades como $T_i=K_i b_i$ y $T_j=K_j b_j$, en m²/s, se obtiene:

$$
C_{ij}=\frac{2T_iT_j}{T_i+T_j}\frac{w}{\Delta x}.
$$

Esta expresión utiliza la media armónica de las transmisividades y se aplica en el modelo de tres celdas. Una semicelda poco transmisiva puede limitar toda la conexión, del mismo modo que un estrechamiento limita el flujo en un canal ancho. Si ambas celdas tienen la misma conductividad y espesor, la expresión se reduce a $C=Kwb/\Delta x$.
