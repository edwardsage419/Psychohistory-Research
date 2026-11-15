# Psychohistory Platform v0.1：十一门验收

日期：2026-11-15（Asia/Shanghai）。独立分支 `feat/psychohistory-platform-v0.1`；基线 main `0aa29bb2dc73c6667ea0a1ae40f1092276d025c6`。

**当前状态：PR #40 已建立并完成后续自主工程审查；Linux 闭环已修复并验证。整体不是全 COMPLETE，Gate 01 的 macOS 原生实测仍为 NOT_RUN。最新修复与收据见 [PR #40 审查报告](PR40_ENGINEERING_REVIEW.md)，下列首次交付的远端恢复 SHA/哈希保留为历史记录。** 不将工程、合成测试、科研预测能力互相替代。

| 门槛 | 状态 | 实际证据与边界 |
|---|---|---|
| Gate 01 工程可运行 | PARTIAL | Linux 安装、启动、健康/API 请求、关闭、54 项 pytest、严格 TS/Vite 与 python -S 核心均通过；macOS 原生 NOT_RUN。|
| Gate 02 科研接入 | COMPLETE | 真实 R233 收据只读读取/哈希/解析/登记/去重；原字段和 R_SERIES_ORIGINAL 原样保留，BROWSE_ONLY。缺失、无效 JSON、symlink 与越界来源拒绝。未执行研究代码。|
| Gate 03 模型插件 | COMPLETE | individual@1.0.0 与 group@1.0.0 实际注册和运行；能力方法真实存在；源代码 SHA 与假设/参数/权限描述；多版本并存与旧状态版本不兼容拒绝。|
| Gate 04 跨模型适配 | COMPLETE | binary-population-prevalence@1.0.0 交换真实生成状态；拒绝类型、单位、身份、联合依赖、未来可用时间、无效离散轮次、额外载荷、不一致不确定性。|
| Gate 05 状态与分支 | COMPLETE | 根、初始 fork、逐 tick 不可变快照及事件/RNG/父哈希实际保存；两独立分支；备份恢复后所有父引用可解析与验哈希。PR #40 已补充快照信封及内置插件状态的语义校验；未知第三方状态仍不开放执行。|
| Gate 06 不确定性 | COMPLETE | 实际 Bernoulli 离散概率、UNKNOWN；有限性与概率和检查；无证成的类型转换/联合分布映射拒绝。其他不确定性类别保留独立协议，不宣称已实现通用推断算法。|
| Gate 07 调度与资源 | COMPLETE | PENDING→APPROVED→RUNNING→COMPLETED；实际 spawn、单并发/队列上限、取消、墙钟超时、失败/重启处理、旧任务超过 200 条历史仍受管理。Linux 512 MiB RLIMIT_AS / 5 CPU 秒，实际记录 enforced；恶意代码沙箱不是本版能力。|
| Gate 08 科学证据与权限 | COMPLETE | discovery、工程状态、科学原证据和执行准入分开；REAL_EXPERIMENT/冻协议变更均拒绝；前端无法绕过后端 token/准入。无科学证据升级，无研究文件修改。|
| Gate 09 真实 Web 流程 | COMPLETE | 实际系统 Chromium 操作连接→提交→明确批准→完成→分支/结果/版本/日志→来源→模型→历史，9 步通过，无 pageerror；最终代码再测通过，截图与 BROWSER.json 保存。|
| Gate 10 复现与安全 | COMPLETE | 同种子与版本确定性；运行源码/版本/协议/数据/Python/OS身份锁定和 worker 结果核验；认证、跨源、请求预算、非法路径、symlink、错误版本、备份清单穿越/篡改拒绝。独立审查 5 个 Important 已回归修复。|
| Gate 11 持久化与灾难恢复 | COMPLETE | 多检查点实际推送并 ls-remote 核验；从 GitHub eaafc58ece6a8f9a8d34f3fb5d1d632395fa21ec 全新克隆、新 venv、npm ci、完整套件/构建、实验与 Git 样例逐字段相等；一致 SQLite 备份/新目录恢复/产物哈希通过。大/受限数据持久化 BLOCKED，不入 Git；PR #40 已实际建立，未合并。|

## 真实命令与收据

- `bash scripts/verify.sh` 最终：**54 passed，1 warning**；严格 TypeScript/Vite 与纯标准库核心 PASS，见 pr40/verify.log。
- `scripts/browser_check.py`：**PASS**；9 步、无 pageerror，见 BROWSER.json、console.png。
- `scripts/disaster_recovery.py --expected-sha eaafc58e…`：**PASS**；8 条实际命令退出码均 0。恢复时该远端检查点套件为 33 项；后续仅增加 4 项安全/兼容性测试和报告，核心源码身份未变。见 DISASTER_RECOVERY.json、logs/remote-recovery.log.gz（解压后 SHA 与收据一致）。
- 合成样例/运行元数据：`../examples/synthetic-result.json`、`../examples/synthetic-run-metadata.json`，seed=123，rounds=6，population=16，intervention=0.2，产物 SHA `0c73f57111a60a9dd1b028c8b88fa7989ae19f401ce0dd479b7d0cd2e1e6a397`。
- 代码身份 `62dd225bf818b93bd8d668168d1ba3ce01b4b4edd32e5784d49a9d38b8a5e109`；此为完整 Python 包源码内容身份，与 Git 提交 SHA 分开。
- 独立审查：INDEPENDENT_REVIEW.md；修复及未运行项：PROGRESS.md、FAILURES.md；原 RED 输出不删除。

## 云端恢复与并发保护

已发布环境 `cecfgver_6af998225600819ab236f246b8e01110` Start skill 实际执行；恢复基础依赖，不依赖上一任务 SQLite/临时文件。当前 main 最新比环境快照多一科研文档提交，工程从最新 main 建分支。9 个既有开放 PR 通过 GitHub 页面和原生 Git ref 只读核验，目标范围与 platform/future_model 无重叠（PR_SCOPE_CHECK.json）。未合并任何 PR，未重跑既有科研线程。

## 资源与费用

Debian 13 x86_64；Python 3.12.14 / pip 26.2.2；Node 24.22.1 LTS / npm 11.9.0；Git 2.52.0；SQLite 3.53.1。5 个可见 CPU，cgroup 4 核配额；内存上限 32 GiB、约 32 GiB 可用；磁盘约 60 GiB 可用，/workspace 和 /tmp 可读写。只用小规模合成数据和免费工具，无 ML/GPU/新增服务。

未购买额度，未调用计费 API，未配置 OPENAI_API_KEY，未启用 CI/部署或新增收费资源。Codex 订阅/剩余额度和 Only me 的账户设置无法由当前工具核验；未声称核验成功。当前限制网络为 package_managers，PR 需要额外 api.github.com；源草稿保存与当前实例生效分开报告，见 NETWORK_AND_PR.json。

## 待办与不夸大的交付边界

1. PR #40 仍保留 draft，供 owner 审阅；当前 GitHub API 已验证可用，无需再为此修改或发布环境。
2. macOS 原生验收 NOT_RUN；不要求 Mac 在线，不虚构跨设备/原生测试。
3. 先前 M1 已补充内置插件状态及快照结构校验；任意第三方插件、外部快照执行和真实资料实验仍不开放。
4. 不合并、不公开部署、不启动全库分类、原创熔炼、个人决策 App；合成结果不证明真实科研预测能力。
