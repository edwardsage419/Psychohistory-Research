# R272 P0 单入口生产调用候选与独立结构回归审查

track: R+B; subflow: original239 12-002 P0 caller integrity; run_date_utc: 2026-11-02T16:48Z
observed_main: 7523153a8c3c7b841bc4298ae189094aedb06175
target_key: (R+B,R272,2026-10-23 prescore freeze,mandatory production caller)
status: COMPLETE_BOUNDED_CANDIDATE_AND_LOCAL_TESTS / PARTIAL_PRODUCTION / P0_OPEN
evidence_scope: INTERNAL_NONBLIND_ARTIFICIAL_E1_ENGINEERING
ci_status: NOT_RUN; billing_checked: ACCOUNT_BILLING_AND_FREE_QUOTA_NOT_VERIFIED

## 1. 先读当前证据并去重

当前生产工作流 `.github/workflows/r272-exact-train-test-oos-e1.yml` 的 Git blob 为 `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`。它仍在验证前运行原始 `--emit`，使用可被优化模式移除的内联 `assert`，持有 `contents: write` 并包含最多六次 `git push origin HEAD:main` 重试。它没有强制调用新的单入口。E168 已记录这些生产治理风险，故本轮没有重复改动生产 YAML，也没有声称发生过违规推送。

R272 冻结协议 blob `9fbdb0078a58c4a9c0a548643227e30da5731119`，原始生成器 blob `13843eecf2f9f05c19ee5545bdb224f58313f367`，现有单入口候选 blob `f33e4e7e544560d65342a899606311d169e4d122`，三份归档 blob 分别为 `8fbbc73d239765f5c66395af1bcf9cf7a8df1f41`、`db3ca11ae224af52c2caf385c898e24aaa0cc54b`、`85d36858911a7eb79c73c607cddf45ea88852a60`。没有修改任何上述输入。

