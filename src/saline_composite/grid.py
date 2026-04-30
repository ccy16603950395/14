from __future__ import annotations

import numpy as np

from .config import SimulationConfig


def create_grid(config: SimulationConfig) -> tuple[np.ndarray, np.ndarray]:
    x = np.arange(config.nx) * config.dx
    y = np.arange(config.ny) * config.dy
    return np.meshgrid(x, y, indexing="xy")


def create_material_map(config: SimulationConfig) -> np.ndarray:
    material_map = np.full((config.ny, config.nx), "rock", dtype=object)
    concrete_end = int(config.nx * config.concrete_ratio)
    interface_width = max(1, int(config.nx * config.interface_ratio))
    interface_end = min(config.nx, concrete_end + interface_width)

    material_map[:, :concrete_end] = "concrete"
    material_map[:, concrete_end:interface_end] = "interface"
    material_map[:, interface_end:] = "rock"
    return material_map
