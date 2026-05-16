import pandas as pd


def winsorized_zscore(df: pd.DataFrame, lower: float = 0.01, upper: float = 0.99) -> pd.DataFrame:
    def _row(row: pd.Series) -> pd.Series:
        ql, qu = row.quantile(lower), row.quantile(upper)
        c = row.clip(ql, qu)
        s = c.std()
        return (c - c.mean()) / s if s and s > 0 else c * 0
    return df.apply(_row, axis=1)