original239 交叉索引 v7.8 blob `36f24235901172642c46853298aebb421f1a3552`，待核队列 blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`。本轮重新逐行解析：154 项，P0=27、P1=82、P2=45。正式待核净减少 0。

当前 12 个 Codex PR 仍为 open；PR #1/#3 对应 R257 S53，均未合并。未将 PR 证据当作 main 已采纳的验收。R333 至 R340 的复合调用链与 R257 S53 历史盲态失败仍为独立开放目标。

## 2. 本轮新增候选

新增 `research/validation/r272_single_entrypoint_caller_candidate_20261103.yml`，仅作为研究目录内的待审候选，不在 `.github/workflows/` 安装。相较此前多任务、多行 shell 方案，此候选只用一个必要科研步骤执行固定命令：

`python research/validation/r272_single_entrypoint_failclosed_20261102.py --root .`

候选具备只读 `contents: read` 权限，禁止额外 job/step、条件跳过、shell 覆盖、忽略失败及任何自动 `git push`。覆盖原始 R272 目录、冻结协议、ZIP 检查器、只读 wrapper、原生负例、单入口、结构验证器和工作流自身的 push / pull_request 路径触发；Python 3.11/3.12 矩阵。它将实际科研执行交给此前已归档的单入口程序，原生程序仍需在可信完整 checkout 中验证。

新增 `research/validation/r272_single_entrypoint_workflow_contract_20261103.py`，在已有 PyYAML 6.0.3 环境中离线解析候选 YAML，严格核对任务/步骤身份、权限、事件路径、单条命令、矩阵与依赖。兼容 PyYAML YAML 1.1 将 `on` 读成布尔键的行为。源代码不依赖 `assert` 执行正例验证，避免优化模式下误报。

## 3. 实际执行与反例

执行环境：本地 Linux CPython 3.13.5，已有 PyYAML 6.0.3，未安装新依赖。确定性结构测试，无随机种子。

普通、`python -O`、`python -OO` 三种模式均 PASS。每种模式中，真实候选正例通过，12 种不同的 YAML 变异均被拒绝。反例覆盖 job/step `if: false`、提前成功退出、shell 配置覆盖、`continue-on-error`、将完整验收替换为 `--selftest`、仓库写权限、漏掉单入口触发路径、丢失 pull_request、额外 job、移除 checkout、缩减 Python 矩阵。共 12 种独立反例，每种重复运行三种 Python 模式；这些是静态结构反例，绝不等同于 36 次真实 Actions 运行。

本轮构建期间发现验证器初稿曾使用 `assert verify(raw)` 作为正例检查；在归档前改为无条件显式检查，并重新在普通、`-O`、`-OO` 三模式全部通过。这是本轮真实修正的验证器优化敏感问题，初稿没有归档为通过版本。

候选 YAML 本地 SHA256 `bec163d69bbe44fdc79fb1872862e914220ff1d2b60eabd8f8cbdead8883e85d`，Git blob `a84b3d13d7d6bc8da45dc523454d7804520ca79c`。验证器 SHA256 `99f6af19a1eb60eff3a650658d90d3b016ce9071ae8c8c0a2261ed80e85973bb`，Git blob `6f1775282d75b8bd3a4380702a7fbcfeff767da0`。

## 4. 生产关闭条件与未执行范围

候选仅证明一个受限 YAML 结构满足静态调用合同。完整真实仓库原生 `--root .`：NOT_RUN；独立科研检查器三模式的完整 checkout 执行：NOT_RUN；生产工作流采纳：NOT_RUN；Actions：NOT_RUN；历史真实损坏归档被 CI 接受：NOT_ESTABLISHED。生产 P0 继续 OPEN。

生产采用还需要 owner/维护者独立审查、固定工作流和单入口来源身份、核对 checkout/第三方 Actions 供应链、确认 required status check 与触发范围能实际强制覆盖相关变更、完整仓库前像只读和隔离重生成实跑、失败传播反例，以及实际免费 Actions 资格。当前 candidate 依赖的 `actions/checkout@v4` 与 `actions/setup-python@v5` 是标签引用，尚未核验不可变 SHA。安装前必须复核，不以本轮静态 PASS 代替生产批准。

## 5. A 公开数据简查

核对 Fudenberg、Rand、Dreber (2012) 重复囚徒困境数据 `stratEst/data/FRD2012.rda`，Git blob `6b196ca1624081850b41dc2084c762257d59dd8f`，二进制文件 26923 字节。本轮通过 GitHub 连接器读取了 base64 编码文件内容，未解析 RData 记录。官方包文档报告 13126 行、9 字段，包含 `id,game,period,choice,last.choice,last.other`，但没有明确 `session` 列。原论文 Table 1 记录六处理合计 18 场次和 384 名参与者；真实场次映射和配对身份不能从包文档直接恢复。原始论文 DOI `10.1257/aer.102.2.720`；来源版本为 `fdvorak/stratEst` 该固定 Git blob。既有 2026-10-25 侦察已指出此实验与 R075 同源，2026-10-27 版权核验记录指出数据单独标注 CC BY 4.0；本轮不重复宣称新独立实验或新许可发现。

R073 冻结协议要求同处理整场次留出、前两轮自己及对手的已观察行动、共同评分风险集与固定七族模型。FRD2012 包版本缺少显式场次身份，且实验每个 supergame 的轮次长度变化；尚无逐行连续性、缺失、噪声行动语义和场次映射核验。因此 `R073_DIRECT_FROZEN_E3_ELIGIBILITY=NOT_ESTABLISHED`，本轮新增合格独立 E3 数据 0，真人预测评分 0。R073 与 PESEN v0.1 均保持冻结。

公开来源：
* https://github.com/fdvorak/stratEst/blob/master/data/FRD2012.rda
* https://search.r-project.org/CRAN/refmans/stratEst/html/FRD2012.html
* https://economics.yale.edu/sites/default/files/drand-140304.pdf
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/STRATEST_DF2011_FRD2012_DFS2020_PUBLIC_SOURCE_DEDUP_AND_SCHEMA_TRIAGE_2026-10-25.md

## 6. 费用与下一步

没有购买数据、调用收费 API、运行 CI、安装生产 workflow 或向公开仓库上传真人原始数据。GitHub 实际账户账单与免费 Actions 额度未独立核验。下一个高价值任务是可信完整 checkout 上运行固定单入口，并由维护者在确认费用后审查生产调用替换和强制状态检查；不得因候选结构测试 PASS 关闭 R272 P0。