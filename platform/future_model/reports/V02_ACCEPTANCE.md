# Psychohistory Platform v0.2 验收

本轮从 GitHub main `7ea6eab94433e3669b6f492d802bb35316dc90d6` 开始。在改动前回读了指定规范、最新 R 系列队列及冻结记录。GitHub 文件清单显示，审查中的 #44–#52 均与平台目录无重叠。#44 的 R132 Phase A 加固与 #51 的 R272 修复仍是候选。浏览器用 #44 的显式提交验证了候选来源的只读准入。历史 GitHub 数据与开放 PR 头见 [范围记录](v02/OPEN_PR_SCOPE.json)。

R123 既有原始来源和审计已进入 main。平台选择 DeGroot 固定行随机矩阵的离散更新，沿用矩阵、初始条件和时间步的定义。R132 与 R233 独立登记，分别验证双阶段收据和 CSV/结果联合身份。v0.2 新增的预测任务只读取内置生成器的合成场次。R123 的理论意见更新与对合成 Bernoulli 事件的评分属于不同层，真实预测和因果证据为 UNKNOWN。具体推导与误差口径见 [数学说明](../docs/MATHEMATICS_V02.md)。

| 验收项 | 状态 | 实际结果 |
| --- | --- | --- |
| 1. v0.2 实现与旧能力 | COMPLETE | 维持 v1 接口和原有两套内置插件，另加 v2 中文工作区、API 和 CLI。v1 完整 54 项基线测试包含在最终 95 项中。 |
| 2. R 系列数学机制 | COMPLETE | R123 DeGroot 1.0.0 在隔离 worker 实际运行。独立解析式核对 32 轮，重现文献例子的权重 1/3、2/3 和极限 2/3。边界、周期、凸包、不兼容状态测试通过。 |
| 3. 合成完整比较 | COMPLETE | 两组独立生成机制、40 场次、240 行，按场次隔离训练、验证和留出。先用训练拟合基线、验证选步长，再计算留出 Brier 和 Log Loss。分别呈现两组表现和预先定义的权重敏感性。 |
| 4. 来源和证据 | COMPLETE | R123、R132、R233 已通过真实登记与复查。固定 Git 提交、路径、blob、SHA256、冻结引用、证据原义、执行边界。重复、候选漂移和失败判定可审计。 |
| 5. 用户交互 | COMPLETE（Linux） | FastAPI 集成、实际 CLI、真实 Chromium v0.2 工作流。完成来源检查、协议审批、取消、重试、执行批准、比较和按 ID 复核。v0.1 浏览器主流程与 203 项历史回归也通过。 |
| 6. 完整性与拒绝 | COMPLETE（当前信任边界） | 来源漂移、符号链接、哈希错配、候选执行、留出泄漏、时间/单位不兼容、UNKNOWN 和证据越权均有负向测试。调度器持久化留出集使用，结果保存失败后也不会重用。隔离进程编译已校验源码，胜任本地受信任平台代码执行。 |
| 7. v0.1 恢复 | COMPLETE（Linux） | 用基线实际 v0.1 CLI 生成并备份结果。v0.2 恢复到新根，读取逐字段相同的旧结果和原工件哈希。v0.2 自身备份恢复保留协议、结果与留出集使用记录。 |
| 8. 验收与独立审查 | COMPLETE（Linux） | 全新 GitHub 检出、锁定依赖安装、95 项 pytest + 11 子测试、严格 TypeScript/Vite。独立审查发现的留出集重用、跨版本读取、缺字段完成标记与来源记录键不一致均已补测试和修复。[独立审查与复核](v02/INDEPENDENT_REVIEW.md)。 |
| 9. 提交与审查 | COMPLETE | 测试源代码提交 `98798a098ea23f97164a519ee9bab24be47910c4`。验证期间 fresh clone 确认此 SHA。最终交付头含后续独立审查和证据文档，以 Draft PR 当前头为准。 |
| 10. 局限与后续 | PARTIAL | 仅三个人工策划来源和一份可执行协议。macOS v0.2 为 NOT_RUN，历史 v0.1 macOS 实测另有记录。未来扩展到新的机制和审定数据时，优先补充目标含义与可用性审计，以及跨平台原生测试。 |

## 可以核验的结果

- 全新远端检出在 Debian 13 x86_64 运行，Python 3.12.14、SQLite 3.53.1、Node v24.22.1、Chromium 156.0.8078.79。pytest 报告 1 条已有 Starlette/httpx 弃用警告。
- 普通 Python、`python -O`、`PYTHONOPTIMIZE=1` 均通过标准库数学与显式拒绝检查。新数据根上普通和优化 CLI 运行 seed 829，比较产物 SHA256 同为 `c0d83967b445f68b790e14bae9e1f60014003d8d98bdaec3be7452671e548b08`。
- seed 7 等权 Brier 为 DeGroot 0.281458、基线 0.250000。Log Loss 为 0.769378、0.693147。对信号一致研究采用预定义 4:1 权重后，DeGroot 的 Brier 0.245990 与 Log Loss 0.686155 均低于基线。排序依赖目标总体的权重选择。
- 浏览器 seed 207 的完整合成产物为 [browser-synthetic-result.json](v02/browser-synthetic-result.json)，SHA256 为 `93f2601af124987e394ef11c7673ba3358897d565b2ebf81d23ef6534267ce37`。查看 [截图](v02/browser-v02.png) 和 [浏览器回执](v02/browser-v02.json)。
- 每条验证命令、环境选项、退出码、输出哈希与测试版本见 [execution.json](v02/execution.json)。两次环回服务的 `-15` 是验证工具主动以 SIGTERM 关闭进程。CLI 及恢复内部的命令与预期拒绝另在 [CLI 记录](v02/cli.json)、[优化 CLI 记录](v02/cli-optimize.json) 和 [旧版备份记录](v02/old-backup.json)。
- 原始输出与开发中失败回归见 [command-logs.zip](v02/command-logs.zip)。首次 API 测试观察到 v2 端点缺失。后续并行改动期间，旧 worker 拒绝了已改变的代码身份，R132 两阶段收据错配控制发现缺失的阶段绑定。稳定后的完整套件通过。留出集、不完整结果与来源记录键控制也保留了修复前失败记录。复查了原 9 个开放 PR，头提交均相同。
- 文件身份见 [SOURCE_SHA256.json](v02/SOURCE_SHA256.json)。可用 `python reports/v02/run-fresh-verification.py <代码提交 SHA> /tmp/新目录` 重跑。工具以独立全量 Git 检出与新 venv 安装，使用免费包源与本地环回服务。已有来源提交和候选引用均从 GitHub 显式获取。

## 适用边界

留出集使用记录约束一个 SQLite 数据根及其继承备份。为工程复现可在两个独立根重建同一个公开合成实验，跨根没有共享锁。现有单工作区模式信任文件系统账户。研究候选、本地审计和理论演算保持原科研状态。真人材料的执行、生产科研流程和科学等级提升为 BLOCKED。v0.2 的原生 macOS 测试为 NOT_RUN。

工程改动均在 `platform/future_model/`。新增科研证据、E2/E3 和正式因果/科学验收增量为零。使用现有云端资源、免费开源依赖及 GitHub 分支/PR。未购买额度，未使用计费 API 或付费基础设施。
