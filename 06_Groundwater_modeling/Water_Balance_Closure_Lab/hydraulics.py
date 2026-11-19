"""Steady three-cell Darcy balance. Heads in m, K in m/s, discharges in m³/s.

Contents
1. Geometry and teaching tolerances
2. Face conductance, cell budget and Picard update
3. Residual derivative and damped Newton update
"""

# 1. Geometry and teaching tolerances
LEFT, RIGHT = 4.0, 1.0
DX, WIDTH = 100.0, 1.0   # Centre-to-centre spacing and out-of-plane width [m]
ROOF, BASE = 0.0, -2.0   # Confined aquifer elevations [m]
WATER_TABLE_BASE = 0.0   # Unconfined aquifer bottom [m]
WATER_TABLE_TOP = 5.0    # All supported heads lie below this aquifer top [m]
DAY = 86_400.0
BUDGET_TOL_PCT = 0.01
HEAD_TOL = 0.0001


# 2. Face conductance, cell budget and Picard update
def conductances(head, conductivity, unconfined):
    """Conductance [m²/s] at the left and right faces of the middle cell."""
    scale = conductivity * WIDTH / DX
    if unconfined:
        # With a horizontal base, integrating T = K(h − z_base) between
        # node heads gives the arithmetic mean saturated thickness exactly.
        return (scale * ((LEFT + head) / 2 - WATER_TABLE_BASE),
                scale * ((head + RIGHT) / 2 - WATER_TABLE_BASE))
    face = scale * (ROOF - BASE)
    return face, face


def budget(head, conductivity, unconfined):
    """Both discharges are positive to the right within the trial-head range."""
    left, right = conductances(head, conductivity, unconfined)
    inflow = left * (LEFT - head)
    outflow = right * (head - RIGHT)
    residual = inflow - outflow
    # For different boundary heads at least one of the two fluxes is positive.
    discrepancy_pct = 200 * residual / (inflow + outflow)
    return inflow, outflow, residual, discrepancy_pct


def picard(head, conductivity, unconfined):
    """Freeze both face conductances at the previous head, then solve for h."""
    left, right = conductances(head, conductivity, unconfined)
    return (left * LEFT + right * RIGHT) / (left + right)


# 3. Residual derivative and damped Newton update
def residual_derivative(head, conductivity, unconfined):
    """Full derivative d(Q_in − Q_out)/dh [m²/s], including dC/dh."""
    thickness = head - WATER_TABLE_BASE if unconfined else ROOF - BASE
    return -2 * conductivity * WIDTH / DX * thickness


def newton(head, conductivity, unconfined):
    """Return the next head and the applied fraction of the Newton correction.

    A low starting head can overshoot the permitted 1–4 m interval. Halve
    the correction until it lies in that interval and reduces |R|. Retain
    full precision. The UI stops applying updates at its budget tolerance.
    """
    residual = budget(head, conductivity, unconfined)[2]
    correction = -residual / residual_derivative(head, conductivity, unconfined)
    fraction = 1.0
    for _ in range(30):
        updated = head + fraction * correction
        if RIGHT <= updated <= LEFT and abs(budget(updated, conductivity, unconfined)[2]) <= abs(residual):
            return updated, fraction
        fraction *= 0.5
    raise ArithmeticError("Newton update could not reduce the residual.")
