# R281 对数预测评分（12-011，P1）

正式研究结题状态：**CLOSED_BOUNDED_E1_EXACT_SYMBOLIC_LOG_SCORE_WITH_INFINITE_RISK**。三真率p=1/4、1/2、3/4 × 五固定预报概率q=0、1/4、1/2、3/4、1，共15个人工world，每world16个有序四bit独立数据源，**240个完整人工原source类型**。完整正对数损失 `−ln P(realized y)` 严格处理真实发生结果的零预测概率：记为INF，不截断也不静默删除。所有有限loss由精确有理数ln2/ln3系数表示，原source加权与独立真Bernoulli理论完全一致。

[先行研究冻结协议](../../protocols/R281_LOG_SCORE_15_WORLDS_240_COMPLETE_SOURCE_SYMBOLIC_FREEZE_2026-10-23.md) · [原生执行源码](r281_exact_symbolic_log_score.py) · [240完整原source逐行符号loss及无限标记](R281_ALL_240_ORIGINAL_LOG_SCORE_SYMBOLIC_SOURCES.csv) · [十五world正式解析JSON](R281_EXACT_RESULTS.json) · [源CSV/结果SHA256机读凭证](R281_MACHINE_RECEIPT.json) · [正式科学报告](R281_SCIENTIFIC_REPORT_2026-10-23.md) · [有界机器验收](R281_FINAL_ACCEPTANCE_STATUS.json)。

真p=1/2报告q=0时，四bit原source中至少一次正事件的概率15/16，意味着四次样本的平均log loss=+∞，因此总体期望也为+∞；只有全部0的四bit source可得偶然0损失。所有内点q的期望交叉熵精确由ln2、ln3有理系数表示，KL理论确保真q=p的总体期望最优。只证明冻结有限Bernoulli空间，不构成真人或历史预测验证。

[最终GitHub Actions run39905387817](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905387817)三job全部completed/success，Python3.11及3.12各134项真正unittest通过共268项，第三独立240-source符号重算与永久GitHub机器归档成功。[完整原source归档commitd038a6b9](https://github.com/edwardsage419/Psychohistory-Research/commit/d038a6b9794152463bf05e058c3d43c22f197cb6)。

新增人类E2=0、真实历史E3=0，R073/PESEN v0.1继续冻结。下一原目录12-012 Open Reproducible Workflow and ODD（R282）；全R候选完成后再统一归纳、分类与熔炼。
