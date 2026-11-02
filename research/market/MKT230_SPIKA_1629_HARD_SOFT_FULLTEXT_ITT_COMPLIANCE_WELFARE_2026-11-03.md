# MKT230：承诺合同完整工作论文审阅，随机提供、实际押金与目标完成的分离

track: market
subflow: commercial_product_research + E_daily_readonly + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (market,Beeminder-vs-Spika-gym-contract,2023-working-paper-fulltext+2024-published-abstract,offer-ITT-vs-actual-stakes-compliance-and-goal-welfare)
baseline_main_before_write: 3fd5a56348214fb53e63ee79cef3ca33fc572f7d
prior_related: research/market/MKT229_BEEMINDER_GOAL_ROAD_COMMITMENT_GYM_RCT_EXTERNAL_VALIDITY_2026-11-03.md
status: COMPLETE_BOUNDED_ORIGINAL_WORKING_PAPER_TABLE_AUDIT
source_scope: 2023 Lund University 82-page working-paper text, Table 1/Table 3, design, results and discussion; 2024 journal abstract independently checked
evidence_grade: MARKET-E2_EXTERNAL_HUMAN_RCT_PUBLISHED_ABSTRACT_PLUS_AUTHOR_WORKING_PAPER_TABLES
Beeminder_product_causal_effect: NOT_VERIFIED
published_2024_final_tables: NOT_VERIFIED
preregistration_record_direct_read: BLOCKED
participant_level_reanalysis: NOT_RUN
new_R_E2_E3: 0
CI: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 一、为什么继续审阅同一研究

MKT229已取得2024年正式发表摘要并记录21%与8%的相对到访变化，但明确留下原始回归表、随机分组、实际支付、退出与长期福利缺口。本轮从德国EconStor公开英文原文取得2023年Lund大学完整工作论文的表格及实验细节。研究目标是纠正“硬合同随机组效果等于押金本身的效果”的潜在混淆，不重新制造Beeminder产品机制编号，也不将2023工作论文表格冒充2024最终出版版表格。

## 二、设计与真正执行的处理

实验在2018至2019年瑞典斯德哥尔摩健身房进行，随机分配1629名现有会员：对照524、软合同提供573、硬合同提供532。软合同可自行设定1至4个月、每月4至24次以上的健身目标。硬合同组获得相同合同设计机会，额外可选择押金，未达标的押金转赠所选慈善机构。合同开始和结束时有邮件通知，合同期间没有持续进度提醒。实际健身次数来自健身房到访记录，实验观察八个月。

Table 1给出软组接受合同487/573=85.0%，硬组接受合同439/532=82.5%。硬组接受押金邀请179/439=40.8%，相对硬组全体179/532=33.6%。工作论文敏感性章节披露61名接受押金者没有完成手机转账，因此实际转账约118/532=22.2%硬组全体，或118/179=65.9%押金接受者。上述后两项为根据公开整数计算的描述性比例，不是独立核验的支付记录。硬组随机化识别的是“提供可选押金合同”的意向处理效应，不能识别押金本身的纯因果效应；接受合同、选择押金及完成转账均发生在随机化之后。

## 三、Table 3的结果口径核查

| 指标 | 软合同提供组相对对照 | 硬合同提供组相对对照 | 证据口径 |
| --- | ---: | ---: | --- |
| 第1至4个月每月到访次数 | +0.460 | +1.140 | Table 3 Panel A ITT，控制组5.500次 |
| 第1至4个月相对控制组 | +8.36% | +20.73% | 本轮用上行整数和5.500独立除法，约等于摘要8%与21% |
| 第1至4个月达到原基线月目标的概率 | +3.72个百分点 | +9.66个百分点 | Table 3 Panel A，控制组10.7% |
| 第5至8个月每月到访次数 | +0.213 | +0.471 | Table 3 Panel A，控制组5.141次 |
| 实际接受合同者达成合同目标 | 15.0% | 19.6% | 条件于接受合同，差4.6个百分点，作者报告p=0.065 |

工作论文正文给出硬组前四个月到访p<0.001，软组p=0.085；后四个月硬组p=0.082。软组前四个月的到访增量在加入控制变量后不再显著。硬组与软组各自对照组的显著性，不能自动证明两处理组之间差异显著。作者关于合同目标达成率的直接组间比较p=0.065，未达到双侧5%阈值。论文表格使用按人聚类稳健标准误。原始参与者级数据和回归代码本轮没有执行。

