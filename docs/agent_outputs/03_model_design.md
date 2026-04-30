# 03 Model Design Output

## Module Design
- `config.py`: 参数集中管理。
- `grid.py`: 网格与材料映射。
- `materials.py`: 材料参数结构。
- `transport.py`: 扩散与边界、稳定性检查。
- `degradation.py`: 退化/损伤/参数衰减。
- `simulation.py`: 主流程类。
- `visualization.py`: 图像输出。

## Data Contracts
- `material_map`: shape `(ny, nx)` 的字符串数组，取值为 `concrete/interface/rock`。
- 所有场变量统一为 `numpy.ndarray` 且 shape 为 `(ny, nx)`。
