# R226 选择与社会影响：两对完整观察等价、潜在同质性与随机信号反例，人工E1

日期：2026-10-22。原始239目录真实条目 **09-017 Selection versus Influence Identification（P0）**。科研状态限定 **CLOSED_BOUNDED_E1_ARTIFICIAL_NETWORK_SELECTION_INFLUENCE**，CI元数据不一致另有明确保留。数据全部为构建的16状态人工外生分布，未使用任何真实参与者或历史人物行为。

## 来源背景、协议和科研方法

参考 Shalizi & Thomas (2011), *Homophily and Contagion Are Generically Confounded in Observational Social Network Studies*, DOI https://doi.org/10.1177/0049124111404820；Aral, Muchnik & Sundararajan (2009), *Distinguishing influence-based contagion from homophily-driven diffusion in dynamic networks*, DOI https://doi.org/10.1073/pnas.0908800106；Eckles, Kizilcec & Bakshy (2016), *Estimating peer effects in networks with peer encouragement designs*, DOI https://doi.org/10.1073/pnas.1511201113。上述研究分别提示观察性网络中的共同混杂、同质连接形成机制和随机鼓励识别条件。本文模型是独立人工有限检验；没有复现Aral等的2700万级真实用户动态研究，也没有运行2016年真实社交网络随机化试验或遵从性估计。

固定[计算前协议](../../protocols/R226_SELECTION_INFLUENCE_8_WORLDS_128_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-22.md)先提交 [e86adecc](https://github.com/edwardsage419/Psychohistory-Research/commit/e86adecc5745ba5b7bafb6eda5511838418df00a)，之后才创建Python和CI。各世界四个独立Bernoulli(1/2)外生源U,V,R,Q，全部16个组合、每条1/16；八世界128原来源。可观测四元组包含是否连边E、发送者A的前期行为、接收者B的前期行为、接收者B下一期行为。干预对象是边形成之后的发送者公开行为A0，保持所有原潜在特征与既有边固定，以16全部原源求受控B下一期改变，禁止把潜在源给观察估计器使用。

完整观测联合P(E,A0,B0,B1)由16原来源分别枚举；独立积分算法消去无关Q，只用八种U/V/R状态及各1/8积分，全部四元组概率逐状态严格一致。两个真因果oracle均经原来源逐状态和独立结构真公式验算。

## 人工八世界的数学结果

| 冻结世界 | 观察已成边同伴关联 | 已成边异行为比例 | 真总体do(A0)同伴效果 | 真已成边效果 |
|---|---:|---:|---:|---:|
| PEER_COPY | 1 | 1/2 | 1 | 1 |
| SHARED_LATENT_SHOCK | 1 | 1/2 | 0 | 0 |
| HOMOPHILY_ONLY | 1 | 0 | 0 | 0 |
| HOMOPHILY_WITH_COPY | 1 | 0 | 1/2 | 1 |
| RANDOMIZED_PEER_COPY | 1 | 1/2 | 1 | 1 |
| RANDOMIZED_NO_COPY | 0 | 1/2 | 0 | 0 |
| RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK | 1 | 1/2 | 1/2 | 1 |
| ANTI_PEER_COPY | −1 | 1/2 | −1 | −1 |

**第一组强反例**：PEER_COPY中接收者在下一期真正模仿发送者A0；SHARED_LATENT_SHOCK中下一期行为只由同一个潜在U引起而与do(A0)完全无关。两个世界的**完整联合观察概率P(E,A0,B0,B1)逐状态精确相同**，观察条件关联均1，且已有边中初始双方行为不同的比例仍1/2，表明仅有时序加上实际可观察不一致，并不足以排除共同潜在原因。真实因果效果一为1、一为0。

**第二组强反例**：HOMOPHILY_ONLY依共同潜在匹配U=V连边并让接收者延续本人行为；HOMOPHILY_WITH_COPY对已连边真正设置模仿，未连边时保持本人行为。由于可连边的实际原来源恰好A0=B0，两世界的**完整P(E,A0,B0,B1)亦完全相同**。已成边条件观察同伴差均1，真已成边受控模仿效果却分别为0和1。总体真效果分别0和1/2。这一反例在已观察网络中欠缺连边之后改变同伴行为的独立支持。

`RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK`即使边形成仍按U=V挑选，给发送者的公开行动外加独立R后，已有边中A0≠B0的概率恢复1/2，并且实际观察联系组效果1与该特定人工随机干预下的真实受控效果1相同。此实验仅证明固定构造中外生行动能够分辨这些机制，现实试验仍须独立核实随机化、干预稳定性、排除条件、溢出与网络缺失。ANTI_PEER_COPY给出负向因果和负向观察差，为方向假设提供反例。

## CI与永久完整原来源

* [原生程序](r226_exact_selection_vs_influence.py)；[八世界128原来源](R226_ALL_128_ORIGINAL_SELECTION_INFLUENCE_ATOMS.csv)；[完整结果JSON](R226_EXACT_RESULTS.json)；[SHA机读验收](R226_FINAL_MACHINE_ACCEPTANCE.json)。
* [GitHub Actions run39792729144](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39792729144)：Python3.11与3.12的**真实逐作业日志**分别显示`Ran 61 tests`、`OK`，总计122次运行通过。第三完整来源作业的真实日志显示 `R226_ALL_128_SOURCE_TWO_COMPLETE_OBSERVATIONAL_ALIAS_PAIRS_VERIFIED`，同时记录3份CSV/JSON机器源文件的真实Git commit并push到main。
* GitHub机器人永久来源提交 [f90aa32b](https://github.com/edwardsage419/Psychohistory-Research/commit/f90aa32bbc3e85eeda00b2713509af668d74da3d)。原文件SHA256：来源 `f5f012fa36b31ee71b8e5f409585a5ddf4d3146a61f5c54ad6f67a6cb05cd572`；结果 `39b2c73c38b654d0f3fe42158536d93f6f038fc0f2b94d4e0872af8147a165d0`。
* **GitHub元数据冲突审计**：本次复核时，run endpoint仍显示`status=queued, conclusion=null`，jobs API亦显示三个job的`queued/null`；这与实际已写入时间戳的两份成功测试日志、原来源门槛成功日志、真实main归档提交相矛盾。应如实保留此元数据不一致，不能笼统记三作业API字段均为success，也不能将实际日志通过误称为run conclusion=success。它属于平台元数据来源一致性问题，与完整有限数学等式是否成立须区分。未来如果接口状态变化，应另行补录更新时点和新状态，不静默覆盖本段。

本研究仅限人工E1小型二元单边模型，未恢复多主体相互反馈、真实网络形成序列、动态匹配一般性或原作者经验数字。新增真人E2=0、真实历史E3=0。R073和PESEN v0.1冻结。下一实际原239目录条目为 **10-001 Classical Test Theory**，拟R227。继续逐项完成所有原R研究，随后统一分类，最后熔炼。
