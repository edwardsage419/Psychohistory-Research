# R281 对数预测评分：15人工Bernoulli世界、240完整有序原source与符号对数无穷风险；事前冻结

日期：2026-10-23 Asia/Taipei。原239目录12-011 Logarithmic Score（P1），研究编号R281。理论基础：Good (1952), *Rational Decisions*, Journal of the Royal Statistical Society B 14(1):107–114, https://doi.org/10.1111/j.2517-6161.1952.tb00104.x；Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378, DOI https://doi.org/10.1198/016214506000001437，原作者公开论文 https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf 。研究是自行建立的有限人工概率检验，未用原论文数据，未声称提出新的严格适当评分理论。

## 冻结原生成与预测空间
真实数据机制p∈{1/4,1/2,3/4}。每source四个独立Bernoulli(p)有序二元bit（共2^4=16种完整原source），来源质量p^K(1−p)^(4−K)，K为四bit成功数。固定报告q∈{0,1/4,1/2,3/4,1}，报告在观察bit之前已经完全冻结。3真率×5报告概率＝15人工world，合计**240个带world标识完整source配置**；同一真实p下五种报告政策重复使用完全相同16个原source，不能将240说成240份独立人类实验。

单条对数损失定义 `L(q,y)=−ln(q)` 若y=1，`L(q,y)=−ln(1−q)` 若y=0。约定`−ln 0=+∞`。固定四bit来源的平均损失只要存在一次+∞即为+∞；**禁止人为截断预测概率、把∞替换为有限哑值或在完整期望中剔除无穷来源**。

## 精确符号对数表示
因为报告q属于{0,1/4,1/2,3/4,1}，所有有限单次loss精确表示为 `a*ln(2)+b*ln(3)`，系数a,b均是有理数，不依赖浮点近似：
- q=1/4，对y=1为2 ln2，对y=0为2 ln2−ln3；
- q=1/2，两种y都是ln2；
- q=3/4，对y=1为2 ln2−ln3，对y=0为2 ln2；
- q=0，仅y=0时loss0，遇y=1为+∞；
- q=1，仅y=1时loss0，遇y=0为+∞。
四bit逐source保存每个row的符号系数或INF标记、source平均有限score的ln2和ln3有理系数及INF标志、精确原质量。

## 冻结十五world真值
对0<q<1，真p下的期望对数损失（四次平均与单次风险相同）：
* q=1/4：`2 ln2 − (1−p) ln3`；
* q=1/2：`ln2`；
* q=3/4：`2 ln2 − p ln3`。
真实分布自身的理论熵H(p)=−p ln p−(1−p)ln(1−p)；上述q=p时风险恰是H(p)。总体期望regret等于 `D_KL(Bernoulli(p)||Bernoulli(q))≥0`，仅q=p等号成立。数值近似只能作为辅助；有理系数*符号ln常数是正式精确归档形式。

当q=0时，完整四bit有至少一个1发生INF损失的原质量为`1−(1−p)^4`；当q=1时，只要有任何0就发生INF，原质量`1−p^4`。其期望对数损失**严格+∞**，因为三种真p全部严格内点；尽管全0来源令q=0报告的四条平均得分0，全1来源令q=1报告同为0，也不能把这些偶然完美样本评分误认为未来可实施的最优预测。

## 独立路线与正式结题协议
路线A枚举十五world各16个有序原source，按四个观察逐行计算符号log2/log3系数或INF，保存全source精确质量并汇总每world正式期望有理符号表达式或无限质量。
路线B完全不读取原source枚举，利用K∼Binomial(4,p)五个类别与单次Bernoulli(p)二类别解析求出相同正式对数系数、q=0/1下发生INF的完整事件概率，以及strict propriety KL形式，双方逐Fraction一致。该路线不声称用有理系数独立证明ln2/ln3值的代数无关性，严格适当性由已知KL非负数学定理提供理论证明。
路线C GitHub Actions独立第三job读取全部240原source CSV，真正重算四bit及其概率、四个符号loss/INF标志、每个world准确期望系数或无限事件质量，核对机器CSV/JSON SHA256。

必须先冻结上述完整协议并存GitHub main的commit SHA，后写标准库Python3.11/3.12各≥45真unittest、独立第三来源审计、240完整CSV和结果JSON及SHA256机器人永久归档，全部3job completed/success方可人工E1有界结题。没有真实人类E2或历史E3，也无新外部预测试验，R073/PESEN v0.1保持冻结。下一原目录12-012 Open Reproducible Workflow and ODD（拟R282），遵守先全R研究、再统一归纳分类、最后熔炼。
