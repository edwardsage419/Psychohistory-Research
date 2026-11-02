# E168: R272 生产工作流写权限与验收调用风险只读审计

track: operations
subflow: E_daily_readonly_governance
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (operations,R272-active-workflow,blob-3132b08c,preimage-acceptance-gate-adoption+automatic-main-write-authority)
observed_main_before_write: 77f10eb3ea5341dd8f000878eda95020b5ac75c5
status: COMPLETE_BOUNDED_STATIC_SOURCE_REVIEW
formal_P0_closure: OPEN
new_math_replay_or_fault_injection: NOT_RUN
native_complete_checkout: NOT_RUN
CI_dispatch: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE
personal_data: NOT_ACCESSED

## 一、此次实际读取与新增治理发现

直接读取当前 main 的 `.github/workflows/r272-exact-train-test-oos-e1.yml`，Git blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`；候选 `research/validation/r272_single_entrypoint_failclosed_20261102.py`，Git blob `f33e4e7e544560d65342a899606311d169e4d122`；R/B 报告 `R272_P0_SINGLE_ENTRYPOINT_FAILCLOSED_CANDIDATE_REVIEW_20261102T1542Z.md`，Git blob `1dc313d4f69aeba16ad41252ee20f55c25c770b4`。原冻结协议与科学结果未修改。

静态确认当前生产 YAML 存在四项组合风险：
1. `permissions: contents: write`，即该 workflow 的 token 被授予仓库内容写权限。
2. `independent-sources-and-archive` job 首先执行原生成器 `--emit`，随后才通过内联 Python `assert` 检查 CSV、JSON、收据。对已归档前像的验证顺序仍可能被重新生成掩盖；Python 优化模式下 `assert` 语义亦不满足 fail-closed 要求。
3. job 末尾存在 `git commit`、`git fetch origin main`、`git rebase origin/main`、`git push origin HEAD:main` 的自动归档路径，最多六次尝试。这意味着一旦工作流实际运行且满足相应条件，它有尝试修改 main 的能力；是否成功取决于 token 权限、分支规则及运行时条件，本轮未执行，不能声称已发生自动写入。
4. `push.paths` 只列原 R272 Python 和 YAML 自身，未覆盖新单入口候选及其依赖文件。生产 YAML 也未调用 `r272_single_entrypoint_failclosed_20261102.py --root .`。

这些事实使 R272 既有 P0 保持 OPEN。新增治理重点是：生产工作流拥有主动写回 main 的能力，与本项目 owner 对 Git 写操作和不自动触发潜在收费 Actions 的授权边界存在需要审查的冲突风险。**这是静态能力与权限风险，不是已发生违规推送或实际 CI 假阳性证据。**

## 二、候选单入口范围

候选程序使用标准库、`subprocess.run(shell=False)`、固定来源 Git blob、ZIP SHA256、归档前像校验、普通/-O/-OO 三种模式和真实负例程序调用。候选源码还会在每轮执行后检查原归档字节不变。该设计减少 shell 早退绕过空间。

R/B 仅报告本地自检：三模式各五项人工拒绝，共15项；完整可信 checkout、原始83项测试和原生负例组合执行仍 NOT_RUN。生产工作流未采纳候选，不能从 main 存在候选脚本推断已经受保护。候选脚本本身的生产调用来源身份也需要在 workflow 层固定和审查。

## 三、PR、队列和跨轨核对

本轮逐一读取 PR #1 至 #12 的状态：12 open、12 Draft、12 merged=false。PR #3 仍是 R257 S53 的非盲态数学门候选，head `97d5f74df5d84916917db943156120f08144f445`；对本轮 main 的比较为 diverged，main 独有1198提交、PR 独有1提交；`mergeable=true` 只是 GitHub 元数据，不能替代来源、冻结协议与盲态验收。PR #8 和 #9 属 R170，同样未合并，#9 旨在弥补 #8 的历史字节身份强制拒绝缺口。R272、R257、R170 分别保留目标键。

original239 待核 CSV blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`、crosswalk blob `36f24235901172642c46853298aebb421f1a3552` 均与 E167 一致，文件级净变化 0。154项/P0 27/P1 82/P2 45是此冻结队列版本的历史分布，本轮未完整逐行重算。R333至R340 八工作流组合强制调用上轮静态证据为0/8，本轮未发现关闭证据，完整 native 仍 NOT_RUN。理论 TH214/C011 交接只构成理论与测量研究，不能提升 R E2/E3。R073 与 PESEN v0.1 保持冻结。

本轮 main `77f10eb3ea5341dd8f000878eda95020b5ac75c5` 的 combined status 返回 0 条，PR-triggered workflow runs 返回 0 条。该接口不穷尽所有 Actions 触发类型。实际账户账单和免费额度未取得，不触发 CI。

## 四、owner 与 R/B 下一步

建议 R 主线及 owner 优先审查 R272 生产 workflow 的 `contents: write` 和自动 `git push`，将验证和归档写入权限分离，任何改动保留单独审查与授权。R/B 先在可信完整 checkout 运行固定候选、保存三模式 stdout/stderr、原生负例与字节身份，再提出具备固定来源、完整触发覆盖和失败传播的生产强制调用变更。E 只核对证据与依赖，不代替 B 复算，不修改 YAML，不触发 Actions，不自动合并 PR。该报告同时作为 R 主线可读取的 P0 风险通知记录；无额外跨轨写入。

source_paths:
* .github/workflows/r272-exact-train-test-oos-e1.yml
* research/validation/r272_single_entrypoint_failclosed_20261102.py
* research/validation/R272_P0_SINGLE_ENTRYPOINT_FAILCLOSED_CANDIDATE_REVIEW_20261102T1542Z.md
* docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv
* docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json
* https://github.com/edwardsage419/Psychohistory-Research/pull/3
* https://github.com/edwardsage419/Psychohistory-Research/pull/8
* https://github.com/edwardsage419/Psychohistory-Research/pull/9
