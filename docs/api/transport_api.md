# Transport API
## 模块功能
执行浓度初始化、边界施加、显式扩散步进和稳定性检查。
## 主要函数或类
- `initialize_concentration(config)`
- `apply_boundary_conditions(C, config)`
- `check_stability(config, materials)`
- `compute_diffusion_step(C, material_map, materials, config)`
## 输入参数
- 浓度场、材料映射、材料参数、配置对象。
## 返回值
- 新浓度场（与输入同尺寸）。
## 简单示例
```python
check_stability(config, mats)
C = compute_diffusion_step(C, material_map, mats, config)
```
## 后续扩展说明
可扩展到对流-扩散、非线性扩散和隐式格式。
