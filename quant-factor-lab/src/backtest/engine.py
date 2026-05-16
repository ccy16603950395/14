import pandas as pd
from .portfolio import build_monthly_topk_weights


def run_backtest(close: pd.DataFrame, score: pd.DataFrame, initial_capital: float=1_000_000, top_k: int=5, buy_fee: float=0.0003, sell_fee: float=0.0003, stamp_duty: float=0.0005, slippage: float=0.0005) -> pd.DataFrame:
    rets = close.pct_change().fillna(0)
    w = build_monthly_topk_weights(score, top_k=top_k)
    w_prev = w.shift(1).fillna(0)
    turn = (w - w_prev).abs().sum(axis=1)
    buy_turn = (w - w_prev).clip(lower=0).sum(axis=1)
    sell_turn = (w_prev - w).clip(lower=0).sum(axis=1)
    costs = buy_turn*(buy_fee+slippage)+sell_turn*(sell_fee+stamp_duty+slippage)
    strat_ret = (w_prev*rets).sum(axis=1)-costs
    nav = (1+strat_ret).cumprod()*initial_capital
    bench_ret = rets.mean(axis=1)
    bench_nav = (1+bench_ret).cumprod()*initial_capital
    return pd.DataFrame({'strategy_return':strat_ret,'strategy_nav':nav,'benchmark_nav':bench_nav,'turnover':turn})
