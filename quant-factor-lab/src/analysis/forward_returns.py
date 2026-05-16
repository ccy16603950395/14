import pandas as pd


def compute_forward_returns(close: pd.DataFrame, horizons: list[int] = [1,5,10]) -> dict[str, pd.DataFrame]:
    out = {}
    for h in horizons:
        out[f'{h}D'] = close.shift(-h) / close - 1
    return out
