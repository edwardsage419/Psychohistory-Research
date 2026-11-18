# Psychohistory Platform v0.3 验收

2026-11-18 UTC。**工程候选 COMPLETE**，以 Draft 供所有者评审。测试代码为 `3a50c48a734194d5ed6bd0910e436007a1c2bc98`，共同基线为 `dd05f32f79efc2f4f4f37117cc039dca1008ed76`。发布范围为合成计算，实证预测等级保持 `UNKNOWN`。 [Draft PR #55](https://github.com/edwardsage419/Psychohistory-Research/pull/55) · [最终 GitHub Actions Run 44257641232](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44257641232)

| 交付 | 状态 | 实测结果 |
| --- | --- | --- |
| R132 独立机制和 R123 轨迹 | COMPLETE | R132 Fraction 核验 Eq.2、Eq.3、Eq.4。连续 Euler、RK4 分别运行，保存规范 Decimal 轨迹和误差。R123 保留精确 DeGroot 轨迹及 v0.2 冻结预测。 |
| 来源、快照与比较 | COMPLETE | 两机制绑定各自来源 blob 和 SHA-256。运行审批、独立历史、父快照恢复通过。拒绝跨机制、不同精确起点、不同观测网格或时间语义和跨机制 Brier。 |
| Linux 与 macOS 完整套件 | COMPLETE | 两个 GitHub runner 从固定 SHA 全新检出，安装锁依赖，运行完整 pytest、严格 TypeScript、生产 Vite、标准库数学检查。 |
| CLI、API 与 Chromium | COMPLETE | 两端真实浏览器执行三个版本的流程。v0.3 实测登记、核验、提交、批准、取消、分支、结果读取、科学诊断及比较。 |
| 进程完整性 | COMPLETE | 独立会话、进程组、取消、墙钟超时、调度器进程强杀后回收均实测。Linux 原有内核死亡通知和限额实测通过。macOS 原生进程 CPU 计时到达阈值后回收所属进程组，忽略软信号的负例通过。 |
| macOS 内存约束 | PARTIAL | 实际 worker 收据为 `NOT_ENFORCED`。Darwin `RLIMIT_CPU` 内核硬限额仅标为已配置，另由 CPU 监测执行回收。 |
| SQLite 与对象故障恢复 | COMPLETE | 工件无覆盖发布与目录同步、备份审计事务一致性、独立数据根的进程退出注入、损坏数据及未知旧审计尾部拒绝。 |
| 历史 v0.1、v0.2 与 v0.3 恢复 | COMPLETE | 真实旧提交生成和备份，v0.3 在两端恢复后读回相同工件。v0.2 留出集的原预留与实验身份保留。 |
| 真实突然断电 | NOT_RUN | 证据范围为两端当前文件系统和实际进程强杀或退出注入。 |
| 新实证预测、因果或正式科研验收 | NOT_RUN | 理论和合成数学复算，新增真实预测和其他科学证据均为零。 |

## 原生运行及故障记录

| 运行环境 | 工具 | 最终结果 |
| --- | --- | --- |
| 标准 `ubuntu-24.04` x86_64，Linux 7.0.0-1017-azure | Python 3.12.16、SQLite 3.45.1、Node 24.22.2、npm 11.19.1、Git 2.56.1、Chromium 151.0.7922.34 | 182 passed，11 subtests passed。Job 134643053964。 |
| 标准 `macos-15` ARM64，macOS 15.8.2 | Python 3.12.10、SQLite 3.49.1、Node 24.22.2、npm 11.19.1、Git 2.56.0、Chromium 151.0.7922.34 | 181 passed，11 subtests passed，1 个 Linux 专项跳过。Job 134643054232。 |

两端的完整测试、TypeScript/Vite、三种解释器守卫和浏览器步骤均成功退出。pytest 各报一条既有 Starlette/httpx 弃用警告。CLI 每端实际运行 56 条命令，43 条退出 `0`，13 条拒绝用例按预期退出 `1`。普通模式、`python -O` 和 `PYTHONOPTIMIZE=1` 分别实测优化标志 0、1、1，科学结果与拒绝信息一致。 [GitHub 回读收据](v03/ACCEPTANCE_RESULTS.json) · [各步命令、退出码和原始输出](v03/verification-evidence.zip)

首轮 `a54c044b730e33a231513b740824fbb71cb50170` 的 Linux 测试通过。原生 Darwin 在忽略 `SIGXCPU` 后超出 8 秒测试期限，证明仅配置的 `RLIMIT_CPU(1,2)` 没有在该环境提供强杀保证。修复保留 POSIX 限额配置，增加 `SIGXCPU` 所属群组终止和以 `time.process_time()` 为时钟的独立回收。最终原生负例在忽略软信号后确认 `SIGKILL`。另测休眠不计入 CPU 时间预算及回收所属后代。生产收据将 CPU 软预算 5 秒和监测回收阈值 6 秒分开记录。此保证适用受信任内置 Python 机制及所测故障，内核硬限的配置与测得的在进程监测分开。 [首轮 Run 44256389862](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44256389862) · [修复与最终原生结果](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44257641232)

Linux 收据包括 `RLIMIT_CPU`、`RLIMIT_AS`、`PR_SET_PDEATHSIG` 和 `OWNED_SESSION`。macOS 包括 `DARWIN_PROCESS_CPU_WATCHDOG`、`RLIMIT_CPU_CONFIGURED_ONLY`、`PPID_WATCHDOG_KILLPG` 和 `OWNED_SESSION`。两端的取消、超时、杀死调度器后的 worker 回收、含留出预留的重启及失败产物拒绝均包含真实进程测试。恶意第三方插件和全进程组资源隔离超出本版受信任执行范围。 [worker 生命周期及跨平台收据](v03/ACCEPTANCE_RESULTS.json)

## 科学口径及跨平台身份

- 来源注册核对 R132 Phase A/B 的冻结协议、源码、测试、报告和两份机器收据。平台保留先前登记使用的固定正式提交 `7ea6eab94433e3669b6f492d802bb35316dc90d6`，与本轮 main 的 R132 文件字节一致。PR #44 仍为 Draft，其候选内容使用只读身份。并行的 #54 涉及独立研究目录。 [R132 的 11 项文件身份](v03/R132_SOURCE.json) · [PR #44](https://github.com/edwardsage419/Psychohistory-Research/pull/44)
- Phase A 共核对 84 个精确状态及 252 次平移、252 次缩放检查。Phase B 核对 75 个精确状态，69 个满足原世代出生条件的状态通过 Eq.3/Eq.4 对照。Logistic、Stag–Hare、Hawk–Dove 的 216 个连续解析端点最大误差为 `8.5937959964728e-11`，原归档门槛为 `1e-6`。Hawk–Dove 在 Euler `h=4` 到达 0，连续参照为 `0.3432022795378542`，Eq.3 原矩阵结果 `2/5`，归档平移矩阵结果 `8/17`。RPS 40 步时 Euler 与 RK4 的乘积漂移分别为 `-0.010113456173247866` 和 `1.0209743605200928e-7`，80、160、320 步收据一并保存。 [数学复算全记录](v03/ACCEPTANCE_RESULTS.json)
- 两平台得到相同的 R123、R132 原始轨迹和快照，五种根工件的完整 SHA-256 均匹配。CLI Logistic RK4 工件为 `6bb3fa1d6c9a60ee1d6289b09274d4c6c91c2dc4630aadf901c9366efc376791`。独立恢复分支的轨迹与快照哈希也匹配。将两端各自的父运行 ID 写入同一信封后分别复算出两个完整分支哈希，差异定位至 `input.branch_from`。 [跨平台哈希与差异归因](v03/ACCEPTANCE_RESULTS.json)
- Chromium 对齐 41 个 Euler／RK4 观测点，两端返回规范最大差 `0.000893126839433267722382866723062316908141`，并实测显示伪灭绝告警与三类比较拒绝。独立审查复现二进制绘图舍入将合法差值变成零，修复后以每个时点的规范数值计算。新回归检出 `4.6874999996093749995117E-20` 的差。 [接口和 Chromium 收据](v03/verification-evidence.zip)

## 恢复与独立审查

对象先同步文件字节，排他链接后同步目录，之后才允许完成状态引用该工件。SQLite 将来源登记和运行状态变更各自与相应审计事件在同一事务中提交。备份由同一个 SQLite 快照导出审计，保留旧 JSONL 内容并拒绝无法纳入的未知尾部。迁移与恢复验证先在暂存目录执行，成功后发布。实测覆盖提交前、提交后镜像前、镜像同步后退出，及重试、并行发布、半写入旧行和恢复错误。旧数据恢复保留原工件，v0.1 在两环境的完整哈希差异经独立复算可由其原版记录的 Python 补丁版本解释。v0.2 两端恢复均读到 `106a34318f686facb552fb61e4b480118b33c4d83570cd700eff4d1b9f335316`，并核实留出集预留仍有效。 [运行与恢复收据](v03/verification-evidence.zip)

独立审查复现并复核了伪造检查点、错误内部轨迹、精确初值被绘图舍入、数值差被绘图舍入、备份遗漏旧失败事件以及恢复失败提前发布目录。最终独立复跑 85 个 v0.3 测试全部通过。失败输出和修复回归另存。 [独立负例和证据归档](v03/verification-evidence.zip)

## 复现、范围与 v0.4

检出测试 SHA 后，从 `platform/future_model` 运行 `bash scripts/install.sh`、`bash scripts/verify.sh`。工作流给出三种解释器模式、CLI 与 Chromium 的准确命令，macOS 先通过 `pwd -P` 规范化临时目录。归档 SHA-256 为 `427719e50b9e208c9702e70bb254d7ac413dfbdead7a36e9dc52dd93b987fdef`。 [验收工作流](../../../.github/workflows/psychohistory-platform-v03-acceptance.yml) · [运行证据归档](v03/verification-evidence.zip)

公开仓库使用 GitHub 标准免费 `ubuntu-24.04` 和 `macos-15`，工作流令牌权限为 `contents: read`，触发范围为同仓库 v0.3 工程分支的 PR。新增费用为零。Git 差异仅含 `platform/future_model/` 和一份工程验收工作流，正式科研及冻结目录的差异为空。 [标准运行器费用规则](https://github.com/github/docs/blob/main/data/reusables/actions/supported-github-runners.md)

v0.4 建议先开展经授权的断电持久性与 macOS 内存控制验证，再扩展过审模型的数值稳定性与不确定性诊断。全 R 系列研究、统一分类、模型熔炼和个人决策应用的原有先后顺序继续适用。
