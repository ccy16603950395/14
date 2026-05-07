import numpy as np
import pandas as pd
import torch
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from config import *
from data_utils import build_case_dataframe, resolve_case_info, sample_case_points
from model import LightPINN
from plot_utils import plot_midplane_maps, plot_scatter_true_pred


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    ckpt = torch.load(OUTPUT_DIR / "best_model.pt", map_location="cpu")
    feature_names = ckpt["feature_names"]
    norm = ckpt["normalizer"]

    model = LightPINN(len(feature_names), out_dim=4)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()

    case_info = resolve_case_info(CASE_INFO_PATH)
    ci = {r["case"]: r for _, r in case_info.iterrows()}

    metrics = []
    for c in TEST_CASES:
        df = build_case_dataframe(c, ci[c])
        df = sample_case_points(df, SAMPLE_POINTS_PER_CASE, RANDOM_SEED)

        x = df[feature_names].to_numpy(float)
        y_true = df[TARGET_COL].to_numpy(float)
        x_n = (x - norm["x_mean"]) / norm["x_std"]

        with torch.no_grad():
            y_pred_n = model(torch.tensor(x_n, dtype=torch.float32))[:, 3].numpy().reshape(-1)
        y_pred = y_pred_n * norm["y_std"] + norm["y_mean"]

        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / np.clip(np.abs(y_true), 1e-12, None))) * 100
        rel_rmse = rmse / (np.mean(np.abs(y_true)) + 1e-12)
        metrics.append({"case": c, "RMSE": rmse, "MAE": mae, "R2": r2, "MAPE": mape, "relative_RMSE": rel_rmse})

        out = pd.DataFrame({
            "x": df["x"], "y": df["y"], "z": df["z"],
            "mises_true": y_true, "mises_pred": y_pred,
        })
        out["abs_error"] = np.abs(out["mises_true"] - out["mises_pred"])
        out["relative_error"] = out["abs_error"] / np.clip(np.abs(out["mises_true"]), 1e-12, None)
        out.to_csv(PRED_DIR / f"{c}_prediction.csv", index=False)

        plot_scatter_true_pred(y_true, y_pred, FIG_DIR / f"{c}_scatter.png", f"{c}: true vs pred")
        plot_midplane_maps(out, FIG_DIR / f"{c}_midplane.png", f"{c} mid-plane")

    pd.DataFrame(metrics).to_csv(OUTPUT_DIR / "test_metrics.csv", index=False)


if __name__ == "__main__":
    main()
