import pandas as pd

def volatility_20(returns: pd.DataFrame) -> pd.DataFrame:
    return -returns.rolling(20).std()
