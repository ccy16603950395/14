import pandas as pd

def equal_weight_composite(factors: dict[str, pd.DataFrame]) -> pd.DataFrame:
    stack = pd.concat(factors.values(), keys=factors.keys(), names=['factor','date'])
    score = stack.groupby(level='date').mean(numeric_only=True)
    score.index.name = 'date'
    return score
