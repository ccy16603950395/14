# Grid API
## 模块功能
生成二维网格和三相材料分区。
## 主要函数或类
- `create_grid(config)`
- `create_material_map(config)`
## 输入参数
- `SimulationConfig`
## 返回值
- `X, Y` 网格坐标；`material_map`（`(ny, nx)` 字符串数组）。
## 简单示例
```python
material_map = create_material_map(config)
```
## 后续扩展说明
可加入非规则界面和随机缺陷分布。
