# Gorman (1968) 原著核读：相邻期替代率条件与加性可分性
track: theory
subflow: primary-source
run_date: 2026-11-10 Asia/Singapore
observed_head: 1387e5e892ff62c9d6505c3936800cbb05ebdc9a
target_key: (theory,Gorman-1968,Econometrica-36-3-4,adjacent-period-MRS-and-additive-separability)
status: PARTIAL_PRIMARY_AUDIT
related: theory/KAHNEMAN_WAKKER_SARIN_1997_APPENDIX_PROOF_AUDIT_2026-11-10.md

## 来源与直接阅读范围
W. M. Gorman (1968), "Conditions for Additive Separability", Econometrica 36(3/4):605–609, JSTOR stable ID 1909527.
原刊页面扫描副本（庆应大学学术网页托管）：https://news.fbc.keio.ac.jp/~hayami/pdf/consumption/Gorman1968.pdf
稳定书目：https://www.jstor.org/stable/1909527
本轮直接读取原刊印刷页605–609，含定理、证明、推论及参考文献。此副本附JSTOR使用声明，仅研究阅读与事实性笔记，不重新分发PDF。未验证出版社是否授权该镜像公开再传播，来源权限保留待核。

## 原始命题和精确条件
1. 作者定义 well behaved 的效用函数：非负正交域上的严格单调、二次连续可微函数，时间/商品分组数 T>2。可加可分是经适当严格递增且二次连续可微的效用变换后，存在分组函数之和；不是说任何原始数值效用标尺直接相加（p.605）。
2. 定义对称矩阵 A；当 a_st 非零时，组 s 与 t 的商品边际替代率只依赖这两组消费。定理：对 well behaved 的 u，这些条件蕴涵加性可分，当且仅当 A 不可分解（p.606）。不可分解可用图的连通性解释；作者以相邻时间段组成的链为特例。
3. 仅要求相邻时期之间的边际替代率不依赖其他时期，在 T>2 且其余正则性成立时，已经足以推出全部时期的加性可分表示（pp.605–606）。因此相邻局部条件并非弱到可保留任意跨期交互。
4. 若 A 可分解，作者给出分块形式的反例族：各连通分块内部可加，跨分块仍允许经一般严格递增函数组合（pp.608–609）。连通性缺失时，不能推出整体可加。
5. 证明依赖 Leontief 的可分性定理、可积性条件以及从局部向全局的延拓论证（pp.606–608及脚注）。Leontief (1947) 原作及全部技术引理未独立重证。

## 竞争解释、跨层边界和构造反例
设三个时间分组的效用 U(x1,x2,x3)=x1+x2+x3，任意相邻组的边际替代率均为1，满足加性表示。作为对照，V(x1,x2,x3)=x1+x2+x3+λx1x3 (λ>0)，有 V_1/V_2=1+λx3；第一和第二组替代率受第三组影响，违反相邻局部独立性。此例仅为逻辑反例，未做程序测试。对时间评价来说，习惯、累积疲劳、互补投资等可能产生跨期交互；它们是竞争机制候选，尚无本轮实证识别。
本论文讨论确定性偏好函数的数学结构。不能据此认定真人效用满足可分性，也不能直接用于群体、制度或历史层预测。
与 Kahneman/Wakker/Sarin (1997) 的关系：1997年附录调用 Gorman 作为可加表示的数学依赖；两文函数域和正则性设置不同。不得未经证明就把1968年的可微有限维条件直接移植到1997年的有界可测时间轮廓。需要单独核验1997年对阶梯函数及连续延拓的论证。

## 证据和剩余任务
证据：原刊五页直接阅读 COMPLETE；论文定理及证明结构核查 COMPLETE；Leontief 1947 依赖核验 NOT_RUN；两个原著之间假设映射 PARTIAL；真人/历史数据 NOT_RUN；数学程序测试 NOT_RUN；CI NOT_RUN。
C当日与D本周均不因本理论档案自动计为完成。R073、PESEN v0.1及E1/E2/E3与MARKET等级保持原状。无付费API或CI调用；实际账户计费状态 NOT_VERIFIED。
