# A轨 Nay 与 Vorobeychik 2016 多研究汇编真人囚徒困境数据：来源、身份与R073资格审计

日期：2026-10-28。类型：公开数据候选的来源与模式审计。未下载或解析原始行为文件；无新增真人E2预测。

## 实际核验的一级来源

1. Nay JJ 与 Vorobeychik Y，2016，*Predicting Human Cooperation*，PLOS ONE 11(5):e0155656，DOI `10.1371/journal.pone.0155656`，正式文章 https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0155656 。文章声明整合168386次个人决策、30种博弈结构，S2 Appendix为ZIP，完整数据文件名 `all_data.csv`。文章2016年5月12日发表。
2. 公开R包作者代码仓库 https://github.com/JohnNay/datafsm ，固定master commit `c2e55eab12f1a24d3a5b09a9b42aeefff8bc5be4`。文件 `data/NV_games.rda` Git blob `36a961908385a7fe33ba688479b5dfc7b0a6b609`，仓库清单显示761556字节。数据文档 `man/NV_games.Rd` Git blob `be625b217505dd05781f5bd9c12925df673a7ac0`，R源码文档 `R/data.R` Git blob `2a1dc849c34036026f45d1238d586376b876ec5f`。文档声明168386行、51列，来源与PLOS论文一致。二进制RDA正文未在本轮解析，行数属于作者文档声明。
3. 文档中 `data` 字段的来源代码AM、BR、DB、DF、DO、FO、FR、KS分别对应Andreoni & Miller、Bereby-Meyer & Roth、Dal Bo、Dal Bo & Frechette、Duffy & Ochs、Friedman & Oprea、Fudenberg Rand & Dreber、Kunreuther等研究。它们属于历史研究汇编，不能计为一个新的独立真人实验，也可能与本仓库此前已审计的DF2011/FRD2012等数据重叠。

## 字段、时间、独立性与数据泄漏风险

作者文档列出 `period`（博弈内轮次）、`my.decision`（当前本人行动）、`my.decision1`至`my.decision9`、`other.decision1`至`other.decision9`、两方历史收益、`data`、`group`、`delta`、`infin`、`contin`、`risk`、收益矩阵参数等。时间单位为每场博弈内轮次；部分 `contin` 条件为连续时间实验。公开的51列字段说明未列出独立参与者ID、会话ID或明确配对ID。不能仅凭 `group` 推断真实独立实验场次或同一参与者跨场身份。

历史行动与收益字段已经预计算。若按记录随机分割训练/测试，可能将同一场次相邻轮次或相同参与者的信息混入两侧。还需检查 `period`、`group`、`data` 与真实实验原始编号的映射，以及滞后字段是否严格使用当前轮之前的信息。仅有作者字段文档，无法判定是否存在实际泄漏；此处为待验证风险。

原论文在个人预测评价中使用留出30种游戏结构，动态预测使用上一轮的已观察行动；在聚合预测中仅输入留出游戏结构而不使用其行为。两种评价的目标与信息集不同，复算时必须分开。

## 许可、可得性与R073门槛

PLOS文章为CC BY公开发表，S2数据ZIP公开列出。R包DESCRIPTION声明 `MIT + file LICENSE`，代码仓库 `LICENSE.md` 给出MIT条款。不同历史来源的原始数据再分发授权未逐项核验，暂不把软件MIT许可自动扩展至所有源实验数据。

公开元数据可取得，GitHub RDA对象存在，PLOS S2 ZIP公开列出；本轮未实际读取RDA二进制和ZIP内部 `all_data.csv`，因此没有逐行验证真实行为、轮次连续性、身份独立性、缺失、各来源样本数或许可。正式状态 `METADATA_VERIFIED_RAW_UNREAD_REPLICATION_BLOCKED`。

R073冻结协议要求真正独立的真人双人100轮实验、明确场次身份及原评分信息集。该汇编包含不同历史实验，文档没有证明存在可独立识别且完整100轮的固定真人配对场次。当前 `R073_DIRECT_ELIGIBILITY=NO`，不得为了使用这套数据修改R073模型或评分。可作为后续跨实验数据侦察候选；下一步先验证PLOS S2原始ZIP文件内容、实验来源映射、ID、轮次及许可，若仍缺真实独立场次则维持阻塞。

本轮无私有数据、账户注册、付费API、数据采购或收费算力。