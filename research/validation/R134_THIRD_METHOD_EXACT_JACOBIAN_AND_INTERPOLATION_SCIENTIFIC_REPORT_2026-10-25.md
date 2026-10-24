# R134 第三方法科学报告：81组双群体局部动力学与精确入侵插值

日期：2026-10-25。轨道：R主线及B内部独立方法审计。状态：`PASS_BOUNDED_LOCAL_TWO_LANGUAGE_EXACT_E1`，新CI `NOT_RUN`，原original239目录统计保持不变。

## 来源、冻结与实际执行

一手理论：Peter D. Taylor (1979), *Evolutionarily Stable Strategies with Two Types of Player*, *Journal of Applied Probability* 16(1):76–83, DOI 10.2307/3213376。原有研究 `research/R134/README.md` 已对原刊第77至79页及原式(1)至(5)作有限复核；既有CI run 39371915556曾完成两个Python环境各45项测试。本轮没有重新执行原有ZIP中的45项测试。

新协议先于计算提交：`da96febe717756c7770626c52c0679153c2f40f1`，文件 `R134_THIRD_METHOD_EXACT_JACOBIAN_INTERPOLATION_PROTOCOL_FREEZE_2026-10-25.md`。随后提交全新JavaScript整数算法、81行CSV和机器收据。再以本地独立Python Fraction矩阵乘法和四点中心差分完整复算，源代码已提交并确认与实际执行的本地字节完全一致：Git blob `2cea2b053a74e9c1d06b365dcf5d08b992eb2d9d`，SHA256 `6c53383233733f4d6a59644808cf585b1345686251e7448a043d923cefa2d599`。

## 81个有限人工世界的精确分类

人工四块矩阵 `A=aS, B=bT, C=cT, D=dS`，`S=[[0,1],[1,0]]`，`T=[[2,0],[0,2]]`，各系数取 `{-1,0,1}`。中心 `x=y=1/2` 的精确雅可比为

```
J = [[-a/2, b],
     [c, -d/2]]
trace = -(a+d)/2
determinant = ad/4 - bc
```

四点中心差分在此三次多项式向量场上精确重现全部324个雅可比元素，两个实现一致。

| 线性局部分类 | 世界数 |
| --- | ---: |
| 鞍点，det<0 | 28 |
| 渐近稳定，det>0且trace<0 | 11 |
| 线性不稳定，det>0且trace>0 | 11 |
| 非双曲，det=0 | 25 |
| 线性中心，det>0且trace=0 | 6 |
| 合计 | 81 |

非双曲25组与线性中心6组的非线性稳定性不能凭此分类判定。分类仅适用于指定中心与指定参数族，不推断任意初始值的全局吸引域。

九组 `a=d=1` 世界的两个群体各自保持另一群体固定时均满足严格单群体二阶抵抗。在其中两组 `(a,b,c,d)=(1,1,1,1)` 和 `(1,-1,-1,1)`，完整双群体系统的 `det<0`，中心成为鞍点。由此严格构造出“各自单独稳定，联合失稳”的两个有限反例。

## 第三方法直接收益插值

对81世界×9组居民×16组变异者，执行11664个完整入侵组合。每个组合在 `epsilon=0,1/2,1` 直接计算源式居民总收益优势，共34992次直接收益求值。

11664项均满足 `2f(1/2)=f(0)+f(1)`。独立计算原二次型Q后，11664项均满足 `f(1)-f(0)=-Q`。两种编程语言的独立实现均对全部11664项重新完成检查。

预设负对照将 `J[0,1]` 错写为 `2b`，以及从Q删除跨群体作用项，均被拒绝。两项正对照和线性中心对照符合协议。无失败检查。

## 审计材料与原始身份

* 事前协议：`research/validation/R134_THIRD_METHOD_EXACT_JACOBIAN_INTERPOLATION_PROTOCOL_FREEZE_2026-10-25.md`。
* JavaScript整数算法：`research/validation/r134_exact_jacobian_interpolation_third_method.js`，Git blob `c59e7bbb5e253d8c342c3be4cdf4943ee7b7e22c`。
* 81行精确结果：`research/validation/R134_THIRD_METHOD_81_EXACT_JACOBIANS_2026-10-25.csv`，Git blob `eaabf33318c28bfb80bf0353059140ca491a9aeb`。
* 机器收据：`research/validation/R134_THIRD_METHOD_EXACT_AUDIT_RECEIPT_2026-10-25.json`，Git blob `7cf2f55a9ed4236dfd132fa7e35ac5697fcd9a90`。
* Python独立矩阵算法：`research/validation/r134_independent_matrix_fraction_recompute.py`，Git blob `2cea2b053a74e9c1d06b365dcf5d08b992eb2d9d`。

Python独立复算在本轮容器中实际执行并返回 `worlds=81, triples=11664, payoff_evaluations=34992`，五种分类数及两个联合鞍点参数与JavaScript完全一致。原始研究作者软件的完整新CI复验本轮未执行。

## 科学限制与后续验收

本轮属于同一研究执行主体的两种独立算法程序性复核，`EXTERNAL_INDEPENDENT_REPLICATION=NO`。全部81世界均为人工数学构造，新增E1有限证据；真人E2=0，历史E3=0。未估计现实参数、真实样本外概率预测、校准、置信区间或因果效应。R073和PESEN v0.1保持冻结。

GitHub Actions没有在本轮启动，原因是用户零新增费用约束下未核实账户实际计费与runner余量。此前R134 CI历史成功仅作为历史证据，不作为本轮新CI。原239交叉索引和待核队列未修改。R134原有有界研究已经归档，此次为新增第三方法的有限机制复核，后续可在单独验收流程中决定是否调整对应队列状态。
