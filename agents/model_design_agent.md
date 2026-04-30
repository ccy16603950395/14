# Model Design Agent
- **Agent 名称**: Model Design Agent
- **核心职责**: 设计模块边界、数据结构与主流程接口。
- **输入内容**: 问题定义输出、机理规则输出。
- **输出内容**: 模块分解与接口契约（对应 `docs/agent_outputs/03_model_design.md`）。
- **与其他 Agent 的协作关系**: 向 Code Implementation Agent 提供文件结构和函数签名；向 Documentation Agent 提供说明骨架。
- **本项目中的具体贡献**: 设计 `config/grid/materials/transport/degradation/simulation/visualization` 分层。
