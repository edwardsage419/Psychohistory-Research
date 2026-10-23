# R281 正式科学报告：对数预测评分严格适当性、精确符号风险及零概率无穷损失

日期2026-10-23 Asia/Taipei。原239模型目录12-011 Logarithmic Score（P1），研究R281。证据为**有限人工数学E1**，不含真人或历史数据。

## 第一来源
I.J. Good (1952), *Rational Decisions*, Journal of the Royal Statistical Society B 14(1):107–114，DOI https://doi.org/10.1111/j.2517-6161.1952.tb00104.x；Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378，DOI https://doi.org/10.1198/016214506000001437，原作者公开文本 https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf 。这是自行构造的边界预测与完全人工四次独立二元原source实验，没有作者历史数据或心理机制实证复现。

## 预评分冻结与形式化精确表示
[冻结源协议](../../protocols/R281_LOG_SCORE_15_WORLDS_240_COMPLETE_SOURCE_SYMBOLIC_FREEZE_2026-10-23.md)，独立GitHub提交[cbf8eec7](https://github.com/edwardsage419/Psychohistory-Research/commit/cbf8eec7db1ab7d78e4c8d3a03b0e0ae5acad2f3)。三个人工真率p∈{1/4,1/2,3/4}和五个固定报告概率q∈{0,1/4,1/2,3/4,1}，形成**15个人工world**；每world原四个相互独立同p Bernoulli bit的16种完整有序来源，准确原概率p^K(1−p)^(4−K)，合计**240个world标识完整source类型**；同p下五种政策共享同一个16源随机空间，绝不能将240理解为240个独立真人。

单行负对数损失：发生事件y=1时L=−lnq，否则L=−ln(1−q)；任意预测为0概率的真实发生事件立即导致+∞损失，四行source平均只要有一条INF即为INF。不对q做epsilon裁剪、不静默抛弃含INF来源、不将Infinity置换为数值零。

正式结果并非浮点近似。所有有限单次loss及完整有限source平均，均用**精确有理系数对数表达式**`a ln2+b ln3`记账：
* q=1/4：y1对应2ln2，y0对应2ln2−ln3；
* q=1/2：两种y均ln2；
* q=3/4：y1对应2ln2−ln3，y0对应2ln2；
* q=0或1：匹配极端类别的单行loss为0，任何矛盾类别为+∞。
保存全部原source每个row损失token（两有理系数或INF），完整source平均有理系数或INF标志。

## 两条独立数学路线及完整真值
路线A枚举每world全部16种有序原source，完整逐行精确符号loss，按真p有理原质量对正式有限log2/log3系数积分，或计算出现任意INF的真实概率质量。
路线B**不调用有序source生成**，利用K~Binomial(4,p)五类别以及独立单次真Bernoulli(p)概率，直接推导如下世界级期望符号表达式与边界∞概率：
```text
If q=1/4: E[L] = 2 ln 2 − (1−p) ln 3
If q=1/2: E[L] = ln 2
If q=3/4: E[L] = 2 ln 2 − p ln 3
If q=0: E[L]=+infinity,  P(a fourbit source contains INF)=1−(1−p)^4
If q=1: E[L]=+infinity,  P(a fourbit source contains INF)=1−p^4
```
对于内点q，理论超额风险E[L(q,Y)]−E[L(p,Y)为二元KL散度`D_KL(Ber(p)||Ber(q))≥0`，且q=p时为0。源码保存精确有理对数基系数，KL严格非负性的**理论依据是已知Gibbs不等式**；仅在测试中对非零符号表达式辅以浮点近似的符号正检查，不据此虚构一个新的机器有理证明ln2、ln3不等式。全部15世界的A/B来源概率质量及精确表达式逐Fraction一致。

|真p|q=0事件∞概率|q=1/4期望L|q=1/2期望L|q=3/4期望L|q=1事件∞概率|
|---|---|---|---|---|---|
|1/4|175/256|2ln2−(3/4)ln3|ln2|2ln2−(1/4)ln3|255/256|
|1/2|15/16|2ln2−(1/2)ln3|ln2|2ln2−(1/2)ln3|15/16|
|3/4|255/256|2ln2−(1/4)ln3|ln2|2ln2−(3/4)ln3|175/256|

三种真实p均是0<p<1，故q=0及q=1两个极端报告的总体未来期望对数loss严格+∞。其有限四次样本中仍有正概率恰好全0或全1，从而source评分全零；这属于有限样本碰巧没有违背错误极端预测的事件，不能把它当成真实预测器具有零泛化风险的证明。与有界Brier评价相比，log score极端概率风险具有更加严重的性质，但两个评分评价的用户目标可能不同，不能混淆为一律优选某种度量。

## 执行、缺失证据与归档
[可运行原生Python程序](r281_exact_symbolic_log_score.py) · [完整240有序原source精确符号CSV](R281_ALL_240_ORIGINAL_LOG_SCORE_SYMBOLIC_SOURCES.csv) · [正式十五世界期望和无穷事件结果JSON](R281_EXACT_RESULTS.json) · [SHA256机读收据](R281_MACHINE_RECEIPT.json)。

[GitHub Actions run39905387817](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905387817)：Python3.11与3.12各134真实unittest，共268项通过；第三独立全部240个原source审计、完整INF标记重算、精确有理系数验证、SHA256审核及机器人永久归档均成功，三job completed/success。原CSV和分析结果SHA256永久main提交[commit d038a6b9](https://github.com/edwardsage419/Psychohistory-Research/commit/d038a6b9794152463bf05e058c3d43c22f197cb6)。

原source SHA256 `02d4a5d8ae9f4da9a580185e0fb09ff0a7b553d98d2c9544f6d285a29ca68fd2`，结果JSON SHA256 `b73358d184daebd3bdf4ed46484e257f92b0ec379cf39104d508d58dd226c5b8`。

全部科研证据仅人工E1，无真实新真人E2或真实历史E3、无R073真人复现、无PESEN v0.1更新。下一原目录12-012 Open Reproducible Workflow and ODD（拟R282），之后按顺序完成剩余原R候选，再统一归纳分类，最后熔炼。
