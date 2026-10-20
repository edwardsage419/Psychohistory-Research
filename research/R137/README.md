# R137 网络互惠：2006图上合作规则与有限人口精确固定概率

原239模型目录：**P1 / 05-013 Network Reciprocity**。日期2026-10-20。与R119–R125的传播/同质/随机图学习分开，本研究关注图上捐赠博弈的合作策略是否受到自然选择促进。

真实一手来源：Ohtsuki, Hauert, Lieberman & Nowak (2006) [*A simple rule for the evolution of cooperation on graphs and social networks*, Nature 441:502–505](https://doi.org/10.1038/nature04605)；有限人口检验来源 Chen, McAvoy & Nowak (2016), [*Fixation Probabilities for Any Configuration of Two Strategies on Regular Graphs*, Scientific Reports 6:39181](https://doi.org/10.1038/srep39181)。2006年主论文的b/c>k是弱选择大人口近似；2016年论文援引2007年Taylor、Day、Wild关于有限双可迁图的精确临界值k(N−2)/(N−2k)。

本研究独立构造固定无向简单图，按原论文捐赠博弈收益与适应度F=1+wπ，精确计算单位成本c=1时单个随机位置合作突变体在w=0的一阶固定概率变化。模型实现先死亡后繁殖（DB）、先繁殖后死亡（BD）、以及自体参与的模仿（IM）三种更新方式。单亲来源根据事件发生前的所有参与者收益计算。

**已完成的结果**：环形C5/C6/C7/C8/C9的DB临界b/c分别6、4、10/3、3、14/5，全部与有限公式2(N−2)/(N−4)严格一致；IM相应在C7/C8/C9为22、13、10；这些有限环网络绝不能被直接套用大人口k+2作为精确IM阈值。全部测试的BD结果均未支持合作有利的正梯度。四节点完全图K4无有限DB促合作阈值。直接计算w=1/10000的小强度正负例与导数符号相符。

**复现材料**
- [研究协议，冻结于远端CI前](../../protocols/R137_OHTSUKI_2006_FINITE_WEAK_SELECTION_GRAPH_FIXATION_PROTOCOL_2026-10-20.md)
- [科学报告](R137_OHTSUKI_2006_NETWORK_RECIPROCITY_FINITE_FIXATION_REPORT_2026-10-20.md)
- [Python源码、40项测试、完整结果ZIP](R137_Ohtsuki_2006_Finite_Exact_40_Tests.zip)
- [机读数学结果](R137_EXACT_FINITE_SELECTION_GRADIENT_RESULTS.json)
- [Github Actions工作流](../../.github/workflows/r137-graph-cooperation-finite-40-tests.yml)
- [正式状态](R137_FINAL_ACCEPTANCE_STATUS.json)

解压ZIP后在同一目录运行：`python -m unittest -v test_r137_network_reciprocity_exact.py`，`python r137_network_reciprocity_exact.py`。Python标准库Fraction精确计算，不需要第三方依赖。

范围：没有原作者2006年数值全尺度大随机图复算；没有从人类或动物行为中估计真实b、c或网络；E2新增0、E3新增0。R073和PESEN v0.1继续冻结，既定R全部学习后再分类和熔炼。
