import pandas as pd

def reversal_5(close: pd.DataFrame) -> pd.DataFrame:
    return -(close / close.shift(5) - 1)
