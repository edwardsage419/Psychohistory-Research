# R153 空间相互作用模型｜60组合成 OD 双重约束与独立求解验证

2026-10-20。原候选目录 **P2 / 06-011 Spatial Interaction Models**。**CLOSED_BOUNDED_E1**。原始研究对象为项目编制的2×2起点与终点流量模型，未读取原作者完整论文/书籍正文，也未使用真实人口、旅行或零售迁移数据，**没有新增 E2、E3 证据**。R073和PESEN v0.1均继续冻结。

**理论模型与来源**：一手出版资料核对 [Wilson (1970), *Entropy in Urban and Regional Modelling*](https://www.routledge.com/Entropy-in-Urban-and-Regional-Modelling-Routledge-Revivals/Wilson/p/book/9780415696319)、[Huff (1964), *Defining and Estimating a Trading Area*](https://journals.sagepub.com/doi/full/10.1177/002224296402800307)、[Fotheringham (1983), *The Theory of Competing Destinations*](https://journals.sagepub.com/doi/10.1177/0308518X8301500103)。本研究仅采用受这些研究领域启发的自建加权流量约束模型，未声称复现作者原有模型拟合或行为估计。

**冻结设计**：三组迁出预算×四组迁入预算×五组路线权重，共60种独立命名且事前确定的人工场景。各场景分别用单侧约束路由、双侧约束的迭代比例拟合IPF、独立二元边际标量交叉积根求解计算。额外使用标准库Fraction进行等权核的精确基准；结构性零流量的可行区间和不可行情形也作独立检验。

**主要结论**：60个场景中，单侧约束有54个无法满足指定迁入总量；双侧约束60个均满足两侧边际，所有单格的独立求解器最大差距7.417×10⁻¹¹。等权核基准起点(3,5)、终点(2,6)时，单侧模型两行分别(1.5,1.5)、(2.5,2.5)，终点合计(4,4)；双侧模型两行分别(0.75,2.25)、(1.25,3.75)，准确满足(2,6)。对权重施加独立行/列正倍数不改变双约束最优流量，显示行列缩放与边际数据之间的不可识别性。结构性零权重的唯一可行表((0,3),(4,1))与不可行表均已作严格检验。

**复验**：[GitHub Actions run 39434054859](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39434054859)成功。Python3.11、3.12分别运行74项不同单元测试，第三归档任务又运行74项且完成四项固定SHA256验收，共222次单测执行、74种不同测试、0失败。[源码与完整结果归档提交9aaeccf](https://github.com/edwardsage419/Psychohistory-Research/commit/9aaeccf4290eb6b2d0badda85292cc7a199c57d4)。

**完整材料**：[计算前协议](../../protocols/R153_SPATIAL_INTERACTION_DOUBLY_CONSTRAINED_PRESCORE_FREEZE_2026-10-20.md)（预冻结提交99183f2）｜[科学报告](R153_SCIENTIFIC_REPORT_2026-10-20.md)｜[结果JSON](R153_EXACT_RESULTS.json)｜[源码与74测试的永久ZIP](R153_Spatial_Interaction_60_Cases_74_Tests.zip)｜[机器验收收据](R153_FINAL_MACHINE_ACCEPTANCE.json)。

SHA256：源码 `ed60ed3952c3e75efd046456e238f260082a839739e81b5cf87deec4c9185d97`；单测 `3b9f0d49d5930fd4c353fc4b72ec1781c42695a084f49edd623391323c379ca7`；JSON `9b2002c0aea89401660bd4b117b4dfcdec9c844479c7cd61e9e32b8fb5bc0f24`；ZIP `d7f5284aeabf3cc6e67317e3e38c67722c2b4d143197b235867401756252dd57`。在 `research/R153` 执行 `python r153_spatial_od.py > R153_EXACT_RESULTS.json`、`python -m unittest -q test_r153_spatial_od.py` 可完整复验；无第三方包依赖，ZIP使用标准库ZIP_LZMA。

下一原始目录：**R154 P1 / 06-012 Stock and Flow System Dynamics（系统动力学存量流量）**。先全部R系列，再归纳分类，最后熔炼。