## 四、风险与外推边界

1. **遵约率与押金因果性**：硬组约五分之一完成真实押金转账，却报告约21%的到访相对提升。不能由此推断“只需押金即可提升21%”；目标设定、合同显著性、选择偏差和其他行为渠道都可能参与。
2. **目标与福利**：合同接受者的目标达成率分别只有15.0%和19.6%。实际增加健身房到访次数不等于健康净福利提升，尤其押金损失、其他运动替代和心理负担未完整计价。论文讨论提到硬组随访期间其他场所运动自报较低，存在行为替代可能。
3. **持续性**：第5至8个月硬组相对对照增加0.471次/月，约为前四个月增量的41.3%，且p=0.082。不能称为确认性的长期稳定效果。
4. **随访选择**：问卷随访率对照90.5%、软组85.5%、硬组83.8%，组间p=0.005。主要到访结果使用健身房记录，问卷衍生的健康和其他运动结果应额外审查选择偏差。
5. **原始预注册**：工作论文注明AEARCTR-0001966，原计划在Uppsala招募，因仅招到184人改为Stockholm，后者1629人。注册全文及版本历史本轮访问失败，变更的事前性和最终分析计划一致性保持UNKNOWN。
6. **发表版本**：2024年正式论文摘要确认1629人及21%和8%，完整最终回归表格未取得；2023年Table 3的具体标准误和p值不应标记为已独立核对2024最终版。
7. **商业外推**：该实验的押金转赠慈善机构，Beeminder则按其实际服务规则收取违约款，目标、数据来源、费用上限、错误申诉与人群均不同。实验不能证明Beeminder本身有同样的效果。

## 五、E每日只读审查及F本周状态

E168已于本地2026-11-03完成实质审计，故本轮只读。当前查询main HEAD为3fd5a56348214fb53e63ee79cef3ca33fc572f7d，main分支API protected=false。原239待核CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，经本轮按行重新计数154项，P0 27、P1 82、P2 45；crosswalk blob 36f24235901172642c46853298aebb421f1a3552，与前轮相同，文件级净减少0。12个开放Codex PR逐一检索，重点#1/#2/#3/#8/#9/#12已回读状态，均为Draft、merged=false。PR#3相对当前main独有1提交，main独有1210提交；此比较是GitHub元数据，未做完整PR代码验收。R272生产完整性P0与R333至R340生产组合门均无新关闭证据，未修改工作流或冻结协议。

R/B最新R074/R075报告只对既有真人E3匿名宏结果进行112项内部算术复核，新增E3为0；此前已有的R074/R075有限E3归档必须保留，不能说项目历史E3为0。R073与PESEN v0.1继续冻结。

F010本周价值权重、人类决定权及数据生命周期专题已经完成。本轮仅增加真实押金承诺产品的经济后果提醒：必须分别衡量签约、押金授权、实际支付、违约、申诉与撤销；不读取用户个人数据，不新增F编号，实际安全部署NOT_RUN。

## 六、来源、费用、下一步

- 2023完整英文工作论文（Lund University Working Paper 2023:4，经EconStor公开存档）：https://www.econstor.eu/bitstream/10419/298486/1/1845110331.pdf
- Lund大学官方原始研究登记及全文入口：https://www.lusem.lu.se/ulf-gerdtham/publication/fdf4c5f0-dfee-4bea-ba81-565c5145852b
- 2024正式发表版PubMed摘要，DOI 10.1016/j.jhealeco.2024.102943：https://pubmed.ncbi.nlm.nih.gov/39571470/
- 预注册号：AEARCTR-0001966；本轮原始登记直接读取BLOCKED。
- 仓库R/B独立治理来源：research/validation/R272_P0_UNPROTECTED_MAIN_TRIGGER_AND_FREEZE_COMPAT_AUDIT_20261102T1740Z.md；research/validation/R074_R075_ARCHIVED_E3_AGGREGATE_CONSISTENCY_REAUDIT_20261102T1845Z.md。

本轮所有研究来自公开资料和整数算术核对；未下载或提交个人级原始数据，未注册收费产品，未触发Actions。账户账单及剩余额度NOT_VERIFIED。下轮优先获取2024正式全文或预注册版本历史；若仍不可取得，转向另一种无需经济惩罚的目标反馈产品，避免重复MKT229/230。R科研始终优先，现阶段不开发个人决策产品。
