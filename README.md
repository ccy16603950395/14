# saline-composite-simulation

砼岩组合体在咸水环境下性能演化模拟（MVP）。该项目实现二维简化模型，模拟咸水侵入、扩散、材料退化、界面弱化和损伤演化过程。

## 1. 项目简介
本项目面向科研原型开发，强调可维护结构、可运行结果和后续扩展能力。

## 2. 项目解决的问题
- 咸水浓度场在组合体中的时空扩散。
- 三类材料（concrete / interface / rock）差异化退化。
- 弹性模量与强度随损伤衰减。

## 3. 核心模型逻辑
- 扩散方程：`∂C/∂t = D∇²C`（显式有限差分）。
- 左边界固定浓度 `C=C0`，其余边界零通量。
- 退化：`Deg = 1 - exp(-k_region * C * t)`。
- 损伤：`Damage = clip(Deg, 0, 1)`。
- 模量：`E = E0 * (1 - alpha * Damage)`。
- 强度：`strength = strength0 * (1 - beta * Damage)`。

## 4. 项目结构
见 `src/`, `examples/`, `tests/`, `docs/`, `outputs/`, `data/`。

## 5. 安装方式
```bash
pip install -r requirements.txt
pip install -e .
```

## 6. 运行方式
```bash
python examples/run_basic_simulation.py
# 或
python -m saline_composite
```

## 7. 输出结果说明
运行后在 `outputs/` 下至少生成：
- `concentration_final.png`
- `degradation_final.png`
- `damage_final.png`
- `elastic_modulus_final.png`
- `average_curves.png`

## 8. API 文档位置
API 文档位于 `docs/api/` 目录。

## 9. 当前模型假设
详见 `docs/model_assumptions.md`。

## 10. 局限性
- 当前为二维简化模型。
- 退化方程为经验形式，未含反应动力学。
- 未耦合显式力学平衡方程。

## 11. 后续扩展方向
- 渗流–损伤–力学耦合。
- 参数反演与不确定性分析。
- 更复杂边界与非均质结构。


## 12. Multi-Agent Collaboration

| Agent | 职责 | 输入 | 输出 | 协作关系 |
|---|---|---|---|---|
| Problem Definition Agent | 定义问题边界与验收标准 | 用户需求、约束 | MVP 范围与验收项 | 驱动机理与模型设计 |
| Mechanism Agent | 提炼机理与数学规则 | 问题定义、材料信息 | 扩散/退化/损伤规则 | 约束模型设计与验证预期 |
| Model Design Agent | 设计模块与接口契约 | 机理规则、MVP目标 | 模块结构和数据契约 | 指导代码实现与文档结构 |
| Code Implementation Agent | 实现代码与示例 | 设计文档、规则 | 可运行代码与测试脚手架 | 交付给验证 Agent |
| Validation Agent | 检查功能、边界、数值范围与输出 | 代码、机理预期 | 验证报告与缺陷反馈 | 反馈实现并供文档汇总 |
| Documentation Agent | 输出统一文档与阶段报告 | 全部 Agent 产物 | README/API/流程与报告 | 支撑人工评审与下轮迭代 |

详见：`agents/` 与 `docs/multi_agent_workflow.md`。
