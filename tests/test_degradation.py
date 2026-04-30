import numpy as np

from saline_composite.config import SimulationConfig
from saline_composite.degradation import (
    compute_damage,
    compute_degradation,
    compute_elastic_modulus_field,
    compute_strength_field,
)
from saline_composite.grid import create_material_map
from saline_composite.materials import default_materials


def test_degradation_range_and_non_negative_fields() -> None:
    config = SimulationConfig(nx=30, ny=20)
    mats = default_materials()
    material_map = create_material_map(config)
    C = np.ones((20, 30)) * 0.8
    deg = compute_degradation(C, material_map, mats, time=10.0)
    dmg = compute_damage(deg)
    E = compute_elastic_modulus_field(dmg, material_map, mats)
    s = compute_strength_field(dmg, material_map, mats)
    assert np.min(deg) >= 0 and np.max(deg) <= 1
    assert np.min(E) >= 0
    assert np.min(s) >= 0
