# R074/R075 既有真人 E3 匿名宏结果的独立算术复核及后续队列纠偏

track: R+B
subflow: archived-real-human-E3-independent-aggregate-arithmetic
run_date_utc: 2026-11-02T18:45:23Z
observed_main_before_write: d4f1c9f626ada3d28aff4413eab2c03f35b15023
target_key: (R+B,R074+R075,2026-10-17-original-frozen-transfer-protocols,archived-E3-aggregate-consistency-and-existing-external-replication-status)
status: COMPLETE_BOUNDED_ARCHIVED_AGGREGATE_ARITHMETIC; FULL_SCIENTIFIC_REVALIDATION=PARTIAL
evidence_grade: EXISTING_R074_R075_HUMAN_E3_ARCHIVES_READ_ONLY; NEW_E3=0; NONBLIND_INTERNAL_AGGREGATE_RECHECK
ci_status: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
new_chargeable_actions: NONE
random_seed: N/A
execution_environment: ChatGPT tool V8 JavaScript Number arithmetic, deterministic
source_scope: main GitHub connector exact file reads; English original publisher and stratEst source descriptions; no participant-level raw files downloaded
source_git_blobs:
  R074_result: c10edcc19526278aac6be6811b5cab00e24d7b20
  R075_result: 50e3cbef9184ea36cd5edb5e3fe7abae40dd19e6
  R074_README: e2a33ac82193e7769bbe4cac8909f6807d76d4e3
  R075_README: a8817a226179c8a9e724df35eda6f7dee1d8dd4e
  R075_freeze: ffaa9253360bb88d4811f3a61cf1ef60ed4a6949
  R075_acceptance: 1241ad79fd1f19195eb591ce60b56668ead8cd76

## 已实际执行的独立算术审计

直接读取并 JSON 解析上述两份匿名宏结果，不导入 R073/R074/R075 模型或计分实现。对每项研究分别遍历7个冻结模型、6个处理组和6项预定模型配对比较。独立使用每处理原始场次数加权重构18场等权宏 Brier 与 log loss；用两模型的处理组均值差重算处理组 Brier 差；用两个模型的18场等权 Brier 差重算整体配对差；核查每组胜、负、平场数之和等于场次数及全局场数汇总。全部采用浮点运算，比较容差2e-12，实际最大绝对差R074为4.44e-16、R075为2.22e-16。每研究14个模型宏评分核验、6个整体配对差核验、36个处理组配对差核验，共56项核心数值比较，两研究合计112项，全部PASS；另行检查每研究7模型、6处理、18场及胜负计数。

| 已归档真人研究 | 宏结果 Git blob | M3减M1 Brier，胜场 | M4减M3 Brier，胜场 |
| --- | --- | --- | --- |
| R074 Dal Bó/Frechette 2011，第二作者来源 | c10edcc19526278aac6be6811b5cab00e24d7b20 | -0.022915328373344184，16/18 | +0.003170501040435799，5/18 |
| R075 Fudenberg/Rand/Dreber 2012，第三作者来源 | 50e3cbef9184ea36cd5edb5e3fe7abae40dd19e6 | -0.029117355804310772，18/18 | -0.012416864447856633，15/18 |

M3比M1低Brier的方向在这两项独立作者真人实验已归档复现。更长的两轮联合历史M4增益跨实验方向不稳定，R074恶化，R075改善；R075零实施噪声组的3场又全部恶化。保留上述负结果。R075与R073目标动作语义不同：R075预测当轮意向，过去历史取已执行可观察动作。R075参数零样本跨实验迁移NOT_TESTED，跨场次真实人是否重新参加UNKNOWN，因果记忆机制NOT_IDENTIFIED。

## 研究状态纠偏及限制

R073原始研究本身为内部E2、E3开放；后续R074和R075已在2026-10-17归档各自的有界真人E3结构转移复验及匿名结果。不能继续将“尚未找到第二独立真人实验”作为当前未完成事实。未来可探索第四项独立来源、R075源与AEA存档的字节同一性、或者先冻结零样本迁移协议；这些均未在本轮完成。原始R074/R075历史验收保留，原协议未变。

本轮的112项检查仅验证匿名宏结果内部的加权与差值一致性。无法从宏结果恢复个人级动作、会话配对、时间泄漏、模型真实执行、来源身份或独立团队盲态验收。既有真人E3来源事实来自项目冻结协议、原始README和验收收据的远端阅读；本轮没有重新执行真人数据评分。不能将本轮宏结果算术PASS提升为新的E3、外部团队复现或完整科学结题。

A数据简查：AEA原刊DOI 10.1257/aer.102.2.720 的 replication package 和 stratEst 的 FRD2012（13,126行，含id/game/period/last.choice/last.other）可供来源资格研究。该整理数据对应已完成R075的同一原作者实验，不可重复登记为新独立实验；其版本与R075共同作者ZIP的字节等价仍UNKNOWN。未下载、解码或对真人评分。来源 https://pubs.aeaweb.org/doi/10.1257/aer.102.2.720 和 https://search.r-project.org/CRAN/refmans/stratEst/html/data.FRD2012.html 。

original239：读取v7.8既有交叉索引blob 36f24235901172642c46853298aebb421f1a3552 与实际待核CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，154项（P0=27、P1=82、P2=45），正式队列净减少0；不更改治理状态。开放Codex PR #1/#3 的R257 S53仅为未合并候选；R272生产P0仍开放，不能以本次R074/R075算术复核抵消。最新R272正式工作流blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d 仍有预验收生成与自动写回风险，候选工作流仍未正式采用。未执行CI，未核实账户账单及Actions剩余额度。

下一步优先级：R272真实完整检出的单入口原生执行、冻结三job兼容性与生产强制调用独立验收；如完整检出仍受阻，转向original239待核P0/P1的真实来源逐项审查。后续A工作只为真正新增独立来源或尚未解决的原作者字节/身份问题投入时间。R073/PESEN v0.1继续冻结，暂不统一分类或熔炼。
