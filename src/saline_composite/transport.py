from __future__ import annotations

import numpy as np

from .config import SimulationConfig
from .materials import MaterialProperties


def initialize_concentration(config: SimulationConfig) -> np.ndarray:
    C = np.zeros((config.ny, config.nx), dtype=float)
    return apply_boundary_conditions(C, config)


def apply_boundary_conditions(C: np.ndarray, config: SimulationConfig) -> np.ndarray:
    C[:, 0] = config.C0
    C[:, -1] = C[:, -2]
    C[0, :] = C[1, :]
    C[-1, :] = C[-2, :]
    C[:, 0] = config.C0
    return C


def check_stability(config: SimulationConfig, materials: dict[str, MaterialProperties]) -> None:
    dmax = max(m.diffusion_coefficient for m in materials.values())
    limit = 1.0 / (2.0 * dmax * (1.0 / config.dx**2 + 1.0 / config.dy**2))
    if config.dt > limit:
        raise ValueError(f"Unstable dt={config.dt:.3e}, should be <= {limit:.3e}")


def compute_diffusion_step(
    C: np.ndarray,
    material_map: np.ndarray,
    materials: dict[str, MaterialProperties],
    config: SimulationConfig,
) -> np.ndarray:
    Cn = C.copy()
    Cnext = C.copy()
    for j in range(1, config.ny - 1):
        for i in range(1, config.nx - 1):
            D = materials[material_map[j, i]].diffusion_coefficient
            lap = ((Cn[j, i + 1] - 2 * Cn[j, i] + Cn[j, i - 1]) / config.dx**2
                   + (Cn[j + 1, i] - 2 * Cn[j, i] + Cn[j - 1, i]) / config.dy**2)
            Cnext[j, i] = Cn[j, i] + config.dt * D * lap

    return apply_boundary_conditions(Cnext, config)
