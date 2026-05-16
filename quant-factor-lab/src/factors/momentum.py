import pandas as pd

def momentum_20(close: pd.DataFrame) -> pd.DataFrame:
    return close / close.shift(20) - 1
