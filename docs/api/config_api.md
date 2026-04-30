# Config API
## 模块功能
管理网格、时间步、边界条件、输出目录等配置参数。
## 主要函数或类
- `SimulationConfig`
## 输入参数
- `nx, ny, dx, dy, dt, total_time, output_interval, C0`
- `concrete_ratio, interface_ratio, output_dir, random_seed, save_figures`
## 返回值
- `n_steps()` 返回总步数。
## 简单示例
```python
from saline_composite.config import SimulationConfig
cfg = SimulationConfig(nx=120, ny=60)
print(cfg.n_steps())
```
## 后续扩展说明
可增加渗透系数、温度场和化学反应参数。
