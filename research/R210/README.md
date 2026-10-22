# R210 随机对照实验（原239目录09-001）：有限人工E1正式结题

日期2026-10-22。原239候选目录真实条目 **09-001 Randomized Controlled Experiment，P0**。状态**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RANDOMIZATION**，不等同所有RCT真实因果效应已得到证实。

[事前冻结协议](../../protocols/R210_RCT_7_WORLDS_140_RANDOM_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md) · [正式完整科学报告](R210_SCIENTIFIC_REPORT_2026-10-22.md) · [七世界全部原精确结果](R210_EXACT_RESULTS.json) · [140条真实人工来源随机分配CSV](R210_ALL_140_COMPLETE_RANDOM_ASSIGNMENT_SOURCES.csv) · [机器SHA验收](R210_FINAL_MACHINE_ACCEPTANCE.json) · [事后科学结题收据](R210_FINAL_ACCEPTANCE_STATUS.json) · [纯标准库Python及40项单测](r210_exact_rct_randomization.py)。

完全固定6名人工单位，均衡处理/对照3/3的C(6,3)=20种分配全部等概率1/20，六个预冻无干扰潜在结果世界与第七个三对邻居干扰世界，合计140条人工原来源记录。六SUTVA世界中完整20分配E[处理对照均值差]=真有限人口ATE；完整设计Var直接逐Fraction枚举与Neyman精确公式`S1²/3+S0²/3−Sτ²/6`一致，通常可见组内方差估计随机平均多出`Sτ²/6`。3/3均衡双侧Fisher尖锐null置换最小p为2/20=0.1，故0.05下无论真实人工效果是否非0都不能拒绝，**设计分辨率过低不能冒称真无效**。三对邻居干扰模型Y_i=i+2z_i+3z_peer，固定同伴条件下真实直接效果恒2，随机处理对照均值差期望却为7/5，显示忽视干扰会改变所估计对象；此源明确禁用不成立的无干扰Neyman和Fisher检验。

[Actions run39736791824](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39736791824) Python3.11与3.12各40项、合计80成功，第三完整原文件SHA归档作业success，[真实机器原结果机器人提交4ce1463c](https://github.com/edwardsage419/Psychohistory-Research/commit/4ce1463ca9ee404f268d24717e8b6c34b3a6e761)。

只支持当前固定人工六人设计的数学恒等式与有界反例，新增真人E2=0、真实历史E3=0，R073/PESEN v0.1冻结。下一真正原目录研究 **R211 09-002 Potential Outcomes Framework**。完成真实原239全部模型后统一分类，再模型熔炼。
