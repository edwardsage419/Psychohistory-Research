# A 公开数据资格核查：Mao 等 2017 长期重复囚徒困境与 R073 冻结单位冲突

track: R+A+B
subflow: 公开数据原始设计核查、R073 冻结协议逐条适配性复核
run_date_utc: 2026-11-01
observed_main_before_write: dbbde2b4efc5cced43ddf542d70fc45ab1fa74ba
target_key: (A,Mao-Dworkin-Suri-Watts-2017-ncomms13800,R073-2026-10-17-frozen,external-data-unit-and-split-eligibility)
status: COMPLETE_BOUNDED_PRIMARY_DESIGN_GATE / RAW_DATA_ACCESS_BLOCKED
source_obtained: PAPER_FULL_TEXT_AND_PUBLIC_CODE_REPO_METADATA_ONLY
raw_data_obtained: NO
frozen_R073_direct_score_eligible: NO_UNDER_UNCHANGED_SESSION_AND_TIME_RULES
independent_new_E2_scoring: NOT_RUN
R073_protocol_changed: NO
PESEN_v0_1: FROZEN
CI: NOT_RUN
billing_checked: NOT_VERIFIED
new_paid_operations: NONE
new_E2_E3: 0
output_path: research/data_scout/A_MAO_DWORKIN_SURI_WATTS_2017_R073_FROZEN_UNIT_GATE_20261101T1845Z.md

## 研究问题与已读原始证据

前轮仅发现 Mao, Dworkin, Suri & Watts (2017) 长期真人重复博弈及 OSF 数据链接。本轮直接阅读原始英文公开论文的 Experimental design、Methods、Data availability，并与 R073 冻结协议逐项对照。

* Mao et al. (2017), *Nature Communications* 8:13800, DOI https://doi.org/10.1038/ncomms13800 ; 免费原始全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC5241863/ 。
* 原作者声明原始数据在 https://osf.io/64z8u/ 。本轮该页面访问返回 HTTP 403；未取得数据文件、字段字典、校验哈希或数据集独立许可。
* 作者实验代码仓库 https://github.com/TurkServer/long-run-cooperation ，公开 master 最新检索提交 `4d8ed83e7745e1ffe82ce9403064e3558fabfa6f`。仅核对仓库存在及其 README 描述，未执行作者代码，未将当前 HEAD 冒充 2015 年实验时使用的版本。
* R073 冻结协议 `protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md`，Git blob `2f910c92436927f1488510af4ca98b665fa0d123`；正式状态 `research/R073/R073_FINAL_ACCEPTANCE_STATUS.json`，Git blob `4dcd30a7b47cc0f81ff186541d791474a3e2e0e9`。
* 本轮起始 original239 交叉索引 v7.8 Git blob `36f24235901172642c46853298aebb421f1a3552`；实际待核 CSV Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`，154 项，其中 P0 27、P1 82、P2 45。只读，无队列变更。

## 从论文可直接确认的单位与时间语义

研究在 2015 年 8 月 4 日至 31 日的 20 个工作日进行。最初 113 名参加者，满足完成标准的为 94 人。参与者被分入每天 13:00 与 15:00 两个实验时段，原论文称分组在实验开始时随机分配并在整个实验中保持不变。每个工作日有 20 场十轮重复囚徒困境，**每场结束后重新随机配对**，每轮双方可见上一轮对手选择。最多约 400 场十轮博弈；原文报告完成者总计 374251 次个人决策。

因此，时间轴应区分 `cohort/session`、`day`、`game/supergame`、`round within game`、`participant` 和 `opponent within game`。20 天是同一批人的重复观察，400 场不是 400 个独立招募实验，十轮一场后重新配对。论文说明两个初始实验时段为固定人群；尚未读取原始文件，无法核验匿名参与者及对手键在 OSF 数据中的实际编码。

## R073 冻结适配逐项判定

| 冻结条件 | R073 已冻结要求 | Mao 2017 原文已确认事实 | 本轮判定 |
| --- | --- | --- | --- |
| 时间单位 | 同一人连续 100 轮；每人共同计分 t3 至 t100 | 400 场各十轮，每场后重配对 | FAIL_UNCHANGED |
| 训练和留出 | 12 个原实验场次，固定与打乱处理各 6 场；每折同处理其余 5 场训练 | 两个固定参与者时段，跨 20 天重复 | FAIL_UNCHANGED |
| 对手语义 | FP 同一对手连续 100 轮；SP 逐轮换对手 | 每十轮结束换对手；场内保持配对 | DIFFERENT_TREATMENT |
| 预定模型与评分 | M0 至 M6 七族，alpha=20，整场等权 Brier/log loss，18424 个共同目标 | 本轮未取得原始行为字段或可计算的合法目标数 | NOT_RUN |
| 数据独立性 | 新原始实验，需与 R073、R074 等来源去重 | 2015 年另一作者实验；精确数据身份和重复登记未完成 | PROVISIONAL |
| 文件再利用 | 实际原始数据、身份字段、哈希、许可可审计 | OSF 公开链接已确认，页面本轮 HTTP 403 | BLOCKED |

**裁定：现有论文设计已足以排除“按 R073 原冻结分割、时间风险集和处理规则直接评分”的资格。** 不必等待 OSF 文件下载后才做这项排除。该研究仍是有价值的独立纵向真人行为候选；未来若采用它，应另行先冻结不同的研究问题、训练和留出单位、配对语义及评分计划，不能将改动后的实验计为 R073 冻结模型原样跨实验复现。

若研究跨天变化，必须按固定人群重复测量处理；仅按天或按 supergame 留出，会在训练和测试中重复出现相同参与者。若按两初始时段留出，只有两个高层独立组，无法照搬 R073 的 12 折同处理五场训练设计。没有原始文件前不对缺失率、可识别键、许可证或预测可执行性作肯定声明。

## 科研审计与限制

本轮是原始论文和冻结协议的**设计级资格裁定**，属于 B 方法复核与 A 数据侦察。未下载原始行为、未运行 R073 代码、未训练或评估模型、未接触个人数据。无新增 E1 数学实验、真人 E2 预测、历史 E3 或外部团队复现。现有 R073 与 PESEN v0.1 冻结状态保持不变。

下一步优先处理 R333 至 R340 的真实复合验收与正式调用路径 P0；若该仓库完整检出仍不可得，转向 original239 的其他 P0 逐项科学验收。对本数据仅在可获得 OSF 原始文件且存在明确新的预冻结科研问题时继续深挖，避免重复登记成 R073 合格来源。
