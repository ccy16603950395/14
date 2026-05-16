import numpy as np
import pandas as pd
from src.factors.momentum import momentum_20
from src.factors.reversal import reversal_5
from src.factors.volatility import volatility_20
from src.factors.volume_price import price_volume_divergence_20
from src.factors.turnover import turnover_20


def make_data():
    idx = pd.date_range('2022-01-01', periods=40)
    close = pd.DataFrame({'A': np.linspace(10, 20, 40), 'B': np.linspace(20, 10, 40)}, index=idx)
    volume = pd.DataFrame({'A': np.linspace(100, 200, 40), 'B': np.linspace(200, 100, 40)}, index=idx)
    turnover = pd.DataFrame({'A': np.linspace(1, 2, 40), 'B': np.linspace(2, 1, 40)}, index=idx)
    returns = close.pct_change()
    return close, volume, turnover, returns


def test_factors_shape_and_direction():
    close, volume, to, returns = make_data()
    m = momentum_20(close)
    r = reversal_5(close)
    v = volatility_20(returns)
    pvd = price_volume_divergence_20(close, volume)
    t = turnover_20(to)
    assert m.shape == close.shape
    assert r.shape == close.shape
    assert v.shape == close.shape
    assert pvd.shape == close.shape
    assert t.shape == close.shape
    assert m.iloc[-1]['A'] > 0 and m.iloc[-1]['B'] < 0
    assert r.iloc[-1]['A'] < 0 and r.iloc[-1]['B'] > 0
