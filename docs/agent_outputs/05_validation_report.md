# 05 Validation Report (Validation Agent)

## Validation Checklist
1. **网格尺寸是否正确**
   - 检查 `material_map.shape == (ny, nx)`。
2. **材料分区是否合理**
   - 检查 `concrete/interface/rock` 三类区域均存在。
3. **边界条件是否正确**
   - 左边界恒等于 `C0`；右边界与相邻列一致；上下边界满足零通量近似。
4. **退化因子是否在 0 到 1**
   - 检查 `min(deg) >= 0 and max(deg) <= 1`。
5. **输出图像是否成功生成**
   - 检查应生成 `concentration/degradation/damage/elastic_modulus/average_curves` 五张图。
6. **模拟结果是否符合机理预期**
   - 浓度从左向右呈扩散趋势；界面区退化相对更快；损伤升高导致平均模量/强度下降。

## Evidence Source
- 测试脚本：`tests/test_grid.py`, `tests/test_transport.py`, `tests/test_degradation.py`, `tests/test_materials.py`。
- 运行入口：`examples/run_basic_simulation.py`。
