import pandas as pd


def compute_ic_series(factor: pd.DataFrame, fwd: pd.DataFrame, method: str = 'pearson') -> pd.Series:
    idx = factor.index.intersection(fwd.index)
    vals=[]
    for d in idx:
        df = pd.concat([factor.loc[d], fwd.loc[d]], axis=1).dropna()
        if len(df) < 3:
            vals.append(float('nan'))
        else:
            vals.append(df.iloc[:,0].corr(df.iloc[:,1], method=method))
    return pd.Series(vals, index=idx)


def summarize_ic(ic: pd.Series) -> pd.Series:
    s = ic.dropna()
    std = s.std()
    return pd.Series({'ic_mean':s.mean(),'ic_std':std,'icir': (s.mean()/std if std and std>0 else 0.0),'win_rate':(s>0).mean()})
