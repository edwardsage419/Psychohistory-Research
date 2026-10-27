# B轨 R205 独立未来分布转移审计：原960行直接加权

日期：2026-10-27。测试规则已在 [事前冻结协议](../../protocols/R205_HELDOUT_AXIS_MIXTURE_SHIFT_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md)固定，冻结提交773064c873f5bf835b3be7a42965d9bde6e3de81。项目内部程序性复核，E1人工数学，外部研究者独立复现0项。

## 独立数据入口与计算方法

R轨读取原240条训练历史，使用所选主轴的解析风险。B轨另行读取原R205完整960条训练×独立未来事件CSV，逐行复核人工尺度、未来轴、正负符号、真实坐标、原重建误差及两目标损失。每行原联合权重1/(2^m×4)；当未来轴为1时乘以2q，轴为2时乘以2(1-q)。直接从960行的原始事件误差积分重算每个36世界，独立计算两个坐标能量、未来oracle方向及风险，不导入R轨函数或使用R轨的p加权解析风险公式。原始960行在三个q下重复计权，构成2880个加权评估单元，并非2880个独立观察者。

程序 [b_r205_heldout_shift_960row_audit_20261027.js](b_r205_heldout_shift_960row_audit_20261027.js)。运行：node research/evidence_audit/b_r205_heldout_shift_960row_audit_20261027.js research/R205/R205_ALL_960_INDEPENDENT_TEST_SOURCE_PAIRS.csv research/validation/R205_HELDOUT_AXIS_SHIFT_36_EXACT_RECEIPT_2026-10-27.json。

## 实际运行结果

960行原始几何与误差共3840项断言通过。36世界每世界12项风险、概率与oracle轴字段比较共432项全部一致，36项世界概率归一全部通过。44项负对照诊断实际检出，其中36世界若非法依据未来真实轴选择PC会产生不允许的零重建损失；q=1/20时另有8世界的实际风险与错误沿用q=1/2权重不同。某些人工世界对q变化不敏感，故没有将所有错误q案例都当作必须检出。总检查数4352项，全部通过，差异0。

机器收据 [B_R205_HELDOUT_AXIS_SHIFT_960_ROW_AUDIT_RECEIPT_2026-10-27.json](B_R205_HELDOUT_AXIS_SHIFT_960_ROW_AUDIT_RECEIPT_2026-10-27.json)保存计数与状态。审计复核了输入事件及积分路径，R/B都在同一研究者工具体系内，未取得外部研究团队独立重复实验或现实数据。因枚举的是完整人工有限总体，未进行重采样置信区间；实际未来q未知时的估计误差及校准风险仍待研究。新增真人E2=0、历史E3=0。远端CI若未运行，应记NOT_RUN；R073与PESEN v0.1不变。
