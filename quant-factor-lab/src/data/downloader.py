from __future__ import annotations
import pandas as pd
import akshare as ak


def get_hs300_symbols(top_n: int = 30) -> list[str]:
    df = ak.index_stock_cons(symbol='000300')
    col = '品种代码' if '品种代码' in df.columns else df.columns[0]
    symbols = df[col].astype(str).str.zfill(6).tolist()
    return symbols[:top_n]


def fetch_daily_ohlcv(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    raw = ak.stock_zh_a_hist(symbol=symbol, period='daily', start_date=start_date.replace('-', ''), end_date=end_date.replace('-', ''), adjust='qfq')
    mapper = {'日期':'date','开盘':'open','收盘':'close','最高':'high','最低':'low','成交量':'volume','成交额':'amount','换手率':'turnover'}
    df = raw.rename(columns={k:v for k,v in mapper.items() if k in raw.columns})
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    df['symbol'] = symbol
    return df


def fetch_panel(symbols: list[str], start_date: str, end_date: str) -> dict[str, pd.DataFrame]:
    return {s: fetch_daily_ohlcv(s, start_date, end_date) for s in symbols}
