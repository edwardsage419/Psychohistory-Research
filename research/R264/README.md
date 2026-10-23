# R264 近似贝叶斯计算（11-024，P2）

九人工三个离散θ、两次2bit Bernoulli模拟、完整**432原先验—模拟source**。科研状态`CLOSED_BOUNDED_E1_EXACT_FINITE_REJECTION_ABC_AND_SUMMARY_INFORMATION_LOSS`，仅做有限拒绝ABC，未复现原论文局部线性回归或真实人口遗传学推断。

[预评分冻结](../../protocols/R264_ABC_9_WORLDS_432_THETA_SIMULATION_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [正式科学报告](R264_SCIENTIFIC_REPORT_2026-10-23.md) · [原生Fraction模拟拒绝ABC与独立解析四Y似然程序](r264_exact_finite_rejection_abc.py) · [432完整原source](R264_ALL_432_ORIGINAL_THETA_SIMULATOR_SOURCE_ATOMS.csv) · [81组距离/ε结果JSON](R264_EXACT_RESULTS.json) · [SHA256机器来源凭证](R264_FINAL_MACHINE_ACCEPTANCE.json) · [有界正式验收](R264_FINAL_ACCEPTANCE_STATUS.json)。

冻结目标人工Yobs=(1,0)，三种距离(full Hamming、总计数count、只观察首项)×ε=0,1,2。全部9×9=81种ABC源拒绝后验/接受率与独立Bernoulli四种输出解析计算精确一致。FULL ε0等于正确全Y Bayes；ε2全接受、回到先验。COMPLEMENTARY_GRADIENT与REVERSED_COMPLEMENT的每θ计数摘要分布相同、COUNT ε0后验皆(5/14,2/7,5/14)，但完整Y后验分别(1/14,2/7,9/14)及(9/14,2/7,1/14)，TV皆2/7。**ε=0也不能弥补不充分摘要丢失的身份信息**。IID条件同分布时count是足够的，FIRST_ONLY θ独立Y2时只取Y1亦足够，必须具体检验。

[GitHub Actions run39899758034](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899758034)三job通过、Python3.11/3.12各82真测试共164，完整CSV/JSON/SHA机器人永久main归档[ce269471](https://github.com/edwardsage419/Psychohistory-Research/commit/ce26947160448c00cbeae80fb6c136be53dd3fe0)。新增真人E2/历史E3=0，R073/PESEN v0.1冻结。下一原11-025 Sobol Global Sensitivity（R265）。
