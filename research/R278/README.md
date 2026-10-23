# R278 模型平均与集成（12-008，P2）

研究状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_BAYESIAN_MODEL_AVERAGING**。三个人工真p×四种固定预测政策＝十二world，每world四训练bit+两独立测试bit的所有64种原source，合计**768个带policy标签完整人工source**。同p的四政策共享相同原随机来源，不是768个真人实验。

[事前冻结协议](../../protocols/R278_BAYES_MODEL_AVERAGING_12_WORLDS_768_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整原生Python](r278_exact_bayesian_model_averaging.py) · [全768原source含逐行预测CSV](R278_ALL_768_ORIGINAL_MODEL_AVERAGING_SOURCES.csv) · [12个数学结果JSON](R278_EXACT_RESULTS.json) · [原来源SHA256凭证](R278_MACHINE_RECEIPT.json) · [正式科学报告](R278_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器E1验收](R278_FINAL_ACCEPTANCE_STATUS.json)。

真p=1/4，硬选择未来Brier205/1024优于BMA 87/410；真p=3/4，BMA 87/410优于硬选择259/1024；真p=1/2，BMA46637/168100优于硬选择5/16但差于固定半概率1/4。硬选择K=2平局事前固定取低p，使两端风险不对称；目标真率oracle是数学下界，非可部署预测器。

[GitHub CI run39904644080](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904644080)三个job completed/success，Python3.11与3.12各108真unittest通过，总216项，第三独立768-source全CSV重算归档完成。机器人永久原数据归档[0f39a4a7](https://github.com/edwardsage419/Psychohistory-Research/commit/0f39a4a753aa47bc4484b9de429da12a316196cb)。

仅人工E1，新增真人E2及历史E3为0，R073/PESEN v0.1保持冻结；下一原目录12-009 Forecast Calibration（拟R279）。先完成全部原R系列，再统一归纳分类，最后开始熔炼。
