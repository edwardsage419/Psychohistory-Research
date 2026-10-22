# R227 经典测验理论：八人工双项目测量世界、128完整单次来源与1024独立重复施测配对

日期2026-10-23（台北时间）。对应原239目录 `10-001 Classical Test Theory`（P1）。科研状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_CLASSICAL_TEST_THEORY**。研究检验经典真分数、跨项目共享误差、α及真正跨次信度之间的有限数学差异。无真人测验数据，新增真人E2=0，真实历史E3=0。

## 第一手依据与实际核阅范围

Melvin R. Novick (1965), [*The Axioms and Principal Results of Classical Test Theory*](https://www.ets.org/research/policy_research_reports/publications/report/1965/hpeu.html), ETS Research Bulletin RB-65-02，及其1966年期刊版[DOI](https://doi.org/10.1016/0022-2496(66)90002-2)，出版社与ETS的一手摘要明确涉及经典真分数、独立测量、平行测验和误差分布要求。Lee Cronbach (1951), [*Coefficient Alpha and the Internal Structure of Tests*](https://doi.org/10.1007/BF02310555), *Psychometrika* 16(3):297–334，出版方及ETS条目确认α公式与项目结构背景；Raykov及合作者[关于误差相关条件的讨论](https://pmc.ncbi.nlm.nih.gov/articles/PMC5965613/)为方法界限参考。本文不声称完整读取、复算上述原作者全部全文中的推导或取得其人级实验记录。

## 冻结协议、人工来源与识别定义

先独立提交[事前冻结协议](../../protocols/R227_CTT_8_WORLDS_128_SINGLE_AND_1024_RETEST_PRESCORE_FREEZE_2026-10-23.md)，其commit为[176e057b](https://github.com/edwardsage419/Psychohistory-Research/commit/176e057bcc121a66633181d6e184b12019ca6e32)，之后提交计算程序及CI。每个世界均有固定二元稳定T及当次独立E1/E2/M共16完整等概率外生源。每次测验生成两项X和Y，总分S=X+Y。测验真总分严格定为`q_S(T)=E[S|T]`，真总分信度`Var(q_S(T))/Var(S)`。**每次新施测重抽E1/E2/M，但保留同一个受试者T**，因此另有每世界128条真实人工跨次源配对，供完整 `Cov(S_time1,S_time2)/Var(S)` 验证。

八世界单次来源共128，独立跨次原配对共1024。128与1024是完整人工枚举的可能性数目，不能解释为1152名真实被试或独立真实观测。观察统计只读X、Y及独立跨次观察S1、S2；条件T的真分数与抽象原系数仅用于独立理论校验，不进入纯观察α。

独立二条计算路线分别由完整Fraction来源人口矩计算项目方差及协方差、由固定线性系数独立解析协方差与真分数方差。另由完整1024配对校验跨次原协方差。两项目α由`4 Cov(X,Y)/Var(X+Y)`精确得出；与`2[1−(Var(X)+Var(Y))/Var(X+Y)]`逐世界严格一致。所有冻结世界分数方差均为正。

## 八项结果

| 人工世界 | 两项方差及协方差 | Cronbach α | 真分数信度 | 独立跨次重测信度 |
|---|---|---:|---:|---:|
| PARALLEL_INDEPENDENT | VarX=2, VarY=2, Cov=1 | 2/3 | 2/3 | 2/3 |
| SHARED_METHOD_WITH_TRAIT | 3,3,2 | 4/5 | 2/5 | 2/5 |
| PERFECT_TRAIT | 1,1,1 | 1 | 1 | 1 |
| PERFECT_METHOD | 1,1,1 | 1 | 0 | 0 |
| UNEQUAL_ERRORS | 2,5,1 | 4/9 | 4/9 | 4/9 |
| OPPOSING_METHOD | 2,2,0 | 0 | 1 | 1 |
| OPPOSING_TRAIT | 2,2,−1 | −2 | 0 | 0 |
| NON_EQUIVALENT_ITEM | 2,5,2 | 8/11 | 9/11 | 9/11 |

**同分布异信度反例：** PERFECT_TRAIT两项都等于稳定T；PERFECT_METHOD两项都等于同一次施测的共同误差M。两世界单次完整 `P(X,Y)` **每一可能观察格及其概率完全相同**，项目Var/Cov一致，α均为1。由于M在下一次测验重新独立抽取，PERFECT_METHOD的条件真分数恒0、重测Cov也为0；PERFECT_TRAIT的真总分方差为4、重测相关为1。两世界 `P(S1,S2)`不同。因此单次测试内部一致性并不能识别同一人稳定特征的跨次再现性；提供真正独立且具有测量等值性的第二次测量，在这两个固定人工世界中能区分两机制。

**共享误差与低估/负α：** SHARED_METHOD_WITH_TRAIT的两项误差协方差来自共用M，项目Cov=2，其中仅1来自稳定T；α=4/5、真实信度2/5，α高估一倍。OPPOSING_METHOD的两个共享方法误差正负抵消，总分S=2T完全无测量误差，项目Cov=0而α=0，真实信度为1。OPPOSING_TRAIT两个项目以相反符号测量T，Cov=−1，α=−2，实际总分完全丢失稳定T，真信度0。这些例子说明α的数值依项目结构与误差相关条件变化，可以负值，也可能与稳定真分数信度不同。

**项目不平行的边界：** UNEQUAL_ERRORS误差方差不同，但此有限例中α恰好等于真信度4/9；这一个等值不能推广为平行测验假设成立。NON_EQUIVALENT_ITEM项目载荷1与2、均值不同，α=8/11而真信度9/11。

## CI、机器证据与可复现性

1. [原生Python Fraction程序](r227_exact_classical_test_theory.py) 与真实测试机制：GitHub [CI run39811576720](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39811576720)，Python3.11和Python3.12实际作业日志各显示`Ran 60 tests`及`OK`，合计120测试执行通过；三作业Jobs API均为completed/success，run总体结论也为completed/success。
2. 全部[128单次原来源CSV](R227_ALL_128_ORIGINAL_SINGLE_TEST_SOURCES.csv) 和[1024跨次配对原来源CSV](R227_ALL_1024_ORIGINAL_RETEST_SOURCE_PAIRS.csv)、[完整世界矩与联合分布JSON](R227_EXACT_RESULTS.json)、[完整SHA256机器验收](R227_FINAL_MACHINE_ACCEPTANCE.json)由第三作业真正重算校验并永久归档，机器人原来源归档commit [4e52ecf9](https://github.com/edwardsage419/Psychohistory-Research/commit/4e52ecf949e9b1d1238a5b23b7fee0cb1c52406b)。
3. 原单次CSV SHA256为 `f9f9dfe6828b95fabf879889417e6f5fc42c3290bfddd137c6add9be369012c5`；原跨次配对CSV为 `e6e5d6784dbe1d56faacec02d6044609f6574af1b0d4a64294750263ea87b667`；精确结果JSON为 `ae948b352c0eaebaec591f661b8674fa8664b49010710a7fd4140a6e70f8a86b`。

## 科学边界与后续

本研究证明以上有限人工结构世界中的代数恒等式及其反例。没有真实题项难度、语言模型测量、纵向时间变化、学习与记忆、样本选择、因子结构、真实构念效度或任何历史因果识别。现实重复施测时可能出现练习、疲劳和不同条件，其跨次测量等值及误差条件须单独证明。人工E1，新增真人E2=0、真实历史E3=0。冻结R073/PESEN v0.1保持原状。

实际239目录下一条为 **10-002 Item Response Theory**，可登记R228。继续先完成全部既定R项目后再统一归类、最终模型熔炼。
