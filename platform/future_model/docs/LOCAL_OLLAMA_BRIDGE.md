# 本地 Qwen3.5 与 v0.5 数学库的候选连接层

状态：工程候选，待独立验收；不合并、不部署、不改变冻结科研协议。

## 目的及边界

将已在用户 Mac 运行的 Ollama 模型 qwen3.5:4b-q4_K_M 与已有 DecisionHubV05 方法库连接，优先解决自然语言提出问题后自动选用科学方法的入口。保留 v0.5 计算引擎、接口、独立记录、方法版本和历史验收。

1. Qwen 只提出初步分析、一个关键追问、用户原话中的待确认方案及精确注册方法。模型输出必须符合 JSON 契约和注册白名单。没有数值计算时 calculated=false。
2. 用户必须对结构化决策状态明确确认，只有满足确认门槛的输入才可走 DecisionHubV05.analyze()。方法返回 EXECUTED、INELIGIBLE、UNKNOWN，不能由 Qwen 自行声称执行成功。
3. 本候选不向模型自动传个人历史、私有文件、访问令牌或决策数据库；不自动保存聊天，不将私人内容写入公开训练集。方法目录为公开登记元数据。
4. 网络端点固定为 127.0.0.1:11434，禁止代理和重定向，不允许自定义远程地址或 Ollama 云端模型。模型名单仅包括已预先安装的本地 qwen3.5:4b-q4_K_M 与 psychohistory:v0。
5. 保持现有 Bearer 身份验证、同源检查、输入限制和私有记录权限。进程内排他锁避免 Mac 在同一时刻重复推理。默认关闭，需要用户显式启用。

## Mac 上测试

前提：Ollama 本地模型已经下载；项目工程的 Python 3.12、Node 24、前端构建和依赖已经按原有 v0.5 安装完毕。

在 Mac 上的现有工程目录运行：

~~~bash
ollama list
cd platform/future_model
PSYCHOHISTORY_LOCAL_AI=1 bash scripts/run.sh --data "$HOME/psychohistory-data" serve --port 8765
~~~

在 http://127.0.0.1:8765 使用已有本地访问令牌连接平台，侧边栏选择「本地智能助手」。确认已有 Qwen 模型和 Ollama 运行。缺少环境变量时，页面将提示本地模型未启用，保留原有确定性工作台。

### API

* GET /api/v5/decisions/local-ai/status 返回本地启用状态；不产生推理请求。
* POST /api/v5/decisions/local-ai/propose 发送 JSON 对象 question，返回暂存的候选 model_key、初步分析和关键追问，不会运行数学模型。
* POST /api/v5/decisions/local-ai/analyze 接收完整已确认 v0.5 决策状态、model_key 和 confirmed_by_user=true。v0.5 重新核验输入并执行登记方法。缺少必要事实继续保留 CLARIFY、INELIGIBLE、UNKNOWN。模型输出不得直接作为已确认状态。

## 工程验证

pytest tests/test_decision_local_ai.py 包含默认关闭、越权模型 ID、重复 JSON 键、用户原文未出现的方案、长输入、明确确认、旧 C028 区间硬约束合成算例。Ollama 在单元测试中被模拟，避免把假响应当成真实的 Qwen 表现。

用户此前报告的 28 道合成工程题中，原始 Qwen3.5 方法匹配 27/28 且 28/28 JSON 有效，这是前一版测试工具的结果。本连接层需要重新开展实际 Mac 测试以及全新独立留出案例，再考虑推广。

## 训练策略

现阶段暂停重复进行无明显收益的 QLoRA。新的样例先从模型选择错误、无来源概率、结构化解析失败、追问错误和人类确认问题收集，逐项审核；对模型提示与确定性基线先做 A/B，再选择是否微调。历史第一轮失败适配器不能自动上架。任何发布都要求独立留出、正反例、跨平台回归和所有者许可。

目前网页只具备一轮自然语言候选和跳转既有数学工作台的入口，尚不支持自动确认完整决策状态、长期记忆、语音和自动更新模型权重；不得描述为完全自主决策系统。
