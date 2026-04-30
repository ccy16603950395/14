from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MaterialProperties:
    name: str
    diffusion_coefficient: float
    degradation_rate: float
    elastic_modulus: float
    strength: float
    alpha_damage_to_E: float
    beta_damage_to_strength: float


def default_materials() -> dict[str, MaterialProperties]:
    return {
        "concrete": MaterialProperties(
            name="concrete",
            diffusion_coefficient=8e-4,
            degradation_rate=0.04,
            elastic_modulus=30e9,
            strength=35e6,
            alpha_damage_to_E=0.6,
            beta_damage_to_strength=0.7,
        ),
        "rock": MaterialProperties(
            name="rock",
            diffusion_coefficient=4e-4,
            degradation_rate=0.025,
            elastic_modulus=42e9,
            strength=55e6,
            alpha_damage_to_E=0.5,
            beta_damage_to_strength=0.55,
        ),
        "interface": MaterialProperties(
            name="interface",
            diffusion_coefficient=1.2e-3,
            degradation_rate=0.085,
            elastic_modulus=18e9,
            strength=20e6,
            alpha_damage_to_E=0.75,
            beta_damage_to_strength=0.8,
        ),
    }
