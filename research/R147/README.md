# R147 制度扩散：观测等价、共同冲击与政策干预

2026-10-20；原模型目录 **P1 / 06-005 Institutional Diffusion Models**。

核读经典政策扩散文献：Berry & Berry 1990 DOI [10.2307/1963526](https://doi.org/10.2307/1963526)，**只读原刊出版方摘要**；Shipan & Volden 2008 DOI [10.1111/j.1540-5907.2008.00346.x](https://doi.org/10.1111/j.1540-5907.2008.00346.x)，**原刊第840、842、845页实际视觉核查**、p841–844原文文本。后者的真实675城反吸烟政策数据未获取/重跑，四大机制并未通过本项目人工数据完成现实识别。与R119–R122网络阈值级联不同，本期重点是独立反例：**同样完整地区采纳观测分布并不决定因果干预效应**。

人工三地区两套结构因果生成器：
- D地区政策扩散与S隐藏外部共同冲击，都产生完全相同的8种采纳状态联合概率：9/32、3/32、3/32、1/32、1/32、3/32、3/32、9/32；
- 观察B对A的风险差都为1/2，但实际 `do(A)` 下D因果效应1/2，S因果效应0。这里隐藏U与A完美同值，明确不具所有隐藏分层内的条件重叠。
- 额外4地区路径/星/环×有无地区邻居效应×有无共同年度冲击共**12种**人工四期概率模型，完整16终态分布由**两个独立Fraction算法逐情景一一核验**；没有真人或历史观测样本。beta=0时图结构不影响最终分布；共同冲击即使没有邻居效应也会制造跨地区采纳相关。

归档：[事前冻结协议](../../protocols/R147_SHIPAN_VOLDEN2008_BERRY1990_POLICY_DIFFUSION_COMMON_SHOCK_CAUSAL_NONIDENTIFICATION_PRESCORE_FREEZE_2026-10-20.md)｜[完整科学研究报告](R147_POLICY_DIFFUSION_OBSERVATIONAL_EQUIVALENCE_CAUSAL_IDENTIFICATION_SCIENTIFIC_REPORT_2026-10-20.md)｜[原Python源码、86项unittest、完整全结果ZIP](R147_ShipanVolden2008_PolicyDiffusion_86_Tests.zip)｜[机器结果摘要](R147_PHASE_A_RESULTS_SUMMARY.json)｜[正式验收状态](R147_FINAL_ACCEPTANCE_STATUS.json)｜[GitHub Actions](../../.github/workflows/r147-policy-diffusion-86-tests.yml)。

解压 ZIP 后执行 `python -m unittest -q test_r147_shipan_volden_policy_diffusion_exact.py` 和 `python r147_shipan_volden_policy_diffusion_exact.py > replay.json`。无第三方依赖。本期全部为**原创人工E1理论实验**：新增真人E2 0，外部历史E3 0；R073和PESEN v0.1继续冻结；既定R完成后再统一分类归纳与熔炼。
