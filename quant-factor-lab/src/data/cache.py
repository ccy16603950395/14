from __future__ import annotations
from pathlib import Path
import pandas as pd


def _preferred_path(base: Path, name: str) -> Path:
    parquet_path = base / f"{name}.parquet"
    csv_path = base / f"{name}.csv"
    return parquet_path if parquet_path.exists() else csv_path


def save_df(df: pd.DataFrame, base_dir: str | Path, name: str) -> Path:
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)
    parquet_path = base / f"{name}.parquet"
    try:
        df.to_parquet(parquet_path)
        return parquet_path
    except Exception:
        csv_path = base / f"{name}.csv"
        df.to_csv(csv_path, index=True)
        return csv_path


def load_df(base_dir: str | Path, name: str) -> pd.DataFrame | None:
    base = Path(base_dir)
    path = _preferred_path(base, name)
    if not path.exists():
        return None
    if path.suffix == '.parquet':
        return pd.read_parquet(path)
    return pd.read_csv(path, index_col=0, parse_dates=True)
