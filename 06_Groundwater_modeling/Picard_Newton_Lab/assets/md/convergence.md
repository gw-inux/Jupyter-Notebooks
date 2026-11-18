A small correction alone is insufficient: the balance may still be poor. Check **both** the maximum absolute head change and maximum absolute flow residual. The experiments let you choose these closure criteria. The defaults are $10^{-4}$ m for head change and $10^{-6}$ m³/s for flow residual.

**Why another update after the flow residual passes?** The last head change may still exceed its own threshold. In a linear problem, the first update can reach the head solution with zero residual, while making a large change from the initial guess. A second, unchanged update confirms head-change closure. In Mehl’s small-flow examples, even the initial guess can pass a 1E-6 m³/s flow test while still having a substantial head error. Passing the flow test alone is therefore insufficient.

The convergence graph shows the maximum head change on its left logarithmic axis and the maximum flow residual on its right logarithmic axis. Both scales stay fixed from $10^{-12}$ to $100$, in their respective units. Purple identifies the flow axis and its closure line; ochre identifies the head-change axis and its closure line. Squares identify flow residuals; circles identify head changes. Green identifies Picard and blue identifies Newton. Edge triangles mark values outside the view: downward for values below the lower limit (including zero), upward for values above the upper limit. A selected closure outside the view still applies and remains listed in the legend.

The head change is computed between accepted iterates; no head-change value is invented at the initial guess. A separate figure below shows the selected cell’s actual head and reference head. The reference head is a visual reference; the iteration does not use the error relative to that known solution as its stopping test.

For a smooth scalar Picard function, $|f'_P(h^*)|<1$ is a sufficient condition for local convergence: sufficiently close estimates move toward the solution. Here $f'_P$ is the derivative of the head-update function with respect to its input head; it is dimensionless. A negative local slope alternates the error sign. Newton can converge quadratically near a smooth root with nonzero derivative, meaning that the remaining head error can decrease very rapidly. An unsuitable starting head or a change between ET segments can prevent convergence. Neither method is universally best.

For many unknown heads, one outer iteration solves a coupled matrix equation:

$$\mathbf A(\mathbf h^k)\widehat{\mathbf h}_P^{k+1}=\mathbf b(\mathbf h^k),\qquad
\mathbf J(\mathbf h^k)\Delta\mathbf h=-\mathbf F(\mathbf h^k).$$

Here $\mathbf h^k$ is the vector of current interior heads (m); $\widehat{\mathbf h}_P^{k+1}$ contains the proposed Picard heads (m); and $\Delta\mathbf h$ contains the Newton head corrections (m). The matrix $\mathbf A$ contains the fixed conductances and active boundary-condition slopes (m²/s), and $\mathbf b$ contains the corresponding boundary and source terms (m³/s). The vector $\mathbf F$ contains the cell flow residuals (m³/s), and $\mathbf J$ is their Jacobian: the matrix of derivatives with respect to the unknown heads (m²/s).

These linear systems are solved directly here. No inner linear-solver iteration history is displayed.
