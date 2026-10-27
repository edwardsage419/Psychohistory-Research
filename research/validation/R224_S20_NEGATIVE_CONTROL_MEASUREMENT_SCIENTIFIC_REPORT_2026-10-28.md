# R224 S20 负对照结果测量误差有限人工机制研究
日期：2026-10-28。证据等级：E1人工。原R224正式验收不变。

## 来源和冻结
预评分冻结提交 `036c04fd069ff47c3ea8bb309258532bd754fea4`，原R224 4096来源CSV blob `8484f9e6546d22d68dee3315b2dc11a7ddf27a26`，原R224结果JSON blob `37a27cfac39a1b06a993fc22d9866c63852b5799`。冻结五个核，8世界×5核=40条件，每条件512原来源×2测量状态=1024来源槽，共40960槽。R直接展开来源，B通过原观察联合分布矩阵变换及oracle联合分布独立复算。所有计算为BigInt精确有理数。

## 主要结果
原HIDDEN_CONFOUNDED_NULL世界真实A→Y效应为0，观察D_AY=1/4；对称误分类1/2使D_AWstar从1/4衰减为0，造成原本可见的混杂信号消失。INVALID_OUTCOME_DIRECT_A世界原真实A→W=1/2；对称误分类1/2使观察A→Wstar关联降为0，测量后的A→Wstar效应也降为0，不能据此反推原W的有效性。按A变化的假阳性测量核可以制造或改变A与Wstar的观察关联，需核验测量过程与A是否独立。

全部40条件的D_AY和D_ZY均与原研究一致，原真实ATE_Y和真实A→W均未修改。对称核满足D_AWstar=(1−2e)D_AW和D_ZWstar=(1−2e)D_ZW。朴素校正D_AY−D_AWstar在误差存在时没有一般因果识别保证。

## 复算与证据边界
R源程序 `research/validation/r224_s20_negative_control_measurement_exact_20261028.js`；机器收据 `research/validation/R224_S20_40_CONDITION_EXACT_RECEIPT_2026-10-28.json`。B独立程序 `research/evidence_audit/b_r224_s20_joint_matrix_independent_20261028.js`，执行320项字段精确核验、184项附加断言、2项错误注入检出，失败0。内部程序性独立复核，外部团队独立复现0。未做真实数据预测、概率校准或历史外推；新增E2=0，E3=0。R073与PESEN v0.1继续冻结。

## 费用与CI
未启动Actions，新增CI状态待远端确认；使用现有工具和免费GitHub权益，主动新增费用0。账户实际账单及免费额度未独立核验。
