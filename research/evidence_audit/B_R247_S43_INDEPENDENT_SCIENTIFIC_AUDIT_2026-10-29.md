# B轨 R247 S43：冻结人工来源的独立整数分组审计

日期：2026-10-29。审计等级：项目内部方法独立的程序性复核。原R247正式结题资格未改变。

## 冻结和输入隔离
预计算协议 `protocols/R247_S43_OBSERVED_GENERATION3_SURVIVAL_BRIER_PRESCORE_FREEZE_2026-10-29.md`，先行冻结commit `5a5f82b57f499486a0ff6ecdafa06c188bf74dda`。R轨读取原R247四代可见路径联合概率JSON，B轨独立从2304条原始八bit来源CSV直接计数。B轨不调用R轨函数，不从R收据推导结果。

B轨原始来源blob `42de5332f4aafae65487a71f03fc0dce5beb59df`；每world256行，每行1/256。对八外生bit组合检查唯一性和完整性；在传感器别名世界检查所有真实H3=0。保留不活跃潜在父节点对应的原始来源，避免选择性样本缩减。

## 真实执行与复核
独立源码 `research/evidence_audit/b_r247_s43_independent_source_counts_20261029.js`。对F0/F1/F2/F12合法前缀的正支持组，以整数计数计算风险 `Σ s(m−s)/(256m)`，与R轨逐路径平方误差积分的结果比较。

B轨执行2350项已计数来源、结构、分组和别名检查，失败0。独立比对九世界×四前缀×风险及支持数两字段，共72项比较，失败0。R轨另完成118项检查。人为将IID_FAIR_0_OR_2的F12风险改为999，审计比较成功拒绝。非法加入未来Y3的完美预测只用于泄漏负例，不算合法性能。IID和隐藏传感器别名两世界的可见风险与支持数全部一致。

B机器收据：`research/evidence_audit/B_R247_S43_INDEPENDENT_COUNT_RECEIPT_2026-10-29.json`。复算命令：

```sh
node research/validation/r247_s43_observed_survival_brier_20261029.js > /tmp/r247_s43_R.json
node research/evidence_audit/b_r247_s43_independent_source_counts_20261029.js research/R247/R247_ALL_2304_ORIGINAL_BINARY_TREE_FAMILY_SOURCES.csv /tmp/r247_s43_R.json
```

## 验收边界
九世界全部是人工E1，原R247三代分支机制不变。Brier概率使用人工真分布，校准属于定义内结果；无真实样本外训练测试、无独立真人实验、无真实历史验证、无重采样不确定区间需求。错误注入仅证明比较器对该变异敏感。未执行外部研究者独立复现。R073与PESEN v0.1冻结。

本轮未运行新增GitHub Actions，是否有对应commit CI须在写入后另行核查。主动新增费用0；GitHub免费额度和实际账单未独立核验。