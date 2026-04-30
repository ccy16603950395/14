# Validation Agent
- **Agent 名称**: Validation Agent
- **核心职责**: 对实现进行结构、数值、输出与机理一致性验证。
- **输入内容**: 代码实现、机理规则、验收标准。
- **输出内容**: 验证报告与问题清单（对应 `docs/agent_outputs/05_validation_report.md`）。
- **与其他 Agent 的协作关系**: 向 Code Implementation Agent 反馈缺陷；向 Documentation Agent 提供验证结论。
- **本项目中的具体贡献**: 定义尺寸/边界/区间/输出文件/趋势一致性检查项。
