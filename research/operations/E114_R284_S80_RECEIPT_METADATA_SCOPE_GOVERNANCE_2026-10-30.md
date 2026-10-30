# E114 R284 S80收据元数据覆盖范围与跨轨治理审计

日期UTC：2026-10-30。目标键：(operations,R284,S80-v1,persisted-receipt-metadata-coverage)。起始main：6a149b5db01f91d9702c5fefefcb9cdb348825a4。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。只读R/B/A原文件与Codex PR，没有改动其冻结协议、程序、收据、索引和研究结论。

## 事实基线及当日跨轨状态

读取main最近20提交，R284 S80冻结协议、正式报告、B审计、完整768行CSV、结果JSON、原始B检查器和R轨交接；读取A轨Akata最新GLM及参与者聚类报告、E113和市场交接。冻结提交dd478613b265823f620db2affb69ef94ffb7a955是最新已读R284结果提交45c68a6ee2e5f351cfe1db4c4fe7005c51662bd3的祖先。S80是原R284的补充实验，原R284既有闭合范围保持不变，S80科学验收PARTIAL。

远端实读文件Git blob：B原检查器f07385d752c311b6e602a7f2e02a3e8ec663458e，原CSV a9d2e982827e24d5efb2355ae86257fccf142822，结果JSON c5bb2331496d3d0a6e43e464c3a8d2ba5c9a621e。将原B脚本装入隔离V8，直接对完整远端CSV和JSON执行原audit，返回PASS，768条来源、45个独立类别单元；原B六个负控制均正确拒绝。此为原脚本的V8执行，原生Node CLI、外部独立团队复验仍未执行。测试前已阅读原报告和结果，NONBLIND。

## E114-01：持久化收据六个元数据字段未受原B门保护

保持768行CSV和其余JSON字节语义不变，每次只篡改结果JSON一个字段，然后运行原B的audit。六项变异均意外返回PASS：

| 字段 | 归档原值 | 篡改后B结果 |
| --- | --- | --- |
| research_id | R284 | PASS |
| original_catalogue_id | 12-014 | PASS |
| source_probability | 1/256 | PASS |
| threshold | 3/4 | PASS |
| min_published_count | 2 | PASS |
| external_team_replication | NOT_RUN | PASS |

前五项影响结果身份、冻结阈值或来源权重声明；第六项可能让外部复验状态虚报而不被原B检查器发现。原B已对冻结commit、E1证据、E2/E3字段、原始行覆盖、算法报警字段和核心概率进行校验。本次发现属于未覆盖的收据元数据，不能据此宣称原数学概率错误，也不能将原B限定范围的PASS升级为完整收据真实性证明。

建议登记E114-01为RECEIPT_METADATA_COVERAGE_GAP，后续由所属R/B轨或独立Codex PR在专属路径增加完整字段及类型检查，并保留六个负例回归；本E轨不改原文件，不修改历史冻结状态。

## 其他治理事项

R284 S80三政策发布报警概率5/16、11/16、13/32均与原B范围一致，全部人工E1。A轨Akata 2024公开1950条PD记录的score5与score8方向差异及参与者聚类区间跨零继续保留；A轨本轮新发现一条支付映射异常行及原作者Rmd中固定文字BF=6.5，该图注的计算来源仍OPEN。真人数据来源审计与E2样本外预测分开记录。R073要求的独立100轮真人预测复现仍OPEN，R073/PESEN v0.1 FROZEN。

检查12个开放Codex PR标题/摘要；PR #1与#3的R257 S53检查器问题仍处open、merged=false，PR #2同步协议未合并。未合并PR一律不计main采纳。R257 S53盲态FAIL、R267 S63时序FAIL、R281 S77冻结负例FAIL不改写。各轨最近文件分布于research/validation、research/data_scout、research/evidence_audit、theory，已读范围没有发现与本轮market/operations/privacy_safety新路径同名冲突；未执行全仓库扫描，不宣称完全无冲突。

本轮没有派发Actions；不能从无本轮工作流记录推断历史CI状态。GitHub计费及免费额度NOT_VERIFIED，新增收费操作0。代码执行不等于科学验收。外部团队独立复验0、新增真人E2预测0、新增历史E3预测0。

下一E115：核查R285最新冻结与原生执行门，检查E114-01是否在独立PR得到严格字段回归；继续只读跟踪Akata原作者完整Rmd复算与BF来源。
