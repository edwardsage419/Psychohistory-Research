# R141：Mancur Olson 1965 集体行动逻辑

原目录 **P1 05-017 Logic of Collective Action**。2026-10-20。

一手资料：Mancur Olson (1965), *The Logic of Collective Action: Public Goods and the Theory of Groups*, Harvard University Press，DOI https://doi.org/10.4159/9780674041660。核阅Wisconsin大学留存[1965原版第一章的27页双面扫描](https://users.ssc.wisc.edu/~oliver/SOC924/Articles/olsonlogic.pdf)，原印刷p6–7、22–23、38–39、50–52：私人受益分享、个人激励与成本、群体规模、privileged/latent群，以及selective positive and negative incentive。这不代表本期已经核对原著后半的历史经验材料。

研究贡献是**两个项目原创的合成博弈**：连续贡献二次公益收益模型N×奖励2维共24个精确有理数场景；门槛供给二元个人行动模型8种N×3种奖励共24个场景，穷举213096组（跨奖励场景重复计数）行动档案，共3331944个可行单侧翻转机会，源程序为遇到盈利偏离时提前停止的NE判定。另核验16人群体把一个人的受益份额调至1/2时，零供给均衡变成(2,0,…,0)的单人供给。

显著边界案例：N8门槛3、无奖励时57个纯均衡（零供给+56个三人供给）；N16无奖励只有零供给，奖励1/2时增至561个纯均衡（零供给仍存在），奖励2时唯一纯均衡为全部贡献16人、需外部财政32、资源总净收益反为−4。持续区分个人动机、资源总收益、协调选择与外部转移财政负担。

[科研完整一手文献及数学报告](R141_OLSON_1965_COLLECTIVE_ACTION_GROUP_SIZE_PRIVILEGED_INCENTIVE_SCIENTIFIC_REPORT_2026-10-20.md) ｜ [计算前冻结协议](../../protocols/R141_OLSON1965_COLLECTIVE_ACTION_SIZE_PRIVILEGED_SELECTIVE_INCENTIVE_EXACT_FREEZE_2026-10-20.md) ｜ [83项Python unittest+源程序+全量结果ZIP](R141_Olson1965_83_Tests_Original_Source.zip) ｜ [接受状态](R141_FINAL_ACCEPTANCE_STATUS.json) ｜ [GitHub Actions 3.11/3.12](../../.github/workflows/r141-olson1965-83-tests.yml)。

解压ZIP运行 `python -m unittest -q test_r141_olson1965_collective_action_exact.py`；随后 `python r141_olson1965_collective_action_exact.py > replay.json`。Python标准库Fraction精确计算，独立按本人行动改变的直接收益差和群体贡献人数双路径核验每个离散均衡。数值全是E1人工模型，无新真人预测E2，无历史预测E3。R073/PESEN v0.1冻结。全部既定R模型学完后再统一归纳，最后熔炼。

**CI已完成的验收**：[GitHub Actions 39390938992](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39390938992)，源码快照commit `f79442aa28a61b13286e58b4dd6b62e97160d032`。Python3.12 job118522008660真实83 tests in 25.960s；Python3.11 job118522008941真实83 tests in 35.378s，双环境合计166项无失败，4种ZIP/原文件SHA256各环境均OK，完整48组数学模型结果逐字节回放通过。详情：[R141_PHASE_A_166_TESTS_213096_SYNTHETIC_PROFILES_GITHUB_CI_RECEIPT.json](R141_PHASE_A_166_TESTS_213096_SYNTHETIC_PROFILES_GITHUB_CI_RECEIPT.json)。数学研究有界结题，真人E2和历史E3仍为0。
