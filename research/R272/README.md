# R272 样本外预测（12-002，P0）

正式研究等级：**CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_OUT_OF_SAMPLE_PREDICTION**。先冻结模型和评分规则，后进行完整九个人工Bernoulli世界、576原source训练4bit及真正独立测试2bit的精确解析复算；新增真人E2/历史E3均0。

[事前冻结协议](../../protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [源码](r272_exact_train_test_prediction.py) · [全部576完整原训练/测试source](R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv) · [精确结果JSON](R272_EXACT_RESULTS.json) · [原CSV和JSON SHA256](R272_MACHINE_RECEIPT.json) · [科学报告](R272_SCIENTIFIC_REPORT_2026-10-23.md) · [机器验收](R272_FINAL_ACCEPTANCE_STATUS.json)。

在真p=1/2时，MLE训练Brier 3/16优于常数1/4，但未来独立Brier 5/16反而高于常数1/4。冻结Laplace平滑在p=1/4或3/4的未来Brier 31/144优于MLE的15/64。未经截尾极端MLE给未来相反测试标签概率0，存在正质量的∞对数损失事件。所有结论限本人工概率空间。

[GitHub Actions run39903106107](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903106107)：Python3.11和3.12各83真单测、166通过，第三独立来源CSV全重算与原数据永久机器人归档均成功，全三job success。[完整原来源归档dd4995e8](https://github.com/edwardsage419/Psychohistory-Research/commit/dd4995e82cd62cc35c493b79f3525854c06a7eab)。

下一原目录12-003 Cross Population Validation（拟R273）。先完成全部R再统一归纳分类，最后熔炼；R073/PESEN v0.1冻结。
