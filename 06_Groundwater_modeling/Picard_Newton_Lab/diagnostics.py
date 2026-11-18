"""Read-only constructions for a coupled iteration; no alternative solver.

TABLE OF CONTENTS
  1. Potential and exact elimination of the other cell balances
  2. Select the latest accepted step or the initial/rejected input state
  3. Evaluate a Picard directional cut or exact reduced Newton residual
  4. Find a sustained near-reference tail for a head-history detail panel

Picard uses a directional restriction of its full-vector map. Newton uses
exact nonlinear elimination, possible because the current 11-cell balance is
linear in discharge potential. Neither construction advances any heads.
"""

import numpy as np
from .model import assemble, iteration_proposal


# 1. The potential and Schur reduction are exact for this fixed-K model.
def potential(model, heads):
    b = np.asarray(heads, dtype=float) - model.bottom
    if not model.unconfined:
        return model.thickness * b
    wet = b if model.top is None else np.minimum(b, model.top - model.bottom)
    return 0.5 * wet**2 + wet * (b - wet)


def reduced_balance(model, cell):
    """Schur complement S and c for F_reduced(h_i)=c-S*Phi(h_i).

    Eliminate the OTHER eight potential unknowns from B*Phi=s. This is exact
    for the present fixed-K/recharge model, including mixed roof branches.
    It is not a generic elimination rule for nonlinear boundary conditions.
    """
    if model.et_max or (
        model.unconfined and model.conductance != "integrated_thickness"
    ):
        return None
    k = np.asarray(model.conductivity, dtype=float)
    faces = 2 / (1 / k[:-1] + 1 / k[1:]) * model.width / model.dx
    matrix = np.diag(faces[:-1] + faces[1:])
    matrix += np.diag(-faces[1:-1], 1) + np.diag(-faces[1:-1], -1)
    source = np.full(model.n - 2, model.recharge * model.area)
    source[0] += faces[0] * potential(model, model.left)
    source[-1] += faces[-1] * potential(model, model.right)
    i = cell - 1
    other = np.arange(model.n - 2) != i
    eliminated = np.linalg.solve(
        matrix[np.ix_(other, other)], np.column_stack([matrix[other, i], source[other]])
    )
    schur = matrix[i, i] - matrix[i, other] @ eliminated[:, 0]
    forcing = source[i] - matrix[i, other] @ eliminated[:, 1]
    return float(schur), float(forcing)


# 2. Always reconstruct the same undamped proposal used by the actual solver.
def coupled_step(model, state, method, cell, omega=1.0):
    failed = state["rejected"] is not None
    accepted = len(state["heads"]) > 1 and not failed
    k = len(state["heads"]) - (2 if accepted else 1)
    base = np.asarray(state["heads"][k], dtype=float)
    weight = state["omega"][k] if accepted else omega
    direction = iteration_proposal(model, base, method) - base
    # If this head barely moves, a direction-to-head parameterization would
    # divide by a negligible number. A selected-head slice through the input
    # vector has the same exact map value at that input and keeps the head axis.
    small = abs(direction[cell]) <= 1e-10 * max(1.0, max(abs(direction)))
    head_slice = method == "Picard" and small
    use_alpha = small and not head_slice
    x0 = 0.0 if use_alpha else base[cell]
    scale = 1.0 if use_alpha else direction[cell]
    residual = assemble(model, base)[2][cell - 1]
    slope = (
        (assemble(model, base)[3] @ direction[1:-1])[cell - 1] / scale
        if method == "Newton"
        else 0.0
    )
    reduced = (
        reduced_balance(model, cell) if method == "Newton" and model.n > 3 else None
    )
    if reduced is not None:
        schur, forcing = reduced
        residual = forcing - schur * potential(model, base[cell])
        wet = (
            min(base[cell], model.top) if model.top is not None else base[cell]
        ) - model.bottom
        slope = -schur * (wet if model.unconfined else model.thickness)
        use_alpha, x0, scale = False, base[cell], direction[cell]
    return dict(
        base=base,
        direction=direction,
        omega=weight,
        k=k,
        accepted=accepted,
        failed=failed,
        use_alpha=use_alpha,
        head_slice=head_slice,
        x0=x0,
        xfull=x0 + scale,
        xend=x0 + weight * scale,
        residual=residual,
        slope=slope,
        cell=cell,
        method=method,
        reduced=reduced,
    )


# 3. The exact reduced residual avoids a misleading zero local-residual tangent.
def step_values(model, step, xs):
    xs = np.asarray(xs, dtype=float)
    if step["reduced"] is not None:
        schur, forcing = step["reduced"]
        values = forcing - schur * potential(model, xs)
        return (
            np.where(xs > model.bottom, values, np.nan) if model.unconfined else values
        )
    cell = step["cell"]
    alpha = (
        xs
        if step["use_alpha"] or step["head_slice"]
        else (xs - step["x0"]) / step["direction"][cell]
    )
    values = np.full(xs.shape, np.nan)
    for idx, fraction in np.ndenumerate(alpha):
        if step["head_slice"]:
            trial = step["base"].copy()
            trial[cell] = fraction
        else:
            trial = step["base"] + fraction * step["direction"]
        if model.unconfined and min(trial) <= model.bottom:
            continue  # Do not extrapolate the wet-cell equations into dry heads.
        try:
            values[idx] = (
                iteration_proposal(model, trial, "Picard")[cell]
                if step["method"] == "Picard"
                else assemble(model, trial)[2][cell - 1]
            )
        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            continue
    return values


# 4. A small change alone is insufficient: also require proximity to reference.
def detail_tails(states, cell, reference_head, threshold=0.01, consecutive=3):
    tails = {}
    for method, state in states.items():
        heads = np.asarray(state["heads"], dtype=float)[:, cell]
        near = np.abs(heads - reference_head) < threshold
        small = (np.abs(np.diff(heads)) < threshold) & near[:-1] & near[1:]
        if len(small) < consecutive or not np.all(small[-consecutive:]):
            continue
        start = len(small) - consecutive
        while start > 0 and small[start - 1]:
            start -= 1
        tails[method] = (np.arange(start, len(heads)), heads[start:])
    return tails
