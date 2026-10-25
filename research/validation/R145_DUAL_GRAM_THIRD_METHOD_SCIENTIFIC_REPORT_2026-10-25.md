# R145 第三方法科学报告：隐藏努力契约的对偶 Gram 解析复核

日期：2026-10-25。原候选 original239 `06-003`，既有 R145 为项目自构造 E1 隐藏努力模型。文献源 Holmström (1979) DOI https://doi.org/10.2307/3003320 与 Grossman–Hart (1983) DOI https://doi.org/10.2307/1912246。新增复核没有重现原作者全部一般模型。

## 事前冻结与独立执行

新增协议先于程序与结果提交，commit `debede2a506fcd58ab848db336b16b946a7e7b4b`，文件 `research/validation/R145_DUAL_GRAM_THIRD_METHOD_PROTOCOL_FREEZE_2026-10-25.md`。
第一方法：JavaScript BigInt 精确有理数，独立对偶 Gram 恒等式，程序 `research/validation/r145_dual_gram_independent_exact.js`，Git blob `28e7b9a883c9812a03a2fc2b58cd1006fdda40ba`。从GitHub回读同一字节并实际在V8运行，12个基本配置、192个四状态标签排列检查全部通过，三项预设负对照全部通过。机器结果 `research/validation/R145_DUAL_GRAM_12_CASE_192_PERMUTATION_EXACT_RECEIPT_2026-10-25.json`。
第二方法：独立 Python 标准库 Fraction，建立 n+2 个未知量的完整 KKT 驻点与绑定约束线性方程，逐列选主元 Gauss–Jordan 消元。没有调用 JavaScript Gram 闭式求解器。实际运行12个配置及192个标签排列，全部一致。归档程序 `research/evidence_audit/r145_b_full_kkt_gauss_jordan.py`，Git blob `41df34feebc6034bd9abb0937f3fdedae8150b13` 与本地实际运行文件的 `git hash-object` 完全一致；本地 Python SHA256 `1b8024661a83977314adafdb962a8994874a22df15345c3eeca1b647e0da18cf`。

## 解析机制与精确结果

记 `d_i=p_Hi-p_Li`，工资效用 `v_i=sqrt(w_i)`，IR 目标 `b=1/2+c`，IC 目标 `c`。对所有正概率状态，定义
[
G=\sum_i\frac{d_i^2}{p_{Hi}}.
]
因为 `sum d_i=0`，IR 与 IC 的 Gram 交叉项为0。两约束同时绑定且所有 `v_i>=0` 时，
[
v_i=b+\frac{c}{G}\frac{d_i}{p_{Hi}},\qquad
C_H=b^2+\frac{c^2}{G}.
]
KKT 乘子 `lambda=2b`、`mu=2c/G` 均非负。逐状态检查驻点、IR、IC、工资非负和精确成本，构成该有界凸问题的充分最优证书。所有12个冻结配置均满足内部解条件。

| 条件 | G | c=1/4 最优工资成本 |
|---|---|---|
| 仅产出 | 4/3 | 39/64 |
| 条件冗余信号 | 4/3 | 39/64 |
| 含增量信息信号 | 569/384 | 5505/9104 |

新增第三方法重新得到增量信息的毛节约 `171/36416`。预设的全部非零监控费用从 `1/64` 起，均高于该毛节约。努力成本 `c=0` 时三个模型的工资成本同为 `1/4`。在 `c=1/8` 时基础成本 `103/256`、信息成本 `14609/36416`；在 `c=3/8` 时分别 `223/256`、`31337/36416`。

三项负对照：冗余信号不能凭空产生严格节约；全部最优配置的 IC 恰好绑定，不能冒称严格激励相容；正监控费后没有净正价值。两种四状态模型各24种排列×4种成本，总计192个精确重算均不改变成本。

## 科学限制和验收

这是**同一项目内部的两种数学方法复核**。Python 与 JS 分别实现，仍依赖同一人工模型假设；外部团队独立复现0。没有真人雇佣数据、概率校准或真实制度因果识别。弱IC下高努力实际执行仍需平局选择假设。原R145的既有CI不代表本次新脚本CI；本轮新CI `NOT_RUN`。
科学状态 `PASS_BOUNDED_LOCAL_TWO_METHOD_EXACT_E1`，原R145正式结题文件保持不变。新增 E1 有界方法证据1项，E2=0，E3=0。original239 待核154项不减少，R073/PESEN v0.1未修改。