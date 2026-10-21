# R167 文化群体选择｜72组人工群体内部与群体之间的精确分解

日期：2026年10月21日。原目录 **P2 / 07-009 Cultural Group Selection**。正式 **CLOSED_BOUNDED_E1**，只结题于本项目原创的两组人工文化频率与群体权重数学演算。模型中的A/B符号及两个群体均无真实人物、地区或社会类别含义。

**一手原文核查：** [Boyd与Richerson2002](https://doi.org/10.1006/jtbi.2001.2515)在结构化群体中研究有利于群体的规范传播；[Henrich2004](https://doi.org/10.1016/S0167-2681%2803%2900094-5)讨论文化学习与群体间竞争对大规模合作的可能作用；[Price1970](https://doi.org/10.1038/227520a0)提出选择与协方差数学分析。原著包含复杂的个体模仿、组织与合作机制，本阶段仅核对出版方摘要和原始文献记录，**没有重建原作者模型、真实合作数据或因果证据**。详情见[正式科学报告](R167_SCIENTIFIC_REPORT_2026-10-21.md)。

**事前冻结72组：** 四种低高组人工A频率起点×两种初始高组权重×三种组内频率变化系数δ×三种组间权重系数κ，共72组，各运行t0至t3四个状态。人工组内更新\(p'_g=p_g-\delta p_g(1-p_g)\)，人工群体权重更新\(w'_g=w_g(1+\kappa p_g)/\sum_iw_i(1+\kappa p_i)\)。两套完全精确的Fraction算法分别使用直接组权重归一化与独立两群体协方差恒等式计算，全部72组完整频率轨迹、权重轨迹和分解数值完全匹配。

**事先指定的聚合反转：** 起点两组权重各1/2，低组A占1/4，高组A占3/4。设δ=1/4与κ=2之后，两组各自A频率分别降至13/64及45/64。按原始群体权重计算，组内变化贡献为**−3/64**；更高A比例的群体被人工赋予更快的权重增长，组间贡献为**+1/16=+4/64**，因此总体A反而从1/2升至**33/64**，净增**1/64**。这是具体的Simpson式聚合反转数学案例，完全不能由此声称现实中的某种行为符合群体利益，也不能证明现实文化群体选择的因果存在。

另有数学控制：κ=0时群体权重不变、组间贡献为0；δ=0时组内频率不变但总体仍可随组间权重变化；当两组A频率相同时组间贡献必为0。相关结果均只在项目假设内成立。

**验证及永久存档：** [首轮GitHub Actions 39534151899](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39534151899)与[最终固定SHA256、归档轮39534227555](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39534227555)均成功；Python3.11/3.12各跑两轮103项真实测试，独立归档再跑103项，合计**515次执行、103种不同测试方法、0失败**。全部JSON和源码测试ZIP永久入库：[提交1925c01](https://github.com/edwardsage419/Psychohistory-Research/commit/1925c0144381562189d440a7794787112aa396cd)。

研究文件：[计算前冻结协议](../../protocols/R167_CULTURAL_GROUP_SELECTION_72_TWO_GROUP_PRICE_COVARIANCE_PRESCORE_FREEZE_2026-10-21.md)（提交a7ba75f）｜[科学报告](R167_SCIENTIFIC_REPORT_2026-10-21.md)｜[程序](r167_cultural_group_covariance_exact.py)｜[103项测试](test_r167_cultural_group_covariance_exact.py)｜[全量JSON](R167_EXACT_RESULTS.json)｜[原生源码ZIP](R167_Cultural_Group_72_Worlds_103_Tests.zip)｜[机器验收](R167_FINAL_MACHINE_ACCEPTANCE.json)。

固定SHA256：
* 源码 `bf005a409c97045c0beb2ca88ee652ca08978ac01d32a8e004b22805cfad8ae6`
* 测试 `88394c087e33ebd816b39077814b39ec78f403a2f7004ec45fca3e3a0e902561`
* JSON `118d8f8d37832777e265205af3f4d05811bf543656c46f2e24873c9ae93a839a`
* ZIP `71209080b55f1fbcb9e4d0365635d6ec5af2c2ceb2633097ef4e6ab7ce5116f6`

独立复算：进入 `research/R167` 运行 `python r167_cultural_group_covariance_exact.py > R167_EXACT_RESULTS.json` 和 `python -m unittest -q test_r167_cultural_group_covariance_exact.py`，只依赖Python标准库。

本阶段新增E2真人独立预测=0、E3外部历史预测=0；R073及PESEN v0.1继续冻结。下一原目录为 **R168 P1 / 07-010 Cumulative Cultural Evolution（文化累积与棘轮效应）**。研究顺序仍为先全部既定R模型，再统一归纳分类，最后熔炼。
