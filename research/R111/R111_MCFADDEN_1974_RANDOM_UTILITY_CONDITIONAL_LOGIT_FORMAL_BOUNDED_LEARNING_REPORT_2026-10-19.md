# R111：随机效用模型与 McFadden 条件 Logit，正式有限模型学习报告

日期：2026-10-19。此研究严格承接原2026-10-14知识候选目录 P0 条目 01-005 Random Utility Model，聚焦一个数学模型的学习与可复现纯合成检验。R111是本次逐项研究编号；01-005是历史候选目录的知识编号，互不等价。阶段A已编写标准库原理实现和18项自含检验。原始真人数据未拟合。

## 第一手来源
1. Daniel McFadden (1974). Conditional Logit Analysis of Qualitative Choice Behavior. In: Zarembka, Frontiers in Econometrics, pp.105–142. 作者伯克利自存原章 https://eml.berkeley.edu/reprints/mcfadden/zarembka.pdf 。本轮实读原文印刷第113页（PDF索引8）式(16)与重复选项的汽车、巴士反例，以及印刷第114页（PDF索引9）对于条件logit和不可辨识的说明。
2. Kenneth Train (2009), Discrete Choice Methods with Simulation, Second Edition. 作者官方教材目录 https://eml.berkeley.edu/books/choice2.html ，出版社 Chapter 3 https://www.cambridge.org/core/books/abs/discrete-choice-methods-with-simulation/logit/957AE41EA000543CB07031602059C6AD 。

上述来自作者与出版社的数学文献索引；本研究仅复现可解析概率规则，**没有作者数据拟合或实人分布认证**。

## 机制与可计算公式

对于人n可选集合 B_n 中的备选j，随机效用为 U_nj=V_nj+eps_nj，选择最大效用者。若 eps_nj 独立同分布，服从相同尺度 tau>0 的 Type-I 极值（Gumbel）分布，则

P_nj = exp(V_nj/tau) / sum_{k in B_n} exp(V_nk/tau).

McFadden原1974条件logit式(16)是线性于参数的系统效用 V_nj=z_nj' theta 下同类选择概率；其估计和效用解释依赖实际可选集、可观测属性及误差假设。tau与效用参数同尺度变化时概率不变，因而若同时估计两者必须作尺度归一化。所有备选共同平移一个常数也不改变概率，跨选项不变的解释变量不能在该模型内直接辨识独立效用系数。

模型可检验关系：
1. 概率非负、总和为1，非可选选项概率为0。
2. 加常数 a 到所有V，P不变；正比例同时缩放V和tau，P不变。必须约束效用基准和噪声尺度。
3. 两选项a、b的概率比 P_a/P_b=exp((V_a-V_b)/tau)，与其它选项无关，即IIA。
4. tau趋向0时倾向最大V的备选；tau趋向无穷时趋向可选集均匀概率。
5. 独立Gumbel抽样最大效用的蒙特卡洛选择频率应接近解析Logit概率。这是**人工随机数验证**，不构成人类决策行为的实证证据。

## 重要反例和适用边界

伯克利原文第113页直接警告极相似选项下的IIA。令汽车系统效用 log(2)，单种巴士效用0，则模型给汽车选择2/3。仅复制为红巴士与蓝巴士且系统效用同为0之后，汽车概率由2/3下降到1/2，两巴士各1/4。若新增选项与原巴士高度相似，这种按比例改写全部选项份额的性质可能不合理。该反例揭示可替代品误差相关时独立极值误差假设的边界；它**不证明所有随机效用模型都具有IIA**。Probit、混合logit等能容纳更广的相关结构，但其独立评估属后续模型任务。

## 程序、检验与科研分级

代码：r111_mcfadden_random_utility_conditional_logit.py
测试：test_r111_mcfadden_random_utility_conditional_logit.py

纯标准库实现稳定归一化、可选集mask、系统效用特征与系数线性组合、数值稳定的极低概率负对数似然、固定种子iid-Gumbel Monte Carlo与红巴士蓝巴士反例。预设合成案例覆盖18项：归一、平移、尺度识别、不可用备选、IIA、温度极限、梯度有限差分、特征效用、NLL高稀有选择数值稳定、随机模拟一致性以及非法输入失效。不得把这些模拟结果写成受试者数或E2真人预测。

模型学习的边界：这是一个具有明确解析式、参数辨识条件及可复算实现的理论/统计模型；没有对R110数据建立随机效用拟合，更没有检验真实群体模仿或长期历史定律。若CI全部通过，可记录 LEARNING_COMPLETE_BOUNDED_FOR_MATHEMATICAL_MECHANISM_AND_SYNTHETIC_IMPLEMENTATION；真实效度、群体跨情境识别和未来前瞻预测仍为空白。PESEN v0.1保持冻结，暂不与其它R模型熔炼。
