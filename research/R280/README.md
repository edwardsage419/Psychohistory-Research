# R280 Brier 评分（12-010，P1）

正式状态：**CLOSED_BOUNDED_E1_FINITE_BERNOULLI_BRIER_STRICT_PROPRIETY**。三人工真实Bernoulli率p×三冻结报告概率q形成九world，每world四独立bit全部16种有序来源配置，共**144个带world标签的原source类型**。精确Brier期望满足`E[(Y-q)^2]=p(1-p)+(q-p)^2`，q=p在真分布下期望最优；但四条有限观测样本可能让错误q偶然获得更低样本平均损失。例如真p=1/2与错报q=1/4时，发生概率5/16。

[事前冻结协议](../../protocols/R280_BRIER_STRICT_PROPRIETY_9_WORLDS_144_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [标准库源码](r280_exact_brier_strict_propriety.py) · [全部144原source和样本逐行损失](R280_ALL_144_ORIGINAL_BRIER_SCORING_SOURCES.csv) · [九world解析真值JSON](R280_EXACT_RESULTS.json) · [SHA256机器收据](R280_MACHINE_RECEIPT.json) · [科学报告](R280_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](R280_FINAL_ACCEPTANCE_STATUS.json)。

[GitHub Actions run39905121175](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905121175)三个job completed/success，Python3.11及3.12各83项真实单测，共166项通过，第三独立原CSV完整重算和机器人永久归档成功。[来源commit 6d94abb6](https://github.com/edwardsage419/Psychohistory-Research/commit/6d94abb697633a44b12db4db587d38c27fce11c9)。

全部只有有限人工E1，新增真人E2/真实历史E3=0，R073/PESEN v0.1冻结；下一原目录12-011 Logarithmic Score（拟R281）。先完成剩余全部R，再统一归纳、分类，最后熔炼原创模型。
