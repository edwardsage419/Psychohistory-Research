# R204 Gaussian Process：人工12世界E1正式有界结题

2026-10-21。原239模型目录P2/08-028。**CLOSED_BOUNDED_E1_ARTIFICIAL_FINITE_GP**。

[研究协议先冻结](../../protocols/R204_GP_12_WORLDS_912_OBSERVED_AND_HELDOUT_PRESCORE_FREEZE_2026-10-21.md) · [正式报告](R204_SCIENTIFIC_REPORT_2026-10-21.md) · [12世界完整机读](R204_EXACT_RESULTS.json) · [912条训练与留出人工来源CSV](R204_ALL_912_REAL_SOURCE_GP_TRAIN_AND_HELDOUT.csv) · [双SHA机器验收](R204_FINAL_MACHINE_ACCEPTANCE.json) · [原生Python与31测试](r204_exact_finite_gp.py)。

以Rasmussen/Williams 2006 Chapter 2原公式为依据，固定四个核IID、CONSTANT、ALTERNATING、LINEAR，三种训练与留出位置划分，完整源912条。真实潜在与观察噪声均离散Rademacher，训练高斯边际似然只是**错设工作模型**。训练核选好之后再看未观测位置的真正潜在函数并给原来源MSE；每个真核/固定候选的留出风险经Fraction完整真信号噪声枚举与解析矩阵矩二路严格相同。真ALTERNATING在训练位置(0,2,4)与真CONSTANT的整个观察分布完全一致，前者因同分规则永远不会被选中，实际留出位置(1,3)选模MSE **89/32=2.78125**，远差于真核已知最优线性1/4。真LINEAR在插值/稀疏布局正确选核概率1，分别达到MSE1/9、1/20。真IID外推有限选核MSE1.76389劣于固定零预测1。

[GitHub Actions run39608802753](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39608802753) Python3.11与3.12各31项共62项成功，第三完整原来源和SHA归档job成功，[原结果已永久写入main提交1d10577](https://github.com/edwardsage419/Psychohistory-Research/commit/1d10577ed85537bf3fbe4c61d01ec62d1f504b69)。

仅数学/人工E1，新增真人E2=0、真实历史E3=0，R073、PESEN v0.1继续冻结。下一 **R205 P1/08-029 Principal Component Analysis**。完成全部R再分类和熔炼。
