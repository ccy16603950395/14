import pandas as pd
from src.analysis.standardize import winsorized_zscore


def test_zscore_cross_sectional():
    df = pd.DataFrame([[1,2,100],[2,3,4]], index=pd.date_range('2022-01-01', periods=2), columns=list('ABC'))
    z = winsorized_zscore(df)
    assert z.shape == df.shape
    assert abs(z.iloc[1].mean()) < 1e-8
