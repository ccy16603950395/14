from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _plot_field(field: np.ndarray, title: str, path: Path, cmap: str = "viridis") -> None:
    fig, ax = plt.subplots(figsize=(8, 3.5))
    im = ax.imshow(field, origin="lower", cmap=cmap, aspect="auto")
    ax.set_title(title)
    ax.set_xlabel("x index")
    ax.set_ylabel("y index")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_concentration(C: np.ndarray, path: Path) -> None:
    _plot_field(C, "Concentration Field", path, cmap="Blues")


def plot_degradation(deg: np.ndarray, path: Path) -> None:
    _plot_field(deg, "Degradation Field", path, cmap="magma")


def plot_damage(damage: np.ndarray, path: Path) -> None:
    _plot_field(damage, "Damage Field", path, cmap="inferno")


def plot_elastic_modulus(E: np.ndarray, path: Path) -> None:
    _plot_field(E / 1e9, "Elastic Modulus Field (GPa)", path, cmap="viridis")


def plot_average_curves(history: dict[str, list[float]], path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    for key, values in history.items():
        if key != "time":
            ax.plot(history["time"], values, label=key)
    ax.set_xlabel("Time")
    ax.set_ylabel("Average value")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
