# Degradation API
## 模块功能
按区域计算退化、损伤及力学参数衰减场。
## 主要函数或类
- `compute_degradation(...)`
- `compute_damage(degradation)`
- `compute_elastic_modulus_field(...)`
- `compute_strength_field(...)`
## 输入参数
- 浓度场、时间、材料图、材料参数。
## 返回值
- 退化场、损伤场、弹性模量场、强度场。
## 简单示例
```python
deg = compute_degradation(C, material_map, mats, time=10.0)
```
## 后续扩展说明
可加入疲劳损伤和路径依赖退化模型。
