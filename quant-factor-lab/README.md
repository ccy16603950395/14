# quant-factor-lab

> 仅用于学习和研究，不构成投资建议。历史回测不代表未来收益。

## 1. 项目简介
本项目是 A 股多因子研究与回测系统（本地版）。流程覆盖：数据下载、清洗、因子构建、标准化、IC 检验、分组收益、多因子合成、简单回测与报告生成。

## 2. 功能列表
- AKShare 下载沪深300成分股（前30只）日线
- 本地缓存（优先 parquet，失败降级 csv）
- 5 个基础因子
- 横截面 winsorize + z-score
- IC / Rank IC / ICIR / 胜率
- 五分组收益 + 多空收益
- 月度调仓 top5 等权回测（含交易成本）
- 报告与图表输出
- PTrade/QMT 预留接口（不接实盘）

## 3. 项目结构
见目录树（src 按 data/factors/analysis/backtest/adapters 分层）。

## 4. 安装方法
```bash
pip install -r requirements.txt
```

## 5. 运行方法
```bash
pytest -q
```

## 6. 运行 Notebook
```bash
jupyter notebook notebooks/01_factor_research_demo.ipynb
```

## 7. 运行测试
```bash
pytest -q
```

## 8. 因子定义
- momentum_20: `close / close.shift(20) - 1`
- reversal_5: `-(close / close.shift(5) - 1)`
- volatility_20: `-returns.rolling(20).std()`
- price_volume_divergence_20: `-corr(价格变化率, 成交量变化率)`
- turnover_20: `-turnover.rolling(20).mean()`

若 AKShare 缺少换手率字段，降级为成交量近似（局限：不能精准反映流通盘换手）。

## 9. 因子检验指标
IC、Rank IC、ICIR、分组收益、多空收益。

## 10. 回测逻辑
按月末调仓，选择综合分数最高 5 只，等权持仓，逐日计算净值。

## 11. 交易成本
买入手续费0.0003，卖出手续费0.0003，卖出印花税0.0005，滑点0.0005。

## 12. 已知局限
- 免费数据源稳定性有限
- 可能存在幸存者偏差
- 暂未做行业/市值中性化
- 停复牌处理为简化版
- 历史回测不代表未来收益

## 13. 扩展方向
接入 Backtrader、Alphalens、QMT、PTrade；加入行业中性化、多因子权重优化、风控模块。

## 14. 实盘说明
当前版本只做研究和回测，不做实盘交易。
