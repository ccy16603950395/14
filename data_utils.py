import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from config import (
    CASE_INFO_COLUMN_MAPPING,
    GLOBAL_FEATURES,
    INTERNAL_DIR,
    SAMPLE_POINTS_PER_CASE,
    SURFACE_DIR,
    TARGET_COL,
)


def clean_col(name: str) -> str:
    s = str(name).strip().lstrip("% ").strip()
    s = s.replace("-w", "minus_w")
    s = s.replace(".", "_")
    s = s.replace("(", "_").replace(")", "")
    s = s.replace("/", "_")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^0-9a-zA-Z_]+", "", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s.lower()


def _detect_header_line(path: Path) -> int:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            line_clean = line.strip().lstrip("%").strip().lower()
            if ("x" in line_clean) and ("y" in line_clean) and ("z" in line_clean):
                return i
    raise ValueError(f"Cannot find header containing X/Y/Z in {path}")


def read_comsol_csv(path: Path) -> pd.DataFrame:
    h = _detect_header_line(path)
    for sep in [",", r"\s+"]:
        try:
            df = pd.read_csv(path, skiprows=h, sep=sep, engine="python", comment=None)
            if df.shape[1] >= 4:
                df.columns = [clean_col(c) for c in df.columns]
                return df
        except Exception:
            continue
    raise ValueError(f"Failed to parse {path}")


def resolve_case_info(case_info_path: Path) -> pd.DataFrame:
    df = pd.read_csv(case_info_path)
    lower = {c.lower(): c for c in df.columns}
    renamed = {}
    for target, candidates in CASE_INFO_COLUMN_MAPPING.items():
        hit = None
        for cand in candidates:
            key = cand.lower()
            if key in lower:
                hit = lower[key]
                break
        if hit is None:
            raise KeyError(f"case_info missing field '{target}', available columns: {list(df.columns)}")
        renamed[hit] = target
    out = df.rename(columns=renamed)
    out["case"] = out["case"].astype(str).str.lower().str.replace(".csv", "", regex=False)
    return out


def _safe_col(df: pd.DataFrame, candidates: List[str], path: Path) -> str:
    for c in candidates:
        if c in df.columns:
            return c
    print(f"[ColumnMissing] {path} columns: {list(df.columns)}")
    raise KeyError(f"Missing any of {candidates} in {path}")


def extract_surface_features(surface_df: pd.DataFrame) -> Dict[str, float]:
    feats = {}
    use_cols = ["u_mm", "v_mm", "w_mm", "minus_w_mm", "solid_disp_mm"]
    for col in use_cols:
        if col in surface_df.columns:
            v = surface_df[col].to_numpy(dtype=float)
            feats[f"surf_{col}_mean"] = np.nanmean(v)
            feats[f"surf_{col}_std"] = np.nanstd(v)
            feats[f"surf_{col}_min"] = np.nanmin(v)
            feats[f"surf_{col}_max"] = np.nanmax(v)
            feats[f"surf_{col}_p95"] = np.nanpercentile(v, 95)

    if "solid_disp_mm" in surface_df.columns:
        amp = surface_df["solid_disp_mm"].to_numpy(dtype=float)
    else:
        ux = surface_df.get("u_mm", 0.0)
        uy = surface_df.get("v_mm", 0.0)
        uz = surface_df.get("w_mm", 0.0)
        amp = np.sqrt(np.asarray(ux, dtype=float) ** 2 + np.asarray(uy, dtype=float) ** 2 + np.asarray(uz, dtype=float) ** 2)

    z = surface_df["z"].to_numpy(dtype=float)
    theta = np.arctan2(surface_df["y"].to_numpy(dtype=float), surface_df["x"].to_numpy(dtype=float))

    z_bins = np.quantile(z, [0, 0.25, 0.5, 0.75, 1.0])
    for i in range(4):
        m = (z >= z_bins[i]) & (z <= z_bins[i + 1] if i == 3 else z < z_bins[i + 1])
        vv = amp[m] if m.any() else np.array([0.0])
        feats[f"zbin_{i}_amp_mean"] = float(np.mean(vv))
        feats[f"zbin_{i}_amp_max"] = float(np.max(vv))

    t_edges = np.linspace(-np.pi, np.pi, 9)
    for i in range(8):
        m = (theta >= t_edges[i]) & (theta < t_edges[i + 1] if i < 7 else theta <= t_edges[i + 1])
        vv = amp[m] if m.any() else np.array([0.0])
        feats[f"tbin_{i}_amp_mean"] = float(np.mean(vv))
        feats[f"tbin_{i}_amp_max"] = float(np.max(vv))

    return feats


def build_case_dataframe(case: str, case_info_row: pd.Series) -> pd.DataFrame:
    s_path = SURFACE_DIR / f"{case}.csv"
    i_path = INTERNAL_DIR / f"{case}.csv"
    s_df = read_comsol_csv(s_path)
    i_df = read_comsol_csv(i_path)

    for required in ["x", "y", "z", TARGET_COL]:
        if required not in i_df.columns:
            print(f"[ColumnMissing] {i_path} columns: {list(i_df.columns)}")
            raise KeyError(f"{required} missing in {i_path}")
    for required in ["x", "y", "z"]:
        if required not in s_df.columns:
            print(f"[ColumnMissing] {s_path} columns: {list(s_df.columns)}")
            raise KeyError(f"{required} missing in {s_path}")

    surf_feats = extract_surface_features(s_df)

    n = len(i_df)
    out = pd.DataFrame()
    out["case"] = [case] * n
    out["x"] = i_df["x"].astype(float)
    out["y"] = i_df["y"].astype(float)
    out["z"] = i_df["z"].astype(float)
    out["r"] = np.sqrt(out["x"] ** 2 + out["y"] ** 2)
    out["theta"] = np.arctan2(out["y"], out["x"])

    for g in GLOBAL_FEATURES:
        out[g] = float(case_info_row[g])
    for k, v in surf_feats.items():
        out[k] = float(v)

    out[TARGET_COL] = i_df[TARGET_COL].astype(float)
    return out


def sample_case_points(df_case: pd.DataFrame, n_sample=SAMPLE_POINTS_PER_CASE, seed=42):
    if len(df_case) <= n_sample:
        return df_case.copy()
    return df_case.sample(n=n_sample, random_state=seed)


def compute_normalizer(x_train: np.ndarray, y_train: np.ndarray):
    x_mean = x_train.mean(axis=0)
    x_std = x_train.std(axis=0)
    x_std[x_std == 0] = 1.0
    y_mean = float(y_train.mean())
    y_std = float(y_train.std()) if float(y_train.std()) != 0 else 1.0
    return x_mean, x_std, y_mean, y_std


class TabularTensorDataset(Dataset):
    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.x = torch.tensor(x, dtype=torch.float32)
        self.y = torch.tensor(y.reshape(-1, 1), dtype=torch.float32)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
