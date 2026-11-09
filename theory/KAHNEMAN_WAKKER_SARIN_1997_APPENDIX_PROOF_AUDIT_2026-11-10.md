# Kahneman, Wakker & Sarin (1997) 附录证明核读与边界更正
track: theory
date: 2026-11-10 Asia/Singapore
observed_main_head: a9f54d9f48af75909f02ccf3b80678986b7bb800
target_key: (theory,Kahneman-Wakker-Sarin-1997,final-QJE,appendix-representation-technical-assumptions)
status: THEORY_NOTE_BOUNDED
related: theory/TH_KAHNEMAN_WAKKER_SARIN_1997_EXPERIENCED_UTILITY_PRIMARY_2026-11-10.md

## 直接阅读
作者 Daniel Kahneman, Peter P. Wakker, Rakesh Sarin (1997), Back to Bentham? Explorations of Experienced Utility, Quarterly Journal of Economics 112(2), DOI https://doi.org/10.1162/003355397555235
Erasmus 机构库正式PDF https://repub.eur.nl/pub/23011/QJE_1997_112_375.pdf
本次直接阅读印刷页397至402（PDF页23至28），含 Appendix 定义、Lemma A.1、Theorem A.1 的证明、Lemma A.2、Theorem 2 的证明及 Theorem A.2/Corollary A.1。此前已读印刷页375至392；本次并未重新复算原作者真人实验。

## 新增且独立的证明边界
1. 正文定理1简写为公理1、2、3。附录正式定理A.1还要求效用轮廓上的弱序（weak order）、supremum norm 连续性，轮廓定义域为有限最大时长 M 内的有界可测函数，瞬时效用值域 X 是含零的区间。结论是存在连续非降 v、v(0)=0，使排序由 ∫v(f(t))dt 表示；v 仅在正比例变换下唯一。不得从三条口头公理单独声称一般积分表示。
2. Lemma A.1 在中性连接与公理3下导出左右可分性；证明将时域分成至少三个等长子区间，再调用 Gorman (1968) 的可加表示，利用中性连接令各段值函数一致，最后由 supnorm 连续性从阶梯函数推广。Gorman 原论文未独立核读，故其定理适用条件属于引用依赖。
3. 正文 Theorem 2 需要公理1、2、4以及附录沿用的技术条件。附录明确说明此处不能预设公理3，先以 Lemma A.2 从公理4对阶梯轮廓导出公理3，再得到 v(x+e)-v(x)=v(e) 的 Cauchy 关系，单调性推出线性。故 Theorem 2 与 Theorem 1 的公理组合有区别。
4. Ordinal 总效用只确定排序，允许积分再作严格递增变换。附录公理 A.2 要求拼接轮廓的总效用数值可加；Theorem A.2 与 Corollary A.1 才将表示强化为总效用数值本身等于积分。不得把排序表示直接解释为可测的数值总效用。
5. 形式化时把分离事件之间的空档删除，按秒表时间连接各段；这依赖无折现与跨日期同一体验值等价。时间顺序和日历时间的信息会丢失。用于人生长期评价时需先检验这些条件。
6. 原刊附录印刷页402的 Corollary A.1 引用“Theorem A.3”的技术条件，而本附录可见的是 A.1 与 A.2；属于原文内部交叉引用疑点。未找到勘误，暂不自行修正原文。

## 竞争解释与识别限制
可分、无折现的时间积分与带折现权重的积分、峰终回忆评分可给出不同排序。假定瞬时效用包含全部前后文影响是强测量要求；同一观测选择不足以识别哪一种评价标准成立。原文论证是规范表示定理，不能视为真实个人长期效用的已验证因果模型。

## 证据及执行
原刊指定附录直接阅读 COMPLETE；Gorman 1968 原作核验 NOT_RUN；数学程序独立测试 NOT_RUN；真人E2、历史E3验证 NOT_RUN；CI NOT_RUN。未使用私人数据、收费API或付费资源。R073、PESEN v0.1及证据分级保持冻结。
