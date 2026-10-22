"""Check the physical connections in the coastal pressure illustration."""

import numpy as np
import pytest

from core.figures import density_principle
from core.i18n import TEXT


def test_coastal_columns_share_interface_depth_and_local_water_levels():
    fig = density_principle(lambda key: TEXT[key]["en"])
    lines = {line.get_gid(): line for line in fig.axes[0].lines if line.get_gid()}
    land_x, land = lines["density_land"].get_data()
    x, head = lines["density_water_table"].get_data()
    interface_x, interface = lines["density_interface"].get_data()
    salt_x, salt_y = lines["density_salt_column"].get_data()
    fresh_x, fresh_y = lines["density_fresh_column"].get_data()

    # Shoreline, water table and sharp interface meet at the sea-level datum.
    assert x[0] == land_x[0] == interface_x[0]
    assert head[0] == land[0] == interface[0] == 0
    assert np.all(head[1:] > 0)
    assert np.all(interface[1:] < 0)
    assert np.all(head[1:] < land[1:])

    # Connected columns compare pressures at one point on the interface.
    assert salt_x[-1] == fresh_x[0] == fresh_x[-1]
    assert salt_y[0] == 0
    assert salt_y[-1] == fresh_y[0]
    assert fresh_y[0] == pytest.approx(np.interp(fresh_x[0], x, interface), abs=1e-5)
    assert fresh_y[-1] == pytest.approx(np.interp(fresh_x[-1], x, head), abs=1e-5)
    assert fresh_y[-1] > salt_y[0] > fresh_y[0]
    fig.clear()
