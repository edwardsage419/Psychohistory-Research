# R135：2004 原始间接互惠信誉规范的4096策略完整ESS复算

**原目录 P1 / 05-011 Indirect Reciprocity，2026-10-20。**

相较此前R072的四人信誉toy，当前读取Ohtsuki/Iwasa2004真实原刊14页，核实Table1、Table2、Eq1–10与Fig2/3；用独立标准库程序穷举**256种规范×16种策略×15种不同入侵行为=61,440次**稀有入侵判定，信誉镜像约化得到2080个独立轨道。本次严格按照原发表 me=ma=.02、b=2、c=1：**161个镜像ESS，其中136个AllD，25个非平凡**；敏感性b=4/3/1.2/1.1依次73/59/15/13。所有数字同论文Fig2，并独立确认领先八种合作收益。

成果导航：

1. [计算前冻结协议](../../protocols/R135_OHTSUKI_IWASA_2004_FULL_4096_NORMS_MUTANT_INVASION_PRESCORE_FREEZE_2026-10-20.md)
2. [科研审计报告](R135_OHTSUKI_IWASA_2004_FULL_4096_RULE_ESS_SCIENTIFIC_REPORT_2026-10-20.md)
3. [Python源码与50项标准库单元测试ZIP](R135_Ohtsuki_Iwasa2004_full_4096_50_tests.zip)
4. [五种收益参数完整机读结果](R135_PHASE_A_4096_CANDIDATES_FIVE_BENEFITS_RESULTS.json)
5. [正式有界验收状态](R135_FINAL_ACCEPTANCE_STATUS.json)
6. [GitHub Actions CI](../../.github/workflows/r135-indirect-reciprocity-50-tests.yml)

解压源码ZIP，运行 `python -m unittest discover -s . -p 'test_r135_ohtsuki_iwasa_2004_exact_norms.py' -v`，然后运行 `python r135_ohtsuki_iwasa_2004_exact_norms.py`。只使用Python3标准库。

新真人/动物原始记录为0，独立人级预测E2=0，外部历史E3=0；R073/PESEN v0.1继续冻结。目录既定R研究完成之前不进行跨目录分类或模型熔炼。
