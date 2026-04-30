# Simulation API
## 模块功能
封装主流程：初始化、时间推进、指标记录和结果保存。
## 主要函数或类
- `SalineCompositeSimulation`
- `initialize / step / run / save_results / get_summary_metrics`
## 输入参数
- `SimulationConfig` 与可选 `materials`。
## 返回值
- 最终场变量与历史曲线可从对象属性读取。
## 简单示例
```python
sim = SalineCompositeSimulation(SimulationConfig())
sim.run()
print(sim.get_summary_metrics())
```
## 后续扩展说明
可扩展耦合求解器、断点续算和参数扫描。
