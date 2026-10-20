# R144：历史制度主义——序列、关键转折点与反事实边界

日期2026-10-20，原目录**P1/06-002 Historical Institutionalism**。

本期一手核读 James Mahoney (2000) *Path Dependence in Historical Sociology* DOI [10.1023/A:1007113830879](https://doi.org/10.1023/A:1007113830879) 原刊507–509页，以及 Capoccia & Kelemen (2007) *The Study of Critical Junctures* DOI [10.1017/S0043887100020852](https://doi.org/10.1017/S0043887100020852) 原刊341–343页。两文均属历史解释与方法论，不包含本项目人工数值状态机。

冻结后新建**六事件、4维状态、两事件长度改革窗口**的项目原创反应性链条，独立核算6⁵=**7776**条人工序列，120种相同事件多重集合的全排列、**38880**对单事件替换的潜在结果。其结果：
- 7776条：从未最终改革/巩固7663，改革但未巩固96，改革且巩固17；
- 38880次配对替换为等待，最终制度改变373，巩固改变69，任一个改变388；
- 五个不同事件共有120种顺序，其中4种形成改革，其余116种未改革；
- `OMAWW`及`OMAEW`同样最终显示改革，但只有后者巩固；两者遭遇下一次相同反对事件后，一个撤销改革，一个维持。由此证明**在人工模型内仅凭终点制度二元编码无法恢复完整形成机制**，不可由此声称真实历史因果被识别。

两条独立状态转移实现对于7776条各逐步完全一致，171项本地单元测试全通过。最初一项测试误传字符串而非元组，校正测试并重验；冻结代码状态更新规则未为迎合测试更改。

正式文件：[事前冻结协议](../../protocols/R144_MAHONEY2000_CAPOCCIA_KELEMEN2007_HISTORICAL_INSTITUTIONALISM_SEQUENCE_COUNTERFACTUAL_PRESCORE_FREEZE_2026-10-20.md)｜[科学报告](R144_HISTORICAL_INSTITUTIONALISM_PRIMARY_SOURCES_AND_COUNTERFACTUAL_REPORT_2026-10-20.md)｜[完整Python源＋171项测试＋全结果JSON的ZIP](R144_Mahoney_Capoccia_Kelemen_171_Tests.zip)｜[机器结果摘要](R144_RESULTS_SUMMARY.json)｜[正式状态](R144_FINAL_ACCEPTANCE_STATUS.json)｜[GitHub Actions](../../.github/workflows/r144-historical-institutionalism-171-tests.yml)。

解压后使用`python -m unittest -q test_r144_historical_institutionalism_exact.py`和`python r144_historical_institutionalism_exact.py > replay.json`。全部仅依赖Python标准库，不发布原论文的版权PDF。

**新真人E2=0、外部历史E3=0**；R073、PESEN v0.1继续冻结。遵循全部R学习结束后再整体归纳分类，最后熔炼。

**GitHub Actions 正式通过**：[run39397216634](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39397216634)。运行源码快照commit `21ee3ac9d2d4eba705304573ebe072ae5ed645d4`；Python3.11 job118542806511实际171 tests in 3.016s；Python3.12 job118542806818实际171 tests in 3.464s，共342项、0失败。两个环境每任务四份SHA256均校验OK且确实重新执行完整序列/反事实全结果JSON逐字节一致。[独立验收收据](R144_PHASE_A_342_REAL_TESTS_7776_HISTORIES_38880_COUNTERFACTUAL_CI_RECEIPT.json)与正式科研状态文件均已归档。**有界结题不等于实际历史制度因果识别。**
