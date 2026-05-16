import pandas as pd

def build_monthly_topk_weights(score: pd.DataFrame, top_k: int = 5) -> pd.DataFrame:
    w = pd.DataFrame(0.0, index=score.index, columns=score.columns)
    rebalance_dates = score.groupby(score.index.to_period('M')).tail(1).index
    current = pd.Series(0.0, index=score.columns)
    for d in score.index:
        if d in rebalance_dates:
            s = score.loc[d].dropna().sort_values(ascending=False).head(top_k)
            current[:] = 0.0
            if len(s)>0:
                current.loc[s.index] = 1/len(s)
        w.loc[d] = current
    return w
