# R251 李雅普诺夫稳定性：九人工离散动力世界、405完整有理初值来源与单步/两步稳定性证书

日期2026-10-23（Asia/Taipei），原239目录 `11-011 Lyapunov Stability`（P2）。正式资格 `CLOSED_BOUNDED_E1_DISCRETE_LYAPUNOV_CANDIDATE_AND_TWO_STEP_PROOFS`。完全人工、无真人和真实历史数据，E2=0、E3=0。原R073与PESEN v0.1保持冻结。

## 原始理论和必要边界

A. M. Lyapunov (1892), *The General Problem of the Stability of Motion*，英文译本见 [*International Journal of Control*, 55(3), 1992](https://doi.org/10.1080/00207179208934253)。离散时间系统的二次候选与增量方法另参考 [University of Washington ME547 Lecture: Discrete-time Lyapunov Stability](https://faculty.washington.edu/chx/teaching/me547/2_1_stability_slides_Lyapunov_light.pdf)。本R固定`V(x)=x²`并严格分别审计正定、`ΔV(x)=V(f(x))-V(x)`的符号和邻域不变性。**仅找到了某些固定原初值ΔV<0，不能证明邻域严格下降；且某候选V单步未下降，也不构成对实际稳定性的反证。**本R将数学符号不等式证明与有限四步source枚举分开。

[事前冻结九人工映射和完整405原source](../../protocols/R251_LYAPUNOV_9_RATIONAL_MAP_WORLDS_405_SOURCES_PRESCORE_FREEZE_2026-10-23.md)先独立commit [15568be1](https://github.com/edwardsage419/Psychohistory-Research/commit/15568be1625414aa72a179c93f315535de704d73)，再提交计算程序及CI。九world每world 9初始状态`−1/2,−1/4,−1/12,−1/24,0,1/24,1/12,1/4,1/2`×5时点n=0..4，各45个完整人工结构来源，每源质量1/45，共405。每行保存初值和n、实际状态x_n、候选V_n、下一次映射f(x_n)、单步ΔV、f′及初值敏感度、原source质量。一个初值五时点是同一确定轨道，不能当五条独立真人实验。

## 九世界正式数学结果

| 冻结人工世界 | f(x) | ΔV或严格邻域证明 | 局部/全局资格 |
|---|---|---|---|
| HALF_CONTRACTION | x/2 | −3x²/4 | 全局渐近吸引 |
| NEGATIVE_HALF_CONTRACTION | −x/2 | −3x²/4 | 全局交替收敛 |
| ZERO_MAP | 0 | −x² | 一步归零、全局渐近 |
| DOUBLE_EXPANSION | 2x | +3x² | 0不稳定 |
| IDENTITY_NEUTRAL | x | 0 | 所有点不动，0稳定但不吸引 |
| SIGN_FLIP_NEUTRAL | −x | 0 | 每两步恢复，0稳定但不吸引 |
| CUBIC_LOCAL_INWARD | x−x³ | `V(f)=x²(1−x²)²<V(x)`，0<|x|<1 | 局部渐近吸引，乘子+1 |
| CUBIC_OUTWARD | x+x³ | `ΔV=x⁴(2+x²)>0`，x≠0 | 0局部不稳定，乘子+1 |
| LOGISTIC_R3_CENTERED | −x−3x² | `ΔV=6x³+9x⁴`两侧异号；两次迭代局部严格内缩 | 0局部渐近吸引，但本候选V不满足两侧单步下降 |

**严格下降的单步候选证书：** 线性收缩、负收缩、零映射对任意非零x都有正定V和严格负ΔV，直接获得全局渐近稳定。对于CUBIC_LOCAL_INWARD，`0<|x|<1`时映射保留符号、`|f(x)|=|x|(1−x²)`严格小于|x|且仍留在邻域，因此`V(f)<V(x)`并由唯一极限固定点0得到局部渐近稳定。反向的CUBIC_OUTWARD对每个非零邻点有`|f(x)|>|x|`，离0严格扩大、不可永远留在一个小邻域，故0不稳定。两者的线性乘子却都是+1，**同样非双曲乘子不能替代高阶非线性证据**。

**稳定但不渐近吸引：** IDENTITY_NEUTRAL所有状态均保持原位，SIGN_FLIP_NEUTRAL非零状态两步回到同一值。二者在x*=0处的V严格正定却`ΔV=0`，轨道始终有界且|x|保持不变，因此Lyapunov稳定，但没有任何非零邻近点会渐近趋向0。这也证明`V≥0`或`ΔV≤0`本身不等于渐近吸引结论。

**单步V可能增加，系统仍局部渐近稳定。** Logistic r=3固定点2/3中心化后令x表示原来的偏差，有`f(x)=−x−3x²`、`ΔV=6x³+9x⁴`。当0<x≤1/12时单步ΔV>0，当−1/12≤x<0时单步ΔV<0；故固定二次函数V=x²**不能作为整个两侧邻域内的严格单步下降证书**。但是精确第二次迭代
[
f^{∘2}(x)=x−18x^3−27x^4=x[1-x^2(18+27x)].
]
在0<|x|≤1/12的邻域内有`0<x²(18+27x)≤9/64<1`，所以每两步严格缩小非零偏差、保持局部邻域；非零极限不可能不继续减小，由此偶数步趋向0、奇数步由f连续性也趋0。**“某一特定单步Lyapunov候选函数不满足充分条件”与“系统本身不渐近稳定”是两回事。**这一证明采用独立形式多项式系数`[0,1,0,-18,-27]`和严格有理上界，而不仅是列举四步轨迹。

## 两条独立数学路线、真实CI及证据保存

第一路线逐源迭代并用`D_{n+1}=f'(x_n)D_n`传播初值灵敏度；第二独立路线不用第一递推或源CSV，而用有理系数多项式形式复合`f^{∘n}`、Horner求值、形式微分计算各项D_n。九world×45全部405原source在状态、候选值、变化量、初值灵敏度上逐格Fraction严格一致。对所有m+n≤4及所有冻结初值另作离散自治半群校验。**长期稳定性的严谨资格来自上述映射结构与邻域不等式，不靠四步人工数据本身推断无限时行为。**

[GitHub Actions run39894992871](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894992871)总体completed/success，三个job均completed/success；Python3.11及3.12实际日志各`Ran 84 tests`、`OK`，合计**168次真实单测通过**。第三独立归档审计重新产生405完整原CSV，验证各世界45独特初值/时点、质量1/45、全部来源上候选V和ΔV公式、非双曲两步严格缩小与单步增大反例、JSON解析数学凭证以及CSV/JSON SHA256。日志`R251_ALL_405_EXACT_LYAPUNOV_CANDIDATE_ATOMS_AND_TWO_STEP_PROOF_VERIFIED`。所有原CSV/JSON/机器收据已机器人永久提交main [4fdebd05](https://github.com/edwardsage419/Psychohistory-Research/commit/4fdebd05aac54718b48a7b925f8993fd9647ddba)。

[原生Fraction Python程序](r251_exact_lyapunov.py) · [405原source CSV](R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv) · [九world完整状态、严格证书JSON](R251_EXACT_RESULTS.json) · [SHA256机器来源收据](R251_FINAL_MACHINE_ACCEPTANCE.json)。

源CSV SHA256 `5b43196a7714336294dbdd332b5c3cb14d6eea8ee269ebc7baa479d8cc5ec25e`，完整JSON结果SHA256 `b8180437577a0125053dd8f319b8f76e126ad77b172b72b89a6022bc1b8288b3`。

最终仅`CLOSED_BOUNDED_E1_DISCRETE_LYAPUNOV_CANDIDATE_AND_TWO_STEP_PROOFS`，未对现实制度系统、历史事件或人的行为做稳定性参数拟合/外部预测。新增真人E2、真实历史E3各为0；R073、PESEN v0.1均冻结。下一原239目录11-012 Entropy and Information Theory（R252，P1），保持先完成所有R、再统一分类、最后熔炼。
