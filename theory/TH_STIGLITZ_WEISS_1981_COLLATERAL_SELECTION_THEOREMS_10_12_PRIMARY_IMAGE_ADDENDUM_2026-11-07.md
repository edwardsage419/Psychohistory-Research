# Stiglitz 与 Weiss（1981）抵押品的双向作用：原刊定理10至12图像审读

track: theory
subflow: theory
run_date: 2026-11-07 (Asia/Shanghai)
observed_head: 737777484a93074588e52a4c8b8316797daf8b9c
target_key: (theory,StiglitzWeiss1981,AER71-3,collateral-selection-theorems-10-12)
status: PRIMARY_IMAGE_SPECIFIED_PAGES_READ; CONDITIONAL_THEORY_NOTE; NO_EMPIRICAL_VALIDATION
source: Joseph E. Stiglitz and Andrew Weiss (1981), Credit Rationing in Markets with Imperfect Information, American Economic Review 71(3):393–410.
stable_link: https://www.jstor.org/stable/1802787
open_scan: https://www.econ.puc-rio.br/mgarcia/Macro%20II%20-%20Mestrado/StiglitzWeiss1981.pdf
reading_scope: 原刊p400（定理7、8和式13、14）、p404（图7、式23至25、定理10至12）、p405（定理12证明、图8和后续动态机制开头）；其余pp401–403、406–407本轮未逐页审读。
source_type: original-journal scan, page images inspected; no redistribution.

## 新增独立理论命题及条件

p400定理7指出，在给定利率处风险中性借款人对两项目无差异时，升息会使其偏好破产概率更高的项目。式(13)为 E[max(R^i-(1+r)B,-C)]；式(14)在该处给出对r的导数 -B[1-F_i((1+r)B-C)]。对不同项目的导数差异由偿付概率决定，故在无差异点风险更高项目的借款人效用下降较慢。该比较是局部的，不能推断所有利率下都偏好高风险。

p404定理10在递减绝对风险厌恶等条件下，财富较高者可能选择更高风险项目。p404定理11的陈述是对**同一给定借款人**提高抵押要求可提高银行回报，形式为 dp/dC>0；证明依赖该模型的项目选择一阶条件。p404定理12指出抵押要求提高可能产生逆向选择，使获贷者的平均和边际风险升高，形式 dW0*/dC>0。p405图8展示银行平均收益随抵押要求上升而出现向下跳跃的可能性；p405文字明确说明选择效应可超过同一借款人层面的直接收益效应。

由此需严格区分两个估计对象：固定借款人类型的抵押条件效应，与允许申请及融资参与组成变化的银行平均回报总效应。前者正向不保证后者正向。该机制的成立取决于风险厌恶、财富分布、抵押和融资参与门槛及项目集合的模型假设。

## 构造性逻辑核查

设低抵押条件下两类借款人银行回报分别为1和3，各占一半，平均为2。提高抵押后，各类型固定条件下回报分别升至1.2和3.2，但申请池变成低回报类型占90%，则平均回报为0.9*1.2+0.1*3.2=1.4，小于2。这个人工算例只验证组成变化能够压过组内改善的算术逻辑；没有证明原著的财富选择阈值、风险排序或完整均衡，也没有任何真人数据。

## 竞争解释、层级与识别

现实抵押提高还可能同时改变贷款需求、法律执行、贷款规模、银行资金成本、担保资产价格与宏观信用周期。若仅观察抵押比例和违约率，获贷样本选择、抵押品估值与风险类型的不可观测性使因果机制不可识别。候选观测量包括申请人财富、报价、抵押、拒贷、项目风险及获贷后行为，需有可审计的外生抵押变化及申请人全样本。

个人层级为财富和项目风险选择，组织层级为银行筛选，制度层级为抵押执行规则；未推断历史层级预测。此处与同日既有信贷配给记录为同一原著不同核心问题的补强，无新增TH编号、无项目级融合。

## 进度与边界

C013当日已有2026-11-07记录；D003本周2026-W45已有2026-11-02记录，本轮均只读。
R073、PESEN v0.1保持冻结；R E1/E2/E3及MARKET证据等级隔离。
原刊指定页图像阅读COMPLETE；构造性算术核查COMPLETE；pp401–403、406–407阅读NOT_RUN；完整数学模型复算NOT_RUN；真人实验NOT_RUN；历史因果验证NOT_RUN；CI NOT_RUN；新增收费服务未使用，实际账户账单NOT_VERIFIED。
下一步优先转向弱覆盖学科原著；如回访本文则核对pp401–403和406–407的全部推导，不重复建立主题编号。
