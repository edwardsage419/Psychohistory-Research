# R133：严格演化稳定策略（ESS）

日期：2026-10-20，原始目录P1/05-009。

本研究从1973 Maynard Smith与Price原刊 p16 Table1、p17严格双条件出发，对625个2×2人工整数博弈完成精确代数分类、对原五策略25格印刷舍入模拟均值的纯ESS见证做审计，并自造三策略明确反例，证明只测试纯策略入侵者可能漏掉混合入侵者。

所有新计算均为数学对照：真实人/动物逐行E2=0，历史E3=0。R073与PESEN v0.1冻结。

- [计算前冻结](../../protocols/R133_ESS_ORIGINAL_1973_TWO_CONDITIONS_ALL_2X2_AND_3STRATEGY_COUNTEREXAMPLE_FREEZE_2026-10-20.md)
- [科学报告](R133_ORIGINAL_1973_STRICT_ESS_ALL_625_2X2_AND_MIXED_MUTANT_REPORT_2026-10-20.md)
- [源码及36项测试归档 ZIP](R133_exact_source_and_tests.zip)
- [真实Actions工作流](../../.github/workflows/r133-original-ess-625-exact.yml)
- [正式状态](R133_FINAL_ACCEPTANCE_STATUS.json)

解压 ZIP 至空目录后 `python -m unittest -v test_r133_ess_1973_exact.py`，再运行 `python r133_ess_1973_exact.py`。

分类结果：625种完整2×2矩阵，300组纯A ESS，300组纯B ESS，100组双纯ESS，200组内部Nash候选，100组内部混合ESS，25组中立无ESS。类别有重叠。三策略toy中纯入侵 D1 为(1,1,8)，混合入侵者D1=−1/9。原1973真实未舍入随机模拟不在可复算证据范围。
