# 心理史学 R 系列完整性修复与历史 PR 整合报告

本轮基准及结束前回读的最新 main 均为 **1e839d3b02cae02833b282c309f5abd58559949e**。不使用旧状态报告推断当前 main。Issue #34 仍 open，当前 R132 checker blob 为原缺陷版本；九个指定 PR 仍 open/draft，当前头分别保存于 PR_HEADS.json。没有发现并发 R132 实际修改；本轮不重复已有 R273/R277/R077 数学研究。

## A. R132 Phase B：实际修复

修改现有 `research/R132/r132_phase_b_ci_attest.py`，原数学源码和原 70 项测试源码不变。原 **13 项数学验收条件全部保留**，改为不受优化影响的显式拒绝；计数严格为整数、布尔证明须为 True、绝对误差有限且非负。精度仍为 `<1e-6`，75 Fraction 场、>40 Eq3/Eq4 状态、216 条轨迹、禁止真人/动物序列等门槛没有放宽。

同时修复 Issue #34 的后续问题：不再凭常量声称“70 项测试成功”。checker 在同次调用启动真实 native unittest 子进程，核对运行 ID、源码 SHA、70 项真实执行、0 failure/error/skip/expectedFailure/unexpectedSuccess、真实退出码及优化级别。父数学模块与子数学/测试模块均直接编译所校验源码字节，避免同大小/时间戳 `.pyc` 替换真实测试。独立审查确实复现了缓存漏洞，三模式 RED 后已修复并独立复验，见 final-integrity-review.md。

收据使用新的 v2 格式和默认文件 `R132_PHASE_B_ATTESTATION_V2_LOCAL_ENGINEERING_RECEIPT.json`，明确 **LOCAL_CODEX_CLOUD_NOT_GITHUB_ACTIONS**。本轮实际 v2 结果在 logs/r132-phase-b-{normal,optimized,environment}.json。历史 Phase A/B 收据和最终科研验收 JSON 未改；同名历史收据输出被拒绝。新尝试开始先清除其自有旧 v2 成功记录，校验失败、源码缺失或原子发布失败均不遗留该成功记录；临时文件清理，成功时才原子替换。

注意：现有 GitHub 工作流/发布步骤仍保留历史收据路径。本轮**没有调整、启用或派发生产 CI**；v2 路由与发布需另行审阅授权，不能把本地成功称为 GitHub CI 重新验收。Phase A 数学/单测回归通过也不意味着其历史内联 workflow 中的 assert 已全部加固。

### 实测

- Phase A 原有 **70 项**在普通、`python -O`、`PYTHONOPTIMIZE=1` 下分别全部通过。
- Phase B 原有 **70 项**通过新 checker 的真实源码绑定子进程在三种模式下分别全部通过；每模式完整独立复算216轨迹，最大绝对误差 `8.593809691648246e-11`。
- 完整性测试 **5 个 unittest 方法**通过，其中 **24 类 × 3 模式 = 72 次故障注入子进程**全部拒绝且无新/遗留自有成功收据。覆盖关键数值、数量不足、真假布尔、真人/动物序列、无/失败/少测/错源码/错 run 测试证明、加载源码身份不符。
- 另含历史不可写、源码缺失、原子发布失败、三模式缓存替换回归。缓存回归实际执行真实70测试，不能把70个缓存空测试当作有效测试。
- 原有 R132 10 个数学源码/测试/报告/历史收据文件逐字节与最新 main 相同，见 IMMUTABLE_R132_FILES.json。未改 R073、PESEN 或 protocols。

完整结果与 raw streams：R132_TEST_MATRIX.json、logs/。首次66项 RED 是修复前的旧矩阵；最终扩大为72项，不把旧失败隐藏或改写为成功。

## B. 九个历史 PR 当前资格

**以下“可合并”仅指工程/证据归档，不是科学准入或生产启用。未经 owner 新授权，本轮未合并任何 PR。**

| PR | 当前固定头（短 SHA） | 工程归档结论 | 依赖和仍阻塞事项 |
|---|---|---|---|
| #30 | 8005fcb7 | 可归档；preflight 两处元数据文字修正，算法/否决不变 | 必须先于当前 #31；不得据此解除 R077 生产否决 |
| #31 | b928dc8d | 可归档；当前头已经采纳正确 pin 刷新 | 17 个外部 pin 仅在 main+#30 全匹配；不要再次套用 #35 的旧补丁；真人数据/许可/生产仍 BLOCKED |
| #32 | 16778c53 | 可归档；模板/工具/候选 patch 不等于已部署 | R127 正式 workflow、发布政策、真实无增费 CI/权限与外部 provenance 未授权/未验证；05-003 科学状态不提升 |
| #33 | 9d5041ac | 可归档；真实组合下否决按预期保留 | 普通/-O 均 exit2，production_ready=false，11 原失败/35 候选正确；R077 使用准入仍 BLOCKED |
| #35 | 9ae4eb92 | 可归档；保留已完成 R127/整合检查 | 当前 #31 已修正其旧报告中的 pin 障碍；旧整合驱动固定旧基线，不能冒充最新复验，也不能重复应用旧 pin patch |
| #36 | 211f90b2 | 可归档；R273 Python 发射/S69 Node 入口及有界 join 的证据范围明确 | 原发射程序在普通模式运行，不证明其所有 assert 可抗优化；R077 来源/许可/session 资格仍 BLOCKED |
| #37 | a6f51d4b | 可归档；S73 原生 Node 文件 I/O 和负向证据 | 15 个子进程不是15个单测；协议写 Python 而归档实现 Node，仍需科学 owner 裁定，未改协议 |
| #38 | fbf71dca | 可归档为缺陷证据/候选资格 | 原 R275 callable 仍有18 assert，生产不可用；新增 opt-in v2 只做归档复验，未切换任何生产调用 |
| #39 | 05961636 | 可归档；56源身份与既有 R333–R340 有界候选证据 | 旧组合仅含6头且旧 main；本轮不将其当作新组合。候选不等于生产/独立数据/外部复现，也不启动原创熔炼 |

