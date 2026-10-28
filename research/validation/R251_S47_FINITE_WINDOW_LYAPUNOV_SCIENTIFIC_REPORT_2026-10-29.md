# R251 S47：有限观察窗口的Lyapunov候选误判审计

日期：2026-10-29。证据：E1人工数学。预先冻结协议commit [89d5311](https://github.com/edwardsage419/Psychohistory-Research/commit/89d53112850eec5662ae2280f7e94c79236e674c)。原R251正式有界验收不变，原九映射和405来源不变。原始CSV Git blob `b8ca35f1e7779f38bcbd60051973819aa3b29061`，原始CSV SHA256 `5b43196a7714336294dbdd332b5c3cb14d6eea8ee269ebc7baa479d8cc5ec25e`。

## 冻结研究问题
给定九个人工离散系统，72条非零初值轨道，比较两条仅用t=0..4观察的有限窗口规则：STRICT4要求t=0至3四次ΔV都严格负；NET4要求第四时点距离0严格小于初值距离0。每世界额外统计45条来源的ΔV符号；局部固定子集|x0|≤1/12、x0≠0，共每世界4轨道。V=x²，精确Fraction/BigInt有理数。原R251无限时稳定性分类只采用已归档的解析证明。

## 完整九世界结果
| 人工世界 | 45来源ΔV负/零/正 | STRICT4通过/8 | NET4收缩/持平/扩大 |
| --- | --- | ---: | --- |
| HALF_CONTRACTION | 40/5/0 | 8 | 8/0/0 |
| NEGATIVE_HALF_CONTRACTION | 40/5/0 | 8 | 8/0/0 |
| ZERO_MAP | 8/37/0 | 0 | 8/0/0 |
| DOUBLE_EXPANSION | 0/5/40 | 0 | 0/0/8 |
| IDENTITY_NEUTRAL | 0/45/0 | 0 | 0/8/0 |
| SIGN_FLIP_NEUTRAL | 0/45/0 | 0 | 0/8/0 |
| CUBIC_LOCAL_INWARD | 40/5/0 | 8 | 8/0/0 |
| CUBIC_OUTWARD | 0/5/40 | 0 | 0/0/8 |
| LOGISTIC_R3_CENTERED | 19/5/21 | 0 | 7/0/1 |

## 科学发现及反例
1. ZERO_MAP是全局一步到达固定点的渐近吸引系统。非零轨道四次ΔV符号均为`-000`，所以STRICT4全部拒绝，NET4全部判断收缩。把“每一步必须严格下降”当作必要条件，会误拒绝有限时间归零的真实吸引机制。
2. LOGISTIC_R3_CENTERED已有独立的二次迭代局部收缩解析证书。局部子集±1/24、±1/12共四条轨道NET4全部收缩、STRICT4全部拒绝。正初值1/12的前四次ΔV符号为`+-+-`，负初值-1/12为`-+-+`。九世界45来源中该世界ΔV有21正、19负、5零，单步符号混合与局部渐近吸引相容。
3. LOGISTIC_R3_CENTERED在冻结较大初值+1/2时四步NET4扩大，在-1/2时NET4收缩。原证明保证的局部邻域|x|≤1/12，故不能把较大初值的有限行为归因于局部证明失败。
4. IDENTITY_NEUTRAL与SIGN_FLIP_NEUTRAL均为Lyapunov稳定但不渐近吸引，NET4均为8条持平。仅以NET4收缩与否二分“稳定/不稳定”，会错误地把中性稳定与不稳定混同。
5. DOUBLE_EXPANSION与CUBIC_OUTWARD的八条非零初值均四步扩大；这一观察与原解析不稳定证明相符，有限样本本身不提供无限时证明。

## 复算与验收范围
R轨脚本 [r251_s47_finite_window_exact_20261029.js](r251_s47_finite_window_exact_20261029.js) 实际从原始405行CSV重建每行状态、V、下一状态、ΔV、导数、初值灵敏度和设计质量，共2835项字段比较，失败0；逐轨道计算72个STRICT4及NET4。故意将首行V改成999，脚本拒绝。
B轨 [独立Fraction脚本](../evidence_audit/b_r251_s47_independent_fraction_20261029.py) 不读取R轨CSV，使用九个冻结映射从初值独立构造全部405个状态及72条轨道；本地Python命令行实际执行。两路线的九世界摘要一致，72条轨道序列化结果均为7268字节，FNV32校验均为`9ba8e576`，独立Python计算的完整worlds序列化SHA256为`21a29ce3780138157037f26221bafb4def5f94f6ff654819ca51f60c473ba43b`。FNV32只是轻量一致性校验，完整收据逐字段比较脚本已提供，尚未以远端JSON执行本地命令行。机器收据 [R251_S47_FINITE_WINDOW_EXACT_RECEIPT_2026-10-29.json](R251_S47_FINITE_WINDOW_EXACT_RECEIPT_2026-10-29.json)。

本轮未触发新增GitHub Actions，新增CI=NOT_RUN。原R251历史CI与本轮新增脚本须分开。所有72条轨道为九个人工世界中同一设计的确定性初值，405条时点记录高度依赖。无统计样本外验证、概率校准或真实因果识别。新增真人E2=0，真实历史E3=0，外部团队独立复现=0。R073冻结评分、PESEN v0.1冻结；全部R研究完成前不开展模型熔炼。
