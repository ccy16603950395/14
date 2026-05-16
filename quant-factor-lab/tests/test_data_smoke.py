import pytest

pytest.importorskip('akshare')
from src.data.downloader import get_hs300_symbols, fetch_panel
from src.data.cache import save_df, load_df
from src.data.cleaner import clean_ohlcv


def test_data_smoke_download_cache_clean(tmp_path):
    try:
        symbols = get_hs300_symbols(top_n=3)
        panel = fetch_panel(symbols, '2022-01-01', '2022-03-31')
    except Exception as exc:
        pytest.skip(f'akshare/network unavailable: {exc}')
    assert len(panel) == 3
    for sym, df in panel.items():
        cleaned = clean_ohlcv(df)
        assert 'return' in cleaned.columns
        save_df(cleaned, tmp_path, sym)
        loaded = load_df(tmp_path, sym)
        assert loaded is not None and len(loaded) > 0
