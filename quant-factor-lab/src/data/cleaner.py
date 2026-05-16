from __future__ import annotations
import pandas as pd
from scipy.stats.mstats import winsorize


def clean_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy().sort_index()
    out = out[out['volume'].fillna(0) > 0]
    out = out.dropna(subset=['open', 'high', 'low', 'close'])
    out['return'] = out['close'].pct_change()
    if out['return'].notna().sum() > 5:
        out['return'] = pd.Series(winsorize(out['return'].fillna(0).values, limits=[0.01, 0.01]), index=out.index)
    out['is_suspended'] = (out['volume'] == 0).astype(int)
    return out


def to_wide(panel: dict[str, pd.DataFrame], field: str) -> pd.DataFrame:
    return pd.concat({k: v[field] for k, v in panel.items()}, axis=1).sort_index()
