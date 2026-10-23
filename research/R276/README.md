# R276 模型可辨识性（12-006，P0）

状态：**CLOSED_BOUNDED_E1_THREE_PARAMETER_STRUCTURAL_IDENTIFIABILITY**。三个冻结人工参数点(1/2,1/2)、(1/4,1)、(1,1/4)有相同产品q=1/4，只观察四Y的联合概率分布不能区分，等先验冻结MAP平均分类正确率1/3；增加两条Z直接测量θ1后，三个参数点的联合概率分布各不相同，平均有限样本识别率**11/16**。此“可辨识”限三个参数点，未覆盖连续二维参数空间。三个模型×全部64六bit=192原source，包含零质量占位，非零source144。

[事前冻结协议](../../protocols/R276_STRUCTURAL_IDENTIFIABILITY_192_SOURCE_ATOMS_THREE_PRODUCT_PARAMS_PRESCORE_FREEZE_2026-10-23.md) · [原生执行程序](r276_exact_structural_identifiability.py) · [全192原source CSV](R276_ALL_192_ORIGINAL_IDENTIFIABILITY_PARAMETER_SOURCES.csv) · [精确JSON结果](R276_EXACT_RESULTS.json) · [SHA机器凭证](R276_MACHINE_RECEIPT.json) · [完整科研报告](R276_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](R276_FINAL_ACCEPTANCE_STATUS.json)。

[GitHub Actions run39904079585](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904079585)三job completed/success，Python3.11与3.12各50真单测共100通过，第三独立源CSV逐条参数似然复算成功，全原source及结果/SHA机器人永久归档[commit e32a4a4f](https://github.com/edwardsage419/Psychohistory-Research/commit/e32a4a4fb38ee90eea6ab7670eadf54ff3bbdbad)。

人工数学E1而已，新增真人E2=0、真实历史E3=0，R073/PESEN v0.1冻结。下一原候选12-007 Model Misspecification Checks（拟R277），全部原R完成后再统一归纳分类和熔炼。
