# R127 机器收据来源身份闭合审计（2026-11-10）

track: R closure independent audit
subflow: provenance boundary
run_date: 2026-11-10
observed_head: 8673a016060a7c23f53185bce42f125ec25d6b3d
status: PARTIAL
evidence_scope: CI provenance and acceptance integrity; no new E1/E2/E3 evidence
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED; no new paid resources requested

## 读取对象与固定身份

* 工作流：`.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml`，Git blob `4b22f653dc7516bb31ead23e45dcf7f62261d79d`。
* 机器收据：`research/R127/R127_PHASE_A_1990_ORIGINAL_MIN_EFFORT_60_TEST_75117_DEVIATIONS_1296_2X2_CI_ACCEPTANCE.json`，Git blob `55bdf82b9e7869c63d46aa4f76ba6bc672dddecb`。
* 最终状态：`research/R127/R127_FINAL_ACCEPTANCE_STATUS.json`，Git blob `3aa5ed67f4d38f91474352627451e46500cde210`。
* 既有审计：`R127_CI_LOG_TRAILING_OK_FALSE_ACCEPTANCE_2026-11-10.md`，Git blob `78a84c17b58e000cb8ac4691e0a63dddceffc4a4`。
* 历史运行：39348775741；此前日志审计登记测试 checkout commit `9c534a2a0604bf6191ba14393a22ea1ce07a752e`，本轮没有重新下载该运行原始日志。

## 新增独立静态核验

逐行检查当前工作流中的 `receipt={...}` 构造和 `code_test_science_SHA256` 字段，并对照机器收据实际字段。三个SHA256覆盖模型源码、测试文件、科学报告。机器收据未登记 workflow SHA256、checkout commit SHA、Actions run ID、job ID、测试日志SHA256、执行命令指纹。工作流在测试后运行 `git pull --rebase origin main`，再推送结果提交。该流程允许测试时checkout身份、结果提交身份、最终main身份各不相同。三文件摘要相等无法单独证明工作流版本、测试运行身份或日志内容身份相等。

反例边界（静态可构造）：保持模型、测试、报告三个文件字节完全不变，仅改变工作流中的日志验收逻辑。三个 `code_test_science_SHA256` 仍然不变，机器收据中的现有三摘要无法发现该变化。该反例证明收据对工作流身份缺少绑定，不证明历史运行被篡改，也不推翻历史60项通过的日志证据。

另外，当前工作流的测试成功日志解析器和源数据检查均使用 `assert`，与此前两个独立负控报告同一根因范围。此处只引用已有发现，不重复计作新的P0缺陷。

## 有界结论与交接

本轮新增P1来源追溯完整性缺口1项：收据缺少工作流及执行身份绑定。已有历史Actions链接及外部日志可以补充来源身份，不能声称收据自身已经完整闭合。R127保持CLOSED_BOUNDED，05-003保持待核；正式关闭0，新增E1/E2/E3均为0。

建议R主线在下一次经授权且确认无新增费用的修复中，使用优化模式仍有效的显式错误检查；在未来新收据中额外登记 `GITHUB_SHA`、`GITHUB_RUN_ID`、workflow blob或SHA256、日志SHA256和明确的运行命令。保留历史收据原件，采用附加证据记录补足旧运行身份。当前无需触发CI，不应追认旧运行使用未来修复后的检查器。

source_links: https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39348775741 ; https://github.com/edwardsage419/Psychohistory-Research/blob/main/.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml
output_paths: research/coordination/closure/R127_RECEIPT_WORKFLOW_RUN_IDENTITY_GAP_2026-11-10.md
commit_sha: recorded by GitHub submission, if successful
blockers: existing R127 validator fixes owned by R mainline; original historical CI log not independently fetched in this run
next_action: R mainline to bind corrected parser and explicit provenance fields, then itemwise 05-003 bounded closure review
