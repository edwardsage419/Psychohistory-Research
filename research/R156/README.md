# R156 内生增长模型｜96组AK和收益递减资本轨迹、118项测试

2026-10-21。原既定候选目录 **P2 / 06-014 Endogenous Growth Models**；本阶段 **CLOSED_BOUNDED_E1**，专门研究项目自建的简约AK增长与收益递减对照，不涉及真实国家资本数据、技术研发市场均衡或原作者实证重算。

一手学术来源仅核对正式出版方论文记录：[Romer 1986](https://doi.org/10.1086/261420)、[Romer 1990](https://doi.org/10.1086/261725)、[Rebelo 1991](https://doi.org/10.1086/261764)。原全文和作者源数据尚未获取，不能将本项目方程当作上述论文的精确版本或实证预测。详细学术边界见[科学报告](R156_SCIENTIFIC_REPORT_2026-10-21.md)。

**冻结模型：** k(0)取1、4、9，储蓄率s取0.1、0.2、0.4、0.6，折旧δ取0、0.1、0.2、0.4，产出资本指数α取1（AK）及0.5（收益递减），共 **96种预先确定的完整场景**。使用解析闭式和独立RK4直接积分capital方程\(dk/dt=sk^\alpha-\delta k\)，保存0、1、5、10时点全部存量、产出及净流量。96组全部通过，最大RK4绝对误差 **3.3651×10⁻¹¹**，且资本量均正。

**明确机制差异：** AK增长取决于净比率s−δ，固定参数下呈指数轨迹；α=0.5且δ>0时有稳定资本量(s/δ)²。以k0=1、s=.2、δ=.1为例，t=10的AK资本2.718281828459，对应递减收益模型1.941756802321，后者稳定资本值为4。AK中(s,δ)=(.2,.1)与(.4,.3)会产生完全相同的资本轨迹，说明仅有资本存量时间序列无法分开识别储蓄与折旧。大步长Euler在一个人工场景产生约−5的负资本，连续精确解仍为0.00247875。

**真实远程复验：** [CI初轮39520340288](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39520340288) Python3.11、3.12各118项测试全部成功；[四项固定哈希复验及归档CI39520425232](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39520425232)相同双环境各118项，第三归档任务又执行118项并验四SHA256，合计590次真实单测执行、118种不同测试、0失败。完整JSON和源程序、测试ZIP已永久归档在[提交4862754](https://github.com/edwardsage419/Psychohistory-Research/commit/4862754b16894fbbc7e4f5e0bdb629875fdb4358)。

**材料：** [计算前冻结协议](../../protocols/R156_REBELO1991_ROMER1986_1990_AK_CONCAVE_96_TRAJECTORIES_PRESCORE_FREEZE_2026-10-21.md)（提交ed806d1）｜[完整科学报告](R156_SCIENTIFIC_REPORT_2026-10-21.md)｜[103608字节完整JSON](R156_EXACT_RESULTS.json)｜[源程序与118项测试ZIP](R156_Growth_96_Worlds_118_Tests.zip)｜[正式机器验收收据](R156_FINAL_MACHINE_ACCEPTANCE.json)。

SHA256四项：
* 程序 `4980bbaad13d2162503aa05ac05829035a6d891144913f7db100e33abc1eda0d`
* 测试 `87ff03e0d15fe1c2edcddc5081488f58f3730fb0fc9df5039984721d32d7cd6a`
* 完整结果 `bc80a9bac0b7c6d26c6e5c829c761f482a2ba1a9803a097bccd3735aeaf0db88`
* 完整ZIP `f7b7ddb26215b76cd5b60a4734e4b492206928141356e35768c7eb7ab4366a45`

在 `research/R156` 中运行 `python r156_growth_pair.py > R156_EXACT_RESULTS.json` 及 `python -m unittest -q test_r156_growth_pair.py` 即可不依赖第三方包复验。

本阶段新增E2=0、E3=0；R073/PESEN v0.1继续FROZEN。下一个正式研究对象是原目录 **R157 P2/06-015 Structural Demographic Theory**。严格先全部R系列，之后分类，再进行熔炼。
