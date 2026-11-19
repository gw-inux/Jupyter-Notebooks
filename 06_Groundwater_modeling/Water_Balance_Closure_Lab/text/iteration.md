**One Picard step.** Evaluate both face conductances at the previous head $h_k$. Hold these conductances fixed and solve the middle-cell balance for the next head.

$$
h_{k+1}=g(h_k)=\frac{C_L(h_k)h_L+C_R(h_k)h_R}{C_L(h_k)+C_R(h_k)}.
$$

“+ Next step” applies this update once. “− Previous step” restores the preceding estimate. Head-change closure requires $|h_{k+1}-h_k|\leq 0.0001$ m. The calculation retains full precision between steps. A confined run starting at 4 m reaches 2.5 m in one update. One further update confirms zero head change.

**Interpreting closure.** A small change measures how far the iteration moved. The flow residual measures how well the current head conserves water. A solver can check both. In the budget view you choose each trial head yourself. Newton’s method would use the residual and its slope to calculate a correction automatically.

The three-node teaching setup is inspired by Steffen Mehl’s study of Picard and Newton iteration. This exercise uses homogeneous conductivity and the prescribed heads of 4 m and 1 m. [Mehl (2006), *Ground Water*, 44(4), 583–594](https://doi.org/10.1111/j.1745-6584.2006.00207.x).
