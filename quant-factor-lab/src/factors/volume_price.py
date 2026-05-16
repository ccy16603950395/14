import pandas as pd

def price_volume_divergence_20(close: pd.DataFrame, volume: pd.DataFrame) -> pd.DataFrame:
    pc = close.pct_change()
    vc = volume.pct_change()
    return -pc.rolling(20).corr(vc)
