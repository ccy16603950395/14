import numpy as np
import pandas as pd
from src.analysis.ic import compute_ic_series, summarize_ic


def test_ic_positive_relation():
    idx = pd.date_range('2022-01-01', periods=5)
    cols = list('ABCDE')
    f = pd.DataFrame([np.arange(5)+i for i in range(5)], index=idx, columns=cols)
    r = f * 0.01
    ic = compute_ic_series(f, r)
    s = summarize_ic(ic)
    assert ic.dropna().mean() > 0.9
    assert s['win_rate'] >= 0.8
