from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def generate_report(ic: pd.Series, quantile_means: pd.Series, long_short: pd.Series, out_dir: str='reports') -> None:
    fig_dir = Path(out_dir)/'figures'; fig_dir.mkdir(parents=True, exist_ok=True)
    ic.plot(title='IC Time Series'); plt.tight_layout(); plt.savefig(fig_dir/'ic_timeseries.png'); plt.close()
    ic.hist(bins=20); plt.title('IC Distribution'); plt.tight_layout(); plt.savefig(fig_dir/'ic_distribution.png'); plt.close()
    quantile_means.plot(kind='bar', title='Quantile Mean Returns'); plt.tight_layout(); plt.savefig(fig_dir/'quantile_bar.png'); plt.close()
    long_short.cumsum().plot(title='Long-Short Cumulative'); plt.tight_layout(); plt.savefig(fig_dir/'long_short_curve.png'); plt.close()
    Path(out_dir,'factor_report.md').write_text('# Factor Report

历史回测不代表未来收益。
', encoding='utf-8')
