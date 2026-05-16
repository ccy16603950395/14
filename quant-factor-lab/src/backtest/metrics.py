import numpy as np
import pandas as pd

def calc_metrics(returns: pd.Series, periods_per_year: int=252) -> pd.Series:
    cum = (1+returns).prod()-1
    ann = (1+cum)**(periods_per_year/max(len(returns),1))-1
    vol = returns.std()*np.sqrt(periods_per_year)
    sharpe = ann/vol if vol>0 else 0.0
    nav = (1+returns).cumprod()
    dd = nav/nav.cummax()-1
    max_dd = dd.min() if len(dd) else 0.0
    win_rate = (returns>0).mean()
    return pd.Series({'cumulative_return':cum,'annual_return':ann,'annual_volatility':vol,'sharpe':sharpe,'max_drawdown':max_dd,'win_rate':win_rate})
