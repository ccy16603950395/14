# 02 Mechanism Rules Output

## Core Rules
1. 扩散：`∂C/∂t = D∇²C`。
2. 边界：左边界 `C=C0`；其余边界零通量近似。
3. 退化：`Deg = 1 - exp(-k_region * C * t)`。
4. 损伤：`Damage = clip(Deg, 0, 1)`。
5. 参数退化：
   - `E = E0 * (1 - alpha * Damage)`
   - `strength = strength0 * (1 - beta * Damage)`

## Region Behavior
- `interface` 的 `degradation_rate` 高于 `concrete` 与 `rock`。
