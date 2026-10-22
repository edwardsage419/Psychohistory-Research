# R232 结构方程模型：八个人工结构—测量联合世界、1024完整来源与媒介因果解释边界

日期：2026-10-23（Asia/Taipei）。原239目录真实**10-006 Structural Equation Modeling（P1）**。科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_SEM_MEDIATION_MEASUREMENT**。只对精确构造的有限人工线性SEM作出结论；没有实际真人心理数据E2、真实社会历史预测E3或真实SEM拟合参数。

## 原方法与本研究范围

Kenneth A. Bollen (1989), *Structural Equations with Latent Variables*, [第8章 *The General Model, Part I: Latent Variable and Measurement Models Combined*](https://doi.org/10.1002/9781118619179.ch8)，方法背景为联合潜在测量模型、结构路径及其隐含协方差。Imai, Keele & Tingley (2010), [*A General Approach to Causal Mediation Analysis*](https://doi.org/10.1037/a0020761), *Psychological Methods* 15:309–334，明确区分因果中介的数学定义、识别假设、估计及敏感性，警告不能单以线性路径参数就充分确立中介因果性。本研究并未重分析其JOBS II等真人数据、未推导一般非线性自然间接效应识别定理、未执行实际SEM因果参数优化。

独立[评分前八世界冻结协议](../../protocols/R232_SEM_8_WORLDS_1024_ORIGINAL_STRUCTURAL_SOURCES_PRESCORE_FREEZE_2026-10-23.md)先行提交[d04ae67b](https://github.com/edwardsage419/Psychohistory-Research/commit/d04ae67b1cdb1a94a783da3df36f88080a65fa70)，再提交模型程序、CI及任何科研结果，模型八项参数与验收假说没有被事后改动。

## 原外生源及可观察变量

每世界人工U、R、E_M、E_Y、E_W、E_Z1、E_Z2 七个互相独立均匀±1外生源，2⁷=128种完整互斥原来源，各1/128，八世界共**1024**条。真实人工治疗A由独立R或潜在共同U确定；真实媒介M由A、U与独立E_M形成；真实结果Y由M、A、U及独立E_Y形成；测量模块W=M+w_E E_W，另外两个实际测量指标Z1=U+E_Z1、Z2=U+E_Z2。**唯一当次实际观察变量为(A,W,Y,Z1,Z2)**，中介真M、U、人工外生及全部潜在干预结局只用于分隔的oracle。

两套相互独立的数学路径：其一直接由全128原结构来源，计算五个实际观察变量的Fraction总体协方差，以及同一外生源的`do(A=+1)`与`do(A=−1)`的真实M/Y潜在差；其二不使用来源行，而从七维外生变量的冻结线性系数向量逐结构边展开，再按向量内积独立取得25个观察Cov，并直接从固定结构系数得到真实总`y_A+y_M m_A`、直接`y_A`、中介`y_M m_A`效应。所有真实干预效应是将A由−1改为+1的平均结果差除以2，本人U及误差保持不变；在这里无交互的线性冻结世界，三者严格可加。

另外三个观察OLS路径只从实际可见(A,W,Y)的Cov取得：A到W单回归、Y对(W,A)二元线性投影及A到Y总回归。观察`A→W`乘`Y~W|A`叫**统计中介路径乘积**，不是无条件可识别的自然间接因果效果。观察路径乘积加上`Y~A|W`一定等于观察总回归系数只是线性投影代数恒等式，不能把相加准确性当成中介路径因果识别。

## 八个人工世界真实与观察结论

| 人工冻结世界 | 真总效应 | 真受控直接 | 真中介 | 观察A→Y总回归 | 观察代理中介乘积 | 观察控制W的A路径 |
|---|---:|---:|---:|---:|---:|---:|
| RANDOMIZED_MEDIATED | 1 | 0 | 1 | 1 | 1 | 0 |
| RANDOMIZED_NULL | 0 | 0 | 0 | 0 | 0 | 0 |
| LATENT_CAUSAL_ALIAS | 1 | 0 | 1 | 1 | 1 | 0 |
| LATENT_COMMON_ALIAS | 0 | 0 | 0 | 1 | 1 | 0 |
| RANDOMIZED_DIRECT_AND_MEDIATED | 2 | 1 | 1 | 2 | 1 | 1 |
| RANDOMIZED_MEDIATOR_CONFOUNDED | 1 | 0 | 1 | 1 | 3/2 | −1/2 |
| RANDOMIZED_DIRECT_ONLY | 1 | 1 | 0 | 1 | 0 | 1 |
| RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR | 1 | 0 | 1 | 1 | 1/2 | 1/2 |

**完整观察分布等价的最强反例：** `LATENT_CAUSAL_ALIAS`中A=U且M=A+E_M，`LATENT_COMMON_ALIAS`中A=U且M=U+E_M，两世界实际来源A、W、Y、Z1、Z2对全部128个独立外生源**每一来源相同**，整个 `P(A,W,Y,Z1,Z2)` 逐状态严格同分布；真实人工do(A)效果却分别为1与0。即使测量指标Z1/Z2携带U信息，因这两个世界A由U确定，给定U后A没有独立变化支持，实际观察分布不能决定干预A是否真正改变M/Y。此结论只证明这两个特定完全非正值性配置下的观察等价，不能扩张为有独立工具、真正重叠和完整代理识别条件下也必然不可能识别。

**媒介—结果共同原因**：`RANDOMIZED_MEDIATOR_CONFOUNDED`处理A由独立R决定，真实总处理效果1仍能由观察总体回归1恢复。但M与Y共享未测U，回归条件媒介系数升为**3/2**、条件直达系数变为**−1/2**，两者代数和仍1；真实直接0、真正媒介1。随机处理A保证总因果关联的此项有限外生性，不自动保证中介M与结果Y之间不存在共同原因，因此路径的真实直接/间接分解错误。

**媒介测量误差**：`RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR`真M产生所有Y处理效应，然而只看W=M+E_W而非M，所得媒介OLS回归斜率为1/2，假直达路径为1/2；真实直接0、真实中介1。虽然观察OLS总效应仍1，未测量真媒介的误差使因果路径分解失败。两个潜在U指标Z1/Z2在本世界不是测量M的误差修正工具，不可不经新假设就用它们纠正这项偏差。

本研究不推断实际心理构念单次指标的因果解释，亦没有将人工oracle效应当作观察可识别量。它只严格展示完全有限人工因果路径的条件性识别边界。

## CI及完整原科研证据归档

[可运行Python源程序](r232_exact_structural_mediation.py) · [1024条完整原外生来源CSV](R232_ALL_1024_ORIGINAL_SEM_EXOGENOUS_SOURCES.csv) · [八世界Fraction结果JSON](R232_EXACT_RESULTS.json) · [来源SHA256机器验收](R232_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39828613170](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39828613170) 总体completed/success，Python3.11与3.12实际日志各 `Ran 60 tests`、`OK`，合计120真实测试执行通过。第三归档作业实际生成1024来源，按每世界128条总概率和、完整来源唯一性、两世界全部可见联合概率相同与真实干预不同、因果路径错归因、SHA256等进行独立校验，并真正永久提交机器人归档[fc2bdfb6](https://github.com/edwardsage419/Psychohistory-Research/commit/fc2bdfb62c6164c400a1d364ee6dc75baea45d54)。

原完整来源CSV SHA256 `86add6aeacc8c4b34bdc7d82738fb0382e1e2e627ef31bb30a5d2ac9ada1d38f`；结果JSON SHA256 `7924759a925e4556ddef75b1161952ce47b98d8d8205a149ddcca246eba6730f`。

科学范围仅人工有限E1，新增真人E2=0、历史E3=0。R073/PESEN v0.1保持冻结。下一原239目录 `10-007 Measurement Invariance`，拟R233；坚持先完成全部R，再统一分类与模型熔炼。
