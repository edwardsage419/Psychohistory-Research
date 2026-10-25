# E005 科研项目治理差量：R166 事后计数勘误与 R073 来源独立性排除

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E
status: COMPLETE_BOUNDED_READONLY_DELTA
observed_main_head_before_write: 360e9999e5ba360aed90011493e9bed2510f537c
ci_status: NOT_RUN_BY_THIS_AUDIT
cost: 仅免费 GitHub 只读审计，无主动新增费用；账户账单与 Actions 免费额度未独立核验

## 去重和只读边界

当日正式 E004 已完成 R165、C003、D002 的实质审计。本差量只审阅 E004 后的 R166 新科学报告、B 独立方法报告、两份 B 运行收据、R166 事后算术勘误、A 轨 R073 原始实验身份排除，以及本轮 MKT036 新报告。没有改写 R、A、B、C、D、TH、F 研究文件、冻结协议或共享索引。

## 1. R166 事后勘误的验收边界

冻结提交 `5704ad07c3c61ffe7293ec8c97f4521727989853` 先于执行。冻结协议将 (5+9)*2 误写为 56，实际为 28。项目归档的更正说明明确报告首次 JS 运行断言失败，并在执行后将计数修正为 28；原冻结协议未被覆盖。首次失败的独立原始终端输出本次未取得，不能声称已核实原始失败日志字节。

R166 科学报告和 B 审计记录最终 28 个非中性条件，8 个观测分布完全相同、20 个可区分，另有 14 个中性对照；84 行原始矩阵核对及一组变异负对照。B 的另一条累计分布阈值算法归档 28 项 TV 结果，与穷举结果一致。已直接读取对应 CDF 收据，其中 exact_cases_verified=28、zero_gap_cases=8、nonzero_gap_cases=20、remote_ci=NOT_RUN。冻结原始 R166_EXACT_RESULTS.json 当前 Git blob `998c80ccb4398d65424bbfccfa6d36c51696a9da`，与两份报告所指对象一致。

治理结论：`PASS_BOUNDED_INTERNAL_E1_WITH_DISCLOSED_POSTEXEC_ARITHMETIC_AMENDMENT`。应始终同时引用原冻结与勘误，避免将事后修正追溯为事前正确。独立 B 方法共享同一项目原始人工核，属于内部交叉核查；真人 E2、历史 E3 和外部团队复现均为 0。归档修正版 Python 程序未运行，不能记作 Python 实际复现。

## 2. CI 真实性

直接查询 GitHub Actions REST 对科学报告提交 `b86b6fdaadfe448186d6a20acbbd0bac904e9412` 与 B 审计提交 `24b667b95a8e94902ab0bc8079830996ed61e0c5` 的 head_sha，均返回 total_count=0。此结果只覆盖两项指定提交，不能推断仓库所有历史 CI 状态。新增算法远端 CI 验收保持 NOT_VERIFIED。无主动触发 CI。

## 3. R073 第二独立真人实验的来源排除

A 轨新增文件 `research/data_scout/MONTERO_2022_R073_ORIGINAL_SOURCE_IDENTITY_HARD_EXCLUSION_2026-10-26.md` 直接比对原 R073 使用的 Montero-Porras 等 2022 Scientific Reports DOI `10.1038/s41598-022-11654-2` 与 Dryad `10.5061/dryad.37pvmcvmk` 的论文身份，判定为同一项原始实验。Dryad 与作者 Git CSV 的字节一致性仍未证实；即使字节不同也不能据此视为第二项独立实验。A 轨未下载新人级数据或完成新评分。治理状态：SECOND_INDEPENDENT_R073_EXPERIMENT=NO；新增外部 E2=0。

## 4. 并发、证据与费用问题队列

E005-01 HIGH：R166 首次失败有透明文字记录，但原始失败输出未在本轮独立取得；引用时保留事后修订标签。
E005-02 HIGH：R073 仍缺不同受试者来源的第二独立真人重复博弈数据集，禁止把 Dryad 同一实验重新计数。
E005-03 HIGH：R136 原冻结负对照失败仍开放，后续纠正性通过不能改写原结果；完整 CSV 字节尚待核验。
E005-04 MEDIUM：original239 154 项逐项证据审计待办继续开放，v7.8 元数据滞后由原责任轨处理。
E005-05 MEDIUM：R166 新方法指定提交无 Actions 运行，科学等级仅内部 E1。
E005-06 MEDIUM：MKT036 新增 WAL 单文件备份失真合成反例及旧记忆恢复风险；市场报告是独立知识储备，不能上升为真实产品已发生事故或个人决策效果证据。

本轮没有发现需要跨轨直接改写的授权，未扫描全仓全部冻结文件哈希，也未核验账户整体计费记录。归档与科研证据分别登记。

## F 当周状态及下一项

2026-W44 的 F002 已归档授权撤销、衍生数据、备份生命周期专题；本轮不重复建 F 专题。将 MKT036 的 WAL 快照一致性和旧备份记忆恢复纳入后续候选负对照清单。下一次 E 重点检查 R167 及其新提交、R136 完整 CSV、R073 新候选来源的独立性和 original239 待办。

研究顺序不变：先完成全部 R 系列，再系统归纳分类，最后模型熔炼。绝对零主动新增费用。

## 原始仓库文件

https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R166_ONE_STEP_COUNT_IDENTIFIABILITY_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R166_TWO_ROUTE_IDENTIFIABILITY_SCIENTIFIC_AUDIT_2026-10-26.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R166_ONE_STEP_COUNT_IDENTIFIABILITY_ARITHMETIC_CORRECTION_2026-10-26.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R166_CDF_THRESHOLD_EXECUTION_RECEIPT_2026-10-26.json
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/MONTERO_2022_R073_ORIGINAL_SOURCE_IDENTITY_HARD_EXCLUSION_2026-10-26.md
