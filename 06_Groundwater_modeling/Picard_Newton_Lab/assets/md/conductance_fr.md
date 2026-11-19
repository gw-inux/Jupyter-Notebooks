### De la loi de Darcy à la conductance

Considérons une connexion uniforme de longueur $L$, de conductivité hydraulique $K$ et de section $A_\perp$ perpendiculaire à l'écoulement. Choisissons le sens allant du point $i$ au point $j$ comme sens positif. La loi de Darcy donne :

$$
Q=-K A_\perp\frac{h_j-h_i}{L}.
$$

| Symbole | Signification | Unité |
|:--|:--|:--|
| $Q$ | Débit volumique, positif de $i$ vers $j$ | m³/s |
| $K$ | Conductivité hydraulique | m/s |
| $A_\perp$ | Section perpendiculaire à l'écoulement | m² |
| $h_i$, $h_j$ | Charges hydrauliques aux deux points | m |
| $L$ | Distance entre les deux points | m |

Le signe négatif traduit l'écoulement dans le sens des charges décroissantes. Si $h_i>h_j$, le gradient $(h_j-h_i)/L$ est négatif et $Q$ est positif dans le sens choisi.

Pour un écoulement horizontal dans une épaisseur saturée $b$ et sur une largeur $w$, la section verticale représentée sur le schéma tridimensionnel est :

$$
A_\perp=w b.
$$

Nous regroupons la propriété du matériau et la géométrie dans la **conductance** $C$ :

$$
C=\frac{K A_\perp}{L}=\frac{K w b}{L},
\qquad
Q=-C(h_j-h_i).
$$

La conductance s'exprime en **m²/s**. Multipliée par une différence de charge en mètres, elle donne un débit en m³/s. Elle n'est donc pas un autre nom de la conductivité hydraulique : elle dépend aussi de la largeur, de l'épaisseur saturée et de la longueur de la connexion.

Imaginez deux canaux remplis du même sable. À longueur et différence de charge égales, un canal saturé plus large laisse passer davantage d'eau. Sa conductivité hydraulique reste identique, mais sa conductance est plus grande.

Par exemple, prenons $K=10^{-4}$ m/s, $w=10$ m, $b=5$ m et $L=100$ m. Alors $A_\perp=50$ m² et $C=5\times10^{-5}$ m²/s. Pour $h_i-h_j=2$ m, le débit vaut $10^{-4}$ m³/s, soit **0,1 L/s**. Si l'épaisseur saturée est divisée par deux, les autres grandeurs et la différence de charge restant constantes, la conductance et le débit sont divisés par deux ; la conductivité hydraulique ne change pas.

#### Relier deux mailles voisines

Entre les centres de deux mailles adjacentes, l'eau traverse la moitié de chacune. Chaque demi-maille oppose une résistance à l'écoulement. Pour des mailles de même longueur $\Delta x$ et de même largeur $w$, les résistances s'ajoutent :

$$
\frac{1}{C_{ij}}
=\frac{\Delta x/2}{K_i w b_i}
+\frac{\Delta x/2}{K_j w b_j}.
$$

$C_{ij}$ est la conductance de la connexion ; $K_i,K_j$ et $b_i,b_j$ sont les conductivités hydrauliques et les épaisseurs saturées des deux mailles. En définissant les transmissivités $T_i=K_i b_i$ et $T_j=K_j b_j$, en m²/s, on obtient :

$$
C_{ij}=\frac{2T_iT_j}{T_i+T_j}\frac{w}{\Delta x}.
$$

C'est l'expression fondée sur la moyenne harmonique des transmissivités utilisée dans le modèle à trois mailles. Une demi-maille peu transmissive peut limiter le débit de toute la connexion, comme un rétrécissement peut limiter l'écoulement dans un canal plus large. Si les deux mailles ont la même conductivité et la même épaisseur, l'expression se réduit à $C=Kwb/\Delta x$.
