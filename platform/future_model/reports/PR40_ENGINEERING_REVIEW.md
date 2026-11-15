# PR #40 自主工程审查与必要修复

日期：2026-11-15（Asia/Shanghai）。审查基线：`23843c2afcfb5e3f28b3ce047804cd7f9144e4b9`。PR 实际 open/draft，base main `0aa29bb2dc73c6667ea0a1ae40f1092276d025c6`，无已有审查/行内/issue 评论。本任务只修复工程，不扩大科研功能。

## 已复现与修复

| 问题 | 修复 | 验证 |
|---|---|---|
| CLI 查询会启动整个调度器，将邻近 APPROVED 任务运行后取消；Web owner 运行时 CLI 也不能查询 | runs/status/result/discover 直接读取/登记 Store；离线维护禁用自动调度；approve/demo 仅显式目标执行 | 真实 CLI 子进程检查读前/读后状态、时间、日志与 PID 不变；持有 Web owner 时查询成功；显式批准不干扰其他队列 |
| CLI 批准遇到 BLOCKED/FAILED 仍 exit 0 | 保留结构化终态，但非 COMPLETED 返回非零 | 旧源码锁测试真实返回 BLOCKED / exit 1 |
| 控制台只读取前 200 条历史，隐藏旧活动任务及已完成结果 | 新增受鉴权 /runs/active；50 条分页；按 ID 保持所选结果；计数标明本页及活动任务；过期轮询响应不覆盖新页 | Chromium：203 条记录、最旧任务取消、翻至第 5 页读取旧结果、翻页后选择保留，PASS |
| 调度器被强杀后 worker 仍计算并写 staging | Linux PR_SET_PDEATHSIG，安装后核对父 PID 关闭竞态；其他平台明确 NOT_ENFORCED | 真实 SIGKILL owner 的子进程回归：worker 退出、不发布孤立结果；独立原探针复验 |
| 离散概率接受 dict 而非数组，UNKNOWN 可携带量化结果 | 明确 JSON 数组类型，禁止 UNKNOWN/UNIDENTIFIABLE 夹带量化载荷 | 负向输入先 RED 后 GREEN |
| 插件状态恢复只校验身份；正确哈希不能保证信封完整或状态可用 | 校验内置 individual 二元状态、group 有限比例；快照校验必要字段、身份、父哈希、事件/环境结构 | 缺失、错误类型、缺失值、bool、NaN、越界比例及正确状态 round-trip |
| 恢复一次性读取全部产物，内存随档案总量增长 | 256 KiB 分块复制，逐文件验哈希、对象预算和 SQLite 引用；只在全部成功后发布新根 | 8×2 MiB 对象恢复：旧实现 tracemalloc 峰值 16,829,155 bytes；新实现通过 <10 MiB 上限及全部内容验真 |

## 实际验证

- 基线 37 项通过；新增 17 个回归先观察失败，再修复：**完整 pytest 54 passed，1 warning**。警告为原 Starlette/httpx 弃用提示，未隐藏。
- 严格 TypeScript/Vite 构建、`python -S` 独立核心 PASS。
- 原 9 步 Chromium 科研流程 PASS；203 条记录的分页/活动任务/选择保持回归 PASS。
- 独立审查与定向复验：`pr40/INDEPENDENT_REVIEW.md`、`pr40/FIX_REVIEW.md`。复验未发现新的 Important/Critical 问题。
- 原始 RED、最终测试日志、浏览器收据保存在 `pr40/`。首次新增浏览器断言等待已取消任务继续留在活动列表而超时；改为选中取消目标并验证详情终态后通过，未禁用测试。
- 合成样例按修复后的源码身份重新生成；旧版本仍保留在 Git 历史，不修改科研证据、不复写原冻结协议。
- 修复后的远端全新重建/SQLite 恢复收据由 `pr40/remote-recovery.json` 记录；具体已测试提交与原始日志哈希以该收据为准。

## 边界与结论

没有发现尚未处理的已复现阻断缺陷；这是已声明的 Linux、本地、受信任合成插件范围内的工程审查结论，不是任意第三方代码/状态或真实预测的安全与科学认证。原后置 M1 的内置状态/快照校验缺口已处理；未来第三方插件必须有自身状态校验。

macOS 原生仍 NOT_RUN，Gate 01 仍 PARTIAL，不将全部门槛称为 COMPLETE。未合并 PR、未部署、未启用收费服务或新增 CI、未修改 research/theory/protocols 等科研内容。GitHub API 当前实测正常；旧 NETWORK_AND_PR.json 是前一运行实例的历史阻塞记录，不代表当前状态。
