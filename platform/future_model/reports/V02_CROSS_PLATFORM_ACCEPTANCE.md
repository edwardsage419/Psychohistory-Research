# Psychohistory Platform v0.2 跨平台定版验收

2026-11-18 UTC。**工程定版候选 COMPLETE**。保持 [PR #53](https://github.com/edwardsage419/Psychohistory-Research/pull/53) 为 Draft，等待项目所有者批准。原生 macOS 和 Linux 验收的代码提交均为 `50bdd07d9b776b5ca052efc6943cec0bc5ed6aa7`。报告归档提交的身份以 PR 的 GitHub 回读为准。

开工和验收时 GitHub `main` 均为 `7ea6eab94433e3669b6f492d802bb35316dc90d6`。PR #53 的起点为 `c6f69bf578ca5d2ba1f507734bd75649913231ef`。开放的 #44–#52 与此前记录的远端头一致，均无平台路径重叠。对 main 的变更范围仅含平台及一份验收工作流。R073、PESEN v0.1、既有冻结协议及其他研究工作流保留原始 Git 字节。新增科研证据为零，真实预测与因果识别保持原有状态。 [开放 PR 和远端收据](v02/cross_platform/GITHUB_RUNS.json)

## 验收矩阵

| 交付 | 状态 | 实际结果 |
| --- | --- | --- |
| GitHub 身份及范围 | COMPLETE | 回读 main、PR #53、其余开放 PR 及 Actions 作业。核对正式科研路径差异。 |
| macOS ARM64 原生安装与构建 | COMPLETE | 标准 `macos-15` 从固定 SHA 全新检出，Python、Node 及浏览器依赖锁安装成功。pip 检查、完整 pytest 命令、严格 TypeScript、Vite、标准库核心和 SQLite 均实际执行。 |
| Linux 修复回归 | COMPLETE | 安装、完整 pytest、严格 TypeScript/Vite 和标准库核心通过。重跑修复所涉及的调度、存储和 CLI/Web 流程。 |
| R123 精确实算及跨平台一致性 | COMPLETE | 32 次更新的 33 个状态与独立解析解逐值吻合。共识极限为 2/3；保存和恢复、隔离分支及非法权重、时间、参数和状态版本拒绝通过。 |
| 冻结合成预测 | COMPLETE | 两个平台重新选择候选步数、进行留出评价和独立重算。相同代码与种子的科学内容及浏览器 worker 工件相同。 |
| API、CLI 和 Chromium | COMPLETE | 两个平台真实环回服务上完成 v0.2 中文操作流及 v0.1 九步浏览器流程。CLI 正常和优化执行、来源准入、取消后受控重试、历史数据读取通过。 |
| v0.1 和 v0.2 备份恢复 | COMPLETE | 在两平台以原始 v0.1 代码生成备份，用 v0.2 恢复。旧产物内容和原始哈希在各自恢复前后保持一致。v0.2 备份恢复保留工件和留出使用记录。 |
| 负向验证与独立审查 | COMPLETE | 非法路径、链接、来源/代码替换、时间和场次隔离、失败或取消无成功工件、优化模式显式校验均通过。独立审查发现两处存储缺陷，两项均复现、修复和复核。 |
| macOS 硬资源控制 | PARTIAL | 墙钟预算及正常取消已测试。CPU、内存和调度器被强杀时的父进程死亡联动均在真实 worker 收据中标记 `NOT_ENFORCED`。Linux 专用父进程死亡测试在 macOS 为 `NOT_RUN`。 |
| 真实数据、外部科研复现 | NOT_RUN | 工程验收仅处理固定理论来源和公开合成数据，实证预测效力保留 `UNKNOWN`。 |

## 运行身份及退出状态

| 环境 | 实测配置 | 测试结果 |
| --- | --- | --- |
| macOS ARM64 | macOS 15.8.2 (24H232)，Apple M1 虚拟机，3 CPU，7 GiB 内存，45 GiB 可用磁盘。Python 3.12.10 / SQLite 3.49.1，Node 24.22.2 / npm 11.19.1，Git 2.56.0，Chromium 151.0.7922.34 | 96 passed，1 skipped，11 subtests passed，1 条 Starlette/httpx 弃用警告。锁依赖安装及完整验证命令退出 0。工作流成功。 |
| Linux x86_64 | Debian 13，内核 6.18.57。Python 3.12.14 / SQLite 3.53.1，Node 24.22.1 / npm 11.9.0，Git 2.52.0，Chromium 156.0.8078.79 | 97 passed，11 subtests passed，同一条弃用警告。锁依赖安装及完整验证命令退出 0。 |

- 首轮 macOS 于代码 `1ad1d664df333edd99c250b15ef6032b986828ad` 上成功。存储故障注入来自后续独立审查，首轮套件尚未包含这两项。该轮 GitHub 日志及工件下载经云端代理返回 HTTP 403，作业步骤和工件摘要可通过 GitHub API 回读。 [首轮 Run 44226714331](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44226714331)
- 修复后原生 Run 44227348341，作业 134543661488，attempt 1，实际 UTC 运行时间为 03:00:49–03:03:28。GitHub Checks 的文本收据已回读，解包后 SHA-256 为 `11560ccdbb7d11ff36fde30189e52ba79fc469d5d85c8afde02ef45164d9a6dd`。GitHub 托管工件 14394040525 含浏览器截图，工件摘要和保留期限见远端收据。 [最终原生 Run 44227348341](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44227348341) · [逐步远端收据](v02/cross_platform/GITHUB_RUNS.json)
- 两个平台普通 Python、`python -O` 和 `PYTHONOPTIMIZE=1` 检查均退出 0，优化标志分别为 0、1、1。每次实际拒绝越过截止时间的特征与变更到实证范围的协议。普通和优化 CLI 各执行 19 条命令，其中 18 条退出 0，未批准协议提交按预期退出 1。两平台四次 seed 829 工件哈希均为 `106a34318f686facb552fb61e4b480118b33c4d83570cd700eff4d1b9f335316`。 [完整命令和日志](v02/cross_platform/verification-evidence.zip)

## 数学、评分与工件

`r123-degroot@1.0.0` 使用原先固定的权重矩阵。独立检查以加权均值和间距 `(x₀ − x₁) / 4ⁿ` 复算 32 轮。第 32 轮的规范精确值为 `6148914691236517205/9223372036854775808`、`12297829382473034411/18446744073709551616`。两平台相同。两种权重情景各自绑定共享起点，恢复后状态继续产生相同的轨迹。数学核心及预测源码的 SHA-256 与原 Linux 验收一致，依赖清单身份见两平台的 `platform.txt`。 [完整轨迹、独立评分与来源](v02/cross_platform/PARITY.json) · [锁定依赖与工具版本](v02/cross_platform/verification-evidence.zip)

冻结协议 `synthetic-degroot-comparison-1.0.0` 在 seed 207 生成 40 个不重叠场次，训练 96 行、验证 48 行、测试 96 行。截止轮次为 19。独立计算只用训练标签拟合两组基线，只用验证分区选择第 1 步。留出评估在后续执行。重算了各研究的两种评分及三种预注册权重。故障注入验证结果保存失败后仍保留留出预留状态，恢复和重试未开启同一留出。 [科学结果和校验](v02/cross_platform/PARITY.json)

| 合成权重 | DeGroot Brier / Log Loss | 训练基线 Brier / Log Loss |
| --- | --- | --- |
| 1:1 | 0.277057 / 0.764945 | 0.236762 / 0.666505 |
| 4:1 信号一致组优先 | 0.234729 / 0.664364 | 0.241319 / 0.675716 |
| 1:4 弱反向信号组优先 | 0.319385 / 0.865525 | 0.232205 / 0.657294 |

两平台规范化科学内容的 SHA-256 均为 `2d57bde43e7b34d34d07a15484b67e31bc487c8dd69317ebd4b5bd27a11a684c`，观察到的浮点差异为零。两端通过真实浏览器触发的隔离 worker 产物 SHA-256 均为 `712c8ad4ccd1d61ee42be92e0e40704685583fc4d6ed01d2677fad60bfc8d566`。验收核对浏览器显示值、API 读取、实际 worker 产物和调度器终态哈希。原 Linux 归档的完整工件哈希不同，变化位于代码身份、绑定该身份的协议 ID 和输入信封，冻结协议内容、数据哈希和科学结果一致。 [工件字节身份和差异字段](v02/cross_platform/PARITY.json)

## 恢复、安全及修复

- 两平台从 main `7ea6eab9…` 提取 v0.1 原始源码，生成 seed 123 实验并在新根恢复。各自的六条 Git/CLI 命令均退出 0。macOS 恢复前后工件为 `4a006aab61367e1c6aea6dd4408e4316041c1c13ce59ea1e511e6cd67c1ed08b`，Linux 为 `2310400d7dd7f3de6df17df8a09392bb80253e3de008d59584953a473d286f8e`。用同一 v0.1 源码只改变记录的 Python 补丁版本即可复现两种哈希，历史 v0.1 快照将该版本写入其内容身份。 [恢复记录](v02/cross_platform/verification-evidence.zip) · [哈希来源诊断](v02/cross_platform/PARITY.json)
- v0.2 中文浏览器实测覆盖 R123 登记和检查、协议批准、取消、重试、执行、比较、按 ID 读取工件以及 #44 候选只读和拒绝执行。两平台 v0.1 九步流程与 v0.2 流程均无页面错误。macOS 完成实验 ID 为 `cb5b69fb6bcc4c82ab548be3fbc93a04`。FastAPI 套件另覆盖故障处理及旧接口边界。 [浏览器、CLI 和 API 结果](v02/cross_platform/verification-evidence.zip)
- 修复前，对原 v0.2 源码 `98798a09…` 执行两项新回归以退出 1 结束。注入写入同步失败时，最终内容地址文件提前可见。另一条回归在 SQLite 备份之后并行提交来源登记，恢复出的审计日志含有数据库中不存在的登记。修复以私有暂存完成数据写入和同步，再无覆盖地发布硬链接。备份与带审计的来源登记使用同一个文件锁，防止二者读取不同快照。 [修复前失败输出](v02/cross_platform/FAILURE_REPRODUCTION.txt) · [修复提交](https://github.com/edwardsage419/Psychohistory-Research/commit/50bdd07d9b776b5ca052efc6943cec0bc5ed6aa7)
- 独立复核关注规范路径、链接拒绝、对象原子可见性、跨实例文件锁、SQLite 备份、进程终止和 worker 科学身份。最终对修复提交的 13 项存储与研究流程测试通过，另用真实 Linux worker 核查工件绑定。完整套件随后在 macOS 与 Linux 通过。审查未发现剩余定版阻塞。突然断电的目录项持久性和 macOS 调度器遭强杀后的 worker 回收分别为 `NOT_RUN`，后者当前没有父进程死亡联动。 [最终测试输出](v02/cross_platform/verification-evidence.zip)

## 复现及费用

检出 `50bdd07d9b776b5ca052efc6943cec0bc5ed6aa7`，取得 `origin/main` 和 PR #44 的固定来源提交，从 `platform/future_model` 按版本化工作流运行 `bash scripts/install.sh`、`bash scripts/verify.sh`、普通及优化科学检查、CLI 和备份测试。原生 macOS 使用 `pwd -P` 规范化临时目录，Chromium 使用 Playwright 锁定引导程序。Linux 端使用系统 Chromium。端到端命令、环境变量和预期退出码在验收工作流及归档内，旧版源代码从固定 Git 对象读取。归档 SHA-256 为 `ef8efcb141711e31d4c9ffe1782b7be6351390034f8daed70d6830792d690c01`。 [验收工作流](../../../.github/workflows/psychohistory-platform-v02-macos.yml) · [测试收据归档](v02/cross_platform/verification-evidence.zip)

仓库公开，GitHub 文档确认所用标准 `macos-15` ARM64 运行器免费。工作流令牌仅有 `contents: read`，检出后移除持久凭据。仅 PR #53 的分支同步执行测试，原 PR #40 作业在两次同步均跳过。服务仅监听本机环回。使用现有 Codex Cloud 及免费依赖和标准托管运行器，新增费用为零。 [GitHub 标准运行器及费用](https://github.com/github/docs/blob/main/data/reusables/actions/supported-github-runners.md) · [GitHub Actions 计费说明](https://github.com/github/docs/blob/main/content/billing/concepts/product-billing/github-actions.md)

v0.3 建议优先补齐 macOS 的进程组回收和可验证的 CPU 限额，再扩展备份审计事务一致性与断电持久性验证。本轮交付为待所有者批准的 v0.2 工程候选。合成结果维持其工程及理论适用范围。
