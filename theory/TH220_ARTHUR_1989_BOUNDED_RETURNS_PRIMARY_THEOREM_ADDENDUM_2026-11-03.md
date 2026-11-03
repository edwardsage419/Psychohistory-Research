# TH220 Arthur (1989) 原始技术竞争模型与有界收益边界补记

track: theory
subflow: main_theory
run_date: 2026-11-03 (Asia/Singapore)
observed_head: 7a93b8e793b177654a85d63797751c71568bc086
target_key: (theory,Arthur1989,original-Economic-Journal-99-394,unbounded-vs-bounded-increasing-returns-monopoly)
status: PRIMARY_READING_BOUNDED; NO_R_UPGRADE; NO_NEW_TH_NUMBER

## 原始文献与实际阅读
W. Brian Arthur (1989), *Competing Technologies, Increasing Returns, and Lock-In by Historical Events*, *The Economic Journal* 99(394):116–131. DOI 10.2307/2234208. 意大利Ferrara大学公开保存的正式原刊扫描：https://www.unife.it/economia/lm.economia/insegnamenti/economia-applicata-avanzata/mat-did/frattini/ff4-arthur1989.pdf 。直接阅读正式原刊pp116–119、124–128及Appendix pp128–129指定段落；其余pp120–123、130–131及完整证明尚未逐行审查。仅引用来源，不复制第三方论文原文。

## 核心条件与新增独立来源证据
原刊p118 Table I假定两种采用者类型R/S，采用收益依赖此前各技术的采用人数n_A、n_B，且两类具有不同自然偏好。p124以采用份额x及下一次采用概率p(x)建立一般框架，固定点p(x)=x决定候选长期份额；p125 Theorem I/II对稳定固定点数量及位置作出条件性论断。

p125–126 Theorem III使用更强的假设：技术改进函数r随采用人数增加至少保持某个正增量，因而是无界增长。原刊p126明确说明：若r有上界，例如学习效应最终耗尽，多种技术可以共同达到改进上限，长期共存成为可能；另一些历史序列仍可能导致单一技术占优。故“正向采用反馈”不足以推出“必然垄断”，需要检查增长上界、固定点稳定性和偏好支持集。这个原著条件为TH220此前David1985与Liebowitz/Margolis1990争论提供直接的数学竞争边界，但不构成项目级模型融合。

## 机制对照、证据与反例
Arthur研究的是条件化的采用动力学，其不确定性来自进入顺序等观察者模型无法预知的小事件。Liebowitz与Margolis质疑具体历史案例中的性能优势及低效率证明。两种问题必须分开：动力学能够产生路径锁定，并不自动证明QWERTY实际低效率。Arthur在p126–127也明确表示现实经济中有多少劣质路径锁定尚未知晓。

构造性反例（独立推导，非原作者数据）：两种技术的收益分别为a_A+r(n_A)、a_B+r(n_B)，令r(n)=min(n,1)，采用者自然偏好分别严格偏向A与B，偏好差为3。因任何技术的学习收益最多增加1，每类采用者始终选择各自偏好的技术；若两类持续等概率进入，两种技术可长期并存。此例仅反驳“有界正反馈必然排除共存”的无条件命题。并不声称重现Arthur的全部随机过程定理。

## 层级、测量与因果限制
微观层：采用者偏好、进入顺序及信息；群体层：采用份额；制度层：标准兼容、专利、转换成本；历史层：累积采用轨迹。真实识别需要历期采用数据、实际收益函数、技术性能、转移成本及进入序列。观察到一个标准长期占优不能区分无界学习、有限网络收益、法规排他、市场力量及初始性能差异；也无法据此估计反事实社会福利。Arthur对核反应堆与蒸汽汽车的历史讨论属于有争议的历史案例提示，未由本轨复算。

## 证据状态与未读
原刊指定页阅读 COMPLETE；独立逻辑反例为构造性推导；原作者随机过程完整定理重证 NOT_RUN；历史采用者数据复算、因果识别及预测 NOT_RUN。原刊pp120–123、130–131和Arthur/Ermoliev/Kaniovski1983原始强律证明未完整阅读。C011 (2026-11-03) 与D003 (2026-W45, 2026-11-02) 已有独立归档，未新增C/D编号。R073/PESEN v0.1冻结，R E1/E2/E3与MARKET不变。无收费API、CI未触发，账户计费NOT_VERIFIED。

## 下一步
后续优先核对p125定理的技术条件及1983原始强律证明，尤其稳定固定点边界；随后转向其他覆盖较弱的学科。