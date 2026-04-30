from __future__ import annotations

import numpy as np

from .materials import MaterialProperties


def compute_degradation(
    C: np.ndarray,
    material_map: np.ndarray,
    materials: dict[str, MaterialProperties],
    time: float,
) -> np.ndarray:
    deg = np.zeros_like(C)
    for name, mat in materials.items():
        mask = material_map == name
        deg[mask] = 1.0 - np.exp(-mat.degradation_rate * C[mask] * time)
    return np.clip(deg, 0.0, 1.0)


def compute_damage(degradation: np.ndarray) -> np.ndarray:
    return np.clip(degradation, 0.0, 1.0)


def compute_elastic_modulus_field(
    damage: np.ndarray,
    material_map: np.ndarray,
    materials: dict[str, MaterialProperties],
) -> np.ndarray:
    E = np.zeros_like(damage)
    for name, mat in materials.items():
        mask = material_map == name
        E[mask] = mat.elastic_modulus * (1.0 - mat.alpha_damage_to_E * damage[mask])
    return np.maximum(E, 0.0)


def compute_strength_field(
    damage: np.ndarray,
    material_map: np.ndarray,
    materials: dict[str, MaterialProperties],
) -> np.ndarray:
    s = np.zeros_like(damage)
    for name, mat in materials.items():
        mask = material_map == name
        s[mask] = mat.strength * (1.0 - mat.beta_damage_to_strength * damage[mask])
    return np.maximum(s, 0.0)
