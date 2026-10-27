# R220 S16：独立人工pilot联合估计倾向与结果模型的未来AIPW风险，计算前冻结

日期：2026-10-27（Asia/Singapore）。状态：PRESCORE_FROZEN。证据等级：E1人工。原239目录09-011，原R220正式有限E1验收保持不变；本补充不新增原239完成条目。冻结前main HEAD：`f546d9fbf0c5bec6a0f498a1427cf0842e25b2d6`。

## 原始来源和不可变条件

严格复用 `protocols/R220_DOUBLY_ROBUST_7_WORLDS_1537_ORIGINAL_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md` 与 `research/R220/R220_EXACT_RESULTS.json` 中七个人工世界、8个未来单位、X=(0,0,0,0,1,1,1,1)、U=(0,0,1,1,0,0,1,1)、Y0=2X+2U、Y1=Y0+2、真实ATE=2、真处理分配p、原公开q/m与正值性定义。原CSV和原正式收据不修改。完整正值性六世界各有256个未来处理赋值；无正值性世界继续严格输出null。

## 新增的独立人工训练与未来评价

另建8个带P标识的人工pilot单位，按同一八个结构类型克隆潜在结果生成机制，pilot处理与未来F标识的8单位处理分别独立按真p伯努利生成。pilot和future不存在相同单位ID，尽管结构类型完全重复。完整pilot 256种赋值，完整future 256种赋值。六个正值性世界共6×256×256=393216个联合赋值可能性；用精确有理数对pilot分布求和，用独立未来伯努利条件矩计算风险，不声称393216个真人样本。

每个X层有4个pilot。仅用pilot实际Z和Yobs学习：`qhat(x)=(1+sum Z)/(6)`，取值1/6至5/6；`mhat_t(x)=sum[1(Z=t)Yobs]/(1+n_t)`，固定零先验与伪计数1。该m估计器允许n_t=0并返回0。不得读取pilot反事实、隐藏U、未来Y、未来Z或未来真p以训练任何模型。真p仅用于人工来源概率、审计和未来积分。

## 事前冻结的五种评价方法

1. `PILOT_BOTH_AIPW`：qhat与mhat。
2. `PILOT_Q_TRUE_M_AIPW`：qhat与已知X层人工真潜在均值m0=2X+1、m1=2X+3；这属于明确标记的特权模型对照。
3. `TRUE_X_Q_PILOT_M_AIPW`：已知X层真平均处理概率qX（普通1/4与3/4，弱重叠1/16与15/16，隐藏U按X平均1/4与3/4）与mhat；特权倾向对照。
4. `PILOT_OUTCOME_ONLY`：mhat1−mhat0的8单位均值。
5. `ORIGINAL_FIXED_AIPW`：原R220公共固定q与m，作为无训练的旧基线。

所有未来AIPW仍用原冻结公式。对于六个正值性世界，分别报告完整pilot与future联合期望、方差、偏差、MSE；结果必须满足MSE=Var+bias²。无正值性世界的五方法因果识别结果均为null，即使pilot qhat有数值也不能绕过真实缺乏支持域的阻塞。对所有正值性世界pilot概率和与future概率和均精确为1。

## 审计与预先指定的负例

R轨用BigInt精确有理数计算pilot分布和未来独立Bernoulli条件矩。B轨使用单独实现的全联合pilot×future赋值枚举，逐世界、逐方法对期望与MSE比较，允许浮点容差1e-9。必须检查完整来源数、原R220固定AIPW基线严格相同、两个模型均由pilot估计时的风险与特权对照差异、隐藏U违反交换性、无正值性返回null。执行一个可检出的错误注入：把未来某单位真实Y1改为Y1+1，确认至少一个世界的PILOT_BOTH_AIPW风险改变。执行一个时间泄漏负对照：将future Z混入pilot倾向计数，应检测与冻结qhat不一致；不得把该错误流程的分数当有效结果。

A轨另行调查真实公开数据的身份、时间、行为和许可，不能与E1混合。R073模型和评分、PESEN v0.1冻结；个人辅助决策产品暂停。新增CI须先核验免费额度，否则NOT_RUN；不引入费用。
