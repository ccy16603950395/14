import numpy as np

from saline_composite.config import SimulationConfig
from saline_composite.grid import create_material_map
from saline_composite.materials import default_materials
from saline_composite.transport import apply_boundary_conditions, initialize_concentration


def test_concentration_shape() -> None:
    config = SimulationConfig(nx=30, ny=20)
    C = initialize_concentration(config)
    assert C.shape == (20, 30)


def test_boundary_conditions_applied() -> None:
    config = SimulationConfig(nx=20, ny=10, C0=2.0)
    C = np.zeros((10, 20))
    C = apply_boundary_conditions(C, config)
    assert (C[:, 0] == 2.0).all()
    assert np.allclose(C[:, -1], C[:, -2])
