# R203 空间回归模型：完整人工E1有界结题

2026-10-21。原239模型目录P1/08-027 Spatial Regression。最终科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_SPATIAL_REGRESSION**。

[计算前冻结](../../protocols/R203_SPATIAL_15_WORLDS_240_TRAIN_3840_INDEPENDENT_PRESCORE_FREEZE_2026-10-21.md) · [正式科学报告](R203_SCIENTIFIC_REPORT_2026-10-21.md) · [15世界完整结果](R203_EXACT_RESULTS.json) · [240原训练CSV](R203_ALL_240_ORIGINAL_SPATIAL_TRAINING_WORLDS.csv) · [3840条独立来源测试配对CSV](R203_ALL_3840_INDEPENDENT_TEST_SOURCE_PAIRS.csv) · [SHA机器验收](R203_FINAL_MACHINE_ACCEPTANCE.json) · [原生Python与36单测](r203_exact_spatial_regression.py)。

五源IID/SAR±/SEM±×平滑、交替、混合三协变量结构，四节点空间权重矩阵经Gauss-Jordan和W³=W双Fraction求逆，完整240训练区域与3840独立新区域配对全部原来源加权。训练采用含Jacobian的高斯**错设工作准似然**，原噪声实际为离散Rademacher，独立未来的MSE双Fraction枚举与Gaussian logscore双路线核验。关键负面：真IID平滑训练选模新区域MSE1.090278劣于固定IID1；真SEM_POS平滑1.923611劣于固定IID1.611111；真SAR_POS平滑选模1.923611优于固定IID2.611111，但劣于真机制已知oracle1.611111。真SEM_POS相同空间相关却因协变量空间构型令OLS方差误读比平滑4、交替4/9；真SAR_POS平滑导致原点OLS系数均值2，虽然原结构β=1。

[GitHub Actions run 39607229468](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39607229468) Python3.11与3.12各36项，共72项全成功，第三归档job成功。完整原始训练、独立测试及结果已由[机器人提交2ffa199](https://github.com/edwardsage419/Psychohistory-Research/commit/2ffa1999030e66ed2b3c5195a3ed78ac8e72d57b)永久写回main。研究证据范围仅人工E1，不等同真实空间因果机制识别，新增真人E2=0、历史E3=0。R073/PESEN v0.1仍冻结。

下一研究 **R204 P2/08-028 Gaussian Process**。维持完成全部R系列后统一分类、最后熔炼。
