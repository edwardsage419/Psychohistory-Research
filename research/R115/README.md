# R115：信息性社会影响——1992原始信息级联模型精确数学复算

日期：2026-10-19（Asia/Taipei）。对照原知识目录P0条目03-006 Informational Social Influence，**完成的是其中Bikhchandani–Hirshleifer–Welch (1992)严格同质二元信号、静态隐藏价值与公开行动观测的限定子模型**，不是全部信息性社会影响理论/真实心理学实证。研究状态：**CLOSED_BOUNDED_ORIGINAL_THEORETICAL_ACTION_CASCADE_RECONSTRUCTION；LEARNING_COMPLETE_BOUNDED_EXACT_ACTION_BAYES_AND_CASCADE；E2原真人预测0条**。R073、PESEN v0.1冻结。

第一手原文：
* [Bikhchandani, Hirshleifer & Welch, 1992 Journal of Political Economy 原著](https://doi.org/10.1086/261849)，[原期刊全文PDF副本](https://snap.stanford.edu/class/cs224w-readings/bikhchandani92fads.pdf)：直接核阅印刷第996-997页Section II.A、Table 1及**式(1)**，源码精确还原。
* [Deutsch & Gerard, 1955 社会信息与规范影响实验](https://doi.org/10.1037/h0046408)，已核对[PubMed](https://pubmed.ncbi.nlm.nih.gov/13286010/)元数据及PsycInfo公开摘要；**不是**全文独立拟合、没有1955年的真实原始个人判断CSV。

主要数学结果：p=7/10、价值V∈{0,1}等先验、采纳成本1/2与公平随机tie。前两人都采纳后，正确公开后验为**119/158≈75.32%**，而错误把两个公开动作当成独立高私人信号会给出**49/58≈84.48%**。当第三人进入上行信息级联，其即使私人信号是低也采纳，新增动作没有任何信息量，公开后验仍119/158。真实V=0时，前两人错误采纳且触发错误上行级联的条件概率仍为**39/200**；群体一致不表示事实正确，更不能证明行动受规范压力而非信息性学习驱动。

用Python标准库Fraction严格构造行动者的Bayesian私人后验、随机tie、公众对私有信号积分的行动likelihood和Bayesian公开后验，并枚举所有可行公开历史。与原作者1992印刷第997页式(1)两种方向概率、无级联概率严格比对，已在p=3/5、7/10、4/5以及n=2、4、6九组解析公式检查中逐项准确吻合。所有历史概率准确总和为1；非法布尔动作、非精确Fraction、信号精度边界、进入级联后的不可能反向行动均严格拒绝。

**GitHub Actions [39240086909](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39240086909) 成功，48项精确数学/合成单元测试全部通过。** 实际机器验收与源码、测试、报告三个文件的SHA256已由工作流提交、并经连接器回读。

研究文件：
- [正式冻结协议](../../protocols/R115_INFORMATONAL_SOCIAL_INFLUENCE_BHW_1992_EXACT_BAYES_ACTION_CASCADE_PRESCORE_FREEZE_2026-10-19.md)
- [第一手论文与数学机制正式报告](R115_BHW_1992_EXACT_ACTION_INFORMATION_CASCADE_SCIENTIFIC_MECHANISM_REPORT_2026-10-19.md)
- [原生Python精确有理数执行程序](r115_bhw_1992_informational_action_cascade_exact.py)
- [48项源公式及合成反例测试](test_r115_bhw_1992_informational_action_cascade_exact.py)
- [实际CI SHA及验收证据](R115_PHASE_A_BHW_1992_EXACT_FRACTION_SYNTHETIC_EQ1_CI_ACCEPTANCE.json)
- [正式科研结题状态](R115_FINAL_ACCEPTANCE_STATUS.json)

复算指令：`PYTHONPATH=research/R115 python -m unittest -v research/R115/test_r115_bhw_1992_informational_action_cascade_exact.py`。

严格保留与R112的区别：R112学习一般固定证据的Bayes更新；R115学习公开动作是由隐藏信号和先前信息**内生生成**，进入级联后新动作不一定提供新私人信息。本项目尚未融合这些研究，也未采集真人E2来判别真实规范影响与信息性学习。R115的数学验收不意味着对真实人际互动、群体事件或长期历史已经取得预测保证。继续已定R系列模型学习，之后统一归类，最后才熔炼。
