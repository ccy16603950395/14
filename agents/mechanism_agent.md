# Mechanism Agent
- **Agent 名称**: Mechanism Agent
- **核心职责**: 将工程机理转化为可编码规则（扩散、退化、损伤、参数衰减）。
- **输入内容**: 问题定义、材料类别、边界条件要求。
- **输出内容**: 机理规则与数学表达（对应 `docs/agent_outputs/02_mechanism_rules.md`）。
- **与其他 Agent 的协作关系**: 向 Model Design Agent 提供方程与变量定义；向 Validation Agent 提供预期行为。
- **本项目中的具体贡献**: 确定左边界定值浓度、其余零通量、`Deg=1-exp(-kCt)` 与 damage/E/strength 关系。