九个 PR 共有 **184 个改变路径，两两交集为0**，与本轮 R132 修复路径也无重叠。完整源码/归档/stream 身份核验详见 pr-dependencies-report.md、pr-native-report.md 及对应 JSON；相同源码的既有独立审查/数学证据复用，未浪费额度重跑旧研究。

明确的新运行时依赖只有 **#30 → 当前 #31**。为了材料完整，建议归档顺序：**30 → 31 → 32 → 33 → 35 → 36 → 37 → 38 → 39**；32/33 先于35便于保留工具上下文，36–38彼此无新增运行依赖。#39引用36的整合审查，但其56源回放并不导入36。

### 实际完整组合

从最新 main 及实际九个固定头建立独立归档组合分支 `integration/r-series-nine-archives-20261117`，组合提交 **a3a76adf8ffba0c0a27fee69aef49cb8588ee2e8** 已推送并回读一致。不是仅依据文本无冲突：

- 当前已提交 HEAD 上 B31 source capture 普通/-O 各22源成功，实际对应 #30 更新后的 pin。
- A33 普通/-O 均保留预期 **exit2 / false / 11 / 35**，没有重跑数学或真人打分。
- #39 普通/-O 56源捕获成功；既有组合数值证据只在源身份未变的限定范围复用。
- #32 当前 prepare 新生成的9448-byte patch 与历史候选完全相同，SHA256 `ed2b03c7985d93db9c915abaa4e3bffeae665803dbd00db8364eba14a62cf44e`；**只生成，未应用、未启用工作流**。
- 七条针对性命令均符合预期退出码，工作区干净；见 combined-verification/result.json。

可由 owner 选择合并这个归档整合 PR **或**按上述顺序处理原九个 PR，**两条路径互斥，不能重复套用相同归档**。组合分支不包含本轮新的 R132 修复；两者改变路径无交集，源码 pin 不受 R132 修复影响，工程修复 PR 可独立审阅/先合并。原九个 PR 本轮不关闭、不改头、不自动标科学通过。

### R275 补充有界处理

对当前 main 的18 assert 实际复现：6类坏文件在普通模式拒绝，但 `-O` 与环境优化下出现 **12次错误 PASS**。这是优化完整性缺陷，不证明历史默认模式的数学结果错误，也不证明历史生产曾被利用。

新增 `r275_archive_gate_v2.py`：先校验原源码及冻结 JSON/CSV 全字节身份，使用同一输入快照，将原18条件在内存转换成显式拒绝，保持全部 Fraction/K-count 数学。**6 个测试方法/43次子进程**通过，包括三模式正向、18次改档身份拒绝、18次独立语义拒绝、原 RED 和源码篡改/缺失控制。公开入口只允许固定归档；私有语义控制绕过的是输入 pin，而非校验条件。旧 checker 未修改，明确 STILL_BLOCKED_FOR_PRODUCTION；无工作流路由或科学等级升级。

## C. 仍然阻塞、并发及费用

- R077 真人资料身份/许可、session映射与准入、历史真人影响未知；不打分、不升级证据。
- R127 正式生产 workflow、实际CI provenance/权限/收费资格和科学重新验收；本地历史60测试证据不替代这些授权。
- R275 旧 callable 的生产路由、S73 协议语言差异、R333–R340正式生产/独立数据资格均保持阻塞。
- R132 v2 工程收据不是正式 CI 重新验收。现存工作流发布路由未改，禁止据此启用生产任务。
- 基准、PR头、main结束前实际回读；分支保存不会覆盖 ChatGPT 的 main/其他 PR 工作。未来若任何 head/source/pin变化，需要针对新版本重新核验，不能拿本报告升级当前状态。
- **新增科研证据/等级变更为0，新增 E2/E3 为0**；新增的是工程负向测试和既有有界数学复验。R073/PESEN/所有冻结协议不变。
- 未购买 credits、未调用计费API、未派发任何CI或启用GPU/付费服务。仅使用现有 Codex 额度和免费工具。账户账单未访问，不声称已核验订阅余额。

## 可复验命令与记录

从仓库根运行（标准库 Python，普通云端 CPU）：

```
python research/engineering_integrity_20261117/run_r132_matrix.py
PYTHONPATH=research/engineering_integrity_20261117 python -m unittest -v test_r275_archive_gate_v2
python research/engineering_integrity_20261117/verify_archive_combination.py --repo /path/to/exact/archive-checkout --output /tmp/new-verification-output
```

后两类仅工程/归档复验；不要执行历史 production publisher 或套用 R127 candidate.patch。`*_as_run.py.txt` 是本轮真实交付命令原文（包括独立分支保存），不是自动测试入口。文件身份总表保留在 ARTIFACT_HASHES.json；最终工程修复提交及 PR URL 在 DELIVERY.json/最终回复中，以 GitHub 回读为准。
