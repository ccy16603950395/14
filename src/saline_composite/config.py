from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SimulationConfig:
    nx: int = 120
    ny: int = 60
    dx: float = 0.01
    dy: float = 0.01
    dt: float = 0.05
    total_time: float = 30.0
    output_interval: int = 20
    C0: float = 1.0

    concrete_ratio: float = 0.45
    interface_ratio: float = 0.1

    output_dir: Path = Path("outputs")
    random_seed: int | None = None
    save_figures: bool = True

    def n_steps(self) -> int:
        return int(self.total_time / self.dt)
