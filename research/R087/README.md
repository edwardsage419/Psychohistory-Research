# R087：另一原作者134真人的十轮条件合作策略变化与不合作迁移（正式结题）

日期2026-10-17。**状态 CLOSED_BOUNDED，证据等级 E2：真实作者原始行为CSV固定Git blob两次独立复算成功，A01–A06已限定验收。** PESEN v0.1继续冻结。

研究来源 Andreozzi, Ploner, Saral (2020), *The stability of conditional cooperation: beliefs alone cannot explain the decline of cooperation in social dilemmas*, *Scientific Reports*, DOI [10.1038/s41598-020-70681-z](https://doi.org/10.1038/s41598-020-70681-z)。作者[完整GitHub仓库](https://github.com/seyhunsaral/stabilitycondcoop) 固定commit `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`，真实作者生成的 `data/csv/subjects.csv` Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`，分析生成 `code/process_raw_data.R` Git blob `522efd459f574ccaef3d9ce1dd2b086ffb70370e`。作者同时公布6原始z-Tree session文件，R087**尚未重新执行R代码对这些原始Excel复清洗**，必须保持此来源边界。

首次真人评分前先提交[预冻结协议](../../protocols/R087_AUTHOR_CONDITIONAL_COOPERATION_134_HUMANS_ORIGINAL_GIT_SOURCE_BEHAVIOR_FREEZE_2026-10-17.md) commit `551cbb044201ffb7e83798118455199d9af68c81`：6个实验场次，134真人（NoCondInfo 68, CondInfo 66），每人10个付费互动期共1340人期记录，固定四策略类别。 C代表条件策略ccL≤ccM≤ccH且ccH>ccL，D代表在对手所有低/中/高行为下均0，F代表无条件固定正合作，O其余非单调/反向；各期非条件uc、实际化action与条件应答是不同概念。

[首次GitHub Actions原作者真实134人run39003772753](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003772753) 先38项synthetic全部PASS，再检验原作者CSV和作者R代码Git blob，真实10期结果执行成功。[第二次独立全源重取、重新评价和永久匿名归档run39003815853](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003815853)再次38项synthetic和全部134人结果PASS，文件**16,647字节 SHA256 `e0663ea1d7829fb1c4ba51b134ca1276e9c16e6e0b3b3d321b343ee66c8e4bbe`**与首次逐字节一致、Git blob `f211736ab095854f5572c4c0673ad3c923fb189e`。

真实结果：期1→期10，**条件合作C 87→46人，完全不合作D 35→79人**；首末个体转移C→D **43人**，逆D→C **4人**，总134人中只有**50人**全部10期从未改变粗类别。实际化行动均值42.5373→17.1642，下降25.3731原始单位；条件高低响应跨度54.1045→24.2537，下降29.8507。两原实验信息处理分别C→D 18/25人、逆D→C均2人，均支持描述性的条件策略类向不合作迁移；但仍是同一论文的两种实验处理，不当作两篇独立原作者E3复验。

完整[科研结题报告](R087_ORIGINAL_134_HUMAN_CONDITIONAL_COOPERATION_STRATEGY_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[机读A01–A06验收](R087_FINAL_ACCEPTANCE_STATUS.json)、[真正原作者1340人期匿名数值](R087_FIRST_PARTY_134_HUMAN_10_PERIOD_CONDITIONAL_STRATEGY_TRANSITIONS_E2_RESULTS.json)、[复算程序](r087_author_134_human_10_period_conditional_strategy_E2.py)、[38项synthetic](test_r087_author_134_human_10_period_conditional_strategy_E2.py)均已归档。**本次不识别信念不起作用或实验信息处理的因果效应，也不证明真实群体制度/长期历史演化。** 原本已经发表的论文结论不能作为我方2026年新模型独立发现，不上传原作者真人逐行决策或ID。
