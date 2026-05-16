import pandas as pd

def turnover_20(turnover: pd.DataFrame) -> pd.DataFrame:
    return -turnover.rolling(20).mean()
