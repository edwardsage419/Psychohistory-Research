# R223 S19 未测混杂敏感性参数误设网格：计算前冻结协议

日期：2026年10月28日。主线 R223 的新增有限人工 E1 机制检验。既有 R223 09-014 正式有限 E1 结题维持原状。该 S19 不扩张原239目录完成数。

## 固定输入与来源

输入固定为 `research/R223/R223_EXACT_RESULTS.json`，Git blob `3a3f2143357832e25ddf483d7ebd4d66298c5dd1`，其七世界来自 `R223_ALL_448_ORIGINAL_CONFOUNDING_STRUCTURAL_ATOMS.csv`，Git blob `7a4b6a94332618abe8a8471a656db0353da0ae1f`。本轮仅在已冻结的世界与结果上增加敏感性假设网格；不修改世界、观察联合分布、潜在结果、E-value、原来源或原协议。所有七世界的 `observed_RR`、`true_causal_RR`、`oracle_sensitivity_RR_EU`、`oracle_sensitivity_RR_UD` 必须与该 JSON 完全一致。

## 预先规定的252个条件

每个世界交叉 `Gamma_E` 和 `Gamma_D`，二者都从整数集合 `{1,2,3,5,7,15}` 取值，共七世界乘36等于252条件，顺序为原世界顺序、Gamma_E升序、Gamma_D升序。全部使用有理数，`B=Gamma_E*Gamma_D/(Gamma_E+Gamma_D-1)`，`RR_lower=RR_observed/B`。定义 `null_compatible` 为 `RR_lower<=1`；此标记仅表示单侧下界是否允许无效应，不能判定真实因果效应存在或不存在。对 `observed_RR=1` 的反向因果世界也按同一公式记载，但不据此声称识别了保护效应。

对六个全部U×T有支持的世界，只有 `Gamma_E>=oracle_RR_EU` 且 `Gamma_D>=oracle_RR_UD` 才允许标记 `oracle_parameter_covered=true`。在该条件下检查 `RR_lower<=true_causal_RR`，违反则为严重FAIL。对NO_POSITIVITY，oracle参数未定义，覆盖标记必须为null，绝不将假定网格当作从数据识别出的真实混杂强度。

另固定两个反例：NULL_CONFOUNDED和CAUSAL_ALIAS在全部36个相同参数格具有相同观测下界及相同null兼容性，却有不同真实RR；NULL_CONFOUNDED在(3,5)应有 `RR_lower=77/75>1`，在(3,7)应有 `RR_lower=33/35<1`。所有网格结果属于敏感性假设下的数学演算，不能声称现实人群的识别保证。

## 事先固定的独立核验与负例

R轨采用逐格有理数公式。B轨使用独立的阈值不等式核验：`RR_lower<=1` 当且仅当 `Gamma_E*Gamma_D >= RR_observed*(Gamma_E+Gamma_D-1)`。另核验每世界 B 随 Gamma_E 或 Gamma_D 不下降，RR_lower 不上升；当 Gamma_E>RR_observed 时，`Gamma_D >= RR_observed*(Gamma_E-1)/(Gamma_E-RR_observed)` 与 null 兼容性等价；当 Gamma_E<=RR_observed 且 RR_observed>1 时，有限 Gamma_D 无法使下界严格小于或等于1（Gamma_E=RR_observed 时只有 Gamma_E=RR_observed=1 的退化例外）。必须有可执行的错误注入负例，故意改动一个格子的下界后被复核拒绝。输出252行机器可读 CSV、汇总收据、R和B脚本及科学报告，必须可复算。报告逐项披露所有FAIL或未运行事项。

## 证据、冻结与成本

E1人工机制，新增真人E2=0、历史E3=0、外部独立团队复现=0。R073模型和评分规则、PESEN v0.1保持冻结。与其他工作流分开路径；原始239 v7.8索引和154项待核队列只读。使用本地或现有工具，禁止计费 API、付费云和未经免费额度核实的Actions。该协议须在本轮任何 S19 网格计算前单独提交，后续不得追认探索性更改为预先冻结。