from saline_composite.config import SimulationConfig
from saline_composite.grid import create_material_map


def test_material_map_shape_and_regions() -> None:
    config = SimulationConfig(nx=100, ny=40)
    m = create_material_map(config)
    assert m.shape == (40, 100)
    assert "concrete" in m
    assert "interface" in m
    assert "rock" in m
