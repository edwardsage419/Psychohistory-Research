# B轨：R269 S65 非盲态双算法独立复算与持久化收据审计

日期：2026-10-29 UTC。目标键：`(B,R269,S65,postselection-new-group-risk-vs-independent-binomial-oracle)`。研究者已阅读 R269 原始数学和既有报告，属于**内部非盲态方法复核**。不存在外部团队或独立研究机构复现。

## 先冻结再执行

新增 S65 预测目标的冻结协议提交 `88f69ecaee497050365b9ea15c5780cec6694b33`，在本轮新结果计算之前。原 R269 研究及原始有界 E1 机器验收未修改。两条路线均保持 p∈{1/4,1/2,3/4}、六个独立潜在群组、每组两行、三候选模型、两种 CV、同分优先顺序以及第七独立新群组目标不变。

## 路线R，原生Python标准库Fraction

本地实际执行 `python r269_s65_postselection.py --selftest --emit ... --check ...`，退出码0。该程序显式重建全部 192 种六位训练来源，对每种来源和三候选重建逐行 LOOR 与完整群组 LOGO 的预测折次，按正确设计质量加权，并在完全独立的第七群组上积分。共 13,824 次逐行折次评分。

原生Python还通过5项预定收据篡改负例，分别为未来风险篡改、选择质量篡改、缺少一个p、E1升级为E2、布尔值伪装数字。五项全部按预期拒绝。该 Python 文件尚未写入 GitHub，本轮只归档 JavaScript 独立路线及科学报告，保留 `PYTHON_NATIVE_SOURCE_ARCHIVE=OPEN`。

## 路线B，独立BigInt二项分布计算

[归档源码](../validation/r269_s65_binomial_fraction_oracle_20261029.js)，Git blob `5022ecb292a83e9008c3868ce05068590b8681d0`。该路线按 K=0..6 的二项质量计算，不使用Python的逐行折次函数。每个K用群组对称性计算LOOR和LOGO候选分数，并独立计算第七组Brier风险。BigInt精确分数运算避免浮点容差。

V8中实际运行归档源，结果与Python原生Fraction路线全部六项未来风险、六项选择概率向量、六项同分质量、六项选中CV分数、六项乐观差、三项配对风险差、九项固定模型风险一致。按原始分数字符串比较，差异0。

[远端持久化收据](../validation/R269_S65_POSTSELECTION_EXACT_RECEIPT_2026-10-29.json)，Git blob `1a071efc8947d986fb175914671835654f7a1040`。写入后重新从GitHub读取归档JS和JSON，在V8执行归档JS，全部嵌套字段和值与持久化JSON严格一致。另有3个p下LOGO未来风险、配对差值和Laplace选中质量的显式独立Python结果断言。

## 科学性审计

* **训练/验证泄漏**：LOOR确实保留同组复制行，群组记忆器全部来源CV为0，未见组风险1/4。LOGO完整排除目标群组，避免这一特定泄漏。
* **真正样本外目标**：第七群组独立于六个训练群组，使用已冻结Bernoulli(p)分布进行精确数学积分。属于E1理论生成分布的样本外目标，未采集真实新群组。
* **基线**：记忆器与常数半概率固定风险1/4；固定Laplace风险为83/392、55/196、83/392。
* **选模偏差**：LOGO选择后的CV最小值在三个p下均比真实新群组风险乐观。p=1/2时LOGO新群组风险425/1568，高于LOOR的1/4。
* **概率校准、重采样和不确定性**：有精确设计概率与期望，尚无真人校准曲线、置信区间或群组层bootstrap；这些对于本轮有限人工全枚举目标并非必要，但现实推广仍OPEN。
* **反例**：整组CV可以比逐行CV的新群组风险更差，说明“避免泄漏”不保证有限样本选模永远更优。
* **结论范围**：只支持六组双重复人工模型下的精确E1反例。新真人E2=0、真实历史E3=0，R073与PESEN v0.1保持冻结。

## 验收状态

`INTERNAL_EXACT_CROSS_ALGORITHM=PASS`。
`PERSISTED_JS_V8_REPLAY=PASS`。
`PYTHON_NATIVE_EXECUTION=PASS_LOCAL_ONLY`。
`PYTHON_SOURCE_REMOTE_ARCHIVE=OPEN`。
`ARCHIVED_NODE_NATIVE_CLI=NOT_RUN`。
`EXTERNAL_INDEPENDENT_REPLICATION=NOT_RUN`。
`CI_NEW_RUN=NOT_RUN`。

没有运行付费服务、GitHub Actions或计费API；账户实际账单与免费额度未核验。下一阶段先归档并回读Python完整来源，再运行其原生CLI与远端JSON对照，之后再考虑正式S65有界验收。代码运行通过与原R269科研验收是两个不同的判断。
