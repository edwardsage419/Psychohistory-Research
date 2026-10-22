# R229 Rasch 模型（10-003）：八人工世界条件似然与题目连接性E1结题

日期2026-10-23。原始239目录 **10-003 Rasch Model（P2）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RASCH_CONDITIONAL_LIKELIHOOD**。不将本项有限人工模型等同真实Rasch CML测验拟合或历史预测复现。

[计算前独立冻结协议](../../protocols/R229_RASCH_8_WORLDS_4096_FULL_RESPONSE_MATRICES_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告与纠错记录](R229_SCIENTIFIC_REPORT_2026-10-23.md) · [原生Python与71项测试](r229_exact_rasch_conditional.py) · [4096原完整响应矩阵来源](R229_ALL_4096_ORIGINAL_3X3_MATRIX_SOURCES.csv) · [八世界精确Fraction结果](R229_EXACT_RESULTS.json) · [源SHA机读凭证](R229_FINAL_MACHINE_ACCEPTANCE.json) · [独立有界正式验收](R229_FINAL_ACCEPTANCE_STATUS.json)。

Rasch合法世界的固定总分条件下相邻题条件赔率对比为2,2，难度差加倍变为4,4；2PL不同题区分度世界则按人变为4/2/1与1/2/4。两组能力分布虽不同，但在固定每人的行总分后保留相同项目条件赔率。第三题与其他题目无共同受试者的世界，在个人条件似然中完全丢失其与其他两题的共同难度尺度，必须补独立共同作答或外部锚定证据。

首轮[CI run39823447220](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39823447220)虽然job全部success，但汇总误计未观测题目数与零概率支持，曾归档首轮旧结果。后经[修复23d361f6](https://github.com/edwardsage419/Psychohistory-Research/commit/23d361f65711abeff8ce51505c48268e7f587ff1)新增三项回归，仅改描述统计元数据、未改冻结数学机制和原矩阵概率。最终[CI run39823620309](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39823620309) 三作业全部success，Python3.11与3.12各71单测共142次；来源最终归档commit [e0cd73cf](https://github.com/edwardsage419/Psychohistory-Research/commit/e0cd73cf5fe3f69af8a65ae30414d46a22548b22)。

E1人工数学，真人E2新增0，真实历史E3新增0；R073/PESEN v0.1保持冻结。下一真实原目录 **10-004 Exploratory Factor Analysis（R230）**，按既定次序完成原R后统一归纳分类，最后熔炼。
