# R159 双重继承理论｜48组人工文化模仿与多数偏向传播的精确有界研究

2026-10-21。原目录 **P1/07-001 Dual Inheritance Theory**。**CLOSED_BOUNDED_E1**。本次从双重继承研究中分离出单一文化频率传播机制：只讨论人工特征A出现频率的纯数学传递，**没有模拟基因遗传与文化遗传相互作用、家庭传播、群体选择或真实文化行为**。

**一手书目及原刊核查：** [Cavalli-Sforza与Feldman1981原书出版方](https://www.jstor.org/stable/j.ctvx5wbt8)、[Boyd与Richerson1985芝加哥大学出版社原书和目录](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html)、[Henrich与Boyd1998原期刊摘要](https://www.sciencedirect.com/science/article/pii/S109051389800018X)。这些原书全文及1998作者原始模型没有重算，科研报告明确界定其为项目自建的三样本多数复制机制。

**冻结设计与结果：** 4种初始人工文化频率p0×4种多数模仿份额h×3种对称重置率u，共48组，每组7期。三名独立示范者中至少两人携带A的概率\(C(p)=3p^2-2p^3\)，人工更新为\(p_{t+1}=(1-u)[(1-h)p+hC(p)]+u/2\)。**直接Fraction三次多项式迭代与独立枚举8种三示范者组合的路线全部严格吻合**，完整保存336个文化频率时点及同数目的三人多数概率。

**理论反例：** p=1/4时多数模仿概率恰为5/32，小于原始频率；p=3/4时恰为27/32，大于原始频率。在不发生重置且h>0时，初始少数文化特征会在本人工模型中逐期降低，占多数的特征逐期增加。h=0且u>0时有精确闭式\(p_t=1/2+(1-u)^t(p_0-1/2)\)。当p0=1/2时，无论h、u取何值，所有时点都恒为1/2；即便完整观察这一条频率路径，也不能在此特例中识别参数。对称重置可以打破p=0或p=1的吸收状态。

**两轮远程验证与完整归档：** [初次CI39523466288](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39523466288)与[最终固定哈希CI39523555967](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39523555967)均success。Python3.11、3.12每轮各73项真实测试，最终独立归档再次执行73项，共365次真实单测、73种不同方法、0失败，固定四项SHA256均匹配。[归档提交df5dcfc](https://github.com/edwardsage419/Psychohistory-Research/commit/df5dcfc7a0f86b0ce46eeb7068ab94688bb2f384)已将完整JSON及源码/测试ZIP永久存入main。

材料：[计算前冻结协议](../../protocols/R159_BOYD_RICHERSON_CAVALLI_FELDMAN_HENRICH_48_TRANSMISSION_PRESCORE_FREEZE_2026-10-21.md)（提交ddb4d36）｜[科学报告与边界](R159_SCIENTIFIC_REPORT_2026-10-21.md)｜[完整344545字节JSON](R159_EXACT_RESULTS.json)｜[程序](r159_cultural_transmission_exact.py)｜[测试](test_r159_cultural_transmission_exact.py)｜[标准库源程序ZIP](R159_Cultural_Majority_48_Worlds_73_Tests.zip)｜[机器验收收据](R159_FINAL_MACHINE_ACCEPTANCE.json)。

四项SHA256：
* 程序 `06e79227a73b802806fbd7a0bb3bd6dc33e3f994a8403c14fd8a06c58fdc8aeb`
* 测试 `e3c9318dc0194d0e2c7f96a8f8e34c7c116797885ca0c6a9371b72873b5d6216`
* JSON `618d975c379eefcc0929efbf20218a78832684abd5772ac5decf2e61415fdb7e`
* ZIP `504ac3f978fee5b93f17af3fbacf0e0360d54dd6bb2518303794529295934363`

复算：进入 `research/R159` 运行 `python r159_cultural_transmission_exact.py > R159_EXACT_RESULTS.json`，再运行 `python -m unittest -q test_r159_cultural_transmission_exact.py`，无需第三方包。

本次新增E2=0、E3=0；R073和PESEN v0.1仍保持FROZEN。原目录下一项是 **R160 P2/07-002 Gene Culture Coevolution**。继续先完成既定全部R系列，再分类归纳，最后开始模型熔炼。
