from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_loss_curve(log_df, out_path: Path):
    plt.figure(figsize=(8, 5))
    plt.plot(log_df["epoch"], log_df["train_loss"], label="train")
    plt.plot(log_df["epoch"], log_df["val_loss"], label="val")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_scatter_true_pred(y_true, y_pred, out_path: Path, title: str):
    plt.figure(figsize=(6, 6))
    plt.scatter(y_true, y_pred, s=2, alpha=0.5)
    vmin = min(np.min(y_true), np.min(y_pred))
    vmax = max(np.max(y_true), np.max(y_pred))
    plt.plot([vmin, vmax], [vmin, vmax], "r--")
    plt.xlabel("mises_true (Pa)")
    plt.ylabel("mises_pred (Pa)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_midplane_maps(df_pred, out_path: Path, title: str):
    z_mid = 0.5 * (df_pred["z"].min() + df_pred["z"].max())
    idx = (df_pred["z"] - z_mid).abs().nsmallest(max(500, min(3000, len(df_pred)//5))).index
    d = df_pred.loc[idx]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    sc0 = axes[0].scatter(d["x"], d["y"], c=d["mises_true"], s=6)
    axes[0].set_title("True Mises")
    plt.colorbar(sc0, ax=axes[0])

    sc1 = axes[1].scatter(d["x"], d["y"], c=d["mises_pred"], s=6)
    axes[1].set_title("Pred Mises")
    plt.colorbar(sc1, ax=axes[1])

    sc2 = axes[2].scatter(d["x"], d["y"], c=d["abs_error"], s=6)
    axes[2].set_title("Abs Error")
    plt.colorbar(sc2, ax=axes[2])

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
