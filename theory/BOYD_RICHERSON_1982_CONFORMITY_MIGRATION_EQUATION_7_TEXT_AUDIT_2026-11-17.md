# Boyd 与 Richerson（1982）：从众传播及迁移递推式的原文一致性审查
track: theory
run_date: 2026-11-17 Asia/Singapore
observed_head: 36f8104a118903536040f38c3197c4c18d1c5541
target_key: (theory,Boyd-Richerson-1982,Human-Ecology-10-3-325-351,Eq7-vs-footnote-and-life-cycle)
status: PARTIAL; PRIMARY_OPEN_PDF_TEXT; SOURCE_TYPO_UNCONFIRMED; NO_EMPIRICAL_VALIDATION

## 原始来源与实际阅读
Robert Boyd and Peter J. Richerson (1982), “Cultural Transmission and the Evolution of Cooperative Behavior”, *Human Ecology* 10(3), pp. 325–351; stable JSTOR https://www.jstor.org/stable/4602658 ; 作者大学站点公开PDF https://www.des.ucdavis.edu/faculty/richerson/BoydRicherson1982.pdf 。本轮实际阅读 pp. 325–335 的正文、Table I、Eq. (1)–(9)及脚注推导。后续 pp. 336–351 未完整审读。来源为原始论文扫描的可检索文本，未核逐页图像与其他刊本勘误。

## 新增高价值疑点：Eq. (7) 与作者自身推导的阶段符号
p. 332 Fig. 1 将生命周期顺序列为文化传递 q'、文化选择 q''、迁移形成下一代 q。p. 333 Eq. (4) 定义选择后的 q''。然而本PDF可检索文本 p. 334 Eq. (7) 迁移公式的第一项显示 (1-m)q'_{i,t}，第二项显示 (m/n)Σ q''_{j,t}。同页至 p. 335 脚注5将迁移更新写成 (1-m)[q_i+F(q_i)]+(m/n)Σ[q_j+F(q_j)]，即两项均使用选择后的状态。若 Eq. (7) 第一项确实为 q'，则在 m=0 时下一代频率忽略文化选择，与 Fig. 1 及脚注推导不一致。该疑点可能来自扫描识别、原刊排印或作者实际公式错误，尚未查证原刊页图，不得将其断言为已确认勘误。

## 独立代数核查
在无迁移 m=0、文化传递后 q'=0.6、选择存活权重 V_C=2、V_D=1 时，Eq. (4) 给 q''=0.6*2/(0.6*2+0.4*1)=0.75。按生命周期下一代应为0.75；按可检索 Eq. (7) 第一项则为0.6。此为构造性逻辑反例，证明两种公式不可同时作为一般更新律。它不验证任何真实社会行为，也不证明作者原刊存在错误。

## 机制与竞争解释
p. 330 Eq. (2) q'=q+Aq(1-q)(2q-1) 仅在三位文化示范者随机抽样及 Table I 所定传递概率下成立。p. 333 Eq. (3) 又加入直接偏向 B_i；Eq. (4) 加入不同文化类型进入下一代示范者池的机会；p. 334迁移进一步改变局部频率。观察到群体规范增加，不能仅由频率变化排他识别从众、直接偏向、文化选择或迁移。作者 p. 334 明确承认变化环境中旧适应性行为可能因偏向延续。与已有 TH188、Henrich/Boyd 1998 和 Cavalli-Sforza/Feldman 1981 记录存在交集，本轮唯一独立增量为 Eq. (7) 与内部生命周期/脚注的可复核符号冲突；不新增TH编号。

## 未解决及验收
必须查看 p. 334 的原始影像、刊本更正及原作者后续推导；确认究竟是OCR还是原刊排印问题后才可标记公式勘误COMPLETE。未读 pp.336–351，未做数据拟合、行为实验或历史预测。C 2026-11-17 新增合格成果未核实，D 2026-W47 D005 完整验收仍 PARTIAL。R验收关闭0，R073/PESEN v0.1及证据等级不变。程序测试 NOT_RUN；CI NOT_RUN；账户账单 NOT_VERIFIED；无主动收费服务调用。

## 2026-11-17 原刊扫描页图校勘：撤销公式疑点（COMPLETE）
source: https://www.des.ucdavis.edu/faculty/richerson/BoydRicherson1982.pdf ，PDF第11页（零起始索引10），印刷页334，直接查看扫描页图而非OCR文本。
原刊影像中的公式(7)明确为 q_{i,t+1}=(1-m)q''_{i,t}+(m/n)Σ_{j=1}^n q''_{j,t}。两项均使用双撇 q''，与该页脚注5的 q''=q+F(q)、生命周期图及选择后的迁移顺序一致。先前基于可检索文字推断第一项是 q' 的怀疑，已被原刊影像证伪，属于文本识别误读。上文“Eq.(7)冲突”段落仅保留为历史审查记录，不再作为开放科学缺陷、作者勘误或新理论成果。此前 m=0 时0.6与0.75的反例仅对误读公式成立；正确公式给出0.75，内部一致性通过这一测试。原刊公式(7)影像核对验收 COMPLETE；整篇论文其他公式与 pp.336–351 审读仍 PARTIAL。未触发CI或行为验证。研究关闭1项文献校勘疑点，R科学验收关闭0项。
