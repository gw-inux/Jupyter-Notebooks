La soluzione di Theis descrive il flusso radiale transitorio verso un pozzo che pompa a una portata costante $Q$ in un acquifero confinato.

L'abbassamento piezometrico (*drawdown*) è dato da:

$$
s(r,t) = \frac{Q}{4\pi T} W(u)
$$

con

$$
u = \frac{r^2 S}{4 T t}
$$

La derivata dell'abbassamento rispetto al logaritmo naturale del tempo è:

$$
\frac{\partial s}{\partial \ln(t)}
=
t \frac{\partial s}{\partial t}
=
\frac{Q}{4\pi T} e^{-u}
$$

Per tempi sufficientemente lunghi, $u$ diventa piccolo ed $e^{-u}$ tende a 1. Di conseguenza, la derivata tende a un valore costante, chiamato *plateau della derivata*:

$$
d = \frac{Q}{4\pi T}
$$

Questa relazione è particolarmente utile perché il valore del plateau dipende direttamente dalla trasmissività dell'acquifero.