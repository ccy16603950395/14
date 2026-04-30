# Code Implementation Agent
- **Agent 名称**: Code Implementation Agent
- **核心职责**: 按设计实现可运行代码与示例脚本。
- **输入内容**: 模型设计文档、机理规则、代码规范。
- **输出内容**: Python 包、示例、测试脚手架（对应 `docs/agent_outputs/04_code_plan.md`）。
- **与其他 Agent 的协作关系**: 接收 Model Design Agent 的接口；向 Validation Agent 提供待测实现。
- **本项目中的具体贡献**: 实现显式扩散步进、材料映射、退化场与绘图输出流程。
