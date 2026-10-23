# R246 泊松过程与Hawkes过程：九人工四格Bernoulli事件世界、4608完整来源与自激误判边界

日期2026-10-23（Asia/Taipei）。原239目录`11-006 Poisson and Hawkes Processes`（P1）。**科学资格仅 `CLOSED_BOUNDED_E1_FINITE_BERNOULLI_EVENT_SELF_EXCITATION_SURROGATE`**，不是连续时间Poisson/Hawkes真实点过程复现。全部原数据为人工四格、每格最多1事件的Bernoulli概率代理，新增真人E2=0、历史E3=0。

## 原论文与严格的非复现声明

Hawkes, Alan G. (1971), [*Spectra of some self-exciting and mutually exciting point processes*](https://doi.org/10.1093/biomet/58.1.83), *Biometrika* 58(1):83–90，提出自激点过程机制及谱与协方差研究。标准Poisson过程章节参见MIT 6.262 *Discrete Stochastic Processes, Poisson Processes* [官方课程说明](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/)。本R虽然借鉴事件发生后提高未来发生概率的思想，但**只计算四个二值时间格，不能容纳单格≥2真实事件、随机连续事件时间、泊松增量分布、Hawkes真实强度或积分似然**。对任意正速率λ和正格宽Δ，真实Poisson单格多事件概率`P(N(Δ)≥2)=1−e^(−λΔ)(1+λΔ)>0`，而本R强行至多一个、概率为0。两者分布类型在这个最简单层面就不等价，不能仅凭过程名称宣布真实Hawkes被精确模拟。

[完整先行冻结协议](../../protocols/R246_POISSON_HAWKES_DISCRETE_SURROGATE_9_WORLDS_4608_ORIGINAL_EVENT_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于代码、CI和来源评分独立提交[7e3c7eff](https://github.com/edwardsage419/Psychohistory-Research/commit/7e3c7efff3da87d3e1cde8cc5db813c1c8650707)。九机制、全部外生来源、独立概率积分和首两格协方差预测值均先冻结且未事后更改。

## 源空间、两独立计算路径与人工事件解释

每world完整九独立fair外生位`U,R11,R12,...,R41,R42`，每格两bit组成均匀值R∈{0,1,2,3}。九world共**4608条原完整外生源**，每world512且每条权重1/512。源保存U、每格随机2bit、实际观察Y1…Y4、观察累计计数N1…N4、人工oracle冻结条件Bernoulli hazard p1…p4和人工真正隐藏事件H1…H4。观察证据严格只允许使用Y1…Y4，不泄露U、p或真实H；这些隐藏来源仅用来核验人工生成机制。

第一路线按冻结每一步`Y_k=1{R_k<4p_k(Y历史,U)}`，COMMON_SHOCK特殊复用第一个R，一步一步完整模拟512源并边缘化全部四元事件观察路径16格概率。第二路线**不调用source生成器或阈值模拟函数**，独立对每条四元Y路径计算四项条件Bernoulli似然乘积`Π_k p_k^{Y_k}(1−p_k)^{1−Y_k}`，隐藏U类型世界对两个条件乘积按1/2加权；共同shock只允许0000与1111各1/2。完整观察16格PMF全部逐world严格Fraction相同，四格均值和累计均值及第1、2格协方差从联合源积分得到。

## 九人工机制结果

| 人工机制 | 第一格P(Y1=1) | 第二格P(Y2=1) | Cov(Y1,Y2) | P(Y2=1｜Y1=1) | P(Y2=1｜Y1=0) |
|---|---:|---:|---:|---:|---:|
| IID_LOW | 1/4 | 1/4 | 0 | 1/4 | 1/4 |
| IID_HIGH | 3/4 | 3/4 | 0 | 3/4 | 3/4 |
| SELF_EXCITING_LAG1 | 1/4 | 3/8 | 3/32 | 3/4 | 1/4 |
| REFRACTORY_LAG1 | 1/2 | 3/8 | −1/16 | 1/4 | 1/2 |
| STATIC_LATENT_RATE_MIXTURE | 1/2 | 1/2 | 1/16 | 5/8 | 3/8 |
| ALTERNATING_EXOGENOUS_RATE | 1/4 | 3/4 | 0 | 3/4 | 3/4 |
| COMMON_SHOCK_ALL_BINS | 1/2 | 1/2 | 1/4 | 1 | 0 |
| STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS | 1/4 | 3/8 | 3/32 | 3/4 | 1/4 |
| SELF_EXCITING_TWO_LAG | 1/4 | 5/16 | 3/64 | 1/2 | 1/4 |

**人工直接一格自激：** SELF_EXCITING_LAG1从首次P(Y1=1)=1/4开始，后一格条件概率p=1/4+Y_{k−1}/2。当上一格有人工事件，下一格条件率增到3/4；上一格无人工事件则1/4，故第二格整体边际3/8且前两格事件指示协方差3/32。它是预先编码在生成器里的局部干预结构，仅证明此四格模型内部自激机制如何导致可见聚集，**不是历史人群事件的因果识别结果**。

**未观测异质性也能制造正相关而没有自激：** STATIC_LATENT_RATE_MIXTURE在U=0世界每格独立p=3/4，在U=1世界每格独立p=1/4，U在整个四格中保持不变。每个个体给定U后真实条件事件互不影响，但观察混合后`Cov(Y1,Y2)=1/16>0`，`P(Y2=1|Y1=1)=5/8`、`P(Y2=1|Y1=0)=3/8`。如果只根据过去发生过事件之后未来事件更常见，就宣称已经识别“事件造成事件”，会把稳定未观察类别造成的选择/后验信息误认成自激。**这两个世界的完整联合统计并非完全一样**；本R提出的是“正相关证据本身不足以识别机制”，而不是“在任意完整统计上自激和混合严格等价”。

**同一事件簇统计还能来自外部共同冲击。** COMMON_SHOCK_ALL_BINS把四格结果都绑定到同一个首格R，完整可见序列只有0000或1111，各1/2。这造成`Cov(Y1,Y2)=1/4`、`P(Y2=1|Y1=1)=1`与`P(Y2=1|Y1=0)=0`，但人工生成器中并没有前一事件提高下一事件hazard的因果箭头，只有外生共源。这一世界可通过完整四元路径与短记忆自激world区分。

**两格记忆与近期时间变化：** SELF_EXCITING_TWO_LAG的第三格概率`p3=1/4+Y2/4+Y1/4`，因此固定近期Y2=0，当更早Y1=1时`P(Y3=1|Y2=0,Y1=1)=1/2`，当Y1=0则1/4。最近一格不够完全预测该有限人工过程。ALTERNATING_EXOGENOUS_RATE的第二格事件率从首次1/4升至3/4，但各格完全由事前日历概率决定、相互独立，Cov=0；它不是自激。REFRACTORY_LAG1显式让此前事件令下一格率下降，Cov=−1/16，也不同于可见聚集与多种正相关机制。

**观察层全路径相同仍不证明真事件存在。** SELF_EXCITING_LAG1与STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS在每条相同九bit来源的全部Y1…Y4 **逐位完全相同**、观察累计N和完整联合统计也完全一样。但第二世界真实隐藏H1…H4全0，观测设备按前者人工条件率输出伪事件。仅在允许传感器产生伪事件、未被独立验真的假设下，这种人工非识别存在；若具有可信事件记录与独立验证则别名被排除。切勿把E1表述成现实事件是否存在的结论。

## GitHub Actions 实验执行与来源审计

[原生Fraction Python源码](r246_exact_binned_poisson_hawkes_surrogate.py) · [九世界全部4608原人工事件source CSV](R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv) · [完整四元路径/均值/条件/协方差JSON](R246_EXACT_RESULTS.json) · [SHA256最终机器凭证](R246_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39891833189](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39891833189)总体completed/success，三job均completed/success；Python3.11和Python3.12实际各`Ran 84 tests`、`OK`，合计**168次真实单测通过**。第三独立源审计实际读取4608原source，验证九world各512九bit唯一外生类型、总质量归一、观察累计N和Y一致、完整四元Bernoulli路径联合归一、两路线逐路径相符、人工hazard正负协方差、混合U条件差、二格记忆、伪事件同观测别名，以及原CSV和结果JSON SHA256，实际日志输出`R246_ALL_4608_BERNOULLI_EVENT_SOURCE_LAWS_NOT_ACTUAL_POISSON_HAWKES_VERIFIED`。原CSV/结果JSON/机器SHA机器人永久归档main提交[8ebea75a](https://github.com/edwardsage419/Psychohistory-Research/commit/8ebea75a9b5aaa70d330466a2c42a60306b4db43)。

原CSV SHA256 `3ca6324f22fa75d8397c836b414a52fcf2ffc3a1db36cc749cfd4a42117c7474`；结果JSON SHA256 `39e5e46f04608e243e861d4945ea186112bad8843acef06411f956ae2af277ee`。

正式科学资格仅`CLOSED_BOUNDED_E1_FINITE_BERNOULLI_EVENT_SELF_EXCITATION_SURROGATE`，不得宣称真正连续Poisson、真正Hawkes原点过程已拟合/复算、真实事件因果激发或跨实验预测成立。新增真人E2=0、真实历史E3=0，R073及PESEN v0.1冻结。下一原239目录`11-007 Branching Processes`（P1）拟R247。先完成全部R后统一归纳分类，最后熔炼。
