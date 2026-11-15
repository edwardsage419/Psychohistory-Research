# Psychohistory Platform v0.1 · M4 MacBook Air 原生验收

**本机工程验收 COMPLETE（v0.1 内置合成工作流）。** 2026-11-15（Asia/Shanghai）。发布基线为 GitHub `main` 的 `5a6cf7fae98e3919db4a6f9c8bb9dfd8721d1431`。历史分页验收脚本在该基线上遇到一项 macOS 启动缺陷，独立分支修复并复验通过。macOS 的 CPU、地址空间和父进程死亡保护均为 **NOT_ENFORCED**。工程结果适用于受信任的内置合成模型。 [PR #40](https://github.com/edwardsage419/Psychohistory-Research/pull/40)

## 实机和来源

| 项目 | 实测 |
|---|---|
| 环境 | 本机 MacBook Air（Mac16,12），Darwin ARM64，macOS 15.3（24D2059） |
| 芯片、CPU、内存 | Apple M4，10 核（4 性能核 + 6 能效核），16 GB 统一内存 |
| 磁盘 | 数据卷 228 GiB，起始可用约 144–145 GiB（`df -h`） |
| 工具 | Python 3.12.3 ARM64、Node.js 24.22.3 ARM64、npm 11.19.1、Git 2.56.0、SQLite CLI 和 Python 模块均为 3.43.2 |
| 浏览器 | Google Chrome 157.0.8103.51（Chromium），Playwright 1.62.0，headless；Chromium 返回 ARM/64-bit，macOS `sample` 对浏览器主进程返回 `ARM64` |
| 电源 | 接入 AC，起始电池 100%，低电量模式关闭。系统未报告已记录的热或性能告警。未测电池模式、持续散热、温度或功耗曲线 |
| 版本核对 | `git ls-remote`、隔离克隆 `HEAD` 和指定合并 SHA 一致。`3ecc1cdca4f51a7fd0a4e1f56e32d80a3da7a74c` 是该提交的祖先，记录了此前托管 M1 的 macOS 结果。 [托管验收](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/43716616538) |

代码、依赖、Chrome 临时配置和所有运行数据库位于独立测试目录。各数据根使用物理路径 `/private/tmp/…`。浏览器的登记页使用只读合成收据，正式 pytest 中的登记用例只读访问隔离克隆内的公开仓库收据。R073、PESEN v0.1 及其他冻结协议未发生变更。执行仅使用内置合成机制。

## 工程结果

| 验收项 | 状态 | 实际结果 |
|---|---|---|
| 锁定依赖安装及首次启动 | COMPLETE | 正式 `bash scripts/install.sh` 重跑 exit 0。锁定 Python wheels 和 `npm ci` 均成功。首次成功启动的 FastAPI 环回健康检查返回 200 |
| 完整 Python 套件 | COMPLETE | **53 通过、0 失败、1 跳过、1 警告**。修复前后均复验；单项结果见 `pytest-detailed.log`。警告为 Starlette 的 httpx TestClient 弃用提示 |
| 严格 TypeScript / 生产构建 | COMPLETE | `tsc --noEmit` 以仓库的 `strict: true` 配置单独执行通过。正式验证调用 `tsc --noEmit && vite build` 通过，Vite 8.3.8 生成静态产物 |
| 独立数学核心 | COMPLETE | `python3.12 -S` 不加载第三方依赖，两次运行结果相等。完整 pytest 验证两个分支从共同快照独立派生、快照状态冻结、哈希/信封和父引用校验、交互时序和概率约束 |
| CLI/API 执行与拒绝 | COMPLETE | 真实 CLI 子进程执行 `demo`、`submit`、`approve`、`cancel`、`runs`、`result`、`backup`、`restore`。非法人口返回 exit 1。pytest 另覆盖 `status`、历史分页、版本锁、无关任务隔离、非法版本/参数和重启。真实 HTTP 验证健康 200、无令牌/错误令牌 401、合法令牌 200、跨源和真实实验请求 403、额外模型版本字段 422、Swagger 404 |
| 任务调度与历史 | COMPLETE | 16 条待批可入队，第 17 条拒绝。取消 13 条，3 条经审批按顺序完成，生命周期无重叠。终态历史拒绝修改。浏览器验证 203 条记录和 5 页 |
| 失败、取消、超时、关闭及重启 | COMPLETE | pytest 覆盖工作进程失败。额外有界探针确认活动 worker 在取消、墙钟超时、正常调度器关闭时收到 SIGTERM 并退出。强杀调度器后的孤立进程及重启行为见下节 |
| 实机 Chromium | COMPLETE | 生产构建 9 步主流程及修复后的 203 条记录历史流程均通过，均为 0 page errors |
| SQLite、产物与复现 | COMPLETE | 备份和新根恢复通过，持久化副本再次实际恢复。7 条运行记录逐条相等，完整性检查 `ok`，schema 2，2 个唯一对象通过 SHA-256。基准按相同种子连跑 5 次，全量载荷逐字段相同 |
| 本机权限和路径 | COMPLETE | 新建数据根和 staging 为 0700，令牌、审计文件、新建对象为 0600。默认 umask 022 下 SQLite 文件为 0644，访问边界依赖其 0700 父目录。符号链接根、`/tmp` 和 `/var/tmp` 路径均被拒绝。生产服务仅监听环回，关闭后健康端口不可达 |
| Linux 专用父死亡回归 | NOT_RUN / SKIPPED | `tests/test_pr40_review.py::test_killed_scheduler_cannot_leave_worker_publishing_results` 依赖 Linux `PR_SET_PDEATHSIG`，pytest 按平台跳过。下节记录独立的实机 macOS 探针 |
| 电池、长时满载和恶意代码隔离 | NOT_RUN | 在 AC 电源下采用保守的合成短样本。平台当前没有第三方代码执行路径，进程隔离仅服务于受信任内置插件 |

pytest 计数按最后一次完整套件统计，重跑和补充探针不叠加。另计两项最终 Chromium 流程 **2 通过、0 失败**，五组合成探针 **5 通过、0 失败**，已归档备份的独立复原 **1 通过、0 失败**。工程验收执行的两次历史失败为首次安装的本地 npm 配置冲突和基线 Linux 专用浏览器路径。

## Chromium 实际交互

- 主流程以生产静态构建连接令牌、提交并批准、等待 COMPLETED、查看两个情景分支及版本、登记合成来源、检查模型注册、打开历史。9 步通过，0 页面异常。合成收据前后 SHA-256 一致。执行 6.252380 s，服务从进程启动到首次健康响应为 0.186717 s。
- 分页流程在 203 条合成记录中取消最旧待批任务，翻至第 5 页取回旧结果，返回第 4 页仍保留选中项，再在情景历史页确认同一实验。修复后执行 1.177791 s，0 页面异常。
- 浏览器绑定独立临时配置，两个 FastAPI 实例均正常退出。令牌没有出现在命令参数、执行日志或备份中。

## 性能原始样本

5 次顺序运行，独立数据根，种子 123、6 轮、16 个合成个体、干预参数 0.2。正式样本在依赖安装完成后采集。端到端时间含 Python 启动、调度和落盘。worker 生命周期为数据库记录的 `ended_at - started_at`。RSS 每轮轮询间隔含 10 ms sleep，记录 CLI 与其直接子进程各自的最大样本。

| 次数 | CLI 墙钟 s | worker 生命周期 s | CLI 峰值采样 RSS KiB | 直接子进程峰值采样 RSS KiB |
|---:|---:|---:|---:|---:|
| 1 | 0.192797 | 0.054082 | 31888 | 18816 |
| 2 | 0.215222 | 0.075355 | 31792 | 19696 |
| 3 | 0.190247 | 0.053474 | 31872 | 18768 |
| 4 | 0.213312 | 0.053396 | 31696 | 19216 |
| 5 | 0.195412 | 0.053442 | 31024 | 19056 |

| 测量 | 原始值 |
|---|---|
| 首次安装尝试 | 144.92 s，Python 已装齐，npm 配置冲突，exit 1 |
| 修正配置后首次完整安装 | 86.78 s，复用已安装 Python，npm 缓存原为空，含正式构建，exit 0 |
| 浏览器锁定依赖安装 | 37.22 s（pip 段，使用已安装的原生 Chrome） |
| 纯核心 5 次墙钟 | 0.008777、0.007196、0.007299、0.007014、0.007871 s |
| 探针进程 RSS 高水位 | 47,005,696 bytes（含框架、保留的合成对象与探针上下文） |
| 同一档案 CLI 备份 / 恢复 | 0.114174 / 0.036935 s，归档 391,570 bytes |
| 验证后的存档副本再次恢复 | 0.03 s（`time -p` 显示精度），SQLite `ok`、schema 2、7 条记录、2 个对象 |
| 有界墙钟超时 / 取消 / 正常关闭 | 0.8 s 配置下超时在 0.808289 s 落为 FAILED；取消 0.138770 s 和关闭 0.152201 s 落为 CANCELED，三例 worker 均以 SIGTERM 结束 |

**性能判断。** 这组短样本端到端中位数 0.195412 s，纯核心中位数 0.007299 s。启动、轮询与存储占据大部分端到端时间。RSS 是抽样下界，直接子进程列包含同一 CLI 的子进程，峰值不相加。样本规模和电源状态限制了结论的外推范围。

## 数据恢复与安全边界

- 5 次重复实验的相同产物 SHA-256 为 `9369c792e32676aa84b4d8315d1245cb185c1f877d453f7127a637ea8de834dd`。备份清单覆盖 SQLite、审计和两个不同哈希的对象。新根中的 6 条完成运行可经 CLI 读取，且每条结果与原根一致。归档副本再次解包还原并比对数据库行和对象字节。令牌、调度锁与 staging 均未归档。
- macOS worker 计算点实读 `RLIMIT_CPU` 与 `RLIMIT_AS`，软/硬上限均为 `RLIM_INFINITY`。任务元数据记录的 5 s CPU 和 512 MiB 地址空间预算为 **NOT_ENFORCED**。墙钟超时、队列上限和单 worker 仍实际生效。
- macOS 的父进程死亡保护为 **NOT_ENFORCED**。探针先暂停该次合成 worker，再 SIGKILL 其调度器。worker 被 PID 1 接管，恢复执行后把真实合成结果写入 staging，并自行退出。重启调度器把原 `RUNNING` 标为 `FAILED`，结果引用为空，内容寻址目录没有新增对象。这个实验使用测试控制点同步，便于稳定观察中间状态。
- Linux 代码路径使用 `RLIMIT_CPU`、`RLIMIT_AS` 及 `PR_SET_PDEATHSIG`，后者安装后还核对父 PID。本次实机未运行 Linux。内容哈希用于完整性校验，普通进程隔离不构成恶意代码沙箱，环回令牌也不提供多用户权限体系。数据根路径检查以受信任目录和本机权限为前提。

## 问题、提交与费用

| 问题 | 修复及复验 |
|---|---|
| 首次安装配置冲突 | 本次隔离设置将 npm 用户及全局配置均指向 `/dev/null`，npm 拒绝 double-loading。同一锁文件下改用两个不同的空配置，正式安装脚本通过 |
| 原生 Node.js 校验环境 | 首次 `shasum` 继承 macOS 上不可用的 `C.UTF-8` locale 而退出。改用 `LC_ALL=C` 后，ARM64 归档通过官方 SHA-256 校验，再解包 |
| 本地默认工具沙箱限制 | 默认 shell 的 GitHub DNS 和环回监听受到限制。GitHub 读取和原生浏览器/HTTP 探针经工具审批后在同一台 Mac 的本地 shell 完成 |
| 历史脚本绑定 Linux 浏览器路径 | 在基线以真实 Playwright 复现 `BrowserType.launch: Failed to launch chromium because executable doesn't exist at /usr/bin/chromium`，exit 1，未进入页面。修复脚本接收 `PH_CHROMIUM_EXECUTABLE`、在 macOS 默认使用 Playwright 自带浏览器、仅在 Linux 沿用原默认路径和参数。相同 fixture 和浏览器上，203 条记录的回归 exit 0，完整工程验证重跑通过 |

修复提交为 `26188e5cd493840c524fb4e49a4ce04802488f8d`，分支 `fix/m4-native-browser-validation-20261115`。本报告与修复提交至同一独立审阅 PR，目标为 `main`，状态为草稿。 [PR #41](https://github.com/edwardsage419/Psychohistory-Research/pull/41)

此次产生新增费用 **0**。依赖来自免费公共注册表，使用已安装的 Chrome，无外部模型 API、付费服务或托管测试运行。

## 命令与证据索引

运行目录为 `platform/future_model/`。下列占位路径须替换为独立、已规范化的实际路径。各文件含执行时间、退出码和输出。详细日志、截图、探针脚本和纯合成的 SQLite 归档单独保存于本机。

| 命令或入口 | 证据 |
|---|---|
| `sw_vers`、`uname -sm`、经字段过滤的 `system_profiler SPHardwareDataType`、`df -h`、`pmset`、`git ls-remote`、`git merge-base --is-ancestor` | `environment.log`、`environment-supplement.log`、`github.log` |
| `bash scripts/install.sh`、`bash scripts/verify.sh`、`.venv/bin/python -m pytest -rs -v -p no:cacheprovider --basetemp <CANONICAL_TMP>` | `install.log`、`install-retry.log`、`verify.log`、`pytest-detailed.log`、`verify-after.log` |
| `python -m pip install --index-url https://pypi.org/simple --only-binary=:all: -r requirements-browser.lock`、`scripts/browser_check.py`、`scripts/browser_history_check.py --prepare` 和实际交互 | `browser-install.log`、`browser-main.log`、`browser-history-before.log`、`browser-history-after.log`、浏览器 JSON/截图、`chrome-architecture.log` |
| `PYTHONPATH=src .venv/bin/python native_probe.py <NEW_CANONICAL_DATA_ROOT>`、`bash scripts/run.sh --data <NEW_ROOT> restore <ARCHIVE>`、`sqlite3 … 'PRAGMA integrity_check;'` | `native-probes.log`、`native-probes-final.log`、`persistent-archive-restore.log` 和独立保存的合成归档 |
