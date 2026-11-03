# TH220 Arthur 1989 附录C原刊影像校勘

track: theory
subflow: main_theory
run_date: 2026-11-03 (Asia/Singapore)
observed_head: d81cec2657b400682300c76b50dfe03b39183473
target_key: (theory,Arthur1989,EconomicJournal99(394),AppendixC-time-varying-pn-visual-proof-boundary)
status: COMPLETE_FOR_PRINTED_TEXT; ORIGINAL_PROOF_NOT_RUN

## 原始来源与本轮实际阅读
W. Brian Arthur (1989), *Competing Technologies, Increasing Returns, and Lock-In by Historical Events*, *Economic Journal* 99(394):116–131, DOI 10.2307/2234208. 开放原刊扫描 https://gamef21.classes.ryansafner.com/readings/Arthur-1989.pdf ，本轮直接目视原刊p.130附录C全部四款定理与紧随其后的引用；PDF物理第16页（从0计数第15页）。其余页沿用既有TH220记录，本轮没有声称重读。

## 原文符号与重要更正
1. (i) 概率映射 p:S^K→S^K 连续；要求 p(x)−x 有Lyapunov函数，原文为正且二次可微的 V，其梯度与 p(x)−x 内积为负；固定点集 B={x:p(x)=x} 有有限个连通分量。原刊结论是 x_n 几乎必然收敛至 B 中某点或一个连通分量的边界。原文没有保证任意情形下收敛到唯一稳定单点。
2. (ii) 另要求 p 将单纯形内部映射到内部，且 z 为稳定点，才陈述收敛到 z 的概率为正。(iii) z 为非顶点不稳定点时，收敛到 z 的概率为零。不能混同为所有不稳定点。
3. (iv) 原刊逐字视觉确认时间变动概率序列 {p_n} 趋近极限 p 的速率条件，原文为“faster than 1/n converges to zero”。这明确涉及比 1/n 更快的收敛，修正此前OCR无法识别速率的未决状态。**原刊未在此句显式给出误差范数、统一性及可检验的精确大O定义**；严谨数学重述暂保留为“作者文字速率条件”，不得擅自写成 sup_x||p_n(x)−p(x)||=o(1/n) 等未在此页核实的表达。
4. (iv) 在所述条件对极限函数p成立时，原文陈述过程以概率一收敛至该极限函数的一个稳定固定点。它与(i)的一般结论适用前提不同。1983/1986原始证明未直接读取，故本轮只确认1989印刷陈述。
5. 参考文献在同页明确列出Arthur、Ermoliev、Kaniovski (1983) *Kibernetika* 19:49–56（英译 *Cybernetics* 19:61–71）及(1986) *Proceedings of the International Conference on Stochastic Optimization*, Kiev 1984, Springer Lecture Notes in Control and Information Sciences 81:187–300。后者会议年与出版年应区分；尚未取得全文。

## 机制竞争与适用范围
上述结果适用于给定状态依赖概率、增量与正则性假设的随机采用过程。市场份额、技术质量、真实采用者预期与制度性排他仍需单独测量。技术标准延续可以由切换成本、兼容性、异质性、政策或战略定价解释，不能用附录定理直接证明历史低效率。个体选择与历史总体份额之间的识别仍开放。

## 验证和保留问题
证据类型：原始论文扫描影像的文字与符号目视校勘，属于原著陈述证据。独立数学证明NOT_RUN；人工数学测试NOT_RUN；真人数据与历史因果NOT_RUN；独立预测NOT_RUN。正式勘误与1983/1986证明未查明。C011 2026-11-03、D003 2026-W45实际2026-11-02沿用现有登记，不新增编号。R073、PESEN v0.1冻结，R E1/E2/E3及MARKET等级不变。CI NOT_RUN；新增收费操作0，账户计费NOT_VERIFIED。

下一步：寻找1983/1986原始证明以澄清(iv)收敛速度的数学量词；之后轮换其他学科，避免技术史连续占用。
