import pandas as pd


def quantile_return_table(factor: pd.DataFrame, fwd: pd.DataFrame, q: int = 5) -> tuple[pd.DataFrame, pd.Series]:
    records=[]; ls=[]
    for d in factor.index.intersection(fwd.index):
        df = pd.concat([factor.loc[d], fwd.loc[d]], axis=1).dropna()
        if len(df) < q:
            continue
        df.columns=['factor','ret']
        df['q']=pd.qcut(df['factor'], q=q, labels=False, duplicates='drop')+1
        m = df.groupby('q')['ret'].mean()
        row = {f'Q{k}': m.get(k, float('nan')) for k in range(1,q+1)}
        records.append(pd.Series(row, name=d))
        ls.append((d, row[f'Q{q}']-row['Q1']))
    table = pd.DataFrame(records)
    ls_series = pd.Series(dict(ls)).sort_index()
    return table, ls_series
