from __future__ import annotations

import numpy as np

from .config import SimulationConfig
from .degradation import (
    compute_damage,
    compute_degradation,
    compute_elastic_modulus_field,
    compute_strength_field,
)
from .grid import create_material_map
from .materials import MaterialProperties, default_materials
from .transport import check_stability, compute_diffusion_step, initialize_concentration
from .utils import ensure_directory
from .visualization import (
    plot_average_curves,
    plot_concentration,
    plot_damage,
    plot_degradation,
    plot_elastic_modulus,
)


class SalineCompositeSimulation:
    def __init__(self, config: SimulationConfig, materials: dict[str, MaterialProperties] | None = None) -> None:
        self.config = config
        self.materials = materials or default_materials()
        check_stability(config, self.materials)
        self.material_map = create_material_map(config)
        self.time = 0.0
        self.C = initialize_concentration(config)
        self.degradation = np.zeros_like(self.C)
        self.damage = np.zeros_like(self.C)
        self.elastic_modulus = np.zeros_like(self.C)
        self.strength = np.zeros_like(self.C)
        self.history: dict[str, list[float]] = {"time": [], "C": [], "degradation": [], "damage": [], "E_GPa": [], "strength_MPa": []}

    def initialize(self) -> None:
        ensure_directory(self.config.output_dir)
        self.time = 0.0

    def step(self) -> None:
        self.C = compute_diffusion_step(self.C, self.material_map, self.materials, self.config)
        self.time += self.config.dt
        self.degradation = compute_degradation(self.C, self.material_map, self.materials, self.time)
        self.damage = compute_damage(self.degradation)
        self.elastic_modulus = compute_elastic_modulus_field(self.damage, self.material_map, self.materials)
        self.strength = compute_strength_field(self.damage, self.material_map, self.materials)
        self._record_history()

    def _record_history(self) -> None:
        self.history["time"].append(self.time)
        self.history["C"].append(float(np.mean(self.C)))
        self.history["degradation"].append(float(np.mean(self.degradation)))
        self.history["damage"].append(float(np.mean(self.damage)))
        self.history["E_GPa"].append(float(np.mean(self.elastic_modulus) / 1e9))
        self.history["strength_MPa"].append(float(np.mean(self.strength) / 1e6))

    def run(self) -> None:
        self.initialize()
        for _ in range(self.config.n_steps()):
            self.step()
        self.save_results()

    def save_results(self) -> None:
        if not self.config.save_figures:
            return
        out = self.config.output_dir
        plot_concentration(self.C, out / "concentration_final.png")
        plot_degradation(self.degradation, out / "degradation_final.png")
        plot_damage(self.damage, out / "damage_final.png")
        plot_elastic_modulus(self.elastic_modulus, out / "elastic_modulus_final.png")
        plot_average_curves(self.history, out / "average_curves.png")

    def get_summary_metrics(self) -> dict[str, float]:
        return {
            "time": self.time,
            "avg_C": float(np.mean(self.C)),
            "avg_degradation": float(np.mean(self.degradation)),
            "avg_damage": float(np.mean(self.damage)),
            "avg_E_GPa": float(np.mean(self.elastic_modulus) / 1e9),
            "avg_strength_MPa": float(np.mean(self.strength) / 1e6),
        }
