# R287 科学报告：原239目录01-001 期望效用理论：共同后果与独立性

日期2026-10-23 Asia/Taipei。由用户所定研究顺序推动：原239项全部学习→统一归纳分类→最后原创模型熔炼。**本项是原目录P1补缺，而不是新增第240/241/242项原候选**。始终区分外部文献理论线索、人工模型数学与真实人类样本的实证验证。

[先行事前冻结](../../protocols/R287_EXPECTED_UTILITY_3_PROFILES_3_COMMON_MIXTURES_2304_FULL_SOURCES_PRESCORE_FREEZE_2026-10-23.md) GitHub提交[52421136](https://github.com/edwardsage419/Psychohistory-Research/commit/524211361d5180624d4350559d53112de31139ab)，先于完整结果生成。

## 模型、原理与反例

核心原始文献线索为von Neumann & Morgenstern (1944), *Theory of Games and Economic Behavior*，Princeton University Press；仅验证期望效用对共同后果混合的一个有限公理性质，**不声称读取或复现了整本书的形式化表征定理，也不把公理当作真实人类总会遵循的事实**。

候选彩票A一定得到4，B独立投币获0或9。共同后果C为1，以λ∈{1/4,1/2,3/4}概率同时替换双方为C。三个人工效用轮廓：线性u(0,1,4,9)=(0,1,4,9)，平方根轮廓(0,1,2,3)，饱和轮廓(0,1,3/2,2)。四次机会的8bit完整来源M1X1...M4X4可穷举256配置/world，三效用×三共同后果=9world、2304原配置，每源质量[(λ)^m(1−λ)^(4−m)]×(1/2)^4。注意全部模型**共享同一随机源**，不能将2304解释为2304个人类决定。

EUT导出EU_A=(1−λ)u4+λu1；EU_B=(1−λ)(u0+u9)/2+λu1，差恒为(1−λ)[u4−(u0+u9)/2]，所以正λ且λ<1时同一偏好轮廓绝不反转相对排序。λ=1/2时线性轮廓Δ(A−B)=−1/4而平方根/饱和轮廓均+1/4，表明**效用曲率能改变基础风险排序，但共同后果混合并未违反EUT的独立性**。严格正仿射u' = 3u+7则彩票差变成3Δ，排序不改变；非仿射单调变换不满足这种基数效用等价条件。

枚举每个原来源的两彩票实际收益和四次平均效用，精确Fraction按真source质量加权得到9组合EU，与不调用原随机源的闭式公式完全一致。第三独立程序再次从CSV逐八bit重算来源概率、共同分支一致性、两彩票实际效用及正仿射结论，九world所有来源无择优排除。

**限制：** 无公理心理适用性的直接实验验证、没有完成一般vNM表征定理的全部假设和证明，也未比较现实风险决策数据；E1人工数学而非E2真人或E3历史。

## 验收记录及源保全

全部来源：[R287_ALL_2304_ORIGINAL_COMMON_CONSEQUENCE_SOURCES.csv](R287_ALL_2304_ORIGINAL_COMMON_CONSEQUENCE_SOURCES.csv)，共2304个带机制标签原始数学配置，9个人工世界；[解析和枚举结果JSON](R287_EXACT_EU_RESULTS.json) · [SHA256机器凭证](R287_MACHINE_RECEIPT.json) · [运行源码](r287_exact_expected_utility.py)。原CSV SHA256 `84d8000d0ed2683a77b12a9e47a43d013960b9a95198457beac9aa5acef1d080`，结果JSON SHA256 `660fa58d9607340878228126415bc37e5a6ab268ffb9204b940302e661211d2f`。

[GitHub Actions run39910069650](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910069650)三个作业全部completed/success，Python3.11与3.12各90个**真实运行**的unit test，共180通过；第三独立审计执行[不导入原模型的审核代码](../catalogue_audit/independent_r287_r289_source_audit.py)，直接逐CSV重建所有原来源、精确质量、实际结果、独立数学解析和SHA。所有原CSV/结果JSON/摘要经机器人永久main归档[提交59196ef0](https://github.com/edwardsage419/Psychohistory-Research/commit/59196ef07a62ea8973727c2333c185de1a3be4f2)。

正式研究决定：**CLOSED_BOUNDED_E1_ARTIFICIAL_R287_MODEL_MECHANICS**，原01-001获得一个独立、可复现、仅人工数学范围的主R。未读取真实个体被试的trial-level资料，未实现完整原作者具体实验复现，新增真人E2=0、真实历史E3=0，R073及PESEN v0.1维持冻结。其它早期研究包可能已包含文献介绍，后续避免重复计为独立实验。下一项按照原目录剩余待核队列推进。
