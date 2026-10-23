# R279 预测校准（12-009，P1）

研究结题 **CLOSED_BOUNDED_E1_ARTIFICIAL_POPULATION_FORECAST_CALIBRATION**。固定两个群体各两条有序二元观测、三种人工真实条件概率世界×三种冻结预测政策＝九个人工world。原完整4bit源每world16种，共144个模型标识类型，其中99个实际有正概率。

[事前冻结协议](../../protocols/R279_FORECAST_CALIBRATION_9_WORLDS_144_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [原生完整源码](r279_exact_forecast_calibration.py) · [全部144来源CSV](R279_ALL_144_ORIGINAL_FORECAST_CALIBRATION_SOURCES.csv) · [九世界REL/RES/UNC和Brier JSON](R279_EXACT_RESULTS.json) · [SHA机器凭证](R279_MACHINE_RECEIPT.json) · [正式科研报告](R279_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](R279_FINAL_ACCEPTANCE_STATUS.json)。

Murphy population Brier分解：Brier=REL−RES+UNC。平坦q=1/2在均值为1/2的三人工真世界都完全总体校准（REL=0），但分辨力RES=0；在真两群体概率1/4与3/4时固定半概率Brier=1/4，不如正确分组预测的3/16。本研究比较真正population conditional rates，不声称从有限样本估计可靠性零误差。

首次[CI run39904785939](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904785939)因执行器断行语法错误失败，已如实保留；[修正提交40fa945d](https://github.com/edwardsage419/Psychohistory-Research/commit/40fa945d0273b085279576f52b5abd0e3d24c284)后，[最终成功CI run39904942557](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904942557)三job completed/success，Python3.11及3.12各84真unittest共168项通过，第三独立来源/Murphy复算通过；完整原source机器人永久归档[commit1f7275b3](https://github.com/edwardsage419/Psychohistory-Research/commit/1f7275b346824e5b235a9fcdf59bd10d40028d6c)。

仅人工E1，新增真人E2和真实历史E3均为0，R073/PESEN v0.1继续冻结。下一原目录12-010 Brier Score（R280），遵守先全R研究完成后统一归纳分类、最后熔炼。
