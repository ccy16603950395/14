# Problem Definition Agent
- **Agent 名称**: Problem Definition Agent
- **核心职责**: 将用户需求转化为可执行问题定义、范围边界和验收标准。
- **输入内容**: 用户原始需求、约束条件、里程碑目标。
- **输出内容**: 问题陈述、MVP 范围、验收清单（对应 `docs/agent_outputs/01_problem_definition.md`）。
- **与其他 Agent 的协作关系**: 为 Mechanism Agent 提供建模语义边界；为 Model Design Agent 提供模块化目标。
- **本项目中的具体贡献**: 明确二维扩散+退化 MVP，限定不引入复杂 FEM/外部平台，定义 outputs 与 tests 的最小验收项。
