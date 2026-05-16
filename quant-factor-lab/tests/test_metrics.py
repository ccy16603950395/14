import pandas as pd
from src.backtest.metrics import calc_metrics


def test_metrics_output():
    rets = pd.Series([0.01, -0.005, 0.002, 0.0, 0.003])
    m = calc_metrics(rets)
    for c in ['cumulative_return','annual_return','annual_volatility','sharpe','max_drawdown','win_rate']:
        assert c in m.index
